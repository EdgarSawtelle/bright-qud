# World map attempts (2026-10-31)

Paused. Nothing here is in the game. The world map still uses the tiles from the zone work.
Pictures: mockups/local/worldmap/ (local only). Scripts: tools/review_worldmap*.py (dev only, need numpy).

## The user's brief, in the end
Stay close to the logic of original Qud: every tile is its own. Shapes a bit more round, and biomes not completely clashing with each
other, because that clash is the frustration. No textures, no marks placed on the land.

## Problems with today's map
- Our redraw turned the game's curved lakes and rivers into stair-stepped blocks.
- Each biome is repeating square wallpaper in lime and white, with hard edges against the next.

## Attempts
| # | Picture | Idea | Verdict |
|---|---|---|---|
| 1 | 01_painted | Per-pixel biome lookup with noise, zone palettes, small marks | Blending "amazing", but looks too real |
| 2 | 02_overworld | 16-bit overworld with outlined regions and dotted paths | "Terrible" |
| 3 | 03_stylised_marks | Flat tones, outlined trees, peaks, site sprites | "Terrible": badly placed sprites on top |
| 4 | 04_shaded_ground | Rounded borders, height surface shaded in tones | Textures "terrible", biomes generic |
| 5 | 05_ten_styles | Ten cartoon styles with big motifs | "I hate all of them" |
| 6 | 06_per_tile_last | Game's own glyph per cell, calm biome background eased across neighbours, glyphs in zone colours, curved water back | Waiting for a verdict |

## What to remember
- Do not generate land, stamp marks or add texture: the user rejected each of those.
- Attempt 6 is per cell only: Ground.Apply can set the background and glyph colours, no generated textures, and it brings back the
  game's own water tiles by dropping our redraw. That makes it cheap to try in game if the user wants it.
- It still has stepped cell edges. Rounding them for real needs tile variants for each border shape.
