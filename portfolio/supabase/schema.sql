-- Guestbook schema for the portfolio site.
-- Run this once in the Supabase project's SQL Editor
-- (https://supabase.com/dashboard/project/_/sql/new).

create table public.messages (
  id         uuid primary key default gen_random_uuid(),
  name       text not null check (char_length(name) between 1 and 50),
  content    text not null check (char_length(content) between 1 and 500),
  created_at timestamptz not null default now()
);

create index messages_created_at_idx on public.messages (created_at desc);

alter table public.messages enable row level security;

create policy "messages_public_read"
  on public.messages
  for select
  to anon, authenticated
  using (true);

create policy "messages_public_insert"
  on public.messages
  for insert
  to anon, authenticated
  with check (true);

-- Troubleshooting: if inserts/reads fail with "permission denied for table
-- messages", the project's default privileges weren't inherited. Run:
-- grant select, insert on public.messages to anon, authenticated;
