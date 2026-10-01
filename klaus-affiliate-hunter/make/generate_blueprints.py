"""Генератор Make-сценариев Claus Affiliate Hunter.

  python3 make/generate_blueprints.py   → make/intake_blueprint.json, make/status_blueprint.json

Make — вторая линия защиты: даже если в webhook придёт непроверенная ссылка,
сценарий сохранит affiliate_url только при affiliate_status = verified и https-адресе.

Важно про формулы Make: операторов and / or в них нет (выражение молча считается неверно),
поэтому все условия собраны из вложенных if() в модуле «Set variables» (id 7) и дальше
используются как готовые флаги "1"/"0".
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
DS = 203568                 # data store «Klaus Affiliate — Produkte»
HOOK_INTAKE = 3820339       # https://hook.eu1.make.com/lrdmvdkf8m3svedd58zei2kn62ptgbam
HOOK_STATUS = 3820340       # https://hook.eu1.make.com/arkbrhuvdrp6fxrzp4vx581lnyayxv81
TG_CONN = 9469273           # Telegram-бот, через который приходят скрипты Meister Klaus
OWNER_CHAT = "6883357001"

meta = lambda x, y=0: {"designer": {"x": x, "y": y}}
# sequential = False: иначе Make ставит запросы в очередь и вебхук отвечает "Accepted" без результата.
SCEN_META = {"instant": True, "version": 1, "scenario": {
    "dlq": False, "dataloss": False, "maxErrors": 3, "autoCommit": True, "roundtrips": 1,
    "sequential": False, "confidential": False, "autoCommitTriggerLast": True}}

# Флаги intake (строки "1"/"0")
F_VALID = ('{{if(1.product_id; if(1.product_name; if(indexOf(ifempty(1.product_url; ""); "http") = 0; '
           '"1"; "0"); "0"); "0")}}')
_VER = 'if(1.affiliate_status = "verified"; if(indexOf(ifempty(1.affiliate_url; ""); "https://") = 0; "1"; "0"); "0")'
_PRIO = 'if(1.commercial_priority = "A"; "1"; if(1.commercial_priority = "B"; "1"; "0"))'
F_VERIFIED = "{{%s}}" % _VER
F_QUEUE = "{{if(%s = \"1\"; %s; \"0\")}}" % (_VER, _PRIO)


def respond(mid, x, y, status, body):
    return {"id": mid, "module": "gateway:WebhookRespond", "version": 1, "metadata": meta(x, y), "parameters": {},
            "mapper": {"status": status, "body": body,
                       "headers": [{"key": "Content-Type", "value": "application/json"}]}}


def set_vars(mid, x, variables):
    return {"id": mid, "module": "util:SetVariables", "version": 1, "metadata": meta(x), "parameters": {},
            "mapper": {"variables": [{"name": k, "value": v} for k, v in variables.items()], "scope": "roundtrip"}}


def flag(name, value):
    return {"a": "{{7.%s}}" % name, "o": "text:equal", "b": value}


def intake():
    keep = lambda f: "{{2.%s}}" % f
    data = {
        "product_id": "{{1.product_id}}", "product_name": "{{1.product_name}}", "brand": "{{1.brand}}",
        "category": "{{1.category}}", "market": "DE", "store": "{{1.store}}", "product_url": "{{1.product_url}}",
        "affiliate_url": '{{if(7.verified = "1"; 1.affiliate_url; "")}}',
        "affiliate_network": "{{1.affiliate_network}}",
        "affiliate_status": '{{if(7.verified = "1"; "verified"; if(1.affiliate_status = "verified"; "unverified"; '
                            'ifempty(1.affiliate_status; "unverified")))}}',
        "price_eur": "{{1.price_eur}}", "commission_percent": "{{1.commission_percent}}",
        "estimated_commission_eur": "{{1.estimated_commission_eur}}",
        "cookie_duration_days": "{{1.cookie_duration_days}}", "availability": '{{ifempty(1.availability; "unknown")}}',
        "source_url": "{{1.source_url}}", "video_category": "{{1.video_category}}",
        "matching_klaus_scenario": "{{1.matching_klaus_scenario}}", "video_hook": "{{1.video_hook}}",
        "commercial_priority": '{{if(7.verified = "1"; ifempty(1.commercial_priority; "C"); "HOLD")}}',
        "score": "{{1.score}}", "epm_base_eur": "{{1.epm_scenarios.base}}",
        "disclosure_text": "{{1.disclosure_text}}", "compliance_flags": '{{join(1.compliance_flags; ", ")}}',
        "discovered_at": '{{ifempty(2.discovered_at; ifempty(1.discovered_at; formatDate(now; "YYYY-MM-DD")))}}',
        "verification_date": "{{1.verification_date}}",
        "link_status": '{{ifempty(1.link_status; ifempty(2.link_status; "unchecked"))}}',
        "last_update": "{{now}}",
        "make_status": '{{if(2.product_id; "updated"; "created")}}',
        "content_queue": '{{if(7.queue = "1"; true; false)}}',
        "video_status": '{{if(ifempty(2.video_status; "none") = "none"; if(7.queue = "1"; "queued"; "none"); '
                        '2.video_status)}}',
        "video_url": keep("video_url"), "publication_results": keep("publication_results"),
        "views": keep("views"), "clicks": keep("clicks"), "sales": keep("sales"),
        "confirmed_commission_eur": keep("confirmed_commission_eur"), "refunds": keep("refunds"),
        "notes": "{{1.notes}}",
    }
    # AddRecord не возвращает сохранённые поля, поэтому ответ и уведомление строятся из тех же формул.
    ok_body = ('{"ok": true, "product_id": "{{1.product_id}}", "make_status": "%s", '
               '"affiliate_status": "%s", "priority": "%s", '
               '"content_queue": {{if(7.queue = "1"; "true"; "false")}}, "video_status": "%s", '
               '"affiliate_url_stored": {{if(7.verified = "1"; "true"; "false")}}}'
               % (data["make_status"], data["affiliate_status"], data["commercial_priority"], data["video_status"]))
    # Уведомление уходит только при queue = 1, т.е. ссылка verified и приоритет A/B — значения берём из запроса.
    tg_text = ("🧰 Klaus Affiliate Hunter — новый товар в очереди контента\n\n"
               "{{1.product_name}}{{if(1.brand; \" · \"; \"\")}}{{1.brand}}\n"
               "Приоритет: {{1.commercial_priority}} · score {{1.score}}\n"
               "Цена: {{ifempty(1.price_eur; \"?\")}} € · комиссия {{ifempty(1.commission_percent; \"?\")}} % "
               "≈ {{ifempty(1.estimated_commission_eur; \"?\")}} € за продажу\n"
               "Магазин: {{1.store}} · сеть: {{1.affiliate_network}} · cookie {{ifempty(1.cookie_duration_days; \"?\")}} дн.\n"
               "Сценарий Klaus: {{ifempty(1.matching_klaus_scenario; \"—\")}}\n"
               "Hook: {{ifempty(1.video_hook; \"—\")}}\n\n"
               "Ссылка (проверена {{1.verification_date}}): {{1.affiliate_url}}\n"
               "Пометка в ролике: {{1.disclosure_text}}\n"
               "ID: {{1.product_id}}")
    return {"name": "Klaus Affiliate Hunter — 1. Intake (Prüfung, Dedup, Speichern, Queue)", "metadata": SCEN_META,
            "flow": [
                {"id": 1, "module": "gateway:CustomWebHook", "version": 1, "metadata": meta(0),
                 "parameters": {"hook": HOOK_INTAKE, "maxResults": 1}, "mapper": {}},
                set_vars(7, 300, {"valid": F_VALID, "verified": F_VERIFIED, "queue": F_QUEUE}),
                {"id": 10, "module": "builtin:BasicRouter", "version": 1, "metadata": meta(600), "mapper": None,
                 "routes": [
                     {"flow": [
                         {"id": 2, "module": "datastore:GetRecord", "version": 1, "metadata": meta(900, -150),
                          "parameters": {"datastore": DS}, "mapper": {"key": "{{1.product_id}}", "returnWrapped": False},
                          "filter": {"name": "Pflichtfelder ok", "conditions": [[flag("valid", "1")]]}},
                         {"id": 3, "module": "datastore:AddRecord", "version": 1, "metadata": meta(1200, -150),
                          "parameters": {"datastore": DS},
                          "mapper": {"key": "{{1.product_id}}", "overwrite": True, "data": data}},
                         respond(4, 1500, -150, 200, ok_body),
                         {"id": 5, "module": "telegram:SendReplyMessage", "version": 1, "metadata": meta(1800, -150),
                          "parameters": {"__IMTCONN__": TG_CONN},
                          "mapper": {"chatId": OWNER_CHAT, "text": tg_text, "parseMode": "",
                                     "disableWebPagePreview": True},
                          "filter": {"name": "Neu in Queue", "conditions": [[
                              flag("queue", "1"),
                              {"a": '{{ifempty(2.video_status; "none")}}', "o": "text:equal", "b": "none"}]]},
                          "onerror": [{"id": 51, "module": "builtin:Ignore", "version": 1, "metadata": meta(1800, 0),
                                       "mapper": None}]},
                     ]},
                     {"flow": [
                         respond(6, 900, 150, 400,
                                 '{"ok": false, "error": "product_id, product_name und product_url (http…) sind Pflicht"}')
                         | {"filter": {"name": "Pflichtfelder fehlen", "conditions": [[flag("valid", "0")]]}},
                     ]},
                 ]},
            ]}


def status():
    """Обратная связь: статус видео, ссылки, статистика публикаций и продаж (по product_id)."""
    num = lambda f: "{{ifempty(1.%s; 2.%s)}}" % (f, f)
    data = {
        "video_status": num("video_status"), "video_url": num("video_url"),
        "publication_results": num("publication_results"), "views": num("views"), "clicks": num("clicks"),
        "sales": num("sales"), "confirmed_commission_eur": num("confirmed_commission_eur"), "refunds": num("refunds"),
        "link_status": num("link_status"), "availability": num("availability"), "price_eur": num("price_eur"),
        "verification_date": num("verification_date"),
        "estimated_commission_eur": "{{if(1.price_eur; if(2.commission_percent; "
                                    "round(1.price_eur * 2.commission_percent) / 100; 2.estimated_commission_eur); "
                                    "2.estimated_commission_eur)}}",
        "content_queue": '{{if(7.drop = "1"; false; 2.content_queue)}}',
        "affiliate_url": '{{if(1.link_status = "broken"; ""; 2.affiliate_url)}}',
        "affiliate_status": '{{if(1.link_status = "broken"; "rejected"; 2.affiliate_status)}}',
        "commercial_priority": '{{if(7.drop = "1"; "HOLD"; 2.commercial_priority)}}',
        "notes": "{{ifempty(1.notes; 2.notes)}}", "last_update": "{{now}}",
    }
    sold = '7.new_sales = "1"'
    tg = ("⚠️ Klaus Affiliate Hunter — {{2.product_name}}\n"
          "{{if(1.link_status = \"broken\"; \"Ссылка больше не работает — товар снят с очереди. \"; \"\")}}"
          "{{if(1.availability = \"out_of_stock\"; \"Товара нет в наличии — снят с очереди. \"; \"\")}}"
          "{{if(1.video_status = \"published\"; \"🎬 Видео опубликовано: \"; \"\")}}{{if(1.video_status = \"published\"; 1.video_url; \"\")}}"
          "{{if(%s; \" 💶 Продажи всего: \"; \"\")}}{{if(%s; 1.sales; \"\")}}"
          "{{if(%s; \" · подтверждено, €: \"; \"\")}}{{if(%s; ifempty(1.confirmed_commission_eur; 0); \"\")}}"
          "\nID: {{2.product_id}}") % (sold, sold, sold, sold)
    return {"name": "Klaus Affiliate Hunter — 2. Status & Statistik (Feedback)", "metadata": SCEN_META,
            "flow": [
                {"id": 1, "module": "gateway:CustomWebHook", "version": 1, "metadata": meta(0),
                 "parameters": {"hook": HOOK_STATUS, "maxResults": 1}, "mapper": {}},
                {"id": 2, "module": "datastore:GetRecord", "version": 1, "metadata": meta(300),
                 "parameters": {"datastore": DS}, "mapper": {"key": "{{1.product_id}}", "returnWrapped": False}},
                set_vars(7, 600, {
                    "exists": '{{if(2.product_id; "1"; "0")}}',
                    "drop": '{{if(1.link_status = "broken"; "1"; if(1.availability = "out_of_stock"; "1"; "0"))}}',
                    "new_sales": '{{if(ifempty(1.sales; 0) > ifempty(2.sales; 0); "1"; "0")}}',
                    "published_now": '{{if(1.video_status = "published"; if(2.video_status = "published"; "0"; "1"); "0")}}',
                }),
                {"id": 10, "module": "builtin:BasicRouter", "version": 1, "metadata": meta(900), "mapper": None,
                 "routes": [
                     {"flow": [
                         {"id": 3, "module": "datastore:UpdateRecord", "version": 1, "metadata": meta(1200, -150),
                          "parameters": {"datastore": DS},
                          "mapper": {"key": "{{1.product_id}}", "upsert": False, "overwriteArrays": False, "data": data},
                          "filter": {"name": "Produkt existiert", "conditions": [[flag("exists", "1")]]}},
                         respond(4, 1500, -150, 200,
                                 '{"ok": true, "product_id": "{{1.product_id}}", '
                                 '"content_queue": {{if(7.drop = "1"; "false"; if(2.content_queue; "true"; "false"))}}, '
                                 '"video_status": "{{ifempty(1.video_status; 2.video_status)}}", '
                                 '"link_status": "{{ifempty(1.link_status; 2.link_status)}}"}'),
                         {"id": 5, "module": "telegram:SendReplyMessage", "version": 1, "metadata": meta(1800, -150),
                          "parameters": {"__IMTCONN__": TG_CONN},
                          "mapper": {"chatId": OWNER_CHAT, "text": tg, "parseMode": "", "disableWebPagePreview": True},
                          "filter": {"name": "Wichtiges Ereignis", "conditions": [
                              [flag("drop", "1")], [flag("new_sales", "1")], [flag("published_now", "1")]]},
                          "onerror": [{"id": 51, "module": "builtin:Ignore", "version": 1, "metadata": meta(1800, 0),
                                       "mapper": None}]},
                     ]},
                     {"flow": [
                         respond(6, 1200, 150, 404, '{"ok": false, "error": "unbekannte product_id"}')
                         | {"filter": {"name": "Produkt fehlt", "conditions": [[flag("exists", "0")]]}},
                     ]},
                 ]},
            ]}


if __name__ == "__main__":
    for name, bp in (("intake_blueprint.json", intake()), ("status_blueprint.json", status())):
        json.dump(bp, open(os.path.join(HERE, name), "w"), ensure_ascii=False, indent=1)
        print("ok", name)
