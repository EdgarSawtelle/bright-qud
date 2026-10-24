"""Moon Stair: the giant hex crystals and the twinkling diamond floor.

Crystals: the game builds each 3x2-cell prism at runtime from 25 part tiles
(ZoneManager.PaintCrystalWall: tiles/cryshex/{nw,n,ne,sw,s,se}/{0-3} by which neighbours are crystal,
tiles/cryshex/full inside a cluster). The parts must line up with each other exactly, so the layout
(which pixels are top face, side wall, edge or empty) is read from the game's own part tiles, then
repainted: a luminous faceted top, a lit and a shaded side wall, light rims, ink on the silhouette.
Colour: the game paints crystals with the foreground (m/M/y/Y, spiral paths C/W/B/G/R), so every
crystal pixel uses roles 1-3.

Floor: "strange floor" (SmallHexFloor, tiles terrain/sw/hex/dotted/*) becomes small diamonds of
moonlight on a loose hex lattice, transparent between them so the black marble ground shows.
FRAMES has 3 more frames per floor tile; the runtime cycles them slowly with a per-cell offset, so
each diamond brightens and dims on its own rhythm.
"""
import glob, math, os, random

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..")
REF = os.path.join(ROOT, "reference", "tiles")
PARTS = {"nw": (0, 0), "n": (16, 0), "ne": (32, 0), "sw": (0, 24), "s": (16, 24), "se": (32, 24)}

# ------------------------------------------------------------------ crystals


