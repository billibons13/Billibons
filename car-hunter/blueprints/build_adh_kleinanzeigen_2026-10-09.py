#!/usr/bin/env python3
"""T-20261009-0037: собирает изменённые блюпринты ADH-01/02/03 из бэкапов (секреты — плейсхолдеры).

Вход:  car-hunter/backup/ADH-0X_before_2026-10-09.json
Выход: car-hunter/blueprints/ADH-0X_kleinanzeigen_2026-10-09.json
Плейсхолдеры __CF_TOKEN__, __CF_ACC__, __D1__, __ADH02_HOOK__ при импорте заменить реальными
значениями из текущего сценария (в git их нет).
"""
import copy
import json
import pathlib

ROOT = pathlib.Path(__file__).resolve().parents[1]
BK = ROOT / "backup"
OUT = ROOT / "blueprints"
R1 = "3.data.result[1].results[1]"   # строка машины после фильтра ADH-02
R4 = "4.data.result[1].results[1]"   # настройки/сравнение ADH-02
R8 = "8.data.result[1].results[1]"   # строка после оценки ADH-02


def load(name):
    return json.loads((BK / f"{name}_before_2026-10-09.json").read_text())


def find(flow, mid):
    for m in flow:
        if m["id"] == mid:
            return m
        for r in m.get("routes") or []:
            hit = find(r["flow"], mid)
            if hit:
                return hit
    return None


def http_d1(mid, data, x):
    return {
        "id": mid, "module": "http:ActionSendData", "version": 3,
        "mapper": {"qs": [], "url": "https://api.cloudflare.com/client/v4/accounts/__CF_ACC__/d1/database/__D1__/query",
                   "data": data, "gzip": True, "method": "post",
                   "headers": [{"name": "Authorization", "value": "Bearer __CF_TOKEN__"}], "timeout": 40,
                   "useMtls": False, "bodyType": "raw", "contentType": "application/json", "serializeUrl": False,
                   "shareCookies": False, "parseResponse": True, "followRedirect": True, "useQuerystring": False,
                   "followAllRedirects": False, "rejectUnauthorized": True},
        "onerror": [{"id": 5000 + mid, "mapper": None, "module": "builtin:Ignore", "version": 1,
                     "metadata": {"designer": {"x": 0, "y": 0}}}],
        "metadata": {"designer": {"x": x, "y": 300}},
        "parameters": {"handleErrors": False, "useNewZLibDeCompress": True},
    }


def tg(mid, method, body, x):
    return {
        "id": mid, "module": "telegram:UniversalAPICall", "version": 1,
        "mapper": {"method": "POST", "bodyType": "assembled_body",
                   "body_spec": [{"key": k, "value": v} for k, v in body], "urlMethod": method},
        "onerror": [{"id": 5000 + mid, "mapper": None, "module": "builtin:Ignore", "version": 1,
                     "metadata": {"designer": {"x": 0, "y": 0}}}],
        "metadata": {"designer": {"x": x, "y": 300}},
        "parameters": {"__IMTCONN__": 11730214},
    }


# ---------------------------------------------------------------- ADH-01
def adh01():
    bp = load("ADH-01")
    m20 = find(bp["flow"], 20)
    # не тратить AI на служебные письма Kleinanzeigen о собственных объявлениях / переписке
    for word in ["Deine Anzeige", "Deine Anfrage", "Nutzer-Anfrage", "Passwort", "Rechnung"]:
        m20["filter"]["conditions"][0].append({"a": "{{1.subject}}", "b": word, "o": "text:notcontain:ci"})
    p = m20["mapper"]["textPrompt"]
    old = "- description: weitere Infos aus der Mail (Ausstattung, TÜV, Unfall, Besitzer), max. 300 Zeichen, sonst \"\"."
    assert old in p
    new = (
        "- description: übernimm WÖRTLICH (auf Deutsch) alle Angaben zu HU/TÜV (z.B. 'HU bis 03/2028', 'TÜV neu', "
        "'ohne TÜV'), Getriebe, Motor, Rost, Unfall, Export/Bastler, fahrbereit; danach weitere Infos "
        "(Ausstattung, Besitzer). Max. 500 Zeichen, sonst \"\".\n"
        "- Kleinanzeigen (Suchauftrag-/Suchagent-Mail, z.B. 'Neue Anzeigen', 'gespeicherte Suche'): jedes Inserat hat "
        "einen Link wie kleinanzeigen.de/s-anzeige/<titel>/<ANZEIGEN-ID>-216-<ort>. listing_id = 'ka-'+ANZEIGEN-ID "
        "(die erste Zahlengruppe im letzten Pfadteil). url: bevorzugt der direkte s-anzeige-Link, sonst der Link aus "
        "der Mail. Preis '1.000 € VB' = 1000; nur 'VB' ohne Zahl = null; 'Zu verschenken' = 0. "
        "seller_type: 'privat', wenn nicht 'gewerblich'/'Händler' steht. Titel unverändert übernehmen."
    )
    m20["mapper"]["textPrompt"] = p.replace(old, new)
    return bp


