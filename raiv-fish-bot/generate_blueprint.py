import json, re
CONN = 11456488  # RAIV_Fish Telegram Bot
GROUP = "-1004438320479"  # канал RAIVFISH
HOOK = 3818482  # v2 webhook (рабочий)
cats = [
 ("a","🐟 Икра вяленая (100 г)",[("Икра толстолоба","6",1),("Икра кеты","8.5",1),("Икра форели","8.5",1),("Икра судака","6.5",0),("Икра щуки","7",1),("Икра плотвы","7",0),("Икра минтая","6.5",0)]),
 ("b","🐠 Рыба вяленая (кг)",[("Плотва с икрой","35",1),("Чищенные тушки плотвы без головы (100% икра)","49",1),("Вобла с икрой (80% икра)","30",1),("Верховодка","35",1),("Лещ с икрой","35",1),("Лещ без икры","20",0),("Карась с икрой","23",1),("Щука потрошеная","25",1),("Форель вяленая потрошеная","35",1),("Судак потрошеный","30",1),("Чехонь","25",1),("Чехонь крупная с икрой 90%","35",1),("Бычок","34",1),("Корюшка с икрой (премиум)","60",0),("Окунь с икрой","34",1),("Юкола лосося","67",1)]),
 ("c","🍢 Рыбные снеки (100 г)",[("Филе горбуши (соломка)","6",1),("Кальмар + лосось (соломка)","4.9",1),("Корюшка сушеная потрошеная","5.5",1),("Соломка леща","3.5",1),("Джерки лосося","6",1),("Ириска из лосося","6",1),("Стейк щуки","4.5",1)]),
 ("d","🦑 Снеки к пиву (кг)",[("Пятачки осьминога","40",1),("Паутинка кальмара «сладкий чили»","40",1),("Кальмар по-шанхайски","40",1),("Стружка кальмара","40",1),("Палочки патасу","40",1),("Филе голубого марлина","40",1),("Кальмар по-перуански","40",1),("Полосатик","40",1),("Стружка краба","40",1),("Анчоус","40",1),("Крабовые палочки","40",1)]),
 ("e","🥫 Консервы",[("Снеток в томате","5",1),("Лещ в томате","5",1)]),
]
UNIT = {"a":"g","b":"k","c":"g","d":"k","e":"p"}
ULBL = {"a":"€ / 100 г","b":"€ / кг","c":"€ / 100 г","d":"€ / кг","e":"€ / шт."}
QTY = {"a":["100","200","300","500"],"b":["0.5","1","1.5","2"],"c":["100","200","300","500"],"d":["0.2","0.3","0.5","1"],"e":["1","2","3","5"]}
QL = {"g":"г","k":"кг","p":"шт."}
HINT = {"g":"в граммах, например 250","k":"в кг, например 0,7","p":"в штуках, например 4"}
DS = 203268  # data store «RAIV_Fish — корзины покупателей»
CUST = 203277   # клиенты: база, бонусы, история
ORD = 203280    # все заказы
PROMO = 203278  # промокоды (/promo) и КАТАЛОГ: записи cat_<код> — цена, наличие (владелец: /price, /stock)
CATALOG_API = "https://hook.eu1.make.com/hzm5bgeixv8k4652x3ofaaxw378nwyhu"  # сценарий 7708101: цены и наличие для витрины
STATS = 203279  # продажи по дням (для ежедневного отчёта)
OWNER_ID = "6883357001"  # владелец магазина: команды /admin /promo /send /report
BONUS_PCT = 5   # начисление бонусов, % от суммы к оплате
BONUS_CAP = 20  # бонусами можно оплатить не больше этого % заказа
TZ = "Europe/Berlin"
MIN_ORDER = 20   # минимальная сумма заказа, €
MAX_KG, MAX_G, MAX_PCS = 10, 5000, 50   # лимиты «Своего веса»: кг, граммы, штуки
PROMO_MAX = 50                       # /promo: скидка не больше 50 %
STRIPE_PUBLIC = False                # тестовый ключ Stripe — кнопку оплаты видит только владелец
REF_BONUS = 3    # «приведи друга»: бонус другу сразу и пригласившему после первого заказа друга
BOT_USER = "RAIV_FISH_bot"
WEBAPP = "https://billibons13.github.io/Billibons/?v=9"  # ?v= — сброс кэша Telegram Desktop  # Mini App витрина: ветка gh-pages (собирается из miniapp/, generate_miniapp.py)
WEBAPP_V = "2"  # поднять, чтобы заново выдать кнопку витрины всем клиентам
STRIPE_CONN = 11458868  # Stripe (test) — онлайн-оплата (Pro)
BOT_URL = "https%3A%2F%2Ft.me%2FRAIV_FISH_bot"
items = {}
for c,_,lst in cats:
    for i,(n,p,s) in enumerate(lst,1): items[f"{c}{i}"]=(n,p,s)

# ---- module 90: unify callback / custom-weight reply into one "d" string + chat id
RT = 'ifempty(1.message.reply_to_message.text; "")'
IS_W = f'contains({RT}; "✏️ Свой вес")'
W_CODE = f'trim(last(split({RT}; "код:")))'
W_TXT = 'lower(trim(ifempty(1.message.text; "")))'
W_NUM = 'parseNumber(replace(replace(replace(replace(replace('+W_TXT+'; "кг"; ""); "шт"; ""); "г"; ""); " "; ""); ","; "."); ".")'
W_UNIT = 'if(contains('+W_TXT+'; "кг"); "k"; if(contains('+W_TXT+'; "г"); "g"; ""))'
W_CAT = 'substring('+W_CODE+'; 0; 1)'
# «700 г» в разделе «кг» → 0,7 кг; «1 кг» в разделе «100 г» → 1000 г
W_QTY = ('switch('+W_CAT+'; "b"; if('+W_UNIT+' = "g"; '+W_NUM+' / 1000; '+W_NUM+'); "d"; if('+W_UNIT+' = "g"; '+W_NUM+' / 1000; '+W_NUM+'); '
         '"a"; if('+W_UNIT+' = "k"; '+W_NUM+' * 1000; '+W_NUM+'); "c"; if('+W_UNIT+' = "k"; '+W_NUM+' * 1000; '+W_NUM+'); '+W_NUM+')')
d_val = ("{{1.callback_query.data}}"
         + "{{if(" + IS_W + '; "q|"; "")}}'
         + "{{if(" + IS_W + "; " + W_CODE + '; "")}}'
         + "{{if(" + IS_W + '; "|"; "")}}'
         + "{{if(" + IS_W + "; " + W_QTY + '; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/orders"; "h"; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/invite"; "rf"; "")}}'
         + '{{if(ifempty(1.message.text; "") = "/contacts"; "cn"; "")}}')
unify = [{"name":"d","value":d_val},
         {"name":"chat","value":"{{1.callback_query.message.chat.id}}{{1.message.chat.id}}"}]

def D(n): return f'get(split(90.d; "|"); {n})'
pref = f'substring(ifempty({D(2)}; "x"); 0; 1)'
IN_STOCK = '{{if(99.stock; "1"; "0")}}'
sw_name = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[0]}"' for k,v in items.items()) + '; "")'
sw_price = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[1]}"' for k,v in items.items()) + '; "0")'
div = f'switch({pref}; "a"; 100; "c"; 100; 1)'
qunit = f'switch({pref}; "a"; "г"; "c"; "г"; "e"; "шт."; "кг")'
Q2 = f'parseNumber(ifempty({D(3)}; "0"); ".")'
LIM = f'switch({pref}; "a"; {MAX_G}; "c"; {MAX_G}; "e"; {MAX_PCS}; {MAX_KG})'  # больше лимита → «Не понял количество»
variables = [
 {"name":"name","value":"{{99.name}}"},
 {"name":"price","value":"{{ifempty(99.price; 0)}}"},
 {"name":"ulabel","value":"{{"+f'switch({pref}; "a"; "€ / 100 г"; "c"; "€ / 100 г"; "e"; "€ / шт."; "€ / кг")'+"}}"},
 {"name":"qlabel","value":"{{"+f'replace(ifempty({D(3)}; ""); "."; ",")'+"}} {{"+qunit+"}}"},
 {"name":"total","value":"{{"+f'ifempty(99.price; 0) * {Q2} / {div} * if({Q2} > {LIM}; 0; 1)'+"}}"},
 {"name":"kg","value":"{{"+f'switch({pref}; "a"; {Q2} / 1000; "c"; {Q2} / 1000; "e"; 0; {Q2})'+"}}"},
 {"name":"pcs","value":"{{"+f'if({pref} = "e"; {Q2}; 0)'+"}}"},
 {"name":"hint","value":"{{"+f'switch({pref}; "a"; "{HINT["g"]}"; "c"; "{HINT["g"]}"; "e"; "{HINT["p"]}"; "{HINT["k"]}")'+"}}"},
]
# ---- main menu text
SELLER = "@esusnob"  # продавец бота
OFFER_BTN = [{"text":"💼 Хочу такой бот для своего бизнеса","callback_data":"p"}]
offer = """💼 Такой бот — для вашего магазина

Этот бот принимает заказы сам: каталог с наличием, корзина, свой вес, расчёт суммы, адрес и телефон. Готовый заказ с маршрутом приходит в ваш Telegram-канал. Работает 24/7.

📦 ПАКЕТЫ
• Start — 350 €
каталог, корзина, доставка, заказ в канал, учёт остатков
• Business — 800 € ⭐
+ база клиентов, рассылки, акции, промокоды, бонусы, ежедневный отчёт
• Pro — 1 500 €
+ AI-помощник по продажам и остаткам, подключение внешних сервисов

🛠 ОБСЛУЖИВАНИЕ
• Базовое — 25 €/мес (250 €/год)
• Полное — 39 €/мес (390 €/год)
🎁 Start + 6 мес. обслуживания — 440 € вместо 500 €

➕ Онлайн-оплата (Apple Pay, Google Pay, карты, PayPal) — 150 €

Запуск Start за 1–2 дня: ваше название, логотип, цены и города. 50% предоплата, остальное после тестового заказа.

Попробуйте сами: соберите корзину и оформите пробный заказ.
Вопросы и заказ бота: @esusnob 👇"""
menu = """📋 ВЕСЬ ПРАЙС RAIV FISH
То, что отмечено ❌, — сейчас нет в наличии.

"""
for c,title,lst in cats:
    menu += title.upper() if c!="e" else "🥫 КОНСЕРВЫ"
    menu += "\n"
    for n,p,s in lst:
        menu += f"• {n} — {p.replace('.',',')} {ULBL[c]}" + ("❌" if not s else "") + "\n"
    menu += "\n"
