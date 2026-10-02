# 07 · Performance и Deployment

## Performance (цель: Lighthouse 90+, хорошие Core Web Vitals)

| Мера | Реализация |
|---|---|
| Статический HTML | Все контентные страницы — SSG (`○`/`●` в выводе `next build`), CDN-кэшируемые |
| Минимум JS | Server Components; клиентские острова только: Header, LeadForm, BeforeAfterSlider, Counter, HeroVideo, RevealObserver. Нет UI-библиотек, нет анимационных библиотек, иконки — inline SVG |
| Минимум CSS | Tailwind v4 генерирует только используемые классы |
| Шрифт | `next/font` self-hosted, `display: swap`, один variable-шрифт, subset latin/latin-ext |
| LCP | Постер Hero через `next/image` с `priority` + `fetchPriority="high"`; видео подгружается **после** `load`, только ≥ 768 px, без `prefers-reduced-motion` и `saveData` |
| Изображения | `next/image`: AVIF → WebP, адаптивные `sizes`, lazy loading по умолчанию, `deviceSizes` до 2560 |
| CLS | Все изображения в контейнерах с `aspect-ratio`; шрифт с fallback-метриками от next/font |
| INP | Один `IntersectionObserver` для всех reveal-анимаций; слайдер — нативный range input; пассивный scroll-listener |
| Фото в форме | Сжатие в браузере до 1600 px → быстрая отправка с мобильного |
| Анимации | Только `transform/opacity/clip-path`; выключаются при reduced motion |

**Проверка:** `npm run build && npm start`, затем Lighthouse (Mobile) в Chrome DevTools или PageSpeed Insights после деплоя. Рекомендуется после `npm run assets:fetch` перевести ассеты на локальные (`ASSET_SOURCE = "local"`) — одно меньше внешнее соединение.

## Deployment

### Требования
Node.js ≥ 20.9 (рекомендуется 22 LTS).

### Локально
```bash
cd innenausbau-website
cp .env.example .env.local      # LEAD_SINK=log для разработки
npm install
npm run dev                     # http://localhost:3000
npm run typecheck && npm run build
```

### Вариант A — Vercel (рекомендуется для Next.js)
1. Импортировать репозиторий, **Root Directory** = `innenausbau-website`.
2. Environment Variables: `NEXT_PUBLIC_SITE_URL`, `LEAD_SINK=make`, `MAKE_WEBHOOK_URL`, `MAKE_WEBHOOK_SECRET`.
3. Region: `fra1` (Frankfurt) — ближе к аудитории, DSGVO.
4. Подключить домен, включить HTTPS (автоматически).

### Вариант B — Netlify
1. *Add new site → Import from Git*, Base directory `innenausbau-website`, Build command `npm run build` (Next.js Runtime подключается автоматически).
2. Те же env-переменные.
3. Лимит тела функции ~6 MB — форма укладывается за счёт сжатия фото (≤ 8 MB проверка на сервере; при необходимости снизить `UPLOAD_LIMITS.maxTotalBytes` до 5.5 MB).

### Вариант C — Свой сервер / Docker (Hetzner, IONOS)
```bash
npm ci && npm run build
NODE_ENV=production PORT=3000 npm start      # за Nginx/Caddy с HTTPS
```
Для Docker добавить `output: "standalone"` в `next.config.ts`.

### После запуска
- [ ] Заменить все плейсхолдеры (см. `docs/03-components-content.md`).
- [ ] Юридически проверить Impressum и Datenschutz.
- [ ] Тестовая заявка → Telegram, письма, Drive, CRM.
- [ ] Google Search Console: добавить домен, отправить `/sitemap.xml`.
- [ ] Google Unternehmensprofil: ссылка на сайт, ссылку на профиль — в `site.social.googleBusiness`.
- [ ] Lighthouse Mobile ≥ 90.
- [ ] (Опционально) Analytics без cookies (Plausible / Matomo cookieless) — внести в Datenschutz.
