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
// Structured output: offer a "respond" tool (the model may not allow forcing it), parse tool input or JSON text,
// and retry once with a plain-JSON instruction if neither comes back.
async function callForJSON(system, user, maxTokens, withTool) {
  const key = env('ANTHROPIC_API_KEY');
  if (!key) throw new Error('Anthropic not configured');
  const body = {
    model: env('ANTHROPIC_MODEL') || 'claude-sonnet-5-5', max_tokens: Math.max(maxTokens, 8000), system,
    messages: [{ role: 'user', content: user + (withTool
      ? '\n\nGive your answer by calling the respond tool with the JSON fields described above.'
      : '\n\nReply with only the JSON object described above. No other text.') }],
  };
  if (withTool) body.tools = [{ name: 'respond', description: 'Return the answer as structured fields.', input_schema: { type: 'object', additionalProperties: true } }];
  const r = await fetch('https://api.anthropic.com/v1/messages', {
    method: 'POST', headers: { 'x-api-key': key, 'anthropic-version': '2023-06-01', 'content-type': 'application/json' }, body: JSON.stringify(body),
  });
  const data = await r.json();
  if (!r.ok) throw new Error(`AI ${r.status}: ${JSON.stringify(data).slice(0, 300)}`);
  const tool = (data.content || []).find((b) => b.type === 'tool_use');
  if (tool && tool.input && Object.keys(tool.input).length) return tool.input;
  const text = (data.content || []).filter((b) => b.type === 'text').map((b) => b.text).join('');
  const s = text.indexOf('{'), e = text.lastIndexOf('}');
  if (s >= 0 && e > s) { try { return JSON.parse(text.slice(s, e + 1)); } catch (_) { /* fall through */ } }
  console.error('AI no JSON', data.stop_reason, JSON.stringify(data.content).slice(0, 800));
  return { __fail: data.stop_reason || 'unknown' };
}
export async function aiJSON(system, user, maxTokens = 4000) {
  let out = await callForJSON(system, user, maxTokens, true);
  if (out.__fail) out = await callForJSON(system, user, maxTokens, false);
  if (out.__fail) throw new Error(`AI returned no JSON (stop: ${out.__fail})`);
  return out;
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
  stay: 'The Stay (included with every booking): inspected home, hotel-grade linens, a welcome kit (local coffee, Ophir lip balm and sticker, local chocolate, and a Casey\'s Durango card with a 10% return-guest code for ophirstays.com), house guide in the app, weather-aware ideas, a local host by text who replies within 15 minutes from 7am to 10pm, urgent issues any hour.',
  arranged: 'The Arranged Stay ($395 for up to 6 guests, $595 for 7 to 12): everything in The Stay, plus two Ophir tumblers to keep, a planning call, skis and boots sized to each guest and waiting in the gear room, bikes fitted and delivered, lift tickets/guides/rafting/fly fishing booked, dinner reservations held, with the first round on the house at partner restaurants that offer it, an itinerary that moves with the weather. The package fee covers planning and booking only: ski and bike rentals, lift tickets, guides, rafting and fly fishing are paid separately at partner rates.',
  private: 'The Private Stay ($1,950 up to 5 nights, $295 per extra night): everything in The Arranged Stay, plus groceries shopped and the fridge stocked, fire laid and wine chosen, a dedicated host on call, private chef/massage/sitter booked, airport transfer booked, mid-stay refresh. The package fee covers planning, booking and hosting only: groceries (at cost), the chef, therapist, sitter, driver and rentals are paid separately at their own rates.',
};
// What each package lets the team DO (used to guard AI tasks), and what can be offered.
export const INCLUDES = {
  stay: [],
  arranged: ['gear', 'bookings', 'dinners'],
  private: ['gear', 'bookings', 'dinners', 'groceries', 'arrival_setup', 'host', 'wellness'],
};
export const OFFERS = {
  arranged: { title: 'The Arranged Stay', price: '$395 (up to 6 guests), $595 for 7 to 12', cents: 39500, cents_large: 59500, blurb: 'We plan and book everything: gear sized and waiting, guides, tickets and tables.' },
  private: { title: 'The Private Stay', price: '$1,950 up to 5 nights', cents: 195000, blurb: 'Your own host. Groceries stocked, fire laid, chef or massage arranged.' },
  addon_fridge: { title: 'A stocked fridge', price: '$95 plus groceries', cents: 9500, blurb: 'Your grocery list, shopped the morning you arrive.', grants: 'groceries' },
  addon_arrival: { title: 'Arrival setup', price: '$95 plus wine at cost', cents: 9500, blurb: 'Fire laid, wine chosen, flowers on the table.', grants: 'arrival_setup' },
  addon_midclean: { title: 'Mid-stay clean', price: '$195', cents: 19500, blurb: 'Fresh linens and towels, a full clean and a restock, halfway through.' },
  addon_early: { title: 'Early check-in', price: '$95', cents: 9500, blurb: 'In the door by noon, when the calendar allows.' },
  addon_late: { title: 'Late checkout', price: '$95', cents: 9500, blurb: 'Stay until 1pm, when the calendar allows.' },
  addon_gear: { title: 'Skis or bikes, fitted and delivered', price: '$45 plus rental', cents: 4500, blurb: 'Sized to each guest and waiting in the gear room.', grants: 'gear' },
  massage: { title: 'In-home massage', price: 'Priced on request', blurb: 'A licensed therapist at the house, after a day outside.' },
  golf: { title: 'A round of golf', price: 'Priced on request', blurb: 'Tee time held, clubs and cart ready.' },
  guide: { title: 'A private guide', price: 'Priced on request', blurb: 'Fly fishing, a guided ride or a backcountry hike with a local.' },
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
  w.body = String(w.body || '').replace(/!+/g, '.'); w.subject = String(w.subject || 'Your Durango trip').replace(/!+/g, '');
  const html = emailShell(paras(w.body) + button(link, 'Plan your trip'));
  if (trip.guest_email) await sendEmail({ to: trip.guest_email, subject: w.subject, html, replyTo: env('OWNER_INBOX') });
  await db.insert('messages', [{ trip_id: trip.id, channel: 'email', direction: 'outbound', subject: w.subject, body: w.body, status: trip.guest_email ? 'sent' : 'draft', sent_at: trip.guest_email ? new Date().toISOString() : null }]);
}

