# Bright Qud – compatibility with other mods

## How Bright Qud touches the game
- Replaces tile images by name (a later-loading mod with the same tile names wins).
- Harmony patches on: ConsoleChar.Set, Cell.Render, SpriteManager.TryGetTextureInfo,
  SpriteManager.GetPooledSprite, UIThreeColorProperties (FromRenderable, FromConsoleChar,
  UpdateColors). All are postfixes or pass-through prefixes, except the TryGetTextureInfo prefix,
  which only answers Bright Qud's own "brightqud:" paths.
- No gameplay data changes (no blueprint, population or stats edits).

## Well-known mods and risk
| Mod | What it does | Risk | Notes |
|---|---|---|---|
| Tiles Extended (installed, disabled) | new connecting tiles for stairs, shafts, pits, qudzu; changes fence/glass/canvas wall families | **Low** | different tile names; its tiles get auto-style. Its fences/canvas walls replace our hand-drawn ones for those objects. |
| Choose Your Fighter (+ tile packs) | tile picker at character creation | **Low** | Bright Qud's "player look" overrides only when not "Game default". CYF tiles get auto-style. |
| Caves of Qud Expanded | big content mod (creatures, items, mutations) | **Low** | new creatures get auto-style; built for 1.0, may not run on 2.0 itself. |
| The Qud Survival Guide, Promethean Furniture, Cask of Rose Wine, Caves of Chords | quests, creatures, items | **Low** | content only; auto-style covers their tiles. |
| Caves of Quick Menu | UI/menu helper | **Low** | different code paths. |
| Other tile/retexture packs | replace the same tile files | **Medium** | whichever loads last wins per tile; their truecolor tiles keep their colors (v0.6.0). |
| Mods that patch rendering (ConsoleChar/SpriteManager) | rare | **Medium** | Harmony stacks patches; visual glitches possible, not crashes. |

## Typical symptoms and quick checks
- A tile looks "half Bright Qud": another tile mod replaced it → change the load order.
- Strange colors on another mod's sprites → turn off "restyle tiles that aren't redrawn yet".
- Anything else: disable Bright Qud in the Mods menu; it changes no save data, so it's safe to
  turn off and on.
