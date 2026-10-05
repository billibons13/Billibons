# Реестр задач директора

Формат и правила — `DIRECTOR.md`, раздел «Поручения владельца — только через директора».
Новые задачи — сверху.

## T-20261005-0003 · chat_id владельца в репозитории
- AGENT: 🛡 Инженер надёжности (`team/RELIABILITY.md`)
- PRIORITY: P3
- OBJECTIVE: OWNER_CHAT_ID не должен лежать в файлах репозитория без необходимости (правило владельца этапа 2).
- INPUT: grep по репозиторию (klaus-affiliate-hunter/make/*, raiv-fish-bot/agents/{DIRECTOR,team/READINESS,team/QA,daily/IDEAS}.md, история git с 844154b).
- ACTION: составить перечень мест, отделить рабочие (карточки агентов, по которым шлются сообщения) от копий/бэкапов; предложить 2–3 варианта.
- EXPECTED_OUTPUT: перечень + варианты + рекомендация директору. Ничего не удалять и историю не переписывать.
- DEADLINE: 06.10.2026
- STATUS: WAITING — решение владельца (переписывание истории git и правка бэкапов = удаление данных, только с «да»).

## T-20261005-0002 · Приёмка этапа 2 Lead Hunter
- AGENT: 🧪 Тестировщик релизов (`team/QA.md`)
- PRIORITY: P1
- OBJECTIVE: доказать фактами, что конвейер «заявка → LH-03 → LH-10 → карточка» работает и безопасен.
- INPUT: `lead-hunter/docs/TESTING.md`, `lead-hunter/tests/TEST_DATA.md` (T1–T7, метка [TEST]).
- ACTION: прогон после T-0001; проверка записей lh_leads/lh_log, дубликатов, caps, чужого chat_id.
- EXPECTED_OUTPUT: таблица тестов ✅/❌ с ID исполнений Make; тестовые записи помечены TEST.
- DEADLINE: после T-0001
- STATUS: NEW (ждёт T-0001)

## T-20261005-0001 · Доделать этап 2 Lead Hunter (уже утверждён владельцем)
- AGENT: 🛠 Make-инженер Lead Hunter (`team/LH_ENGINEER.md`)
- PRIORITY: P1
- OBJECTIVE: рабочий пульт в Zulius: LH-20 + LH-03 + LH-10 активны, LH-99 выполнен один раз.
- INPUT: `lead-hunter/blueprints/LH-20.json`, LH-03 = 7789167 (обновлён), LH-10 = 7789247 (создан), генератор.
- ACTION: создать LH-20 и LH-99 в папке 400613; активировать LH-03/10/20; запустить LH-99; проверить вебхук Zulius.
- EXPECTED_OUTPUT: ID сценариев, статусы активации, результат LH-99, getWebhookInfo (url = хук LH-20, без секретов).
- DEADLINE: 05–06.10.2026
- STATUS: ASSIGNED
