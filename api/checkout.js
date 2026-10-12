// POST /api/checkout?t=<token> { key } -> Stripe Checkout URL for a fixed-price offer on this trip.
import { db, json, readBody, OFFERS, priceFor, stripe, SITE } from './_lib.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  const token = String(req.query.t || '');
  if (!/^[a-f0-9]{24,64}$/.test(token)) return json(res, 400, { error: 'Invalid link' });
  try {
    const trip = await db.one('trips', `access_token=eq.${token}`);
    if (!trip || trip.status === 'cancelled') return json(res, 404, { error: 'Trip not found' });
    const key = String(readBody(req).key || '');
    if (!(trip.offers || []).some((o) => o.key === key)) return json(res, 400, { error: 'This addition is not available for your trip.' });
    const price = priceFor(key, trip);
    if (!price || price.cents <= 0) return json(res, 400, { error: 'This addition is priced on request.' });
    const already = await db.select('payments', `trip_id=eq.${trip.id}&item=eq.${key}&status=eq.paid`);
    if (already.length) return json(res, 409, { error: 'Already added to your trip.' });

    const session = await stripe('checkout/sessions', {
      mode: 'payment',
      success_url: `${SITE}/trip/${token}?paid=${encodeURIComponent(key)}`,
      cancel_url: `${SITE}/trip/${token}`,
      customer_email: trip.guest_email || undefined,
      'line_items[0][quantity]': 1,
      'line_items[0][price_data][currency]': 'usd',
      'line_items[0][price_data][unit_amount]': price.cents,
      'line_items[0][price_data][product_data][name]': `${price.label} · Ophir Stays`,
      'line_items[0][price_data][product_data][description]': `${OFFERS[key].blurb} ${trip.check_in} to ${trip.check_out}.`,
      metadata: { trip_id: trip.id, item: key },
      payment_intent_data: { metadata: { trip_id: trip.id, item: key }, statement_descriptor_suffix: 'OPHIR STAYS' },
    });
    await db.insert('payments', [{ trip_id: trip.id, item: key, amount_cents: price.cents, stripe_session_id: session.id, status: 'pending' }]);
    return json(res, 200, { url: session.url });
  } catch (e) {
    console.error('checkout', e);
    return json(res, 500, { error: 'Payment could not start. Please try again, or reply to our email.' });
  }
}
