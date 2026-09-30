from collections import Counter
from datetime import timedelta

from ..guard import Action
from ..plans import Feature
from .base import Agent


class AnalyticsAgent(Agent):
    """Daily report and sales dynamics."""
    name = "analytics"
    feature = Feature.ANALYTICS

    def _orders_between(self, start, end):
        return [o for o in self.store.orders if start <= o.created_at < end]

    def daily_report(self, day_start):
        self._allow(Action.READ)
        today = self._orders_between(day_start, day_start + timedelta(days=1))
        prev = self._orders_between(day_start - timedelta(days=1), day_start)
        revenue = round(sum(o.total_eur for o in today), 2)
        prev_revenue = round(sum(o.total_eur for o in prev), 2)
        top = Counter()
        for o in today:
            for l in o.lines:
                top[l.product_id] += l.qty
        return {
            "orders": len(today),
            "revenue_eur": revenue,
            "avg_check_eur": round(revenue / len(today), 2) if today else 0,
            "revenue_change_pct": round((revenue - prev_revenue) / prev_revenue * 100, 1) if prev_revenue else None,
            "top_products": [pid for pid, _ in top.most_common(3)],
        }
