import type { LeadAttachment, LeadPayload, LeadSink } from "../types";

/** Generischer JSON-Webhook (z. B. n8n, Zapier, eigenes Backend). Fotos als Base64. */
export class GenericWebhookSink implements LeadSink {
  readonly name = "webhook";

  constructor(private readonly url: string) {}

  async send(payload: LeadPayload, attachments: LeadAttachment[]) {
    const files = await Promise.all(
      attachments.map(async (a) => ({
        field: a.field,
        name: a.file.name,
        type: a.file.type,
        data_base64: Buffer.from(await a.file.arrayBuffer()).toString("base64"),
      })),
    );
    const res = await fetch(this.url, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ ...payload, files }),
      signal: AbortSignal.timeout(15_000),
    });
    if (!res.ok) throw new Error(`Webhook antwortete mit ${res.status}`);
  }
}