const WX = (c) => c == null ? '' : c === 0 ? 'Sunny' : c <= 2 ? 'Partly cloudy' : c === 3 ? 'Cloudy' : c <= 48 ? 'Fog' : c <= 57 ? 'Drizzle' : c <= 67 ? 'Rain' : c <= 77 ? 'Snow' : c <= 82 ? 'Showers' : c <= 86 ? 'Snow showers' : 'Thunderstorms';
const noBang = (t) => (t == null ? t : String(t).replace(/!+/g, '.').replace(/\.\.+/g, '.'));

export async function paidAddons(tripId) {
  const paid = await db.select('payments', `trip_id=eq.${tripId}&status=eq.paid`);
  return paid.map((p) => p.item);
}

export async function planTrip(tripId) {
  const t = await loadTrip(`id=eq.${tripId}`);
  if (!t) throw new Error('Trip not found');
  const { trip, home, party, answers } = t;
  const addons = await paidAddons(trip.id);
  const granted = new Set([...(INCLUDES[trip.package] || []), ...addons.map((k) => OFFERS[k]?.grants).filter(Boolean)]);
  const weather = await forecast(trip.check_in, trip.check_out);
  const restaurants = await db.select('restaurants', 'active=eq.true&order=name').catch(() => []);
  const dining = (answers && answers.raw && answers.raw.dining) || {};
  const offerKeys = Object.keys(OFFERS).filter((k) => !(k === 'arranged' && trip.package !== 'stay') && !(k === 'private' && trip.package === 'private') && !addons.includes(k)
    && !(OFFERS[k].grants && granted.has(OFFERS[k].grants)));
  const plan = await aiJSON(
    `You are the head concierge of Ophir Stays in Durango, Colorado. You plan trips with local precision and create the behind-the-scenes task list for the team. ${DURANGO_NOTES} ${TEAM}
VOICE for anything the guest reads: short, warm, certain, understated. Never use exclamation marks. Never say "luxury". Never mention packages, prices, upgrades or what is "not included" inside the itinerary.
PACKAGE RULES (strict):
- What Ophir will actually do for this guest: ${[...granted].join(', ') || 'nothing beyond the home and local tips'}.
- Only promise or create tasks for those. "gear" = sizing and delivering skis/boots/bikes. "bookings" = guides, tickets, rafting, fishing, golf. "dinners" = holding tables and the first round. "groceries" = shopping and stocking the fridge. "arrival_setup" = fire, wine, flowers. "wellness" = massage, chef, sitter.
- Anything the guest would enjoy that is NOT in that list: do not promise it and create no task for it. Put it in the itinerary as a plain idea (e.g. "Ride Horse Gulch", "Dinner on Main Avenue"), and instead add a matching offer key to "offers".
- Allowed offer keys: ${offerKeys.join(', ') || 'none'}.
Use the forecast when given: move outdoor plans away from storms, put riding in the morning in summer, flag powder days. If a resort or activity is closed for the season, plan around it and say why in the summary. Keep days relaxed, 2 to 4 items. Arrival day: settle in. Departure day: checkout by 10am. Task due times must be before they are needed, ISO 8601 with Denver offset. Every gear task lists each person's height, weight, boot size and level.
DINNERS: Choose restaurants ONLY from Casey's list below, matching the guest's cuisine, atmosphere, budget, kids and dietary needs; never invent a restaurant. Book only as many dinners as the guest asked for. Each dinner task must read like: "Book <Restaurant>, <Day Mon D> <time>, party of N (X children), <occasion>, <seating/atmosphere request>, <dietary needs>. Book via <method> <phone or url>." Do not ask the restaurant to arrange anything. If that restaurant has first_round true, ALSO create a separate task assigned to "Casey" with needs "dinners", due the day before arrival: "Pack first-round card: <Restaurant>, $<10 x adults, rounded up to 20 or 40> (<N> adults)". Add a ready_list line like "Your first round at <Restaurant>, on us. The card is on the counter." Restaurants without first_round get no card and no first-round promise. Use the restaurant name in the itinerary title (e.g. "Dinner at <Restaurant>"). If the list is empty, create one task "Choose and book dinner: <guest's preferences>" for Casey and keep the itinerary title generic.
Casey's restaurant list: ${JSON.stringify(restaurants.map(({ name, cuisine, vibe, price, kid_friendly, book_via, phone, booking_url, first_round, notes }) => ({ name, cuisine, vibe, price: price ? '$'.repeat(price) : null, kid_friendly, book_via, phone, booking_url, first_round, notes })))}`,
    `Trip: ${home?.name || 'Home'} (${home?.area || 'Durango'}, sleeps ${home?.sleeps || '?'}). ${trip.check_in} to ${trip.check_out}. Package: ${trip.package}. Paid add-ons: ${addons.join(', ') || 'none'}.
Party: ${JSON.stringify(party.map(({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes }) => ({ name, age_group, height_cm, weight_kg, boot_size, ski_level, bike_level, notes })))}
Answers: ${JSON.stringify(answers ? { interests: answers.interests, pace: answers.pace, groceries: answers.groceries, dietary: answers.dietary, coffee: answers.coffee, arrival_time: answers.arrival_time, celebrations: answers.celebrations, notes: answers.notes } : {})}
Dining preferences: ${JSON.stringify(dining)}
Forecast (may be empty if dates are far out): ${JSON.stringify(weather)}
Return JSON: {"summary": "2-4 sentences for Casey: shape of the trip, anything to confirm, anything closed or risky",
"ready_list": ["what the guest will find waiting on arrival, ONLY things Ophir will do, e.g. 'Bikes fitted for John and Loic in the gear room'; 3 to 6 short lines"],
"days": [{"date": "YYYY-MM-DD", "items": [{"time": "9:00 AM", "title": "...", "details": "1-2 sentences for the guest", "kind": "ski|bike|dine|spa|golf|river|hike|rest|arrival|departure|town", "place": "short place name for a map search, or empty", "weather_note": ""}]}],
"tasks": [{"title": "...", "assignee": "one of the team names", "due_at": "ISO", "needs": "one of: gear, bookings, dinners, groceries, arrival_setup, wellness, house"}],
"offers": [{"key": "one allowed offer key", "reason": "one short sentence tied to this guest, e.g. 'For your anniversary evening'"}]}`, 6000);

  // Guard: drop any task the package doesn't cover (house tasks like cleaning are always allowed).
  const tasks = (plan.tasks || []).filter((k) => !k.needs || k.needs === 'house' || granted.has(k.needs))
    .map((k) => ({ trip_id: trip.id, title: k.title, assignee: k.assignee || 'Casey', due_at: k.due_at || null, created_by: 'ai', approved: false }));
  const items = (plan.days || []).flatMap((d) => (d.items || []).map((it, i) => ({ trip_id: trip.id, day: d.date, start_time: it.time || null, title: noBang(it.title),
    details: noBang(it.details) || null, kind: it.kind || null, partner: it.place || null, weather_note: noBang(it.weather_note) || null, position: i })));
  const offers = (plan.offers || []).filter((o) => offerKeys.includes(o.key)).filter((o, i, a) => a.findIndex((x) => x.key === o.key) === i).slice(0, 4)
    .map((o) => ({ key: o.key, ...OFFERS[o.key], reason: noBang(o.reason || '') }));
  const ready = (plan.ready_list || []).map(noBang).slice(0, 6);
  const wx = weather.map((w) => ({ date: w.date, label: WX(w.code), high: w.high, low: w.low, precip: w.precip_chance, snow: w.snow_in }));

  await db.remove('itinerary_items', `trip_id=eq.${trip.id}`);
  await db.remove('tasks', `trip_id=eq.${trip.id}&created_by=eq.ai&approved=eq.false`);
  if (items.length) await db.insert('itinerary_items', items);
  if (tasks.length) await db.insert('tasks', tasks);
  await db.update('trips', `id=eq.${trip.id}`, { status: 'plan_ready', offers, ready_list: ready, weather: wx, plan_summary: plan.summary || null });
  await db.insert('messages', [{ trip_id: trip.id, channel: 'app', direction: 'outbound', subject: 'Plan summary', body: plan.summary || '', status: 'draft' }]);

  const inbox = env('OWNER_INBOX');
  if (inbox) await sendEmail({ to: inbox, subject: `Plan ready to approve: ${trip.guest_name}, ${trip.check_in}`,
    html: emailShell(`<p><strong>${esc(trip.guest_name)}</strong> · ${esc(home?.name || '')} · ${fmt(trip.check_in)} to ${fmt(trip.check_out)}</p>${paras(plan.summary || '')}<p>${items.length} itinerary items, ${tasks.length} team tasks and ${offers.length} offers are waiting for you.</p>${button(`${SITE}/admin`, 'Review and approve')}`) });
  return { items: items.length, tasks: tasks.length, offers: offers.length };
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

// ---------- Stripe ----------
export function partyOf(trip) { return (Number(trip.adults) || 0) + (Number(trip.children) || 0); }
export function arrangedCents(trip) { return partyOf(trip) > 6 ? OFFERS.arranged.cents_large : OFFERS.arranged.cents; }
export function nightsOf(trip) { return Math.round((new Date(trip.check_out) - new Date(trip.check_in)) / 864e5); }
// What the guest pays today for an item, given their current package.
export function priceFor(key, trip) {
  const o = OFFERS[key];
  if (!o || !o.cents) return null;
  if (key === 'arranged') return { cents: arrangedCents(trip), label: o.title };
  if (key === 'private') {
    const extra = Math.max(0, nightsOf(trip) - 5) * 29500;
    const credit = trip.package === 'arranged' ? arrangedCents(trip) : 0;
    return { cents: o.cents + extra - credit, label: credit ? 'The Private Stay (upgrade from Arranged)' : 'The Private Stay' };
  }
  return { cents: o.cents, label: o.title };
}
export async function stripe(path, params) {
  const key = env('STRIPE_SECRET_KEY');
  if (!key) throw new Error('Stripe not configured');
  const body = new URLSearchParams();
  const add = (k, v) => { if (v === undefined || v === null) return; if (typeof v === 'object') for (const [kk, vv] of Object.entries(v)) add(`${k}[${kk}]`, vv); else body.append(k, String(v)); };
  for (const [k, v] of Object.entries(params || {})) add(k, v);
  const r = await fetch(`https://api.stripe.com/v1/${path}`, { method: 'POST', headers: { Authorization: `Bearer ${key}`, 'Content-Type': 'application/x-www-form-urlencoded' }, body });
  const data = await r.json();
  if (!r.ok) throw new Error(`Stripe ${r.status}: ${data.error?.message || 'error'}`);
  return data;
}

// ---------- House manual (one per home; edited in admin, shown on the guest trip page, used by Ask Ophir) ----------
export const MANUAL_SECTIONS = [
  { key: 'arrival', label: 'Arrival and parking', hint: 'Directions from Hwy 550 or 160, driveway, where to park, winter road notes, how the lock works' },
  { key: 'heat', label: 'Heat and thermostat', hint: 'Thermostat location and settings, radiant floors, keep heat at or above 60 in winter' },
  { key: 'fireplace', label: 'Fireplace', hint: 'Gas or wood, how to turn it on and off, firewood location' },
  { key: 'hot_tub', label: 'Hot tub', hint: 'Cover, controls, jets, rules (no glass, kids supervised), what to do if it trips' },
  { key: 'kitchen', label: 'Kitchen and coffee', hint: 'Coffee maker, dishwasher pods, grill and propane, anything unusual' },
  { key: 'tv_wifi', label: 'TV and Wi-Fi', hint: 'Remotes, streaming logins, where the router is' },
  { key: 'laundry', label: 'Laundry', hint: 'Washer and dryer location, detergent' },
  { key: 'trash', label: 'Trash, recycling and bears', hint: 'Bear-proof cans, pickup day, never leave trash outside or in vehicles' },
  { key: 'rules', label: 'House rules', hint: 'Quiet hours, maximum guests, pets, no smoking, parking limits, HOA rules guests must follow' },
  { key: 'checkout', label: 'Checkout', hint: 'Checkout time and steps: dishes, towels, trash, thermostat, lock the door' },
  { key: 'shutoffs', label: 'Water, gas and power shutoffs', hint: 'Location of the main water shutoff, gas shutoff and breaker panel' },
  { key: 'emergency', label: 'Emergency and medical', hint: 'Nearest ER (Mercy Regional Medical Center, 1010 Three Springs Blvd), urgent care, 911 address to give' },
];
export function cleanManual(m) {
  const out = {};
  for (const { key } of MANUAL_SECTIONS) { const v = String((m || {})[key] || '').trim().slice(0, 2000); if (v) out[key] = v; }
  return out;
}
export function manualForGuest(m) {
  return MANUAL_SECTIONS.filter((x) => m && m[x.key]).map((x) => ({ label: x.label, text: m[x.key] }));
}
