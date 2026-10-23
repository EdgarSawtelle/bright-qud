"""Fixtures wave 2, batch 1: furniture, statues, machines, doors, gates, stairs, murals (60 sprites)."""
from fixtures_keys import BATCH_KEYS

KEYS = BATCH_KEYS[1]


class C:
    def __init__(s, fill="."):
        s.g = [[fill] * 16 for _ in range(24)]

    def r(s, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < 16 and 0 <= y < 24:
                    s.g[y][x] = c
        return s

    def p(s, x, y, c):
        if 0 <= x < 16 and 0 <= y < 24:
            s.g[y][x] = c
        return s

    def pts(s, c, *xy):
        for x, y in xy:
            s.p(x, y, c)
        return s

    def box(s, x0, y0, x1, y1, c):
        s.r(x0, y0, x1, y0, c); s.r(x0, y1, x1, y1, c)
        s.r(x0, y0, x0, y1, c); s.r(x1, y0, x1, y1, c)
        return s

    def ell(s, cx, cy, rx, ry, c):
        for y in range(24):
            for x in range(16):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    s.g[y][x] = c
        return s

    def out(s):
        return ["".join({"Y": "y", "C": "c", "W": "w", "o": "y"}.get(ch, ch) for ch in r) for r in s.g]


def shade(c, x0, y0, x1, y1, lt="1", md="2", dk="3", top=None):
    """Volume block: light top row/left col, dark bottom row/right col."""
    c.r(x0, y0, x1, y1, md)
    c.r(x0, y0, x1, y0, lt); c.r(x0, y0, x0, y1, lt)
    c.r(x0, y1, x1, y1, dk); c.r(x1, y1 and y0, x1, y1, dk)
    return c


SPRITES = {}
KINDS = {}


def T(name, c):
    SPRITES[name] = c.out()
    KINDS[name] = "terrain"


def O(name, c):
    SPRITES[name] = c.out()


# ---------------- stone / gates / doors (terrain) ----------------
c = C()
c.r(1, 2, 14, 23, "2"); c.r(1, 2, 14, 3, "1")
c.r(3, 6, 12, 23, "3")
c.r(4, 8, 11, 23, "O")
c.r(4, 7, 11, 7, "3")
for y in (2, 5, 8, 11, 14, 17, 20):
    pass
c.r(1, 6, 2, 23, "2"); c.r(13, 6, 14, 23, "2")
c.pts("1", (1, 8), (1, 12), (1, 16), (1, 20), (13, 10), (13, 14), (13, 18))
c.pts("3", (2, 9), (2, 13), (2, 17), (14, 11), (14, 15), (14, 19), (2, 21), (14, 22))
c.r(2, 4, 13, 5, "1"); c.r(2, 5, 13, 5, "2")
c.r(7, 3, 8, 4, "4")
c.r(4, 22, 11, 23, "x")
T("arch", c)

c = C()
c.r(0, 1, 15, 2, "5"); c.r(0, 1, 15, 1, "4")
c.r(1, 3, 14, 22, "O")
for x in range(2, 14, 2):
    c.r(x, 3, x, 21, "O" if x % 4 else "3")
    c.r(x + 1, 3, x + 1, 21, "3" if x % 4 else "2")
c.r(2, 3, 13, 3, "1")
c.r(2, 21, 13, 21, "3")
c.pts("1", (3, 8), (7, 12), (11, 6), (5, 16), (9, 18))
c.r(0, 22, 15, 23, "5")
T("belt_curtains", c)


def bronze_gate(side, life):
    c = C()
    c.r(0, 0, 15, 23, "2")
    c.r(0, 0, 15, 1, "1"); c.r(0, 22, 15, 23, "3")
    c.r(0, 0, 0, 23, "1"); c.r(15, 0, 15, 23, "3")
    # two door halves
    c.r(1, 2, 7, 21, "3"); c.r(8, 2, 14, 21, "3")
    c.box(1, 2, 7, 21, "O"); c.box(8, 2, 14, 21, "O")
    c.r(2, 3, 6, 20, "2"); c.r(9, 3, 13, 20, "2")
    # patina (cyan detail) shelves
    for (x, y) in [(2, 5), (3, 5), (5, 9), (6, 9), (2, 14), (3, 14), (4, 14), (5, 18), (6, 18), (10, 6), (11, 6), (9, 12), (10, 12), (12, 16), (13, 16), (9, 19), (10, 19)]:
        c.p(x, y, "4")
    for (x, y) in [(4, 5), (6, 13), (11, 9), (12, 18), (3, 18), (9, 15)]:
        c.p(x, y, "5")
    # relief panel
    if life:   # palm / pyramid
        c.pts("1", (4, 10), (3, 11), (5, 11), (4, 12), (4, 13), (11, 10), (10, 11), (12, 11), (11, 12))
        c.pts("4", (10, 14), (11, 13), (12, 14), (11, 14), (11, 15))
    else:      # inverted pyramid on chains
        c.pts("1", (4, 8), (3, 9), (4, 9), (5, 9), (4, 10), (11, 7), (11, 8), (10, 9), (11, 9), (12, 9))
        c.pts("3", (4, 6), (4, 7), (11, 5), (11, 6))
    c.p(7, 12, "y"); c.p(8, 12, "y")
    return c


T("deathgate_w", bronze_gate("w", False))
T("lifegate_e", bronze_gate("e", True))


def door2(style, part):
    c = C()
    horiz = part in ("top", "bottom")
    # frame fills tile; leaf inside
    c.r(0, 0, 15, 23, "3")
    if part == "left":
        x0, x1, y0, y1 = 0, 15, 2, 21
    # general: frame on outer edges, seam on inner edge
    if part == "left":   box = (1, 2, 15, 22)
    elif part == "right": box = (0, 2, 14, 22)
    elif part == "top":   box = (1, 3, 14, 23)
    else:                 box = (1, 0, 14, 21)
    bx0, by0, bx1, by1 = box
    base = {"basic": ("2", "1"), "striped": ("2", "1"), "wavy": ("l", "w"), "metal": ("l", "L"),
            "window": ("2", "1")}[style]
    c.r(bx0, by0, bx1, by1, "O")
    c.r(bx0 + 1, by0 + 1, bx1 - 1, by1 - 1, base[0])
    # light top-left edge
    c.r(bx0 + 1, by0 + 1, bx1 - 1, by0 + 1, base[1])
    c.r(bx0 + 1, by0 + 1, bx0 + 1, by1 - 1, base[1])
    c.r(bx0 + 1, by1 - 1, bx1 - 1, by1 - 1, "3" if style in ("basic", "striped", "window") else "L")
    ix0, iy0, ix1, iy1 = bx0 + 2, by0 + 2, bx1 - 2, by1 - 2
    if style == "basic":
        if horiz:
            for y in range(iy0, iy1 + 1, 3):
                c.r(ix0, y, ix1, y, "3")
        else:
            for x in range(ix0, ix1 + 1, 3):
                c.r(x, iy0, x, iy1, "3")
        c.pts("4", (ix0 + 2, iy0 + 3), (ix0 + 2, iy0 + 4), (ix1 - 2, iy1 - 3))
    elif style == "striped":
        n = 0
        rng = range(iy0, iy1 + 1) if horiz else range(ix0, ix1 + 1)
        for i in rng:
            if (i // 2) % 2:
                if horiz: c.r(ix0, i, ix1, i, "4")
                else: c.r(i, iy0, i, iy1, "4")
        if horiz: c.r(ix0, (iy0 + iy1) // 2, ix1, (iy0 + iy1) // 2, "3")
        else: c.r((ix0 + ix1) // 2, iy0, (ix0 + ix1) // 2, iy1, "3")
    elif style == "wavy":
        for y in range(iy0, iy1 + 1):
            for x in range(ix0, ix1 + 1):
                if (x + (2 if (y // 2) % 2 else 0)) % 4 in (0, 1) and (y % 2 == 0):
                    c.p(x, y, "5")
                elif (x + y) % 4 == 0:
                    c.p(x, y, "4")
        # chrome stiles
        if part == "left": c.r(bx1 - 2, by0 + 1, bx1 - 1, by1 - 1, "w")
        if part == "right": c.r(bx0 + 1, by0 + 1, bx0 + 2, by1 - 1, "w")
        if part == "top": c.r(bx0 + 1, by1 - 2, bx1 - 1, by1 - 1, "w")
        if part == "bottom": c.r(bx0 + 1, by0 + 1, bx1 - 1, by0 + 2, "w")
    elif style == "metal":
        # furrows + centre slide panel
        for i in range(ix0, ix1 + 1, 2) if not horiz else range(iy0, iy1 + 1, 2):
            if horiz: c.r(ix0, i, ix1, i, "L")
            else: c.r(i, iy0, i, iy1, "L")
        if part in ("left", "right"):
            sx = bx1 - 5 if part == "left" else bx0 + 1
            c.r(sx, 8, sx + 3, 13, "O"); c.r(sx + 1, 9, sx + 2, 12, "4")
        else:
            sy = by1 - 5 if part == "top" else by0 + 1
            c.r(5, sy, 10, sy + 3, "O"); c.r(6, sy + 1, 9, sy + 2, "4")
    elif style == "window":
        c.r(ix0, iy0, ix1, iy1, "3")
        if part in ("left", "right"):
            wx0 = bx1 - 6 if part == "left" else bx0 + 2
            c.r(wx0, 6, wx0 + 3, 11, "O"); c.r(wx0 + 1, 7, wx0 + 2, 10, "c"); c.p(wx0 + 1, 7, "w")
        else:
            wy = by1 - 6 if part == "top" else by0 + 2
            c.r(5, wy, 10, wy + 3, "O"); c.r(6, wy + 1, 9, wy + 2, "c"); c.p(6, wy + 1, "w")
    # handle near seam
    if style in ("basic", "striped", "window"):
        if part == "left": c.p(bx1 - 2, 13, "y")
        if part == "right": c.p(bx0 + 2, 13, "y")
        if part == "top": c.p(8, by1 - 2, "y")
        if part == "bottom": c.p(8, by0 + 2, "y")
    return c


for st, parts in [("basic", ("top", "bottom")), ("metal", ("right",)), ("striped", ("left",)),
                  ("wavy", ("top", "bottom")), ("window", ("right",))]:
    for pt in parts:
        T(f"door2_{st}_{pt}", door2(st, pt))


def door_single(style):
    c = C()
    c.r(1, 2, 14, 23, "O")
    c.r(2, 3, 13, 22, "2")
    c.r(2, 3, 13, 4, "1"); c.r(2, 3, 2, 22, "1")
    c.r(2, 22, 13, 22, "3"); c.r(13, 4, 13, 22, "3")
    for y in range(5, 22):
        if (y // 2) % 2:
            c.r(3, y, 12, y, "4")
    c.r(3, 12, 12, 12, "3")
    c.r(3, 13, 12, 13, "3")
    c.pts("y", (11, 14), (11, 15))
    return c


T("door_striped", door_single("striped"))

c = C()
c.r(0, 3, 15, 22, "O")
c.r(1, 4, 14, 21, "C")
for x in (4, 8, 12):
    c.r(x, 4, x, 21, "O")
    c.r(x - 1, 4, x - 1, 21, "w")
c.r(1, 4, 14, 5, "w"); c.r(1, 21, 14, 21, "B")
c.r(0, 0, 15, 2, "5"); c.r(0, 0, 15, 0, "4")
c.r(5, 8, 6, 14, "w"); c.r(9, 12, 10, 18, "w")
c.pts("w", (2, 7), (13, 9), (7, 18))
T("gate_glass_w_closed", c)

c = C()
c.r(0, 0, 15, 23, "2")
c.r(0, 0, 15, 1, "1"); c.r(0, 22, 15, 23, "3")
c.ell(8, 12, 7, 9, "O"); c.ell(8, 12, 6, 8, "3")
c.ell(8, 12, 5, 7, "4"); c.ell(8, 12, 3, 5, "5")
c.r(8, 5, 8, 19, "O"); c.r(2, 12, 14, 12, "O")
c.r(4, 8, 5, 9, "w"); c.p(4, 8, "w")
T("earth_gate_left", c)

c = C()
c.r(0, 0, 15, 23, "3")
c.r(1, 1, 14, 22, "2")
c.r(1, 1, 14, 1, "1"); c.r(1, 1, 1, 22, "1")
c.r(2, 3, 13, 20, "O")
c.r(3, 4, 7, 19, "5"); c.r(8, 4, 12, 19, "5")
c.r(3, 4, 7, 4, "4"); c.r(8, 4, 12, 4, "4")
c.r(7, 4, 8, 19, "O")
c.r(5, 10, 6, 14, "6"); c.r(9, 10, 10, 14, "6")
c.r(6, 11, 6, 13, "4"); c.r(9, 11, 9, 13, "4")
c.pts("y", (3, 8), (12, 8), (3, 16), (12, 16))
T("golem_interior_hatch_closed", c)

# stairs
c = C()
c.r(0, 0, 15, 23, "3")
for i, y in enumerate(range(20, 2, -4)):
    ins = i
    c.r(ins, y - 3, 15 - ins, y, "2")
    c.r(ins, y - 3, 15 - ins, y - 3, "1")
    c.r(ins, y, 15 - ins, y, "5")
    c.r(ins, y - 3, ins, y, "1")
c.r(0, 0, 15, 1, "O")
c.pts("O", (0, 0))
c.pts("4", (6, 6), (9, 10), (4, 14))
c.r(5, 2, 10, 2, "6")
T("stairsup", c)


def sunken(d):
    """sunken room stairs corners: marble steps stepping into pit. d: 'ne' or 'se'."""
    c = C()
    c.r(0, 0, 15, 23, "O")
    # marble slabs, 3 steps
    for i in range(3):
        if d == "ne":
            x0, x1, y0, y1 = 0, 15 - i * 3, 0 + i * 3 + 5 if False else 14 - i * 5, 22 - i * 0
            c.r(0, 18 - i * 6, 15 - i * 5, 22 - i * 6 + 0, "W")
        else:
            c.r(0, 1 + i * 6, 15 - i * 5, 5 + i * 6, "W")
    # restructure: clean draw
    c = C()
    c.r(0, 0, 15, 23, "k" if False else "3")
    steps = [(0, 15), (0, 11), (0, 7)]
    for i, (a, b) in enumerate(steps):
        if d == "ne":
            y0 = 15 - i * 5 + 0
            c.r(a, y0 - 4, b + 0, y0 + 0, "W" if False else "1")
            c.r(a, y0 - 4, b, y0 - 4, "w")
            c.r(a, y0, b, y0, "3")
            c.r(b, y0 - 4, b, y0, "3")
            c.p((a + b) // 2, y0 - 2, "2")
        else:
            y0 = 4 + i * 5
            c.r(a, y0, b, y0 + 4, "1")
            c.r(a, y0, b, y0, "w")
            c.r(a, y0 + 4, b, y0 + 4, "3")
            c.r(b, y0, b, y0 + 4, "3")
    return c


def stairs_s(d):
    c = C()
    c.r(0, 0, 15, 23, "O")
    pit = "3"
    c.r(0, 0, 15, 23, "O")
    if d == "ne":
        rows = [(0, 3), (4, 7), (8, 11), (12, 15)]   # stepping up, wider toward top-right
    ys = [20, 14, 8]
    for i in range(3):
        if d == "ne":
            x0 = 0
            x1 = 15 - i * 4 - 0
            y0 = 18 - i * 6
            y1 = y0 + 4
        else:
            x0 = 0
            x1 = 15 - i * 4
            y0 = 2 + i * 6 + 0
            y1 = y0 + 4
        c.r(x0, y0, x1, y1, "1")
        c.r(x0, y0, x1, y0, "w"); c.r(x0, y0, x0, y1, "w")
        c.r(x0, y1, x1, y1, "2"); c.r(x1, y0, x1, y1, "2")
        c.pts("2", (x0 + 3, y0 + 2), (x0 + 7, y0 + 2))
    # pit shadow at far corner
    return c


T("sunken_room_stairs_ne", stairs_s("ne"))
T("sunken_room_stairs_se", stairs_s("se"))

c = C()
c.r(0, 0, 15, 23, "O")
c.r(1, 1, 14, 22, "3")
c.r(2, 2, 13, 21, "O")
for i, y in enumerate((18, 14, 10, 6)):
    c.r(7 + (i % 2) * 0, y, 8, y, "4")
c.r(7, 2, 8, 21, "5")
for y in range(3, 21, 3):
    c.r(5, y, 10, y, "4")
c.r(7, 2, 8, 2, "4")
c.pts("5", (4, 5), (11, 8), (3, 12), (12, 16), (4, 19))
T("openpit", c)

c = C()
for y in range(0, 24):
    off = (y // 6) % 2 * 4
    for x in range(16):
        c.p(x, y, "2")
for y in range(0, 24, 6):
    c.r(0, y, 15, y, "O")
for yb in range(0, 24, 6):
    off = 0 if (yb // 6) % 2 == 0 else 4
    for x in range(off, 16, 8):
        c.r(x, yb, x, yb + 5, "O")
    for x in range(0, 16, 8):
        pass
for yb in range(0, 24, 6):
    off = 0 if (yb // 6) % 2 == 0 else 4
    for x in range(off, 16 + 8, 8):
        c.r(x + 1, yb + 1, min(x + 7, 15), yb + 1, "1")
        c.r(x + 1, yb + 1, x + 1, yb + 4, "1")
        c.p(x + 4, yb + 3, "3")
T("floor_brick", c)

# ---------------- murals / walls (terrain) ----------------


def wall_base(c, light="1", mid="2", dark="3"):
    c.r(0, 0, 15, 23, mid)
    c.r(0, 0, 15, 3, light)
    c.r(0, 4, 15, 4, mid)
    c.r(0, 20, 15, 23, dark)
    c.r(0, 20, 15, 20, "O")
    return c


def mural(kind, end=None, ruined=False):
    c = wall_base(C())
    # stone panel border
    c.box(1, 6, 14, 19, "3")
    if end == "r": c.r(14, 6, 14, 19, "1")
    if kind == "baetyl":
        # figure kneeling to a stone
        c.r(9, 11, 12, 15, "4"); c.r(10, 12, 11, 14, "5"); c.p(10, 12, "w")
        c.r(3, 9, 5, 9, "6"); c.r(3, 10, 4, 14, "6"); c.r(2, 15, 6, 15, "6"); c.p(5, 12, "6"); c.p(6, 13, "6"); c.p(7, 13, "6")
    elif kind == "period":
        c.pts("4", (3, 9), (4, 9), (3, 10), (6, 8), (7, 8), (7, 9), (10, 10), (11, 10), (11, 11), (5, 14), (6, 14), (5, 15), (9, 15), (10, 15), (12, 14))
        c.pts("5", (4, 10), (8, 9), (12, 11), (6, 15), (11, 15))
        c.r(2, 17, 13, 17, "6")
    elif kind == "ruined":
        c.pts("4", (3, 9), (4, 9), (3, 10), (4, 12), (5, 12))
        c.pts("5", (4, 10), (6, 12))
        c.pts("2", (8, 8), (9, 9), (9, 10), (10, 10), (10, 11), (11, 12), (12, 13), (12, 14), (11, 15), (12, 16))
        c.r(9, 11, 13, 19, "2")
        c.pts("O", (9, 11), (10, 12), (11, 13), (10, 14), (12, 15), (11, 17))
        c.pts("3", (9, 13), (10, 15), (9, 17), (12, 18))
    if end == "l":
        c.r(0, 6, 0, 19, "3")
    return c


T("mural_appeasesbaetyl_r", mural("baetyl", "r"))
T("mural_rightend_period", mural("period", "r"))
T("mural_ruined4_r", mural("ruined", "r", True))

c = wall_base(C())
for x in range(1, 15, 3):
    c.r(x, 6, x, 19, "3")
    c.r(x + 1, 6, x + 1, 19, "2")
# vacuum tubes / circuit rivers
c.r(1, 8, 14, 8, "5"); c.r(1, 8, 4, 8, "4")
c.r(4, 8, 4, 14, "5"); c.r(4, 14, 11, 14, "5"); c.r(11, 14, 11, 18, "5"); c.r(8, 11, 8, 18, "6")
c.pts("4", (4, 11), (11, 16), (8, 14), (2, 8), (13, 8), (14, 14))
c.r(12, 10, 14, 12, "O"); c.r(13, 11, 13, 11, "c")
c.r(1, 16, 3, 18, "O"); c.r(2, 17, 2, 17, "c")
T("wall_coolant", c)

c = wall_base(C())
c.r(1, 5, 14, 19, "O")
c.r(2, 6, 13, 18, "n")
c.r(2, 6, 13, 6, "t")
# blanket and curtain
c.r(2, 10, 13, 18, "1"); c.r(2, 10, 13, 10, "4")
c.r(2, 11, 13, 11, "2")
for x in range(2, 14, 2):
    c.p(x, 14, "4")
c.r(2, 7, 5, 9, "w"); c.r(3, 7, 4, 8, "w")  # pillow
c.r(10, 6, 13, 12, "5"); c.pts("4", (11, 8), (12, 10))
c.r(2, 18, 13, 18, "N")
T("starship_1_wallbed_e", c)

c = wall_base(C())
c.r(1, 5, 14, 19, "O")
c.r(2, 6, 13, 18, "N")
for y in (9, 13, 17):
    c.r(2, y, 13, y, "n")
cols = "rbgyrmcgbr"
for sy in (6, 10, 14):
    for i, x in enumerate(range(2, 14)):
        if (x + sy) % 5 != 0:
            c.r(x, sy, x, sy + 2 if sy < 14 else sy + 2, "rbgyrmcgbrbg"[(x * 3 + sy) % 12])
    c.r(2, sy + 3 if sy < 14 else 17, 13, sy + 3 if sy < 14 else 17, "n")
T("starship_1_wallbookshelf_w", c)

# ---------------- furniture and objects (object kind) ----------------
c = C()
c.r(2, 10, 13, 19, "2"); c.r(2, 10, 13, 12, "1"); c.r(2, 17, 13, 19, "3")
c.r(2, 13, 13, 13, "3")
c.r(2, 10, 2, 19, "4"); c.r(13, 10, 13, 19, "5")
c.r(2, 10, 3, 11, "y"); c.r(12, 10, 13, 11, "y")
c.r(2, 18, 3, 19, "y"); c.r(12, 18, 13, 19, "y")
c.r(7, 13, 8, 15, "y"); c.p(7, 14, "O")
c.pts("w", (5, 11), (9, 11))
c.r(3, 20, 12, 20, "x")
O("chest", c)

c = C()
c.r(3, 8, 12, 12, "3")
c.r(2, 7, 13, 9, "1"); c.r(2, 9, 13, 9, "2")
c.r(3, 10, 3, 19, "3"); c.r(12, 10, 12, 19, "3")
c.r(4, 10, 11, 17, "O")
c.r(5, 13, 10, 18, "5"); c.r(6, 15, 9, 18, "4"); c.r(7, 16, 8, 18, "w")
c.pts("w", (4, 11), (11, 11))
c.r(3, 19, 12, 19, "2"); c.r(2, 20, 13, 21, "x")
c.r(4, 5, 5, 6, "1"); c.r(10, 5, 11, 6, "1")   # awning pegs
c.r(2, 5, 13, 7, "1"); c.r(2, 7, 13, 7, "4"); c.pts("5", (4, 6), (6, 6), (9, 6), (11, 6))
c.r(2, 5, 13, 5, "w")
O("oven", c)

c = C()
c.r(1, 9, 14, 18, "2"); c.r(1, 9, 14, 11, "1"); c.r(1, 17, 14, 18, "3")
c.r(1, 12, 14, 12, "3")
c.r(2, 14, 2, 20, "3"); c.r(13, 14, 13, 20, "3"); c.r(3, 14, 3, 20, "2"); c.r(12, 14, 12, 20, "2")
c.pts("1", (2, 15), (2, 16)); c.pts("2", (5, 10), (9, 11), (11, 10), (4, 11))
c.r(2, 21, 13, 21, "x")
O("table", c)

c = C()
c.r(2, 8, 13, 17, "n"); c.r(2, 8, 13, 10, "t"); c.r(2, 16, 13, 17, "N")
c.r(2, 11, 13, 11, "N")
c.r(3, 12, 3, 20, "N"); c.r(12, 12, 12, 20, "N"); c.r(4, 12, 4, 19, "n")
c.pts("N", (5, 9), (8, 9), (11, 10), (6, 10))
c.r(7, 11, 9, 11, "y")
c.r(2, 21, 13, 21, "x")
O("starship_wooden_table", c)

c = C()
c.r(3, 3, 12, 11, "2"); c.r(3, 3, 12, 4, "1"); c.r(3, 11, 12, 11, "3")
c.r(3, 3, 3, 11, "5"); c.r(12, 3, 12, 11, "6")
c.r(4, 5, 11, 10, "2"); c.r(5, 6, 10, 9, "3")
c.r(4, 12, 11, 16, "2"); c.r(4, 12, 11, 12, "1")
c.r(4, 16, 4, 20, "3"); c.r(11, 16, 11, 20, "3"); c.r(3, 12, 4, 16, "3"); c.r(11, 12, 12, 16, "3")
c.r(5, 13, 10, 15, "2"); c.pts("g", (7, 14), (8, 14), (7, 6), (8, 8))
c.r(4, 21, 11, 21, "x")
O("wood_carved_chair", c)

c = C()
c.r(1, 5, 14, 12, "2"); c.r(1, 5, 14, 6, "1")
c.r(1, 5, 1, 17, "3"); c.r(14, 5, 14, 17, "3")
c.r(2, 13, 13, 18, "2"); c.r(2, 13, 13, 14, "1"); c.r(2, 18, 13, 18, "3")
c.r(7, 6, 8, 18, "3")
c.r(2, 7, 6, 11, "3"); c.r(9, 7, 13, 11, "3")
c.pts("1", (3, 8), (10, 8))
c.r(2, 19, 3, 20, "3"); c.r(12, 19, 13, 20, "3")
c.r(2, 21, 13, 22, "x")
O("eater_chair_double", c)

c = C()
c.r(1, 6, 14, 11, "2"); c.r(1, 6, 14, 7, "1"); c.r(1, 6, 1, 17, "3")
c.r(2, 12, 14, 17, "2"); c.r(2, 12, 14, 13, "1"); c.r(2, 17, 14, 17, "3")
c.r(1, 6, 3, 17, "3"); c.r(4, 8, 4, 8, "1")
c.pts("1", (6, 9), (9, 9), (12, 9)); c.pts("3", (7, 15), (11, 14))
c.r(13, 8, 14, 17, "3")
c.r(1, 18, 2, 20, "3"); c.r(13, 18, 14, 20, "3")
c.r(2, 21, 13, 22, "x")
O("eater_couch_l", c)

c = C()
c.ell(8, 11, 6, 7, "O"); c.ell(8, 11, 5, 6, "B"); c.ell(8, 11, 4, 5, "b")
c.pts("t", (6, 8), (7, 8), (6, 9), (10, 11), (11, 12), (10, 12), (8, 14), (7, 14), (5, 12))
c.pts("w", (5, 8), (4, 9))
c.r(5, 17, 10, 17, "4"); c.r(6, 18, 9, 19, "5"); c.r(4, 19, 11, 19, "6")
c.r(8, 3, 8, 4, "5")
c.r(4, 21, 11, 21, "x")
O("eater_globe", c)

c = C()
c.r(1, 5, 14, 17, "O"); c.r(2, 6, 13, 16, "2")
c.r(2, 6, 13, 6, "1")
c.pts("w", (3, 8), (4, 9), (3, 10), (5, 11))
c.r(7, 8, 12, 8, "1"); c.r(10, 7, 10, 9, "1"); c.p(11, 7, "1"); c.p(11, 9, "1"); c.pts("1", (12, 8))
c.pts("y", (8, 13), (10, 14), (12, 13))
c.r(7, 18, 8, 20, "3")
c.r(5, 21, 10, 21, "x")
O("eater_sign_arrow", c)

c = C()
c.r(6, 3, 9, 3, "y")
c.r(7, 2, 8, 2, "w")
c.r(7, 4, 8, 4, "y")
c.r(4, 5, 11, 12, "2"); c.r(4, 5, 11, 6, "1"); c.r(4, 12, 11, 12, "3"); c.r(11, 5, 11, 12, "3")
c.pts("O", (7, 8), (8, 8), (6, 9), (9, 9), (7, 10), (8, 10))
c.pts("4", (7, 9), (8, 9))
c.r(6, 13, 9, 14, "2"); c.r(5, 15, 10, 16, "2"); c.r(5, 15, 10, 15, "1"); c.r(5, 16, 10, 16, "3")
c.r(7, 17, 8, 18, "3"); c.r(4, 19, 11, 19, "2"); c.r(4, 20, 11, 20, "3")
c.pts("W" if False else "w", (3, 1), (12, 0), (5, 0))
c.r(4, 21, 11, 21, "x")
O("eater_thrurible", c)

# floor clock quadrants: nw/sw of a large ecliptic mosaic
import math


def clock(quad):
    c = C()
    c.r(0, 0, 15, 23, "2")
    cx = 15.5 if quad[1] == "w" else -0.5
    cy = 23.5 if quad[0] == "n" else -0.5
    for y in range(24):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            ang = int(math.degrees(math.atan2(y - cy, x - cx)) / 15) % 2
            if 18 <= d < 20:
                c.p(x, y, "3")
            elif 16 <= d < 18:
                c.p(x, y, "1")
            elif 11 <= d < 16:
                c.p(x, y, "y" if (ang and d > 12.5 and d < 14.5) else "3" if d < 12 else "2")
            elif d < 11:
                c.p(x, y, "1" if int(d / 2) % 2 else "2")
            if d < 3:
                c.p(x, y, "y")
    if quad[0] == "n":
        c.r(7, 18, 8, 23, "3")
    return c


T("floor_clock_nw", clock("nw"))
T("floor_clock_sw", clock("sw"))

c = C()
c.r(3, 3, 12, 15, "3"); c.r(4, 4, 11, 14, "O")
c.r(5, 5, 10, 13, "5"); c.r(5, 5, 10, 5, "4")
c.pts("w", (6, 7), (7, 7), (8, 7), (6, 9), (9, 9), (7, 11), (8, 11), (9, 11))
c.r(2, 15, 13, 17, "2"); c.r(2, 15, 13, 15, "1"); c.r(2, 17, 13, 17, "3")
c.r(4, 18, 11, 19, "3"); c.r(5, 20, 10, 20, "O")
c.pts("1", (6, 6), (7, 6))
c.r(3, 21, 12, 21, "x")
O("starship_1_status_panel", c)

c = C()
c.r(2, 13, 13, 18, "2"); c.r(2, 13, 13, 14, "1"); c.r(2, 18, 13, 18, "3")
c.ell(8, 9, 5, 3, "O"); c.ell(8, 9, 4, 2, "5")
c.r(4, 10, 4, 12, "4"); c.r(11, 10, 11, 12, "4")
c.r(7, 3, 8, 8, "4"); c.pts("w", (8, 2), (6, 5), (10, 6), (7, 7))
c.pts("4", (5, 4), (11, 4), (4, 7), (12, 7))
c.pts("5", (6, 16), (9, 16))
c.r(3, 19, 12, 19, "3"); c.r(3, 21, 12, 21, "x")
O("hologram_projector", c)

# spindle ribbons: tall carbon ribbon going skyward
def ribbon(side, top, anchor):
    c = C()
    cx = 7 if side == "m" else (6 if side == "l" else 9)
    if not top:
        for y in range(0, 17):
            w = 1 if y < 5 else 2 if y < 11 else 3
            for x in range(cx - w // 2, cx - w // 2 + w + 1):
                c.p(x + (1 if (y // 3) % 2 else 0), y, "4" if x == cx - w // 2 else "5")
        # anchor
        c.r(4, 17, 11, 19, "2"); c.r(4, 17, 11, 17, "1"); c.r(4, 19, 11, 19, "3")
        c.r(5, 20, 10, 20, "L"); c.pts("l", (5, 18), (10, 18))
        c.r(5, 21, 10, 21, "x")
    else:
        for y in range(0, 24):
            w = 1 if y < 8 else 2
            for x in range(cx - w // 2, cx - w // 2 + w + 1):
                c.p(x + (1 if (y // 4) % 2 else 0), y, "4" if x == cx - w // 2 else "5")
        c.pts("w", (cx, 3), (cx, 12))
    return c


O("spindle_ribbon", ribbon("m", False, 0))
O("left_spindle_ribbon_top", ribbon("l", True, 0))
O("right_spindle_ribbon", ribbon("r", False, 0))
# support arm
c = C()
c.r(0, 2, 7, 5, "2"); c.r(0, 2, 7, 2, "1"); c.r(0, 5, 7, 5, "3")
c.r(6, 4, 9, 10, "2"); c.r(6, 4, 6, 10, "1"); c.r(9, 4, 9, 10, "3")
c.r(7, 10, 10, 20, "2"); c.r(7, 10, 7, 20, "1"); c.r(10, 10, 10, 20, "3")
c.r(10, 6, 14, 8, "B"); c.r(10, 6, 14, 6, "b"); c.pts("c", (12, 7))
c.r(4, 20, 13, 21, "3"); c.r(4, 20, 13, 20, "2")
c.pts("l", (2, 3), (4, 3), (8, 14), (8, 17))
c.r(5, 22, 12, 22, "x")
O("right_spindle_support_top", c)

# lamp
c = C()
c.ell(8, 6, 5, 4, "4"); c.ell(8, 6, 4, 3, "5"); c.r(5, 3, 11, 3, "4")
c.pts("w", (6, 5), (8, 6), (10, 5), (7, 7), (9, 8)); c.pts("Y", (7, 6), (9, 7), (6, 4), (11, 6))
c.r(5, 9, 10, 9, "3")
c.r(7, 10, 8, 18, "g"); c.r(7, 10, 7, 18, "G"); c.r(8, 10, 8, 18, "h")
c.pts("g", (6, 13), (9, 16), (6, 17)); c.pts("w", (8, 12), (7, 15))
c.r(5, 19, 10, 20, "2"); c.r(5, 19, 10, 19, "1"); c.r(5, 20, 10, 20, "3")
c.r(4, 21, 11, 21, "x")
O("moted_lamp", c)

# nephilim statues
c = C()
c.r(3, 17, 12, 20, "2"); c.r(3, 17, 12, 17, "1"); c.r(3, 20, 12, 20, "3")
c.r(4, 5, 11, 16, "2"); c.r(4, 5, 11, 6, "1"); c.r(4, 5, 4, 16, "1"); c.r(11, 7, 11, 16, "3")
c.r(5, 3, 10, 6, "2"); c.r(5, 3, 10, 3, "1")
c.r(1, 8, 3, 15, "2"); c.r(12, 8, 14, 15, "2"); c.r(1, 8, 1, 15, "1"); c.r(14, 8, 14, 15, "3")
c.r(2, 16, 3, 16, "3"); c.r(12, 16, 13, 16, "3")
c.pts("O", (6, 4), (9, 4), (7, 11), (8, 11))
c.pts("g", (5, 7), (6, 7), (4, 10), (10, 13), (12, 9), (3, 12), (7, 18), (9, 19), (5, 17))
c.pts("G", (5, 8), (11, 13), (2, 11))
c.r(3, 21, 12, 21, "x")
O("nephilim_statue_bethsaida", c)

c = C()
c.r(2, 17, 13, 20, "2"); c.r(2, 17, 13, 17, "c"); c.r(2, 17, 13, 17, "B"); c.r(2, 18, 13, 19, "b")
c.r(2, 20, 13, 20, "3")
c.ell(8, 11, 5, 5, "2"); c.ell(7, 10, 4, 4, "1"); c.ell(8, 11, 5, 5, "2")
c.r(3, 10, 12, 14, "2"); c.r(3, 10, 12, 11, "1"); c.r(12, 11, 12, 14, "3")
c.r(1, 8, 4, 9, "3")  # head
c.r(2, 6, 6, 9, "2"); c.r(2, 6, 6, 6, "1"); c.pts("O", (3, 8), (4, 8))
c.pts("1", (3, 5), (5, 5), (7, 5))  # spines
c.r(12, 12, 15, 15, "3"); c.r(13, 13, 15, 14, "2")  # tail fin
c.pts("O", (6, 12), (9, 13))
c.pts("g", (6, 7), (9, 11), (11, 12), (4, 12), (8, 15), (12, 14)); c.pts("G", (5, 6), (10, 12))
c.pts("w", (4, 18), (9, 19), (12, 18))
c.r(3, 21, 12, 21, "x")
O("nephilim_statue_rermadon", c)

# temple gate SE (stage/loop gate, lilies)
c = C()
c.r(0, 0, 15, 23, "O")
c.r(1, 1, 14, 22, "2")
c.r(0, 14, 15, 23, "1"); c.r(0, 14, 15, 14, "w")
c.r(0, 19, 15, 19, "2"); c.r(0, 23, 15, 23, "3")
c.box(1, 1, 14, 13, "Y"); c.r(2, 2, 13, 12, "o" if False else "2")
c.r(3, 3, 12, 12, "O"); c.r(4, 4, 11, 11, "5")
c.pts("w", (6, 7), (9, 6), (7, 9), (10, 9))
c.pts("w", (3, 16), (4, 15), (5, 16), (11, 20), (12, 19), (13, 20)); c.pts("Y", (4, 16), (12, 20))
c.pts("g", (3, 17), (13, 21), (9, 16))
T("orchid_gate_se", c)

# torchpost
c = C()
c.r(7, 12, 8, 20, "n"); c.r(7, 12, 7, 20, "t")
c.r(5, 8, 6, 12, "n"); c.r(9, 8, 10, 12, "n"); c.r(6, 11, 7, 12, "n"); c.r(8, 11, 9, 12, "n")
c.r(4, 6, 11, 8, "L"); c.r(5, 8, 10, 8, "L"); c.r(4, 6, 11, 6, "l")
c.r(5, 3, 10, 5, "R"); c.r(6, 2, 9, 4, "r"); c.r(7, 0, 8, 3, "y"); c.pts("w", (7, 3), (8, 4))
c.pts("r", (6, 1), (9, 1))
c.r(5, 21, 10, 21, "x"); c.r(5, 20, 10, 20, "N")
O("torchpost", c)

# machines
c = C()
c.r(1, 9, 14, 19, "2"); c.r(1, 9, 14, 10, "1"); c.r(1, 19, 14, 19, "3"); c.r(14, 10, 14, 19, "3")
c.r(2, 6, 5, 9, "3"); c.r(2, 6, 5, 6, "1")
c.r(6, 11, 10, 15, "l"); c.r(6, 11, 10, 11, "w"); c.pts("L", (6, 15), (7, 14), (8, 13), (9, 12), (10, 15))
c.r(10, 12, 13, 14, "L"); c.pts("r", (13, 13), (12, 13))
c.r(11, 16, 13, 18, "O"); c.pts("5", (12, 17))
c.r(1, 20, 14, 20, "x")
O("wire_extruder", c)

# star carousel
c = C()
c.ell(8, 12, 7, 7, "O"); c.ell(8, 12, 6, 6, "2"); c.ell(8, 12, 5, 5, "3"); c.ell(8, 12, 4, 4, "O")
c.ell(8, 12, 3, 3, "G"); c.pts("g", (7, 11), (9, 13))
c.r(7, 4, 7, 7, "G"); c.r(8, 17, 8, 20, "G")
c.pts("1", (3, 9), (4, 8), (5, 7)); c.pts("Y", (3, 14), (13, 14))
T("star_carousel_hatch", c)
KINDS["star_carousel_hatch"] = "terrain"

c = C()
c.r(1, 6, 14, 16, "2"); c.r(1, 6, 14, 7, "1"); c.r(1, 16, 14, 16, "3")
c.r(2, 8, 13, 15, "B"); c.r(2, 8, 13, 8, "b")
for x in range(3, 13, 2):
    c.r(x, 15 - (x % 4) - 2, x, 14, "C")
c.pts("w", (3, 10), (7, 9), (11, 11))
c.r(1, 17, 14, 19, "3"); c.r(2, 17, 13, 17, "2")
c.r(2, 21, 13, 21, "x")
O("star_carousel_pilot_console_n", c)

c = C()
c.r(4, 3, 11, 5, "2"); c.r(4, 3, 11, 3, "1")
c.ell(8, 12, 6, 6, "O"); c.ell(8, 12, 5, 5, "w"); c.ell(8, 12, 4, 4, "g")
c.pts("Y", (6, 10), (7, 11), (10, 12), (9, 14), (7, 14), (11, 11)); c.pts("w", (6, 9), (5, 10))
c.pts("G", (8, 15), (5, 13), (10, 9))
c.r(4, 18, 11, 20, "2"); c.r(4, 18, 11, 18, "1"); c.r(4, 20, 11, 20, "3")
c.r(7, 6, 8, 7, "2")
c.r(3, 21, 12, 21, "x")
O("star_carousel_power_core", c)

c = C()
c.r(1, 3, 14, 18, "O"); c.r(2, 4, 13, 17, "3")
c.r(2, 4, 13, 17, "3")
pts = [(3, 6), (6, 5), (10, 7), (12, 5), (4, 10), (8, 9), (12, 11), (5, 14), (9, 15), (11, 14), (3, 15), (7, 12)]
for x, y in pts:
    c.p(x, y, "w")
c.pts("w", (6, 6), (9, 8)); c.pts("B", (3, 7), (5, 11), (10, 12))
c.r(3, 6, 6, 6, "5") if False else None
c.pts("c", (4, 6), (5, 6), (7, 5), (8, 7), (9, 7), (6, 10), (7, 10), (7, 11), (10, 14), (10, 15))
c.r(2, 4, 13, 4, "1"); c.r(2, 17, 13, 17, "O")
c.r(6, 19, 9, 20, "2"); c.r(4, 21, 11, 21, "x")
O("star_carousel_star_chart_r", c)

c = C()
c.r(7, 1, 8, 5, "L"); c.r(6, 5, 9, 6, "l")
for sx in (3, 7, 11):
    c.r(sx + 1, 7, sx + 1, 10, "C")
    c.r(sx, 11, sx + 2, 14, "2"); c.r(sx, 11, sx + 2, 11, "1"); c.r(sx + 2, 12, sx + 2, 14, "3")
    c.pts("O", (sx + 1, 12), (sx + 1, 13)); c.p(sx + 1, 12, "4")
c.r(4, 7, 4, 10, "5"); c.r(8, 7, 8, 10, "5"); c.r(12, 7, 12, 10, "5")
c.r(5, 21, 10, 21, "x")
O("starship_1_comms", c)

c = C()
c.r(1, 5, 14, 15, "2"); c.r(1, 5, 14, 6, "1"); c.r(1, 15, 14, 15, "3")
c.r(3, 7, 12, 12, "O"); c.r(4, 8, 11, 11, "B"); c.r(4, 8, 11, 8, "b")
c.pts("C", (5, 10), (6, 9), (8, 10), (9, 9), (10, 10)); c.pts("w", (5, 8))
c.pts("4", (2, 13), (4, 13), (11, 13), (13, 13)); c.pts("5", (6, 13), (9, 13))
c.r(2, 16, 13, 19, "3"); c.r(2, 16, 13, 16, "2")
c.r(2, 20, 13, 20, "x")
O("starship_1_pilot_console", c)

c = C()
c.r(1, 3, 14, 16, "O"); c.r(2, 4, 13, 15, "B"); c.r(2, 4, 13, 4, "b")
c.r(3, 6, 6, 9, "O"); c.pts("c", (4, 7), (5, 8))
c.r(8, 6, 12, 7, "O"); c.pts("C", (9, 6), (11, 7)); c.r(8, 9, 12, 13, "O"); c.pts("w", (9, 10), (11, 12), (10, 11))
c.pts("C", (4, 12), (5, 11))
c.r(3, 17, 12, 19, "3"); c.r(3, 17, 12, 17, "2")
c.r(3, 20, 12, 20, "x")
O("golem_interior_screen_s", c)

# shrines
def shrine(part):
    c = C()
    c.r(0, 14, 15, 22, "2"); c.r(0, 14, 15, 15, "1"); c.r(0, 22, 15, 22, "3")
    c.r(0, 18, 15, 18, "3")
    for x in range(1, 15, 3):
        c.r(x, 16, x + 1, 17, "c"); c.p(x, 16, "w")
    if part == "n":
        c.r(3, 3, 12, 13, "2"); c.r(3, 3, 12, 4, "1"); c.r(12, 4, 12, 13, "3")
        c.r(4, 5, 11, 10, "O"); c.r(5, 6, 10, 9, "c"); c.pts("w", (6, 7), (9, 8))
        c.r(4, 11, 11, 12, "3"); c.pts("Y", (5, 12), (7, 12), (9, 12))
    else:
        # kneeling marble eater
        c.r(5, 8, 10, 13, "w"); c.r(5, 8, 5, 13, "w"); c.r(9, 9, 10, 13, "l")
        c.r(6, 4, 9, 7, "w"); c.pts("O", (7, 6), (8, 6)); c.r(6, 4, 9, 4, "l")
        c.r(10, 10, 12, 11, "w"); c.pts("Y", (12, 9), (12, 10))
        c.pts("y", (6, 3), (7, 3), (8, 3), (9, 3))
    return c


O("great_machine_shrine_n", shrine("n"))
O("great_machine_shrine_sw", shrine("sw"))
KINDS.pop("great_machine_shrine_n", None)

# tile_9 crystal branch
c = C()
c.r(7, 14, 8, 20, "1"); c.r(7, 14, 7, 20, "w")
for (x, y0, y1) in [(5, 8, 15), (10, 6, 14), (3, 5, 11), (12, 9, 13), (7, 2, 9), (8, 1, 6)]:
    c.r(x, y0, x, y1, "2"); c.r(x + (1 if x < 12 else 0), y0 + 1, x + (1 if x < 12 else 0), y1, "1")
    c.p(x, y0 - 1 if y0 > 0 else 0, "w")
c.pts("w", (5, 9), (10, 8), (3, 7), (7, 4)); c.pts("4", (6, 12), (9, 11), (4, 9), (11, 11))
c.r(5, 21, 10, 21, "x")
O("tile_9", c)
