-- Ophir Partner Hosts: run once in the Supabase SQL editor.
-- A Partner Host home is run by its own owner on Airbnb or Vrbo. Ophir plans and books the guest's trip
-- (gear, guides, dinners) and pays the host a share of what their guests buy.

alter table homes add column if not exists partner boolean not null default false;
alter table homes add column if not exists partner_status text check (partner_status in ('applied','active','paused','declined'));
alter table homes add column if not exists partner_rate numeric not null default 0.10;   -- host's share of guest purchases
alter table homes add column if not exists host_name text;
alter table homes add column if not exists host_email text;
alter table homes add column if not exists host_phone text;
alter table homes add column if not exists listing_url text;
alter table homes add column if not exists partner_notes text;

-- Guests who start from a Partner Host link are trips with source 'partner'.
alter table trips drop constraint if exists trips_source_check;
alter table trips add constraint trips_source_check check (source in ('airbnb','vrbo','direct','simulated','other','partner'));

-- To approve a host: Table editor -> homes -> set partner_status = 'active'.
-- Their guest link is then https://ophirstays.com/h/<slug>

-- What each Partner Host has earned, by month: their share of Ophir's own packages and add-ons.
-- Pass-through charges (rentals, lift tickets, guides billed at partner rates, item charge_...) are excluded,
-- since Ophir earns no margin on them. Paid items only; refunds drop out automatically.
create or replace view partner_payouts as
select
  h.slug,
  h.name as home,
  h.host_name,
  h.host_email,
  date_trunc('month', p.created_at)::date as month,
  count(distinct t.id) as trips,
  count(p.id) as purchases,
  round(sum(p.amount_cents) / 100.0, 2) as guest_spend,
  h.partner_rate,
  round(sum(p.amount_cents) * h.partner_rate / 100.0, 2) as host_payout
from payments p
join trips t on t.id = p.trip_id
join homes h on h.id = t.home_id
where h.partner and p.status = 'paid' and p.item not like 'charge\_%'
group by h.slug, h.name, h.host_name, h.host_email, h.partner_rate, date_trunc('month', p.created_at)
order by month desc, host_payout desc;
