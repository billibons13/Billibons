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

def build():
    F = []
    F.append(ds_get(1, S_SET, "main"))
    F.append(ds_get(2, S_SET, "hb_lh01"))
    F.append(ds_get(3, S_SET, "search"))
    F.append(ds_get(4, S_SET, "guardian_state"))
    F.append(ds_get(5, S_SET, "day_" + TODAY))
    F.append(tg(6, "getWebhookInfo", [], onerror=True))
    # зависшие NEW (> 2 ч) и APPROVED без ТЗ (> 1 ч)
    F.append(ds_search(7, S_LEADS, [[c("status", "text:equal", "NEW"), c("created_at", "date:less", "{{addHours(now; -2)}}")]], limit=10))
    F.append(agg(8, 7, {"id": "{{7.lead_id}}"}))
    F.append(ds_search(9, S_LEADS, [[c("status", "text:equal", "APPROVED"), c("approved_at", "date:less", "{{addHours(now; -1)}}"),
                                       c("architect_json", "notexist")]], limit=10))
    F.append(agg(10, 9, {"id": "{{9.lead_id}}"}))
    F.append(ds_search(11, S_LEADS, [[c("status", "text:equal", "ERROR"), c("day", "text:equal", TODAY)]], limit=10))
    F.append(agg(12, 11, {"id": "{{11.lead_id}}", "code": "{{11.error_code}}"}))
    WH = "6.body.result"
    alarms = (
        '{{if(ifempty(2.hb_at; "") = ""; "🔭 Scout ещё ни разу не отметился\\n"; '
        'if(2.hb_at < addHours(now; 0 - ifempty(3.window_hours; 12) - 1); "🔭 Scout не запускался с " + formatDate(2.hb_at; "DD.MM HH:mm"; ' + TZ + ') + "\\n"; ""))}}'
        '{{if(ifempty(' + WH + '.pending_update_count; 0) > 5; "📨 Telegram: в очереди " + ' + WH + '.pending_update_count + " обновлений\\n"; "")}}'
        '{{if(ifempty(' + WH + '.last_error_date; 0) > formatDate(addHours(now; -1); "X"); "📨 Telegram webhook: " + ' + WH + '.last_error_message + "\\n"; "")}}'
        '{{if(ifempty(' + WH + '.url; "") = ""; "📨 Telegram webhook не установлен\\n"; "")}}'
        '{{if(length(8.array) > 0 & 1.paused != true; "⏳ Зависли NEW > 2 ч: " + join(map(8.array; "id"); ", ") + "\\n"; "")}}'
        '{{if(length(10.array) > 0; "⏳ Одобрены, но нет ТЗ > 1 ч: " + join(map(10.array; "id"); ", ") + "\\n"; "")}}'
        '{{if(length(12.array) >= 2; "❌ Ошибок за сутки: " + length(12.array) + " (" + join(map(12.array; "code"); ", ") + ")\\n"; "")}}'
        '{{if(ifempty(5.cost_usd; 0) >= 0.8 * ifempty(1.daily_budget_usd; 1); "💸 Расход AI " + formatNumber(5.cost_usd; 2) + " $ из " + 1.daily_budget_usd + " $\\n"; "")}}'
        '{{if(1.paused = true & ifempty(1.updated_at; now) < addHours(now; -24); "⏸ Пауза дольше суток: " + ifempty(1.paused_reason; "") + "\\n"; "")}}')
    F.append(setvars(13, [("alarms", alarms), ("hash", "{{md5(13.alarms)}}")]))
    # hash считаем вторым SetVariables, т.к. в одном модуле нельзя ссылаться на соседнюю переменную
    F[-1] = setvars(13, [("alarms", alarms)])
    F.append(setvars(14, [("hash", "{{md5(13.alarms)}}"), ("ok_day", TODAY)]))
    changed = [c("{{14.hash}}", "text:notequal", "{{ifempty(4.hash; \"\")}}")]
    daily_ok = [c("{{13.alarms}}", "text:equal", ""), c("{{ifempty(4.ok_day; \"\")}}", "text:notequal", "{{14.ok_day}}"),
                c("{{formatDate(now; \"H\"; " + TZ + ")}}", "number:greaterorequal", "8")]
    F.append(router(15, [
        [tg(16, "sendMessage", [("chat_id", OWNER), ("text",
            "{{if(13.alarms = \"\"; \"🛡 Guardian: ✅ восстановлено, всё в порядке\"; \"🛡 Guardian: ⚠️ проблема\\n\" + 13.alarms)}}")],
            name="Состояние изменилось", conds=[changed]),
         ds_upd(17, S_SET, "guardian_state", {"hash": "{{14.hash}}", "hb_note": "{{13.alarms}}", "hb_at": "{{now}}"})],
        [tg(18, "sendMessage", [("chat_id", OWNER), ("text",
            "🛡 Guardian: всё в порядке · Scout {{formatDate(2.hb_at; \"DD.MM HH:mm\"; " + TZ + ")}} · расход AI сегодня "
            "{{formatNumber(ifempty(5.cost_usd; 0); 2)}} $ из {{1.daily_budget_usd}} $")],
            name="Раз в сутки: всё в порядке", conds=[daily_ok]),
         ds_upd(19, S_SET, "guardian_state", {"ok_day": "{{14.ok_day}}"})],
        [ds_upd(20, S_SET, "hb_gd01", {"hb_at": "{{now}}", "hb_status": "{{if(13.alarms = \"\"; \"ok\"; \"alarm\")}}"}, name="heartbeat")],
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
