"""📦 Агент склада: каждое утро присылает владельцу сводку наличия и кнопки «Склад».
Нажатие на товар в боте сразу переключает наличие (маршрут ct|... в основном сценарии, только владелец).
Агент сам ничего не меняет — только напоминает и показывает, что скрыто.
"""
import json, sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
argv = sys.argv[:]; sys.argv = [sys.argv[0], "/tmp/_bp_tmp.json"]
spec = importlib.util.spec_from_file_location("g", os.path.join(here, "generate_blueprint.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)
meta = lambda x: {"designer": {"x": x, "y": 0}}
bp = {"name": "RAIV_Fish — 📦 агент склада (утро 09:00)", "metadata": {"version": 1}, "flow": [
 {"id": 1, "module": "datastore:SearchRecord", "version": 1, "metadata": meta(0),
  "parameters": {"datastore": g.PROMO, "continueWhenNoRes": True, "limit": 100},
  "mapper": {"filter": [[{"a": "item", "o": "exist"}]], "sort": []}},
 {"id": 2, "module": "builtin:BasicAggregator", "version": 1, "metadata": meta(300), "parameters": {"feeder": 1},
  "mapper": {"off": "".join('{{if(1.data.stock; ""; %s)}}' % x for x in ['"• "', '1.data.item', '" · "', '1.data.name']), "on": '{{if(1.data.stock; 1; 0)}}'},
  "filter": {"name": "Товар", "conditions": [[{"a": "{{1.data.item}}", "o": "exist"}]]}},
 {"id": 3, "module": "telegram:UniversalAPICall", "version": 1, "metadata": meta(600), "parameters": {"__IMTCONN__": g.CONN},
  "mapper": {"method": "POST", "bodyType": "assembled_body", "urlMethod": "sendMessage", "body_spec": [
   {"key": "chat_id", "value": g.OWNER_ID},
   {"key": "text", "value": "📦 Доброе утро! Проверка наличия RAIV FISH\n\n✅ В продаже: {{sum(map(2.array; \"on\"))}} из {{length(2.array)}}\n❌ Скрыто (нет в наличии):\n{{ifempty(join(remove(map(2.array; \"off\"); \"\"); \"\n\"); \"— всё в наличии\")}}\n\nЧто-то закончилось или появилось? Откройте раздел и нажмите на товар — бот и витрина обновятся сразу."},
   {"key": "reply_markup", "value": g.SK_MENU}]},
  "onerror": [{"id": 503, "mapper": None, "module": "builtin:Ignore", "version": 1, "metadata": meta(600)}]}]}
out = argv[1] if len(argv) > 1 else "stock_agent_blueprint.json"
json.dump(bp, open(out, "w"), ensure_ascii=False, indent=1); print("ok", out)
