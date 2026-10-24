"""Joppa's "salt-spangled earth": textured ground tiles so the pale earth is never flat.

In Joppa (world terrain TerrainJoppa*) the runtime shows one of these on every bare ground cell, picked
per cell by a hash: pebbles, hairline cracks, dry grass tufts, small green sprouts and salt crust.
EARTH 13-15 carry one salt glint that slowly twinkles (frames in FRAMES).
Colours are fixed palette letters; the ground colour under them comes from the zone.
"""
import random

COUNT, ANIMATED = 16, (13, 14, 15)


def _put(g, x, y, ch):
    if 0 <= x < 16 and 0 <= y < 24:
        g[y][x] = ch


def _pebbles(rnd, g):
    cx, cy = rnd.randrange(2, 14), rnd.randrange(6, 22)
    for _ in range(rnd.randrange(2, 5)):
        x, y = cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2)
        _put(g, x, y, "l")
        _put(g, x + 1, y, "L")
        _put(g, x, y + 1, "E")                     # tiny shadow under each stone


def _crack(rnd, g):
    x, y = rnd.randrange(1, 12), rnd.randrange(4, 20)
    for _ in range(rnd.randrange(4, 8)):
        _put(g, x, y, "E")
        x += 1
        y += rnd.choice((-1, 0, 0, 1))
        if rnd.random() < 0.25:                    # a short branch
            _put(g, x, y + 1, "E")


def _tuft(rnd, g, green):
    x, y = rnd.randrange(2, 14), rnd.randrange(9, 22)
    light, dark = ("G", "g") if green else ("t", "n")
    for dx, h in ((-1, 2), (0, 3), (1, 2)):
        for i in range(h):
            _put(g, x + dx + (i == h - 1) * dx, y - i, light if i else dark)


def _salt(rnd, g):
    cx, cy = rnd.randrange(2, 14), rnd.randrange(4, 22)
    for _ in range(rnd.randrange(3, 7)):
        _put(g, cx + rnd.randint(-2, 2), cy + rnd.randint(-1, 1), rnd.choice("wlt"))


def _variant(i):
    rnd = random.Random("earth%d" % i)
    g = [["." for _ in range(16)] for _ in range(24)]
    for _ in range(rnd.randrange(2, 4)):           # soft lighter/darker patches: the ground undulates
        cx, cy, tone = rnd.randrange(16), rnd.randrange(24), rnd.choice("uuU")
        for _ in range(rnd.randrange(6, 14)):
            _put(g, cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2), tone)
    for _ in range(rnd.randrange(5, 10)):          # fine grain everywhere: never a flat tile
        _put(g, rnd.randrange(16), rnd.randrange(24), rnd.choice("EEEt"))
    picks = [_pebbles, _crack, _salt, lambda r, gg: _tuft(r, gg, False), lambda r, gg: _tuft(r, gg, True)]
    for f in rnd.sample(picks, rnd.choice((1, 1, 2, 2, 3))):
        f(rnd, g)
    return g, rnd


def _animated(i):
    """4 frames: one salt grain catches the light: dull, bright, star, bright."""
    base, rnd = _variant(i)
    x, y = rnd.randrange(3, 13), rnd.randrange(5, 20)
    frames = []
    for f in range(4):
        g = [row[:] for row in base]
        _put(g, x, y, "l" if f == 0 else "w")
        if f == 2:
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                _put(g, x + dx, y + dy, "l")
        frames.append(["".join(r) for r in g])
    return frames


SPRITES, FRAMES = {}, {}
for i in range(COUNT):
    key = "brightqudearth/%d" % i
    if i in ANIMATED:
        fr = _animated(i)
        SPRITES[key], FRAMES[key] = fr[0], fr[1:]
    else:
        SPRITES[key] = ["".join(r) for r in _variant(i)[0]]
