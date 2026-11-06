"""Bethesda Susa's "angleless architecture": pale marble with no hard corner anywhere. Rounded ends, a soft arcade of pointed arches
as in the fan art's monolith, lilac shadow in place of black ink, a little of the rust ground's light on the foot."""
import random

from PIL import Image

def hexes(*names):
    return tuple(tuple(int(h[i:i + 2], 16) for i in (0, 2, 4)) for h in names)


# top, lit top, face, soft, shade, deep, foot light, ribbon. Below ground the game keeps its marble cool, and it gets colder every level.
PALETTES = {"surface": hexes("f2eade", "faf5ec", "e6dcd0", "d6cac8", "bcaebc", "988aa6", "e6c0a0", "dcd4d4"),
            "ward": hexes("dfe6e8", "eef3f3", "cfd9dd", "bac8d0", "96a8b6", "66788e", "aecbd0", "8fb8bc"),
            "ice": hexes("e4f2f6", "fafdfe", "cde4ec", "b2d2e0", "8ab4cc", "5886a8", "c2ecf4", "a4d2e2")}
W, H, EAVE = 16, 24, 8


def arch_half(y):
    """Half-width of the tall pointed arch at height y on the front face."""
    t = y - (EAVE + 1)
    return (1, 1, 2, 2, 3, 3, 4)[t] if t < 7 else 4


def wall(mask, palette="surface"):
    """mask is NESW, as the mod's wall sets: 1 where the next cell is the same wall."""
    TOP, TOP_LIT, FACE, SOFT, SHADE, DEEP, GLOW, VEIN = PALETTES[palette]
    n, e, s, w = (c == "1" for c in mask)
    im = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    p = im.load()
    bottom = H if s else H - 1
    for y in range(bottom):
        for x in range(W):
            front = not s and y >= EAVE
            c = FACE if front else TOP
            if not front and (y < 2 or x < 2) and not n and not w:
                c = TOP_LIT
            p[x, y] = c + (255,)
    r = random.Random(mask)
    for _ in range(5):                                       # "ribbons of impurity" in the marble, all soft curves
        x, y = r.randrange(1, 12), r.randrange(1, bottom - 2)
        for i in range(r.randrange(3, 6)):
            if x + i < W and y + (i * i) // 7 < bottom:
                p[x + i, y + (i * i) // 7] = VEIN + (255,)
    if not s:
        for x in range(W):
            p[x, EAVE] = SOFT + (255,)                       # the lip, soft
            p[x, EAVE - 1] = TOP_LIT + (255,)
            p[x, H - 2] = GLOW + (255,)                      # warm light from the ground
            p[x, H - 3] = SOFT + (255,)
        for y in range(EAVE + 1, H - 3):                     # one tall arch per cell, so a run reads as an arcade
            half = arch_half(y)
            for x in range(8 - half, 8 + half):
                p[x, y] = (DEEP if x < 8 else SHADE) + (255,)
            if y > H - 8:                                    # warm light reaches into the foot of the arch
                for x in range(8 - half, 8 + half):
                    p[x, y] = (GLOW if x >= 8 else SHADE) + (255,)
            p[max(8 - half - 1, 0), y] = SOFT + (255,)
            p[min(8 + half, W - 1), y] = TOP_LIT + (255,)
    if not e:                                                # the side falling away, in lilac
        for y in range(bottom):
            p[W - 1, y] = SHADE + (255,)
            p[W - 2, y] = SOFT + (255,)
    # no corners: every free end is rounded back to the ground
    def cut(xs, ys):
        for x, y in zip(xs, ys):
            p[x, y] = (0, 0, 0, 0)
    far, low = W - 1, bottom - 1
    if not n and not w:
        cut((0, 0, 0, 1, 2), (0, 1, 2, 0, 0))
    if not n and not e:
        cut((far, far, far, far - 1, far - 2), (0, 1, 2, 0, 0))
    if not s and not w:
        cut((0, 0, 0, 1, 2), (low, low - 1, low - 2, low, low))
    if not s and not e:
        cut((far, far, far, far - 1, far - 2), (low, low - 1, low - 2, low, low))
    return im
