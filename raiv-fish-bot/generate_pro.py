"""Pro-функции RAIV FISH (отдельные сценарии Make):
  1) AI-помощник владельца — каждое утро 08:30 разбирает продажи и даёт советы (только советы, решения — владелец)
  2) Напоминания клиентам, которые не заходили 14 дней (одно напоминание на период неактивности)
"""
import json, sys, os, importlib.util
sys.argv = [sys.argv[0], "/tmp/_bp_tmp.json"]
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__) or ".", "generate_blueprint.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
CONN, OWNER, STATS, CUST, TZ = g.CONN, g.OWNER_ID, g.STATS, g.CUST, g.TZ
REMIND_DAYS = 14
out_of_stock = ", ".join(n for _,_,lst in g.cats for n,p,s in lst if not s)
catalog = "; ".join(f"{n} {p.replace('.',',')} {g.ULBL[c]}" for c,_,lst in g.cats for n,p,s in lst if s)
M = lambda x,y=0: {"designer":{"x":x,"y":y}}
FMT = lambda e: "{{formatNumber("+e+'; 2; ","; ".")}}'
def day(n): return '{{formatDate(addDays(now; '+str(n)+'); "YYYY-MM-DD"; "'+TZ+'")}}'
def touch(i,x,key): return {"id":i,"module":"datastore:UpdateRecord","version":1,"metadata":M(x),"parameters":{"datastore":STATS},"mapper":{"key":key,"upsert":True,"overwriteArrays":False,"data":{"day":key}}}
def get(i,x,key,store): return {"id":i,"module":"datastore:GetRecord","version":1,"metadata":M(x),"parameters":{"datastore":store},"mapper":{"key":key,"returnWrapped":False}}
def tg(i,x,chat,text,kb=None,onerror=False):
    spec=[{"key":"chat_id","value":chat},{"key":"text","value":text}]
    if kb: spec.append({"key":"reply_markup","value":json.dumps({"inline_keyboard":kb},ensure_ascii=False)})
    m={"id":i,"module":"telegram:UniversalAPICall","version":1,"metadata":M(x),"parameters":{"__IMTCONN__":CONN},"mapper":{"method":"POST","bodyType":"assembled_body","urlMethod":"sendMessage","body_spec":spec}}
    if onerror: m["onerror"]=[{"id":i+500,"module":"builtin:Ignore","version":1,"metadata":M(x,300),"mapper":None}]
    return m

# ---------- 1) AI-помощник
MON = '{{formatDate(now; "YYYY-MM"; "'+TZ+'")}}'
Y, Y2 = day(-1), day(-2)
stat = lambda s: ("заказов {{ifempty("+s+".orders; 0)}}, выручка "+FMT("ifempty("+s+".revenue; 0)")+" €, новых клиентов {{ifempty("+s+".newcust; 0)}}, скидки "+FMT("ifempty("+s+".disc; 0)")+" €, бонусами "+FMT("ifempty("+s+".bused; 0)")+" €")
prompt = ("Ты — помощник владельца небольшого магазина вяленой рыбы и снеков RAIV FISH (доставка: Эдделак, Марне, Брунсбюттель, Хайде; заказы через Telegram-бота). "
 "Дай владельцу 3 коротких конкретных совета на сегодня по-русски: что продвигать, кому и что написать, какую акцию или промокод можно предложить. "
 "Правила: ты только советуешь; не меняй цены и не обещай клиентам скидки от имени магазина; учитывай, что товаров «нет в наличии» продвигать нельзя. "
 "Пиши без вступлений, нумерованным списком, каждый пункт 1–2 предложения, в конце одна строка «Идея для рассылки:» с готовым текстом до 300 знаков.\n\n"
 "Вчера: "+stat("2")+".\nПозавчера: "+stat("4")+".\nЗаказы вчера:\n{{ifempty(2.lines; \"нет\")}}\n"
 "С начала месяца: заказов {{ifempty(12.orders; 0)}}, выручка "+FMT("ifempty(12.revenue; 0)")+" €, продано "+FMT("ifempty(12.kg; 0)")+" кг.\n"
 "Всего клиентов в базе бота: {{6.count}}.\nКаталог сейчас (живые цены, ✅ есть / ❌ нет в наличии):\n{{join(map(10.array; \"line\"); \"\n\")}}")