# ---------------------------------------------------------------- ADH-02
RE_NONE = (r"/^[\s\S]*?(?:\b(?:ohne|kein|keinen)\s+(?:HU|TÜV|TUEV|TUV)\b|\b(?:HU|TÜV|TUEV|TUV)(?:\s*\/\s*AU)?"
           r"\s*(?:ist\s+)?(?:abgelaufen|überzogen|überfällig))[\s\S]*$/i")
RE_NEW = (r"/^[\s\S]*?(?:\b(?:HU|TÜV|TUEV|TUV)(?:\s*\/\s*AU)?\s*[:\-]?\s*(?:neu|frisch|2\s*Jahre)|"
          r"\b(?:neue[rnms]?|frische[rnms]?)\s+(?:HU|TÜV|TUEV|TUV))"
          r"(?!\s*(?:nötig|notwendig|fällig|erforderlich|muss|benötigt))[\s\S]*$/i")
RE_YEAR = (r"/^[\s\S]*?\b(?:HU|TÜV|TUEV|TUV)(?:\s*\/\s*AU)?[^0-9\n]{0,15}?(?:(?:0?[1-9]|1[0-2])\s*[.\/-]\s*)?"
           r"((?:20)?[2-4]\d)(?!\d)[\s\S]*$/i")


def adh02():
    bp = load("ADH-02")
    flow = bp["flow"]
    ids = [m["id"] for m in flow]
    m3, m4, m5, m8, m9 = (find(flow, i) for i in (3, 4, 5, 8, 9))

    # 4: дополнительно читаем hu_min_year и send_all_matches из settings
    d4 = m4["mapper"]["data"]
    assert d4.count(" AS weights\",\"params") == 1
    m4["mapper"]["data"] = d4.replace(
        " AS weights\",\"params",
        " AS weights, (SELECT value FROM settings WHERE key='hu_min_year') AS hu_min, "
        "(SELECT value FROM settings WHERE key='send_all_matches') AS send_all\",\"params")

    text = f'ifempty({R1}.title; "") + " " + ifempty({R1}.description; "")'
    m11 = {"id": 11, "module": "util:SetVariables", "version": 1, "parameters": {},
           "metadata": {"designer": {"x": 1350, "y": 0}},
           "mapper": {"scope": "roundtrip", "variables": [
               {"name": "hu_none", "value": "{{replace(" + text + '; "' + RE_NONE + '"; "1")}}'},
               {"name": "hu_new", "value": "{{replace(" + text + '; "' + RE_NEW + '"; "1")}}'},
               {"name": "hu_raw", "value": "{{replace(" + text + '; "' + RE_YEAR + '"; "§$1")}}'},
           ]}}
    m12 = {"id": 12, "module": "util:SetVariables", "version": 1, "parameters": {},
           "metadata": {"designer": {"x": 1500, "y": 0}},
           "mapper": {"scope": "roundtrip", "variables": [
               {"name": "hu_year", "value":
                '{{if(11.hu_none = "1"; "0"; if(11.hu_new = "1"; formatDate(addMonths(now; 24); "YYYY"); '
                'if(substring(11.hu_raw; 0; 1) = "§"; if(length(11.hu_raw) = 5; substring(11.hu_raw; 1; 5); '
                '"20" + substring(11.hu_raw; 1; 3)); "")))}}'},
           ]}}
    hu_min = "{{" + R4 + ".hu_min}}"
    m14 = http_d1(14, "{\"sql\":\"UPDATE cars SET status='filtered_out', filter_reason=?2, updated_at=datetime('now') "
                      "WHERE listing_id=?1\",\"params\":[\"{{2.id}}\",\"HU/TÜV: {{12.hu_year}} (0 = нет/истекла), "
                      "нужно ≥ " + hu_min + "\"]}", 1800)
    m14["filter"] = {"name": "HU раньше минимума → отсеять", "conditions": [[
        {"a": "{{12.hu_year}}", "o": "exist"},
        {"a": hu_min, "o": "exist"},
        {"a": "{{12.hu_year}}", "b": hu_min, "o": "number:less"}]]}

    # 5: AI-инспектор — добавляем HU и критерии состояния
    m5["filter"] = {"name": "HU ок или неизвестна", "conditions": [
        [{"a": "{{12.hu_year}}", "o": "notexist"}],
        [{"a": hu_min, "o": "notexist"}],
        [{"a": "{{12.hu_year}}", "b": hu_min, "o": "number:greaterorequal"}]]}
    p = m5["mapper"]["textPrompt"]
    old_out = p[p.index("Верни ТОЛЬКО JSON"):]
    add = (
        "HU/TÜV (детерминированно из текста, год): {{ifempty(12.hu_year; \"не указано\")}}.\n\n"
        "СОСТОЯНИЕ — критерии владельца: коробка работает, мотор работает, без ржавчины. Оценивай ТОЛЬКО по тексту "
        "продавца (заголовок + описание). Для КПП, мотора и ржавчины выбери ровно одно:\n"
        "• «ок по словам продавца» — продавец прямо пишет, что исправно / без ржавчины;\n"
        "• «дефект: <короткая цитата на немецком>» — дефект назван прямо;\n"
        "• «не указано — проверить при осмотре» — текст молчит.\n"
        "reject = \"1\" ТОЛЬКО если текст прямо называет дефект: Getriebe defekt, Getriebeschaden, Gang springt raus, "
        "schaltet nicht; Motorschaden, Motor defekt, springt nicht an, läuft nicht, Kolbenfresser, Pleuel, "
        "Zylinderkopfdichtung defekt; Rost, rostig, Durchrostung, durchgerostet, Rostlöcher; Bastlerfahrzeug, "
        "an Bastler, für Export, nur Export, nicht fahrbereit. Отрицания («kein Motorschaden», «rostfrei», "
        "«ohne Rost», «kein Rost») — НЕ дефект. Мелкий косметический «Flugrost» — не reject, но отметь. "
        "Сомневаешься — reject = \"0\". Никогда не утверждай, что машина исправна: только «по словам продавца». "
        "Учитывай состояние в risk_score.\n\n"
    )
    new_out = (
        "Верни ТОЛЬКО JSON без пояснений:\n{\"deal_score\": целое, \"params\": [\"красные флаги кратко по-русски "
        "через '; ' или 'не найдено'\", risk_score, market_price, deal_score, \"вердикт 1–2 предложения по-русски: "
        "стоит ли смотреть и что проверить на осмотре\", \"КПП: …; Мотор: …; Ржавчина: …\", \"0 или 1 (reject)\"]}"
    )
    m5["mapper"]["textPrompt"] = p.replace(old_out, add + new_out)

    # 8: сохраняем состояние в verdict, reject → filtered_out
    d8 = m8["mapper"]["data"]
    old8 = "verdict=?5, status='scored', updated_at"
    assert old8 in d8
    d8 = d8.replace(old8, "verdict='🔧 '||ifnull(?6,'КПП/мотор/ржавчина: не указано — проверить при осмотре')||char(10)||?5, "
                          "status=CASE WHEN CAST(?7 AS TEXT)='1' THEN 'filtered_out' ELSE 'scored' END, "
                          "filter_reason=CASE WHEN CAST(?7 AS TEXT)='1' THEN 'дефект по тексту: '||ifnull(?6,'') "
                          "ELSE filter_reason END, updated_at")
    assert d8.count("deal_score, verdict\",\"params") == 1
    d8 = d8.replace("deal_score, verdict\",\"params", "deal_score, verdict, status\",\"params")
    m8["mapper"]["data"] = d8

    # 9: карточка
    base = [{"a": f"{{{{{R4}.paused}}}}", "b": "1", "o": "text:notequal"},
            {"a": f"{{{{{R4}.chat}}}}", "o": "exist"},
            {"a": f"{{{{{R8}.status}}}}", "b": "scored", "o": "text:equal"}]
    m9["filter"] = {"name": "Подходит: score ≥ порога ИЛИ send_all_matches=1; не пауза; без явного дефекта",
                    "conditions": [
                        [{"a": f"{{{{{R8}.deal_score}}}}", "b": f"{{{{{R4}.threshold}}}}",
                          "o": "number:greaterorequal"}] + copy.deepcopy(base),
                        [{"a": f"{{{{{R4}.send_all}}}}", "b": "1", "o": "text:equal"}] + copy.deepcopy(base)]}
    body = {b["key"]: b for b in m9["mapper"]["body_spec"]}
    t = body["text"]["value"]
    t = t.replace("\n\n🏆 Deal Score",
                  "\n📋 HU/TÜV: {{ifempty(12.hu_year; \"? — не указано, уточнить у продавца\")}}\n\n🏆 Deal Score")
    t += "\n\nℹ️ Состояние — только по тексту продавца, не проверено. Нужны осмотр и пробная поездка."
    body["text"]["value"] = t
    body["reply_markup"]["value"] = (
        "{\"inline_keyboard\":[[{\"text\":\"⭐ В избранное\",\"callback_data\":\"fav:{{2.id}}\"},"
        "{\"text\":\"❌ Скрыть\",\"callback_data\":\"hide:{{2.id}}\"}],"
        "[{\"text\":\"🔍 Подробнее\",\"callback_data\":\"det:{{2.id}}\"},"
        "{\"text\":\"✍️ Написать продавцу\",\"callback_data\":\"msg:{{2.id}}\"}],"
        "[{\"text\":\"🔗 Открыть объявление\",\"url\":\"{{" + R8 + ".url}}\"}],"
        "[{\"text\":\"🤖 AI-черновик\",\"callback_data\":\"ai:{{2.id}}\"},"
        "{\"text\":\"➡️ Следующее\",\"callback_data\":\"next:x\"}]]}")

    # сборка: 1,2,3,4,11,12, router 13 → [14] | [5..10]
    head = [m for m in flow if m["id"] in (1, 2, 3, 4)]
    rest = [m for m in flow if m["id"] in (5, 6, 7, 8, 9, 10)]
    router = {"id": 13, "module": "builtin:BasicRouter", "version": 1, "mapper": None,
              "metadata": {"designer": {"x": 1650, "y": 0}},
              "routes": [{"flow": [m14]}, {"flow": rest}]}
    bp["flow"] = head + [m11, m12, router]
    assert sorted(ids) == sorted([m["id"] for m in head + rest])
    return bp


