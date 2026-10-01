# Схема конфига клиента — v1.0

Один JSON-файл описывает одного клиента (магазин, кондитерскую, салон и т. п.). Генератор ядра собирает из него сценарии Make (а позже — Python-ядро), не зная ничего о конкретной стране, языке или отрасли.

Примеры: `platform/clients/raiv_fish.example.json` (шаблон Shop, DE, RU, EUR), `platform/clients/bakery.example.json` (шаблон Pre-order, CH, DE/EN, CHF).

## 0. Принципы

1. **Конфиг — только данные.** Логика (проверки денег, прав, согласий) живёт в ядре и одинакова для всех клиентов. Конфиг задаёт параметры, но не может выключить стандартные проверки (раздел 12).
2. **Никаких секретов.** Токены ботов, адреса вебхуков, ключи Stripe, `secret_token` в файл не пишутся. Вместо них — ссылки:
   - `make_connection:<id>` — подключение Make, где лежит токен;
   - `secret://<client_id>/<name>` — значение из хранилища секретов (переменные Make / env / vault).
   Загрузчик отклоняет конфиг, если находит строку, похожую на токен Telegram (`\d{6,}:[A-Za-z0-9_-]{30,}`), ключ Stripe (`\b(sk|rk|pk)_(live|test)_`, `\bwhsec_`) или URL `hook.*.make.com`.
3. **Тариф решает PlanManager, не конфиг.** Модуль работает, только если он включён в конфиге **и** входит в оплаченный тариф (`plans.py`). Конфиг может только сузить набор функций.
4. **Тексты многоязычные.** Любая строка для покупателя — объект `{"<lang>": "..."}`. Обязателен язык `locale.default_language`; если перевода нет, берётся он.
5. **Деньги** — числа в основных единицах валюты (`8.5` = 8,50 €), формат показа задаёт `currency`. Внутри расчётов — целые центы (`round(x*100)`).
6. **ID** Telegram и чатов — строки (`"-1004438320479"`), чтобы не терять точность. ID объектов Make — числа.
7. Ключи, начинающиеся с `_` (`_comment`), игнорируются. Значение `"TODO..."` в обязательном поле — ошибка при `env: "prod"`, предупреждение при `env: "test"`.

## 1. Верхний уровень

| Поле | Тип | Обяз. | По умолчанию | Описание |
|---|---|---|---|---|
| `schema_version` | string | да | — | `"1.0"`. Мажорная версия меняется при несовместимых изменениях. |
| `client_id` | string `[a-z0-9_]{3,40}` | да | — | Уникальный ID клиента, он же `shop_id` в `PlanManager`. |
| `env` | `prod` \| `test` | нет | `prod` | `test` — тестовый бот (свои чаты, хранилища, Stripe test). |
| `template` | `shop` \| `preorder` \| `termin` \| `request_quote` | да | — | Базовый сценарий (раздел 10). |
| `plan` | object | да | — | Тариф и аддоны (раздел 9). |
| `business` | object | да | — | Раздел 2. |
| `locale` | object | да | — | Раздел 3. |
| `currency` | object | да | — | Раздел 3. |
| `texts` | object | нет | пакет шаблона | Раздел 4. |
| `channels` | object | да | — | Раздел 5. |
| `catalog` | object | для `shop`, `preorder` | — | Раздел 6. |
| `services`, `staff`, `schedule` | object | для `termin` | — | Раздел 6.4. |
| `preorder` | object | для `preorder` | — | Раздел 6.3. |
| `request_form` | object | для `request_quote` | — | Раздел 6.5. |
| `fulfillment` | object | для `shop`, `preorder` | — | Раздел 7. |
| `payment` | object | да | — | Раздел 8. |
| `modules` | object | нет | все `false`, кроме `cart` | Раздел 9. |
| `compliance` | object | да | — | Раздел 11. |
| `security` | object | нет | безопасные значения | Раздел 11.3. |
| `limits` | object | нет | см. ниже | Раздел 12.2. |
| `infra` | object | да | — | Раздел 13. |

## 2. `business`

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `name` | string | да | — | Название в текстах бота. |
| `tagline` | i18n | нет | — | Одна строка под названием. |
| `category` | string | нет | `retail` | `food_retail`, `bakery`, `beauty`, `services`… — для подсказок AI и шаблонов текстов. |
| `contact.telegram` / `.phone` / `.email` | string | хотя бы одно | — | Показывается в /help и /privacy. |
| `legal.legal_name`, `.address` | string | да при `prod`, если `compliance.regime` требует Impressum | — | Для /privacy и чеков. |
| `legal.vat_id` | string\|null | нет | null | |
| `legal.small_business_vat_exempt` | bool\|null | нет | null | Влияет на строку «без НДС» в чеке. |
| `seller_promo.enabled` | bool | нет | `false` | Кнопка «💼 Хочу такой бот» (реклама платформы). Включается только в демо-ботах. |
| `seller_promo.seller_contact` | string | если `enabled` | — | |

