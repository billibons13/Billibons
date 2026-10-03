"""Ежедневный отчёт о продажах RAIV FISH (Make, по расписанию 21:00) -> канал заказов."""
import json, sys
CONN = 11456488; GROUP = "-1004438320479"; STATS = 203279; TZ = "Europe/Berlin"
DAY = '{{formatDate(now; "YYYY-MM-DD"; "'+TZ+'")}}'
MON = '{{formatDate(now; "YYYY-MM"; "'+TZ+'")}}'
FMT = lambda e: "{{formatNumber("+e+'; 2; ","; ".")}}'
S = "3"
text = ("📊 Отчёт за {{formatDate(now; \"DD.MM.YYYY\"; \""+TZ+"\")}} — RAIV FISH\n\n"
 "🧾 Заказов: {{ifempty("+S+".orders; 0)}}\n💶 Выручка: "+FMT("ifempty("+S+".revenue; 0)")+" €\n"
 "🧮 Средний чек: "+FMT("if(ifempty("+S+".orders; 0) > 0; "+S+".revenue / "+S+".orders; 0)")+" €\n"
 "🆕 Новых клиентов: {{ifempty("+S+".newcust; 0)}}\n🎟 Скидки по промокодам: "+FMT("ifempty("+S+".disc; 0)")+" €\n"
 "💎 Оплачено бонусами: "+FMT("ifempty("+S+".bused; 0)")+" €\n"
 "⭐ Средняя оценка: {{if(ifempty("+S+".rcount; 0) > 0; formatNumber("+S+".rsum / "+S+".rcount; 1; \",\"; \".\"); \"—\")}} (оценок: {{ifempty("+S+".rcount; 0)}})\n"
 "⚖️ Продано: "+FMT("ifempty("+S+".kg; 0)")+" кг · {{ifempty("+S+".pcs; 0)}} шт\n"
 "🧺 Напомнили о брошенной корзине: {{ifempty("+S+".abandoned; 0)}}\n\n{{ifempty("+S+".lines; \"Сегодня заказов не было.\")}}\n\n"
 "📅 С начала месяца: {{ifempty(5.orders; 0)}} зак. · "+FMT("ifempty(5.revenue; 0)")+" € · ⚖️ "+FMT("ifempty(5.kg; 0)")+" кг · {{ifempty(5.pcs; 0)}} шт")
m = lambda i,x: {"designer":{"x":x,"y":0}}
bp = {"name":"RAIV_Fish — ежедневный отчёт 21:00 (кг + месяц)","metadata":{"version":1},"flow":[
 {"id":1,"module":"datastore:UpdateRecord","version":1,"metadata":m(1,0),"parameters":{"datastore":STATS},"mapper":{"key":DAY,"upsert":True,"overwriteArrays":False,"data":{"day":DAY}}},
 {"id":3,"module":"datastore:GetRecord","version":1,"metadata":m(3,300),"parameters":{"datastore":STATS},"mapper":{"key":DAY,"returnWrapped":False}},
 {"id":6,"module":"datastore:UpdateRecord","version":1,"metadata":m(6,400),"parameters":{"datastore":STATS},"mapper":{"key":MON,"upsert":True,"overwriteArrays":False,"data":{"day":MON}}},
 {"id":5,"module":"datastore:GetRecord","version":1,"metadata":m(5,450),"parameters":{"datastore":STATS},"mapper":{"key":MON,"returnWrapped":False}},
 {"id":4,"module":"telegram:UniversalAPICall","version":1,"metadata":m(4,600),"parameters":{"__IMTCONN__":CONN},
  "mapper":{"method":"POST","bodyType":"assembled_body","urlMethod":"sendMessage","body_spec":[{"key":"chat_id","value":GROUP},{"key":"text","value":text}]}}]}
json.dump(bp, open(sys.argv[1] if len(sys.argv)>1 else "daily_report_blueprint.json","w"), ensure_ascii=False, indent=1)
print("ok")
