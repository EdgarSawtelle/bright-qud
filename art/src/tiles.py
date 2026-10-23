"""Bright Qud tiles. Original art, 16x24, one character per pixel.

Letters are fixed palette colors (palette.py). Digits are recolored from the game's colors
(colors.py: 1-3 foreground light/mid/dark, 4-6 detail light/mid/dark). '.' is transparent and
'x' is a translucent ground shadow.

KIND (walkability tiers, see docs/STYLE_GUIDE.md):
    object  - creatures/items: outline + drop shadow (sprites keep a 1px empty margin)
    tall    - walk-through but blocks sight (trees): outline, no drop shadow
    terrain - floor-level (grass, crops, paths, water, walls): no outline, no shadow
"""
import random

E = "................"

SPRITES = {
    # Player pregen "Gunwing": winged gunslinger. Coat = foreground, wings = detail.
    "gunwing": [
        E, E, E, E,
        ".....NNNNNN.....",
        "....NNNnNNNN....",
        "...NNnnNNNNNN...",
        "...NNNNNNNNNN...",
        "...NrrrrrrrrN...",
        "...NssssssssN...",
        "...ssOOssOOss...",
        "...ssOwssOwss...",
        "....srssssrs....",
        ".4...SSSSSS...4.",
        ".45.22222222.54.",
        ".55s21222222s55.",
        ".56s22222222sLl.",
        "..6.22yy2222.L..",
        "....33333333....",
        ".....33..33.....",
        "....xNNxxNNx....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E,
    ],
    # Generic adventurer (kept for Phase 4 player-look options). Tunic = foreground.
    "adventurer": [
        E, E, E, E,
        ".....NNNNNN.....",
        "....NNNnNNNN....",
        "...NNnnNNNNNN...",
        "...NNNNNNNNNN...",
        "...NNNNNNNNNN...",
        "...NssssssssN...",
        "...ssOOssOOss...",
        "...ssOwssOwss...",
        "....srssssrs....",
        ".....SSSSSS..l..",
        "....rrrrrrrr.l..",
        "...s22rr2222sl..",
        "...s21222222yyy.",
        "....22nynn22s...",
        "....33333333....",
        ".....33..33.....",
        "....xNNxxNNx....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E,
    ],
    # Shirt = foreground, trousers = detail.
    "farmer": [
        E, E, E,
        "......tyyt......",
        ".....tyyyyt.....",
        "...tttyyyyttt...",
        "..tttttttttttt..",
        "..tttttttttttt..",
        "...NNNNNNNNNN...",
        "...NssssssssN...",
        "...ssOOssOOss...",
        "...ssOwssOwss...",
        "....srssssrs....",
        ".....SSSSSS..n..",
        "....22222222.n..",
        "...s21222222sn..",
        "...s22222222sn..",
        "....55nnnn55.n..",
        "....55555555.n..",
        ".....55..55..n..",
        "....xNNxxNNxlll.",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E,
    ],
    # Fur = foreground, ear/vest markings = detail.
    "snapjaw": [
        E, E,
        "...2........2...",
        "...22......22...",
        "...252....252...",
        "...2222222222...",
        "..222222222222..",
        "..212222222212..",
        "..22rO2222rO22..",
        "..2222tttt2222..",
        "...22ttttttt22..",
        "....ttOttOtt....",
        "....wOwOwOwO....",
        ".....tttttt.....",
        "...2255555522...",
        "..t2252222522t..",
        "..t.22222222.t..",
        "....22222222....",
        ".....33..33.....",
        ".....33..33.....",
        "....xttxxttx....",
        "...xxxxxxxxxx...",
        "....xxxxxxxx....",
        E,
    ],
    # Body = foreground, fins/glow = detail.
    "glowfish": [
        E, E, E, E, E, E, E,
        "......5.........",
        ".....555........",
        "....222222...5..",
        "...2111222.55...",
        "..21wO1222225...",
        "..21112222222...",
        "..2222222222....",
        "...33222223.55..",
        "....333333...5..",
        ".....5..5.......",
        E, E, E, E, E, E, E,
    ],
    # Low leafy crop, walkable (kept low and curly so rows don't read as fences). Stalks = foreground (game: TileColor w), leaves/wafers = detail
    # (game: g when ripe, K when unripe), so ripeness shows like in the original.
    "watervine": [
        E, E, E, E, E, E, E, E, E, E, E, E,
        "................",
        "...4.......4....",
        "..444..4..444...",
        "...1..444..1..4.",
        ".4.1...1.4.1.444",
        "444.1.41.44.1.1.",
        ".4..1.1...4.1.1.",
        "....21.....21.2.",
        "....2......2....",
        E, E, E,
    ],
    # Canopy = foreground, thorns = detail. Walk-through, blocks sight.
    "tree": [
        E, E,
        "......1111......",
        "....11111111....",
        "...1112111111...",
        "..111222111411..",
        "..112222211111..",
        ".11122222221111.",
        ".14112223222111.",
        ".11222333222141.",
        ".12222333222241.",
        "..222333333222..",
        "..223333333322..",
        "...3333NN3333...",
        "....333NN333....",
        "......nNNn......",
        "......nNNn......",
        "......nNNn......",
        "......nNNn......",
        "......nNNn......",
        ".....nnNNnn.....",
        "..xxnnNxxNnnxx..",
        "...xxxxxxxxxx...",
        E,
    ],
    # Wood = foreground, metal bands = detail.
    "chest": [
        E, E, E, E, E, E, E, E, E, E, E, E,
        "...3333333333...",
        "..322222222223..",
        "..311111111123..",
        "..322222222223..",
        "..555555555555..",
        "..32222yw22223..",
        "..32222yy22223..",
        "..322222222223..",
        "..322222222223..",
        "..333333333333..",
        E, E,
    ],
    # Flame = foreground: the game animates it by cycling the color (&R, &W, &r).
    "torch_lit": [
        E, E, E, E, E, E,
        ".......1........",
        "......111.......",
        "......121.......",
        ".....12321......",
        "......232.......",
        ".....LLLLL......",
        "......LlL.......",
        ".......n........",
        ".......n........",
        ".......n........",
        ".......n........",
        ".......n........",
        ".......n........",
        ".......n........",
        "......nNn.......",
        ".....NNNNN......",
        E, E,
    ],
}
SPRITES["torch"] = [E] * 11 + SPRITES["torch_lit"][11:]