## 3. `locale` и `currency`

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `locale.country` | ISO 3166-1 alpha-2 | да | — | Определяет набор правил в `compliance` по умолчанию. |
| `locale.region` | string | нет | — | Земля/кантон — для праздников и налогов. |
| `locale.timezone` | IANA | да | — | Все даты, слоты, отчёты, «сегодня/завтра». |
| `locale.languages` | string[] (ISO 639-1) | да | — | Языки бота. |
| `locale.default_language` | string | да | `languages[0]` | Должен входить в `languages`. |
| `locale.language_detection` | `fixed` \| `telegram_language_code` \| `ask` | нет | `fixed` при одном языке, иначе `telegram_language_code` | Плюс команда `/language`. |
| `locale.date_format`, `time_format` | string | нет | `DD.MM.YYYY`, `HH:mm` | Формат Make `formatDate`. |
| `currency.code` | ISO 4217 | да | — | `EUR`, `CHF`, `PLN`, `UAH`… Передаётся в Stripe в нижнем регистре. |
| `currency.symbol` | string | нет | код | `€`, `CHF`, `zł`. |
| `currency.symbol_position` | `before` \| `after` | нет | `after` | `8,50 €` / `CHF 8.50`. |
| `currency.decimal_separator` | string | нет | `,` | |
| `currency.thousands_separator` | string | нет | `.` | Для CH — `’`. |
| `currency.decimals` | int 0–3 | нет | 2 | |
| `currency.always_show_decimals` | bool | нет | `true` | `8,50 €`, а не `8,5 €` (аудит v5, раздел B). |
| `currency.rounding` | `floor_cent` \| `round_cent` \| `nearest_0.05` | нет | `round_cent` | Скидки и бонусы — всегда вниз (`floor`), в пользу клиента; итог — по этому правилу. |

## 4. `texts`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `pack` | string | нет | Пакет стандартных текстов шаблона (`shop_ru_v1`, `preorder_de_en_v1`…). Пакеты лежат в ядре, по одному файлу на язык. |
| `overrides.<lang>.<key>` | string | нет | Замена отдельных текстов. Плейсхолдеры: `{order_no}`, `{min_order}`, `{zones}`, `{bonus_pct}`, `{lead_time}`, `{free_from}`, `{date}`, `{slot}`. Деньги в плейсхолдерах уже отформатированы по `currency`. |

Ограничения: текст ≤ 4096 знаков (лимит Telegram), стартовое сообщение ≤ 600 знаков (аудит v4), кнопки ≤ 64 байт `callback_data`. Загрузчик проверяет, что для каждого обязательного ключа пакета есть текст на `default_language`.

## 5. `channels`

### 5.1 `channels.customer[]` — где пишет покупатель

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `type` | `telegram_bot` | да | — | Сейчас ядро умеет только Telegram. Зарезервировано: `whatsapp_cloud`, `instagram`, `web_chat` (поле `planned_customer_channels`). |
| `bot_username` | string | да | — | Без `@`. |
| `bot_user_id` | string | да при `prod` | — | Для проверки «бот — админ канала заказов». |
| `token_ref` | ref | да | — | `make_connection:<id>` или `secret://…`. |
| `webhook.make_hook_id` | int\|null | да при `prod` | — | Только ID. URL — `webhook.url_ref`. |
| `webhook.secret_token_ref` | ref | да | — | Значение для `setWebhook(secret_token=…)`; ядро фильтрует запросы без заголовка `X-Telegram-Bot-Api-Secret-Token` (CHK-01). |
| `webhook.rotate_required` | bool | нет | `false` | `true` — URL был раскрыт, нужен новый хук. Генератор выводит предупреждение. |
| `commands` | string[] | нет | из шаблона | Меню `setMyCommands`. `/privacy`, `/delete`, `/stop` добавляются всегда. |
| `mini_app.enabled`, `.url`, `.button_version` | | нет | `false` | Витрина Telegram Mini App. Витрина шлёт только коды и количества; цену считает бот (CHK-03). |

