"""Fixtures batch 2: furniture, statues, machines, doors, gates, stairs, murals (Wave 2)."""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b3kit import C  # noqa: E402
from fixtures_keys import BATCH_KEYS  # noqa: E402

KEYS = BATCH_KEYS[2]
SPRITES = {}
KINDS = {}


def reg(kind=None):
    def deco(fn):
        SPRITES[fn.__name__] = fn()
        if kind:
            KINDS[fn.__name__] = kind
        return fn
    return deco


def fill(c, ch):
    c.r(0, 0, 15, 23, ch)


def ring(c, cx, cy, r0, r1, ch, y0=0, y1=23):
    for y in range(y0, y1 + 1):
        for x in range(16):
            d = math.hypot(x - cx, y - cy)
            if r0 <= d <= r1:
                c.p(x, y, ch)


def wall_base(c, top=6, base=3):
    """3/4 wall look: lit top face, mid face, dark base."""
    c.r(0, 0, 15, top - 1, "1")
    c.r(0, top - 2, 15, top - 1, "2")
    c.r(0, top, 15, 23, "2")
    c.r(0, top, 15, top, "1")
    c.r(0, 24 - base, 15, 23, "3")
    c.r(0, 23 - base, 15, 23 - base, "2")


# ====================================================================== DOORS
def door2(side, style):
    c = C()
    off = 16 if side == "right" else 0
    fill(c, "2")
    for y in range(24):
        for x in range(16):
            gx, gy = x + (off if side in ("left", "right") else 0), y + (24 if side == "bottom" else 0)
            ch = "2"
            if style == "basic":
                ch = "3" if (gx % 4 == 3) else ("1" if gx % 4 == 0 else "2")
            elif style == "metal":
                ch = "3" if gy % 5 == 4 else ("1" if gy % 5 == 0 else "2")
                if gy % 12 == 2 and x % 5 == 2:
                    ch = "4"
            elif style == "striped":
                ch = "4" if (gx + gy) % 6 < 3 else "2"
                if ch == "4" and (gx + gy) % 6 == 0:
                    ch = "5"
            elif style == "wavy":
                w = round(2 * math.sin(gx * 0.9)) + 3
                ch = "1" if (gy + w) % 5 == 0 else ("3" if (gy + w) % 5 == 4 else "2")
            elif style == "window":
                ch = "3" if (gx % 4 == 3) else ("1" if gx % 4 == 0 else "2")
            c.p(x, y, ch)
    if style == "basic":
        for (x, y) in ((4, 8), (5, 8), (4, 9), (6, 9), (9, 13), (10, 13), (9, 14), (11, 15)):
            c.p(x, y, "5")
        c.p(7, 4, "6")
        c.p(3, 18, "6")
    if style == "metal":
        # sliding panel cut in the centre of the pair
        pass
    if style == "window":
        # aperture straddles the double door's seam
        yy = (4, 11) if side != "bottom" else (0, 0)
        if side == "top":
            c.r(2, 13, 13, 19, "O"); c.r(3, 14, 12, 18, "c"); c.r(3, 14, 12, 14, "w")
            c.r(7, 14, 8, 18, "4")
        if side == "bottom":
            c.r(2, 3, 13, 9, "O"); c.r(3, 4, 12, 8, "c"); c.r(3, 4, 12, 4, "w")
            c.r(7, 4, 8, 8, "4")
        if side == "left":
            c.r(5, 6, 15, 13, "O"); c.r(6, 7, 15, 12, "c"); c.r(6, 7, 15, 7, "w")
        if side == "right":
            c.r(0, 6, 10, 13, "O"); c.r(0, 7, 9, 12, "c"); c.r(0, 7, 9, 7, "w")
    # frame and seam
    if side == "left":
        c.r(0, 0, 1, 23, "3"); c.p(2, 0, "3"); c.r(15, 0, 15, 23, "6")
        c.r(0, 0, 15, 1, "3"); c.r(0, 22, 15, 23, "3")
        c.r(3, 4, 3, 5, "4"); c.r(3, 18, 3, 19, "4")
    elif side == "right":
        c.r(14, 0, 15, 23, "3"); c.r(0, 0, 0, 23, "6")
        c.r(0, 0, 15, 1, "3"); c.r(0, 22, 15, 23, "3")
        c.r(12, 4, 12, 5, "4"); c.r(12, 18, 12, 19, "4")
        c.p(12, 11, "y"); c.p(12, 12, "y")
    elif side == "top":
        c.r(0, 0, 15, 2, "3"); c.r(0, 0, 1, 23, "3"); c.r(14, 0, 15, 23, "3")
        c.r(0, 23, 15, 23, "6"); c.r(0, 3, 15, 3, "1")
        c.p(7, 22, "y"); c.p(8, 22, "y")
    else:
        c.r(0, 21, 15, 23, "3"); c.r(0, 0, 1, 23, "3"); c.r(14, 0, 15, 23, "3")
        c.r(0, 0, 15, 0, "6"); c.r(7, 0, 8, 23, "3") if style in ("metal", "striped") else None
    if style == "metal" and side in ("top", "bottom"):
        c.r(7, 0, 8, 23, "6")
        c.r(5, 8, 10, 14, "6"); c.r(6, 9, 9, 13, "5"); c.r(7, 10, 8, 12, "O")
    if style == "metal" and side in ("left", "right"):
        c.r(4, 8, 11, 14, "6"); c.r(5, 9, 10, 13, "5"); c.r(6, 11, 9, 12, "O")
    if style == "striped" and side in ("left", "right"):
        c.r(0 if side == "right" else 4, 11, 11 if side == "right" else 15, 12, "3")
    return c.out()


def _d(name, side, style):
    SPRITES[name] = door2(side, style)
    KINDS[name] = "terrain"


_d("door2_basic_left", "left", "basic")
_d("door2_metal_bottom", "bottom", "metal")
_d("door2_metal_top", "top", "metal")
_d("door2_striped_right", "right", "striped")
_d("door2_wavy_left", "left", "wavy")
_d("door2_window_bottom", "bottom", "window")
_d("door2_window_top", "top", "window")


