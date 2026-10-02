import { randomUUID } from "node:crypto";
import type { LeadInput } from "./schema";
import type { LeadAttachment, LeadPayload, LeadSink } from "./types";
import { LogSink } from "./sinks/log";
import { MakeWebhookSink } from "./sinks/make";
import { GenericWebhookSink } from "./sinks/webhook";

/** Version des Einwilligungstexts im Formular – bei Textänderung hochzählen */
export const CONSENT_TEXT_VERSION = "2026-10-v1";

/**
 * Abstraktionsschicht: Die Website kennt nur `LeadSink`. Wohin der Lead geht
 * (Make → HubSpot/Pipedrive/Airtable/Sheets, direkter Webhook, Log), wird
 * ausschließlich über Umgebungsvariablen entschieden.
 */
export function getLeadSink(): LeadSink {
  const kind = process.env.LEAD_SINK ?? "make";
  if (kind === "make" && process.env.MAKE_WEBHOOK_URL) {
    return new MakeWebhookSink(process.env.MAKE_WEBHOOK_URL, process.env.MAKE_WEBHOOK_SECRET);
  }
  if (kind === "webhook" && process.env.GENERIC_WEBHOOK_URL) {
    return new GenericWebhookSink(process.env.GENERIC_WEBHOOK_URL);
  }
  if (process.env.NODE_ENV === "production" && kind !== "log") {
    throw new Error(`Lead-Sink "${kind}" ist nicht konfiguriert (Umgebungsvariablen prüfen).`);
  }
  return new LogSink();
}

export function buildLeadPayload(
  input: LeadInput,
  attachments: LeadAttachment[],
  ctx: { userAgent: string },
): LeadPayload {
  const now = new Date().toISOString();
  return {
    schema_version: "1.0",
    lead_id: `L-${now.slice(0, 10).replaceAll("-", "")}-${randomUUID().slice(0, 8)}`,
    timestamp: now,
    name: input.name,
    phone: input.phone,
    email: input.email,
    location: input.location,
    project_type: input.projectType,
    services: input.services,
    area: input.area,
    budget: input.budget,
    preferred_date: input.timeframe,
    message: input.message,
    uploaded_files: attachments.map((a) => ({
      field: a.field,
      name: a.file.name,
      type: a.file.type,
      size: a.file.size,
    })),
    consent: { given: true, text_version: CONSENT_TEXT_VERSION, timestamp: now },
    meta: {
      source: "website",
      source_page: input.sourcePage,
      utm: input.utm,
      user_agent: ctx.userAgent.slice(0, 300),
      locale: "de",
    },
  };
}
