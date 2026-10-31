"""Yd Freehold's glass pipework: "glass was blown into a machine artery ... fluorescent green-yellow". Two parallel tubes seen
from the side, the floor showing between them. Each tube looks round across its width: dark at both edges, light down the
middle. They run along the pipe and bend at corners. Set ydtube2 adds gold collars, used on one cell in four.
Roles 1-3 glass, 4-5 gold. The runtime reduces a cell's neighbours with straight() below."""
import math
import random

V = ((2, 8), (9, 15))        # columns of the two tubes on a vertical run
H = ((3, 10), (14, 21))      # rows on a horizontal run


def profile(t):
    """Shade across a tube, t 0..1: round by light alone."""
    return "3" if t < 0.17 or t > 0.83 else ("2" if t < 0.36 or t > 0.64 else "1")


def across(p, bands):
    for a, b in bands:
        if a <= p < b:
            return profile((p - a + 0.5) / (b - a))
    return None


def straight(n, e, s, w, across_run, along_run):
    """A cell in a thick run has neighbours on three or four sides: keep the direction of the longer run, so the cells stay
    tubes and don't turn into junctions. across_run/along_run: length of the horizontal and vertical runs through it."""
    if n + e + s + w >= 3:
        return (0, 1, 0, 1) if across_run >= along_run else (1, 0, 1, 0)
    if n and s or e and w or n + e + s + w < 2:
        return n, e, s, w
    return n, e, s, w


def tube(n, e, s, w, collar, seed):
    rnd = random.Random(seed * 53 + (n * 8 + e * 4 + s * 2 + w))
    g = [["."] * 16 for _ in range(24)]
    corner = n + s == 1 and e + w == 1
    for y in range(24):
        for x in range(16):
            if corner:
                u = (15.5 - x if e else x + 0.5) / 16                    # distance from the corner the tubes bend round
                v = (23.5 - y if s else y + 0.5) / 24
                r = math.hypot(u, v)
                c = across(r, ((0.14, 0.44), (0.58, 0.88)))
            elif e or w:
                c = across(y, H)
                if not e and x > 12 or not w and x < 3:
                    c = None
            else:
                c = across(x, V)
                if not s and n and y > 17 or not n and s and y < 6:
                    c = None
            if c:
                g[y][x] = c
    if not corner:
        for _ in range(2):                                 # a bubble riding the glass
            y, x = rnd.randrange(24), rnd.randrange(16)
            if g[y][x] == "1":
                g[y][x] = "w"
    if collar and not corner:
        for i in (11, 12):
            for j in range(24 if e or w else 16):
                x, y = (i - 4, j) if e or w else (j, i)
                if g[y][x] != ".":
                    g[y][x] = "4" if i == 11 else "5"
    return ["".join(r) for r in g]


def pump():
    """Fusion pumping station: a squat glass housing with gold bands, where the tubes plug in."""
    g = [["."] * 16 for _ in range(24)]
    for y in range(2, 22):
        for x in range(1, 15):
            edge = y in (2, 21) or x in (1, 14)
            g[y][x] = "O" if edge else profile((x - 1.5) / 13)
    for y in (6, 7, 16, 17):
        for x in range(2, 14):
            g[y][x] = "4" if y in (6, 16) else "5"
    for y in range(9, 15):                                 # the fusion core behind glass
        for x in range(5, 11):
            g[y][x] = "w" if 6 <= x <= 9 and 10 <= y <= 13 else "1"
    return ["".join(r) for r in g]


def variants():
    out = []
    for i in range(16):
        out.append((f"brightqudwall/ydpump-{(i >> 3) & 1}{(i >> 2) & 1}{(i >> 1) & 1}{i & 1}", pump()))
    for collar, name in ((False, "ydtube"), (True, "ydtube2")):
        for i in range(16):
            n, e, s, w = (i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1
            out.append((f"brightqudwall/{name}-{n}{e}{s}{w}", tube(n, e, s, w, collar, i)))
    return out