### 5.2 `channels.owner` — куда приходят заказы и кто управляет

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `owner_user_ids` | string[] ≥ 1 | да | Telegram ID владельцев. Только им доступны `/admin`, `/promo`, `/send`, `/report`. |
| `staff_user_ids` | string[] | нет | Курьеры/кондитеры: могут нажимать кнопки статусов, но не админ-команды. |
| `orders_chat_id` | string | да | Канал/группа заказов. Бот должен быть админом. |
| `reports_chat_id` | string | нет (= `orders_chat_id`) | Отчёт дня. |
| `ai_assistant_chat_id` | string | нет (= первый `owner_user_ids`) | Советы AI — лично владельцу. |
| `public_channel` | string\|null | нет | Публичный канал магазина (для постов с кнопками). |
| `public_channel_bot_admin` | bool | нет | Известно ли, что бот — админ публичного канала. |

## 6. Что продаём

### 6.1 `catalog` (Shop, Pre-order)

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `source` | `inline` \| `datastore` \| `sheet` | нет | `inline` | `inline` — каталог в конфиге, вшивается в blueprint (как сейчас `cats` + `switch()`). `datastore` — каталог в Make data store, цены и наличие меняются без переразвёртывания. `sheet` — Google Таблица (обещана в оферте, ещё нет). |
| `out_of_stock_mark` | string | нет | `❌` | |
| `show_out_of_stock` | bool | нет | `true` | Показывать в прайсе с пометкой или скрывать. |
| `photos.base_url`, `.pattern` | string | нет | — | `{code}` подставляется. |
| `units.<id>` | object | да | — | Единицы продажи (6.2). |
| `categories[]` | object | да (≥ 1) | — | Разделы. |
| `categories[].id` | string `[a-z0-9]{1,3}` | да | — | Входит в `callback_data` — коротко. |
| `categories[].title` | i18n | да | — | |
| `categories[].unit` | ключ `units` | да | — | |
| `categories[].price_per` | number | да | 1 | Цена указана за сколько единиц: `100` для «€ / 100 г», `1` для «€ / кг». |
| `categories[].qty_presets` | number[] | да | — | Кнопки быстрого выбора (в единицах `unit`). |
| `items[].code` | string | да | — | Уникален во всём каталоге, ≤ 8 знаков. Не переиспользуется после удаления товара (старые кнопки, CHK-07). |
| `items[].name` | i18n | да | — | |
| `items[].price` | number\|null | да | — | `null` только при `price_mode: "quote"`. |
| `items[].price_mode` | `fixed` \| `quote` | нет | `fixed` | `quote` — цена по запросу (модуль `request_quote`). |
| `items[].in_stock` | bool | да | — | |
| `items[].stock_qty` | number | нет | — | При наличии — списание остатка (`stock_basic`). |
| `items[].weight_g` | number | для `pcs` при включённой посылке | — | Вес одной штуки для расчёта посылки. |
| `items[].min_qty` / `max_qty` | number | нет | из `units` | Переопределение лимита для товара. |
| `items[].allergens` | string[] | нет (рекомендуется для еды) | — | Коды EU 1169/2011: `gluten`, `eggs`, `milk`, `nuts`, `fish`, `soy`… |
| `items[].variants[]` | `{id, label, price}` | нет | — | Размеры/варианты; цена варианта заменяет `price`. |
| `items[].options[]` | `{id, type, label, max_length, price}` | нет | — | Доп. поля: надпись на торте и т. п. Текст очищается и обрезается. |
| `items[].lead_time_hours`, `daily_capacity` | number | для `preorder` | из `preorder` | |
| `items[].photo` | string | нет | `photos.pattern` | |

### 6.2 `catalog.units.<id>`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `label` | i18n | да | `г`, `кг`, `шт.` |
| `price_label` | i18n | да | `€ / 100 г` — символ валюты подставляется из `currency`. |
| `input_hint` | i18n | если разрешён «свой вес/кол-во» | Подсказка для ввода. |
| `min_qty`, `max_qty`, `step` | number | да | Лимиты ввода (CHK-04). По умолчанию для `g`: 50 / 3000 / 10, `kg`: 0,1 / 10 / 0,1, `pcs`: 1 / 50 / 1. |

Ввод покупателя разбирается с явной единицей: `700 г` в разделе «кг» → 0,7 кг, а не 700 кг (CHK-04).

