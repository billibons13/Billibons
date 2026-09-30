from ..guard import Action
from ..plans import Feature
from .base import Agent


class StockAgent(Agent):
    """Tracks stock, warns about shortages, drafts restock lists."""
    name = "stock"
    feature = Feature.STOCK_BASIC

    def low_stock(self):
        self._allow(Action.READ)
        return [p for p in self.store.products.values() if p.stock <= p.min_stock]

    def restock_list(self, target_multiplier=2):
        self._allow(Action.DRAFT)
        return [{"product_id": p.id, "name": p.name,
                 "order_qty": round(max(p.min_stock * target_multiplier - p.stock, 0), 2),
                 "unit": p.unit}
                for p in self.low_stock()]
