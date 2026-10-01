"""Подбор товаров под сценарии Klaus.

Сценарии приходят из Make-сценария «Meister Klaus — 1. Wochenskripte» в формате:
    [Tag] – [Titel]
    Hook (0–3 s): ...
    ...
    Produkt: [Produkttyp] oder «nur Tipp»
Скрипты разделены строкой '---'. Если в скрипте «nur Tipp», товары не подбираются —
не продаём там, где Klaus просто даёт совет.
"""
import re

from .taxonomy import COMPLIANCE_NOTES, PROBLEMS

ROLE_ORDER = {"solve": 0, "measure": 1, "prevent": 2, "protect": 3}


def _norm(s):
    return re.sub(r"\s+", " ", (s or "").lower().replace("ß", "ss")).strip()


def split_scripts(text):
    parts = [p.strip() for p in re.split(r"^\s*-{3,}\s*$", text or "", flags=re.MULTILINE)]
    scripts = []
    for part in parts:
        if not part:
            continue
        lines = [l.strip() for l in part.splitlines() if l.strip()]
        title = lines[0] if lines else ""
        m = re.search(r"^Produkt\s*:\s*(.+)$", part, flags=re.MULTILINE | re.IGNORECASE)
        product = m.group(1).strip().strip("[]«»\"' ") if m else None
        scripts.append({"title": title, "text": part, "product_hint": product,
                        "tip_only": bool(product and "nur tipp" in _norm(product))})
    return scripts


def detect_problems(text):
    t = _norm(text)
    hits = []
    for key, prob in PROBLEMS.items():
        n = sum(1 for kw in prob["keywords"] if _norm(kw) in t)
        if n:
            hits.append((n, key))
    hits.sort(key=lambda x: (-x[0], x[1]))
    return [k for _, k in hits]


def _hint_matches(hint, product_type):
    h, p = _norm(hint), _norm(product_type)
    if not h:
        return False
    words = [w for w in re.split(r"[^a-zäöü0-9]+", p) if len(w) > 3]
    return h in p or p in h or any(w in h for w in words)


def match_script(script, max_products=6):
    """Возвращает список типов товаров, реально связанных с проблемой в ролике."""
    if isinstance(script, str):
        script = (split_scripts(script) or [{"title": "", "text": script, "product_hint": None, "tip_only": False}])[0]
    if script.get("tip_only"):
        return {"title": script["title"], "tip_only": True, "problems": [], "products": []}
    problems = detect_problems(script["text"])[:2]
    hint = script.get("product_hint")
    seen, products = set(), []
    # Сначала — то, что назвал сам сценарий (Produkt: ...), если такой тип есть в таксономии.
    if hint:
        for key, prob in PROBLEMS.items():
            for ptype, query, role in prob["products"]:
                if _hint_matches(hint, ptype) and ptype not in seen:
                    seen.add(ptype)
                    products.append(_row(key, prob, ptype, query, role, explicit=True))
                    if key not in problems:
                        problems.append(key)
    for key in problems:
        prob = PROBLEMS[key]
        for ptype, query, role in sorted(prob["products"], key=lambda r: ROLE_ORDER[r[2]]):
            if ptype not in seen:
                seen.add(ptype)
                products.append(_row(key, prob, ptype, query, role, explicit=False))
    return {"title": script["title"], "tip_only": False, "problems": problems,
            "product_hint": hint, "products": products[:max_products]}


def _row(key, prob, ptype, query, role, explicit):
    return {"problem": key, "category": prob["category"], "product_type": ptype, "search_query_de": query,
            "role": role, "from_script_hint": explicit,
            "compliance": [COMPLIANCE_NOTES[c] for c in prob["compliance"]]}


def match_week(text):
    return [match_script(s) for s in split_scripts(text)]
