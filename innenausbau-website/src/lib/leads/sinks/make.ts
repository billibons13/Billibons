import type { LeadAttachment, LeadPayload, LeadSink } from "../types";

/**
 * Sendet den Lead als multipart/form-data an einen Make "Custom webhook".
 *  - Feld `payload`: JSON (LeadPayload) → in Make mit "JSON > Parse JSON" auslesen
 *  - Felder `file_0..n`: Fotos als Binärdaten → in Make direkt an Google Drive / Dropbox übergeben
 */
export class MakeWebhookSink implements LeadSink {
  readonly name = "make";

  constructor(
    private readonly url: string,
    private readonly secret?: string,
  ) {}

  async send(payload: LeadPayload, attachments: LeadAttachment[]) {
    const body = new FormData();
    body.set("payload", JSON.stringify(payload));
    for (const a of attachments) body.set(a.field, a.file, a.file.name);

    const res = await fetch(this.url, {
      method: "POST",
      body,
      headers: this.secret ? { "X-Lead-Secret": this.secret } : undefined,
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok) throw new Error(`Make webhook antwortete mit ${res.status}`);
  }
}
