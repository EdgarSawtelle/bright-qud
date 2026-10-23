"""Terrain batch 1 (wave 2): plants, trees, ruins, ground decorations, world-map tiles.
Mostly built with small drawing helpers; every sprite is a 24x16 grid of palette chars / role digits."""
import math
import random

from terrain_keys import BATCH_KEYS

KEYS = BATCH_KEYS[1]


# ---------- helpers ----------
def new(c="."):
    return [[c] * 16 for _ in range(24)]


def rows(g):
    return ["".join(r) for r in g]


def put(g, x, y, c):
    if 0 <= x < 16 and 0 <= y < 24:
        g[y][x] = c


def rect(g, x0, y0, x1, y1, c):
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            put(g, x, y, c)


def line(g, x0, y0, x1, y1, c):
    n = max(abs(x1 - x0), abs(y1 - y0), 1)
    for i in range(n + 1):
        put(g, round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), c)


def disc(g, cx, cy, rx, ry, hi, mid, lo, hard=0.7, only=None):
    for y in range(24):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            if d <= 1:
                if only and g[y][x] not in only:
                    continue
                g[y][x] = lo if (d > hard and (x - cx) + (y - cy) > -1) else (hi if (x - cx) + (y - cy) < -0.45 * rx and d > 0.15 else mid)


def speck(g, rnd, n, chars, over):
    for _ in range(n):
        x, y = rnd.randrange(16), rnd.randrange(24)
        if g[y][x] in over:
            g[y][x] = rnd.choice(chars)


def land(seed, base="g"):
    rnd = random.Random(seed)
    g = new(base)
    for _ in range(26):
        g[rnd.randrange(24)][rnd.randrange(16)] = "G"
    for _ in range(22):
        g[rnd.randrange(24)][rnd.randrange(16)] = "h"
    return g


def dirt(seed):
    rnd = random.Random(seed)
    g = new("e")
    for _ in range(30):
        g[rnd.randrange(24)][rnd.randrange(16)] = "E"
    return g


def outline_into(g, edge, over="."):
    """Darken: every non-empty pixel touching '.' gets the edge char (inner rim, keeps silhouette)."""
    h = [r[:] for r in g]
    for y in range(24):
        for x in range(16):
            if g[y][x] in over:
                continue
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                xx, yy = x + dx, y + dy
                if 0 <= xx < 16 and 0 <= yy < 24 and g[yy][xx] in over:
                    h[y][x] = edge
                    break
    return h


S = {}
KINDS = {}


def reg(name, kind):
    def deco(f):
        S[name] = rows(f())
        if kind:
            KINDS[name] = kind
        return f
    return deco


