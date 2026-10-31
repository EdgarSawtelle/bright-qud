"""Six Day Stilt: the six Argent Father statues, the marble dais around the sacred well, the well
itself and the two seven-tile reliefs. Original art, 16x24 text grids."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402

HUMANOID = set()

KEYS = {
    "terrain/sw/statue1": ("statue_mason", "object"),
    "terrain/sw/statue2": ("statue_knight", "object"),
    "terrain/sw/statue3": ("statue_dagon", "object"),
    "terrain/sw/statue4": ("statue_shekhinah", "object"),
    "terrain/sw/statue5": ("statue_athlete", "object"),
    "terrain/sw/statue6": ("statue_resheph", "object"),
    "items/sw/well": ("sacred_well", "terrain"),
}
for _k in ("n", "ne", "nw", "e", "w", "se", "sw", "south1", "south2",
           "east1", "east2", "east3", "west1", "west2", "west3"):
    KEYS["items/sw/dais/" + _k] = ("dais_" + _k, "terrain")
for _f in (1, 2):
    for _i in range(1, 8):
        KEYS[f"terrain/sw/fresco{_f}-{_i}"] = (f"fresco{_f}_{_i}", "terrain")


# ---------------------------------------------------------------- statues
def plinth(c, tall=False):
    c.r(3, 18, 12, 18, "1")
    c.r(4, 19, 11, 19, "5"); c.p(11, 19, "6"); c.p(4, 19, "4")
    c.r(4, 20, 11, 21, "2"); c.r(4, 20, 4, 21, "1"); c.r(10, 20, 11, 21, "3")
    c.r(2, 22, 13, 22, "3"); c.r(2, 22, 5, 22, "2")
    c.shadow(2, 13, 23)


def shade_box(c, x0, y0, x1, y1):
    """marble block lit top-left, dark bottom-right"""
    c.r(x0, y0, x1, y1, "2")
    c.r(x0, y0, x1, y0, "1"); c.r(x0, y0, x0, y1, "1")
    c.r(x1, y0 + 1, x1, y1, "3"); c.r(x0 + 1, y1, x1, y1, "3")


def head(c, x, y, w=3, h=3):
    """blind marble head: plain face, no eyes"""
    shade_box(c, x, y, x + w - 1, y + h - 1)


def overlay(c, rows, y0=0):
    for dy, r in enumerate(rows):
        assert len(r) == 16, (y0 + dy, r)
        for x, ch in enumerate(r):
            if ch != ".":
                c.p(x, y0 + dy, ch)


def limb(c, x0, y0, x1, y1, w=2, ch="2", hi="1", lo="3"):
    """chunky limb: w x w brush along a line, lit on its upper-left, dark on lower-right"""
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    pts = [(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n)) for i in range(n + 1)]
    for x, y in pts:
        c.r(x, y, x + w - 1, y + w - 1, lo)
    for x, y in pts:
        c.r(x, y, x + w - 2, y + w - 2, ch) if w > 1 else c.p(x, y, ch)
    for x, y in pts:
        c.p(x, y, hi)


def statue_shekhinah():
    c = C()
    overlay(c, [
        ".......45.......",
        "......4554......",
        "......1122......",
        "......1122......",
        ".......112......",
        ".......12.......",
        "...1111112222...",
        "..11111111222...",
        "..11.111122.22..",
        "..11.111322.22..",
        "..11..1132..22..",
        "..11..1232..22..",
        "..11..1132..22..",
        "..22.111122.22..",
        "....11111122....",
        "....45555556....",
        "....1112.222....",
        ".....112.223....",
    ])
    plinth(c)
    return c.out()


def statue_mason():
    c = C()
    overlay(c, [
        "..........11112.",
        "..........11223.",
        "............2...",
        "......3333..2...",
        "......1122..2...",
        "......1122..2...",
        ".......12...2...",
        "...1111112222...",
        "..11111112223...",
        "..11111112223...",
        "...111111223....",
        "...111111223....",
        "...333333333....",
        "...1111.2222....",
        "..1111...2222...",
        "..1111...2223...",
        ".1111.....2223..",
        ".1111.....2223..",
    ])
    c.line(3, 7, 9, 12, "5"); c.line(4, 7, 10, 12, "5"); c.p(3, 7, "4")      # gold sash
    c.r(1, 8, 1, 12, "5"); c.r(1, 12, 4, 12, "5"); c.p(1, 8, "4")           # held set-square
    shade_box(c, 6, 14, 8, 17); c.p(7, 15, "5")                              # block at his feet
    plinth(c)
    return c.out()


def statue_knight():
    c = C()
    overlay(c, [
        ".......54.......",
        ".......55.......",
        "......1112......",
        "......3333......",
        "......1122......",
        "......1122......",
        ".......12.......",
        "..11111112222...",
        ".....1111222....",
        ".....1111222....",
        ".....1113222....",
        ".....1111222....",
        ".....5555555....",
        "....111111222...",
        "....111111222...",
        ".....111.222....",
        ".....111.222....",
        ".....111.223....",
    ])
    # tall kite shield on the left arm, gold rim and boss
    for y in range(8, 15):
        c.r(1, y, 6, y, "2")
    c.r(2, 15, 5, 15, "2"); c.r(3, 16, 4, 16, "2")
    c.r(1, 8, 1, 14, "1"); c.r(6, 9, 6, 14, "3"); c.r(5, 15, 5, 15, "3")
    c.r(1, 8, 6, 8, "5"); c.r(1, 8, 1, 14, "5"); c.r(6, 8, 6, 14, "6"); c.r(2, 14, 5, 14, "6"); c.r(2, 15, 5, 15, "6"); c.r(3, 16, 4, 16, "6")
    c.r(3, 10, 4, 12, "5"); c.p(3, 10, "4"); c.p(3, 11, "4")
    # sword, point down, with gold cross-guard and pommel
    c.r(13, 4, 13, 17, "1"); c.r(14, 6, 14, 17, "3") if False else None
    c.r(12, 7, 14, 7, "5"); c.p(13, 3, "4"); c.p(13, 4, "5")
    c.r(12, 8, 12, 10, "2")        # fist
    plinth(c)
    return c.out()


def statue_dagon():
    c = C()
    overlay(c, [
        "................",
        "......5.55......",
        "......4444......",
        "......1122......",
        "......1122......",
        "......1122......",
        "......1112......",
        ".......12.......",
    ])
    for r in range(8, 18):
        k = (r - 8) // 3
        L, R = 4 - k, 11 + k
        for x in range(L, R + 1):
            t = (x - L) / (R - L)
            c.p(x, r, "1" if t < 0.34 else ("2" if t < 0.72 else "3"))
    for x0, x1 in ((6, 5), (9, 9)):
        c.line(x0, 11, x1, 17, "3")
    c.r(5, 9, 10, 9, "5"); c.p(5, 9, "4")                                     # gold collar
    c.r(1, 17, 14, 17, "5"); c.p(1, 17, "4")
    # right arm flung up in command
    limb(c, 10, 8, 13, 4, 2, "2", "1", "3")
    c.r(13, 1, 15, 3, "1"); c.r(15, 1, 15, 3, "2"); c.p(14, 0, "1"); c.p(13, 1, "3")  # open hand
    # left arm down, hand gathering the robe
    limb(c, 4, 9, 2, 13, 2, "2", "1", "3")
    plinth(c)
    return c.out()


def statue_athlete():
    c = C()
    head(c, 9, 1, 3, 3)
    c.r(9, 1, 11, 1, "3")
    limb(c, 8, 2, 4, 3, 2, "2", "1", "3")                                      # hair tail
    c.r(9, 4, 10, 4, "2")
    c.r(8, 5, 11, 6, "1"); c.r(11, 5, 11, 6, "2")                              # shoulders
    limb(c, 8, 7, 7, 10, 3, "2", "1", "3")                                     # leaning torso
    c.r(6, 10, 9, 11, "1"); c.r(9, 10, 9, 11, "3")
    c.r(5, 12, 9, 12, "5"); c.p(5, 12, "4")                                    # gold-edged drape
    limb(c, 8, 13, 11, 15, 2, "2", "1", "3")                                   # front leg: bent knee
    limb(c, 11, 15, 11, 17, 2, "2", "1", "3")
    c.r(10, 17, 13, 17, "1")
    limb(c, 5, 13, 1, 14, 2, "2", "1", "3")                                    # back leg: trailing, airborne
    limb(c, 1, 14, 0, 16, 2, "2", "1", "3")
    limb(c, 12, 6, 14, 2, 2, "2", "1", "3")                                    # reaching arm
    limb(c, 7, 7, 3, 7, 2, "2", "1", "3")                                      # back arm
    c.shadow(0, 8, 17) if False else None
    plinth(c)
    return c.out()


def statue_resheph():
    c = C()
    overlay(c, [
        "......3333......",
        ".....333333.....",
        ".....3112 33....".replace(" ", "3"),
        ".....3112.3.....".replace(".3.", "33."),
        ".....3112 3.....".replace(" ", "3"),
        ".....3322 3.....".replace(" ", "3"),
        "......3333......",
        ".......22.......",
    ])
    for r in range(8, 18):
        k = (r - 8) // 4
        L, R = 4 - k, 11 + k
        for x in range(L, R + 1):
            t = (x - L) / (R - L)
            c.p(x, r, "1" if t < 0.34 else ("2" if t < 0.72 else "3"))
    c.r(2, 17, 13, 17, "5"); c.p(2, 17, "4")
    c.r(5, 11, 11, 11, "5")
    # right arm raised, one finger up
    limb(c, 11, 9, 13, 6, 2, "2", "1", "3")
    c.r(13, 3, 13, 5, "1"); c.p(13, 2, "1"); c.p(14, 4, "2")
    # open book held at the chest, gold cover
    c.r(1, 10, 8, 15, "5"); c.r(1, 10, 8, 10, "4"); c.r(1, 10, 1, 15, "4"); c.r(1, 15, 8, 15, "6")
    c.r(2, 11, 7, 14, "1"); c.line(4, 11, 4, 14, "3"); c.line(2, 12, 3, 12, "2"); c.line(5, 12, 6, 12, "2"); c.line(5, 13, 6, 13, "2")
    c.r(8, 11, 9, 14, "2")   # fingers
    plinth(c)
    return c.out()


# ---------------------------------------------------------------- well
def sacred_well():
    """Sacred well in the white cathedral: the dais marble runs edge to edge (detail roles), so the fount sits in the
    platform; a gold relief rim and a white lip round a deep blue shaft. Fixed blues: the game's colours would be black."""
    rows = []
    for y in range(24):
        r = ""
        for x in range(16):
            d = math.hypot((x - 7.5) / 7.4, (y - 11.5) / 10.6)
            if d > 1.0:
                c = "4"
            elif d > 0.84:
                c = "1" if (x + y) % 4 else "3"                    # gold relief band
            elif d > 0.72:
                c = "w"                                            # white marble lip
            elif d > 0.46:
                c = "b"
            else:
                c = "d"                                            # the shaft recedes
            r += c
        rows.append(r)
    rows[8] = rows[8][:5] + "B" + rows[8][6:]                      # a glint on the water
    rows[9] = rows[9][:4] + "BB" + rows[9][6:]
    return rows


