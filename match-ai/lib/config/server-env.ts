import "server-only";

/**
 * Server-only environment variables. Importing this module from a Client
 * Component fails the build (thanks to `server-only`), which keeps secrets
 * out of the browser bundle.
 */

function clean(value: string | undefined): string | undefined {
  const trimmed = value?.trim();
  return trimmed ? trimmed : undefined;
}

export const serverEnv = {
  supabaseServiceRoleKey: clean(process.env.SUPABASE_SERVICE_ROLE_KEY),
  aiProvider: clean(process.env.AI_PROVIDER),
  openaiApiKey: clean(process.env.OPENAI_API_KEY),
  openaiModel: clean(process.env.OPENAI_MODEL),
  stripeSecretKey: clean(process.env.STRIPE_SECRET_KEY),
  stripeWebhookSecret: clean(process.env.STRIPE_WEBHOOK_SECRET),
  stripePricePro: clean(process.env.STRIPE_PRICE_PRO),
  stripePricePremium: clean(process.env.STRIPE_PRICE_PREMIUM),
  maxUploadMb: clean(process.env.MAX_UPLOAD_MB),
  imageRetentionDays: clean(process.env.IMAGE_RETENTION_DAYS),
} as const;