KIND = {name: "object" for name in SPRITES}
KIND.update({"watervine": "terrain", "tree": "tall"})


def _grid(fill):
    return [[fill] * 16 for _ in range(24)]


def _rows(g):
    return ["".join(r) for r in g]


def shifted(rows, dx):
    """Horizontal wrap-around shift: cheap variety for tile families (vine1..3)."""
    return [r[-dx:] + r[:-dx] if dx else r for r in rows]


def grass(seed=1):
    """Ground grass tuft, walkable: foreground ramp, no outline."""
    rnd = random.Random(seed)
    g = _grid(".")
    for _ in range(rnd.choice((1, 2))):
        cx, base = rnd.randrange(3, 12), rnd.randrange(15, 21)
        for dx in (-2, 0, 2):
            h = rnd.randrange(2, 5)
            for k in range(h):
                lean = (1 if dx > 0 else -1) if (dx and k == h - 1) else 0
                x = cx + dx + lean
                if 0 <= x < 16:
                    g[base - k][x] = "1" if k == h - 1 else ("2" if k else "3")
    return _rows(g)


def floor(seed=1, density=0.16):
    """Dirt path: dense specks over the cell background, foreground ramp (biome colored)."""
    rnd = random.Random(seed)
    g = _grid(".")
    for y in range(24):
        for x in range(16):
            r = rnd.random()
            if r < density * 0.55:
                g[y][x] = "3"
            elif r < density:
                g[y][x] = "e"
    for _ in range(2):
        x, y = rnd.randrange(1, 14), rnd.randrange(1, 22)
        g[y][x] = g[y][x + 1] = "3"
    return _rows(g)


