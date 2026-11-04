// Ophir Partner Hosts.
// POST ?action=apply            host application from /partner -> homes row (partner, status 'applied'), emails Casey and the host.
// GET  ?h=<slug>                public info for a guest landing page /h/<slug> (active partner homes only).
// POST ?action=trip&h=<slug>    a guest of that home starts their trip -> trip (source 'partner') + welcome email, returns the trip link.
import crypto from 'node:crypto';
import { db, json, readBody, esc, sendEmail, emailShell, createTrip, SITE } from './_lib.js';

const clip = (v, n) => String(v ?? '').trim().slice(0, n);
const emailOk = (e) => /^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(e);
const isDate = (d) => /^\d{4}-\d{2}-\d{2}$/.test(d) && !isNaN(new Date(d + 'T12:00:00'));
const today = () => new Date().toLocaleDateString('en-CA', { timeZone: 'America/Denver' });
const inbox = () => (process.env.OWNER_INBOX || '').trim();
const first = (n) => String(n || '').trim().split(/\s+/)[0] || 'there';
const slugify = (s) => String(s || '').toLowerCase().normalize('NFKD').replace(/[^a-z0-9]+/g, '-').replace(/^-+|-+$/g, '').slice(0, 40) || 'home';
const table = (rows) => `<table style="font-size:15px;border-collapse:collapse">${rows.map(([k, v]) => `<tr><td style="padding:4px 14px 4px 0;color:#6F685F;vertical-align:top">${k}</td><td style="padding:4px 0">${esc(v) || '—'}</td></tr>`).join('')}</table>`;
const AREAS = { downtown: 'Downtown Durango', valley: 'Animas Valley', purgatory: 'Purgatory and Durango Mountain', vallecito: 'Vallecito and Bayfield', west: 'West of Durango', east: 'East of Durango', other: 'La Plata County' };

async function activeHome(slug) {
  if (!/^[a-z0-9-]{3,60}$/.test(slug)) return null;
  const h = await db.one('homes', `slug=eq.${slug}&partner=eq.true`);
  return h && h.partner_status === 'active' ? h : null;
}

