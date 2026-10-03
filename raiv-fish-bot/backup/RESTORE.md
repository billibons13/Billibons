# Полная копия проекта RAIV_FISH и восстановление

## Что где (Make, zone eu1, team 2241615)
| Объект | ID | Статус |
|---|---|---|
| Сценарий v2 (корзина) — РАБОЧИЙ | 7707233 | включён, вебхук 3818482 `https://hook.eu1.make.com/m78gj1qqmhr42sm7mrzqbcjj5d93ewiu` |
| Сценарий v1 (без корзины) — РЕЗЕРВ | 7706268 | выключен, вебхук 3818163 `https://hook.eu1.make.com/xykao4wf3fux8knvlu4y2vuva6mhtz82` |
| Data store «RAIV_Fish — корзины покупателей» | 203268 | структура 609962 (text, total, count) |
| Telegram-подключение @RAIV_FISH_bot | 11456488 | |
| Канал заказов RAIVFISH | chat_id -1004438320479 | бот — админ |
| Инструмент «Telegram API (чат)» | 7706891 | getChatMember / sendMessage |
| Инструмент «updates/webhook» | 7706894 | setWebhook / getUpdates |
| Инструмент «тест v2 (отправка апдейта)» | 7707234 | шлёт тестовый апдейт на рабочий вебхук v2 |
| Инструмент «чтение корзины» | 7707208 | GetRecord по chat_id |

## Файлы в репозитории
- `backup/v2_cart_blueprint.json` — полный blueprint рабочей версии (можно импортировать в Make: Create scenario → Import blueprint).
- `backup/v1_no_cart_blueprint.json` — полный blueprint версии без корзины.
- `generate_blueprint.py` — генератор (каталог, цены, наличие — список `cats`).

## Откат на v1 за 1 минуту
1. Включить сценарий 7706268.
2. Инструмент 7706894: `setWebhook` с url `https://hook.eu1.make.com/xykao4wf3fux8knvlu4y2vuva6mhtz82`.
3. (по желанию) выключить 7707233.

## Восстановление с нуля
1. Make → Create scenario → Import blueprint → `backup/v2_cart_blueprint.json`.
2. Пересоздать при необходимости: Telegram-подключение (токен бота), data store со структурой text/total/count, вебхук; поправить ID в блупринте (CONN, HOOK, DS в `generate_blueprint.py` и перегенерировать).
3. setWebhook на URL нового вебхука.

## v3 Business (01.10.2026)

| Что | ID |
|---|---|
| Рабочий сценарий (тот же) | 7707233 «Заказы v3 (Business) — РАБОЧИЙ» |
| Ежедневный отчёт 21:00 | 7707443 (blueprint: `daily_report_blueprint.json`) |
| Data store: клиенты | 203277 (структура 609976) |
| Data store: заказы | 203280 (структура 609977) |
| Data store: промокоды | 203278 (структура 609978, поиск по полю `code`) |
| Data store: продажи по дням | 203279 (структура 609979) |
| Data store: корзины | 203268 (структура 609962 + promo/pcode/disc/bused/final/city) |

Blueprint v3: `v3_business_blueprint.json` (генератор: `generate_blueprint.py`).
Откат на v2 с корзиной и кнопкой предложения: загрузить `v2_cart_offer_blueprint.json` в сценарий 7707233.

Команды владельца (chat 6883357001): `/admin`, `/report`, `/promo КОД 10`, `/send текст`. Клиент: `/stop` — отписка от рассылок.

## Pro (01.10.2026)

| Что | ID | Расписание |
|---|---|---|
| AI-помощник владельца (Make AI Tools, только советы) | 7707489 (`pro_ai_assistant_blueprint.json`) | ежедневно 08:30 → личка владельца |
| Напоминания «давно не заказывали» (14 дней, одно на период) | 7707493 (`pro_reminders_blueprint.json`) | ежедневно 11:00 |
| Онлайн-оплата Stripe (test, conn 11458868): кнопка «💳 Оплатить онлайн» после заказа (основной сценарий, модули 130–131) | 7707233 | при заказе |
| Подтверждение оплаты (hook 3818580, checkout.session.completed) | 7707560 | мгновенно |
| Служебный вызов Stripe API | 7707531 | вручную |

