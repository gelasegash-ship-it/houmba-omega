-- NOVA CORE foundation: private per-user mission tracking.
create table if not exists public.nova_missions (
  id uuid primary key default gen_random_uuid(),
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 180),
  goal text not null check (char_length(goal) between 1 and 4000),
  status text not null default 'planned' check (status in ('planned','active','blocked','completed','cancelled')),
  budget_cents bigint not null default 0 check (budget_cents >= 0),
  currency text not null default 'XAF' check (currency ~ '^[A-Z]{3}$'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists nova_missions_user_created_idx on public.nova_missions(user_id, created_at desc);
alter table public.nova_missions enable row level security;
drop policy if exists "Users can read own NOVA missions" on public.nova_missions;
create policy "Users can read own NOVA missions" on public.nova_missions for select to authenticated using ((select auth.uid()) = user_id);
drop policy if exists "Users can create own NOVA missions" on public.nova_missions;
create policy "Users can create own NOVA missions" on public.nova_missions for insert to authenticated with check ((select auth.uid()) = user_id);
drop policy if exists "Users can update own NOVA missions" on public.nova_missions;
create policy "Users can update own NOVA missions" on public.nova_missions for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id);
drop policy if exists "Users can delete own NOVA missions" on public.nova_missions;
create policy "Users can delete own NOVA missions" on public.nova_missions for delete to authenticated using ((select auth.uid()) = user_id);

create table if not exists public.nova_tasks (
  id uuid primary key default gen_random_uuid(),
  mission_id uuid not null references public.nova_missions(id) on delete cascade,
  user_id uuid not null references auth.users(id) on delete cascade,
  title text not null check (char_length(title) between 1 and 240),
  status text not null default 'planned' check (status in ('planned','in_progress','blocked','completed','cancelled')),
  risk_level text not null default 'low' check (risk_level in ('low','medium','high','critical')),
  requires_approval boolean not null default false,
  evidence jsonb not null default '[]'::jsonb check (jsonb_typeof(evidence) = 'array'),
  created_at timestamptz not null default now(),
  updated_at timestamptz not null default now()
);
create index if not exists nova_tasks_user_mission_idx on public.nova_tasks(user_id, mission_id);
alter table public.nova_tasks enable row level security;
drop policy if exists "Users can read own NOVA tasks" on public.nova_tasks;
create policy "Users can read own NOVA tasks" on public.nova_tasks for select to authenticated using ((select auth.uid()) = user_id);
drop policy if exists "Users can create own NOVA tasks" on public.nova_tasks;
create policy "Users can create own NOVA tasks" on public.nova_tasks for insert to authenticated with check ((select auth.uid()) = user_id and exists (select 1 from public.nova_missions m where m.id = mission_id and m.user_id = (select auth.uid())));
drop policy if exists "Users can update own NOVA tasks" on public.nova_tasks;
create policy "Users can update own NOVA tasks" on public.nova_tasks for update to authenticated using ((select auth.uid()) = user_id) with check ((select auth.uid()) = user_id and exists (select 1 from public.nova_missions m where m.id = mission_id and m.user_id = (select auth.uid())));
drop policy if exists "Users can delete own NOVA tasks" on public.nova_tasks;
create policy "Users can delete own NOVA tasks" on public.nova_tasks for delete to authenticated using ((select auth.uid()) = user_id);
