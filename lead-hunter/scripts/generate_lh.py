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
             "Перешлите заявку (текст + ссылка) — пришлю карточку с оценкой.\n/new /today /stats /pause /resume /settings /help")
    routes.append([LS, A, day_touch(22), day_get(23), tg(24, "sendMessage", [("chat_id", OWNER), ("text", START)])])
    # --- /help
    HELP = ("ℹ️ Lead Hunter — пульт владельца\n\n"
            "1. Перешлите сюда заявку: текст, текст + ссылка или пост из канала.\n"
            "2. Через ~1 мин придёт карточка: оценка 0–100, HOT/WARM/COLD/REJECT, причины.\n"
            "3. Кнопки: ✅ Approve — отметить (клиенту ничего не отправляется), ❌ Reject — с причиной, 🔍 More analysis.\n\n"
            "/new — новые HOT/WARM без решения (до 5)\n/today — итоги дня\n/stats — 7 и 30 дней\n"
            "/pause — пауза AI (заявки копятся в очереди)\n/resume — продолжить и разобрать очередь\n/settings — настройки\n\n"
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
    routes.append([http_form(80, URL03, [
        ("token", "{{2.internal_token}}"), ("text", "{{3.txt}}"), ("message_id", "{{1.message.message_id}}"),
        ("text_links", '{{join(map(ifempty(1.message.entities; 1.message.caption_entities); "url"; "type"; "text_link"); " ")}}'),
        ("fwd_type", "{{" + fo + ".type}}"), ("fwd_chat_username", "{{" + fo + ".chat.username}}"),
        ("fwd_chat_title", "{{" + fo + ".chat.title}}"), ("fwd_message_id", "{{" + fo + ".message_id}}"),
        ("fwd_user_username", "{{" + fo + ".sender_user.username}}"),
        ("fwd_user_name", "{{" + fo + ".sender_user.first_name}}{{" + fo + ".sender_user_name}}"),
        ("fwd_date", "{{" + fo + ".date}}")],
        name="Пересланная заявка", conds=[MSG + [c("{{3.txt}}", "exist"), c("{{3.txt}}", "text:notpattern", "^/")]]),
        tg(81, "sendMessage", [("chat_id", OWNER), ("text", "⏳ Принял, сохраняю…")])])
    routes.append([tg(82, "sendMessage", [("chat_id", OWNER), ("text", "🖼 Скриншоты и файлы без текста пока не разбираю (этап 2). Пришлите текст заявки и ссылку.")],
                      name="Медиа без текста", conds=[MSG + [c("{{3.txt}}", "notexist")]])])
    # --- кнопки
    LEADK = "{{3.lead}}"
    dec = lambda mid, action, reason="": ds_add(mid, S_LOG, "{{uuid}}", {
        "table": "decisions", "decision_id": "{{uuid}}", "lead_id": LEADK, "owner_chat_id": "{{3.from}}", "action": action,
        "reason": reason, "telegram_message_id": "{{3.mid}}", "created_at": "{{now}}", "day": DAY_S})
    routes.append([ds_get(90, S_LEADS, LEADK, name="✅ Approve", conds=[act("ap")]),
                   ds_upd(91, S_LEADS, LEADK, {"status": "APPROVED", "status_at": "{{now}}", "updated_at": "{{now}}"}, upsert=False),
                   dec(92, "APPROVE"), ev(93, LEADK, "OWNER_APPROVED", "button", old="{{90.status}}", new="APPROVED"),
                   answer(94, "Approved"),
                   tg(95, "editMessageReplyMarkup", [("chat_id", OWNER), ("message_id", "{{3.mid}}"),
                                                     ("reply_markup", KB([[{"text": "✅ Approved", "callback_data": "z"}]]))]),
                   tg(96, "sendMessage", [("chat_id", OWNER), ("text", "Lead approved. Client contact is still manual.\n" + LEADK)])])
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
                   tg(123, "sendMessage", [("chat_id", OWNER), ("text", "Detailed Architect analysis will be available in the next phase.\n" + LEADK)])])
    routes.append([answer(130, "", name="Служебная кнопка", conds=[act("z")])])
    routes.append([answer(131, "Эта кнопка из старой системы и больше не используется.", name="Неизвестная кнопка",
                          conds=[CB + [c("{{3.a}}", "text:notequal", a) for a in ("ap", "rj", "rr", "ma", "z")]])])
    flow = [hook(1, HOOK20), ds_get(2, S_SET, "main"), v, router(4, routes, 600, 0)]
    return {"name": "LH-20 Lead Hunter — Telegram Owner Panel", "metadata": {"version": 1, "instant": True}, "flow": flow}