def _hash(name):
    h = 0
    for ch in name:
        h = (h * 31 + ord(ch)) & 0xFFFF
    return h


def dais(name, edges="", fill="4", shade=()):
    """Flat marble tile: top fills to the borders; gold lines only on the listed outer edges.
    shade: extra (side, role) one-pixel lines for step risers."""
    c = C()
    c.r(0, 0, 15, 23, fill)
    veinc = "5" if fill == "4" else "4"
    h = _hash(name)
    for k in range(3):                                   # a few short, calm veins away from the borders
        x = 3 + (h >> (k * 3)) % 9
        y = 4 + ((h >> (k * 2 + 1)) % 15)
        n = 2 + k % 2
        for j in range(n):
            c.p(x + j, y + j, veinc)
    for side, role, w in shade:
        if side == "N": c.r(0, 0, 15, w - 1, role)
        if side == "S": c.r(0, 24 - w, 15, 23, role)
        if side == "W": c.r(0, 0, w - 1, 23, role)
        if side == "E": c.r(16 - w, 0, 15, 23, role)
    if "N" in edges:
        c.r(0, 0, 15, 0, "2"); c.r(0, 1, 15, 1, "1")
    if "S" in edges:
        c.r(0, 22, 15, 22, "2"); c.r(0, 23, 15, 23, "3")
    if "W" in edges:
        c.r(0, 0, 0, 23, "2"); c.r(1, 1 if "N" in edges else 0, 1, 22 if "S" in edges else 23, "1")
    if "E" in edges:
        c.r(15, 0, 15, 23, "3"); c.r(14, 1 if "N" in edges else 0, 14, 22 if "S" in edges else 23, "2")
    # shade lines for the gold corners
    if "N" in edges and "E" in edges:
        c.p(15, 0, "3")
    if "N" in edges and "W" in edges:
        c.p(0, 0, "2")
    return c.out()


