"""Plans and feature flags. The single source of truth for what each plan unlocks."""
from enum import Enum


class Feature(str, Enum):
    SALES_BOT = "sales_bot"                # catalog, photos, weight, total, checkout, order handoff
    STOCK_BASIC = "stock_basic"            # stock levels, low-stock warnings, restock lists
    CUSTOMERS = "customers"                # customer base, order history, personal offers
    MARKETING = "marketing"                # posts, promos, reminders (never prices)
    ANALYTICS = "analytics"                # daily reports, sales dynamics
    BROADCASTS = "broadcasts"
    PROMO_CODES = "promo_codes"
    BONUSES = "bonuses"
    AI_BUSINESS = "ai_business"            # cross-domain analysis and daily recommendations
    MAKE_AUTOMATION = "make_automation"
    API_INTEGRATIONS = "api_integrations"
    EXTERNAL_SERVICES = "external_services"


START_350 = "start_350"
BUSINESS_800 = "business_800"
PRO_1500 = "pro_1500"

_START = frozenset({Feature.SALES_BOT, Feature.STOCK_BASIC})
_BUSINESS = _START | {
    Feature.CUSTOMERS, Feature.MARKETING, Feature.ANALYTICS,
    Feature.BROADCASTS, Feature.PROMO_CODES, Feature.BONUSES,
}
_PRO = _BUSINESS | {
    Feature.AI_BUSINESS, Feature.MAKE_AUTOMATION,
    Feature.API_INTEGRATIONS, Feature.EXTERNAL_SERVICES,
}

PLANS = {
    START_350: {"price_eur": 350, "features": _START},
    BUSINESS_800: {"price_eur": 800, "features": frozenset(_BUSINESS)},
    PRO_1500: {"price_eur": 1500, "features": frozenset(_PRO)},
}
