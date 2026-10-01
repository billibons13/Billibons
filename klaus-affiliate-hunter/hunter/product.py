"""Нормализация и проверка карточки товара перед отправкой в Make.

Главное правило: в Make никогда не уходит выдуманная или непроверенная партнёрская ссылка.
Если ссылка не подтверждена, поле affiliate_url очищается, а статус становится "unverified".
"""
import hashlib
import re
from datetime import date
from urllib.parse import parse_qs, urlsplit, urlunsplit

SCHEMA_VERSION = "1.0"

AFFILIATE_STATUSES = ("verified", "pending", "unverified", "rejected")
AVAILABILITY = ("in_stock", "out_of_stock", "preorder", "unknown")
NETWORKS = ("amazon_de", "awin", "adcell", "belboon", "tradetracker", "cj", "impact",
            "digistore24", "brand_direct", "other")

# Признаки шаблонных/выдуманных ссылок: такие значения никогда не считаются ссылкой.
_PLACEHOLDER = re.compile(r"example\.|VERIFIED_AFFILIATE_URL|YOUR[_-]?TAG|xxx|\{|\}|<|>|TODO|placeholder",
                          re.IGNORECASE)
_ASIN = re.compile(r"/(?:dp|gp/product)/([A-Z0-9]{10})(?:[/?]|$)")
_AMAZON_TAG = re.compile(r"^[a-z0-9][a-z0-9-]{1,40}-21$")

FIELDS = (
    "schema_version", "product_id", "product_name", "brand", "category", "market", "store",
    "product_url", "affiliate_url", "affiliate_network", "affiliate_status", "price_eur",
    "commission_percent", "commission_fixed_eur", "estimated_commission_eur",
    "cookie_duration_days", "availability", "source_url", "product_description",
    "video_category", "matching_klaus_scenario", "video_hook", "commercial_priority", "score",
    "epm_scenarios", "compliance_flags", "disclosure_text", "discovered_at",
    "verification_date", "content_queue", "notes",
)


def is_url(value):
    if not isinstance(value, str) or _PLACEHOLDER.search(value):
        return False
    parts = urlsplit(value.strip())
    return parts.scheme in ("http", "https") and "." in parts.netloc and " " not in value.strip()


def canonical_url(url):
    """Адрес без параметров отслеживания и якоря: один товар — один адрес."""
    p = urlsplit(url.strip())
    host = p.netloc.lower().removeprefix("www.")
    path = p.path.rstrip("/") or "/"
    return urlunsplit(("https", host, path, "", ""))


def amazon_asin(url):
    if not is_url(url) or "amazon.de" not in urlsplit(url).netloc.lower():
        return None
    m = _ASIN.search(urlsplit(url).path + "/")
    return m.group(1) if m else None


def make_product_id(product_url, network=None):
    asin = amazon_asin(product_url or "")
    if asin:
        return "amzn-de-" + asin
    digest = hashlib.sha1(canonical_url(product_url).encode()).hexdigest()[:16]
    return "de-" + digest


def parse_money(value):
    """49.99 / "49,99 €" / "1.299,00 EUR" → float. Пустое или непонятное → None."""
    if value is None or value == "":
        return None
    if isinstance(value, bool):
        return None
    if isinstance(value, (int, float)):
        return round(float(value), 2) if value >= 0 else None
    s = re.sub(r"[^\d,.\-]", "", str(value))
    if not s or s.startswith("-"):
        return None
    if "," in s and "." in s:
        s = s.replace(".", "").replace(",", ".") if s.rfind(",") > s.rfind(".") else s.replace(",", "")
    elif "," in s:
        s = s.replace(",", ".")
    try:
        return round(float(s), 2)
    except ValueError:
        return None


def parse_percent(value):
    """8 / "8 %" / "8,5%" → 8.0 / 8.5. Значения вне 0–100 отбрасываются."""
    if value is None or value == "" or isinstance(value, bool):
        return None
    n = parse_money(value) if not isinstance(value, (int, float)) else float(value)
    if n is None or n < 0 or n > 100:
        return None
    return round(n, 2)


