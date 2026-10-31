-- Guest's chosen cause for Ophir's $10-per-stay donation. Run once in Supabase SQL editor.
alter table trips add column if not exists cause text check (cause in ('trails','adaptive','housing'));
