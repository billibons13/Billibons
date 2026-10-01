"""Обучение на фактических результатах: какие категории и сценарии Klaus приносят деньги.

Берёт записи из Make data store (как их отдаёт data-store-records_list) и считает по категориям
реальные CTR (клики/просмотры), конверсию (продажи/клики), долю подтверждённых (1 − возвраты/продажи)
и фактический EPM. Пока данных мало (меньше MIN_VIEWS просмотров), категория помечается как "мало данных"
и scoring продолжает работать на допущениях.
"""
from collections import defaultdict

MIN_VIEWS = 3000
MIN_CLICKS = 30


def _num(x):
    try:
        return float(x) if x not in (None, "") else 0.0
    except (TypeError, ValueError):
        return 0.0


def category_stats(records):
    agg = defaultdict(lambda: {"products": 0, "published": 0, "views": 0.0, "clicks": 0.0, "sales": 0.0,
                               "refunds": 0.0, "commission": 0.0})
    for r in records:
        d = r.get("data", r)
        if d.get("category") in (None, "", "_klaus_scripts"):
            continue
        a = agg[d["category"]]
        a["products"] += 1
        a["published"] += d.get("video_status") == "published"
        for k, f in (("views", "views"), ("clicks", "clicks"), ("sales", "sales"), ("refunds", "refunds"),
                     ("commission", "confirmed_commission_eur")):
            a[k] += _num(d.get(f))
    out = {}
    for cat, a in agg.items():
        enough = a["views"] >= MIN_VIEWS and a["clicks"] >= MIN_CLICKS
        s = {**a, "enough_data": enough,
             "ctr": round(a["clicks"] / a["views"], 4) if a["views"] else None,
             "conversion": round(a["sales"] / a["clicks"], 4) if a["clicks"] else None,
             "approval": round(1 - a["refunds"] / a["sales"], 4) if a["sales"] else None,
             "epm_measured_eur": round(1000 * a["commission"] / a["views"], 2) if a["views"] else None}
        out[cat] = s
    return dict(sorted(out.items(), key=lambda kv: -(kv[1]["epm_measured_eur"] or 0)))


def real_rates(stats, category):
    """Фактические коэффициенты для scoring.epm_scenarios — только если данных достаточно."""
    s = stats.get(category)
    if not s or not s["enough_data"] or s["approval"] is None:
        return None
    return {"ctr": s["ctr"], "conversion": s["conversion"], "approval": s["approval"]}
