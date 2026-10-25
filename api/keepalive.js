// Daily ping so the free Supabase project never sits idle long enough to be paused.
// Called by the Vercel cron in vercel.json. Read-only: fetches one id from homes.
import { db, json } from './_lib.js';

export default async function handler(req, res) {
  try {
    const rows = await db.select('homes', 'select=id&limit=1');
    return json(res, 200, { ok: true, rows: rows ? rows.length : 0, at: new Date().toISOString() });
  } catch (e) {
    return json(res, 500, { ok: false, error: String(e.message || e).slice(0, 200) });
  }
}
