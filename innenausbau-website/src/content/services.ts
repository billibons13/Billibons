import type { AssetKey } from "./assets";

export type ServiceGroup = "ausbau" | "oberflaechen" | "komplett";

export type Service = {
  slug: string;
  title: string;
  /** Eine Zeile für Karten */
  short: string;
  /** Einleitung auf der Detailseite */
  intro: string;
  image: AssetKey;
  group: ServiceGroup;
  benefits: string[];
  includes: string[];
  /** Typische Anlässe – hilft Kunden, sich wiederzufinden */
  occasions: string[];
  seo: { title: string; description: string };
};

export const serviceGroups: Record<ServiceGroup, string> = {
  ausbau: "Ausbau & Konstruktion",
  oberflaechen: "Oberflächen & Beläge",
  komplett: "Renovierung & Sanierung",
};

export const services: Service[] = [
  {
    slug: "trockenbau",
    title: "Trockenbau",
    short: "Wände, Decken und Vorsatzschalen – schnell, sauber und präzise gestellt.",
    intro:
      "Mit Trockenbau verändern wir Grundrisse ohne Nassbaustelle: neue Raumaufteilungen, abgehängte Decken, Installationswände oder der Ausbau des Dachgeschosses. Präzise Unterkonstruktion, saubere Fugen und eine Oberfläche, die bereit für den Maler ist.",
    image: "trockenbau",
    group: "ausbau",
    benefits: [
      "Kurze Bauzeit, kaum Trocknungszeiten",
      "Flexible Grundrisse ohne tragende Eingriffe",
      "Schall- und Brandschutz nach Anforderung planbar",
      "Leitungen verschwinden unsichtbar in der Wand",
    ],
    includes: [
      "Ständerwände mit Metall- oder Holzunterkonstruktion",
      "Abgehängte Decken und Deckenabsenkungen",
      "Vorsatzschalen und Installationswände",
      "Dachgeschossausbau inkl. Dämmung",
      "Revisionsöffnungen, Schattenfugen, Lichtvouten",
      "Verspachtelung bis Qualitätsstufe Q4",
    ],
    occasions: ["Neue Raumaufteilung", "Dachgeschossausbau", "Büroumbau", "Akustik verbessern"],
    seo: {
      title: "Trockenbau in Schleswig-Holstein",
      description:
        "Trockenbau für Wohnung, Haus und Büro in Schleswig-Holstein: Wände, Decken, Dachausbau und Vorsatzschalen – sauber geplant und präzise ausgeführt.",
    },
  },
  {
    slug: "innenputz",
    title: "Innenputz",
    short: "Gleichmäßige Wandflächen als Grundlage für jedes hochwertige Finish.",
    intro:
      "Putz ist das Fundament jeder Wand. Wir bereiten den Untergrund sorgfältig vor und bringen Kalk-, Gips- oder Kalkzementputz in der gewünschten Struktur auf – von glatt gefilzt bis dekorativ.",
    image: "putz",
    group: "oberflaechen",
    benefits: [
      "Ebenmäßige Flächen ohne Wellen und Kanten",
      "Raumklima-freundliche Materialien auf Wunsch",
      "Fachgerechte Untergrundprüfung vor Beginn",
      "Saubere Abklebung und Schutz angrenzender Bauteile",
    ],
    includes: [
      "Untergrundprüfung und -vorbereitung",
      "Gips-, Kalk- und Kalkzementputze",
      "Ausbesserung von Rissen und Fehlstellen",
      "Eckschutz- und Putzprofile",
      "Glatt-, Filz- und Strukturputz",
    ],
    occasions: ["Altbau-Wände", "Nach Leitungsarbeiten", "Neue Oberflächen", "Vorbereitung für Maler"],
    seo: {
      title: "Innenputz in Schleswig-Holstein",
      description:
        "Innenputz vom Fachbetrieb: Gips-, Kalk- und Strukturputz für Alt- und Neubau in Schleswig-Holstein. Saubere Vorbereitung, ebene Flächen.",
    },
  },
  {
    slug: "malerarbeiten",
    title: "Malerarbeiten",
    short: "Farbe mit klaren Kanten, satter Deckung und ruhiger Wirkung.",
    intro:
      "Gute Malerarbeiten erkennt man an dem, was man nicht sieht: keine Ansätze, keine Farbnasen, keine unsauberen Übergänge. Wir schützen Ihre Räume, bereiten Untergründe vor und arbeiten mit Farben, die zur Nutzung passen.",
    image: "maler",
    group: "oberflaechen",
    benefits: [
      "Vollständiger Schutz von Boden, Fenstern und Möbeln",
      "Saubere Kanten und gleichmäßige Deckung",
      "Beratung zu Farbtönen und Glanzgraden",
      "Emissionsarme Farben auf Wunsch",
    ],
    includes: [
      "Wand- und Deckenanstriche",
      "Lackierung von Türen, Zargen und Heizkörpern",
      "Tapezierarbeiten inkl. Vlies und Glattvlies",
      "Entfernen alter Tapeten und Beschichtungen",
      "Farbberatung und Musterflächen",
    ],
    occasions: ["Wohnungsübergabe", "Neuer Look", "Nach Renovierung", "Gewerbeflächen"],
    seo: {
      title: "Malerarbeiten in Schleswig-Holstein",
      description:
        "Malerarbeiten innen für Wohnung, Haus und Gewerbe in Schleswig-Holstein: Anstrich, Lackierung, Tapezieren – mit sauberem Schutz und klaren Kanten.",
    },
  },
  {
    slug: "bodenbelaege",
    title: "Bodenbeläge",
    short: "Parkett, Vinyl und Laminat – auf einem Untergrund, der wirklich passt.",
    intro:
      "Ein Boden ist nur so gut wie sein Untergrund. Deshalb prüfen wir Ebenheit und Feuchte, gleichen aus und verlegen danach Parkett, Designboden oder Laminat mit präzisen Übergängen und passenden Sockelleisten.",
    image: "boden",
    group: "oberflaechen",
    benefits: [
      "Untergrundprüfung inkl. Feuchte und Ebenheit",
      "Präzise Anschlüsse an Türen, Treppen und Wände",
      "Beratung zu Material, Nutzung und Fußbodenheizung",
      "Fachgerechte Entsorgung alter Beläge",
    ],
    includes: [
      "Entfernen alter Beläge",
      "Spachtel- und Ausgleichsarbeiten",
      "Parkett (geklebt oder schwimmend)",
      "Vinyl- und Designböden, Laminat",
      "Sockelleisten, Übergangs- und Abschlussprofile",
    ],
    occasions: ["Neubezug", "Abgenutzter Boden", "Fußbodenheizung", "Vermietung"],
    seo: {
      title: "Bodenbeläge verlegen in Schleswig-Holstein",
      description:
        "Parkett, Vinyl und Laminat fachgerecht verlegen lassen – inkl. Untergrundvorbereitung und Sockelleisten. Für Wohnung, Haus und Büro in Schleswig-Holstein.",
    },
  },
  {
    slug: "fliesenarbeiten",
    title: "Fliesenarbeiten",
    short: "Großformate, exakte Fugenbilder und dichte Anschlüsse.",
    intro:
      "Fliesen verzeihen keine Ungenauigkeit. Wir planen Fugenbild und Anschnitte vorab, dichten Nassbereiche normgerecht ab und verlegen auch großformatige Fliesen plan und fluchtgerecht.",
    image: "fliesen",
    group: "oberflaechen",
    benefits: [
      "Fugenbild wird vor Verlegebeginn geplant",
      "Verbundabdichtung in Nassbereichen",
      "Großformat-Verlegung mit Nivelliersystem",
      "Gehrungen und Schienen sauber ausgeführt",
    ],
    includes: [
      "Wand- und Bodenfliesen",
      "Großformatige Feinsteinzeugplatten",
      "Abdichtung von Dusche und Bad",
      "Bodengleiche Duschen mit Rinne oder Punktablauf",
      "Silikon- und Wartungsfugen",
    ],
    occasions: ["Badsanierung", "Küchenspiegel", "Flur und Eingang", "Gewerbeflächen"],
    seo: {
      title: "Fliesenarbeiten in Schleswig-Holstein",
      description:
        "Fliesenleger-Arbeiten für Bad, Küche und Wohnräume in Schleswig-Holstein: Großformate, Abdichtung, bodengleiche Duschen – exakt verlegt.",
    },
  },
  {
    slug: "renovierung",
    title: "Renovierung",
    short: "Frische Räume mit Bestand: gezielte Arbeiten statt Komplettabriss.",
    intro:
      "Nicht jeder Raum braucht einen Neuanfang. Bei einer Renovierung erneuern wir gezielt Oberflächen, Böden, Türen und Details – so wirken Räume wieder zeitgemäß, ohne dass die Substanz angetastet werden muss.",
    image: "wohnenNachher",
    group: "komplett",
    benefits: [
      "Klarer Umfang, klares Budget",
      "Kurze Ausführungszeiten, auch im bewohnten Zustand",
      "Alle Gewerke aus einer Hand koordiniert",
      "Ideal vor Vermietung oder Verkauf",
    ],
    includes: [
      "Wände und Decken spachteln und streichen",
      "Neue Bodenbeläge",
      "Türen, Zargen und Leisten erneuern",
      "Kleinere Trockenbauarbeiten",
      "Endreinigung nach Abschluss",
    ],
    occasions: ["Mieterwechsel", "Nach dem Kauf", "Vor dem Verkauf", "Neue Lebensphase"],
    seo: {
      title: "Renovierung in Schleswig-Holstein",
      description:
        "Renovierung von Wohnung, Haus und Büro in Schleswig-Holstein: Wände, Böden, Türen – koordiniert aus einer Hand, sauber und termingerecht.",
    },
  },
  {
    slug: "sanierung",
    title: "Sanierung",
    short: "Substanz erhalten, Schäden beheben, Räume zukunftsfähig machen.",
    intro:
      "Bei einer Sanierung geht es um mehr als die Oberfläche. Wir prüfen den Bestand, beheben Schäden fachgerecht und bauen Räume so auf, dass sie technisch und gestalterisch wieder auf der Höhe der Zeit sind.",
    image: "sanierung",
    group: "komplett",
    benefits: [
      "Bestandsaufnahme vor Angebotserstellung",
      "Transparente Dokumentation verdeckter Mängel",
      "Koordination mit Elektro- und Sanitär-Fachbetrieben",
      "Planbare Bauabschnitte",
    ],
    includes: [
      "Rückbau und Entsorgung",
      "Untergrund- und Wandsanierung",
      "Erneuerung von Decken, Wänden und Böden",
      "Koordination der Haustechnik-Gewerke",
      "Fotodokumentation des Baufortschritts",
    ],
    occasions: ["Altbau", "Erbschaft", "Immobilienkauf", "Wasserschaden (nach Trocknung)"],
    seo: {
      title: "Sanierung in Schleswig-Holstein",
      description:
        "Innensanierung von Altbau, Haus und Wohnung in Schleswig-Holstein: Bestandsaufnahme, Rückbau, Wände, Decken, Böden – planbar und dokumentiert.",
    },
  },
  {
    slug: "badsanierung",
    title: "Badsanierung",
    short: "Vom gefliesten 80er-Bad zum ruhigen, pflegeleichten Raum.",
    intro:
      "Ein Bad wird täglich genutzt – deshalb muss es funktionieren und lange halten. Wir planen Ihr neues Bad mit Ihnen, koordinieren Sanitär und Elektro und setzen alles in einem klar strukturierten Ablauf um.",
    image: "badNachher",
    group: "komplett",
    benefits: [
      "Ein Ansprechpartner für alle Gewerke",
      "Bodengleiche Duschen und barrierearme Lösungen",
      "Fester Zeitplan mit Bauabschnitten",
      "Normgerechte Abdichtung",
    ],
    includes: [
      "Planung und Materialauswahl",
      "Rückbau des alten Bades",
      "Vorwandinstallation und Trockenbau",
      "Abdichtung, Fliesen und Spachteltechnik",
      "Montage in Abstimmung mit dem Sanitärbetrieb",
    ],
    occasions: ["Veraltetes Bad", "Barrierefreiheit", "Wanne zu Dusche", "Gäste-WC"],
    seo: {
      title: "Badsanierung in Schleswig-Holstein",
      description:
        "Badsanierung aus einer Hand in Schleswig-Holstein: Planung, Rückbau, Abdichtung, Fliesen und bodengleiche Dusche – mit festem Ansprechpartner.",
    },
  },
  {
    slug: "kuechenrenovierung",
    title: "Küchenrenovierung",
    short: "Wände, Böden und Anschlüsse vorbereitet – bereit für Ihre neue Küche.",
    intro:
      "Bevor eine neue Küche eingebaut wird, muss der Raum stimmen. Wir übernehmen Rückbau, Wände, Fliesenspiegel, Boden und die Abstimmung mit Elektro und Sanitär – damit der Küchenbauer auf einen perfekt vorbereiteten Raum trifft.",
    image: "kuecheNachher",
    group: "komplett",
    benefits: [
      "Raum exakt nach Küchenplanung vorbereitet",
      "Abstimmung mit Küchenstudio und Haustechnik",
      "Robuste, pflegeleichte Oberflächen",
      "Kurze Ausfallzeit der Küche",
    ],
    includes: [
      "Demontage und Entsorgung der Altküche",
      "Wände spachteln, Fliesenspiegel oder Glasrückwand vorbereiten",
      "Neuer Bodenbelag",
      "Deckenlösungen und Beleuchtungsvorbereitung",
      "Koordination der Anschlüsse",
    ],
    occasions: ["Neue Küche", "Offene Wohnküche", "Wand öffnen (nach Statikprüfung)", "Altbau-Küche"],
    seo: {
      title: "Küchenrenovierung in Schleswig-Holstein",
      description:
        "Küchenrenovierung in Schleswig-Holstein: Rückbau, Wände, Boden und Vorbereitung für die neue Küche – koordiniert mit Küchenstudio und Haustechnik.",
    },
  },
  {
    slug: "innenausbau",
    title: "Innenausbau",
    short: "Vom Rohbau oder Bestand zum fertigen, bezugsfertigen Raum.",
    intro:
      "Innenausbau verbindet viele Gewerke: Trockenbau, Putz, Spachtel, Boden, Fliesen und Maler. Wir koordinieren alles in der richtigen Reihenfolge, damit aus einer Fläche ein fertiger Raum wird – ohne Schnittstellenprobleme.",
    image: "hero",
    group: "ausbau",
    benefits: [
      "Alle Ausbaugewerke in einer Hand",
      "Abgestimmte Reihenfolge ohne Leerlauf",
      "Ein Zeitplan, ein Ansprechpartner",
      "Für Wohnen und Gewerbe",
    ],
    includes: [
      "Planung der Ausbaureihenfolge",
      "Trockenbau, Putz und Spachtel",
      "Boden- und Fliesenarbeiten",
      "Maler- und Lackierarbeiten",
      "Endreinigung und Abnahme",
    ],
    occasions: ["Dachgeschoss", "Souterrain", "Gewerbeeinheit", "Anbau"],
    seo: {
      title: "Innenausbau in Schleswig-Holstein",
      description:
        "Innenausbau aus einer Hand in Schleswig-Holstein: Trockenbau, Putz, Boden, Fliesen und Maler für Wohnungen, Häuser, Büros und Gewerbe.",
    },
  },
  {
    slug: "spachtelarbeiten",
    title: "Spachtelarbeiten",
    short: "Q1 bis Q4: die Oberfläche, die zu Licht und Anspruch passt.",
    intro:
      "Streiflicht zeigt jede Unebenheit. Wir spachteln Wände und Decken in der Qualitätsstufe, die zur Nutzung und Beleuchtung passt – bis hin zur vollflächigen Q4-Oberfläche für glatte, edle Wände.",
    image: "decke",
    group: "oberflaechen",
    benefits: [
      "Qualitätsstufe wird vorab gemeinsam festgelegt",
      "Geeignet für Streiflicht und große Fensterflächen",
      "Perfekte Basis für matte Farben",
      "Staubarmes Schleifen",
    ],
    includes: [
      "Fugen- und Flächenspachtelung",
      "Qualitätsstufen Q1 bis Q4",
      "Kanten- und Eckausbildung",
      "Schleifen und Grundieren",
    ],
    occasions: ["Trockenbauflächen", "Glatte Wände gewünscht", "Altbau-Wände", "Große Fenster"],
    seo: {
      title: "Spachtelarbeiten Q1–Q4 in Schleswig-Holstein",
      description:
        "Spachtelarbeiten in Q1 bis Q4 für Wände und Decken in Schleswig-Holstein – glatte Oberflächen, auch bei Streiflicht.",
    },
  },
  {
    slug: "decken-und-waende",
    title: "Decken & Wände",
    short: "Abgehängte Decken, Schattenfugen, Lichtvouten und glatte Wände.",
    intro:
      "Decken und Wände bestimmen die Wirkung eines Raums. Mit Deckenabhängungen, integrierter Beleuchtung, Schattenfugen und sauberen Wandoberflächen schaffen wir Ruhe und Struktur.",
    image: "decke",
    group: "ausbau",
    benefits: [
      "Integrierte Beleuchtung sauber vorbereitet",
      "Moderne Details wie Schattenfugen",
      "Verbesserte Akustik möglich",
      "Leitungen unsichtbar geführt",
    ],
    includes: [
      "Abgehängte und abgesenkte Decken",
      "Lichtvouten und Einbauleuchten-Ausschnitte",
      "Schattenfugen und Akustikdecken",
      "Wandbekleidungen und Vorsatzschalen",
      "Spachtel und Anstrich",
    ],
    occasions: ["Neue Beleuchtung", "Unebene Altbaudecke", "Akustik im Büro", "Moderner Look"],
    seo: {
      title: "Decken & Wände – Innenausbau in Schleswig-Holstein",
      description:
        "Abgehängte Decken, Lichtvouten, Schattenfugen und glatte Wände in Schleswig-Holstein – präziser Innenausbau für Wohnen und Gewerbe.",
    },
  },
  {
    slug: "komplettrenovierung",
    title: "Komplettrenovierung",
    short: "Eine Immobilie, ein Plan, ein Ansprechpartner – bis zur Schlüsselübergabe.",
    intro:
      "Bei einer Komplettrenovierung übernehmen wir die gesamte Innenrenovierung Ihrer Wohnung oder Ihres Hauses. Sie haben einen Ansprechpartner, einen Zeitplan und ein Angebot – wir koordinieren alles Weitere.",
    image: "komplett",
    group: "komplett",
    benefits: [
      "Ein Angebot für alle Leistungen",
      "Fester Ansprechpartner während des gesamten Projekts",
      "Regelmäßige Updates mit Fotos",
      "Strukturierte Abnahme mit Protokoll",
    ],
    includes: [
      "Bestandsaufnahme und Planung",
      "Rückbau und Entsorgung",
      "Alle Ausbaugewerke",
      "Koordination von Elektro und Sanitär",
      "Endreinigung und Übergabe",
    ],
    occasions: ["Immobilienkauf", "Erbschaft", "Leerstand", "Vermietung vorbereiten"],
    seo: {
      title: "Komplettrenovierung in Schleswig-Holstein",
      description:
        "Komplettrenovierung von Wohnung und Haus in Schleswig-Holstein: Planung, Rückbau, alle Ausbaugewerke und Übergabe – aus einer Hand.",
    },
  },
];

export const getService = (slug: string) => services.find((s) => s.slug === slug);

/** Auswahl für die Startseite (Reihenfolge = Priorität) */
export const featuredServiceSlugs = [
  "komplettrenovierung",
  "badsanierung",
  "trockenbau",
  "malerarbeiten",
  "bodenbelaege",
  "kuechenrenovierung",
];
