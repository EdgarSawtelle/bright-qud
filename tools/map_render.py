"""Render a hand-made game map (.rpm, e.g. Joppa) with the original tiles, Bright Qud as it is today,
and proposals. Uses vanilla tiles, so output stays local: mockups/local/zones/.

Each cell shows only its top object (highest render layer), as the game does. Walls with a PaintWith
tag get their 8-direction neighbour mask; liquids use the deep-water tile.

Library use: render(map_name, mode, box, ground=None, ...) -> RGBA image at Deck 2x zoom.
"""
import os, random, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image  # noqa: E402
from qudxml import Blueprints, BASE  # noqa: E402
from build_mod import color_letters  # noqa: E402
import zone_mockup as zm  # noqa: E402

BP = None
DIRS = ((0, -1), (1, -1), (1, 0), (1, 1), (0, 1), (-1, 1), (-1, 0), (-1, -1))   # N NE E SE S SW W NW
SKIP = {"DaylightWidget", "Dirty"}


def bp():
    global BP
    BP = BP or Blueprints()
    return BP


def load(map_name):
    if isinstance(map_name, dict):          # a generated scene: (x, y) -> [object names]
        return map_name
    root = ET.fromstring(re.sub(r"&#x?[0-9a-fA-F]+;", "?", open(os.path.join(BASE, map_name + ".rpm"), encoding="utf-8-sig").read()))
    cells = {}
    for c in root.iter("cell"):
        cells[int(c.get("X")), int(c.get("Y"))] = [o.get("Name") for o in c.findall("object") if o.get("Name") not in SKIP]
    return cells


def is_liquid(name):
    b = bp()
    return any(n in ("Water", "LiquidVolume") for n in _chain(name)) or b.part(name, "LiquidVolume", "MaxVolume") is not None


def _chain(name):
    b, seen = bp(), []
    while name in b.objs and len(seen) < 50:
        seen.append(name)
        name = b.objs[name]["inh"]
    return seen


def tile_of(name, rnd):
    b = bp()
    if is_liquid(name):
        return zm.WATER
    for src in (b.builder(name, "RandomTile", "Tiles"), b.part(name, "RandomTileOnMove", "Tiles"),
                b.part(name, "RandomTile", "Tiles")):
        if src:
            return rnd.choice(src.split(","))
    t = b.part(name, "Render", "Tile")
    pick = b.part(name, "PickRandomTile", "Tile")
    if pick:
        m = re.search(r"~#?(\d+)-(\d+)~", pick)
        if m:
            t = pick[:m.start()] + str(rnd.randint(int(m.group(1)), int(m.group(2)))) + pick[m.end():]
    return t


def layer(name):
    try:
        return int(bp().part(name, "Render", "RenderLayer") or 5)
    except ValueError:
        return 5


def top_objects(cells):
    """(x, y) -> top object name (or None)."""
    out = {}
    for xy, objs in cells.items():
        withtile = [o for o in objs if o in bp().objs and (bp().part(o, "Render", "Tile") or is_liquid(o)
                                                           or bp().builder(o, "RandomTile", "Tiles")
                                                           or bp().part(o, "RandomTileOnMove", "Tiles"))]
        out[xy] = max(withtile, key=layer) if withtile else None
    return out


def wall_mask(cells, x, y, group):
    bits = ""
    for dx, dy in DIRS:
        objs = cells.get((x + dx, y + dy), [])
        bits += "1" if any(bp().tag(o, "PaintWith") == group for o in objs if o in bp().objs) else "0"
    return bits


def render(map_name, mode, box, ground=None, night=None, tone=None, bare=None, swap=None):
    """mode: vanilla | now | new. box = (x0, y0, x1, y1) in cells. ground(x, y) -> RGB for mode new.
    bare(x, y) -> RGBA tile drawn on cells with no object (mode new), like the runtime's zone floors.
    tone(name, fg, detail, tile) -> (fg_rgb, detail_rgb) or None: proposal recolours (mode new)."""
    cells = load(map_name)
    tops = top_objects(cells)
    rnd = random.Random(str(map_name)[:40])
    x0, y0, x1, y1 = box
    img = Image.new("RGBA", ((x1 - x0) * 16, (y1 - y0) * 24), (0, 0, 0, 255))
    for y in range(y0, y1):
        for x in range(x0, x1):
            name = tops.get((x, y))
            if mode == "vanilla":
                bg = zm.q("k")
            elif mode == "now":
                bg = zm.current_ground("w")   # FromPaint: greys -> Earth (real paint unknown)
            else:
                bg = ground(x, y)
            cell = Image.new("RGBA", (16, 24), bg + (255,))
            if not name and bare and mode == "new":
                cell.alpha_composite(bare(x, y))
            liquid = next((o for o in cells.get((x, y), []) if o in bp().objs and is_liquid(o)), None)
            if name and liquid and name != liquid and mode != "vanilla":
                # swimmers and floating plants: the game draws the water under them
                fgl, dtl = color_letters(bp(), liquid)
                w = zm.ours(zm.key_of(zm.WATER), fgl, fgl)
                if w is not None:
                    r = tone(liquid, fgl, dtl, None) if (tone and mode == "new") else None
                    cell.alpha_composite(zm.recolor_to(w, *r) if r else w)
            if name:
                tile = tile_of(name, rnd)
                group = bp().tag(name, "PaintWith")
                if tile and group and "-00000000" in tile:
                    tile = tile.replace("-00000000", "-" + wall_mask(cells, x, y, group))
                fg, dt = color_letters(bp(), name)
                key = zm.key_of(tile) if tile else None
                if swap and mode == "new":
                    key = swap(name, x, y, cells) or key       # runtime tile swaps (e.g. Kyakukya cage walls)
                t = None
                if key:
                    if mode == "vanilla":
                        t = zm.vanilla(key, fg, dt)
                    else:
                        t = zm.ours(key, fg, dt)
                        if t is not None and mode == "new" and tone:
                            r = tone(name, fg, dt, key)
                            if r:
                                t = zm.recolor_to(t, *r) if r[0] is not None else t
                        if t is not None and mode == "new" and ground and layer(name) == 0 and not is_liquid(name) \
                                and not (tone and tone(name, fg, dt, key)):
                            # floors placed as objects (paths, dirt floors) stay low-contrast with the ground
                            g = ground(x, y)
                            t = zm.recolor_to(t, tuple(min(255, int(c * 1.14)) for c in g), tuple(int(c * 0.86) for c in g))
                        if t is not None and mode == "now" and key.startswith("liquids"):
                            t = zm.tone_liquid(t)
                if t is None and key:
                    t = zm.vanilla(key, fg, dt)
                    if t is not None and mode != "vanilla":
                        t = zm.bright_vanilla(key, fg, dt) if hasattr(zm, "bright_vanilla") else t
                if t is not None:
                    cell.alpha_composite(t)
            if night:
                cell = night(cell, x, y)
            img.alpha_composite(cell, ((x - x0) * 16, (y - y0) * 24))
    return img.resize((img.width * zm.Z, img.height * zm.Z), Image.NEAREST)


if __name__ == "__main__":
    cells = load(sys.argv[1] if len(sys.argv) > 1 else "Joppa")
    xs = [x for (x, y), o in cells.items() if o]
    ys = [y for (x, y), o in cells.items() if o]
    print("objects span", min(xs), min(ys), max(xs), max(ys))