_DAIS = {
    "nw": ("NW", "4", ()), "n": ("N", "4", ()), "ne": ("NE", "4", ()),
    "w": ("W", "4", ()), "e": ("E", "4", ()),
    "sw": ("SW", "4", ()), "se": ("SE", "4", ()),
    "south1": ("SW", "4", ()), "south2": ("SE", "4", ()),
    "west1": ("NWS", "5", ()),
    "west2": ("", "4", (("W", "6", 1),)),
    "west3": ("", "4", (("W", "5", 1), ("S", "5", 2), ("E", "5", 2))),
    "east1": ("NES", "5", (("W", "6", 2),)),
    "east2": ("", "4", (("E", "5", 1),)),
    "east3": ("", "4", (("S", "5", 2), ("E", "5", 1), ("W", "5", 2))),
}

# ---------------------------------------------------------------- reliefs (two 7-tile friezes)
class Wide(C):
    """112 x 24 canvas: seven tiles side by side, sliced at the end."""
    W = 112

    def __init__(s):
        s.g = [["."] * s.W for _ in range(24)]

    def p(s, x, y, ch):
        if 0 <= x < s.W and 0 <= y < 24:
            s.g[y][x] = ch

    def ell(s, cx, cy, rx, ry, ch):
        for y in range(24):
            for x in range(s.W):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    s.p(x, y, ch)

    def slice(s, i):
        return ["".join(r[i * 16:(i + 1) * 16]) for r in s.g]


