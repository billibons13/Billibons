"""Guardrails every agent goes through. Forbidden actions become proposals for the owner."""
from dataclasses import dataclass, field
from enum import Enum

from .plan_manager import PlanManager


class Action(str, Enum):
    READ = "read"
    NOTIFY = "notify"              # message the owner
    DRAFT = "draft"                # draft a post, offer, restock list
    SEND_TO_CUSTOMERS = "send_to_customers"
    CHANGE_PRICE = "change_price"
    GRANT_PLAN = "grant_plan"
    DELETE_DATA = "delete_data"


# Never executed by an agent: at most proposed to the owner.
FORBIDDEN = frozenset({Action.CHANGE_PRICE, Action.GRANT_PLAN, Action.DELETE_DATA})


@dataclass
class Proposal:
    agent: str
    action: Action
    summary: str
    payload: dict = field(default_factory=dict)
    needs_owner_approval: bool = True


class GuardError(Exception):
    pass


class Guard:
    def __init__(self, plan_manager: PlanManager):
        self.plans = plan_manager
        self.proposals = []

    def check(self, shop_id, agent, action: Action):
        self.plans.require(shop_id, agent.feature)
        if action in FORBIDDEN:
            raise GuardError(f"{agent.name} may not {action.value}; propose it to the owner instead")

    def propose(self, shop_id, agent, action: Action, summary, payload=None):
        self.plans.require(shop_id, agent.feature)
        p = Proposal(agent.name, action, summary, payload or {})
        self.proposals.append(p)
        return p
