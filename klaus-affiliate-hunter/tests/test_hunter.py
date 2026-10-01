import unittest
from datetime import date

from hunter.links import build
from hunter.learning import category_stats, real_rates
from hunter.matching import match_script, match_week, split_scripts
from hunter.pipeline import prepare
from hunter.product import make_product_id, normalize, parse_money, parse_percent
from hunter.scoring import epm_scenarios, score

TODAY = date(2026, 10, 1)
TAG = "klaus-21"

BASE = {
    "product_name": "Luftentfeuchter 12 l", "brand": "Muster", "category": "Lüften & Entfeuchten",
    "store": "Amazon.de", "product_url": "https://www.amazon.de/dp/B0TESTTEST?ref=x",
    "affiliate_network": "amazon_de", "affiliate_status": "verified",
    "affiliate_url": "https://www.amazon.de/dp/B0TESTTEST?tag=klaus-21",
    "price_eur": "49,99 €", "commission_percent": "7 %", "cookie_duration_days": 1,
    "availability": "in_stock", "verification_date": "2026-10-01",
}
GOOD = {"demand": 0.8, "competition": 0.4, "video_fit": 0.9}


class ParseTest(unittest.TestCase):
    def test_money(self):
        for raw, want in [("49,99 €", 49.99), ("1.299,00 EUR", 1299.0), ("1,299.50", 1299.5), (12, 12.0),
                          ("", None), (None, None), ("abc", None), (-5, None), (True, None)]:
            self.assertEqual(parse_money(raw), want, raw)

    def test_percent(self):
        for raw, want in [("8 %", 8.0), ("8,5%", 8.5), (7, 7.0), (150, None), ("-1", None), (None, None)]:
            self.assertEqual(parse_percent(raw), want, raw)

    def test_ids_are_stable_and_dedup_friendly(self):
        self.assertEqual(make_product_id("https://www.amazon.de/Some-Name/dp/B0TESTTEST/ref=sr_1"),
                         "amzn-de-B0TESTTEST")
        a = make_product_id("https://www.obi.de/p/123/x?utm_source=a#top")
        b = make_product_id("https://obi.de/p/123/x/")
        self.assertEqual(a, b)


class AffiliateLinkTest(unittest.TestCase):
    def test_verified_amazon_link_kept(self):
        p, err, _ = normalize(BASE, TODAY, amazon_tag=TAG)
        self.assertEqual(err, [])
        self.assertEqual(p["affiliate_status"], "verified")
        self.assertEqual(p["estimated_commission_eur"], 3.5)

    def test_placeholder_or_foreign_tag_never_sent(self):
        for url in ["VERIFIED_AFFILIATE_URL", "https://example.de/product", "https://www.amazon.de/dp/B0TESTTEST",
                    "https://www.amazon.de/dp/B0TESTTEST?tag=someoneelse-21", ""]:
            p, _, warn = normalize({**BASE, "affiliate_url": url}, TODAY, amazon_tag=TAG)
            self.assertEqual(p["affiliate_status"], "unverified", url)
            self.assertIsNone(p["affiliate_url"], url)
            self.assertTrue(any("verified → unverified" in w for w in warn), url)

    def test_no_tag_configured_means_unverified(self):
        p, _, _ = normalize(BASE, TODAY, amazon_tag=None)
        self.assertEqual(p["affiliate_status"], "unverified")

    def test_unverified_status_drops_url(self):
        p, _, _ = normalize({**BASE, "affiliate_status": "pending"}, TODAY, amazon_tag=TAG)
        self.assertIsNone(p["affiliate_url"])

    def test_missing_verification_date(self):
        p, _, _ = normalize({**BASE, "verification_date": None}, TODAY, amazon_tag=TAG)
        self.assertEqual(p["affiliate_status"], "unverified")

    def test_awin_link_needs_network_and_date(self):
        raw = {**BASE, "affiliate_network": "awin", "product_url": "https://www.obi.de/p/1",
               "affiliate_url": "https://www.awin1.com/cread.php?awinmid=1&awinaffid=2&ued=x"}
        p, _, _ = normalize(raw, TODAY)
        self.assertEqual(p["affiliate_status"], "verified")


class ValidationTest(unittest.TestCase):
    def test_required_fields(self):
        p, err, _ = normalize({"product_url": "nonsense"}, TODAY)
        self.assertEqual(len(err), 2)

    def test_missing_values_are_null_not_invented(self):
        p, err, warn = normalize({"product_name": "X", "product_url": "https://shop.de/x"}, TODAY)
        self.assertEqual(err, [])
        self.assertIsNone(p["price_eur"])
        self.assertIsNone(p["estimated_commission_eur"])
        self.assertEqual(p["availability"], "unknown")
        self.assertEqual(p["market"], "DE")