# ================= LH-03: Manual Intake =================
def lh03():
    T = "1.text"
    url_in_text = ('if(contains(' + T + '; "http"); replace(' + T + '; "/^[\\s\\S]*?(https?:\\/\\/[^\\s<>)\\]]+)[\\s\\S]*$/"; "$1"); "")')
    chan = ('if(1.fwd_chat_username; "https://t.me/" + 1.fwd_chat_username + "/" + 1.fwd_message_id; "")')
    v3 = setvars(3, [
        ("raw", "{{trim(" + T + ")}}"),
        ("u", "{{ifempty(" + url_in_text + "; ifempty(first(split(1.text_links; \" \")); " + chan + "))}}"),
        ("source", '{{if(1.fwd_chat_username; "telegram:@" + 1.fwd_chat_username; if(1.fwd_type = "channel"; "telegram:" + 1.fwd_chat_title; "manual"))}}'),
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
            "🆔 {{1.lead_id}}")
    # COLD/REJECT — одна строка; причина = ограничение (cap) или критерий с наименьшим баллом
    part = lambda k: ('if(' + num(k) + ' < 10; "0"; "") + toString(10.scores.' + k + ') + "|' + LABEL[k] + ' " + '
                      'toString(10.scores.' + k + ') + "/10: " + 20.r_' + k)
    lowest = ('replace(first(sort(split(' + ' + "§" + '.join(part(k) for k in KEYS) + '; "§"))); "/^[0-9.]+\\|/"; "")')
    short = ("{{" + EMO + "}} {{1.lead_id}} · {{14.grade}} {{13.score}} — в архиве, причина: "
             "{{if(13.cap_reason; replace(13.cap_reason; \"/;\\s*$/\"; \"\"); " + lowest + ")}}")
    v20 = setvars(20, [("r_" + k, "{{" + esc("10.reasons." + k) + "}}") for k in KEYS])  # причины без " и \\, в одну строку
    v25 = setvars(25, [("full", card), ("short", short)])
    v15 = setvars(15, [("card", '{{if(14.grade = "HOT"; 25.full; if(14.grade = "WARM"; 25.full; 25.short))}}'), ("next",'{{if(14.grade = "HOT"; "SENT_TO_TELEGRAM"; if(14.grade = "WARM"; "SENT_TO_TELEGRAM"; "ARCHIVED"))}}')])
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
    BTN = KB([[{"text": "✅ Approve", "callback_data": "ap|{{1.lead_id}}"}, {"text": "❌ Reject", "callback_data": "rj|{{1.lead_id}}"}],
              [{"text": "🔍 More analysis", "callback_data": "ma|{{1.lead_id}}"}]])
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
    for name, fn in [("LH-99", lh99), ("LH-20", lh20), ("LH-03", lh03), ("LH-10", lh10), ("LH-11", lh11)]:
        bp = fn()
        n = check(bp)
        json.dump(bp, open(os.path.join(ROOT, "blueprints", name + ".json"), "w"), ensure_ascii=False, indent=1)
        print(name, "modules", n, "bytes", len(json.dumps(bp, ensure_ascii=False)))
