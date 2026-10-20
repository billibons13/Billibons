import "server-only";

import Stripe from "stripe";
import { serverEnv } from "@/lib/config/server-env";
import type { PlanId } from "@/lib/config/plans";

let stripe: Stripe | null = null;

/** Server-only Stripe client. Returns null when STRIPE_SECRET_KEY is not set. */
export function getStripe(): Stripe | null {
  if (!serverEnv.stripeSecretKey) return null;
  stripe ??= new Stripe(serverEnv.stripeSecretKey, { typescript: true });
  return stripe;
}

export function isStripeConfigured(): boolean {
  return Boolean(serverEnv.stripeSecretKey && serverEnv.stripePricePro && serverEnv.stripePricePremium);
}

/** Stripe price IDs per paid plan, from env (STRIPE_PRICE_PRO / STRIPE_PRICE_PREMIUM). */
export function getStripePriceId(plan: PlanId): string | null {
  switch (plan) {
    case "pro":
      return serverEnv.stripePricePro ?? null;
    case "premium":
      return serverEnv.stripePricePremium ?? null;
    default:
      return null;
  }
}

/** Reverse lookup used by the webhook (phase 9) to map a Stripe price to a plan. */
export function getPlanByStripePriceId(priceId: string): PlanId | null {
  if (priceId && priceId === serverEnv.stripePricePro) return "pro";
  if (priceId && priceId === serverEnv.stripePricePremium) return "premium";
  return null;
}