def ground(seed=1):
    """Unpathed ground painted by the game (tile-dirt1): sparse dark specks."""
    rnd = random.Random(seed)
    g = _grid(".")
    for y in range(24):
        for x in range(16):
            if rnd.random() < 0.035:
                g[y][x] = "3" if rnd.random() < 0.4 else "e"
    return _rows(g)


def _bits(mask):
    """8-char mask from the game, in order N, NE, E, SE, S, SW, W, NW (1 = same kind there)."""
    return dict(zip(("n", "ne", "e", "se", "s", "sw", "w", "nw"), (c == "1" for c in mask)))


def water(mask="11111111", seed=1, deep=True):
    """Painted liquid: foreground ramp; open sides get a dark rim and rounded outer corners."""
    rnd = random.Random(seed)
    m = _bits(mask)
    g = _grid("2" if deep else "1")
    for row in range(2, 24, 6):
        phase = rnd.randrange(16)
        for x in range(16):
            y = row + (1 if ((x + phase) // 4) % 2 else 0)
            g[y][x] = "3"
            if ((x + phase) % 8) in (1, 2, 3):
                g[y - 1][x] = "1" if deep else "2"
    if not m["n"]:
        g[0] = list("." * 16)
        g[1] = list("3" * 16)
    if not m["s"]:
        g[23] = list("." * 16)
        g[22] = list("3" * 16)
    for y in range(24):
        if not m["w"]:
            g[y][0], g[y][1] = ".", "3"
        if not m["e"]:
            g[y][15], g[y][14] = ".", "3"
    corners = (("n", "w", (0, 1, 2), (0, 1, 2)), ("n", "e", (0, 1, 2), (15, 14, 13)),
               ("s", "w", (23, 22, 21), (0, 1, 2)), ("s", "e", (23, 22, 21), (15, 14, 13)))
    for vert, horiz, ys, xs in corners:
        if not m[vert] and not m[horiz]:  # rounded outer corner
            for y, x in ((ys[0], xs[1]), (ys[1], xs[0]), (ys[0], xs[2]), (ys[2], xs[0]), (ys[1], xs[1])):
                g[y][x] = "."
            g[ys[1]][xs[2]] = g[ys[2]][xs[1]] = "3"
    return _rows(g)


def wall(mask="00000000", seed=1):
    """Brinestalk wall, 3/4 view. Front face only when nothing of the same wall is to the south."""
    rnd = random.Random(seed)
    m = _bits(mask)
    face = not m["s"]
    g = _grid("n")
    top = 9 if face else 24
    for y in range(top):
        for x in range(16):
            if (x + y) % 4 == 0:
                g[y][x] = "t"
            elif (x - y) % 4 == 0:
                g[y][x] = "N"
            elif rnd.random() < 0.04:
                g[y][x] = "t"
    if not m["n"]:
        g[0] = list("t" * 16)  # lit top edge
    if face:
        g[top - 1] = list("N" * 16)  # ledge shadow
        for y in range(top, 24):
            for x in range(16):
                col = x % 4
                g[y][x] = "t" if col == 1 else ("n" if col in (0, 2) else "N")
            if y in (14, 20):
                g[y] = list("R" * 16)  # binding cords
        g[23] = list("O" * 16)  # dark base: "this blocks you"
    for y in range(24):
        if not m["w"]:
            g[y][0] = "N"
        if not m["e"]:
            g[y][15] = "O"
    return _rows(g)


def door(seed=1):
    """Hut door set into a brinestalk wall (mockups only for now)."""
    g = [list(r) for r in wall("10000000", seed)]
    for y in range(10, 23):
        for x in range(3, 13):
            g[y][x] = "N" if x in (3, 12) or y == 10 else ("n" if x % 3 else "N")
    g[16][10] = "y"
    return _rows(g)
