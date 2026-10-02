# 03 · Компонентная и контентная архитектура

## Структура проекта

```
innenausbau-website/
├── src/
│   ├── app/                         Next.js App Router (страницы = маршруты)
│   │   ├── layout.tsx               Шрифт, Header/Footer/MobileCtaBar, LocalBusiness JSON-LD
│   │   ├── page.tsx                 Home (сборка секций)
│   │   ├── leistungen/[slug]/       SSG из content/services.ts
│   │   ├── projekte/[slug]/         SSG из content/projects.ts
│   │   ├── innenausbau/[ort]/       SSG только для published-локаций
│   │   ├── api/lead/route.ts        Приём заявок → LeadSink
│   │   ├── sitemap.ts · robots.ts
│   │   └── globals.css              Tailwind v4 + design tokens (@theme)
│   ├── config/site.ts               ЕДИНСТВЕННОЕ место для данных компании
│   ├── content/                     Весь контент как типизированные данные
│   │   ├── services.ts  projects.ts  faq.ts  process.ts
│   │   ├── testimonials.ts  locations.ts  navigation.ts
│   │   └── assets.ts                Манифест изображений/видео (Higgsfield)
│   ├── lib/
│   │   ├── leads/                   Lead-слой (CRM-agnostic)
│   │   │   ├── options.ts           Опции формы (общие для клиента и сервера)
│   │   │   ├── schema.ts            zod-валидация
│   │   │   ├── types.ts             LeadPayload + интерфейс LeadSink
│   │   │   ├── index.ts             getLeadSink(), buildLeadPayload()
│   │   │   └── sinks/               make.ts · webhook.ts · log.ts
│   │   └── seo/                     metadata.ts · jsonld.ts
│   └── components/
│       ├── layout/                  Header · Footer · MobileCtaBar · Logo
│       ├── sections/                Hero, TrustBar, ServicesPreview, BeforeAfterShowcase,
│       │                            FeaturedProjects, WhyUs, ProcessSteps, MaterialsQuality,
│       │                            Testimonials, Faq, RegionBlock, CtaBand, PageHeader, *Card
│       ├── forms/LeadForm.tsx       2-шаговая форма
│       └── ui/                      Button, Icons, SiteImage, BeforeAfterSlider, Counter,
│                                    SectionHeading, Breadcrumbs, JsonLd, RevealObserver
├── scripts/fetch-assets.mjs         Скачивание Higgsfield-ассетов → public/images/*.webp
├── make/                            JSON-схема и пример webhook-payload
└── docs/                            Эта документация
```

## Принципы

- **Server Components по умолчанию.** Клиентские (`"use client"`) только там, где нужна интерактивность: `Header`, `LeadForm`, `BeforeAfterSlider`, `Counter`, `HeroVideo`, `RevealObserver`. Остальное рендерится статически → минимум JS.
- **Контент отделён от вёрстки.** Новая услуга/проект = новый объект в `content/*.ts`; страницы, sitemap, Schema и навигация обновятся автоматически.
- **Конфигурация через env.** Куда уходят заявки — решает `LEAD_SINK`, а не код.
- **Типобезопасность.** `AssetKey` — union всех ключей изображений: опечатка в ключе ломает сборку, а не прод.

## Как добавить реальный проект

1. Сфотографировать «до» и «после» **с одной точки** (штатив, 24 мм, вертикали ровные, дневной свет).
2. Положить в `public/images/` (например `projekt-heide-bad-vorher.jpg`).
3. В `content/assets.ts` добавить ключи (`kind: "photo"`, width/height, alt по-немецки).
4. В `content/projects.ts` добавить проект с `isExample: false`, реальными `location` и `duration`.
5. Когда все визуализации заменены: `site.labelVisualizations = false`.

## Чек-лист плейсхолдеров перед запуском

| Где | Что заполнить |
|---|---|
| `src/config/site.ts` | name, legalName, phone, phoneE164, whatsappE164, email, address, openingHours, social, facts (только реальное) |
| `content/projects.ts` | `[Ort]`, `[Dauer]` → реальные данные или заменить проект |
| `content/faq.ts` | ответ «Ist die Besichtigung kostenlos?» — подтвердить |
| `app/ueber-uns/page.tsx` | портрет владельца / история |
| `app/impressum`, `app/datenschutz` | юридически проверенные тексты (§ 5 DDG, DSGVO, Make/Google/Telegram как обработчики) |
| `components/sections/WhyUs.tsx`, `MaterialsQuality.tsx` | подтвердить, что описанные процессы реально выполняются |

## i18n (DE → RU / UK / EN)

Сейчас один язык, но всё подготовлено:

- Тексты живут в `content/*` и компонентах; при добавлении языков контент переносится в `content/<locale>/…` с тем же типом.
- Маршрутизация: сегмент `app/[locale]/…` (DE без префикса как default, `/en`, `/ru`, `/uk`), `proxy.ts` (Next 16) для определения языка по `Accept-Language` только как подсказка (без принудительного редиректа).
- `pageMetadata()` уже выводит `alternates.languages` — достаточно добавить ключи `en`, `ru`, `uk`.
- Форма: `meta.locale` уже передаётся в payload → Make может отвечать клиенту на его языке.
