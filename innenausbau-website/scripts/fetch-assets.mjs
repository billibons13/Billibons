/**
 * Lädt alle Higgsfield-Assets aus src/content/assets.ts herunter und legt sie
 * als optimierte WebP-Dateien unter public/images/<key>.webp ab (max. 2560 px).
 * Danach in assets.ts: ASSET_SOURCE = "local".
 *
 *   npm run assets:fetch
 */
import { mkdir, readFile, writeFile } from "node:fs/promises";
import sharp from "sharp";

const src = await readFile(new URL("../src/content/assets.ts", import.meta.url), "utf8");
const cdn = src.match(/const CDN = "([^"]+)"/)[1];
const entries = [...src.matchAll(/^\s{2}(\w+): \{\s*\n\s*file: "([^"]+)"/gm)].map((m) => ({ key: m[1], file: m[2] }));
const video = src.match(/\/(hf_[\w-]+\.mp4)/)?.[1];

const out = new URL("../public/images/", import.meta.url);
await mkdir(out, { recursive: true });

for (const { key, file } of entries) {
  const res = await fetch(`${cdn}/${file}.png`);
  if (!res.ok) throw new Error(`${key}: HTTP ${res.status}`);
  const buf = Buffer.from(await res.arrayBuffer());
  const webp = await sharp(buf).resize({ width: 2560, withoutEnlargement: true }).webp({ quality: 82 }).toBuffer();
  await writeFile(new URL(`${key}.webp`, out), webp);
  console.log(`✓ ${key}.webp  ${(webp.length / 1024).toFixed(0)} KB`);
}

if (video) {
  const res = await fetch(`${cdn}/${video}`);
  if (res.ok) {
    await writeFile(new URL("hero-transformation.mp4", out), Buffer.from(await res.arrayBuffer()));
    console.log("✓ hero-transformation.mp4");
  }
}
console.log(`\nFertig: ${entries.length} Bilder. Jetzt in src/content/assets.ts ASSET_SOURCE = "local" setzen.`);
