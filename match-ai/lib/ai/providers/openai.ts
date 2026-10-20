import "server-only";

import { AppError } from "@/lib/errors";
import { validateWithRepair } from "../json";
import {
  ANALYSIS_SYSTEM_PROMPT,
  EXTRACTION_SYSTEM_PROMPT,
  REPAIR_SYSTEM_PROMPT,
  buildAnalysisUserPrompt,
  buildRepairUserPrompt,
} from "../prompts";
import {
  AnalysisResultSchema,
  MatchExtractionSchema,
  type AnalysisResult,
  type MatchExtraction,
} from "../schema";
import type { AIImageInput, AIProvider, AnalysisContext } from "../types";

const ENDPOINT = "https://api.openai.com/v1/chat/completions";
const REQUEST_TIMEOUT_MS = 60_000;

type ContentPart =
  | { type: "text"; text: string }
  | { type: "image_url"; image_url: { url: string; detail: "high" | "low" | "auto" } };

interface ChatMessage {
  role: "system" | "user";
  content: string | ContentPart[];
}

interface ChatCompletionResponse {
  choices?: { message?: { content?: string | null } }[];
}

export interface OpenAIProviderOptions {
  apiKey: string;
  model: string;
  fetchImpl?: typeof fetch;
}

/**
 * OpenAI vision provider (Chat Completions API, JSON mode). Server-only:
 * the API key never leaves the server.
 */
export class OpenAIProvider implements AIProvider {
  readonly id = "openai";
  readonly model: string;
  private readonly apiKey: string;
  private readonly fetchImpl: typeof fetch;

  constructor(options: OpenAIProviderOptions) {
    this.apiKey = options.apiKey;
    this.model = options.model;
    this.fetchImpl = options.fetchImpl ?? fetch;
  }

  async extractMatch(image: AIImageInput): Promise<MatchExtraction> {
    const raw = await this.complete([
      { role: "system", content: EXTRACTION_SYSTEM_PROMPT },
      {
        role: "user",
        content: [
          { type: "text", text: "Extract the match information from this screenshot." },
          { type: "image_url", image_url: { url: `data:${image.mimeType};base64,${image.base64}`, detail: "high" } },
        ],
      },
    ]);
    const data = await validateWithRepair(MatchExtractionSchema, raw, (invalid, issues) =>
      this.repair(invalid, issues),
    );
    if (!data) throw new AppError("ANALYSIS_FAILED", { cause: "extraction_validation_failed" });
    return data;
  }

  async analyze(extraction: MatchExtraction, context: AnalysisContext): Promise<AnalysisResult> {
    const raw = await this.complete([
      { role: "system", content: ANALYSIS_SYSTEM_PROMPT },
      { role: "user", content: buildAnalysisUserPrompt(extraction, context, this.model) },
    ]);
    const data = await validateWithRepair(AnalysisResultSchema, raw, (invalid, issues) =>
      this.repair(invalid, issues),
    );
    if (!data) throw new AppError("ANALYSIS_FAILED", { cause: "analysis_validation_failed" });
    // The provider is the source of truth for the model id, not the model's own claim.
    return { ...data, model_version: this.model };
  }

  private repair(invalidOutput: string, issues: string): Promise<string> {
    return this.complete([
      { role: "system", content: REPAIR_SYSTEM_PROMPT },
      { role: "user", content: buildRepairUserPrompt(invalidOutput, issues) },
    ]);
  }

  private async complete(messages: ChatMessage[]): Promise<string> {
    let response: Response;
    try {
      response = await this.fetchImpl(ENDPOINT, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${this.apiKey}`,
        },
        body: JSON.stringify({
          model: this.model,
          messages,
          temperature: 0,
          response_format: { type: "json_object" },
        }),
        signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
      });
    } catch (cause) {
      throw new AppError("AI_UNAVAILABLE", { cause });
    }

    if (response.status === 429 || response.status >= 500) {
      throw new AppError("AI_UNAVAILABLE", { cause: `openai_status_${response.status}` });
    }
    if (!response.ok) {
      throw new AppError("ANALYSIS_FAILED", { cause: `openai_status_${response.status}` });
    }

    const body = (await response.json()) as ChatCompletionResponse;
    const content = body.choices?.[0]?.message?.content;
    if (!content) throw new AppError("ANALYSIS_FAILED", { cause: "openai_empty_response" });
    return content;
  }
}
