"""Генератор Make-сценариев Bau Hunter, этап 1 (минимум): BH-01 — ежедневная сводка тендеров TED в бот Zulius.
Запуск: python3 bau-hunter/scripts/generate_bh.py [--days N]  → bau-hunter/blueprints/BH-01.json
Секретов в файле нет (стиль lead-hunter/scripts/generate_lh.py):
- токен бота живёт в Telegram-подключении Make (CONN_TG), в сценарии его не видно;
- chat_id владельца читается внутри Make из data store 207951 (lh_settings), запись `main`, поле owner_chat_id.
  Если задан env LH_OWNER_CHAT_ID — дополнительно пишется BH-01.local.json (в .gitignore) с chat_id из env
  и без чтения data store; в репозиторий он не попадает.
--days N — окно публикации N дней (для разового теста при 0 объявлений за вчера); по умолчанию 1 = вчера.
"""
import json, os, sys

TEAM = 2241615
CONN_TG = 9480305            # Telegram-подключение Make (бот Zulius), как в LH
S_SET = 207951               # lh_settings, запись main
OWNER_CHAT_ID = os.environ.get("LH_OWNER_CHAT_ID", "")
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)

TED_URL = "https://api.ted.europa.eu/v3/notices/search"
NUTS = ["DEF", "DE6", "DE5", "DE9", "DE8"]       # SH, HH, HB, NI, MV
LIMIT = 15
TZ = "Europe/Berlin"
FIELDS = ["publication-number", "notice-title", "buyer-name", "buyer-city", "deadline-receipt-tender-date-lot",
          "estimated-value-lot", "estimated-value-cur-lot", "identifier-lot"]


def meta(x, y): return {"designer": {"x": x, "y": y}}
def c(a, o, b=None):
    d = {"a": a, "o": o}
    if b is not None: d["b"] = b
    return d
def m(mid, module, version, mapper, parameters=None, x=0, y=0, name=None, conds=None, onerror=None):
    mod = {"id": mid, "module": module, "version": version, "mapper": mapper,
           "parameters": parameters or {}, "metadata": meta(x, y)}
    if conds is not None: mod["filter"] = {"name": name or "filter", "conditions": conds}
    if onerror: mod["onerror"] = onerror
    return mod
def tg(mid, method, spec, **kw):
    """Telegram Bot API через подключение Make (токен не виден в сценарии)."""
    return m(mid, "telegram:UniversalAPICall", 1,
             {"method": "POST", "bodyType": "assembled_body", "body_spec": [{"key": k, "value": v} for k, v in spec],
              "urlMethod": method}, {"__IMTCONN__": CONN_TG}, **kw)

def day(offset, fmt): return 'formatDate(addDays(now; ' + str(offset) + '); "' + fmt + '"; "' + TZ + '")'


