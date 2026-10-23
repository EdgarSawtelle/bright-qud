# Wave 2 – items, fixtures and terrain still in the game's default art (brief for art agents)

Read docs/ART_BRIEF_AGENTS.md first (hard rules, grid format, colour roles, workflow). This file adds
what is specific to this wave. Project: /home/deck/bright-qud, Python `.venv/bin/python -I`.

## Hard rules (repeat)
- ORIGINAL ART ONLY: draw from the name and the game description in your work list. Never read
  reference/, never copy any game's sprites.
- Only create YOUR file. Don't edit anything else, don't run release/sync/build_mod.

## Your file
`art/src/<label>_<i>.py` (label = items4, fixtures or terrain3; i = your batch number):
```python
from <keys module> import BATCH_KEYS     # items_keys / fixtures_keys / terrain_keys
KEYS = BATCH_KEYS[<i>]                     # {tile key: sprite name}; don't edit
SPRITES = {"<sprite name>": grid, ...}     # one per sprite name in your work list
KINDS = {"<sprite name>": "terrain" | "tall"}   # only for sprites that are not "object"
```
Work list: `docs/b3_worklists/<keys label>_<i>.md` (items_<i>, fixtures_<i> or terrain_<i>): sprite
name, tile keys (several keys may share one sprite: numbered variants, ruined copies), the game's
colours &F/D, an example object with its display name, and the game description.

Kinds: `object` (default) gets the dark outline + drop shadow: items, furniture, statues, machines.
`terrain` = flat, no outline, fills the cell: floors, ground patterns, wall-like murals, doors,
gates, stairs, world-map tiles. `tall` = walk-through plants/trees (soft outline).

## Style per category (look at these files first and match them)
- **Items** (art/src/items2.py, items3.py): small object lying on the ground, centred, roughly rows
  9-20, 6-13 px wide, chunky readable silhouette, 2-3 tones per material, one accent. Numbered
  variants share one sprite (their colours differ in game).
  Weapons: blade/head in steel `l/L` or role 4-6, handle in wood `n/N` or roles. Armour/clothes:
  folded garment shapes. Artifacts/tech: chrome + a glowing role-4 light.
- **Fixtures** (furniture, statues, machines, doors, gates, stairs, murals): art/src/tiles.py,
  terrain2.py (door_closed/door_open, walls), items.py (bed, table, chest). Seen in 3/4 view, may fill
  most of the tile; walls/murals/doors keep the walls' look (light top face, dark base). Directional
  pieces (…/n /s /e /w /left /right /top /bottom, nw/ne…) are separate sprites in your list: make
  them fit together.
- **Terrain** (art/src/terrain2.py, tiles.py): ground decorations, plants, trees, ruins and the
  WORLD MAP tiles (keys containing "worldmap" or location tiles). World-map tiles fill the whole
  16x24 cell like a little landscape icon (mountains, jungle, river, lake, ruins...), bold and
  saturated, with roles 1-3 for the region's main colour so the game's colours show through.
  River/lake pieces must connect at the edges the key name suggests (n/s/e/w, ns, we, nw...).

## Preview
`.venv/bin/python -I tools/preview_sprites.py <label>_<i> SPRITES KEYS /tmp/claude-1000/-home-deck-bright-qud/b2cd656e-7755-4bfc-a464-786552d8d609/scratchpad/<label>_<i>.png`
Zero ERROR lines, then open the PNG and look: is each one recognisable as what its name and
description say? At least 2 full review rounds. Final answer (short): file, preview path, count,
the 5 weakest.
