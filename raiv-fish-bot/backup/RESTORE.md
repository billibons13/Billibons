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
