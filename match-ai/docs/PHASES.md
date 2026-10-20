# Phases

**Кратко (RU):** этапы 0 и 1 выполнены — создан каталог `match-ai/` (Next.js 16 + TS + Tailwind),
дизайн-система, лендинг, страницы входа/регистрации/сброса пароля (работают после подключения
Supabase, сейчас честно отвечают «Authentication is not configured yet»), юридические шаблоны,
SEO, cookie-баннер, основа AI-слоя (без выдуманных результатов), схема БД с RLS. Цены тарифов —
ПРЕДЛОЖЕНИЕ, не утверждены владельцем. Для запуска владелец должен подключить: Supabase, OpenAI,
Stripe (+ цены), домен, Vercel.

## Status

| #  | Phase                                              | Status |
| -- | -------------------------------------------------- | ------ |
| 0  | Audit & architecture                               | ✅ done |
| 1  | Design system & landing (+ auth pages, legal, SEO) | ✅ done |
| 2  | Supabase auth live (needs project)                 | 🟡 code ready, waiting for Supabase credentials |
| 3  | Database (migration applied, types generated)      | 🟡 migration written & tested locally, not applied to a project |
| 4  | Upload flow (private bucket, validation, UI)       | ⏳ validation done, route/UI pending |
| 5  | AI pipeline live (OpenAI)                          | 🟡 provider + pipeline + tests done, waiting for API key |
| 6  | Analysis result page                               | ⏳ |
| 7  | Dashboard & history                                | ⏳ minimal dashboard exists |
| 8  | Usage limits enforcement                           | 🟡 `consume_analysis_credit()` ready, not wired |
| 9  | Stripe checkout, portal, webhook                   | ⏳ client skeleton only; prices need owner approval |
| 10 | Analytics & consent                                | 🟡 consent + `track()` ready, no provider key |
| 11 | i18n (de, ru, uk)                                  | ⏳ architecture ready, only `en` |
| 12 | Hardening & launch (legal review, CSP, monitoring) | ⏳ |

## Phase 0 — audit result

- The repository contained no web application; `match-ai/` is a new, self-contained
  Next.js project (own `package.json`, lockfile, docs). Nothing outside it was changed.
- Next.js 16 specifics adopted: `proxy.ts` instead of `middleware.ts`, Cache Components
  (session reads are behind `<Suspense>`), `next typegen` for `LayoutProps`, ESLint flat config.
- Decisions: hand-written UI kit (no Radix) — native `<dialog>` and `<details>` give
  accessible modal/accordion without extra deps; OpenAI via `fetch` (no SDK); prices are
  configuration and the defaults are a **PROPOSAL — not approved by owner**.
- Placeholders that must be replaced before launch: `support@example.com` and
  `[Company name]` in `lib/config/brand.ts`; all `[bracketed]` fields in the legal templates
  (`lib/i18n/messages/en/legal.ts`). The legal pages are templates, not legal advice.

## Verification (phase 1)

`npm run lint`, `npm run typecheck`, `npm test` (5 files, unit tests), `npm run build` — all
green. Playwright (Chromium) at 1440 px and 390 px: no console errors, no horizontal overflow
on `/`, `/login`, `/register`, `/forgot-password`, `/reset-password`, `/privacy`, `/terms`,
`/imprint`. Screenshots in `docs/screenshots/`.

## What the owner must connect

1. **Supabase project** → `NEXT_PUBLIC_SUPABASE_URL`, `NEXT_PUBLIC_SUPABASE_ANON_KEY`,
   `SUPABASE_SERVICE_ROLE_KEY`; run `supabase/migrations/0001_init.sql`; set Site URL and the
   redirect URL `https://<domain>/auth/callback` in Supabase Auth settings.
2. **OpenAI API key** → `AI_PROVIDER=openai`, `OPENAI_API_KEY`, optionally `OPENAI_MODEL`.
3. **Stripe account** → decide final prices, create Products/Prices for Pro and Premium →
   `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, `STRIPE_PRICE_PRO`, `STRIPE_PRICE_PREMIUM`,
   and the display prices `NEXT_PUBLIC_PLAN_PRICE_PRO` / `_PREMIUM` / `NEXT_PUBLIC_PLAN_CURRENCY`.
4. **Domain** → `NEXT_PUBLIC_APP_URL`.
5. **Vercel project** (root directory `match-ai`) with the env variables above.
6. Optional: PostHog project key (`NEXT_PUBLIC_POSTHOG_KEY`), real support email, company
   details for the imprint/privacy/terms, legal review.
