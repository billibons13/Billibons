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

# --- search v3 — ПРЕДЛОЖЕНИЕ тренера (T-0041), в Make НЕ внесено. Внести = обновить запись `search` в lh_settings
# (решение директора; сценарий LH-01 не меняется — regex читается из записи). Причины — ложные пропуски боевого запуска
# LH-01 13.10 14:33 UTC (search v2): «Jet Charter Growth with Claude» (маркетинг, прошёл по «claude») → COLD 41;
# «AI Agent 智能体…｜仅限中国工程师…» (только китайские инженеры) → REJECT 37; офлайн: «обработка/работа» ловились на «бот».
# 1) claude|gpt|openai|llm засчитываются только вместе с признаком разработки (lookahead, JS и Python поддерживают);
# 2) «бот» — только с начала слова: (^|[^а-яё])бот (без lookbehind — работает в любом движке);
# 3) exclude + ограничения по национальности/месту («仅限», «only chinese», «indian developers only», «local only»)
#    и чистый маркетинг (email-кампании, growth/social media marketing, cold outreach).
#    «nur deutschsprachig» НЕ исключается: владелец работает из Германии (Europe/Berlin) — вопрос директору, если нужно иначе.
DEV = r"(bots?|agents?|automation|automate|integrat\w*|api|workflows?|webhooks?|assistants?|chatbots?|pipelines?)"
NAT = r"(chinese|indian|pakistani|bangladeshi|filipino|vietnamese|indonesian|nigerian|kenyan|american|us|uk|local)"
SEARCH_V3 = dict(SEARCH_V2,
    version=3,
    include_regex=(r"\b(telegram|chat ?bots?|bots?|mini ?apps?|make\.com|integromat|n8n|zapier|webhooks?|automation|automate"
                   r"|automatizaci[oó]n|automatisierung|ai agents?|ai assistants?)\b"
                   r"|(^|[^а-яё])бот|автоматиз"
                   r"|^(?=[\s\S]*\b(gpt|llm|openai|claude)\b)(?=[\s\S]*\b" + DEV + r"\b)"),
    exclude_regex=(SEARCH_V2["exclude_regex"] +
                   r"|仅限|只限|限中国|\bonly " + NAT + r"\b|\b" + NAT + r" (engineers?|developers?|freelancers?|candidates?|residents?) only\b"
                   r"|email (marketing|campaigns?)|growth marketing|social media (manager|marketing)|cold (email|outreach)"),
)
SEARCH_V3_TEST = dict(SEARCH_V3, languages=LANGS.split(","))
