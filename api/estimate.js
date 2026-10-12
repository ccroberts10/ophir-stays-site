// Vercel serverless function: receives the owner estimate form and emails it via Resend.
// Env vars (Vercel → Project → Settings → Environment Variables):
//   RESEND_API_KEY   from resend.com
//   OWNER_INBOX      where requests go, e.g. casey@ophirstays.com
//   FROM_ADDRESS     a verified sender, e.g. "Ophir Stays <hello@ophirstays.com>"

const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));
const clip = (s, n) => String(s ?? '').trim().slice(0, n);

export default async function handler(req, res) {
  if (req.method !== 'POST') return res.status(405).json({ error: 'Method not allowed' });

  const b = typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {});
  if (b.website) return res.status(200).json({ ok: true }); // honeypot: bots fill it, people never see it

  const d = {
    name: clip(b.name, 120), email: clip(b.email, 160), phone: clip(b.phone, 40),
    address: clip(b.address, 200), bedrooms: clip(b.bedrooms, 10), renting: clip(b.renting, 60),
    revenue: clip(b.revenue, 40), notes: clip(b.notes, 2000),
  };
  if (!d.name || !d.address || !/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(d.email)) {
    return res.status(400).json({ error: 'Missing name, email or address' });
  }

  const rows = [['Name', d.name], ['Email', d.email], ['Phone', d.phone], ['Home address', d.address],
    ['Bedrooms', d.bedrooms], ['Rented now', d.renting], ['Last 12 months income', d.revenue], ['Notes', d.notes]]
    .map(([k, v]) => `<tr><td style="padding:6px 16px 6px 0;color:#6B645B">${k}</td><td style="padding:6px 0">${esc(v) || '—'}</td></tr>`).join('');

  const key = (process.env.RESEND_API_KEY || '').trim();
  const to = (process.env.OWNER_INBOX || '').trim();
  if (!key || !to) {
    console.error('Missing env vars:', { RESEND_API_KEY: !!key, OWNER_INBOX: !!to });
    return res.status(500).json({ error: 'Server not configured' });
  }

  const message = {
    to: [to],
    reply_to: d.email,
    subject: `Owner estimate request: ${d.address}`,
    html: `<div style="font-family:Arial,sans-serif;font-size:15px;color:#2A2826"><h2 style="font-weight:500">New owner estimate request</h2><table>${rows}</table><p style="color:#6B645B">Reply to this email to answer ${esc(d.name)} directly.</p></div>`,
  };
  const send = (from) => fetch('https://api.resend.com/emails', {
    method: 'POST',
    headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ ...message, from }),
  });

  // Try the branded sender first; if the domain isn't verified yet, fall back to Resend's
  // shared sender (it can deliver to the Resend account owner's own inbox).
  let r = await send((process.env.FROM_ADDRESS || '').trim() || 'Ophir Stays <hello@ophirstays.com>');
  if (!r.ok) {
    console.error('Resend error (branded sender)', r.status, await r.text());
    r = await send('Ophir Stays <onboarding@resend.dev>');
  }
  if (!r.ok) {
    const detail = await r.text();
    console.error('Resend error (fallback sender)', r.status, detail);
    return res.status(502).json({ error: 'Could not send', status: r.status });
  }
  return res.status(200).json({ ok: true });
}
