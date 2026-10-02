# 05 · HIGGSFIELD ASSET PLAN

## Визуальные правила (добавлять к любому промпту)

> German premium architecture photography, natural daylight, realistic materials with subtle imperfections, straight verticals (tilt-shift look), calm palette of off-white, anthracite, concrete grey and warm oak, believable mid-to-high quality German home — **not** a luxury hotel, no people or only hands/backs, no text, no distorted architecture, photorealistic.

**Модели:** изображения — `gpt_image_2_5` (quality `high`, resolution `2k`); видео — `seedance_2_5` (720p, без аудио).
**Пары Before/After:** сначала генерируется «Vorher», затем «Nachher» как **редактирование с референсом** (`image_references` = job «Vorher») с жёстким требованием «identical camera position, lens, perspective, window position» → кадры совпадают для слайдера.

Статус ✅ = сгенерировано в этой сессии и подключено в `src/content/assets.ts` (ключ в скобках). Все ассеты — визуализации и на сайте помечены «Visualisierung».

---

### 1. Hero image / video ✅ (`hero`, видео `hero-transformation`)
**Image:**
```
Architectural interior photograph of a freshly renovated open-plan living area in a 1930s northern German brick house, smooth white plastered walls, light oak engineered parquet floor, large steel-framed window with soft overcast North Sea daylight, recessed ceiling with shadow gap, minimal furniture, a single linen sofa, concrete-grey accent wall, no people. Shot on full-frame camera, 24mm tilt-shift lens, straight verticals, natural light, realistic materials and subtle imperfections, calm muted palette of off-white, anthracite and warm oak, editorial architecture magazine style, photorealistic, not luxury, believable German home. Leave calm negative space on the left third for headline text.
```
**Video (start = `wohnenVorher`, end = `wohnenNachher`, 6 s, 16:9):**
```
Locked-off tripod shot of an empty apartment room under renovation transforming into the finished renovated room. Very slow, subtle forward dolly. The torn wallpaper, ladder and dust sheets dissolve away gently as smooth plastered walls, oak herringbone parquet and furniture appear naturally, like a calm time-lapse. Soft natural daylight from the window stays constant. Straight verticals, no camera shake, no people, no morphing of the window or walls, photorealistic architectural film look.
```

### 2. Renovation transformation ✅ (`wohnenVorher` → `wohnenNachher`)
**Vorher:**
```
Realistic documentary photograph of an empty living room in an older German apartment before renovation: torn woodchip wallpaper, cracked plaster, old worn laminate floor partly removed, exposed cables, ladder and dust sheets, large window with daylight, straight verticals, 24mm lens, eye level, photorealistic, no people.
```
**Nachher (с референсом «Vorher»):**
```
Show this exact room after a complete professional renovation. Keep the identical camera position, lens, perspective, room geometry, window and door positions. Perfectly smooth plastered walls painted warm off-white, light oak herringbone parquet, new white skirting boards, smooth ceiling with recessed spots, all tools, ladder and dust sheets removed, cables hidden, minimal furniture: a grey sofa and an oak sideboard, soft natural daylight. Photorealistic architectural photograph, straight verticals, believable German apartment, not luxury, no people.
```

### 3. Modern bathroom ✅ (`bad`)
```
Architectural interior photograph of a modern renovated bathroom in a German family house: grey large format wall tiles, walk-in shower with matte black rain shower, floating oak vanity with white basin, round mirror, soft side daylight from window, clean grout lines, straight verticals, 35mm lens, realistic materials, calm palette, photorealistic, no people, no luxury hotel look.
```

### 4. Modern kitchen ✅ (`kueche`)
```
Architectural interior photograph of a newly renovated kitchen in a northern German house: matte anthracite handleless cabinets, light oak open shelf, quartz worktop, white smooth plastered walls, large format concrete-grey floor tiles, pendant lights, window with soft overcast daylight, straight verticals, 28mm lens, realistic, believable mid-to-high quality, photorealistic, no people.
```

