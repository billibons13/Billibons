import unittest
from datetime import datetime, timedelta, timezone

from raiv_platform.agents import (AIBusinessAgent, AnalyticsAgent, CustomerAgent,
                                  MarketingAgent, SalesAgent, StockAgent)
from raiv_platform.guard import Action, Guard, GuardError
from raiv_platform.plan_manager import PlanError, PlanManager, Subscription
from raiv_platform.plans import BUSINESS_800, PRO_1500, START_350, Feature
from raiv_platform.store import Customer, OrderLine, Product, Store

NOW = datetime(2026, 10, 1, 12, tzinfo=timezone.utc)
DAY = datetime(2026, 10, 1, tzinfo=timezone.utc)


def make_store():
    s = Store()
    s.products = {
        "ikra": Product("ikra", "Икра кеты", 8.5, "100g", stock=20, min_stock=5),
        "lesch": Product("lesch", "Лещ с икрой", 35, "kg", stock=3, min_stock=4),
    }
    s.customers = {"c1": Customer("c1", "Анна")}
    return s


def setup(plan, status="paid", amount=None, valid_until=None):
    amount = {START_350: 350, BUSINESS_800: 800, PRO_1500: 1500}[plan] if amount is None else amount
    pm = PlanManager([Subscription("shop", plan, status, amount, valid_until)])
    return pm, Guard(pm), make_store()


class PlanManagerTest(unittest.TestCase):
    def test_tiers(self):
        for plan, has, lacks in [
            (START_350, {Feature.SALES_BOT, Feature.STOCK_BASIC}, {Feature.CUSTOMERS, Feature.AI_BUSINESS}),
            (BUSINESS_800, {Feature.CUSTOMERS, Feature.MARKETING, Feature.ANALYTICS, Feature.PROMO_CODES,
                            Feature.BROADCASTS, Feature.BONUSES}, {Feature.AI_BUSINESS, Feature.MAKE_AUTOMATION}),
            (PRO_1500, {Feature.AI_BUSINESS, Feature.MAKE_AUTOMATION, Feature.API_INTEGRATIONS}, set()),
        ]:
            pm, _, _ = setup(plan)
            f = pm.features("shop", NOW)
            self.assertTrue(has <= f, plan)
            self.assertFalse(lacks & f, plan)

    def test_unpaid_pending_refunded_unlock_nothing(self):
        for status in ["pending", "failed", "refunded", "PAID ", ""]:
            pm, _, _ = setup(PRO_1500, status=status)
            self.assertEqual(pm.features("shop", NOW), frozenset(), status)

    def test_underpayment_unlocks_nothing(self):
        pm, _, _ = setup(PRO_1500, amount=800)
        self.assertEqual(pm.features("shop", NOW), frozenset())

    def test_expired_subscription(self):
        pm, _, _ = setup(BUSINESS_800, valid_until=NOW - timedelta(days=1))
        self.assertEqual(pm.features("shop", NOW), frozenset())

    def test_unknown_shop_and_plan(self):
        pm = PlanManager([Subscription("shop", "vip_free", "paid", 0)])
        self.assertEqual(pm.features("shop", NOW), frozenset())
        self.assertEqual(pm.features("other", NOW), frozenset())

    def test_plan_cannot_be_changed_in_code(self):
        pm, _, _ = setup(START_350)
        with self.assertRaises(PlanError):
            pm.change_plan("shop", PRO_1500)


class GuardTest(unittest.TestCase):
    def test_agent_blocked_outside_plan(self):
        pm, g, s = setup(START_350)
        with self.assertRaises(PlanError):
            CustomerAgent("shop", s, g).history("c1")
        with self.assertRaises(PlanError):
            AIBusinessAgent("shop", s, g).today(DAY)

    def test_forbidden_actions(self):
        pm, g, s = setup(PRO_1500)
        agent = MarketingAgent("shop", s, g)
        for a in [Action.CHANGE_PRICE, Action.GRANT_PLAN, Action.DELETE_DATA]:
            with self.assertRaises(GuardError):
                g.check("shop", agent, a)

    def test_discount_is_only_a_proposal(self):
        pm, g, s = setup(BUSINESS_800)
        p = MarketingAgent("shop", s, g).suggest_discount("lesch", 10, "медленно продаётся")
        self.assertTrue(p.needs_owner_approval)
        self.assertEqual(s.products["lesch"].price_eur, 35)


class AgentsTest(unittest.TestCase):
    def test_sales_checkout(self):
        pm, g, s = setup(START_350)
        sales = SalesAgent("shop", s, g)
        o = sales.checkout("c1", [OrderLine("ikra", 3), OrderLine("lesch", 1.5)], "Эдделак", "Str 1", "+49", NOW)
        self.assertEqual(o.total_eur, 78.0)
        self.assertEqual(s.products["ikra"].stock, 17)
        with self.assertRaises(ValueError):
            sales.quote([OrderLine("lesch", 10)])

    def test_stock(self):
        pm, g, s = setup(START_350)
        st = StockAgent("shop", s, g)
        self.assertEqual([p.id for p in st.low_stock()], ["lesch"])
        self.assertEqual(st.restock_list()[0]["order_qty"], 5)

    def test_analytics_and_ai(self):
        pm, g, s = setup(PRO_1500)
        sales = SalesAgent("shop", s, g)
        sales.checkout("c1", [OrderLine("lesch", 1)], "Марне", "a", "p", DAY - timedelta(hours=5))
        sales.checkout("c1", [OrderLine("ikra", 2)], "Марне", "a", "p", DAY + timedelta(hours=3))
        r = AnalyticsAgent("shop", s, g).daily_report(DAY)
        self.assertEqual((r["orders"], r["revenue_eur"]), (1, 17.0))
        self.assertLess(r["revenue_change_pct"], -20)
        tips = AIBusinessAgent("shop", s, g).today(DAY)["recommendations"]
        self.assertTrue(any("Пополнить" in t for t in tips))
        self.assertTrue(any("акцию" in t for t in tips))

    def test_customer_offer(self):
        pm, g, s = setup(BUSINESS_800)
        SalesAgent("shop", s, g).checkout("c1", [OrderLine("ikra", 1)], "x", "a", "p", NOW)
        p = CustomerAgent("shop", s, g).personal_offer("c1")
        self.assertIn("Икра кеты", p.summary)


if __name__ == "__main__":
    unittest.main()
