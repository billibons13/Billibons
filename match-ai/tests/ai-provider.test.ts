import { describe, expect, it } from "vitest";
import { AnalysisResultSchema } from "@/lib/ai/schema";
import { createAIProvider } from "@/lib/ai/factory";
import { runAnalysisPipeline } from "@/lib/ai/pipeline";
import { DevelopmentProvider } from "@/lib/ai/providers/development";
import { OpenAIProvider } from "@/lib/ai/providers/openai";
import { AppError } from "@/lib/errors";
import type { AIProvider } from "@/lib/ai/types";

const image = { mimeType: "image/png" as const, base64: "iVBORw0KGgo=" };

describe("DevelopmentProvider", () => {
  it("returns insufficient_data and never invents numbers", async () => {
    const provider = new DevelopmentProvider();
    const extraction = await provider.extractMatch(image);
    expect(extraction.status).toBe("insufficient_data");
    expect(extraction.home_team).toBeNull();
    expect(extraction.extraction_confidence).toBe(0);

    const result = await provider.analyze(extraction, { sources: [], notes: [] });
    expect(AnalysisResultSchema.parse(result)).toEqual(result);
    expect(result.status).toBe("insufficient_data");
    expect(result.confidence).toBe(0);
    expect(result.key_factors).toEqual([]);
    expect(result.summary).toMatch(/No AI provider is configured/);
  });

  it("is deterministic", async () => {
    const provider = new DevelopmentProvider();
    const a = await provider.analyze(await provider.extractMatch(image), { sources: [], notes: [] });
    const b = await provider.analyze(await provider.extractMatch(image), { sources: [], notes: [] });
    expect(a).toEqual(b);
  });
});

describe("createAIProvider", () => {
  it("defaults to the development provider", () => {
    expect(createAIProvider({}).id).toBe("development");
  });

  it("requires an API key for openai", () => {
    expect(() => createAIProvider({ provider: "openai" })).toThrow(AppError);
    expect(createAIProvider({ provider: "openai", openaiApiKey: "test" })).toBeInstanceOf(OpenAIProvider);
  });

  it("rejects unknown providers", () => {
    expect(() => createAIProvider({ provider: "magic" })).toThrow(AppError);
  });
});

describe("runAnalysisPipeline", () => {
  it("returns insufficient_data end-to-end with the development provider", async () => {
    const out = await runAnalysisPipeline(image, new DevelopmentProvider());
    expect(out.provider).toBe("development");
    expect(out.result.status).toBe("insufficient_data");
    expect(out.context.sources).toEqual([]);
  });

  it("throws MATCH_NOT_RECOGNIZED when no match is visible", async () => {
    const dev = new DevelopmentProvider();
    const provider: AIProvider = {
      id: "stub",
      model: "stub",
      extractMatch: async (img) => ({ ...(await dev.extractMatch(img)), status: "not_recognized" }),
      analyze: dev.analyze.bind(dev),
    };
    await expect(runAnalysisPipeline(image, provider)).rejects.toMatchObject({ code: "MATCH_NOT_RECOGNIZED" });
  });

  it("rejects invalid analysis output", async () => {
    const dev = new DevelopmentProvider();
    const provider: AIProvider = {
      id: "stub",
      model: "stub",
      extractMatch: async (img) => ({
        ...(await dev.extractMatch(img)),
        status: "ok",
        home_team: "A",
        away_team: "B",
        extraction_confidence: 0.9,
      }),
      analyze: async () => ({ ...(await dev.analyze({} as never, { sources: [], notes: [] })), confidence: 0.9 }),
    };
    await expect(runAnalysisPipeline(image, provider)).rejects.toMatchObject({ code: "ANALYSIS_FAILED" });
  });
});

describe("OpenAIProvider", () => {
  it("maps 5xx / 429 to AI_UNAVAILABLE", async () => {
    const provider = new OpenAIProvider({
      apiKey: "k",
      model: "m",
      fetchImpl: async () => new Response("busy", { status: 503 }),
    });
    await expect(provider.extractMatch(image)).rejects.toMatchObject({ code: "AI_UNAVAILABLE" });
  });

  it("repairs invalid JSON once", async () => {
    const bodies = ["not json", JSON.stringify({
      status: "not_recognized", sport: null, competition: null, home_team: null, away_team: null,
      match_date: null, match_status: "unknown", score: null, visible_odds: [], visible_stats: [],
      extraction_confidence: 0, notes: [],
    })];
    let call = 0;
    const provider = new OpenAIProvider({
      apiKey: "k",
      model: "m",
      fetchImpl: async () =>
        new Response(JSON.stringify({ choices: [{ message: { content: bodies[call++] } }] }), { status: 200 }),
    });
    const extraction = await provider.extractMatch(image);
    expect(call).toBe(2);
    expect(extraction.status).toBe("not_recognized");
  });
});
