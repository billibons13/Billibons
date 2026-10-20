import { DEFAULT_LOCALE, isLocale, type Locale } from "./config";
import { en } from "./messages/en";
import type { MessageKey, Messages, MessageVars } from "./types";

export type { Locale } from "./config";
export type { MessageKey, Messages, MessageVars } from "./types";

const dictionaries: Record<Locale, Messages> = {
  en,
};

/** Returns the dictionary for a locale, falling back to the default locale. */
export function getMessages(locale?: string | null): Messages {
  return dictionaries[isLocale(locale) ? locale : DEFAULT_LOCALE];
}

/** Replaces `{name}` placeholders. Unknown placeholders are left untouched. */
export function format(template: string, vars?: MessageVars): string {
  if (!vars) return template;
  return template.replace(/\{(\w+)\}/g, (match, name: string) =>
    Object.prototype.hasOwnProperty.call(vars, name) ? String(vars[name]) : match,
  );
}

/** Looks up a dot-path key. Returns the key itself if it is missing (never throws). */
export function translate(messages: Messages, key: MessageKey, vars?: MessageVars): string {
  let node: unknown = messages;
  for (const part of key.split(".")) {
    if (node && typeof node === "object" && part in node) {
      node = (node as Record<string, unknown>)[part];
    } else {
      return key;
    }
  }
  return typeof node === "string" ? format(node, vars) : key;
}

/** Convenience: a `t()` bound to a locale. */
export function getTranslator(locale?: string | null) {
  const messages = getMessages(locale);
  return (key: MessageKey, vars?: MessageVars) => translate(messages, key, vars);
}
