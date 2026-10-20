-- =============================================================================
-- 0001_init — core schema for the match-analysis SaaS.
-- Users are Supabase auth.users. Every user-owned table has RLS enabled with
-- "own rows only" policies. Writes that affect billing or usage are performed
-- by trusted server code (service role) or SECURITY DEFINER functions.
-- =============================================================================

create extension if not exists "pgcrypto";

-- ----------------------------------------------------------------------------
-- plans (public catalogue; mirrors lib/config/plans.ts)
-- Prices are NOT stored here: they live in Stripe (owner decision, phase 9).
-- ----------------------------------------------------------------------------
create table public.plans (
  id                 text primary key check (id in ('free', 'pro', 'premium')),
  analyses_per_month integer not null check (analyses_per_month >= 0),
  stripe_price_id    text unique,
  is_active          boolean not null default true,
  created_at         timestamptz not null default now()
);

insert into public.plans (id, analyses_per_month) values
  ('free', 3),
  ('pro', 50),
  ('premium', 200);

-- ----------------------------------------------------------------------------
-- profiles (1:1 with auth.users)
-- ----------------------------------------------------------------------------
create table public.profiles (
  id                 uuid primary key references auth.users (id) on delete cascade,
  email              text,
  plan_id            text not null default 'free' references public.plans (id),
  locale             text not null default 'en',
  stripe_customer_id text unique,
  created_at         timestamptz not null default now(),
  updated_at         timestamptz not null default now()
);

-- ----------------------------------------------------------------------------
-- subscriptions (written by the Stripe webhook with the service role)
-- ----------------------------------------------------------------------------
create table public.subscriptions (
  id                     uuid primary key default gen_random_uuid(),
  user_id                uuid not null references auth.users (id) on delete cascade,
  plan_id                text not null references public.plans (id),
  stripe_subscription_id text unique,
  status                 text not null check (status in ('trialing', 'active', 'past_due', 'canceled', 'incomplete', 'incomplete_expired', 'unpaid', 'paused')),
  current_period_start   timestamptz,
  current_period_end     timestamptz,
  cancel_at_period_end   boolean not null default false,
  created_at             timestamptz not null default now(),
  updated_at             timestamptz not null default now()
);
create index subscriptions_user_id_idx on public.subscriptions (user_id);
create index subscriptions_status_idx on public.subscriptions (status);

-- ----------------------------------------------------------------------------
-- uploaded_images (files live in a private Storage bucket; this is metadata)
-- ----------------------------------------------------------------------------
create table public.uploaded_images (
  id           uuid primary key default gen_random_uuid(),
  user_id      uuid not null references auth.users (id) on delete cascade,
  storage_path text not null unique,
  mime_type    text not null check (mime_type in ('image/png', 'image/jpeg', 'image/webp')),
  size_bytes   integer not null check (size_bytes > 0),
  sha256       text,
  expires_at   timestamptz not null,  -- now() + IMAGE_RETENTION_DAYS, enforced by a cleanup job
  deleted_at   timestamptz,
  created_at   timestamptz not null default now()
);
create index uploaded_images_user_id_idx on public.uploaded_images (user_id, created_at desc);
create index uploaded_images_expires_at_idx on public.uploaded_images (expires_at) where deleted_at is null;

-- ----------------------------------------------------------------------------
-- analyses (one per analysis request)
-- ----------------------------------------------------------------------------
create table public.analyses (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references auth.users (id) on delete cascade,
  image_id      uuid references public.uploaded_images (id) on delete set null,
  status        text not null default 'pending' check (status in ('pending', 'processing', 'completed', 'insufficient_data', 'failed')),
  error_code    text,
  sport         text,
  home_team     text,
  away_team     text,
  competition   text,
  extraction    jsonb,  -- validated MatchExtraction
  created_at    timestamptz not null default now(),
  completed_at  timestamptz
);
create index analyses_user_id_created_idx on public.analyses (user_id, created_at desc);
create index analyses_status_idx on public.analyses (status);

-- ----------------------------------------------------------------------------
-- analysis_results (validated AnalysisResult JSON)
-- ----------------------------------------------------------------------------
create table public.analysis_results (
  id            uuid primary key default gen_random_uuid(),
  analysis_id   uuid not null unique references public.analyses (id) on delete cascade,
  user_id       uuid not null references auth.users (id) on delete cascade,
  result        jsonb not null,
  confidence    numeric(4, 3) check (confidence >= 0 and confidence <= 1),
  model_version text not null,
  created_at    timestamptz not null default now()
);
create index analysis_results_user_id_idx on public.analysis_results (user_id);

-- ----------------------------------------------------------------------------
-- usage (analyses consumed per user per billing period, e.g. '2026-10')
-- ----------------------------------------------------------------------------
create table public.usage (
  id              uuid primary key default gen_random_uuid(),
  user_id         uuid not null references auth.users (id) on delete cascade,
  period          text not null check (period ~ '^\d{4}-\d{2}$'),
  analyses_used   integer not null default 0 check (analyses_used >= 0),
  updated_at      timestamptz not null default now(),
  constraint usage_user_period_unique unique (user_id, period)
);

