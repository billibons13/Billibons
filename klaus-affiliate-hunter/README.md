# Claus Affiliate Hunter — Германия

Автономный агент, который ищет товары для роликов **Meister Klaus**, проверяет партнёрские программы,
считает экономику и передаёт готовые предложения в **Make.com**.

- **Claude** — интеллект: поиск, проверка, оценка, подбор под сценарии (Routine по расписанию, регламент — `AGENT.md`).
- **Make.com** — автоматизация: приём, проверка, дедупликация, база, очередь контента, уведомления, обратная связь.
- **Klaus** — видео. **Владелец** — контроль и стратегические решения.

## Архитектура

```
 Routine «Claus Affiliate Hunter» (Claude, ежедневно 06:52 Berlin, свежая сессия с этим репозиторием)
   │ 1 читает базу и недельные скрипты Klaus ─────────────► Make data store 203568
   │ 2 python3 -m hunter match  (проблема → типы товаров)
   │ 3 WebSearch/WebFetch: amazon.de, магазины программ Awin (только официальные страницы)
   │ 4 python3 -m hunter link / prepare  (ссылка только по вашим аккаунтам, скоринг A/B/C/HOLD)
   │ 5 Make-инструмент 7712897 «an Make senden» ─► Webhook Intake ─► Сценарий 7712881
   │                                                   ├ Set variables: valid / verified / queue
   │                                                   ├ GetRecord (дедупликация по product_id)
   │                                                   ├ AddRecord (сохранение; непроверенная ссылка не сохраняется)
   │                                                   ├ ответ JSON (created/updated, priority, queue)
   │                                                   └ Telegram владельцу: новый товар в очереди Klaus (только A/B)
   │ 6 проверка ссылок/цен ───────────────────────► Webhook Status ─► Сценарий 7712888
   │                                                   ├ обновление статуса видео, кликов, продаж, комиссий
   │                                                   ├ битая ссылка / нет в наличии → снять с очереди, HOLD
   │                                                   └ Telegram: публикация, продажи, проблемы
   └ 7 отчёты (дневной при событиях, недельный, месячный) ► Make-инструмент 7713110 → Telegram

 Сценарий 7712068 «Meister Klaus — Wochenskripte» (сб 10:00): Gemini → Telegram → + сохранение скриптов
 в базу как запись klaus-scripts-ГГГГ-WНН — отсюда агент берёт сценарии для подбора товаров.
```

### Почему так
- В Make нет подключения Anthropic API, а Claude Routine уже имеет доступ к Make и веб-поиску — ключ не нужен.
- Make — вторая линия защиты: даже ошибочный payload не сохранит непроверенную ссылку и не попадёт в очередь
  (проверено тестом «spoof»).
- База — Make data store (1 МБ ≈ 600 товаров), видна в Make и читается агентом. При росте — перенос в
  Google Sheets/Airtable без изменения формата JSON.

## Объекты в Make (eu1, team 2241615)
| Объект | ID |
|---|---|
| Data store «Klaus Affiliate — Produkte» | 203568 (структура 610447) |
| Сценарий «1. Intake (Prüfung, Dedup, Speichern, Queue)» | 7712881, webhook 3820339 `https://hook.eu1.make.com/lrdmvdkf8m3svedd58zei2kn62ptgbam` |
| Сценарий «2. Status & Statistik (Feedback)» | 7712888, webhook 3820340 `https://hook.eu1.make.com/arkbrhuvdrp6fxrzp4vx581lnyayxv81` |
| Инструмент «an Make senden» (target intake/status) | 7712897 |
| Инструмент «Bericht an Telegram» | 7713110 |
| «Meister Klaus — 1. Wochenskripte» (дополнен сохранением скриптов) | 7712068 (резервная копия до изменения: `make/backup_meister_klaus_7712068_before.json`) |

Blueprints генерируются `python3 make/generate_blueprints.py` → `make/*_blueprint.json`.

## Данные
- Схемы: `schema/product.schema.json` (intake), `schema/status.schema.json` (обратная связь).
- Отсутствующие значения — `null`, не выдумываются. Цена/комиссия парсятся из «49,99 €», «8,5 %».
- `product_id`: `amzn-de-<ASIN>` или `de-<sha1 канонического URL>` — один товар = одна запись.
- Приоритет: **A** (score ≥ 0,70, verified, в наличии), **B** (≥ 0,55, verified), **C** (эксперимент),
  **HOLD** (нет подтверждённой ссылки / нет в наличии / исключённая категория). В очередь Klaus — только A/B.
- Ожидаемое вознаграждение = цена × комиссия. EPM — три сценария на допущениях (`assumption: true`),
  заменяются фактом по категории, когда набирается ≥ 3000 просмотров и ≥ 30 кликов (`hunter/learning.py`).

## Обратная связь (как сообщать результаты)
POST JSON на webhook Status (или инструмент 7712897 с `target: "status"`):
`{"product_id": "...", "video_status": "published", "video_url": "...", "views": 1200, "clicks": 9, "sales": 1, "confirmed_commission_eur": 2.62}`.
Пустые поля не затирают сохранённые.

## Тесты
`python3 -m unittest discover -s tests` — 26 тестов ядра (ссылки, парсинг, скоринг, подбор, обучение).
Сквозной тест Make (01.10.2026): невалидный товар → 400; подделка «verified» с не-https ссылкой →
сохранён как unverified/HOLD без ссылки; A-товар → created + queued + Telegram; повтор → updated без
второго уведомления; публикация/продажи → обновлено; битая ссылка → rejected/HOLD, снят с очереди;
неизвестный ID → 404. Тестовые записи удалены.

## Что нужно от владельца
См. раздел «Статус» в ответе агента и `config.json`: Amazon tag, Awin Publisher ID + список одобренных
программ, API-ключи (только через Make), решение о запуске ежедневного расписания.
