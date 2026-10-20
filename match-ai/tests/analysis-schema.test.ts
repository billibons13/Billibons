import { describe, expect, it } from "vitest";
import { AnalysisResultSchema, MatchExtractionSchema } from "@/lib/ai/schema";
import { buildInsufficientResult } from "@/lib/ai/insufficient";
import { parseModelJson, validateJson, validateWithRepair } from "@/lib/ai/json";

const valid = {
  status: "ok",
  summary: "Balanced match based on visible data.",
  confidence: 0.62,
  key_factors: [{ type: "form", title: "Form", detail: "Home side won 3 of last 5 (visible).", impact: "positive" }],
  positive_signals: ["Home form"],
  negative_signals: [],
  risk_factors: ["Small sample"],
  uncertainties: ["Line-ups unknown"],
  data_quality: "medium",
  model_version: "test-model",
};

describe("AnalysisResultSchema", () => {
  it("accepts a valid result", () => {
    expect(AnalysisResultSchema.safeParse(valid).success).toBe(true);
  });

  it("rejects confidence outside 0..1", () => {
    expect(AnalysisResultSchema.safeParse({ ...valid, confidence: 1.2 }).success).toBe(false);
    expect(AnalysisResultSchema.safeParse({ ...valid, confidence: -0.1 }).success).toBe(false);
  });

  it("rejects unknown status, factor type and impact", () => {
    expect(AnalysisResultSchema.safeParse({ ...valid, status: "win" }).success).toBe(false);
    expect(
      AnalysisResultSchema.safeParse({ ...valid, key_factors: [{ ...valid.key_factors[0], impact: "huge" }] }).success,
    ).toBe(false);
    expect(
      AnalysisResultSchema.safeParse({ ...valid, key_factors: [{ ...valid.key_factors[0], type: "luck" }] }).success,
    ).toBe(false);
  });

  it("rejects missing fields", () => {
    const { summary: _omit, ...rest } = valid;
    void _omit;
    expect(AnalysisResultSchema.safeParse(rest).success).toBe(false);
  });

  it("requires confidence 0 and insufficient data quality for insufficient_data", () => {
    expect(
      AnalysisResultSchema.safeParse({ ...valid, status: "insufficient_data", confidence: 0.5, data_quality: "insufficient" })
        .success,
    ).toBe(false);
    expect(AnalysisResultSchema.safeParse({ ...valid, data_quality: "insufficient" }).success).toBe(false);
    expect(AnalysisResultSchema.safeParse(buildInsufficientResult("No data", "m")).success).toBe(true);
  });
});

describe("MatchExtractionSchema", () => {
  it("accepts nulls for unknown fields", () => {
    const result = MatchExtractionSchema.safeParse({
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
      notes: [],
    });
    expect(result.success).toBe(true);
  });
});

describe("model JSON helpers", () => {
  it("parses fenced JSON", () => {
    expect(parseModelJson('```json\n{"a":1}\n```')).toEqual({ a: 1 });
    expect(parseModelJson('Here: {"a":2} done')).toEqual({ a: 2 });
  });

  it("reports issues for invalid output", () => {
    const outcome = validateJson(AnalysisResultSchema, JSON.stringify({ ...valid, confidence: 5 }));
    expect(outcome.ok).toBe(false);
  });

  it("repairs once and gives up after a second failure", async () => {
    let calls = 0;
    const repaired = await validateWithRepair(AnalysisResultSchema, "not json", async () => {
      calls += 1;
      return JSON.stringify(valid);
    });
    expect(calls).toBe(1);
    expect(repaired?.confidence).toBe(0.62);

    const failed = await validateWithRepair(AnalysisResultSchema, "not json", async () => "still not json");
    expect(failed).toBeNull();
  });
});
