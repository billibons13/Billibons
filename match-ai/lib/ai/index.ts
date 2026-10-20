import "server-only";

import { serverEnv } from "@/lib/config/server-env";
import { createAIProvider } from "./factory";
import type { AIProvider } from "./types";

export { runAnalysisPipeline } from "./pipeline";
export * from "./schema";
export type * from "./types";

/** Returns the AI provider configured via AI_PROVIDER (server-only). */
export function getAIProvider(): AIProvider {
  return createAIProvider({
    provider: serverEnv.aiProvider,
    openaiApiKey: serverEnv.openaiApiKey,
    openaiModel: serverEnv.openaiModel,
  });
}
