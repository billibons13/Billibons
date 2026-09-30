import uuid
from datetime import datetime, timezone

from ..guard import Action
from ..plans import Feature
from ..store import Order, OrderLine
from .base import Agent


class SalesAgent(Agent):
    """Catalog, weight choice, totals, checkout and order handoff."""
    name = "sales"
    feature = Feature.SALES_BOT

    def catalog(self):
        self._allow(Action.READ)
        return [p for p in self.store.products.values() if p.stock > 0]

    def quote(self, lines):
        self._allow(Action.READ)
        total = 0.0
        for line in lines:
            p = self.store.products[line.product_id]
            if line.qty <= 0 or line.qty > p.stock:
                raise ValueError(f"{p.name}: not enough stock")
            total += p.price_eur * line.qty       # price comes from the catalog, never from input
        return round(total, 2)

    def checkout(self, customer_id, lines, city, address, phone, now=None):
        total = self.quote(lines)
        for line in lines:
            self.store.products[line.product_id].stock -= line.qty
        order = Order(str(uuid.uuid4())[:8], self.shop_id, customer_id, list(lines), total,
                      now or datetime.now(timezone.utc), city, address, phone)
        self.store.orders.append(order)
        return order
