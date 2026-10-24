"""Family redraw: frogs (svardym, wild frogs, cherubs, golems). One shared 'Qud frog' body plan:
squat, head+body one mass, two eyes ON TOP at the outer corners, wide mouth, pale belly,
webbed hands in front and big hind feet at the sides."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402

HUMANOID = set()

KEYS = {
    "creatures/sw/svardym/hatchling": "svardym_hatchling",
    "creatures/chiliad-svardym": "svardym_hatchling",
    "creatures/sw/svardym/jut": "svardym_jut",
    "creatures/sw/svardym/scrounge": "svardym_scrounge",
    "creatures/sw/svardym/eld": "svardym_eld",
    "creatures/sw/yd/svardym/1": "yd_bep",
    "creatures/sw/yd/svardym/2": "yd_krka",
    "creatures/sw/yd/elder/svardym/1": "yd_goek",
    "creatures/sw/yd/elder/svardym/2": "yd_mak",
    "creatures/sw/yd/elder/svardym/3": "yd_geeub",
    "creatures/sw/frog": "ice_frog",
    "creatures/chiliad-frog": "ice_frog",
    "creatures/sw/giant/frog": "pearlfrog",
    "creatures/sw/cherub/frog": "cherub_frog",
    "creatures/sw/cherub/frog/mechanical": "cherub_frog_mechanical",
    "creatures/sw/golem/frog": "golem_frog",
    "creatures/sw/golem/svardym": "golem_svardym",
}

HEAD = [
    "...11......11...",
    "..1wO1....1Ow1..",
    "..111133331111..",
    "..223333333322..",
    ".22233333333222.",
    ".22222222222222.",
    ".OOOOOOOOOOOOOO.",
]
SHOULDER = ".22211111111222."
TORSO = ".22.33211233.22."
HANDS = ".11.33211233.11."
BELLY = "3332111111112333"
FEET = [
    ".33321111112333.",
    "1133.22..22.3311",
    "1111.11..11.1111",
]
SMALL_HEAD = [
    ".1wO1..1Ow1.",
    ".111133 1111.".replace(" ", ""),
    "223333333322",
    "222333333222",
    "2OOOOOOOOOO2",
]


def squat(extra=1):
    rows = HEAD + [".33211111111233.", BELLY] + [BELLY] * extra + FEET
    return rows, 22 - len(rows)


def upright(H):
    n = H - len(HEAD) - 1 - 1 - len(FEET)
    rows = HEAD + [SHOULDER] + [TORSO] * n + [HANDS] + FEET
    return rows, 22 - len(rows)


def small(extra=0, open_mouth=False, big_feet=True):
    rows = list(SMALL_HEAD)
    rows.append("2ORRRRRRRRO2" if open_mouth else "332111111233")
    rows += ["332111111233"] * extra
    rows += ["333211112333", "3333.22.3333", "1111.11.1111"]
    return rows, 22 - len(rows)


def paint(c, rows, top, x0=0):
    for dy, row in enumerate(rows):
        assert len(row) in (12, 16), row
        for dx, ch in enumerate(row):
            if ch != ".":
                c.p(x0 + dx, top + dy, ch)


def finish(c, a=0, b=15):
    c.shadow(a, b)
    return c.out()


def spots(c, pts, a="4", b="5"):
    for i, (x, y) in enumerate(pts):
        if 0 <= y < 24 and c.g[y][x] in "23":
            c.p(x, y, a if i % 2 else b)


def crown(c, top, x0=0):
    spots(c, [(x0 + 6, top + 2), (x0 + 9, top + 2), (x0 + 5, top + 3), (x0 + 8, top + 3),
              (x0 + 10, top + 3), (x0 + 6, top + 4), (x0 + 9, top + 4), (x0 + 4, top + 4)])


# ------------------------------------------------------------------ svardym
# ------------------------------------------------------------------ yd named
# ------------------------------------------------------------------ others
def ice_frog():
    c = C()
    c.ell(7.5, 16.6, 6.8, 4.6, "3")
    c.ell(7.5, 16.2, 5.6, 3.6, "2")
    c.ell(7.5, 18.4, 3.6, 2.4, "1")
    c.ell(7.5, 13.6, 3.2, 1.5, "3")
    spots(c, [(6, 13), (9, 13), (7, 12), (4, 16), (11, 16)], "4", "5")
    for x in (2, 11):
        c.r(x, 10, x + 2, 12, "1"); c.p(x + 1, 11, "O")
    c.p(2, 10, "w"); c.p(13, 10, "w")
    c.r(3, 16, 12, 16, "O"); c.p(2, 15, "O"); c.p(13, 15, "O")
    # frost tufts on nostrils and brow
    for x, y in [(6, 14), (9, 14), (5, 13), (10, 13), (7, 14), (8, 14)]:
        c.p(x, y, "w")
    c.p(3, 9, "w"); c.p(12, 9, "w"); c.p(7, 11, "w"); c.p(8, 10, "w")
    # feet
    c.r(0, 19, 3, 21, "2"); c.r(12, 19, 15, 21, "2")
    for x in (0, 1, 2, 3, 12, 13, 14, 15):
        c.p(x, 21, "1")
    c.r(5, 20, 6, 21, "2"); c.r(9, 20, 10, 21, "2"); c.p(5, 21, "1"); c.p(6, 21, "1"); c.p(9, 21, "1"); c.p(10, 21, "1")
    c.p(0, 16, "4"); c.p(15, 18, "4")
    return finish(c)


def pearlfrog():
    c = C()
    c.ell(7.5, 15.5, 7.2, 5.8, "1")
    c.ell(7.5, 14, 5.4, 3.8, "w")
    c.ell(5.5, 12.5, 2.0, 1.4, "w")
    c.ell(7.5, 19.5, 6, 2, "3")
    c.line(2, 17, 13, 17, "4")
    c.line(4, 19, 11, 19, "4")
    c.r(2, 20, 4, 21, "2"); c.r(11, 20, 13, 21, "2")
    c.p(2, 21, "1"); c.p(3, 21, "1"); c.p(12, 21, "1"); c.p(13, 21, "1")
    for x, y in [(3, 14), (12, 13), (10, 16), (5, 16)]:
        c.p(x, y, "4")
    c.ell(7.5, 7.5, 3.4, 2.3, "3")
    c.r(5, 9, 10, 9, "O")
    c.r(3, 4, 5, 6, "4"); c.r(10, 4, 12, 6, "4")
    c.p(4, 5, "O"); c.p(11, 5, "O"); c.p(3, 4, "w"); c.p(12, 4, "w")
    c.r(5, 10, 6, 11, "2"); c.r(9, 10, 10, 11, "2")
    return finish(c)


def rims(c, top, ch):
    for x in (2, 5, 10, 13):
        c.p(x, top + 1, ch)
    c.p(3, top, ch); c.p(12, top, ch)
    c.p(2, top + 2, ch); c.p(13, top + 2, ch)


def cherub_frog():
    c = C()
    rows, top = squat(1)
    paint(c, rows, top)
    rims(c, top, "y")
    c.r(5, top, 10, top + 2, "1")
    c.r(5, top + 3, 10, top + 4, "2")
    c.r(5, top - 4, 10, top - 4, "y"); c.r(4, top - 3, 4, top - 2, "y"); c.r(11, top - 3, 11, top - 2, "y")
    c.r(5, top - 1, 10, top - 1, "y"); c.p(5, top - 4, "w")
    c.r(4, top + 8, 11, top + 8, "4")
    c.p(7, top + 9, "y"); c.p(8, top + 9, "y"); c.p(7, top + 10, "4"); c.p(8, top + 10, "4")
    c.p(3, top + 3, "4"); c.p(12, top + 3, "4")
    return finish(c)


def cherub_frog_mechanical():
    c = C()
    rows, top = squat(1)
    paint(c, rows, top)
    rims(c, top, "L")
    c.r(5, top, 10, top + 2, "1")
    c.r(5, top + 3, 10, top + 4, "2")
    c.r(3, top + 3, 12, top + 3, "l")
    c.r(4, top + 4, 11, top + 4, "L")
    c.r(4, top + 8, 11, top + 8, "l")
    c.r(5, top + 9, 10, top + 11, "l"); c.line(7, top + 9, 7, top + 11, "L"); c.line(8, top + 9, 8, top + 11, "L")
    for x, y in [(2, top + 3), (13, top + 3), (4, top + 9), (11, top + 9), (3, top + 6), (12, top + 6)]:
        c.p(x, y, "w")
    for x in (3, 4, 11, 12):
        c.p(x, top + 1, "c")
    c.p(2, top, "w"); c.p(13, top, "w")
    c.p(7, top + 10, "c"); c.p(8, top + 10, "c")
    c.r(5, top - 4, 10, top - 4, "l"); c.r(4, top - 3, 4, top - 2, "L"); c.r(11, top - 3, 11, top - 2, "L")
    c.r(5, top - 1, 10, top - 1, "L"); c.p(5, top - 4, "w"); c.p(8, top - 4, "c")
    return finish(c)


def _golem_marks(c, top, bottom):
    c.r(2, top + 3, 13, top + 3, "3"); c.r(1, top + 8, 7, top + 8, "3"); c.r(9, top + 10, 14, top + 10, "3")
    c.line(7, top + 8, 7, bottom - 4, "3"); c.line(9, top + 3, 9, top + 10, "3")
    for pts in [[(3, top + 4), (4, top + 6), (3, top + 8), (4, top + 10), (3, bottom)],
                [(12, top + 4), (11, top + 6), (12, top + 8), (11, top + 11), (12, bottom)],
                [(5, top + 10), (6, top + 11), (8, top + 11), (10, top + 10)]]:
        for q, r in zip(pts, pts[1:]):
            c.line(q[0], q[1], r[0], r[1], "4")
    for x, y in [(7, top + 5), (8, top + 5), (4, top + 7), (11, top + 7)]:
        c.p(x, y, "5")
    for x in (3, 4, 11, 12):
        c.p(x, top + 1, "4")
    c.p(2, top, "4"); c.p(13, top, "4")


def golem_svardym():
    c = C()
    rows, top = upright(20)
    paint(c, rows, top)
    _golem_marks(c, top, 17)
    c.r(0, 6, 0, 18, "4"); c.r(1, 7, 1, 18, "5"); c.p(0, 5, "4"); c.p(1, 12, ".")
    c.r(0, 19, 3, 20, "2"); c.r(0, 18, 3, 18, "6")
    return finish(c)


def ov(c, x0, y0, rows):
    """overlay text rows ('.' keeps what is below, '_' erases)"""
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            c.p(x0 + dx, y0 + dy, "." if ch == "_" else ch)


def svardym_scrounge():
    c = C()
    rows, top = squat(1)
    paint(c, rows, top)
    crown(c, top)
    spots(c, [(3, top + 8), (12, top + 8), (4, top + 10), (11, top + 10)])
    # lumpy sack of trinkets on its back
    c.ell(11.5, 7.4, 3.6, 3.6, "4")
    c.ell(12, 8, 2.6, 2.6, "5")
    c.r(10, 3, 13, 4, "4"); c.p(11, 2, "6"); c.p(12, 2, "6"); c.p(10, 3, "6"); c.p(13, 3, "6")
    c.line(9, 4, 14, 4, "6")
    for x, y, ch in [(10, 6, "y"), (13, 6, "c"), (11, 8, "r"), (14, 8, "y"), (12, 10, "c"), (12, 3, "y")]:
        c.p(x, y, ch)
    c.p(11, 5, "w")
    c.line(8, 9, 12, 13, "6")
    # spit-rolled coral pellet pinched in the left forefoot
    c.r(0, 17, 3, 19, "1"); c.p(0, 17, "."); c.p(0, 19, "2")
    c.ell(1.5, 14.8, 1.8, 1.8, "4"); c.p(2, 14, "w"); c.p(1, 16, "5"); c.p(2, 16, "6"); c.p(3, 15, "6")
    c.p(0, 17, "1")
    return finish(c)


def yd_bep():
    c = C()
    top = 6
    # round head with a warty ridge up the middle
    c.ell(7.5, 10.5, 4.6, 3.9, "2")
    c.ell(7.5, 9.2, 3.2, 2.2, "3")
    c.r(3, 13, 12, 13, "O")
    c.p(2, 12, "O"); c.p(13, 12, "O")
    c.r(5, 14, 10, 14, "1")
    for y, a, b in [(3, "4", "."), (4, "5", "4"), (5, "4", "5"), (6, "5", "4"), (7, "4", "5"), (8, "5", "4")]:
        c.p(7, y, a)
        if b != ".":
            c.p(8, y, b)
    c.p(6, 5, "6"); c.p(9, 6, "6")
    # eyes bulging far apart, narrow slit pupils
    for x in (0, 13):
        c.r(x, 7, x + 2, 11, "1")
        c.r(x, 8, x + 2, 10, "w")
        c.p(x + 1, 7, "1"); c.p(x + 1, 8, "O"); c.p(x + 1, 9, "O"); c.p(x + 1, 10, "O")
        c.p(x, 11, "2"); c.p(x + 2, 11, "2")
    c.p(3, 8, "2"); c.p(12, 8, "2")
    # small body
    c.ell(7.5, 17, 2.9, 2.6, "1")
    c.r(6, 15, 9, 15, "1")
    # thin spotted limbs flung wide
    for a, b in [((5, 16), (1, 14)), ((10, 16), (14, 14)),
                 ((6, 19), (2, 19)), ((9, 19), (13, 19)),
                 ((1, 14), (0, 13)), ((14, 14), (15, 13)),
                 ((2, 19), (1, 21)), ((13, 19), (14, 21))]:
        c.line(a[0], a[1], b[0], b[1], "2")
    for x, y in [(4, 15), (2, 14), (13, 14), (11, 15), (4, 19), (11, 19), (3, 19), (12, 19), (1, 20), (14, 20)]:
        c.p(x, y, "4")
    c.r(0, 21, 2, 21, "1"); c.r(13, 21, 15, 21, "1")
    c.p(0, 20, "1"); c.p(15, 20, "1")
    c.p(6, 17, "4"); c.p(9, 18, "4")
    return finish(c)


def yd_krka():
    c = C()
    # small round body on huge webbed feet
    c.ell(7.5, 14.5, 4.3, 4.8, "2")
    c.ell(7.5, 8.5, 6.0, 3.6, "2")
    c.ell(7.5, 8.2, 4.0, 2.2, "3")
    c.ell(7.5, 16.6, 3.4, 3.0, "1")
    # striped rings: alternate detail and fixed red around each eye
    import math
    for cx in (3.5, 12.5):
        c.ell(cx, 7, 2.9, 2.9, "1")
        pts = []
        for y in range(3, 12):
            for x in range(16):
                d = math.hypot(x - cx, y - 7)
                if 1.7 <= d <= 3.0:
                    pts.append((math.atan2(y - 7, x - cx), x, y))
        pts.sort()
        for i, (_, x, y) in enumerate(pts):
            c.p(x, y, "4" if i % 2 else "r")
        c.p(round(cx), 7, "O"); c.p(round(cx), 6, "w")
    c.p(3, 7, "O"); c.p(12, 7, "O")
    # nostrils with a ring through them
    c.p(7, 8, "O"); c.p(8, 8, "O")
    c.p(6, 9, "r"); c.p(7, 9, "4"); c.p(8, 9, "r"); c.p(9, 9, "4")
    # mouth
    c.r(3, 12, 12, 12, "O")
    c.p(2, 11, "O"); c.p(13, 11, "O")
    # forearms
    c.r(1, 15, 2, 18, "1"); c.r(13, 15, 14, 18, "1")
    # huge webbed feet
    for x0, dx in ((0, 1), (8, 1)):
        c.r(x0, 18, x0 + 7, 20, "1")
        c.r(x0, 20, x0 + 7, 21, "2")
        for k in (0, 2, 4, 6):
            c.p(x0 + k, 21, "1")
        c.p(x0 + 1, 19, "w"); c.p(x0 + 5, 19, "w")
        c.r(x0 + 2, 18, x0 + 5, 18, "2")
    c.r(0, 21, 15, 21, "2")
    for x in (0, 2, 4, 6, 8, 10, 12, 14):
        c.p(x, 21, "1")
    return finish(c)


def golem_frog():
    c = C()
    rows, top = squat(2)
    paint(c, rows, top)
    # clay seams
    c.r(1, top + 8, 3, top + 8, "3"); c.r(12, top + 8, 14, top + 8, "3")
    # a few glowing glass arteries: heart node on the chest, branches to arms and legs
    c.r(7, top + 6, 8, top + 7, "4"); c.p(7, top + 6, "5"); c.p(8, top + 7, "5")
    for pts in [[(6, top + 7), (4, top + 8), (3, top + 10), (3, 19)],
                [(9, top + 7), (11, top + 8), (12, top + 10), (12, 19)],
                [(7, top + 8), (7, top + 10), (6, top + 11)],
                [(7, top + 5), (5, top + 4), (4, top + 3)],
                [(8, top + 5), (10, top + 4), (11, top + 3)]]:
        for q, r in zip(pts, pts[1:]):
            c.line(q[0], q[1], r[0], r[1], "4")
    c.p(2, top, "4"); c.p(13, top, "4")
    return finish(c)


def golem_svardym():
    c = C()
    rows, top = upright(20)
    paint(c, rows, top)
    _golem_marks(c, top, 17)
    c.r(0, 6, 0, 18, "4"); c.r(1, 7, 1, 18, "5"); c.p(0, 5, "4"); c.p(1, 12, ".")
    c.r(0, 19, 3, 20, "2"); c.r(0, 18, 3, 18, "6")
    return finish(c)


def ov(c, x0, y0, rows):
    """overlay text rows ('.' keeps what is below, '_' erases)"""
    for dy, row in enumerate(rows):
        for dx, ch in enumerate(row):
            if ch == ".":
                continue
            c.p(x0 + dx, y0 + dy, "." if ch == "_" else ch)


def svardym_scrounge():
    c = C()
    rows, top = squat(1)
    paint(c, rows, top)
    crown(c, top)
    spots(c, [(3, top + 8), (12, top + 8), (4, top + 10), (11, top + 10)])
    # lumpy sack of trinkets on its back
    c.ell(11.5, 7.4, 3.6, 3.6, "4")
    c.ell(12, 8, 2.6, 2.6, "5")
    c.r(10, 3, 13, 4, "4"); c.p(11, 2, "6"); c.p(12, 2, "6"); c.p(10, 3, "6"); c.p(13, 3, "6")
    c.line(9, 4, 14, 4, "6")
    for x, y, ch in [(10, 6, "y"), (13, 6, "c"), (11, 8, "r"), (14, 8, "y"), (12, 10, "c"), (12, 3, "y")]:
        c.p(x, y, ch)
    c.p(11, 5, "w")
    c.line(8, 9, 12, 13, "6")
    # spit-rolled coral pellet pinched in the left forefoot
    c.r(0, 17, 3, 19, "1"); c.p(0, 17, "."); c.p(0, 19, "2")
    c.ell(1.5, 14.8, 1.8, 1.8, "4"); c.p(2, 14, "w"); c.p(1, 16, "5"); c.p(2, 16, "6"); c.p(3, 15, "6")
    c.p(0, 17, "1")
    return finish(c)


def yd_bep():
    c = C()
    top = 6
    # round head with a warty ridge up the middle
    c.ell(7.5, 10.5, 4.6, 3.9, "2")
    c.ell(7.5, 9.2, 3.2, 2.2, "3")
    c.r(3, 13, 12, 13, "O")
    c.p(2, 12, "O"); c.p(13, 12, "O")
    c.r(5, 14, 10, 14, "1")
    for y, a, b in [(3, "4", "."), (4, "5", "4"), (5, "4", "5"), (6, "5", "4"), (7, "4", "5"), (8, "5", "4")]:
        c.p(7, y, a)
        if b != ".":
            c.p(8, y, b)
    c.p(6, 5, "6"); c.p(9, 6, "6")
    # eyes bulging far apart, narrow slit pupils
    for x in (0, 13):
        c.r(x, 7, x + 2, 11, "1")
        c.r(x, 8, x + 2, 10, "w")
        c.p(x + 1, 7, "1"); c.p(x + 1, 8, "O"); c.p(x + 1, 9, "O"); c.p(x + 1, 10, "O")
        c.p(x, 11, "2"); c.p(x + 2, 11, "2")
    c.p(3, 8, "2"); c.p(12, 8, "2")
    # small body
    c.ell(7.5, 17, 2.9, 2.6, "1")
    c.r(6, 15, 9, 15, "1")
    # thin spotted limbs flung wide
    for a, b in [((5, 16), (1, 14)), ((10, 16), (14, 14)),
                 ((6, 19), (2, 19)), ((9, 19), (13, 19)),
                 ((1, 14), (0, 13)), ((14, 14), (15, 13)),
                 ((2, 19), (1, 21)), ((13, 19), (14, 21))]:
        c.line(a[0], a[1], b[0], b[1], "2")
    for x, y in [(4, 15), (2, 14), (13, 14), (11, 15), (4, 19), (11, 19), (3, 19), (12, 19), (1, 20), (14, 20)]:
        c.p(x, y, "4")
    c.r(0, 21, 2, 21, "1"); c.r(13, 21, 15, 21, "1")
    c.p(0, 20, "1"); c.p(15, 20, "1")
    c.p(6, 17, "4"); c.p(9, 18, "4")
    return finish(c)


def yd_krka():
    c = C()
    # small round body on huge webbed feet
    c.ell(7.5, 14.5, 4.3, 4.8, "2")
    c.ell(7.5, 8.5, 6.0, 3.6, "2")
    c.ell(7.5, 8.2, 4.0, 2.2, "3")
    c.ell(7.5, 16.6, 3.4, 3.0, "1")
    # striped rings: alternate detail and fixed red around each eye
    import math
    for cx in (3.5, 12.5):
        c.ell(cx, 7, 2.9, 2.9, "1")
        pts = []
        for y in range(3, 12):
            for x in range(16):
                d = math.hypot(x - cx, y - 7)
                if 1.7 <= d <= 3.0:
                    pts.append((math.atan2(y - 7, x - cx), x, y))
        pts.sort()
        for i, (_, x, y) in enumerate(pts):
            c.p(x, y, "4" if i % 2 else "r")
        c.p(round(cx), 7, "O"); c.p(round(cx), 6, "w")
    c.p(3, 7, "O"); c.p(12, 7, "O")
    # nostrils with a ring through them
    c.p(7, 8, "O"); c.p(8, 8, "O")
    c.p(6, 9, "r"); c.p(7, 9, "4"); c.p(8, 9, "r"); c.p(9, 9, "4")
    # mouth
    c.r(3, 12, 12, 12, "O")
    c.p(2, 11, "O"); c.p(13, 11, "O")
    # forearms
    c.r(1, 15, 2, 18, "1"); c.r(13, 15, 14, 18, "1")
    # huge webbed feet
    for x0, dx in ((0, 1), (8, 1)):
        c.r(x0, 18, x0 + 7, 20, "1")
        c.r(x0, 20, x0 + 7, 21, "2")
        for k in (0, 2, 4, 6):
            c.p(x0 + k, 21, "1")
        c.p(x0 + 1, 19, "w"); c.p(x0 + 5, 19, "w")
        c.r(x0 + 2, 18, x0 + 5, 18, "2")
    c.r(0, 21, 15, 21, "2")
    for x in (0, 2, 4, 6, 8, 10, 12, 14):
        c.p(x, 21, "1")
    return finish(c)


def golem_frog():
    c = C()
    rows, top = squat(2)
    paint(c, rows, top)
    # clay seams
    c.r(5, top + 6, 10, top + 6, "3")
    c.p(7, top + 5, "3"); c.p(8, top + 5, "3")
    c.r(1, top + 8, 3, top + 8, "3"); c.r(12, top + 8, 14, top + 8, "3")
    # glowing glass arteries
    c.line(7, top + 1, 7, top + 5, "4")
    c.line(8, top + 1, 8, top + 5, "4")
    for pts in [[(7, top + 7), (4, top + 9), (3, top + 12), (3, 19)],
                [(8, top + 7), (11, top + 9), (12, top + 12), (12, 19)]]:
        for q, r in zip(pts, pts[1:]):
            c.line(q[0], q[1], r[0], r[1], "4")
    c.r(7, top + 6, 8, top + 7, "5")
    c.p(7, top + 6, "4"); c.p(8, top + 6, "4")
    c.line(5, top + 7, 10, top + 7, "5") if False else None
    c.p(3, top + 1, "4"); c.p(12, top + 1, "4"); c.p(2, top, "4"); c.p(13, top, "4")
    return finish(c)


def svardym_hatchling():
    c = C()
    ov(c, 0, 12, [
        "...1111..1111...",
        "...1wO1..1Ow1...",
        "...2333333332...",
        "...OOOOOOOOOO...",
        ".44OmmmmmmmmO44.",
        "4w4OMMmmmmMMO4w4",
        ".44.OOOOOOOO.44.",
        "1w111.3223.111w1",
        "11111.2112.11111",
        "w1w1w......w1w1w",
    ])
    c.p(5, 14, "4"); c.p(9, 14, "5")
    return finish(c, 0, 15)


def svardym_jut():
    c = C()
    rows, top = squat(1)
    paint(c, rows, top)
    crown(c, top)
    spots(c, [(3, top + 8), (12, top + 8), (4, top + 10), (11, top + 10)])
    # chipped, jagged coral blade, pale, held up in the right forefoot
    for t in range(11):
        y = 13 - t
        x = 11 + round(t * 0.4)
        wd = 3 if t < 6 else 2
        c.p(x, y, "4")
        c.p(x + 1, y, "5")
        if wd == 3:
            c.p(x + 2, y, "6")
    for t in (3, 6, 8):
        c.p(11 + round(t * 0.4) - 1, 13 - t, "4")
    c.p(11 + round(9 * 0.4) + 1, 4, "."); c.p(15, 4, ".")
    c.p(15, 3, "4"); c.p(15, 2, "4")
    c.line(11, 13, 14, 13, "6")
    # forefoot gripping the handle
    c.r(11, 14, 14, 17, "1"); c.r(11, 17, 14, 17, "2")
    c.p(11, 14, "3"); c.p(14, 15, "3"); c.p(12, 15, "w")
    c.line(11, 14, 14, 14, "6")
    return finish(c)


def svardym_eld():
    c = C()
    # enormous lumpy wart-brain
    c.ell(7.5, 7.5, 6.2, 4.6, "3")
    for x, y in [(3.5, 3.6), (6, 2.6), (9, 2.6), (11.6, 3.8), (7.5, 4.2), (4.5, 6)]:
        c.ell(x, y, 1.7, 1.5, "3")
    for x, y in [(3, 3), (6, 2), (9, 2), (12, 3), (7, 4), (4, 6)]:
        c.p(x, y, "1"); c.p(x + 1, y + 1, "2")
    for x, y in [(5, 5), (10, 5), (2, 6), (13, 6)]:
        c.p(x, y, "4")
    for x in (0, 12):
        c.r(x, 7, x + 3, 9, "1")
    c.p(2, 8, "O"); c.p(13, 8, "O"); c.p(1, 8, "w"); c.p(14, 8, "w")
    c.p(2, 7, "c"); c.p(13, 7, "c")
    for x, y in [(0, 5), (15, 5), (1, 3), (14, 3), (8, 0), (12, 1)]:
        c.p(x, y, "c")
    c.r(3, 11, 12, 11, "O"); c.p(2, 10, "O"); c.p(13, 10, "O")
    c.ell(7.5, 16, 6.6, 4.8, "2")
    c.ell(7.5, 15.6, 3.4, 3.4, "1")
    # cloak: sloping from the shoulders, flaring to a zigzag hem, diagonal folds
    for side in (0, 1):
        def X(x):
            return x if side == 0 else 15 - x
        for y in range(11, 22):
            w = min(3 + (y - 11) // 2, 7)
            if y == 11:
                w = 3
            for x in range(w):
                bot = 21 if x % 2 == 0 else 20
                if y > bot or (y == 21 and x == w - 1 and False):
                    continue
                d = (x + y) % 4
                ch = "4" if d == 0 else ("6" if d == 2 else "5")
                if x == w - 1:
                    ch = "6"
                c.p(X(x), y, ch)
        c.p(X(0), 11, "."); 
    c.r(5, 12, 10, 12, "6")
    c.p(7, 13, "y"); c.p(8, 13, "y")
    c.r(5, 19, 6, 21, "1"); c.r(9, 19, 10, 21, "1")
    return finish(c)


def yd_goek():
    c = C()
    # crooked, hunched body leaning to the right, tall
    c.ell(9.5, 15, 4.6, 5.4, "2")
    c.ell(8.8, 15.5, 2.9, 4.2, "1")
    c.ell(12.2, 11, 2.8, 3.2, "3"); c.ell(12, 10.3, 1.8, 1.6, "2")
    for x, y in [(12, 9), (13, 11), (11, 12), (14, 8)]:
        c.p(x, y, "4")
    # head, tilted to the left, cheerful
    c.ell(6, 6, 5.3, 4.2, "2")
    c.r(2, 3, 9, 3, "3")
    c.p(3, 4, "4"); c.p(8, 3, "5"); c.p(10, 5, "4")
    for x in (0, 8):
        c.r(x, 0, x + 3, 2, "1")
    c.p(2, 1, "O"); c.p(10, 1, "O"); c.p(1, 1, "w"); c.p(9, 1, "w")
    # wide affable upturned grin with a big pale chin
    c.ell(6, 9.6, 3.4, 1.2, "1")
    c.r(2, 7, 10, 7, "O"); c.p(1, 6, "O"); c.p(11, 6, "O")
    c.p(2, 8, "O"); c.p(10, 8, "O"); c.r(3, 8, 9, 8, "M"); c.r(3, 9, 9, 9, "O")
    # gigantic tongue: out of the mouth, down the left side to the ground and curling
    c.r(4, 8, 7, 9, "m")
    tg = [(4, 10), (3, 11), (2, 12), (1, 13), (1, 14), (0, 15), (0, 16), (0, 17), (0, 18), (0, 19), (1, 19)]
    for i, (x, y) in enumerate(tg):
        c.r(x, y, x + 3, y, "m")
        c.p(x, y, "M"); c.p(x + 3, y, "M")
        if i % 3 == 1:
            c.p(x + 1, y, "w")
    c.r(1, 20, 7, 21, "m"); c.r(2, 21, 8, 21, "M"); c.p(2, 20, "w"); c.p(8, 20, "M")
    c.p(1, 21, "M"); c.p(7, 19, "m"); c.p(8, 19, "m"); c.p(8, 20, "m")
    # arms
    c.r(14, 14, 15, 18, "2"); c.r(13, 18, 15, 19, "1")
    # legs and feet
    c.r(8, 19, 11, 20, "2")
    c.r(9, 21, 15, 21, "1"); c.r(9, 20, 10, 20, "1"); c.r(13, 19, 14, 20, "2")
    return finish(c, 1, 15)


def yd_mak():
    c = C()
    c.ell(7.5, 8.2, 7.4, 5.0, "2")
    c.ell(7.5, 6.6, 5.4, 2.6, "3")
    for x, h in [(1, 3), (3, 4), (5, 5), (7, 6), (9, 5), (11, 4), (13, 3)]:
        base = 4 if 2 <= x <= 12 else 6
        for k in range(h):
            c.p(x, base - k, "4" if k < h - 1 else "w")
        c.p(x + 1, base, "5")
        if h > 3:
            c.p(x + 1, base - 1, "5")
    c.r(1, 5, 14, 5, "3")
    for x0, inner in ((1, 1), (9, -1)):
        c.r(x0, 7, x0 + 5, 9, "y")
        px = x0 + (4 if inner == 1 else 1)
        c.p(px, 8, "O"); c.p(px, 9, "O")
        for k in range(6):
            c.p(x0 + k, 6, "1")
        c.r(x0, 7, x0 + 5, 7, "1")
        if inner == 1:
            c.r(x0 + 3, 8, x0 + 5, 8, "1")
            c.p(x0 + 5, 9, "1")
        else:
            c.r(x0, 8, x0 + 2, 8, "1")
            c.p(x0, 9, "1")
        c.r(x0, 10, x0 + 5, 10, "3")
        c.p(x0 + 1, 8, "w") if inner == 1 else c.p(x0 + 4, 9, "w")
    c.r(3, 12, 12, 12, "O"); c.p(2, 13, "O"); c.p(13, 13, "O")
    # big pale inflated vocal sac under the chin
    c.ell(7.5, 16.4, 5.9, 4.6, "3")
    c.ell(7.5, 16.4, 5.0, 3.8, "1")
    c.r(4, 15, 6, 15, "w"); c.p(4, 16, "w")
    c.line(5, 19, 10, 19, "2")
    c.r(0, 13, 2, 18, "2"); c.r(13, 13, 15, 18, "2")
    c.r(0, 17, 2, 18, "1"); c.r(13, 17, 15, 18, "1")
    for x, y in [(4, 4), (11, 4), (1, 11), (14, 11), (7, 11)]:
        c.r(x, y, x + 1, y + 1, "4"); c.p(x, y, "w"); c.p(x + 1, y + 1, "5")
    for x0 in (0, 10):
        c.r(x0, 20, x0 + 5, 20, "2")
        for k in (0, 2, 4):
            c.p(x0 + k, 21, "1"); c.p(x0 + k, 22, "1")
    c.r(5, 20, 10, 20, "3")
    return finish(c)


def yd_geeub():
    c = C()
    c.ell(7.5, 14, 4.6, 7, "2")
    c.ell(7.5, 14.5, 2.8, 5.2, "1")
    c.ell(7.5, 5.6, 5.2, 3.9, "2")
    c.r(4, 3, 11, 3, "3")
    c.ell(7.5, 7.6, 3.6, 1.5, "1")
    for x in (1, 10):
        c.r(x, 1, x + 4, 3, "1")
        c.r(x + 1, 2, x + 3, 2, "O")
        c.p(x + 1, 1, "w")
    c.p(7, 4, "4"); c.p(8, 5, "5")
    # gentle smile
    c.r(5, 8, 10, 8, "O"); c.p(4, 7, "O"); c.p(11, 7, "O")
    for side in (0, 1):
        def X(x):
            return x if side == 0 else 15 - x
        for y in range(9, 21):
            off = 2 if y == 9 else (1 if y == 10 else 0)
            w = min(4 if y < 16 else 4 + (y - 15) // 2, 6)
            for x in range(off, w):
                ch = "4" if (x + y // 3) % 3 else "5"
                if x == off:
                    ch = "5"
                if x == w - 1:
                    ch = "6"
                c.p(X(x), y, ch)
        c.line(X(2), 12, X(2), 19, "5")
        c.p(X(1), 20, "6"); c.p(X(3), 21, "6"); c.p(X(2), 21, "4")
    c.line(5, 10, 10, 10, "4")
    for x, y, ch in [(5, 12, "r"), (6, 13, "y"), (7, 14, "c"), (8, 14, "y"), (9, 13, "r"), (10, 12, "c")]:
        c.p(x, y, ch)
    c.p(7, 15, "y"); c.p(8, 15, "y"); c.p(7, 16, "b"); c.p(8, 16, "b"); c.p(7, 17, "B"); c.p(8, 16, "w")
    c.r(1, 14, 2, 15, "y"); c.p(1, 14, "w")
    c.p(2, 19, "r"); c.p(2, 20, "r")
    for k, ch in enumerate(["m", "c", "y", "m"]):
        c.p(13, 12 + k * 2, ch)
    c.p(14, 18, "r")
    c.r(5, 20, 10, 20, "2"); c.r(4, 21, 11, 21, "1")
    return finish(c)


SPRITES = {
    "svardym_hatchling": svardym_hatchling(),
    "svardym_jut": svardym_jut(),
    "svardym_scrounge": svardym_scrounge(),
    "svardym_eld": svardym_eld(),
    "yd_bep": yd_bep(),
    "yd_krka": yd_krka(),
    "yd_goek": yd_goek(),
    "yd_mak": yd_mak(),
    "yd_geeub": yd_geeub(),
    "ice_frog": ice_frog(),
    "pearlfrog": pearlfrog(),
    "cherub_frog": cherub_frog(),
    "cherub_frog_mechanical": cherub_frog_mechanical(),
    "golem_frog": golem_frog(),
    "golem_svardym": golem_svardym(),
}
