// Daily cron (vercel.json): keeps the free Supabase project awake, then sends any due upgrade-offer emails.
import { db, json, runUpgradeOffers } from './_lib.js';

export default async function handler(req, res) {
  try {
    const rows = await db.select('homes', 'select=id&limit=1');
    let upgrades = 0;
    try { upgrades = await runUpgradeOffers(); } catch (e) { console.error('upgrade offers', e); }
    return json(res, 200, { ok: true, rows: rows ? rows.length : 0, upgrades, at: new Date().toISOString() });
  } catch (e) {
    return json(res, 500, { ok: false, error: String(e.message || e).slice(0, 200) });
  }
}
