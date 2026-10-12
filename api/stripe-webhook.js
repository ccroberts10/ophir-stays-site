// Stripe webhook: checkout.session.completed -> mark paid, upgrade trip, re-plan with AI, tell Casey.
// Stripe Dashboard -> Developers -> Webhooks -> endpoint https://ophirstays.com/api/stripe-webhook, event checkout.session.completed.
import crypto from 'node:crypto';
import { db, json, planTrip, sendEmail, emailShell, esc, OFFERS, SITE } from './_lib.js';

export const config = { api: { bodyParser: false } };

async function rawBody(req) { const chunks = []; for await (const c of req) chunks.push(typeof c === 'string' ? Buffer.from(c) : c); return Buffer.concat(chunks).toString('utf8'); }

function verify(raw, header, secret) {
  const parts = Object.fromEntries(String(header || '').split(',').map((p) => p.split('=')).filter((x) => x.length === 2).map(([k, v]) => [k, v]));
  const sigs = String(header || '').split(',').filter((p) => p.startsWith('v1=')).map((p) => p.slice(3));
  if (!parts.t || !sigs.length) return false;
  if (Math.abs(Date.now() / 1000 - Number(parts.t)) > 300) return false;
  const expected = crypto.createHmac('sha256', secret).update(`${parts.t}.${raw}`).digest('hex');
  return sigs.some((s) => s.length === expected.length && crypto.timingSafeEqual(Buffer.from(s), Buffer.from(expected)));
}

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  const secret = (process.env.STRIPE_WEBHOOK_SECRET || '').trim();
  const raw = await rawBody(req);
  if (!secret || !verify(raw, req.headers['stripe-signature'], secret)) return json(res, 400, { error: 'Bad signature' });
  const event = JSON.parse(raw);
  if (event.type !== 'checkout.session.completed') return json(res, 200, { ok: true, ignored: event.type });
  const s = event.data.object;
  if (s.payment_status !== 'paid') return json(res, 200, { ok: true, unpaid: true });
  try {
    const pay = await db.one('payments', `stripe_session_id=eq.${s.id}`);
    if (!pay || pay.status === 'paid') return json(res, 200, { ok: true, duplicate: !!pay });
    await db.update('payments', `id=eq.${pay.id}`, { status: 'paid' });
    const trip = await db.one('trips', `id=eq.${pay.trip_id}`);
    if (pay.item === 'arranged' || pay.item === 'private') await db.update('trips', `id=eq.${trip.id}`, { package: pay.item });
    // Re-plan so the paid services become real tasks; Casey re-approves.
    let result = null;
    try { result = await planTrip(trip.id); } catch (e) { console.error('replan after payment', e); }
    const inbox = (process.env.OWNER_INBOX || '').trim();
    if (inbox) await sendEmail({ to: inbox, subject: `Paid: ${trip.guest_name} added ${OFFERS[pay.item]?.title || pay.item} ($${(pay.amount_cents / 100).toFixed(2)})`,
      html: emailShell(`<p><strong>${esc(trip.guest_name)}</strong> paid <strong>$${(pay.amount_cents / 100).toFixed(2)}</strong> for <strong>${esc(OFFERS[pay.item]?.title || pay.item)}</strong>.</p><p>${result ? 'The AI has updated the plan and tasks to include it. Please review and approve.' : 'Please re-plan this trip in admin.'}</p><p><a href="${SITE}/admin">Open admin</a></p>`) });
    return json(res, 200, { ok: true });
  } catch (e) {
    console.error('stripe webhook', e);
    return json(res, 500, { error: 'failed' });
  }
}