-- ----------------------------------------------------------------------------
-- ai_requests (audit / cost tracking, no image content)
-- ----------------------------------------------------------------------------
create table public.ai_requests (
  id            uuid primary key default gen_random_uuid(),
  user_id       uuid not null references auth.users (id) on delete cascade,
  analysis_id   uuid references public.analyses (id) on delete set null,
  provider      text not null,
  model         text not null,
  step          text not null check (step in ('extraction', 'analysis', 'repair')),
  status        text not null check (status in ('ok', 'invalid_output', 'error')),
  input_tokens  integer,
  output_tokens integer,
  latency_ms    integer,
  created_at    timestamptz not null default now()
);
create index ai_requests_user_id_idx on public.ai_requests (user_id, created_at desc);
create index ai_requests_analysis_id_idx on public.ai_requests (analysis_id);

-- ----------------------------------------------------------------------------
-- payments (written by the Stripe webhook with the service role)
-- ----------------------------------------------------------------------------
create table public.payments (
  id                       uuid primary key default gen_random_uuid(),
  user_id                  uuid not null references auth.users (id) on delete cascade,
  subscription_id          uuid references public.subscriptions (id) on delete set null,
  stripe_invoice_id        text unique,
  stripe_payment_intent_id text unique,
  amount_cents             integer not null check (amount_cents >= 0),
  currency                 text not null,
  status                   text not null check (status in ('succeeded', 'failed', 'pending', 'refunded')),
  created_at               timestamptz not null default now()
);
create index payments_user_id_idx on public.payments (user_id, created_at desc);

-- ============================================================================
-- updated_at helper
-- ============================================================================
create or replace function public.set_updated_at()
returns trigger language plpgsql as $$
begin
  new.updated_at := now();
  return new;
end;
$$;

create trigger profiles_set_updated_at before update on public.profiles
  for each row execute function public.set_updated_at();
create trigger subscriptions_set_updated_at before update on public.subscriptions
  for each row execute function public.set_updated_at();

-- ============================================================================
-- Profile creation on sign-up
-- ============================================================================
create or replace function public.handle_new_user()
returns trigger
language plpgsql
security definer
set search_path = public
as $$
begin
  insert into public.profiles (id, email)
  values (new.id, new.email)
  on conflict (id) do nothing;
  return new;
end;
$$;

create trigger on_auth_user_created
  after insert on auth.users
  for each row execute function public.handle_new_user();

-- ============================================================================
-- Atomic usage accounting
-- Returns the new count if a credit was consumed, or NULL if the limit is
-- reached. Concurrency-safe: the upsert takes a row lock on (user_id, period)
-- and the WHERE clause on the conflict update prevents exceeding the limit.
-- ============================================================================
create or replace function public.consume_analysis_credit(
  p_user_id uuid,
  p_period  text,
  p_limit   integer
)
returns integer
language plpgsql
security definer
set search_path = public
as $$
declare
  v_used integer;
begin
  if p_limit is null or p_limit <= 0 then
    return null;
  end if;

  insert into public.usage as u (user_id, period, analyses_used)
  values (p_user_id, p_period, 1)
  on conflict (user_id, period) do update
    set analyses_used = u.analyses_used + 1,
        updated_at    = now()
    where u.analyses_used < p_limit
  returning u.analyses_used into v_used;

  return v_used;  -- NULL when the conflict update was skipped (limit reached)
end;
$$;

-- Refund a credit when an analysis fails for technical reasons.
create or replace function public.refund_analysis_credit(p_user_id uuid, p_period text)
returns void
language sql
security definer
set search_path = public
as $$
  update public.usage
     set analyses_used = greatest(analyses_used - 1, 0), updated_at = now()
   where user_id = p_user_id and period = p_period;
$$;

-- Only the server (service role) may call the accounting functions.
revoke all on function public.consume_analysis_credit(uuid, text, integer) from public, anon, authenticated;
revoke all on function public.refund_analysis_credit(uuid, text) from public, anon, authenticated;
grant execute on function public.consume_analysis_credit(uuid, text, integer) to service_role;
grant execute on function public.refund_analysis_credit(uuid, text) to service_role;

-- ============================================================================
-- Row Level Security
-- ============================================================================
alter table public.plans            enable row level security;
alter table public.profiles         enable row level security;
alter table public.subscriptions    enable row level security;
alter table public.uploaded_images  enable row level security;
alter table public.analyses         enable row level security;
alter table public.analysis_results enable row level security;
alter table public.usage            enable row level security;
alter table public.ai_requests      enable row level security;
alter table public.payments         enable row level security;

-- plans: readable by everyone, writable only by the service role.
create policy "plans are readable by everyone" on public.plans
  for select to anon, authenticated using (true);

-- profiles: users read and update their own profile (plan changes go through Stripe webhook).
create policy "own profile: select" on public.profiles
  for select to authenticated using ((select auth.uid()) = id);
create policy "own profile: update" on public.profiles
  for update to authenticated using ((select auth.uid()) = id) with check ((select auth.uid()) = id);

-- Users may not change their own plan or Stripe customer id.
revoke update on public.profiles from authenticated;
grant update (locale) on public.profiles to authenticated;

-- Read-only for users; written by the server.
create policy "own subscriptions: select" on public.subscriptions
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own payments: select" on public.payments
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own usage: select" on public.usage
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own ai_requests: select" on public.ai_requests
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own analysis_results: select" on public.analysis_results
  for select to authenticated using ((select auth.uid()) = user_id);

-- Images and analyses: users can read and delete their own rows.
create policy "own images: select" on public.uploaded_images
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own images: delete" on public.uploaded_images
  for delete to authenticated using ((select auth.uid()) = user_id);
create policy "own analyses: select" on public.analyses
  for select to authenticated using ((select auth.uid()) = user_id);
create policy "own analyses: delete" on public.analyses
  for delete to authenticated using ((select auth.uid()) = user_id);
