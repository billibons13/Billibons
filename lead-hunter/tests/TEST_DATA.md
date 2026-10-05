# ⚠️ TEST DATA — вымышленные заявки, НЕ реальные заказы

Используются только для проверки конвейера. Перед пересылкой боту начинайте текст с `[TEST]`,
чтобы такие лиды отличались в базе. URL ведут на example.com и не существуют.

| # | Страна | Тест | Текст для пересылки |
|---|---|---|---|
| T1 | Германия | valid lead | [TEST] Wir suchen einen Entwickler für einen Telegram-Bot für unseren Onlineshop (Katalog, Warenkorb, Bezahlung mit Stripe). Budget 1.200 EUR, Start nächste Woche. https://example.com/jobs/t1?utm_source=tg |
| T2 | США | no budget | [TEST] Need a Telegram bot for booking appointments in my barbershop in Austin, TX. Google Calendar sync, reminders. https://example.com/jobs/t2 |
| T3 | Великобритания | no URL | [TEST] Looking for someone to build a Telegram support bot for a London cafe chain, FAQ + handover to staff. Budget £800. |
| T4 | Испания | budget < 500 € | [TEST] Busco desarrollador para un bot de Telegram que envíe notificaciones de pedidos. Presupuesto 150 EUR. https://example.com/jobs/t4 |
| T5 | Польша | suspicious | [TEST] Telegram bot for crypto signals and betting, payment only after unpaid test task, contact me on WhatsApp off-platform. Budget $5000. https://example.com/jobs/t5 |
| T6 | Германия | duplicate | повторно перешлите T1, но с `?utm_campaign=x` в ссылке — должен сработать DUPLICATE_DETECTED |
| T7 | — | malformed Claude JSON | проверяется без Claude: `python3 scripts/scoring.py` (validate) + в Make через тестовый вызов LH-10 с подменой ответа (см. TESTING.md) |
