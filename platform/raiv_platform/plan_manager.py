"""Resolves which features a shop may use. Features exist only for a confirmed payment."""
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Optional

from .plans import PLANS, Feature

PAID = "paid"


@dataclass(frozen=True)
class Subscription:
    shop_id: str
    plan_id: str
    payment_status: str            # only "paid" unlocks anything
    paid_amount_eur: float
    valid_until: Optional[datetime] = None   # None = one-off purchase without expiry


class PlanError(Exception):
    pass


class PlanManager:
    def __init__(self, subscriptions):
        self._subs = {s.shop_id: s for s in subscriptions}

    def features(self, shop_id, now=None):
        sub = self._subs.get(shop_id)
        if sub is None or sub.plan_id not in PLANS:
            return frozenset()
        plan = PLANS[sub.plan_id]
        if sub.payment_status != PAID:
            return frozenset()
        if sub.paid_amount_eur < plan["price_eur"]:
            return frozenset()      # underpayment never unlocks a plan
        now = now or datetime.now(timezone.utc)
        if sub.valid_until is not None and now > sub.valid_until:
            return frozenset()
        return plan["features"]

    def has(self, shop_id, feature: Feature, now=None):
        return feature in self.features(shop_id, now)

    def require(self, shop_id, feature: Feature, now=None):
        if not self.has(shop_id, feature, now):
            raise PlanError(f"{feature.value} is not available for shop {shop_id}")

    def change_plan(self, *_args, **_kwargs):
        """Plans change only through a verified payment record, never through an agent."""
        raise PlanError("plan changes must come from a confirmed payment, not from code or agents")
