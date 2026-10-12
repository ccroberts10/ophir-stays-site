// Shared server helpers for the Ophir Stays app. Files starting with "_" are not exposed as routes.
// Env: SUPABASE_URL, SUPABASE_SECRET_KEY, ANTHROPIC_API_KEY, RESEND_API_KEY, OWNER_INBOX, FROM_ADDRESS,
//      ADMIN_PASSWORD, SITE_URL (optional, default https://ophirstays.com), ANTHROPIC_MODEL (optional)

export const SITE = (process.env.SITE_URL || 'https://ophirstays.com').replace(/\/$/, '');
const env = (k) => (process.env[k] || '').trim();

export function json(res, code, body) { res.status(code).setHeader('Cache-Control', 'no-store'); return res.json(body); }
export function readBody(req) { return typeof req.body === 'string' ? JSON.parse(req.body || '{}') : (req.body || {}); }
export const esc = (s) => String(s ?? '').replace(/[&<>"']/g, (c) => ({ '&': '&amp;', '<': '&lt;', '>': '&gt;', '"': '&quot;', "'": '&#39;' }[c]));

// ---------- Supabase (PostgREST) ----------
function dbHeaders(extra = {}) {
  const key = env('SUPABASE_SECRET_KEY');
  const h = { apikey: key, 'Content-Type': 'application/json', ...extra };
  if (!key.startsWith('sb_')) h.Authorization = `Bearer ${key}`; // legacy service_role JWT
  return h;
}
async function rest(path, opts = {}) {
  const base = env('SUPABASE_URL').replace(/\/$/, '');
  if (!base || !env('SUPABASE_SECRET_KEY')) throw new Error('Supabase not configured');
  const r = await fetch(`${base}/rest/v1/${path}`, { ...opts, headers: dbHeaders(opts.headers) });
  const text = await r.text();
  if (!r.ok) throw new Error(`DB ${r.status}: ${text.slice(0, 300)}`);
  return text ? JSON.parse(text) : null;
}
export const db = {
  select: (table, query = '') => rest(`${table}?${query}`),
  one: async (table, query) => (await rest(`${table}?${query}&limit=1`))[0] || null,
  insert: (table, rows) => rest(table, { method: 'POST', headers: { Prefer: 'return=representation' }, body: JSON.stringify(rows) }),
  upsert: (table, rows, onConflict) => rest(`${table}${onConflict ? `?on_conflict=${onConflict}` : ''}`, {
    method: 'POST', headers: { Prefer: 'return=representation,resolution=merge-duplicates' }, body: JSON.stringify(rows) }),
  update: (table, query, patch) => rest(`${table}?${query}`, { method: 'PATCH', headers: { Prefer: 'return=representation' }, body: JSON.stringify(patch) }),
  remove: (table, query) => rest(`${table}?${query}`, { method: 'DELETE' }),
};

// ---------- Anthropic ----------
export async function ai(system, user, maxTokens = 4000) {
  const key = env('ANTHROPIC_API_KEY');
  if (!key) throw new Error('Anthropic not configured');
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST',
    headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' },
    body: JSON.stringify({ model: env('ANTHROPIC_MODEL') || 'claude-sonnet-5-5', max_tokens: maxTokens, system, messages: [{ role: 'user', content: user }] }),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(`AI ${r.status}: ${JSON.stringify(data).slice(0, 300)}`);
  return (data.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('');
}
export async function aiJSON(system, user, maxTokens) {
  const text = await ai(system + '\n\nRespond with a single JSON object only. No prose, no code fences.', user, maxTokens);
  const start = text.indexOf('{'), end = text.lastIndexOf('}');
  if (start < 0 || end < 0) throw new Error('AI returned no JSON');
  return JSON.parse(text.slice(start, end + 1));
}

// ---------- Email ----------
export async function sendEmail({ to, subject, html, replyTo }) {
  const key = env('RESEND_API_KEY');
  if (!key || !to) throw new Error('Email not configured');
  const send = (from) => fetch('https://api.resend.com/emails', {
    method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/json' },
    body: JSON.stringify({ from, to: [to], subject, html, ...(replyTo ? { reply_to: replyTo } : {}) }),
  });
  let r = await send(env('FROM_ADDRESS') || 'Ophir Stays <hello@ophirstays.com>');
  if (!r.ok) { console.error('Resend', r.status, await r.text()); r = await send('Ophir Stays <onboarding@resend.dev>'); }
  if (!r.ok) throw new Error(`Email ${r.status}: ${(await r.text()).slice(0, 200)}`);
}
export function emailShell(bodyHtml) {
  return `<div style="background:#FAF8F4;padding:32px 16px;font-family:Georgia,serif;color:#2A2826">
  <div style="max-width:560px;margin:0 auto;background:#fff;border:1px solid #E7E1D6;padding:36px 32px">
    <div style="text-align:center;letter-spacing:.5em;font-family:Arial,sans-serif;font-size:18px;font-weight:600">OPHIR</div>
    <div style="text-align:center;letter-spacing:.6em;font-family:Arial,sans-serif;font-size:10px;color:#B4572B;margin:6px 0 28px">STAYS</div>
    <div style="font-size:16px;line-height:1.65">${bodyHtml}</div>
    <div style="border-top:1px solid #E7E1D6;margin-top:28px;padding-top:16px;font-family:Arial,sans-serif;font-size:12px;color:#6F685F;text-align:center">Ophir Stays · Durango, Colorado · ophirstays.com</div>
  </div></div>`;
}
const button = (href, label) => `<p style="text-align:center;margin:28px 0"><a href="${href}" style="background:#B4572B;color:#fff;text-decoration:none;padding:14px 26px;font-family:Arial,sans-serif;font-size:13px;letter-spacing:.2em;text-transform:uppercase">${label}</a></p>`;
const paras = (text) => String(text).split(/\n{2,}/).map((p) => `<p style="margin:0 0 16px">${esc(p).replace(/\n/g, '<br>')}</p>`).join('');

// ---------- Weather (Open-Meteo, free, no key) ----------
const DURANGO = { lat: 37.2753, lon: -107.8801 };
export async function forecast(startDate, endDate) {
  try {
    const url = `https://api.open-meteo.com/v1/forecast?latitude=${DURANGO.lat}&longitude=${DURANGO.lon}&daily=weather_code,temperature_2m_max,temperature_2m_min,precipitation_probability_max,snowfall_sum&temperature_unit=fahrenheit&precipitation_unit=inch&timezone=America%2FDenver&forecast_days=16`;
    const d = (await (await fetch(url)).json()).daily;
    if (!d) return [];
    return d.time.map((t, i) => ({ date: t, high: Math.round(d.temperature_2m_max[i]), low: Math.round(d.temperature_2m_min[i]),
      precip_chance: d.precipitation_probability_max[i], snow_in: d.snowfall_sum[i], code: d.weather_code[i] }))
      .filter((x) => x.date >= startDate && x.date <= endDate);
  } catch (e) { console.error('weather', e.message); return []; }
}

// ---------- Business knowledge given to the AI ----------
export const PACKAGES = {
  stay: 'The Stay (included): inspected home, welcome card, house guide in app, weather-aware ideas, local host by text. Ophir does NOT book activities or shop for groceries unless an add-on is bought; suggest them instead.',
  arranged: 'The Arranged Stay ($395): planning call, skis and boots sized to each guest and waiting in the gear room, bikes fitted and delivered, lift tickets/guides/rafting/fly fishing booked, dinner reservations held with first round on us, itinerary that moves with the weather.',
  private: 'The Private Stay ($1,250 up to 5 nights): everything in Arranged, plus groceries shopped and fridge stocked, fire laid and wine chosen, a dedicated host on call, private chef/massage/sitter arranged, airport arrival arranged, mid-stay refresh.',
};
export const TEAM = 'Team and partners (assign tasks to these names): "Casey" (owner/host, books everything), "CRC Janitorial" (cleaning and turnover), "James Hillyer" (maintenance/handyman), "Ski shop" (ski and boot rentals), "Bike shop" (bike rentals and delivery), "San Juan Angler" (fly fishing), "Grocery run" (shopping, done by Casey).';
export const DURANGO_NOTES = 'Durango, Colorado. Purgatory Resort is about 30 minutes north (ski/ride in winter, bike park and alpine coaster in summer). Downtown Main Avenue for dining. Animas River for rafting and fly fishing. Trails: Horse Gulch, Animas Mountain, Log Chutes, Colorado Trail at Junction Creek, Hermosa Creek. Hot springs north of town. Glacier Club and Dalton Ranch for golf. Afternoon thunderstorms are common in July and August, so plan rides and hikes in the morning.';

// ---------- Core flows ----------
const fmt = (d) => new Date(d + 'T12:00:00').toLocaleDateString('en-US', { weekday: 'long', month: 'long', day: 'numeric' });
const firstName = (n) => String(n || '').trim().split(/\s+/)[0] || 'there';

export async function loadTrip(where) {
  const trip = await db.one('trips', where);
  if (!trip) return null;
  const [home, party, answers, itinerary, tasks] = await Promise.all([
    trip.home_id ? db.one('homes', `id=eq.${trip.home_id}`) : null,
    db.select('party_members', `trip_id=eq.${trip.id}&order=name`),
    db.one('trip_answers', `trip_id=eq.${trip.id}`),
    db.select('itinerary_items', `trip_id=eq.${trip.id}&order=day,position`),
    db.select('tasks', `trip_id=eq.${trip.id}&order=due_at`),
  ]);
  return { trip, home, party, answers, itinerary, tasks };
}

export async function createTrip(b) {
  if (b.external_id) {
    const existing = await db.one('trips', `source=eq.${encodeURIComponent(b.source || 'other')}&external_id=eq.${encodeURIComponent(b.external_id)}`);
    if (existing) return existing; // duplicate webhook: never welcome twice
  }
  const home = b.home_id ? await db.one('homes', `id=eq.${b.home_id}`)
    : (b.hostaway_listing_id ? await db.one('homes', `hostaway_listing_id=eq.${encodeURIComponent(b.hostaway_listing_id)}`) : null)
      || await db.one('homes', 'slug=eq.test-home');
  const [trip] = await db.upsert('trips', [{
    home_id: home?.id || null, source: b.source || 'other', external_id: b.external_id || null,
    guest_name: b.guest_name, guest_email: b.guest_email || null, guest_phone: b.guest_phone || null,
    check_in: b.check_in, check_out: b.check_out, adults: b.adults || 2, children: b.children || 0, package: b.package || 'stay',
  }], 'source,external_id');
  await sendWelcome(trip, home);
  return trip;
}

export async function sendWelcome(trip, home) {
  const link = `${SITE}/trip/${trip.access_token}`;
  const w = await aiJSON(
    `You are the concierge voice of Ophir Stays, a small luxury vacation home collection in Durango, Colorado. Voice: short, warm, certain. No exclamation marks. Never use the word "luxury". Sign as "Casey, Ophir Stays".`,
    `Write the welcome email for a new booking. Guest first name: ${firstName(trip.guest_name)}. Home: ${home?.name || 'your home'} (${home?.area || 'Durango'}). Dates: ${fmt(trip.check_in)} to ${fmt(trip.check_out)}. Party: ${trip.adults} adults, ${trip.children} children. Package: ${PACKAGES[trip.package]}
The email must invite them to tell us about their trip at a private link (a button is added for you; do not include the URL). Explain in one sentence what we'll do with it (sizes for gear, groceries, the itinerary). 90 to 140 words.
JSON: {"subject": "...", "body": "plain text, paragraphs separated by blank lines"}`, 800);
  const html = emailShell(paras(w.body) + button(link, 'Plan your trip'));
  if (trip.guest_email) await sendEmail({ to: trip.guest_email, subject: w.subject, html, replyTo: env('OWNER_INBOX') });
  await db.insert('messages', [{ trip_id: trip.id, channel: 'email', direction: 'outbound', subject: w.subject, body: w.body, status: trip.guest_email ? 'sent' : 'draft', sent_at: trip.guest_email ? new Date().toISOString() : null }]);
}

export async function planTrip(tripId) {
  const t = await loadTrip(`id=eq.${tripId}`);
  if (!t) throw new Error('Trip not found');
  const { trip, home, party, answers } = t;
  const weather = await forecast(trip.check_in, trip.check_out);
  const plan = await aiJSON(
    `You are the head concierge of Ophir Stays in Durango, Colorado. You plan trips with local precision and create the behind-the-scenes task list for the team. ${DURANGO_NOTES} ${TEAM}
Rules: Respect the guest's package: only promise and create booking tasks for what their package includes; for anything else, list it as a suggestion in the itinerary and note it is available as an upgrade. Use the forecast when given: move outdoor plans away from storms, put riding in the morning in summer, flag powder days. Keep days relaxed, 2 to 4 items per day. Arrival day: settle in. Departure day: checkout by 10am. Task due times must be before the moment they are needed, in ISO 8601 with -06:00 or -07:00 Denver offset. Every gear task must list each person's size (height, boot size, level). Never invent prices for partners.`,
    `Trip: ${home?.name || 'Home'} (${home?.area || 'Durango'}, sleeps ${home?.sleeps || '?'}). ${trip.check_in} to ${trip.check_out}. Package: ${trip.package}: ${PACKAGES[trip.package]}
Party: ${JSON.stringify(party.map(({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes }) => ({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes })))}
Answers: ${JSON.stringify(answers ? { interests: answers.interests, pace: answers.pace, groceries: answers.groceries, dietary: answers.dietary, coffee: answers.coffee, arrival_time: answers.arrival_time, celebrations: answers.celebrations, notes: answers.notes } : {})}
Forecast (may be empty if dates are far out): ${JSON.stringify(weather)}
Return JSON: {"summary": "2 sentences for Casey on the shape of this trip and anything to watch",
"days": [{"date": "YYYY-MM-DD", "items": [{"time": "9:00 AM", "title": "...", "details": "1-2 sentences for the guest", "kind": "ski|bike|dine|spa|golf|river|hike|rest|arrival|departure|town", "partner": "", "weather_note": ""}]}],
"tasks": [{"title": "...", "assignee": "one of the team names", "due_at": "ISO"}],
"upsell": "one sentence suggesting a relevant upgrade, or empty string"}`, 6000);

  await db.remove('itinerary_items', `trip_id=eq.${trip.id}`);
  await db.remove('tasks', `trip_id=eq.${trip.id}&created_by=eq.ai&approved=eq.false`);
  const items = (plan.days || []).flatMap((d) => (d.items || []).map((it, i) => ({ trip_id: trip.id, day: d.date, start_time: it.time || null, title: it.title, details: it.details || null, kind: it.kind || null, partner: it.partner || null, weather_note: it.weather_note || null, position: i })));
  if (items.length) await db.insert('itinerary_items', items);
  const tasks = (plan.tasks || []).map((k) => ({ trip_id: trip.id, title: k.title, assignee: k.assignee || 'Casey', due_at: k.due_at || null, created_by: 'ai', approved: false }));
  if (tasks.length) await db.insert('tasks', tasks);
  await db.update('trips', `id=eq.${trip.id}`, { status: 'plan_ready' });
  await db.insert('messages', [{ trip_id: trip.id, channel: 'app', direction: 'outbound', subject: 'Plan summary', body: `${plan.summary || ''}${plan.upsell ? '\n\nUpsell: ' + plan.upsell : ''}`, status: 'draft' }]);

  const inbox = env('OWNER_INBOX');
  if (inbox) await sendEmail({ to: inbox, subject: `Plan ready to approve: ${trip.guest_name}, ${trip.check_in}`,
    html: emailShell(`<p><strong>${esc(trip.guest_name)}</strong> · ${esc(home?.name || '')} · ${fmt(trip.check_in)} to ${fmt(trip.check_out)}</p>${paras(plan.summary || '')}<p>${items.length} itinerary items and ${tasks.length} team tasks are waiting for you.</p>${button(`${SITE}/admin`, 'Review and approve')}`) });
  return { items: items.length, tasks: tasks.length };
}

export async function approveTrip(tripId) {
  const t = await loadTrip(`id=eq.${tripId}`);
  if (!t) throw new Error('Trip not found');
  await db.update('trips', `id=eq.${tripId}`, { status: 'approved' });
  await db.update('tasks', `trip_id=eq.${tripId}&approved=eq.false`, { approved: true });
  const link = `${SITE}/trip/${t.trip.access_token}`;
  const body = `${firstName(t.trip.guest_name)},\n\nYour trip is planned. Every day is in your trip page, built around the forecast, and we'll move things if the weather does.\n\nEverything you asked for will be ready when you walk in. If anything changes, just reply to this email.\n\nCasey, Ophir Stays`;
  if (t.trip.guest_email) await sendEmail({ to: t.trip.guest_email, subject: 'Your Durango trip is ready', html: emailShell(paras(body) + button(link, 'See your trip')), replyTo: env('OWNER_INBOX') });
  await db.insert('messages', [{ trip_id: tripId, channel: 'email', direction: 'outbound', subject: 'Your Durango trip is ready', body, status: t.trip.guest_email ? 'sent' : 'draft', sent_at: new Date().toISOString() }]);
}

export function isAdmin(req) {
  const pw = env('ADMIN_PASSWORD');
  return pw && (req.headers['x-admin-key'] || '') === pw;
}
