"""AI-01 «RAIV Director — чат владельца» (T-20261008-0034).

Отдельный Telegram-бот «RAIV Director»: владелец пишет боту → Claude (Sonnet) отвечает как «Директор RAIV FISH».
Запуск:  python3 raiv-fish-bot/generate_ai_chat.py   → raiv-fish-bot/blueprints/AI-01.json

Секретов в файле и в blueprint нет:
- токен бота живёт только в подключении Make «RAIV Director» (его создаёт владелец);
- chat_id владельца хранится только в Make: data store lh_settings (207951), запись «ai_chat_owner», поле owner_chat_id;
- id подключения и вебхука — не секреты, но до создания бота их нет: берутся из окружения AI01_CONN / AI01_HOOK
  (без них в blueprint стоят заглушки 0 — такой blueprint в Make не создаётся, это нормально).

Запись «ai_chat_owner» (одна на всё): owner_chat_id, day (YYYY-MM-DD, Europe/Berlin), ai_count (вызовов Claude за day),
ai_history (последние обмены, ≤ HIST_MAX знаков). Поля ai_count / ai_history нужно добавить в структуру 618648 (аддитивно).
"""
import ast, json, os, re

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
STORE = 207951                    # lh_settings: 1 МБ, занято ~2 КБ — своя запись, свой ключ
KEY = "ai_chat_owner"
CONN = int(os.environ.get("AI01_CONN", "0"))   # Telegram Bot подключение «RAIV Director» (НЕ 11456488 и НЕ 9480305)
HOOK = int(os.environ.get("AI01_HOOK", "0"))   # вебхук telegram (WatchUpdates) на этом подключении
assert CONN not in (11456488, 11456487, 9480305, 9480304, 11276087), "это чужой бот — нужен новый «RAIV Director»"
MODEL, MAX_TOKENS = "claude-sonnet-5-5", 2000
DAILY_LIMIT = 10  # решение директора 08.10: кредиты Make на исходе; владелец может поднять
HIST_MAX = 6000
TG_MAX = 4000
TZ = "Europe/Berlin"


# ---------------- контекст проекта (собирается из репозитория, без секретов и без цен) ----------------
def catalog():
    src = open(os.path.join(HERE, "generate_blueprint.py"), encoding="utf-8").read()
    node = re.search(r"^cats = (\[.*?^\])", src, re.S | re.M).group(1)
    out = []
    for _, title, items in ast.literal_eval(node):
        names = [n for n, _, s in items if s]
        out.append(f"{title}: {len(names)} поз. в наличии (напр. {', '.join(names[:4])})")
    return "\n".join(out)

def waiting_tasks():
    txt = open(os.path.join(HERE, "agents", "tasks", "TASKS.md"), encoding="utf-8").read()
    res = []
    for block in re.split(r"\n(?=## T-)", txt):
        if "STATUS: WAITING" in block:
            title = block.split("\n", 1)[0].split("·", 1)[-1].strip()
            res.append("- " + title[:120])
    return "\n".join(res[:8]) or "- нет"

CONTEXT = f"""О ПРОЕКТЕ (сводка на дату генерации, без секретов):
RAIV FISH — небольшой магазин вяленой рыбы, икры и снеков к пиву в Шлезвиг-Гольштейне (Германия). Доставка: Эдделак, Марне, Брунсбюттель, Хайде (другие места — по договорённости). Канал t.me/raiv_fish1.
Ассортимент (категории; цены не называй — они в боте и меняются только владельцем):
{catalog()}
Telegram-бот заказов (Make): каталог, корзина, город, оплата (наличные; онлайн-оплата Stripe в тестовом режиме), бонусы и промокоды, отчёт владельцу 21:00, AI-советы 08:30, напоминания клиентам, агент склада 09:00, витрина Mini App. Языки ru/de/es/uk готовятся.
Lead Hunter — поиск заказов на разработку Telegram-ботов (Freelancer.com и ручная пересылка заявок): оценка AI, ТЗ и КП, пульт владельца в отдельном боте.
Bau Hunter — ежедневная сводка строительных тендеров Германии (TED), план развития ждёт решений владельца.
Контент-система (план): ролики о рыбе для TikTok/Instagram → Telegram-бот → заказ; публикации только после одобрения владельца.
Команда агентов под руководством Директора; правило: агенты предлагают — владелец решает.
Сейчас ПАУЗА ВЛАДЕЛЬЦА: с 07.10 все сценарии Make выключены владельцем. Кредиты Make ограничены (≈4 000 до 30.10).
Открытые вопросы, ждущие владельца:
{waiting_tasks()}"""

RULES = """ТЫ — «Директор RAIV FISH», AI-помощник владельца. Пишешь только владельцу, по-русски, коротко и по делу (до ~1500 знаков, если не просят больше).
Можно: отвечать на вопросы о проекте, советовать, готовить черновики текстов, постов, рассылок, коммерческих предложений, планы и чек-листы.
Нельзя (и ты технически не можешь): менять сценарии Make, цены, скидки, промокоды, наличие, данные клиентов; писать клиентам; публиковать. Если владелец просит такое — объясни, что это делается через чат Claude («поручение директору») или кнопками в рабочем боте, и предложи готовый текст/план.
Не выдумывай факты, цифры, цены и статусы: если не знаешь — так и скажи. Не проси и не повторяй токены, пароли, личные данные клиентов.
Без Markdown-разметки (обычный текст, можно эмодзи и списки с «•»)."""