FT, FB = 4, 19      # field rows


def _frame(c):
    c.r(0, FT, c.W - 1, FB, "2")                       # carved field
    c.r(0, 0, c.W - 1, 0, "1"); c.r(0, 1, c.W - 1, 1, "5"); c.r(0, 2, c.W - 1, 2, "2"); c.r(0, 3, c.W - 1, 3, "3")
    c.r(0, 20, c.W - 1, 20, "1"); c.r(0, 21, c.W - 1, 21, "2"); c.r(0, 22, c.W - 1, 22, "5"); c.r(0, 23, c.W - 1, 23, "3")
    c.r(0, 0, 0, 23, "2"); c.r(c.W - 1, 0, c.W - 1, 23, "3")
    for x in range(0, c.W, 4):                         # faint egg-and-dart rhythm in the top moulding
        c.p(x + 1, 2, "1")


def _put(c, pts, ch):
    for x, y in pts:
        c.p(x, y, ch)


def fig(c, x, base, h, face=1, attr=None, crown=False, robe=False, stride=False):
    """tiny carved figure standing on row `base` (5 px wide, lit left, shaded right)"""
    top = base - h + 1
    pts = {(x + 1 + dx, top + dy) for dx in range(3) for dy in range(3)}     # head
    body = set()
    for y in range(top + 3, base - 2):                                       # torso (top row = shoulders)
        for dx in range(5 if y == top + 3 else 4):
            body.add((x + (0 if y == top + 3 else 0) + dx, y))
    if robe:
        for y in range(base - 2, base + 1):
            f = base - y
            for dx in range(-(2 - f), 4 + (2 - f)):
                body.add((x + dx, y))
    else:
        for y in range(base - 2, base + 1):
            lean = (base - y) if stride else 0
            for dx in (0, 1):
                body.add((x + dx - lean, y))
            for dx in (2, 3):
                body.add((x + dx + lean, y))
        if not stride:
            for y in range(base - 2, base + 1):
                body.discard((x + 1, y)); body.discard((x + 2, y))
            body.add((x, base - 2)); body.add((x + 1, base - 2)); body.add((x + 2, base - 2)); body.add((x + 3, base - 2))
            body.discard((x + 1, base - 1)); body.discard((x + 2, base - 1))
            body.add((x, base - 1)); body.add((x + 3, base - 1))
    allp = pts | body
    _put(c, {(a + 1, b + 1) for a, b in allp}, "3")
    for a, b in allp:
        c.p(a, b, "1" if a < x + 2 else "3")
    for a, b in pts:                                                         # head stays lit, with a dark neck
        c.p(a, b, "1")
    c.p(x + 2, top + 3, "3")
    fx = x + 4
    if attr == "raise":
        _put(c, [(fx, top + 4), (fx, top + 3), (fx, top + 2), (fx, top + 1)], "1")
    if attr == "point":
        _put(c, [(fx + d, top + 4) for d in range(0, 5)], "1")
    if attr == "hammer":
        _put(c, [(fx, top + 5), (fx, top + 4), (fx, top + 3), (fx, top + 2), (fx - 1, top + 1), (fx, top + 1), (fx + 1, top + 1)], "1")
    if attr == "spear":
        _put(c, [(fx, y) for y in range(top - 2, base + 1)], "1")
        _put(c, [(fx, top - 3)], "5")
    if attr == "shield":
        c.r(fx, top + 4, fx + 2, top + 8, "3"); c.r(fx, top + 4, fx + 1, top + 7, "1"); c.p(fx, top + 5, "5")
    if attr == "book":
        c.r(fx - 1, top + 4, fx + 1, top + 6, "5"); c.p(fx, top + 5, "4")
    if crown:
        _put(c, [(x + 1, top - 1), (x + 2, top - 2), (x + 3, top - 1), (x + 2, top - 1)], "5")
    if attr == "basket":
        c.r(fx, top + 5, fx + 2, top + 6, "3")


