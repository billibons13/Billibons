from ..guard import Action
from ..plans import Feature
from .analytics import AnalyticsAgent
from .base import Agent
from .stock import StockAgent


class AIBusinessAgent(Agent):
    """Combines sales, customers and stock into 'what to look at today'. Recommends, never acts."""
    name = "ai_business"
    feature = Feature.AI_BUSINESS

    def today(self, day_start):
        self._allow(Action.READ)
        report = AnalyticsAgent(self.shop_id, self.store, self.guard).daily_report(day_start)
        low = StockAgent(self.shop_id, self.store, self.guard).low_stock()
        tips = []
        if low:
            tips.append("Пополнить: " + ", ".join(p.name for p in low))
        top_low = [p for p in low if p.id in report["top_products"]]
        if top_low:
            tips.append("Хиты продаж заканчиваются: " + ", ".join(p.name for p in top_low))
        if report["revenue_change_pct"] is not None and report["revenue_change_pct"] < -20:
            tips.append("Выручка упала более чем на 20% — подготовить акцию (нужно ваше одобрение)")
        if not tips:
            tips.append("Всё в норме")
        return {"report": report, "recommendations": tips}