report = ("🤖 AI-помощник RAIV FISH · {{formatDate(now; \"DD.MM\"; \""+TZ+"\")}}\n\n"
 "📊 Вчера: {{ifempty(2.orders; 0)}} зак. · "+FMT("ifempty(2.revenue; 0)")+" € · ⚖️ "+FMT("ifempty(2.kg; 0)")+" кг (позавчера "+FMT("ifempty(4.revenue; 0)")+" €)\n"
 "📅 Месяц: {{ifempty(12.orders; 0)}} зак. · "+FMT("ifempty(12.revenue; 0)")+" € · "+FMT("ifempty(12.kg; 0)")+" кг · клиентов в базе: {{6.count}}\n\n"
 "{{7.answer}}\n\n"
 "ℹ️ Это советы. Решаете вы: /promo КОД 10 — промокод, /send текст — рассылка.")
ai = {"name":"RAIV_Fish Pro — AI-помощник 08:30 (живой каталог)","metadata":{"version":1},"flow":[
 touch(1,0,Y), get(2,300,Y,STATS), touch(3,600,Y2), get(4,900,Y2,STATS),
 {"id":6,"module":"datastore:Stats","version":1,"metadata":M(1200),"parameters":{"datastore":CUST},"mapper":{}},
 touch(11,1250,MON), get(12,1300,MON,STATS),
 {"id":9,"module":"datastore:SearchRecord","version":1,"metadata":M(1350),"parameters":{"datastore":g.CATALOG if hasattr(g,"CATALOG") else 203278,"continueWhenNoRes":True,"limit":100},"mapper":{"filter":[[{"a":"item","o":"exist"}]],"sort":[]}},
 {"id":10,"module":"builtin:BasicAggregator","version":1,"metadata":M(1400),"parameters":{"feeder":9},"mapper":{"line":"{{if(9.data.stock; \"✅\"; \"❌\")}} {{9.data.name}} — {{replace(toString(9.data.price); \".\"; \",\")}} {{switch(9.data.cat; \"a\"; \"€/100 г\"; \"c\"; \"€/100 г\"; \"e\"; \"€/шт\"; \"€/кг\")}}"},
  "filter":{"name":"Товар","conditions":[[{"a":"{{9.data.item}}","o":"exist"}]]}},
 {"id":7,"module":"ai-tools:Ask","version":1,"metadata":M(1500),"parameters":{},"mapper":{"input":prompt}},
 tg(8,1800,OWNER,report)]}

# ---------- 2) Напоминания
CUT = "{{addDays(now; -"+str(REMIND_DAYS)+")}}"
base = [{"a":"orders","o":"number:greater","b":"0"},{"a":"last_seen","o":"date:less","b":CUT}]
remind_text = ("👋 Давно не виделись! У нас свежая вяленая рыба и снеки.\n"
 "💎 Ваши бонусы: "+FMT("ifempty(1.data.bonus; 0)")+" € — спишутся при заказе автоматически.\n\n"
 "Соберите прошлый заказ одной кнопкой 👇\n\n/stop — не получать сообщения")
rem = {"name":"RAIV_Fish Pro — напоминания (14 дней) 11:00","metadata":{"version":1},"flow":[
 {"id":1,"module":"datastore:SearchRecord","version":1,"metadata":M(0),"parameters":{"datastore":CUST,"continueWhenNoRes":False,"limit":200},
  "mapper":{"filter":[base+[{"a":"blocked","o":"notexist"}], base+[{"a":"blocked","o":"boolean:isfalse"}]],"sort":[]}},
 dict(tg(2,300,"{{1.data.chat}}",remind_text,[[{"text":"🔁 Повторить прошлый заказ","callback_data":"r"}],[{"text":"📋 Каталог","callback_data":"m"}]],onerror=True),
      filter={"name":"Ещё не напоминали","conditions":[[{"a":"{{1.data.reminded}}","o":"notexist"}],[{"a":"{{1.data.reminded}}","o":"date:less","b":"{{1.data.last_seen}}"}]]}),
 {"id":3,"module":"datastore:UpdateRecord","version":1,"metadata":M(600),"parameters":{"datastore":CUST},"mapper":{"key":"{{1.key}}","upsert":False,"overwriteArrays":False,"data":{"reminded":"{{now}}"}}}]}

os.makedirs("backup", exist_ok=True)
json.dump(ai, open("backup/pro_ai_assistant_blueprint.json","w"), ensure_ascii=False, indent=1)
json.dump(rem, open("backup/pro_reminders_blueprint.json","w"), ensure_ascii=False, indent=1)
print("ok", len(prompt))
