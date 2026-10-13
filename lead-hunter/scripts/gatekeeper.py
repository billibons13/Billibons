"""Gatekeeper (агент 2) — эталон логики предфильтра до AI. Та же логика собирается в Make (LH-01).
Правила читаются из записи `search` в lh_settings; здесь — значения по умолчанию."""
import re

DEFAULT_SEARCH = {
    "version": 1,
    "include_regex": r"\b(telegram|chat ?bots?|bots?|mini ?apps?|make\.com|integromat|n8n|zapier|webhooks?|automation|automate)\b",
    "exclude_regex": r"translat|garment|instructor|copywrit|chat admin|virtual assistant|data entry|\bseo\b|moodle|vertriebspartner|sales partner|voice (call|assistant)",
    "languages": ["en", "de", "ru", "uk", "es"],
    "budget_fixed_min_eur": 300,
    "budget_hourly_min_eur": 15,
    "max_bids": 200,
}

def gate(p, s=DEFAULT_SEARCH):
    """p: title, description, language, type (fixed|hourly), budget_max_eur, bid_count. → (passed, reason)"""
    text = (p.get("title", "") + " " + p.get("description", "")[:2000]).lower()
    if p.get("language") not in s["languages"]:
        return False, "language:" + str(p.get("language"))
    if re.search(s["exclude_regex"], text):
        return False, "exclude:" + re.search(s["exclude_regex"], text).group(0)
    if not re.search(s["include_regex"], text):
        return False, "no_keyword"
    floor = s["budget_fixed_min_eur"] if p.get("type") == "fixed" else s["budget_hourly_min_eur"]
    if (p.get("budget_max_eur") or 0) < floor:
        return False, "budget<%s" % floor
    if (p.get("bid_count") or 0) > s["max_bids"]:
        return False, "bids>%s" % s["max_bids"]
    return True, "ok"
