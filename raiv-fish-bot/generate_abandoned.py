"""Брошенная корзина RAIV FISH (отдельный сценарий Make, каждый час 10:00–20:00).
Корзина с товарами, не тронутая 2 часа (но не старше 2 дней) → одно напоминание клиенту
с кнопками «Оформить» / «Добавить ещё». Повторно — только если клиент снова менял корзину.
Пишем в stats.abandoned для отчёта 21:00. Отписавшимся (/stop) не пишем.
"""
import json, sys, os, importlib.util
sys.argv = [sys.argv[0], "/tmp/_bp_tmp.json"]
spec = importlib.util.spec_from_file_location("g", os.path.join(os.path.dirname(__file__) or ".", "generate_blueprint.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
CONN, DS, CUST, STATS, TZ, MIN_ORDER = g.CONN, g.DS, g.CUST, g.STATS, g.TZ, g.MIN_ORDER
M = lambda x,y=0: {"designer":{"x":x,"y":y}}
FMT = lambda e: "{{formatNumber("+e+'; 2; ","; ".")}}'
DAY = '{{formatDate(now; "YYYY-MM-DD"; "'+TZ+'")}}'
HOUR = '{{formatDate(now; "H"; "'+TZ+'")}}'

text = ("🧺 Вы собрали корзину, но не оформили заказ:\n{{1.data.text}}"
        "💶 Итого: "+FMT("1.data.total")+" €\n\n"
        "{{if(1.data.total >= "+str(MIN_ORDER)+"; \"🚗 Доставка бесплатно. \"; \"Добавьте товаров до "+str(MIN_ORDER)+" € — и доставка бесплатно. \")}}"
        "Оформление займёт минуту 👇\n\n/stop — не получать сообщения")
kb = [[{"text":"🧾 Оформить заказ","callback_data":"o"}],[{"text":"➕ Добавить ещё","callback_data":"m"}]]

bp = {"name":"RAIV_Fish — брошенная корзина (каждый час)","metadata":{"version":1},"flow":[
 {"id":1,"module":"datastore:SearchRecord","version":1,"metadata":M(0),"parameters":{"datastore":DS,"continueWhenNoRes":False,"limit":50},
  "mapper":{"filter":[[{"a":"count","o":"number:greater","b":"0"},
                       {"a":"seen","o":"date:less","b":"{{addHours(now; -2)}}"},
                       {"a":"seen","o":"date:greater","b":"{{addDays(now; -2)}}"}]],"sort":[]},
  "filter":None},
 {"id":2,"module":"datastore:GetRecord","version":1,"metadata":M(300),"parameters":{"datastore":CUST},"mapper":{"key":"{{1.key}}","returnWrapped":False},
  "filter":{"name":"Не напоминали · дневное время","conditions":[
     [{"a":"{{1.data.abandon_notified}}","o":"notexist"},{"a":HOUR,"o":"number:greaterorequal","b":"10"},{"a":HOUR,"o":"number:lessorequal","b":"20"}],
     [{"a":"{{1.data.abandon_notified}}","o":"date:less","b":"{{1.data.seen}}"},{"a":HOUR,"o":"number:greaterorequal","b":"10"},{"a":HOUR,"o":"number:lessorequal","b":"20"}]]}},
 {"id":3,"module":"telegram:UniversalAPICall","version":1,"metadata":M(600),"parameters":{"__IMTCONN__":CONN},
  "mapper":{"method":"POST","bodyType":"assembled_body","urlMethod":"sendMessage","body_spec":[
     {"key":"chat_id","value":"{{1.key}}"},{"key":"text","value":text},
     {"key":"reply_markup","value":json.dumps({"inline_keyboard":kb},ensure_ascii=False)}]},
  "filter":{"name":"Не отписан","conditions":[[{"a":"{{2.blocked}}","o":"notexist"}],[{"a":"{{2.blocked}}","o":"boolean:isfalse"}]]},
  "onerror":[{"id":503,"module":"builtin:Ignore","version":1,"metadata":M(600,300),"mapper":None}]},
 {"id":4,"module":"datastore:UpdateRecord","version":1,"metadata":M(900),"parameters":{"datastore":DS},
  "mapper":{"key":"{{1.key}}","upsert":False,"overwriteArrays":False,"data":{"abandon_notified":"{{now}}"}}},
 {"id":5,"module":"datastore:UpdateRecord","version":1,"metadata":M(1200),"parameters":{"datastore":STATS},
  "mapper":{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}}},
 {"id":6,"module":"datastore:GetRecord","version":1,"metadata":M(1500),"parameters":{"datastore":STATS},"mapper":{"key":DAY,"returnWrapped":False}},
 {"id":7,"module":"datastore:UpdateRecord","version":1,"metadata":M(1800),"parameters":{"datastore":STATS},
  "mapper":{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"abandoned":"{{ifempty(6.abandoned; 0) + 1}}"}}},
]}
bp["flow"][0].pop("filter")
f=bp["flow"]; f[3]["filter"]=f[2].pop("filter"); f[2],f[3]=f[3],f[2]  # сначала отметка, потом отправка
os.makedirs("backup", exist_ok=True)
json.dump(bp, open("backup/abandoned_cart_blueprint.json","w"), ensure_ascii=False, indent=1)
print("ok")
