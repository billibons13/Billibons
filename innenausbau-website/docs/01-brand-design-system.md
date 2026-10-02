# 01 · Brand-концепция и Design System

## Позиционирование

**Идея бренда:** «Wir verwandeln Räume.» — компания продаёт не «ремонт», а **трансформацию** пространства: VORHER → NACHHER.

Сайт не хвалит компанию лозунгами («Wir sind die Besten»). Каждый блок отвечает на вопрос клиента
**«Почему я могу доверить этим людям свой дом?»** — через проверяемые признаки работы:

| Ценность | Как она показана на сайте |
|---|---|
| Qualität / Präzision | Q1–Q4 Spachtel, план швов плитки до укладки, детальные фото (шов, теневой паз) |
| Saubere Ausführung | Защита помещений, ежедневная уборка, фото «аккуратной стройки» |
| Transparente Kommunikation | Один контакт, смета по позициям, регулярные апдейты с фото |
| Zuverlässigkeit / Termine | Реалистичный график, этапы, протокол приёмки |
| Hochwertige Materialien | Блок «Materialien & Qualität», образцы материалов |
| Professionelle Planung | 6-шаговый процесс, координация смежников (электрика/сантехника) |

**Тон текста (DE):** спокойный, конкретный, без превосходных степеней. Короткие предложения, «Sie»-форма, факты вместо обещаний.

**Название и логотип:** `AKKERMAN` + монограмма `SK` — по эскизу владельца: купол (полукруг на основании), «AKKERMAN» по дуге, «SK» в центре. Линия основания — в акцентном цвете Ziegel.
- Полный логотип: `BrandMark` (`components/layout/Logo.tsx`) — футер, документы; файлы `public/brand/akkerman-logo-dark.svg` / `-light.svg`.
- Компактный знак (купол + SK): `BrandIcon` — шапка (вместе со словом AKKERMAN), favicon `app/icon.svg`, `public/brand/akkerman-icon.svg`.
- В шапке дуговая надпись не используется: при высоте 40 px она нечитаема.
- Данные компании (юр. название, телефон, адрес) пока плейсхолдеры в `src/config/site.ts`.

## Правило честности (Trust)

- Никаких выдуманных цифр, лет опыта, сертификатов, отзывов.
- Все поля в `site.facts` по умолчанию `null`/пусто → соответствующие элементы **не выводятся** (ни на сайте, ни в Schema.org).
- Отзывы (`content/testimonials.ts`) пустые → блок показывает честный текст «публикуем только реальные отзывы».
- Все изображения сейчас — **визуализации Higgsfield**. Пока `site.labelVisualizations = true`, на них стоит метка «Visualisierung», а проекты помечены «Beispielprojekt». Это требование честной рекламы (UWG) — снять только после замены на реальные фото.
- Фразы, которые компания должна подтвердить, помечены `[Bitte vom Betrieb bestätigen]` (например, бесплатный выезд).

## Цвета

| Токен | HEX | Использование |
|---|---|---|
| `paper` | `#F5F3EF` | Фон (Off-White) |
| `paper-2` | `#EBE8E2` | Вторичный фон секций |
| `beton-100` | `#DEDBD5` | Линии, плейсхолдеры изображений |
| `beton-300` | `#B9B5AD` | Placeholder-текст |
| `beton-500` | `#8A867F` | Eyebrow, мета-текст |
| `anthrazit` | `#2B2D2F` | Вторичный текст, hover |
| `ink` | `#121314` | Основной текст, тёмные секции |
| `ziegel` | `#A8462A` | **Единственный акцент** — кирпич северогерманских домов. CTA, маркеры, номера |

Акцент используется точечно: основная CTA, тонкая линия перед eyebrow, номера, точка в «Räume.». Контраст `ziegel` на `paper` ≈ 5.6:1 (AA для текста).

## Типографика

- Шрифт: **Inter Tight** (variable, grotesk), self-hosted через `next/font` → без запросов к Google в рантайме (DSGVO).
- Шкала (fluid, `clamp`):
  - `text-display` 44 → 104 px, line-height 0.95, tracking −0.035em (H1 Hero, CTA)
  - `text-h2` 32 → 56 px, tracking −0.03em
  - `text-h3` 20 → 26 px
  - Body 16–20 px, line-height 1.6
  - `.eyebrow` 11.5 px, uppercase, tracking 0.22em
- `text-balance` для заголовков, `text-pretty` для абзацев.

## Сетка и пространство

- Контейнер `max-w-[90rem]` (1440 px), поля 20/32/48 px.
- 12-колоночная сетка, асимметричные композиции (7/5, 5/6) — «архитектурная» вёрстка.
- Вертикальный ритм секций: 80 / 112 / 144 px (`.section`).
- Тонкие линии `1px` вместо карточек с тенями. Углы — прямые (без `rounded`), только кнопка-ручка слайдера круглая.

## Компоненты UI (атомы)

| Компонент | Файл | Примечание |
|---|---|---|
| `ButtonLink` | `components/ui/Button.tsx` | Варианты: primary (Ziegel), dark, outline, ghost, light. Мин. высота 48/56 px |
| `SectionHeading` | `components/ui/SectionHeading.tsx` | eyebrow + H2 + intro, режим `split` |
| `SiteImage` | `components/ui/SiteImage.tsx` | `next/image` + метка «Visualisierung» |
| `BeforeAfterSlider` | `components/ui/BeforeAfterSlider.tsx` | Нативный `input[type=range]` → клавиатура + screen reader |
| `Counter` | `components/ui/Counter.tsx` | Только для проверяемых значений |
| `Icons` | `components/ui/Icons.tsx` | Inline-SVG, без иконочных библиотек |

## Анимации (сдержанно)

- **Scroll reveal:** fade + translateY 24px, 0.9s, `cubic-bezier(.22,1,.36,1)`; один общий `IntersectionObserver` (`RevealObserver`).
- **Image masking:** `data-reveal="mask"` — `clip-path` раскрывает Hero/крупные изображения.
- **Hover:** медленный zoom 1.04 на изображениях карточек, заливка стрелки акцентом.
- **Counter:** easeOutCubic 1.2s.
- **Before/After slider.**
- Всё отключается при `prefers-reduced-motion`; без JS контент сразу видим (класс `.js` ставится инлайн-скриптом).
