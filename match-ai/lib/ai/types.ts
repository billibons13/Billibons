import type { AllowedImageType } from "@/lib/config/upload";
import type { AnalysisResult, MatchExtraction } from "./schema";

export type { AnalysisResult, KeyFactor, MatchExtraction } from "./schema";

/** A validated image ready to be sent to a vision model. */
export interface AIImageInput {
  mimeType: AllowedImageType;
  /** Base64 without the `data:` prefix. */
  base64: string;
}

/**
 * Extra data gathered between extraction and analysis (stats APIs, news …).
 * Phase 1: no sources are connected, so it is always empty — see pipeline.ts.
 */
export interface AnalysisContext {
  sources: { name: string; retrievedAt: string; data: Record<string, unknown> }[];
  notes: string[];
}

export interface AIProvider {
  /** Stable identifier, stored in ai_requests.provider. */
  readonly id: string;
  /** Model identifier, stored in analysis_results.model_version. */
  readonly model: string;
  extractMatch(image: AIImageInput): Promise<MatchExtraction>;
  analyze(extraction: MatchExtraction, context: AnalysisContext): Promise<AnalysisResult>;
}

export interface PipelineResult {
  provider: string;
  extraction: MatchExtraction;
  context: AnalysisContext;
  result: AnalysisResult;
}
