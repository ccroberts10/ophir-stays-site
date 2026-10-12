// Admin API for Casey. Every call needs header x-admin-key = ADMIN_PASSWORD.
// POST { action: 'list' | 'detail' | 'approve' | 'replan' | 'simulate' | 'task' | 'resend_welcome', ... }
import { db, json, readBody, isAdmin, loadTrip, createTrip, planTrip, approveTrip, sendWelcome } from './_lib.js';

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
        return json(res, 200, { ...t, messages, link: `/trip/${t.trip.access_token}` });
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
      default: return json(res, 400, { error: 'Unknown action' });
    }
  } catch (e) {
    console.error('admin api', e);
    return json(res, 500, { error: e.message });
  }
}
