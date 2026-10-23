"""Fixtures batch 3: furniture, statues, machines, doors, gates, stairs, murals (60 sprites)."""
from fixtures_keys import BATCH_KEYS

KEYS = BATCH_KEYS[3]
SPRITES = {}
KINDS = {}


class Cv:
    def __init__(s):
        s.g = [["."] * 16 for _ in range(24)]

    def p(s, x, y, ch):
        if 0 <= x < 16 and 0 <= y < 24:
            s.g[y][x] = ch

    def r(s, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.p(x, y, ch)

    def box(s, x0, y0, x1, y1, l="1", m="2", d="3"):
        s.r(x0, y0, x1, y1, m)
        s.r(x0, y0, x1, y0, l)
        s.r(x0, y0, x0, y1, l)
        s.r(x1, y0 + 1, x1, y1, d)
        s.r(x0 + 1, y1, x1, y1, d)

    def ell(s, cx, cy, rx, ry, ch):
        for y in range(24):
            for x in range(16):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1.0:
                    s.p(x, y, ch)

    def line(s, x0, y0, x1, y1, ch):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            s.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), ch)

    def sh(s, x0, x1, y=21):
        for x in range(x0, x1 + 1):
            if s.g[y][x] == ".":
                s.p(x, y, "x")

    def out(s):
        return ["".join(r) for r in s.g]


def reg(name, c, kind=None):
    SPRITES[name] = c.out()
    if kind:
        KINDS[name] = kind


def S(*a):
    return a


# ---------- helpers for walls / doors (terrain) ----------
def wallbase(c, top="1", mid="2", dark="3"):
    c.r(0, 0, 15, 23, mid)
    c.r(0, 0, 15, 3, top)
    c.r(0, 20, 15, 23, dark)


def plank_leaf(c, x0, x1, y0, y1, light="n", dark="N"):
    c.r(x0, y0, x1, y1, light)
    for x in range(x0 + 1, x1, 3):
        c.r(x, y0, x, y1, dark)


