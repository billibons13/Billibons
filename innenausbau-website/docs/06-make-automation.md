# 06 · Make.com — Automation Hub, Webhook, CRM, Telegram

## Общая схема

```
Website-Formular (LeadForm, 2 Schritte, Fotos komprimiert)
        │  multipart/form-data
        ▼
Next.js  POST /api/lead     ── Validierung (zod), Spam-Schutz, Rate-Limit, lead_id
        │  LeadSink (LEAD_SINK=make)
        ▼
Make  ① Custom Webhook  ──► ② Secret-Filter ──► ③ Parse JSON
        │
        ├─► ④ Variablen (Ordnername, Priorität A/B/C)
        ├─► ⑤ Google Drive: Ordner anlegen ─► ⑥ Iterator Fotos ─► Upload ─► Aggregator (Links)
        ├─► ⑦ Data Store "leads" (Quelle der Wahrheit für Follow-up)
        ├─► ⑧ CRM-Adapter (Sub-Szenario)  ─► Sheets | Airtable | HubSpot | Pipedrive  → crm_url
        ├─► ⑨ Telegram: "🔔 Neue Anfrage" + Button "Lead öffnen"
        ├─► ⑩ E-Mail an Kunden (Bestätigung)        [nur wenn email ≠ ""]
        └─► ⑪ E-Mail intern (vollständige Anfrage)
                                    ⋮
Szenario B (täglich 07:45)  Follow-up: Erinnerungen, Aufgaben, Bewertungsanfrage
Szenario C (optional)       Telegram-Buttons → Status im Data Store/CRM ändern
```

## Почему именно так

- **Сайт не знает о CRM.** Он отправляет один стабильный контракт (`LeadPayload v1.0`) в один webhook. Смена CRM = изменение в Make, без деплоя сайта.
- **Двухуровневая абстракция:**
  1. На сайте — интерфейс `LeadSink` (`src/lib/leads/types.ts`): `make` / `webhook` (n8n, Zapier, свой backend) / `log`. Выбирается env-переменной `LEAD_SINK`.
  2. В Make — отдельный под-сценарий **«CRM-Adapter»**, который принимает нормализованный лид и пишет его в выбранную CRM. Основной сценарий не меняется.
- **Data Store** хранит минимальный статус лида независимо от CRM → follow-up работает даже с Google Sheets.

## Webhook-контракт

`POST <MAKE_WEBHOOK_URL>` · `Content-Type: multipart/form-data` · Header `X-Lead-Secret: <MAKE_WEBHOOK_SECRET>`

| Поле | Тип | Содержимое |
|---|---|---|
| `payload` | text (JSON) | `LeadPayload` — схема `make/lead-payload.schema.json`, пример `make/sample-payload.json` |
| `file_0` … `file_5` | binary | Фото (JPEG после сжатия в браузере, ≤ 2.5 MB каждое, ≤ 8 MB всего) |

```jsonc
{
  "schema_version": "1.0",
  "lead_id": "L-20261002-2e467793",      // генерируется сервером, сквозной ID везде
  "timestamp": "2026-10-02T22:58:41.825Z",
  "name": "…", "phone": "…", "email": "…", "location": "…",
  "project_type": "Wohnung|Haus|Büro|Gewerbe",
  "services": ["Badsanierung", "Fliesenarbeiten"],
  "area": "8", "budget": "10.000–25.000 €", "preferred_date": "In 1–3 Monaten",
  "message": "…",
  "uploaded_files": [{ "field": "file_0", "name": "bad.jpg", "type": "image/jpeg", "size": 284113 }],
  "consent": { "given": true, "text_version": "2026-10-v1", "timestamp": "…" },
  "meta": { "source": "website", "source_page": "/leistungen/badsanierung", "utm": {…}, "user_agent": "…", "locale": "de" }
}
```

Ответ: сайт считает успехом любой HTTP 2xx. Make по умолчанию сразу отвечает `200 Accepted` (если в сценарии нет модуля *Webhook response*) — пользователь не ждёт выполнения всех модулей.

## Сценарий A «Lead-Intake» — модули

