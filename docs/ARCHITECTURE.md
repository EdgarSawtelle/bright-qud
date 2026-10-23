# Bright Qud – how the mod works

Qud generates much of the world from a seed: villages, villagers, legendary creatures and random
tile picks. Colors come from factions, mutations, status effects and lighting. So the mod can't
tell the game "object X uses tile Y". It has to work at the level of **tile files** and **runtime
colors**. Everything below was verified in the game's code (decompiled locally into
`reference/decomp/`, never shared).

## 1. Override tile paths, not objects
`Kobold/SpriteManager.Load()` registers mod PNGs under `Textures/` *after* the game's own tiles,
using the same key: lowercase, extension dropped, `_` and `\` turned into `/`, and the prefix
`assets/content/textures/` stripped. So `Mods/BrightQud/Textures/Creatures/sw_farmer.png` replaces
`Assets_Content_Textures_Creatures_sw_farmer.bmp` **for every object that uses it**, generated ones
included. No XML merges are needed.

Painted families (walls, liquids) use 8-digit neighbour masks, in the order N, NE, E, SE, S, SW, W, NW.
`tools/build_mod.py` generates exactly the mask names the game ships (e.g. 256 brinestalk walls,
47 deep water, 16 shallow water).

## 2. Truecolor art plus runtime recolor
Shader code, extracted from the game:
- 3-color shader: `rgb = mix(fg, detail, tex.r) * a + bg * (1 - a)`. Only red and alpha matter, so
  there can be no fixed ink outline.
- Truecolor shader: `rgb = tex.rgb * a + bg * (1 - a)`. The game's fg/detail colors are ignored.

The mod is truecolor (`modconfig.json` `shadermode: 1`). Each tile also ships a **role mask**
(`Textures/BrightQudMask/<same path>`: R = 100 foreground / 200 detail, G = 0/127/254 light/mid/dark).

`BrightQud.cs` (Harmony; the game runs `PatchAll` on mod code automatically):
- **Postfix `ConsoleChar.Set(RenderEvent)`**: the one point where each map cell gets its final tile
  and colors (called from `Zone.Render` for all 80×25 cells). If the tile has a mask, the cell's tile
  becomes a virtual path `brightqud:<key>|<fg>|<detail>[|m]`. Results are cached per
  (tile, fg, detail), so steady-state cost is one dictionary lookup per cell.
- **Prefix `SpriteManager.TryGetTextureInfo`**: resolves virtual paths. On the UI thread it builds and
  caches a recolored copy. Masked pixels become `ramp(brighten(game color), shade)`; everything else
  (ink outline, skin, eyes, shadows) stays fixed.
- **Remembered cells**: the postfix gets the RenderEvent. When `!Event.Visible || Event.Lit <= 1`
  (the same test `Cell.Render` uses before forcing `&K`), it renders a dim teal monochrome version,
  so visible vs remembered still reads clearly. Guessing from colors alone misfired: unripe
  watervine is legitimately colored `K`.
- **UI tiles**: `UIThreeColorProperties` (status-bar portrait, look/inventory panels) uses a 3-color
  UI material. For our tiles, a postfix on `FromRenderable`/`FromConsoleChar` swaps in the recolored
  sprite with the default UI material, and a prefix on `UpdateColors` stops the game re-applying
  its material while ours is shown.

- **Ground**: the cell background (what shaders blend under transparent pixels) is replaced where
  it is the default black `k`: outdoors a muted version of the cell's painted ground color
  (`Cell.PaintColorString`, set by Dirty/Grassy/... painters, so it follows the biome), enclosed
  rooms (flood fill from the zone edge through non-wall, non-door cells) a warm floor, and
  `Zone.IsInside()` zones (underground) stone. A `Cell.Render` postfix stores the cell for the
  `ConsoleChar.Set` postfix that `Zone.Render` calls next with the same RenderEvent.

- **Underlay (terrain under creatures)**: the game draws one object per cell, and marks swimmers only
  with a flat liquid-colored background. When a cell has a LiquidVolume object and something else is
  on top, the script composites: our water tile (recolored with the cell's liquid background color),
  then the top tile over it. The top tile can be ours or vanilla; vanilla 3-color tiles are converted
  with the shader math (`mix(fg, detail, r)`, alpha). If building fails, the plain tile is shown.
  This is the hook for drawing more terrain under creatures later (grass, floors).

- **Auto-style (whole world)**: vanilla tiles we haven't drawn are converted at runtime: brighter
  palette, plus ink outline and drop shadow by walkability tier. The tier is decided from the cell's top
  object: Brain or takeable = object; wall, solid or liquid = flat; occluding = tall; render
  layer >= 5 = object (furniture). Hand-drawn tiles override auto-style.
- **Mutations**: the game never changes sprites for mutations. For creatures with a Brain, the
  script checks the parts listed in `Generated.cs` (Horns, MultipleArms, Wings, Carapace, Quills,
  Stinger, TwoHeaded, Beak, BurrowingClaws, ThickFur, MultipleLegs; PhotosyntheticSkin and Albino
  tint the skin). On humanoid-kit tiles (`Generated.HumanoidKeys`) it composites overlay textures
  `brightqudmut/<name>`, back layers behind the body and front layers over it.
- `Generated.cs` is written by `tools/build_mod.py` (humanoid keys, mutation layers, skin colors).

Color math lives in `art/src/colors.py` and is mirrored in C# (`Bright` table, `Ramp`).

## 3. Fallbacks
- If scripting mods are off, the PNGs still load with sensible default colors. You lose per-object
  colors and the remembered-cell dimming.
- Tiles we haven't drawn stay vanilla (3-color) and keep working normally.

## Build & install
```
.venv/bin/python -I tools/build_mod.py      # art/src -> mod/BrightQud/Textures (+ masks)
tools/cscheck: dotnet build                 # compile-check BrightQud.cs against the game DLLs
tools/sync_mod.sh                           # copy to ~/.config/unity3d/Freehold Games/CavesOfQud/Mods/BrightQud
```
Logs to check after launch: `build_log.txt` (mod compile, "Applying Harmony patches... Success") and
`Player.log` (runtime errors, `BrightQud.*` exceptions).

## Known risks (verify in game)
- Other UI paths that don't go through UIThreeColorProperties may still show raw PNGs.
- Lighting modes (safelight red, radar) arrive as fg/detail colors and are recolored like any
  others, which should be close to vanilla behaviour.

## Map markers and legend (v0.6-0.7)
- `Recolor.DrawHud` draws markers into the tile from a `hud` bit field (part of the virtual path
  `|hN`): 1 hostile ring, 2 ally ring, 4-28 health bucket, 32 item sparkle, 64 player ring,
  128 low-health pulse, 256 talk bubble, 512 gold corner (stairs, filled containers), 1024 faded bubble.
- `Ground.StyleOf` / `HudOf` / `PlayerHud` / `Talk.Bubble` decide the bits; each feature has an
  Options → Mods checkbox (`Settings`).
- `AfterConversationPatch` (postfix on `AfterConversationEvent.Send`) stores int property
  `BrightQudTalked` on whoever the player talked to. That's plain object data, harmless without the mod.
- Legend: `Legend.Show` is the OnClick of a `Type="Button"` option; icons are `brightqudlegend/*`
  tiles built by `tools/legend.py` with empty masks (shown as drawn). Keep legend.py's marker
  drawing in sync with DrawHud.

## Wall aliases (v0.10)
Painted wall families in `terrain2.ALIAS_FAMILIES` ship only 16 tiles per material
(`brightqudwall/<material>-<N><E><S><W>`). `Recolor.Key` -> `WallAlias` maps the game's
8-direction mask key (e.g. `walls/wall/sultan/runes-10111010`) to that tile; the table is emitted
into Generated.WallAliases by build_mod. Older families (rock, marble, metal, mud, brick-as-canvas)
still ship all 256 variants.

## Effects (v0.9)
Burning objects: `Ground.Apply` resets the flickering background/foreground and sets hud bits
2048/4096 (flames). `ParticlePatch` (ParticleManager.Render prefix/postfix) fixes tile particles'
black background and recolors their tile. Gas: `tiles2/gas/0..3` translucent puffs (effects.py,
per-pixel alpha preserved by Recolored).
