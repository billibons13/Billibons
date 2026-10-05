# Delivery Manager — AI Operations Manager

Этап 2: это логика Make, а не вызов Claude (токены не тратятся). Отвечает за: очередь и статусы
(NEW → ANALYZED → SENT_TO_TELEGRAM, плюс ARCHIVED / REJECTED / APPROVED / ERROR), проверку JSON Analyst,
расчёт score, hard caps и grade, повторы (до `max_retry_attempts`), учёт расходов (`daily_budget_usd`, 80 % —
предупреждение, 100 % — paused), Telegram-карточки и кнопки, события в lh_events.
Все пороги и веса берутся из lh_settings (запись `main`), в логике не захардкожены.
