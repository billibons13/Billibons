import { z } from "zod";

/* ----------------------------- Match extraction ----------------------------- */

export const MatchStatusSchema = z.enum(["scheduled", "live", "finished", "unknown"]);

export const VisibleOddSchema = z.object({
  market: z.string().min(1),
  selection: z.string().min(1),
  value: z.number().positive(),
});

/**
 * What the vision step could read from the screenshot. Every field that is not
 * clearly visible MUST be null — the model is instructed not to guess.
 */
export const MatchExtractionSchema = z.object({
  status: z.enum(["ok", "not_recognized", "insufficient_data"]),
  sport: z.string().min(1).nullable(),
  competition: z.string().min(1).nullable(),
  home_team: z.string().min(1).nullable(),
  away_team: z.string().min(1).nullable(),
  match_date: z.string().min(1).nullable(),
  match_status: MatchStatusSchema,
  score: z
    .object({ home: z.number().int().min(0), away: z.number().int().min(0) })
    .nullable(),
  visible_odds: z.array(VisibleOddSchema).max(50),
  visible_stats: z.array(z.object({ label: z.string().min(1), value: z.string().min(1) })).max(50),
  extraction_confidence: z.number().min(0).max(1),
  notes: z.array(z.string()).max(20),
});

export type MatchExtraction = z.infer<typeof MatchExtractionSchema>;

/* -------------------------------- Analysis -------------------------------- */

export const KeyFactorTypeSchema = z.enum([
  "form",
  "head_to_head",
  "home_advantage",
  "recent_performance",
  "injuries",
  "schedule",
  "motivation",
  "market",
  "other",
]);

export const KeyFactorSchema = z.object({
  type: KeyFactorTypeSchema,
  title: z.string().min(1).max(120),
  detail: z.string().min(1).max(600),
  impact: z.enum(["positive", "negative", "neutral"]),
});

export const DataQualitySchema = z.enum(["high", "medium", "low", "insufficient"]);

const stringList = z.array(z.string().min(1).max(400)).max(20);

export const AnalysisResultSchema = z
  .object({
    status: z.enum(["ok", "insufficient_data"]),
    summary: z.string().min(1).max(1200),
    confidence: z.number().min(0).max(1),
    key_factors: z.array(KeyFactorSchema).max(12),
    positive_signals: stringList,
    negative_signals: stringList,
    risk_factors: stringList,
    uncertainties: stringList,
    data_quality: DataQualitySchema,
    model_version: z.string().min(1).max(120),
  })
  .superRefine((value, ctx) => {
    if (value.status === "insufficient_data") {
      if (value.confidence !== 0) {
        ctx.addIssue({
          code: "custom",
          path: ["confidence"],
          message: "confidence must be 0 when status is insufficient_data",
        });
      }
      if (value.data_quality !== "insufficient") {
        ctx.addIssue({
          code: "custom",
          path: ["data_quality"],
          message: "data_quality must be 'insufficient' when status is insufficient_data",
        });
      }
    }
    if (value.status === "ok" && value.data_quality === "insufficient") {
      ctx.addIssue({
        code: "custom",
        path: ["status"],
        message: "status must be insufficient_data when data_quality is insufficient",
      });
    }
  });

export type AnalysisResult = z.infer<typeof AnalysisResultSchema>;
export type KeyFactor = z.infer<typeof KeyFactorSchema>;
