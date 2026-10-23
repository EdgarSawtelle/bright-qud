"""Terrain batch 2: ground decorations, plants, trees, ruins and world-map tiles (procedural grids)."""
import math
import random

from terrain_keys import BATCH_KEYS

KEYS = BATCH_KEYS[2]


class C:
    def __init__(self, fill="."):
        self.g = [[fill] * 16 for _ in range(24)]

    def p(self, x, y, c):
        x, y = int(x), int(y)
        if 0 <= x < 16 and 0 <= y < 24:
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < 16 and 0 <= y < 24 else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def ell(self, cx, cy, rx, ry, c, only=None):
        rx, ry = max(rx, 0.6), max(ry, 0.6)
        for y in range(int(cy - ry - 1), int(cy + ry + 2)):
            for x in range(int(cx - rx - 1), int(cx + rx + 2)):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    if only is None or self.get(x, y) in only:
                        self.p(x, y, c)

    def line(self, x0, y0, x1, y1, c):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)

    def poly(self, pts, c):
        ys = [q[1] for q in pts]
        for y in range(min(ys), max(ys) + 1):
            xs = []
            for i in range(len(pts)):
                (ax, ay), (bx, by) = pts[i], pts[(i + 1) % len(pts)]
                if ay != by and min(ay, by) <= y <= max(ay, by):
                    xs.append(ax + (bx - ax) * (y - ay) / (by - ay))
            if xs:
                for x in range(math.ceil(min(xs) - 0.01), int(max(xs) + 0.01) + 1):
                    self.p(x, y, c)

    def speck(self, rnd, n, c, only=None, y0=0, y1=24):
        for _ in range(n):
            x, y = rnd.randrange(16), rnd.randrange(y0, y1)
            if only is None or self.get(x, y) in only:
                self.p(x, y, c)

    def out(self):
        return ["".join(r) for r in self.g]


