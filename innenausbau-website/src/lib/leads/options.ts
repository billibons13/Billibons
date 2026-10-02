/** Auswahloptionen des Anfrageformulars – geteilt von Client und Server */
export const projectTypes = ["Wohnung", "Haus", "Büro", "Gewerbe"] as const;

export const workOptions = [
  "Komplettrenovierung",
  "Badsanierung",
  "Küchenrenovierung",
  "Trockenbau",
  "Innenputz",
  "Spachtelarbeiten",
  "Malerarbeiten",
  "Bodenbeläge",
  "Fliesenarbeiten",
  "Decken & Wände",
  "Sanierung",
  "Sonstiges",
] as const;

export const timeframes = [
  "So schnell wie möglich",
  "In 1–3 Monaten",
  "In 3–6 Monaten",
  "Später / noch offen",
] as const;

export const budgets = [
  "Keine Angabe",
  "unter 10.000 €",
  "10.000–25.000 €",
  "25.000–50.000 €",
  "50.000–100.000 €",
  "über 100.000 €",
] as const;

export const UPLOAD_LIMITS = {
  maxFiles: 6,
  /** nach clientseitiger Komprimierung */
  maxFileBytes: 2.5 * 1024 * 1024,
  maxTotalBytes: 8 * 1024 * 1024,
  accept: ["image/jpeg", "image/png", "image/webp", "image/heic", "image/heif"],
};
