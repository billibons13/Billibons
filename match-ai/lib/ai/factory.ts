import { AppError } from "@/lib/errors";
import { DevelopmentProvider } from "./providers/development";
import { OpenAIProvider } from "./providers/openai";
import type { AIProvider } from "./types";

export const AI_PROVIDER_IDS = ["development", "openai"] as const;
export type AIProviderId = (typeof AI_PROVIDER_IDS)[number];

/** Default model when OPENAI_MODEL is not set. Override via env. */
export const DEFAULT_OPENAI_MODEL = "gpt-4o-mini";

export interface AIProviderEnv {
  provider?: string;
  openaiApiKey?: string;
  openaiModel?: string;
}

/**
 * Pure factory (testable). Unset AI_PROVIDER → development provider, which
 * never fabricates results. A misconfigured real provider throws NOT_CONFIGURED
 * instead of silently falling back.
 */
export function createAIProvider(env: AIProviderEnv): AIProvider {
  const id = (env.provider ?? "development").toLowerCase();
  switch (id) {
    case "development":
      return new DevelopmentProvider();
    case "openai":
      if (!env.openaiApiKey) throw new AppError("NOT_CONFIGURED", { cause: "OPENAI_API_KEY missing" });
      return new OpenAIProvider({
        apiKey: env.openaiApiKey,
        model: env.openaiModel ?? DEFAULT_OPENAI_MODEL,
      });
    default:
      throw new AppError("NOT_CONFIGURED", { cause: `Unknown AI_PROVIDER: ${id}` });
  }
}
