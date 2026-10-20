import type { z } from "zod";

/** Parses a model response that should be JSON; tolerates code fences / surrounding text. */
export function parseModelJson(text: string): unknown {
  const trimmed = text.trim();
  const fenced = trimmed.match(/^```(?:json)?\s*([\s\S]*?)\s*```$/i);
  const candidate = fenced?.[1] ?? trimmed;
  try {
    return JSON.parse(candidate);
  } catch {
    const start = candidate.indexOf("{");
    const end = candidate.lastIndexOf("}");
    if (start >= 0 && end > start) {
      return JSON.parse(candidate.slice(start, end + 1));
    }
    throw new SyntaxError("Model response is not valid JSON");
  }
}

export function formatIssues(error: z.ZodError): string {
  return error.issues
    .map((issue) => `${issue.path.join(".") || "(root)"}: ${issue.message}`)
    .join("\n");
}

export type ValidationOutcome<T> = { ok: true; data: T } | { ok: false; issues: string };

export function validateJson<T>(schema: z.ZodType<T>, text: string): ValidationOutcome<T> {
  let parsed: unknown;
  try {
    parsed = parseModelJson(text);
  } catch (error) {
    return { ok: false, issues: error instanceof Error ? error.message : "Invalid JSON" };
  }
  const result = schema.safeParse(parsed);
  return result.success ? { ok: true, data: result.data } : { ok: false, issues: formatIssues(result.error) };
}

/**
 * Validates model output; on failure asks the model ONCE to repair it.
 * Returns null if the repaired output is still invalid.
 */
export async function validateWithRepair<T>(
  schema: z.ZodType<T>,
  text: string,
  repair: (invalidOutput: string, issues: string) => Promise<string>,
): Promise<T | null> {
  const first = validateJson(schema, text);
  if (first.ok) return first.data;
  const repaired = await repair(text, first.issues);
  const second = validateJson(schema, repaired);
  return second.ok ? second.data : null;
}