def bh01(days=1, chat_id=None):
    if days == 1:
        date_q = "publication-date={{" + day(-1, "YYYYMMDD") + "}}"
        date_h = "{{" + day(-1, "DD.MM.YYYY") + "}}"
    else:
        date_q = "publication-date>={{" + day(-days, "YYYYMMDD") + "}} AND publication-date<={{" + day(-1, "YYYYMMDD") + "}}"
        date_h = "{{" + day(-days, "DD.MM") + "}}–{{" + day(-1, "DD.MM.YYYY") + "}}"
    query = "classification-cpv=45* AND place-of-performance IN (" + " ".join(NUTS) + ") AND " + date_q
    # IML внутри {{}} содержит кавычки — подставляем его после json.dumps, иначе \" сломает формулу
    body = json.dumps({"query": "@Q@", "fields": FIELDS, "limit": LIMIT, "page": 1, "scope": "ALL",
                       "paginationMode": "PAGE_NUMBER", "onlyLatestVersions": True}, ensure_ascii=False).replace("@Q@", query)
    http = m(1, "http:ActionSendData", 3,
             {"url": TED_URL, "method": "post", "headers": [{"name": "Accept", "value": "application/json"}], "qs": [],
              "bodyType": "raw", "contentType": "application/json", "data": body, "parseResponse": True,
              "serializeUrl": False, "shareCookies": False, "rejectUnauthorized": True, "followRedirect": True,
              "followAllRedirects": False, "useQuerystring": False, "gzip": True, "useMtls": False, "timeout": 40},
             {"handleErrors": False, "useNewZLibDeCompress": True}, x=0, y=0)

    # 0 объявлений → итератор не пропускает фильтр, дальше ничего не выполняется и ничего не уходит
    it = m(2, "builtin:BasicFeeder", 1, {"array": "{{1.data.notices}}"}, {}, x=300, y=0, name="есть объявления",
           conds=[[c("{{1.data.totalNoticeCount}}", "number:greater", "0")]])

    F = lambda k: "2.`" + k + "`"
    ml = lambda k: 'ifempty(first(get(' + F(k) + '; "deu")); first(get(' + F(k) + '; "eng")))'
    title = 'ifempty(get(' + F("notice-title") + '; "deu"); get(' + F("notice-title") + '; "eng"))'
    val = 'first(' + F("estimated-value-lot") + ')'
    lots = 'length(' + F("identifier-lot") + ')'
    row = ("{{2.__IMTINDEX__}}. {{substring(" + title + "; 0; 150)}}\n"
           "🏛 {{" + ml("buyer-name") + "}}{{if(" + ml("buyer-city") + '; ", " + ' + ml("buyer-city") + '; "")}}\n'
           "⏳ Frist: {{ifempty(substring(first(" + F("deadline-receipt-tender-date-lot") + "); 0; 10); \"—\")}}"
           "{{if(" + val + '; " · 💶 " + formatNumber(' + val + '; 0; ","; ".") + " " + ifempty(first(' + F("estimated-value-cur-lot") + '); "EUR"); "")}}'
           "{{if(" + lots + ' > 1; " · Lose: " + ' + lots + '; "")}}\n'
           "🔗 https://ted.europa.eu/de/notice/-/detail/{{" + F("publication-number") + "}}\n")
    agg = m(3, "util:TextAggregator", 1, {"value": row}, {"feeder": 2, "rowSeparator": "\n"}, x=600, y=0)

    text = ("🏗 Тендеры стройки, Север DE — " + date_h + ": {{1.data.totalNoticeCount}}\n"
            "CPV 45 · SH, HH, HB, NI, MV · TED\n\n"
            "{{substring(3.text; 0; 3700)}}"
            '{{if(1.data.totalNoticeCount > ' + str(LIMIT) + '; "\n… ещё " + (1.data.totalNoticeCount - ' + str(LIMIT) + ') + " на ted.europa.eu"; "")}}')
    flow = [http, it, agg]
    if chat_id:
        chat = chat_id
    else:
        flow.append(m(4, "datastore:GetRecord", 1, {"key": "main", "returnWrapped": False}, {"datastore": S_SET}, x=900, y=0))
        chat = "{{4.owner_chat_id}}"
    flow.append(tg(5, "sendMessage", [("chat_id", chat), ("text", text),
                                      ("link_preview_options", '{"is_disabled":true}')], x=1200, y=0))
    return {"name": "BH-01 Bau — TED Tagesübersicht", "flow": flow,
            "metadata": {"version": 1, "instant": False, "scenario": {"roundtrips": 1, "maxErrors": 3, "autoCommit": True,
                         "autoCommitTriggerLast": True, "sequential": True, "confidential": False,
                         "dataloss": False, "dlq": False, "freshVariables": False},
                         "designer": {"orphans": []}, "zone": "eu1.make.com"}}

SCHEDULING = {"type": "daily", "time": "06:30"}


def check(bp, allow_chat=False):
    s = json.dumps(bp, ensure_ascii=False)
    assert "bot_token" not in s.lower() and "sk-ant" not in s
    if OWNER_CHAT_ID and not allow_chat: assert OWNER_CHAT_ID not in s, "chat_id в коммитимом файле"
    assert len(s.encode()) < 45000, len(s.encode())
    return len(s.encode())


if __name__ == "__main__":
    days = int(sys.argv[sys.argv.index("--days") + 1]) if "--days" in sys.argv else 1
    out = os.path.join(ROOT, "blueprints"); os.makedirs(out, exist_ok=True)
    bp = bh01(days)
    json.dump(bp, open(os.path.join(out, "BH-01.json"), "w"), ensure_ascii=False, indent=1)
    print("BH-01 days", days, "bytes", check(bp))
    if OWNER_CHAT_ID:
        loc = bh01(days, OWNER_CHAT_ID)
        json.dump(loc, open(os.path.join(out, "BH-01.local.json"), "w"), ensure_ascii=False, indent=1)
        print("BH-01.local (env chat_id, gitignored) bytes", check(loc, allow_chat=True))
