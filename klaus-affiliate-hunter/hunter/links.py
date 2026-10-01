"""Построение партнёрских ссылок только по официальным форматам сетей и только для ваших аккаунтов.

Amazon.de: https://www.amazon.de/dp/<ASIN>?tag=<ваш tag>-21 — стандартная ссылка PartnerNet.
Awin:      https://www.awin1.com/cread.php?awinmid=<advertiser>&awinaffid=<publisher>&ued=<URL> —
           стандартный deeplink Awin; допустим только для программ со статусом joined и deeplink_enabled.
Если данных аккаунта нет — ссылка не строится (None), товар остаётся pending/unverified.
"""
from urllib.parse import quote, urlsplit

from .product import _AMAZON_TAG, amazon_asin


def amazon_link(product_url, tag):
    asin = amazon_asin(product_url)
    if not asin or not tag or not _AMAZON_TAG.match(tag):
        return None
    return f"https://www.amazon.de/dp/{asin}?tag={tag}"


def awin_link(product_url, config):
    """config: {"awin_publisher_id": "123", "awin_programmes": [{"domain": "obi.de", "advertiser_id": "9326",
    "status": "joined", "deeplink_enabled": true}, ...]} — статусы берутся из кабинета/API Awin, не угадываются."""
    pub = str(config.get("awin_publisher_id") or "")
    if not pub.isdigit():
        return None, None
    host = urlsplit(product_url).netloc.lower().removeprefix("www.")
    for prog in config.get("awin_programmes") or []:
        dom = (prog.get("domain") or "").lower().removeprefix("www.")
        if dom and (host == dom or host.endswith("." + dom)):
            if prog.get("status") != "joined" or not prog.get("deeplink_enabled") \
                    or not str(prog.get("advertiser_id") or "").isdigit():
                return None, prog
            return (f"https://www.awin1.com/cread.php?awinmid={prog['advertiser_id']}&awinaffid={pub}"
                    f"&ued={quote(product_url, safe='')}"), prog
    return None, None


def build(product_url, config):
    """→ (affiliate_url | None, network | None, status, cookie_days | None)."""
    if "amazon.de" in urlsplit(product_url).netloc.lower():
        link = amazon_link(product_url, config.get("amazon_partner_tag"))
        return (link, "amazon_de", "verified" if link else "unverified", 1)
    link, prog = awin_link(product_url, config)
    if link:
        return link, "awin", "verified", prog.get("cookie_days")
    if prog:
        return None, "awin", "pending", prog.get("cookie_days")
    return None, None, "unverified", None
