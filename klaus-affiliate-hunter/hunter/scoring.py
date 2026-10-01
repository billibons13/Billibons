"""Коммерческая оценка товара и приоритет A / B / C.

Ожидаемое вознаграждение за продажу = цена × комиссия (считается в product.normalize).
EPM (доход на 1000 просмотров) — только СЦЕНАРНЫЙ расчёт на допущениях, пока нет своих данных.
Как только из Make приходит статистика (клики, продажи), допущения заменяются фактом.
"""
from .taxonomy import KLAUS_CATEGORIES, PROBLEMS

# Допущения для EPM. Это НЕ измеренные данные — они явно помечаются в выдаче.
EPM_ASSUMPTIONS = {
    "conservative": {"ctr": 0.002, "conversion": 0.03, "approval": 0.80},
    "base": {"ctr": 0.005, "conversion": 0.06, "approval": 0.88},
    "optimistic": {"ctr": 0.010, "conversion": 0.10, "approval": 0.93},
}

WEIGHTS = {
    "commission_value": 0.22, "price_fit": 0.10, "demand": 0.14, "competition": 0.06, "season": 0.08,
    "video_fit": 0.16, "klaus_fit": 0.12, "cookie": 0.04, "data_confidence": 0.08,
}

EXCLUDED_CATEGORIES = ("Waffen", "Pyrotechnik", "Medizinprodukt", "Nahrungsergänzung", "Tabak", "Glücksspiel")


def epm_scenarios(estimated_commission_eur, real=None):
    """real = {"ctr":..., "conversion":..., "approval":...} из фактической статистики, если есть."""
    if not estimated_commission_eur:
        return None
    out = {}
    for name, a in EPM_ASSUMPTIONS.items():
        out[name] = round(1000 * a["ctr"] * a["conversion"] * a["approval"] * estimated_commission_eur, 2)
    out["assumption"] = True
    if real and all(real.get(k) is not None for k in ("ctr", "conversion", "approval")):
        out["measured"] = round(1000 * real["ctr"] * real["conversion"] * real["approval"]
                                * estimated_commission_eur, 2)
        out["assumption"] = False
    return out


def _price_fit(price):
    if price is None:
        return 0.3
    if 15 <= price <= 80:
        return 1.0  # импульсная покупка после короткого ролика
    if 8 <= price < 15 or 80 < price <= 150:
        return 0.7
    if 150 < price <= 300:
        return 0.45
    return 0.2


def _season(category, month):
    months = set()
    for prob in PROBLEMS.values():
        if prob["category"] == category:
            months |= set(prob["season"])
    if not months:
        return 0.7  # круглогодичный товар
    return 1.0 if month in months else 0.35


def _clamp(x, default=0.5):
    if x is None or isinstance(x, bool):
        return default
    return max(0.0, min(1.0, float(x)))


def score(product, signals=None, month=1):
    """signals — оценки агента 0..1: demand, competition, video_fit (+ любые пояснения в notes).

    Возвращает (score 0..1, priority, breakdown). Приоритет:
      A — score ≥ 0.70, ссылка verified, товар в наличии;
      B — score ≥ 0.55, ссылка verified;
      C — остальные verified (эксперимент);
      HOLD — нет подтверждённой ссылки / нет в наличии / исключённая категория: в очередь контента не идёт.
    """
    s = signals or {}
    est = product.get("estimated_commission_eur")
    cookie = product.get("cookie_duration_days")
    parts = {
        "commission_value": min(1.0, (est or 0) / 8.0),
        "price_fit": _price_fit(product.get("price_eur")),
        "demand": _clamp(s.get("demand")),
        "competition": 1 - _clamp(s.get("competition")),
        "season": _season(product.get("category"), month),
        "video_fit": _clamp(s.get("video_fit")),
        "klaus_fit": 1.0 if product.get("category") in KLAUS_CATEGORIES else 0.3,
        "cookie": 0.3 if cookie is None else min(1.0, 0.3 + cookie / 30 * 0.7),
        "data_confidence": {"verified": 1.0, "pending": 0.4}.get(product.get("affiliate_status"), 0.0),
    }
    total = round(sum(WEIGHTS[k] * v for k, v in parts.items()), 3)

    hold_reasons = []
    if product.get("affiliate_status") != "verified":
        hold_reasons.append("нет подтверждённой партнёрской ссылки")
    if product.get("availability") == "out_of_stock":
        hold_reasons.append("нет в наличии")
    cat = (product.get("category") or "") + " " + (product.get("product_name") or "")
    if any(x.lower() in cat.lower() for x in EXCLUDED_CATEGORIES):
        hold_reasons.append("исключённая категория")
    if hold_reasons:
        priority = "HOLD"
    elif total >= 0.70 and product.get("availability") == "in_stock":
        priority = "A"
    elif total >= 0.55:
        priority = "B"
    else:
        priority = "C"
    return total, priority, {"parts": {k: round(v, 3) for k, v in parts.items()}, "hold_reasons": hold_reasons}
