import { AppError } from "@/lib/errors";
import { buildInsufficientResult } from "./insufficient";
import { AnalysisResultSchema, MatchExtractionSchema, type MatchExtraction } from "./schema";
import type { AIImageInput, AIProvider, AnalysisContext, PipelineResult } from "./types";

/**
 * Context enrichment — STUB (phase 1).
 * Later phases may add sources such as a sports statistics API. Each source
 * must be appended to `sources` with its name and retrieval time so that the
 * analysis remains traceable. Today it adds nothing, on purpose: the analysis
 * step must not assume any data beyond the screenshot.
 */
export async function enrichContext(extraction: MatchExtraction): Promise<AnalysisContext> {
  void extraction;
  return { sources: [], notes: ["No external data sources are connected; analysis is based on the screenshot only."] };
}

/**
 * image → extraction → validation → context enrichment → analysis → validation.
 * The image must already be validated (lib/upload/validate.ts).
 */
export async function runAnalysisPipeline(image: AIImageInput, provider: AIProvider): Promise<PipelineResult> {
  const extraction = MatchExtractionSchema.parse(await provider.extractMatch(image));

  if (extraction.status === "not_recognized") {
    throw new AppError("MATCH_NOT_RECOGNIZED");
  }

  const context = await enrichContext(extraction);

  if (extraction.status === "insufficient_data" || !extraction.home_team || !extraction.away_team) {
    const reason =
      extraction.notes[0] ?? "The screenshot does not contain enough readable match information for an analysis.";
    return {
      provider: provider.id,
      extraction,
      context,
      result: buildInsufficientResult(reason, provider.model),
    };
  }

  const parsed = AnalysisResultSchema.safeParse(await provider.analyze(extraction, context));
  if (!parsed.success) {
    throw new AppError("ANALYSIS_FAILED", { cause: parsed.error });
  }

  return { provider: provider.id, extraction, context, result: parsed.data };
}
