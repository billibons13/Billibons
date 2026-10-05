"""Эталонная реализация скоринга Lead Hunter (этап 2).
Make (LH-10) считает то же самое формулами; этот файл — проверяемая спецификация + тесты.
Запуск тестов: python3 scripts/scoring.py
"""
import json, re

DEFAULT_SETTINGS = {
    "hot_threshold": 80, "warm_threshold": 60, "cold_threshold": 40, "minimum_order_eur": 500,
    "weights": {"telegram_relevance": .15, "budget": .15, "project_clarity": .12, "client_credibility": .12,
                "commercial_potential": .12, "fit": .10, "urgency": .08, "competition": .06,
                "source_quality": .05, "complexity_fit": .05},
    "fx_to_eur": {"EUR": 1.0},  # реальные курсы владелец задаёт в lh_settings (fx_usd, fx_gbp, ...) с датой
}
KEYS = list(DEFAULT_SETTINGS["weights"])
RISK_CAP, NO_URL_CAP, LOW_BUDGET_CAP, PROSPECT_CAP = 39, 59, 59, 59
SCORE_RE = re.compile(r"^(10(\.0+)?|[0-9](\.\d+)?)$")


def strip_fences(text):
    return re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text.strip())


def validate(raw_text, lead_id):
    """Возвращает (analysis, error_code). Проверки = те же, что фильтр «JSON valid» в LH-10."""
    try:
        a = json.loads(strip_fences(raw_text))
    except Exception:
        return None, "JSON_PARSE"
    if not isinstance(a, dict) or a.get("lead_id") != lead_id:
        return None, "LEAD_ID_MISMATCH"
    s = a.get("scores")
    if not isinstance(s, dict) or any(k not in s for k in KEYS):
        return None, "SCORES_MISSING"
    if any(not SCORE_RE.match(str(s[k])) for k in KEYS):
        return None, "SCORE_OUT_OF_RANGE"
    if not isinstance(a.get("risk_flags"), list):
        return None, "RISK_FLAGS_TYPE"
    if a.get("kind") not in ("lead", "prospect"):
        return None, "KIND_INVALID"
    return a, None


def score(analysis, source_url, settings=DEFAULT_SETTINGS):
    w = settings["weights"]
    assert abs(sum(w.values()) - 1) < 1e-9, "weights must sum to 1"
    raw = round(10 * sum(w[k] * float(analysis["scores"][k]) for k in KEYS))
    caps, reasons = [100], []
    if not source_url:
        caps.append(NO_URL_CAP); reasons.append("нет source_url — не выше COLD (59)")
    if analysis["risk_flags"]:
        caps.append(RISK_CAP); reasons.append("risk_flags: " + ", ".join(analysis["risk_flags"]) + " — не выше 39")
    b = analysis.get("budget")
    budget_eur = None
    if b and b.get("amount") is not None:
        rate = settings["fx_to_eur"].get(str(b.get("currency", "")).upper())
        if rate:
            budget_eur = round(float(b["amount"]) * rate, 2)
            if budget_eur < settings["minimum_order_eur"]:
                caps.append(LOW_BUDGET_CAP)
                reasons.append(f"бюджет ≈ {budget_eur} € < {settings['minimum_order_eur']} € — не выше 59")
    if analysis.get("kind") == "prospect":
        caps.append(PROSPECT_CAP); reasons.append("prospect (не опубликованный заказ) — не выше 59")
    final = min([raw] + caps)
    g = ("HOT" if final >= settings["hot_threshold"] else "WARM" if final >= settings["warm_threshold"]
         else "COLD" if final >= settings["cold_threshold"] else "REJECT")
    return {"score_raw": raw, "score": final, "grade": g, "score_cap_reason": "; ".join(reasons) or None,
            "budget_eur": budget_eur}


# ---------- тесты (TEST DATA, вымышленные значения) ----------
def _a(**kw):
    base = {"lead_id": "LH-20261005-aaaaaa", "kind": "lead", "budget": None, "risk_flags": [],
            "scores": {k: 8 for k in KEYS}}
    base.update(kw); return base

if __name__ == "__main__":
    s = DEFAULT_SETTINGS
    assert score(_a(), "https://x")["grade"] == "HOT" and score(_a(), "https://x")["score"] == 80
    assert score(_a(), None)["score"] == 59 and score(_a(), None)["grade"] == "COLD"          # нет URL
    assert score(_a(risk_flags=["crypto_scheme"]), "https://x")["grade"] == "REJECT"           # риск
    low = dict(s, fx_to_eur={"EUR": 1.0})
    assert score(_a(budget={"amount": 300, "currency": "EUR"}), "https://x", low)["score"] == 59  # < 500 €
    assert score(_a(kind="prospect"), "https://x")["score"] == 59                               # prospect
    assert score(_a(scores={k: 10 for k in KEYS}), "https://x")["score"] == 100
    assert score(_a(scores={k: 0 for k in KEYS}), "https://x")["grade"] == "REJECT"
    ok = json.dumps(_a())
    assert validate(ok, "LH-20261005-aaaaaa")[1] is None
    assert validate("```json\n" + ok + "\n```", "LH-20261005-aaaaaa")[1] is None
    assert validate("not json", "LH-20261005-aaaaaa")[1] == "JSON_PARSE"
    assert validate(ok, "LH-other")[1] == "LEAD_ID_MISMATCH"
    bad = _a(); bad["scores"]["fit"] = 11
    assert validate(json.dumps(bad), "LH-20261005-aaaaaa")[1] == "SCORE_OUT_OF_RANGE"
    bad = _a(); del bad["scores"]["urgency"]
    assert validate(json.dumps(bad), "LH-20261005-aaaaaa")[1] == "SCORES_MISSING"
    print("scoring: all tests passed")
