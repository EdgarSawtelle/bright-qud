"""Terrain batch 4: ground decorations, plants, trees, ruins and world-map tiles.

Sprites are drawn with a tiny canvas (pixel/rect/disc/line helpers) so edges and tiling stay exact.
Roles 1-3 = region main colour, 4-6 = detail colour; fixed letters only for land, ink and sparkle.
"""
import math
import random

from terrain_keys import BATCH_KEYS

KEYS = BATCH_KEYS[4]


class Cv:
    def __init__(self, fill="."):
        self.g = [[fill] * 16 for _ in range(24)]

    def px(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < 16 and 0 <= y < 24:
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < 16 and 0 <= y < 24 else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.px(x, y, c)

    def disc(self, cx, cy, rx, ry, c, shade=None):
        """Filled ellipse; shade=(light, mid, dark) gives top-left light / bottom-right dark."""
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1.0:
                    if shade:
                        t = ((x - cx) / rx + (y - cy) / ry) / 2
                        c = shade[0] if t < -0.28 else (shade[2] if t > 0.32 else shade[1])
                    self.px(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
        for i in range(n + 1):
            t = i / n
            self.px(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)

    def shadow(self, cx, y, w):
        for x in range(int(cx - w), int(cx + w) + 1):
            if self.get(x, y) == ".":
                self.px(x, y, "x")

    def rows(self):
        return ["".join(r) for r in self.g]


def speckle(c, rnd, n, cols, y0=0, y1=23):
    for _ in range(n):
        c.px(rnd.randrange(16), rnd.randrange(y0, y1 + 1), rnd.choice(cols))


# ------------------------------------------------------------------ plants / tall

def bending_gjaus():
    c = Cv()
    for i, (x0, ph, top) in enumerate(((4, 0.0, 5), (8, 2.0, 2), (12, 4.0, 6))):
        for y in range(20, top - 1, -1):
            k = 20 - y
            x = x0 + 1.6 * math.sin(k * 0.55 + ph) * (0.5 + k / 30)
            c.px(x - 1, y, "1")
            c.px(x, y, "2")
            c.px(x + 1, y, "3")
            if k % 5 == 2:  # nodes in detail colour
                c.px(x - 1, y, "4"); c.px(x, y, "5"); c.px(x + 1, y, "6")
        xt = x0 + 1.6 * math.sin((20 - top) * 0.55 + ph) * (0.5 + (20 - top) / 30)
        c.line(xt, top, xt + (2 if i != 1 else -2), top - 2, "1")
        c.line(xt, top, xt + (-2 if i != 1 else 2), top - 1, "2")
    for (x, y) in ((2, 9), (14, 11), (6, 3), (10, 7), (13, 3), (3, 15)):
        c.px(x, y, "w"); c.px(x + 1, y, "c") if c.get(x + 1, y) == "." else None
    c.shadow(8, 21, 6)
    c.shadow(8, 22, 4)
    return c.rows()


def chavvah_chime():
    c = Cv()
    for cx, top, w, bot in ((3, 9, 2, 20), (8, 3, 2, 20), (13, 11, 2, 20)):
        for y in range(top, bot + 1):
            ww = w if y > top + w else (y - top)
            for x in range(cx - ww, cx + ww + 1):
                c.px(x, y, "1" if x < cx - ww + 1 and ww > 0 else ("3" if x >= cx + ww - 0 and ww > 0 else "2"))
        for y in range(top + 3, bot - 1):
            c.px(cx, y, "4" if y % 4 else "w")
    for (x, y) in ((1, 6), (15, 8), (6, 1), (11, 2), (2, 14), (14, 15), (9, 13)):
        c.px(x, y, "c" if (x + y) % 2 else "4")
    c.shadow(8, 21, 7)
    c.shadow(8, 22, 5)
    return c.rows()


def coral_ball():
    c = Cv()
    c.disc(8, 12, 6.5, 6.5, "2", ("1", "2", "3"))
    rnd = random.Random(3)
    for (x, y) in ((6, 9), (10, 10), (8, 13), (5, 13), (11, 14), (7, 16), (9, 7)):
        c.px(x, y, "6"); c.px(x - 1, y - 1, "4") if c.get(x - 1, y - 1) not in ".x" else None
    c.px(6, 8, "w"); c.px(7, 7, "w")
    c.shadow(8, 20, 6)
    c.shadow(8, 21, 4)
    return c.rows()


def finger_root():
    c = Cv()
    c.disc(8, 19, 6, 2, "e")
    for x in range(3, 14):
        c.px(x, 19, "E") if x % 3 == 0 else None
    for (x0, x1, y1) in ((8, 8, 2), (6, 3, 5), (10, 13, 5), (5, 1, 10), (11, 15, 10), (7, 5, 3), (9, 11, 3)):
        c.line(x0, 19, x1, y1, "2")
        c.line(x0 + 1, 19, x1 + (1 if x1 >= x0 else 0), y1 + 2, "3")
        c.line(x0 - 1, 19, x1 - 1, y1 + 1, "1") if x1 <= x0 else None
        c.px(x1, y1, "w")
    c.shadow(8, 21, 6)
    return c.rows()


def hex_small():
    c = Cv()
    def hexa(cx, top, h):
        for y in range(top, top + h):
            t = y - top
            w = min(3, 1 + t)
            for x in range(cx - w, cx + w + 1):
                c.px(x, y, "1" if x == cx - w else ("3" if x == cx + w else "2"))
        c.px(cx - 1, top + 1, "4"); c.px(cx, top + h // 2, "4"); c.px(cx - 1, top + 2, "w")
    hexa(5, 9, 11)
    hexa(11, 11, 9)
    hexa(8, 5, 15)
    for (x, y) in ((2, 19), (4, 20), (13, 19), (14, 20), (9, 20), (7, 20)):
        c.px(x, y, "g" if (x + y) % 3 else "G")
    c.shadow(8, 21, 7)
    return c.rows()


def monument():
    c = Cv()
    for y in range(3, 21):
        l = 3 + (0 if y > 8 else (8 - y) // 2)
        r = 12 - (0 if y > 10 else (10 - y) // 2)
        for x in range(l, r + 1):
            c.px(x, y, "1" if x <= l + 1 else ("3" if x >= r - 1 else "2"))
    for (x, y) in ((8, 8), (9, 8), (10, 9), (10, 10), (10, 11), (9, 12), (8, 12), (7, 12), (6, 11), (6, 10), (6, 9), (7, 8), (7, 9), (8, 10), (8, 14), (8, 15), (7, 16), (9, 16)):
        c.px(x, y, "6")
    c.px(8, 5, "5"); c.px(7, 4, "1")
    c.rect(2, 20, 4, 21, "3"); c.rect(11, 20, 13, 21, "3"); c.px(2, 20, "1")
    c.shadow(8, 21, 7); c.shadow(8, 22, 5)
    return c.rows()


def reef_organic_odd():
    c = Cv()
    for y in range(11, 21):
        w = 2 if y < 16 else 3
        for x in range(8 - w, 8 + w + 1):
            c.px(x, y, "1" if x == 8 - w else ("3" if x == 8 + w else "2"))
    for y in (13, 16, 19):
        c.rect(5, y, 11, y, "3") if y != 13 else c.rect(6, y, 10, y, "3")
    for dx, ex, ey in ((-1, -5, 4), (1, 5, 4), (0, 0, 3), (-1, -3, 5), (1, 3, 5)):
        c.line(8 + dx, 11, 8 + ex, ey + 1, "5")
        c.px(8 + ex, ey, "4"); c.px(8 + ex, ey - 1, "w") if abs(ex) > 3 else None
    c.px(8, 9, "4")
    c.shadow(8, 21, 6); c.shadow(8, 22, 4)
    return c.rows()


def tile_tombstone():
    c = Cv()
    for y in range(6, 21):
        w = 4 if y > 9 else {6: 1, 7: 2, 8: 3, 9: 3}[y]
        for x in range(8 - w, 8 + w + 1):
            c.px(x, y, "l" if x <= 8 - w + 1 else ("L" if x >= 8 + w - 1 else "l"))
    c.rect(6, 20, 10, 20, "L")
    c.line(8, 8, 8, 14, "1"); c.line(6, 10, 10, 10, "1")  # sun/cross glyph in gold
    c.px(8, 12, "2"); c.px(6, 8, "w")
    for x in (2, 3, 5, 11, 12, 14):
        c.px(x, 21, "g"); c.px(x, 20, "G") if x % 2 else c.px(x, 19, "4")
    c.shadow(8, 22, 6)
    return c.rows()


def tree_crystal():
    c = Cv()
    c.rect(7, 13, 8, 21, "N"); c.px(7, 14, "n"); c.px(7, 17, "n")
    c.line(7, 15, 3, 10, "4"); c.line(8, 14, 12, 9, "4"); c.line(7, 12, 5, 7, "4"); c.line(8, 12, 10, 5, "4")
    c.line(7, 12, 8, 4, "4")
    rnd = random.Random(4)
    for (cx, cy, r) in ((3, 8, 3), (12, 7, 3), (6, 5, 3), (10, 4, 3), (8, 9, 3), (8, 2, 2)):
        c.disc(cx, cy, r, r, "2", ("1", "2", "3"))
    for _ in range(14):
        x, y = rnd.randrange(1, 15), rnd.randrange(1, 11)
        if c.get(x, y) in "123":
            c.px(x, y, "w" if rnd.random() < 0.6 else "6")
    c.shadow(8, 22, 5)
    return c.rows()


def urberry_bush():
    c = Cv()
    c.disc(8, 14, 7, 5.5, "2", ("1", "2", "3"))
    c.disc(5, 12, 3.5, 3, "2", ("1", "2", "3")); c.disc(11, 12, 3.5, 3, "2", ("1", "2", "3"))
    for (x, y) in ((5, 11), (9, 10), (12, 12), (7, 15), (11, 16), (4, 15), (8, 13)):
        c.px(x, y, "4"); c.px(x + 1, y, "5"); c.px(x, y + 1, "6")
    for (x, y) in ((6, 9), (10, 10), (3, 14)):
        c.px(x, y, "G")
    c.shadow(8, 20, 7); c.shadow(8, 21, 5)
    return c.rows()


def witchwood():
    c = Cv()
    c.rect(7, 12, 8, 21, "1"); c.rect(8, 12, 8, 21, "2"); c.rect(9, 14, 9, 21, "3")
    for y in (14, 17, 19):
        c.px(7, y, "3"); c.px(8, y + 1, "3")
    for (x1, y1) in ((2, 6), (14, 6), (4, 2), (12, 2), (8, 1)):
        c.line(8, 12, x1, y1, "1")
        for k in range(-2, 3):
            c.line(x1, y1, x1 + k * 1.5, y1 - 2 + abs(k) * 0.6, "5" if k else "4")
    c.disc(8, 8, 4.5, 3, "5", ("4", "5", "6"))
    for (x, y) in ((3, 4), (12, 4), (8, 5), (6, 8), (10, 9)):
        c.px(x, y, "4")
    c.shadow(8, 22, 5)
    return c.rows()


def yempuris_phi():
    c = Cv()
    pts = []
    for i in range(1, 22):
        r = 1.45 * math.sqrt(i)
        a = i * 2.39996
        pts.append((8 + r * math.cos(a), 11 + r * math.sin(a) * 0.95, i))
    for x, y, i in sorted(pts, key=lambda p: -p[2]):
        rr = 0.9 + i / 14
        c.disc(x, y, rr, rr, "2", ("1", "2", "3"))
    for x, y, i in pts:
        if i < 7:
            c.px(x, y, "4")
    c.px(8, 11, "M") if False else None
    c.shadow(8, 21, 6)
    return c.rows()


# ------------------------------------------------------------------ flat decorations

def chavvah_soft():
    rnd = random.Random(7)
    c = Cv()
    c.rect(0, 0, 15, 23, "e")
    speckle(c, rnd, 22, ["E", "3"])
    for k in range(9):
        a = k * 0.7 + 0.2
        x, y = 8.0, 12.0
        for s in range(14):
            a += rnd.uniform(-0.35, 0.35)
            x += math.cos(a) * 1.0; y += math.sin(a) * 1.2
            c.px(x, y, "2"); c.px(x + 1, y, "3")
            if s < 5:
                c.px(x, y, "1")
    for (rx, ry, col) in ((5, 5, "5"), (3, 3, "4"), (1.5, 1.5, "w")):
        c.disc(8, 12, rx, ry, col)
    c.line(8, 4, 8, 20, "5") if False else None
    return c.rows()


def desert():
    rnd = random.Random(11)
    c = Cv()
    for y in range(24):
        for x in range(16):
            band = (y + int(2.2 * math.sin(x * 0.45 + y * 0.2))) % 8
            c.px(x, y, "1" if band in (0, 1, 2) else ("2" if band in (3, 4, 5) else "3"))
    for y in range(24):
        for x in range(16):
            if ((y + int(2.2 * math.sin(x * 0.45 + y * 0.2))) % 8) == 6:
                c.px(x, y, "3")
    # salt cracks
    for (x, y) in ((3, 3), (4, 4), (5, 4), (6, 5), (11, 12), (12, 13), (13, 13), (2, 18), (3, 19), (4, 19), (9, 8)):
        c.px(x, y, "6")
    speckle(c, rnd, 14, ["w"])
    return c.rows()


def fresco1():
    c = Cv()
    c.rect(0, 0, 15, 23, "2")
    c.rect(0, 0, 15, 3, "1")
    c.rect(0, 20, 15, 23, "3")
    c.rect(0, 4, 0, 19, "1"); c.rect(15, 4, 15, 19, "3")
    c.rect(2, 6, 13, 17, "3"); c.rect(3, 7, 12, 16, "2")
    # eight-pointed star orchid glyph
    c.line(8, 7, 8, 16, "4"); c.line(3, 11, 12, 11, "4")
    c.line(5, 8, 11, 15, "5"); c.line(11, 8, 5, 15, "5")
    c.disc(8, 11, 1.6, 1.6, "6"); c.px(8, 11, "w")
    for x in (1, 14):
        c.px(x, 8, "5"); c.px(x, 15, "5")
    return c.rows()


def hills_art(c):
    pass


def _ground(seed=5, amt=26):
    rnd = random.Random(seed)
    c = Cv()
    c.rect(0, 0, 15, 23, "e")
    speckle(c, rnd, amt, ["E", "E", "e"])
    return c, rnd


def historic_hills():
    c, rnd = _ground(1)
    for (cx, cy, rx, ry) in ((4, 17, 6, 6), (12, 14, 6, 7), (8, 21, 8, 5)):
        c.disc(cx, cy, rx, ry, "2", ("1", "2", "3"))
    for (x, y) in ((3, 14), (11, 10), (9, 17), (5, 19), (14, 15)):
        c.px(x, y, "4"); c.px(x + 1, y + 1, "5")
    for y in range(1, 24):
        for x in range(16):
            if c.get(x, y) in "123" and c.get(x, y - 1) in "e":
                c.px(x, y - 1, "3")
    c.rect(0, 0, 15, 4, ".")
    for x in range(16):
        for y in range(0, 5):
            if c.get(x, y) == "e":
                c.px(x, y, ".")
    return c.rows()


def _house(c, x0, y0, w, h, roof=2):
    c.rect(x0, y0 + roof + 1, x0 + w - 1, y0 + roof + h, "2")
    c.rect(x0, y0 + roof + h, x0 + w - 1, y0 + roof + h, "3")
    c.rect(x0, y0 + roof + 1, x0, y0 + roof + h - 1, "1")
    for i in range(roof + 1):
        c.rect(x0 - 1 + i * 0, y0 + roof - i, x0 + w, y0 + roof - i, "5" if i % 2 == 0 else "4")
    c.rect(x0 - 1, y0 + roof, x0 + w, y0 + roof, "6")
    c.px(x0 + w // 2, y0 + roof + h - 1, "O")
    c.px(x0 + w // 2, y0 + roof + h - 2, "O")
    if w > 4:
        c.px(x0 + 1, y0 + roof + 2, "O")


def historic_building():
    c, rnd = _ground(2)
    for x in range(16):
        c.px(x, 0, "."); c.px(x, 1, ".")
    _house(c, 1, 3, 6, 5, 2)
    _house(c, 9, 6, 6, 5, 2)
    _house(c, 3, 13, 8, 6, 3)
    return c.rows()


def historic_pantheon():
    c, rnd = _ground(3)
    c.rect(1, 20, 14, 21, "3")
    c.rect(2, 18, 13, 19, "1")
    for x in (3, 6, 9, 12):
        c.rect(x, 10, x + 1, 17, "2"); c.px(x, 10, "1"); c.rect(x + 1, 11, x + 1, 17, "3")
    c.rect(2, 8, 13, 9, "1"); c.rect(2, 9, 13, 9, "3")
    for i in range(6):
        c.rect(2 + i + 1, 7 - i, 13 - i - 1, 7 - i, "5" if i % 2 == 0 else "4")
    c.disc(8, 6, 1.2, 1.2, "6")
    return c.rows()


def historic_tower():
    c, rnd = _ground(4)
    for y in range(4, 21):
        for x in range(5, 11):
            c.px(x, y, "1" if x == 5 else ("3" if x >= 10 else "2"))
    for x in (4, 6, 8, 10):
        c.rect(x, 2, x + 1, 4, "2"); c.px(x, 2, "1")
    c.rect(4, 4, 11, 4, "3")
    c.rect(7, 8, 8, 10, "O"); c.rect(7, 14, 8, 15, "O")
    c.rect(7, 18, 8, 20, "6")
    for y in (7, 12, 17):
        c.rect(5, y, 10, y, "3") if False else None
    c.rect(3, 20, 12, 21, "3")
    c.px(8, 1, "4"); c.rect(8, 0, 11, 0, "5") if False else None
    c.px(8, 0, "5")
    return c.rows()


def mover_chute(top):
    c = Cv()
    c.rect(0, 0, 15, 23, "e")
    # wooden bed in detail colours, blue rails
    c.rect(3, 0, 12, 23, "5")
    for y in range(0, 24, 4):
        c.rect(3, y, 12, y, "6"); c.rect(4, y + 1, 11, y + 1, "4")
    c.rect(3, 0, 4, 23, "2"); c.rect(11, 0, 12, 23, "2")
    c.rect(3, 0, 3, 23, "1"); c.rect(12, 0, 12, 23, "3")
    if top:
        c.rect(0, 0, 15, 7, "e")
        c.rect(2, 0, 13, 1, "3"); c.rect(1, 2, 14, 7, "3")
        c.rect(3, 3, 12, 7, "O")
        c.rect(2, 2, 13, 2, "1")
        c.rect(0, 8, 2, 16, "O") if False else None
    else:
        c.rect(0, 16, 15, 23, "e")
        c.rect(3, 16, 12, 21, "O")
        c.rect(2, 15, 13, 15, "1"); c.rect(1, 16, 14, 16, "2")
        c.rect(2, 22, 13, 23, "3")
    for y in range(8, 16) if top else range(3, 12):
        c.px(7, y, "4" if y % 3 else "w") if False else None
    # opening on the left side: dark mouth
    c.rect(0, 9, 3, 15, "O")
    c.rect(0, 8, 3, 8, "1")
    c.rect(0, 16, 3, 16, "3")
    c.px(1, 12, "c")
    return c.rows()


def normality_field():
    c = Cv()
    for y in range(24):
        for x in range(16):
            a, b = (x + y) % 6, (x - y) % 6
            c.px(x, y, "2" if a == 0 or b == 0 else ".")
    for y in range(0, 24, 6):
        for x in range(16):
            if (x + y) % 6 == 0:
                c.px(x, y, "1")
    for (x, y) in ((6, 0), (0, 6), (12, 6), (6, 12), (0, 18), (12, 18), (6, 24)):
        c.px(x, y, "1")
    return c.rows()


def reef_both_even():
    c = Cv()
    rnd = random.Random(9)
    c.rect(0, 0, 15, 23, "e")
    speckle(c, rnd, 18, ["E"])
    # palladium struts: a lattice of steel beams
    for (x0, y0, x1, y1) in ((0, 5, 15, 5), (0, 17, 15, 17), (3, 0, 3, 23), (12, 0, 12, 23)):
        c.line(x0, y0, x1, y1, "l")
        c.line(x0 + (1 if x0 == x1 else 0), y0 + (1 if y0 == y1 else 0), x1 + (1 if x0 == x1 else 0), y1 + (1 if y0 == y1 else 0), "L")
    c.line(3, 5, 12, 17, "L"); c.line(12, 5, 3, 17, "L")
    for (x, y) in ((3, 5), (12, 5), (3, 17), (12, 17), (7, 11)):
        c.disc(x, y, 1.2, 1.2, "w")
    # coral growth
    for (x, y) in ((7, 11), (3, 17), (12, 5), (9, 17), (6, 5)):
        c.disc(x, y, 2.2, 2.2, "4", ("4", "4", "6"))
        c.px(x - 1, y - 1, "w"); c.px(x, y + 1, "5")
    for (x, y) in ((7, 11), (3, 17), (12, 5)):
        for dx, dy in ((0, -3), (3, 0), (-3, 0), (0, 3)):
            c.px(x + dx, y + dy, "1")
    return c.rows()


def spindle_bottom():
    c = Cv()
    rnd = random.Random(12)
    c.rect(0, 0, 15, 23, "e")
    speckle(c, rnd, 30, ["E", "E", "3"])
    for y in range(0, 24):
        w = 1 + y // 6
        for x in range(8 - w, 8 + w):
            c.px(x, y, "1" if x < 8 - w + 1 else ("3" if x >= 8 + w - 1 else "2"))
    c.line(8, 0, 8, 23, "w") if False else None
    for y in range(2, 22, 5):
        c.px(8 - 1 - y // 6, y, "w")
    # tomb-dressed earth: stone slabs around the base
    for (x, y) in ((1, 21), (3, 22), (11, 21), (13, 22), (0, 17), (14, 18)):
        c.rect(x, y, x + 2, y + 1, "L"); c.px(x, y, "l")
    for y in range(18, 24):
        w = 1 + y // 6
        c.rect(8 - w - 1, y, 8 - w - 1, y, "4") if False else None
    c.rect(2, 23, 13, 23, "4")
    return c.rows()


def star_orchid_lily():
    c = Cv()
    rnd = random.Random(14)
    c.rect(0, 0, 15, 23, ".")
    def lily(cx, cy, r):
        for k in range(5):
            a = k * 2 * math.pi / 5 + 0.4
            c.disc(cx + math.cos(a) * r * 0.9, cy + math.sin(a) * r * 0.9, r * 0.75, r * 0.65, "2", ("1", "2", "3"))
        for k in range(5):
            a = k * 2 * math.pi / 5 + 0.4 + 0.63
            c.px(cx + math.cos(a) * r * 1.0, cy + math.sin(a) * r * 1.0, "3")
        for k in range(5):
            a = k * 2 * math.pi / 5 - 1.3
            c.line(cx, cy, cx + math.cos(a) * 3.2, cy + math.sin(a) * 3.2, "5")
            c.px(cx + math.cos(a) * 3.8, cy + math.sin(a) * 3.8, "4")
        c.disc(cx, cy, 1.4, 1.4, "6"); c.px(cx, cy, "w")
    lily(5, 7, 3.4)
    lily(11, 16, 3.6)
    lily(4, 20, 2.2) if False else None
    return c.rows()


def tile_jungleleft():
    rnd = random.Random(21)
    c = Cv()
    c.rect(0, 0, 15, 23, "3")
    blobs = [(rnd.uniform(0, 15), rnd.uniform(0, 23), rnd.uniform(2.4, 4)) for _ in range(16)]
    for cx, cy, r in sorted(blobs, key=lambda b: b[1]):
        if cx > 11 and rnd.random() < 0.5:
            continue
        c.disc(cx, cy, r, r * 0.85, "2", ("1", "2", "3"))
        c.line(cx - r * 0.6, cy + r * 0.7, cx + r * 0.6, cy + r * 0.7, "3")
    for _ in range(10):
        c.px(rnd.randrange(16), rnd.randrange(24), "1")
    return c.rows()


def ruins_deep():
    rnd = random.Random(31)
    c = Cv()
    c.rect(0, 0, 15, 23, "h")
    for y in range(24):
        for x in range(16):
            r = rnd.random()
            c.px(x, y, "g" if r < 0.35 else ("G" if r < 0.45 else "h"))
    # peeking ruins: arch corner top-left, balustrade bottom-right
    c.rect(0, 0, 3, 8, "2"); c.rect(0, 0, 0, 8, "1"); c.rect(3, 0, 3, 8, "3")
    c.rect(4, 0, 9, 2, "2"); c.rect(4, 0, 9, 0, "1"); c.rect(4, 2, 9, 2, "3")
    c.rect(1, 3, 2, 7, "O") if False else None
    for x in (9, 11, 13):
        c.rect(x, 17, x + 1, 22, "c"); c.px(x, 17, "w"); c.px(x + 1, 22, "d")
    c.rect(8, 16, 15, 16, "1"); c.rect(8, 23, 15, 23, "3")
    for (x, y) in ((1, 13), (2, 12), (12, 8), (13, 9)):
        c.px(x, y, "M"); c.px(x - 1, y, "m"); c.px(x + 1, y, "m"); c.px(x, y - 1, "m")
    # leaves over the stonework
    for (x, y, r) in ((4, 5, 2.5), (8, 20, 2.5), (14, 4, 2.2), (5, 14, 2.6), (10, 11, 2.4)):
        c.disc(x, y, r, r * 0.8, "g", ("G", "g", "h"))
    return c.rows()


# ------------------------------------------------------------------ rivers and lakes

def _water_fill(c, wmask, wlight="1", wmid="2", wdark="3", seed=1):
    rnd = random.Random(seed)
    for y in range(24):
        for x in range(16):
            if wmask[y][x]:
                c.px(x, y, wmid)
    for y in range(24):
        for x in range(16):
            if wmask[y][x]:
                edge = any(not (0 <= x + dx < 16 and 0 <= y + dy < 24) or not wmask[y + dy][x + dx]
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))
                           if 0 <= x + dx < 16 and 0 <= y + dy < 24)
                if edge:
                    c.px(x, y, wdark)
    for _ in range(34):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 22)
        if all(wmask[y][x + k] and c.get(x + k, y) == wmid for k in range(3)):
            c.px(x, y, wlight); c.px(x + 1, y, wlight)


def _land(c, kind, seed):
    rnd = random.Random(seed)
    if kind == "grass":
        cols = ("g", "g", "h", "G")
        base = "g"
    else:
        cols = ("L", "L", "l", "e")
        base = "L"
    for y in range(24):
        for x in range(16):
            c.px(x, y, base if rnd.random() < 0.6 else rnd.choice(cols))
    if kind == "rock":
        for _ in range(4):
            x, y = rnd.randrange(1, 13), rnd.randrange(1, 21)
            c.rect(x, y, x + 2, y + 1, "l"); c.rect(x + 1, y + 1, x + 2, y + 1, "e")


def river(sides, kind="grass", seed=1, end=False):
    c = Cv()
    _land(c, kind, seed)
    w = [[False] * 16 for _ in range(24)]
    def rect(x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                if 0 <= x < 16 and 0 <= y < 24:
                    w[y][x] = True
    cx0, cx1, cy0, cy1 = 5, 10, 9, 14
    rect(cx0 + 1, cy0 + 1, cx1 - 1, cy1 - 1)
    if end:
        rect(cx0, cy0 + 1, cx1, cy1 - 1)
    if "n" in sides: rect(cx0, 0, cx1, cy0 + 1)
    if "s" in sides: rect(cx0, cy1 - 1, cx1, 23)
    if "w" in sides: rect(0, cy0, cx0 + 1, cy1)
    if "e" in sides: rect(cx1 - 1, cy0, 15, cy1)
    if not sides or not (set(sides) & {"n", "s"}) or True:
        # round the central blob unless it connects to a straight neighbour
        for (x, y) in ((cx0, cy0), (cx1, cy0), (cx0, cy1), (cx1, cy1)):
            if not w[y][x] if False else False:
                pass
    # round the outside corners of the junction block where nothing connects
    corners = (("n", "w", cx0, cy0), ("n", "e", cx1, cy0), ("s", "w", cx0, cy1), ("s", "e", cx1, cy1))
    for a, b, x, y in corners:
        if a not in sides and b not in sides:
            w[y][x] = False
    _water_fill(c, w, seed=seed)
    # bank shading on land next to water
    for y in range(24):
        for x in range(16):
            if not w[y][x]:
                near = any(0 <= x + dx < 16 and 0 <= y + dy < 24 and w[y + dy][x + dx]
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if near:
                    c.px(x, y, "G" if kind == "grass" else "l")
    return c.rows()


def lake(shore, seed, land="g", deco=None):
    c = Cv()
    rnd = random.Random(seed)
    w = [[True] * 16 for _ in range(24)]
    depth = {}
    for s in "nsew":
        depth[s] = [3 + rnd.randrange(0, 2) for _ in range(24 if s in "ew" else 16)]
        for i in range(1, len(depth[s])):
            depth[s][i] = max(2, min(5, depth[s][i - 1] + rnd.choice((-1, 0, 0, 1))))
    for y in range(24):
        for x in range(16):
            if ("n" in shore and y < depth["n"][x]) or ("s" in shore and y > 23 - depth["s"][x]) \
               or ("w" in shore and x < depth["w"][y] - 1) or ("e" in shore and x > 15 - depth["e"][y] + 1):
                w[y][x] = False
    for a, b, (cx, cy) in (("n", "w", (0, 0)), ("n", "e", (15, 0)), ("s", "w", (0, 23)), ("s", "e", (15, 23))):
        if a in shore and b in shore:
            for y in range(24):
                for x in range(16):
                    if math.hypot(x - cx, (y - cy) * 0.7) < 7:
                        w[y][x] = False
    c.rect(0, 0, 15, 23, land)
    for y in range(24):
        for x in range(16):
            if not w[y][x] and rnd.random() < 0.3:
                c.px(x, y, "G" if land == "g" else "t")
    _water_fill(c, w, seed=seed)
    if deco:
        deco(c, w, rnd)
    return c.rows()


def _hinnom_deco(c, w, rnd):
    cells = [(x, y) for y in range(3, 21) for x in range(2, 14) if w[y][x] and c.get(x, y) in "12"]
    rnd.shuffle(cells)
    n = 0
    for x, y in cells:
        if n >= 2:
            break
        if all(w[y + dy][x + dx] for dx in (-2, 2) for dy in (-3, 3) if 0 <= y + dy < 24 and 0 <= x + dx < 16):
            c.line(x, y + 2, x, y - 1, "5"); c.px(x, y - 2, "4"); c.px(x - 1, y - 1, "5"); c.px(x + 1, y, "5")
            n += 1
    for (x, y) in cells[8:20]:
        if c.get(x, y) in "12" and rnd.random() < 0.7:
            c.px(x, y, "g"); c.px(x + 1, y, "G")
    for (x, y) in cells[24:32]:
        if c.get(x, y) in "12":
            c.px(x, y, "w")


def _reef_deco(c, w, rnd):
    for (x0, y0, x1, y1) in ((0, 7, 15, 7), (0, 16, 15, 16), (4, 0, 4, 23), (11, 0, 11, 23)):
        for i in range(17):
            x = x0 + (x1 - x0) * i // 16 if x1 != x0 else x0
            y = y0 + (y1 - y0) * i // 23 if y1 != y0 else y0
            if x1 == x0:
                y = i * 23 // 16
            if 0 <= x < 16 and 0 <= y < 24 and w[y][x] and (i + x + y) % 2 == 0:
                c.px(x, y, "l" if (x + y) % 3 else "L")
    cells = [(x, y) for y in range(3, 21) for x in range(2, 14) if w[y][x]]
    rnd.shuffle(cells)
    for x, y in cells[:3]:
        c.disc(x, y, 1.6, 1.6, "4", ("4", "4", "6")); c.px(x, y - 1, "w")
    for x, y in cells[3:8]:
        c.px(x, y, "5")


def _letter_n(s):
    return int(s[:-1]), s[-1]


def lakes_for(group, nrng, lrng, deco, land, shift=0):
    out = {}
    return out


def edges(name, nmax, lmin, lmax):
    n, l = _letter_n(name)
    s = ""
    if n == 1: s += "w"
    if n == nmax: s += "e"
    if l == lmin: s += "n"
    if l == lmax: s += "s"
    return s


SPRITES = {}
KINDS = {}


def add(name, grid, kind):
    SPRITES[name] = grid
    KINDS[name] = kind


add("bending_gjaus", bending_gjaus(), "tall")
add("chavvah_chime", chavvah_chime(), "tall")
add("chavvah_soft", chavvah_soft(), "terrain")
add("coral_ball", coral_ball(), "tall")
add("desert", desert(), "terrain")
add("finger_root", finger_root(), "tall")
add("fresco1", fresco1(), "terrain")
add("hex_small", hex_small(), "tall")
add("historic_building", historic_building(), "terrain")
add("historic_hills", historic_hills(), "terrain")
add("historic_pantheon", historic_pantheon(), "terrain")
add("historic_tower", historic_tower(), "terrain")
add("monument", monument(), "tall")
add("mover_chute_bottom_opening_l", mover_chute(False), "terrain")
add("mover_chute_top_opening_l", mover_chute(True), "terrain")
add("normality_field", normality_field(), "terrain")
add("reef_both_even", reef_both_even(), "terrain")
add("reef_organic_odd", reef_organic_odd(), "tall")
add("river_lake_nw", lake("nw", 41), "terrain")
add("river_worldmap_11a", river("nw", "grass", 11), "terrain")
add("river_worldmap_13a", river("e", "grass", 13, end=True), "terrain")
add("river_worldmap_1a", river("se", "grass", 1), "terrain")
add("river_worldmap_3a", river("sw", "rock", 3), "terrain")
add("river_worldmap_7a", river("nsw", "rock", 7), "terrain")
add("river_worldmap_9a", river("ne", "rock", 9), "terrain")
add("ruins_deep", ruins_deep(), "terrain")
add("spindle_bottom", spindle_bottom(), "terrain")
add("star_orchid_lily", star_orchid_lily(), "terrain")
for nm in ("1i", "2j", "3h", "4e", "5c", "6c", "7a", "7e", "8d"):
    add("svylake_worldmap_" + nm, lake("", ord(nm[1]) * 11 + int(nm[0]), "g"), "terrain")
for nm in ("1j", "2l", "3d", "3o", "4f", "6a", "6h", "7b", "7f", "7k", "8c", "8g", "9f"):
    add("terrainlakehinnom_" + nm, lake("", ord(nm[1]) * 7 + int(nm[0]), "g", _hinnom_deco), "terrain")
for nm in ("1k", "2i", "3k", "3p", "4l", "5h", "5l", "6k"):
    add("terrainpalladiumreef_" + nm, lake("", ord(nm[1]) * 5 + int(nm[0]), "t", _reef_deco), "terrain")
add("tile_jungleleft", tile_jungleleft(), "terrain")
add("tile_tombstone", tile_tombstone(), "tall")
add("tree_crystal", tree_crystal(), "tall")
add("urberry_bush", urberry_bush(), "tall")
add("witchwood", witchwood(), "tall")
add("yempuris_phi", yempuris_phi(), "tall")
