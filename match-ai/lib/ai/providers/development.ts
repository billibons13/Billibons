import { buildInsufficientResult } from "../insufficient";
import type { AIProvider, AnalysisContext, AIImageInput } from "../types";
import type { AnalysisResult, MatchExtraction } from "../schema";

export const DEVELOPMENT_PROVIDER_NOTE =
  "No AI provider is configured (AI_PROVIDER=development). No analysis was performed and no numbers were generated.";

/**
 * Development provider: lets the full pipeline run locally without an AI key.
 * It deliberately does NOT fabricate data — it always reports insufficient data.
 */
export class DevelopmentProvider implements AIProvider {
  readonly id = "development";
  readonly model = "development-no-ai";

  async extractMatch(image: AIImageInput): Promise<MatchExtraction> {
    void image;
    return {
      status: "insufficient_data",
      sport: null,
      competition: null,
      home_team: null,
      away_team: null,
      match_date: null,
      match_status: "unknown",
      score: null,
      visible_odds: [],
      visible_stats: [],
      extraction_confidence: 0,
      notes: [DEVELOPMENT_PROVIDER_NOTE],
    };
  }

  async analyze(extraction: MatchExtraction, context: AnalysisContext): Promise<AnalysisResult> {
    void extraction;
    void context;
    return buildInsufficientResult(DEVELOPMENT_PROVIDER_NOTE, this.model);
  }
}
