import type { AnalysisResult } from "./schema";

/**
 * Deterministic "insufficient data" result. Used whenever the system cannot
 * support a conclusion — never replaced by invented numbers.
 */
export function buildInsufficientResult(reason: string, modelVersion: string): AnalysisResult {
  return {
    status: "insufficient_data",
    summary: reason,
    confidence: 0,
    key_factors: [],
    positive_signals: [],
    negative_signals: [],
    risk_factors: [],
    uncertainties: [reason],
    data_quality: "insufficient",
    model_version: modelVersion,
  };
}
