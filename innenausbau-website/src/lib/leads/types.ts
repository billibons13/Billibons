/**
 * Kanonisches Lead-Format = Webhook-Payload an Make.com.
 * Snake_case, damit es in Make, Google Sheets und CRMs ohne Mapping lesbar ist.
 * Änderungen hier IMMER mit make/lead-payload.schema.json abgleichen.
 */
export type LeadFile = {
  field: string; // Name des Multipart-Felds, z. B. "file_0"
  name: string;
  type: string;
  size: number;
};

export type LeadPayload = {
  schema_version: "1.0";
  lead_id: string;
  timestamp: string; // ISO 8601, UTC
  name: string;
  phone: string;
  email: string;
  location: string;
  project_type: string;
  services: string[];
  area: string; // m², Freitext
  budget: string;
  preferred_date: string; // gewünschter Zeitraum
  message: string;
  uploaded_files: LeadFile[];
  consent: { given: true; text_version: string; timestamp: string };
  meta: {
    source: "website";
    source_page: string;
    utm: Record<string, string>;
    user_agent: string;
    locale: string;
  };
};

export type LeadAttachment = { field: string; file: File };

export interface LeadSink {
  readonly name: string;
  send(payload: LeadPayload, attachments: LeadAttachment[]): Promise<void>;
}
