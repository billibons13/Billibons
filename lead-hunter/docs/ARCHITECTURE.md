# Lead Hunter — архитектура (кратко)

Полная версия этапа 1: `../Lead_Hunter_Architecture.pdf` и документ https://claude.ai/artifact/6YnqAroTHE5U5LpUsnirsK

## Этап 2 — один цикл
Telegram (владелец пересылает заявку) → **LH-20 Owner Panel** (единственный webhook бота: проверка secret_token
и OWNER_CHAT_ID, команды, кнопки) → **LH-03 Manual Intake** (URL, нормализация, хеши, дубли, лид NEW) →
**LH-10 Lead Pipeline** (бюджет дня, Analyst, проверка JSON, score, caps, grade, карточка) → Telegram.

Почему LH-20 — вход для всего: у Telegram-бота может быть только один webhook, поэтому и команды, и пересланные
заявки приходят в один сценарий; он сразу отсекает чужих и передаёт заявку в LH-03 внутренним webhook
с токеном `internal_token` (из lh_settings).

## Хранилище (Make Data Stores)
lh_leads, lh_runs, lh_decisions, lh_events, lh_sources, lh_settings (запись `main` + записи `day_YYYY-MM-DD`
со счётчиком расходов). Поля совпадают с будущими колонками PostgreSQL; JSON-поля (scores, reasons, risk_flags,
duplicates, brief, offer) хранятся строкой JSON → jsonb.

## Scoring
score = round(10 × Σ wᵢ·sᵢ), веса из lh_settings (сумма = 1). Caps: нет source_url → ≤ 59; risk_flags → ≤ 39;
опубликованный бюджет < minimum_order_eur → ≤ 59; kind = prospect → ≤ 59. Причина — в `score_cap_reason`.
Grade: HOT ≥ hot_threshold (80), WARM ≥ warm_threshold (60), COLD ≥ cold_threshold (40), иначе REJECT.
Эталон с тестами: `scripts/scoring.py`.

## Пауза
/pause: ручной ввод не блокируется — заявка сохраняется (NEW, в очереди), AI не вызывается.
/resume: все лиды NEW отправляются в LH-10. Так владелец ничего не теряет и не тратит деньги во время паузы.

## Этап 2.5 — LH DIRECTOR (архитектура на согласовании)

Документ: https://claude.ai/code/artifact/b1005ba2-b738-4a0b-9120-4fdbf72d0ef8
Статус: ждёт утверждения владельца. Реализация не начата.
Кратко: LH-30 DIRECTOR Gate (детерминированные проверки в Make), LH-31 Feedback,
LH-40 Daily Review (Claude по агрегатам + валидатор evidence), LH-41 Improvement Apply
(только по кнопке владельца, белый список ключей, откат), LH-42 Weekly Review.
