// Admin API for Casey. Every call needs header x-admin-key = ADMIN_PASSWORD.
// POST { action: 'list' | 'detail' | 'approve' | 'replan' | 'simulate' | 'task' | 'resend_welcome', ... }
import { db, json, readBody, isAdmin, loadTrip, createTrip, planTrip, approveTrip, sendWelcome, sendEmail, emailShell, esc, SITE } from './_lib.js';

const addDays = (n) => { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
const SAMPLE_NAMES = ['Taylor Brooks', 'Morgan Hale', 'Jordan Pierce', 'Avery Collins', 'Riley Dawson'];

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  if (!isAdmin(req)) return json(res, 401, { error: 'Wrong password' });
  const b = readBody(req);
  try {
    switch (b.action) {
      case 'list': {
        const trips = await db.select('trips', 'select=id,guest_name,guest_email,check_in,check_out,adults,children,package,status,source,created_at,homes(name)&order=check_in.asc&limit=200');
        const tasks = await db.select('tasks', 'select=id,trip_id,title,assignee,due_at,status,approved&status=eq.open&order=due_at.asc&limit=300');
        return json(res, 200, { trips, tasks });
      }
      case 'detail': {
        const t = await loadTrip(`id=eq.${b.id}`);
        if (!t) return json(res, 404, { error: 'Not found' });
        const messages = await db.select('messages', `trip_id=eq.${b.id}&order=created_at.desc&limit=20`);
        const payments = await db.select('payments', `trip_id=eq.${b.id}&order=created_at.desc`);
        const charges = await db.select('charges', `trip_id=eq.${b.id}&order=created_at.desc`);
        return json(res, 200, { ...t, messages, payments, charges, link: `/trip/${t.trip.access_token}` });
      }
      case 'approve': await approveTrip(b.id); return json(res, 200, { ok: true });
      case 'replan': return json(res, 200, { ok: true, ...(await planTrip(b.id)) });
      case 'resend_welcome': { const t = await loadTrip(`id=eq.${b.id}`); await sendWelcome(t.trip, t.home); return json(res, 200, { ok: true }); }
      case 'task': {
        const patch = {};
        if (b.status) patch.status = b.status;
        if (b.assignee) patch.assignee = String(b.assignee).slice(0, 60);
        await db.update('tasks', `id=eq.${b.id}`, patch);
        return json(res, 200, { ok: true });
      }
      case 'simulate': {
        const name = SAMPLE_NAMES[Math.floor(Math.random() * SAMPLE_NAMES.length)];
        const start = Number.isFinite(+b.days_out) ? +b.days_out : 10;
        const trip = await createTrip({
          source: 'simulated', external_id: `SIM-${Date.now()}`, guest_name: name,
          guest_email: b.email || process.env.OWNER_INBOX, check_in: addDays(start), check_out: addDays(start + 4),
          adults: 2, children: 2, package: ['stay', 'arranged', 'private'].includes(b.package) ? b.package : 'arranged',
        });
        return json(res, 200, { ok: true, id: trip.id, link: `/trip/${trip.access_token}` });
      }
      case 'charge_create': {
        const t = await loadTrip(`id=eq.${b.id}`);
        if (!t) return json(res, 404, { error: 'Not found' });
        const title = String(b.title || '').trim().slice(0, 80);
        const cents = Math.round(parseFloat(String(b.amount || '').replace(/[$,]/g, '')) * 100);
        if (!title || !(cents >= 100 && cents <= 2000000)) return json(res, 400, { error: 'Add an item name and an amount between $1 and $20,000.' });
        const [c] = await db.insert('charges', [{ trip_id: t.trip.id, title, note: String(b.note || '').trim().slice(0, 300) || null, amount_cents: cents }]);
        if (t.trip.guest_email && b.notify !== false) {
          const link = `${SITE}/trip/${t.trip.access_token}`;
          await sendEmail({ to: t.trip.guest_email, subject: `For your Durango trip: ${title}`,
            html: emailShell(`<p>Hi ${esc(String(t.trip.guest_name).split(/\s+/)[0])},</p><p>${esc(title)} is arranged and held for you${c.note ? `: ${esc(c.note)}` : '.'}</p><p><strong>$${(cents / 100).toFixed(2)}</strong>. Confirm it on your trip page and it's done.</p><p><a href="${link}">Open your trip</a></p>`) });
        }
        return json(res, 200, { ok: true, charge: c });
      }
      case 'charge_void': await db.update('charges', `id=eq.${b.charge_id}&status=eq.open`, { status: 'void' }); return json(res, 200, { ok: true });
      case 'restaurants': return json(res, 200, { restaurants: await db.select('restaurants', 'order=active.desc,name') });
      case 'restaurant_save': {
        const r = b.restaurant || {};
        const row = { name: String(r.name || '').trim().slice(0, 80), cuisine: (r.cuisine || '').slice(0, 60) || null, vibe: (r.vibe || '').slice(0, 80) || null,
          price: [1, 2, 3, 4].includes(+r.price) ? +r.price : null, kid_friendly: !!r.kid_friendly, book_via: (r.book_via || '').slice(0, 40) || null,
          phone: (r.phone || '').slice(0, 30) || null, booking_url: (r.booking_url || '').slice(0, 300) || null, first_round: !!r.first_round,
          notes: (r.notes || '').slice(0, 300) || null, active: r.active !== false };
        if (!row.name) return json(res, 400, { error: 'Name required' });
        const out = r.id ? await db.update('restaurants', `id=eq.${r.id}`, row) : await db.insert('restaurants', [row]);
        return json(res, 200, { ok: true, restaurant: out[0] });
      }
      default: return json(res, 400, { error: 'Unknown action' });
    }
  } catch (e) {
    console.error('admin api', e);
    return json(res, 500, { error: e.message });
  }
}
