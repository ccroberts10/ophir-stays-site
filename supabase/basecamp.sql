-- Ophir Basecamp: run once in the Supabase SQL editor.
alter table trips drop constraint if exists trips_package_check;
alter table trips add constraint trips_package_check check (package in ('stay','arranged','basecamp','private'));
alter table homes add column if not exists basecamp_ready boolean not null default false;
-- Mark a qualifying home (garage or locked bike storage, wash station, gear room, 15 min to trailhead or lifts):
-- update homes set basecamp_ready = true where name = 'Home name here';

-- Basecamp trip inquiries from ophirstays.com/basecamp
create table if not exists basecamp_inquiries (
  id uuid primary key default gen_random_uuid(),
  created_at timestamptz not null default now(),
  name text not null, email text not null, phone text,
  trip_type text, group_size text, level text, dates text, notes text,
  status text not null default 'new' check (status in ('new','replied','booked','closed'))
);
alter table basecamp_inquiries enable row level security;
