"""Rainbow Wood floor: lush moss, green and cyan tufts and tiny mushrooms on dark olive ground.

The game paints each fungal-forest cell with a grass or dirt tile (Mushroomy.Paint). In Rainbow Wood zones
(world terrain TerrainFungal*) the runtime shows one of these tiles instead, picked per cell by a hash:
about 35% bare (LUSH 0-1), the rest busy (LUSH 2-15). LUSH 13-15 hold one tiny mushroom that slowly
breathes and lets a spore drift up (frames in FRAMES), so about 1 tiny mushroom in 8 moves.
Colours are fixed palette letters: the ground under them is the zone's olive moss colour.
"""
import random

# tiny mushrooms: c cap, h highlight, s stem
MINI = [
    [".c.", "chc", ".s."],
    [".ccc.", "chccc", "..s..", "..s.."],
    [".c.", "chc", ".s.", ".s.", ".s."],
    [".cc.", "chcc", ".cc."],
    ["cc", "hc", ".s"],
]
CAPS = [("m", "M"), ("c", "w"), ("y", "w"), ("G", "w"), ("B", "w"), ("r", "M")]   # (cap, highlight)
STEM = "t"
COUNT, BARE, ANIMATED = 16, 2, (13, 14, 15)


def _put(g, x, y, ch):
    if 0 <= x < 16 and 0 <= y < 24:
        g[y][x] = ch


def _mini(g, shape, x0, y0, cap, hi, stem=STEM):
    for gy, row in enumerate(MINI[shape]):
        for gx, ch in enumerate(row):
            c = {"c": cap, "h": hi, "s": stem}.get(ch)
            if c:
                _put(g, x0 + gx, y0 + gy, c)


def _ground(rnd, g, busy):
    if busy and rnd.random() < 0.75:            # moss patch
        cx, cy = rnd.randrange(3, 13), rnd.randrange(12, 21)
        for _ in range(rnd.randrange(10, 20)):
            _put(g, cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2), rnd.choice("hhgG"))
    else:                                       # a few specks
        for _ in range(rnd.randrange(2, 5)):
            _put(g, rnd.randrange(16), rnd.randrange(24), "h")
    if not busy:
        return
    for _ in range(rnd.choice((0, 1, 1, 2))):   # tufts, mostly green, some cyan fungal grass
        col = "c" if rnd.random() < 0.3 else rnd.choice("gG")
        x, y = rnd.randrange(2, 14), rnd.randrange(10, 22)
        for dx, h in ((-1, 2), (0, 3), (1, 2)):
            for i in range(h):
                _put(g, x + dx + (i == h - 1) * dx, y - i, col if i else "h")


def _variant(i):
    rnd = random.Random("lush%d" % i)
    g = [["." for _ in range(16)] for _ in range(24)]
    busy = i >= BARE
    _ground(rnd, g, busy)
    if busy:
        n = rnd.choice((1, 1, 2, 2, 3)) - (1 if i in ANIMATED else 0)
        for _ in range(n):
            cap, hi = rnd.choice(CAPS)
            _mini(g, rnd.randrange(len(MINI)), rnd.randrange(1, 12), rnd.randrange(6, 19), cap, hi)
    return g, rnd


def _animated(i):
    """4 frames: the breathing mushroom goes dim, lit, glowing (spore leaves), lit (spore rises)."""
    base, rnd = _variant(i)
    cap, hi = rnd.choice(CAPS[:5])
    shape, x0, y0 = rnd.randrange(len(MINI)), rnd.randrange(2, 11), rnd.randrange(9, 18)
    dim = {"m": "R", "c": "B", "y": "t", "G": "g", "B": "b"}
    frames = []
    for f in range(4):
        g = [row[:] for row in base]
        if f == 0:
            _mini(g, shape, x0, y0, dim.get(cap, cap), cap)
        else:
            _mini(g, shape, x0, y0, cap, hi)
        if f == 2:                                  # faint glow on the ground, spore just above the cap
            w = len(MINI[shape][0])
            for gx in range(-1, w + 1, 2):
                _put(g, x0 + gx, y0 + len(MINI[shape]), cap)
            _put(g, x0 + 1, y0 - 2, "w")
        if f == 3:
            _put(g, x0 + 2, y0 - 5, hi if hi != "w" else "l")
        frames.append(["".join(r) for r in g])
    return frames


SPRITES, FRAMES = {}, {}
for i in range(COUNT):
    key = "brightqudlush/%d" % i
    if i in ANIMATED:
        fr = _animated(i)
        SPRITES[key], FRAMES[key] = fr[0], fr[1:]
    else:
        SPRITES[key] = ["".join(r) for r in _variant(i)[0]]
