# RAIV — архитектура агентов и тарифов

## Принцип
Каждый агент — отдельный модуль с одной зоной ответственности. Любое действие агента проходит через **Guard**, который спрашивает **PlanManager**: оплачен ли тариф и входит ли функция в него. Опасные действия агент не выполняет — только создаёт **Proposal** владельцу.

```
Telegram / Make ──► Agent ──► Guard ──► PlanManager ──► Subscription (payment_status, plan_id, сумма, срок)
                                 │
                                 └── FORBIDDEN → Proposal → владелец одобряет
```

## Тарифы и feature flags (`raiv_platform/plans.py`)
| plan_id | Цена | Функции |
|---|---|---|
| `start_350` | 350 € | sales_bot, stock_basic |
| `business_800` | 800 € | + customers, marketing, analytics, broadcasts, promo_codes, bonuses |
| `pro_1500` | 1500 € | + ai_business, make_automation, api_integrations, external_services |

## Агенты (`raiv_platform/agents/`)
| Агент | Flag | Делает | Не может |
|---|---|---|---|
| Sales | sales_bot | каталог, вес, расчёт по цене из каталога, оформление, списание остатка | менять цены |
| Stock | stock_basic | остатки, дефицит, список пополнения (черновик) | удалять товары |
| Customer | customers | база, история, персональные предложения (как Proposal) | рассылать без одобрения |
| Marketing | marketing | посты, акции, напоминания; скидки — только Proposal | менять цены |
| Analytics | analytics | дневной отчёт, динамика к вчера, топ товаров | — |
| AI Business | ai_business | сводит продажи + остатки + клиентов → «что сделать сегодня» | действовать сам |

## Жёсткие правила (проверены тестами)
1. Функции открываются **только** при `payment_status == "paid"`, сумме ≥ цены тарифа и не истёкшем сроке. `pending`, `failed`, `refunded`, недоплата, неизвестный plan_id → **ничего**.
2. `CHANGE_PRICE`, `GRANT_PLAN`, `DELETE_DATA` запрещены любому агенту (`GuardError`) — только Proposal.
3. `PlanManager.change_plan` всегда падает: тариф меняет только запись об оплате из платёжной системы (webhook Stripe/PayPal), не код и не агент.
4. Цена в заказе берётся из каталога, не из ввода покупателя.

## Запуск тестов
```
cd platform && python3 -m unittest discover -s tests -v
```

## Что дальше (не сделано)
- Хранилище: сейчас in-memory `Store`; нужна БД (Make Data Store / SQLite / Postgres).
- Источник payment status: webhook платёжной системы → запись Subscription (с проверкой подписи).
- Хостинг: Python-ядро нужно где-то запускать (небольшой сервер или serverless); текущий бот RAIV_FISH работает в Make и пока ядро не использует.
- Подключение: Make-сценарий вызывает ядро по HTTP для Stock/Analytics; Sales пока остаётся в Make.
- Фото товаров в каталоге, корзина в Telegram-интерфейсе.
