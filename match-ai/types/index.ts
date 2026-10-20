/** Shared domain types re-exported for convenient imports across the app. */
export type { PlanId, Plan, PlanPrice } from "@/lib/config/plans";
export type { Locale, Messages, MessageKey } from "@/lib/i18n";
export type { ErrorCode, PublicError } from "@/lib/errors";
export type { AnalysisResult, MatchExtraction, KeyFactor } from "@/lib/ai/schema";
export type { AIProvider, AnalysisContext, PipelineResult } from "@/lib/ai/types";
export type { AnalyticsEvent } from "@/lib/analytics";
