"""Генератор Make-сценариев Lead Hunter, этап 2: LH-99 (установка), LH-20 (пульт), LH-03 (приём), LH-10 (конвейер).
Запуск: python3 scripts/generate_lh.py  → blueprints/*.json
Секретов в файле нет: токен бота живёт в подключении Make, webhook_secret и internal_token
генерирует LH-99 внутри Make и хранит только в lh_settings.
"""
import json, os, re

TEAM = 2241615
CONN_TG = 9480305            # Zulius Passport Queue Bot (Telegram-подключение в Make)
S_LEADS, S_SET, S_LOG = 207950, 207951, 207952
DS_ANALYSIS = 618689         # data structure ответа Analyst для Parse JSON
HOOK20, HOOK03, HOOK10 = 3846694, 3846695, 3846697
HOOK11 = 3853986             # LH-11 Architect+Sales (внутренний, только с internal_token)
URL11 = "https://hook.eu1.make.com/x6cnrfo2bt495fg5od84c49lui47todk"
DS_ARCH, DS_SALES = 620802, 620803   # data structures ответов Architect / Sales для Parse JSON
URL20 = "https://hook.eu1.make.com/69syfagsko64kd9oelsekoz11e3k341q"
URL03 = "https://hook.eu1.make.com/i7nnyj1mxyeez4mgznqk6x58oqhinbdr"
URL10 = "https://hook.eu1.make.com/2g6fjqg256vhydy4s3swxukppc486udl"
URL_AI01 = "https://hook.eu1.make.com/k4psdiuhxt026uqf739x27xh5nyq4j0o"  # AI-01 7852575 (хук 3868349); приоритет — lh_settings.main.ai01_url
OWNER_CHAT_ID = os.environ.get("LH_OWNER_CHAT_ID", "")  # только из окружения; в репозиторий не попадает, пишется в lh_settings через LH-99
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

PROMPT = open(os.path.join(ROOT, "agents", "analyst.md"), encoding="utf-8").read()
PROMPT_VERSION = re.search(r"Версия промта: \*\*(ANALYST_v\d+)\*\*", PROMPT).group(1)  # пишется в run-запись
PROMPT = PROMPT.split("## SYSTEM PROMPT", 1)[1].split("## END SYSTEM PROMPT", 1)[0].strip()

def load_prompt(fname, tag):
    txt = open(os.path.join(ROOT, "agents", fname), encoding="utf-8").read()
    ver = re.search(r"Версия промта: \*\*(" + tag + r"_v\d+)\*\*", txt).group(1)
    return txt.split("## SYSTEM PROMPT", 1)[1].split("## END SYSTEM PROMPT", 1)[0].strip(), ver

ARCH_PROMPT, ARCH_VERSION = load_prompt("architect.md", "ARCHITECT")
SALES_PROMPT, SALES_VERSION = load_prompt("sales.md", "SALES")

KEYS = ["telegram_relevance", "budget", "project_clarity", "client_credibility", "commercial_potential",
        "fit", "urgency", "competition", "source_quality", "complexity_fit"]
LABEL = {"telegram_relevance": "Telegram relevance", "budget": "Budget", "project_clarity": "Clarity",
         "client_credibility": "Credibility", "commercial_potential": "Commercial", "fit": "Fit",
         "urgency": "Urgency", "competition": "Competition", "source_quality": "Source",
         "complexity_fit": "Complexity fit"}
WEIGHTS = dict(zip(KEYS, [.15, .15, .12, .12, .12, .10, .08, .06, .05, .05]))
assert abs(sum(WEIGHTS.values()) - 1) < 1e-9


# ---------------- helpers ----------------
def meta(x, y): return {"designer": {"x": x, "y": y}}
def flt(name, groups): return {"name": name, "conditions": groups}
def c(a, o, b=None):
    d = {"a": a, "o": o}
    if b is not None: d["b"] = b
    return d

def m(mid, module, version, mapper, parameters=None, x=0, y=0, name=None, conds=None, onerror=None):
    mod = {"id": mid, "module": module, "version": version, "mapper": mapper,
           "parameters": parameters or {}, "metadata": meta(x, y)}
    if conds is not None: mod["filter"] = flt(name or "filter", conds)
    if onerror: mod["onerror"] = onerror
    return mod

def hook(mid, hook_id): return m(mid, "gateway:CustomWebHook", 1, {}, {"hook": hook_id, "maxResults": 1})
def setvars(mid, pairs, **kw):
    return m(mid, "util:SetVariables", 1, {"variables": [{"name": k, "value": v} for k, v in pairs], "scope": "roundtrip"}, **kw)
def ds_get(mid, store, key, **kw): return m(mid, "datastore:GetRecord", 1, {"key": key, "returnWrapped": False}, {"datastore": store}, **kw)
def ds_upd(mid, store, key, data, upsert=True, **kw):
    return m(mid, "datastore:UpdateRecord", 1, {"key": key, "upsert": upsert, "overwriteArrays": False, "data": data}, {"datastore": store}, **kw)
def ds_add(mid, store, key, data, **kw):
    return m(mid, "datastore:AddRecord", 1, {"key": key, "overwrite": True, "data": data}, {"datastore": store}, **kw)
def ds_search(mid, store, groups, limit=1, cont=True, **kw):
    return m(mid, "datastore:SearchRecord", 1, {"filter": groups, "sort": []},
             {"datastore": store, "continueWhenNoRes": cont, "limit": limit}, **kw)
def agg(mid, feeder, fields, **kw):
    return m(mid, "builtin:BasicAggregator", 1, fields, {"feeder": feeder}, **kw)
def router(mid, routes, x=0, y=0):
    return {"id": mid, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "metadata": meta(x, y),
            "routes": [{"flow": r} for r in routes]}
def ignore(mid): return [{"id": mid, "module": "builtin:Ignore", "version": 1, "mapper": None, "metadata": meta(0, 0)}]

def tg(mid, method, spec, onerror=True, **kw):
    """Telegram Bot API через подключение Make (токен не виден в сценарии)."""
    mod = m(mid, "telegram:UniversalAPICall", 1,
            {"method": "POST", "bodyType": "assembled_body", "body_spec": [{"key": k, "value": v} for k, v in spec],
             "urlMethod": method}, {"__IMTCONN__": CONN_TG}, **kw)
    if onerror and "onerror" not in mod: mod["onerror"] = ignore(mid + 500)
    return mod

def http_form(mid, url, fields, **kw):
    """Внутренний вызов другого сценария Lead Hunter (form-urlencoded: экранирование делает Make)."""
    mod = m(mid, "http:ActionSendData", 3,
            {"url": url, "method": "post", "headers": [], "qs": [], "bodyType": "x_www_form_urlencoded",
             "formFields": [{"key": k, "value": v} for k, v in fields], "parseResponse": False,
             "serializeUrl": False, "shareCookies": False, "rejectUnauthorized": True, "followRedirect": True,
             "followAllRedirects": False, "useQuerystring": False, "gzip": True, "useMtls": False},
            {"handleErrors": True, "useNewZLibDeCompress": True}, **kw)
    mod.setdefault("onerror", ignore(mid + 500))
    return mod

KB = lambda rows: json.dumps({"inline_keyboard": rows}, ensure_ascii=False)

def write_url(r):
    """T-0021: IML-выражение (без {{}}) URL кнопки «✍️ Написать клиенту» по записи лида r (ds_get, без обёртки).
    client_hint похож на Telegram-username (^[a-z0-9_]+$, длина 5–32; «noclient-…» не проходит из-за «-») → https://t.me/<hint>;
    иначе source_url; иначе пусто (кнопки нет). Фигурные скобки в regex не используем — длина проверяется length()."""
    h, src = r + ".client_hint", 'ifempty(' + r + '.source_url; "")'
    return ('if(' + h + '; if(replace(' + h + '; "/^[a-z0-9_]+$/"; "") = ""; if(length(' + h + ') >= 5; if(length(' + h + ') <= 32; '
            '"https://t.me/" + ' + h + '; ' + src + '); ' + src + '); ' + src + '); ' + src + ')')
WRITE_BTN = lambda ref: [{"text": "✍️ Написать клиенту", "url": "{{" + ref + "}}"}]
NO_CONTACT = "✍️ Контакт неизвестен — ответьте на площадке"
def ev(mid, lead, event, details, old="", new="", **kw):
    return ds_add(mid, S_LOG, "{{uuid}}", {"table": "events", "event_id": "{{uuid}}", "lead_id": lead, "event": event,
                  "details": details, "old_status": old, "new_status": new, "created_at": "{{now}}", "day": DAY_S}, **kw)

# settings в каждом сценарии читаются модулем 2; DAY — по часовому поясу из настроек
DAY_S = '{{formatDate(now; "YYYY-MM-DD"; ifempty(2.timezone; "Europe/Berlin"))}}'
OWNER = "{{2.owner_chat_id}}"


# ================= LH-99: установка (запускается один раз вручную) =================
def lh99():
    defaults = {"owner_chat_id": OWNER_CHAT_ID, "paused": False, "paused_reason": "", "daily_budget_usd": 3,
                "architect_threshold": 60, "hot_threshold": 80, "warm_threshold": 60, "cold_threshold": 40,
                "minimum_order_eur": 500, "timezone": "Europe/Berlin", "analyst_model": "claude-haiku-4-5",
                "analyst_max_tokens": 1500, "architect_model": "claude-sonnet-5-5", "sales_model": "claude-sonnet-5-5",
                "max_retry_attempts": 3, "retry_delays": "1,5,30", "analyst_price_in_mtok": 1, "analyst_price_out_mtok": 5,
                "fx_date": "", "lh03_url": URL03, "lh10_url": URL10, "lh11_url": URL11,
                "architect_max_tokens": 8000, "sales_max_tokens": 4000, "sonnet_price_in_mtok": 2, "sonnet_price_out_mtok": 10,
                "architect_prompt_version": ARCH_VERSION, "sales_prompt_version": SALES_VERSION, "cleanup_days": 30, "warned_80": "", "updated_at": "{{now}}",
                "webhook_secret": "{{1.ws}}", "internal_token": "{{1.it}}"}
    defaults.update({"w_" + k: v for k, v in WEIGHTS.items()})
    flow = [
        setvars(1, [("ws", '{{replace(uuid; "-"; "")}}{{replace(uuid; "-"; "")}}'), ("it", '{{replace(uuid; "-"; "")}}')]),
        ds_add(2, S_SET, "main", defaults),
        ds_add(3, S_SET, "source_manual", {"source": "manual", "label": "Ручной ввод (пересылка в пульт)",
               "access_method": "manual", "enabled": True, "owner_decision": "этап 2: единственный источник",
               "updated_at": "{{now}}"}),
        tg(4, "setWebhook", [("url", URL20), ("secret_token", "{{1.ws}}"),
                             ("allowed_updates", '["message","callback_query"]'), ("drop_pending_updates", "true")], onerror=False),
        tg(5, "sendMessage", [("chat_id", OWNER_CHAT_ID), ("text", "✅ Lead Hunter подключён к этому боту.\nПерешлите заявку (текст + ссылка) или нажмите /start.")]),
    ]
    return {"name": "LH-99 Lead Hunter — установка (разово)", "metadata": {"version": 1}, "flow": flow}


