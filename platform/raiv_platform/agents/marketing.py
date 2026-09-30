from ..guard import Action
from ..plans import Feature
from .base import Agent


class MarketingAgent(Agent):
    """Posts, promos, reminders. Prices only via an owner-approved proposal."""
    name = "marketing"
    feature = Feature.MARKETING

    def draft_post(self):
        self._allow(Action.DRAFT)
        items = [p for p in self.store.products.values() if p.stock > 0][:5]
        lines = "\n".join(f"• {p.name} — {p.price_eur:g} € / {p.unit}" for p in items)
        return f"🐟 Сегодня в наличии:\n{lines}\n\nЗаказ — в нашем боте 👇"

    def suggest_discount(self, product_id, percent, reason):
        # Never applied directly: goes to the owner as a proposal.
        return self._propose(Action.CHANGE_PRICE,
                             f"Скидка {percent}% на {self.store.products[product_id].name}: {reason}",
                             {"product_id": product_id, "percent": percent})
