from ..guard import Action, Guard
from ..plans import Feature


class Agent:
    name = "agent"
    feature: Feature = None

    def __init__(self, shop_id, store, guard: Guard):
        self.shop_id, self.store, self.guard = shop_id, store, guard

    def _allow(self, action: Action):
        self.guard.check(self.shop_id, self, action)

    def _propose(self, action: Action, summary, payload=None):
        return self.guard.propose(self.shop_id, self, action, summary, payload)