# ---------- ground / structures ----------
@reg("arena_floor", "terrain")
def _():
    g = new("2")
    for y in range(24):
        for x in range(16):
            if y % 6 == 5 or (x + (3 if (y // 6) % 2 else 0)) % 8 == 7:
                g[y][x] = "3"
            elif y % 6 == 0 or (x + (3 if (y // 6) % 2 else 0)) % 8 == 0:
                g[y][x] = "1"
    rnd = random.Random(4)
    speck(g, rnd, 14, "13", "2")
    return g


@reg("fresco2", "terrain")
def _():
    g = new("2")
    rect(g, 0, 0, 15, 3, "1")          # lit top face
    rect(g, 0, 20, 15, 23, "3")        # dark base
    rect(g, 0, 4, 15, 4, "1")
    for x in range(1, 15):             # frame
        put(g, x, 6, "3"); put(g, x, 18, "3")
    for y in range(6, 19):
        put(g, 1, y, "3"); put(g, 14, y, "3")
    rect(g, 2, 7, 13, 17, "2")
    # sun halo
    disc(g, 8, 10, 3.2, 2.8, "4", "5", "4", hard=2)
    for x, y in ((8, 6), (4, 8), (12, 8)):
        pass
    for a in range(8):
        put(g, round(8 + 4.5 * math.cos(a * math.pi / 4)), round(10 + 3.6 * math.sin(a * math.pi / 4)), "4")
    # figure with raised arms
    rect(g, 7, 9, 8, 10, "5")
    put(g, 7, 9, "4")
    rect(g, 6, 11, 9, 15, "5")
    rect(g, 7, 11, 7, 15, "4")
    put(g, 5, 11, "4"); put(g, 4, 10, "4"); put(g, 10, 11, "4"); put(g, 11, 10, "4")
    rect(g, 6, 16, 9, 16, "6")
    for x in (3, 12):
        for y in range(12, 16):
            put(g, x, y, "5")
        put(g, x, 11, "4")
    for x in range(2, 14):
        put(g, x, 17, "6")
    put(g, 7, 8, "5")
    for x in range(0, 16, 4):
        put(g, x, 2, "2")
    return g


@reg("chavvah_chime_double", "terrain")
def _():
    g = new(".")
    disc(g, 5, 15, 5, 5.5, "1", "2", "3")
    disc(g, 11.3, 17, 3.8, 3.8, "1", "2", "3")
    # crystal corms (faceted shards)
    def shard(x, y, h):
        for k in range(h):
            put(g, x, y - k, "5"); put(g, x + 1, y - k, "6")
            if k < h - 2:
                put(g, x - 1, y - k, "4")
        put(g, x, y - h, "4"); put(g, x - 1, y - h + 1, "w")
    shard(4, 11, 7); shard(7, 12, 4); shard(2, 14, 3); shard(11, 14, 4); shard(13, 15, 2)
    for y in range(24):
        for x in range(16):
            if g[y][x] in "123":
                if (x < 15 and g[y][x + 1] == ".") or (y < 23 and g[y + 1][x] == "."):
                    g[y][x] = "3"
    for x in range(1, 15):
        if g[20][x] == "." and g[19][x] != ".":
            g[20][x] = "x"
        if g[21][x] == ".":
            g[21][x] = "x"
    return g


@reg("chavvah_stairsdown", "terrain")
def _():
    g = new("3")
    # funnel of spiralling steps going down: ellipses shrink and sink, each with a lit rim
    for i, (cy, rx, ry) in enumerate(((10, 7.4, 8.4), (11.5, 6, 6.8), (13, 4.6, 5.2), (14.5, 3.2, 3.6), (15.5, 1.8, 2))):
        for y in range(24):
            for x in range(16):
                d = ((x - 7.5) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1:
                    top = y < cy - ry * .55
                    g[y][x] = "4" if top and d > .6 else ("1" if i % 2 == 0 else "2")
                    if d > .78 and y > cy:
                        g[y][x] = "6"
    disc(g, 7.5, 16, 1.2, 1.4, "O", "O", "O")
    for k, (x, y) in enumerate(((3, 6), (12, 8), (4, 13))):   # a few hovering frustums
        put(g, x, y, "w"); put(g, x + 1, y, "w"); put(g, x, y + 1, "6")
    return g


@reg("coral_branching", "terrain")
def _():
    g = new(".")
    rnd = random.Random(11)

    def branch(x, y, dx, dy, ln, th):
        for i in range(ln):
            for t in range(th):
                put(g, x + t, y, "2")
            x += dx if rnd.random() < 0.5 else 0
            y -= 1
            if i == ln // 2 and ln > 5:
                branch(x, y, -1, -1, ln // 2, max(1, th - 1))
                branch(x, y, 1, -1, ln // 2, max(1, th - 1))
            if y < 1:
                break
        put(g, x, y, "5")
        put(g, x, y - 1, "4")
    branch(6, 21, 1, -1, 17, 3)
    branch(3, 21, -1, -1, 8, 2)
    branch(11, 21, 1, -1, 9, 2)
    for y in range(24):
        for x in range(16):
            if g[y][x] == "2":
                if x > 0 and g[y][x - 1] in ".":
                    g[y][x] = "1"
                elif x < 15 and g[y][x + 1] == ".":
                    g[y][x] = "3"
                elif y < 23 and g[y + 1][x] == "." :
                    g[y][x] = "3"
    for (x, y) in ((7, 15), (6, 11), (9, 7), (4, 18), (11, 18), (8, 19)):
        if g[y][x] in "123":
            g[y][x] = "6"
    for x in range(2, 14):
        if g[22][x] == ".":
            g[22][x] = "x"
    g = outline_into(g, "3") if False else g
    return g


@reg("flowers_bunched", "terrain")
def _():
    g = new(".")
    for (cx, base, col) in ((4, 19, 0), (9, 17, 1), (12, 20, 0), (6, 21, 1)):
        for y in range(base - 5, base + 1):
            put(g, cx, y, "g")
        put(g, cx + 1, base - 2, "G"); put(g, cx - 1, base - 1, "h")
        top = base - 6
        for dx, dy in ((0, -1), (1, 0), (-1, 0), (0, 1)):
            put(g, cx + dx, top + dy, "1" if col else "2")
        put(g, cx, top, "4")
        put(g, cx - 1, top - 1, "3"); put(g, cx + 1, top + 1, "3")
    for x in range(2, 14):
        put(g, x, 22, "x")
    return g


@reg("rusted_archway", "terrain")
def _():
    g = new(".")
    for y in range(24):
        for x in range(16):
            d = ((x - 7.5) / 7.2) ** 2 + ((y - 12) / 9.6) ** 2
            d2 = ((x - 7.5) / 4.4) ** 2 + ((y - 12) / 7.2) ** 2
            if d <= 1 and d2 > 1 and y < 22:
                g[y][x] = "2"
    for y in range(12, 22):
        for x in (1, 2, 13, 14):
            put(g, x, y, "2")
    for y in range(24):
        for x in range(16):
            if g[y][x] == "2":
                if x < 8 and (g[y][x - 1] == "." if x else True) or (y > 0 and g[y - 1][x] == "."):
                    g[y][x] = "1"
                elif (x < 15 and g[y][x + 1] == ".") or (y < 23 and g[y + 1][x] == "."):
                    g[y][x] = "3"
    rnd = random.Random(9)
    speck(g, rnd, 22, "444566", "123")
    for x, y in ((7, 2), (8, 3), (3, 6)):
        put(g, x, y, "l")
    for y in range(20, 23):
        for x in (0, 1, 2, 13, 14, 15):
            if g[y][x] == ".":
                g[y][x] = "x"
    return g


@reg("omonporch", "terrain")
def _():
    g = dirt(3)
    # back wall with arcade
    rect(g, 0, 5, 15, 8, "1")
    rect(g, 0, 9, 15, 19, "2")
    rect(g, 0, 20, 15, 23, "3")
    rect(g, 0, 8, 15, 8, "4")
    for ax in (1, 6, 11):
        for y in range(11, 21):
            for x in range(ax, ax + 4):
                if y == 11 and x in (ax, ax + 3):
                    continue
                g[y][x] = "O" if y < 19 else "3"
        put(g, ax, 10, "5"); put(g, ax + 3, 10, "5")
        for x in range(ax, ax + 4):
            put(g, x, 10, "5")
        put(g, ax + 1, 9, "5"); put(g, ax + 2, 9, "5")
    for y in range(9, 20):
        for x in (5, 10, 0, 15):
            put(g, x, y, "1" if x in (5, 10) else "2")
    rect(g, 0, 5, 15, 5, "4")
    # choking trees at the sides
    disc(g, 1, 4, 3.5, 4, "G", "g", "h")
    disc(g, 14, 3, 3.5, 3.6, "G", "g", "h")
    disc(g, 8, 2, 4, 2.2, "G", "g", "h")
    line(g, 3, 8, 3, 16, "h"); put(g, 3, 12, "g")
    for x, y in ((12, 14), (13, 17), (2, 19)):
        put(g, x, y, "g"); put(g, x, y - 1, "G")
    return g


@reg("historic_castle", "terrain")
def _():
    g = dirt(5)
    rect(g, 3, 9, 12, 20, "2")
    rect(g, 3, 9, 12, 9, "1")
    for x in range(3, 13, 2):
        rect(g, x, 7, x, 8, "1")
    rect(g, 0, 5, 3, 20, "2"); rect(g, 12, 5, 15, 20, "2")
    for tx in (0, 12):
        rect(g, tx, 5, tx + 3, 5, "1")
        for x in (tx, tx + 2):
            rect(g, x, 3, x, 4, "1")
        rect(g, tx + 3, 6, tx + 3, 20, "3")
    rect(g, 12, 9, 12, 20, "3")
    rect(g, 6, 14, 9, 20, "O"); rect(g, 6, 13, 9, 13, "6")
    put(g, 7, 12, "6"); put(g, 8, 12, "6")
    for y in (8, 12):
        put(g, 1, y, "O"); put(g, 14, y, "O")
    # flags
    line(g, 1, 0, 1, 3, "6"); put(g, 2, 0, "4"); put(g, 3, 1, "5"); put(g, 2, 1, "5")
    line(g, 14, 0, 14, 3, "6"); put(g, 13, 0, "4"); put(g, 12, 1, "5"); put(g, 13, 1, "5")
    rect(g, 3, 21, 12, 21, "3")
    return g


@reg("historic_house", "terrain")
def _():
    g = dirt(6)
    rect(g, 2, 12, 13, 21, "2")
    rect(g, 2, 21, 13, 21, "3")
    rect(g, 13, 12, 13, 20, "3")
    for i in range(7):                 # gable roof
        rect(g, 1 + i, 6 + (6 - i) - 0, 14 - i, 6 + (6 - i), "5")
    for i in range(7):
        put(g, 1 + i, 12 - i, "4"); put(g, 14 - i, 12 - i, "6")
    for y in range(7, 13):
        pass
    rect(g, 0, 12, 15, 12, "6")
    rect(g, 6, 15, 9, 21, "6"); rect(g, 7, 16, 8, 21, "O")
    rect(g, 3, 14, 4, 15, "O"); rect(g, 11, 14, 12, 15, "O")
    rect(g, 11, 2, 12, 7, "3"); rect(g, 11, 2, 11, 7, "2")
    return g


@reg("historic_pond", "terrain")
def _():
    g = dirt(7)
    disc(g, 8, 12, 7.5, 7.5, "1", "2", "3", hard=0.8)
    disc(g, 8, 12, 6.2, 6.2, "B", "b", "d", hard=0.8)
    for (x, y) in ((5, 9), (6, 9), (9, 14), (10, 14), (7, 12)):
        put(g, x, y, "B")
    # reeds
    for (x, h) in ((2, 5), (13, 6), (14, 4)):
        line(g, x, 19, x, 19 - h, "t"); put(g, x, 19 - h, "y")
    put(g, 3, 17, "g"); put(g, 12, 18, "g"); put(g, 11, 6, "g")
    return g


@reg("joppa", "terrain")
def _():
    g = dirt(8)
    for y in range(16, 24):
        for x in range(16):
            g[y][x] = "g" if (y // 2) % 2 else "h"
    for x in range(0, 16, 3):
        put(g, x, 17, "G")
    def hut(x0, y0, w, h):
        rect(g, x0, y0 + 2, x0 + w - 1, y0 + h - 1, "2")
        rect(g, x0, y0 + 2, x0 + w - 1, y0 + 2, "1")
        rect(g, x0 + w - 1, y0 + 3, x0 + w - 1, y0 + h - 1, "3")
        rect(g, x0 - 1, y0 + 1, x0 + w, y0 + 1, "5")
        rect(g, x0, y0, x0 + w - 1, y0, "4")
        rect(g, x0 + w // 2 - 1, y0 + h - 3, x0 + w // 2, y0 + h - 1, "O")
    hut(1, 8, 5, 8)
    hut(9, 9, 6, 7)
    # tower
    rect(g, 6, 3, 8, 15, "2"); rect(g, 6, 3, 6, 15, "1"); rect(g, 8, 4, 8, 15, "3")
    rect(g, 5, 2, 9, 2, "5"); rect(g, 6, 1, 8, 1, "4")
    put(g, 7, 6, "O"); put(g, 7, 10, "O")
    return g


@reg("mover_chute_bottom_opening_r", "terrain")
def _():
    g = new(".")
    rect(g, 0, 8, 15, 20, "3")
    rect(g, 0, 9, 15, 19, "2")
    rect(g, 0, 8, 15, 8, "1")
    for x in range(0, 16, 4):
        rect(g, x, 9, x, 19, "3")
    rect(g, 0, 12, 15, 12, "4"); rect(g, 0, 16, 15, 16, "4")
    for x in range(1, 15, 2):
        put(g, x, 14, "5")
    rect(g, 12, 6, 15, 21, "3"); rect(g, 12, 6, 12, 21, "1")
    rect(g, 13, 9, 15, 19, "O")
    rect(g, 13, 12, 15, 12, "4"); rect(g, 13, 16, 15, 16, "4")
    rect(g, 0, 21, 15, 22, "x")
    return g


@reg("mover_chute_top_opening_r", "terrain")
def _():
    g = new(".")
    rect(g, 0, 3, 15, 15, "3")
    rect(g, 0, 3, 15, 4, "1")
    rect(g, 0, 5, 15, 14, "2")
    for x in range(0, 16, 4):
        rect(g, x, 5, x, 14, "3")
    rect(g, 0, 8, 15, 8, "4"); rect(g, 0, 12, 15, 12, "4")
    for x in range(1, 15, 2):
        put(g, x, 10, "5")
    rect(g, 12, 2, 15, 16, "3"); rect(g, 12, 2, 12, 16, "1")
    rect(g, 13, 5, 15, 14, "O")
    rect(g, 13, 8, 15, 8, "4"); rect(g, 13, 12, 15, 12, "4")
    rect(g, 0, 16, 15, 17, "x")
    return g


@reg("reef_metal_even", "terrain")
def _():
    g = new("3")
    rnd = random.Random(21)
    # orthogonal lattice of struts with polyps
    for y in range(24):
        for x in range(16):
            if x % 8 in (0, 1) or y % 8 in (0, 1):
                g[y][x] = "l" if (x % 8 == 0 or y % 8 == 0) else "L"
    for y in range(24):
        for x in range(16):
            if g[y][x] == "3" and rnd.random() < 0.18:
                g[y][x] = "2"
    for (x, y) in ((0, 0), (8, 0), (0, 8), (8, 8), (0, 16), (8, 16)):
        put(g, x + 1, y + 1, "1")
    for (x, y) in ((3, 4), (11, 2), (4, 12), (12, 11), (3, 19), (12, 20), (10, 6), (6, 21), (13, 14)):
        put(g, x, y, "5"); put(g, x, y - 1, "4")
        put(g, x + 1, y, "6")
    for (x, y) in ((2, 2), (10, 10), (2, 10), (10, 18)):
        put(g, x, y, "1"); put(g, x + 1, y, "2"); put(g, x, y + 1, "2")
    return g


def reef(seed, pipes=False):
    rnd = random.Random(seed)
    g = new("3")
    for _ in range(26):
        put(g, rnd.randrange(16), rnd.randrange(24), "2")
    # bold arches of polyps (2px thick) with bright tips
    for _ in range(2):
        cx, cy = rnd.randrange(4, 12), rnd.randrange(10, 20)
        r = rnd.randrange(3, 5)
        for a in range(0, 181, 15):
            x = round(cx + r * math.cos(math.radians(a)))
            y = round(cy - r * 1.2 * math.sin(math.radians(a)))
            put(g, x, y, "1"); put(g, x, y + 1, "2"); put(g, x + 1, y + 1, "2")
            if a % 45 == 0:
                put(g, x, y - 1, "4"); put(g, x - 1, y - 1, "6")
        put(g, cx - r, cy + 1, "2"); put(g, cx + r, cy + 1, "2")
        put(g, cx - r, cy + 2, "2"); put(g, cx + r, cy + 2, "2")
    for _ in range(6):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 22)
        put(g, x, y, "5"); put(g, x + 1, y, "4"); put(g, x, y + 1, "6")
    if pipes:
        for y in (5, 15):
            rect(g, 0, y, 15, y + 1, "l"); rect(g, 0, y + 2, 15, y + 2, "L")
            for x in (3, 11):
                rect(g, x, y - 1, x + 1, y + 3, "4")
        rect(g, 7, 0, 8, 23, "5"); rect(g, 7, 0, 7, 23, "4")
    else:
        y = rnd.randrange(13, 19)
        for x in range(16):
            put(g, x, y + (x // 4) % 2, "l" if x % 2 else "L")
    return g


S["reef_worldmap"] = rows(reef(31)); KINDS["reef_worldmap"] = "terrain"
for _n, _s in (("1l", 41), ("2j", 42), ("4h", 44), ("4n", 45), ("5i", 46), ("5m", 47), ("6l", 48)):
    S["terrainpalladiumreef_" + _n] = rows(reef(_s)); KINDS["terrainpalladiumreef_" + _n] = "terrain"
S["terrainpalladiumreef_3l"] = rows(reef(43, pipes=True)); KINDS["terrainpalladiumreef_3l"] = "terrain"


# ---------- rivers / lakes ----------
def watercell(g, rnd, water_set):
    """Shade water: edges dark (3) next to land, ripples light (1)."""
    h = [r[:] for r in g]
    for y in range(24):
        for x in range(16):
            if g[y][x] in "2":
                for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                    xx, yy = x + dx, y + dy
                    if 0 <= xx < 16 and 0 <= yy < 24 and g[yy][xx] not in "2":
                        h[y][x] = "3"
                        break
    for y in range(24):
        for x in range(16):
            if h[y][x] == "2" and rnd.random() < 0.09:
                h[y][x] = "1"
                if x < 15 and h[y][x + 1] == "2":
                    h[y][x + 1] = "1"
    return h


def trees_small(g, pts):
    for (x, y) in pts:
        rect(g, x, y, x + 2, y + 1, "G"); rect(g, x, y + 1, x + 2, y + 2, "g")
        put(g, x + 1, y + 3, "n")
        put(g, x + 2, y + 2, "h")


def peaks(g, pts):
    for (cx, top, hgt) in pts:
        for i in range(hgt):
            for x in range(cx - i, cx + i + 1):
                put(g, x, top + i, "l" if x < cx else ("L" if x > cx else "w"))
        put(g, cx, top, "w")
        if hgt > 3:
            put(g, cx - 1, top + 1, "w")


def river(edges, deco, seed):
    rnd = random.Random(seed)
    g = land(seed)
    w = {"N": (5, 0, 10, 12), "S": (5, 12, 10, 23), "W": (0, 9, 8, 14), "E": (8, 9, 15, 14)}
    for e in edges:
        x0, y0, x1, y1 = w[e]
        # slight meander
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                put(g, x, y, "2")
    # soften corners
    for (x, y) in ((5, 12), (10, 12)):
        pass
    disc(g, 7.5, 11.5, 3.5, 3.3, "2", "2", "2", hard=2)
    # round off hard rectangle corners at ends
    g = watercell(g, rnd, "2")
    if deco == "mount":
        free = [(2, 3, 4), (13, 19, 4)] if "N" in edges and "W" in edges else [(3, 16, 4), (12, 3, 4)]
        peaks(g, [(2, 15, 3)] if False else [(p[0], p[1], p[2]) for p in free[:2]])
        for p in free[:2]:
            pass
    elif deco == "trees":
        trees_small(g, [(1, 1), (12, 18)])
    return g


RIV = {
    "11b": ("NW", "trees"), "1b": ("SE", "trees"), "3b": ("SW", "mount"),
    "7b": ("NSW", "mount"), "9b": ("NE", "mount"), "13b": ("E", "chrome"),
}
for _n, (_e, _d) in RIV.items():
    _g = river(_e, _d, hash(_n) % 1000 if False else sum(map(ord, _n)))
    if _d == "chrome":
        # river ends: lake mouth, chrome giants' carcasses on the bank
        for (x, y) in ((2, 4), (3, 4), (4, 4), (2, 5), (3, 6), (12, 18), (13, 18), (13, 19), (11, 19)):
            put(_g, x, y, "l")
        put(_g, 2, 4, "w"); put(_g, 12, 18, "w")
        for (x, y) in ((3, 5), (4, 5), (12, 19)):
            put(_g, x, y, "L")
    S["river_worldmap_" + _n] = rows(_g); KINDS["river_worldmap_" + _n] = "terrain"


@reg("river_lake_we", "terrain")
def _():
    rnd = random.Random(13)
    g = land(13)
    for x in range(16):
        top = 7 + round(1.2 * math.sin(x / 2.5))
        bot = 17 + round(1.2 * math.sin(x / 2.8 + 1))
        rect(g, x, top, x, bot, "2")
    g = watercell(g, rnd, "2")
    for x in range(0, 16, 5):
        put(g, x, 6, "t")
    put(g, 3, 3, "h"); put(g, 12, 21, "t"); put(g, 13, 20, "t")
    return g


# svy lake pieces: shoreline sets
def lake(seed, shores, trees=0, island=False, extra=None):
    rnd = random.Random(seed)
    g = land(seed)
    for y in range(24):
        for x in range(16):
            g[y][x] = "2"
    land_cells = set()
    for s in shores:
        depth = rnd.randrange(3, 6)
        for y in range(24):
            for x in range(16):
                wob = round(1.3 * math.sin((x if s in "NS" else y) / 2.2 + seed))
                if s == "N" and y < depth + wob: land_cells.add((x, y))
                if s == "S" and y > 23 - depth - wob: land_cells.add((x, y))
                if s == "W" and x < depth - 1 + wob: land_cells.add((x, y))
                if s == "E" and x > 16 - depth + wob: land_cells.add((x, y))
    L = land(seed + 100)
    for (x, y) in land_cells:
        g[y][x] = L[y][x]
    if island:
        disc(g, 8, 12, 3, 2.4, "G", "g", "h")
    g = watercell(g, rnd, "2")
    return g


def openwater(seed):
    """Open water filling the whole tile (pieces of one big lake): no shore, only ripples."""
    rnd = random.Random(seed)
    g = new("2")
    for _ in range(9):
        x, y = rnd.randrange(0, 13), rnd.randrange(0, 24)
        for k in range(rnd.randrange(2, 4)):
            put(g, x + k, y, "1")
    for _ in range(7):
        x, y = rnd.randrange(0, 14), rnd.randrange(0, 24)
        put(g, x, y, "3"); put(g, x + 1, y, "3")
    return g


for _n in ("1j", "3e", "3i", "4f", "5d", "6f", "7b", "7f", "blank"):
    S["svylake_worldmap_" + _n] = rows(openwater(sum(map(ord, _n)) + 7)); KINDS["svylake_worldmap_" + _n] = "terrain"


def hinnom(seed):
    rnd = random.Random(seed)
    g = openwater(seed)
    for _ in range(3):   # algal bloom
        cx, cy = rnd.randrange(3, 13), rnd.randrange(3, 21)
        for _ in range(7):
            x, y = cx + rnd.randrange(-2, 3), cy + rnd.randrange(-2, 3)
            put(g, x, y, rnd.choice("456"))
    if rnd.random() < 0.6:   # coral finger poking through
        x, y = rnd.randrange(3, 12), rnd.randrange(5, 19)
        put(g, x, y, "M"); put(g, x, y - 1, "M"); put(g, x, y + 1, "r"); put(g, x + 1, y, "r")
    for _ in range(4):       # esh flock
        put(g, rnd.randrange(1, 15), rnd.randrange(1, 23), "w")
    return g


for _n in ("2c", "2m", "3e", "4c", "4m", "6b", "6i", "7c", "7g", "7l", "8d", "9c", "9g"):
    S["terrainlakehinnom_" + _n] = rows(hinnom(sum(map(ord, _n)) * 3)); KINDS["terrainlakehinnom_" + _n] = "terrain"


# ---------- world-map landscape icons ----------
@reg("hills", "terrain")
def _():
    g = new("2")           # sandy ground
    rnd = random.Random(3)
    speck(g, rnd, 14, "1", "2")
    speck(g, rnd, 10, "3", "2")
    def mesa(x0, x1, top, base):
        w = x1 - x0 + 1
        rect(g, x0, top, x1, top + 1, "1")          # flat lit top
        rect(g, x0, top + 2, x1, base, "2")
        for y in range(top + 2, base + 1):          # strata: dark crease every 3rd row, light band between
            k = (y - top) % 3
            if k == 0:
                rect(g, x0, y, x1, y, "6")
            elif k == 1:
                rect(g, x0, y, x1 - 2, y, "1")
        rect(g, x1 - 1, top + 2, x1, base, "3")     # shadow face on the right
        rect(g, x0, top + 1, x1, top + 1, "6")
        rect(g, x0, base + 1, x1, base + 1, "3")
        rect(g, x0 + 1, base + 2, x1 + 1, base + 2, "3")
    mesa(0, 6, 1, 10)
    mesa(9, 15, 7, 17)
    # winding canyon cleft between and below them
    path = [(7, 0), (7, 3), (8, 6), (8, 9), (7, 12), (6, 15), (6, 18), (7, 21), (8, 23)]
    for (x, y), (x2, y2) in zip(path, path[1:]):
        for yy in range(y, y2 + 1):
            xx = round(x + (x2 - x) * (yy - y) / max(1, y2 - y))
            put(g, xx, yy, "O"); put(g, xx + 1, yy, "O") if 4 < yy < 20 else None
            put(g, xx - 1, yy, "3") if g[yy][xx - 1] != "O" else None
    for x in range(0, 6):
        put(g, x, 14, "6"); put(g, x, 15, "3")
    for x in range(10, 16):
        put(g, x, 20, "6"); put(g, x, 21, "3")
    return g


@reg("spindle_mid", "terrain")
def _():
    g = land(5, "h")
    # the Spindle: pale tower, shadow cast onto grove
    rect(g, 7, 0, 9, 14, "1"); rect(g, 9, 0, 9, 14, "2")
    rect(g, 6, 14, 10, 17, "2"); rect(g, 10, 14, 10, 17, "3")
    for y in range(2, 14, 4):
        rect(g, 7, y, 8, y, "4")
    for y in range(18, 24):
        rect(g, 9, y, min(15, 9 + (y - 17) * 1), y, "g") if False else None
    # palm fronds
    for (cx, cy) in ((3, 18), (12, 20), (3, 7), (13, 9), (11, 4)):
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1, -1), (1, 1), (1, -1), (-1, 1)):
            put(g, cx + dx, cy + dy, "g")
        put(g, cx, cy, "y"); put(g, cx - 1, cy - 1, "G"); put(g, cx + 1, cy - 1, "G")
        put(g, cx + 1, cy, "G")
    # spindle's shadow
    for y in range(17, 24):
        for x in range(10, 16):
            if g[y][x] in "ghG":
                g[y][x] = "h"
    return g


@reg("tile_kya", "terrain")
def _():
    g = land(8, "h")
    def shroom(cx, top, rx, stem):
        disc(g, cx, top + 2, rx, 2.8, "1", "2", "3", hard=.6)
        for dx in (-rx + 2, 0, rx - 2):
            put(g, round(cx + dx * .6), top + 1, "5")
        put(g, cx - 1, top + 1, "4")
        rect(g, cx - 1, top + 5, cx, top + 5 + stem, "t")
        put(g, cx, top + 5 + stem, "N") if False else None
        rect(g, cx - 1, top + 3 + stem, cx, top + 5 + stem, "t")
        rect(g, cx, top + 4, cx, top + 5 + stem, "n")
        put(g, cx - 1, top + 6 + stem, "O") if False else None
    shroom(4, 11, 4.4, 4)
    shroom(11, 3, 4.6, 4)
    shroom(11, 14, 3.6, 4)
    shroom(5, 2, 3.2, 2)
    for x, y in ((4, 18), (10, 11)):
        pass
    return g


@reg("worldmap_musa", "terrain")
def _():
    g = land(9, "g")
    rnd = random.Random(9)
    for (cx, cy) in ((4, 4), (11, 5), (3, 12), (12, 13), (7, 9), (5, 19), (12, 20), (8, 3)):
        put(g, cx, cy, "n")
        for dx, dy in ((-2, -1), (-1, -1), (1, -1), (2, -1), (0, -1), (-1, -2), (1, -2), (0, -2), (-2, 0), (2, 0)):
            put(g, cx + dx, cy + dy, "h" if dx and dy == 0 else rnd.choice("GgG"))
        put(g, cx + 1, cy + 1, "W") if False else put(g, cx, cy + 1, "y")
    return g


# ---------- tall plants and trees ----------
def clump(g, cx, cy, rx, ry, hi="1", mid="2", lo="3", hard=.72):
    disc(g, cx, cy, rx, ry, hi, mid, lo, hard)


@reg("bigtree", "tall")
def _():
    g = new(".")
    rnd = random.Random(2)
    for (cx, cy, rx, ry) in ((4, 8, 4, 4.4), (11.5, 8, 4.3, 4.4), (8, 4.5, 5.2, 4.2), (8, 10, 6.5, 4)):
        clump(g, cx, cy, rx, ry)
    # trunk
    for y in range(12, 22):
        w = 5 if y < 19 else 7
        x0 = 8 - w // 2
        for x in range(x0, x0 + w):
            g[y][x] = "n" if x < x0 + w // 2 else "N"
        if y % 3 == 0:
            g[y][x0 + 1] = "w"
    for y in range(12, 17):               # shade under canopy
        for x in range(5, 12):
            if g[y][x] in "nN" and y < 14:
                g[y][x] = "N"
    speck(g, rnd, 16, "4", "12")
    for x in range(2, 14):
        put(g, x, 22, "x")
    return g


@reg("dogthorn", "tall")
def _():
    g = new(".")
    rnd = random.Random(6)
    for (cx, cy, rx, ry) in ((4, 8, 3.6, 3), (11, 7, 3.8, 3.2), (7.5, 4.5, 4.6, 3.2), (8, 10, 5, 2.8)):
        clump(g, cx, cy, rx, ry, "G", "g", "h")
    # trunk, splintered
    for y in range(11, 20):
        rect(g, 7, y, 8, y, "n"); put(g, 8, y, "N")
    for (x, y, dx) in ((6, 13, -1), (9, 14, 1), (6, 16, -1), (9, 17, 1)):
        put(g, x, y, "w"); put(g, x + dx, y - 1, "w")
    # tangled roots
    for (x0, dx) in ((7, -1), (8, 1)):
        x = x0
        for y in range(19, 22):
            put(g, x, y, "N"); x += dx
        put(g, x, 21, "n")
    line(g, 4, 21, 7, 19, "N"); line(g, 11, 20, 8, 19, "N"); put(g, 3, 20, "N")
    # thorns around canopy
    for (x, y) in ((1, 5), (2, 10), (14, 5), (13, 10), (5, 1), (10, 1), (8, 0), (2, 3), (14, 8), (4, 11), (11, 11)):
        put(g, x, y, "w")
    for (x, y, dx, dy) in ((0, 4, -1, -1), (15, 4, 1, -1), (3, 1, -1, -1), (12, 1, 1, -1), (1, 11, -1, 1), (14, 11, 1, 1)):
        put(g, x, y, "w"); put(g, x + dx, y + dy, "w")
    speck(g, rnd, 8, "3", "g")
    for x in range(3, 13):
        put(g, x, 22, "x")
    return g


@reg("moon_and_sun_shade", "tall")
def _():
    g = new(".")
    rnd = random.Random(12)
    for (cx, cy, rx, ry) in ((4.5, 8, 4, 3.6), (11.5, 8, 4, 3.6), (8, 5, 5.5, 4), (8, 9, 6.5, 3)):
        clump(g, cx, cy, rx, ry)
    for (cx, cy) in ((4, 6), (9, 3), (12, 8), (6, 10), (9, 11), (2, 9)):
        put(g, cx, cy, "w")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            put(g, cx + dx, cy + dy, "4")
    # dripping star leaves
    for x in (3, 7, 12):
        put(g, x, 12, "4"); put(g, x, 13, "5") if x != 7 else None
    for y in range(12, 21):
        rect(g, 7, y, 8, y, "n"); put(g, 8, y, "N")
    line(g, 5, 21, 7, 19, "n"); line(g, 10, 21, 8, 19, "N")
    # shadow with roots
    for x in range(1, 15):
        put(g, x, 22, "x")
    for x in range(3, 13):
        put(g, x, 21, "x") if g[21][x] == "." else None
    return g


@reg("starapple", "tall")
def _():
    g = new(".")
    rnd = random.Random(4)
    # ashen branching trunk
    line(g, 8, 21, 8, 11, "l"); line(g, 9, 21, 9, 12, "L")
    line(g, 8, 13, 3, 6, "l"); line(g, 8, 12, 13, 5, "l"); line(g, 8, 11, 8, 2, "l")
    line(g, 6, 9, 2, 10, "l") if False else None
    for (cx, cy, rx, ry) in ((3.5, 6, 3.4, 3), (12.5, 5, 3.4, 3), (8, 3.5, 3.8, 2.8), (6, 10, 3, 2.2), (11, 10, 3, 2.2)):
        clump(g, cx, cy, rx, ry)
    for (x, y) in ((3, 8), (12, 7), (7, 6), (10, 12), (5, 12), (8, 9)):
        put(g, x, y, "4"); put(g, x, y + 1, "5"); put(g, x, y - 1, "w") if False else None
    put(g, 2, 4, "w")
    for x in range(4, 13):
        put(g, x, 22, "x")
    return g


@reg("tree_banana", "tall")
def _():
    g = new(".")
    for y in range(8, 22):
        put(g, 7 + (1 if y > 14 else 0), y, "n"); put(g, 8 + (1 if y > 14 else 0), y, "N")
    for (x, y) in ((6, 11), (6, 14), (8, 17)):
        put(g, x, y, "n")
    # fronds
    for (ex, ey) in ((1, 6), (0, 11), (14, 11), (15, 6), (8, 0), (4, 1), (12, 1)):
        line(g, 8, 6, ex, ey, "2")
        line(g, 8, 7, ex, ey + 1, "3") if ex not in (8,) else None
        mid = ((8 + ex) // 2, (6 + ey) // 2)
        put(g, mid[0], mid[1] - 1, "1")
        put(g, (8 + ex * 3) // 4, (6 + ey * 3) // 4 - 1, "1")
    clump(g, 8, 6, 2, 1.6)
    # hanging bunch of bananas
    for y in range(8, 12):
        put(g, 10, y, "4"); put(g, 11, y, "5") if y > 8 else None
    put(g, 11, 12, "6"); put(g, 10, 12, "5")
    for x in range(4, 13):
        put(g, x, 22, "x")
    return g


TC = [
    "................",
    "..11111.........",
    ".1122222........",
    ".12.....2.......",
    ".12..1..2..111..",
    ".12.12..2.12.22.",
    ".12.12222.12..2.",
    "..12......12.12.",
    "...22.11.12..2..",
    "....22221...33..",
    ".....3333.......",
    "........3.......",
    ".......3n.......",
    "......3n........",
    "......nn........",
    "......nNn.......",
    ".....nnN........",
    ".....nN.........",
    ".....nNN........",
    "....nnNN........",
    "...nnnNNn.......",
    "..xxxxxxxxx.....",
    "................",
    "................",
]
# nachash tree: slouching trunk with moss shoots coiling at the crown (hand drawn)
S["tree_curly"] = [
    "................",
    "...1111..1111...",
    "..122221122221..",
    "..12..2112..21..",
    "..12.12112.12.1.",
    "..1..1.22.1.2.1.",
    ".111122..22.2111",
    ".1222.3..3.22221",
    ".12...22222...21",
    ".1.1.3....3.1.1.",
    "..1.22.11.22.1..",
    "...12.2112.21...",
    "....22.23.22....",
    ".....33.3.33....",
    "......3.n.3.....",
    ".......nn.......",
    ".......nNn......",
    "......nnN.......",
    "......nNN.......",
    ".....nnNN.......",
    "....nnnNNn......",
    "..xxxxxxxxxx....",
    "................",
    "................",
]
KINDS["tree_curly"] = "tall"


@reg("watervine", "tall")
def _():
    g = new(".")
    rnd = random.Random(7)
    for x in (3, 8, 12):
        h = rnd.randrange(8, 12)
        for k in range(h):
            put(g, x + (1 if k % 4 > 1 else 0), 20 - k, "1" if k % 3 else "2")
        # wafers instead of leaves
        for k in range(2, h, 2):
            yy = 20 - k
            put(g, x - 1, yy, "4"); put(g, x - 2, yy, "5")
            put(g, x + 2, yy - 1, "4"); put(g, x + 3, yy - 1, "5")
    for x in range(1, 15):
        put(g, x, 21, "x")
    return g


SPRITES = S
for _k, _v in KEYS.items():
    assert _v in SPRITES, (_k, _v)
