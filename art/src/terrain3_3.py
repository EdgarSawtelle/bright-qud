"""Terrain batch 3 (ground decorations, plants, ruins, world-map tiles). Procedural 16x24 grids."""
import math
import random

from terrain_keys import BATCH_KEYS

KEYS = BATCH_KEYS[3]
W_, H_ = 16, 24


class C:
    def __init__(self, fill="."):
        self.g = [[fill] * W_ for _ in range(H_)]

    def p(self, x, y, c):
        x, y = int(round(x)), int(round(y))
        if 0 <= x < W_ and 0 <= y < H_:
            self.g[y][x] = c

    def get(self, x, y):
        return self.g[y][x] if 0 <= x < W_ and 0 <= y < H_ else "."

    def rect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(x, y, c)

    def ell(self, cx, cy, rx, ry, c, shade=None):
        """Filled ellipse. shade=(light, mid, dark) gives top-left light, bottom-right dark."""
        for y in range(H_):
            for x in range(W_):
                d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
                if d <= 1:
                    if shade:
                        t = ((x - cx) / rx + (y - cy) / ry)
                        self.g[y][x] = shade[0] if t < -0.5 else (shade[2] if t > 0.6 else shade[1])
                    else:
                        self.g[y][x] = c

    def line(self, x0, y0, x1, y1, c):
        n = int(max(abs(x1 - x0), abs(y1 - y0))) * 2 + 1
        for i in range(n + 1):
            t = i / n
            self.p(x0 + (x1 - x0) * t, y0 + (y1 - y0) * t, c)

    def speckle(self, rnd, chars, n, only=None):
        for _ in range(n):
            x, y = rnd.randrange(W_), rnd.randrange(H_)
            if only is None or self.g[y][x] in only:
                self.g[y][x] = rnd.choice(chars)

    def rows(self):
        return ["".join(r) for r in self.g]


def noise_fill(c, rnd, base, alts, prob):
    for y in range(H_):
        for x in range(W_):
            c.g[y][x] = rnd.choice(alts) if rnd.random() < prob else base


def tri(c, cx, top, base_y, half, light, dark, snow=None, snow_h=0):
    """Mountain peak: lit left, dark right."""
    for y in range(top, base_y + 1):
        w = (y - top) * half / max(1, base_y - top)
        for x in range(W_):
            dx = x - cx
            if -w <= dx <= w:
                ch = light if dx < w * 0.1 else dark
                if snow and y - top < snow_h:
                    ch = snow if dx < w * 0.1 else "l"
                c.p(x, y, ch)
    c.p(cx, top, snow or light)


SPR = {}
KIND = {}


def reg(name, c, kind="terrain"):
    SPR[name] = c.rows() if isinstance(c, C) else c
    KIND[name] = kind


# ------------------------------------------------------------------ ground decorations
def arsplice():
    c = C()
    cx, cy, rx, ry = 7.5, 12.5, 6, 6.5
    pts = []
    for i in range(11):
        a = i / 11 * 2 * math.pi
        pts.append((cx + rx * math.cos(a), cy + ry * math.sin(a)))
    pts.sort(key=lambda q: q[1])
    for x, y in pts:
        x, y = int(round(x)), int(round(y))
        c.p(x, y + 1, "3")  # stem
        c.rect(x - 1, y, x + 1, y, "1")
        c.p(x - 1, y - 1, "2"); c.p(x, y - 1, "1"); c.p(x + 1, y - 1, "2")
        c.p(x + 1, y, "2")
        c.p(x, y - 1, "4")
    # faint threads inside the ring
    for x, y in ((7, 12), (8, 13), (6, 14), (9, 11)):
        c.p(x, y, "3")
    return c
reg("arsplice_hyphae_unripe_odd", arsplice())


