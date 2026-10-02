import type { AssetKey } from "./assets";

export type Project = {
  slug: string;
  title: string;
  location: string;
  services: string[];
  /** Freitext, z. B. "4 Wochen" – nur echte Angaben */
  duration: string;
  objectType: "Wohnung" | "Haus" | "Büro" | "Gewerbe";
  summary: string;
  challenge: string;
  solution: string;
  before: AssetKey;
  after: AssetKey;
  gallery: AssetKey[];
  /**
   * true = Beispielprojekt mit KI-Visualisierung. Wird auf der Website
   * sichtbar gekennzeichnet und muss durch ein echtes Referenzprojekt
   * ersetzt werden (siehe docs/03-components-content.md).
   */
  isExample: boolean;
};

export const projects: Project[] = [
  {
    slug: "badsanierung-einfamilienhaus",
    title: "Badsanierung im Einfamilienhaus",
    location: "[Ort], Schleswig-Holstein",
    services: ["Badsanierung", "Fliesenarbeiten", "Trockenbau"],
    duration: "[Dauer]",
    objectType: "Haus",
    summary:
      "Aus einem Bad der 80er-Jahre wurde ein ruhiger, pflegeleichter Raum mit bodengleicher Dusche und großformatigen Fliesen.",
    challenge:
      "Kleine Grundfläche, eine Badewanne, die kaum noch genutzt wurde, und Fliesen, deren Fugen nicht mehr dicht waren.",
    solution:
      "Rückbau bis auf den Rohbau, Vorwandinstallation in Trockenbau, Verbundabdichtung und großformatige Feinsteinzeugfliesen. Die Wanne wich einer bodengleichen Dusche.",
    before: "badVorher",
    after: "badNachher",
    gallery: ["badNachher", "bad", "fliesen"],
    isExample: true,
  },
  {
    slug: "wohnungsrenovierung-altbau",
    title: "Renovierung einer Altbauwohnung",
    location: "[Ort], Schleswig-Holstein",
    services: ["Renovierung", "Spachtelarbeiten", "Bodenbeläge", "Malerarbeiten"],
    duration: "[Dauer]",
    objectType: "Wohnung",
    summary:
      "Raufaser, Risse und ein abgenutzter Boden – heute glatte Wände in Q4, Fischgrätparkett und eine ruhige Lichtplanung.",
    challenge:
      "Unebene Altbauwände, offene Leitungen und ein Boden, der nicht mehr zu retten war.",
    solution:
      "Tapeten entfernt, Wände vollflächig gespachtelt, Leitungen unter Putz gelegt, Fischgrätparkett verlegt und Decken mit Einbauleuchten neu aufgebaut.",
    before: "wohnenVorher",
    after: "wohnenNachher",
    gallery: ["wohnenNachher", "boden", "decke"],
    isExample: true,
  },
  {
    slug: "kuechenrenovierung-reihenhaus",
    title: "Küchenrenovierung im Reihenhaus",
    location: "[Ort], Schleswig-Holstein",
    services: ["Küchenrenovierung", "Bodenbeläge", "Malerarbeiten"],
    duration: "[Dauer]",
    objectType: "Haus",
    summary:
      "Die Küche aus den 70ern wurde zurückgebaut und der Raum für eine moderne, grifflose Küche vorbereitet.",
    challenge:
      "Alte Fliesenspiegel, ein PVC-Boden auf unebenem Estrich und Anschlüsse an den falschen Stellen.",
    solution:
      "Komplettrückbau, Wände neu verputzt, Estrich ausgeglichen, großformatige Bodenfliesen verlegt und Anschlüsse in Abstimmung mit der Küchenplanung neu positioniert.",
    before: "kuecheVorher",
    after: "kuecheNachher",
    gallery: ["kuecheNachher", "kueche", "material"],
    isExample: true,
  },
];

export const getProject = (slug: string) => projects.find((p) => p.slug === slug);
