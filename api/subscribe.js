// Newsletter signup. POST { email, list: 'guest' | 'owner' } -> saved in Supabase table "subscribers".
import { db, json, readBody } from './_lib.js';

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  try {
    const b = readBody(req);
    if (b.website) return json(res, 200, { ok: true }); // honeypot
    const email = String(b.email || '').trim().toLowerCase().slice(0, 160);
    if (!/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(email)) return json(res, 400, { error: 'Invalid email' });
    const list = b.list === 'owner' ? 'owner' : 'guest';
    await db.upsert('subscribers', [{ email, list, source: String(b.source || 'site').slice(0, 40), unsubscribed: false }], 'email,list');
    return json(res, 200, { ok: true });
  } catch (e) {
    console.error('subscribe', e);
    return json(res, 500, { error: 'Could not subscribe' });
  }
}