### 5. Living room renovation ✅ (`wohnenNachher`, см. п. 2)

### 6. Flooring ✅ (`boden`)
```
Close-up architectural detail photograph of freshly laid light oak herringbone parquet meeting a white skirting board in a renovated German apartment, precise joints, low raking natural daylight emphasizing wood grain, clean finish, 50mm lens, shallow depth of field, photorealistic, no people.
```

### 7. Painting ✅ (`maler`)
```
Documentary photograph of interior painting in progress in a German apartment: a painter's hands holding a roller applying warm off-white paint to a smooth wall, masking tape cleanly along a white window frame, floor covered with grey protective fleece, natural daylight, realistic, face not visible, 35mm lens, photorealistic, authentic anthracite workwear, natural hand anatomy.
```

### 8. Drywall / Trockenbau ✅ (`trockenbau`)
```
Documentary photograph of drywall installation in a German attic conversion: galvanized metal stud framework, several gypsum boards already mounted with neat screw lines, mineral wool insulation between rafters, red laser level line on the wall, tidy construction site, natural light from a roof window, 24mm lens, photorealistic, no people.
```

### 9. Plastering ✅ (`putz`)
```
Close-up documentary photograph of a craftsman smoothing fresh white gypsum plaster on an interior wall with a stainless steel trowel, raking side light revealing the even surface, only hands and forearms visible, realistic texture, 50mm lens, photorealistic, authentic anthracite work clothes, natural hand anatomy.
```

### 10. Complete interior renovation ✅ (`komplett`)
```
Architectural interior photograph of a completely renovated older German townhouse interior, view from hallway into living and dining area: smooth white walls, new interior doors in matte white, oak floor throughout, new staircase with oak treads, recessed lighting, natural daylight, minimal furniture, straight verticals, 20mm tilt-shift lens, photorealistic, believable, no people.
```
**Sanierung (доп.) ✅ (`sanierung`):**
```
Documentary photograph of an old German brick house interior during renovation (Sanierung): old plaster removed down to the brick on one wall, the adjacent wall freshly re-plastered and smooth, new electrical conduits neatly routed, swept floor with protective board, buckets and a mixing paddle in one corner, natural daylight from window, straight verticals, 24mm lens, photorealistic, tidy professional site, no people.
```

### 11. Before/After visuals ✅
**Bad — Vorher (`badVorher`):**
```
Realistic documentary photograph of a dated German bathroom before renovation: 1980s beige and brown patterned wall tiles, worn grout, old white bathtub with chrome mixer, small window, fluorescent ceiling light, slightly cluttered, real house in Schleswig-Holstein, straight verticals, 24mm lens, eye-level, natural flat daylight, photorealistic, no people.
```
**Bad — Nachher (`badNachher`, референс = Vorher):**
```
Show this exact bathroom after a professional renovation. Keep the identical camera position, lens, perspective, room geometry, window position and size. Replace everything inside: large-format warm grey stone-look porcelain tiles on floor and walls, walk-in shower with frameless glass and floor-level drain where the bathtub was, wall-hung white WC, matte black fittings, oak vanity with white basin, wall niche with soft LED strip, smooth white plastered ceiling with recessed spots, soft natural daylight. Photorealistic architectural photograph, straight verticals, believable mid-range German renovation, no people.
```
**Küche — Vorher (`kuecheVorher`):**
```
Realistic documentary photograph of an outdated German kitchen before renovation in a 1970s house: dark brown wooden kitchen units, orange-beige wall tiles, worn PVC floor, old extractor hood, fluorescent ceiling light, window with daylight, slightly cluttered, straight verticals, 24mm lens, eye-level, photorealistic, no people.
```
**Küche — Nachher (`kuecheNachher`, референс = Vorher):**
```
Show this exact kitchen after a professional renovation. Keep the identical camera position, lens, perspective, room geometry and window position. New matte anthracite handleless kitchen units, light oak open shelf, light quartz worktop, smooth white plastered walls instead of old tiles, large-format concrete-grey floor tiles, simple pendant lights, recessed ceiling spots, soft natural daylight, tidy and empty worktops. Photorealistic architectural photograph, straight verticals, believable German family home, not luxury, no people.
```