# ================= LH-20: Telegram Owner Panel =================
def lh20():
    H = "1.`__IMTHEADERS__`"
    secret = ('{{ifempty(get(map(' + H + '; "value"; "name"; "x-telegram-bot-api-secret-token"); 1); '
              'get(map(' + H + '; "value"; "name"; "X-Telegram-Bot-Api-Secret-Token"); 1))}}')
    txt = 'trim(ifempty(1.message.text; ifempty(1.message.caption; "")))'
    v = setvars(3, [
        ("from", "{{1.message.from.id}}{{1.callback_query.from.id}}"),
        ("chat", "{{1.message.chat.id}}{{1.callback_query.message.chat.id}}"),
        ("secret", secret),
        ("txt", "{{" + txt + "}}"),
        ("cmd", '{{lower(first(split(first(split(' + txt + '; " ")); "@")))}}'),
        ("a", '{{first(split(ifempty(1.callback_query.data; "-"); "|"))}}'),
        ("lead", '{{get(split(ifempty(1.callback_query.data; "-"); "|"); 2)}}'),
        ("r", '{{get(split(ifempty(1.callback_query.data; "-"); "|"); 3)}}'),
        ("mid", "{{1.callback_query.message.message_id}}"),
        ("cbid", "{{1.callback_query.id}}"),
    ])
    OK = [c("{{3.secret}}", "text:equal", "{{2.webhook_secret}}"), c("{{3.from}}", "text:equal", "{{2.owner_chat_id}}")]
    MSG = OK + [c("{{1.message.message_id}}", "exist")]
    CB = OK + [c("{{1.callback_query.id}}", "exist")]
    def cmd(name): return MSG + [c("{{3.cmd}}", "text:equal", name)]
    def act(a): return CB + [c("{{3.a}}", "text:equal", a)]
    answer = lambda mid, text="", **kw: tg(mid, "answerCallbackQuery", [("callback_query_id", "{{3.cbid}}")] + ([("text", text)] if text else []), **kw)
    routes = []
    y = 0
    # --- безопасность
    routes.append([ev(10, "", "SECURITY_DENIED", "from={{3.from}} secret_ok={{if(3.secret = 2.webhook_secret; \"yes\"; \"no\")}}",
                      name="Чужой chat_id или неверный secret",
                      conds=[[c("{{3.secret}}", "text:notequal", "{{2.webhook_secret}}")],
                             [c("{{3.from}}", "text:notequal", "{{2.owner_chat_id}}")]])])
    routes.append([tg(11, "sendMessage", [("chat_id", "{{3.chat}}"), ("text", "Access denied")],
                      name="Ответ чужому (только настоящий Telegram)",
                      conds=[[c("{{3.secret}}", "text:equal", "{{2.webhook_secret}}"),
                              c("{{3.from}}", "text:notequal", "{{2.owner_chat_id}}"),
                              c("{{1.message.message_id}}", "exist")]])])
    # --- /start
    LS = ds_search(20, S_LEADS, [[c("status", "text:equal", "NEW")], [c("status", "text:equal", "SENT_TO_TELEGRAM")]],
                   limit=500, name="/start", conds=[cmd("/start")])
    A = agg(21, 20, {"status": "{{20.data.status}}", "grade": "{{20.data.grade}}", "lead_id": "{{20.key}}"})
    day_touch = lambda mid: ds_upd(mid, S_SET, "day_" + DAY_S, {"day": DAY_S})
    day_get = lambda mid: ds_get(mid, S_SET, "day_" + DAY_S)
    START = ("🧭 Lead Hunter — пульт\n"
             "Статус: {{if(2.paused; \"⏸ пауза\"; \"▶️ работает\")}}{{if(2.paused; \" (\" + ifempty(2.paused_reason; \"владелец\") + \")\"; \"\")}}\n"
             "📥 В очереди (NEW): {{length(map(21.array; \"lead_id\"; \"status\"; \"NEW\"))}}\n"
             "🆕 Без решения: {{length(map(21.array; \"lead_id\"; \"status\"; \"SENT_TO_TELEGRAM\"))}}"
             " · 🔥 HOT: {{length(map(21.array; \"lead_id\"; \"grade\"; \"HOT\"))}}\n"
             "💵 Claude сегодня: ${{formatNumber(ifempty(23.cost_usd; 0); 4; \".\"; \"\")}} из ${{2.daily_budget_usd}}\n"
             "📡 Источники: ✅ ручной ввод · ⏸ автоисточники выключены (этап 2)\n\n"
             "Перешлите заявку (текст + ссылка) — пришлю карточку с оценкой.\n/new /today /stats /pause /resume /settings /help\n"
             "🤖 /ai — чат с AI-директором{{if(2.ai_mode; \" (включён, /ai off — выключить)\"; \"\")}}")
    routes.append([LS, A, day_touch(22), day_get(23), tg(24, "sendMessage", [("chat_id", OWNER), ("text", START)])])
    # --- /help
    HELP = ("ℹ️ Lead Hunter — пульт владельца\n\n"
            "1. Перешлите сюда заявку: текст, текст + ссылка или пост из канала.\n"
            "2. Через ~1 мин придёт карточка: оценка 0–100, HOT/WARM/COLD/REJECT, причины.\n"
            "3. ✅ Approve — Architect + Sales готовят ТЗ и КП (~1–3 мин), придёт коммерческая карточка; ❌ Reject — с причиной.\n"
            "4. На карточке: 📋 Full ТЗ (+ файл .md), 💰 Offer, 💬 Client Message, ❓ Questions, 🔍 More Analysis (1 раз), 📞 Contacted, 🏆 Won, ❌ Lost, 📦 Archive.\n"
            "Клиенту бот ничего не отправляет — только вы вручную.\n\n"
            "/new — новые HOT/WARM без решения (до 5)\n/today — итоги дня\n/stats — 7 и 30 дней\n"
            "/won LEAD сумма — исправить сумму сделки\n/pause — пауза AI (заявки копятся в очереди)\n/resume — продолжить и разобрать очередь\n/settings — настройки\n\n"
            "🤖 /ai — чат с AI-директором: /ai — включить (обычный текст идёт AI, пересланное и ссылки — заявки), "
            "/ai вопрос — разовый вопрос, /ai off или /stop — выключить, /ai new — очистить память, /ai status — счётчик (лимит 10 ответов в день).\n\n"
            "Скриншоты и файлы пока не разбираются — пришлите текст и ссылку.")
    routes.append([tg(30, "sendMessage", [("chat_id", OWNER), ("text", HELP)], name="/help", conds=[cmd("/help")])])
    # --- /settings
    SET = ("⚙️ Настройки (lh_settings → main)\n"
           "Пауза: {{if(2.paused; \"да\"; \"нет\")}} · бюджет в день: ${{2.daily_budget_usd}}\n"
           "Пороги: HOT ≥ {{2.hot_threshold}} · WARM ≥ {{2.warm_threshold}} · COLD ≥ {{2.cold_threshold}} · Architect ≥ {{2.architect_threshold}}\n"
           "Мин. заказ: {{2.minimum_order_eur}} € · часовой пояс: {{2.timezone}}\n"
           "Analyst: {{2.analyst_model}} (до {{2.analyst_max_tokens}} токенов), цена ${{2.analyst_price_in_mtok}}/${{2.analyst_price_out_mtok}} за 1M\n"
           "Повторы: до {{2.max_retry_attempts}}, задержки {{2.retry_delays}} мин\n"
           "Веса: " + " · ".join(f"{LABEL[k]} {{{{2.w_{k}}}}}" for k in KEYS) + "\n"
           "Курсы к EUR ({{ifempty(2.fx_date; \"не заданы\")}}): USD {{2.fx_usd}} · GBP {{2.fx_gbp}} · CHF {{2.fx_chf}} · PLN {{2.fx_pln}} · UAH {{2.fx_uah}}\n\n"
           "Изменить: Make → Data stores → lh_settings → запись main.")
    routes.append([tg(31, "sendMessage", [("chat_id", OWNER), ("text", SET)], name="/settings", conds=[cmd("/settings")])])
    # --- /pause, /resume
    routes.append([ds_upd(40, S_SET, "main", {"paused": True, "paused_reason": "владелец (/pause)", "updated_at": "{{now}}"},
                          name="/pause", conds=[cmd("/pause")]),
                   ev(41, "", "PAUSED", "owner /pause"),
                   tg(42, "sendMessage", [("chat_id", OWNER), ("text", "⏸ AI-обработка на паузе. Пересланные заявки сохраняются в очередь (NEW) без вызова Claude. /resume — продолжить.")])])
    routes.append([ds_upd(43, S_SET, "main", {"paused": False, "paused_reason": "", "updated_at": "{{now}}"},
                          name="/resume", conds=[cmd("/resume")]),
                   ev(44, "", "RESUMED", "owner /resume"),
                   tg(45, "sendMessage", [("chat_id", OWNER), ("text", "▶️ Продолжаю. Разбираю очередь — карточки придут по одной.")]),
                   ds_search(46, S_LEADS, [[c("status", "text:equal", "NEW")]], limit=20, cont=False),
                   http_form(47, URL10, [("token", "{{2.internal_token}}"), ("lead_id", "{{46.key}}")])])
    # --- /new
    routes.append([ds_search(50, S_LEADS, [[c("status", "text:equal", "SENT_TO_TELEGRAM"), c("grade", "text:equal", "HOT")],
                                           [c("status", "text:equal", "SENT_TO_TELEGRAM"), c("grade", "text:equal", "WARM")]],
                             limit=5, name="/new", conds=[cmd("/new")]),
                   router(51, [
                       [tg(52, "sendMessage", [("chat_id", OWNER), ("text", "{{50.data.card_text}}"),
                                               ("reply_markup", KB([[{"text": "✅ Approve", "callback_data": "ap|{{50.key}}"},
                                                                     {"text": "❌ Reject", "callback_data": "rj|{{50.key}}"}],
                                                                    [{"text": "🔍 More analysis", "callback_data": "ma|{{50.key}}"}]]))],
                           name="Есть лид", conds=[[c("{{50.key}}", "exist")]])],
                       [tg(53, "sendMessage", [("chat_id", OWNER), ("text", "Новых HOT/WARM без решения нет.")],
                           name="Пусто", conds=[[c("{{50.key}}", "notexist")]])]])])
    # --- /today
    TODAY = ("📅 Сегодня {{formatDate(now; \"DD.MM.YYYY\"; 2.timezone)}}\n"
             "Found: {{length(map(61.array; \"lead_id\"; \"has\"; \"1\"))}}\n"
             "Analyzed: {{length(map(61.array; \"lead_id\"; \"grade\"; \"HOT\")) + length(map(61.array; \"lead_id\"; \"grade\"; \"WARM\")) + length(map(61.array; \"lead_id\"; \"grade\"; \"COLD\")) + length(map(61.array; \"lead_id\"; \"grade\"; \"REJECT\"))}}\n"
             "🔥 HOT: {{length(map(61.array; \"lead_id\"; \"grade\"; \"HOT\"))}} · 🌤 WARM: {{length(map(61.array; \"lead_id\"; \"grade\"; \"WARM\"))}}\n"
             "✅ Approved: {{length(map(63.array; \"id\"; \"action\"; \"APPROVE\"))}} · ❌ Rejected: {{length(map(63.array; \"id\"; \"action\"; \"REJECT\"))}}\n"
             "⚠️ Errors: {{length(map(61.array; \"lead_id\"; \"status\"; \"ERROR\"))}}\n"
             "💵 Claude cost: ${{formatNumber(ifempty(65.cost_usd; 0); 4; \".\"; \"\")}}")
    routes.append([ds_search(60, S_LEADS, [[c("day", "text:equal", DAY_S)]], limit=500, name="/today", conds=[cmd("/today")]),
                   agg(61, 60, {"lead_id": "{{60.key}}", "has": "{{if(60.key; \"1\"; \"\")}}", "grade": "{{60.data.grade}}", "status": "{{60.data.status}}"}),
                   ds_search(62, S_LOG, [[c("table", "text:equal", "decisions"), c("day", "text:equal", DAY_S)]], limit=500),
                   agg(63, 62, {"id": "{{62.key}}", "action": "{{62.data.action}}"}),
                   day_touch(64), day_get(65),
                   tg(66, "sendMessage", [("chat_id", OWNER), ("text", TODAY)])])
    # --- /stats (7 и 30 дней)
    def stats_block(L, R, title):
        cnt = lambda f, v: '{{length(map(' + L + '.array; "lead_id"; "' + f + '"; "' + v + '"))}}'
        an = ('length(map(' + L + '.array; "lead_id"; "grade"; "HOT")) + length(map(' + L + '.array; "lead_id"; "grade"; "WARM")) + '
              'length(map(' + L + '.array; "lead_id"; "grade"; "COLD")) + length(map(' + L + '.array; "lead_id"; "grade"; "REJECT"))')
        return (f"{title}\n"
                "Found: {{length(map(" + L + ".array; \"lead_id\"; \"has\"; \"1\"))}} · HOT: " + cnt("grade", "HOT") + " · WARM: " + cnt("grade", "WARM") +
                " · REJECT: " + cnt("grade", "REJECT") + "\n"
                "Approved: " + cnt("status", "APPROVED") + " · Contacted: " + cnt("status", "CONTACTED") +
                " · Won: " + cnt("status", "WON") + " · Lost: " + cnt("status", "LOST") + "\n"
                "Avg score: {{round(sum(map(" + L + ".array; \"score\")) / max(1; " + an + "))}}"
                " · Avg budget: {{if(length(map(" + L + ".array; \"lead_id\"; \"hb\"; \"1\")) > 0; round(sum(map(" + L + ".array; \"budget_eur\")) / length(map(" + L + ".array; \"lead_id\"; \"hb\"; \"1\"))) + \" €\"; \"—\")}}\n"
                "Claude cost: ${{formatNumber(sum(map(" + R + ".array; \"cost\")); 4; \".\"; \"\")}}")
    def win(base, days):
        since = '{{addDays(now; -' + str(days) + ')}}'
        L, LA, R, RA = base, base + 1, base + 2, base + 3
        return [ds_search(L, S_LEADS, [[c("created_at", "date:greaterorequal", since)]], limit=1000),
                agg(LA, L, {"lead_id": "{{" + str(L) + ".key}}", "has": "{{if(" + str(L) + ".key; \"1\"; \"\")}}",
                            "grade": "{{" + str(L) + ".data.grade}}", "status": "{{" + str(L) + ".data.status}}",
                            "score": "{{ifempty(" + str(L) + ".data.score; 0)}}", "budget_eur": "{{ifempty(" + str(L) + ".data.budget_eur; 0)}}",
                            "hb": "{{if(" + str(L) + ".data.budget_eur; \"1\"; \"\")}}"}),
                ds_search(R, S_LOG, [[c("table", "text:equal", "runs"), c("created_at", "date:greaterorequal", since)]], limit=1000),
                agg(RA, R, {"cost": "{{ifempty(" + str(R) + ".data.estimated_cost_usd; 0)}}"})]
    w7, w30 = win(70, 7), win(74, 30)
    w7[0]["filter"] = flt("/stats", [cmd("/stats")])
    STATS = ("📊 Статистика\n\n" + stats_block("71", "73", "— 7 дней") + "\n\n" + stats_block("75", "77", "— 30 дней") +
             "\n\nПока данных мало — нули реальные, а не оценки.")
    routes.append(w7 + w30 + [tg(78, "sendMessage", [("chat_id", OWNER), ("text", STATS)])])
    # --- приём заявки → LH-03
    fo = "1.message.forward_origin"
    LEADBASE = MSG + [c("{{3.txt}}", "exist"), c("{{3.txt}}", "text:notpattern", "^/")]
    AI_ON = c('{{if(2.ai_mode; "on"; "off")}}', "text:equal", "on")
    AI_OFF = c('{{if(2.ai_mode; "on"; "off")}}', "text:equal", "off")
    FWD = c("{{1.message.forward_origin.type}}{{1.message.forward_date}}", "exist")
    NOT_FWD = c("{{1.message.forward_origin.type}}", "notexist")
    NOT_FWD_OLD = c("{{1.message.forward_date}}", "notexist")
    LINK_RE = "t\\.me/|https?://|text_link"
    LINKSRC = '{{lower(3.txt)}} {{join(map(ifempty(1.message.entities; 1.message.caption_entities); "type"); " ")}}'
    LINK = c(LINKSRC, "text:pattern", LINK_RE)
    NOT_LINK = c(LINKSRC, "text:notpattern", LINK_RE)
    routes.append([http_form(80, URL03, [
        ("token", "{{2.internal_token}}"), ("text", "{{3.txt}}"), ("message_id", "{{1.message.message_id}}"),
        ("text_links", '{{join(map(ifempty(1.message.entities; 1.message.caption_entities); "url"; "type"; "text_link"); " ")}}'),
        ("fwd_type", "{{" + fo + ".type}}"), ("fwd_chat_username", "{{" + fo + ".chat.username}}"),
        ("fwd_chat_title", "{{" + fo + ".chat.title}}"), ("fwd_message_id", "{{" + fo + ".message_id}}"),
        ("fwd_user_username", "{{" + fo + ".sender_user.username}}"),
        ("fwd_user_name", "{{" + fo + ".sender_user.first_name}}{{" + fo + ".sender_user_name}}"),
        ("fwd_date", "{{" + fo + ".date}}")],
        name="Пересланная заявка", conds=[LEADBASE + [AI_OFF], LEADBASE + [FWD], LEADBASE + [LINK]]),
        tg(81, "sendMessage", [("chat_id", OWNER), ("text", "⏳ Принял, сохраняю…")])])
    # --- AI-чат владельца (T-20261008-0034): LH-20 → AI-01 (7852575) POST {token, chat_id, text}; ответ шлёт AI-01 через тот же бот.
    # /ai — включить режим; /ai off, /stop — выключить; /ai new|status → /new|/status AI-01; /ai <вопрос> — разовый вопрос.
    # В AI-режиме обычный текст (не команда, не пересланный, без t.me/http-ссылки) идёт в AI-01; пересланное и ссылки — всегда заявки.
    AIURL = '{{ifempty(2.ai01_url; "' + URL_AI01 + '")}}'
    to_ai = lambda mid, text, **kw: http_form(mid, AIURL, [("token", "{{2.internal_token}}"), ("chat_id", "{{3.from}}"), ("text", text)], **kw)
    AI_HINT = ("🤖 AI-чат включён. Пишите обычным текстом — отвечает AI-директор RAIV FISH (совет, план, черновик поста или КП).\n"
               "Пересланные сообщения и ссылки по-прежнему идут как заявки.\n"
               "/ai off или /stop — выключить · /ai new — очистить память · /ai status — счётчик. Лимит 10 ответов в день.")
    AI_OFF_TXT = "💤 AI-чат выключен. Пересланное и текст снова идут как заявки. /ai — включить."
    ARG = 'lower(trim(substring(3.txt; length(first(split(3.txt; " "))); 4000)))'
    routes.append([setvars(261, [("arg", '{{trim(substring(3.txt; length(first(split(3.txt; " "))); 4000))}}'),
                                ("sub", "{{" + ARG + "}}")], name="/ai", conds=[cmd("/ai")]),
                   router(262, [
                       [ds_upd(263, S_SET, "main", {"ai_mode": True, "updated_at": "{{now}}"}, name="/ai → включить",
                               conds=[[c("{{261.arg}}", "notexist")]]),
                        tg(264, "sendMessage", [("chat_id", OWNER), ("text", AI_HINT)])],
                       [ds_upd(265, S_SET, "main", {"ai_mode": False, "updated_at": "{{now}}"}, name="/ai off → выключить",
                               conds=[[c("{{261.sub}}", "text:equal", "off")]]),
                        tg(266, "sendMessage", [("chat_id", OWNER), ("text", AI_OFF_TXT)])],
                       [to_ai(267, "/{{261.sub}}", name="/ai new | /ai status → AI-01",
                              conds=[[c("{{261.sub}}", "text:equal", "new")], [c("{{261.sub}}", "text:equal", "status")]])],
                       [to_ai(268, "{{261.arg}}", name="/ai вопрос → AI-01 (разово)",
                              conds=[[c("{{261.arg}}", "exist")] + [c("{{261.sub}}", "text:notequal", x) for x in ("off", "new", "status")]])]])])
    routes.append([ds_upd(269, S_SET, "main", {"ai_mode": False, "updated_at": "{{now}}"}, name="/stop → AI-чат выкл", conds=[cmd("/stop")]),
                   tg(270, "sendMessage", [("chat_id", OWNER), ("text", AI_OFF_TXT)])])
    routes.append([to_ai(260, "{{3.txt}}", name="AI-режим: обычный текст → AI-01",
                         conds=[LEADBASE + [AI_ON, NOT_FWD, NOT_FWD_OLD, NOT_LINK]])])
    routes.append([tg(82, "sendMessage", [("chat_id", OWNER), ("text", "🖼 Скриншоты и файлы без текста пока не разбираю (этап 2). Пришлите текст заявки и ссылку.")],
                      name="Медиа без текста", conds=[MSG + [c("{{3.txt}}", "notexist")]])])
    # --- кнопки
    LEADK = "{{3.lead}}"
    dec = lambda mid, action, reason="": ds_add(mid, S_LOG, "{{uuid}}", {
        "table": "decisions", "decision_id": "{{uuid}}", "lead_id": LEADK, "owner_chat_id": "{{3.from}}", "action": action,
        "reason": reason, "telegram_message_id": "{{3.mid}}", "created_at": "{{now}}", "day": DAY_S})
    # --- ✅ Approve → защита от повтора → LH-11 (Architect + Sales), этап 3
    URL11X = "{{ifempty(2.lh11_url; \"" + URL11 + "\")}}"
    call11 = lambda mid, run, mode: http_form(mid, URL11X, [("token", "{{2.internal_token}}"), ("lead_id", LEADK), ("run_id", run), ("mode", mode)])
    STALE = "{{addMinutes(now; -10)}}"  # «сторож»: APPROVED без движения > 10 мин = завис, повтор разрешён
    AP_AT = '{{ifempty(90.approved_at; "2000-01-01T00:00:00.000Z")}}'
    can_run = [[c("{{90.status}}", "exist"), c('{{ifempty(90.architect_run_id; "none")}}', "text:equal", "none")],
               [c("{{90.status}}", "exist"), c("{{90.status}}", "text:equal", "ERROR")],
               [c("{{90.status}}", "text:equal", "APPROVED"), c(AP_AT, "date:less", STALE)]]
    COLDW = '{{if(90.grade = "COLD"; newline + "⚠️ Grade COLD: Architect запущен по вашему решению."; if(90.grade = "REJECT"; newline + "⚠️ Grade REJECT: Architect запущен по вашему решению, проверьте риски."; ""))}}'
    routes.append([ds_get(90, S_LEADS, LEADK, name="✅ Approve", conds=[act("ap")]),
                   router(132, [
                       [setvars(133, [("run", "{{uuid}}")], name="Первый Approve (или повтор после ERROR)", conds=can_run),
                        ds_upd(91, S_LEADS, LEADK, {"status": "APPROVED", "status_at": "{{now}}", "approved_at": "{{now}}",
                                                    "architect_run_id": "{{133.run}}", "error_code": "", "error_message": "",
                                                    "updated_at": "{{now}}"}, upsert=False),
                        dec(92, "APPROVE"), ev(93, LEADK, "OWNER_APPROVED", "button · run {{133.run}}", old="{{90.status}}", new="APPROVED"),
                        call11(134, "{{133.run}}", "normal"),  # D1: LH-11 до любых Telegram-вызовов
                        answer(94, "Approved → Architect + Sales"),
                        tg(95, "editMessageReplyMarkup", [("chat_id", OWNER), ("message_id", "{{3.mid}}"),
                                                          ("reply_markup", KB([[{"text": "✅ Approved · Architect работает", "callback_data": "z"}]]))]),
                        tg(96, "sendMessage", [("chat_id", OWNER), ("text", "✅ " + LEADK + " одобрен. Architect + Sales готовят ТЗ и КП (~1–3 мин), пришлю коммерческую карточку.\n"
                                               "Клиенту ничего не отправляется." + COLDW)])],
                       [answer(135, "Уже одобрен: Architect уже запускался ({{ifempty(90.status; \"лид не найден\")}}). Повтор — после ERROR или если APPROVED завис > 10 мин.",
                               name="Повторный Approve — без запуска",
                               conds=[[c('{{ifempty(90.architect_run_id; "none")}}', "text:notequal", "none"), c("{{90.status}}", "text:notequal", "ERROR"),
                                       c("{{90.status}}", "text:notequal", "APPROVED")],
                                      [c('{{ifempty(90.architect_run_id; "none")}}', "text:notequal", "none"), c("{{90.status}}", "text:equal", "APPROVED"),
                                       c(AP_AT, "date:greaterorequal", STALE)],
                                      [c("{{90.status}}", "notexist")]])]])])
    REASONS = [("1", "💰 Too cheap"), ("2", "🎯 Not our profile"), ("3", "⚠️ Suspicious"), ("4", "🏗 Too complex"), ("5", "❌ Other")]
    routes.append([answer(100, "Причина?", name="❌ Reject → причины", conds=[act("rj")]),
                   tg(101, "editMessageReplyMarkup", [("chat_id", OWNER), ("message_id", "{{3.mid}}"),
                      ("reply_markup", KB([[{"text": t, "callback_data": "rr|" + LEADK + "|" + k}] for k, t in REASONS]))])])
    RS = "switch(3.r; " + "; ".join(f'"{k}"; "{t}"' for k, t in REASONS) + '; "Other")'
    routes.append([ds_get(110, S_LEADS, LEADK, name="❌ Reject с причиной", conds=[act("rr")]),
                   ds_upd(111, S_LEADS, LEADK, {"status": "REJECTED", "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False),
                   dec(112, "REJECT", "{{" + RS + "}}"),
                   ev(113, LEADK, "OWNER_REJECTED", "{{" + RS + "}}", old="{{110.status}}", new="REJECTED"),
                   answer(114, "Rejected"),
                   tg(115, "editMessageReplyMarkup", [("chat_id", OWNER), ("message_id", "{{3.mid}}"),
                      ("reply_markup", KB([[{"text": "❌ Rejected", "callback_data": "z"}]]))])])
    routes.append([dec(120, "MORE_ANALYSIS_REQUESTED", name="🔍 More analysis", conds=[act("ma")]) if False else
                   ds_add(120, S_LOG, "{{uuid}}", {"table": "decisions", "decision_id": "{{uuid}}", "lead_id": LEADK,
                          "owner_chat_id": "{{3.from}}", "action": "MORE_ANALYSIS_REQUESTED", "reason": "",
                          "telegram_message_id": "{{3.mid}}", "created_at": "{{now}}", "day": DAY_S},
                          name="🔍 More analysis", conds=[act("ma")]),
                   ev(121, LEADK, "MORE_ANALYSIS_REQUESTED", "button"),
                   answer(122, "OK"),
                   tg(123, "sendMessage", [("chat_id", OWNER), ("text", "🔍 Углублённый анализ делает Architect после ✅ Approve. На коммерческой карточке будет кнопка 🔍 More Analysis (1 повторный прогон на лид).\n" + LEADK)])])
    # --- кнопки коммерческой карточки (этап 3); клиенту ничего не отправляется
    lst = lambda p: '{{if(length(' + p + ') > 0; "- " + join(' + p + '; newline + "- "); "- —")}}'
    X = "142."
    MD = ("# Техническое задание (черновик) — " + LEADK + "\n\n"
          "{{140.title}}\nИсточник: {{140.source}} · {{ifempty(140.source_url; \"нет ссылки\")}}\n"
          "Черновик Architect ({{ifempty(2.architect_prompt_version; \"" + ARCH_VERSION + "\")}}), требует проверки. Метки: CLIENT_REQUIREMENT — написал клиент; "
          "INFERRED — вывод из текста; RECOMMENDATION — наше предложение; UNKNOWN — уточнить у клиента.\n\n"
          "## 1. Суть проекта\n{{142.project_summary}}\n\n## 2. Цель клиента\n{{142.client_goal}}\n\n"
          "## 3. Решение в Telegram\n" + "".join(f"- {t}: {{{{142.telegram_solution.{k}}}}}\n" for k, t in
              [("bot", "Бот"), ("mini_app", "Mini App"), ("ai", "AI"), ("crm", "CRM"), ("payments", "Платежи"),
               ("notifications", "Уведомления"), ("admin_panel", "Админ-панель")]) + "\n" +
          "".join(f"## {n}. {t}\n" + lst(X + k) + "\n\n" for n, (k, t) in enumerate([
              ("functional_requirements", "Функциональные требования"), ("user_roles", "Роли пользователей"),
              ("user_flow", "Пользовательский сценарий"), ("mvp", "MVP"), ("phase_2", "Фаза 2"), ("integrations", "Интеграции"),
              ("api_requirements", "Требования к API")], start=4)) +
          "## 11. База данных\nНужна: {{142.database.required}} · предлагаем: {{ifempty(142.database.suggested; \"—\")}}\n" + lst(X + "database.entities") + "\n\n"
          "## 12. Админ-панель\nНужна: {{142.admin_panel.required}}\n" + lst(X + "admin_panel.functions") + "\n\n" +
          "".join(f"## {n}. {t}\n" + lst(X + k) + "\n\n" for n, (k, t) in enumerate([
              ("ai_features", "AI-функции"), ("notifications", "Уведомления"), ("analytics", "Аналитика"), ("security", "Безопасность"),
              ("technology_stack", "Технологии"), ("technical_risks", "Технические риски"), ("missing_information", "Чего не хватает"),
              ("questions_for_client", "Вопросы клиенту (по приоритету)"), ("required_specialists", "Нужные специалисты")], start=13)) +
          "## 22. Аутентификация и хостинг\n- Аутентификация: {{142.authentication}}\n- Хостинг: {{142.hosting}}\n\n"
          "## 23. Оценка\nСложность: {{142.complexity}} · {{142.estimated_hours_min}}–{{142.estimated_hours_max}} ч (диапазон, оценка Architect)\n\n"
          "## 24. Заметки архитектора\n{{142.architecture_notes}}\n")
    SUMMARY = ("📋 ТЗ " + LEADK + " · {{142.complexity}} · ⏱ {{142.estimated_hours_min}}–{{142.estimated_hours_max}} ч\n"
               "{{substring(142.project_summary; 0; 700)}}\n\nMVP:\n• {{join(slice(142.mvp; 0; 6); newline + \"• \")}}\n\nПолное ТЗ — в файле .md ниже.")
    NOTREADY = lambda mid, what: answer(mid, what + " ещё не готово (нужен ✅ Approve и завершённый Architect + Sales).")
    doc = m(146, "telegram:SendDocument", 1, {"chatId": OWNER, "sendType": "send_bydata", "filename": "TZ_" + LEADK + ".md",
            "data": "{{toBinary(144.md)}}", "caption": "ТЗ " + LEADK + " — черновик Architect (не отправлено клиенту)", "contentType": "text/plain"},
            {"__IMTCONN__": CONN_TG})
    doc["onerror"] = ignore(646)
    routes.append([ds_get(140, S_LEADS, LEADK, name="📋 Full ТЗ", conds=[act("ft")]),
                   router(141, [
                       [m(142, "json:ParseJSON", 1, {"json": "{{140.architect_json}}"}, {"type": DS_ARCH}, onerror=ignore(642),
                          name="ТЗ есть", conds=[[c("{{140.architect_json}}", "exist")]]),
                        answer(143, "ТЗ"), setvars(144, [("md", MD)]),
                        tg(145, "sendMessage", [("chat_id", OWNER), ("text", SUMMARY)]), doc],
                       [dict(NOTREADY(147, "ТЗ"), filter=flt("ТЗ нет", [[c("{{140.architect_json}}", "notexist")]]))]])])
    PK = lambda k, t: ("📦 " + t + " — {{152.packages." + k + ".price}} € · {{ifempty(152.packages." + k + ".timeline; \"срок ?\")}}\n"
                       "✅ {{join(slice(152.packages." + k + ".included; 0; 8); \"; \")}}\n🚫 {{join(slice(152.packages." + k + ".excluded; 0; 5); \"; \")}}\n\n")
    OFFER = ("💰 КП " + LEADK + " (наша оценка, не бюджет клиента)\n"
             "Себестоимость ≈ {{152.estimated_cost}} € · рекомендуем {{152.recommended_price}} € · цель {{152.target_price}} € · минимум {{152.minimum_acceptable_price}} €\n"
             "{{substring(152.price_reasoning; 0; 500)}}\n\n" + PK("basic", "Basic") + PK("professional", "Professional") + PK("premium", "Premium") +
             "📈 Win {{152.win_probability}}% — {{152.win_probability_reason}}\n"
             "🏦 Потенциал {{152.commercial_potential}} — {{152.commercial_potential_reason}}\n"
             "Выручка: проект {{ifempty(152.potential_revenue; \"UNKNOWN\")}} · фаза 2 {{ifempty(152.phase_2_revenue; \"UNKNOWN\")}} · "
             "поддержка {{ifempty(152.maintenance_revenue; \"UNKNOWN\")}} · upsell {{ifempty(152.upsell_revenue; \"UNKNOWN\")}}\n"
             "➕ Upsells: {{ifempty(join(152.upsells; \"; \"); \"—\")}}\n"
             "📎 Допущения: {{ifempty(join(slice(152.assumptions; 0; 5); \"; \"); \"—\")}}")
    routes.append([ds_get(150, S_LEADS, LEADK, name="💰 Offer", conds=[act("of")]),
                   router(151, [
                       [m(152, "json:ParseJSON", 1, {"json": "{{150.sales_json}}"}, {"type": DS_SALES}, onerror=ignore(652),
                          name="КП есть", conds=[[c("{{150.sales_json}}", "exist")]]),
                        setvars(156, [("t", OFFER)]), answer(153, "Offer"),
                        tg(154, "sendMessage", [("chat_id", OWNER), ("text", "{{substring(156.t; 0; 4000)}}")])],
                       [dict(NOTREADY(155, "КП"), filter=flt("КП нет", [[c("{{150.sales_json}}", "notexist")]]))]])])
    routes.append([ds_get(160, S_LEADS, LEADK, name="💬 Client Message", conds=[act("cm")]),
                   router(161, [
                       [answer(162, "Client message", name="Есть", conds=[[c("{{160.client_message}}", "exist")]]),
                        setvars(165, [("wurl", "{{" + write_url("160") + "}}")]),
                        setvars(166, [("kb1", KB([WRITE_BTN("165.wurl")])), ("kb0", KB([]))]),
                        tg(163, "sendMessage", [("chat_id", OWNER), ("text",
                           "💬 Сообщение клиенту " + LEADK + " ({{ifempty(160.language; \"?\")}}) — отправляете только вы, вручную. "
                           "Текст для копирования — следующим сообщением.\n"
                           "{{if(165.wurl; \"✍️ Кнопка «Написать клиенту» — под ним.\"; \"" + NO_CONTACT + "\")}}\n\n"
                           "🇷🇺 Перевод:\n{{substring(160.client_message_ru; 0; 3500)}}")]),
                        tg(167, "sendMessage", [("chat_id", OWNER), ("text", "{{substring(160.client_message; 0; 4000)}}"),
                                                ("reply_markup", "{{if(165.wurl; 166.kb1; 166.kb0)}}")])],
                       [dict(NOTREADY(164, "Сообщение"), filter=flt("Нет", [[c("{{160.client_message}}", "notexist")]]))]])])
    routes.append([ds_get(170, S_LEADS, LEADK, name="❓ Questions", conds=[act("qs")]),
                   router(171, [
                       [answer(172, "Questions", name="Есть", conds=[[c("{{170.client_questions}}", "exist")]]),
                        tg(173, "sendMessage", [("chat_id", OWNER), ("text",
                           "❓ Вопросы клиенту " + LEADK + " (по приоритету):\n{{substring(170.client_questions; 0; 2500)}}\n\n"
                           "🧩 Чего не хватает:\n{{ifempty(substring(170.missing_information; 0; 1200); \"—\")}}")])],
                       [dict(NOTREADY(174, "Вопросы"), filter=flt("Нет", [[c("{{170.client_questions}}", "notexist")]]))]])])
    # 🔍 More Analysis — 1 углублённый прогон Architect + Sales на лид
    MX_DONE = c('{{ifempty(180.sales_run_id; "none")}}', "text:notequal", '{{ifempty(180.architect_run_id; "none")}}')  # углублённый прогон не завершён
    MX_AT = '{{ifempty(180.more_analysis_at; "2000-01-01T00:00:00.000Z")}}'
    MX_SET = c('{{ifempty(180.more_analysis_at; "none")}}', "text:notequal", "none")
    can_more = [[c("{{180.sales_json}}", "exist"), c('{{ifempty(180.more_analysis_at; "none")}}', "text:equal", "none")],
                [c("{{180.sales_json}}", "exist"), MX_SET, MX_DONE, c("{{180.status}}", "text:equal", "ERROR")],
                [c("{{180.sales_json}}", "exist"), MX_SET, MX_DONE, c(MX_AT, "date:less", "{{addMinutes(now; -10)}}")]]
    no_more = [[c("{{180.sales_json}}", "notexist")],
               [MX_SET, c('{{ifempty(180.sales_run_id; "none")}}', "text:equal", '{{ifempty(180.architect_run_id; "none")}}')],
               [MX_SET, c("{{180.status}}", "text:notequal", "ERROR"), c(MX_AT, "date:greaterorequal", "{{addMinutes(now; -10)}}")]]
    routes.append([ds_get(180, S_LEADS, LEADK, name="🔍 More Analysis", conds=[act("mx")]),
                   router(181, [
                       [setvars(182, [("run", "{{uuid}}")], name="Ещё не было (или прошлый завис/ERROR)", conds=can_more),
                        ds_upd(183, S_LEADS, LEADK, {"more_analysis_at": "{{now}}", "architect_run_id": "{{182.run}}", "updated_at": "{{now}}"}, upsert=False),
                        dec(184, "MORE_ANALYSIS_REQUESTED"), ev(185, LEADK, "MORE_ANALYSIS_REQUESTED", "deep re-run {{182.run}}"),
                        call11(188, "{{182.run}}", "more"),  # D1: LH-11 до любых Telegram-вызовов
                        answer(186, "Углублённый анализ запущен"),
                        tg(187, "sendMessage", [("chat_id", OWNER), ("text", "🔍 " + LEADK + ": углублённый прогон Architect + Sales запущен "
                                                "(единственный для этого лида). Пришлю новую карточку через ~1–3 мин.")])],
                       [answer(189, "Углублённый анализ уже был (1 раз на лид) или КП ещё не готово.", name="Нельзя",
                               conds=no_more)]])])
    st = lambda base, label, status, action, extra, emo: [
        ds_get(base, S_LEADS, LEADK, name=label, conds=[act(action)]),
        ds_upd(base + 1, S_LEADS, LEADK, dict({"status": status, "status_at": "{{now}}", "updated_at": "{{now}}"}, **extra), upsert=False),
        dec(base + 2, status), ev(base + 3, LEADK, "OWNER_" + status, "button", old="{{" + str(base) + ".status}}", new=status),
        answer(base + 4, emo)]
    routes.append(st(200, "📞 Contacted", "CONTACTED", "ct", {"contacted_at": "{{now}}"}, "📞 Contacted (бот клиенту ничего не отправлял)"))
    routes.append(st(210, "🏆 Won", "WON", "wn", {"won_at": "{{now}}", "deal_amount_eur": "{{210.recommended_price}}"}, "🏆 Won") +
                  [tg(215, "sendMessage", [("chat_id", OWNER), ("text", "🏆 " + LEADK + " — WON. Сумма сделки = рекомендованная цена: "
                                           "{{ifempty(210.recommended_price; \"не задана\")}} €.\nИсправить: /won " + LEADK + " <сумма в EUR>")])])
    routes.append(st(240, "📦 Archive", "ARCHIVED", "ar", {}, "📦 В архиве"))
    LOST = [("1", "💸 Дорого для клиента"), ("2", "🤝 Выбрали другого"), ("3", "🔇 Клиент пропал"), ("4", "🚫 Проект отменён"), ("5", "❓ Другое")]
    routes.append([answer(220, "Причина?", name="❌ Lost → причины", conds=[act("ls")]),
                   tg(221, "sendMessage", [("chat_id", OWNER), ("text", "❌ " + LEADK + ": почему проиграли?"),
                      ("reply_markup", KB([[{"text": t, "callback_data": "lr|" + LEADK + "|" + k}] for k, t in LOST]))])])
    LRS = "switch(3.r; " + "; ".join(f'"{k}"; "{t}"' for k, t in LOST) + '; "Другое")'
    routes.append([ds_get(230, S_LEADS, LEADK, name="❌ Lost с причиной", conds=[act("lr")]),
                   ds_upd(231, S_LEADS, LEADK, {"status": "LOST", "lost_reason": "{{" + LRS + "}}", "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False),
                   dec(232, "LOST", "{{" + LRS + "}}"),
                   ev(233, LEADK, "OWNER_LOST", "{{" + LRS + "}}", old="{{230.status}}", new="LOST"),
                   answer(234, "Lost"),
                   tg(235, "editMessageReplyMarkup", [("chat_id", OWNER), ("message_id", "{{3.mid}}"),
                      ("reply_markup", KB([[{"text": "❌ Lost — причина сохранена", "callback_data": "z"}]]))])])
    # /won LEAD СУММА — исправление суммы сделки
    routes.append([setvars(250, [("wl", '{{get(split(3.txt; " "); 2)}}'), ("wa", '{{replace(get(split(3.txt; " "); 3); ","; ".")}}')],
                           name="/won", conds=[cmd("/won")]),
                   ds_get(251, S_LEADS, "{{ifempty(250.wl; \"-\")}}"),
                   router(252, [
                       [ds_upd(253, S_LEADS, "{{250.wl}}", {"status": "WON", "deal_amount_eur": "{{250.wa}}", "won_at": "{{ifempty(251.won_at; now)}}",
                                                            "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False,
                               name="Лид есть, сумма — число", conds=[[c("{{251.status}}", "exist"), c("{{250.wa}}", "text:pattern", NUM_RE)]]),
                        ev(254, "{{250.wl}}", "DEAL_AMOUNT_SET", "owner /won {{250.wa}} EUR", old="{{251.status}}", new="WON"),
                        tg(255, "sendMessage", [("chat_id", OWNER), ("text", "🏆 {{250.wl}}: сумма сделки {{250.wa}} € сохранена (WON).")])],
                       [tg(256, "sendMessage", [("chat_id", OWNER), ("text", "Формат: /won LH-YYYYMMDD-xxxxxx 1500 (лид не найден или сумма не число).")],
                           name="Ошибка формата", conds=[[c("{{251.status}}", "notexist")], [c("{{250.wa}}", "text:notpattern", NUM_RE)]])]])])
    routes.append([answer(130, "", name="Служебная кнопка", conds=[act("z")])])
    routes.append([answer(131, "Эта кнопка из старой системы и больше не используется.", name="Неизвестная кнопка",
                          conds=[CB + [c("{{3.a}}", "text:notequal", a) for a in ("ap", "rj", "rr", "ma", "z", "ft", "of", "cm", "qs", "mx", "ct", "wn", "ls", "lr", "ar")]])])
    flow = [hook(1, HOOK20), ds_get(2, S_SET, "main"), v, router(4, routes, 600, 0)]
    return {"name": "LH-20 Lead Hunter — Telegram Owner Panel", "metadata": {"version": 1, "instant": True}, "flow": flow}


# ================= LH-03: Manual Intake =================
def lh03():
    T = "1.text"
    url_in_text = ('if(contains(' + T + '; "http"); replace(' + T + '; "/^[\\s\\S]*?(https?:\\/\\/[^\\s<>)\\]]+)[\\s\\S]*$/"; "$1"); "")')
    chan = ('if(1.fwd_chat_username; "https://t.me/" + 1.fwd_chat_username + "/" + 1.fwd_message_id; "")')
    v3 = setvars(3, [
        ("raw", "{{trim(" + T + ")}}"),
        # T-0020 (решение 1): автоматические источники передают source и source_url; если пусто — как раньше
        ("u", "{{ifempty(1.source_url; ifempty(" + url_in_text + "; ifempty(first(split(1.text_links; \" \")); " + chan + ")))}}"),
        ("source", '{{ifempty(1.source; if(1.fwd_chat_username; "telegram:@" + 1.fwd_chat_username; if(1.fwd_type = "channel"; "telegram:" + 1.fwd_chat_title; "manual")))}}'),
        ("client_hint", "{{lower(ifempty(1.fwd_user_username; ifempty(1.fwd_chat_username; ifempty(1.fwd_user_name; \"\"))))}}"),
        ("published_at", '{{if(1.fwd_date; parseDate(1.fwd_date; "X"); "")}}'),
    ], name="Внутренний токен", conds=[[c("{{1.token}}", "text:equal", "{{2.internal_token}}")]])
    U = "3.u"
    clean = ('replace(replace(replace(replace(replace(' + U + '; "/#.*$/"; ""); '
             '"/([?&])(utm_[^=&]*|fbclid|gclid|yclid|igsh|igshid|mibextid|si|ref|ref_src)=[^&]*/g"; "$1"); "/&&+/g"; "&"); "/\\?&/"; "?"); "/[?&]+$/"; "")')
    host = 'lower(replace(' + clean + '; "/^https?:\\/\\/(www\\.)?([^\\/?#]+).*$/i"; "$2"))'
    rest = 'replace(replace(' + clean + '; "/^https?:\\/\\/(www\\.)?[^\\/?#]+/i"; ""); "/\\/$/"; "")'
    v4 = setvars(4, [
        ("url", '{{if(' + U + '; "https://" + ' + host + ' + ' + rest + '; "")}}'),
        ("text_norm", '{{lower(trim(replace(replace(3.raw; "/https?:\\/\\/\\S+/g"; ""); "/\\s+/g"; " ")))}}'),
        ("title", '{{substring(trim(replace(3.raw; "/\\n[\\s\\S]*$/"; "")); 0; 120)}}'),
    ])
    v5 = setvars(5, [
        ("text_hash", "{{sha256(4.text_norm)}}"),
        ("url_hash", '{{if(4.url; sha256(4.url); "nourl-" + sha256(4.text_norm))}}'),
        ("lead_id", '{{"LH-" + formatDate(now; "YYYYMMDD"; 2.timezone) + "-" + substring(sha256(4.text_norm + "|" + 4.url); 0; 6)}}'),
        ("title_key", '{{substring(lower(replace(4.title; "/[\\s.,:;!?()\\[\\]«»\\-–—_*#]+/g"; "")); 0; 40)}}'),
        ("client_key", '{{if(3.client_hint; 3.client_hint; "noclient-" + sha256(4.text_norm))}}'),
        ("source", '{{if(3.source = "manual"; if(4.url; replace(4.url; "/^https:\\/\\/([^\\/]+).*$/"; "$1"); "manual"); 3.source)}}'),
    ])
    s6 = ds_search(6, S_LEADS, [[c("url_hash", "text:equal", "{{5.url_hash}}")],
                                [c("text_hash", "text:equal", "{{5.text_hash}}")],
                                [c("client_hint", "text:equal", "{{5.client_key}}"), c("title_key", "text:equal", "{{5.title_key}}")]], limit=1)
    AT = '{{formatDate(now; "YYYY-MM-DD HH:mm"; ifempty(2.timezone; "Europe/Berlin"))}}'
    # в duplicates и в событии — сырой входящий URL (до очистки) + время
    dup = [ds_upd(10, S_LEADS, "{{6.key}}", {"duplicates": '{{if(6.data.duplicates; 6.data.duplicates + " | "; "")}}{{ifempty(3.u; "text:" + 5.lead_id)}} @ ' + AT,
                                             "updated_at": "{{now}}"}, upsert=False, name="Дубликат", conds=[[c("{{6.key}}", "exist")]]),
           ev(11, "{{6.key}}", "DUPLICATE_DETECTED", 'existing={{6.key}} incoming_url={{ifempty(3.u; "none")}} at=' + AT),
           tg(12, "sendMessage", [("chat_id", OWNER), ("text", "♻️ Дубликат: эта заявка уже есть — {{6.key}} ({{ifempty(6.data.grade; 6.data.status)}} {{6.data.score}}).\nНовый лид не создан, ссылка добавлена в duplicates.")])]
    new = [ds_add(20, S_LEADS, "{{5.lead_id}}", {
               "lead_id": "{{5.lead_id}}", "kind": "lead", "title": "{{4.title}}", "title_key": "{{5.title_key}}",
               "description_original": "{{3.raw}}", "source": "{{5.source}}", "source_url": "{{4.url}}",
               "url_hash": "{{5.url_hash}}", "text_hash": "{{5.text_hash}}", "client_hint": "{{5.client_key}}",
               "published_at": "{{3.published_at}}", "found_at": "{{now}}", "status": "NEW", "status_at": "{{now}}",
               "attempts": 0, "duplicates": "", "created_at": "{{now}}", "updated_at": "{{now}}", "day": DAY_S},
               name="Новый лид", conds=[[c("{{6.key}}", "notexist")]]),
           ev(21, "{{5.lead_id}}", "LEAD_CREATED", "source={{5.source}} url={{ifempty(4.url; \"none\")}}", new="NEW"),
           router(22, [
               [tg(23, "sendMessage", [("chat_id", OWNER), ("text", "⏸ Пауза: {{5.lead_id}} сохранён в очередь (NEW). Разберу после /resume.")],
                   name="Пауза", conds=[[c("{{2.paused}}", "text:equal", "true")]])],
               [tg(24, "sendMessage", [("chat_id", OWNER), ("text", "📥 {{5.lead_id}} создан{{if(4.url; \"\"; \" (без ссылки — не выше COLD)\")}}. Analyst оценивает…")],
                   name="Работаем", conds=[[c("{{2.paused}}", "text:notequal", "true")]]),
                http_form(25, URL10, [("token", "{{2.internal_token}}"), ("lead_id", "{{5.lead_id}}")])]])]
    # неверный internal token → событие SECURITY_DENIED (сам токен не пишется)
    denied = [ev(31, "", "SECURITY_DENIED", 'LH-03: неверный internal token (token_present={{if(1.token; "yes"; "no")}})',
                 name="Неверный токен", conds=[[c("{{1.token}}", "text:notequal", "{{2.internal_token}}")]])]
    flow = [hook(1, HOOK03), ds_get(2, S_SET, "main"),
            router(30, [denied, [v3, v4, v5, s6, router(7, [dup, new], 1500, 0)]], 300, 0)]
    return {"name": "LH-03 Lead Hunter — Manual Intake", "metadata": {"version": 1, "instant": True}, "flow": flow}


# ================= LH-10: Lead Pipeline (Analyst) =================
def lh10():
    L = "1.lead_id"
    lead_block = ('LEAD (JSON fields, description separately):\n'
                  '{"lead_id":"{{3.lead_id}}","title":"{{3.title}}","source":"{{3.source}}",'
                  '"source_url":"{{ifempty(3.source_url; "null")}}",'
                  '"client_hint":"{{if(contains(3.client_hint; "noclient-"); "null"; 3.client_hint)}}"}\n'
                  '<description_original>\n{{3.description_original}}\n</description_original>\n'
                  'Return ONLY the JSON object for lead_id {{3.lead_id}}.')
    claude = m(9, "anthropic-claude:simpleTextPrompt", 1,
               {"model": "claude-haiku-4-5", "textPrompt": PROMPT + "\n\n" + lead_block, "max_tokens": "{{ifempty(2.analyst_max_tokens; 1500)}}"},
               onerror=[{"id": 509, "module": "builtin:Resume", "version": 1, "metadata": meta(0, 0),
                         "mapper": {"result": "", "stop_reason": "error", "usage": {"input_tokens": 0, "output_tokens": 0}}}])
    parse = m(10, "json:ParseJSON", 1, {"json": '{{trim(replace(replace(9.result; "/^\\s*```(json)?/"; ""); "/```\\s*$/"; ""))}}'},
              {"type": DS_ANALYSIS},
              onerror=[{"id": 510, "module": "builtin:Resume", "version": 1, "metadata": meta(0, 0), "mapper": {"lead_id": ""}}])
    PAT = "^(10(\\.0+)?|[0-9](\\.[0-9]+)?)$"
    valid_conds = [c("{{10.lead_id}}", "text:equal", "{{" + L + "}}"), c("{{10.kind}}", "text:pattern", "^(lead|prospect)$")] + \
                  [c("{{10.scores." + k + "}}", "text:pattern", PAT) for k in KEYS]
    invalid_groups = [[c("{{10.lead_id}}", "text:notequal", "{{" + L + "}}")], [c("{{10.kind}}", "text:notpattern", "^(lead|prospect)$")]] + \
                     [[c("{{10.scores." + k + "}}", "text:notpattern", PAT)] for k in KEYS]
    num = lambda k: "parseNumber(10.scores." + k + '; ".")'
    # текст для JSON-строки без экранирования: \ и " → ', переводы строк/пробелы → один пробел
    esc = lambda x: 'replace(replace(ifempty(' + x + '; ""); "/[\\\\\\x22]/g"; "\'"); "/\\s+/g"; " ")'
    ATT = "ifempty(3.attempts; 0) + 1"   # номер текущей попытки (3 = запись лида до инкремента в модуле 7)
    raw = "round(10 * (" + " + ".join(f"2.w_{k} * {num(k)}" for k in KEYS) + "))"
    cur = 'upper(ifempty(10.budget.currency; ""))'
    rate = ('switch(' + cur + '; "EUR"; 1; "USD"; 2.fx_usd; "GBP"; 2.fx_gbp; "CHF"; 2.fx_chf; "PLN"; 2.fx_pln; '
            '"UAH"; 2.fx_uah; "CAD"; 2.fx_cad; "AUD"; 2.fx_aud; "INR"; 2.fx_inr; "RUB"; 2.fx_rub; "")')
    cost = ("ifempty(9.usage.input_tokens; 0) * ifempty(2.analyst_price_in_mtok; 1) / 1000000 + "
            "ifempty(9.usage.output_tokens; 0) * ifempty(2.analyst_price_out_mtok; 5) / 1000000")
    v12 = setvars(12, [("raw", "{{" + raw + "}}"),
                       ("beur", '{{if(10.budget.amount; if(' + rate + '; round(10.budget.amount * ' + rate + '; 2); ""); "")}}'),
                       ("cost", "{{" + cost + "}}"),
                       ("flags", '{{join(10.risk_flags; ", ")}}')],
                  name="JSON валиден", conds=[valid_conds])
    capreason = ('{{if(3.source_url; ""; "нет source_url — не выше COLD (59); ")}}'
                 '{{if(12.flags; "risk_flags: " + 12.flags + " — не выше 39; "; "")}}'
                 '{{if(12.beur; if(12.beur < 2.minimum_order_eur; "бюджет ≈ " + 12.beur + " € < " + 2.minimum_order_eur + " € — не выше 59; "; ""); "")}}'
                 '{{if(10.kind = "prospect"; "prospect — не выше 59; "; "")}}')
    score = ('min(12.raw; if(3.source_url; 100; 59); if(12.flags; 39; 100); '
             'if(12.beur; if(12.beur < 2.minimum_order_eur; 59; 100); 100); if(10.kind = "prospect"; 59; 100))')
    v13 = setvars(13, [("score", "{{" + score + "}}"), ("cap_reason", capreason)])
    grade = ('if(13.score >= 2.hot_threshold; "HOT"; if(13.score >= 2.warm_threshold; "WARM"; '
             'if(13.score >= 2.cold_threshold; "COLD"; "REJECT")))')
    v14 = setvars(14, [("grade", "{{" + grade + "}}")])
    EMO = 'switch(14.grade; "HOT"; "🔥"; "WARM"; "🌤"; "COLD"; "❄️"; "⛔")'
    card = ("{{" + EMO + "}} {{14.grade}} · {{13.score}}/100\n"
            "📌 {{3.title}}\n"
            "🌍 {{ifempty(10.country; \"страна неизвестна\")}} · 🌐 {{ifempty(10.language; \"?\")}} · 📍 {{3.source}}\n"
            "💰 Бюджет: {{if(10.budget.amount; 10.budget.amount + \" \" + 10.budget.currency + if(12.beur; \" ≈ \" + 12.beur + \" EUR\"; \" (курс не задан)\"); \"не указан\")}}\n"
            "🎯 Тип: {{ifempty(10.bot_type; \"unknown\")}} · {{10.kind}}\n"
            "🧠 Суть: {{10.description_ru}}\n\n"
            "📊 Оценка:\n" +
            "".join(f"{LABEL[k]}: {{{{10.scores.{k}}}}}/10 — {{{{10.reasons.{k}}}}}\n" for k in KEYS) +
            "\n{{if(12.flags; \"⚠️ Risk: \" + 12.flags + newline; \"\")}}"
            "{{if(13.cap_reason; \"🧮 Ограничение: \" + 13.cap_reason + newline; \"\")}}"
            "🔗 Original: {{ifempty(3.source_url; \"нет ссылки\")}}\n"
            "{{if(" + write_url("3") + "; \"\"; \"" + NO_CONTACT + "\" + newline)}}"
            "🆔 {{1.lead_id}}")
    # COLD/REJECT — одна строка; причина = ограничение (cap) или критерий с наименьшим баллом
    part = lambda k: ('if(' + num(k) + ' < 10; "0"; "") + toString(10.scores.' + k + ') + "|' + LABEL[k] + ' " + '
                      'toString(10.scores.' + k + ') + "/10: " + 20.r_' + k)
    lowest = ('replace(first(sort(split(' + ' + "§" + '.join(part(k) for k in KEYS) + '; "§"))); "/^[0-9.]+\\|/"; "")')
    short = ("{{" + EMO + "}} {{1.lead_id}} · {{14.grade}} {{13.score}} — в архиве, причина: "
             "{{if(13.cap_reason; replace(13.cap_reason; \"/;\\s*$/\"; \"\"); " + lowest + ")}}")
    v20 = setvars(20, [("r_" + k, "{{" + esc("10.reasons." + k) + "}}") for k in KEYS])  # причины без " и \\, в одну строку
    # T-0021: wurl только для HOT/WARM (COLD/REJECT — короткая строка без кнопки)
    v25 = setvars(25, [("full", card), ("short", short),
                       ("wurl", '{{if(14.grade = "HOT"; ' + write_url("3") + '; if(14.grade = "WARM"; ' + write_url("3") + '; ""))}}')])
    BTN_ROWS = [[{"text": "✅ Approve", "callback_data": "ap|{{1.lead_id}}"}, {"text": "❌ Reject", "callback_data": "rj|{{1.lead_id}}"}],
                [{"text": "🔍 More analysis", "callback_data": "ma|{{1.lead_id}}"}]]
    v15 = setvars(15, [("card", '{{if(14.grade = "HOT"; 25.full; if(14.grade = "WARM"; 25.full; 25.short))}}'), ("next",'{{if(14.grade = "HOT"; "SENT_TO_TELEGRAM"; if(14.grade = "WARM"; "SENT_TO_TELEGRAM"; "ARCHIVED"))}}'),
                       ("kb1", KB([WRITE_BTN("25.wurl")] + BTN_ROWS)), ("kb0", KB(BTN_ROWS))])
    scores_json = "{" + ",".join(f'"{k}":{{{{{num(k)}}}}}' for k in KEYS) + "}"
    # reasons — только объект reasons из разобранного JSON, минифицированный (кавычки/\ → ', пробелы схлопнуты)
    reasons_json = "{" + ",".join(f'"{k}":"{{{{20.r_{k}}}}}"' for k in KEYS) + "}"
    save = ds_upd(16, S_LEADS, "{{1.lead_id}}", {
        "kind": "{{10.kind}}", "language": "{{10.language}}", "bot_type": "{{10.bot_type}}", "description_ru": "{{10.description_ru}}",
        "client_name": "{{10.client_name}}", "country": "{{10.country}}", "budget_amount": "{{10.budget.amount}}",
        "budget_currency": "{{10.budget.currency}}", "budget_type": "{{10.budget.type}}", "budget_eur": "{{12.beur}}",
        "scores": scores_json, "reasons": reasons_json, "score_raw": "{{12.raw}}", "score": "{{13.score}}",
        "score_cap_reason": "{{13.cap_reason}}", "grade": "{{14.grade}}", "risk_flags": "{{12.flags}}",
        "duplicate_of": "{{10.duplicate_of}}", "card_text": "{{15.card}}", "status": "ANALYZED", "status_at": "{{now}}",
        "error_code": "", "error_message": "", "updated_at": "{{now}}"}, upsert=False)
    run_ok = ds_add(17, S_LOG, "{{uuid}}", {"table": "runs", "run_id": "{{uuid}}", "lead_id": "{{1.lead_id}}", "agent": "analyst",
                    "model": "{{ifempty(9.model; \"claude-haiku-4-5\")}}", "started_at": "{{7.updated_at}}", "finished_at": "{{now}}",
                    "input_tokens": "{{9.usage.input_tokens}}", "output_tokens": "{{9.usage.output_tokens}}",
                    "estimated_cost_usd": "{{12.cost}}", "status": "OK", "attempt": "{{" + ATT + "}}", "prompt_version": PROMPT_VERSION, "created_at": "{{now}}", "day": DAY_S})
    day_cost = ds_upd(18, S_SET, "day_" + DAY_S, {"day": DAY_S, "cost_usd": "{{ifempty(5.cost_usd; 0) + 12.cost}}"})
    e1 = ev(19, "{{1.lead_id}}", "ANALYST_COMPLETED", "tokens in/out {{9.usage.input_tokens}}/{{9.usage.output_tokens}}, ${{12.cost}}", old="NEW", new="ANALYZED")
    e2 = ev(26, "{{1.lead_id}}", "SCORE_CALCULATED", "raw {{12.raw}} → {{13.score}} {{14.grade}}; {{13.cap_reason}}")
    BTN = "{{if(25.wurl; 15.kb1; 15.kb0)}}"
    send = tg(27, "sendMessage", [("chat_id", OWNER), ("text", "{{15.card}}"), ("reply_markup", BTN)], onerror=False)
    send["onerror"] = [ds_upd(527, S_LEADS, "{{1.lead_id}}", {"status": "ERROR", "error_code": "TELEGRAM_SEND",
                              "error_message": "sendMessage failed", "status_at": "{{now}}"}, upsert=False),
                       {"id": 627, "module": "builtin:Ignore", "version": 1, "mapper": None, "metadata": meta(0, 0)}]
    sent = ds_upd(28, S_LEADS, "{{1.lead_id}}", {"status": "{{15.next}}", "tg_message_id": "{{27.body.result.message_id}}", "status_at": "{{now}}"}, upsert=False)
    e3 = ev(29, "{{1.lead_id}}", "TELEGRAM_SENT", "message {{27.body.result.message_id}}", old="ANALYZED", new="{{15.next}}")
    spent = "(ifempty(5.cost_usd; 0) + 12.cost)"
    budget_r = router(30, [
        [ds_upd(31, S_SET, "main", {"warned_80": DAY_S}, name="80 % бюджета",
                conds=[[c("{{" + spent + "}}", "number:greaterorequal", "{{2.daily_budget_usd * 0.8}}"),
                        c("{{" + spent + "}}", "number:less", "{{2.daily_budget_usd}}"),
                        c("{{2.warned_80}}", "text:notequal", DAY_S)]]),
         tg(32, "sendMessage", [("chat_id", OWNER), ("text", "⚠️ Израсходовано 80 % дневного бюджета Claude: ${{formatNumber(" + spent + "; 4; \".\"; \"\")}} из ${{2.daily_budget_usd}}.")])],
        [ds_upd(33, S_SET, "main", {"paused": True, "paused_reason": "дневной бюджет исчерпан", "updated_at": "{{now}}"},
                name="100 % бюджета", conds=[[c("{{" + spent + "}}", "number:greaterorequal", "{{2.daily_budget_usd}}")]]),
         ev(34, "", "BUDGET_PAUSED", "spent ${{" + spent + "}}"),
         tg(35, "sendMessage", [("chat_id", OWNER), ("text", "⛔ Дневной бюджет Claude исчерпан (${{2.daily_budget_usd}}). AI-обработка на паузе, новые заявки копятся в очереди. /resume — продолжить.")])]])
    valid_flow = [v12, v13, v14, v20, v25, v15, save, run_ok, day_cost, e1, e2, send, sent, e3, budget_r]
    # --- невалидный ответ: повтор или ERROR
    attempts = ATT
    run_bad = ds_add(40, S_LOG, "{{uuid}}", {"table": "runs", "run_id": "{{uuid}}", "lead_id": "{{1.lead_id}}", "agent": "analyst",
                     "model": "claude-haiku-4-5", "started_at": "{{7.updated_at}}", "finished_at": "{{now}}",
                     "input_tokens": "{{ifempty(9.usage.input_tokens; 0)}}", "output_tokens": "{{ifempty(9.usage.output_tokens; 0)}}",
                     "estimated_cost_usd": "{{" + cost + "}}", "status": "FAILED",
                     "error_code": '{{if(9.stop_reason = "error"; "MODEL_ERROR"; if(9.stop_reason = "refusal"; "REFUSAL"; "JSON_INVALID"))}}',
                     "error_message": "{{substring(ifempty(9.result; \"(empty)\"); 0; 300)}}", "attempt": "{{" + attempts + "}}",
                     "prompt_version": PROMPT_VERSION,
                     "created_at": "{{now}}", "day": DAY_S},
                     name="JSON невалиден", conds=invalid_groups)
    day_cost2 = ds_upd(41, S_SET, "day_" + DAY_S, {"day": DAY_S, "cost_usd": "{{ifempty(5.cost_usd; 0) + " + cost + "}}"})
    delay = "min(300; parseNumber(ifempty(get(split(2.retry_delays; \",\"); " + attempts + "); \"1\"); \".\") * 60)"
    retry_r = router(42, [
        [ev(43, "{{1.lead_id}}", "ANALYST_RETRY", "attempt {{" + attempts + "}} failed, retry in {{" + delay + "}} s",
            name="Повтор", conds=[[c("{{" + attempts + "}}", "number:less", "{{ifempty(2.max_retry_attempts; 3)}}")]]),
         m(44, "util:FunctionSleep", 1, {"duration": "{{" + delay + "}}"}),
         http_form(45, URL10, [("token", "{{2.internal_token}}"), ("lead_id", "{{1.lead_id}}")])],
        [ds_upd(46, S_LEADS, "{{1.lead_id}}", {"status": "ERROR", "status_at": "{{now}}", "error_code": "ANALYST_FAILED",
                "error_message": "{{substring(ifempty(9.result; ifempty(9.stop_reason; \"empty\")); 0; 300)}}", "updated_at": "{{now}}"},
                upsert=False, name="Попытки исчерпаны",
                conds=[[c("{{" + attempts + "}}", "number:greaterorequal", "{{ifempty(2.max_retry_attempts; 3)}}")]]),
         ev(47, "{{1.lead_id}}", "ERROR", "Analyst failed after {{" + attempts + "}} attempts", old="NEW", new="ERROR"),
         tg(48, "sendMessage", [("chat_id", OWNER), ("text", "⚠️ {{1.lead_id}}: Analyst не дал корректный ответ после {{" + attempts + "}} попыток. Лид сохранён со статусом ERROR, заявка не потеряна.")])]])
    invalid_flow = [run_bad, day_cost2, retry_r]
    process = [ds_upd(7, S_LEADS, "{{1.lead_id}}", {"attempts": "{{ifempty(3.attempts; 0) + 1}}", "updated_at": "{{now}}"}, upsert=False,
                      name="Обработка: NEW, без паузы, бюджет есть",
                      conds=[[c("{{3.status}}", "text:equal", "NEW"), c("{{2.paused}}", "text:notequal", "true"),
                              c("{{ifempty(5.cost_usd; 0)}}", "number:less", "{{2.daily_budget_usd}}")]]),
               ev(8, "{{1.lead_id}}", "ANALYST_STARTED", "attempt {{" + ATT + "}} · prompt " + PROMPT_VERSION),
               claude, parse, router(11, [valid_flow, invalid_flow], 2400, 0)]
    over = [ds_upd(50, S_SET, "main", {"paused": True, "paused_reason": "дневной бюджет исчерпан", "updated_at": "{{now}}"},
                   name="Бюджет исчерпан до вызова",
                   conds=[[c("{{3.status}}", "text:equal", "NEW"), c("{{2.paused}}", "text:notequal", "true"),
                           c("{{ifempty(5.cost_usd; 0)}}", "number:greaterorequal", "{{2.daily_budget_usd}}")]]),
            tg(51, "sendMessage", [("chat_id", OWNER), ("text", "⛔ Дневной бюджет Claude исчерпан — {{1.lead_id}} ждёт в очереди. /resume — продолжить.")])]
    flow = [hook(1, HOOK10), ds_get(2, S_SET, "main"),
            ds_get(3, S_LEADS, "{{1.lead_id}}", name="Внутренний токен", conds=[[c("{{1.token}}", "text:equal", "{{2.internal_token}}")]]),
            ds_upd(4, S_SET, "day_" + DAY_S, {"day": DAY_S}), ds_get(5, S_SET, "day_" + DAY_S),
            router(6, [process, over], 900, 0)]
    return {"name": "LH-10 Lead Hunter — Lead Pipeline (Analyst)", "metadata": {"version": 1, "instant": True}, "flow": flow}


# ================= LH-11: Architect + Sales (этап 3) =================
NUM_RE = "^[0-9]+(\\.[0-9]+)?$"
NEG = {"text:equal": "text:notequal", "text:notequal": "text:equal", "text:pattern": "text:notpattern",
       "number:lessorequal": "number:greater", "number:greater": "number:lessorequal", "number:less": "number:greaterorequal",
       "number:greaterorequal": "number:less", "exist": "notexist"}
def negate_each(conds): return [[dict(x, o=NEG[x["o"]])] for x in conds]
def clean_json(ref):  # снять ```-обёртку и минифицировать (переводы строк вне строк JSON)
    return ('{{replace(trim(replace(replace(' + ref + '; "/^\\s*```(json)?/"; ""); "/```\\s*$/"; "")); "/\\n\\s*/g"; "")}}')
def resume(mid, mapper): return [{"id": mid, "module": "builtin:Resume", "version": 1, "metadata": meta(0, 0), "mapper": mapper}]
LH11_KB = lambda L, extra=(): KB(list(extra) + [[{"text": "📋 Full ТЗ", "callback_data": "ft|" + L}, {"text": "💰 Offer", "callback_data": "of|" + L}],
                        [{"text": "💬 Client Message", "callback_data": "cm|" + L}, {"text": "❓ Questions", "callback_data": "qs|" + L}],
                        [{"text": "🔍 More Analysis", "callback_data": "mx|" + L}, {"text": "📞 Contacted", "callback_data": "ct|" + L}],
                        [{"text": "🏆 Won", "callback_data": "wn|" + L}, {"text": "❌ Lost", "callback_data": "ls|" + L},
                         {"text": "📦 Archive", "callback_data": "ar|" + L}]])
# D3: после прогона не перетирать финальные/ручные статусы владельца (нажал во время More Analysis)
PROT = lambda r: 'switch(' + r + '.status; "WON"; 1; "LOST"; 1; "ARCHIVED"; 1; "CONTACTED"; 1; 0)'
KEEP = lambda r, new: '{{if(' + PROT(r) + ' = 1; ' + r + '.status; "' + new + '")}}'
KEEP_AT = lambda r: '{{if(' + PROT(r) + ' = 1; ' + r + '.status_at; now)}}'
RETRY_KB = lambda L: KB([[{"text": "🔁 Повторить Architect + Sales", "callback_data": "ap|" + L}]])

def lh11():
    L = "{{1.lead_id}}"
    TOK = [c("{{1.token}}", "text:equal", "{{2.internal_token}}")]
    PIN, POUT = "ifempty(2.sonnet_price_in_mtok; 2)", "ifempty(2.sonnet_price_out_mtok; 10)"
    cost = lambda m: ("if(" + m + ".usage.input_tokens; " + m + ".usage.input_tokens * " + PIN + " / 1000000 + "
                      "ifempty(" + m + ".usage.output_tokens; 0) * " + POUT + " / 1000000; 0)")
    budget_txt = ('{{if(8.budget_amount; 8.budget_amount + " " + 8.budget_currency + " (" + ifempty(8.budget_type; "unknown") + ")"; "not stated")}}')
    lead_block = ('LEAD (approved by the owner; analyst summary + original text):\n'
                  '{"lead_id":"{{1.lead_id}}","title":"{{8.title}}","source":"{{8.source}}","source_url":"{{ifempty(8.source_url; "null")}}",'
                  '"language":"{{ifempty(8.language; "unknown")}}","country":"{{ifempty(8.country; "unknown")}}","bot_type":"{{ifempty(8.bot_type; "unknown")}}",'
                  '"kind":"{{8.kind}}","client_budget_from_lead":"' + budget_txt + '","analyst_grade":"{{8.grade}}","analyst_score":"{{8.score}}"}\n'
                  '<description_ru>\n{{8.description_ru}}\n</description_ru>\n'
                  '<description_original>\n{{8.description_original}}\n</description_original>\n')
    deep_a = ('{{if(1.mode = "more"; "DEEP ANALYSIS MODE (owner pressed More Analysis; the only allowed re-run for this lead): '
              're-check every item of PREVIOUS_ANALYSIS against the lead text, expand technical_risks and missing_information, '
              'make questions_for_client sharper and strictly prioritized, refine the hour range. Same output format. PREVIOUS_ANALYSIS: "; "")}}'
              '{{if(1.mode = "more"; 8.architect_json; "")}}\n')
    deep_s = ('{{if(1.mode = "more"; "DEEP ANALYSIS MODE: the spec was refined; re-check prices, packages and win probability. PREVIOUS_OFFER: "; "")}}'
              '{{if(1.mode = "more"; 8.sales_json; "")}}\n')
    # ---------- Architect
    started = ev(12, L, "ARCHITECT_STARTED", "run {{1.run_id}} · mode {{ifempty(1.mode; \"normal\")}} · prompt " + ARCH_VERSION, old="{{8.status}}", new="{{8.status}}")
    t0 = setvars(13, [("t0", "{{now}}")])
    arch = m(14, "anthropic-claude:simpleTextPrompt", 1,
             {"model": "claude-sonnet-5-5", "textPrompt": ARCH_PROMPT + "\n\n" + lead_block + deep_a +
              "Return ONLY the minified JSON object for lead_id {{1.lead_id}}.",
              "max_tokens": "{{ifempty(2.architect_max_tokens; 8000)}}"},
             onerror=resume(514, {"result": "", "stop_reason": "error", "usage": {"input_tokens": 0, "output_tokens": 0}}))
    aj = setvars(15, [("aj", clean_json("14.result")), ("acost", "{{" + cost("14") + "}}")])  # стоимость считается один раз
    pa = m(16, "json:ParseJSON", 1, {"json": "{{15.aj}}"}, {"type": DS_ARCH}, onerror=resume(516, {"lead_id": ""}))
    A = "16."
    va = [c("{{16.lead_id}}", "text:equal", "{{1.lead_id}}"), c("{{16.complexity}}", "text:pattern", "^(S|M|L|XL)$"),
          c("{{16.estimated_hours_min}}", "text:pattern", NUM_RE), c("{{16.estimated_hours_max}}", "text:pattern", NUM_RE),
          c("{{16.estimated_hours_min}}", "number:lessorequal", "{{16.estimated_hours_max}}"),
          c("{{14.stop_reason}}", "text:notequal", "max_tokens"), c("{{16.project_summary}}", "exist"),
          c("{{16.telegram_solution.bot}}", "exist"), c("{{16.database.required}}", "exist"), c("{{16.admin_panel.required}}", "exist")] + \
         [c("{{length(16." + k + ")}}", "number:greater", "0") for k in ("functional_requirements", "mvp", "technology_stack", "questions_for_client")]
    acost = "15.acost"
    a_vars = setvars(18, [("acost", "{{15.acost}}"),
                          ("q", '{{"• " + join(slice(16.questions_for_client; 0; 10); newline + "• ")}}'),
                          ("miss", '{{if(length(16.missing_information) > 0; "• " + join(16.missing_information; newline + "• "); "")}}')],
                     name="ТЗ валидно", conds=[va])
    a_save = ds_upd(19, S_LEADS, L, {"architect_json": "{{15.aj}}", "complexity": "{{16.complexity}}",
                    "estimated_hours_min": "{{16.estimated_hours_min}}", "estimated_hours_max": "{{16.estimated_hours_max}}",
                    "missing_information": "{{18.miss}}", "client_questions": "{{18.q}}", "status": KEEP("55", "TECHNICAL_SPEC_READY"),
                    "status_at": KEEP_AT("55"), "error_code": "", "error_message": "", "updated_at": "{{now}}"}, upsert=False)
    a_reread = ds_get(55, S_LEADS, L)  # D3: актуальный статус перед записью
    run = lambda mid, agent, mod, t_start, status, costx, version, err=None, **kw: ds_add(mid, S_LOG, "{{uuid}}", dict({
        "table": "runs", "run_id": "{{1.run_id}}", "lead_id": L, "agent": agent,
        "model": "{{ifempty(" + mod + ".model; \"claude-sonnet-5-5\")}}", "started_at": t_start, "finished_at": "{{now}}",
        "input_tokens": "{{" + mod + ".usage.input_tokens}}", "output_tokens": "{{" + mod + ".usage.output_tokens}}",
        "estimated_cost_usd": "{{" + costx + "}}", "status": status, "attempt": "{{if(1.mode = \"more\"; 2; 1)}}",
        "prompt_version": version, "created_at": "{{now}}", "day": DAY_S}, **(err or {})), **kw)
    a_run = run(20, "architect", "14", "{{13.t0}}", "OK", "18.acost", ARCH_VERSION)
    a_done = ev(21, L, "ARCHITECT_COMPLETED", "complexity {{16.complexity}}, {{16.estimated_hours_min}}-{{16.estimated_hours_max}} h, "
                "tokens {{14.usage.input_tokens}}/{{14.usage.output_tokens}}, ${{18.acost}}", old="{{55.status}}", new=KEEP("55", "TECHNICAL_SPEC_READY"))
    s_start = ev(22, L, "SALES_STARTED", "run {{1.run_id}} · prompt " + SALES_VERSION, old="TECHNICAL_SPEC_READY", new="TECHNICAL_SPEC_READY")
    # ---------- Sales
    settings_block = ('SETTINGS: {"currency":"EUR","minimum_order_eur":{{ifempty(2.minimum_order_eur; 500)}},'
                      '"internal_hourly_rate_eur":"{{ifempty(2.sales_hourly_rate_eur; "UNKNOWN")}}"}\n')
    sales = m(23, "anthropic-claude:simpleTextPrompt", 1,
              {"model": "claude-sonnet-5-5", "textPrompt": SALES_PROMPT + "\n\n" + settings_block + lead_block +
               "ARCHITECT_SPEC (JSON):\n{{15.aj}}\n" + deep_s + "Return ONLY the minified JSON object for lead_id {{1.lead_id}}.",
               "max_tokens": "{{ifempty(2.sales_max_tokens; 4000)}}"},
              onerror=resume(523, {"result": "", "stop_reason": "error", "usage": {"input_tokens": 0, "output_tokens": 0}}))
    sj = setvars(24, [("sj", clean_json("23.result")), ("t1", "{{now}}"), ("scost", "{{" + cost("23") + "}}")])
    ps = m(25, "json:ParseJSON", 1, {"json": "{{24.sj}}"}, {"type": DS_SALES}, onerror=resume(525, {"lead_id": ""}))
    P = lambda k: "{{25." + k + "}}"
    prices = ["estimated_cost", "recommended_price", "target_price", "minimum_acceptable_price",
              "packages.basic.price", "packages.professional.price", "packages.premium.price"]
    vs = [c(P("lead_id"), "text:equal", "{{1.lead_id}}")] + [c(P(k), "text:pattern", NUM_RE) for k in prices] + [
          c(P("minimum_acceptable_price"), "number:greaterorequal", "{{ifempty(2.minimum_order_eur; 500)}}"),
          c(P("minimum_acceptable_price"), "number:lessorequal", P("recommended_price")),
          c(P("recommended_price"), "number:lessorequal", P("target_price")),
          c(P("packages.basic.price"), "number:less", P("packages.professional.price")),
          c(P("packages.professional.price"), "number:less", P("packages.premium.price")),
          c(P("win_probability"), "text:pattern", "^(100|[0-9]{1,2})(\\.0+)?$"),
          c(P("commercial_potential"), "text:pattern", "^(LOW|MEDIUM|HIGH)$"),
          c(P("client_message"), "exist"), c(P("client_message_ru"), "exist"),
          c("{{23.stop_reason}}", "text:notequal", "max_tokens")]
    scost = "24.scost"
    s_vars = setvars(27, [("scost", "{{24.scost}}"), ("total", "{{15.acost + 24.scost}}"),
                          ("ups", '{{join(slice(25.upsells; 0; 5); "; ")}}'),
                          ("tin", "{{ifempty(14.usage.input_tokens; 0) + ifempty(23.usage.input_tokens; 0)}}"),
                          ("tout", "{{ifempty(14.usage.output_tokens; 0) + ifempty(23.usage.output_tokens; 0)}}"),
                          ("wurl", "{{" + write_url("8") + "}}")], name="КП валидно", conds=[vs])
    CARD = ("💼 КП готово · {{1.lead_id}}{{if(1.mode = \"more\"; \" · 🔍 углублённый анализ\"; \"\")}}\n"
            "📌 {{8.title}}\n"
            "🎯 Тип: {{ifempty(8.bot_type; \"unknown\")}} · 🌍 {{ifempty(8.country; \"страна неизвестна\")}} · 🌐 {{ifempty(8.language; \"?\")}}\n"
            "💰 Бюджет клиента: {{if(8.budget_amount; 8.budget_amount + \" \" + 8.budget_currency + \" (\" + ifempty(8.budget_type; \"тип ?\") + "
            "if(8.budget_eur; \", ≈ \" + 8.budget_eur + \" EUR\"; \"\") + \"; источник: текст заявки)\"; \"не указан в заявке\")}}\n"
            "📊 Score {{8.score}}/100 · {{8.grade}} · сложность {{16.complexity}} · ⏱ {{16.estimated_hours_min}}–{{16.estimated_hours_max}} ч\n\n"
            "💵 Наша оценка (не бюджет клиента):\n"
            "себестоимость ≈ {{25.estimated_cost}} € · рекомендуем {{25.recommended_price}} € · цель {{25.target_price}} € · минимум {{25.minimum_acceptable_price}} €\n"
            "📦 Basic {{25.packages.basic.price}} € · Professional {{25.packages.professional.price}} € · Premium {{25.packages.premium.price}} €\n"
            "📈 Win {{25.win_probability}}% — {{25.win_probability_reason}}\n"
            "🏦 Потенциал {{25.commercial_potential}} · фаза 2: {{ifempty(25.phase_2_revenue; \"UNKNOWN\")}} · поддержка: {{ifempty(25.maintenance_revenue; \"UNKNOWN\")}}\n"
            "➕ Upsells: {{ifempty(27.ups; \"—\")}}\n\n"
            "📝 ТЗ кратко: {{substring(16.project_summary; 0; 450)}}\n"
            "⚠️ Риски:\n• {{join(slice(16.technical_risks; 0; 3); newline + \"• \")}}\n"
            "❓ Главные вопросы:\n• {{join(slice(16.questions_for_client; 0; 3); newline + \"• \")}}\n\n"
            "✉️ Первое сообщение ({{ifempty(25.client_language; 8.language)}}):\n{{substring(25.client_message; 0; 700)}}\n\n"
            "Клиенту ничего не отправлено. 🆔 {{1.lead_id}}")
    FOOT = ('{{if(27.wurl; "✍️ Написать клиенту — кнопка ниже"; "' + NO_CONTACT + '")}}\n'
            '💵 AI: ${{formatNumber(27.total; 4; "."; "")}}')
    # клавиатура: строка «✍️ Написать клиенту» (wrow) подставляется перед обычными кнопками, только если есть URL
    card = setvars(28, [("card", CARD), ("foot", FOOT), ("wrow", json.dumps(WRITE_BTN("27.wurl"), ensure_ascii=False, separators=(",", ":")) + ",")])
    KB11 = json.loads(LH11_KB(L))["inline_keyboard"]
    KB11_TXT = '{"inline_keyboard":[{{if(27.wurl; 28.wrow; "")}}' + json.dumps(KB11, ensure_ascii=False, separators=(",", ":"))[1:]+ "}"
    s_save = ds_upd(29, S_LEADS, L, {
        "sales_json": "{{24.sj}}", "recommended_price": P("recommended_price"), "target_price": P("target_price"),
        "minimum_acceptable_price": P("minimum_acceptable_price"), "commercial_potential": P("commercial_potential"),
        "win_probability": P("win_probability"), "basic_price": P("packages.basic.price"),
        "professional_price": P("packages.professional.price"), "premium_price": P("packages.premium.price"),
        "client_message": P("client_message"), "client_message_ru": P("client_message_ru"), "upsells": "{{27.ups}}",
        "phase_2_revenue": '{{ifempty(25.phase_2_revenue; "UNKNOWN")}}', "maintenance_revenue": '{{ifempty(25.maintenance_revenue; "UNKNOWN")}}',
        "last_run_tokens_in": "{{27.tin}}", "last_run_tokens_out": "{{27.tout}}", "last_run_cost_usd": "{{27.total}}",  # L1
        "sales_run_id": "{{1.run_id}}", "status": KEEP("56", "COMMERCIAL_READY"), "status_at": KEEP_AT("56"), "updated_at": "{{now}}"}, upsert=False)
    s_reread = ds_get(56, S_LEADS, L)  # D3
    s_run = run(30, "sales", "23", "{{24.t1}}", "OK", "27.scost", SALES_VERSION)
    day_cost = lambda mid, add: ds_upd(mid, S_SET, "day_" + DAY_S, {"day": DAY_S, "cost_usd": "{{ifempty(10.cost_usd; 0) + " + add + "}}"})
    s_done = ev(32, L, "SALES_COMPLETED", "rec {{25.recommended_price}} €, win {{25.win_probability}}%, tokens {{23.usage.input_tokens}}/{{23.usage.output_tokens}}, ${{27.scost}}",
                old="{{56.status}}", new=KEEP("56", "COMMERCIAL_READY"))
    send = tg(33, "sendMessage", [("chat_id", OWNER), ("text", "{{substring(28.card; 0; 3500)}}\n{{28.foot}}"),
                                  ("reply_markup", KB11_TXT)], onerror=False)
    send["onerror"] = [ds_upd(533, S_LEADS, L, {"status": "ERROR", "error_code": "TELEGRAM_SEND", "error_message": "commercial card sendMessage failed",
                              "status_at": "{{now}}"}, upsert=False),
                       ev(633, L, "ERROR", "TELEGRAM_SEND: commercial card not delivered", old="COMMERCIAL_READY", new="ERROR"),
                       {"id": 733, "module": "builtin:Ignore", "version": 1, "mapper": None, "metadata": meta(0, 0)}]
    sent_reread = ds_get(57, S_LEADS, L)  # D3
    sent = ds_upd(34, S_LEADS, L, {"status": KEEP("57", "SENT_TO_TELEGRAM"), "commercial_message_id": "{{33.body.result.message_id}}",
                                   "status_at": KEEP_AT("57")}, upsert=False)
    e_sent = ev(35, L, "COMMERCIAL_SENT_TO_OWNER", "message {{33.body.result.message_id}}{{if(" + PROT("57") + " = 1; \" · статус владельца \" + 57.status + \" сохранён\"; \"\")}}",
                old="{{57.status}}", new=KEEP("57", "SENT_TO_TELEGRAM"))
    spent = "(ifempty(10.cost_usd; 0) + 27.total)"
    budget_r = lambda card_route: router(36, [
        [ds_upd(37, S_SET, "main", {"warned_80": DAY_S}, name="80 % бюджета",
                conds=[[c("{{" + spent + "}}", "number:greaterorequal", "{{2.daily_budget_usd * 0.8}}"),
                        c("{{" + spent + "}}", "number:less", "{{2.daily_budget_usd}}"), c("{{2.warned_80}}", "text:notequal", DAY_S)]]),
         tg(38, "sendMessage", [("chat_id", OWNER), ("text", "⚠️ Израсходовано 80 % дневного бюджета Claude: ${{formatNumber(" + spent + "; 4; \".\"; \"\")}} из ${{2.daily_budget_usd}}.")])],
        [ds_upd(39, S_SET, "main", {"paused": True, "paused_reason": "дневной бюджет исчерпан", "updated_at": "{{now}}"},
                name="100 % бюджета", conds=[[c("{{" + spent + "}}", "number:greaterorequal", "{{2.daily_budget_usd}}")]]),
         ev(40, "", "BUDGET_PAUSED", "spent ${{" + spent + "}}"),
         tg(41, "sendMessage", [("chat_id", OWNER), ("text", "⛔ Дневной бюджет Claude исчерпан (${{2.daily_budget_usd}}). AI-обработка на паузе. /resume — продолжить.")])],
        card_route])
    s_ok = [s_vars, card, s_reread, s_save, s_run, day_cost(31, "27.total"), s_done, budget_r([send, sent_reread, sent, e_sent])]
    s_code = ('{{if(23.stop_reason = "error"; "MODEL_ERROR"; if(23.stop_reason = "max_tokens"; "TRUNCATED"; '
              'if(23.stop_reason = "refusal"; "REFUSAL"; if(25.lead_id; "VALIDATION_FAILED"; "JSON_INVALID"))))}}')
    s_bad = [run(42, "sales", "23", "{{24.t1}}", "FAILED", scost, SALES_VERSION,
                 {"error_code": s_code, "error_message": "{{substring(ifempty(23.result; \"(empty)\"); 0; 300)}}"},
                 name="КП невалидно", conds=negate_each(vs)),
             day_cost(43, "18.acost + " + scost),
             ds_upd(44, S_LEADS, L, {"status": "ERROR", "error_code": "SALES_FAILED", "error_message": s_code,
                    "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False),
             ev(45, L, "SALES_ERROR", s_code + " (run {{1.run_id}})", old="TECHNICAL_SPEC_READY", new="ERROR"),
             tg(46, "sendMessage", [("chat_id", OWNER), ("text", "⚠️ {{1.lead_id}}: Sales не дал корректное КП (" + s_code + "). ТЗ сохранено, статус ERROR. "
                                     "Повторить — кнопка ниже (новый прогон Architect + Sales, ≈ $0,1)."), ("reply_markup", RETRY_KB(L))])]
    a_ok = [a_vars, a_reread, a_save, a_run, a_done, s_start, sales, sj, ps, router(26, [s_ok, s_bad], 3600, 0)]
    a_code = ('{{if(14.stop_reason = "error"; "MODEL_ERROR"; if(14.stop_reason = "max_tokens"; "TRUNCATED"; '
              'if(14.stop_reason = "refusal"; "REFUSAL"; if(16.lead_id; "VALIDATION_FAILED"; "JSON_INVALID"))))}}')
    a_bad = [run(47, "architect", "14", "{{13.t0}}", "FAILED", acost, ARCH_VERSION,
                 {"error_code": a_code, "error_message": "{{substring(ifempty(14.result; \"(empty)\"); 0; 300)}}"},
                 name="ТЗ невалидно", conds=negate_each(va)),
             day_cost(48, acost),
             ds_upd(49, S_LEADS, L, {"status": "ERROR", "error_code": "ARCHITECT_FAILED", "error_message": a_code,
                    "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False),
             ev(50, L, "ARCHITECT_ERROR", a_code + " (run {{1.run_id}})", old="{{8.status}}", new="ERROR"),
             tg(51, "sendMessage", [("chat_id", OWNER), ("text", "⚠️ {{1.lead_id}}: Architect не дал корректное ТЗ (" + a_code + "). Статус ERROR, лид сохранён. "
                                     "Повторить — кнопка ниже (≈ $0,1)."), ("reply_markup", RETRY_KB(L))])]
    # ---------- маршрутизация: run_id из LH-20 = защита от повторов; бюджет и пауза
    base = [c("{{1.run_id}}", "exist"), c("{{8.architect_run_id}}", "text:equal", "{{1.run_id}}"),
            c('{{ifempty(8.sales_run_id; "none")}}', "text:notequal", "{{1.run_id}}")]
    modes = [[c("{{1.mode}}", "text:notequal", "more"), c("{{8.status}}", "text:equal", "APPROVED")], [c("{{1.mode}}", "text:equal", "more")]]
    ok_b = [c("{{2.paused}}", "text:notequal", "true"), c("{{ifempty(10.cost_usd; 0)}}", "number:less", "{{2.daily_budget_usd}}")]
    started["filter"] = flt("Запуск: run_id совпадает, бюджет есть", [base + md + ok_b for md in modes])
    run_flow = [started, t0, arch, aj, pa, router(17, [a_ok, a_bad], 2400, 0)]
    over_groups = [base + md + [x] for md in modes for x in (c("{{2.paused}}", "text:equal", "true"),
                                                               c("{{ifempty(10.cost_usd; 0)}}", "number:greaterorequal", "{{2.daily_budget_usd}}"))]
    over = [ds_upd(52, S_LEADS, L, {"status": "ERROR", "error_code": "BUDGET_OR_PAUSED", "error_message": "дневной бюджет исчерпан или пауза",
                   "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False, name="Пауза / бюджет исчерпан", conds=over_groups),
            ev(53, L, "ARCHITECT_ERROR", "BUDGET_OR_PAUSED: spent ${{ifempty(10.cost_usd; 0)}} of ${{2.daily_budget_usd}}, paused={{2.paused}}", old="{{8.status}}", new="ERROR"),
            tg(54, "sendMessage", [("chat_id", OWNER), ("text", "⏸ {{1.lead_id}}: Architect не запущен — AI на паузе или дневной бюджет Claude исчерпан "
                                    "(${{formatNumber(ifempty(10.cost_usd; 0); 4; \".\"; \"\")}} из ${{2.daily_budget_usd}}). После /resume нажмите кнопку ниже."),
                                   ("reply_markup", RETRY_KB(L))])]
    main = [ds_get(8, S_LEADS, L, name="Внутренний токен", conds=[TOK]),
            ds_upd(9, S_SET, "day_" + DAY_S, {"day": DAY_S}), ds_get(10, S_SET, "day_" + DAY_S),
            router(11, [run_flow, over], 900, 0)]
    # ---------- хранилище, вариант A (решение владельца T-0009): у LOST/ARCHIVED старше N дней очищаются тяжёлые поля
    since = "{{addDays(now; 0 - ifempty(2.cleanup_days; 30))}}"
    cleanup = [ds_search(4, S_LEADS, [[c("status", "text:equal", st), c("status_at", "date:less", since), c("architect_json", "exist")]
                                      for st in ("LOST", "ARCHIVED")], limit=5, cont=False, name="Очистка (вариант A)", conds=[TOK]),
               ds_upd(5, S_LEADS, "{{4.key}}", {"architect_json": "", "sales_json": "", "client_message": "", "client_message_ru": "",
                      "card_text": "", "updated_at": "{{now}}"}, upsert=False),
               ev(6, "{{4.key}}", "STORAGE_CLEANED", "variant A: architect_json, sales_json, client_message(_ru), card_text cleared ({{4.data.status}} > {{ifempty(2.cleanup_days; 30)}} d)")]
    denied = [ev(7, "", "SECURITY_DENIED", 'LH-11: неверный internal token (token_present={{if(1.token; "yes"; "no")}})',
                 name="Неверный токен", conds=[[c("{{1.token}}", "text:notequal", "{{2.internal_token}}")]])]
    # размер блюпринта: после модуля 10 (запись дня) дата дня = 10.day вместо повторяющегося formatDate(...)
    def short_day(mods):
        for mod in mods:
            if mod["id"] not in (9, 10):
                for k in ("mapper", "filter"):
                    if mod.get(k): mod[k] = json.loads(json.dumps(mod[k], ensure_ascii=False).replace(json.dumps(DAY_S)[1:-1], "{{10.day}}"))
            for e in mod.get("onerror") or []: short_day([e])
            for r in mod.get("routes") or []: short_day(r["flow"])
    short_day(main)
    flow = [hook(1, HOOK11), ds_get(2, S_SET, "main"), router(3, [cleanup, denied, main], 300, 0)]
    return {"name": "LH-11 Lead Hunter — Architect + Sales", "metadata": {"version": 1, "instant": True}, "flow": flow}


TG_MODS = ("telegram:UniversalAPICall", "telegram:SendDocument")
def tg_resume(flow):
    """D1: Ignore обрывает остаток маршрута. Если после Telegram-модуля в маршруте ещё есть модули — Resume (пустой выход)."""
    n = 0
    for i, mod in enumerate(flow):
        oe = mod.get("onerror") or []
        if mod["module"] in TG_MODS and i < len(flow) - 1 and len(oe) == 1 and oe[0]["module"] == "builtin:Ignore":
            mod["onerror"] = resume(oe[0]["id"], {"statusCode": 0} if mod["module"] == TG_MODS[0] else {})
            n += 1
        for r in mod.get("routes", []) or []: n += tg_resume(r["flow"])
    return n

def lh98():
    """LH-98: режим lh_log — журнал lh_log по lead_id (поле data) через Return output (обход лимита 100 записей у records_list)."""
    bp = json.load(open(os.path.join(ROOT, "blueprints", "LH-98.json")))
    routes = bp["flow"][1]["routes"]
    routes[:] = [r for r in routes if r["flow"][0]["id"] != 11]
    F = lambda k: "{{11.data." + k + "}}"
    routes.append({"flow": [
        ds_search(11, S_LOG, [[c("lead_id", "text:equal", "{{var.input.data}}")]], limit=50, cont=False, x=600, y=1000,
                  name="mode=lh_log + data LH-id", conds=[[c("{{var.input.mode}}", "text:equal", "lh_log"),
                                                           c("{{var.input.data}}", "text:pattern", "^LH-[0-9]{8}-[0-9a-f]{6}$")]]),
        agg(12, 11, {"table": F("table"), "event": F("event"), "details": F("details"), "created_at": F("created_at"),
                     "status": F("status"), "agent": F("agent"), "tokens_in": F("input_tokens"), "tokens_out": F("output_tokens"),
                     "estimated_cost_usd": F("estimated_cost_usd"), "prompt_version": F("prompt_version"),
                     "error_code": F("error_code"), "old_status": F("old_status"), "new_status": F("new_status"), "run_id": F("run_id")},
            x=900, y=1000),
        m(13, "scenario-service:ReturnData", 2, {"log": "{{12.array}}", "count": "{{length(12.array)}}"}, {}, x=1200, y=1000)]})
    return bp

def check(bp):
    ids = []
    def walk(flow):
        for mod in flow:
            ids.append(mod["id"])
            for e in mod.get("onerror", []) or []: ids.append(e["id"])
            for r in mod.get("routes", []) or []: walk(r["flow"])
    walk(bp["flow"])
    dup = {i for i in ids if ids.count(i) > 1}
    assert not dup, (bp["name"], sorted(dup))
    s = json.dumps(bp, ensure_ascii=False)
    assert "bot_token" not in s.lower() and "sk-ant" not in s
    return len(ids)

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "blueprints"), exist_ok=True)
    for name, fn in [("LH-99", lh99), ("LH-20", lh20), ("LH-03", lh03), ("LH-10", lh10), ("LH-11", lh11), ("LH-98", lh98)]:
        bp = fn()
        if name in ("LH-20", "LH-11"): print(name, "Telegram onerror Ignore→Resume:", tg_resume(bp["flow"]))
        n = check(bp)
        json.dump(bp, open(os.path.join(ROOT, "blueprints", name + ".json"), "w"), ensure_ascii=False, indent=1)
        print(name, "modules", n, "bytes", len(json.dumps(bp, ensure_ascii=False)))