# ---------------- helpers (стиль generate_lh.py) ----------------
def meta(x, y): return {"designer": {"x": x, "y": y}}
def c(a, o, b=None):
    d = {"a": a, "o": o}
    if b is not None: d["b"] = b
    return d
def m(mid, module, version, mapper, parameters=None, x=0, y=0, name=None, conds=None, onerror=None):
    mod = {"id": mid, "module": module, "version": version, "parameters": parameters or {}, "mapper": mapper, "metadata": meta(x, y)}
    if conds is not None: mod["filter"] = {"name": name or "filter", "conditions": conds}
    if onerror: mod["onerror"] = onerror
    return mod
def resume(mid, mapper): return [{"id": mid, "module": "builtin:Resume", "version": 1, "metadata": meta(0, 0), "mapper": mapper}]
def ignore(mid): return [{"id": mid, "module": "builtin:Ignore", "version": 1, "metadata": meta(0, 0), "mapper": None}]
def router(mid, routes, x=0, y=0):
    return {"id": mid, "module": "builtin:BasicRouter", "version": 1, "mapper": None, "metadata": meta(x, y),
            "routes": [{"flow": r} for r in routes]}
def upd(mid, data, **kw):
    return m(mid, "datastore:UpdateRecord", 1, {"key": KEY, "upsert": False, "overwriteArrays": False, "data": data},
             {"datastore": STORE}, **kw)
def send(mid, text, last=True, **kw):
    """sendMessage владельцу. Последний модуль маршрута → Ignore; если дальше есть модули → Resume (Ignore обрывает маршрут)."""
    return m(mid, "telegram:UniversalAPICall", 1,
             {"method": "POST", "bodyType": "assembled_body", "urlMethod": "sendMessage",
              "body_spec": [{"key": "chat_id", "value": "{{3.chat}}"}, {"key": "text", "value": text}]},
             {"__IMTCONN__": CONN}, onerror=ignore(mid + 500) if last else resume(mid + 500, {"statusCode": 0}), **kw)


