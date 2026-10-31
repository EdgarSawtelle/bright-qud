"""Palladium Reef struts: "cylinders joined at right angles ... a vast arcological lattice". Thick silver pipes that join
their neighbours (16 N/E/S/W variants, brightqudwall/strut-NESW), and the same pipes colonised by coral (strutcoral):
"bow polyps colonize the cylindrical topology". Pipe in roles 1-3, coral in roles 4-6, drawn with their own ink edge."""
import random

L, R, T, B = 4, 11, 8, 15


def pipe(n, e, s, w, coral, seed):
    rnd = random.Random(seed * 131 + n * 8 + e * 4 + s * 2 + w + (1000 if coral else 0))
    g = [["."] * 16 for _ in range(24)]

    def vert(y0, y1):
        for y in range(y0, y1):
            for x in range(L, R + 1):
                g[y][x] = {L: "O", L + 1: "1", L + 2: "1", L + 3: "2", L + 4: "2", L + 5: "2", L + 6: "3", R: "O"}[x]

    def horz(x0, x1):
        for x in range(x0, x1):
            for y in range(T, B + 1):
                g[y][x] = {T: "O", T + 1: "1", T + 2: "1", T + 3: "2", T + 4: "2", T + 5: "2", T + 6: "3", B: "O"}[y]

    joins = n + e + s + w
    if n: vert(0, T + 1 if joins > 1 else 18)
    if s: vert(B if joins > 1 else 6, 24)
    if w: horz(0, L + 1 if joins > 1 else 13)
    if e: horz(R if joins > 1 else 3, 16)
    if joins == 0:                                         # a stump on its foot
        vert(3, 20)
        for x in range(2, 14):
            g[20][x] = "3"
            g[21][x] = "O"
        for x in range(3, 13):
            g[2][x] = "O"
    if joins == 1:                                         # a capped end
        rows = [(17 if n else 5, range(L - 1, R + 2))] if n or s else []
        for y, xs in rows:
            for x in xs:
                g[y][x] = "O"
        if e or w:
            x = 13 if w else 2
            for y in range(T - 1, B + 2):
                g[y][x] = "O"
    if joins >= 2:                                         # a riveted joint where pipes meet
        for y in range(T - 1, B + 2):
            for x in range(L - 1, R + 2):
                edge = y in (T - 1, B + 1) or x in (L - 1, R + 1)
                g[y][x] = "O" if edge else ("1" if x + y < L + T + 5 else ("3" if x + y > L + T + 11 else "2"))
        for x, y in ((L + 1, T + 1), (R - 1, T + 1), (L + 1, B - 1), (R - 1, B - 1)):
            g[y][x] = "O"
        g[T + 3][L + 3] = "w"
    for _ in range(7):                                     # casing freckles
        y, x = rnd.randrange(24), rnd.randrange(16)
        if g[y][x] in ("1", "2"):
            g[y][x] = "3"
    if coral:
        solid = [(x, y) for y in range(24) for x in range(16) if g[y][x] != "."]
        for _ in range(11):                                # polyp crust all over the metal
            x, y = rnd.choice(solid)
            for dx, dy in ((0, 0), (1, 0), (-1, 0), (0, 1), (0, -1), (1, 1)):
                px, py = x + dx, y + dy
                if 0 <= px < 16 and 0 <= py < 24 and g[py][px] != ".":
                    g[py][px] = rnd.choice("4455")
            g[y][x] = "6"
        for _ in range(7):                                 # coral fingers reaching off the pipe
            x, y = rnd.choice(solid)
            dx, dy = rnd.choice(((1, -1), (-1, -1), (1, 0), (-1, 0)))
            for i in range(rnd.randrange(3, 6)):
                px, py = x + dx * i, y + dy * i
                if 0 <= px < 16 and 0 <= py < 24:
                    g[py][px] = "5" if i else "4"
                    if g[py][px] and 0 <= px + 1 < 16 and g[py][px + 1] == ".":
                        g[py][px + 1] = "O"
    return ["".join(r) for r in g]


def variants():
    """(tile key, rows) for both sets."""
    out = []
    for coral, name in ((False, "strut"), (True, "strutcoral")):
        for i in range(16):
            n, e, s, w = (i >> 3) & 1, (i >> 2) & 1, (i >> 1) & 1, i & 1
            out.append((f"brightqudwall/{name}-{n}{e}{s}{w}", pipe(n, e, s, w, coral, i)))
    return out