def ground(c, rnd, base="2", n=14):
    c.rect(0, 0, 15, 23, base)
    c.speck(rnd, n, "3")
    c.speck(rnd, n // 2, "1")


S = {}
K = {}


# ---------------- ground decorations ----------------
def arsplice():
    c = C()
    rnd = random.Random(3)
    c.speck(rnd, 10, "e")
    pts = [(8, 6), (12, 8), (13, 12), (11, 16), (8, 18), (4, 16), (2, 12), (4, 8)]
    for i, (x, y) in enumerate(pts):
        c.p(x, y + 3, "6")
        c.rect(x - 1, y + 1, x + 1, y + 2, "2" if i % 2 else "1")
        c.p(x - 1, y + 2, "3"); c.p(x + 1, y + 2, "3")
        c.p(x, y + 1, "4" if i % 2 else "w")
        c.p(x, y + 3, "6")
    for x, y in ((7, 12), (9, 11), (8, 13)):
        c.p(x, y, "5")
    c.p(8, 12, "4")
    return c.out()
S["arsplice_hyphae_unripe_even"] = arsplice()


def canyon():
    c = C(); rnd = random.Random(5)
    ground(c, rnd, "2", 16)
    c.rect(0, 0, 15, 2, "1")
    pts = [(10, 0), (13, 0), (11, 5), (12, 10), (8, 15), (9, 23), (4, 23), (4, 17), (7, 11), (6, 6)]
    c.poly(pts, "3")
    c.poly([(11, 0), (12, 0), (10, 5), (11, 10), (7, 15), (7, 23), (6, 23), (6, 16), (9, 11), (8, 6)], "6")
    c.line(5, 7, 6, 6, "1"); c.line(3, 18, 4, 17, "1"); c.line(10, 16, 11, 11, "1")
    c.speck(rnd, 14, "w", only="12", y0=0, y1=24)
    return c.out()
S["canyon"] = canyon()


def crystal_cluster(c, x, base, h, tone="1", hi="w"):
    for i in range(h):
        c.p(x, base - i, tone); c.p(x - 1, base - i, "2" if i < h - 1 else ".")
        c.p(x + 1, base - i, "3")
    c.p(x, base - h, hi); c.p(x, base - h - 1, tone)
    c.p(x - 1, base - h + 1, hi)


def chavvah_leaves():
    c = C()
    for x, b, h in ((4, 18, 6), (8, 19, 9), (12, 18, 7), (6, 20, 4), (10, 20, 5), (2, 19, 3), (14, 20, 3)):
        crystal_cluster(c, x, b, h, "1")
    for x, y in ((3, 8), (11, 6), (7, 5), (13, 12)):
        c.p(x, y, "w"); c.p(x - 1, y, "4"); c.p(x + 1, y, "4"); c.p(x, y - 1, "4"); c.p(x, y + 1, "4")
    return c.out()
S["chavvah_leaves_dense"] = chavvah_leaves()


def chavvah_stairs():
    c = C()
    c.ell(8, 14, 6, 3, "3"); c.ell(8, 14, 3, 1, "6")
    steps = [(3, 18), (11, 17), (12, 14), (9, 12), (4, 11), (5, 8), (10, 7), (8, 4)]
    for i, (x, y) in enumerate(steps):
        w = 3
        c.rect(x - 1, y, x + 2, y + 1, "2")
        c.rect(x - 1, y, x + 2, y, "1")
        c.p(x - 1, y + 1, "3"); c.p(x + 2, y + 1, "3")
        c.p(x + 1, y + 2, "4" if i % 2 else "5")
    c.p(8, 2, "w"); c.p(7, 2, "4"); c.p(9, 2, "4"); c.p(8, 1, "4"); c.p(8, 3, "4")
    return c.out()
S["chavvah_stairsup"] = chavvah_stairs()


def craters():
    c = C(); rnd = random.Random(8)
    pass
    c.speck(rnd, 10, "e")
    for cx, cy, rx, ry in ((5, 8, 4, 3), (11, 16, 4, 3), (4, 19, 2, 1)):
        c.ell(cx, cy, rx, ry, "3")
        c.ell(cx + 0.5, cy + 0.5, rx - 1.5, ry - 1, "e")
        for x in range(cx - rx, cx + rx + 1):
            c.p(x, cy - ry, "1") if abs(x - cx) < rx - 1 else None
        c.p(cx - rx, cy - 1, "2"); c.p(cx + rx, cy + 1, "2")
    return c.out()
S["craters"] = craters()


def eelgrass():
    c = C(); rnd = random.Random(2)
    for x in range(1, 16, 2):
        h = rnd.randrange(8, 17)
        ph = rnd.random() * 6
        for k in range(h):
            xx = x + round(math.sin(k / 2.5 + ph) * 1.5)
            c.p(xx, 22 - k, "g" if k < h - 3 else "G")
            if k > 2:
                c.p(xx - 1, 22 - k, "h")
    for x in range(0, 16):
        c.p(x, 22, "h")
    return c.out()
S["extrasolar_grass"] = eelgrass()


def flowers_crystal():
    c = C()
    for x, b, h, t in ((4, 21, 7, "1"), (8, 22, 11, "4"), (12, 21, 8, "1")):
        for k in range(h):
            c.p(x, b - k, "h")
        top = b - h
        c.ell(x, top, 2.5, 2.5, t); c.p(x - 1, top - 1, "w"); c.p(x + 1, top + 1, "3")
        c.p(x, top - 3, "w"); c.p(x - 3, top, t); c.p(x + 3, top, t)
        c.p(x, top, "w")
    c.p(2, 14, "w"); c.p(14, 12, "w"); c.p(6, 7, "w")
    return c.out()
S["flowers_crystal"] = flowers_crystal()


def dune():
    c = C(); rnd = random.Random(11)
    c.rect(0, 0, 15, 23, "1")
    for y0, ph in ((4, 0), (10, 5), (16, 2), (22, 7)):
        for x in range(16):
            y = y0 + round(math.sin((x + ph) / 2.6) * 1.5)
            c.p(x, y, "2"); c.p(x, y + 1, "3"); c.p(x, y + 2, "2")
    c.speck(rnd, 10, "3", only="1")
    return c.out()
S["ground_dune"] = dune()


# ---------------- ruins ----------------
def ruin_base():
    c = C(); rnd = random.Random(4)
    c.speck(rnd, 10, "e"); c.speck(rnd, 8, "3")
    return c


def historic_arch():
    c = ruin_base()
    c.rect(2, 8, 5, 21, "2"); c.rect(10, 8, 13, 21, "2")
    c.rect(2, 8, 5, 8, "1"); c.rect(10, 8, 13, 8, "1")
    c.rect(5, 9, 5, 21, "3"); c.rect(13, 9, 13, 21, "3")
    c.ell(8, 9, 5, 5, "2", only=".e3"); 
    c.ell(8, 11, 3, 4, "."); c.rect(6, 12, 9, 21, ".")
    c.rect(2, 21, 13, 22, "3")
    c.line(4, 5, 11, 5, "1")
    for x, y in ((3, 12), (11, 14), (4, 17), (12, 18)):
        c.p(x, y, "6")
    c.rect(6, 6, 9, 6, "1")
    c.p(8, 4, "5"); c.p(8, 5, "4"); c.rect(6, 7, 9, 7, "2")
    c.p(7, 8, "3"); c.p(10, 7, "3")
    c.rect(7, 19, 9, 20, "3"); c.p(8, 19, "2")
    return c.out()
S["historic_arch"] = historic_arch()


def historic_gardens():
    c = ruin_base()
    for y0 in (4, 13):
        c.rect(1, y0, 14, y0 + 6, "5")
        c.rect(1, y0, 14, y0, "6"); c.rect(1, y0 + 6, 14, y0 + 6, "6")
        c.rect(1, y0, 1, y0 + 6, "6"); c.rect(14, y0, 14, y0 + 6, "6")
        for x in range(3, 14, 3):
            for y in range(y0 + 2, y0 + 6, 2):
                c.p(x, y, "g"); c.p(x, y - 1, "G")
        c.p(5, y0 + 1, "1")
    c.rect(1, 10, 14, 11, "e"); c.speck(random.Random(1), 6, "3", y0=10, y1=12)
    c.rect(1, 3, 4, 3, "1"); c.rect(11, 20, 14, 20, "1")
    c.p(7, 8, "1"); c.p(8, 8, "2")
    return c.out()
S["historic_gardens"] = historic_gardens()


def historic_houses():
    c = ruin_base()
    for x0, y0, w, h in ((1, 4, 6, 8), (9, 11, 6, 9)):
        c.rect(x0, y0, x0 + w, y0 + h, "2")
        c.rect(x0, y0 + h - 1, x0 + w, y0 + h, "3")
        c.rect(x0 + 1, y0 + 1, x0 + w - 1, y0 + h - 2, "e")
        c.rect(x0, y0, x0 + w, y0, "1")
        c.rect(x0, y0, x0, y0 + h, "1")
        c.p(x0 + 2, y0 + h, "e"); c.p(x0 + 3, y0 + h, "e")
        c.rect(x0 + 1, y0 + 1, x0 + 2, y0 + 1, "5")
    c.p(3, 6, "." ); c.p(3, 4, "e"); c.p(4, 4, "e")
    c.p(12, 11, "e"); c.p(13, 11, "e")
    for x, y in ((7, 14), (8, 15), (6, 12), (14, 8), (4, 14)):
        c.p(x, y, "3")
    c.p(4, 7, "4"); c.p(12, 15, "4")
    return c.out()
S["historic_houses"] = historic_houses()


def historic_pools():
    c = ruin_base()
    for cx, cy, rx, ry in ((8, 7, 6, 3), (8, 17, 6, 4)):
        c.ell(cx, cy, rx, ry, "2")
        c.ell(cx, cy, rx - 1, ry - 1, "B")
        c.ell(cx, cy + 1, rx - 2, ry - 2, "b")
        c.line(cx - 2, cy - 1, cx, cy - 1, "w")
    c.rect(7, 10, 8, 13, "2"); c.p(7, 11, "e")
    c.p(2, 20, "4"); c.p(13, 4, "4"); c.p(13, 21, "6")
    return c.out()
S["historic_pools"] = historic_pools()


# ---------------- plants and trees ----------------
def lahbloom():
    c = C()
    for k in range(9):
        c.p(8 + (1 if k > 5 else 0), 21 - k, "h"); c.p(9 + (1 if k > 5 else 0), 21 - k, "g")
    c.p(6, 18, "g"); c.p(5, 17, "G"); c.p(12, 16, "g"); c.p(13, 15, "G")
    for dx, dy in ((-1, 0), (1, 0), (0, -1), (0, 1)):
        pass
    for sx in (-1, 1):
        for tone in (0, 1):
            x0 = 9 + sx * (3 + tone * 2)
            c.ell(x0, 9 + tone * 2, 2.2, 2.5, "n")
            c.ell(x0 - sx * 0.5, 8 + tone * 2, 1.2, 1.2, "t")
            c.p(x0, 11 + tone * 2, "N")
    c.ell(9, 8, 2, 2, "y"); c.p(9, 8, "N"); c.p(8, 7, "w")
    c.p(3, 5, "O"); c.p(4, 5, "l"); c.p(14, 4, "O"); c.p(13, 4, "l"); c.p(2, 14, "O")
    return c.out()
S["lahbloom"] = lahbloom()


def tree_bulbs():
    c = C()
    c.line(8, 22, 8, 10, "n"); c.line(9, 22, 9, 10, "N")
    c.line(8, 13, 3, 8, "n"); c.line(9, 11, 13, 7, "N"); c.line(8, 16, 12, 14, "N"); c.line(8, 17, 4, 15, "n")
    for x, y, r in ((3, 8, 3), (13, 7, 3), (8, 6, 3), (12, 14, 2), (4, 15, 2)):
        pts = [(x, y - r), (x + r, y - 1), (x + r - 1, y + r - 1), (x - r + 1, y + r - 1), (x - r, y - 1)]
        c.poly(pts, "1")
        c.line(x - r + 1, y + r - 1, x + r - 1, y + r - 1, "3")
        c.line(x, y - r, x - r, y - 1, "w")
        c.line(x, y - r + 1, x + 1, y + r - 1, "2")
        c.p(x - 1, y - 1, "4")
    c.rect(6, 22, 11, 22, "x")
    return c.out()
S["tree_bulbs"] = tree_bulbs()


def tree_fuzzy():
    c = C()
    c.rect(7, 4, 8, 21, "n"); c.line(9, 6, 9, 21, "N")
    c.rect(5, 22, 11, 22, "x")
    for y, w in ((3, 2), (7, 3), (11, 4), (15, 4), (19, 3)):
        c.ell(8, y, w + 1.5, 2.2, "g")
        c.ell(8 - 1, y - 1, w, 1.2, "G")
        c.p(8 + w + 1, y + 1, "h"); c.p(8 - w - 1, y + 1, "h")
        c.line(8 - w, y + 2, 8 + w, y + 2, "h")
        for x in (8 - w, 8, 8 + w):
            c.p(x, y - 2, "w")
    c.p(8, 1, "w"); c.p(8, 2, "G")
    return c.out()
S["tree_fuzzy"] = tree_fuzzy()


def mushroom_terrain():
    c = C(); rnd = random.Random(7)
    c.speck(rnd, 8, "e")
    for x, y, r, col in ((4, 8, 3, "r"), (11, 7, 3, "B"), (8, 15, 4, "m"), (3, 18, 2, "y"), (13, 18, 2, "c")):
        c.ell(x, y, r, r * 0.7, col)
        c.rect(x, y + 1, x, y + 3, "w") if r > 2 else None
        c.p(x - 1, y - 1, "w"); c.p(x + 1, y, "w")
        c.line(x - r, y + 1, x + r, y + 1, "w" if r < 3 else col)
    c.rect(7, 19, 8, 20, "w"); c.rect(3, 20, 3, 21, "w"); c.rect(13, 20, 13, 21, "w")
    c.rect(4, 11, 4, 13, "w"); c.rect(11, 10, 11, 12, "w"); c.rect(8, 18, 8, 19, "w")
    return c.out()
S["mushroom_terrain"] = mushroom_terrain()


def openpit():
    c = C(); rnd = random.Random(9)
    c.speck(rnd, 10, "e")
    c.ell(8, 12, 7, 8, "3")
    c.ell(8, 12.5, 5.5, 6.5, "O")
    c.ell(8, 13, 3.5, 4, "e")
    for a in range(0, 360, 40):
        x, y = 8 + 7 * math.cos(math.radians(a)), 12 + 8 * math.sin(math.radians(a))
        c.rect(int(x) - 1, int(y), int(x), int(y) + 1, "2" if a % 80 else "1")
        c.p(x, y - 1, "4" if a % 80 else "5")
    c.p(7, 13, "c"); c.p(10, 11, "c")
    return c.out()
S["openpit"] = openpit()


def reef_metal():
    c = C(); rnd = random.Random(6)
    c.speck(rnd, 8, "e")
    for y in (4, 12, 20):
        c.rect(0, y, 15, y + 1, "l"); c.rect(0, y + 1, 15, y + 1, "L")
    for x in (3, 11):
        c.rect(x, 0, x + 1, 23, "l"); c.rect(x + 1, 0, x + 1, 23, "L")
    for x, y in ((3, 4), (11, 12), (3, 20), (11, 4)):
        c.ell(x + 0.5, y - 0.5, 2, 2, "2"); c.p(x, y - 1, "1"); c.p(x + 1, y + 1, "3")
        c.p(x - 1, y - 2, "4"); c.p(x + 2, y - 2, "5")
    for x, y in ((7, 8), (14, 16), (7, 16), (0, 8)):
        c.rect(x - 1, y, x, y + 1, "4"); c.p(x - 1, y - 1, "5"); c.p(x, y + 2, "6")
    return c.out()
S["reef_metal_odd"] = reef_metal()


# ---------------- fixtures-ish ----------------
def mover_chute():
    c = C()
    c.rect(2, 3, 5, 18, "n"); c.rect(2, 16, 14, 19, "n")
    c.rect(3, 3, 4, 17, "N"); c.rect(3, 17, 14, 18, "N")
    c.rect(2, 3, 2, 18, "n"); c.rect(5, 3, 5, 15, "1")
    c.rect(2, 19, 14, 19, "3"); c.rect(6, 15, 14, 15, "1")
    for y in range(4, 17, 3):
        c.p(3, y, "B"); c.p(4, y, "w")
    for x in range(7, 14, 3):
        c.p(x, 17, "B"); c.p(x + 1, 17, "w")
    c.p(12, 17, "B"); c.p(13, 17, "w")
    c.p(4, 13, "4"); c.p(4, 14, "4"); c.p(5, 14, "w")
    c.p(14, 17, "w"); c.p(15, 17, "w")
    return c.out()
S["mover_chute_l"] = mover_chute()


def securitydoor():
    c = C()
    c.rect(1, 1, 14, 23, "L"); c.rect(1, 1, 14, 2, "l")
    c.rect(2, 3, 13, 23, "S" if False else "L")
    c.rect(3, 4, 12, 22, "l")
    c.rect(3, 4, 12, 4, "w"); c.rect(12, 5, 12, 22, "L"); c.rect(3, 22, 12, 22, "L")
    c.rect(5, 7, 10, 20, "L"); c.rect(6, 8, 9, 19, "1")
    c.rect(6, 8, 6, 19, "2"); c.rect(9, 8, 9, 19, "3")
    for y in (8, 12, 16):
        c.rect(3, y, 4, y, "L")
    c.rect(11, 12, 12, 15, "d"); c.rect(11, 12, 12, 12, "B")
    c.rect(11, 17, 12, 18, "r") if False else None
    c.rect(7, 11, 8, 14, "O"); c.p(7, 11, "B")
    c.p(11, 7, "B")
    return c.out()
S["securitydoor"] = securitydoor()


def web():
    c = C()
    cx, cy = 8, 11
    for a in range(0, 360, 45):
        c.line(cx, cy, cx + round(8 * math.cos(math.radians(a))), cy + round(11 * math.sin(math.radians(a))), "1")
    for r in (3, 6, 9):
        pts = [(cx + r * math.cos(math.radians(a)), cy + r * 1.3 * math.sin(math.radians(a))) for a in range(0, 361, 45)]
        for i in range(8):
            c.line(round(pts[i][0]), round(pts[i][1]), round(pts[i + 1][0]), round(pts[i + 1][1]), "1" if r != 6 else "2")
    c.p(cx, cy, "w")
    for x, y in ((3, 4), (13, 5), (12, 19), (4, 18), (8, 2), (8, 20)):
        c.p(x, y, "w")
    return c.out()
S["web"] = web()


def tile_empty():
    c = C(); rnd = random.Random(12)
    for _ in range(9):
        x, y = rnd.randrange(16), rnd.randrange(24)
        c.p(x, y, rnd.choice("rcBmyM"))
        if rnd.random() < 0.3:
            c.p(x + 1, y, "w")
    c.speck(rnd, 6, "L")
    return c.out()
S["tile_empty"] = tile_empty()


def tile_location():
    c = C(); rnd = random.Random(13)
    c.rect(0, 0, 15, 23, "3")
    c.speck(rnd, 30, "e"); c.speck(rnd, 14, "2")
    c.poly([(2, 20), (4, 12), (8, 8), (12, 12), (14, 20)], "2")
    c.poly([(2, 20), (4, 12), (6, 10), (6, 20)], "1")
    c.poly([(11, 11), (12, 12), (14, 20), (10, 20)], "3")
    c.rect(6, 13, 10, 20, "O"); c.rect(5, 12, 5, 20, "N"); c.rect(11, 12, 11, 20, "N"); c.rect(5, 11, 11, 11, "n")
    c.rect(7, 15, 9, 20, "e")
    c.p(7, 16, "y")
    for x, y in ((2, 21), (4, 22), (6, 21), (11, 22), (13, 21), (9, 22), (1, 19)):
        c.p(x, y, "1"); c.p(x + 1, y, "2")
    c.p(8, 6, "w"); c.p(8, 5, "1")
    return c.out()
S["tile_location"] = tile_location()


def switch():
    c = C()
    c.rect(3, 4, 12, 20, "L"); c.rect(3, 4, 12, 4, "l"); c.rect(3, 4, 3, 20, "l")
    c.rect(4, 5, 11, 19, "l"); c.rect(11, 5, 11, 19, "L"); c.rect(4, 19, 11, 19, "L")
    for x, y in ((4, 5), (11, 5), (4, 18), (11, 18)):
        c.p(x, y, "O")
    for y in (7, 13):
        c.rect(6, y, 9, y + 3, "R"); c.rect(6, y, 9, y + 1, "r"); c.p(6, y, "w"); c.rect(6, y + 3, 9, y + 3, "O")
    c.p(11, 9, "O")
    c.line(5, 11, 10, 11, "O")
    c.rect(4, 21, 11, 22, "x")
    return c.out()
S["switch"] = switch()


# ---------------- statues ----------------
def statue():
    c = C()
    c.rect(3, 17, 12, 20, "L"); c.rect(3, 17, 12, 17, "l"); c.rect(3, 20, 12, 20, "O")
    c.rect(5, 9, 10, 17, "2"); c.rect(5, 9, 6, 17, "1"); c.rect(10, 10, 10, 17, "3")
    c.rect(3, 10, 4, 15, "2"); c.rect(11, 10, 12, 15, "3"); c.rect(3, 10, 3, 14, "1")
    c.ell(8, 6, 3, 3.3, "1"); c.rect(9, 5, 10, 8, "2")
    c.rect(5, 2, 10, 3, "y"); c.p(5, 1, "y"); c.p(8, 1, "y"); c.p(10, 1, "y"); c.p(8, 2, "w")
    c.p(7, 6, "O"); c.p(9, 6, "O"); c.line(7, 8, 9, 8, "3")
    c.line(7, 12, 8, 14, "3")
    c.rect(4, 21, 11, 21, "x")
    return c.out()
S["statue"] = statue()


def hologram():
    c = C()
    c.ell(8, 20, 5, 1.3, "4"); c.ell(8, 20, 3, 0.8, "w")
    c.ell(8, 11, 4.5, 8, "y")
    c.ell(8, 11, 3, 6, "w")
    c.ell(8, 4, 2, 2, "y"); c.rect(7, 2, 9, 2, "w")
    for y in range(3, 20, 2):
        for x in range(0, 16):
            if c.get(x, y) != ".":
                c.p(x, y, "4")
    for a in range(0, 360, 60):
        c.p(8 + 7 * math.cos(math.radians(a)), 11 + 9 * math.sin(math.radians(a)), "w")
    c.p(8, 21, "y")
    return c.out()
S["resheph_sultanstatue"] = hologram()


def moonstair():
    c = C(); rnd = random.Random(21)
    c.rect(0, 0, 15, 23, "O")
    c.speck(rnd, 14, "L")
    for cx, cy, r in ((4, 5, 3), (11, 7, 3), (7, 12, 3), (3, 18, 3), (12, 17, 3), (8, 21, 2)):
        pts = [(cx - 1, cy - r), (cx + 1, cy - r), (cx + r, cy), (cx + 1, cy + r), (cx - 1, cy + r), (cx - r, cy)]
        c.poly(pts, "2")
        c.poly([(cx - 1, cy - r), (cx + 1, cy - r), (cx, cy - 1), (cx - r, cy)], "1")
        c.poly([(cx + 1, cy + r), (cx - 1, cy + r), (cx, cy + 1), (cx + r, cy)], "3")
        c.p(cx, cy - 1, "w")
        c.p(cx + r + 1, cy - r, "5")
    c.p(1, 10, "M"); c.p(14, 12, "M"); c.p(6, 2, "M"); c.p(15, 21, "M")
    return c.out()
S["moonstair_worldmap"] = moonstair()


def spindle():
    c = C(); rnd = random.Random(31)
    c.rect(0, 0, 15, 23, "3")
    c.speck(rnd, 14, "2")
    for cx, top, hw in ((4, 6, 5), (11, 3, 6), (8, 12, 6)):
        base = 21
        c.poly([(cx, top), (cx + hw, base), (cx - hw, base)], "2")
        c.poly([(cx, top), (cx - hw, base), (cx - 1, base)], "1")
        c.poly([(cx, top), (cx + 1, base - 2), (cx + hw, base)], "3")
        c.poly([(cx, top), (cx - 1, top + 3), (cx + 1, top + 3)], "1")
        c.p(cx, top, "w")
    for y in range(0, 24, 4):
        c.p(1 + y % 7, y, "4")
    c.rect(0, 22, 15, 23, "3")
    return c.out()
S["spindle_top"] = spindle()


def rainbowwood():
    c = C(); rnd = random.Random(41)
    c.rect(0, 0, 15, 23, "e")
    c.speck(rnd, 16, "E")
    cols = "rmBygcM"
    for i, (x, y, r) in enumerate(((4, 5, 3), (12, 4, 3), (8, 10, 4), (3, 15, 3), (13, 14, 3), (7, 20, 3), (14, 21, 2))):
        col = cols[i % 7]
        c.ell(x, y, r + 0.5, r * 0.75 + 0.5, col)
        c.p(x - 1, y - 1, "w"); c.p(x + 1, y, "w")
        c.line(x - r, y + 1, x + r, y + 1, "O")
        c.rect(x, y + 2, x, y + 3, "w")
    c.speck(rnd, 5, "w")
    return c.out()
S["worldmap_rainbowwood"] = rainbowwood()


# ---------------- water: rivers, lakes ----------------
CX, CY = 7.5, 11.5


def bank(c, rnd):
    c.rect(0, 0, 15, 23, "g")
    c.speck(rnd, 26, "h"); c.speck(rnd, 14, "G")
    for _ in range(3):
        x, y = rnd.randrange(1, 15), rnd.randrange(1, 23)
        c.p(x, y, "t"); c.p(x, y - 1, "t")


def river(dirs, end=None, seed=1, mountain=False):
    c = C(); rnd = random.Random(seed)
    bank(c, rnd)
    if mountain:
        for x, y in ((2, 3), (13, 4), (3, 19), (12, 20), (13, 9), (2, 11)):
            c.poly([(x, y - 2), (x + 2, y + 1), (x - 2, y + 1)], "L"); c.p(x, y - 2, "w"); c.line(x, y - 1, x - 1, y + 1, "l")
    w = 3.3
    box = {"n": (5, 0, 10, 12), "s": (5, 11, 10, 23), "w": (0, 8, 8, 15), "e": (7, 8, 15, 15)}
    for d in dirs:
        x0, y0, x1, y1 = box[d]
        # widen with outer rim: rim = 3, water = 2
        for rim, col in ((1, "3"), (0, "2")):
            c.rect(x0 + (rim if d in "ns" else 0), y0 + (rim if d in "we" else 0),
                   x1 - (rim if d in "ns" else 0), y1 - (rim if d in "we" else 0), col)
    c.ell(CX, CY, 4.4, 4.4, "3"); c.ell(CX, CY, 3.4, 3.4, "2")
    if end:
        c.ell(CX, CY, 3.6, 3.6, "2")
    # highlights
    for d in dirs:
        if d in "ns":
            for y in range(1 if d == "n" else 14, 11 if d == "n" else 22, 4):
                c.p(7 + (y // 4) % 2, y, "1"); c.p(8 + (y // 4) % 2, y, "1")
        else:
            for x in range(1 if d == "w" else 10, 6 if d == "w" else 15, 4):
                c.p(x, 11 + (x // 4) % 2, "1"); c.p(x + 1, 11 + (x // 4) % 2, "1")
    c.p(6, 10, "w"); c.p(7, 10, "1")
    if end:
        c.ell(CX, CY, 2, 2, "d" if False else "1"); c.p(7, 11, "w"); c.p(8, 12, "2")
    return c.out()


S["river_worldmap_10a"] = river("nwe", seed=2)
S["river_worldmap_12a"] = river("n", end=True, seed=3)
S["river_worldmap_14a"] = river("we", seed=4, mountain=True)
S["river_worldmap_2a"] = river("swe", seed=5)
S["river_worldmap_5a"] = river("nse", seed=6)
S["river_worldmap_8a"] = river("ns", seed=7, mountain=True)


def duskwaters():
    c = C(); rnd = random.Random(51)
    c.rect(0, 0, 15, 23, "2")
    for y in range(1, 24, 4):
        for x in range(16):
            c.p(x, y + (x // 3) % 2, "3")
    for _ in range(5):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 22)
        c.p(x, y, "1"); c.p(x + 1, y, "1")
    # tree shadows
    for x, y, r in ((3, 6, 4), (13, 16, 4), (6, 20, 3)):
        c.ell(x, y, r, r * 0.8, "d")
        c.ell(x + 1, y - 1, r - 2, r * 0.6, "O")
    c.p(10, 8, "w"); c.p(5, 14, "w")
    return c.out()
S["river_worldmap_duskwaters"] = duskwaters()


def lake(land, seed, coral=False):
    """Open water filling the tile (no shore): tiles seamlessly; per-piece highlights only."""
    c = C(); rnd = random.Random(seed)
    c.rect(0, 0, 15, 23, "2")
    for y in range(1, 24, 4):
        for x in range(16):
            c.p(x, y + (x // 4) % 2, "3")
            if x % 8 in (1, 2, 3):
                c.p(x, y - 1 + (x // 4) % 2, "1")
    for _ in range(4):
        x, y = rnd.randrange(16), rnd.randrange(24)
        c.p(x, y, "1"); c.p(x + 1, y, "1")
    if coral:
        for _ in range(3):
            x, y = rnd.randrange(2, 14), rnd.randrange(3, 21)
            c.p(x, y, "c"); c.p(x, y - 1, "w")
    else:
        for _ in range(2):
            c.p(rnd.randrange(16), rnd.randrange(24), "w")
    return c.out()


SVY = {"2h": "nw", "3f": "n", "3j": "e", "4g": "sw", "5h": "w", "6h": "s", "7c": "ne", "8b": "se"}
for i, (k, d) in enumerate(SVY.items()):
    S["svylake_worldmap_" + k] = lake(d, 60 + i)
HIN = {"2d": "nw", "2n": "n", "3f": "ne", "4d": "w", "5b": "", "6c": "e", "6m": "sw", "7d": "s",
       "7i": "se", "8a": "nw", "8e": "w", "9d": "ne", "9h": "s"}
for i, (k, d) in enumerate(HIN.items()):
    S["terrainlakehinnom_" + k] = lake(d, 80 + i, coral=True)


def palreef(seed):
    c = C(); rnd = random.Random(seed)
    c.rect(0, 0, 15, 23, "e"); c.speck(rnd, 12, "E")
    off = rnd.randrange(4)
    for y in range(2 + off, 24, 8):
        c.rect(0, y, 15, y + 1, "l"); c.rect(0, y + 1, 15, y + 1, "L")
    for x in range(1 + off, 16, 8):
        c.rect(x, 0, x + 1, 23, "l"); c.rect(x + 1, 0, x + 1, 23, "L")
    for _ in range(7):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 21)
        col = rnd.choice(("1", "4", "c"))
        c.ell(x, y, 2, 2, "2")
        c.p(x, y, col); c.p(x - 1, y - 1, "w")
        c.p(x + 1, y + 1, "3")
        c.line(x, y - 2, x, y - 3, "5")
    c.speck(rnd, 8, "c")
    return c.out()


for i, k in enumerate(("1o", "2k", "3m", "4j", "4o", "5j", "5n")):
    S["terrainpalladiumreef_" + k] = palreef(100 + i)

SPRITES = S
KINDS = {n: "terrain" for n in S}
for n in ("chavvah_leaves_dense", "flowers_crystal", "lahbloom", "tree_bulbs", "tree_fuzzy"):
    KINDS[n] = "tall"
for n in ("statue", "resheph_sultanstatue", "switch"):
    del KINDS[n]
