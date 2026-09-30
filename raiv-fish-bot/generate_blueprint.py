import json
CONN = 11456488  # RAIV_Fish Telegram Bot
GROUP = "-1003911949676"
HOOK = 3818163
cats = [
 ("a","🐟 Икра вяленая (100 г)",[("Икра толстолоба","6",1),("Икра кеты","8.5",1),("Икра форели","8.5",1),("Икра судака","6.5",0),("Икра щуки","7",1),("Икра плотвы","7",0),("Икра минтая","6.5",0)]),
 ("b","🐠 Рыба вяленая (кг)",[("Плотва с икрой","35",1),("Чищенные тушки плотвы без головы (100% икра)","49",1),("Вобла с икрой (80% икра)","30",1),("Верховодка","35",1),("Лещ с икрой","35",1),("Лещ без икры","20",0),("Карась с икрой","23",1),("Щука потрошеная","25",1),("Форель вяленая потрошеная","35",1),("Судак потрошеный","30",1),("Чехонь","25",1),("Чехонь крупная с икрой 90%","35",1),("Бычок","34",1),("Корюшка с икрой (премиум)","60",0),("Окунь с икрой","34",1),("Юкола лосося","67",1)]),
 ("c","🍢 Рыбные снеки (100 г)",[("Филе горбуши (соломка)","6",1),("Кальмар + лосось (соломка)","4.9",1),("Корюшка сушеная потрошеная","5.5",1),("Соломка леща","3.5",1),("Джерки лосося","6",1),("Ириска из лосося","6",1),("Стейк щуки","4.5",1)]),
 ("d","🦑 Снеки к пиву (кг)",[("Пятачки осьминога","40",1),("Паутинка кальмара «сладкий чили»","40",1),("Кальмар по-шанхайски","40",1),("Стружка кальмара","40",1),("Палочки патасу","40",1),("Филе голубого марлина","40",1),("Кальмар по-перуански","40",1),("Полосатик","40",1),("Стружка краба","40",1),("Анчоус","40",1),("Крабовые палочки","40",1)]),
 ("e","🥫 Консервы",[("Снеток в томате","5",1),("Лещ в томате","5",1)]),
]
UNIT = {"a":"g","b":"k","c":"g","d":"k","e":"p"}
ULBL = {"a":"€ / 100 г","b":"€ / кг","c":"€ / 100 г","d":"€ / кг","e":"€ / шт."}
QTY = {"g":["100","200","300","500"],"k":["0.5","1","1.5","2"],"p":["1","2","3","5"]}
QL = {"g":"г","k":"кг","p":"шт."}
items = {}
for c,_,lst in cats:
    for i,(n,p,s) in enumerate(lst,1): items[f"{c}{i}"]=(n,p,s)
def D(n): return f'get(split(1.callback_query.data; "|"); {n})'
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
 {"name":"city","value":"{{"+f'switch(ifempty({D(4)}; "0"); "1"; "Эдделак"; "2"; "Марне"; "3"; "Брунсбюттель"; "4"; "Хайде"; "Другое место")'+"}}"},
]
# ---- main menu text
menu = """Здравствуйте! 🐟 RAIV FISH — вяленая рыба и снеки.
Весь ассортимент и наличие внизу. То, что отмечено ❌, — нет в наличии.

"""
for c,title,lst in cats:
    menu += title.upper() if c!="e" else "🥫 КОНСЕРВЫ"
    menu += "\n"
    for n,p,s in lst:
        menu += f"• {n} — {p.replace('.',',')} {ULBL[c]}" + ("❌" if not s else "") + "\n"
    menu += "\n"
menu += "🚗 Доставка каждый день: Эдделак, Марне, Брунсбюттель, Хайде\n💶 Оплата при получении\n\nВыберите раздел 👇"
cat_kb = lambda mode: {"inline_keyboard":[[{"text":t,"callback_data":f"k|{c}|{mode}"}] for c,t,_ in cats]}
T = {}  # placeholder -> raw template
def ph(expr):
    k=f"@@{len(T)}@@"; T[k]=expr; return k
def body(obj):
    s=json.dumps(obj,ensure_ascii=False)
    for k,v in T.items():
        s=s.replace(f'"{k}"',v).replace(k,v)
    return s
