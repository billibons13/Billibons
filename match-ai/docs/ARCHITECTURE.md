# Architecture

## Stack

| Concern       | Choice                                                                 |
| ------------- | ---------------------------------------------------------------------- |
| Framework     | Next.js 16 App Router, Turbopack, Cache Components + Partial Prefetching |
| Language      | TypeScript `strict`                                                    |
| Styling       | Tailwind CSS v4 (tokens in `app/globals.css`), hand-written UI kit (cva + tailwind-merge) |
| Icons         | lucide-react                                                           |
| Validation    | zod v4 (forms, AI output, env-derived config)                          |
| Auth + DB     | Supabase (`@supabase/ssr`, Postgres with RLS)                          |
| Payments      | Stripe (server-only client, phase 9)                                   |
| AI            | Provider-agnostic layer; OpenAI vision via `fetch` (no SDK)            |
| Tests         | Vitest (unit)                                                          |

## Folders

```
app/
  (marketing)/        landing, /privacy, /terms, /imprint (Navbar + Footer layout)
  (auth)/             /login, /register, /forgot-password, /reset-password
  dashboard/          minimal authenticated page (session read inside <Suspense>)
  auth/callback/      Supabase email-link code exchange
  icon.svg, opengraph-image.tsx, robots.ts, sitemap.ts, not-found.tsx
components/
  ui/                 Button, Card, Input, Label, Badge, Container/Section, Dialog, Toast, Spinner, Skeleton
  layout/             Navbar, MobileMenu, Footer, Logo, CookieConsent
  landing/            Hero, TrustStrip, HowItWorks, DemoAnalysis, Features, Pricing, Faq, FinalCta
  auth/, legal/       forms and the legal template layout
lib/
  config/             env.ts (public), server-env.ts (server-only), brand.ts, plans.ts, upload.ts
  i18n/               config.ts, index.ts (getMessages / translate / format), messages/en(.ts|/*)
  ai/                 schema.ts, types.ts, prompts.ts, json.ts, factory.ts, pipeline.ts, providers/
  auth/               schemas.ts (zod), actions.ts (server actions), session.ts (DAL)
  db/                 server.ts, browser.ts, admin.ts (service role, server-only)
  stripe/             server-only client + price-id mapping
  analytics/          track() + PostHog adapter (consent-gated)
  errors/             typed user-facing error codes
  upload/             magic-byte image validation
  consent.ts, utils.ts
hooks/                use-messages, use-consent, use-auth-form
types/                shared type re-exports
proxy.ts              session refresh + /dashboard protection (Next 16 "proxy" = former middleware)
supabase/migrations/  SQL schema
tests/                Vitest unit tests
```

## AI pipeline

```
upload ──► validateUpload()  (size, MIME, extension, magic bytes)
              │
              ▼
        provider.extractMatch(image) ──► MatchExtractionSchema.parse
              │                           (invalid JSON → one repair call → else ANALYSIS_FAILED)
              ├─ status = not_recognized ─────────► AppError MATCH_NOT_RECOGNIZED
              ▼
        enrichContext(extraction)   STUB: adds no data (documented in pipeline.ts)
              │
              ├─ insufficient_data / teams missing ─► buildInsufficientResult()  (confidence 0)
              ▼
        provider.analyze(extraction, context) ──► AnalysisResultSchema.safeParse
              │                                    (refinement: insufficient_data ⇒ confidence 0)
              ▼
        PipelineResult { provider, extraction, context, result }
```

Rules enforced in prompts **and** schema: no invented facts, `null` instead of guesses,
`insufficient_data` when evidence is lacking, `confidence` describes data support — not the
probability of an outcome. `DevelopmentProvider` (default) never calls an AI and always
returns `insufficient_data`.

Planned (phase 4+): an API route that authenticates, calls `consume_analysis_credit()`,
stores the image in a private bucket, runs the pipeline, writes `analyses`,
`analysis_results`, `ai_requests`, and refunds the credit on technical failure.