| # | Модуль Make | Настройка |
|---|---|---|
| ① | **Webhooks › Custom webhook** | Новый hook «website-lead». В *Advanced*: ✅ *Get request headers*. Определить структуру: отправить тестовую заявку (LEAD_SINK=make) при *Redetermine data structure* |
| ② | **Filter** (между ① и ③) | `headers[]` → значение `x-lead-secret` = секрет из env. Иначе — стоп |
| ③ | **JSON › Parse JSON** | JSON string = `{{1.payload}}`; Data structure «Lead v1» (сгенерировать из `make/sample-payload.json`) |
| ④ | **Tools › Set multiple variables** | `folder_name = {{3.lead_id}} – {{3.name}} – {{3.location}}`; `priority = if(contains(3.services; "Komplettrenovierung") or parseNumber(3.area) >= 60; "A"; if(length(3.services) >= 2; "B"; "C"))`; `services_text = join(3.services; ", ")` |
| ⑤ | **Google Drive › Create a folder** | Родитель: `Leads/{{formatDate(now; "YYYY")}}`, имя = `folder_name`. Доступ — только аккаунт фирмы (не «anyone with link» — DSGVO) |
| ⑥ | **Flow Control › Iterator** | Array = `{{3.uploaded_files}}` |
| ⑥a | **Google Drive › Upload a file** | File name = `{{6.name}}`; Data = `{{switch(6.field; "file_0"; 1.file_0.data; "file_1"; 1.file_1.data; "file_2"; 1.file_2.data; "file_3"; 1.file_3.data; "file_4"; 1.file_4.data; "file_5"; 1.file_5.data)}}`; папка из ⑤ |
| ⑥b | **Flow Control › Array aggregator** | Source = ⑥, собрать `webViewLink` → `photo_links` |
| ⑦ | **Data store › Add/replace a record** | Store «leads», key = `lead_id`; поля: `status=neu`, `created`, `name`, `phone`, `priority`, `folder_url`, `crm_url` (заполняется после ⑧), `next_followup = addDays(now; 1)` |
| ⑧ | **Scenarios › Run a scenario** (или *HTTP › Make a request* на webhook под-сценария) | Под-сценарий «CRM-Adapter» c входами: весь лид + `folder_url` + `priority`. Возвращает `crm_url` |
| ⑨ | **Telegram Bot › Send a text message or a reply** | Chat ID группы «Anfragen»; Parse mode HTML; Reply markup — см. ниже |
| ⑩ | **Gmail › Send an email** (или *Email › Send* через SMTP фирмы) | Filter: `email` не пустой. Текст подтверждения ниже |
| ⑪ | **Gmail › Send an email** | Внутреннее письмо всем ответственным, ссылки на папку и CRM |

**Обработка ошибок:** на ⑤/⑥a/⑧ — обработчик *Resume* (лид всё равно уходит в Telegram и почту), на ⑨/⑩ — *Break* (автоповтор 3×). Включить *Settings › Allow storing of incomplete executions*. Отдельный сценарий-«сторож»: ошибки → Telegram-чат админа.

### Под-сценарий «CRM-Adapter» (абстракция CRM)

Вход: `lead` (структура Lead v1) + `priority`, `folder_url`. Выбор цели — **Team variable** `CRM_TARGET` (`sheets` | `airtable` | `hubspot` | `pipedrive`). Router с фильтром по `CRM_TARGET`:

| Цель | Модули | Маппинг |
|---|---|---|
| **Google Sheets** (старт) | *Google Sheets › Add a row* | Лист «Leads»: lead_id, Datum, Name, Telefon, E-Mail, Ort, Objekt, Leistungen, Fläche, Budget, Zeitraum, Nachricht, Fotos (folder_url), Priorität, Status, Quelle/UTM. `crm_url` = ссылка на лист `#gid=…&range=A{{rowNumber}}` |
| **Airtable** | *Airtable › Create a record* | Таблица Leads с теми же полями; Single select для Status/Priority. `crm_url` = `https://airtable.com/{base}/{table}/{{id}}` |
| **HubSpot** | *HubSpot CRM › Search contacts* (по email/phone) → *Create/Update a contact* → *Create a deal* (pipeline «Renovierung», stage «Neue Anfrage») → *Create an association* | Deal name = `{{services_text}} – {{location}}`; свойства-кастомы `lead_id`, `project_type`, `area`, `budget_range`. `crm_url` = `https://app.hubspot.com/contacts/{portal}/record/0-3/{{deal.id}}` |
| **Pipedrive** | *Pipedrive › Search persons* → *Create a person* → *Create a lead* (label = priority) → *Add a note* (вся заявка + folder_url) | `crm_url` = `https://{company}.pipedrive.com/leads/inbox/{{lead.id}}` |

Выход: *Scenarios › Return output* `{ crm_url }`. Новая CRM = новая ветка Router, основной сценарий и сайт не трогаются. Можно включить две ветки одновременно (например, Sheets как бэкап + HubSpot).

## Telegram

**Настройка:** @BotFather → бот «Firmenname Anfragen» → токен в Make-Connection «Telegram Bot». Создать закрытую группу «Anfragen», добавить бота, получить chat_id (модуль *Telegram › Watch updates* один раз).