CB_CHAT="{{1.callback_query.message.chat.id}}"; CB_MID="{{1.callback_query.message.message_id}}"
def resp(mid, x, y, name, cond, obj):
    return {"id":mid,"filter":{"name":name,"conditions":[cond]},"mapper":{"body":body(obj),"status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":{"designer":{"x":x,"y":y}},"parameters":{}}
def eq(a,b): return {"a":"{{"+a+"}}","b":b,"o":"text:equal"}
routes=[]
chat=ph("{{1.message.chat.id}}")
routes.append(resp(4,900,-900,"Меню",[{"a":"{{1.message.text}}","o":"exist"},{"a":"{{1.message.reply_to_message.message_id}}","o":"notexist"}],
  {"method":"sendMessage","chat_id":chat,"text":menu,"reply_markup":cat_kb("s")}))
cbchat=ph(CB_CHAT); cbmid=ph(CB_MID)
routes.append(resp(5,900,-700,"Разделы",[eq(D(1),"m")],
  {"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"Выберите раздел 👇","reply_markup":cat_kb("e")}))
# category: one route per category
y=-500
for idx,(c,title,lst) in enumerate(cats):
    kb=[[{"text":f"{n} — {p.replace('.',',')} {ULBL[c]}","callback_data":f"f|{c}{i}"}] for i,(n,p,s) in enumerate(lst,1) if s]
    kb.append([{"text":"⬅️ Все разделы","callback_data":"m"}])
    method=ph('"{{if('+D(3)+' = "e"; "editMessageText"; "sendMessage")}}"')
    routes.append(resp(6+idx,900,y,f"Раздел {c}",[eq(D(1),"k"),eq(D(2),c)],
      {"method":method,"chat_id":cbchat,"message_id":cbmid,"text":f"{title}\n\nВыберите товар 👇","reply_markup":{"inline_keyboard":kb}}))
    y+=200
# product chosen -> qty (one route per unit type)
mid=20
for u in ["g","k","p"]:
    prefs=[c for c in UNIT if UNIT[c]==u]
    code=ph("{{"+D(2)+"}}"); 
    qk=[[{"text":f"{q.replace('.',',')} {QL[u]}","callback_data":f"q|@@CODE@@|{q}"} for q in QTY[u][:2]],[{"text":f"{q.replace('.',',')} {QL[u]}","callback_data":f"q|@@CODE@@|{q}"} for q in QTY[u][2:]],[{"text":"⬅️ Назад","callback_data":"k|@@CAT@@|e"}]]
    T["@@CODE@@"]="{{"+D(2)+"}}"; T["@@CAT@@"]="{{"+pref+"}}"
    cond=[eq(D(1),"f")]
    conds=[[eq(D(1),"f"),{"a":"{{"+pref+"}}","b":p_,"o":"text:equal"}] for p_ in prefs]
    obj={"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":"🐟 {{2.name}} — {{replace(2.price; \".\"; \",\")}} {{2.ulabel}}\n\nСколько взять?","reply_markup":{"inline_keyboard":qk}}
    r=resp(mid,900,y,f"Товар ({u})",[],obj); r["filter"]["conditions"]=conds
    routes.append(r); mid+=1; y+=200
SUM='{{formatNumber(2.total; 2; ","; ".")}}'
SUM20='{{formatNumber(2.total * 1.2; 2; ","; ".")}}'
D2=ph("{{"+D(2)+"}}"); D3=ph("{{"+D(3)+"}}"); D4=ph("{{"+D(4)+"}}")
T["@@D2@@"]="{{"+D(2)+"}}"; T["@@D3@@"]="{{"+D(3)+"}}"; T["@@D4@@"]="{{"+D(4)+"}}"
base="@@D2@@|@@D3@@"
cities=["Эдделак","Марне","Брунсбюттель","Хайде","Другое место"]
ck=[[{"text":cities[0],"callback_data":f"c|{base}|1"},{"text":cities[1],"callback_data":f"c|{base}|2"}],[{"text":cities[2],"callback_data":f"c|{base}|3"},{"text":cities[3],"callback_data":f"c|{base}|4"}],[{"text":cities[4],"callback_data":f"c|{base}|5"}]]
routes.append(resp(mid,900,y,"Выбран вес",[eq(D(1),"q")],{"method":"editMessageText","chat_id":cbchat,"message_id":cbmid,"text":f"🐟 {{{{2.name}}}} — {{{{2.qlabel}}}}\n💶 Сумма: {SUM} €\n\nКуда доставить?","reply_markup":{"inline_keyboard":ck}})); mid+=1; y+=200
fr={"force_reply":True,"input_field_placeholder":"Улица, дом, город"}
routes.append(resp(mid,900,y,"Выбран город → заказ",[eq(D(1),"c")],{"method":"sendMessage","chat_id":cbchat,"text":f"🧾 Ваш заказ\n🐟 {{{{2.name}}}} — {{{{2.qlabel}}}}\n📍 {{{{2.city}}}}\n💳 Наличными при получении\n💶 К оплате: {SUM} €\n\n✍️ Ответьте на это сообщение: напишите адрес доставки — улица, дом, город","reply_markup":fr})); mid+=1; y+=200
addr={"id":40,"filter":{"name":"Получен адрес","conditions":[[{"a":"{{1.message.reply_to_message.text}}","b":"Ваш заказ","o":"text:contain"},{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:notcontain"}]]},
 "mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":"chat_id","value":"{{1.message.chat.id}}"},{"key":"text","value":"{{trim(first(split(1.message.reply_to_message.text; \"✍️\")))}}\n🏠 Адрес доставки: {{1.message.text}}\n\n📞 Ответьте на это сообщение: напишите ваш номер телефона"},{"key":"reply_markup","value":"{\"force_reply\":true,\"input_field_placeholder\":\"Номер телефона\"}"}],"urlMethod":"sendMessage"},
 "module":"telegram:UniversalAPICall","version":1,"metadata":{"designer":{"x":900,"y":y}},"parameters":{"__IMTCONN__":CONN}}
y+=200
g1={"id":41,"filter":{"name":"Получен телефон","conditions":[[{"a":"{{1.message.reply_to_message.text}}","b":"Адрес доставки:","o":"text:contain"}]]},
 "mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":"chat_id","value":GROUP},{"key":"text","value":"🆕 НОВЫЙ ЗАКАЗ — RAIV FISH\n\n{{trim(first(split(1.message.reply_to_message.text; \"📞\")))}}\n📞 Телефон: {{1.message.text}}\n👤 Клиент: {{1.message.from.first_name}} {{1.message.from.last_name}} @{{1.message.from.username}}\n\n🗺 Маршрут: https://www.google.com/maps/search/?api=1&query={{encodeURL(trim(replace(first(split(get(split(1.message.reply_to_message.text; \"🏠\"); 2); \"📞\")); \"Адрес доставки:\"; \"\")))}}%2C%20Deutschland"}],"urlMethod":"sendMessage"},
 "module":"telegram:UniversalAPICall","version":1,"metadata":{"designer":{"x":900,"y":y}},"parameters":{"__IMTCONN__":CONN}}
g2={"id":42,"mapper":{"body":"{\"method\":\"sendMessage\",\"chat_id\":{{1.message.chat.id}},\"text\":\"✅ Спасибо! Заказ принят.\\nМы свяжемся с вами, чтобы договориться о времени доставки.\\n\\nНовый заказ: /start\"}","status":200,"headers":[{"key":"Content-Type","value":"application/json"}]},"module":"gateway:WebhookRespond","version":1,"metadata":{"designer":{"x":1200,"y":y}},"parameters":{}}
g3={"id":43,"mapper":{"method":"POST","bodyType":"assembled_body","body_spec":[{"key":"chat_id","value":GROUP},{"key":"text","value":"💬 Связаться с клиентом в Telegram 👇"},{"key":"reply_to_message_id","value":"{{41.body.result.message_id}}"},{"key":"reply_markup","value":"{\"inline_keyboard\":[[{\"text\":\"💬 Написать клиенту\",\"url\":\"tg://user?id={{1.message.from.id}}\"}]]}"}],"urlMethod":"sendMessage"},
 "module":"telegram:UniversalAPICall","onerror":[{"id":44,"mapper":None,"module":"builtin:Ignore","version":1,"metadata":{"designer":{"x":1500,"y":y+300}}}],"version":1,"metadata":{"designer":{"x":1500,"y":y}},"parameters":{"__IMTCONN__":CONN}}
rts=[{"flow":[r]} for r in routes]+[{"flow":[addr]},{"flow":[g1,g2,g3]}]
bp={"name":"RAIV_Fish Bot — Заказы","metadata":{"instant":True,"version":1},"flow":[
 {"id":1,"mapper":{},"module":"gateway:CustomWebHook","version":1,"metadata":{"designer":{"x":0,"y":0}},"parameters":{"hook":HOOK,"maxResults":1}},
 {"id":2,"mapper":{"variables":variables,"scope":"roundtrip"},"module":"util:SetVariables","version":1,"metadata":{"designer":{"x":300,"y":0}},"parameters":{}},
 {"id":3,"mapper":None,"module":"builtin:BasicRouter","version":1,"metadata":{"designer":{"x":600,"y":0}},"routes":rts}]}
s=json.dumps(bp,ensure_ascii=False)
assert "@@" not in s, [m for m in T if m in s]
json.dump(bp,open("bp.json","w"),ensure_ascii=False)
print(len(s), len(menu))
# check callback byte lengths worst-case
print(max(len(f"p|{k}|1.5|5|D".encode()) for k in items))
# validate bodies are valid JSON after substituting sample
import re
for r in routes:
    b=re.sub(r"\{\{.*?\}\}","1",r["mapper"]["body"])
    json.loads(b)
print("ok")
import re
def fix(s): return re.sub(r"\{\{.*?\}\}", lambda m: m.group(0).replace('\\"','"'), s)
for rt in bp["flow"][2]["routes"]:
    for m in rt["flow"]:
        if m["module"]=="gateway:WebhookRespond": m["mapper"]["body"]=fix(m["mapper"]["body"])
json.dump(bp,open("bp.json","w"),ensure_ascii=False)
for rt in bp["flow"][2]["routes"]:
    m=rt["flow"][0]
    if m["module"]=="gateway:WebhookRespond":
        json.loads(re.sub(r"\{\{.*?\}\}","1",m["mapper"]["body"]))
print(bp["flow"][2]["routes"][10]["flow"][0]["mapper"]["body"][:260])
