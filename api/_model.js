// Ophir earnings estimate model. Pure functions: inputs in, numbers out. Every figure is a planning assumption
// that Casey reviews before a report is sent; adr_adjust / occ_adjust are his overrides.
import { COMPS } from './_comps.js';

export const AREAS = {
  downtown: { label: 'Downtown Durango', profile: 'town', adr: 1.0 },
  valley: { label: 'Animas Valley', profile: 'town', adr: 1.05 },
  purgatory: { label: 'Purgatory and Durango Mountain', profile: 'mountain', adr: 1.0 },
  vallecito: { label: 'Vallecito Lake and Bayfield', profile: 'lake', adr: 0.9 },
  west: { label: 'West of Durango (Hesperus, Lightner Creek)', profile: 'town', adr: 0.9 },
  east: { label: 'East of Durango (Florida Road, Florida Mesa)', profile: 'town', adr: 0.95 },
  other: { label: 'La Plata County', profile: 'town', adr: 0.9 },
};
const MONTHS = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
const DAYS = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31];
// Share of nights booked and nightly-rate index (1 = the home's average rate) by month.
const PROFILES = {
  town: { occ: [.36, .40, .42, .08, .18, .58, .74, .66, .50, .26, .08, .45], rate: [.87, .88, .91, .54, .63, 1.05, 1.17, 1.12, 1.0, .74, .57, 1.22] },
  mountain: { occ: [.62, .66, .68, .10, .08, .40, .55, .48, .35, .15, .10, .60], rate: [1.15, 1.15, 1.2, .6, .55, .8, .9, .85, .75, .6, .6, 1.4] },
  lake: { occ: [.10, .10, .12, .06, .25, .62, .80, .72, .45, .18, .05, .15], rate: [.7, .7, .7, .6, .85, 1.1, 1.25, 1.2, .95, .75, .6, .9] },
};
const BASE_ADR = { 1: 190, 2: 270, 3: 400, 4: 560, 5: 700, 6: 860, 7: 1000 };
export const FEATURES = {
  hot_tub: { label: 'Hot tub', adr: 1.08 }, views: { label: 'Mountain views', adr: 1.05 }, water: { label: 'On the river or lake', adr: 1.08 },
  ski_in: { label: 'Ski-in, ski-out', adr: 1.12 }, gear: { label: 'Garage or gear room', adr: 1.02 }, ac: { label: 'Air conditioning', adr: 1.02 },
  game: { label: 'Game or media room', adr: 1.03 }, acreage: { label: 'Private acreage', adr: 1.03 }, pets: { label: 'Pet friendly', occ: 1.04 },
};

const r5 = (n) => Math.round(n / 5) * 5;
const r100 = (n) => Math.round(n / 100) * 100;

export function computeEstimate(e) {
  const beds = Math.max(1, Math.min(7, parseInt(e.bedrooms, 10) || 3));
  const area = AREAS[e.area] || AREAS.other;
  const prof = PROFILES[area.profile];
  const feats = (e.features || []).filter((f) => FEATURES[f]);
  let adrMult = area.adr; let occMult = beds >= 6 ? 0.92 : 1;
  feats.forEach((f) => { adrMult *= FEATURES[f].adr || 1; occMult *= FEATURES[f].occ || 1; });
  adrMult = Math.min(adrMult, 1.35 * area.adr);
  const adrAdj = Number(e.adr_adjust) || 1; const occAdj = Number(e.occ_adjust) || 1;
  const avgRate = BASE_ADR[beds] * adrMult * adrAdj;
  const months = MONTHS.map((m, i) => {
    const occ = Math.min(0.92, prof.occ[i] * occMult * occAdj);
    const nights = Math.round(DAYS[i] * occ);
    const rate = r5(avgRate * prof.rate[i]);
    return { m, nights, rate, rent: nights * rate, occ };
  });
  const rent = months.reduce((s, x) => s + x.rent, 0);
  const nights = months.reduce((s, x) => s + x.nights, 0);
  const stays = Math.round(nights / 4.3);
  const condo = e.home_type === 'condo';
  const costs = [
    ['Utilities, Wi-Fi, trash', r100((3600 + 600 * beds) * (condo ? 0.8 : 1))],
    ['Guest supplies', stays * 40],
    ...(feats.includes('hot_tub') ? [['Hot tub service', 1200]] : []),
    ...(condo ? [] : [['Snow removal', area.profile === 'lake' ? 800 : 1500]]),
    ['Repairs reserve', r100(900 + 400 * beds)],
    ['Added STR insurance', condo ? 900 : 1500],
  ];
  const running = costs.reduce((s, c) => s + c[1], 0);
  // Booking-channel fees, owner side. Planning mix: 50% Airbnb, 25% Vrbo, 25% direct.
  // Airbnb host-only fee 15.5% of rent + cleaning (mandatory for software-connected hosts since Oct 2025).
  // Vrbo 5% commission on rent + cleaning, plus 3% processing on the full charge incl. ~6.9% tax.
  // Direct: Stripe 2.9% + $0.30 on the full charge incl. tax.
  const clean = 100 + 50 * beds;
  const TAX = 1.069;
  const mix = { airbnb: 0.5, vrbo: 0.25, direct: 0.25 };
  const perStay = (rent / Math.max(stays, 1)) + clean;
  const feeAirbnb = perStay * 0.155;
  const feeVrbo = perStay * 0.05 + perStay * TAX * 0.03;
  const feeDirect = perStay * TAX * 0.029 + 0.30;
  const platform = stays ? Math.round(stays * (mix.airbnb * feeAirbnb + mix.vrbo * feeVrbo + mix.direct * feeDirect)) : 0;
  const platformPct = rent ? platform / rent : 0;
  const ophir = Math.round(rent * 0.22);
  const keep = rent - platform - ophir - running;
  const keepAt = (fee) => Math.round(rent - platform - rent * fee - running);
  const lo = rent * 0.82, hi = rent * 1.18;
  const week = (i) => Math.round(7 * months[i].occ * months[i].rate / 100) * 100;
  const comps = COMPS.map((c) => ({ ...c, score: (c.group === e.area ? 0 : 2) + Math.abs(c.bedrooms - beds) }))
    .filter((c) => Math.abs(c.bedrooms - beds) <= 1).sort((a, b) => a.score - b.score).slice(0, 5).map(({ score, group, ...c }) => c);
  return {
    months: months.map(({ occ, ...x }) => x), rent, nights, stays, avg_rate: nights ? Math.round(rent / nights) : 0, occupancy: Math.round(nights / 365 * 100),
    range: [r100(lo), r100(hi)], platform, ophir, costs, running, keep,
    keep_range: [r100(lo * (1 - platformPct - 0.22) - running), r100(hi * (1 - platformPct - 0.22) - running)],
    platform_pct: Math.round(platformPct * 1000) / 10,
    managers: [['Ophir, 22%', keepAt(0.22)], ['Typical, 28%', keepAt(0.28)], ['Resort program, 35%', keepAt(0.35)]],
    weeks: [['A week in July', week(6)], ['A week in September', week(8)], ['A week in February', week(1)], ['A week in April', week(3)]],
    comps, area_label: area.label, profile: area.profile, beds,
  };
}
