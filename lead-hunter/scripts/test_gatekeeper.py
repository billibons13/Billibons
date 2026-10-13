"""T1: Gatekeeper на реальных проектах Freelancer (хранилище 205357 + выборка API 13.10.2026) + расширение T-0041.
expected — разметка директора: True = тема наша (Telegram/чат-бот/автоматизация/AI-интеграция), стоит показать Analyst.
Приёмка: все кейсы совпадают на действующих настройках поиска (SEARCH_V3_TEST — предложение для записи `search`);
исходные 23 кейса дополнительно обязаны совпасть на v1 (DEFAULT_SEARCH) — обратная совместимость.
Запуск: python3 scripts/test_gatekeeper.py (офлайн, 0 операций Make, 0 токенов)."""
from gatekeeper import gate, DEFAULT_SEARCH
from search_v2 import SEARCH_V2_TEST, SEARCH_V3_TEST

CASES = [  # title, lang, type, budget_max_eur, bids, ключевой фрагмент описания, expected
 ("Telegram-Based Production Tracker Upgrade","en","fixed",750,173,"Telegram-based production tracking python-telegram-bot PostgreSQL",True),
 ("Upgrade Moodle & Edwiser","id","fixed",667,21,"upgrade LMS Moodle",False),
 ("Vietnamese to English Translator Required","en","hourly",18,2,"translation",False),
 ("Online CCNA Routing Instructor","en","fixed",1497,22,"certified instructor Enterprise Networking, Security & Automation",False),
 ("Custom Black Cotton Bib Overalls","en","fixed",465,5,"garment maker overalls",False),
 ("Vietnamese Health Blog Translation","en","hourly",18,15,"translate the text",False),
 ("Customizable Live Chat System Development","en","fixed",345,66,"live chat optional AI chatbot like telegram windows app",True),
 ("Mobile Subscription Site with Telegram Integration: Irish League Edge","en","fixed",916,132,"paid Telegram channel access automated",True),
 ("Penjawab Chat Produk Freelance","id","hourly",22,16,"menjawab chat pelanggan",False),
 ("End-to-End B2B Quotation Automation","en","fixed",1339,104,"Make.com & AI Automation Architect Claude Gmail WhatsApp",True),
 ("Ai sales booster","en","fixed",346,43,"AI Voice Calling SaaS Shopify COD voice call",False),
 ("Custom Bot for Collectibles - 10/10/2026 07:00 EDT","en","fixed",6235,96,"purchasing bot web automation",True),
 ("Balas Chat Informasi Harga","id","hourly",22,2,"merespons chat",False),
 ("Asynchronous Consulting Business Model Development","en","fixed",1773,98,"Zapier or Make.com webhooks",True),
 ("Customer Support Voice Assistant AI","en","fixed",2309,31,"conversational AI voice assistant TTS STT",False),
 ("Bot WhatsApp Respuestas Automáticas","es","hourly",22,88,"asistente virtual WhatsApp bot automáticos",True),
 ("Kooperationspartner/Vertriebspartner Software Business Booster","de","fixed",1501,18,"Vertriebspartner gesucht KI",False),
 ("Diseño Web Logístico + SEO/AEO","es","fixed",670,124,"sitio web SEO chat en vivo",False),
 ("WhatsApp Chat Admin & Script","en","hourly",22,24,"dedicated chat admin reply script",False),
 ("Bantuan Menulis Pesan Penjualan","id","hourly",50,1,"menulis pesan chat",False),
 ("SEO-Driven AI Lead Generation","en","fixed",131,59,"smart, well-structured SEO",False),
 ("Claude AI Business Automation Setup","en","hourly",6,163,"step-by-step guidance Claude automation",False),
 ("Admin Live Chat Website Responsif","id","hourly",15,44,"admin chat",False),
]