menu += "🚗 Доставка бесплатно от "+str(MIN_ORDER)+" €: Эдделак, Марне, Брунсбюттель, Хайде\nВыберите раздел 👇"
start_text = ("🐟 RAIV FISH — вяленая рыба, икра и снеки к пиву\n\n"
 "🚗 Бесплатная доставка от "+str(MIN_ORDER)+" €: Эдделак, Марне, Брунсбюттель, Хайде\n"
 "🕐 Сегодня или завтра — днём или вечером\n"
 "💳 Онлайн или наличными · 💎 "+str(BONUS_PCT)+"% бонусами с каждого заказа\n\n"
 "Выберите раздел 👇")
SERVICE_ROWS = [[{"text":"📋 Весь прайс","callback_data":"pl"},{"text":"🔁 Повторить заказ","callback_data":"r"}],
                [{"text":"📜 Мои заказы","callback_data":"h"},{"text":"🎟 Промокод","callback_data":"pr"}],
                [{"text":"🎁 Приведи друга — 3 € обоим","callback_data":"rf"},{"text":"📇 Контакты","callback_data":"cn"}]]
cat_kb = lambda mode: {"inline_keyboard":[[{"text":t,"callback_data":f"k|{c}|{mode}"}] for c,t,_ in cats]+(SERVICE_ROWS+[OFFER_BTN] if mode=="s" else [])}
T = {}
def ph(expr):
    k=f"@@{len(T)}@@"; T[k]=expr; return k
def body(obj):
    s=json.dumps(obj,ensure_ascii=False)
    for k,v in T.items():
        s=s.replace(f'"{k}"',v).replace(k,v)
    return s
def meta(x,y): return {"designer":{"x":x,"y":y}}
def resp(mid, x, y, name, conds, obj):
    m={"id":mid,"mapper":{"body":body(obj),"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(x,y),"parameters":{}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
SAFE_SEND={103,104,143,175,184,193,194,195,196}
def api(mid, x, y, method, spec, name=None, conds=None, onerror=False):
    m={"id":mid,"mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":k,"value":v} for k,v in spec],"urlMethod":method},
       "module":"telegram:UniversalAPICall","version":1,"metadata":meta(x,y),"parameters":{"__IMTCONN__":CONN}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    if mid in SAFE_SEND: onerror=True  # клиент мог заблокировать бота — не роняем сценарий
    if onerror: m["onerror"]=[{"id":mid+500,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":meta(x,y+300)}]
    return m
def ds(mid, x, y, module, mapper, name=None, conds=None, store=None):
    m={"id":mid,"mapper":mapper,"module":f"datastore:{module}","version":1,"metadata":meta(x,y),"parameters":{"datastore":store or DS}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
def sv(mid, x, y, pairs): return {"id":mid,"mapper":{"variables":[{"name":k,"value":v} for k,v in pairs],"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(x,y),"parameters":{}}
def search(mid, x, y, store, flt, name=None, conds=None, limit=1000):
    m={"id":mid,"mapper":{"filter":flt,"sort":[]},"module":"datastore:SearchRecord","version":1,"metadata":meta(x,y),"parameters":{"datastore":store,"continueWhenNoRes":True,"limit":limit}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
def router(mid, x, y, routes): return {"id":mid,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(x,y),"routes":[{"flow":r} for r in routes]}
def eq(a,b): return {"a":"{{"+a+"}}","b":b,"o":"text:equal"}
# кавычки внутри формул {{...}} не экранируем — иначе Make получит \".\" вместо "."
KB = lambda rows: re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"', '"'), json.dumps({"inline_keyboard":rows},ensure_ascii=False))
CHAT="{{90.chat}}"; MID="{{1.callback_query.message.message_id}}"
routes=[]
chat=ph("{{1.message.chat.id}}")
CMDS = ["/admin","/promo","/send","/report","/stop","/orders","/help","/invite","/price","/stock","/catalog","/sklad","/contacts"]
REFC = '{{replace(trim(1.message.text); "/start ref_"; "")}}'
IS_TEXT = [{"a":"{{1.message.text}}","o":"exist"},{"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}]
FMT = lambda e: "{{formatNumber("+e+'; 2; ","; ".")}}'
RET = "ifempty(101.orders; 0) > 0"
greet = ph('{{if('+RET+'; "👋 С возвращением! Ваши бонусы: 💎 "; "")}}{{if('+RET+'; formatNumber(ifempty(101.bonus; 0); 2; ","; "."); "")}}{{if('+RET+'; " €\\n\\n"; "")}}')
routes.append([
 ds(100,900,-1100,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}}","username":"{{1.message.from.username}}","last_seen":"{{now}}"}},"Меню",
    [IS_TEXT+[{"a":"{{1.message.text}}","b":c,"o":"text:notstartwith"} for c in CMDS+["/start c_"]]],store=CUST),
 ds(101,1200,-1100,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 resp(4,1500,-1100,None,None,{"method":"sendMessage","chat_id":chat,"text":greet+start_text,"reply_markup":cat_kb("s")}),
 router(108,1800,-1100,[[
 ds(102,2100,-1100,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"ref":REFC,"bonus":"{{ifempty(101.bonus; 0) + "+str(REF_BONUS)+"}}"}},"Новый по приглашению",
    [[{"a":"{{1.message.text}}","b":"/start ref_","o":"text:startwith"},{"a":"{{ifempty(101.orders; 0)}}","b":"0","o":"number:equal"},{"a":"{{101.ref}}","o":"notexist"},{"a":REFC,"b":CHAT,"o":"text:notequal"}]],store=CUST),
 api(103,2100,-1100,"sendMessage",[("chat_id",CHAT),("text","🎁 Вам начислено "+str(REF_BONUS)+" € бонусами по приглашению друга! Они спишутся при первом заказе.")]),
 api(104,2400,-1100,"sendMessage",[("chat_id",REFC),("text","👋 По вашей ссылке пришёл новый покупатель. Когда он сделает первый заказ, вам начислится "+str(REF_BONUS)+" € бонусами.")],onerror=True)],
 [api(109,2100,-800,"sendMessage",[("chat_id",CHAT),("text","🛍 Новинка: витрина с фото! Кнопка «🛍 Витрина» теперь всегда внизу чата — выбирайте товары по фото, корзина соберётся сама."),
   ("reply_markup",json.dumps({"keyboard":[[{"text":"🛍 Витрина","web_app":{"url":WEBAPP},"style":"primary"}]],"resize_keyboard":True,"is_persistent":True},ensure_ascii=False))],
   "Кнопка витрины ещё не выдана",[[{"a":"{{101.kb}}","b":WEBAPP_V,"o":"text:notequal"}]],onerror=True),
  ds(98,2400,-800,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"kb":WEBAPP_V}},store=CUST)]])])
TOUCH_CUST = lambda mid,x,y,name,conds: ds(mid,x,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"last_seen":"{{now}}"}},name,conds,store=CUST)
cbchat=ph("{{1.callback_query.message.chat.id}}"); cbmid=ph(MID)
routes.append([resp(5,900,-700,"Разделы",[[eq(D(1),"m")]],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"Выберите раздел 👇","reply_markup":cat_kb("e")})])
routes.append([resp(30,900,-600,"Предложение",[[eq(D(1),"p")]],
  {"method":"sendMessage","chat_id":cbchat,"text":offer,"reply_markup":{"inline_keyboard":[
    [{"text":"💬 Написать продавцу","url":"https://t.me/esusnob"}],
    [{"text":"🛒 Попробовать заказ","callback_data":"m"}]]}})])
# весь прайс
PL_LINE = ('{{switch(213.data.cat; "a"; "🐟"; "b"; "🐠"; "c"; "🍢"; "d"; "🦑"; "🥫")}} {{213.data.name}} — {{replace(toString(213.data.price); "."; ",")}} {{'
  +'switch(213.data.cat; "a"; "€ / 100 г"; "c"; "€ / 100 г"; "e"; "€ / шт."; "€ / кг")'+'}}{{if(213.data.stock; ""; " ❌")}}')