## Data model (`supabase/migrations/0001_init.sql`)

| Table              | Purpose                                                        |
| ------------------ | -------------------------------------------------------------- |
| `plans`            | free / pro / premium + monthly limits (3 / 50 / 200); readable by all |
| `profiles`         | 1:1 with `auth.users`, created by trigger `on_auth_user_created` |
| `subscriptions`    | Stripe subscription state (written by webhook, service role)   |
| `uploaded_images`  | metadata of private-bucket images, `expires_at` for retention  |
| `analyses`         | one per request, status + validated extraction (jsonb)         |
| `analysis_results` | validated `AnalysisResult` (jsonb), confidence, model_version  |
| `usage`            | analyses used per user per period, `unique (user_id, period)`  |
| `ai_requests`      | provider/model/step/status/tokens/latency (no image content)   |
| `payments`         | invoices / payment intents                                     |

`consume_analysis_credit(user_id, period, limit)` is a single `INSERT … ON CONFLICT DO
UPDATE … WHERE analyses_used < limit RETURNING`, so concurrent requests cannot exceed the
limit (verified locally: 20 parallel calls with limit 5 → exactly 5 consumed). It returns
`NULL` when the limit is reached. Only `service_role` may execute it.

## Security model

- **RLS on every table.** Users can only `select` their own rows; they can delete their own
  images/analyses; they can update only `profiles.locale` (column grant). Billing, usage and
  AI audit rows are written by the server with the service role.
- **Secrets are server-only.** `lib/config/server-env.ts`, `lib/db/admin.ts`, `lib/stripe`,
  `lib/ai` import `server-only`, so importing them from client code fails the build.
- **Auth.** Server actions validate with zod again (client validation is UX only). The DAL
  uses `supabase.auth.getUser()` (verified), never a raw cookie. `proxy.ts` refreshes the
  session and protects `/dashboard`. The callback only accepts same-origin relative `next`.
  Password reset never reveals whether an email exists.
- **Uploads.** Content is identified by magic bytes; MIME and extension must agree with it.
- **Privacy.** Analytics are no-op until the user accepts them in the cookie banner; no
  personal data is sent in event props. Images get an `expires_at` (IMAGE_RETENTION_DAYS).
- **Errors.** Only `AppError` codes with dictionary messages reach users; causes stay in logs.

## Renaming the brand

Change `name` (and optionally `shortName`, `tagline`, `description`, `supportEmail`,
`legalEntity`) in `lib/config/brand.ts`. All UI, metadata, OG image and the footer read it.
Also replace the mark in `components/layout/logo.tsx` and `app/icon.svg` if desired.

## Adding a language (de / ru / uk planned)

1. Create `lib/i18n/messages/de.ts` exporting `const de: Messages = { … }` — TypeScript
   enforces the exact same shape as `en`.
2. Add `"de"` to `LOCALES` in `lib/i18n/config.ts` and register it in `dictionaries` in
   `lib/i18n/index.ts`.
3. Routing: add an `app/[locale]/…` segment (or detect via `Accept-Language` in `proxy.ts`),
   pass the locale to `getMessages(locale)` on the server and provide it through a context
   read by `hooks/use-messages.ts` on the client. Set `<html lang>` accordingly.

## Adding an AI provider

1. Implement `AIProvider` (`lib/ai/types.ts`) in `lib/ai/providers/<name>.ts` with
   `import "server-only"`. Return data validated by `MatchExtractionSchema` /
   `AnalysisResultSchema` (use `validateWithRepair` from `lib/ai/json.ts`).
2. Map transport errors to `AI_UNAVAILABLE`, invalid output to `ANALYSIS_FAILED`.
3. Add a `case` to `createAIProvider()` in `lib/ai/factory.ts` and its env vars to
   `lib/config/server-env.ts` and `.env.example`.
4. Add unit tests with a mocked `fetch`.
