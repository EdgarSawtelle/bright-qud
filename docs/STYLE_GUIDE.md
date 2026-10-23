# Bright Qud – Style Guide (Phase 1 draft)

## Display facts (measured on the Deck)
- Tiles are 16×24 px, shown at **2× zoom** (32×48 screen px). About 29×12 cells are visible next to the message log.
- The cell background is Qud color `k` (#0f3b3a, dark teal). Each cell shows **one** tile; nothing is drawn under a creature.
- Scanline and vignette shaders sit on top. Art must survive them, so no 1-px details that carry meaning alone.

## Palette (23 colors, `art/src/palette.py`)
| Band | Colors | Used for |
|---|---|---|
| Ink | `O` #10141f | outlines, eyes |
| Light neutrals | `w` `l` `L` | teeth, steel, stone |
| Skin | `s` `S` | |
| Wood / straw | `t` `n` `N` `y` | walls, chests, hair, gold |
| Greens | `G` `g` `h` | plants |
| Blues | `B` `b` `d` | water, cloth |
| Reds | `r` `R` | scarves, cords, danger |
| Magic | `m` `M` `c` | glow, weird creatures |
| Floor | `e` `E` | dirt specks only |

## Readability rules (most important first)
1. **Value hierarchy:** creatures > items > obstacles (walls, trees) > floor / water. The player is the brightest figure on screen.
2. **Outlines:** creatures, items and tall walk-through plants (trees) get an ink outline. Terrain and low plants (floor, walls, water, grass, crops) never have one (see rule 8).
3. **Floors are speckle, not fill:** paths are dense warm specks over the teal ground, so open areas stay calm and edges never look blocky.
4. **Light from the top-left:** highlights go top-left, shadow and ledge lines bottom-right.
5. **3/4 walls:** a wall shows its lit woven top; if the cell south of it is open, it also shows a front face. This is a preview of the painted-wall logic.
6. **Keep Qud's color language:** each object keeps the hue the game gives it (snapjaw red, glowfish magenta/cyan, watervine green). One shared game tile becomes several **recolored variants** (e.g. the farmer in yellow, white or cyan), so truecolor doesn't erase the meaning of colors.
7. **Caricature characters:** big head (about 10 of 24 rows), short body, seen slightly from above: the top of the head or hat is visible and the face sits low on the head. Big 2-px eyes, and one distinctive shape cue each (hat, ears, fin). A translucent ground shadow sits under the feet.
8. **Walkability tiers.** These follow the game's real data (Physics `Solid`, Render `Occluding`). Note that in Qud, normal trees are walk-through.
   - *Blocks you* (Solid: walls, fences, solid trees): a full-cell raised block with a dark base.
   - *Walk-through but blocks sight* (trees, brinestalk): outline, no drop shadow, a soft shade at the base.
   - *Creatures & items*: outline + drop shadow.
   - *Open ground* (paths, grass, crops, water): flat, no outline, no shadow.

## Variants
**Chosen: C** (user, Checkpoint 1 feedback). A and B remain in `tools/build_tiles.py` for reference.
- **A Bold:** black ink outline (4-neighbour), full saturation.
- **B Soft:** colored "sel-out" outline (a darker shade of the adjacent color), saturation −18%, slightly lighter.
- **C Chunky:** 8-neighbour outline plus a soft drop shadow, saturation +15%.
