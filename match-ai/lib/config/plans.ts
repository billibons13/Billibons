import { parsePositiveNumber, publicEnv } from "./env";

export const PLAN_IDS = ["free", "pro", "premium"] as const;
export type PlanId = (typeof PLAN_IDS)[number];

export interface PlanPrice {
  /** Price per billing interval in major units (e.g. 9.9 = 9.90 EUR). 0 = free. */
  amount: number;
  currency: string;
  interval: "month";
}

export interface Plan {
  id: PlanId;
  /** Monthly analysis allowance. Enforced server-side via consume_analysis_credit(). */
  analysesPerMonth: number;
  price: PlanPrice;
  /** Visually emphasised on the pricing page. */
  highlighted: boolean;
  /** Whether a paid Stripe checkout is required. Stripe price IDs live in lib/stripe/prices.ts. */
  paid: boolean;
}

/**
 * PROPOSAL — not approved by owner.
 * Default display prices used only when NEXT_PUBLIC_PLAN_PRICE_* is not set.
 * Final prices are decided by the owner (phase 9, Stripe) and must match the Stripe prices.
 */
export const DEFAULT_PRICE_PROPOSAL = {
  currency: "EUR",
  pro: 9.9,
  premium: 24.9,
} as const;

/** Monthly analysis limits per plan (from the product brief). */
export const PLAN_LIMITS: Record<PlanId, number> = {
  free: 3,
  pro: 50,
  premium: 200,
};

export interface PlanEnv {
  currency?: string;
  pricePro?: string;
  pricePremium?: string;
}

export function buildPlans(env: PlanEnv = {}): Plan[] {
  const currency = (env.currency ?? DEFAULT_PRICE_PROPOSAL.currency).toUpperCase();
  return [
    {
      id: "free",
      analysesPerMonth: PLAN_LIMITS.free,
      price: { amount: 0, currency, interval: "month" },
      highlighted: false,
      paid: false,
    },
    {
      id: "pro",
      analysesPerMonth: PLAN_LIMITS.pro,
      price: {
        amount: parsePositiveNumber(env.pricePro, DEFAULT_PRICE_PROPOSAL.pro),
        currency,
        interval: "month",
      },
      highlighted: true,
      paid: true,
    },
    {
      id: "premium",
      analysesPerMonth: PLAN_LIMITS.premium,
      price: {
        amount: parsePositiveNumber(env.pricePremium, DEFAULT_PRICE_PROPOSAL.premium),
        currency,
        interval: "month",
      },
      highlighted: false,
      paid: true,
    },
  ];
}

export const plans: Plan[] = buildPlans({
  currency: publicEnv.planCurrency,
  pricePro: publicEnv.planPricePro,
  pricePremium: publicEnv.planPricePremium,
});

export function getPlan(id: PlanId, source: Plan[] = plans): Plan {
  const plan = source.find((p) => p.id === id);
  if (!plan) throw new Error(`Unknown plan: ${id}`);
  return plan;
}

export function formatPrice(price: PlanPrice, locale = "en"): string {
  return new Intl.NumberFormat(locale, {
    style: "currency",
    currency: price.currency,
    minimumFractionDigits: Number.isInteger(price.amount) ? 0 : 2,
    maximumFractionDigits: 2,
  }).format(price.amount);
}
