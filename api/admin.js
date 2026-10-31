// Admin API for Casey. Every call needs header x-admin-key = ADMIN_PASSWORD.
// POST { action: 'list' | 'detail' | 'approve' | 'replan' | 'simulate' | 'task' | 'resend_welcome' | 'send_upgrade' | 'preview_upgrade', ... }
import { db, json, readBody, isAdmin, loadTrip, createTrip, planTrip, approveTrip, sendWelcome, sendUpgradeOffer, upgradeEmailHtml, menuFor, paidAddons, sendEmail, emailShell, esc, SITE, MANUAL_SECTIONS, cleanManual } from './_lib.js';
import { computeEstimate, AREAS, FEATURES } from './_model.js';

const money = (n) => '$' + Math.round(n).toLocaleString('en-US');

const addDays = (n) => { const d = new Date(); d.setDate(d.getDate() + n); return d.toISOString().slice(0, 10); };
const SAMPLE_NAMES = ['Taylor Brooks', 'Morgan Hale', 'Jordan Pierce', 'Avery Collins', 'Riley Dawson'];

export default async function handler(req, res) {
  if (req.method !== 'POST') return json(res, 405, { error: 'Method not allowed' });
  if (!isAdmin(req)) return json(res, 401, { error: 'Wrong password' });
  const b = readBody(req);
  try {
    switch (b.action) {
      case 'list': {
        const trips = await db.select('trips', 'select=id,guest_name,guest_email,check_in,check_out,adults,children,package,status,source,created_at,homes(name)&order=check_in.asc&limit=200');
        const tasks = await db.select('tasks', 'select=id,trip_id,title,assignee,due_at,status,approved&status=eq.open&order=due_at.asc&limit=300');
        // $10 per completed stay, by the guest's chosen cause (unchosen counts toward Durango Trails).
        const today = new Date().toLocaleDateString('en-CA', { timeZone: 'America/Denver' });
        let causes = [];
        try { causes = await db.select('trips', `select=cause&status=neq.cancelled&check_out=lte.${today}`); } catch (e) { causes = []; }
        const give = { trails: 0, adaptive: 0, housing: 0 };
        causes.forEach((t) => { give[t.cause && give[t.cause] !== undefined ? t.cause : 'trails'] += 10; });
        return json(res, 200, { trips, tasks, give });
      }
      case 'detail': {
        const t = await loadTrip(`id=eq.${b.id}`);
        if (!t) return json(res, 404, { error: 'Not found' });
        const messages = await db.select('messages', `trip_id=eq.${b.id}&order=created_at.desc&limit=20`);
        const payments = await db.select('payments', `trip_id=eq.${b.id}&order=created_at.desc`);
        const charges = await db.select('charges', `trip_id=eq.${b.id}&order=created_at.desc`);
        return json(res, 200, { ...t, messages, payments, charges, link: `/trip/${t.trip.access_token}` });
      }
      case 'approve': await approveTrip(b.id); return json(res, 200, { ok: true });
      case 'replan': return json(res, 200, { ok: true, ...(await planTrip(b.id)) });
      case 'resend_welcome': { const t = await loadTrip(`id=eq.${b.id}`); await sendWelcome(t.trip, t.home); return json(res, 200, { ok: true }); }
      case 'send_upgrade': { const t = await loadTrip(`id=eq.${b.id}`); return json(res, 200, await sendUpgradeOffer(t.trip, t.home)); }
      case 'preview_upgrade': { const t = await loadTrip(`id=eq.${b.id}`); return json(res, 200, { html: upgradeEmailHtml(t.trip, t.home, menuFor(t.trip, await paidAddons(t.trip.id))) }); }
      case 'task': {
        const patch = {};
        if (b.status) patch.status = b.status;
        if (b.assignee) patch.assignee = String(b.assignee).slice(0, 60);
        await db.update('tasks', `id=eq.${b.id}`, patch);
        return json(res, 200, { ok: true });
      }
      case 'simulate': {
        const name = SAMPLE_NAMES[Math.floor(Math.random() * SAMPLE_NAMES.length)];
        const start = Number.isFinite(+b.days_out) ? +b.days_out : 10;
        const trip = await createTrip({
          source: 'simulated', external_id: `SIM-${Date.now()}`, guest_name: name,
          guest_email: b.email || process.env.OWNER_INBOX, check_in: addDays(start), check_out: addDays(start + 4),
          adults: 2, children: 2, package: ['stay', 'arranged', 'private'].includes(b.package) ? b.package : 'arranged',
        });
        return json(res, 200, { ok: true, id: trip.id, link: `/trip/${trip.access_token}` });
      }
      case 'charge_create': {
        const t = await loadTrip(`id=eq.${b.id}`);
        if (!t) return json(res, 404, { error: 'Not found' });
        const title = String(b.title || '').trim().slice(0, 80);
        const cents = Math.round(parseFloat(String(b.amount || '').replace(/[$,]/g, '')) * 100);
        if (!title || !(cents >= 100 && cents <= 2000000)) return json(res, 400, { error: 'Add an item name and an amount between $1 and $20,000.' });
        const [c] = await db.insert('charges', [{ trip_id: t.trip.id, title, note: String(b.note || '').trim().slice(0, 300) || null, amount_cents: cents }]);
        if (t.trip.guest_email && b.notify !== false) {
          const link = `${SITE}/trip/${t.trip.access_token}`;
          await sendEmail({ to: t.trip.guest_email, subject: `For your Durango trip: ${title}`,
            html: emailShell(`<p>Hi ${esc(String(t.trip.guest_name).split(/\s+/)[0])},</p><p>${esc(title)} is arranged and held for you${c.note ? `: ${esc(c.note)}` : '.'}</p><p><strong>$${(cents / 100).toFixed(2)}</strong>. Confirm it on your trip page and it's done.</p><p><a href="${link}">Open your trip</a></p>`) });
        }
        return json(res, 200, { ok: true, charge: c });
      }
      case 'charge_void': await db.update('charges', `id=eq.${b.charge_id}&status=eq.open`, { status: 'void' }); return json(res, 200, { ok: true });
      case 'homes': return json(res, 200, { homes: await db.select('homes', 'order=name'), sections: MANUAL_SECTIONS });
      case 'home_save': {
        const h = b.home || {};
        const name = String(h.name || '').trim().slice(0, 80);
        if (!name) return json(res, 400, { error: 'Name required' });
        const int = (v) => (v === '' || v == null || !Number.isFinite(+v) ? null : Math.round(+v));
        const row = { name, slug: (String(h.slug || '').trim() || name).toLowerCase().replace(/[^a-z0-9]+/g, '-').replace(/^-|-$/g, '').slice(0, 60),
          area: (h.area || '').slice(0, 60) || null, address: (h.address || '').slice(0, 160) || null,
          beds: int(h.beds), baths: h.baths === '' || h.baths == null || !Number.isFinite(+h.baths) ? null : +h.baths, sleeps: int(h.sleeps),
          door_code: (h.door_code || '').slice(0, 40) || null, wifi_name: (h.wifi_name || '').slice(0, 60) || null, wifi_password: (h.wifi_password || '').slice(0, 60) || null,
          hostaway_listing_id: (String(h.hostaway_listing_id || '').trim()).slice(0, 40) || null, house_notes: (h.house_notes || '').slice(0, 2000) || null,
          manual: cleanManual(h.manual) };
        const out = h.id ? await db.update('homes', `id=eq.${h.id}`, row) : await db.insert('homes', [row]);
        return json(res, 200, { ok: true, home: out[0] });
      }
      case 'restaurants': return json(res, 200, { restaurants: await db.select('restaurants', 'order=active.desc,name') });
      case 'restaurant_save': {
        const r = b.restaurant || {};
        const row = { name: String(r.name || '').trim().slice(0, 80), cuisine: (r.cuisine || '').slice(0, 60) || null, vibe: (r.vibe || '').slice(0, 80) || null,
          price: [1, 2, 3, 4].includes(+r.price) ? +r.price : null, kid_friendly: !!r.kid_friendly, book_via: (r.book_via || '').slice(0, 40) || null,
          phone: (r.phone || '').slice(0, 30) || null, booking_url: (r.booking_url || '').slice(0, 300) || null, first_round: !!r.first_round,
          notes: (r.notes || '').slice(0, 300) || null, active: r.active !== false };
        if (!row.name) return json(res, 400, { error: 'Name required' });
        const out = r.id ? await db.update('restaurants', `id=eq.${r.id}`, row) : await db.insert('restaurants', [row]);
        return json(res, 200, { ok: true, restaurant: out[0] });
      }
      case 'estimates': return json(res, 200, { estimates: await db.select('estimates', 'select=id,token,created_at,status,requester_role,requester_name,brokerage,owner_name,address,bedrooms,area,sent_at,model->rent,model->keep&order=created_at.desc&limit=200'), areas: AREAS, features: Object.fromEntries(Object.entries(FEATURES).map(([k, v]) => [k, v.label])) });
      case 'estimate_get': return json(res, 200, { estimate: await db.one('estimates', `id=eq.${b.id}`) });
      case 'estimate_save': {
        const e = await db.one('estimates', `id=eq.${b.id}`);
        if (!e) return json(res, 404, { error: 'Not found' });
        const p = b.patch || {};
        const next = { ...e };
        if (p.adr_adjust != null) next.adr_adjust = Math.min(1.6, Math.max(0.5, Number(p.adr_adjust) || 1));
        if (p.occ_adjust != null) next.occ_adjust = Math.min(1.6, Math.max(0.5, Number(p.occ_adjust) || 1));
        if (p.bedrooms != null) next.bedrooms = Math.max(1, Math.min(10, parseInt(p.bedrooms, 10) || e.bedrooms));
        if (p.area && AREAS[p.area]) next.area = p.area;
        if (p.home_type) next.home_type = String(p.home_type).slice(0, 20);
        if (Array.isArray(p.features)) next.features = p.features.filter((f) => FEATURES[f]);
        if (p.personal_note != null) next.personal_note = String(p.personal_note).slice(0, 1500);
        if (p.owner_name != null) next.owner_name = String(p.owner_name).slice(0, 120);
        if (p.address) next.address = String(p.address).slice(0, 200);
        next.model = computeEstimate(next);
        const [row] = await db.update('estimates', `id=eq.${e.id}`, { adr_adjust: next.adr_adjust, occ_adjust: next.occ_adjust, bedrooms: next.bedrooms, area: next.area, home_type: next.home_type,
          features: next.features, personal_note: next.personal_note, owner_name: next.owner_name, address: next.address, model: next.model });
        return json(res, 200, { estimate: row });
      }
      case 'estimate_send': {
        const e = await db.one('estimates', `id=eq.${b.id}`);
        if (!e) return json(res, 404, { error: 'Not found' });
        const m = e.model, link = `${SITE}/report/${e.token}`, first = String(e.requester_name || '').split(/\s+/)[0] || 'Hello';
        const note = e.personal_note ? String(e.personal_note).split(/\n{2,}/).map((x) => `<p>${esc(x).replace(/\n/g, '<br>')}</p>`).join('') : '';
        const forWho = e.requester_role === 'agent' && e.owner_name ? `your client ${esc(e.owner_name)}'s home at ` : '';
        await sendEmail({ to: e.requester_email, replyTo: process.env.OWNER_INBOX, subject: `Your Ophir earnings estimate: ${e.address}`,
          html: emailShell(`<p>${esc(first)},</p><p>Here is the earnings estimate for ${forWho}${esc(e.address)}.</p>${note}
            <table style="width:100%;border-top:2px solid #2A2826;margin:18px 0;font-family:Arial,sans-serif"><tr>
            <td style="padding:12px 12px 0 0"><div style="font-size:11px;letter-spacing:2px;color:#6F685F">EXPECTED RENT</div><div style="font-size:30px;font-family:Georgia,serif">${money(m.rent)}</div><div style="font-size:12px;color:#6F685F">${money(m.range[0])} to ${money(m.range[1])}</div></td>
            <td style="padding:12px 0 0 12px;border-left:1px solid #E7E1D6"><div style="font-size:11px;letter-spacing:2px;color:#6F685F">THE OWNER KEEPS</div><div style="font-size:30px;font-family:Georgia,serif">${money(m.keep)}</div><div style="font-size:12px;color:#6F685F">after every fee and cost</div></td></tr></table>
            <p style="text-align:center;margin:26px 0"><a href="${link}" style="background:#B4572B;color:#fff;text-decoration:none;padding:14px 26px;font-family:Arial,sans-serif;font-size:13px;letter-spacing:.2em;text-transform:uppercase">Open the full report</a></p>
            <p style="font-size:14px;color:#6F685F">The report has the month-by-month numbers, comparable homes and our terms, and saves as a PDF from the Download button.</p>
            <p>Casey Roberts<br>Ophir Stays · 970-779-8992</p>`) });
        const [row] = await db.update('estimates', `id=eq.${e.id}`, { status: 'sent', sent_at: new Date().toISOString() });
        return json(res, 200, { estimate: row });
      }
      case 'estimate_status': {
        if (!['new', 'sent', 'signed', 'closed'].includes(b.status)) return json(res, 400, { error: 'Bad status' });
        const [row] = await db.update('estimates', `id=eq.${b.id}`, { status: b.status });
        return json(res, 200, { estimate: row });
      }
      default: return json(res, 400, { error: 'Unknown action' });
    }
  } catch (e) {
    console.error('admin api', e);
    return json(res, 500, { error: e.message });
  }
}
