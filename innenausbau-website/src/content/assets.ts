/**
 * Zentrales Bild-/Video-Manifest.
 *
 * Alle Visuals wurden mit Higgsfield erzeugt (Prompts: docs/05-higgsfield-asset-plan.md)
 * und liegen vorerst auf dem Higgsfield-CDN. `npm run assets:fetch` lädt sie nach
 * /public/images herunter; danach `ASSET_BASE` auf "/images" umstellen.
 *
 * Echte Projektfotos ersetzen diese Einträge 1:1 (gleicher Key, neues `src`,
 * `kind: "photo"`). KI-Visualisierungen werden auf der Website gekennzeichnet.
 */
const CDN = "https://d8j0ntlcm91z4.cloudfront.net/user_3HTV2MBYBXlPAv5lY0z9PJuFl4p";

/** "cdn" = Higgsfield-CDN, "local" = /public/images (nach assets:fetch) */
const ASSET_SOURCE: "cdn" | "local" = "cdn";

type AssetDef = {
  file: string;
  width: number;
  height: number;
  alt: string;
  kind: "visualization" | "photo";
};

const defs = {
  hero: {
    file: "hf_20261002_224452_166ce3b5-1150-4f8c-8f1c-9d158f8107f8",
    width: 2688,
    height: 1520,
    alt: "Renovierter Wohnbereich mit glatten weißen Wänden, Eichenparkett und großem Fenster",
    kind: "visualization",
  },
  badVorher: {
    file: "hf_20261002_224249_81c27087-0eda-44ec-9a39-167f0768e2be",
    width: 1168,
    height: 880,
    alt: "Badezimmer vor der Sanierung mit beige-braunen Fliesen der 80er-Jahre und Badewanne",
    kind: "visualization",
  },
  badNachher: {
    file: "hf_20261002_224452_463f8455-3434-4d29-8826-cf15d52c433c",
    width: 2336,
    height: 1744,
    alt: "Dasselbe Badezimmer nach der Sanierung mit großformatigen grauen Fliesen und bodengleicher Dusche",
    kind: "visualization",
  },
  wohnenVorher: {
    file: "hf_20261002_224250_73df04d7-ed5f-4af4-bd91-ec14ff148052",
    width: 1168,
    height: 880,
    alt: "Wohnzimmer vor der Renovierung mit abgerissener Raufaser, offenen Kabeln und altem Boden",
    kind: "visualization",
  },
  wohnenNachher: {
    file: "hf_20261002_224454_fccbffa0-acd7-4756-97da-2647e5ac5672",
    width: 2336,
    height: 1744,
    alt: "Dasselbe Wohnzimmer nach der Renovierung mit glatten Wänden und Fischgrätparkett",
    kind: "visualization",
  },
  kuecheVorher: {
    file: "hf_20261002_224452_706f2fa4-5a1b-4f9b-93aa-a1c8b86d1916",
    width: 2336,
    height: 1744,
    alt: "Küche der 70er-Jahre vor der Renovierung mit dunklen Holzfronten und orangefarbenen Fliesen",
    kind: "visualization",
  },
  kuecheNachher: {
    file: "hf_20261002_224609_5124a3f9-9676-494d-bf53-bf0e34e09320",
    width: 2336,
    height: 1744,
    alt: "Dieselbe Küche nach der Renovierung mit anthrazitfarbenen grifflosen Fronten und hellen Wänden",
    kind: "visualization",
  },
  kueche: {
    file: "hf_20261002_224610_d7584ed5-46e6-4a46-9bc3-419cf7c78396",
    width: 2688,
    height: 1520,
    alt: "Renovierte Küche mit anthrazitfarbenen Fronten, Eichenregal und großformatigen Bodenfliesen",
    kind: "visualization",
  },
  komplett: {
    file: "hf_20261002_224608_06b5c3c1-210c-449d-a99c-6e0c66ab14ab",
    width: 2688,
    height: 1520,
    alt: "Komplett renoviertes Stadthaus: Blick aus dem Flur in den Wohn- und Essbereich mit Eichentreppe",
    kind: "visualization",
  },
  bad: {
    file: "hf_20261002_224608_0d5c6702-5282-4136-99e5-51987ac366fa",
    width: 1792,
    height: 2240,
    alt: "Modernes Bad mit Walk-in-Dusche, schwarzer Regenbrause und Waschtisch aus Eiche",
    kind: "visualization",
  },
  team: {
    file: "hf_20261002_224650_6676f191-c9b6-4b1b-8418-1a10e2156e5a",
    width: 2048,
    height: 1360,
    alt: "Zwei Handwerker besprechen einen Grundriss auf dem Tablet in einem Raum während der Renovierung",
    kind: "visualization",
  },
  fliesen: {
    file: "hf_20261002_224650_de57e30a-e2a4-4d37-bfed-b3e52f95dff1",
    width: 1792,
    height: 2240,
    alt: "Detailaufnahme: exakte Fuge und Gehrung an großformatigen grauen Fliesen",
    kind: "visualization",
  },
  decke: {
    file: "hf_20261002_224651_0682c355-c997-4ec9-88db-4b0e6ba6e8e6",
    width: 1792,
    height: 2240,
    alt: "Detailaufnahme: Schattenfuge zwischen Trockenbaudecke und Wand mit Einbauleuchte",
    kind: "visualization",
  },
  material: {
    file: "hf_20261002_224650_0d3eba2d-e717-46aa-929d-12a64ce31a0d",
    width: 1792,
    height: 2240,
    alt: "Materialmuster auf Betontisch: Eichendiele, graue Fliese, Putzprobe und Farbkarten",
    kind: "visualization",
  },
  maler: {
    file: "hf_20261002_224824_c3c3ddc3-836d-49bb-91a6-ddc62016da21",
    width: 2048,
    height: 1360,
    alt: "Maler streicht eine Wand mit der Rolle, Fensterrahmen sauber abgeklebt",
    kind: "visualization",
  },
  putz: {
    file: "hf_20261002_224825_83592425-7146-440c-8f13-f798f5d1ea84",
    width: 2048,
    height: 1360,
    alt: "Handwerker glättet frischen Gipsputz mit der Glättkelle",
    kind: "visualization",
  },
  trockenbau: {
    file: "hf_20261002_224824_e13a0d5f-cefd-4ab1-9d62-f8ea461c4c4c",
    width: 2048,
    height: 1360,
    alt: "Trockenbau im Dachgeschoss: Metallständerwerk, Gipskartonplatten und Dämmung",
    kind: "visualization",
  },
  boden: {
    file: "hf_20261002_224826_a673756e-2f5d-4ea9-996e-f513155e363e",
    width: 2048,
    height: 1360,
    alt: "Detailaufnahme: Fischgrätparkett aus heller Eiche mit weißer Sockelleiste",
    kind: "visualization",
  },
  sanierung: {
    file: "hf_20261002_224825_66d85d1f-c065-485a-8926-c1aaad6e1a7b",
    width: 2048,
    height: 1360,
    alt: "Altbausanierung: Wand bis aufs Mauerwerk freigelegt, Nachbarwand frisch verputzt",
    kind: "visualization",
  },
} satisfies Record<string, AssetDef>;

export type AssetKey = keyof typeof defs;

export type Asset = AssetDef & { src: string; key: AssetKey };

export function asset(key: AssetKey): Asset {
  const d: AssetDef = defs[key];
  const src = ASSET_SOURCE === "cdn" ? `${CDN}/${d.file}.png` : `/images/${key}.webp`;
  return { ...d, key, src };
}

export const assetKeys = Object.keys(defs) as AssetKey[];
export const assetFiles = assetKeys.map((key) => ({ key, url: `${CDN}/${defs[key].file}.png` }));

export const heroVideo = {
  src:
    ASSET_SOURCE === "cdn"
      ? `${CDN}/hf_20261002_224631_f11593a9-8462-43f2-9fe1-9562bcd8042e.mp4`
      : "/images/hero-transformation.mp4",
  poster: "wohnenNachher" as AssetKey,
  remote: `${CDN}/hf_20261002_224631_f11593a9-8462-43f2-9fe1-9562bcd8042e.mp4`,
};
