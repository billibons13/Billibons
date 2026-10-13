"""GD-01 SYSTEM GUARDIAN L1 «пульс» (T-0040, этап 4). Только чтение + сообщение владельцу; ничего не чинит сам.
Проверки (docs/AUTONOMOUS_TEAM_v2.md §4.3): Scout жив (hb_lh01), webhook бота (getWebhookInfo), зависшие NEW/APPROVED,
ERROR за сутки, бюджет AI дня, забытая пауза. Сообщение — только при смене состояния (guardian_state.hash)
и одна строка «всё в порядке» раз в сутки. Пишет hb_gd01 (сторож сторожа — проверяет L2).
Запуск: python3 scripts/build_gd01.py → blueprints/GD-01.json (создаётся в Make выключенным; включает владелец)."""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_lh import m, ds_get, ds_upd, ds_search, agg, router, tg, setvars, c, S_SET, S_LEADS, S_LOG

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TZ = 'ifempty(1.timezone; "Europe/Berlin")'
TODAY = '{{formatDate(now; "YYYY-MM-DD"; ' + TZ + ')}}'
OWNER = "{{1.owner_chat_id}}"

LH20_HOOK = "69syfagsko64kd9oelsekoz11e3k341q"   # udid вебхука LH-20 (бот должен смотреть сюда)
IDS = lambda a: 'remove(split(join(map(' + a + '; "id"); ","); ","); "")'   # пустой поиск даёт 1 бандл с null — join/split/remove убирает и null, и ""