# basket
c = Cv()
c.ell(8, 15, 6, 4, "2")
c.r(3, 12, 12, 12, "1")
c.r(3, 12, 12, 13, "1")
c.r(4, 11, 11, 11, "3")
c.r(4, 9, 11, 10, "2"); c.r(5, 9, 10, 9, "3")
for y in (14, 16, 18):
    for x in range(4 + (y // 2) % 2, 13, 2):
        c.p(x, y, "3")
for x in range(3, 13, 2):
    c.p(x, 13, "3")
c.ell(8, 15, 6, 4, "2") if False else None
c.r(5, 7, 5, 11, "5"); c.r(10, 7, 10, 11, "5"); c.r(5, 6, 10, 6, "4"); c.r(6, 7, 9, 7, "5")
c.r(4, 19, 11, 19, "3")
c.sh(3, 12, 21)
reg("basket", c)

# cage
c = Cv()
c.r(3, 17, 12, 18, "3")
c.r(3, 17, 12, 17, "2")
c.r(3, 6, 12, 7, "2"); c.r(3, 6, 12, 6, "1")
for x in (3, 6, 9, 12):
    c.r(x, 8, x, 16, "L")
for x in (4, 7, 10):
    c.r(x, 8, x, 16, "l") if False else None
c.r(4, 8, 5, 16, "O") if False else None
for x in (4, 5, 7, 8, 10, 11):
    c.r(x, 8, x, 16, "O")
for x in (3, 6, 9, 12):
    c.r(x, 8, x, 16, "l")
c.r(7, 3, 8, 5, "2"); c.r(6, 3, 9, 3, "1")
c.p(7, 4, "O"); c.p(8, 4, "O")
c.r(5, 12, 10, 13, "w") if False else None
c.p(8, 13, "4"); c.p(7, 14, "4")
c.sh(2, 13, 20)
reg("cage", c)

# ---- doors (terrain) ----
def frame_door(c, x0=1, x1=14, top=1):
    c.r(0, 0, 15, 23, "3")
    c.r(x0, top, x1, 22, "2")


# deathgate_e
c = Cv()
c.r(0, 0, 15, 23, "3")
c.r(0, 0, 15, 2, "1")
c.r(1, 3, 14, 22, "2")
c.r(1, 3, 14, 3, "1")
c.r(2, 4, 6, 21, "1"); c.r(9, 4, 13, 21, "1")
c.r(7, 3, 8, 22, "3")
for y in range(6, 21, 4):
    c.r(3, y, 5, y + 2, "4"); c.r(10, y, 12, y + 2, "4")
    c.p(4, y + 1, "5"); c.p(11, y + 1, "5")
c.r(2, 4, 2, 21, "2") if False else None
c.r(6, 4, 6, 21, "2"); c.r(9, 4, 9, 21, "2")
c.p(6, 13, "y"); c.p(9, 13, "y")
c.r(0, 22, 15, 23, "3")
reg("deathgate_e", c, "terrain")

# dock_platform_s
c = Cv()
c.r(0, 4, 15, 21, "3")
c.r(1, 5, 14, 20, "6")
for y in range(6, 20, 3):
    c.r(1, y, 14, y, "3")
for x in range(2, 14, 3):
    c.r(x, 5, x, 20, "3")
for x in range(2, 14, 3):
    for y in range(6, 20, 3):
        c.p(x + 1, y + 1, "5")
c.r(0, 4, 15, 5, "2"); c.r(0, 4, 15, 4, "1")
c.r(0, 20, 15, 21, "2"); c.r(0, 21, 15, 21, "3")
for x in (0, 15):
    c.r(x, 4, x, 21, "1" if x == 0 else "3")
for x in (1, 14):
    c.p(x, 5, "4"); c.p(x, 20, "4")
c.r(6, 12, 9, 13, "4"); c.r(7, 12, 8, 13, "5")
reg("dock_platform_s", c)


def double_door(name, side, style):
    """side: 'left' (frame at left edge, seam at right), 'right'."""
    c = Cv()
    c.r(0, 0, 15, 23, "3")
    c.r(0, 0, 15, 1, "1")
    lo, hi = (1, 15) if side == "left" else (0, 14)
    c.r(lo, 2, hi, 22, "2")
    seam = 15 if side == "left" else 0
    hinge = 0 if side == "left" else 15
    fx0, fx1 = (1, 14) if side == "left" else (1, 14)
    if style == "basic":
        for x in range(lo + 1, hi, 3):
            c.r(x, 3, x, 21, "3")
        for y in (6, 17):
            c.r(lo, y, hi, y + 1, "L")
        c.r(lo, 6, hi, 6, "l"); c.r(lo, 17, hi, 17, "l")
        c.r(seam - (1 if side == "left" else -1) * 2 if False else (13 if side == "left" else 2), 12, (14 if side == "left" else 3), 13, "y")
        for x in range(lo, hi, 4):
            c.p(x + 1, 9, "5")
    elif style == "metal":
        c.r(lo, 3, hi, 21, "1")
        c.r(lo, 3, hi, 3, "2") if False else None
        c.r(lo + 1, 4, hi - 1, 20, "2")
        for y in (6, 9, 12, 15, 18):
            c.r(lo + 1, y, hi - 1, y, "3")
        sx = (6, 11) if side == "left" else (4, 9)
        c.r(sx[0], 8, sx[1], 11, "6"); c.r(sx[0] + 1, 9, sx[1] - 1, 10, "4")
    elif style == "window":
        c.r(lo, 3, hi, 21, "n")
        for x in range(lo + 1, hi, 3):
            c.r(x, 3, x, 21, "N")
        wx = (4, 11) if side == "left" else (4, 11)
        c.r(wx[0], 6, wx[1], 13, "O")
        c.r(wx[0] + 1, 7, wx[1] - 1, 12, "b")
        c.r(wx[0] + 1, 7, wx[0] + 2, 8, "w")
        c.p(wx[0] + 4, 11, "B") if False else None
        c.r(wx[0] + 3, 10, wx[0] + 4, 12, "B")
        c.r(lo, 17, hi, 17, "N")
        c.r(13 if side == "left" else 2, 16, 14 if side == "left" else 3, 17, "y")
    elif style == "wavy":
        c.r(lo, 3, hi, 21, "1")
        for y in range(4, 21, 4):
            for x in range(lo, hi + 1):
                c.p(x, y + (1 if (x // 2) % 2 else 0), "5")
                c.p(x, y + 2 + (1 if (x // 2) % 2 else 0), "3") if False else None
        c.r(lo, 3, hi, 3, "4")
        c.r(seam if side == "left" else 0, 3, seam, 21, "4") if False else None
        c.r(14 if side == "left" else 1, 3, 14 if side == "left" else 1, 21, "4")
        c.r(13 if side == "left" else 2, 11, 13 if side == "left" else 2, 14, "L")
    # hinge side post and seam
    c.r(hinge, 2, hinge, 23, "3")
    c.r(seam, 2, seam, 23, "6" if style != "window" else "N") if False else None
    c.r(0, 22, 15, 23, "3")
    reg(name, c, "terrain")


double_door("door2_basic_right", "right", "basic")
double_door("door2_metal_left", "left", "metal")
double_door("door2_wavy_right", "right", "wavy")
double_door("door2_window_left", "left", "window")


def vdouble(name, top):
    c = Cv()
    c.r(0, 0, 15, 23, "3")
    c.r(0, 0, 15, 23, "3")
    if top:
        c.r(0, 0, 15, 2, "1")
        c.r(1, 3, 14, 23, "2")
    else:
        c.r(1, 0, 14, 20, "2")
        c.r(0, 21, 15, 23, "3")
    ys = range(4, 24, 5) if top else range(0, 19, 5)
    for x0 in (2, 9):
        pass
    # panels: vertical stripes (K) with warning bars (y)
    for x in range(2, 14):
        for y in range(3 if top else 0, 23 if top else 20):
            if (x + y) % 4 < 2:
                c.p(x, y, "6")
    # crossbar near the seam
    yb = 19 if top else 3
    c.r(1, yb, 14, yb + 1, "L"); c.r(1, yb, 14, yb, "l")
    for x in (3, 12):
        c.p(x, yb + 1, "y")
    c.r(0, 23 if top else 0, 15, 23 if top else 0, "3")
    reg(name, c, "terrain")


vdouble("door2_striped_top", True)
vdouble("door2_striped_bottom", False)

# door_metal / door_window
c = Cv()
c.r(0, 0, 15, 23, "3"); c.r(0, 0, 15, 1, "1")
c.r(2, 2, 13, 22, "1"); c.r(3, 3, 12, 21, "2")
for y in (6, 10, 14, 18):
    c.r(3, y, 12, y, "3")
c.r(5, 7, 10, 9, "6"); c.r(6, 8, 9, 8, "4")
c.r(11, 13, 11, 14, "y")
c.r(0, 22, 15, 23, "3")
reg("door_metal", c, "terrain")

c = Cv()
c.r(0, 0, 15, 23, "3"); c.r(0, 0, 15, 1, "1")
c.r(2, 2, 13, 22, "n")
for x in range(3, 13, 3):
    c.r(x, 3, x, 21, "N")
c.r(4, 5, 11, 12, "O"); c.r(5, 6, 10, 11, "b"); c.r(5, 6, 6, 7, "w"); c.r(8, 9, 9, 10, "B")
c.r(2, 16, 13, 16, "N")
c.r(11, 14, 11, 15, "y")
c.r(0, 22, 15, 23, "3")
reg("door_window", c, "terrain")

# eater_bell
c = Cv()
c.r(2, 3, 13, 4, "3"); c.r(2, 3, 13, 3, "1")
c.r(2, 3, 3, 20, "2"); c.r(12, 3, 13, 20, "2"); c.r(2, 3, 2, 20, "1"); c.r(13, 4, 13, 20, "3")
c.r(7, 5, 8, 6, "5")
c.r(6, 7, 9, 8, "1")
c.r(5, 9, 10, 11, "1"); c.r(5, 9, 6, 11, "w") if False else None
c.r(4, 12, 11, 14, "1"); c.r(10, 9, 11, 14, "2") if False else None
c.r(9, 9, 10, 14, "2"); c.r(11, 12, 11, 14, "3")
c.r(3, 15, 12, 15, "2"); c.r(3, 15, 12, 15, "3") if False else None
c.p(5, 10, "w"); c.p(5, 12, "w")
c.r(7, 16, 8, 17, "4")
c.r(2, 20, 13, 20, "3")
c.sh(2, 13, 21)
reg("eater_bell", c)

# eater_couch_c
c = Cv()
c.r(2, 7, 13, 16, "2")
c.r(3, 6, 12, 6, "1"); c.r(2, 7, 13, 8, "1")
c.r(2, 8, 2, 16, "1")
c.r(4, 9, 11, 11, "2"); c.r(4, 9, 11, 9, "3")
c.r(1, 11, 3, 17, "1"); c.r(12, 11, 14, 17, "1"); c.r(14, 12, 14, 17, "3"); c.r(12, 11, 14, 11, "w") if False else None
c.r(3, 12, 12, 16, "w"); c.r(3, 12, 12, 12, "l"); c.r(3, 16, 12, 16, "l")
c.r(5, 13, 10, 15, "l") if False else None
c.p(7, 14, "4"); c.p(8, 14, "4")
c.r(2, 17, 13, 18, "3")
c.r(3, 19, 4, 19, "N"); c.r(11, 19, 12, 19, "N")
c.sh(1, 14, 20)
reg("eater_couch_c", c)

# eater_diagonal_monument
c = Cv()
c.r(2, 18, 13, 19, "3"); c.r(2, 18, 13, 18, "2")
for i in range(0, 13):
    x0 = 8 - (i // 2) - 1 if False else 2 + 0
c.line(8, 3, 3, 17, "1"); c.line(8, 3, 13, 17, "3")
for y in range(4, 18):
    xl = 8 - round((y - 3) * 5 / 14)
    xr = 8 + round((y - 3) * 5 / 14)
    c.r(xl, y, xr, y, "2")
    c.p(xl, y, "1"); c.p(xr, y, "3")
c.line(5, 13, 11, 13, "3"); c.line(6, 10, 10, 10, "3")
c.line(8, 5, 8, 17, "3") if False else None
c.p(8, 7, "w"); c.p(8, 12, "4"); c.p(6, 15, "4"); c.p(10, 15, "4")
c.r(7, 1, 8, 2, "4")
c.sh(2, 13, 21)
reg("eater_diagonal_monument", c)

# eater_monument (megalith)
c = Cv()
c.r(5, 3, 11, 19, "2")
c.r(6, 2, 10, 2, "1"); c.r(5, 3, 6, 19, "1"); c.r(11, 4, 11, 19, "3"); c.r(10, 4, 10, 19, "3")
c.r(4, 17, 12, 20, "2"); c.r(4, 17, 12, 17, "1"); c.r(4, 20, 12, 20, "3")
for y in (6, 10, 14):
    c.r(7, y, 9, y, "4"); c.p(8, y + 1, "5")
c.p(7, 4, "w")
c.sh(3, 13, 21)
reg("eater_monument", c)

# eater_sign_shard
c = Cv()
c.r(7, 15, 8, 20, "3"); c.r(7, 15, 7, 20, "2")
c.r(2, 5, 13, 14, "3")
c.r(3, 6, 12, 13, "2"); c.r(3, 6, 12, 6, "1")
c.r(3, 6, 3, 13, "1")
c.p(5, 8, "4"); c.p(8, 7, "4"); c.p(11, 9, "4"); c.p(6, 11, "4"); c.p(10, 12, "4"); c.p(9, 10, "w"); c.p(4, 12, "w")
c.line(5, 9, 10, 9, "5") if False else None
c.sh(5, 10, 21)
reg("eater_sign_shard", c)

# fan
c = Cv()
c.ell(8, 11, 7.5, 7.5, "3")
c.ell(8, 11, 6, 6, "5")
c.ell(8, 11, 5, 5, "6")
c.r(1, 5, 4, 6, "2") if False else None
c.line(8, 11, 8, 6, "4"); c.line(8, 11, 13, 9, "4"); c.line(8, 11, 12, 15, "4"); c.line(8, 11, 4, 15, "4"); c.line(8, 11, 3, 8, "4")
c.line(9, 11, 9, 6, "5") if False else None
c.ell(8, 11, 1.5, 1.5, "L")
c.p(8, 11, "l")
c.line(2, 6, 5, 3, "1"); c.line(4, 4, 11, 4, "1")
c.r(4, 18, 11, 19, "2"); c.r(4, 18, 11, 18, "1")
c.sh(3, 12, 20)
reg("fan", c)


def clock(name, ne):
    c = Cv()
    c.r(0, 0, 15, 23, "2")
    # quarter circle centred on bottom-left (ne) or top-left (se)
    cy = 23 if ne else 0
    for y in range(24):
        for x in range(16):
            d = ((x + 0.5) ** 2 + (y + 0.5 - (cy + 0.5)) ** 2) ** 0.5
            if d <= 21:
                c.p(x, y, "1")
            if 21 > d > 19 or (d <= 21 and d > 17.5 and False):
                c.p(x, y, "3")
            if 15.5 < d <= 16.5 or 10.5 < d <= 11.5:
                c.p(x, y, "l")
    for x in range(16):
        for y in range(24):
            if x == 0 or (y == 0 if not ne else y == 23):
                pass
    # numerals ticks
    for ang in range(0, 90, 18):
        import math
        a = math.radians(ang)
        for rr in (13, 14):
            x = int(rr * math.cos(a)); y = int(rr * math.sin(a))
            c.p(x, (cy - y) if ne else (cy + y), "y")
    c.r(0, 0, 15, 0, "3") if ne else c.r(0, 23, 15, 23, "3")
    reg(name, c, "terrain")


clock("floor_clock_ne", True)
clock("floor_clock_se", False)

# gate_glass_e_closed (vertical sliding glass seen from side)
c = Cv()
c.r(5, 0, 10, 23, "3")
c.r(6, 0, 9, 23, "2")
c.r(7, 1, 8, 22, "c") if False else None
c.r(6, 1, 9, 22, "B") if False else None
c.r(6, 1, 9, 22, "c")
c.r(6, 1, 6, 22, "w")
c.r(9, 1, 9, 22, "b")
for y in (1, 12, 22):
    c.r(5, y, 10, y, "1")
c.r(2, 0, 3, 23, "3") if False else None
c.r(0, 11, 15, 12, "3") if False else None
c.r(0, 0, 4, 1, "3") if False else None
c.p(7, 4, "w"); c.p(7, 5, "w"); c.p(8, 16, "w")
c.r(5, 11, 10, 13, "1") if False else None
reg("gate_glass_e_closed", c, "terrain")

# golem_interior_chair
c = Cv()
c.r(4, 3, 11, 14, "1"); c.r(4, 3, 11, 3, "w") if False else None
c.r(5, 4, 10, 13, "4"); c.r(5, 4, 10, 4, "w") if False else None
c.r(4, 3, 4, 14, "1"); c.r(11, 3, 11, 14, "3")
c.r(5, 9, 10, 15, "4") if False else None
c.r(3, 14, 12, 17, "4"); c.r(3, 14, 12, 14, "w") if False else None
c.r(3, 17, 12, 17, "6")
c.r(1, 10, 3, 17, "2"); c.r(12, 10, 14, 17, "2"); c.r(1, 10, 3, 10, "1"); c.r(12, 10, 14, 10, "1")
c.p(2, 12, "r"); c.p(13, 12, "c"); c.p(2, 14, "c"); c.p(13, 14, "y")
c.r(6, 18, 9, 19, "L"); c.r(5, 19, 10, 20, "3")
c.sh(3, 12, 21)
reg("golem_interior_chair", c)

# golem_interior_screen_n
c = Cv()
c.r(1, 3, 14, 18, "3")
c.r(2, 4, 13, 17, "O")
c.r(3, 5, 12, 16, "6")
c.ell(5, 10, 1.5, 1.5, "4"); c.ell(10, 10, 2.5, 2.5, "4")
c.p(5, 10, "w"); c.p(10, 10, "w")
for x in range(3, 13, 2):
    c.p(x, 6, "5")
c.line(3, 15, 12, 15, "5") if False else None
c.r(1, 3, 14, 3, "1"); c.r(1, 3, 1, 18, "1")
c.r(0, 19, 15, 21, "2"); c.r(0, 19, 15, 19, "1")
for x in (2, 5, 8, 11):
    c.p(x, 20, "4")
c.sh(0, 15, 22)
reg("golem_interior_screen_n", c)


def shrine(name, face_e):
    c = Cv()
    c.r(1, 15, 14, 19, "3"); c.r(1, 15, 14, 16, "1"); c.r(1, 17, 14, 18, "2")
    for i, x in enumerate((2, 9)):
        # kneeling marble eater
        c.r(x, 8, x + 3, 14, "w")
        c.r(x + 3, 9, x + 3, 14, "l")
        c.ell(x + 1.5, 6, 2, 2, "w")
        c.p(x + 1, 6, "O")
        c.r(x, 13, x + 4, 14, "l")
    if face_e:
        c.r(6, 8, 7, 14, "5"); c.r(5, 5, 7, 8, "4") if False else None
        c.r(12, 4, 14, 14, "6"); c.r(12, 4, 12, 14, "4"); c.p(13, 6, "5")
    else:
        c.r(6, 9, 8, 13, "6"); c.r(6, 9, 8, 9, "4")
        c.p(7, 11, "5")
        c.r(12, 8, 13, 14, "2") if False else None
    c.p(2, 16, "4"); c.p(5, 16, "4"); c.p(9, 16, "4"); c.p(12, 16, "4")
    c.sh(0, 15, 20)
    reg(name, c)


shrine("great_machine_shrine_e", True)
shrine("great_machine_shrine_s", False)

# hologram_circle
c = Cv()
c.ell(8, 16, 7, 3.5, "3"); c.ell(8, 16, 6, 2.5, "2"); c.ell(8, 16, 4, 1.5, "1")
for x, y in ((3, 8), (6, 5), (9, 10), (12, 7), (8, 13), (5, 12), (11, 13), (7, 8)):
    c.p(x, y, "w")
c.p(6, 6, "1"); c.p(10, 8, "1"); c.p(4, 10, "1"); c.p(12, 11, "1")
c.line(6, 5, 9, 10, "1") if False else None
c.r(8, 14, 8, 14, "w")
c.sh(2, 13, 20)
reg("hologram_circle", c)

# left_spindle_ribbon
c = Cv()
for y in range(24):
    w = 1 + (23 - y) // 7 if False else 2
    x0 = 7
    c.r(7, y, 8, y, "1" if y % 2 else "2")
c.r(7, 0, 7, 23, "1"); c.r(8, 0, 8, 23, "3")
for y in range(1, 23, 4):
    c.p(6, y, "4"); c.p(9, y + 2, "4")
c.r(5, 20, 10, 22, "2"); c.r(5, 20, 10, 20, "1"); c.r(5, 22, 10, 22, "3")
reg("left_spindle_ribbon", c)

# left_spindle_support_top
c = Cv()
c.r(0, 4, 15, 7, "2"); c.r(0, 4, 15, 4, "1"); c.r(0, 7, 15, 7, "3")
c.r(10, 7, 12, 14, "2"); c.r(10, 7, 10, 14, "1"); c.r(12, 8, 12, 14, "3")
c.r(8, 14, 14, 17, "5"); c.r(8, 14, 14, 14, "4"); c.r(8, 17, 14, 17, "6")
c.p(9, 5, "w"); c.p(3, 5, "w"); c.p(11, 15, "w")
c.r(0, 8, 8, 8, "3") if False else None
c.sh(8, 14, 18)
reg("left_spindle_support_top", c)

# right_spindle_support
c = Cv()
c.r(0, 6, 15, 9, "2"); c.r(0, 6, 15, 6, "1"); c.r(0, 9, 15, 9, "3")
c.r(3, 9, 5, 16, "2"); c.r(3, 9, 3, 16, "1"); c.r(5, 10, 5, 16, "3")
c.r(1, 16, 7, 19, "5"); c.r(1, 16, 7, 16, "4"); c.r(1, 19, 7, 19, "6")
c.p(12, 7, "w"); c.p(6, 7, "w"); c.p(4, 17, "w")
c.sh(1, 7, 20)
reg("right_spindle_support", c)

# monument orb
c = Cv()
c.r(4, 17, 11, 20, "3"); c.r(4, 17, 11, 18, "2"); c.r(4, 17, 11, 17, "1")
c.r(6, 16, 9, 16, "3")
c.ell(8, 10, 5.5, 5.5, "2")
c.ell(7, 9, 4, 4, "1")
c.ell(10, 12, 2.5, 2.5, "3") if False else None
for y in range(24):
    for x in range(16):
        if c.g[y][x] == "2" and x + y > 19:
            c.p(x, y, "3")
c.r(2, 10, 13, 10, "5") if False else None
c.line(3, 10, 12, 10, "5")
c.line(8, 5, 8, 15, "5")
c.p(5, 7, "w"); c.p(6, 6, "w")
c.sh(3, 12, 21)
reg("monument", c)

# murals (terrain wall pieces)
def mural_base(c, left=True):
    c.r(0, 0, 15, 23, "2")
    c.r(0, 0, 15, 3, "1")
    c.r(0, 20, 15, 23, "3")
    c.r(0 if left else 15, 0, 0 if left else 15, 23, "3" if not left else "1")


c = Cv(); mural_base(c)
c.r(2, 6, 13, 18, "3"); c.r(3, 7, 12, 17, "2")
c.ell(8, 12, 3, 3, "w"); c.ell(8, 12, 1.5, 1.5, "4")
c.line(3, 8, 6, 10, "w"); c.line(13, 8, 10, 10, "w"); c.line(3, 16, 6, 14, "w"); c.line(12, 16, 10, 14, "w")
reg("mural_appeasesbaetyl_l", c, "terrain")

c = Cv(); mural_base(c)
c.r(3, 6, 12, 17, "3"); c.r(4, 7, 11, 16, "2") if False else None
c.r(4, 7, 11, 16, "1")
c.r(5, 9, 6, 14, "6"); c.r(9, 8, 10, 10, "6")
c.p(5, 12, "4"); c.p(10, 14, "5")
c.r(0, 4, 1, 19, "3") if False else None
c.r(0, 0, 1, 23, "3"); c.r(0, 0, 1, 3, "1")
c.r(13, 15, 14, 16, "4")
c.p(1, 8, "2") if False else None
reg("mural_leftend_period", c, "terrain")

c = Cv(); mural_base(c)
c.r(2, 6, 13, 18, "3"); c.r(3, 7, 12, 17, "2")
c.line(4, 8, 7, 11, "w"); c.line(7, 11, 5, 15, "w"); c.line(11, 9, 9, 13, "w")
for x, y in ((3, 7), (12, 7), (3, 17), (12, 17), (8, 16), (10, 11)):
    c.p(x, y, "3")
c.r(4, 16, 5, 17, "1") if False else None
c.p(9, 15, "3"); c.p(6, 8, "1")
c.r(11, 15, 12, 17, "1")
c.p(0, 10, "1") if False else None
c.r(8, 17, 9, 17, "1")
c.line(0, 19, 3, 15, "1") if False else None
reg("mural_ruined4_l", c, "terrain")

# nephilim statues
def plinth(c):
    c.r(2, 18, 13, 20, "3"); c.r(2, 18, 13, 18, "2"); c.r(2, 19, 13, 19, "1") if False else None
    c.r(2, 18, 2, 20, "2")
    c.p(3, 19, "g"); c.p(7, 19, "g"); c.p(11, 19, "g"); c.p(5, 18, "g"); c.p(10, 18, "g")


c = Cv(); plinth(c)
c.ell(8, 11, 6, 5.5, "2"); c.ell(7, 10, 4.5, 4, "1")
c.r(3, 15, 4, 17, "2"); c.r(11, 15, 12, 17, "3"); c.p(4, 17, "g"); c.p(11, 17, "g")
c.p(5, 9, "O"); c.p(6, 9, "O"); c.p(10, 9, "O"); c.p(9, 9, "O")
c.r(6, 13, 10, 13, "O"); c.p(6, 14, "w"); c.p(8, 14, "w"); c.p(10, 14, "w")
for x, y in ((4, 6), (8, 5), (11, 7), (12, 11), (3, 11)):
    c.p(x, y, "g"); c.p(x + 1 if x < 11 else x - 1, y, "G") if False else None
c.p(8, 6, "6"); c.p(5, 7, "6"); c.p(11, 8, "6")
c.sh(2, 13, 21)
reg("nephilim_statue_agolgot", c)

c = Cv(); plinth(c)
# swan: neck and head, body with fanned train
c.ell(6, 15, 4, 3, "1"); c.r(3, 13, 8, 14, "1")
c.ell(11, 12, 3, 4, "2"); c.r(12, 8, 13, 16, "3")
c.line(5, 13, 4, 10, "1"); c.line(4, 10, 6, 6, "1"); c.line(5, 13, 5, 10, "1")
c.r(4, 8, 6, 10, "1"); c.ell(6, 5, 2, 2, "1"); c.r(3, 4, 3, 5, "2")
c.p(6, 5, "O")
c.line(11, 8, 11, 15, "3"); c.line(9, 10, 13, 10, "3")
c.p(2, 17, "g"); c.p(12, 17, "g"); c.p(7, 17, "g")
c.sh(2, 13, 21)
reg("nephilim_statue_qon", c)

c = Cv(); plinth(c)
# coiled worm with spines
for i, (x, y) in enumerate([(3, 15), (5, 12), (8, 10), (11, 11), (12, 14), (10, 16), (7, 16)]):
    c.ell(x, y, 2.2, 2.2, "2")
    c.p(x - 1, y - 1, "1")
c.ell(5, 7, 2.5, 2.5, "1"); c.ell(5, 7, 2.5, 2.5, "1")
c.p(4, 6, "O"); c.p(6, 6, "O"); c.p(5, 8, "O"); c.p(3, 7, "6"); c.p(7, 7, "6")
for x, y in ((2, 4), (6, 3), (9, 8), (13, 9), (12, 17), (4, 12)):
    c.p(x, y, "1")
c.p(10, 12, "3"); c.p(11, 14, "3"); c.p(8, 15, "3")
c.p(13, 13, "g"); c.p(2, 14, "g"); c.p(9, 17, "g")
c.sh(2, 13, 21)
reg("nephilim_statue_shugruith", c)

# orchid_gate_s
c = Cv()
c.r(0, 0, 15, 23, "2")
c.r(0, 0, 15, 2, "1")
c.r(0, 2, 2, 23, "1"); c.r(13, 2, 15, 23, "3")
c.r(3, 3, 12, 20, "3")
c.r(4, 4, 11, 19, "O")
c.line(4, 8, 8, 4, "o") if False else None
c.r(4, 4, 11, 19, "6")
c.r(6, 12, 9, 19, "4"); c.r(7, 12, 8, 19, "w")
c.ell(8, 8, 2, 2, "4")
c.p(5, 16, "g"); c.p(10, 17, "g"); c.p(5, 15, "w") if False else None
c.r(3, 20, 12, 20, "1")
c.r(0, 21, 15, 23, "3")
for x in (3, 5, 7, 9, 11):
    c.p(x, 21, "2")
reg("orchid_gate_s", c, "terrain")

# orchid_projector
c = Cv()
c.r(5, 15, 10, 19, "3"); c.r(5, 15, 10, 16, "2"); c.r(5, 15, 10, 15, "1")
c.r(7, 11, 8, 14, "3")
c.ell(8, 9, 6.5, 2.5, "3"); c.ell(8, 8, 5.5, 2, "2"); c.ell(8, 8, 4, 1.2, "1")
c.p(5, 8, "5"); c.p(11, 8, "5"); c.p(8, 9, "6")
c.p(4, 10, "w"); c.p(12, 7, "w")
c.p(9, 7, "w")
c.r(4, 19, 11, 19, "3")
c.sh(3, 12, 20)
reg("orchid_projector", c)

# reshaping_pad
c = Cv()
c.r(1, 6, 14, 21, "3")
c.r(2, 7, 13, 20, "2"); c.r(1, 6, 14, 6, "1"); c.r(1, 6, 1, 21, "1")
c.r(3, 9, 12, 18, "5"); c.r(3, 9, 12, 9, "4")
c.r(4, 10, 11, 17, "6") if False else None
c.ell(8, 13, 3.5, 3, "6")
c.p(8, 12, "4"); c.p(7, 13, "4"); c.p(9, 13, "4"); c.p(8, 14, "4"); c.p(8, 13, "w")
for x in (4, 7, 10):
    c.r(x, 2, x + 1, 4, "4") if False else None
c.r(2, 2, 13, 3, "2") if False else None
c.p(2, 3, "4"); c.p(5, 3, "4"); c.p(10, 3, "4"); c.p(13, 3, "4")
c.r(2, 2, 13, 2, "5")
c.sh(0, 15, 22)
reg("reshaping_pad", c)

# sheva_mover (palanquin on magnetic legs)
c = Cv()
c.r(2, 2, 13, 4, "y"); c.r(3, 1, 12, 1, "y"); c.r(2, 2, 13, 2, "Y") if False else None
c.r(4, 0, 11, 0, "y") if False else None
c.r(2, 4, 13, 4, "3")
c.r(3, 5, 12, 12, "1"); c.r(3, 5, 3, 12, "w"); c.r(12, 6, 12, 12, "3")
c.r(5, 6, 10, 10, "3"); c.r(6, 7, 9, 9, "O") if False else None
c.r(5, 6, 10, 10, "2"); c.r(6, 7, 9, 9, "4")
c.p(7, 8, "w")
c.r(2, 13, 13, 14, "2"); c.r(2, 13, 13, 13, "1")
for x in (2, 5, 9, 12):
    c.r(x, 15, x + 1, 19, "2"); c.p(x, 15, "1"); c.p(x + 1, 19, "3")
c.p(1, 13, "g"); c.p(3, 5, "g"); c.p(12, 7, "r"); c.p(13, 16, "G")
c.p(1, 16, "G"); c.p(1, 14, "g")
c.p(7, 3, "w"); c.p(4, 3, "w")
c.sh(1, 14, 20)
reg("sheva_mover", c)

# stairsdown: open air (terrain)
c = Cv()
c.r(0, 0, 15, 23, "3")
c.r(1, 1, 14, 22, "5")
for k in range(4):
    c.r(1 + k, 1 + k * 5, 14 - k, 5 + k * 5 - 1 + 0, "5" if k % 2 else "6")
    c.r(1 + k, 5 + k * 5, 14 - k, 5 + k * 5, "4")
c.r(6, 12, 9, 14, "O")
c.p(7, 13, "w")
reg("stairsdown", c, "terrain")

# star_carousel_display_case
c = Cv()
c.r(1, 3, 14, 20, "3")
c.r(2, 4, 13, 19, "2")
c.r(1, 3, 14, 3, "1"); c.r(1, 3, 1, 20, "1")
c.r(3, 5, 12, 18, "O")
c.r(3, 9, 12, 9, "l"); c.r(3, 13, 12, 13, "l"); c.r(7, 5, 7, 18, "l")
c.r(3, 5, 6, 8, "6") if False else None
for x, y, ch in ((4, 7, "4"), (5, 6, "r"), (9, 7, "y"), (10, 8, "b"), (4, 11, "g"), (5, 12, "m"), (9, 11, "c"), (11, 12, "4"), (4, 16, "y"), (5, 15, "b"), (9, 16, "r"), (10, 15, "w")):
    c.p(x, y, ch)
c.p(8, 7, "y"); c.p(11, 17, "c")
c.sh(0, 15, 21)
reg("star_carousel_display_case", c)


def seat(name, tall):
    c = Cv()
    c.r(4, 4 if tall else 6, 11, 13, "2")
    c.r(4, 4 if tall else 6, 11, 4 if tall else 6, "1"); c.r(4, 4 if tall else 6, 4, 13, "1"); c.r(11, 7, 11, 13, "3")
    c.r(5, 6 if tall else 8, 10, 12, "1") if False else None
    c.r(3, 13, 12, 16, "1"); c.r(3, 13, 12, 13, "w") if False else None
    c.r(3, 16, 12, 16, "3"); c.r(12, 14, 12, 16, "3")
    if tall:
        c.r(6, 2, 9, 3, "5"); c.r(6, 2, 9, 2, "4")
    c.r(1, 10, 2, 15, "5"); c.r(13, 10, 14, 15, "5"); c.r(1, 10, 2, 10, "4"); c.r(13, 10, 14, 10, "4")
    c.p(2, 12, "r") if tall else None
    c.p(13, 12, "c")
    c.r(6, 17, 9, 17, "L"); c.r(4, 18, 11, 19, "5"); c.r(4, 18, 11, 18, "4"); c.r(4, 19, 11, 19, "6")
    c.sh(3, 12, 20)
    reg(name, c)


seat("star_carousel_passenger_seat", False)
seat("star_carousel_pilot_seat", True)

# star chart
c = Cv()
c.r(0, 3, 15, 16, "3")
c.r(1, 4, 14, 15, "O")
c.r(1, 4, 14, 4, "l")
stars = [(3, 6), (6, 9), (9, 6), (12, 8), (5, 13), (10, 12), (13, 13), (2, 10), (8, 11)]
for x, y in stars:
    c.p(x, y, "w")
c.line(3, 6, 6, 9, "c"); c.line(6, 9, 9, 6, "c"); c.line(9, 6, 12, 8, "c"); c.line(6, 9, 5, 13, "b"); c.line(8, 11, 10, 12, "b"); c.line(10, 12, 13, 13, "b")
for x, y in stars:
    c.p(x, y, "w")
c.p(9, 6, "y"); c.p(5, 13, "y")
c.r(5, 17, 10, 19, "2"); c.r(5, 17, 10, 17, "1")
c.sh(4, 11, 20)
reg("star_carousel_star_chart_l", c)

# star_orchid_monument (terrain wall)
c = Cv()
c.r(0, 0, 15, 23, "2")
c.r(0, 0, 15, 3, "1"); c.r(0, 20, 15, 23, "3")
c.r(2, 5, 13, 18, "3"); c.r(3, 6, 12, 17, "2")
c.ell(8, 11, 3.5, 4.5, "5"); c.ell(8, 11, 2, 3, "6")
c.p(7, 9, "4"); c.p(8, 8, "4")
c.r(5, 5, 5, 17, "1"); c.r(10, 6, 10, 17, "3") if False else None
c.p(3, 6, "y"); c.p(12, 6, "y"); c.p(3, 17, "y"); c.p(12, 17, "y")
reg("star_orchid_monument", c, "terrain")

# starship_1_passenger_seat
c = Cv()
c.r(4, 5, 11, 12, "2"); c.r(4, 5, 11, 5, "1"); c.r(4, 5, 4, 12, "1"); c.r(11, 6, 11, 12, "3")
c.r(3, 12, 12, 16, "2"); c.r(3, 12, 12, 12, "1"); c.r(3, 16, 12, 16, "3")
c.p(6, 8, "3"); c.p(8, 10, "3"); c.p(9, 7, "3")
c.r(2, 10, 3, 15, "4") if False else None
c.r(1, 11, 2, 15, "6"); c.r(13, 11, 14, 15, "6")
c.r(5, 17, 10, 19, "4"); c.r(5, 17, 10, 17, "w"); c.r(5, 19, 10, 19, "6") if False else None
c.r(3, 19, 12, 19, "l")
c.sh(2, 13, 20)
reg("starship_1_passenger_seat", c)

# power core hedron
c = Cv()
c.r(3, 17, 12, 20, "3"); c.r(3, 17, 12, 18, "2"); c.r(3, 17, 12, 17, "1")
c.line(8, 3, 3, 9, "1"); c.line(8, 3, 13, 9, "2"); c.line(3, 9, 8, 16, "1"); c.line(13, 9, 8, 16, "3")
c.line(3, 9, 13, 9, "1")
for y in range(4, 16):
    for x in range(16):
        pass
c.r(5, 9, 11, 10, "5") if False else None
for y in range(4, 16):
    xs = [x for x in range(16) if c.g[y][x] != "."]
c.ell(8, 10, 3, 3, "6"); c.ell(8, 10, 2, 2, "5"); c.p(8, 10, "4"); c.p(7, 9, "w")
c.line(8, 3, 8, 16, "3") if False else None
c.p(8, 4, "w")
c.sh(2, 13, 21)
reg("starship_1_power_core", c)

# crate / viewer
c = Cv()
c.r(2, 7, 13, 19, "2")
c.r(2, 7, 13, 9, "1"); c.r(2, 7, 2, 19, "1")
c.r(13, 8, 13, 19, "3"); c.r(2, 19, 13, 19, "3")
c.r(2, 13, 13, 13, "3")
c.r(2, 7, 13, 7, "w") if False else None
for x, y in ((4, 11), (11, 11), (4, 17), (11, 17)):
    c.p(x, y, "l")
c.r(6, 14, 9, 17, "l"); c.r(7, 15, 8, 16, "w")
c.line(3, 8, 12, 8, "3") if False else None
c.sh(1, 14, 20)
reg("starship_1_viewer", c)

# wall bookshelf (terrain, e)
c = Cv()
c.r(0, 0, 15, 23, "3")
c.r(0, 0, 15, 2, "1")
c.r(2, 3, 14, 21, "2")
cols = "r b y g m c 4 5".split()
for ys in (4, 10, 16):
    c.r(2, ys + 5, 14, ys + 5, "3") if False else None
    c.r(2, ys + 5, 14, ys + 5, "N")
    x = 3
    k = ys
    while x < 14:
        w = 1 + (x + k) % 2
        h = 4 - ((x * 3 + k) % 3)
        ch = "rbygmc"[(x + k) % 6]
        c.r(x, ys + 5 - h, min(x + w - 1, 13), ys + 4, ch)
        x += w
c.r(0, 3, 1, 22, "3")
c.r(0, 22, 15, 23, "3")
c.r(3, 22, 12, 22, "4")
reg("starship_1_wallbookshelf_e", c, "terrain")

# wooden chair
c = Cv()
c.r(4, 5, 11, 13, "n"); c.r(4, 5, 11, 5, "t"); c.r(4, 5, 4, 13, "t")
for x in (6, 9):
    c.r(x, 6, x, 12, "N")
c.r(11, 6, 11, 13, "N")
c.r(3, 13, 12, 16, "n"); c.r(3, 13, 12, 13, "t"); c.r(3, 16, 12, 16, "N")
c.r(3, 17, 4, 19, "N"); c.r(11, 17, 12, 19, "N"); c.r(3, 17, 3, 19, "n"); c.r(11, 17, 11, 19, "n")
c.r(5, 14, 10, 15, "y") if False else None
c.p(7, 14, "y"); c.p(8, 14, "y")
c.sh(2, 13, 20)
reg("starship_wooden_chair", c)

# sunken room stairs
def sunk(name, d):
    c = Cv()
    c.r(0, 0, 15, 23, "3")
    if d == "n":
        for i in range(4):
            y0 = i * 6
            c.r(0, y0, 15, y0 + 3, "l" if i % 2 else "w")
            c.r(0, y0 + 4, 15, y0 + 5, "3")
            c.r(0, y0, 15, y0, "w")
    elif d == "s":
        for i in range(4):
            y0 = i * 6
            c.r(0, y0 + 2, 15, y0 + 5, "w" if i % 2 else "l")
            c.r(0, y0, 15, y0 + 1, "3")
            c.r(0, y0 + 2, 15, y0 + 2, "w")
    else:
        for i in range(4):
            x0 = i * 4
            c.r(x0, 0, x0 + 2, 23, "w" if i % 2 else "l")
            c.r(x0 + 3, 0, x0 + 3, 23, "3")
            c.r(x0, 0, x0, 23, "w")
    for x, y in ((3, 3), (11, 9), (6, 15), (12, 20), (2, 21)):
        c.p(x, y, "K") if False else c.p(x, y, "S") if False else None
    reg(name, c, "terrain")


sunk("sunken_room_stairs_n", "n")
sunk("sunken_room_stairs_s", "s")
sunk("sunken_room_stairs_w", "w")

# tile_1 charred wood
c = Cv()
c.r(0, 0, 15, 23, "3")
for x in range(0, 16, 4):
    c.r(x, 0, x, 23, "O")
for y, x in ((3, 1), (9, 6), (15, 2), (20, 10), (6, 11), (12, 13)):
    c.r(x, y, x + 1, y + 2, "2")
    c.p(x, y, "4")
c.p(5, 14, "4"); c.p(9, 5, "5"); c.p(14, 18, "5"); c.p(3, 21, "5")
c.r(3, 5, 3, 7, "2"); c.r(7, 17, 7, 19, "2")
reg("tile_1", c, "terrain")

# tile_water
c = Cv()
c.r(0, 0, 15, 23, "2")
for y in range(0, 24, 5):
    for x in range(16):
        c.p(x, y + (1 if (x // 3) % 2 else 0), "1")
        c.p(x, y + 3 - (1 if (x // 3) % 2 else 0), "3")
for x, y in ((3, 2), (10, 8), (6, 14), (13, 19), (2, 21)):
    c.p(x, y, "w")
reg("tile_water", c, "terrain")

# vase
c = Cv()
c.r(6, 5, 9, 6, "2"); c.r(5, 4, 10, 4, "1")
c.r(7, 7, 8, 8, "2")
c.ell(8, 13, 4, 5, "2"); c.ell(7, 12, 2.5, 3.5, "1")
for y in range(24):
    for x in range(16):
        if c.g[y][x] == "2" and x + y > 21 and y > 9:
            c.p(x, y, "3")
c.r(3, 9, 3, 12, "5"); c.r(12, 9, 12, 12, "5"); c.p(4, 8, "5"); c.p(11, 8, "5"); c.p(3, 13, "5"); c.p(12, 13, "5")
c.r(5, 12, 10, 13, "4") if False else None
c.line(5, 13, 10, 13, "5")
c.p(6, 11, "w"); c.p(6, 10, "w")
c.r(6, 18, 9, 18, "3")
c.sh(4, 11, 20)
reg("vase", c)

# wall_sharp_geometry
c = Cv()
c.r(0, 0, 15, 23, "2")
c.r(0, 0, 15, 3, "1"); c.r(0, 20, 15, 23, "3")
c.r(0, 11, 15, 12, "3")
c.r(0, 12, 15, 12, "6") if False else None
c.line(0, 10, 7, 5, "1"); c.line(15, 10, 8, 5, "1")
c.line(0, 18, 15, 14, "3")
c.r(3, 6, 3, 9, "w") if False else None
c.p(2, 7, "w"); c.p(13, 16, "w")
c.r(0, 0, 0, 23, "w") if False else None
reg("wall_sharp_geometry", c, "terrain")

# wood-carved bookshelf
c = Cv()
c.r(2, 2, 13, 20, "N")
c.r(3, 3, 12, 19, "n")
c.r(3, 3, 12, 3, "t")
c.r(4, 4, 11, 18, "O")
for ys in (4, 10, 15):
    pass
for ys, hs in ((4, 5), (10, 4), (15, 4)):
    x = 4
    while x < 12:
        w = 1 + (x + ys) % 2
        h = hs - ((x * 5 + ys) % 3)
        c.r(x, ys + hs - h, min(x + w - 1, 11), ys + hs - 1, "rbygmc"[(x + ys) % 6])
        x += w
    c.r(4, ys + hs, 11, ys + hs, "n")
c.r(5, 2, 6, 2, "t") if False else None
c.p(2, 1, "t"); c.p(13, 1, "t"); c.r(6, 1, 9, 1, "n")
c.sh(2, 13, 21)
reg("wood_carved_bookshelf", c)

# wood-carved table
c = Cv()
c.ell(8, 11, 7, 4.5, "n")
c.ell(8, 10, 6, 3.5, "t")
c.ell(8, 10, 4.5, 2.5, "n")
c.line(5, 10, 11, 10, "N") if False else None
c.p(6, 9, "t"); c.p(7, 8, "t")
for x in (3, 12):
    c.r(x, 14, x + 1, 19, "N"); c.p(x, 14, "n")
c.r(6, 15, 9, 19, "N") if False else None
c.r(7, 15, 8, 18, "N")
c.sh(2, 13, 20)
reg("wood_carved_table", c)


# ---- review round 1 redraws ----
# stairsdown: steps descending into a dark well
c = Cv()
c.r(0, 0, 15, 23, "3")
c.r(0, 0, 15, 2, "1")
for k in range(5):
    y0 = 3 + k * 4
    inset = k * 1
    c.r(inset, y0, 15 - inset, y0 + 2, "2" if k < 2 else "6")
    c.r(inset, y0, 15 - inset, y0, "1" if k < 2 else "5")
    c.r(inset, y0 + 3, 15 - inset, y0 + 3, "O")
c.r(5, 20, 10, 23, "O")
c.p(0, 5, "4"); c.p(15, 5, "4")
reg("stairsdown", c, "terrain")

# wall_sharp_geometry: banded fulcrete / metal / foam with angled cut
c = Cv()
c.r(0, 0, 15, 23, "2")
c.r(0, 0, 15, 3, "1"); c.r(0, 20, 15, 23, "3")
c.r(0, 4, 15, 4, "w")
c.r(0, 9, 15, 10, "3"); c.r(0, 9, 15, 9, "l")
c.r(0, 15, 15, 16, "3"); c.r(0, 15, 15, 15, "l")
c.line(0, 8, 7, 5, "6"); c.line(8, 5, 15, 8, "6")
c.line(0, 14, 15, 11, "w")
c.line(0, 19, 15, 17, "6")
c.r(11, 5, 12, 6, "1") if False else None
c.p(3, 12, "w"); c.p(12, 13, "w"); c.p(5, 18, "l")
reg("wall_sharp_geometry", c, "terrain")


# floor clocks: bold ecliptic rings and gold ticks
def clock(name, ne):
    import math
    c = Cv()
    c.r(0, 0, 15, 23, "2")
    cy = 23.5 if ne else 0.5
    for y in range(24):
        for x in range(16):
            d = math.hypot(x + 0.5, y + 0.5 - cy)
            if d <= 22:
                c.p(x, y, "1")
            if 19 < d <= 22:
                c.p(x, y, "3")
            if 16 < d <= 17.5 or 9 < d <= 10.5:
                c.p(x, y, "y")
            if 12.5 < d <= 14:
                c.p(x, y, "2")
    for ang in range(5, 90, 15):
        a = math.radians(ang)
        for rr in (12, 13, 14, 15, 16):
            x = int(rr * math.cos(a)); y = int(rr * math.sin(a))
            c.p(x, int(cy - y) if ne else int(cy + y), "y" if rr > 12 else "3")
    reg(name, c, "terrain")


clock("floor_clock_ne", True)
clock("floor_clock_se", False)