def _layout(name):
    """Classify the game's part tile: F top face (checkerboard), W foreground pixels (lit facet, rims),
    E detail pixels (shaded facet, outline), . empty."""
    from PIL import Image
    path = glob.glob(os.path.join(REF, "assets_content_textures_tiles_cryshex_" + name + ".*"))[0]
    im = Image.open(path).convert("RGBA")
    px = im.load()

    def white(x, y):
        return 0 <= x < 16 and 0 <= y < 24 and px[x, y][3] > 0 and px[x, y][0] > 127

    cls = [["." for _ in range(16)] for _ in range(24)]
    for y in range(24):
        for x in range(16):
            r, _, _, a = px[x, y]
            if a and r <= 127:
                cls[y][x] = "W"
            elif a:
                run = any(white(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                cls[y][x] = "E" if run else "F"
    # transparent cells of the checkerboard are face too
    for _ in range(3):
        grow = []
        for y in range(24):
            for x in range(16):
                if cls[y][x] != "." or px[x, y][3]:
                    continue
                n = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                        if 0 <= x + dx < 16 and 0 <= y + dy < 24 and cls[y + dy][x + dx] == "F")
                if n >= 2 or (n == 1 and _ == 0):
                    grow.append((x, y))
        for x, y in grow:
            cls[y][x] = "F"
    return cls


def _face_centre():
    pts = []
    for part, (ox, oy) in PARTS.items():
        cls = _layout(part + "_0")
        pts += [(ox + x, oy + y) for y in range(24) for x in range(16) if cls[y][x] == "F"]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return sum(xs) / len(xs), sum(ys) / len(ys), (max(xs) - min(xs)) / 2, (max(ys) - min(ys)) / 2


def _silhouette():
    """Rows of the whole prism (48 x 48): x span covered by any part of the lone prism."""
    span = {}
    for part, (ox, oy) in PARTS.items():
        cls = _layout(part + "_0")
        for y in range(24):
            for x in range(16):
                if cls[y][x] != ".":
                    lo, hi = span.get(oy + y, (99, -1))
                    span[oy + y] = (min(lo, ox + x), max(hi, ox + x))
    return span


SIL = None
NAME_V0 = False   # set while painting a lone top part (n/nw/ne, variant 0): carve spires


def _shard(gx, gy, shade):
    """Big shards leaning up to the right: a thin bright edge, a lit body, a cool periwinkle underside."""
    u = gy + gx * 0.6 + (2 if (gx // 9) % 2 else 0)   # offset every 9 px so the shards don't line up
    t = u % 12
    edge = "w" if int(u // 12) % 2 == 0 else "1"
    tone = edge if t < 1 else "1" if t < 3 else "2" if t < 8 else "p" if t < 10.5 else "P"
    if shade:
        tone = {"w": "1", "1": "2", "2": "p", "p": "P", "P": "P"}[tone]
    return tone


def _jag(out, origin):
    """Carve the top edge of a lone crystal into spires (sawtooth), tips lit."""
    ox, oy = origin
    for x in range(16):
        gx = ox + x
        col = [y for y in range(24) if out[y][x] != "."]
        if not col:
            continue
        top = col[0]
        depth = 7 - (gx % 9) if (gx // 9) % 2 == 0 else 5 - (gx % 9) // 2   # spires leaning right
        for y in range(top, min(24, top + depth)):
            out[y][x] = "."
        if top + depth < 24 and out[top + depth][x] != ".":
            out[top + depth][x] = "w" if depth <= 1 else "1"


def _paint(cls, origin, centre):
    global SIL
    SIL = SIL or _silhouette()
    if origin is not None:
        # the game leaves dark gaps inside the side walls: they are wall (shadow), not floor
        cls = [row[:] for row in cls]
        for y in range(24):
            lo, hi = SIL.get(origin[1] + y, (99, -1))
            for x in range(16):
                if cls[y][x] == "." and lo < origin[0] + x < hi:
                    cls[y][x] = "H"
    cx, cy, rx, ry = centre
    out = [["." for _ in range(16)] for _ in range(24)]
    ox, oy = origin if origin is not None else (0, 0)
    for y in range(24):
        for x in range(16):
            c = cls[y][x]
            if c == ".":
                continue
            gx, gy = ox + x, oy + y
            if c == "F" or origin is None:
                # top: long shards leaning up to the right, a bright streak on each upper edge and a
                # cool periwinkle underside; the right of the crystal falls into shade
                out[y][x] = _shard(gx, gy, gx > cx + rx * 0.35)
            else:
                same = sum(1 for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                           if 0 <= x + dx < 16 and 0 <= y + dy < 24 and cls[y + dy][x + dx] == c)
                if c == "W" and same >= 3:          # lit front-left facet, faint vertical grain
                    out[y][x] = "1" if (gx * 3 + gy // 4) % 11 == 0 else "2"
                elif c == "W":                      # rim lines catch the light
                    out[y][x] = "1"
                elif c == "E" and same >= 3:        # shaded front-right facet: cool, not black
                    out[y][x] = "P" if (gx * 5 + gy // 3) % 9 == 0 else "p"
                else:                               # outline and gaps in the walls
                    out[y][x] = "P"
    if origin is not None and cls is not None and NAME_V0:
        _jag(out, origin)
    return ["".join(r) for r in out]


def crystals():
    centre = _face_centre()
    sprites, keys = {}, {}
    for part, origin in PARTS.items():
        for v in range(4):
            name = f"cryshex_{part}_{v}"
            global NAME_V0
            NAME_V0 = v == 0 and part in ("n", "nw", "ne")
            sprites[name] = _paint(_layout(f"{part}_{v}"), origin, centre)
            NAME_V0 = False
            keys[f"tiles/cryshex/{part}/{v}"] = (name, "terrain")
    sprites["cryshex_full"] = _paint(_layout("full"), None, centre)
    keys["tiles/cryshex/full"] = ("cryshex_full", "terrain")
    return sprites, keys


# ------------------------------------------------------------------ diamond floor

LEVELS = [0, 1, 2, 1]      # brightness per step of a diamond's 4-step cycle


def _diamond(g, x, y, level):
    if not (0 <= x < 16 and 0 <= y < 24):
        return
    if level == 0:
        g[y][x] = "3"
        return
    g[y][x] = "2" if level == 1 else "w"
    if level == 2:
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            if 0 <= x + dx < 16 and 0 <= y + dy < 24:
                g[y + dy][x + dx] = "1"


# Hex plates that tile seamlessly across cells: pointy-top hexes 16 wide, rows 12 apart, odd rows
# shifted 8 (period 16 x 24 = one cell).
HEX_CENTRES = [(x + dx, y) for y, dx in ((-6, 8), (6, 0), (18, 8), (30, 0)) for x in (-16, 0, 16, 32)]


def _hex_lattice():
    """Per pixel: 'seam' on hex borders, 'bevel' just inside a plate's upper-left border, 'node' at
    the corners where three plates meet, else None."""
    info = {}
    for y in range(24):
        for x in range(16):
            ds = sorted((math.hypot(x + 0.5 - cx, (y + 0.5 - cy) * 1.15), (cx, cy)) for cx, cy in HEX_CENTRES)
            (d0, c0), (d1, _), (d2, _) = ds[:3]
            if d2 - d0 < 1.6:
                info[x, y] = "node"
            elif d1 - d0 < 1.1:
                info[x, y] = "seam"
            elif d1 - d0 < 2.2 and (x + 0.5 - c0[0]) + (y + 0.5 - c0[1]) < 0:
                info[x, y] = "bevel"
    # one node pixel per corner (the most central of each clump)
    nodes = [p for p, k in info.items() if k == "node"]
    keep = []
    for p in sorted(nodes):
        if all(abs(p[0] - q[0]) > 2 or abs(p[1] - q[1]) > 2 for q in keep):
            keep.append(p)
    for p in nodes:
        info[p] = "seam"
    return info, keep


def floor_frames(seed):
    """4 frames of one floor tile: sci-fi hex plates (seams, a lit bevel), a small diamond light on
    each corner node that brightens and dims on its own phase."""
    rnd = random.Random(seed)
    info, nodes = _hex_lattice()
    phases = {p: rnd.randrange(4) for p in nodes}
    frames = []
    for f in range(4):
        g = [["." for _ in range(16)] for _ in range(24)]
        for (x, y), k in info.items():
            g[y][x] = "P" if k == "seam" else "3"
        for (x, y), ph in phases.items():
            _diamond(g, x, y, LEVELS[(f + ph) % 4])
        frames.append(["".join(r) for r in g])
    return frames


FLOOR_KEYS = ["terrain/sw/hex/dotted/1", "terrain/sw/hex/dotted/2/l", "terrain/sw/hex/dotted/2/r"]

SPRITES, KEYS = crystals()
FRAMES = {}   # tile key -> [frame1, frame2, frame3] (frame 0 is the tile itself)
for k in FLOOR_KEYS:
    fr = floor_frames(k)
    name = "moonfloor_" + k.rsplit("dotted/", 1)[1].replace("/", "_")
    SPRITES[name] = fr[0]
    KEYS[k] = (name, "terrain")
    FRAMES[k] = fr[1:]
