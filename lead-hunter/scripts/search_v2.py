"""search v2 (T-0039, решение директора 13.10 по исходным владельца): категории «боты/автоматизация/AI» сейчас;
«сайты» и «изготовление продукции» — после Analyst v3 (иначе промпт Analyst, заточенный под Telegram, их занижает).
Все языки (перевод на русский делает Analyst — поле description_ru). Мин. бюджет 100 € (fixed). max_per_run 2 — ограниченный запуск (кредиты)."""
LANGS = "en,de,ru,uk,es,fr,it,pt,pl,nl,tr,ar,id,hi,zh,ja,ko,vi,th,ro,cs,sk,sv,da,fi,no,el,hu,bg,he,ms,tl,ur,bn,fa,sr,hr,sl,lt,lv,et,ca,sq,az,kk,ka,hy,uz"
SEARCH_V2 = {
    "version": 2,
    # ID категорий Freelancer — все взяты из ответов API 13.10 (jobs[] в выдаче): 2380 Telegram API, 2068 Chatbot, 2918 Bot Development,
    # 2917 AI Chatbot, 2823 Make.com, 2916 AI Chatbot Development, 3377 Chatbot Development, 3380 AI Automation,
    # 3508 AI Workflow Automation, 1977 Automation, 2986 AI Development, 3375 AI Integration
    "jobs_csv": "2380,2068,2918,2917,2823,2916,3377,3380,3508,1977,2986,3375",
    "include_regex": r"\b(telegram|chat ?bots?|bots?|mini ?apps?|make\.com|integromat|n8n|zapier|webhooks?|automation|automate|automatizaci[oó]n|automatisierung|ai agents?|ai assistants?|gpt|llm|openai|claude)\b|бот|автоматиз",
    "exclude_regex": r"translat|instructor|tutor|copywrit|chat admin|virtual assistant|data entry|\bseo\b|moodle|vertriebspartner|sales partner|voice (call|assistant)",
    "languages_csv": LANGS, "countries_csv": "",
    "budget_fixed_min_eur": 100, "budget_hourly_min_eur": 15, "max_bids": 200,
    "window_hours": 12, "max_per_run": 2, "send_grades_csv": "HOT,WARM,COLD",
}
SEARCH_V2_TEST = dict(SEARCH_V2, languages=LANGS.split(","))