def build():
    txt = 'trim(ifempty(1.message.text; ""))'
    today = '{{formatDate(now; "YYYY-MM-DD"; "' + TZ + '")}}'
    v = m(3, "util:SetVariables", 1, {"scope": "roundtrip", "variables": [
        {"name": "chat", "value": "{{1.message.chat.id}}"},
        {"name": "txt", "value": "{{" + txt + "}}"},
        {"name": "cmd", "value": '{{lower(first(split(first(split(' + txt + '; " ")); "@")))}}'},
        {"name": "today", "value": today},
        {"name": "cnt", "value": '{{if(2.day = formatDate(now; "YYYY-MM-DD"; "' + TZ + '"); ifempty(2.ai_count; 0); 0)}}'},
    ]}, x=600, name="Только владелец, только текст",
        conds=[[c("{{2.owner_chat_id}}", "exist"), c("{{1.message.from.id}}", "text:equal", "{{2.owner_chat_id}}"),
                c("{{1.message.chat.type}}", "text:equal", "private"), c("{{1.message.text}}", "exist")]])


    CMD = lambda name: [[c("{{3.cmd}}", "text:equal", name)]]
    START = ("🧭 RAIV Director — ваш AI-помощник по проекту RAIV FISH.\n\n"
             "Пишите вопрос или задачу обычным текстом: совет, план, черновик поста, рассылки или КП.\n"
             "Я только отвечаю и готовлю тексты — в Make, ценах и данных ничего не меняю, клиентам не пишу.\n\n"
             "/new — начать разговор заново (очистить память)\n/status — сводка и счётчик\n"
             f"Лимит: {DAILY_LIMIT} ответов в день.")
    STATUS = ("📊 RAIV Director\n"
              "Сегодня ответов AI: {{3.cnt}} из " + str(DAILY_LIMIT) + "\n"
              "Память: {{length(ifempty(2.ai_history; \"\"))}} из " + str(HIST_MAX) + " знаков\n"
              "Модель: Claude Sonnet, ответ до " + str(MAX_TOKENS) + " токенов\n"
              "Проект: магазин RAIV FISH, Lead Hunter, Bau Hunter, контент-система (план). "
              "Сценарии Make — на паузе владельца с 07.10.")
    r_start = [send(10, START, x=900, y=0, name="/start", conds=CMD("/start"))]
    r_new = [upd(20, {"ai_history": ""}, x=900, y=300, name="/new", conds=CMD("/new")),
             send(21, "🧹 Память очищена. Начинаем заново.", x=1200, y=300)]
    r_status = [send(30, STATUS, x=900, y=600, name="/status", conds=CMD("/status"))]
    not_cmd = [c("{{3.cmd}}", "text:notequal", x) for x in ("/start", "/new", "/status")]
    r_limit = [send(40, "⏳ Лимит на сегодня исчерпан (" + str(DAILY_LIMIT) + " ответов). Завтра продолжим.",
                    x=900, y=900, name="Лимит исчерпан", conds=[not_cmd + [c("{{3.cnt}}", "number:greaterorequal", str(DAILY_LIMIT))]])]

    hist = 'ifempty(2.ai_history; "")'
    prompt = (RULES + "\n\n" + CONTEXT + "\n\nИСТОРИЯ РАЗГОВОРА (последние сообщения):\n"
              '{{ifempty(2.ai_history; "— пусто —")}}'
              "\n\nНОВОЕ СООБЩЕНИЕ ВЛАДЕЛЬЦА:\n{{3.txt}}\n\nОтветь владельцу.")
    count = upd(50, {"day": "{{3.today}}", "ai_count": "{{3.cnt + 1}}"}, x=900, y=1200, name="Сообщение → Claude",
                conds=[not_cmd + [c("{{3.cnt}}", "number:less", str(DAILY_LIMIT))]])
    claude = m(51, "anthropic-claude:simpleTextPrompt", 1,
               {"model": MODEL, "textPrompt": prompt, "max_tokens": MAX_TOKENS}, x=1200, y=1200,
               onerror=resume(551, {"result": "", "stop_reason": "error", "usage": {"input_tokens": 0, "output_tokens": 0}}))
    ans = 'trim(ifempty(51.result; ""))'
    new_hist = ('{{substring(' + hist + ' + "\n\nВладелец: " + substring(3.txt; 0; 1500) + "\nДиректор: " + substring(' + ans + '; 0; 2500); '
                'max(0; length(' + hist + ' + "\n\nВладелец: " + substring(3.txt; 0; 1500) + "\nДиректор: " + substring(' + ans + '; 0; 2500)) - ' + str(HIST_MAX) + '); '
                + str(HIST_MAX * 2) + ')}}')
    ok = [upd(52, {"ai_history": new_hist}, x=1800, y=1200, name="Ответ получен",
              conds=[[c("{{51.stop_reason}}", "text:notequal", "error"), c("{{" + ans + "}}", "exist")]]),
          send(53, '{{substring(' + ans + '; 0; ' + str(TG_MAX) + ')}}', last=False, x=2100, y=1200),
          send(54, '{{substring(' + ans + '; ' + str(TG_MAX) + '; ' + str(TG_MAX * 2) + ')}}', x=2400, y=1200,
               name="Длинный ответ: часть 2", conds=[[c("{{length(" + ans + ")}}", "number:greater", str(TG_MAX))]])]
    fail = [send(56, "⚠️ AI сейчас недоступен, попробуйте позже.", x=1800, y=1500, name="Ошибка Claude",
                 conds=[[c("{{51.stop_reason}}", "text:equal", "error")], [c("{{" + ans + "}}", "notexist")]])]
    r_chat = [count, claude, router(55, [ok, fail], 1500, 1200)]

    flow = [m(1, "telegram:WatchUpdates", 1, {}, {"__IMTHOOK__": HOOK}, x=0),
            m(2, "datastore:GetRecord", 1, {"key": KEY, "returnWrapped": False}, {"datastore": STORE}, x=300),
            v, router(4, [r_start, r_new, r_status, r_limit, r_chat], 900, 0)]
    return {"name": "AI-01 RAIV Director — чат владельца", "flow": flow,
            "metadata": {"version": 1, "instant": True,
                         "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True, "autoCommitTriggerLast": True,
                                      "sequential": True, "confidential": False, "dataloss": False, "dlq": False,
                                      "freshVariables": False}}}


def check(bp):
    ids = []
    def walk(flow):
        for mod in flow:
            ids.append(mod["id"])
            ids.extend(e["id"] for e in mod.get("onerror", []) or [])
            for r in mod.get("routes", []) or []: walk(r["flow"])
    walk(bp["flow"])
    assert len(ids) == len(set(ids)), "дубли id"
    s = json.dumps(bp, ensure_ascii=False)
    assert (not os.environ.get("LH_OWNER_CHAT_ID") or os.environ["LH_OWNER_CHAT_ID"] not in s) and "bot_token" not in s.lower() and "sk-ant" not in s, "секрет в blueprint"
    assert not re.search(r"\b\d{9,10}:[A-Za-z0-9_-]{30,}", s), "похоже на токен бота"
    assert len(s.encode()) < 45_000, len(s.encode())
    return len(ids), len(s.encode())


if __name__ == "__main__":
    bp = build()
    n, size = check(bp)
    os.makedirs(os.path.join(HERE, "blueprints"), exist_ok=True)
    out = os.path.join(HERE, "blueprints", "AI-01.json")
    json.dump(bp, open(out, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
    print("AI-01 modules", n, "bytes", size, "conn", CONN or "PLACEHOLDER", "hook", HOOK or "PLACEHOLDER",
          "prompt chars", len(bp["flow"][3]["routes"][4]["flow"][1]["mapper"]["textPrompt"]))
