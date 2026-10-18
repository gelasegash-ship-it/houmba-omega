-- NOVA CORE social messaging and payment-intent foundation.
-- This records payment requests only; it does not debit, transfer, or hold money.
create table if not exists public.nova_messages (
  id uuid primary key default gen_random_uuid(),
  sender_id uuid not null references auth.users(id) on delete cascade,
  recipient_id uuid not null references auth.users(id) on delete cascade,
  body text not null check (char_length(body) between 1 and 4000),
  created_at timestamptz not null default now(),
  read_at timestamptz,
  constraint nova_messages_no_self_message check (sender_id <> recipient_id)
);
create index if not exists nova_messages_inbox_idx on public.nova_messages(recipient_id, created_at desc);
create index if not exists nova_messages_outbox_idx on public.nova_messages(sender_id, created_at desc);
alter table public.nova_messages enable row level security;
drop policy if exists "Users can read their own messages" on public.nova_messages;
create policy "Users can read their own messages" on public.nova_messages for select to authenticated
using ((select auth.uid()) = sender_id or (select auth.uid()) = recipient_id);
drop policy if exists "Users can send messages as themselves" on public.nova_messages;
create policy "Users can send messages as themselves" on public.nova_messages for insert to authenticated
with check ((select auth.uid()) = sender_id and recipient_id <> (select auth.uid()));
drop policy if exists "Recipients can mark messages read" on public.nova_messages;
create policy "Recipients can mark messages read" on public.nova_messages for update to authenticated
using ((select auth.uid()) = recipient_id) with check ((select auth.uid()) = recipient_id);

create table if not exists public.nova_payment_intents (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  amount_minor bigint not null check (amount_minor > 0),
  currency text not null default 'XAF' check (currency ~ '^[A-Z]{3}$'),
  purpose text not null check (char_length(purpose) between 1 and 500),
  provider text not null default 'unconfigured' check (provider in ('unconfigured','manual','cinetpay','flutterwave','stripe')),
  provider_reference text,
  status text not null default 'pending_provider' check (status in ('pending_provider','pending','succeeded','failed','cancelled','refunded')),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists nova_payment_intents_user_created_idx on public.nova_payment_intents(user_id, created_at desc);
alter table public.nova_payment_intents enable row level security;
drop policy if exists "Users can read own payment intents" on public.nova_payment_intents;
create policy "Users can read own payment intents" on public.nova_payment_intents for select to authenticated
using ((select auth.uid()) = user_id);
drop policy if exists "Users can create own payment intents" on public.nova_payment_intents;
create policy "Users can create own payment intents" on public.nova_payment_intents for insert to authenticated
with check ((select auth.uid()) = user_id and status = 'pending_provider' and provider = 'unconfigured' and provider_reference is null);
-- Clients cannot mark an intent paid. A verified provider webhook/service role must do that.