async function apply(req, res) {
  const b = readBody(req);
  if (b.website) return json(res, 200, { ok: true }); // honeypot
  const d = {
    host_name: clip(b.name, 120), host_email: clip(b.email, 160).toLowerCase(), host_phone: clip(b.phone, 40),
    name: clip(b.home_name, 80) || clip(b.address, 80), address: clip(b.address, 200), area: AREAS[b.area] ? AREAS[b.area] : AREAS.other,
    beds: parseInt(b.bedrooms, 10) || null, sleeps: parseInt(b.sleeps, 10) || null, listing_url: clip(b.listing_url, 300), partner_notes: clip(b.notes, 1500),
  };
  if (!d.host_name || !d.address || !emailOk(d.host_email)) return json(res, 400, { error: 'Please add your name, email and the home address.' });
  if (d.listing_url && !/^https?:\/\//i.test(d.listing_url)) d.listing_url = 'https://' + d.listing_url;
  const slug = `${slugify(d.name)}-${crypto.randomBytes(2).toString('hex')}`;
  let saved = true;
  try { await db.insert('homes', [{ ...d, slug, partner: true, partner_status: 'applied', partner_rate: 0.10 }]); }
  catch (e) { saved = false; console.error('partner apply save', e.message); }
  try {
    await sendEmail({ to: inbox(), replyTo: d.host_email, subject: `Partner Host application: ${d.host_name}, ${d.address}`,
      html: emailShell(`<p><strong>${esc(d.host_name)}</strong> wants to be an Ophir Partner Host. Call within a day.</p>${table([['Home', d.name], ['Address', d.address], ['Area', d.area], ['Size', [d.beds && `${d.beds} bd`, d.sleeps && `sleeps ${d.sleeps}`].filter(Boolean).join(', ')], ['Listing', d.listing_url], ['Email', d.host_email], ['Phone', d.host_phone], ['Notes', d.partner_notes]])}
<p>${saved ? `To approve: Supabase → homes → <code>${esc(slug)}</code> → set <code>partner_status</code> to <code>active</code>. Their guest link is then <a href="${SITE}/h/${slug}">${SITE}/h/${slug}</a>` : '<span style="color:#9B2C1C">Not saved: run supabase/partners.sql, then add the home by hand.</span>'}</p>`) });
  } catch (e) { console.error('partner notify', e.message); if (!saved) return json(res, 502, { error: 'Could not send' }); }
  try {
    await sendEmail({ to: d.host_email, replyTo: inbox(), subject: 'Your Ophir Partner Host application',
      html: emailShell(`<p>${esc(first(d.host_name))},</p><p>Thank you. I have your details for ${esc(d.address)} and I'll call or email within a day to set you up.</p><p>Once you're live you'll get your home's own guest link and a card for the counter. Your guests plan their trip with us, and you earn 10% of every Ophir package and add-on they book.</p><p>Casey Roberts<br>Ophir Stays · casey@ophirstays.com</p>`) });
  } catch (e) { console.error('partner ack', e.message); }
  return json(res, 200, { ok: true });
}

async function guestTrip(req, res, home) {
  const b = readBody(req);
  if (b.website) return json(res, 200, { ok: true, url: null }); // honeypot
  const g = {
    guest_name: clip(b.name, 120), guest_email: clip(b.email, 160).toLowerCase(), guest_phone: clip(b.phone, 40) || null,
    check_in: clip(b.check_in, 10), check_out: clip(b.check_out, 10),
    adults: Math.max(1, Math.min(16, parseInt(b.adults, 10) || 2)), children: Math.max(0, Math.min(12, parseInt(b.children, 10) || 0)),
  };
  if (!g.guest_name || !emailOk(g.guest_email)) return json(res, 400, { error: 'Please add your name and email.' });
  if (!isDate(g.check_in) || !isDate(g.check_out) || g.check_out <= g.check_in) return json(res, 400, { error: 'Please check your dates.' });
  const nights = Math.round((new Date(g.check_out) - new Date(g.check_in)) / 864e5);
  if (g.check_out < today() || nights > 30) return json(res, 400, { error: 'Please check your dates.' });

  // One trip per guest, home and arrival date. A repeat never reveals the link on screen: we email it again.
  const external_id = crypto.createHash('sha256').update(`${home.id}|${g.guest_email}|${g.check_in}`).digest('hex').slice(0, 32);
  const existing = await db.one('trips', `source=eq.partner&external_id=eq.${external_id}`);
  if (existing) {
    await sendEmail({ to: g.guest_email, replyTo: inbox(), subject: 'Your Durango trip link',
      html: emailShell(`<p>${esc(first(existing.guest_name))},</p><p>Here is your private trip page again.</p><p style="text-align:center;margin:28px 0"><a href="${SITE}/trip/${existing.access_token}" style="background:#B4572B;color:#fff;text-decoration:none;padding:14px 26px;font-family:Arial,sans-serif;font-size:13px;letter-spacing:.2em;text-transform:uppercase">Plan your trip</a></p><p>Casey, Ophir Stays</p>`) }).catch((e) => console.error('partner resend', e.message));
    return json(res, 200, { ok: true, url: null, emailed: true });
  }
  const trip = await createTrip({ ...g, source: 'partner', external_id, home_id: home.id, package: 'stay' });
  sendEmail({ to: inbox(), replyTo: g.guest_email, subject: `Partner guest: ${g.guest_name}, ${home.name}, ${g.check_in}`,
    html: emailShell(`<p><strong>${esc(g.guest_name)}</strong> started a trip from <strong>${esc(home.name)}</strong> (host ${esc(home.host_name || '')}).</p>${table([['Dates', `${g.check_in} to ${g.check_out}, ${nights} nights`], ['Party', `${g.adults} adults, ${g.children} children`], ['Email', g.guest_email], ['Phone', g.guest_phone]])}<p><a href="${SITE}/admin">Open admin</a></p>`) })
    .catch((e) => console.error('partner guest notify', e.message));
  return json(res, 200, { ok: true, url: `/trip/${trip.access_token}` });
}

export default async function handler(req, res) {
  try {
    const action = String(req.query.action || '');
    if (req.method === 'POST' && action === 'apply') return await apply(req, res);
    const slug = String(req.query.h || '').toLowerCase();
    if (req.method === 'GET') {
      const h = await activeHome(slug);
      if (!h) return json(res, 404, { error: 'This link is not active yet.' });
      return json(res, 200, { name: h.name, area: h.area, host_first: first(h.host_name) });
    }
    if (req.method === 'POST' && action === 'trip') {
      const h = await activeHome(slug);
      if (!h) return json(res, 404, { error: 'This link is not active yet. Please email casey@ophirstays.com.' });
      return await guestTrip(req, res, h);
    }
    return json(res, 405, { error: 'Method not allowed' });
  } catch (e) {
    console.error('partner', e);
    return json(res, 500, { error: 'Something went wrong. Please email casey@ophirstays.com and we will reply today.' });
  }
}
