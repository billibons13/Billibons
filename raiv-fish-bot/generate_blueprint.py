import json
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
items = {}
for c,_,lst in cats:
    for i,(n,p,s) in enumerate(lst,1): items[f"{c}{i}"]=(n,p,s)

# ---- module 90: unify callback / custom-weight reply into one "d" string + chat id
RT = 'ifempty(1.message.reply_to_message.text; "")'
IS_W = f'contains({RT}; "✏️ Свой вес")'
W_CODE = f'trim(last(split({RT}; "код:")))'
W_QTY = ('parseNumber(replace(replace(replace(replace(replace(lower(trim(ifempty(1.message.text; ""))); "кг"; ""); "шт"; ""); "г"; ""); " "; ""); ","; "."); ".")')
d_val = ("{{1.callback_query.data}}"
         + "{{if(" + IS_W + '; "q|"; "")}}'
         + "{{if(" + IS_W + "; " + W_CODE + '; "")}}'
         + "{{if(" + IS_W + '; "|"; "")}}'
         + "{{if(" + IS_W + "; " + W_QTY + '; "")}}')
unify = [{"name":"d","value":d_val},
         {"name":"chat","value":"{{1.callback_query.message.chat.id}}{{1.message.chat.id}}"}]

def D(n): return f'get(split(90.d; "|"); {n})'
pref = f'substring(ifempty({D(2)}; "x"); 0; 1)'
sw_name = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[0]}"' for k,v in items.items()) + '; "")'
sw_price = "switch(" + D(2) + "; " + "; ".join(f'"{k}"; "{v[1]}"' for k,v in items.items()) + '; "0")'
div = f'switch({pref}; "a"; 100; "c"; 100; 1)'
qunit = f'switch({pref}; "a"; "г"; "c"; "г"; "e"; "шт."; "кг")'
variables = [
 {"name":"name","value":"{{"+sw_name+"}}"},
 {"name":"price","value":"{{"+sw_price+"}}"},
 {"name":"ulabel","value":"{{"+f'switch({pref}; "a"; "€ / 100 г"; "c"; "€ / 100 г"; "e"; "€ / шт."; "€ / кг")'+"}}"},
 {"name":"qlabel","value":"{{"+f'replace(ifempty({D(3)}; ""); "."; ",")'+"}} {{"+qunit+"}}"},
 {"name":"total","value":"{{"+f'parseNumber({sw_price}; ".") * parseNumber(ifempty({D(3)}; "0"); ".") / {div}'+"}}"},
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
menu = """💼 Хотите такой бот для своего магазина? Кнопка внизу.

Здравствуйте! 🐟 RAIV FISH — вяленая рыба и снеки.
Весь ассортимент и наличие внизу. То, что отмечено ❌, — нет в наличии.

"""
for c,title,lst in cats:
    menu += title.upper() if c!="e" else "🥫 КОНСЕРВЫ"
    menu += "\n"
    for n,p,s in lst:
        menu += f"• {n} — {p.replace('.',',')} {ULBL[c]}" + ("❌" if not s else "") + "\n"
    menu += "\n"
menu += "🚗 Доставка каждый день: Эдделак, Марне, Брунсбюттель, Хайде\n💶 Оплата при получении\n\n🧺 Можно собрать корзину из нескольких товаров.\nВыберите раздел 👇"
cat_kb = lambda mode: {"inline_keyboard":([OFFER_BTN] if mode=="s" else [])+[[{"text":t,"callback_data":f"k|{c}|{mode}"}] for c,t,_ in cats]}
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
def api(mid, x, y, method, spec, name=None, conds=None, onerror=False):
    m={"id":mid,"mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":k,"value":v} for k,v in spec],"urlMethod":method},
       "module":"telegram:UniversalAPICall","version":1,"metadata":meta(x,y),"parameters":{"__IMTCONN__":CONN}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    if onerror: m["onerror"]=[{"id":mid+500,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":meta(x,y+300)}]
    return m
def ds(mid, x, y, module, mapper, name=None, conds=None):
    m={"id":mid,"mapper":mapper,"module":f"datastore:{module}","version":1,"metadata":meta(x,y),"parameters":{"datastore":DS}}
    if conds is not None: m["filter"]={"name":name,"conditions":conds}
    return m
def router(mid, x, y, routes): return {"id":mid,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(x,y),"routes":[{"flow":r} for r in routes]}
def eq(a,b): return {"a":"{{"+a+"}}","b":b,"o":"text:equal"}
KB = lambda rows: json.dumps({"inline_keyboard":rows},ensure_ascii=False)
CHAT="{{90.chat}}"; MID="{{1.callback_query.message.message_id}}"
routes=[]
chat=ph("{{1.message.chat.id}}")
routes.append([resp(4,900,-900,"Меню",[[{"a":"{{1.message.text}}","o":"exist"},{"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}]],
  {"method":"sendMessage","chat_id":chat,"text":menu,"reply_markup":cat_kb("s")})])
cbchat=ph("{{1.callback_query.message.chat.id}}"); cbmid=ph(MID)
routes.append([resp(5,900,-700,"Разделы",[[eq(D(1),"m")]],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"Выберите раздел 👇","reply_markup":cat_kb("e")})])
routes.append([resp(30,900,-600,"Предложение",[[eq(D(1),"p")]],
  {"method":"sendMessage","chat_id":cbchat,"text":offer,"reply_markup":{"inline_keyboard":[
    [{"text":"💬 Написать продавцу","url":"https://t.me/esusnob"}],
    [{"text":"🛒 Попробовать заказ","callback_data":"m"}]]}})])
y=-500
for idx,(c,title,lst) in enumerate(cats):
    kb=[[{"text":f"{n} — {p.replace('.',',')} {ULBL[c]}","callback_data":f"f|{c}{i}"}] for i,(n,p,s) in enumerate(lst,1) if s]
    kb.append([{"text":"🧺 Корзина / оформить","callback_data":"o"}])
    kb.append([{"text":"⬅️ Все разделы","callback_data":"m"}])
    method=ph('"{{if('+D(3)+' = "e"; "editMessageText"; "sendMessage")}}"')
    routes.append([resp(6+idx,900,y,f"Раздел {c}",[[eq(D(1),"k"),eq(D(2),c)]],
      {"method":method,"chat_id":cbchat,"message_id":cbmid,"text":f"{title}\n\nВыберите товар 👇","reply_markup":{"inline_keyboard":kb}})])
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
    routes.append([resp(mid,900,y,f"Товар ({c})",[[eq(D(1),"f"),{"a":"{{"+pref+"}}","b":c,"o":"text:equal"}]],obj)])
    mid+=1; y+=200
# custom weight prompt
routes.append([resp(26,900,y,"Свой вес — вопрос",[[eq(D(1),"w")]],
  {"method":"sendMessage","chat_id":cbchat,"text":"✏️ Свой вес\n🐟 {{2.name}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\nОтветьте на это сообщение: сколько взять {{2.hint}}.\nкод: {{"+D(2)+"}}",
   "reply_markup":{"force_reply":True,"input_field_placeholder":"Например 0,7"}})]); y+=200
# ---- add to cart
SUM='{{formatNumber(2.total; 2; ","; ".")}}'
CART_BTNS=KB([[{"text":"➕ Добавить ещё","callback_data":"m"}],[{"text":"🧾 Оформить заказ","callback_data":"o"}],[{"text":"🗑 Очистить корзину","callback_data":"x"}]])
cart_view="✅ Добавлено: {{2.name}} — {{2.qlabel}} — "+SUM+" €\n\n🧺 Ваша корзина:\n{{52text}}💶 Итого: {{formatNumber(52total; 2; \",\"; \".\")}} €"
NEWTEXT='{{51.text}}• {{2.name}} — {{2.qlabel}} — '+SUM+' €\n'
NEWTOTAL='{{ifempty(51.total; 0) + 2.total}}'
view=cart_view.replace("{{52text}}",NEWTEXT).replace("52total","(ifempty(51.total; 0) + 2.total)")
add_flow=[
 ds(50,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Добавить в корзину",
    [[eq(D(1),"q"),{"a":"{{2.total}}","b":"0","o":"number:greater"}]]),
 ds(51,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 ds(52,1500,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":{"text":NEWTEXT,"total":NEWTOTAL,"count":"{{ifempty(51.count; 0) + 1}}"}}),
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
  [api(63,1800,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🧺 Ваша корзина:\n{{61.text}}💶 Итого: {{formatNumber(61.total; 2; \",\"; \".\")}} €\n\nКуда доставить?"),("reply_markup",CITY_KB)],"Есть товары",[[{"a":"{{61.count}}","b":"0","o":"number:greater"}]])],
  [api(64,1800,y+200,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🧺 Корзина пуста."),("reply_markup",EMPTY_KB)],"Пусто",[[{"a":"{{ifempty(61.count; 0)}}","b":"0","o":"number:lessorequal"}]])],
 ])]); y+=400
CITY='{{switch('+D(2)+'; "1"; "Эдделак"; "2"; "Марне"; "3"; "Брунсбюттель"; "4"; "Хайде"; "Другое место")}}'
routes.append([
 ds(70,900,y,"UpdateRecord",{"key":CHAT,"upsert":True,"overwriteArrays":False,"data":{"seen":"{{now}}"}},"Выбран город",[[eq(D(1),"c")]]),
 ds(71,1200,y,"GetRecord",{"key":CHAT,"returnWrapped":False}),
 router(72,1500,y,[
  [api(73,1800,y,"sendMessage",[("chat_id",CHAT),("text","🧾 Ваш заказ\n{{71.text}}📍 "+CITY+"\n💳 Наличными при получении\n💶 К оплате: {{formatNumber(71.total; 2; \",\"; \".\")}} €\n\n✍️ Ответьте на это сообщение: напишите адрес доставки — улица, дом, город"),("reply_markup",'{"force_reply":true,"input_field_placeholder":"Улица, дом, город"}')],"Есть товары",[[{"a":"{{71.count}}","b":"0","o":"number:greater"}]])],
  [api(74,1800,y+200,"sendMessage",[("chat_id",CHAT),("text","🧺 Корзина пуста. Нажмите /start, чтобы выбрать товары.")],"Пусто",[[{"a":"{{ifempty(71.count; 0)}}","b":"0","o":"number:lessorequal"}]])],
 ])]); y+=400
EMPTY_REC={"text":"","total":0,"count":0}
routes.append([
 ds(80,900,y,"AddRecord",{"key":CHAT,"overwrite":True,"data":EMPTY_REC},"Очистить",[[eq(D(1),"x")]]),
 api(81,1200,y,"editMessageText",[("chat_id",CHAT),("message_id",MID),("text","🗑 Корзина очищена."),("reply_markup",EMPTY_KB)])]); y+=200
addr=api(40,900,y,"sendMessage",[("chat_id","{{1.message.chat.id}}"),("text","{{trim(first(split(1.message.reply_to_message.text; \"✍️\")))}}\n🏠 Адрес доставки: {{1.message.text}}\n\n📞 Ответьте на это сообщение: напишите ваш номер телефона"),("reply_markup","{\"force_reply\":true,\"input_field_placeholder\":\"Номер телефона\"}")],
   "Получен адрес",[[{"a":"{{1.message.reply_to_message.text}}","b":"Ваш заказ","o":"text:contain"},{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:notcontain"}]])
y+=200
g2={"id":42,"filter":{"name":"Получен телефон","conditions":[[{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:contain"}]]},"mapper":{"body":"{\"method\":\"sendMessage\",\"chat_id\":{{1.message.chat.id}},\"text\":\"✅ Спасибо! Заказ принят.\\nМы свяжемся с вами, чтобы договориться о времени доставки.\\n\\nНовый заказ: /start\"}","status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":meta(900,y),"parameters":{}}
g_clear=ds(45,1200,y,"AddRecord",{"key":"{{1.message.chat.id}}","overwrite":True,"data":EMPTY_REC})
g1=api(41,1500,y,"sendMessage",[("chat_id",GROUP),("text","🆕 НОВЫЙ ЗАКАЗ — RAIV FISH\n\n{{trim(first(split(1.message.reply_to_message.text; \"📞\")))}}\n📞 Телефон: {{1.message.text}}\n👤 Клиент: {{1.message.from.first_name}} {{1.message.from.last_name}} @{{1.message.from.username}}\n\n🗺 Маршрут: https://www.google.com/maps/search/?api=1&query={{encodeURL(trim(replace(first(split(get(split(1.message.reply_to_message.text; \"🏠\"); 2); \"📞\")); \"Адрес доставки:\"; \"\")))}}%2C%20Deutschland")])
g3=api(43,1800,y,"sendMessage",[("chat_id",GROUP),("text","💬 Связаться с клиентом в Telegram 👇"),("reply_to_message_id","{{41.body.result.message_id}}"),("reply_markup","{\"inline_keyboard\":[[{\"text\":\"💬 Написать клиенту\",\"url\":\"tg://user?id={{1.message.from.id}}\"}]]}")],onerror=True)
rts=[{"flow":r} for r in routes]+[{"flow":[addr]},{"flow":[g2,g_clear,g1,g3]}]
bp={"name":"RAIV_Fish Bot — Заказы","metadata":{"instant":True,"version":1},"flow":[
 {"id":1,"mapper":{},"module":"gateway:CustomWebHook","version":1,"metadata":meta(0,0),"parameters":{"hook":HOOK,"maxResults":1}},
 {"id":90,"mapper":{"variables":unify,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(150,0),"parameters":{}},
 {"id":2,"mapper":{"variables":variables,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":meta(300,0),"parameters":{}},
 {"id":3,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":meta(600,0),"routes":rts}]}
import re, sys
def fix(s): return re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"','"'), s)
def walk(flow):
    for m in flow:
        if m["module"]=="gateway:WebhookRespond":
            m["mapper"]["body"]=fix(m["mapper"]["body"])
            json.loads(re.sub(r"\{\{.*?\}\}","1",m["mapper"]["body"]))
        for r in m.get("routes",[]): walk(r["flow"])
walk(bp["flow"])
s=json.dumps(bp,ensure_ascii=False)
assert "@@" not in s
ids=[]
def collect(flow):
    for m in flow:
        ids.append(m["id"]); [ids.append(e["id"]) for e in m.get("onerror",[])]
        for r in m.get("routes",[]): collect(r["flow"])
collect(bp["flow"]); assert len(ids)==len(set(ids)), sorted(ids)
out = sys.argv[1] if len(sys.argv)>1 else "bp.json"
json.dump(bp,open(out,"w"),ensure_ascii=False)
print("ok", len(s), "modules", len(ids))