def build():
    """v2 (13.10, исправлены дефекты тренера): состояние = набор кодов тревог (не текст) → нет повторов при новых id;
    ERROR — по status_at за 24 ч; проверка «карточка не доставлена»; webhook → LH-20; пустой поиск не считается лидом.
    Поля guardian_state — из существующей структуры lh_settings: hb_note = коды, day = дата последнего «всё в порядке»."""
    F = []
    F.append(ds_get(1, S_SET, "main"))
    F.append(ds_get(2, S_SET, "hb_lh01"))
    F.append(ds_get(3, S_SET, "search"))
    F.append(ds_get(4, S_SET, "guardian_state"))
    F.append(ds_get(5, S_SET, "day_" + TODAY))
    F.append(tg(6, "getWebhookInfo", [], onerror=True))
    F.append(ds_search(7, S_LEADS, [[c("status", "text:equal", "NEW"), c("created_at", "date:less", "{{addHours(now; -2)}}")]], limit=10))
    F.append(agg(8, 7, {"id": "{{7.lead_id}}"}))
    F.append(ds_search(9, S_LEADS, [[c("status", "text:equal", "APPROVED"), c("approved_at", "date:less", "{{addHours(now; -1)}}"),
                                       c("architect_json", "notexist")]], limit=10))
    F.append(agg(10, 9, {"id": "{{9.lead_id}}"}))
    F.append(ds_search(11, S_LEADS, [[c("status", "text:equal", "ERROR"), c("status_at", "date:greater", "{{addHours(now; -24)}}")]], limit=10))
    F.append(agg(12, 11, {"id": "{{11.lead_id}}", "code": "{{11.error_code}}"}))
    F.append(ds_search(21, S_LEADS, [[c("status", "text:equal", "SENT_TO_TELEGRAM"), c("tg_message_id", "notexist")]], limit=10))
    F.append(agg(22, 21, {"id": "{{21.lead_id}}"}))
    WH = "6.body.result"
    HB_OLD = 'if(ifempty(2.hb_at; "") = ""; true; 2.hb_at < addHours(now; 0 - ifempty(3.window_hours; 12) - 1))'
    checks = [  # (код, условие IML, текст тревоги IML)
        ("SCOUT_STALE", HB_OLD, '"🔭 Scout не отмечался дольше окна поиска (последний: " + ifempty(formatDate(2.hb_at; "DD.MM HH:mm"; ' + TZ + '); "никогда") + ")"'),
        ("TG_PENDING", 'ifempty(' + WH + '.pending_update_count; 0) > 5', '"📨 Telegram: в очереди " + ' + WH + '.pending_update_count + " обновлений"'),
        ("TG_ERROR", 'ifempty(' + WH + '.last_error_date; 0) > parseNumber(formatDate(addHours(now; -1); "X"))', '"📨 Ошибка webhook Telegram: " + ifempty(' + WH + '.last_error_message; "")'),
        ("TG_URL", 'contains(ifempty(' + WH + '.url; ""); "' + LH20_HOOK + '") = false', '"📨 Webhook бота не указывает на LH-20 — нужна кнопка восстановления (владелец)"'),
        ("STUCK_NEW", 'length(' + IDS("8.array") + ') > 0 & 1.paused != true', '"⏳ NEW > 2 ч: " + join(' + IDS("8.array") + '; ", ")'),
        ("STUCK_APPROVED", 'length(' + IDS("10.array") + ') > 0', '"⏳ Одобрены, ТЗ нет > 1 ч: " + join(' + IDS("10.array") + '; ", ")'),
        ("ERRORS", 'length(' + IDS("12.array") + ') >= 2', '"❌ Ошибок за 24 ч: " + length(' + IDS("12.array") + ') + " (" + join(remove(split(join(map(12.array; "code"); ","); ","); ""); ", ") + ")"'),
        ("NO_CARD", 'length(' + IDS("22.array") + ') > 0', '"📭 Карточка не доставлена: " + join(' + IDS("22.array") + '; ", ")'),
        ("BUDGET80", 'ifempty(5.cost_usd; 0) >= 0.8 * ifempty(1.daily_budget_usd; 1)', '"💸 Расход AI " + formatNumber(ifempty(5.cost_usd; 0); 2) + " $ из " + 1.daily_budget_usd + " $"'),
        ("PAUSE24", '1.paused = true & ifempty(1.updated_at; now) < addHours(now; -24)', '"⏸ Пауза дольше суток: " + ifempty(1.paused_reason; "")'),
    ]
    codes = "".join('{{if(' + cond + '; "' + code + ' "; "")}}' for code, cond, _ in checks)
    text = "".join('{{if(' + cond + '; "• " + ' + msg + ' + newline; "")}}' for _, cond, msg in checks)
    F.append(setvars(13, [("codes", codes), ("text", text)]))
    changed = [c("{{trim(13.codes)}}", "text:notequal", "{{trim(ifempty(4.hb_note; \"\"))}}")]
    daily_ok = [c("{{trim(13.codes)}}", "text:equal", ""), c("{{ifempty(4.day; \"\")}}", "text:notequal", TODAY),
                c("{{formatDate(now; \"H\"; " + TZ + ")}}", "number:greaterorequal", "8")]
    F.append(router(15, [
        [tg(16, "sendMessage", [("chat_id", OWNER), ("text",
            "{{if(trim(13.codes) = \"\"; \"🛡 Guardian: ✅ восстановлено, всё в порядке\"; \"🛡 Guardian: ⚠️ проблема\" + newline + 13.text)}}")],
            name="Состояние изменилось (по кодам)", conds=[changed]),
         ds_upd(17, S_SET, "guardian_state", {"hb_note": "{{trim(13.codes)}}", "hb_at": "{{now}}"})],
        [tg(18, "sendMessage", [("chat_id", OWNER), ("text",
            "🛡 Guardian: всё в порядке · Scout {{formatDate(2.hb_at; \"DD.MM HH:mm\"; " + TZ + ")}} · расход AI сегодня "
            "{{formatNumber(ifempty(5.cost_usd; 0); 2)}} $ из {{1.daily_budget_usd}} $")],
            name="Раз в сутки: всё в порядке", conds=[daily_ok]),
         ds_upd(19, S_SET, "guardian_state", {"day": TODAY})],
        [ds_upd(20, S_SET, "hb_gd01", {"hb_at": "{{now}}", "hb_status": "{{if(trim(13.codes) = \"\"; \"ok\"; \"alarm\")}}",
                                        "hb_note": "{{trim(13.codes)}}"}, name="heartbeat")],
    ], 1800, 0))
    return {"name": "GD-01 SYSTEM GUARDIAN — пульс Lead Hunter", "metadata": {"version": 1}, "flow": F}

if __name__ == "__main__":
    bp = build()
    ids = []
    def walk(fl):
        for x in fl:
            ids.append(x["id"]); ids.extend(e["id"] for e in x.get("onerror") or [])
            for r in x.get("routes") or []: walk(r["flow"])
    walk(bp["flow"])
    assert len(ids) == len(set(ids)), sorted(ids)
    s = json.dumps(bp, ensure_ascii=False)
    assert "sk-ant" not in s and "bot_token" not in s.lower() and (not os.environ.get("LH_OWNER_CHAT_ID") or os.environ["LH_OWNER_CHAT_ID"] not in s)
    json.dump(bp, open(os.path.join(ROOT, "blueprints", "GD-01.json"), "w"), ensure_ascii=False, indent=1)
    print("GD-01 modules", len(ids), "bytes", len(s.encode()))
