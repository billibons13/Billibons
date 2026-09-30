from collections import Counter

from ..guard import Action
from ..plans import Feature
from .base import Agent


class CustomerAgent(Agent):
    """Customer base, order history, personal offers (as drafts)."""
    name = "customer"
    feature = Feature.CUSTOMERS

    def history(self, customer_id):
        self._allow(Action.READ)
        return [o for o in self.store.orders if o.customer_id == customer_id]

    def favorite_products(self, customer_id, top=3):
        counts = Counter(l.product_id for o in self.history(customer_id) for l in o.lines)
        return [pid for pid, _ in counts.most_common(top)]

    def personal_offer(self, customer_id):
        self._allow(Action.DRAFT)
        favs = [self.store.products[p].name for p in self.favorite_products(customer_id)
                if p in self.store.products and self.store.products[p].stock > 0]
        if not favs:
            return None
        return self._propose(Action.SEND_TO_CUSTOMERS,
                             f"Предложить клиенту {customer_id}: {', '.join(favs)}",
                             {"customer_id": customer_id, "products": favs})
