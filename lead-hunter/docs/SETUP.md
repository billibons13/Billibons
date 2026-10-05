# Lead Hunter — запуск этапа 2

## 1. Бот-пульт через @BotFather (делает владелец)
1. Telegram → @BotFather → `/newbot`.
2. Имя: `Lead Hunter Panel`; username, например `RaivLeadHunter_bot` (должен оканчиваться на `bot`).
3. BotFather пришлёт токен. **Не вставляйте его в чат с Claude.**
4. `/setprivacy` → выбрать бота → `Enable` (бот читает только то, что ему пишут лично).
5. `/setjoingroups` → `Disable` (бота нельзя добавить в группы).
6. `/setcommands` → вставить:
```
start - статус системы
new - новые HOT/WARM без решения
today - итоги дня
stats - 7 и 30 дней
pause - пауза AI-обработки
resume - продолжить обработку
settings - текущие настройки
help - как пользоваться
```

## 2. Подключения в Make (делает владелец, секреты остаются в Make)
Ссылка-запрос (уже создана): https://eu1.make.com/2241615/credentials-requests/inbox?requestId=cf919fc9-24f8-4705-8ef6-5de03c9f163b
- **Telegram** — вставить токен нового бота.
- **Anthropic Claude** — можно пропустить: для MVP Analyst работает через модуль Make «Simple Text Prompt»
  (Claude Haiku 4.5, без ключа, оплата кредитами Make: ~904 входных / ~181 выходных токенов за кредит).
  Свой ключ понадобится, когда объём вырастет.

## 3. Место под Data Stores (решение владельца)
Тариф Core: 10 МБ на все хранилища, сейчас занято 10 × 1 МБ. Make ответил «Not enough space in storage».
Нужно освободить место (удалить неиспользуемые хранилища старых проектов) или расширить тариф.
Минимум для этапа 2 — 6 МБ (по 1 МБ на lh_leads, lh_runs, lh_decisions, lh_events, lh_sources, lh_settings).
Компромисс — 3 МБ: lh_leads, lh_log (runs + decisions + events), lh_settings (+ sources).

## 4. Настройки по умолчанию (lh_settings, запись `main`)
owner_chat_id 6883357001 · paused false · daily_budget_usd 1 · architect_threshold 60 · hot 80 · warm 60 · cold 40 ·
minimum_order_eur 500 · timezone Europe/Berlin · analyst_model claude-haiku-4-5 · analyst_max_tokens 1500 ·
max_retry_attempts 3 · retry_delays "1,5,30" · analyst price in/out 1 / 5 USD за 1M токенов ·
веса 0.15/0.15/0.12/0.12/0.12/0.10/0.08/0.06/0.05/0.05 · курсы fx_* — заполняет владелец с датой.
webhook_secret и internal_token генерируются при установке и хранятся только в lh_settings.

## 5. После подключения (делает Claude)
Создать data stores → записать settings → собрать LH-20, LH-03, LH-10 генератором → setWebhook с secret_token →
прогнать тесты из TESTING.md → отчёт.
