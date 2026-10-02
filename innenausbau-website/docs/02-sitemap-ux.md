# 02 · Sitemap, UX-архитектура, Mobile UX

## Sitemap

```
/                                Home
├── /leistungen                  Übersicht (3 группы)
│   ├── /leistungen/trockenbau
│   ├── /leistungen/innenputz
│   ├── /leistungen/malerarbeiten
│   ├── /leistungen/bodenbelaege
│   ├── /leistungen/fliesenarbeiten
│   ├── /leistungen/renovierung
│   ├── /leistungen/sanierung
│   ├── /leistungen/badsanierung
│   ├── /leistungen/kuechenrenovierung
│   ├── /leistungen/innenausbau
│   ├── /leistungen/spachtelarbeiten
│   ├── /leistungen/decken-und-waende
│   └── /leistungen/komplettrenovierung
├── /projekte                    Portfolio
│   └── /projekte/[slug]         Проект: факты, Before/After, решение, галерея
├── /ablauf                      Процесс 01–06 + FAQ
├── /ueber-uns
├── /kontakt                     Форма заявки (#anfrage) + прямые каналы
├── /innenausbau/[ort]           Location pages — генерируются ТОЛЬКО при published: true
├── /impressum                   noindex
├── /datenschutz                 noindex
├── /sitemap.xml                 генерируется из контента
└── /robots.txt
```

## Структура Home (конверсионная логика)

| # | Секция | Задача | CTA |
|---|---|---|---|
| 1 | Hero | Что, для кого, какой результат. H1 «Wir verwandeln Räume.» + Before→After видео | Projekt anfragen / Unsere Leistungen |
| 2 | Trust indicators | Быстрые проверяемые якоря (13 услуг, 6 шагов, 1 контакт, регион) | — |
| 3 | Leistungen | 6 приоритетных услуг с фото | Alle Leistungen |
| 4 | Before / After | Интерактивное доказательство результата (тёмная секция = визуальная пауза) | Projekt ansehen |
| 5 | Featured Projects | Портфолио 1 крупный + 2 | Alle Projekte |
| 6 | Warum wir | 6 принципов работы вместо суперлативов (sticky-левая колонка) | — |
| 7 | Arbeitsprozess | Снять страх «ремонт = хаос» | Besichtigung vereinbaren |
| 8 | Materialien / Qualität | Что скрыто под поверхностью | — |
| 9 | Kundenstimmen | Только реальные; иначе честный блок | Referenzen anfragen |
| 10 | FAQ | Снять возражения + FAQ-Schema | — |
| 11 | Region | Local SEO «Innenausbau in Schleswig-Holstein» | — |
| 12 | CTA | Финальная конверсия: форма / звонок / WhatsApp | 3 канала |
| 13 | Footer | Навигация, контакты, регион, правовые страницы | Projekt anfragen |

CTA-формулировки чередуются: «Projekt anfragen», «Kostenlose Anfrage», «Besichtigung vereinbaren», «Jetzt Projekt besprechen» — по одной основной на экран, без поп-апов.

## Страница услуги (шаблон)

Breadcrumbs → H1 + короткое описание → широкое фото → вводный текст + CTA (с предвыбором услуги в форме через `?leistung=`) → **Vorteile** / **Was dazugehört** / **Typische Anlässe** → проекты с этой услугой → FAQ → другие услуги группы → CTA. Schema: `Service` + `BreadcrumbList` + `FAQPage`.

## Страница проекта (шаблон)

Breadcrumbs → H1, краткое описание → таблица фактов (Ort, Objekt, Leistung, Dauer) → **Before/After slider** → Ausgangslage / Lösung + CTA «Ähnliches Projekt anfragen» → галерея → другие проекты → CTA.

## Форма заявки — UX

Двухшаговая, чтобы первый шаг был коротким:

1. **Kontakt & Projekt (обязательное, ~1 мин):** Name, Telefon, E-Mail (опц.), Ort, Objektart (4 крупные кнопки), Welche Arbeiten? (чипы, мультивыбор).
2. **Details (опционально):** Fläche, Zeitraum, Budget (опц.), Nachricht, **фото** (до 6, камера на мобильном), согласие DSGVO.

- Клиентская валидация шага 1 до перехода, серверная (zod) — финальная.
- Фото сжимаются в браузере до 1600 px JPEG (~200–400 КБ) → быстрая отправка по мобильной сети и укладка в лимиты serverless.
- Спам-защита без капчи: honeypot + минимальное время заполнения + rate limit.
- При ошибке отправки — сообщение с прямой ссылкой на WhatsApp (заявка не теряется).
- Экран успеха объясняет следующий шаг и даёт телефон.

## Mobile UX (Mobile First)

- **Sticky header** 64 px с полупрозрачным blur после скролла; бургер → полноэкранное меню с крупными пунктами и CTA.
- **Фиксированная нижняя панель** (только < 640 px): `Anrufen` · `WhatsApp` · `Projekt anfragen` → **контакт за 1 тап**, учтён `safe-area-inset-bottom`.
- Все интерактивные элементы ≥ 44–56 px; поля ввода 16 px (без авто-зума iOS); `inputMode="tel"` / `numeric`, `autocomplete`.
- Hero-видео на мобильном не загружается (экономия трафика) — показывается постер.
- Before/After: `touch-pan-y` — горизонтальный жест двигает слайдер, вертикальный скроллит страницу.
- Без горизонтального скролла (проверено Playwright на 390 px и 1440 px).

## Доступность

Skip-link, `aria-current` в навигации, нативные `<details>` для FAQ, `fieldset/legend` в форме, `aria-invalid` + текст ошибок, фокус-кольцо в цвете акцента, `prefers-reduced-motion`, alt-тексты на немецком для всех изображений.
