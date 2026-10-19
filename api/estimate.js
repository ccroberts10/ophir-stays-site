// Earnings estimate requests.
// POST (public form): saves the request, drafts the report with the model, emails Casey and thanks the requester.
// GET ?t=<token>: the report data for /report/<token> (tokens are unguessable; nothing private beyond the report).
import { db, json, readBody, esc, sendEmail, emailShell, SITE } from './_lib.js';
import { computeEstimate, AREAS, FEATURES } from './_model.js';

const clip = (s, n) => String(s ?? '').trim().slice(0, n);
const money = (n) => '$' + Math.round(n).toLocaleString('en-US');
const env = (k) => (process.env[k] || '').trim();

export function publicReport(e) {
  return {
    address: e.address, area: e.area, home_type: e.home_type, bedrooms: e.bedrooms, baths: e.baths, sleeps: e.sleeps,
    features: (e.features || []).map((f) => FEATURES[f]?.label).filter(Boolean), hoa: e.hoa, current_rent: e.current_rent,
    owner_name: e.requester_role === 'agent' ? e.owner_name : e.requester_name,
    agent_name: e.requester_role === 'agent' ? e.requester_name : null, brokerage: e.requester_role === 'agent' ? e.brokerage : null,
    personal_note: e.personal_note, date: (e.sent_at || e.created_at || new Date().toISOString()).slice(0, 10), status: e.status,
    model: e.model,
  };
}

export default async function handler(req, res) {
  if (req.method === 'GET') {
    const t = String(req.query.t || '');
    if (!/^[a-f0-9]{32}$/.test(t)) return json(res, 400, { error: 'Invalid link' });
    try {
      const e = await db.one('estimates', `token=eq.${t}`);
      if (!e) return json(res, 404, { error: 'Report not found' });
      return json(res, 200, publicReport(e));
    } catch (err) { console.error(err); return json(res, 500, { error: 'Could not load report' }); }
  }
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });

  const b = readBody(req);
  if (b.website) return json(res, 200, { ok: true }); // honeypot
  const role = b.role === 'agent' ? 'agent' : 'owner';
  const d = {
    requester_role: role, requester_name: clip(b.name, 120), requester_email: clip(b.email, 160).toLowerCase(), requester_phone: clip(b.phone, 40),
    brokerage: role === 'agent' ? clip(b.brokerage, 120) : null, owner_name: role === 'agent' ? clip(b.owner_name, 120) : null,
    address: clip(b.address, 200), area: AREAS[b.area] ? b.area : 'other', home_type: ['house', 'cabin', 'townhome', 'condo'].includes(b.home_type) ? b.home_type : 'house',
    bedrooms: Math.max(1, Math.min(10, parseInt(b.bedrooms, 10) || 0)) || null, baths: parseFloat(b.baths) || null, sleeps: parseInt(b.sleeps, 10) || null,
    features: [].concat(b.features || []).filter((f) => FEATURES[f]).slice(0, 12), hoa: clip(b.hoa, 40), current_use: clip(b.current_use, 60),
    current_rent: parseInt(String(b.current_rent || '').replace(/[^\d]/g, ''), 10) || null, source: clip(b.source, 120), notes: clip(b.notes, 2000),
  };
  if (!d.requester_name || !d.address || !d.bedrooms || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.requester_email)) {
    return json(res, 400, { error: 'Please add your name, email, the home address and bedrooms.' });
  }
  d.model = computeEstimate(d);

  let row = null;
  try { [row] = await db.insert('estimates', [d]); } catch (err) { console.error('estimates insert', err.message); }

  const m = d.model;
  const lines = [['From', `${d.requester_name} (${role}${d.brokerage ? ', ' + d.brokerage : ''})`], ['Email', d.requester_email], ['Phone', d.requester_phone],
    ...(role === 'agent' ? [['Owner', d.owner_name]] : []), ['Home', d.address], ['Area', AREAS[d.area].label],
    ['Home', `${d.home_type}, ${d.bedrooms} bd${d.baths ? ', ' + d.baths + ' ba' : ''}${d.sleeps ? ', sleeps ' + d.sleeps : ''}`],
    ['Features', d.features.map((f) => FEATURES[f].label).join(', ')], ['HOA', d.hoa], ['Now', d.current_use], ['Last 12 months', d.current_rent ? money(d.current_rent) : ''],
    ['Heard about us', d.source], ['Notes', d.notes]]
    .map(([k, v]) => `<tr><td style="padding:5px 14px 5px 0;color:#6F685F;vertical-align:top">${k}</td><td style="padding:5px 0">${esc(v) || '—'}</td></tr>`).join('');
  const draft = `<p style="font-size:15px;margin:0 0 12px"><b>Draft:</b> ${money(m.rent)} expected rent (${money(m.range[0])}–${money(m.range[1])}), owner keeps ${money(m.keep)}, ${m.nights} nights at ${money(m.avg_rate)}.</p>`;
  try {
    await sendEmail({
      to: env('OWNER_INBOX'), replyTo: d.requester_email,
      subject: `Estimate request: ${d.address}${role === 'agent' ? ' (from ' + d.requester_name + ')' : ''}`,
      html: emailShell(`${draft}<table style="font-size:14px">${lines}</table>${row ? `<p style="margin-top:20px"><a href="${SITE}/admin#estimate-${row.id}">Review and send the report</a> · <a href="${SITE}/report/${row.token}">Preview</a></p>` : '<p style="color:#9B2C1C">Not saved to the database (run supabase/estimates.sql). Reply by email.</p>'}`),
    });
  } catch (err) { console.error('notify', err.message); if (!row) return json(res, 502, { error: 'Could not send' }); }

  try {
    const first = d.requester_name.split(/\s+/)[0];
    await sendEmail({
      to: d.requester_email, replyTo: env('OWNER_INBOX'), subject: `Your earnings estimate for ${d.address}`,
      html: emailShell(`<p>${esc(first)},</p><p>Thank you. I have everything I need for ${esc(d.address)}. I'll check the numbers myself and send your report within 24 hours.</p><p>If there's anything about the home I should know, just reply to this email.</p><p>Casey Roberts<br>Ophir Stays · 970-779-8992</p>`),
    });
  } catch (err) { console.error('ack', err.message); }
  return json(res, 200, { ok: true });
}
