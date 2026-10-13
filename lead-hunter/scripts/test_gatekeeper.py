"""T1: Gatekeeper на реальных проектах Freelancer (хранилище 205357 + выборка API 13.10.2026).
expected — разметка директора: True = тема наша (Telegram/чат-бот/автоматизация), стоит показать Analyst."""
from gatekeeper import gate

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

def run():
    ok = 0; rows = []
    for t, lang, typ, b, bids, desc, exp in CASES:
        got, why = gate({"title": t, "description": desc, "language": lang, "type": typ, "budget_max_eur": b, "bid_count": bids})
        ok += got == exp
        rows.append(("✅" if got == exp else "❌", "PASS" if got else "drop", why, t[:60]))
    for r in rows: print(*r, sep=" | ")
    passed = sum(1 for r in rows if r[1] == "PASS")
    print(f"\nсовпало с разметкой: {ok}/{len(CASES)} · прошло к Analyst: {passed}/{len(CASES)}")
    assert ok == len(CASES), "Gatekeeper расходится с разметкой"

if __name__ == "__main__":
    run()
