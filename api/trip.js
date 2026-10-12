// Guest trip API. GET /api/trip?t=<token> returns the guest's trip; POST saves pre-trip answers and runs the AI planner.
import { db, json, readBody, loadTrip, planTrip, PACKAGES, OFFERS, priceFor, sendEmail, emailShell, esc, SITE } from './_lib.js';

const clip = (s, n) => (s == null ? null : String(s).trim().slice(0, n) || null);
const num = (v, lo, hi) => { const n = parseInt(v, 10); return Number.isFinite(n) && n >= lo && n <= hi ? n : null; };
const today = () => new Date().toLocaleDateString('en-CA', { timeZone: 'America/Denver' });

export default async function handler(req, res) {
  const token = String(req.query.t || '');
  if (!/^[a-f0-9]{24,64}$/.test(token)) return json(res, 400, { error: 'Invalid link' });
  try {
    const t = await loadTrip(`access_token=eq.${token}`);
    if (!t) return json(res, 404, { error: 'Trip not found' });
    const { trip, home } = t;

    if (req.method === 'GET') {
      const showPlan = ['approved', 'in_stay', 'complete'].includes(trip.status);
      const arrived = today() >= trip.check_in && trip.status !== 'cancelled';
      return json(res, 200, {
        guest_first: String(trip.guest_name).split(/\s+/)[0],
        home: home ? { name: home.name, area: home.area, sleeps: home.sleeps } : null,
        check_in: trip.check_in, check_out: trip.check_out, adults: trip.adults, children: trip.children,
        package: trip.package, package_text: PACKAGES[trip.package], status: trip.status,
        party: t.party.map(({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes }) => ({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes })),
        answers: t.answers ? { dining: (t.answers.raw && t.answers.raw.dining) || null, interests: t.answers.interests, pace: t.answers.pace, groceries: t.answers.groceries, dietary: t.answers.dietary, coffee: t.answers.coffee, arrival_time: t.answers.arrival_time, celebrations: t.answers.celebrations, notes: t.answers.notes } : null,
        itinerary: showPlan ? t.itinerary.map(({ day, start_time, title, details, kind, weather_note, partner }) => ({ day, start_time, title, details, kind, weather_note, place: partner })) : [],
        ready_list: showPlan ? (trip.ready_list || []) : [], offers: showPlan ? (trip.offers || []).map((o) => { const p = priceFor(o.key, trip); return { ...o, pay_cents: p && p.cents > 0 ? p.cents : null }; }) : [], weather: showPlan ? (trip.weather || []) : [],
        host_phone: (process.env.HOST_PHONE || '').trim() || null, requested: (t.tasks || []).filter((k) => k.title.startsWith('Guest requested:')).map((k) => k.title.replace('Guest requested: ', '')),
        stay: arrived && showPlan && home ? { door_code: home.door_code, wifi_name: home.wifi_name, wifi_password: home.wifi_password } : null,
      });
    }

    if (req.method === 'POST' && req.query.action === 'request') {
      const key = String(readBody(req).key || '');
      const offer = OFFERS[key];
      if (!offer || !(trip.offers || []).some((o) => o.key === key)) return json(res, 400, { error: 'Not available' });
      const title = `Guest requested: ${offer.title}`;
      if (!(t.tasks || []).some((k) => k.title === title)) {
        await db.insert('tasks', [{ trip_id: trip.id, title, assignee: 'Casey', due_at: new Date(Date.now() + 864e5).toISOString(), created_by: 'guest', approved: true }]);
        const inbox = (process.env.OWNER_INBOX || '').trim();
        if (inbox) await sendEmail({ to: inbox, subject: `${trip.guest_name} requested: ${offer.title}`, html: emailShell(`<p><strong>${esc(trip.guest_name)}</strong> asked for <strong>${esc(offer.title)}</strong> (${esc(offer.price)}) for ${esc(trip.check_in)}.</p><p>Confirm with the guest and arrange payment.</p><p><a href="${SITE}/admin">Open admin</a></p>`) });
      }
      return json(res, 200, { ok: true });
    }

    if (req.method === 'POST') {
      if (['approved', 'in_stay', 'complete', 'cancelled'].includes(trip.status)) return json(res, 409, { error: 'Your trip is already planned. Reply to our email to change anything.' });
      const b = readBody(req);
      const party = (Array.isArray(b.party) ? b.party : []).slice(0, 16).filter((p) => p && clip(p.name, 60)).map((p) => ({
        trip_id: trip.id, name: clip(p.name, 60), age_group: ['adult', 'teen', 'child'].includes(p.age_group) ? p.age_group : 'adult',
        height_cm: num(p.height_cm, 60, 230), weight_kg: num(p.weight_kg, 10, 200), boot_size: clip(p.boot_size, 12),
        ski_level: clip(p.ski_level, 30), bike_level: clip(p.bike_level, 30), notes: clip(p.notes, 300),
      }));
      if (!party.length) return json(res, 400, { error: 'Please add at least one person.' });
      const a = b.answers || {};
      await db.remove('party_members', `trip_id=eq.${trip.id}`);
      await db.insert('party_members', party);
      await db.upsert('trip_answers', [{
        trip_id: trip.id, interests: (Array.isArray(a.interests) ? a.interests : []).slice(0, 12).map((x) => String(x).slice(0, 40)),
        pace: clip(a.pace, 40), groceries: clip(a.groceries, 2000), dietary: clip(a.dietary, 500), coffee: clip(a.coffee, 200),
        arrival_time: clip(a.arrival_time, 40), celebrations: clip(a.celebrations, 300), notes: clip(a.notes, 1500),
        raw: { ...a, dining: a.dining && typeof a.dining === 'object' ? {
          cuisines: (Array.isArray(a.dining.cuisines) ? a.dining.cuisines : []).slice(0, 10).map((x) => String(x).slice(0, 40)),
          atmosphere: (Array.isArray(a.dining.atmosphere) ? a.dining.atmosphere : []).slice(0, 6).map((x) => String(x).slice(0, 40)),
          budget: clip(a.dining.budget, 10), nights: num(a.dining.nights, 0, 14), notes: clip(a.dining.notes, 400) } : null },
        updated_at: new Date().toISOString(),
      }], 'trip_id');
      await db.update('trips', `id=eq.${trip.id}`, { status: 'planning' });
      const result = await planTrip(trip.id);
      return json(res, 200, { ok: true, ...result });
    }
    return json(res, 405, { error: 'Method not allowed' });
  } catch (e) {
    console.error('trip api', e);
    return json(res, 500, { error: 'Something went wrong. Please try again, or reply to our email.' });
  }
}
