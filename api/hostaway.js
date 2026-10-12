// Hostaway webhook: new reservation -> trip created -> AI welcome sent.
// In Hostaway: Settings -> Webhooks -> URL: https://ophirstays.com/api/hostaway?secret=<HOSTAWAY_WEBHOOK_SECRET>
// NOTE: written against Hostaway's documented reservation fields; verify with the first real webhook payload.
import { json, readBody, createTrip, db } from './_lib.js';

const channel = (name = '') => { const n = String(name).toLowerCase(); return n.includes('airbnb') ? 'airbnb' : n.includes('vrbo') || n.includes('homeaway') ? 'vrbo' : n.includes('direct') ? 'direct' : 'other'; };

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  const secret = (process.env.HOSTAWAY_WEBHOOK_SECRET || '').trim();
  if (!secret || req.query.secret !== secret) return json(res, 401, { error: 'Unauthorized' });
  try {
    const b = readBody(req);
    const r = b.data || b.reservation || b;
    const event = String(b.event || b.object || '').toLowerCase();
    const status = String(r.status || '').toLowerCase();
    if (status === 'cancelled' || event.includes('cancel')) {
      await db.update('trips', `external_id=eq.${encodeURIComponent(String(r.id))}`, { status: 'cancelled' });
      return json(res, 200, { ok: true, cancelled: true });
    }
    if (!r.id || !r.arrivalDate || !r.departureDate) return json(res, 200, { ok: true, ignored: true });
    const guests = Number(r.numberOfGuests || r.adults || 2);
    const trip = await createTrip({
      source: channel(r.channelName || r.source), external_id: String(r.id), hostaway_listing_id: String(r.listingMapId || r.listingId || ''),
      guest_name: r.guestName || [r.guestFirstName, r.guestLastName].filter(Boolean).join(' ') || 'Guest',
      guest_email: r.guestEmail || null, guest_phone: r.phone || r.guestPhone || null,
      check_in: r.arrivalDate, check_out: r.departureDate, adults: Number(r.adults || guests), children: Number(r.children || 0),
    });
    return json(res, 200, { ok: true, trip: trip.id });
  } catch (e) {
    console.error('hostaway webhook', e);
    return json(res, 500, { error: 'failed' });
  }
}
