"""Полная подготовка товара: нормализация → оценка → требования к рекламе → JSON для Make."""
from datetime import date

from .product import normalize
from .scoring import epm_scenarios, score
from .taxonomy import COMPLIANCE_NOTES, PROBLEMS

DISCLOSURE = ("Werbung | *Affiliate-Link: Kaufst du über den Link, erhalte ich eine Provision. "
              "Der Preis ändert sich für dich nicht.")
AMAZON_DISCLOSURE = "Als Amazon-Partner verdiene ich an qualifizierten Verkäufen."


def compliance_flags(category):
    flags = []
    for prob in PROBLEMS.values():
        if prob["category"] == category:
            flags += [c for c in prob["compliance"] if c not in flags]
    return flags


def prepare(raw, signals=None, today=None, amazon_tag=None, real_rates=None):
    """→ (payload | None, report). payload = None, если есть критические ошибки."""
    today = today or date.today()
    p, errors, warnings = normalize(raw, today=today, amazon_tag=amazon_tag)
    report = {"product_id": p.get("product_id"), "errors": errors, "warnings": warnings}
    if errors:
        return None, report
    total, priority, breakdown = score(p, signals, month=today.month)
    p["score"] = total
    p["commercial_priority"] = priority
    p["epm_scenarios"] = epm_scenarios(p["estimated_commission_eur"], real_rates)
    p["compliance_flags"] = compliance_flags(p["category"])
    disclosure = DISCLOSURE + (" " + AMAZON_DISCLOSURE if p["affiliate_network"] == "amazon_de" else "")
    extra = [COMPLIANCE_NOTES[f] for f in p["compliance_flags"] if f == "biocide"]
    p["disclosure_text"] = disclosure if not extra else disclosure + " | " + extra[0]
    # В очередь контента Klaus — только A/B с подтверждённой ссылкой. C — эксперимент по решению владельца.
    p["content_queue"] = priority in ("A", "B")
    report.update({"score": total, "priority": priority, **breakdown})
    return p, report