**Сообщение (Parse mode: HTML):**
```
🔔 <b>Neue Anfrage</b>  · Priorität {{4.priority}}

<b>Name:</b> {{3.name}}
<b>Telefon:</b> {{3.phone}}
<b>Ort:</b> {{3.location}}
<b>Projekt:</b> {{3.project_type}}
<b>Leistung:</b> {{4.services_text}}
<b>Fläche:</b> {{ifempty(3.area; "–")}} m²
<b>Budget:</b> {{ifempty(3.budget; "–")}}
<b>Zeitraum:</b> {{ifempty(3.preferred_date; "–")}}
<b>Fotos:</b> {{length(3.uploaded_files)}} · <a href="{{5.webViewLink}}">Ordner öffnen</a>

{{substring(3.message; 0; 500)}}

<code>{{3.lead_id}}</code>
```

**Reply markup (Inline keyboard):**
```json
{
  "inline_keyboard": [
    [ { "text": "Lead öffnen", "url": "{{8.crm_url}}" } ],
    [ { "text": "📁 Fotos", "url": "{{5.webViewLink}}" },
      { "text": "✅ Kontaktiert", "callback_data": "contacted:{{3.lead_id}}" } ]
  ]
}
```
(Telegram не поддерживает `tel:`-ссылки в кнопках — номер в тексте кликабелен в приложении.)

**Сценарий C (опционально):** *Telegram Bot › Watch updates* → Router по `callback_query.data` → `contacted:<id>` → *Data store › Update record* (`status=kontaktiert`) + обновить CRM + *Answer callback query* «Status gespeichert» + *Edit message* (добавить «✅ kontaktiert von {{first_name}}»).

## Письмо клиенту (DE)

**Betreff:** Ihre Anfrage bei {{Firmenname}} – {{3.lead_id}}

```
Guten Tag {{3.name}},

vielen Dank für Ihre Anfrage zu {{4.services_text}} in {{3.location}}.
Wir haben Ihre Angaben{{if(length(3.uploaded_files) > 0; " und Fotos"; "")}} erhalten und melden uns zeitnah telefonisch
unter {{3.phone}} oder per E-Mail, um die nächsten Schritte und ggf. einen Besichtigungstermin abzustimmen.

Ihre Anfragenummer: {{3.lead_id}}

Mit freundlichen Grüßen
{{Firmenname}}
Telefon · WhatsApp · Website
```
(Без обещаний конкретных сроков, пока компания их не утвердила.)

## Сценарий B «Follow-up» (Schedule: ежедневно 07:45)

1. **Data store › Search records**: `status = neu` и `created < addHours(now; -24)` → Telegram-напоминание «⏰ Noch nicht kontaktiert: …» (+ кнопка «Lead öffnen»).
2. `status = angebot_gesendet` и `next_followup <= now` → *Google Calendar › Create an event* / *Todoist/Asana/ClickUp › Create a task* «Nachfassen: {{name}}» для ответственного + сдвинуть `next_followup = addDays(now; 5)`.
3. `status = abgeschlossen` и `review_requested = false` → письмо с просьбой об отзыве (ссылка на Google-профиль) → `review_requested = true`. *Это основа для реальных отзывов на сайте и Local SEO.*
4. Лиды старше 12 месяцев без договора → удалить персональные данные (DSGVO, срок хранения согласовать).

Статусы: `neu → kontaktiert → besichtigung → angebot_gesendet → beauftragt | verloren → abgeschlossen`.

## Безопасность и DSGVO

- Секрет webhook только на сервере (`MAKE_WEBHOOK_SECRET`, не `NEXT_PUBLIC_`), проверка фильтром ②.
- В Make выбрать EU-регион (eu1/eu2) организации; заключить AVV/DPA с Make, Google, CRM.
- Папки Drive не публикуются по ссылке; Telegram-группа закрытая.
- В payload есть `consent.text_version` — доказуемость согласия.
- Автоудаление старых лидов (сценарий B, шаг 4).

## Подключение (чек-лист)

1. Make → *Create scenario* «Lead-Intake» → ① Custom webhook → скопировать URL.
2. В хостинге: `LEAD_SINK=make`, `MAKE_WEBHOOK_URL=…`, `MAKE_WEBHOOK_SECRET=<openssl rand -hex 32>`.
3. Отправить тестовую заявку с сайта → *Redetermine data structure* в ①.
4. Собрать ②–⑪, под-сценарий CRM-Adapter, Team variable `CRM_TARGET=sheets`.
5. Включить сценарий (*Immediately as data arrives*). Проверить: Telegram, письма, Drive, строка в таблице.
6. Сценарий B по расписанию.