@reg("terrain")
def door_wavy():
    c = C()
    fill(c, "3")
    c.r(0, 0, 15, 1, "2"); c.mr(0, 0, 1, 23, "2")
    c.r(0, 0, 15, 0, "1")
    c.r(2, 2, 13, 22, "O")
    for y in range(3, 23):
        for x in range(3, 13):
            v = math.sin(y * 0.8 + x * 0.5) + math.cos(x * 0.9)
            c.p(x, y, "w" if v > 1.0 else ("1" if v > 0.1 else ("4" if v > -0.8 else "2")))
    ring(c, 7.5, 12.5, 2.5, 3.5, "w")
    c.r(7, 12, 8, 13, "O")
    return c.out()


# ====================================================================== GATES
@reg("terrain")
def earth_gate_right():
    c = C()
    fill(c, "2")
    for y in range(24):
        for x in range(16):
            if (x + y // 3) % 5 == 0:
                c.p(x, y, "3")
    c.r(0, 0, 15, 1, "1"); c.r(0, 22, 15, 23, "3")
    c.r(14, 0, 15, 23, "3"); c.r(0, 0, 0, 23, "6")
    # right half of the jewelled planet
    for y in range(24):
        for x in range(16):
            d = math.hypot(x - 0, y - 12)
            if d <= 9.6:
                c.p(x, y, "O")
            if d <= 8.4:
                ch = "B"
                v = math.sin(x * 0.8 + y * 0.5) + math.cos(y * 0.9 - x * 0.3)
                ch = "c" if v > 0.6 else ("b" if v < -0.9 else "B")
                if v > 1.3:
                    ch = "w"
                c.p(x, y, ch)
    for (x, y) in ((3, 8), (4, 8), (5, 9), (2, 15), (3, 16), (6, 13)):
        c.p(x, y, "4")        # agate islands
    for (x, y) in ((12, 5), (12, 6), (12, 18), (12, 17)):
        c.p(x, y, "5")        # patina
    return c.out()


@reg("terrain")
def lifegate_w():
    c = C()
    fill(c, "2")
    c.r(0, 0, 15, 1, "1"); c.r(0, 0, 1, 23, "3"); c.r(0, 22, 15, 23, "3")
    c.r(15, 0, 15, 23, "6")
    for y in range(2, 22):
        for x in range(2, 15):
            if (x * 3 + y) % 7 == 0:
                c.p(x, y, "5")           # coral patina
    # relief: a palm lifting a pyramid
    c.r(5, 14, 13, 19, "3"); c.r(6, 13, 12, 13, "3"); c.r(7, 12, 11, 12, "3")
    c.r(8, 11, 10, 11, "3"); c.p(9, 10, "1")
    c.line(6, 14, 12, 14, "1"); c.line(7, 13, 11, 13, "1"); c.line(8, 12, 10, 12, "1")
    c.line(9, 9, 3, 4, "4"); c.line(9, 9, 13, 4, "4"); c.line(9, 9, 9, 3, "4")
    c.line(9, 9, 4, 7, "5"); c.line(9, 9, 14, 7, "5")
    c.r(8, 20, 10, 21, "3")
    return c.out()


def _orchid(side):
    c = C()
    fill(c, "1")
    for y in range(24):
        for x in range(16):
            if (x // 4 + y // 4) % 2:
                c.p(x, y, "2")
    # lily field showing through
    if side == "n":
        c.r(0, 0, 15, 5, "3"); c.r(0, 6, 15, 6, "1")
        c.r(2, 7, 13, 23, "o")
        c.mr(0, 7, 1, 23, "3")
        for (x, y) in ((4, 12), (9, 17), (6, 20), (11, 10), (5, 8)):
            c.p(x, y, "w"); c.p(x - 1, y, "5"); c.p(x + 1, y, "5"); c.p(x, y + 1, "g")
        c.r(5, 1, 10, 4, "5"); c.r(6, 2, 9, 3, "4"); c.p(7, 2, "w"); c.p(8, 2, "w")
    else:
        c.r(0, 0, 3, 23, "3"); c.r(4, 0, 4, 23, "1")
        c.r(0, 19, 15, 23, "3"); c.r(4, 18, 15, 18, "1")
        c.r(5, 0, 15, 17, "o")
        for (x, y) in ((8, 4), (12, 9), (7, 13), (11, 15), (13, 2)):
            c.p(x, y, "w"); c.p(x - 1, y, "5"); c.p(x + 1, y, "5"); c.p(x, y + 1, "g")
        c.r(5, 20, 15, 21, "2")
        c.r(1, 3, 2, 6, "5"); c.r(1, 10, 2, 13, "5")
    return c.out()


SPRITES["orchid_gate_n"] = _orchid("n"); KINDS["orchid_gate_n"] = "terrain"
SPRITES["orchid_gate_sw"] = _orchid("sw"); KINDS["orchid_gate_sw"] = "terrain"


# ====================================================================== STAIRS
def stairs(kind):
    c = C()
    fill(c, "O")                  # the pit
    c.r(2, 2, 13, 21, "O")
    def tread(x0, y0, x1, y1):
        c.r(x0, y0, x1, y1, "w"); c.r(x0, y1, x1, y1, "L")
        c.r(x0, y0, x1, y0, "w")
        c.p(x0 + 1, y0 + 1, "4") if (x1 - x0) > 2 else None
    if kind == "e":
        c.r(0, 0, 15, 23, "O")
        for i, x in enumerate((13, 9, 5)):
            c.r(x, 0, 15, 23, "O")
            c.r(x, 0, x + 3, 23, "w"); c.r(x + 3, 0, x + 3, 23, "L")
            c.r(x + 1, 3, x + 1, 5, "4"); c.r(x + 1, 14, x + 1, 17, "4")
        c.r(0, 0, 3, 23, "O")
    elif kind == "nw":
        c.r(0, 0, 15, 23, "O")
        for i in range(3):
            o = i * 4
            c.r(o, o, 15, o + 3, "w"); c.r(o, o, o + 3, 23, "w")
            c.r(o + 4, o + 3, 15, o + 3, "L") if False else None
            c.r(o, o + 3, 15, o + 3, "L"); c.r(o + 3, o, o + 3, 23, "L")
            c.p(o + 1, o + 1, "4")
        c.r(10, 10, 15, 23, "O"); c.r(0, 12, 15, 23, "O") if False else None
        c.r(0, 12, 9, 23, "O") if False else None
        c.r(4, 12, 15, 23, "O"); c.r(12, 4, 15, 23, "O")
        c.r(0, 0, 15, 3, "w"); c.r(0, 3, 15, 3, "L"); c.r(0, 0, 3, 23, "w"); c.r(3, 0, 3, 23, "L")
        c.r(4, 4, 15, 7, "w"); c.r(4, 7, 15, 7, "L"); c.r(4, 4, 7, 23, "w"); c.r(7, 4, 7, 23, "L")
        c.r(8, 8, 15, 11, "w"); c.r(8, 11, 15, 11, "L"); c.r(8, 8, 11, 23, "w"); c.r(11, 8, 11, 23, "L")
        c.r(12, 12, 15, 23, "O"); c.r(8, 12, 11, 23, "w") if False else None
        c.r(12, 12, 15, 23, "O"); c.r(8, 12, 11, 23, "O")
        c.r(4, 8, 7, 23, "w"); c.r(7, 8, 7, 23, "L")
        c.r(8, 12, 15, 23, "O")
        c.p(1, 1, "4"); c.p(5, 5, "4"); c.p(9, 9, "4")
    else:  # sw
        c.r(0, 0, 15, 23, "O")
        c.r(0, 20, 15, 23, "w"); c.r(0, 20, 15, 20, "L") if False else None
        c.r(0, 20, 15, 23, "w"); c.r(0, 23, 15, 23, "L"); c.r(0, 0, 3, 23, "w"); c.r(3, 0, 3, 23, "L")
        c.r(4, 16, 15, 19, "w"); c.r(4, 19, 15, 19, "L"); c.r(4, 12, 7, 19, "w"); c.r(7, 12, 7, 19, "L")
        c.r(8, 12, 15, 15, "w"); c.r(8, 15, 15, 15, "L"); c.r(8, 8, 11, 15, "w"); c.r(11, 8, 11, 15, "L")
        c.p(1, 21, "4"); c.p(5, 17, "4"); c.p(9, 13, "4")
        c.r(0, 0, 15, 7, "O"); c.r(12, 8, 15, 15, "O")
    return c.out()


for _k in ("e", "nw", "sw"):
    SPRITES["sunken_room_stairs_" + _k] = stairs(_k)
    KINDS["sunken_room_stairs_" + _k] = "terrain"


# ====================================================================== MURALS / WALLS
@reg("terrain")
def mural_appeasesbaetyl_c():
    c = C()
    wall_base(c, 6, 2)
    c.r(0, 7, 15, 7, "3")
    # a kneeling figure offering to a standing stone
    c.r(10, 9, 12, 19, "4"); c.r(10, 9, 10, 19, "5"); c.p(11, 8, "4")
    c.r(3, 15, 6, 19, "5"); c.r(3, 12, 5, 14, "4"); c.p(4, 11, "4")
    c.line(6, 15, 9, 14, "4"); c.p(9, 13, "w")
    c.r(2, 20, 13, 20, "6")
    c.p(1, 9, "5"); c.p(14, 10, "5")
    return c.out()


@reg("terrain")
def mural_centerpiece_period():
    c = C()
    wall_base(c, 6, 2)
    c.r(4, 7, 11, 20, "O"); c.r(5, 8, 10, 19, "3"); c.r(6, 8, 9, 19, "2")
    for y in (10, 14, 18):
        c.r(5, y, 10, y, "4")
    c.line(7, 11, 6, 12, "5"); c.line(8, 11, 9, 12, "5"); c.line(6, 12, 7, 13, "5"); c.line(9, 12, 8, 13, "5")
    c.r(0, 7, 4, 7, "3"); c.r(11, 7, 15, 7, "3")
    c.r(0, 13, 3, 13, "5"); c.r(12, 13, 15, 13, "5")
    return c.out()


@reg("terrain")
def mural_ruined4_c():
    c = C()
    wall_base(c, 6, 2)
    c.r(0, 7, 15, 7, "3")
    c.r(2, 9, 7, 12, "3"); c.r(3, 10, 6, 11, "4")
    c.r(9, 13, 13, 17, "3"); c.r(10, 14, 12, 16, "5")
    # cracks and missing chunks
    c.line(7, 7, 5, 14, "O"); c.line(5, 14, 7, 20, "O"); c.line(11, 7, 12, 12, "O")
    c.r(0, 16, 3, 20, "O"); c.r(1, 15, 2, 15, "O"); c.p(14, 8, "O"); c.p(15, 8, "O"); c.r(14, 9, 15, 10, "O")
    c.p(6, 10, "1"); c.p(10, 15, "1")
    c.r(12, 21, 15, 22, "3")
    return c.out()


@reg("terrain")
def wall_golem_interior():
    c = C()
    wall_base(c, 5, 2)
    for y in range(6, 21):
        for x in range(16):
            if (x * 5 + y * 3) % 11 == 0:
                c.p(x, y, "1")           # moist sheen
    # undercircuitry under a translucent film
    c.line(2, 8, 2, 14, "y"); c.line(2, 14, 7, 14, "y"); c.line(7, 14, 7, 19, "y")
    c.line(7, 9, 13, 9, "y"); c.line(13, 9, 13, 16, "y")
    for (x, y) in ((2, 8), (7, 19), (13, 16), (7, 9)):
        c.p(x, y, "w")
    c.r(9, 12, 11, 14, "L"); c.p(10, 13, "y")
    return c.out()


@reg("terrain")
def starship_1_wallbed_w():
    c = C()
    wall_base(c, 5, 2)
    c.r(2, 7, 15, 20, "O")                     # hollow
    c.r(3, 8, 15, 19, "N")
    c.r(3, 14, 15, 19, "w"); c.r(3, 14, 15, 14, "W")
    c.r(3, 15, 15, 15, "w")
    c.r(4, 11, 7, 14, "w"); c.r(4, 11, 7, 11, "l")      # pillow
    for x in range(8, 15, 2):
        c.r(x, 16, x, 19, "4"); c.r(x + 1, 16, x + 1, 19, "5")   # patterned blanket
    c.r(3, 8, 3, 13, "5"); c.r(4, 8, 4, 13, "4")                   # curtain at the front-left
    c.r(2, 7, 15, 7, "6")
    return c.out()


@reg("terrain")
def tile_dirt():
    c = C()
    fill(c, "3")
    c.r(0, 0, 15, 0, "2"); c.r(0, 12, 15, 12, "2"); c.r(0, 0, 0, 23, "2"); c.r(8, 0, 8, 23, "2") if False else None
    c.r(0, 12, 15, 12, "2")
    for (x, y) in ((3, 3), (4, 4), (5, 5), (11, 7), (12, 8), (2, 16), (3, 17), (4, 17), (10, 19), (11, 20), (13, 15)):
        c.p(x, y, "2")
    for (x, y) in ((6, 2), (13, 3), (9, 15), (4, 21), (8, 8)):
        c.p(x, y, "1")
    c.line(8, 14, 12, 18, "2")
    return c.out()


@reg("terrain")
def dock_platform_n():
    c = C()
    fill(c, "O")
    for y in range(4, 24):
        for x in range(16):
            c.p(x, y, "3" if (x % 4 and y % 4) else "2")
    c.r(0, 0, 15, 3, "4")
    for x in range(-4, 16, 4):
        c.line(x, 0, x + 3, 3, "6"); c.line(x + 1, 0, x + 4, 3, "6")
    c.r(0, 4, 15, 4, "5")
    c.r(0, 4, 0, 23, "5"); c.r(15, 4, 15, 23, "5")
    return c.out()


@reg("terrain")
def great_machine_shrine_c():
    c = C()
    fill(c, "L")
    c.r(1, 1, 14, 22, "3")
    for y in range(3, 22, 4):
        for x in range(3, 14, 4):
            c.r(x, y, x + 1, y + 1, "c"); c.p(x, y, "w")
    c.r(0, 0, 15, 0, "y"); c.r(0, 23, 15, 23, "y"); c.r(0, 0, 0, 23, "y"); c.r(15, 0, 15, 23, "y")
    c.r(2, 2, 13, 2, "2")
    return c.out()


def _kneeler(c, x0, y0, flip=False):
    """small marble figure kneeling at a lever; drawn at (x0,y0) top-left, 6x9."""
    rows = ["..OO..", ".OwwO.", ".OwwO.", "OwwwwO", "OlwwlO", "OlllLO", "OLlllO", "OLLLLO", ".OOOO."]
    for j, r in enumerate(rows):
        for i, ch in enumerate(r):
            if ch != ".":
                c.p(x0 + (5 - i if flip else i), y0 + j, ch)


@reg("terrain")
def great_machine_shrine_w():
    c = C()
    fill(c, "L")
    c.r(1, 1, 14, 22, "3")
    for y in range(3, 22, 4):
        for x in range(8, 14, 4):
            c.r(x + 2, y, x + 3, y + 1, "c")
    c.r(0, 0, 15, 0, "y"); c.r(0, 23, 15, 23, "y"); c.r(15, 0, 15, 23, "y"); c.r(0, 0, 0, 23, "y")
    _kneeler(c, 2, 7)
    c.line(9, 8, 11, 13, "Y") if False else c.line(9, 9, 11, 13, "y")
    c.p(9, 8, "r")
    return c.out()


@reg("terrain")
def great_machine_shrine_nw():
    c = C()
    fill(c, "L")
    c.r(1, 1, 14, 22, "3")
    for y in range(9, 22, 4):
        for x in range(3, 14, 4):
            c.r(x, y, x + 1, y + 1, "c")
    c.r(0, 0, 15, 0, "y"); c.r(0, 23, 15, 23, "y"); c.r(15, 0, 15, 23, "y"); c.r(0, 0, 0, 23, "y")
    _kneeler(c, 2, 2)
    c.line(9, 3, 12, 6, "y"); c.p(9, 3, "r")
    c.r(8, 8, 15, 8, "2")
    return c.out()


# ====================================================================== FLOOR CLOCKS (mosaic)
def clock(half):
    c = C()
    fill(c, "O")
    cy = 24 if half == "n" else -1
    for y in range(24):
        for x in range(16):
            d = math.hypot(x - 7.5, y - cy)
            if 11 <= d <= 13:
                c.p(x, y, "w" if (x + y) % 2 else "1")
            elif d < 11 and d > 9:
                c.p(x, y, "3")
            elif d < 9 and (x + y) % 4 == 0:
                c.p(x, y, "3")
            elif d < 9:
                c.p(x, y, "2")
    for ang in range(0, 360, 30):
        a = math.radians(ang)
        x = round(7.5 + 10 * math.cos(a)); y = round(cy - 10 * math.sin(a))
        if 0 <= y < 24:
            c.p(x, y, "O"); c.p(x + 1, y, "O")
    if half == "n":
        c.line(7, 23, 7, 17, "w"); c.line(8, 23, 8, 17, "w")
    else:
        c.line(7, 0, 10, 4, "w"); c.line(8, 0, 11, 4, "w")
    return c.out()


for _h in ("n", "s"):
    SPRITES["floor_clock_" + _h] = clock(_h)
    KINDS["floor_clock_" + _h] = "terrain"


# ====================================================================== OBJECTS
@reg()
def arkcore():
    c = C()
    c.ell(7.5, 10, 6, 6, "R"); c.ell(7.5, 10, 5, 5, "4"); c.ell(7.5, 10, 3.2, 3.2, "5")
    c.ell(6.5, 9, 1.6, 1.6, "w")
    c.line(4, 6, 11, 14, "M"); c.line(11, 6, 4, 14, "b")
    ring(c, 7.5, 10, 6.2, 7.4, "1", 0, 21)
    c.r(3, 17, 12, 18, "2"); c.r(2, 19, 13, 21, "2"); c.r(2, 21, 13, 21, "3"); c.r(2, 19, 13, 19, "1")
    c.r(6, 16, 9, 16, "3"); c.p(4, 20, "R"); c.p(11, 20, "R")
    c.shadow(2, 13, 22)
    return c.out()


@reg()
def bottle():
    c = C()
    c.ell(7.5, 14, 4.5, 5.5, "2"); c.ell(7, 13, 3, 4, "1")
    c.r(6, 6, 9, 10, "2"); c.r(6, 6, 6, 10, "1")
    c.r(5, 5, 10, 5, "w") ; c.r(6, 3, 9, 4, "n"); c.r(7, 2, 8, 2, "n")
    ring(c, 11.5, 8, 1.2, 2.2, "y", 5, 12)
    c.r(5, 15, 10, 19, "3") if False else c.r(5, 17, 10, 19, "3")
    c.p(5, 12, "w"); c.p(5, 13, "w"); c.p(6, 11, "w")
    c.shadow(3, 12, 21)
    return c.out()


@reg()
def dagasha_crucifix():
    c = C()
    c.r(6, 1, 9, 20, "2"); c.r(6, 1, 6, 20, "1"); c.r(9, 1, 9, 20, "3")
    c.r(1, 6, 14, 9, "2"); c.r(1, 6, 14, 6, "1"); c.r(1, 9, 14, 9, "3")
    for (x, y) in ((4, 4), (11, 4), (3, 11), (12, 11), (4, 15), (11, 17), (7, 0), (0, 7), (15, 8), (8, 22)):
        c.p(x, y, "4")
    for (x, y) in ((5, 5), (10, 5), (5, 10), (10, 10), (5, 17), (10, 14), (3, 5), (12, 5)):
        c.p(x, y, "4")
    c.r(7, 7, 8, 8, "w")
    c.shadow(4, 11, 22) if False else None
    return c.out()


@reg()
def eater_chimes():
    c = C()
    c.r(1, 2, 14, 3, "n"); c.r(1, 3, 14, 3, "N"); c.r(0, 2, 0, 20, "N"); c.r(15, 2, 15, 20, "N")
    c.r(0, 1, 15, 1, "N")
    for i, x in enumerate((3, 6, 9, 12)):
        h = (11, 7, 9, 6)[i]
        c.p(x, 4, "L")
        c.r(x - 1, 5, x + 1, 5 + h, "2" if i % 2 else "1")
        c.r(x + 1, 5, x + 1, 5 + h, "3")
        c.r(x - 1, 5 + h, x + 1, 6 + h, "4")
        c.p(x - 1, 6, "w")
    c.r(2, 20, 13, 20, "N")
    c.shadow(1, 14, 21)
    return c.out()


@reg()
def eater_couch_r():
    c = C()
    c.r(2, 5, 12, 9, "2"); c.r(2, 5, 12, 5, "1"); c.r(1, 6, 1, 14, "2")
    c.r(2, 10, 10, 15, "1"); c.r(2, 10, 10, 10, "w"); c.r(2, 15, 10, 15, "3")
    c.r(11, 8, 14, 17, "2"); c.r(11, 8, 14, 9, "1"); c.r(14, 9, 14, 17, "3"); c.r(11, 17, 14, 17, "3")
    c.r(2, 16, 10, 17, "n"); c.r(2, 17, 10, 17, "N")
    c.r(2, 18, 3, 19, "N"); c.r(11, 18, 13, 19, "N")
    c.p(5, 12, "4"); c.p(8, 12, "4"); c.p(12, 12, "4")
    c.r(1, 15, 1, 16, "n")
    c.shadow(1, 14, 20)
    return c.out()


@reg()
def eater_hookah():
    c = C()
    for (x, y) in ((3, 2), (4, 4), (5, 5), (6, 6), (7, 3), (7, 5), (9, 4), (9, 6), (10, 5), (11, 3), (12, 2)):
        pass
    c.line(7, 12, 3, 4, "w"); c.line(8, 12, 6, 2, "4"); c.line(8, 12, 10, 2, "4"); c.line(9, 12, 13, 4, "w")
    for (x, y) in ((3, 3), (6, 1), (10, 1), (13, 3)):
        c.p(x, y, "c")
    c.ell(7.5, 15, 5, 3.5, "2"); c.ell(7, 14.5, 3, 2, "1"); c.r(4, 17, 11, 18, "3")
    c.r(6, 11, 9, 12, "1")
    c.p(5, 14, "w")
    c.line(13, 16, 15, 20, "y")
    c.shadow(3, 12, 22)
    return c.out()


@reg()
def eater_sign_script():
    c = C()
    c.r(1, 4, 14, 15, "N"); c.r(2, 5, 13, 14, "2"); c.r(2, 5, 13, 5, "1"); c.r(2, 14, 13, 14, "3")
    for (x, y) in ((3, 7), (4, 8), (6, 7), (6, 9), (8, 8), (9, 7), (9, 9), (11, 7), (11, 9), (12, 8), (4, 11), (5, 12), (7, 11), (8, 12), (10, 11)):
        c.p(x, y, "4")
    c.p(3, 6, "w"); c.p(8, 11, "w")
    c.r(3, 16, 4, 20, "N"); c.r(11, 16, 12, 20, "N")
    c.shadow(2, 13, 21)
    return c.out()


@reg()
def eater_vessel():
    c = C()
    c.ell(7.5, 13, 5.5, 6, "2"); c.ell(6.5, 12, 3.5, 4, "1"); c.r(5, 17, 10, 19, "3")
    c.r(5, 5, 10, 7, "2"); c.r(5, 5, 5, 7, "1"); c.r(4, 4, 11, 4, "1")
    c.r(10, 7, 10, 8, "3")
    for (x, y) in ((4, 11), (5, 12), (9, 10), (10, 13), (7, 16), (8, 15), (6, 9)):
        c.p(x, y, "3")
    c.shadow(3, 12, 21)
    return c.out()


@reg()
def floor_cushion():
    c = C()
    c.ell(7.5, 14, 7, 5, "3"); c.ell(7.5, 13, 6.5, 4.5, "2"); c.ell(6.5, 12, 4.5, 3, "1")
    c.r(6, 12, 9, 13, "4") if False else None
    c.p(7, 13, "4"); c.p(8, 13, "4"); c.p(7, 12, "5"); c.p(8, 12, "5")
    for (x, y) in ((3, 12), (12, 12), (7, 17), (7, 9)):
        c.p(x, y, "4")
    c.p(4, 10, "w")
    c.shadow(1, 14, 20)
    return c.out()


@reg()
def generator():
    c = C()
    c.r(1, 8, 12, 18, "3"); c.r(1, 8, 12, 9, "1"); c.r(1, 10, 11, 17, "2"); c.r(1, 10, 1, 17, "1")
    for x in (3, 5, 7, 9):
        c.r(x, 11, x, 16, "3")
    c.r(2, 3, 11, 6, "5"); c.r(2, 3, 11, 3, "4"); c.r(2, 6, 11, 6, "6")        # solar panel
    for x in (5, 8):
        c.r(x, 4, x, 5, "6")
    c.r(6, 7, 7, 7, "L")
    c.r(13, 11, 14, 11, "L"); c.r(14, 11, 14, 14, "l"); c.r(13, 14, 15, 14, "l")    # crank
    c.r(10, 12, 11, 13, "O"); c.p(10, 12, "c")
    c.r(2, 19, 3, 20, "L"); c.r(10, 19, 11, 20, "L")
    c.shadow(1, 14, 21)
    return c.out()


@reg()
def golem_interior_locker():
    c = C()
    c.r(2, 2, 13, 21, "3"); c.r(3, 3, 12, 20, "2"); c.r(3, 3, 12, 3, "1")
    c.r(7, 3, 8, 20, "3")
    for y in (7, 11, 15):
        c.r(3, y, 6, y, "3"); c.r(9, y, 12, y, "3")
        c.r(3, y + 1, 6, y + 1, "1"); c.r(9, y + 1, 12, y + 1, "1")
    c.r(6, 11, 6, 13, "y") if False else None
    c.p(6, 10, "y"); c.p(9, 10, "y")
    c.r(2, 2, 13, 2, "1") if False else None
    c.p(4, 5, "4"); c.p(11, 5, "4")
    c.shadow(2, 13, 22)
    return c.out()


@reg()
def kah_conveyor():
    c = C()
    ring(c, 4.5, 11, 2.6, 4.2, "4", 5, 17)
    ring(c, 11, 11, 2.6, 4.2, "4", 5, 17)
    ring(c, 4.5, 11, 3.2, 3.8, "5", 5, 17)
    c.line(5, 8, 10, 14, "5"); c.line(10, 8, 5, 14, "5")
    c.r(5, 9, 10, 13, "O") if False else None
    c.r(5, 16, 10, 20, "2"); c.r(5, 16, 10, 16, "1"); c.r(5, 20, 10, 20, "3")
    c.r(7, 17, 8, 18, "c")
    c.r(6, 12, 9, 13, "3"); c.r(7, 12, 8, 12, "c")
    c.shadow(3, 12, 22)
    return c.out()


@reg()
def left_spindle_support():
    c = C()
    c.r(1, 18, 14, 20, "2"); c.r(1, 18, 14, 18, "1"); c.r(1, 20, 14, 20, "3")
    c.p(2, 19, "l"); c.p(13, 19, "l"); c.p(7, 19, "L") if False else None
    c.line(4, 18, 9, 5, "1"); c.line(5, 18, 10, 5, "2"); c.line(6, 18, 11, 5, "3")
    c.r(9, 3, 12, 6, "2"); c.r(9, 3, 12, 3, "1"); c.r(12, 4, 12, 6, "3")
    c.r(2, 4, 8, 5, "B") if False else None
    c.line(9, 4, 2, 2, "B"); c.line(9, 5, 2, 4, "b")
    c.shadow(1, 14, 22)
    return c.out()


def spindle_top(lean):
    c = C()
    for y in range(0, 21):
        w = 1 + y * 5 // 20
        cx = 7.5 + lean * (20 - y) / 20.0 * 0 + lean
        x0 = int(round(cx - w)); x1 = int(round(cx + w))
        c.r(x0, y, x1, y, "2")
        c.p(x0, y, "1"); c.p(x1, y, "3")
        if y % 4 == 2:
            c.p(x0 + 1, y, "4")
    c.r(2, 19, 13, 21, "3"); c.r(2, 19, 13, 19, "1") if False else None
    c.r(3, 20, 12, 20, "2")
    c.shadow(2, 13, 22)
    return c.out()


SPRITES["spindle_ribbon_top"] = spindle_top(0)
SPRITES["right_spindle_ribbon_top"] = spindle_top(1)


@reg()
def nacham_loom():
    c = C()
    c.r(1, 3, 2, 20, "3"); c.r(13, 3, 14, 20, "3"); c.r(1, 3, 14, 5, "2"); c.r(1, 3, 14, 3, "1")
    c.r(1, 18, 14, 20, "2"); c.r(1, 20, 14, 20, "3")
    for x in range(4, 13, 2):
        c.r(x, 6, x, 17, "4")
    c.r(3, 12, 12, 13, "1"); c.r(3, 13, 12, 13, "L")                 # sheet metal
    c.r(5, 6, 10, 7, "5"); c.r(5, 7, 10, 7, "6")
    for (x, y) in ((4, 9), (9, 15), (11, 9), (6, 16)):
        c.p(x, y, "c"); c.p(x + 1, y - 1, "w")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def reshaping_nook():
    c = C()
    c.r(1, 3, 14, 21, "1") ; c.r(2, 4, 13, 20, "2"); c.r(1, 3, 14, 4, "y")
    ring(c, 7.5, 9, 4, 6, "y", 0, 21)
    c.r(1, 12, 14, 21, "1")
    c.r(3, 5, 12, 20, "O") if False else None
    c.r(3, 6, 12, 19, "3")
    c.r(4, 7, 11, 8, "c"); c.p(4, 7, "w") if False else None
    c.r(4, 5, 5, 6, "w") ; c.r(5, 4, 5, 5, "w") if False else None
    c.line(10, 5, 8, 10, "l"); c.line(8, 10, 9, 12, "L"); c.p(9, 12, "r")
    c.r(4, 15, 11, 17, "L"); c.r(4, 15, 11, 15, "l")
    c.r(5, 12, 10, 14, "4"); c.r(6, 11, 9, 11, "5"); c.p(6, 12, "w")
    c.r(2, 20, 13, 20, "3")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def shelf():
    c = C()
    c.r(1, 2, 14, 21, "L"); c.r(2, 3, 13, 20, "3")
    for y in (6, 11, 16):
        c.r(2, y, 13, y, "1"); c.r(2, y + 1, 13, y + 1, "2")
    for (y0, xs) in ((3, (3, 7, 10)), (8, (4, 9)), (13, (3, 6, 11)), (18, (5, 10))):
        for x in xs:
            c.r(x, y0, x + 1, y0 + 2, "4"); c.p(x, y0, "Y"); c.p(x + 1, y0 + 2, "5")
    for y in (4, 9, 14, 19):
        c.p(2, y, "l"); c.p(13, y, "l")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def star_carousel_art():
    c = C()
    c.r(2, 8, 13, 19, "C"); c.r(3, 9, 12, 18, "3") ; c.r(3, 9, 3, 18, "w") if False else None
    c.r(3, 12, 12, 18, "h"); c.r(3, 11, 12, 11, "c")
    for (x, y) in ((4, 12), (7, 13), (10, 12), (5, 15), (9, 16), (11, 14)):
        c.p(x, y, "G"); c.p(x, y + 1, "g")
    for (x, y) in ((6, 14), (8, 17), (4, 17)):
        c.p(x, y, "c")
    c.r(3, 9, 5, 9, "w"); c.p(3, 10, "w")
    c.line(13, 15, 14, 8, "4"); c.line(14, 8, 12, 3, "4"); c.line(12, 3, 9, 2, "4"); c.p(8, 2, "w")
    c.r(2, 19, 13, 20, "2")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def star_carousel_passenger_console():
    c = C()
    c.r(1, 10, 14, 19, "d"); c.r(1, 10, 14, 10, "b")
    c.r(2, 5, 13, 11, "O"); c.r(3, 6, 12, 10, "b")
    c.r(3, 6, 12, 6, "B")
    c.line(4, 9, 6, 7, "w"); c.line(6, 7, 8, 9, "w"); c.line(8, 9, 11, 7, "B")
    c.p(11, 9, "c")
    c.r(2, 12, 13, 12, "b")
    for x in (3, 6, 9, 12):
        c.p(x, 14, "c")
    c.r(3, 16, 12, 17, "B")
    c.r(2, 19, 13, 20, "d")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def star_carousel_pilot_console_s():
    c = C()
    c.r(1, 6, 14, 20, "d"); c.r(1, 6, 14, 6, "b")
    c.r(2, 7, 13, 18, "O")
    for i, x in enumerate(range(3, 13, 2)):
        h = (3, 6, 9, 5, 7)[i]
        c.r(x, 17 - h, x + 1, 17, "B"); c.r(x, 17 - h, x + 1, 17 - h, "w"); c.r(x + 1, 18 - h, x + 1, 17, "b")
    c.r(2, 18, 13, 20, "b"); c.r(2, 18, 13, 18, "B")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def star_carousel_star_chart_c():
    c = C()
    c.ell(7.5, 18, 6, 2.5, "3"); c.ell(7.5, 17, 5.5, 2, "2"); c.r(5, 16, 10, 16, "1")
    c.r(6, 15, 9, 15, "c")
    pts = [(3, 3), (7, 5), (12, 4), (5, 9), (10, 10), (13, 8), (7, 13), (3, 12)]
    for a, b in ((0, 1), (1, 2), (1, 3), (3, 4), (4, 5), (4, 6), (6, 7), (3, 7)):
        c.line(*pts[a], *pts[b], "4")
    for (x, y) in pts:
        c.r(x, y, x + 1, y + 1, "w")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def star_carousel_table():
    c = C()
    c.r(1, 4, 14, 7, "2"); c.r(1, 4, 14, 4, "1"); c.r(1, 7, 14, 7, "3")
    c.r(3, 8, 12, 19, "2"); c.r(3, 8, 5, 19, "1"); c.r(10, 8, 12, 19, "3")
    c.r(5, 9, 10, 13, "1"); c.r(6, 9, 9, 12, "2")           # blank, eyeless face
    c.r(7, 14, 8, 15, "3")
    c.r(1, 19, 14, 21, "3"); c.r(1, 19, 14, 19, "2")
    c.r(6, 10, 9, 10, "3")
    c.shadow(1, 14, 22)
    return c.out()


@reg("terrain")
def starship_1_escape_hatch():
    c = C()
    fill(c, "3")
    for y in range(24):
        for x in range(16):
            if abs(x - 7.5) * 0.866 + abs(y - 11.5) * 0.5 <= 6.9 and abs(y - 11.5) <= 10.5:
                c.p(x, y, "O")
            if abs(x - 7.5) * 0.866 + abs(y - 11.5) * 0.5 <= 5.6 and abs(y - 11.5) <= 9.2:
                c.p(x, y, "2")
    c.r(0, 4, 15, 5, "y"); c.r(0, 18, 15, 19, "y")      # oiled tracks
    for y in range(7, 17):
        c.r(4, y, 4, y, "1")
    c.r(6, 9, 9, 14, "3"); c.r(7, 10, 8, 13, "y"); c.p(7, 10, "w")
    return c.out()


@reg()
def starship_1_pilot_seat():
    c = C()
    c.r(3, 3, 11, 11, "b"); c.r(3, 3, 11, 3, "B"); c.r(3, 3, 4, 11, "B"); c.r(11, 3, 11, 11, "d")
    c.r(3, 12, 11, 17, "b"); c.r(3, 12, 11, 12, "B"); c.r(3, 17, 11, 17, "d")
    c.r(12, 10, 14, 18, "W"); c.r(12, 10, 14, 10, "w")
    c.p(13, 12, "r"); c.p(13, 14, "c"); c.p(12, 16, "y"); c.r(13, 16, 13, 16, "w")
    c.r(1, 10, 2, 17, "W")
    c.r(4, 18, 10, 19, "L"); c.r(6, 20, 8, 20, "L")
    c.shadow(2, 13, 21)
    return c.out()


@reg()
def starship_1_tree_sculpture():
    c = C()
    c.line(7, 20, 7, 12, "N"); c.line(8, 20, 8, 12, "n")
    c.r(3, 19, 12, 21, "n"); c.r(3, 19, 12, 19, "t") ; c.r(3, 21, 12, 21, "N")
    # spiralling triangle
    c.line(7, 1, 2, 11, "y"); c.line(2, 11, 13, 11, "y"); c.line(13, 11, 8, 1, "y")
    c.line(7, 4, 4, 10, "t"); c.line(4, 10, 11, 10, "t"); c.line(11, 10, 8, 4, "t")
    c.line(7, 7, 6, 9, "w"); c.line(6, 9, 9, 9, "w")
    c.p(7, 1, "w")
    c.p(3, 11, "n"); c.p(12, 11, "n")
    c.shadow(2, 13, 22)
    return c.out()


@reg()
def starship_floor_cushion():
    c = C()
    c.r(2, 9, 13, 17, "W"); c.r(2, 9, 13, 10, "w"); c.r(2, 9, 2, 17, "w"); c.r(13, 10, 13, 17, "l")
    c.r(3, 17, 12, 17, "l")
    c.r(3, 11, 12, 16, "w")
    c.p(7, 13, "W"); c.p(8, 13, "W"); c.p(7, 14, "W"); c.p(8, 14, "W")
    for (x, y) in ((2, 8), (13, 8), (2, 18), (13, 18)):
        c.p(x, y, "y"); c.p(x + (1 if x < 8 else -1), y, "y") if False else None
    c.p(3, 11, "y"); c.p(12, 11, "y"); c.p(3, 16, "y"); c.p(12, 16, "y")
    c.shadow(1, 14, 20)
    return c.out()


@reg()
def techlamp():
    c = C()
    c.r(3, 12, 12, 14, "2"); c.r(3, 12, 12, 12, "1"); c.r(4, 15, 11, 15, "3")
    c.r(6, 16, 9, 19, "3"); c.r(4, 20, 11, 21, "2"); c.r(4, 20, 11, 20, "1")
    c.ell(7.5, 8, 3.8, 5, "5"); c.ell(7.5, 9, 2.6, 3.8, "4"); c.ell(7.5, 10, 1.4, 2.2, "w")
    c.line(7, 1, 7, 3, "5"); c.p(5, 4, "5"); c.p(10, 5, "6"); c.p(4, 7, "6")
    c.p(11, 2, "c"); c.p(3, 3, "c")
    c.shadow(3, 12, 22)
    return c.out()


@reg()
def vaam_blower():
    c = C()
    c.r(1, 6, 8, 17, "2"); c.r(1, 6, 8, 7, "1") ; c.r(1, 6, 1, 17, "1"); c.r(8, 7, 8, 17, "3")
    ring(c, 4.5, 11.5, 2, 3, "4", 6, 17)
    c.p(4, 11, "w") if False else c.r(4, 11, 5, 12, "w")
    c.r(1, 17, 8, 17, "3")
    c.r(9, 9, 11, 14, "5"); c.r(9, 9, 11, 9, "4")
    c.line(12, 8, 14, 5, "L") ; c.r(12, 8, 14, 15, "l") ; c.r(12, 8, 14, 8, "w"); c.r(14, 9, 14, 15, "L")
    c.r(11, 15, 15, 17, "L") if False else None
    c.r(12, 15, 14, 17, "5")
    c.r(1, 18, 14, 19, "3"); c.p(10, 6, "c"); c.p(11, 5, "c")
    c.shadow(1, 14, 21)
    return c.out()


@reg()
def wood_carved_bed():
    c = C()
    c.r(1, 2, 14, 5, "n"); c.r(1, 2, 14, 2, "t"); c.r(1, 5, 14, 5, "N")     # headboard
    c.r(1, 6, 14, 19, "N"); c.r(2, 6, 13, 18, "n")
    c.r(3, 6, 12, 9, "w"); c.r(3, 6, 12, 6, "W") if False else None
    c.r(3, 9, 12, 9, "l") ; c.r(2, 10, 13, 18, "B"); c.r(2, 10, 13, 10, "w")
    for y in (12, 14, 16):
        for x in range(3, 13, 2):
            c.p(x, y, "4"); c.p(x + 1, y + 1, "w")
    c.r(1, 19, 14, 20, "N"); c.r(1, 19, 14, 19, "n")
    c.r(0, 2, 0, 20, "N") if False else None
    c.p(1, 3, "y"); c.p(14, 3, "y")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def wood_carved_dresser():
    c = C()
    c.r(1, 4, 14, 20, "N"); c.r(2, 5, 13, 19, "n"); c.r(1, 3, 14, 4, "t") ; c.r(1, 4, 14, 4, "n")
    for y in (6, 11, 15):
        c.r(2, y, 13, y, "N")
    for y in (7, 12):
        c.r(3, y, 12, y + 2, "n") if False else None
    for y in (8, 12, 16):
        c.r(7, y, 8, y, "y") if y != 16 else c.r(7, 17, 8, 17, "y")
    for y in (7, 12):
        c.r(3, y, 3, y + 2, "4"); c.r(12, y, 12, y + 2, "4")
    c.r(3, 16, 4, 18, "4"); c.r(11, 16, 12, 18, "4")
    c.p(5, 8, "w"); c.p(10, 8, "w")
    c.r(2, 19, 3, 21, "N"); c.r(12, 19, 13, 21, "N")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def nephilim_statue_qas():
    c = C()
    # kneeling halfgod beast on wide haunches; moss in 4-6
    c.r(1, 18, 14, 21, "3"); c.r(1, 18, 14, 18, "2")
    for x in range(1, 15, 3):
        c.p(x, 19, "2"); c.p(x + 1, 20, "2")           # tiled polygons
    c.ell(7.5, 15, 6.5, 3.8, "2"); c.ell(7, 14, 5, 2.6, "1")
    c.r(4, 8, 11, 14, "2"); c.r(4, 8, 5, 14, "1"); c.r(11, 9, 11, 14, "3")
    c.r(5, 3, 10, 8, "2"); c.r(5, 3, 7, 7, "1"); c.r(10, 4, 10, 8, "3")
    c.line(4, 4, 2, 1, "2"); c.line(11, 4, 13, 1, "2"); c.p(2, 1, "1")
    c.r(6, 5, 6, 5, "O"); c.r(9, 5, 9, 5, "O"); c.r(7, 7, 8, 7, "3")
    c.r(1, 13, 3, 16, "2"); c.r(12, 13, 14, 16, "3")
    for (x, y) in ((2, 19), (3, 20), (12, 19), (6, 16), (11, 10), (5, 4), (4, 12), (13, 21), (1, 14)):
        c.p(x, y, "5")
    c.p(7, 17, "4"); c.p(3, 18, "4"); c.p(10, 18, "4")
    c.shadow(1, 14, 22)
    return c.out()


@reg()
def nephilim_statue_ruined():
    c = C()
    c.r(1, 18, 14, 21, "3"); c.r(1, 18, 14, 18, "2")
    c.ell(7.5, 15.5, 6, 3, "2"); c.ell(7, 14.5, 4.5, 2, "1")
    c.r(4, 10, 9, 14, "2"); c.r(4, 10, 5, 14, "1"); c.line(4, 10, 6, 8, "2"); c.r(6, 9, 8, 9, "2")
    c.line(9, 10, 11, 12, "3")
    c.r(11, 18, 14, 19, "3")
    c.r(12, 15, 14, 17, "2"); c.r(13, 14, 13, 14, "3")      # fallen chunks
    c.r(0, 19, 1, 20, "2") if False else None
    c.p(6, 12, "O"); c.p(7, 13, "O"); c.p(6, 14, "O")
    for (x, y) in ((3, 19), (5, 17), (9, 12), (12, 19), (7, 10)):
        c.p(x, y, "5")
    c.shadow(1, 14, 22)
    return c.out()


# =====================================================================
_MAP = str.maketrans({"W": "l", "C": "c", "Y": "y", "o": "h"})
for _n, _g in SPRITES.items():
    SPRITES[_n] = [r.translate(_MAP) for r in _g]

if __name__ == "__main__":
    print(len(SPRITES), "sprites", len(KEYS), "keys")
