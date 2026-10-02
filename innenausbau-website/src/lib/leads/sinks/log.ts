import type { LeadAttachment, LeadPayload, LeadSink } from "../types";

/** Entwicklung: schreibt den Lead nur ins Server-Log. */
export class LogSink implements LeadSink {
  readonly name = "log";

  async send(payload: LeadPayload, attachments: LeadAttachment[]) {
    console.info("[lead]", JSON.stringify(payload, null, 2), `+ ${attachments.length} Datei(en)`);
  }
}