# ---------------------------------------------------------------- ADH-03
DRAFT_DE = (
    "Hallo,\n\nich interessiere mich für Ihr Fahrzeug „{{escapeHTML(ifempty(261.data.result[1].results[1].title; "
    "\"\"))}}“. Ist es noch zu haben?\n\nVorab ein paar kurze Fragen:\n"
    "1. Bis wann ist die HU/TÜV gültig?\n"
    "2. Schaltet das Getriebe sauber (keine Geräusche, kein Rucken)?\n"
    "3. Läuft der Motor einwandfrei (kein Ölverlust, keine Warnleuchten)?\n"
    "4. Gibt es Rost, z. B. an Schwellern, Radläufen oder am Unterboden?\n"
    "5. Wann wäre eine Besichtigung mit Probefahrt möglich?\n"
    "6. Ist beim Preis noch etwas Spielraum?\n\nVielen Dank und viele Grüße"
)
DRAFT_RU = (
    "Перевод: Здравствуйте, меня интересует ваш автомобиль. Он ещё продаётся? Несколько вопросов: 1) до какого "
    "срока HU/TÜV; 2) коробка переключается чисто, без шумов и рывков; 3) мотор работает исправно, без течи масла "
    "и ошибок; 4) есть ли ржавчина (пороги, арки, днище); 5) когда можно посмотреть и прокатиться; 6) есть ли торг. "
    "Спасибо, с уважением."
)


