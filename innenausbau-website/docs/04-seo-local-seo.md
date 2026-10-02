# 04 · SEO и Local SEO

## Техническая база (реализовано)

| Элемент | Реализация |
|---|---|
| Title / Description | `pageMetadata()` на каждой странице, шаблон `%s | NORDRAUM` |
| Canonical | абсолютный URL из `NEXT_PUBLIC_SITE_URL` |
| Open Graph / Twitter | изображение страницы (из манифеста), `de_DE` |
| H1 | ровно один на страницу (Hero / PageHeader) |
| Schema.org | `HomeAndConstructionBusiness` + `GeneralContractor` (глобально), `Service` (услуги), `FAQPage`, `BreadcrumbList` |
| Sitemap | `/sitemap.xml` из контента (услуги, проекты, только опубликованные локации) |
| Robots | `/robots.txt`, `/api/` закрыт; Impressum/Datenschutz — `noindex, follow` |
| Рендеринг | все контентные страницы — статический HTML (SSG) |
| Изображения | AVIF/WebP, `sizes`, lazy, немецкие alt-тексты |

Schema не содержит выдуманных данных: плейсхолдеры `[…]` автоматически выбрасываются, `aggregateRating` не выводится вообще, пока нет реальных отзывов.

## Ключевые запросы → страницы

| Запрос | Целевая страница | Title | H1 |
|---|---|---|---|
| Innenausbau Schleswig-Holstein | `/` + `/leistungen/innenausbau` | Innenausbau, Renovierung & Sanierung in Schleswig-Holstein | Wir verwandeln Räume. / Innenausbau |
| Renovierung Schleswig-Holstein | `/leistungen/renovierung` | Renovierung in Schleswig-Holstein | Renovierung |
| Sanierung Schleswig-Holstein | `/leistungen/sanierung` | Sanierung in Schleswig-Holstein | Sanierung |
| Trockenbau Schleswig-Holstein | `/leistungen/trockenbau` | Trockenbau in Schleswig-Holstein | Trockenbau |
| Badsanierung Schleswig-Holstein | `/leistungen/badsanierung` | Badsanierung in Schleswig-Holstein | Badsanierung |
| Malerarbeiten Schleswig-Holstein | `/leistungen/malerarbeiten` | Malerarbeiten in Schleswig-Holstein | Malerarbeiten |
| Komplettrenovierung Schleswig-Holstein | `/leistungen/komplettrenovierung` | Komplettrenovierung in Schleswig-Holstein | Komplettrenovierung |

Meta Descriptions для каждой услуги лежат в `content/services.ts → seo.description` (≤ 160 символов, регион + выгода).

### H2-структура Home
Alles für den Innenraum… · Der Unterschied liegt im Ergebnis · Räume, die wir verwandelt haben · Qualität ist kein Versprechen… · Sechs Schritte… · Was man später nicht sieht… · Was unsere Kunden sagen · Häufige Fragen · **Innenausbau in Schleswig-Holstein** · Jetzt Projekt besprechen.

## Local SEO стратегия

1. **Google Unternehmensprofil** (самый сильный фактор): категория «Innenausbauunternehmen»/«Renovierungsunternehmen», зона обслуживания SH + HH, реальные фото проектов, запрос отзывов после каждой приёмки (ссылка в Make follow-up письме). Ссылку внести в `site.social.googleBusiness` → кнопка появится в блоке отзывов.
2. **NAP-консистентность:** имя, адрес, телефон — идентично на сайте, в профиле Google, Handwerkskammer, Gelbe Seiten, 11880, MyHammer.
3. **Блок «Innenausbau in Schleswig-Holstein»** на Home с регионами (Dithmarschen, Steinburg, Rendsburg-Eckernförde, Pinneberg, Hamburg).
4. **Location pages** `/innenausbau/[ort]` — архитектура готова, **страницы пока не создаются**.

### Правила для location pages (anti-doorway)

Страница города публикуется (`published: true` в `content/locations.ts`) только если есть:
- уникальный `intro` (не шаблон с заменой города);
- минимум одно **реальное референс-проектов в этом городе** (`projectSlugs`) **или** конкретные локальные заметки (`localNotes`: типичная застройка — например, кирпичные дома 1920–30-х в Heide, расстояние/выезд, контакт);
- собственные фото.

Без этого маршрут отдаёт 404 и не попадает в sitemap. Подготовлены: Heide, Brunsbüttel, Itzehoe, Rendsburg, Neumünster, Kiel, Elmshorn, Hamburg.

## Контент-план (после запуска)

- 1 реальный проект в месяц с Before/After → страница проекта + пост в Google-профиле.
- Ратгебер-статьи (будущий раздел `/ratgeber`): «Badsanierung Kosten – wovon sie abhängen», «Spachtelqualität Q1–Q4 erklärt», «Altbau sanieren in Schleswig-Holstein: typische Probleme». Без выдуманных цен — только факторы.
- Отдельные FAQ для каждой услуги (сейчас используются общие).
