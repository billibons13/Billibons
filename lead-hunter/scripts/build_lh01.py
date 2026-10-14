"""LH-01 Scout + Gatekeeper (бывш. 7744024). Этап 1 плана AUTONOMOUS_TEAM_v2.
Берёт бэкап рабочего сценария и добавляет: чтение записи `search` (lh_settings), heartbeat `hb_lh01`,
URL Freelancer из настроек, Gatekeeper-фильтр (язык, include/exclude regex, бюджет, ставки) ДО записи в базу —
отсеянное не тратит операций и не идёт в AI. Логика — копия scripts/gatekeeper.py (тест: test_gatekeeper.py).
Запуск: python3 scripts/build_lh01.py → blueprints/LH-01.json"""
import json, os, copy
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
S_SET = 207951
src = json.load(open(os.path.join(ROOT, "backup", "7744024_before_2026-10-13.json")))
bp = copy.deepcopy(src)
f = {m["id"]: m for m in bp["flow"]}
meta = lambda: {"designer": {"x": 0, "y": 0}}

m20 = {"id": 20, "module": "datastore:GetRecord", "version": 1, "metadata": meta(),
       "mapper": {"key": "search", "returnWrapped": False}, "parameters": {"datastore": S_SET}}
m21 = {"id": 21, "module": "datastore:UpdateRecord", "version": 1, "metadata": meta(),
       "mapper": {"key": "hb_lh01", "upsert": True, "overwriteArrays": False,
                  "data": {"hb_at": "{{now}}", "hb_status": "ok", "hb_note": "scout run, search v{{20.version}}"}},
       "parameters": {"datastore": S_SET}}

f[2]["mapper"]["url"] = ("https://www.freelancer.com/api/projects/0.1/projects/active/?jobs[]="
    "{{join(split(20.jobs_csv; \",\"); \"&jobs[]=\")}}&project_types[]=fixed&project_types[]=hourly&limit=50"
    "&full_description=true&compact=true&from_time={{formatDate(addHours(now; 0 - 20.window_hours); \"X\")}}")

EUR = "{{round(3.budget.maximum * 3.currency.exchange_rate / first(map(1.data.result.currencies; \"exchange_rate\")))}}"
# 14.10 (решение владельца): порог бюджета — по МИНИМУМУ диапазона (раньше по максимуму: «1500–12500 INR» = 14–120 € проходил порог 100 €)
EUR_MIN = EUR.replace("3.budget.maximum", "ifempty(3.budget.minimum; 3.budget.maximum)")
TEXT = "{{lower(3.title)}} {{lower(substring(ifempty(3.description; \"\"); 0; 2000))}}"
common = [
    {"a": "{{if(contains(split(20.languages_csv; \",\"); 3.language); \"yes\"; \"no\")}}", "o": "text:equal", "b": "yes"},
    {"a": TEXT, "o": "text:pattern", "b": "{{20.include_regex}}"},
    {"a": TEXT, "o": "text:notpattern", "b": "{{20.exclude_regex}}"},
    {"a": "{{ifempty(3.bid_stats.bid_count; 0)}}", "o": "number:lessorequal", "b": "{{20.max_bids}}"},
]
f[6]["filter"] = {"name": "Gatekeeper: язык, тема (regex), не мусор, бюджет, ставки — из /search_settings",
    "conditions": [
        [{"a": "{{3.type}}", "o": "text:equal", "b": "fixed"}, {"a": EUR_MIN, "o": "number:greaterorequal", "b": "{{20.budget_fixed_min_eur}}"}] + common,
        [{"a": "{{3.type}}", "o": "text:equal", "b": "hourly"}, {"a": EUR_MIN, "o": "number:greaterorequal", "b": "{{20.budget_hourly_min_eur}}"}] + common]}
f[9]["filter"] = {"name": "Не больше max_per_run за запуск", "conditions": [[{"a": "{{7.i}}", "o": "number:lessorequal", "b": "{{20.max_per_run}}"}]]}
f[11]["mapper"]["data"]["verification"] = ("API: status={{3.status}}, nonpublic={{3.nonpublic}}, deleted={{3.deleted}}; "
                                           "Gatekeeper ok (search v{{20.version}}); передан в LH-03")
bp["flow"] = [m20, m21] + bp["flow"]
bp["name"] = "LH-01 Scout + Gatekeeper (Freelancer.com → LH-03)"

ids = [m["id"] for m in bp["flow"]] + [e["id"] for m in bp["flow"] for e in m.get("onerror") or []]
assert len(ids) == len(set(ids)), ids
s = json.dumps(bp, ensure_ascii=False)
assert "sk-ant" not in s and "bot_token" not in s.lower()
json.dump(bp, open(os.path.join(ROOT, "blueprints", "LH-01.json"), "w"), ensure_ascii=False, indent=1)
print("LH-01 modules", len(ids), "bytes", len(s.encode()))

SEARCH_DEFAULT = {  # запись `search` в lh_settings (значения = scripts/gatekeeper.py DEFAULT_SEARCH)
    "version": 1, "jobs_csv": "2380,2068,2823,2917,2918",
    "include_regex": r"\b(telegram|chat ?bots?|bots?|mini ?apps?|make\.com|integromat|n8n|zapier|webhooks?|automation|automate)\b",
    "exclude_regex": r"translat|garment|instructor|copywrit|chat admin|virtual assistant|data entry|\bseo\b|moodle|vertriebspartner|sales partner|voice (call|assistant)",
    "languages_csv": "en,de,ru,uk,es", "countries_csv": "", "budget_fixed_min_eur": 300, "budget_hourly_min_eur": 15,
    "max_bids": 200, "window_hours": 12, "max_per_run": 5, "send_grades_csv": "HOT,WARM,COLD"}
json.dump(SEARCH_DEFAULT, open(os.path.join(ROOT, "schemas", "search_default.json"), "w"), ensure_ascii=False, indent=1)
