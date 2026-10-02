/**
 * Nur echte Kundenstimmen eintragen – mit Einverständnis der Kunden.
 * Solange die Liste leer ist, zeigt die Website stattdessen einen
 * ehrlichen Hinweis und einen Link zu den Google-Bewertungen (falls vorhanden).
 */
export type Testimonial = {
  quote: string;
  name: string; // z. B. "Familie M." – Kürzel mit Einverständnis
  location: string;
  project: string;
  source?: "Google" | "Direkt" | "MyHammer" | "Andere";
};

export const testimonials: Testimonial[] = [];