### 6.3 `preorder` (шаблон Pre-order)

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `default_lead_time_hours` | int | да | — | Минимум между заказом и выдачей. |
| `order_cutoff` | `HH:mm` | нет | — | После этого времени день заказа считается следующим. |
| `max_days_ahead` | int | нет | 30 | |
| `closed_weekdays`, `closed_dates` | string[] | нет | — | |
| `capacity_scope` | `per_item_per_day` \| `per_day` | нет | `per_item_per_day` | Лимит загрузки; занятая ёмкость освобождается при отмене/неоплате. |
| `requires_owner_confirmation` | bool | нет | `true` | Заказ «новый → подтверждён» вручную. |
| `confirmation_sla_minutes` | int | нет | 120 | Напоминание владельцу, если не подтвердил. |
| `cancellation.free_until_hours` | int | нет | — | |

### 6.4 `services`, `staff`, `schedule` (шаблон Termin)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `services[]` | `{code, name, duration_min, price, buffer_min, staff_ids[]}` | да | Услуги. |
| `staff[]` | `{id, name, telegram_user_id?}` | да (≥ 1) | Мастера/кабинеты. |
| `schedule.weekly` | `{mon: [["09:00","18:00"]], …}` | да | Рабочие часы по умолчанию. |
| `schedule.exceptions[]` | `{date, hours|closed}` | нет | Отпуск, праздники. |
| `schedule.slot_step_min` | int | нет (15) | Шаг сетки. |
| `booking.min_notice_hours`, `max_days_ahead` | int | нет (2, 30) | |
| `booking.cancel_until_hours` | int | нет (24) | |
| `booking.reminder_hours_before` | int[] | нет ([24, 2]) | Напоминания — сервисные, согласие на рекламу не нужно. |
| `booking.no_show_policy` | `none` \| `deposit` | нет | `deposit` → `payment.prepayment`. |

Хранилище слотов — отдельный data store `bookings` с ключом `<staff_id>|<date>|<HH:mm>`; запись создаётся атомарно (CHK-01a), двойная бронь невозможна.

### 6.5 `request_form` (шаблон Request/Quote и модуль `request_quote`)

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `fields[]` | `{id, type: text|number|date|choice|photo|phone, label, required, max_length}` | да | Вопросы по шагам. |
| `owner_reply_sla_hours` | int | нет (24) | |
| `quote_valid_days` | int | нет (7) | Ответ владельца → кнопка «Принять» → обычный заказ с этой ценой. Цена в заказе берётся из ответа владельца, не из ввода клиента. |

Опт (`modules.wholesale`) и товары `price_mode: "quote"` используют этот же поток.

## 7. `fulfillment` — как получает покупатель

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `min_order` | number | нет | 0 | Проверяется при подтверждении по сумме из корзины (CHK-03). |
| **`local_delivery`** | | | | Курьер владельца. |
| `.enabled` | bool | да | — | |
| `.fee` / `.free_from` | number / number\|null | нет | 0 / null | Базовая цена и порог бесплатной доставки. |
| `.zones[]` | `{id, name, fee}` | да при `enabled` | — | Города/районы. `fee` переопределяет базовую. |
| `.other_place` | `{enabled, fee, label, price_text}` | нет | `enabled:false` | «Другое место»: `fee: null` = «по договорённости», никогда не «бесплатно» без явного 0. |
| `.slots.windows[]` | `{id, day_offset | weekdays, from, to}` | нет | — | Окна доставки. |
| `.slots.hide_if_ends_within_min` | int | нет | 60 | Окно «сегодня» не предлагается, если до его конца меньше N минут (аудит v5, B). |
| **`pickup`** | | | | Самовывоз. |
| `.enabled`, `.points[]` `{id, name, address}`, `.slots` | | | `false` | |
| **`parcel`** | | | | Посылка по странам. |
| `.enabled` | bool | да | `false` | Требует модуль `parcel_shipping`. |
| `.carrier` | string | при `enabled` | — | Для текста и трекинга. |
| `.ship_days` | string[] | нет | — | Дни отправки. |
| `.packaging_weight_g` | number | нет | 0 | Добавляется к весу товаров. |
| `.max_parcel_weight_kg` | number | да при `enabled` | — | Больше — разбивка или отказ с подсказкой. |
| `.countries[]` | `{code, tiers: [{up_to_kg, price}]}` | да при `enabled` | — | Цена по весу: берётся первый тир, где `вес ≤ up_to_kg`. Все `price` при `enabled` — не `null`. |
| `.free_from` | number\|null | нет | null | |
| `.requires_address_fields` | string[] | нет | имя, улица, индекс, город, страна, телефон | |
| `.eu_only` | bool | нет | `true` | Вне ЕС — таможня и запреты на продукты; ядро это не считает, страны вне ЕС отклоняются. |

Вес посылки = Σ(кол-во в граммах; для `pcs` — `qty × weight_g`) + `packaging_weight_g`.