routes.append([search(213,900,-2400,PROMO,[[{"a":"item","o":"exist"}]],"Весь прайс",[[eq(D(1),"pl")]],limit=100),
  {"id":214,"mapper":{"line":PL_LINE},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,-2400),"parameters":{"feeder":213},
   "filter":{"name":"Товар","conditions":[[{"a":"{{213.data.item}}","o":"exist"}]]}},
  api(105,1500,-2400,"sendMessage",[("chat_id",CHAT),("text","📋 ВЕСЬ ПРАЙС RAIV FISH\n❌ — сейчас нет в наличии\n\n{{join(map(214.array; \"line\"); \"\n\")}}\n\n🚗 Доставка бесплатно от "+str(MIN_ORDER)+" €: Эдделак, Марне, Брунсбюттель, Хайде\nВыберите раздел 👇"),("reply_markup",KB(cat_kb("s")["inline_keyboard"][:len(cats)]))])])
# приведи друга
REFLINK = "https://t.me/"+BOT_USER+"?start=ref_{{90.chat}}"
routes.append([api(106,900,-2300,"sendMessage",[("chat_id",CHAT),("text","🎁 Приведи друга — получите оба по "+str(REF_BONUS)+" €\n\nВаша личная ссылка:\n"+REFLINK+"\n\nДруг получает "+str(REF_BONUS)+" € бонусами сразу, вы — после его первого заказа."),
   ("reply_markup",'{"inline_keyboard":[[{"text":"📤 Отправить другу","url":"https://t.me/share/url?url={{encodeURL(\"https://t.me/'+BOT_USER+'?start=ref_\")}}{{90.chat}}&text={{encodeURL(\"Вяленая рыба и снеки с доставкой — держи 3 € на первый заказ 🐟\")}}"}],[{"text":"📋 К покупкам","callback_data":"m"}]]}')],"Приведи друга",[[eq(D(1),"rf")]])])
# контакты и медиа (новые ссылки — строкой в CONTACT_LINKS: подпись, url)
CONTACT_LINKS = [
  ("🎵 TikTok — видео", "https://www.tiktok.com/@vasya_raivfish"),
  ("📸 Instagram — фото", "https://www.instagram.com/vasya_ivanchuk_/"),
  ("👍 Facebook", "https://www.facebook.com/share/1K6wTjKZx9/"),
  ("📣 Telegram-канал @raiv_fish1", "https://t.me/raiv_fish1"),
  ("🐟 Поставщик — Василий", "https://t.me/vasyaivancuk"),
  ("💬 Написать продавцу", "https://t.me/"+SELLER.lstrip("@")),
]
CONTACT_TEXT = ("📇 Контакты RAIV FISH\n\n"
 "🐟 Рыба и икра — от поставщика из Эстонии: @vasyaivancuk\n"
 "🎬 Видео, фото и новинки — TikTok, Instagram, Facebook и канал @raiv_fish1\n"
 "💬 Вопросы по заказу — "+SELLER+"\n\n"
 "🚗 Доставка бесплатно от "+str(MIN_ORDER)+" €: Эдделак, Марне, Брунсбюттель, Хайде")
routes.append([api(266,900,-2250,"sendMessage",[("chat_id",CHAT),("text",CONTACT_TEXT),
   ("reply_markup",json.dumps({"inline_keyboard":[[{"text":t,"url":u}] for t,u in CONTACT_LINKS]+[[{"text":"📋 К покупкам","callback_data":"m"}]]},ensure_ascii=False))],"Контакты",[[eq(D(1),"cn")]])])