def chavvah_branch():
    rnd = random.Random(5)
    c = C("3")
    for y in range(H_):
        for x in range(W_):
            if (x + y) % 5 == 0:
                c.g[y][x] = "2"
    def branch(x, y, ang, ln, depth):
        for i in range(ln):
            nx, ny = x + math.cos(ang), y + math.sin(ang)
            c.p(nx, ny, "1" if depth > 1 else "2")
            if depth > 1:
                c.p(nx + 1, ny, "2")
            x, y = nx, ny
        c.p(x, y, "w")
        if depth > 0:
            branch(x, y, ang - 0.55, ln * 2 // 3 + 1, depth - 1)
            branch(x, y, ang + 0.5, ln * 2 // 3 + 1, depth - 1)
    branch(7.5, 22, -math.pi / 2, 7, 3)
    for _ in range(9):
        c.p(rnd.randrange(16), rnd.randrange(24), "4")
    for x, y in ((3, 6), (12, 9), (2, 15), (13, 17)):
        c.p(x, y, "4"); c.p(x, y - 1, "w")
    return c
reg("chavvah_branch_floor", chavvah_branch())


def chavvah_leaves():
    c = C()
    for x, y, big in ((3, 5, 0), (11, 7, 1), (6, 12, 1), (12, 15, 0), (2, 18, 1), (8, 20, 0), (9, 3, 0)):
        c.p(x, y, "1"); c.p(x - 1, y, "2"); c.p(x + 1, y, "3"); c.p(x, y - 1, "1"); c.p(x, y + 1, "2")
        if big:
            c.p(x, y - 2, "2"); c.p(x, y + 2, "3")
            c.p(x - 1, y - 1, "w")
        c.p(x + 2, y + 1, "4")
    return c
reg("chavvah_leaves_sparse", chavvah_leaves())


def chavvah_world():
    rnd = random.Random(11)
    c = C("w")
    for y in range(H_):
        for x in range(W_):
            if rnd.random() < 0.25:
                c.g[y][x] = "l"
    for x in range(W_):  # marble veins
        c.p(x, 3 + (x // 3) % 2, "l")
    # fallen leaf carpet
    c.ell(7.5, 19, 7, 3.5, "4")
    c.speckle(rnd, ["1", "4", "y"], 30, only="4")
    # crown
    c.ell(7.5, 8, 7, 7, None, shade=("1", "2", "3"))
    c.speckle(rnd, ["4", "M", "w"], 14, only="123")
    # cloven trunk
    c.rect(5, 14, 7, 20, "n"); c.rect(9, 14, 10, 20, "N")
    c.rect(5, 14, 5, 20, "t"); c.rect(8, 14, 8, 20, "O")
    c.rect(4, 20, 11, 20, "N")
    return c
reg("chavvah_worldmap", chavvah_world())


def cyberterminal():
    c = C("e")
    c.rect(0, 0, 15, 23, "L")
    c.rect(0, 0, 15, 1, "1")
    c.rect(0, 22, 15, 23, "3")
    # glass arch
    for y in range(2, 14):
        for x in range(1, 15):
            r = 6.5
            inside = (y >= 8 and 2 <= x <= 13) or (((x - 7.5) ** 2 + (y - 8) ** 2) <= r * r)
            if inside:
                c.p(x, y, "3")
    for y in range(2, 14):
        for x in range(1, 15):
            if c.get(x, y) == "3":
                edge = any(c.get(x + dx, y + dy) != "3" for dx, dy in ((1, 0), (-1, 0), (0, -1)))
                if edge:
                    c.p(x, y, "c")
    # glyph screen
    c.rect(4, 5, 11, 8, "O")
    for x in (5, 7, 8, 10):
        c.p(x, 6, "4")
    for x in (5, 6, 9, 10):
        c.p(x, 7, "5")
    c.p(7, 4, "4"); c.p(8, 4, "4")
    # neutrofoam bed with human imprint
    c.rect(2, 14, 13, 21, "w")
    c.rect(2, 14, 13, 14, "l")
    c.rect(2, 21, 13, 21, "l")
    c.ell(7.5, 17.5, 1.6, 1.6, "L")       # head
    c.rect(6, 19, 9, 21, "L")             # torso
    c.rect(4, 18, 5, 20, "L"); c.rect(10, 18, 11, 20, "L")
    # blinding light
    c.p(1, 12, "Y"); 
    for x, y in ((1, 3), (14, 3), (1, 12), (14, 12)):
        c.p(x, y, "y")
    return c
reg("cyberterminal", cyberterminal())


def extrasolar():
    c = C()
    pts = []
    for i in range(0, 80):
        t = i / 79
        y = 21 - t * 18
        x = 7.5 + math.sin(t * 7.5) * (4.2 - t * 1.5)
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        c.p(x, y, "2"); c.p(x + 1, y, "1" if i % 2 else "2")
    for i, (x, y) in enumerate(pts):
        if i % 9 == 0:
            c.p(x + 2, y, "4"); c.p(x + 2, y - 1, "5")
    x, y = pts[-1]
    c.ell(x + 1, y - 1, 1.5, 1.5, "4")
    c.p(x + 1, y - 1, "w")
    for y in range(18, 22):
        c.p(7, y, "3"); c.p(8, y, "3")
    return c
reg("extrasolar_vine", extrasolar(), "tall")


def hilbert(n):
    def d2xy(n, d):
        t = d
        x = y = 0
        s = 1
        while s < n:
            rx = 1 & (t // 2)
            ry = 1 & (t ^ rx)
            if ry == 0:
                if rx == 1:
                    x = s - 1 - x
                    y = s - 1 - y
                x, y = y, x
            x += s * rx
            y += s * ry
            t //= 4
            s *= 2
        return x, y
    return [d2xy(n, d) for d in range(n * n)]


def fracti():
    c = C()
    pts = hilbert(8)
    sc = [(x * 2 + 0.5, y * 2 + 4.5) for x, y in pts]
    for (x0, y0), (x1, y1) in zip(sc, sc[1:]):
        c.line(x0, y0, x1, y1, "2")
    for i, (x, y) in enumerate(sc):
        c.p(x, y, "1")
        if i % 3 == 0:
            c.p(x + 1, y + 1, "3")
        if i % 4 == 1:
            c.p(x, y - 1, "4")
    return c
reg("fracti", fracti())


def hex_dotted():
    c = C()
    centers = []
    for j in range(-1, 6):
        for i in range(-1, 4):
            centers.append((i * 8 + (4 if j % 2 else 0) + 0.5, j * 5 + 2))
    for y in range(H_):
        for x in range(W_):
            ds = sorted(math.hypot((x - cx) * 0.9, y - cy) for cx, cy in centers)
            if ds[1] - ds[0] < 0.9:
                c.p(x, y, "3")
            else:
                c.p(x, y, "2" if (x + y) % 7 else "1")
    for cx, cy in centers:
        c.p(cx, cy, "1"); c.p(cx + 1, cy, "1")
    return c
reg("hex_dotted", hex_dotted())


# ------------------------------------------------------------------ historic world-map icons
def earth(seed):
    rnd = random.Random(seed)
    c = C("e")
    c.speckle(rnd, ["E"], 40)
    return c


def hist_arms():
    c = earth(1)
    c.line(2, 4, 13, 19, "l"); c.line(3, 4, 14, 19, "L")
    c.line(13, 4, 2, 19, "l"); c.line(12, 4, 1, 19, "L")
    c.rect(1, 18, 4, 18, "y"); c.rect(11, 18, 14, 18, "y")
    # shield
    for y in range(7, 20):
        w = 5 if y < 14 else max(0, 5 - (y - 13))
        for x in range(8 - w, 8 + w):
            c.p(x, y, "4" if (x < 8) else "5")
    for y in range(7, 20):
        for x in range(16):
            if c.get(x, y) in "45":
                e = any(c.get(x + dx, y + dy) not in "45" for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if e:
                    c.p(x, y, "1")
    c.rect(7, 9, 8, 17, "1"); c.rect(4, 11, 11, 12, "2")
    return c
reg("historic_arms", hist_arms())


def hist_grid():
    c = earth(2)
    for r in range(3):
        for k in range(3):
            x0, y0 = 1 + k * 5, 1 + r * 7
            c.rect(x0, y0, x0 + 3, y0 + 2, "4" if k != 1 else "5")
            c.rect(x0, y0 + 3, x0 + 3, y0 + 5, "1")
            c.rect(x0, y0 + 5, x0 + 3, y0 + 5, "3")
            c.p(x0 + 1, y0 + 4, "O")
            c.p(x0 + 2, y0 + 4, "2")
    return c
reg("historic_grid", hist_grid())


def hist_huts():
    c = earth(3)
    for cx, by in ((4, 9), (11, 8), (7, 15), (3, 20), (12, 20)):
        c.rect(cx - 2, by, cx + 2, by + 2, "1")
        c.rect(cx - 2, by + 2, cx + 2, by + 2, "3")
        c.p(cx, by + 1, "O"); c.p(cx, by + 2, "O")
        for i in range(4):
            c.rect(cx - 1 - i // 1 if False else cx - 3 + i, by - 3 + i, cx + 3 - i, by - 3 + i, "4" if i < 2 else "5")
        c.rect(cx - 3, by - 1, cx + 3, by - 1, "5")
        c.p(cx, by - 4, "6")
    return c
reg("historic_huts", hist_huts())


def hist_ring():
    c = earth(4)
    for y in range(24):
        for x in range(16):
            d = math.hypot((x - 7.5) / 7, (y - 11.5) / 10)
            if 0.75 < d <= 1:
                c.p(x, y, "1" if (x + y) % 2 else "2")
            elif 1 < d <= 1.1:
                c.p(x, y, "3")
    for x, y in ((7, 2), (8, 2), (7, 21), (8, 21), (1, 11), (14, 11)):
        c.rect(x - 1, y - 1, x + 1, y + 1, "4")
        c.p(x, y, "5")
    c.rect(6, 9, 9, 13, "1"); c.rect(6, 13, 9, 13, "3"); c.rect(6, 8, 9, 8, "5")
    return c
reg("historic_ring", hist_ring())


# ------------------------------------------------------------------ world map land
def marsh():
    rnd = random.Random(21)
    c = C("2")
    noise_fill(c, rnd, "2", ["1", "3"], 0.2)
    for cx, cy, rx, ry in ((4.5, 6, 4, 2.5), (11, 12, 4.5, 3), (5, 18, 4, 2.5)):
        c.ell(cx, cy, rx + 1, ry + 1, "3")
        c.ell(cx, cy, rx, ry, "b")
        c.ell(cx - 1, cy - 1, rx - 2, ry - 1, "B")
        c.ell(cx, cy, rx - 1, ry - 1, "b")
        c.p(cx + 1, cy, "M"); c.p(cx - 1, cy + 1, "w"); c.p(cx + 2, cy - 1, "w")
    for x, y in ((2, 11), (13, 5), (9, 20), (13, 19), (9, 4)):
        for k in range(4):
            c.p(x, y - k, "h" if k % 2 else "g")
        c.p(x + 1, y - 3, "G")
    return c
reg("marsh_worldmap", marsh())


def mountains():
    rnd = random.Random(31)
    c = C("2")
    noise_fill(c, rnd, "2", ["1", "3"], 0.08)
    peaks = ((12, 9, 20, 5), (6, 3, 21, 8))  # cx, top, base, half-width (back to front)
    for cx, top, base, half in peaks:
        mask = set()
        for y in range(top, base + 1):
            w = (y - top) * half / (base - top)
            for x in range(W_):
                if abs(x - cx) <= w + 0.3:
                    mask.add((x, y))
        for x, y in mask:
            dx = x - cx
            w = (y - top) * half / (base - top)
            sn = y - top < 3 + (top < 8)
            if dx < 0:
                ch = "w" if sn else ("1" if (x + 2 * y) % 6 else "2")
            elif dx == 0 and not sn:
                ch = "O"
            else:
                ch = "l" if sn else ("3" if (x * 2 + y) % 6 else "2")
            if dx > 0 and not sn and (x + y) % 7 == 0:
                ch = "2"
            c.p(x, y, ch)
        for x, y in mask:  # dark outline
            if any((x + ex, y + ey) not in mask for ex, ey in ((1, 0), (-1, 0), (0, -1))):
                if c.get(x, y) not in "w":
                    c.p(x, y, "O" if x > cx else "3")
    c.rect(0, 21, 15, 23, "3")
    for x in range(16):
        if (x * 3) % 5 < 2:
            c.p(x, 21, "2")
        if x % 4 == 1:
            c.p(x, 22, "1")
    return c
reg("mountains", mountains())


def mover():
    c = C()
    c.rect(0, 8, 15, 15, "3")
    c.rect(0, 8, 15, 9, "1")
    c.rect(0, 9, 15, 9, "2")
    c.rect(0, 10, 15, 13, "O")
    c.rect(0, 14, 15, 15, "3")
    c.rect(0, 15, 15, 15, "2")
    for x in (3, 8, 13):  # chevrons >
        c.p(x, 10, "4"); c.p(x + 1, 11, "4"); c.p(x + 1, 12, "4"); c.p(x, 13, "4")
        c.p(x - 1, 11, "5"); c.p(x - 1, 12, "5")
    for x in (1, 7, 14):
        c.p(x, 16, "x")
    c.rect(1, 16, 14, 16, "x")
    return c
reg("mover_chute_r", mover())


def plains():
    rnd = random.Random(41)
    c = C("2")
    for k, (base, ph) in enumerate(((3, 0.0), (11, 2.0), (19, 4.0))):
        for x in range(W_):
            y = base + int(round(1.6 * math.sin(2 * math.pi * x / 16 + ph)))
            c.p(x, y - 1, "1"); c.p(x, y, "1")
            for d in (1, 2, 3):
                c.p(x, y + d, "3" if d < 3 else "2")
    for x0, y0 in ((2, 8), (10, 16), (6, 22)):
        x, y = x0, y0
        for _ in range(5):
            c.p(x, y, "3")
            x += rnd.choice((1, 1, 0)); y += rnd.choice((0, 0, 1))
    c.speckle(rnd, ["w"], 6, only="1")
    return c
reg("plains", plains())


def six_day():
    rnd = random.Random(51)
    c = C("6")
    noise_fill(c, rnd, "6", ["5", "6"], 0.25)
    c.ell(5, 12, 4.5, 6.5, None, shade=("1", "2", "3"))
    c.p(3, 9, "w"); c.p(4, 8, "w")
    c.p(3, 12, "O"); c.p(3, 13, "O"); c.p(6, 12, "O"); c.p(6, 13, "O")
    # tentacles arching right
    for k, (dy, h) in enumerate(((0, 8), (3, 6), (6, 4))):
        for i in range(12):
            t = i / 11
            x = 8 + t * 7
            y = 12 + dy * 1.0 - math.sin(t * math.pi) * h + t * (7 - dy)
            c.p(x, y, "1" if i % 2 else "2"); c.p(x, y + 1, "3")
    c.rect(0, 23, 15, 23, "6")
    return c
reg("six_day_stilt", six_day())


# ------------------------------------------------------------------ plants
def noise_grass():
    rnd = random.Random(61)
    c = C()
    for x in (2, 4, 6, 8, 10, 12, 13):
        h = rnd.randrange(7, 14)
        d = rnd.choice((-1, 1))
        for k in range(h):
            xx = x + (d if k > h * 0.55 else 0) + (d if k > h * 0.85 else 0)
            c.p(xx, 21 - k, "1" if k % 3 == 0 else ("2" if k % 3 == 1 else "3"))
        c.p(x + d + (d if h > 9 else 0), 21 - h, "4")
    c.rect(2, 21, 13, 21, "3")
    return c
reg("noise_grass", noise_grass(), "tall")


def reef_organic():
    c = C()
    for y in range(11, 21):  # vase column
        w = 2 + (y - 11) * 0.35 if y < 15 else 3.5 - (y - 15) * 0.1
        for x in range(16):
            dx = x - 7.5
            if abs(dx) <= w:
                c.p(x, y, "1" if dx < -w * 0.3 else ("3" if dx > w * 0.4 else "2"))
    c.rect(4, 20, 11, 20, "3")
    c.rect(5, 11, 10, 11, "4"); c.rect(5, 12, 10, 12, "3")
    for i, (dx, dy) in enumerate(((-6, -2), (-4, -5), (-2, -7), (2, -7), (4, -5), (6, -2))):
        x0, y0 = 7.5 + dx / 3, 11
        c.line(x0, y0, 7.5 + dx, 11 + dy - 2 + 2, "4")
        c.p(7.5 + dx, 11 + dy - 2, "5")
        c.p(7.5 + dx, 11 + dy - 3, "4")
    c.rect(7, 13, 8, 14, "6")
    c.p(6, 17, "3"); c.p(9, 16, "3")
    return c
reg("reef_organic_even", reef_organic(), "tall")


def ring_moss():
    rnd = random.Random(71)
    c = C()
    pts = [(7.5 + 6.2 * math.cos(a / 12 * 6.283), 12.5 + 7 * math.sin(a / 12 * 6.283)) for a in range(12)]
    pts.sort(key=lambda q: q[1])
    for x, y in pts:
        c.p(x, y, "n"); c.p(x + 1, y, "N")
        c.p(x - 1, y, "t") if rnd.random() < .5 else None
    for _ in range(26):
        a = rnd.random() * 6.283
        r = 0.9 + rnd.random() * 0.3
        x, y = 7.5 + 6 * r * math.cos(a), 12.5 + 6.7 * r * math.sin(a)
        c.p(x, y, rnd.choice("gGgh"))
        c.p(x + 1, y, rnd.choice("gGh"))
    for x, y in ((6, 11), (9, 13), (7, 14)):
        c.p(x, y, "w")
    return c
reg("ring_moss", ring_moss())


def sponge_tube():
    c = C()
    for cx, top, w in ((4, 8, 2), (9, 4, 3), (13, 10, 1.5)):
        for y in range(top, 21):
            for x in range(16):
                dx = x - cx
                ww = w + (y - top) * 0.07
                if abs(dx) <= ww:
                    c.p(x, y, "1" if dx < -ww * 0.3 else ("3" if dx > ww * 0.5 else "2"))
        c.rect(int(cx - w), top, int(cx + w), top, "1")
        c.rect(int(cx - w) + 1, top + 1, int(cx + w) - 1, top + 1, "5")
        c.p(cx, top + 1, "6")
        for k in range(top + 3, 20, 3):
            c.p(cx - 1 + (k % 2), k, "4"); c.p(cx + 1, k + 1, "3")
    c.rect(1, 21, 14, 21, "3")
    return c
reg("sponge_tube", sponge_tube(), "tall")


def sunslag():
    c = C()
    c.rect(7, 12, 8, 21, "L")
    c.rect(7, 12, 7, 21, "l")
    c.rect(5, 21, 10, 21, "R")
    c.p(8, 16, "R"); c.p(7, 18, "R"); c.p(8, 19, "n")
    c.ell(7.5, 8, 5.5, 5.5, None, shade=("1", "2", "3"))
    c.ell(7.5, 8.5, 3.2, 3.2, "4")
    c.ell(7.5, 8.5, 1.8, 1.8, "w")
    c.p(4, 5, "w"); c.p(5, 4, "w")
    for dx in (-5, 5):  # feelers of the polyp
        c.line(7.5 + dx * .6, 14, 7.5 + dx * 1.3, 11, "5")
        c.p(7.5 + dx * 1.3, 10, "4")
    return c
reg("sunslag_bulb_odd", sunslag(), "tall")


def flowers():
    rnd = random.Random(81)
    c = C()
    x, y = 0, 6
    while x < 16:
        c.p(x, y, "3")
        x += 1
        y += rnd.choice((-1, 0, 1, 1))
        y = max(2, min(20, y))
    x, y = 8, 0
    while y < 24:
        c.p(x, y, "3")
        y += 1
        x += rnd.choice((-1, 0, 0, 1))
        x = max(1, min(14, x))
    cols = "mcyrMB"
    for i, (px, py) in enumerate(((3, 4), (10, 4), (5, 10), (12, 12), (3, 17), (9, 18), (13, 21), (7, 8), (1, 12))):
        k = cols[i % 6]
        c.p(px, py, "w")
        for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            c.p(px + dx, py + dy, k)
        c.p(px, py + 2, "g")
    return c
reg("tile_flowers", flowers())


def swamp():
    rnd = random.Random(91)
    c = C()
    for cx, cy, rx, ry in ((5, 7, 5, 3), (11, 16, 4.5, 3.5), (4, 19, 3, 2)):
        c.ell(cx, cy, rx + .8, ry + .8, "h")
        c.ell(cx, cy, rx, ry, "d")
        c.ell(cx - 1, cy - 1, rx - 2, ry - 1.5, "b")
        c.p(cx + 1, cy, "M"); c.p(cx + 2, cy, "w"); c.p(cx - 2, cy + 1, "G"); c.p(cx - 1, cy + 1, "g")
    for x, y in ((12, 6), (1, 14), (8, 12), (14, 11)):
        for k in range(5):
            c.p(x + (k > 2), y - k, "g" if k % 2 else "G")
    return c
reg("tile_swamp", swamp())


def sunflower():
    c = C()
    c.rect(7, 12, 8, 21, "g"); c.rect(8, 12, 8, 21, "h")
    for x, y, d in ((5, 16, -1), (10, 18, 1)):
        c.rect(x - 1 if d < 0 else x, y, x + (1 if d > 0 else 0) + 0, y + 1, "G")
        c.p(x + d, y - 1, "G"); c.p(x + 2 * d, y - 2, "g")
    for a in range(12):
        ang = a / 12 * 6.283
        x, y = 7.5 + 6 * math.cos(ang), 7 + 6 * math.sin(ang)
        c.p(x, y, "1" if a % 2 else "2")
        c.p(7.5 + 4.8 * math.cos(ang), 7 + 4.8 * math.sin(ang), "1" if a % 2 else "2")
    c.ell(7.5, 7, 4, 4, "2")
    for a in range(12):
        ang = a / 12 * 6.283
        c.p(7.5 + 5.2 * math.cos(ang), 7 + 5.2 * math.sin(ang), "1")
    c.ell(7.5, 7, 3, 3, "N")
    c.ell(7.5, 7, 1.8, 1.8, "n")
    for x, y in ((6, 6), (8, 8), (7, 7), (9, 6), (6, 8)):
        c.p(x, y, "t" if (x + y) % 2 else "N")
    c.rect(5, 21, 10, 21, "x")
    return c
reg("tree_circle", sunflower(), "tall")


def wheat():
    rnd = random.Random(101)
    c = C()
    for x, h in ((3, 11), (6, 15), (9, 13), (12, 10)):
        for k in range(h):
            c.p(x + (k > h * .7), 21 - k, "2" if k % 2 else "1")
        tx, ty = x + 1, 21 - h
        c.p(tx, ty, "4"); c.p(tx - 1, ty + 1, "5"); c.p(tx + 1, ty + 1, "5"); c.p(tx, ty - 1, "4")
        c.p(tx - 1, ty, "6"); c.p(tx + 1, ty, "6")
    c.p(5, 18, "1"); c.p(4, 17, "1"); c.p(11, 17, "2"); c.p(12, 16, "2")
    c.rect(2, 21, 13, 21, "3")
    return c
reg("wheat", wheat(), "tall")


def rainbow():
    rnd = random.Random(111)
    c = C("e")
    c.speckle(rnd, ["E"], 30)
    # soup river
    x = 0
    for y in range(24):
        xx = 7 + 3.5 * math.sin(y / 4.0)
        c.p(xx - 1, y, "3"); c.p(xx, y, "2"); c.p(xx + 1, y, "1"); c.p(xx + 2, y, "3")
        if y % 5 == 0:
            c.p(xx + 1, y, "y")
    cols = [("r", "R"), ("y", "t"), ("c", "B"), ("m", "M"), ("g", "G"), ("B", "b")]
    spots = [(3, 5), (12, 4), (4, 11), (12, 11), (3, 18), (12, 18), (8, 2), (8, 21)]
    for i, (cx, cy) in enumerate(spots):
        a, b = cols[i % 6]
        c.ell(cx, cy, 2.6, 1.8, None, shade=(b if False else "w", a, b))
        c.rect(cx - 1, cy + 2, cx, cy + 2, "t")
        c.p(cx, cy - 1, "w"); c.p(cx + 1, cy, "w")
    return c
reg("worldmap_rainbowwood_center", rainbow())


def ueater():
    c = C()
    c.rect(0, 0, 15, 23, "3")
    c.rect(0, 0, 15, 4, "2")
    c.rect(0, 5, 15, 5, "O")
    c.rect(0, 22, 15, 23, "3")
    c.rect(0, 0, 0, 23, "1"); c.rect(15, 0, 15, 23, "3")
    # emerging relief face
    c.ell(7.5, 13, 5.5, 8, None, shade=("1", "2", "3"))
    c.rect(2, 7, 13, 7, "4")            # hair
    c.rect(3, 8, 12, 8, "5")
    c.p(2, 9, "4"); c.p(13, 9, "5"); c.p(2, 12, "4"); c.p(13, 13, "5")
    c.rect(4, 10, 11, 10, "3")          # brow
    c.rect(4, 11, 6, 12, "O"); c.rect(9, 11, 11, 12, "O")
    c.p(5, 11, "y"); c.p(10, 11, "y")
    c.rect(7, 12, 8, 15, "1"); c.rect(8, 15, 9, 15, "3")
    c.rect(5, 17, 10, 17, "O"); c.rect(6, 18, 9, 18, "3")
    c.p(2, 7, "4"); c.p(3, 20, "4"); c.p(12, 21, "4"); c.p(1, 15, "5")
    return c
reg("ueater", ueater())


# ------------------------------------------------------------------ rivers and lakes
def land(c, rnd):
    for y in range(H_):
        for x in range(W_):
            c.g[y][x] = "g" if rnd.random() > .2 else rnd.choice("hGg")


def water_tex(c, rnd, mask, deep="3", mid="2", lite="1", foam="4"):
    for y in range(H_):
        for x in range(W_):
            if mask(x, y):
                c.g[y][x] = mid
    for y in range(H_):
        for x in range(W_):
            if c.g[y][x] == mid:
                if (x * 3 + y * 5) % 11 == 0 and rnd.random() < .8:
                    c.g[y][x] = lite
                    if mask(x + 1, y):
                        if x + 1 < W_:
                            c.g[y][x + 1] = lite
    for y in range(H_):
        for x in range(W_):
            if mask(x, y):
                edge = any(not mask(x + dx, y + dy) and 0 <= x + dx < W_ and 0 <= y + dy < H_
                           for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)))
                if edge:
                    c.g[y][x] = foam
                elif (x + y * 2) % 13 == 3:
                    c.g[y][x] = deep


def river(dirs, name, seed):
    rnd = random.Random(seed)
    c = C()
    land(c, rnd)
    for x, y in ((2, 3), (13, 20), (3, 21), (12, 2)):
        c.p(x, y, "O" if False else "h"); c.p(x, y - 1, "G")
    w = 1.8
    def m(x, y):
        if not (0 <= x < W_ and 0 <= y < H_):
            return True
        cx, cy = 7.5, 11.5
        wob = math.sin(y / 3.0) * 0.6
        wobh = math.sin(x / 2.5) * 0.6
        if math.hypot(x - cx, (y - cy) * .9) <= 2.9:
            return True
        if "n" in dirs and y <= cy and abs(x - cx - wob) <= w + .6:
            return True
        if "s" in dirs and y >= cy and abs(x - cx - wob) <= w + .6:
            return True
        if "w" in dirs and x <= cx and abs(y - cy - wobh) <= w + .6:
            return True
        if "e" in dirs and x >= cx and abs(y - cy - wobh) <= w + .6:
            return True
        return False
    water_tex(c, rnd, m)
    # sandy bank
    for y in range(H_):
        for x in range(W_):
            if c.g[y][x] in "gGh" and any(m(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                c.g[y][x] = "t"
    return c
for nm, d, sd in (("10b", "nwe", 1), ("12b", "n", 2), ("14b", "we", 3), ("2b", "swe", 4), ("5b", "nse", 5), ("8b", "ns", 6)):
    reg("river_worldmap_" + nm, river(d, nm, sd))


def lake(name, kind):
    rnd = random.Random(sum(ord(ch) * (i + 3) for i, ch in enumerate(name)) + len(kind))
    c = C()
    sides = {"n": 0, "s": 0, "w": 0, "e": 0}
    ph = [rnd.random() * 6 for _ in range(4)]
    def island(x, y):
        if sides["n"] and y < sides["n"] - 1 + 1.6 * math.sin(x / 2.2 + ph[0]):
            return True
        if sides["s"] and (23 - y) < sides["s"] + 1.6 * math.sin(x / 2.2 + ph[1]):
            return True
        if sides["w"] and x < sides["w"] * .6 + 1.3 * math.sin(y / 2.5 + ph[2]):
            return True
        if sides["e"] and (15 - x) < sides["e"] * .6 + 1.3 * math.sin(y / 2.5 + ph[3]):
            return True
        return False
    for y in range(H_):
        for x in range(W_):
            if kind == "svy":
                c.g[y][x] = "g" if rnd.random() > .2 else rnd.choice("hGg")
            elif kind == "hinnom":
                c.g[y][x] = "t" if rnd.random() > .25 else "E"
            else:
                c.g[y][x] = "L" if rnd.random() > .3 else "e"
    water_tex(c, rnd, lambda x, y: not island(x, y) if (0 <= x < W_ and 0 <= y < H_) else True)
    if False:
        for y in range(H_):
            for x in range(W_):
                if c.g[y][x] in "gGh" and any(not island(x + dx, y + dy) for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1))):
                    c.g[y][x] = "t"
    elif kind == "hinnom":
        for _ in range(26):  # algal bloom
            x, y = rnd.randrange(16), rnd.randrange(24)
            if not island(x, y):
                c.p(x, y, rnd.choice("45")); c.p(x + 1, y, "5")
        for _ in range(3):  # white esh fish
            x, y = rnd.randrange(1, 15), rnd.randrange(1, 23)
            if not island(x, y):
                c.p(x, y, "w"); c.p(x - 1, y, "l")
        for _ in range(2):  # coral fingers
            x, y = rnd.randrange(2, 14), rnd.randrange(8, 22)
            if not island(x, y):
                for k in range(3):
                    c.p(x, y - k, "M" if k else "m")
                c.p(x - 1, y - 2, "M"); c.p(x + 1, y - 3, "M")
    elif kind == "pal":  # palladium reef: polyps and trellis
        for _ in range(5):
            x, y = rnd.randrange(2, 14), rnd.randrange(3, 22)
            if not island(x, y):
                c.p(x, y, "5"); c.p(x - 1, y - 1, "4"); c.p(x + 1, y - 1, "4"); c.p(x, y + 1, "6")
        if rnd.random() < .7:
            y = rnd.randrange(6, 18)
            for x in range(16):
                if not island(x, y):
                    c.p(x, y, "l" if x % 2 else "L")
        for x in range(0, 16, 5):
            for y in range(24):
                if not island(x, y) and rnd.random() < .12:
                    c.p(x, y, "4")
    return c

for k in ("2i", "3g", "4d", "4i", "5i", "6i", "7d", "8c"):
    reg("svylake_worldmap_" + k, lake(k, "svy"))
for k in ("1i", "2g", "3c", "3g", "4e", "5c", "6g", "7a", "7e", "7j", "8b", "8f", "9e", "blank"):
    reg("terrainlakehinnom_" + k, lake(k, "hinnom"))
for k in ("2h", "3j", "3n", "4k", "4q", "5k", "6j"):
    reg("terrainpalladiumreef_" + k, lake(k, "pal"))


def ruins():
    rnd = random.Random(121)
    c = C()
    # broken wall stubs (white stone, fg ramp) with green overgrowth (detail)
    for x0, x1, top in ((1, 5, 8), (7, 9, 11), (10, 14, 6)):
        for y in range(top, 18):
            for x in range(x0, x1 + 1):
                jag = (x * 7 + y) % 4 == 0 and y == top
                if jag:
                    continue
                ch = "1" if y == top or x == x0 else ("3" if x == x1 or y == 17 else "2")
                if (x + y) % 5 == 0 and ch == "2":
                    ch = "3"
                c.p(x, y, ch)
    for x in range(1, 15):
        c.p(x, 18, "x") if c.get(x, 18) == "." else None
    c.rect(2, 19, 13, 19, "x")
    for x, y in ((3, 19), (6, 18), (9, 19), (12, 18), (5, 20), (10, 20)):
        c.p(x, y, "3"); c.p(x + 1, y, "2")  # rubble
    for _ in range(18):
        x, y = rnd.randrange(1, 15), rnd.randrange(6, 19)
        if c.get(x, y) in "123":
            c.p(x, y, rnd.choice("gGh"))
    c.p(7, 14, "G"); c.p(8, 15, "g")
    return c
reg("ruins", ruins())

SPRITES = SPR
KINDS = KIND


# Reviewer (Opus) redraw: world-map mountains, two solid peaks that read at any colour.
def _mountains():
    g = [["2"] * 16 for _ in range(24)]
    for x, y in ((3, 2), (11, 1), (1, 6), (14, 5)):        # rocky specks in the background
        g[y][x] = "3"

    def peak(apex_x, apex_y, half, base_y):
        for y in range(apex_y, base_y + 1):
            w = round((y - apex_y) * half / (base_y - apex_y))
            for x in range(apex_x - w, apex_x + w + 1):
                if 0 <= x < 16:
                    g[y][x] = "1" if x < apex_x else "3"
            if 0 <= apex_x - w < 16:
                g[y][apex_x - w] = "O"                      # left outline
            if 0 <= apex_x + w < 16:
                g[y][apex_x + w] = "O"                      # right outline
            g[y][apex_x] = "O" if y > apex_y + 3 else g[y][apex_x]   # ridge crease
        for y in range(apex_y, min(apex_y + 3, base_y)):    # snow cap
            w = round((y - apex_y) * half / (base_y - apex_y))
            for x in range(apex_x - w, apex_x + w + 1):
                if 0 <= x < 16:
                    g[y][x] = "w"

    peak(11, 8, 6, 20)      # small peak behind
    peak(6, 3, 7, 20)       # big peak in front
    for y in (21, 22, 23):  # rocky base
        for x in range(16):
            g[y][x] = "3" if (x + y) % 3 else "O"
    return ["".join(r) for r in g]


SPRITES["mountains"] = _mountains()