## 8. `payment`

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `methods[]` | object | да (≥ 1) | — | |
| `methods[].id` | `cash_on_delivery` \| `cash_on_pickup` \| `bank_transfer` \| `stripe_checkout` \| `telegram_stars` \| `paypal` | да | — | |
| `methods[].applies_to` | string[] | нет | все способы получения | Например, наличные только при курьере. |
| `methods[].connection_ref` | ref | для онлайн | — | |
| `methods[].mode` | `test` \| `live` | для онлайн | `test` | |
| `methods[].visible_to` | `owner_only` \| `all` | нет | `owner_only` при `test`, `all` при `live` | При `mode: test` значение `all` запрещено (CHK-08). |
| `methods[].min_amount` | number | нет | 0,50 (минимум Stripe) | |
| `methods[].payment_method_types` | string[] | нет | `["card"]` | `twint`, `klarna`, `paypal` — если доступны в стране. |
| `methods[].webhook_secret_ref` | ref | для `stripe_checkout` | — | Подтверждение оплаты проверяет подпись, номер заказа и сумму (CHK-08). |
| `prepayment.required_for` | string[] | нет | — | `parcel`, `preorder_items_over`, `booking`. |
| `prepayment.percent`, `threshold`, `deadline_hours`, `unpaid_action` | | нет | 100 / — / 24 / `cancel_and_release_capacity` | |

## 9. `plan` и `modules` (feature flags)

`plan.plan_id` — один из `PLANS` в `raiv_platform/plans.py`; `plan.addons` — оплаченные отдельно аддоны. Эффективный набор функций:

```
effective = PlanManager.features(client_id)   # только при payment_status == "paid", сумме ≥ цены, сроке
          ∩ { f | modules[f].enabled }
```

Генератор не собирает модули, которых нет в `effective`; для Make-сценариев, которые уже собраны, при окончании оплаты используется `PlanManager` → выключение сценариев модулей (только Proposal для владельца платформы, `Guard`).

| Модуль конфига | Feature в `plans.py` | Тариф сейчас | Параметры |
|---|---|---|---|
| `cart`, `repeat_order`, `order_statuses` | `sales_bot` | Start | `repeat_order.reprice` (всегда `true` по CHK-07) |
| остатки (`items[].stock_qty`) | `stock_basic` | Start | |
| `mini_app` | `sales_bot` (+ предложен `mini_app`) | Start | |
| `customers`, `ratings` | `customers` | Business | `ratings.low_rating_threshold`, `ask_reason_below` |
| `promo_codes` | `promo_codes` | Business | `min_percent` ≥ 1, `max_percent` ≤ 50 (CHK-06), `default_max_uses` |
| `bonuses` | `bonuses` | Business | `earn_percent` 0–20, `max_pay_percent` 0–50, `credit_on` = `delivered` (CHK-05) |
| `referral` | `marketing` (+ предложен `referral`) | Business | `bonus_friend`, `bonus_referrer`, `credit_on` |
| `broadcasts` | `broadcasts` | Business | `preview_before_send`, `requires_marketing_consent` (всегда `true`) |
| `reminders`, `abandoned_cart` | `marketing` | Business | `inactive_days`, `after_hours`, `window`… |
| `daily_report` | `analytics` | Business | `send_at`, `include` |
| `ai_assistant` | `ai_business` | Pro | `send_customer_names` (всегда `false`) |
| `ai_faq` | **новый** `ai_faq` | предложение: Pro или аддон Business | `knowledge[]`, `may_quote_prices` (по умолч. `false`), `handoff_to_owner` |
| `request_quote`, `wholesale` | **новый** `request_quote` | предложение: Business | см. 6.5; `wholesale.min_order_amount`, `min_qty_kg`, `requires_company_data` |
| `parcel_shipping` | **новый** `parcel_shipping` | предложение: Business | см. 7 |
| шаблон `preorder` | **новый** `preorder` | предложение: Start (вместо `cart`) | см. 6.3 |
| шаблон `termin` | **новый** `booking` | предложение: Start | см. 6.4 |
| онлайн-оплата | **новый** аддон `online_payment` (150 € в оферте) | аддон | `payment.methods[stripe_checkout]` |
| несколько языков | **новый** аддон `multi_language` (60 € в PRICES.md) | аддон | `locale.languages` > 1 |

Новые флаги — предложение к `plans.py`, в код пока не внесены. Аддоны требуют своей записи об оплате (как `Subscription`), иначе `PlanManager` их не откроет. Цены тарифов в конфиге не хранятся: источник правды — `plans.py` (расхождение 800/1 500 € против 1 490/2 490 € в OFFER_Business — аудит v5, C).

