import { describe, expect, it } from "vitest";
import { getErrorMessage, ERROR_CODES } from "@/lib/errors";
import { format, getMessages, getTranslator, translate } from "@/lib/i18n";
import { isLocale } from "@/lib/i18n/config";

describe("i18n", () => {
  it("returns the English dictionary by default and for unknown locales", () => {
    expect(getMessages().nav.login).toBe("Log in");
    expect(getMessages("xx")).toBe(getMessages("en"));
    expect(getMessages(null)).toBe(getMessages("en"));
  });

  it("translates dot-path keys with interpolation", () => {
    const m = getMessages();
    expect(translate(m, "landing.hero.primaryCta")).toBe("Try for free");
    expect(translate(m, "landing.pricing.analysesPerMonth", { count: 50 })).toBe("50 analyses per month");
    const t = getTranslator("en");
    expect(t("dashboard.signedInAs", { email: "a@b.c" })).toBe("Signed in as a@b.c");
  });

  it("returns the key for missing entries instead of throwing", () => {
    // @ts-expect-error — deliberately invalid key
    expect(translate(getMessages(), "landing.nope")).toBe("landing.nope");
  });

  it("format keeps unknown placeholders", () => {
    expect(format("Hi {name}, {other}", { name: "A" })).toBe("Hi A, {other}");
  });

  it("validates locales", () => {
    expect(isLocale("en")).toBe(true);
    expect(isLocale("de")).toBe(false);
  });

  it("has a message for every error code", () => {
    for (const code of ERROR_CODES) {
      expect(getErrorMessage(code).length).toBeGreaterThan(10);
    }
    expect(getErrorMessage("IMAGE_TOO_LARGE", { maxMb: 8 })).toContain("8 MB");
  });

  it("contains no outcome guarantees in user-facing text", () => {
    const text = JSON.stringify(getMessages()).toLowerCase();
    for (const banned of ["100% win", "guaranteed win", "sure bet", "risk-free", "risk free"]) {
      expect(text).not.toContain(banned);
    }
  });
});
