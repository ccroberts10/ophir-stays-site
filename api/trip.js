// Guest trip API. GET /api/trip?t=<token> returns the guest's trip; POST saves pre-trip answers and runs the AI planner.
import { db, json, readBody, loadTrip, planTrip, aiJSON, PACKAGES, OFFERS, priceFor, sendEmail, emailShell, esc, SITE, manualForGuest, menuFor, paidAddons } from './_lib.js';

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
        charges: (await db.select('charges', `trip_id=eq.${trip.id}&status=neq.void&order=created_at.asc`)).map((c) => ({ key: `charge_${c.id}`, title: c.title, note: c.note, cents: c.amount_cents, status: c.status })),
        ask: (await db.select('messages', `trip_id=eq.${trip.id}&subject=eq.Ask%20Ophir&order=created_at.desc&limit=12`)).reverse().map((m) => ({ from: m.direction === 'inbound' ? 'guest' : 'ophir', body: m.body })),
        manual: showPlan && home ? manualForGuest(home.manual) : [],
        menu: trip.status === 'cancelled' ? [] : menuFor(trip, await paidAddons(trip.id)).map((m) => ({ ...m, price: OFFERS[m.key].price })),
        nights: Math.round((new Date(trip.check_out) - new Date(trip.check_in)) / 864e5),
        stay: arrived && showPlan && home ? { door_code: home.door_code, wifi_name: home.wifi_name, wifi_password: home.wifi_password } : null,
      });
    }

    if (req.method === 'POST' && req.query.action === 'ask') {
      if (trip.status === 'cancelled') return json(res, 409, { error: 'This trip is cancelled.' });
      const q = clip(readBody(req).question, 500);
      if (!q) return json(res, 400, { error: 'Please type a question.' });
      const since = new Date(Date.now() - 864e5).toISOString();
      const recent = await db.select('messages', `trip_id=eq.${trip.id}&subject=eq.Ask%20Ophir&direction=eq.inbound&created_at=gte.${since}&select=id`);
      if (recent.length >= 20) return json(res, 429, { error: 'That’s a lot of questions for one day. Text your host and Casey will answer directly.' });
      const history = (await db.select('messages', `trip_id=eq.${trip.id}&subject=eq.Ask%20Ophir&order=created_at.desc&limit=8`)).reverse();
      const restaurants = await db.select('restaurants', 'active=eq.true&order=name').catch(() => []);
      const arrived = today() >= trip.check_in;
      const ctx = {
        today: today(), guest: trip.guest_name, check_in: trip.check_in, check_out: trip.check_out, adults: trip.adults, children: trip.children,
        package: PACKAGES[trip.package] || trip.package,
        home: home ? { name: home.name, area: home.area, beds: home.beds, baths: home.baths, sleeps: home.sleeps, house_notes: home.house_notes, house_manual: manualForGuest(home.manual),
          ...(arrived ? { door_code: home.door_code, wifi_name: home.wifi_name, wifi_password: home.wifi_password } : {}) } : null,
        itinerary: (['approved', 'in_stay', 'complete'].includes(trip.status) ? t.itinerary : []).map(({ day, start_time, title, details }) => ({ day, start_time, title, details })),
        weather: trip.weather || [],
        restaurants: restaurants.map(({ name, cuisine, vibe, price, kid_friendly, notes }) => ({ name, cuisine, vibe, price: price ? '$'.repeat(price) : null, kid_friendly, notes })),
        host_phone: (process.env.HOST_PHONE || '').trim() || null,
      };
      const system = `You are Ask Ophir, the in-app guide for guests of Ophir Stays, a small, locally owned collection of vacation homes in Durango, Colorado, run by Casey Roberts, who has lived in Durango for 23 years.
Answer the guest's question using ONLY the trip context below and general, stable knowledge of Durango. Voice: warm, plain and brief, like a local friend who knows the town. Two to five sentences, under 90 words. No exclamation marks. Never use the word "luxury". No lists unless the guest asks for steps.
Rules:
- House questions (appliances, hot tub, parking, trash, thermostat, codes, check-in, checkout): answer only from house_manual, house_notes and the codes given. If the answer isn't there, say Casey will confirm shortly, and set notify_casey true. Never guess about the house.
- Door code and Wi-Fi exist in the context only on or after arrival day. Before that, say they appear on this page on arrival day.
- Restaurants: recommend only from the restaurants list. If it's empty or nothing fits, say Casey will suggest a spot and set notify_casey true.
- Bookings, changes, refunds, prices not in the context, early check-in, late checkout, extra guests, pets: never promise anything. Say Casey will confirm, and set notify_casey true.
- Anything unsafe or broken (no heat, a leak, lockout, a smoke or carbon monoxide alarm, hot tub fault, damage, injury): set notify_casey true and urgent true. For fire, gas smell, a carbon monoxide alarm or a medical emergency, tell them to leave if needed and call 911 first. Then give the host phone if there is one.
- Trail, river and road conditions change. Give general guidance and say to check current conditions. Never state today's conditions as fact.
- If the question is unrelated to their trip, answer briefly if harmless, or steer back politely.
Return JSON: {"answer": string, "notify_casey": boolean, "urgent": boolean, "summary": string (under 12 words, what Casey needs to know; empty when notify_casey is false)}.
Trip context: ${JSON.stringify(ctx)}`;
      const convo = history.map((m) => `${m.direction === 'inbound' ? 'Guest' : 'Ask Ophir'}: ${m.body}`).join('\n');
      const out = await aiJSON(system, `${convo ? `Earlier in this conversation:\n${convo}\n\n` : ''}Guest's new question: ${q}`, 800);
      const answer = clip(out.answer, 1200) || 'Casey will get back to you shortly.';
      const notify = !!out.notify_casey || !!out.urgent;
      const nowIso = new Date().toISOString();
      await db.insert('messages', [
        { trip_id: trip.id, channel: 'app', direction: 'inbound', subject: 'Ask Ophir', body: q, status: 'received', created_at: new Date(Date.now() - 1000).toISOString() },
        { trip_id: trip.id, channel: 'app', direction: 'outbound', subject: 'Ask Ophir', body: answer, status: 'sent', sent_at: nowIso, created_at: nowIso },
      ]);
      if (notify) {
        const summary = clip(out.summary, 120) || clip(q, 120);
        await db.insert('tasks', [{ trip_id: trip.id, title: `${out.urgent ? 'URGENT guest question' : 'Guest question'}: ${summary}`, assignee: 'Casey', due_at: new Date(Date.now() + (out.urgent ? 9e5 : 36e5)).toISOString(), created_by: 'guest', approved: true }]);
        const inbox = (process.env.OWNER_INBOX || '').trim();
        if (inbox) await sendEmail({ to: inbox, subject: `${out.urgent ? 'URGENT: ' : ''}${trip.guest_name} asked: ${summary}`,
          html: emailShell(`<p><strong>${esc(trip.guest_name)}</strong> (${esc(trip.check_in)} to ${esc(trip.check_out)}${home ? `, ${esc(home.name)}` : ''}) asked:</p><p style="border-left:2px solid #B4572B;padding-left:12px">${esc(q)}</p><p>Ask Ophir answered:</p><p style="color:#6B645B">${esc(answer)}</p><p>Follow up with the guest directly.</p><p><a href="${SITE}/admin">Open admin</a></p>`) }).catch((e) => console.error('ask email', e));
      }
      return json(res, 200, { answer, notified: notify });
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