## 10. Шаблоны

| Шаблон | Обязательные разделы | Поток покупателя |
|---|---|---|
| `shop` | `catalog`, `fulfillment` | раздел → товар → кол-во → корзина → способ получения → слот → адрес/телефон → подтверждение → оплата |
| `preorder` | `catalog`, `preorder`, `fulfillment` | товар → вариант/опции → дата (с учётом lead time и ёмкости) → слот → подтверждение владельцем → предоплата |
| `termin` | `services`, `staff`, `schedule` | услуга → мастер (или «любой») → день → время → телефон → подтверждение → напоминания |
| `request_quote` | `request_form` | вопросы по шагам → заявка владельцу → ответ с ценой → «Принять» → заказ |

Модуль `ai_faq` подключается к любому шаблону: отвечает на свободный текст только по `knowledge[]` и данным конфига (часы, зоны, способы оплаты), без обещаний цен/скидок; при неуверенности — передача владельцу.

## 11. `compliance` и `security`

### 11.1 `compliance`

| Поле | Тип | Обяз. | По умолч. | Описание |
|---|---|---|---|---|
| `regime` | `EU_GDPR` \| `CH_revDSG` \| `UK_GDPR` \| `UA_PDP` \| `none` | да | по `locale.country` | Набор правил ядра. `none` в `prod` — ошибка для стран ЕС/ЕЭЗ/CH/UK. |
| `national_rules` | string[] | нет | по стране | Справочно: `DE_UWG_7` (реклама только с согласия), `DE_TDDDG`, `CH_UWG_3o`… |
| `controller` | `{name, email, address}` | да при `prod` | — | Ответственный за данные — в /privacy. |
| `privacy_policy_url`, `impressum_url` | url | да при `prod` для ЕС/CH | — | |
| `consent.order_processing.basis` | `contract` | нет | `contract` | Для заказа согласие не спрашивается (исполнение договора). |
| `consent.marketing.ask` | bool | да | `true` | Рассылки, напоминания, брошенная корзина — только с `marketing_consent = true` (CHK-10). |
| `consent.marketing.default` | bool | — | `false` | Всегда `false` (без «галочки по умолчанию»). |
| `consent.marketing.ask_at` | `start` \| `after_first_order` | нет | `after_first_order` | |
| `consent.marketing.text` | i18n | да | из пакета | Вопрос с кнопками «Да / Нет». Ответ пишется с датой (`consent_at`). |
| `consent.existing_customers_without_consent` | `no_marketing` \| `ask_once` | нет | `no_marketing` | Что делать с базой, собранной до введения согласия. |
| `commands.privacy` / `delete` / `unsubscribe` | string | нет | `/privacy`, `/delete`, `/stop` | Всегда включены, отключить нельзя. |
| `delete_policy.mode` | `anonymize` \| `hard_delete` | нет | `anonymize` | `/delete`: удаляются имя, телефон, адрес, chat_id, бонусы; в заказах остаются только поля `keep_for_accounting`. |
| `retention_days.carts` | int | нет | 30 | |
| `retention_days.customers_inactive` | int | нет | 730 | Нет заказов и сообщений N дней → анонимизация. |
| `retention_days.orders_personal_data` | int | нет | 730 | Потом имя/телефон/адрес в заказе обезличиваются. |
| `retention_days.orders_accounting` | int | нет | по стране | Бухгалтерские поля. DE — 8 лет для Buchungsbelege (с 2025), CH — 10 лет (OR 958f); уточняется налоговым консультантом клиента. |
| `retention_days.chat_messages` | int | нет | 0 | Тексты сообщений не храним. |
| `ai_processing.send_personal_data` | bool | — | `false` | В AI не уходят имена, телефоны, адреса, chat_id (аудит v5, A13). |
| `ai_processing.provider_region` | string | нет | — | |
| `status` | `implemented` \| `not_implemented` \| `required_before_launch` | нет | — | Для отчётов: что из обязательного ещё не сделано. |

Очистка по срокам — отдельный ежедневный сценарий `retention_cleanup` (ядро, для всех клиентов).

### 11.2 Права доступа

- Админ-команды — только `channels.owner.owner_user_ids`, **и** только из личного чата с ботом.
- Кнопки статусов заказа — только `owner_user_ids ∪ staff_user_ids` **и** только в `orders_chat_id` (CHK-09).
- Кнопки оценки — только покупатель этого заказа, один раз.

### 11.3 `security`

