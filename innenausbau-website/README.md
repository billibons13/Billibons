# Innenausbau-Website · Digital Sales System

Website + Portfolio + Lead-Generator + CRM-Einstiegspunkt + Automation-Hub für einen
Innenausbau-/Renovierungsbetrieb in Schleswig-Holstein.

**Stack:** Next.js 16 (App Router) · React 19 · TypeScript · Tailwind CSS 4 · zod · Make.com · Higgsfield (Visuals)

```bash
cp .env.example .env.local   # LEAD_SINK=log für lokale Entwicklung
npm install
npm run dev                  # http://localhost:3000
npm run build                # Produktionsbuild (alle Inhaltsseiten statisch)
npm run assets:fetch         # Higgsfield-Bilder lokal als WebP ablegen
```

## Dokumentation

| Datei | Inhalt |
|---|---|
| [docs/01-brand-design-system.md](docs/01-brand-design-system.md) | Markenkonzept, Positionierung, Farben, Typografie, Animationen |
| [docs/02-sitemap-ux.md](docs/02-sitemap-ux.md) | Sitemap, Seitenstruktur, Formular-UX, Mobile UX, Barrierefreiheit |
| [docs/03-components-content.md](docs/03-components-content.md) | Komponenten-/Content-Architektur, Platzhalter-Checkliste, i18n |
| [docs/04-seo-local-seo.md](docs/04-seo-local-seo.md) | SEO, Schema.org, Keywords, Local SEO, Standortseiten |
| [docs/05-higgsfield-asset-plan.md](docs/05-higgsfield-asset-plan.md) | Higgsfield Asset Plan mit allen Prompts |
| [docs/06-make-automation.md](docs/06-make-automation.md) | Make-Szenarien, Webhook, CRM-Abstraktion, Telegram, Follow-up |
| [docs/07-performance-deployment.md](docs/07-performance-deployment.md) | Performance-Maßnahmen, Deployment (Vercel/Netlify/Server) |
| [make/](make/) | JSON-Schema und Beispiel des Webhook-Payloads |

## Vor dem Livegang

Alle Firmendaten stehen in `src/config/site.ts` (Arbeitstitel „NORDRAUM“, Telefon, Adresse … sind Platzhalter).
Es werden keine Zahlen, Zertifikate oder Bewertungen erfunden – leere Felder werden automatisch ausgeblendet.
Projektbilder sind KI-Visualisierungen und werden gekennzeichnet, bis echte Fotos vorliegen.
