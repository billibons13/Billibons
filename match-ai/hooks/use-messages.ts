"use client";

import { DEFAULT_LOCALE } from "@/lib/i18n/config";
import { getMessages, type Messages } from "@/lib/i18n";

/**
 * Client-side access to the dictionary. Today there is one locale; when more
 * are added, read the active locale from a context set in the root layout
 * (see docs/ARCHITECTURE.md → "Adding a language").
 */
export function useMessages(): Messages {
  return getMessages(DEFAULT_LOCALE);
}
