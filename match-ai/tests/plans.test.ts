import { describe, expect, it } from "vitest";
import { DEFAULT_PRICE_PROPOSAL, PLAN_IDS, buildPlans, formatPrice, getPlan, plans } from "@/lib/config/plans";

describe("plans config", () => {
  it("defines FREE / PRO / PREMIUM with limits 3 / 50 / 200", () => {
    expect(plans.map((p) => p.id)).toEqual([...PLAN_IDS]);
    expect(getPlan("free").analysesPerMonth).toBe(3);
    expect(getPlan("pro").analysesPerMonth).toBe(50);
    expect(getPlan("premium").analysesPerMonth).toBe(200);
  });

  it("free plan costs nothing and is not paid", () => {
    const free = getPlan("free");
    expect(free.price.amount).toBe(0);
    expect(free.paid).toBe(false);
  });

  it("uses proposal prices when env is missing", () => {
    const built = buildPlans({});
    expect(getPlan("pro", built).price.amount).toBe(DEFAULT_PRICE_PROPOSAL.pro);
    expect(getPlan("premium", built).price.amount).toBe(DEFAULT_PRICE_PROPOSAL.premium);
    expect(getPlan("pro", built).price.currency).toBe("EUR");
  });

  it("reads prices and currency from env", () => {
    const built = buildPlans({ currency: "usd", pricePro: "12", pricePremium: "30.5" });
    expect(getPlan("pro", built).price).toEqual({ amount: 12, currency: "USD", interval: "month" });
    expect(getPlan("premium", built).price.amount).toBe(30.5);
  });

  it("ignores invalid env prices", () => {
    const built = buildPlans({ pricePro: "free", pricePremium: "-3" });
    expect(getPlan("pro", built).price.amount).toBe(DEFAULT_PRICE_PROPOSAL.pro);
    expect(getPlan("premium", built).price.amount).toBe(DEFAULT_PRICE_PROPOSAL.premium);
  });

  it("formats prices", () => {
    expect(formatPrice({ amount: 0, currency: "EUR", interval: "month" })).toBe("€0");
    expect(formatPrice({ amount: 9.9, currency: "EUR", interval: "month" })).toBe("€9.90");
  });

  it("highlights exactly one plan", () => {
    expect(plans.filter((p) => p.highlighted)).toHaveLength(1);
  });
});
