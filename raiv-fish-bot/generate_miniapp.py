"""Mini App витрина RAIV FISH (GitHub Pages: billibons13.github.io/Billibons, ветка gh-pages).
Каталог и цены берутся из generate_blueprint.py — один источник правды.
Витрина отправляет в бота только коды и количества ("b5:1,a2:300"); сумму бот считает сам.
"""
import json, sys, os, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
sys.argv = [sys.argv[0], "/tmp/_bp_tmp.json"]
spec = importlib.util.spec_from_file_location("g", os.path.join(here, "generate_blueprint.py"))
g = importlib.util.module_from_spec(spec); spec.loader.exec_module(g)

photos = {f[:-4] for f in os.listdir(os.path.join(here, "miniapp", "img")) if f.endswith(".jpg")}
cats = [{"c": c, "t": t, "u": g.UNIT[c], "q": g.QTY[c], "l": g.ULBL[c],
         "items": [{"k": f"{c}{i}", "n": n, "p": float(p), "s": s, "img": (f"img/{c}{i}.jpg" if f"{c}{i}" in photos else "")}
                   for i, (n, p, s) in enumerate(lst, 1)]} for c, t, lst in g.cats]
data = {"cats": cats, "min": g.MIN_ORDER, "bonus": g.BONUS_PCT, "bot": g.BOT_USER, "seller": g.SELLER, "api": g.CATALOG_API}

tpl = open(os.path.join(here, "miniapp", "template.html"), encoding="utf-8").read()
out = tpl.replace("/*@@DATA@@*/", "const DATA = " + json.dumps(data, ensure_ascii=False) + ";")
open(os.path.join(here, "miniapp", "index.html"), "w", encoding="utf-8").write(out)
print("ok", sum(len(c["items"]) for c in cats), "товаров,", len(photos), "фото")