Генератор: `generate_pro.py`. Поле клиентов `last_seen` теперь типа date, добавлено `reminded`.

## Этап 1 «10/10» (v5, 01.10.2026)

| Что | ID | Расписание |
|---|---|---|
| Основной бот v5: короткий старт, слоты, мин. 20 €, номер заказа, статусы, оценка, рефералка | 7707233 (`v5_stage1_blueprint.json`) | мгновенно |
| Брошенная корзина (2 ч без действий, одно напоминание, 10:00–20:00) | 7707656 (`abandoned_cart_blueprint.json`, `generate_abandoned.py`) | каждый час |
| Отчёт 21:00 + средняя оценка и брошенные корзины | 7707443 (`daily_report_blueprint.json`) | 21:00 |
| Меню команд и описание бота (setMyCommands / setMyDescription) | инструмент 7707653 | разово |

## Этап 2: витрина (v6, 01.10.2026)

| Что | Где |
|---|---|
| Бот v6: кнопка «🛍 Витрина», корзина из витрины (цены считает бот), цветные кнопки | сценарий 7707233 (`v6_miniapp_blueprint.json`) |
| Витрина Mini App | GitHub Pages, ветка `gh-pages` → https://billibons13.github.io/Billibons/ (`miniapp/DEPLOY.md`) |
Откат на v5: загрузить `v5_stage1_blueprint.json` в сценарий 7707233.

## Этап 3: живой каталог и склад (v7–v8, 01.10.2026)

| Что | Где |
|---|---|
| Бот v8: каталог из data store 203278 (`cat_<код>`: цена, наличие), /price /stock /catalog с подтверждением, «📦 Склад» (/sklad, кнопки ✅/❌), корзина по ссылке `/start c_...` | сценарий 7707233 (`v8_sklad_blueprint.json`; предыдущая — `v7_catalog_blueprint.json`) |
| Каталог API для витрины (цены и наличие, CORS *) | сценарий 7708101, хук https://hook.eu1.make.com/hzm5bgeixv8k4652x3ofaaxw378nwyhu |
| 📦 Агент склада: утренняя сводка наличия владельцу + кнопки разделов | сценарий 7708259 (`stock_agent_blueprint.json`, `generate_stock_agent.py`), ежедневно 09:00 |
| Разовая загрузка каталога (43 товара) | сценарий 7708099 (выключен) |
Откат на v7: загрузить `v7_catalog_blueprint.json` в сценарий 7707233. Каталог при откате не теряется — он в data store.

## Pro: надёжность (v9.2, 03.10.2026)

| Что | Где |
|---|---|
| Бот v9.2 Pro: свой вес «700 г»/«1 кг» с пересчётом единиц, лимиты (10 кг / 5000 г / 50 шт), промокод сохраняется в корзине, /promo только 0–50 %, защита от повторного заказа, бонусы и реферальные 3 € начисляются только по «✅ Доставлен» и один раз (`bonus_done`), Stripe-кнопка пока только владельцу, учёт кг/шт в заказах, днях и месяцах, /report с кг и итогом месяца | сценарий 7707233 (`v9_pro_blueprint.json`; откат — `v8_sklad_blueprint.json`) |

Проверено 03.10: «700 г» → 0,7 кг; «50 кг» отклонено; /promo 150 % не создан; повтор телефона — второй заказ не создан; «Доставлен» — бонус +1,23 € начислен один раз.

## Контакты и медиа (v9.4, 03.10.2026)
Кнопка «📇 Контакты» в главном меню и команда /contacts: TikTok @vasya_raivfish, Instagram vasya_ivanchuk_, Facebook, канал @raiv_fish1, поставщик @vasyaivancuk, продавец. Ссылки — список `CONTACT_LINKS` в generate_blueprint.py. Сценарий 7707233 (`v9_pro_blueprint.json`; предыдущая — `v9_2_blueprint.json`).
