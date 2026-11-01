// Basecamp trip inquiry. POST from /basecamp -> saved to Supabase "basecamp_inquiries" (if the table exists) and emailed to Casey.
import { db, json, readBody, sendEmail, emailShell, esc } from './_lib.js';

const TYPES = { bike: 'Bike trip', camp: 'Training camp', iron_horse: 'Iron Horse week', ski: 'Ski trip', other: 'Something else' };
const clip = (v, n) => String(v || '').trim().slice(0, n);

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  try {
    const b = readBody(req);
    if (b.website) return json(res, 200, { ok: true }); // honeypot
    const row = {
      name: clip(b.name, 120), email: clip(b.email, 160).toLowerCase(), phone: clip(b.phone, 40),
      trip_type: TYPES[b.trip_type] ? b.trip_type : 'other', group_size: clip(b.group_size, 20),
      level: clip(b.level, 20), dates: clip(b.dates, 200), notes: clip(b.notes, 2000),
    };
    if (!row.name || !row.dates || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(row.email)) return json(res, 400, { error: 'Missing name, email or dates' });
    let saved = true;
    try { await db.insert('basecamp_inquiries', [row]); } catch (e) { saved = false; console.error('basecamp save', e.message); }
    const lines = [['Trip', TYPES[row.trip_type]], ['Group', row.group_size], ['Level', row.level], ['When', row.dates], ['Email', row.email], ['Phone', row.phone || '—'], ['Notes', row.notes || '—']];
    await sendEmail({
      to: process.env.OWNER_INBOX, replyTo: row.email,
      subject: `Basecamp inquiry: ${row.name}, ${TYPES[row.trip_type]}, ${row.group_size}`,
      html: emailShell(`<p><strong>${esc(row.name)}</strong> wants to plan a Basecamp trip.</p><table style="font-size:15px;border-collapse:collapse">${lines.map(([k, v]) => `<tr><td style="padding:4px 14px 4px 0;color:#6F685F">${k}</td><td style="padding:4px 0">${esc(v)}</td></tr>`).join('')}</table><p style="color:#6F685F;font-size:13px">Reply to this email to answer them directly.${saved ? '' : ' (Not saved to Supabase: run supabase/basecamp.sql.)'}</p>`),
    });
    return json(res, 200, { ok: true });
  } catch (e) {
    console.error('basecamp', e);
    return json(res, 500, { error: 'Could not send' });
  }
}
