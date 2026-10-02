/**
 * Zentrale Firmendaten.
 *
 * WICHTIG: Alles in [eckigen Klammern] ist ein Platzhalter und muss vor dem
 * Livegang durch echte Angaben ersetzt werden. Es werden bewusst keine Zahlen,
 * Zertifikate oder Jahre erfunden – Felder, die leer bleiben, werden auf der
 * Website und im strukturierten Schema automatisch ausgeblendet.
 */
export const site = {
  /** Arbeitstitel – durch den echten Firmennamen ersetzen */
  name: "NORDRAUM",
  legalName: "[Firmenname GmbH]",
  tagline: "Innenausbau & Renovierung",
  claim: "Wir verwandeln Räume.",
  url: (process.env.NEXT_PUBLIC_SITE_URL ?? "http://localhost:3000").replace(/\/$/, ""),
  locale: "de_DE",

  contact: {
    /** Anzeigeformat */
    phone: "[+49 000 000 00 00]",
    /** E.164 ohne Leerzeichen – für tel: und WhatsApp. Leer = Button ausblenden */
    phoneE164: "+490000000000",
    whatsappE164: "490000000000",
    email: "[info@firma.de]",
    whatsappText: "Hallo, ich interessiere mich für eine Renovierung und hätte gern eine Beratung.",
  },

  address: {
    street: "[Straße Hausnummer]",
    postalCode: "[PLZ]",
    city: "[Ort]",
    region: "Schleswig-Holstein",
    country: "DE",
    /** Optional für Schema/Karte */
    geo: null as null | { lat: number; lng: number },
  },

  serviceArea: {
    label: "Schleswig-Holstein & Hamburg",
    regions: ["Dithmarschen", "Steinburg", "Rendsburg-Eckernförde", "Pinneberg", "Hamburg"],
  },

  openingHours: [
    // Format laut schema.org; leer lassen, wenn unbekannt
    // { days: ["Mo", "Tu", "We", "Th", "Fr"], opens: "07:30", closes: "17:00" },
  ] as { days: string[]; opens: string; closes: string }[],

  /** Nur echte Angaben eintragen – null blendet Elemente aus */
  facts: {
    foundedYear: null as number | null,
    completedProjects: null as number | null,
    teamSize: null as number | null,
    certifications: [] as string[],
    memberships: [] as string[], // z. B. "Handwerkskammer Lübeck" – nur wenn zutreffend
  },

  social: {
    instagram: "",
    facebook: "",
    linkedin: "",
    googleBusiness: "",
  },

  /**
   * Solange Projektbilder KI-Visualisierungen sind, wird das sichtbar gekennzeichnet.
   * Erst auf false setzen, wenn ausschließlich echte Projektfotos verwendet werden.
   */
  labelVisualizations: true,
} as const;

export const telHref = `tel:${site.contact.phoneE164}`;
export const mailHref = `mailto:${site.contact.email}`;
export const whatsappHref = `https://wa.me/${site.contact.whatsappE164}?text=${encodeURIComponent(site.contact.whatsappText)}`;

export const isPlaceholder = (value: string) => /^\[.*\]$/.test(value.trim());