def adh03():
    bp = load("ADH-03")
    router = find(bp["flow"], 4)
    m231 = find(bp["flow"], 231)
    m231["filter"]["name"] = "🤖 AI-черновик"
    for c in m231["filter"]["conditions"][0]:
        if c.get("b") == "cb_msg":
            c["b"] = "cb_ai"
    m231["mapper"]["data"] = m231["mapper"]["data"].replace("SELECT title, price,", "SELECT title, url, price,")
    m233 = find(bp["flow"], 233)
    m233["mapper"]["textPrompt"] = m233["mapper"]["textPrompt"].replace(
        "3–4 konkrete Fragen (Unfallfreiheit, Scheckheft/Service, Anzahl Vorbesitzer, TÜV, bekannte Mängel)",
        "4–6 konkrete Fragen (HU/TÜV bis wann, Getriebe schaltet sauber, Motor läuft einwandfrei, Rost, "
        "Unfallfreiheit, Spielraum beim Preis)")
    m234 = find(bp["flow"], 234)
    b234 = {b["key"]: b for b in m234["mapper"]["body_spec"]}
    b234["text"]["value"] = b234["text"]["value"].replace(
        "✉️ Черновик для продавца — скопируй и отправь через площадку:",
        "🤖 AI-черновик для продавца — скопируй и отправь САМ через чат Kleinanzeigen (бот продавцу ничего не отправляет):")
    m234["mapper"]["body_spec"].append({"key": "reply_markup", "value":
        "{\"inline_keyboard\":[[{\"text\":\"🔗 Открыть объявление\",\"url\":\"{{231.data.result[1].results[1].url}}\"}]]}"})

    m261 = http_d1(261, "{\"sql\":\"SELECT title, url, price FROM cars WHERE listing_id='{{2.lid}}'\"}", 10900)
    m261["filter"] = {"name": "✍️ Написать продавцу (шаблон, без AI)", "conditions": [[
        {"a": "{{2.cmd}}", "b": "cb_msg", "o": "text:equal"},
        {"a": "{{3.data.result[2].results[1].owner}}", "b": "{{2.chat}}", "o": "text:equal"}]]}
    m262 = tg(262, "answerCallbackQuery", [("callback_query_id", "{{2.cbid}}"), ("text", "✍️ Черновик готов")], 11200)
    text = ("✍️ <b>Черновик для продавца</b>\nНажми на текст — он скопируется. Потом «🔗 Открыть объявление» и "
            "отправь его САМ в чате Kleinanzeigen. Бот продавцу ничего не отправляет.\n\n<pre>" + DRAFT_DE +
            "</pre>\n\n🇷🇺 <i>" + DRAFT_RU + "</i>")
    m263 = tg(263, "sendMessage", [
        ("chat_id", "{{2.chat}}"), ("text", text), ("parse_mode", "HTML"),
        ("reply_markup", "{\"inline_keyboard\":[[{\"text\":\"🔗 Открыть объявление\",\"url\":"
                         "\"{{261.data.result[1].results[1].url}}\"}],[{\"text\":\"🤖 AI-вариант\","
                         "\"callback_data\":\"ai:{{2.lid}}\"}]]}"),
        ("link_preview_options", "{\"is_disabled\":true}")], 11500)
    pos = next(i for i, r in enumerate(router["routes"]) if r["flow"][0]["id"] == 231)
    router["routes"].insert(pos + 1, {"flow": [m261, m262, m263]})
    return bp


if __name__ == "__main__":
    for name, fn in (("ADH-01", adh01), ("ADH-02", adh02), ("ADH-03", adh03)):
        bp = fn()
        s = json.dumps(bp, ensure_ascii=False, separators=(",", ":"))
        (OUT / f"{name}_kleinanzeigen_2026-10-09.json").write_text(s)
        print(name, len(s.encode()), "bytes")
