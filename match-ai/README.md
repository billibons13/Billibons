# MATCH AI (working name)

SaaS that turns a screenshot of a sports match into a structured, transparent AI analysis
(summary, confidence, key factors, signals, risks, uncertainties).

> AI analysis is informational and does not guarantee any outcome.

Stack: Next.js 16 (App Router, Cache Components) · TypeScript (strict) · Tailwind CSS v4 ·
lucide-react · zod · Supabase (auth + Postgres) · Stripe · Vitest.

## Setup

```bash
cd match-ai
npm ci                      # install exact versions from package-lock.json
cp .env.example .env.local  # fill in what you have; everything is optional for local dev
npm run dev                 # http://localhost:3000
```

Without any env variables the site runs fully: the landing, legal pages and auth forms work;
auth submissions answer "Authentication is not configured yet", and the AI layer uses the
development provider (always `insufficient_data`, never invented numbers).

## Scripts

| Command             | What it does                                  |
| ------------------- | --------------------------------------------- |
| `npm run dev`       | Development server                            |
| `npm run build`     | Production build                              |
| `npm run start`     | Serve the production build                    |
| `npm run lint`      | ESLint (next/core-web-vitals + TypeScript)    |
| `npm run typecheck` | Generate route types + `tsc --noEmit`         |
| `npm test`          | Unit tests (Vitest)                           |

## Database

Apply `supabase/migrations/0001_init.sql` to the Supabase project (SQL editor or
`supabase db push`). It creates all tables with RLS, the sign-up trigger and the atomic
`consume_analysis_credit()` function.

## Docs

- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — structure, AI pipeline, data & security model, how to rename / translate / add providers
- [docs/PHASES.md](docs/PHASES.md) — phase status and what the owner must connect
- `docs/screenshots/` — current landing (desktop, mobile) and login (mobile)
