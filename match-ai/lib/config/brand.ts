import { getAppUrl } from "./env";

/**
 * Brand configuration — the ONLY place the product name lives.
 * To rename the product, change `name` (and optionally `shortName`/`tagline`).
 * See docs/ARCHITECTURE.md → "Renaming the brand".
 */
export const brand = {
  /** Working name — not final. */
  name: "MATCH AI",
  shortName: "MATCH AI",
  tagline: "Structured AI analysis from a single match screenshot.",
  description:
    "Upload a screenshot of a sports match. AI recognizes the match and returns a structured, transparent analysis: key factors, signals, risks and a confidence score.",
  /** PLACEHOLDER — replace with the real support address before launch. */
  supportEmail: "support@example.com",
  /** PLACEHOLDER — legal entity name shown in the footer. Fill in before launch. */
  legalEntity: "[Company name]",
  get appUrl(): string {
    return getAppUrl();
  },
} as const;

export function absoluteUrl(path = "/"): string {
  const normalized = path.startsWith("/") ? path : `/${path}`;
  return `${getAppUrl()}${normalized}`;
}