| Поле | Тип | По умолч. | Можно менять? |
|---|---|---|---|
| `webhook_secret_required` | bool | `true` | Нет в `prod`. |
| `sequential_processing` | bool | `true` | Нет: без него гонки в корзине (аудит v5, A11). |
| `admin_commands_owner_only` | bool | `true` | Нет. |
| `status_buttons_allowed_ids` | `owner_and_staff` \| `owner_only` | `owner_and_staff` | Да. |
| `status_buttons_chat_id` | string | `orders_chat_id` | Да. |
| `rating_buttons` | `order_customer_only` | — | Нет. |
| `outbound_chat_ids` | `known_customers_only` | — | Нет: бот пишет только тем, кто есть в базе клиентов или в заказе (аудит v5, A6, модуль 104). |
| `ignore_message_not_modified` | bool | `true` | Да. |

## 12. Стандартные проверки ядра

Проверки встроены в генератор для **всех** клиентов и шаблонов. Конфиг даёт им только параметры; выключить их нельзя. Каждая проверка — отдельная функция генератора с тестом (снимок blueprint + сценарий в тестовом боте).

### 12.1 Обязательные проверки

| ID | Проверка | Как работает | Аудит v5 | Параметры из конфига |
|---|---|---|---|---|
| CHK-01 | **Подлинность запроса** | Первый фильтр сценария: заголовок `X-Telegram-Bot-Api-Secret-Token` = секрет. Иначе — 200 без действий. | A1 | `channels.customer[].webhook.secret_token_ref` |
| CHK-01a | **Нет дублей заказа** | Заказ создаётся, только если корзина не пуста **и** её `cart_version` ещё не оформлена. Ключ идемпотентности `chat|cart_version`; повторный ответ с телефоном, двойное нажатие, повтор вебхука → «Заказ №… уже принят». Корзина очищается в том же шаге. Номер заказа уникален: счётчик в data store, а не `DDMM-HHmm`. | A3, A15 | — |
| CHK-02 | **Обработка ошибок отправки** | Каждый `sendMessage`/`editMessage*` с обработчиком `Ignore`/`Resume`; заблокировавший бота клиент не роняет сценарий; «message is not modified» игнорируется; на каждый callback — `answerCallbackQuery`. | A12, B | `security.ignore_message_not_modified` |
| CHK-03 | **Сумма из корзины** | Состав и сумма заказа, сообщение в канал и сумма Stripe берутся из **одного** снимка корзины в момент подтверждения; цена — из каталога, не из ввода и не из старого сообщения; `min_order` проверяется по этому снимку. Витрина присылает только коды и количества. | A4 | `fulfillment.min_order`, `catalog` |
| CHK-04 | **Единицы и лимиты** | Ввод «своего веса» разбирается с единицей (`700 г` в разделе «кг» → 0,7 кг; `1,5 кг` в разделе «г» → 1500 г); вне `[min_qty, max_qty]` или ≤ 0 → вежливый отказ с подсказкой. Лимиты на корзину: `max_items_in_cart`, `max_order_amount`. | A5 | `catalog.units.*`, `items[].min_qty/max_qty`, `limits` |
| CHK-05 | **Бонусы после доставки** | При заказе бонусы только резервируются (`pending`); зачисляются при статусе «доставлен»/«выполнен»; при отмене резерв снимается, списанные бонусы возвращаются. Реферальный бонус: пригласивший существует в базе, ≠ сам клиент, клиент новый (0 заказов), начисление — после **доставки** первого заказа друга; сообщения — только существующему клиенту. | A6 | `modules.bonuses.*`, `modules.referral.*` |
| CHK-06 | **Промокоды 1–50 %** | `/promo КОД N` принимает только целое `N` от `min_percent` (≥ 1) до `max_percent` (≤ 50), `0` — выключить. Промокод хранится в корзине отдельно и не стирается при добавлении товара; `uses` растёт при оформлении; учитываются `max_uses` и срок; итог после промокода и бонусов ≥ `payment.min_amount` и никогда не < 0. | A7 | `modules.promo_codes.*` |
| CHK-07 | **Актуальные цены и наличие** | Старые кнопки и «Повторить заказ» пересчитывают по текущему каталогу: товары без наличия отбрасываются с сообщением, цены — новые. Коды товаров не переиспользуются. | A10 | `catalog` |
| CHK-08 | **Оплата** | Онлайн-оплата в `test` видна только владельцу; подтверждение проверяет подпись Stripe, `metadata.order`, сумму и валюту против заказа; обрабатывает `checkout.session.completed` и `checkout.session.async_payment_succeeded`; пишет номер заказа, не chat_id. | A8 | `payment.methods[]` |
| CHK-09 | **Кто нажал кнопку** | Статусы заказа: `callback_query.from.id ∈ owner ∪ staff` **и** `message.chat.id = orders_chat_id`. Оценка: `from.id` = покупатель заказа, один раз. Админ-команды: `from.id ∈ owner_user_ids`, личный чат. Чужое нажатие → «Нет доступа», без изменений. | A9, A1 | `channels.owner.*`, `security.*` |
| CHK-10 | **Согласие и данные** | Рассылки/напоминания/брошенная корзина — только при `marketing_consent = true` и не `blocked`; `/privacy`, `/delete`, `/stop` всегда работают; сроки хранения соблюдает `retention_cleanup`; в AI не уходят персональные данные. | A13 | `compliance.*` |
| CHK-11 | **Последовательная обработка** | Сценарий Make с `sequential: true` (одно обновление за раз) — без гонок в корзине. | A11 | — |
| CHK-12 | **Слоты в будущем** | Слот/день не предлагается, если он уже прошёл или кончается раньше чем через `hide_if_ends_within_min`; для preorder/termin — с учётом lead time, ёмкости и уже занятых слотов. Подтверждение показывает выбранный слот, а не общий текст. | B | `fulfillment.*.slots`, `preorder`, `booking` |
| CHK-13 | **Проверка контактов** | Телефон: `+` и 7–15 цифр после очистки; адрес: ≥ 5 знаков, не команда; для посылки — все поля `requires_address_fields`. Текст без «Ответить» распознаётся по состоянию диалога, а не по `reply_to_message`. | B | `fulfillment.parcel.requires_address_fields` |
| CHK-14 | **Предпросмотр рассылки** | `/send` сначала показывает текст и число получателей (с согласием), отправка — после «✅ Отправить». Не чаще `limits.max_broadcast_per_day`. | B | `limits.max_broadcast_per_day` |
| CHK-15 | **Нет секретов в репозитории** | Загрузчик ищет токены/ключи/URL хуков в конфиге и в собранном blueprint перед записью в git. | A1, A2 | — |