class ScoringTest(unittest.TestCase):
    def test_priority_a(self):
        payload, rep = prepare(BASE, GOOD, today=TODAY, amazon_tag=TAG)
        self.assertEqual(payload["commercial_priority"], "A", rep)
        self.assertTrue(payload["content_queue"])
        self.assertIn("Als Amazon-Partner", payload["disclosure_text"])

    def test_unverified_is_hold_and_never_queued(self):
        payload, _ = prepare({**BASE, "affiliate_status": "unverified"}, GOOD, today=TODAY, amazon_tag=TAG)
        self.assertEqual(payload["commercial_priority"], "HOLD")
        self.assertFalse(payload["content_queue"])

    def test_out_of_stock_is_hold(self):
        p, _, _ = normalize({**BASE, "availability": "out_of_stock"}, TODAY, amazon_tag=TAG)
        self.assertEqual(score(p, GOOD, 10)[1], "HOLD")

    def test_weak_signals_lower_priority(self):
        payload, _ = prepare(BASE, {"demand": 0.1, "competition": 0.95, "video_fit": 0.2}, today=TODAY,
                             amazon_tag=TAG)
        self.assertIn(payload["commercial_priority"], ("B", "C"))

    def test_epm_is_marked_as_assumption(self):
        e = epm_scenarios(3.5)
        self.assertTrue(e["assumption"])
        self.assertLess(e["conservative"], e["base"])
        self.assertIsNone(epm_scenarios(None))
        m = epm_scenarios(3.5, {"ctr": 0.01, "conversion": 0.05, "approval": 1})
        self.assertEqual(m["measured"], 1.75)
        self.assertFalse(m["assumption"])

    def test_biocide_disclosure(self):
        payload, _ = prepare({**BASE, "category": "Schimmel & Feuchtigkeit"}, GOOD, today=TODAY, amazon_tag=TAG)
        self.assertIn("biocide", payload["compliance_flags"])
        self.assertIn("Biozidprodukte vorsichtig verwenden", payload["disclosure_text"])

    def test_invalid_product_rejected(self):
        payload, rep = prepare({"product_name": ""}, today=TODAY)
        self.assertIsNone(payload)
        self.assertTrue(rep["errors"])


WEEK = """Montag – Schimmel in der Dusche
Hook (0–3 s): Na, Problem? Klaus ist da! Schwarze Fugen in der Dusche?
Szene 2: Schimmel entsteht durch Feuchtigkeit und schlechtes Lüften.
Schluss: Das kriegen wir hin!
Produkt: Hygrometer
---
Mittwoch – Richtig stoßlüften
Hook (0–3 s): Beschlagene Fenster am Morgen?
Szene 2: Dreimal täglich stoßlüften.
Produkt: «nur Tipp»
---
Freitag – Abfluss verstopft
Hook (0–3 s): Das Wasser läuft nicht ab?
Szene 2: Haare im Abfluss, Siphon reinigen.
Produkt: Rohrreinigungsspirale
"""


class MatchingTest(unittest.TestCase):
    def test_split(self):
        s = split_scripts(WEEK)
        self.assertEqual(len(s), 3)
        self.assertEqual(s[0]["product_hint"], "Hygrometer")
        self.assertTrue(s[1]["tip_only"])

    def test_mold_scenario(self):
        r = match_script(split_scripts(WEEK)[0])
        types = [p["product_type"] for p in r["products"]]
        self.assertEqual(types[0], "Hygrometer")  # то, что назвал сценарий, — первым
        self.assertIn("Schimmelentferner", types)
        self.assertIn("schimmel_bad", r["problems"])
        self.assertTrue(any("Biozid" in c for p in r["products"] for c in p["compliance"]))

    def test_tip_only_gets_no_products(self):
        self.assertEqual(match_week(WEEK)[1]["products"], [])

    def test_drain(self):
        r = match_week(WEEK)[2]
        self.assertEqual(r["products"][0]["product_type"], "Rohrreinigungsspirale")
        self.assertNotIn("Luftentfeuchter", [p["product_type"] for p in r["products"]])

    def test_unrelated_text_gets_nothing(self):
        self.assertEqual(match_script("Heute erzähle ich einen Witz über Katzen.")["products"], [])


class LinksTest(unittest.TestCase):
    CFG = {"amazon_partner_tag": "klaus-21", "awin_publisher_id": "555",
           "awin_programmes": [{"domain": "obi.de", "advertiser_id": "9326", "status": "joined",
                                "deeplink_enabled": True, "cookie_days": 30},
                               {"domain": "toom.de", "advertiser_id": "16017", "status": "pending",
                                "deeplink_enabled": True}]}

    def test_amazon(self):
        self.assertEqual(build("https://www.amazon.de/Foo/dp/B0TESTTEST/ref=x", self.CFG)[:3],
                         ("https://www.amazon.de/dp/B0TESTTEST?tag=klaus-21", "amazon_de", "verified"))
        self.assertEqual(build("https://www.amazon.de/dp/B0TESTTEST", {})[2], "unverified")

    def test_awin_joined_only(self):
        url, net, st, cookie = build("https://www.obi.de/p/123", self.CFG)
        self.assertTrue(url.startswith("https://www.awin1.com/cread.php?awinmid=9326&awinaffid=555&ued=https%3A"))
        self.assertEqual((net, st, cookie), ("awin", "verified", 30))
        self.assertEqual(build("https://www.toom.de/p/1", self.CFG)[:3], (None, "awin", "pending"))
        self.assertEqual(build("https://www.hornbach.de/p/1", self.CFG)[:3], (None, None, "unverified"))


class LearningTest(unittest.TestCase):
    def test_stats_and_threshold(self):
        recs = [{"key": "a", "data": {"category": "Lüften & Entfeuchten", "video_status": "published", "views": 5000,
                                      "clicks": 40, "sales": 4, "refunds": 1, "confirmed_commission_eur": 9}},
                {"key": "s", "data": {"category": "_klaus_scripts", "notes": "..."}},
                {"key": "b", "data": {"category": "Küche & Haushalt", "views": 100, "clicks": 1}}]
        st = category_stats(recs)
        self.assertNotIn("_klaus_scripts", st)
        lu = st["Lüften & Entfeuchten"]
        self.assertTrue(lu["enough_data"])
        self.assertEqual((lu["ctr"], lu["conversion"], lu["approval"], lu["epm_measured_eur"]), (0.008, 0.1, 0.75, 1.8))
        self.assertIsNotNone(real_rates(st, "Lüften & Entfeuchten"))
        self.assertIsNone(real_rates(st, "Küche & Haushalt"))  # мало данных → остаются допущения


if __name__ == "__main__":
    unittest.main()