def _stars(c, pts):
    for x, y in pts:
        c.p(x, y, "4")


def _sun(c, cx, cy, r, rays, ring=True):
    for a in range(rays):
        t = a * 2 * math.pi / rays
        for d in range(int(r) + 2, int(r) + 5):
            x, y = round(cx + math.cos(t) * d * 1.3), round(cy + math.sin(t) * d)
            if FT <= y <= FB:
                c.p(x, y, "5")
    c.ell(cx, cy, r * 1.3, r, "5")
    c.ell(cx, cy, r * 1.3 - 1.3, r - 1.1, "2" if ring else "4")


def fresco_joining():
    """The Sacred Joining: five Fathers follow Shekhinah towards the radiant Kasaphescence."""
    c = Wide()
    _frame(c)
    c.r(0, 19, c.W - 1, 19, "3")                       # ground ledge
    _stars(c, [(6, 6), (19, 8), (29, 5), (38, 7), (47, 5), (58, 8), (64, 5), (73, 7), (9, 11), (33, 12), (51, 11)])
    kinds = [("hammer", False, False), ("shield", False, False), ("raise", True, False), ("spear", False, False), ("book", True, False)]
    xs = [4, 14, 24, 34, 44]
    hs = [10, 11, 10, 9, 10]
    for x, h, (a, robe, _) in zip(xs, hs, kinds):
        fig(c, x, 18, h, 1, a, robe=robe)
    fig(c, 57, 18, 14, 1, "point", crown=True)         # Shekhinah, taller, diadem, hand out to Her
    # the Kasaphescence: a slender luminous figure, arms spread, in a halo and rays
    for k in range(-4, 5):
        t = k * 0.36 - math.pi / 2
        for d in range(9, 20, 2):
            x, y = round(93 + math.cos(t) * d * 1.5), round(12 + math.sin(t) * d)
            if FT + 1 <= y <= FB - 1:
                c.p(x, y, "5")
    for y in range(9, 19):
        w = 1 + (y - 9) // 3
        c.r(93 - w, y, 93 + w, y, "1"); c.r(93, y, 93 + w, y, "3") if False else None
    c.r(93, 9, 94, 18, "1")
    c.r(85, 11, 101, 11, "1"); c.r(85, 12, 101, 12, "3")
    c.ell(93, 6.5, 3.4, 3.4, "5"); c.ell(93, 6.5, 2.2, 2.2, "1")
    c.ell(93, 6.5, 1.0, 1.0, "3") if False else None
    # chrome machines unfolding from Her: small gears
    for gx, gy in ((75, 15), (109, 15), (79, 11)):
        c.r(gx, gy, gx + 2, gy + 2, "1"); c.p(gx + 1, gy + 1, "3")
        _put(c, [(gx + 1, gy - 1), (gx - 1, gy + 1), (gx + 3, gy + 1), (gx + 1, gy + 3)], "5")
    _put(c, [(104, 15), (106, 14), (104, 12)], "4")
    return c