def amazon_link_ok(affiliate_url, expected_tag):
    """Ссылка Amazon.de считается подтверждённой, только если в ней ваш собственный tag."""
    if not is_url(affiliate_url) or "amazon.de" not in urlsplit(affiliate_url).netloc.lower():
        return False
    tags = parse_qs(urlsplit(affiliate_url).query).get("tag", [])
    return bool(expected_tag) and _AMAZON_TAG.match(expected_tag or "") is not None and tags == [expected_tag]


def normalize(raw, today=None, amazon_tag=None):
    """Возвращает (product, errors, warnings). При errors товар в Make не отправляется."""
    today = today or date.today()
    errors, warnings = [], []
    p = {k: None for k in FIELDS}
    p.update({k: v for k, v in (raw or {}).items() if k in FIELDS})
    p["schema_version"] = SCHEMA_VERSION
    p["market"] = "DE"

    for k in ("product_name", "brand", "category", "store", "product_description", "video_category",
              "matching_klaus_scenario", "video_hook", "notes"):
        if isinstance(p[k], str):
            p[k] = p[k].strip() or None
        elif p[k] is not None:
            p[k] = str(p[k])

    if not p["product_name"]:
        errors.append("product_name: пусто")
    if not is_url(p["product_url"]):
        errors.append("product_url: нет корректного адреса товара")
    elif not urlsplit(p["product_url"]).netloc.lower().endswith(".de") and p["store"] is None:
        warnings.append("product_url: домен не .de — подтвердите доставку в Германию и укажите store")

    if p["source_url"] is not None and not is_url(p["source_url"]):
        warnings.append("source_url: некорректный адрес, очищен")
        p["source_url"] = None

    if not p["product_id"] and is_url(p["product_url"]):
        p["product_id"] = make_product_id(p["product_url"])
    elif p["product_id"]:
        p["product_id"] = re.sub(r"[^A-Za-z0-9_.-]", "-", str(p["product_id"]))[:64]

    p["price_eur"] = parse_money(p["price_eur"])
    if p["price_eur"] is None:
        warnings.append("price_eur: цена не подтверждена")
    p["commission_percent"] = parse_percent(p["commission_percent"])
    p["commission_fixed_eur"] = parse_money(p["commission_fixed_eur"])
    if p["commission_percent"] is not None and p["price_eur"] is not None:
        p["estimated_commission_eur"] = round(p["price_eur"] * p["commission_percent"] / 100, 2)
    elif p["commission_fixed_eur"] is not None:
        p["estimated_commission_eur"] = p["commission_fixed_eur"]
    else:
        p["estimated_commission_eur"] = None
        warnings.append("commission: комиссия не подтверждена")

    c = p["cookie_duration_days"]
    p["cookie_duration_days"] = c if isinstance(c, (int, float)) and not isinstance(c, bool) and c >= 0 else None

    if p["availability"] not in AVAILABILITY:
        p["availability"] = "unknown"
    if p["affiliate_network"] not in NETWORKS:
        if p["affiliate_network"] is not None:
            warnings.append(f"affiliate_network: неизвестная сеть {p['affiliate_network']!r} → other")
        p["affiliate_network"] = "other" if p["affiliate_network"] else None

    # --- партнёрская ссылка: строгие правила ---
    status = p["affiliate_status"] if p["affiliate_status"] in AFFILIATE_STATUSES else "unverified"
    link = p["affiliate_url"]
    if status == "verified":
        reason = None
        if not is_url(link):
            reason = "affiliate_url отсутствует или похожа на шаблон"
        elif not p["affiliate_network"]:
            reason = "не указана партнёрская сеть"
        elif p["affiliate_network"] == "amazon_de" and not amazon_link_ok(link, amazon_tag):
            reason = "ссылка Amazon.de без вашего tag (…-21)"
        elif not p["verification_date"]:
            reason = "нет даты проверки"
        if reason:
            warnings.append(f"affiliate_status: verified → unverified ({reason})")
            status = "unverified"
    p["affiliate_status"] = status
    if status != "verified":
        p["affiliate_url"] = None  # никогда не отправляем непроверенную ссылку

    if p["verification_date"] is not None and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", str(p["verification_date"])):
        warnings.append("verification_date: не в формате YYYY-MM-DD, очищена")
        p["verification_date"] = None
    p["discovered_at"] = p["discovered_at"] or today.isoformat()
    return p, errors, warnings