### 12.2 `limits` — значения по умолчанию

| Поле | По умолч. |
|---|---|
| `max_items_in_cart` | 30 |
| `max_order_amount` | 1 000 (в валюте) |
| `max_broadcast_per_day` | 1 |
| `max_text_length` | 4 000 |

## 13. `infra`

| Поле | Тип | Обяз. | Описание |
|---|---|---|---|
| `runtime` | `make` \| `python` | да | Сейчас `make`. |
| `make.zone`, `make.team_id` | string / int | да для `make` | |
| `make.scenarios.<role>` | int | нет | ID существующих сценариев (`main`, `daily_report`, `ai_assistant`, `reminders`, `stripe_confirm`, `abandoned_cart`, `retention_cleanup`). Пусто — сценарий создаётся при первом развёртывании. |
| `make.datastores.<role>` | int | нет | `carts`, `customers`, `orders`, `promo_codes`, `stats`, `catalog`, `bookings`, `counters`. |
| `make.tools.<role>` | int | нет | Служебные инструменты. |

Тестовый бот — отдельный файл `clients/<id>.test.json` с `env: "test"` и своими `infra`/`channels` (наложение поверх основного: `"extends": "raiv_fish.json"`).

## 14. Проверки загрузчика (fail fast)

Загрузчик (`raiv_platform/config.py`, ещё не написан) отклоняет конфиг, если:

1. нет обязательного поля для выбранного `template` или `env: prod` содержит `TODO`;
2. `default_language ∉ languages`, или у i18n-строки нет перевода на `default_language`;
3. коды товаров/разделов не уникальны, `unit` не описан в `units`, `qty_presets` вне `[min_qty, max_qty]`;
4. `price` < 0, или `null` без `price_mode: "quote"`;
5. `parcel.enabled` и есть тир с `price: null` или товар `pcs` без `weight_g`;
6. `stripe_checkout.mode = test` и `visible_to = all`;
7. `promo_codes.max_percent > 50`, `bonuses.max_pay_percent > 50`, `bonuses.credit_on ≠ delivered`;
8. включены `broadcasts`/`reminders`/`abandoned_cart`, а `compliance.consent.marketing.ask = false`;
9. `owner_user_ids` пуст, `orders_chat_id` не задан;
10. найден секрет (принцип 2);
11. модуль включён, но не входит в тариф — **предупреждение** (модуль будет пропущен), не ошибка.