def fresco_edification():
    """The Edification: Shekhinah overlooks spires, towers and a bridge raised on the new world."""
    c = Wide()
    _frame(c)
    c.r(0, 19, c.W - 1, 19, "3")
    _stars(c, [(30, 6), (45, 5), (60, 6), (78, 5), (97, 6), (108, 8), (6, 6), (24, 9)])
    _sun(c, 5, 9, 2.4, 8)
    fig(c, 17, 18, 14, 1, "point", crown=True, robe=True)   # Shekhinah gazing east
    # workers hauling blocks
    for x, a in ((30, "basket"), (38, "hammer"), (45, "basket")):
        fig(c, x, 18, 7, 1, a)
    c.r(33, 17, 35, 18, "1"); c.r(42, 17, 43, 18, "1")
    # mountains with spires
    for cx, top, half in ((58, 8, 12), (78, 11, 10)):
        for y in range(top, 19):
            hw = (y - top) * half / (19 - top)
            for x in range(int(cx - hw), int(cx + hw) + 1):
                c.p(x, y, "1" if x < cx else "3")
        c.p(cx, top, "1")
    for sx, st, sh in ((58, 3, 5), (78, 6, 5), (52, 11, 3)):
        c.r(sx, st, sx, st + sh, "1"); c.p(sx, st - 1, "5"); c.p(sx, st - 2, "4")
    # bridge arches over a river on the right, towers beyond
    for x in range(84, 112):
        c.p(x, 18, "3")
    for ax in (86, 94):
        for dx in range(-3, 4):
            y = 17 - int(round(math.sqrt(max(0, 9 - dx * dx))))
            c.p(ax + dx + 3, y + 1, "1")
        c.r(ax, 17, ax, 18, "1"); c.r(ax + 6, 17, ax + 6, 18, "1")
    c.r(84, 12, 102, 12, "1")                            # deck
    for tx, th in ((103, 9), (107, 6)):
        c.r(tx, FB - th, tx + 2, 18, "1"); c.r(tx + 2, FB - th, tx + 2, 18, "2")
        c.p(tx + 1, FB - th - 1, "5"); c.p(tx + 1, FB - th - 2, "4")
    return c


SPRITES = {}
for _n, _f in list(globals().items()):
    if _n.startswith(("statue_", "sacred_")) and callable(_f):
        SPRITES[_n] = _f()
for _k, (_e, _fl, _sh) in _DAIS.items():
    _ed = _e.replace("NW", "N,W").replace("NE", "N,E").replace("SW", "S,W").replace("SE", "S,E")
    SPRITES["dais_" + _k] = dais(_k, "".join(ch for ch in _e if ch in "NSEW"), _fl, _sh)

for _f, _fn in ((1, fresco_joining), (2, fresco_edification)):
    _c = _fn()
    for _i in range(7):
        SPRITES[f"fresco{_f}_{_i + 1}"] = _c.slice(_i)