# помощь
routes.append([resp(107,900,-2200,"/help",[[IS_TEXT[1],{"a":"{{1.message.text}}","b":"/help","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,
  "text":"ℹ️ Как заказать\n1. /start → раздел → товар → вес (или «✏️ Свой вес»)\n2. «🧺 Корзина / оформить» → город → время → адрес → телефон\n3. Оплатите онлайн по кнопке или наличными курьеру\n\nДоставка бесплатно от "+str(MIN_ORDER)+" €. С каждого заказа — "+str(BONUS_PCT)+"% бонусами.\n\n/orders — мои заказы и бонусы\n/invite — приведи друга\n/contacts — контакты, канал и медиа\n/stop — не получать рассылки\nВопросы: "+SELLER})])
# повторить прошлый заказ
routes.append([TOUCH_CUST(110,900,-2000,"Повторить заказ",[[eq(D(1),"r")]]),
 ds(111,1200,-2000,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 router(112,1500,-2000,[
  [ds(113,1800,-2000,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":"{{111.last_text}}","total":"{{111.last_total}}","count":"{{111.last_count}}","kg":"{{ifempty(111.last_kg; 0)}}","pcs":"{{ifempty(111.last_pcs; 0)}}"}},"Есть прошлый заказ",[[{"a":"{{ifempty(111.last_count; 0)}}","b":"0","o":"number:greater"}]]),
   api(114,2100,-2000,"sendMessage",[("chat_id",CHAT),("text","🔁 Корзина как в прошлый раз:\n{{111.last_text}}💶 Итого: "+FMT("111.last_total")+" €\n\nМожно добавить ещё товары или сразу оформить."),("reply_markup","@@CARTBTNS@@")])],
  [api(115,1800,-1800,"sendMessage",[("chat_id",CHAT),("text","Прошлых заказов пока нет. Выберите товары 👇"),("reply_markup","@@EMPTYKB@@")],"Нет заказов",[[{"a":"{{ifempty(111.last_count; 0)}}","b":"0","o":"number:lessorequal"}]])]])])
# мои заказы и бонусы
routes.append([TOUCH_CUST(116,900,-1700,"Мои заказы",[[eq(D(1),"h")]]),
 ds(117,1200,-1700,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 api(118,1500,-1700,"sendMessage",[("chat_id",CHAT),("text","📜 Ваши заказы\n\n{{ifempty(117.history; \"Пока заказов нет.\")}}\n\n💎 Бонусы: "+FMT("ifempty(117.bonus; 0)")+" €\nЗа каждый заказ начисляем "+str(BONUS_PCT)+"% бонусами. При оформлении они списываются автоматически — до "+str(BONUS_CAP)+"% суммы заказа."),
   ("reply_markup",KB([[{"text":"🔁 Повторить прошлый заказ","callback_data":"r"}],[{"text":"📋 К покупкам","callback_data":"m"}]]))])])
# промокод: вопрос
routes.append([resp(119,900,-1500,"Промокод — вопрос",[[eq(D(1),"pr")]],
  {"method":"sendMessage","chat_id":cbchat,"text":"🎟 Промокод\n\nОтветьте на это сообщение: напишите промокод.","reply_markup":{"force_reply":True,"input_field_placeholder":"Например FISH10"}})])
# промокод: ответ
PCODE = "{{upper(trim(1.message.text))}}"
routes.append([search(160,900,-1300,PROMO,[[{"a":"code","o":"text:equal","b":PCODE}]],"Промокод — ответ",[[{"a":"{{1.message.reply_to_message.text}}","b":"🎟 Промокод","o":"text:contain"}]],limit=1),
 router(161,1200,-1300,[
  [ds(162,1500,-1300,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"promo":"{{160.data.percent}}","pcode":PCODE}},"Действует",[[{"a":"{{ifempty(160.data.percent; 0)}}","b":"0","o":"number:greater"}]]),
   api(163,1800,-1300,"sendMessage",[("chat_id",CHAT),("text","✅ Промокод "+PCODE+" принят: скидка {{160.data.percent}}% на этот заказ.\nСкидка появится при оформлении."),("reply_markup",KB([[{"text":"📋 Выбрать товары","callback_data":"m"}],[{"text":"🧾 Оформить заказ","callback_data":"o"}]]))])],
  [api(164,1500,-1100,"sendMessage",[("chat_id",CHAT),("text","❌ Промокод «{{trim(1.message.text)}}» не найден или уже не действует."),("reply_markup",KB([[{"text":"🎟 Ввести другой","callback_data":"pr"}],[{"text":"📋 К покупкам","callback_data":"m"}]]))],"Нет такого",[[{"a":"{{ifempty(160.data.percent; 0)}}","b":"0","o":"number:lessorequal"}]])]])])
y=-500
CAT_TITLE = "switch("+D(2)+"; "+"; ".join(f'"{c}"; "{t}"' for c,t,_ in cats)+'; "Каталог")'
UL_OF = lambda e: 'switch('+e+'; "a"; "€ / 100 г"; "c"; "€ / 100 г"; "e"; "€ / шт."; "€ / кг")'
catbtn = '[{"text":"{{210.data.name}} — {{replace(toString(210.data.price); "."; ",")}} {{'+UL_OF("210.data.cat")+'}}","callback_data":"f|{{210.data.item}}"}]'
cat_body = ('{"method":"{{if('+D(3)+' = "e"; "editMessageText"; "sendMessage")}}","chat_id":{{1.callback_query.message.chat.id}},'
  '"message_id":{{1.callback_query.message.message_id}},"text":"{{'+CAT_TITLE+'}}\\n\\nВыберите товар 👇",'
  '"reply_markup":{"inline_keyboard":[{{join(map(211.array; "btn"); ",")}}{{if(length(211.array) > 0; ","; "")}}'
  '[{"text":"🧺 Корзина / оформить","callback_data":"o"}],[{"text":"⬅️ Все разделы","callback_data":"m"}]]}}')
routes.append([
  search(210,900,y,PROMO,[[{"a":"item","o":"exist"},{"a":"cat","o":"text:equal","b":"{{"+D(2)+"}}"}]],"Раздел (каталог)",[[eq(D(1),"k")]],limit=50),
  {"id":211,"mapper":{"btn":catbtn},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":210},
   "filter":{"name":"Товар есть в наличии","conditions":[[{"a":"{{210.data.item}}","o":"exist"},{"a":'{{if(210.data.stock; "1"; "0")}}',"b":"1","o":"text:equal"}]]}},
  {"id":212,"mapper":{"body":cat_body,"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1500,y),"parameters":{}}])
y+=200
# product chosen -> qty (one route per category: quantities differ)
T["@@CODE@@"]="{{"+D(2)+"}}"; T["@@CAT@@"]="{{"+pref+"}}"
mid=20
for c in UNIT:
    u=UNIT[c]; qs=QTY[c]
    qk=[[{"text":f"{q.replace('.',',')} {QL[u]}","callback_data":f"q|@@CODE@@|{q}"} for q in qs[:2]],
        [{"text":f"{q.replace('.',',')} {QL[u]}","callback_data":f"q|@@CODE@@|{q}"} for q in qs[2:]],
        [{"text":"✏️ Свой вес","callback_data":"w|@@CODE@@"}],
        [{"text":"⬅️ Назад","callback_data":"k|@@CAT@@|e"}]]
    obj={"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"🐟 {{2.name}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\nСколько добавить в корзину?","reply_markup":{"inline_keyboard":qk}}
    routes.append([resp(mid,900,y,f"Товар ({c})",[[eq(D(1),"f"),{"a":"{{"+pref+"}}","b":c,"o":"text:equal"},{"a":IN_STOCK,"b":"1","o":"text:equal"}]],obj)])
    mid+=1; y+=200
# custom weight prompt
routes.append([resp(26,900,y,"Свой вес — вопрос",[[eq(D(1),"w")]],
  {"method":"sendMessage","chat_id":cbchat,"text":"✏️ Свой вес\n🐟 {{2.name}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\nОтветьте на это сообщение: сколько взять {{2.hint}}.\nкод: {{"+D(2)+"}}",
   "reply_markup":{"force_reply":True,"input_field_placeholder":"Например 0,7"}})]); y+=200
routes.append([resp(25,900,y,"Нет в наличии",[[eq(D(1),"f"),{"a":IN_STOCK,"b":"1","o":"text:notequal"}]],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"❌ {{ifempty(99.name; \"Этот товар\")}} — сейчас нет в наличии.\nВыберите другой товар 👇","reply_markup":{"inline_keyboard":[[{"text":"⬅️ Все разделы","callback_data":"m"}]]}})]); y+=200
# ---- add to cart
SUM='{{formatNumber(2.total; 2; ","; ".")}}'
CART_BTNS=KB([[{"text":"➕ Добавить ещё","callback_data":"m"}],[{"text":"🧾 Оформить заказ","callback_data":"o"}],[{"text":"🗑 Очистить корзину","callback_data":"x"}]])
cart_view="✅ Добавлено: {{2.name}} — {{2.qlabel}} — "+SUM+" €\n\n🧺 Ваша корзина:\n{{52text}}💶 Итого: {{formatNumber(52total; 2; \",\"; \".\")}} €"
NEWTEXT='{{51.text}}• {{2.name}} — {{2.qlabel}} — '+SUM+' €\n'
NEWTOTAL='{{ifempty(51.total; 0) + 2.total}}'
view=cart_view.replace("{{52text}}",NEWTEXT).replace("52total","(ifempty(51.total; 0) + 2.total)")
add_flow=[
 ds(50,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Добавить в корзину",
    [[eq(D(1),"q"),{"a":"{{2.total}}","b":"0","o":"number:greater"},{"a":IN_STOCK,"b":"1","o":"text:equal"}]]),
 ds(51,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 ds(52,1500,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":NEWTEXT,"total":NEWTOTAL,"count":"{{ifempty(51.count; 0) + 1}}","kg":"{{ifempty(51.kg; 0) + 2.kg}}","pcs":"{{ifempty(51.pcs; 0) + 2.pcs}}"}}),
 router(53,1800,y,[
   [api(54,2100,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text",view),("reply_markup",CART_BTNS)],"Кнопка",[[{"a":"{{1.callback_query.id}}","o":"exist"}]])],
   [api(55,2100,y+200,"sendMessage",[("chat_id",CHAT),("text",view),("reply_markup",CART_BTNS)],"Свой вес",[[{"a":"{{1.callback_query.id}}","o":"notexist"}]])],
 ])]
routes.append(add_flow); y+=400
routes.append([api(56,900,y,"sendMessage",[("chat_id",CHAT),("text","🤔 Не понял количество. Нажмите «✏️ Свой вес» ещё раз и напишите число, например 0,7 или 250.")],
   "Неверный вес",[[eq(D(1),"q"),{"a":"{{2.total}}","b":"0","o":"number:lessorequal"}]])]); y+=200
# ---- checkout: city choice
cities=["Эдделак","Марне","Брунсбюттель","Хайде","Другое место"]
CITY_KB=KB([[{"text":cities[0],"callback_data":"c|1"},{"text":cities[1],"callback_data":"c|2"}],[{"text":cities[2],"callback_data":"c|3"},{"text":cities[3],"callback_data":"c|4"}],[{"text":cities[4],"callback_data":"c|5"}],[{"text":"➕ Добавить ещё","callback_data":"m"}]])
EMPTY_KB=KB([[{"text":"📋 Выбрать товары","callback_data":"m"}]])
routes.append([
 ds(60,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Оформить",[[eq(D(1),"o")]]),
 ds(61,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 router(62,1500,y,[
  [api(63,1800,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🧺 Ваша корзина:\n{{61.text}}💶 Итого: {{formatNumber(61.total; 2; \",\"; \".\")}} €\n\n📍 Куда доставить? Доставка бесплатно."),("reply_markup",CITY_KB)],"Есть товары",[[{"a":"{{61.count}}","b":"0","o":"number:greater"},{"a":"{{61.total}}","b":str(MIN_ORDER),"o":"number:greaterorequal"}]],onerror=True)],
  [api(65,1800,y+400,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🧺 Ваша корзина:\n{{61.text}}💶 Итого: {{formatNumber(61.total; 2; \",\"; \".\")}} €\n\nМинимальный заказ — "+str(MIN_ORDER)+" €. Добавьте ещё на {{formatNumber("+str(MIN_ORDER)+" - 61.total; 2; \",\"; \".\")}} € 👇"),("reply_markup",KB([[{"text":"➕ Добавить ещё","callback_data":"m"}]]))],"Меньше минимума",[[{"a":"{{61.count}}","b":"0","o":"number:greater"},{"a":"{{61.total}}","b":str(MIN_ORDER),"o":"number:less"}]],onerror=True)],
  [api(64,1800,y+200,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🧺 Корзина пуста."),("reply_markup",EMPTY_KB)],"Пусто",[[{"a":"{{ifempty(61.count; 0)}}","b":"0","o":"number:lessorequal"}]],onerror=True)],
 ])]); y+=400
DISC = "floor(ifempty(71.total; 0) * ifempty(71.promo; 0)) / 100"
AFTER = "(ifempty(71.total; 0) - "+DISC+")"
BUSED = "floor(min(ifempty(77.bonus; 0); "+AFTER+" * "+str(BONUS_CAP/100)+") * 100) / 100"
CITY='{{switch('+D(2)+'; "1"; "Эдделак"; "2"; "Марне"; "3"; "Брунсбюттель"; "4"; "Хайде"; "Другое место")}}'
SLOTS=["Сегодня 12–16","Сегодня 17–21","Завтра 12–16","Завтра 17–21"]
SLOT='{{switch('+D(3)+'; "1"; "'+SLOTS[0]+'"; "2"; "'+SLOTS[1]+'"; "3"; "'+SLOTS[2]+'"; "'+SLOTS[3]+'")}}'
SLOT_KB=('{"inline_keyboard":[[{"text":"'+SLOTS[0]+'","callback_data":"t|{{'+D(2)+'}}|1"},{"text":"'+SLOTS[1]+'","callback_data":"t|{{'+D(2)+'}}|2"}],'
 '[{"text":"'+SLOTS[2]+'","callback_data":"t|{{'+D(2)+'}}|3"},{"text":"'+SLOTS[3]+'","callback_data":"t|{{'+D(2)+'}}|4"}],[{"text":"⬅️ Другой город","callback_data":"o"}]]}')
routes.append([api(66,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","📍 "+CITY+"\n🕐 Когда удобно получить заказ?"),("reply_markup",SLOT_KB)],"Выбран город",[[eq(D(1),"c")]],onerror=True)]); y+=200
routes.append([
 ds(70,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Выбрано время",[[eq(D(1),"t")]]),
 ds(71,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 TOUCH_CUST(76,1350,y,None,None),
 ds(77,1500,y,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 sv(78,1650,y,[("disc","{{"+DISC+"}}"),("bused","{{"+BUSED+"}}"),("final","{{"+AFTER+" - "+BUSED+"}}")]),
 sv(79,1800,y,[("pline","🎟 Промокод {{71.pcode}} (−{{71.promo}}%): −"+FMT("78.disc")+" €\n"),("bline","💎 Бонусами: −"+FMT("78.bused")+" €\n")]),
 ds(75,1950,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"disc":"{{78.disc}}","bused":"{{78.bused}}","final":"{{78.final}}","city":CITY,"slot":SLOT}}),
 router(72,2100,y,[
  [api(73,2400,y,"sendMessage",[("chat_id",CHAT),("text","🧾 Ваш заказ\n{{71.text}}📍 "+CITY+"\n🕐 "+SLOT+"\n💳 Оплата: онлайн или наличными при получении\n🧺 Товары: "+FMT("71.total")+" €\n{{if(78.disc > 0; 79.pline; \"\")}}{{if(78.bused > 0; 79.bline; \"\")}}💶 К оплате: "+FMT("78.final")+" €\n\n✍️ Ответьте на это сообщение: напишите адрес доставки — улица, дом, город"),("reply_markup",'{"force_reply":true,"input_field_placeholder":"Улица, дом, город"}')],"Есть товары",[[{"a":"{{71.count}}","b":"0","o":"number:greater"}]])],
  [api(74,2400,y+200,"sendMessage",[("chat_id",CHAT),("text","🧺 Корзина пуста. Нажмите /start, чтобы выбрать товары.")],"Пусто",[[{"a":"{{ifempty(71.count; 0)}}","b":"0","o":"number:lessorequal"}]])],
 ])]); y+=400
EMPTY_REC={"text":"","total":0,"count":0,"kg":0,"pcs":0}
routes.append([
 ds(80,900,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":EMPTY_REC},"Очистить",[[eq(D(1),"x")]]),
 api(81,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🗑 Корзина очищена."),("reply_markup",EMPTY_KB)],onerror=True)]); y+=200
addr=api(40,900,y,"sendMessage",[("chat_id","{{1.message.chat.id}}"),("text","{{trim(first(split(1.message.reply_to_message.text; \"✍️\")))}}\n🏠 Адрес доставки: {{1.message.text}}\n\n📞 Ответьте на это сообщение: напишите ваш номер телефона"),("reply_markup","{\"force_reply\":true,\"input_field_placeholder\":\"Номер телефона\"}")],
   "Получен адрес",[[{"a":"{{1.message.reply_to_message.text}}","b":"Ваш заказ","o":"text:contain"},{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:notcontain"}]])
y+=200
EARN = "floor(ifempty(120.final; 120.total) * "+str(BONUS_PCT)+") / 100"
DAY = '{{formatDate(now; "YYYY-MM-DD"; "'+TZ+'")}}'
MONTH = '{{formatDate(now; "YYYY-MM"; "'+TZ+'")}}'
ph_flow=[
 ds(121,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Получен телефон",[[{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:contain"}]]),
 ds(120,1050,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 ds(122,1200,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}} {{1.message.from.last_name}}","username":"{{1.message.from.username}}","phone":"{{1.message.text}}","last_seen":"{{now}}"}},"Корзина не пуста",[[{"a":"{{ifempty(120.count; 0)}}","b":"0","o":"number:greater"}]],store=CUST),
 ds(123,1350,y,"GetRecord",{"key":CHAT,"returnWrapped":False},store=CUST),
 sv(124,1500,y,[("earn","{{"+EARN+"}}"),("nb","{{ifempty(123.bonus; 0) - ifempty(120.bused; 0)}}"),("n","{{ifempty(123.orders; 0) + 1}}"),("day",DAY),
   ("okey","{{90.chat}}-{{formatDate(now; \"X\")}}"),("ono",'{{formatDate(now; "DDMM-HHmm"; "'+TZ+'")}}'),
   ("hist",'{{formatDate(now; "DD.MM.YY"; "'+TZ+'")}} — {{120.count}} поз. — '+FMT("ifempty(120.final; 120.total)")+" €")]),
 {"id":42,"mapper":{"body":'{"method":"sendMessage","chat_id":{{1.message.chat.id}},"text":"✅ Спасибо! Заказ №{{124.ono}} принят.\\nМы свяжемся с вами, чтобы договориться о времени доставки.\\n\\n💎 После доставки начислим '+FMT("124.earn")+' € бонусами.\\nВаш баланс: '+FMT("124.nb")+' €\\n\\nНовый заказ: /start"}',"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1650,y),"parameters":{}},
 ds(125,1800,y,"AddRecord",{"key":"{{124.okey}}","overwrite":True,"data":{"chat":CHAT,"name":"{{1.message.from.first_name}} {{1.message.from.last_name}}","phone":"{{1.message.text}}","items":"{{120.text}}","total":"{{120.total}}","disc":"{{ifempty(120.disc; 0)}}","bused":"{{ifempty(120.bused; 0)}}","final":"{{ifempty(120.final; 120.total)}}","pcode":"{{120.pcode}}","city":"{{120.city}}","slot":"{{120.slot}}","no":"{{124.ono}}","status":"принят","day":"{{124.day}}","created":"{{now}}",
   "kg":"{{ifempty(120.kg; 0)}}","pcs":"{{ifempty(120.pcs; 0)}}","earn":"{{124.earn}}","ref":"{{123.ref}}","first":"{{ifempty(123.orders; 0) = 0}}","bonus_done":False}},store=ORD),
 ds(126,1950,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"orders":"{{124.n}}","spent":"{{ifempty(123.spent; 0) + ifempty(120.final; 120.total)}}","bonus":"{{124.nb}}",
   "history":"{{124.hist}}\n{{substring(ifempty(123.history; \"\"); 0; 600)}}","last_text":"{{120.text}}","last_total":"{{120.total}}","last_count":"{{120.count}}","last_kg":"{{ifempty(120.kg; 0)}}","last_pcs":"{{ifempty(120.pcs; 0)}}"}},store=CUST),
 ds(127,2100,y,"UpdateRecord",{"key":"{{124.day}}","upsert":True,"overwriteArrays":False,"data":{"day":"{{124.day}}"}},store=STATS),
 ds(128,2250,y,"GetRecord",{"key":"{{124.day}}","returnWrapped":False},store=STATS),
 ds(129,2400,y,"UpdateRecord",{"key":"{{124.day}}","upsert":True,"overwriteArrays":False,"data":{"orders":"{{ifempty(128.orders; 0) + 1}}","revenue":"{{ifempty(128.revenue; 0) + ifempty(120.final; 120.total)}}",
   "newcust":"{{ifempty(128.newcust; 0) + if(ifempty(123.orders; 0) > 0; 0; 1)}}","disc":"{{ifempty(128.disc; 0) + ifempty(120.disc; 0)}}","bused":"{{ifempty(128.bused; 0) + ifempty(120.bused; 0)}}","kg":"{{ifempty(128.kg; 0) + ifempty(120.kg; 0)}}","pcs":"{{ifempty(128.pcs; 0) + ifempty(120.pcs; 0)}}",
   "lines":'{{ifempty(128.lines; "")}}• {{formatDate(now; "HH:mm"; "'+TZ+'")}} {{1.message.from.first_name}}, {{120.city}} — '+FMT("ifempty(120.final; 120.total)")+" €\n"}},store=STATS),
 ds(260,2400,y+150,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"day":MONTH}},store=STATS),
 ds(261,2450,y+150,"GetRecord",{"key":MONTH,"returnWrapped":False},store=STATS),
 ds(262,2500,y+150,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"orders":"{{ifempty(261.orders; 0) + 1}}","revenue":"{{ifempty(261.revenue; 0) + ifempty(120.final; 120.total)}}",
   "kg":"{{ifempty(261.kg; 0) + ifempty(120.kg; 0)}}","pcs":"{{ifempty(261.pcs; 0) + ifempty(120.pcs; 0)}}"}},store=STATS),
]
g_clear=ds(45,2550,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":EMPTY_REC})
g1=api(41,2700,y,"sendMessage",[("chat_id",GROUP),("text","🆕 НОВЫЙ ЗАКАЗ №{{124.ono}} — RAIV FISH\n{{if(ifempty(123.orders; 0) > 0; \"🔁 Постоянный клиент, заказ №\"; \"🆕 Новый клиент\")}}{{if(ifempty(123.orders; 0) > 0; 124.n; \"\")}} · ⚖️ {{formatNumber(ifempty(120.kg; 0); 2; \",\"; \".\")}} кг · 💎 после доставки +"+FMT("124.earn")+" €\n\n{{trim(first(split(1.message.reply_to_message.text; \"📞\")))}}\n📞 Телефон: {{1.message.text}}\n👤 Клиент: {{1.message.from.first_name}} {{1.message.from.last_name}} @{{1.message.from.username}}\n\n🗺 Маршрут: https://www.google.com/maps/search/?api=1&query={{encodeURL(trim(replace(first(split(get(split(1.message.reply_to_message.text; \"🏠\"); 2); \"📞\")); \"Адрес доставки:\"; \"\")))}}%2C%20Deutschland"),("reply_markup",'{"inline_keyboard":[[{"text":"🚚 В пути","callback_data":"s|{{124.okey}}|1"},{"text":"✅ Доставлен","callback_data":"s|{{124.okey}}|2"}]]}')])
g3=api(43,2850,y,"sendMessage",[("chat_id",GROUP),("text","💬 Связаться с клиентом в Telegram 👇"),("reply_to_message_id","{{41.body.result.message_id}}"),("reply_markup","{\"inline_keyboard\":[[{\"text\":\"💬 Написать клиенту\",\"url\":\"tg://user?id={{1.message.from.id}}\"}]]}")],onerror=True)
OWN = {"a":"{{1.message.from.id}}","b":OWNER_ID,"o":"text:equal"}
NOREPLY = {"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}
ARG = lambda n: 'get(split(trim(1.message.text); " "); '+str(n)+')'
admin_help = ("🛠 Команды владельца\n\n"
 "/report — продажи за сегодня\n"
 "/promo КОД 10 — создать промокод на 10% (КОД 0 — выключить)\n"
 "/send текст — рассылка всем клиентам бота\n"
 "/catalog — коды товаров, цены и наличие\n"
 "/price b5 37 — новая цена (подтверждение кнопкой)\n"
 "/stock b5 0 — нет в наличии, /stock b5 1 — снова есть\n"
 "В канале под заказом: 🚚 В пути / ✅ Доставлен — клиент получит уведомление и оценит заказ\n\n"
 "Каждый вечер в 21:00 отчёт приходит в канал заказов.\n"
 "Бонусы: "+str(BONUS_PCT)+"% с заказа, списание до "+str(BONUS_CAP)+"% суммы.")
y+=600
own=[]
ORDK = "{{"+D(2)+"}}"
STAR = '{{switch('+D(3)+'; "1"; "⭐"; "2"; "⭐⭐"; "3"; "⭐⭐⭐"; "4"; "⭐⭐⭐⭐"; "⭐⭐⭐⭐⭐")}}'
own.append([ds(190,900,y,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"status":'{{if('+D(3)+' = "1"; "в пути"; "доставлен")}}',"status_at":"{{now}}"}},"Статус заказа",[[eq(D(1),"s")]],store=ORD),
  ds(191,1200,y,"GetRecord",{"key":ORDK,"returnWrapped":False},store=ORD),
  router(192,1500,y,[
   [api(193,1800,y,"sendMessage",[("chat_id","{{191.chat}}"),("text","🚚 Ваш заказ №{{191.no}} уже в пути! Скоро будем.")],"В пути",[[eq(D(3),"1")]],onerror=True),
    api(194,2100,y,"editMessageReplyMarkup",[("chat_id",CHAT),("message_id",MID),("reply_markup",'{"inline_keyboard":[[{"text":"🚚 В пути ✓","callback_data":"z"},{"text":"✅ Доставлен","callback_data":"s|'+ORDK+'|2"}]]}')],onerror=True)],
   [router(264,1800,y+250,[
    [api(195,1800,y+250,"sendMessage",[("chat_id","{{191.chat}}"),("text","✅ Заказ №{{191.no}} доставлен. Приятного аппетита! 🐟\n\nОцените, пожалуйста, заказ:"),
     ("reply_markup",'{"inline_keyboard":[['+",".join('{"text":"'+"⭐"*i+'","callback_data":"rt|'+ORDK+'|'+str(i)+'"}' for i in (1,2,3))+'],['+",".join('{"text":"'+"⭐"*i+'","callback_data":"rt|'+ORDK+'|'+str(i)+'"}' for i in (4,5))+']]}')],"Доставлен",[[eq(D(3),"2")]],onerror=True),
    api(196,2100,y+250,"editMessageReplyMarkup",[("chat_id",CHAT),("message_id",MID),("reply_markup",'{"inline_keyboard":[[{"text":"✅ Доставлен","callback_data":"z"}]]}')],onerror=True)],
    [ds(250,2400,y+250,"GetRecord",{"key":"{{191.chat}}","returnWrapped":False},"Доставлен, бонусы ещё не начислены",[[{"a":"{{191.bonus_done}}","b":"true","o":"text:notequal"},eq(D(3),"2")]],store=CUST),
    ds(251,2700,y+250,"UpdateRecord",{"key":"{{191.chat}}","upsert":False,"overwriteArrays":False,"data":{"bonus":"{{ifempty(250.bonus; 0) + ifempty(191.earn; 0)}}"}},store=CUST),
    ds(252,3000,y+250,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"bonus_done":True}},store=ORD),
    api(259,3300,y+250,"sendMessage",[("chat_id","{{191.chat}}"),("text","💎 Начислено "+FMT("ifempty(191.earn; 0)")+" € бонусами за заказ №{{191.no}}. Баланс: "+FMT("ifempty(250.bonus; 0) + ifempty(191.earn; 0)")+" €")],onerror=True)],
    [ds(253,3600,y+250,"GetRecord",{"key":"{{191.ref}}","returnWrapped":False},"Доставлен, первый заказ друга",[[eq(D(3),"2"),{"a":"{{191.first}}","b":"true","o":"text:equal"},{"a":"{{191.ref}}","o":"exist"}]],store=CUST),
    ds(254,3900,y+250,"UpdateRecord",{"key":"{{191.ref}}","upsert":False,"overwriteArrays":False,"data":{"bonus":"{{ifempty(253.bonus; 0) + "+str(REF_BONUS)+"}}"}},"Пригласивший есть в базе",[[{"a":"{{253.chat}}","o":"exist"}]],store=CUST),
    api(255,4200,y+250,"sendMessage",[("chat_id","{{191.ref}}"),("text","🎁 Ваш друг получил первый заказ — вам +"+str(REF_BONUS)+" € бонусами! Спасибо, что советуете RAIV FISH.")],onerror=True)]])]]) ]); y+=500
own.append([ds(197,900,y,"UpdateRecord",{"key":ORDK,"upsert":False,"overwriteArrays":False,"data":{"rating":"{{"+D(3)+"}}"}},"Оценка",[[eq(D(1),"rt")]],store=ORD),
  ds(198,1200,y,"GetRecord",{"key":ORDK,"returnWrapped":False},store=ORD),
  api(199,1500,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","Спасибо за оценку "+STAR+"!\nБудем рады видеть вас снова 🐟"),("reply_markup",KB([[{"text":"🛒 Новый заказ","callback_data":"m"}]]))],onerror=True),
  api(184,1800,y,"sendMessage",[("chat_id",GROUP),("text",STAR+" Оценка заказа №{{198.no}} — {{198.name}}{{if(parseNumber("+D(3)+"; \".\") < 4; \"\\n⚠️ Низкая оценка — напишите клиенту\"; \"\")}}")],onerror=True),
  ds(185,2100,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}},store=STATS),
  ds(186,2400,y,"GetRecord",{"key":DAY,"returnWrapped":False},store=STATS),
  ds(187,2700,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"rsum":"{{ifempty(186.rsum; 0) + parseNumber("+D(3)+"; \".\")}}","rcount":"{{ifempty(186.rcount; 0) + 1}}"}},store=STATS)]); y+=300
own.append([resp(170,900,y,"/admin",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/admin","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,"text":admin_help})]); y+=200
PCT = "parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\")"
own.append([api(256,900,y,"sendMessage",[("chat_id",CHAT),("text","⚠️ Скидка по промокоду — от 1 до "+str(PROMO_MAX)+" %. Пример: /promo FISH10 10\n/promo FISH10 0 — выключить.")],"/promo вне 0–"+str(PROMO_MAX),
   [[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":str(PROMO_MAX),"o":"number:greater"}],[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":"0","o":"number:less"}]])]); y+=200
own.append([ds(171,900,y,"AddRecord",{"key":"{{upper("+ARG(2)+")}}","overwrite":True,"data":{"code":"{{upper("+ARG(2)+")}}","percent":"{{parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\")}}","active":"{{parseNumber(ifempty("+ARG(3)+"; \"0\"); \".\") > 0}}","uses":0}},"/promo",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/promo ","o":"text:startwith"},{"a":"{{"+PCT+"}}","b":str(PROMO_MAX),"o":"number:lessorequal"},{"a":"{{"+PCT+"}}","b":"0","o":"number:greaterorequal"}]],store=PROMO),
  resp(172,1200,y,None,None,{"method":"sendMessage","chat_id":chat,"text":ph('"🎟 Промокод {{upper('+ARG(2)+')}}: {{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; "скидка "; "выключен")}}{{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; '+ARG(3)+'; "")}}{{if(parseNumber(ifempty('+ARG(3)+'; "0"); ".") > 0; "%"; "")}}.\\nКлиенты вводят его кнопкой «🎟 Промокод»."')})]); y+=200
own.append([resp(173,900,y,"/send",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/send ","o":"text:startwith"}]],{"method":"sendMessage","chat_id":chat,"text":"📣 Рассылка отправляется всем клиентам бота. Копия придёт и вам."}),
  search(174,1200,y,CUST,[[{"a":"chat","o":"exist"},{"a":"blocked","o":"notexist"}],[{"a":"chat","o":"exist"},{"a":"blocked","o":"boolean:isfalse"}]]),
  api(175,1500,y,"sendMessage",[("chat_id","{{174.data.chat}}"),("text",'{{substring(trim(1.message.text); 6; 4000)}}\n\n/start — каталог · /stop — отписаться от рассылок'),("reply_markup",KB([[{"text":"🛒 К покупкам","callback_data":"m"}]]))],"Есть клиент",[[{"a":"{{174.data.chat}}","o":"exist"}]],onerror=True)]); y+=200
own.append([TOUCH_CUST(176,900,y,"/stop",[[NOREPLY,{"a":"{{1.message.text}}","b":"/stop","o":"text:startwith"}]]),
  ds(177,1200,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"blocked":True}},store=CUST),
  resp(178,1500,y,None,None,{"method":"sendMessage","chat_id":chat,"text":"Вы отписались от рассылок. Заказы и бонусы сохранены.\n/start — открыть каталог"})]); y+=200
CODEK = 'cat_{{lower('+ARG(2)+')}}'
NEWP = 'parseNumber(replace(ifempty('+ARG(3)+'; "0"); ","; "."); ".")'
CB_OWN = {"a":"{{1.callback_query.from.id}}","b":OWNER_ID,"o":"text:equal"}
CONFIRM = lambda code, cbv: KB([[{"text":"✅ Подтвердить","callback_data":code+"|{{lower("+ARG(2)+")}}|"+cbv,"style":"success"},{"text":"Отмена","callback_data":"zx"}]])
# /price b5 37
own.append([ds(220,900,y,"GetRecord",{"key":CODEK,"returnWrapped":False},"/price",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/price ","o":"text:startwith"}]],store=PROMO),
  router(221,1200,y,[
   [api(222,1500,y,"sendMessage",[("chat_id",CHAT),("text","💶 {{220.name}}: {{replace(toString(220.price); \".\"; \",\")}} € → {{replace(toString("+NEWP+"); \".\"; \",\")}} €\nПодтвердить новую цену?"),
     ("reply_markup",CONFIRM("cp","{{"+NEWP+"}}"))],"Товар есть и цена > 0",[[{"a":"{{220.item}}","o":"exist"},{"a":"{{"+NEWP+"}}","b":"0","o":"number:greater"}]])],
   [api(223,1500,y+200,"sendMessage",[("chat_id",CHAT),("text","🤔 Не понял. Пример: /price b5 37\nКоды товаров: /catalog")],"Ошибка",
     [[{"a":"{{220.item}}","o":"notexist"}],[{"a":"{{"+NEWP+"}}","b":"0","o":"number:lessorequal"}]])]])]); y+=400
# /stock b5 0|1
own.append([ds(224,900,y,"GetRecord",{"key":CODEK,"returnWrapped":False},"/stock",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/stock ","o":"text:startwith"}]],store=PROMO),
  router(225,1200,y,[
   [api(226,1500,y,"sendMessage",[("chat_id",CHAT),("text","📦 {{224.name}}: {{if(224.stock; \"есть\"; \"нет\")}} → {{if("+ARG(3)+" = \"1\"; \"есть в наличии\"; \"нет в наличии\")}}\nПодтвердить?"),
     ("reply_markup",CONFIRM("cs","{{if("+ARG(3)+" = \"1\"; \"1\"; \"0\")}}"))],"Товар есть",[[{"a":"{{224.item}}","o":"exist"}]])],
   [api(227,1500,y+200,"sendMessage",[("chat_id",CHAT),("text","🤔 Не понял. Пример: /stock b5 0 — нет в наличии, /stock b5 1 — есть\nКоды товаров: /catalog")],"Нет товара",[[{"a":"{{224.item}}","o":"notexist"}]])]])]); y+=400
# подтверждение кнопкой (только владелец)
own.append([ds(228,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"price":"{{parseNumber("+D(3)+"; \".\")}}","updated":"{{now}}"}},"Подтверждена цена",[[eq(D(1),"cp"),CB_OWN]],store=PROMO),
  api(229,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","✅ Цена обновлена: {{99.name}} — было {{replace(toString(99.price); \".\"; \",\")}} €, стало {{replace("+D(3)+"; \".\"; \",\")}} €.\nБот и витрина уже показывают новую цену.")],onerror=True)]); y+=200
own.append([ds(230,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"stock":"{{"+D(3)+" = \"1\"}}","updated":"{{now}}"}},"Подтверждено наличие",[[eq(D(1),"cs"),CB_OWN]],store=PROMO),
  api(231,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","✅ {{99.name}}: {{if("+D(3)+" = \"1\"; \"снова в наличии\"; \"нет в наличии — скрыт из каталога и витрины\")}}.")],onerror=True)]); y+=200
own.append([api(232,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","Отменено.")],"Отмена",[[eq(D(1),"zx")]],onerror=True)]); y+=200
# /catalog
own.append([search(233,900,y,PROMO,[[{"a":"item","o":"exist"}]],"/catalog",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/catalog","o":"text:startwith"}]],limit=100),
  {"id":234,"mapper":{"line":"{{233.data.item}} · {{233.data.name}} — {{replace(toString(233.data.price); \".\"; \",\")}} € {{if(233.data.stock; \"✅\"; \"❌\")}}"},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":233},
   "filter":{"name":"Товар","conditions":[[{"a":"{{233.data.item}}","o":"exist"}]]}},
  api(235,1500,y,"sendMessage",[("chat_id",CHAT),("text","🗂 Каталог (код · товар — цена · наличие)\n\n{{join(map(234.array; \"line\"); \"\n\")}}\n\nИзменить: /price b5 37 · /stock b5 0")])]); y+=200
# 📦 Склад: владелец переключает наличие кнопками (sk|b — раздел, ct|b5|0 — переключить, sm//sklad — разделы)
SKC = 'substring('+D(2)+'; 0; 1)'
SK_TITLE = "switch("+SKC+"; "+"; ".join(f'"{c}"; "{t}"' for c,t,_ in cats)+'; "Склад")'
sk_btn = '[{"text":"{{if(237.data.stock; "✅"; "❌")}} {{237.data.name}}","callback_data":"ct|{{237.data.item}}|{{if(237.data.stock; "0"; "1")}}"}]'
sk_body = ('{"method":"editMessageText","chat_id":{{1.callback_query.message.chat.id}},"message_id":{{1.callback_query.message.message_id}},'
  '"text":"📦 Склад · {{'+SK_TITLE+'}}\\nНажмите на товар, чтобы переключить: ✅ есть → ❌ нет и обратно.\\nИзменения сразу видны в боте и витрине.",'
  '"reply_markup":{"inline_keyboard":[{{join(map(238.array; "btn"); ",")}}{{if(length(238.array) > 0; ","; "")}}[{"text":"⬅️ Разделы склада","callback_data":"sm"}]]}}')
SK_MENU = KB([[{"text":t,"callback_data":"sk|"+c}] for c,t,_ in cats])
SK_CB_OWN = [eq(D(1),"sk"),CB_OWN]
own.append([ds(236,900,y,"UpdateRecord",{"key":"cat_{{"+D(2)+"}}","upsert":False,"overwriteArrays":False,"data":{"stock":"{{"+D(3)+" = \"1\"}}","updated":"{{now}}"}},"Склад: переключить",[[eq(D(1),"ct"),CB_OWN]],store=PROMO)]); y+=200
own.append([search(237,900,y,PROMO,[[{"a":"item","o":"exist"},{"a":"cat","o":"text:equal","b":"{{"+SKC+"}}"}]],"Склад: раздел",[[eq(D(1),"sk"),CB_OWN],[eq(D(1),"ct"),CB_OWN]],limit=50),
  {"id":238,"mapper":{"btn":sk_btn},"module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,y),"parameters":{"feeder":237},
   "filter":{"name":"Товар","conditions":[[{"a":"{{237.data.item}}","o":"exist"}]]}},
  {"id":239,"mapper":{"body":sk_body,"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(1500,y),"parameters":{}}]); y+=200
own.append([api(240,900,y,"sendMessage",[("chat_id",CHAT),("text","📦 Склад — выберите раздел. Нажатие на товар переключает наличие."),("reply_markup",SK_MENU)],"/sklad",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/sklad","o":"text:startwith"}]])]); y+=200
own.append([api(241,900,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","📦 Склад — выберите раздел. Нажатие на товар переключает наличие."),("reply_markup",SK_MENU)],"Склад: разделы",[[eq(D(1),"sm"),CB_OWN]],onerror=True)]); y+=200
REPORT_TXT = ("📊 Продажи за {{formatDate(now; \"DD.MM.YYYY\"; \""+TZ+"\")}}\n\n"
 "🧾 Заказов: {{ifempty(@S.orders; 0)}}\n💶 Выручка: "+FMT("ifempty(@S.revenue; 0)")+" €\n"
 "🧮 Средний чек: "+FMT("if(ifempty(@S.orders; 0) > 0; @S.revenue / @S.orders; 0)")+" €\n"
 "🆕 Новых клиентов: {{ifempty(@S.newcust; 0)}}\n🎟 Скидки по промокодам: "+FMT("ifempty(@S.disc; 0)")+" €\n💎 Оплачено бонусами: "+FMT("ifempty(@S.bused; 0)")+" €\n"
 "⭐ Средняя оценка: {{if(ifempty(@S.rcount; 0) > 0; formatNumber(@S.rsum / @S.rcount; 1; \",\"; \".\"); \"—\")}} ({{ifempty(@S.rcount; 0)}})\n"
 "⚖️ Продано: {{formatNumber(ifempty(@S.kg; 0); 2; \",\"; \".\")}} кг · {{ifempty(@S.pcs; 0)}} шт\n"
 "🧺 Напомнили о брошенной корзине: {{ifempty(@S.abandoned; 0)}}\n\n{{ifempty(@S.lines; \"Заказов пока нет.\")}}")
MONTH_TXT = ("\n\n📅 С начала месяца: {{ifempty(@M.orders; 0)}} зак. · "+FMT("ifempty(@M.revenue; 0)")+" € · ⚖️ {{formatNumber(ifempty(@M.kg; 0); 2; \",\"; \".\")}} кг · {{ifempty(@M.pcs; 0)}} шт")
own.append([ds(179,900,y,"UpdateRecord",{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}},"/report",[[OWN,NOREPLY,{"a":"{{1.message.text}}","b":"/report","o":"text:startwith"}]],store=STATS),
  ds(180,1200,y,"GetRecord",{"key":DAY,"returnWrapped":False},store=STATS),
  ds(265,1300,y,"UpdateRecord",{"key":MONTH,"upsert":True,"overwriteArrays":False,"data":{"day":MONTH}},store=STATS),
  ds(263,1350,y,"GetRecord",{"key":MONTH,"returnWrapped":False},store=STATS),
  api(181,1500,y,"sendMessage",[("chat_id",CHAT),("text",REPORT_TXT.replace("@S","180")+MONTH_TXT.replace("@M","263"))])])
AMOUNT = "{{round(ifempty(120.final; 120.total) * 100)}}"
pay_body = ("mode=payment&success_url="+BOT_URL+"&cancel_url="+BOT_URL+"&client_reference_id={{124.okey}}"
 "&metadata[chat]={{90.chat}}&metadata[order]={{124.okey}}&metadata[no]={{124.ono}}&metadata[name]={{encodeURL(1.message.from.first_name)}}"
 "&line_items[0][quantity]=1&line_items[0][price_data][currency]=eur&line_items[0][price_data][unit_amount]="+AMOUNT+
 "&line_items[0][price_data][product_data][name]={{encodeURL(\"RAIV FISH — заказ\")}}"
 "&line_items[0][price_data][product_data][description]={{encodeURL(substring(120.text; 0; 300))}}")
pay = {"id":130,"module":"stripe:makeAnApiCall","version":1,"metadata":meta(2700,y+250),"parameters":{"__IMTCONN__":STRIPE_CONN},
  "mapper":{"url":"/v1/checkout/sessions","method":"POST","headers":[{"key":"Content-Type","value":"application/x-www-form-urlencoded"}],"qs":[],"body":pay_body},
  "filter":{"name":"Сумма от 0,50 €","conditions":[[{"a":"{{ifempty(120.final; 120.total)}}","b":"0.5","o":"number:greaterorequal"}]+([] if STRIPE_PUBLIC else [{"a":"{{90.chat}}","b":OWNER_ID,"o":"text:equal"}])]},
  "onerror":[{"id":630,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":meta(2700,y+550)}]}
pay_msg = api(131,3000,y+250,"sendMessage",[("chat_id",CHAT),("text","💳 Можно оплатить заказ онлайн — "+FMT("ifempty(120.final; 120.total)")+" €\nApple Pay, Google Pay или карта, безопасно через Stripe.\nИли наличными при получении — как удобно."),
  ("reply_markup",'{"inline_keyboard":[[{"text":"💳 Оплатить онлайн","url":"{{130.body.url}}"}]]}')],"Ссылка есть",[[{"a":"{{130.body.url}}","o":"exist"}]],onerror=True)
# корзина из витрины: sendData ("b5:1,a2:0.3") или ссылка /start c_b5-1_a2-0p3 (кнопка меню / браузер)
DEEP = "/start c_"
WA_SRC = ('ifempty(1.message.web_app_data.data; replace(replace(replace(replace(ifempty(1.message.text; ""); "'+DEEP+'"; ""); "_"; ","); "-"; ":"); "p"; "."))')
IT='first(split(201.value; ":"))'
IQ='last(split(201.value; ":"))'
ipref=f'substring({IT}; 0; 1)'
iname="205.name"
istock='if(205.stock; "1"; "0")'
itot=f'ifempty(205.price; 0) * parseNumber({IQ}; ".") / switch({ipref}; "a"; 100; "c"; 100; 1)'
iunit=f'switch({ipref}; "a"; "г"; "c"; "г"; "e"; "шт."; "кг")'
ikg=f'switch({ipref}; "a"; parseNumber({IQ}; ".") / 1000; "c"; parseNumber({IQ}; ".") / 1000; "e"; 0; parseNumber({IQ}; "."))'
ipcs=f'if({ipref} = "e"; parseNumber({IQ}; "."); 0)'
ilim=f'switch({ipref}; "a"; {MAX_G}; "c"; {MAX_G}; "e"; {MAX_PCS}; {MAX_KG})'
WA_TEXT='{{join(map(202.array; "line"); "")}}'
WA_TOTAL='sum(map(202.array; "total"))'
routes.append([
 {"id":201,"mapper":{"array":'{{split('+WA_SRC+'; ",")}}'},"module":"builtin:BasicFeeder","version":1,"metadata":meta(900,-2600),"parameters":{},
  "filter":{"name":"Корзина из витрины","conditions":[[{"a":"{{1.message.web_app_data.data}}","o":"exist"}],[{"a":"{{1.message.text}}","b":DEEP,"o":"text:startwith"}]]}},
 ds(205,1050,-2600,"GetRecord",{"key":"cat_{{"+IT+"}}","returnWrapped":False},store=PROMO),
 {"id":202,"mapper":{"line":"• {{"+iname+"}} — {{replace("+IQ+'; "."; ",")}} {{'+iunit+"}} — {{formatNumber("+itot+'; 2; ","; ".")}} €\n',"total":"{{"+itot+"}}","kg":"{{"+ikg+"}}","pcs":"{{"+ipcs+"}}"},
  "module":"builtin:BasicAggregator","version":1,"metadata":meta(1200,-2600),"parameters":{"feeder":201},
  "filter":{"name":"Есть в наличии","conditions":[[{"a":"{{"+istock+"}}","b":"1","o":"text:equal"},{"a":"{{"+itot+"}}","b":"0","o":"number:greater"},{"a":"{{parseNumber("+IQ+"; \".\")}}","b":"{{"+ilim+"}}","o":"number:lessorequal"}]]}},
 ds(203,1500,-2600,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"text":WA_TEXT,"total":"{{"+WA_TOTAL+"}}","count":"{{length(202.array)}}","kg":"{{sum(map(202.array; \"kg\"))}}","pcs":"{{sum(map(202.array; \"pcs\"))}}","seen":"{{now}}"}},
    "Корзина не пустая",[[{"a":"{{length(202.array)}}","b":"0","o":"number:greater"}]]),
 api(204,1800,-2600,"sendMessage",[("chat_id",CHAT),("text","🛍 Корзина из витрины:\n"+WA_TEXT+"💶 Итого: {{formatNumber("+WA_TOTAL+'; 2; ","; ".")}} €\n\n{{if('+WA_TOTAL+" >= "+str(MIN_ORDER)+'; "🚗 Доставка бесплатно. Оформим?"; "Минимальный заказ '+str(MIN_ORDER)+' € — добавьте ещё товаров.")}}'),("reply_markup",CART_BTNS)])])
dup_msg=api(258,1200,y+300,"sendMessage",[("chat_id",CHAT),("text","✅ Этот заказ уже оформлен и передан продавцу.\nНовый заказ: /start")],"Корзина пуста",[[{"a":"{{ifempty(120.count; 0)}}","b":"0","o":"number:lessorequal"}]],onerror=True)
rts=[{"flow":r} for r in routes]+[{"flow":[addr]},{"flow":ph_flow[:2]+[router(257,1150,y,[ph_flow[2:]+[g_clear,router(140,2650,y,[[g1,g3],[pay,pay_msg]])],[dup_msg]])]}]+[{"flow":r} for r in own]
bp={"name":"RAIV_Fish Bot — Заказы","metadata":{"instant":True,"version":1},"flow":[
 {"id":1,"mapper":{},"module":"gateway:CustomWebHook","version":1,"metadata":meta(0,0),"parameters":{"hook":HOOK,"maxResults":1}},
 {"id":90,"mapper":{"variables":unify,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(150,0),"parameters":{}},
 {"id":99,"mapper":{"key":"cat_{{"+D(2)+"}}","returnWrapped":False},"module":"datastore:GetRecord","version":1,"metadata":meta(225,0),"parameters":{"datastore":PROMO}},
 {"id":2,"mapper":{"variables":variables,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(300,0),"parameters":{}},
 {"id":3,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(600,0),"routes":rts}]}
import re, sys
_s=json.dumps(bp,ensure_ascii=False)
_s=_s.replace("@@CARTBTNS@@",json.dumps(CART_BTNS,ensure_ascii=False)[1:-1]).replace("@@EMPTYKB@@",json.dumps(EMPTY_KB,ensure_ascii=False)[1:-1])
bp=json.loads(_s)
def fix(s): return re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"','"'), s)
def walk(flow):
    for m in flow:
        if m["module"]=="gateway:WebhookRespond":
            m["mapper"]["body"]=fix(m["mapper"]["body"])
            json.loads(re.sub(r"\{\{.*?\}\}","1",m["mapper"]["body"].replace("}}{{if(length(211.array) > 0; \",\"; \"\")}}","}},").replace("}}{{if(length(238.array) > 0; \",\"; \"\")}}","}},")))
        for r in m.get("routes",[]): walk(r["flow"])
walk(bp["flow"])
# цветные кнопки (Bot API 9.4): главное действие зелёное, удаление красное, статусы заказа в канале
_t=json.dumps(bp,ensure_ascii=False)
STYLE={"o":"success","x":"danger"}
_t=re.sub(r'((?:🧾 Оформить заказ|🧺 Корзина / оформить|🗑 Очистить корзину)\\",\s?\\"callback_data\\":\s?\\"(o|x)\\")', lambda m: m.group(1)+', \\"style\\": \\"'+STYLE[m.group(2)]+'\\"', _t)
_t=re.sub(r'(\\"callback_data\\":\s?\\"s\|[^"\\]*\|([12])\\")', lambda m: m.group(1)+', \\"style\\": \\"'+("primary" if m.group(2)=="1" else "success")+'\\"', _t)
bp=json.loads(_t)
s=json.dumps(bp,ensure_ascii=False)
assert "@@" not in s, s[s.find("@@")-80:s.find("@@")+40]
ids=[]
def collect(flow):
    for m in flow:
        ids.append(m["id"]); [ids.append(e["id"]) for e in m.get("onerror",[])]
        for r in m.get("routes",[]): collect(r["flow"])
collect(bp["flow"]); assert len(ids)==len(set(ids)), sorted(ids)
out = sys.argv[1] if len(sys.argv)>1 else "bp.json"
json.dump(bp,open(out,"w"),ensure_ascii=False)
print("ok", len(s), "modules", len(ids))
