-- Ophir Stays app schema. Paste into Supabase → SQL Editor → Run.
-- All tables have Row Level Security on and no public policies:
-- only the server (Vercel functions, using the secret key) can read or write.

create extension if not exists pgcrypto;

create table if not exists homes (
  id uuid primary key default gen_random_uuid(),
  slug text unique not null,
  name text not null,
  area text,
  address text,
  beds int, baths numeric, sleeps int,
  door_code text,            -- shown to guests only on arrival day
  wifi_name text, wifi_password text,
  house_notes text,
  hostaway_listing_id text unique,
  created_at timestamptz default now()
);

create table if not exists trips (
  id uuid primary key default gen_random_uuid(),
  home_id uuid references homes(id),
  source text not null check (source in ('airbnb','vrbo','direct','simulated','other')),
  external_id text,          -- booking id from Hostaway / channel
  guest_name text not null,
  guest_email text,
  guest_phone text,
  check_in date not null,
  check_out date not null,
  adults int default 2,
  children int default 0,
  package text not null default 'stay' check (package in ('stay','arranged','private')),
  status text not null default 'booked' check (status in ('booked','planning','plan_ready','approved','in_stay','complete','cancelled')),
  access_token text unique not null default encode(gen_random_bytes(18), 'hex'),  -- the guest's private link
  created_at timestamptz default now(),
  unique (source, external_id)
);

create table if not exists party_members (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid not null references trips(id) on delete cascade,
  name text not null,
  age_group text check (age_group in ('adult','teen','child')),
  height_cm int,
  weight_kg int,
  boot_size text,
  ski_level text,
  bike_level text,
  notes text
);

create table if not exists trip_answers (
  trip_id uuid primary key references trips(id) on delete cascade,
  interests text[] default '{}',
  pace text,
  groceries text,
  dietary text,
  coffee text,
  arrival_time text,
  celebrations text,
  notes text,
  raw jsonb default '{}'::jsonb,
  updated_at timestamptz default now()
);

create table if not exists itinerary_items (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid not null references trips(id) on delete cascade,
  day date not null,
  start_time text,
  title text not null,
  details text,
  kind text,                 -- ski, bike, dine, spa, golf, river, rest, arrival
  weather_note text,
  partner text,
  position int default 0,
  created_at timestamptz default now()
);

create table if not exists tasks (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid references trips(id) on delete cascade,
  title text not null,
  assignee text,             -- Casey, James Hillyer, CRC Janitorial, ski shop...
  due_at timestamptz,
  status text not null default 'open' check (status in ('open','done','cancelled')),
  created_by text default 'ai',
  approved boolean default false,
  created_at timestamptz default now()
);

create table if not exists messages (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid references trips(id) on delete cascade,
  channel text check (channel in ('email','sms','app')),
  direction text check (direction in ('outbound','inbound')),
  subject text,
  body text not null,
  status text not null default 'draft' check (status in ('draft','approved','sent','failed','received')),
  created_at timestamptz default now(),
  sent_at timestamptz
);

create table if not exists payments (
  id uuid primary key default gen_random_uuid(),
  trip_id uuid references trips(id) on delete cascade,
  item text not null,        -- arranged, private, addon_fridge, addon_arrival, addon_gear
  amount_cents int not null,
  stripe_session_id text unique,
  status text not null default 'pending' check (status in ('pending','paid','refunded','failed')),
  created_at timestamptz default now()
);

create index if not exists trips_check_in_idx on trips(check_in);
create index if not exists tasks_due_idx on tasks(due_at) where status = 'open';
create index if not exists itinerary_trip_day_idx on itinerary_items(trip_id, day, position);

-- Lock everything down: RLS on, no policies => only the server's secret key can access.
alter table homes enable row level security;
alter table trips enable row level security;
alter table party_members enable row level security;
alter table trip_answers enable row level security;
alter table itinerary_items enable row level security;
alter table tasks enable row level security;
alter table messages enable row level security;
alter table payments enable row level security;

-- One sample home so simulated bookings have somewhere to land (not shown on the website).
insert into homes (slug, name, area, beds, baths, sleeps, house_notes)
values ('test-home', 'Test Home', 'Durango', 4, 3, 8, 'Simulated home for testing the trip flow.')
on conflict (slug) do nothing;

-- Server access. Needed because "automatically expose new tables" is off: grant only the secret-key role.
grant usage on schema public to service_role;
grant all privileges on all tables in schema public to service_role;
grant all privileges on all sequences in schema public to service_role;
alter default privileges in schema public grant all on tables to service_role;
alter default privileges in schema public grant all on sequences to service_role;

-- v1.1: plan extras shown to the guest
alter table trips add column if not exists offers jsonb default '[]'::jsonb;
alter table trips add column if not exists ready_list jsonb default '[]'::jsonb;
alter table trips add column if not exists weather jsonb default '[]'::jsonb;
alter table trips add column if not exists plan_summary text;

-- v1.2: Casey's restaurant list (the AI only books from this)
create table if not exists restaurants (
  id uuid primary key default gen_random_uuid(),
  name text not null,
  cuisine text,
  vibe text,                 -- e.g. quiet and romantic, lively, family-friendly, special occasion, casual
  price int check (price between 1 and 4),
  kid_friendly boolean default true,
  book_via text,             -- phone, OpenTable, Resy, text the owner, walk-in
  phone text,
  booking_url text,
  first_round boolean default false,   -- owner has agreed to the "first round on us" arrangement
  notes text,
  active boolean default true,
  created_at timestamptz default now()
);
alter table restaurants enable row level security;
grant all privileges on restaurants to service_role;