### 12. Team / work process ✅ (`team`)
```
Documentary photograph of two craftsmen in plain anthracite workwear discussing a floor plan on a tablet inside a room under renovation in a German house, seen from behind and side, faces turned away and not in focus, laser measuring device on a trestle, natural window light, tidy site with protective floor covering, 35mm lens, authentic, photorealistic, not staged stock look, natural anatomy.
```
> ⚠️ Для «Über uns» и команды **настоятельно рекомендуется реальная фотосессия** — AI-люди подрывают доверие. Визуализация — только временная.

### 13. Detail shots of craftsmanship ✅ (`fliesen`, `decke`, `material`)
```
Macro architectural detail photograph of precise tile work: large format grey porcelain tiles with a perfectly straight 2mm grout line meeting a mitred tile corner edge, matte black shower fitting in soft focus, natural side light, realistic texture, 85mm lens, photorealistic.
```
```
Architectural detail photograph of a ceiling with a clean shadow gap where a smooth drywall ceiling meets a white plastered wall, one recessed LED downlight, natural daylight, minimalist, precise edges, 35mm lens looking upward at an angle, photorealistic.
```
```
Still life photograph of interior renovation material samples on a raw concrete table: an oak parquet plank, a grey porcelain tile, a white plaster sample board, paint colour cards in off-white, warm grey and anthracite, a yellow folding ruler, natural window light from the left, editorial architecture studio style, photorealistic.
```

---

## Видео для Project-секций (не сгенерированы — по ~35–45 кредитов каждое)

Модель `seedance_2_5`, `mode: omni_reference`, `start_image` = Vorher, `end_image` = Nachher, 6 s, 720p, `generate_audio: false`.

| Asset | start → end | Prompt |
|---|---|---|
| `bad-transformation.mp4` | `badVorher` → `badNachher` | `Locked-off tripod shot of a dated bathroom transforming into the renovated bathroom. Old patterned tiles and bathtub fade away as large-format grey tiles, a walk-in shower and oak vanity appear naturally, calm time-lapse feel, constant soft daylight from the small window, no camera shake, no people, no morphing of walls or window, photorealistic.` |
| `kueche-transformation.mp4` | `kuecheVorher` → `kuecheNachher` | `Locked-off tripod shot of a 1970s kitchen transforming into a modern anthracite kitchen. Old units and orange tiles dissolve, new handleless cabinets, smooth white walls and grey floor tiles appear, calm time-lapse, constant daylight, very slow push-in, no people, photorealistic.` |
| `detail-loop.mp4` | `boden` | `Very slow lateral slider move across oak herringbone parquet and a white skirting board in soft raking daylight, shallow depth of field, seamless calm loop, no people, photorealistic.` |

## Использование на сайте

| Ключ | Где |
|---|---|
| `wohnenNachher` + видео | Hero (постер = LCP, видео подгружается после `load` только на ≥ 768 px) |
| `badVorher/Nachher`, `wohnenVorher/Nachher`, `kuecheVorher/Nachher` | Before/After на Home и страницах проектов |
| `hero`, `trockenbau`, `putz`, `maler`, `boden`, `fliesen`, `sanierung`, `decke`, `komplett`, `badNachher`, `kuecheNachher`, `wohnenNachher` | Карточки и шапки услуг |
| `team` | Warum wir, Ablauf, Über uns |
| `material`, `fliesen` | Materialien & Qualität |

## Хранение

Ассеты пока отдаются с CDN Higgsfield (`d8j0ntlcm91z4.cloudfront.net`, разрешён в `next.config.ts → images.remotePatterns`). Для независимости от внешнего CDN:

```bash
npm run assets:fetch          # скачивает → public/images/<key>.webp (sharp, ≤2560 px, q82) + hero mp4
# затем в src/content/assets.ts: const ASSET_SOURCE = "local";
```