# T-0041: новые кейсы. Метка в конце — что проверяет кейс.
NEW_CASES = [  # title, lang, type, budget_max_eur, bids, описание, expected, метка
 # реальные ложные пропуски боевого запуска LH-01 13.10 14:33 UTC (search v2) — Analyst дал COLD 41 и REJECT 37
 ("Jet Charter Growth with Claude","en","fixed",900,35,"growth marketing for a private jet charter company: email campaigns, LinkedIn content and newsletters written with Claude",False,"real-FP: claude без разработки"),
 ("AI Agent 智能体与自动化工作流开发｜仅限中国工程师｜长期项目外包合作","zh","hourly",27,12,"AI Agent 自动化工作流 开发 仅限中国工程师 长期合作",False,"real-FP: ограничение по национальности"),
 ("Blog articles with Claude","en","fixed",300,14,"we need 10 blog posts for our travel agency, drafted with Claude",False,"claude без признака разработки → нет темы"),
 ("WhatsApp bot — Indian developers only","en","fixed",400,40,"whatsapp bot for clinic, indian developers only",False,"ограничение по национальности (en)"),
 # бюджет 100–300 € (новый порог владельца 100 € fixed) и разные языки
 ("Telegram-бот для записи клиентов в салон","ru","fixed",150,7,"нужен бот в телеграм: запись, напоминания, админка",True,"ru, кириллица «бот», 150 €"),
 ("Бот для Telegram-каналу: автопостинг","uk","fixed",250,4,"потрібен бот для автопостингу в канал",True,"uk, кириллица, 250 €"),
 ("Développement d'un bot Telegram pour restaurant","fr","fixed",280,9,"réservations et menu du jour dans Telegram",True,"fr — новый язык v2, 280 €"),
 ("Automatización de pedidos con n8n","es","fixed",120,15,"automatización de pedidos de Shopify a Google Sheets con n8n",True,"es, 120 €"),
 ("Rechnungen automatisch mit Make.com verarbeiten","de","hourly",25,6,"Automatisierung: Rechnungen aus Gmail in Lexoffice via Make.com",True,"de hourly 25 €/ч"),
 ("开发Telegram机器人","zh","fixed",500,20,"需要Telegram机器人 自动回复",True,"zh без пробелов: \\b как в JS (ASCII)"),
 ("Claude API integration for support inbox","en","fixed",600,30,"integrate Claude API into our helpdesk workflow",True,"claude + признак разработки"),
 # пограничные значения
 ("Telegram bot for orders","en","fixed",99,3,"simple order bot",False,"граница: 99 € < 100"),
 ("Telegram bot for orders v2","en","fixed",100,3,"simple order bot",True,"граница: ровно 100 €"),
 ("Zapier automation fix","en","hourly",14,3,"fix zapier zap",False,"граница hourly 14 < 15"),
 ("Zapier automation fix 2","en","hourly",15,3,"fix zapier zap",True,"граница hourly ровно 15"),
 ("Telegram mini app MVP","en","fixed",1500,200,"mini app with payments",True,"граница: ставок ровно 200"),
 ("Telegram mini app MVP 2","en","fixed",1500,201,"mini app with payments",False,"граница: ставок 201"),
 # мусор и неполные данные
 ("Обработка фотографий для каталога","ru","fixed",200,5,"работа на дому, обработка 300 фото",False,"кириллица: «бот» внутри «обработка/работа»"),
 ("Robot arm calibration","en","fixed",2000,4,"industrial robots calibration on site",False,"«robots» ≠ bots (\\b)"),
 ("Telegram bot + SEO texts","en","fixed",400,10,"bot and seo articles",False,"exclude важнее include"),
 ("Python tutor for automation","en","hourly",20,8,"tutor me in python automation",False,"exclude: tutor"),
 ("","en","fixed",500,0,"",False,"пустой текст"),
 ("Telegram bot","xx","fixed",500,0,"bot",False,"неизвестный язык"),
 ("Telegram bot","en",None,500,0,"bot",False,"нет типа бюджета (в Make не проходит ни одна ветка)"),
 ("Telegram bot","en","fixed",None,0,"bot",False,"нет бюджета → 0 €"),
]

ALL = [c + ("исходный",) for c in CASES] + NEW_CASES

def check(settings, cases, label, must=True):
    ok = tp = fp = fn = 0; bad = []
    for t, lang, typ, b, bids, desc, exp, tag in cases:
        got, why = gate({"title": t, "description": desc, "language": lang, "type": typ, "budget_max_eur": b, "bid_count": bids}, settings)
        ok += got == exp; tp += got and exp; fp += got and not exp; fn += exp and not got
        if got != exp: bad.append((t[:55], why, tag))
    prec = tp / (tp + fp) if tp + fp else 1.0; rec = tp / (tp + fn) if tp + fn else 1.0
    print(f"{label}: совпало {ok}/{len(cases)} ({100*ok/len(cases):.0f} %) · precision {prec:.2f} · recall {rec:.2f}")
    for r in bad: print("   ❌", *r, sep=" | ")
    if must: assert ok == len(cases), label + ": Gatekeeper расходится с разметкой"
    return ok, len(cases)

def js_parity(settings):
    """Make считает regex движком JavaScript. Если есть node — сверяем include/exclude JS vs Python на всех кейсах (0 расхождений)."""
    import json, re, shutil, subprocess
    if not shutil.which("node"):
        print("JS-паритет: node не найден — пропуск"); return
    texts = [((t or "") + " " + (d or "")[:2000]).lower() for t, _l, _ty, _b, _bi, d, _e, _tag in ALL]
    js = ("const S=%s,T=%s;console.log(JSON.stringify(T.map(t=>[new RegExp(S.i).test(t),new RegExp(S.e).test(t)])))"
          % (json.dumps({"i": settings["include_regex"], "e": settings["exclude_regex"]}), json.dumps(texts, ensure_ascii=False)))
    out = json.loads(subprocess.run(["node", "-e", js], capture_output=True, text=True, check=True).stdout)
    diff = [t[:50] for (i, e), t in zip(out, texts)
            if (i, e) != (bool(re.search(settings["include_regex"], t, re.A)), bool(re.search(settings["exclude_regex"], t, re.A)))]
    print(f"JS-паритет regex (v{settings['version']}): расхождений {len(diff)} из {len(texts)}", diff or "")
    assert not diff, "regex ведёт себя в JS (Make) иначе, чем в Python"

def run():
    for t, lang, typ, b, bids, desc, exp, tag in ALL:
        got, why = gate({"title": t, "description": desc, "language": lang, "type": typ, "budget_max_eur": b, "bid_count": bids}, SEARCH_V3_TEST)
        print("✅" if got == exp else "❌", "PASS" if got else "drop", why, t[:60], sep=" | ")
    print()
    check(DEFAULT_SEARCH, [c + ("исходный",) for c in CASES], "v1 исходные 23 (совместимость)")
    check(SEARCH_V2_TEST, ALL, "v2 (сейчас в Make) — справочно", must=False)
    js_parity(SEARCH_V3_TEST)
    return check(SEARCH_V3_TEST, ALL, "v3 (предложение) — ПРИЁМКА")

if __name__ == "__main__":
    run()
