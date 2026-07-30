-- Profanity filter for the guestbook.
-- Run this in the Supabase SQL Editor AFTER schema.sql.
-- Enforced in the database (not just client JS) so it can't be bypassed by
-- posting directly to the REST API.

create table public.banned_words (
  word text primary key
);

-- RLS enabled with no policies: invisible to anon/authenticated clients.
-- Manage the word list via the Table Editor or SQL Editor (postgres role
-- bypasses RLS).
alter table public.banned_words enable row level security;

insert into public.banned_words (word) values
  ('씨발'), ('시발'), ('개새끼'), ('병신'), ('지랄'),
  ('좆'), ('존나'), ('새끼'), ('걸레'), ('창녀'),
  ('fuck'), ('shit'), ('bitch'), ('asshole'), ('bastard'),
  ('cunt'), ('dick'), ('whore'), ('slut')
on conflict do nothing;

create or replace function public.check_profanity()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
declare
  normalized_name text := lower(regexp_replace(new.name, '\s+', '', 'g'));
  normalized_content text := lower(regexp_replace(new.content, '\s+', '', 'g'));
  banned record;
begin
  for banned in select word from public.banned_words loop
    if normalized_name like '%' || banned.word || '%'
       or normalized_content like '%' || banned.word || '%' then
      raise exception 'message contains inappropriate language';
    end if;
  end loop;
  return new;
end;
$$;

drop trigger if exists messages_profanity_check on public.messages;
create trigger messages_profanity_check
  before insert on public.messages
  for each row
  execute function public.check_profanity();
