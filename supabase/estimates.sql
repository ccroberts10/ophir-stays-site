-- Earnings estimate requests (owners and agents). Run once in Supabase → SQL Editor.
create extension if not exists pgcrypto;
create table if not exists estimates (
  id uuid primary key default gen_random_uuid(),
  token text unique not null default encode(gen_random_bytes(16), 'hex'),
  created_at timestamptz not null default now(),
  status text not null default 'new',            -- new, sent, signed, closed
  requester_role text,                            -- owner | agent
  requester_name text, requester_email text, requester_phone text, brokerage text,
  owner_name text, owner_email text,
  address text, area text, home_type text, bedrooms int, baths numeric, sleeps int,
  features text[] default '{}', hoa text, current_use text, current_rent int,
  source text, notes text,
  adr_adjust numeric not null default 1, occ_adjust numeric not null default 1,
  personal_note text, model jsonb, sent_at timestamptz
);
alter table estimates enable row level security;  -- only the server (secret key) reads or writes
create index if not exists estimates_created on estimates (created_at desc);
