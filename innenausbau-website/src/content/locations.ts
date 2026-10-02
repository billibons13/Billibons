/**
 * Architektur für zukünftige Standortseiten (/innenausbau/[ort]).
 *
 * Regeln gegen Doorway Pages:
 *  - Eine Seite wird nur generiert, wenn `published: true` UND echter, eigener Inhalt vorliegt.
 *  - Mindestens: lokales Referenzprojekt ODER konkrete lokale Besonderheiten (Bausubstanz, Anfahrt, Ansprechpartner).
 *  - Kein Textbaustein mit ausgetauschtem Ortsnamen.
 */
export type Location = {
  slug: string;
  city: string;
  district: string;
  published: boolean;
  intro?: string;
  localNotes?: string[]; // z. B. typische Bausubstanz, Besonderheiten
  projectSlugs?: string[];
  distanceNote?: string;
};

export const locations: Location[] = [
  { slug: "heide", city: "Heide", district: "Dithmarschen", published: false },
  { slug: "brunsbuettel", city: "Brunsbüttel", district: "Dithmarschen", published: false },
  { slug: "itzehoe", city: "Itzehoe", district: "Steinburg", published: false },
  { slug: "rendsburg", city: "Rendsburg", district: "Rendsburg-Eckernförde", published: false },
  { slug: "neumuenster", city: "Neumünster", district: "kreisfrei", published: false },
  { slug: "kiel", city: "Kiel", district: "kreisfrei", published: false },
  { slug: "elmshorn", city: "Elmshorn", district: "Pinneberg", published: false },
  { slug: "hamburg", city: "Hamburg", district: "Hamburg", published: false },
];

export const publishedLocations = locations.filter((l) => l.published && l.intro);
