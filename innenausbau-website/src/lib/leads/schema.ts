import { z } from "zod";
import { budgets, projectTypes, timeframes, workOptions } from "./options";

const trimmed = (max: number) => z.string().trim().max(max);

/** Validierung der Formulardaten (Server-seitig maßgeblich) */
export const leadInputSchema = z.object({
  name: trimmed(120).min(2, "Bitte geben Sie Ihren Namen an."),
  phone: trimmed(40).regex(/^[+()\d\s/-]{6,}$/, "Bitte geben Sie eine gültige Telefonnummer an."),
  email: z.union([z.literal(""), z.email("Bitte geben Sie eine gültige E-Mail-Adresse an.")]),
  location: trimmed(120).min(2, "Bitte geben Sie den Ort des Projekts an."),
  projectType: z.enum(projectTypes, { message: "Bitte wählen Sie die Objektart." }),
  services: z.array(z.enum(workOptions)).min(1, "Bitte wählen Sie mindestens eine Leistung."),
  area: trimmed(20).optional().default(""),
  timeframe: z.union([z.literal(""), z.enum(timeframes)]).default(""),
  budget: z.union([z.literal(""), z.enum(budgets)]).default(""),
  message: trimmed(3000).optional().default(""),
  consent: z.literal(true, { message: "Bitte stimmen Sie der Verarbeitung Ihrer Daten zu." }),
  // Tracking (optional, vom Client gesetzt)
  sourcePage: trimmed(200).optional().default(""),
  utm: z.record(z.string(), z.string().max(200)).optional().default({}),
});

export type LeadInput = z.infer<typeof leadInputSchema>;
