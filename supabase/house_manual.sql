-- House manual for each home. Run once in Supabase: SQL Editor -> New query -> paste -> Run.
alter table homes add column if not exists manual jsonb not null default '{}'::jsonb;
