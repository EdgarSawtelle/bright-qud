"""Family redraw after player feedback: drop the cute look. Lean feral dog, face-less root plants,
scanline hologram, and the two Nephal as repulsive slumped / raw-humped masses."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402

HUMANOID = set()

KEYS = {
    "terrain/sw/fattree1": ("dogthorn1", "tall"),
    "terrain/sw/fattree2": ("dogthorn2", "tall"),
    "creatures/sw/dog": "feral_dog",
    "creatures/sw/dreadroot": "dreadroot",
    "creatures/sw/lagroot": "lagroot",
    "creatures/sw/elder/lagroot": "elder_lagroot",
    "items/sw/shekhinah/hologram": "shekhinah_hologram",
    "creatures/nephilim/agolgut": "agolgot",
    "creatures/nephilim/bethsaida": "bethsaida",
    "creatures/wight/agolgot": "wight_agolgot",
    "creatures/wight/bethsaida": "wight_bethsaida",
}


def feral_dog():
    c = C()
    # long low back with bristles, lean belly
    c.r(5, 13, 12, 13, "1")
    c.r(4, 14, 13, 15, "2")
    c.r(5, 16, 12, 16, "3")
    c.r(7, 17, 10, 17, "3")
    for x in (5, 7, 9, 11):
        c.p(x, 12, "2")
    c.p(6, 12, "1"); c.p(10, 12, "1")
    # ribs
    for x in (6, 8, 10):
        c.p(x, 15, "3"); c.p(x, 14, "3")
    c.p(12, 14, "1"); c.p(12, 13, "1")  # hip bone
    c.r(13, 14, 13, 15, "3")
    # neck, lowered head and snout
    c.r(3, 13, 4, 14, "2")
    c.r(2, 14, 4, 16, "2")
    c.r(0, 16, 3, 17, "2")
    c.r(0, 17, 2, 18, "3")
    c.p(1, 16, "1"); c.p(2, 15, "1")
    c.p(3, 12, "3"); c.p(4, 12, "2"); c.p(4, 11, "3")  # ragged ear
    c.p(2, 16, "O")  # slit eye
    c.p(0, 17, "O")  # nose
    c.p(1, 18, "w"); c.p(3, 18, "w")  # a bared tooth
    # legs: thin, bent hind
    c.r(5, 17, 5, 21, "2"); c.r(4, 21, 4, 21, "2")
    c.r(7, 17, 7, 20, "3"); c.p(7, 21, "3"); c.p(8, 21, "3")
    c.r(12, 16, 12, 18, "2"); c.r(11, 18, 11, 19, "2"); c.r(12, 20, 12, 21, "3"); c.p(13, 21, "3")
    c.p(10, 17, "3"); c.p(10, 18, "3"); c.p(10, 19, "3"); c.p(10, 20, "3")
    # ragged tail
    c.p(13, 13, "2"); c.p(14, 13, "3"); c.p(15, 14, "3"); c.p(15, 15, "2"); c.p(14, 16, "3"); c.p(15, 17, "3")
    c.shadow(0, 15, 22)
    c.shadow(0, 15, 23)
    return c.out()


def _stalk(c, pts, w=1, hi="2", lo="3"):
    for (x0, y0, x1, y1) in pts:
        c.line(x0, y0, x1, y1, lo)
        if w > 1:
            c.line(x0 - 1, y0, x1 - 1, y1, hi)


def _roots(c, cx, y, spread, hi="2", lo="3"):
    for dx, dy in spread:
        c.line(cx, y, cx + dx, y + dy, lo)
        c.line(cx, y, cx - dx, y + dy, lo) if False else None
    return c


def bulb(c, x, y, r=1.0):
    """pale round bulb in detail roles, centre x,y"""
    if r < 0.9:
        x, y = int(x), int(y)
        c.r(x, y, x + 1, y + 1, "5"); c.p(x, y, "4")
        return
    c.ell(x, y, r + 0.6, r + 0.6, "5")
    c.ell(x - 0.3, y - 0.3, r - 0.1, r - 0.1, "4")


def dreadroot():
    c = C()
    # spread of spiky roots
    for tx, ty in [(0, 20), (2, 22), (4, 21), (11, 21), (13, 22), (15, 19), (6, 22), (9, 22)]:
        c.line(7 if tx < 8 else 8, 18, tx, ty, "3")
    for x in (3, 5, 10, 12):
        c.p(x, 20, "2")
    # thick gnarled stalk
    pts = [(7, 19), (7, 16), (8, 13), (7, 10), (8, 7), (8, 4), (7, 2)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], "3"); c.line(a[0] + 1, a[1], b[0] + 1, b[1], "3")
        c.line(a[0] - 1, a[1], b[0] - 1, b[1], "2")
    # thorny twigs
    c.line(8, 9, 12, 7, "3"); c.line(12, 7, 14, 5, "3")
    c.line(7, 6, 3, 5, "3"); c.line(3, 5, 2, 3, "3")
    c.line(8, 4, 11, 2, "3"); c.line(7, 2, 5, 0, "3")
    c.p(10, 8, "2"); c.p(4, 5, "2")
    # one thick central bulb, two small ones
    c.ell(7.5, 13, 3.4, 3.2, "5")
    c.ell(7.0, 12.4, 2.6, 2.4, "4")
    c.p(6, 11, "w"); c.p(5, 12, "4")
    c.r(9, 14, 10, 15, "5")
    bulb(c, 14, 5, 1.0)
    bulb(c, 2, 3, 1.0)
    c.shadow(0, 15, 23)
    return c.out()


def lagroot():
    c = C()
    for tx, ty in [(1, 21), (4, 22), (11, 22), (14, 21), (6, 22), (9, 22)]:
        c.line(7 if tx < 8 else 8, 19, tx, ty, "3")
    c.p(3, 21, "2"); c.p(12, 21, "2")
    pts = [(7, 20), (8, 16), (7, 12), (8, 8), (7, 4), (8, 1)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], "3")
    # thin branches with small bulbs
    br = [((8, 16), (13, 13), (14, 12)), ((7, 14), (2, 12), (1, 11)),
          ((7, 10), (3, 7), (2, 6)), ((8, 9), (12, 6), (13, 5)),
          ((7, 5), (4, 3), (3, 2)), ((8, 3), (11, 1), (12, 1))]
    for a, b, e in br:
        c.line(a[0], a[1], b[0], b[1], "3")
        c.line(b[0], b[1], e[0], e[1], "3")
        bulb(c, e[0], e[1], 0.5)
    for x, y in [(11, 14), (4, 13), (5, 8), (10, 7), (6, 4)]:
        bulb(c, x, y, 0.4)
    bulb(c, 8, 0, 0.4)
    c.shadow(0, 15, 23)
    return c.out()


def elder_lagroot():
    c = C()
    for tx, ty in [(0, 20), (1, 22), (3, 22), (5, 22), (10, 22), (12, 22), (14, 22), (15, 20)]:
        c.line(7 if tx < 8 else 8, 18, tx, ty, "3")
    for x in (2, 4, 11, 13):
        c.p(x, 21, "2")
    pts = [(7, 20), (8, 16), (7, 12), (8, 8), (7, 4), (8, 1)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], "3"); c.line(a[0] + 1, a[1], b[0] + 1, b[1], "3")
        c.line(a[0] - 1, a[1], b[0] - 1, b[1], "2")
    br = [((8, 17), (13, 15), (15, 13)), ((7, 16), (3, 15), (0, 13)),
          ((8, 13), (13, 10), (15, 9)), ((7, 12), (3, 10), (0, 8)),
          ((8, 9), (12, 6), (14, 4)), ((7, 8), (4, 5), (1, 3)),
          ((8, 5), (11, 3), (13, 1)), ((7, 4), (5, 2), (3, 0))]
    for a, b, e in br:
        c.line(a[0], a[1], b[0], b[1], "3")
        c.line(b[0], b[1], e[0], e[1], "3")
        bulb(c, e[0], e[1], 0.5)
    for x, y in [(11, 16), (5, 16), (11, 12), (5, 11), (10, 8), (5, 6), (10, 4), (5, 3), (14, 12), (1, 11), (13, 8), (2, 6)]:
        bulb(c, x, y, 0.4)
    bulb(c, 8, 0, 0.5)
    bulb(c, 9, 14, 0.8) if False else None
    c.shadow(0, 15, 23)
    return c.out()


def shekhinah_hologram():
    c = C()
    # halo crescent (opening upward)
    c.p(4, 0, "1"); c.p(11, 0, "1")
    c.p(5, 1, "1"); c.p(10, 1, "1")
    c.r(6, 2, 9, 2, "1")
    # head
    c.r(6, 4, 9, 6, "1"); c.r(7, 5, 8, 5, "2")
    # robed body, widening
    for y in range(7, 19):
        w = 1.6 + (y - 7) * 0.32
        c.r(round(7.5 - w), y, round(7.5 + w), y, "1")
    c.r(7, 8, 8, 18, "2")
    # scanline gaps every other row
    for y in range(7, 19):
        if y % 2 == 1:
            for x in range(16):
                if c.g[y][x] != ".":
                    c.g[y][x] = "."
    # swept wings (drawn after the scanlines: they keep a slower 4-row scan gap): a sickle sweep with
    # three long feather blades whose tips taper to a point, notches between the blades
    poly = [(5.5, 7.5), (3.5, 4.5), (1.5, 2.5), (-0.5, 1.5), (0.5, 4.2), (2.6, 5.6), (-0.5, 7.4),
            (1.6, 9.6), (0.8, 11.8), (1.0, 12.6), (3.2, 11.2), (5.0, 10.0)]
    def inside(px, py):
        n = len(poly); ins = False
        for i in range(n):
            (x1, y1), (x2, y2) = poly[i], poly[(i + 1) % n]
            if (y1 > py) != (y2 > py) and px < (x2 - x1) * (py - y1) / (y2 - y1) + x1:
                ins = not ins
        return ins
    for y in range(24):
        for x in range(0, 8):
            if inside(x + 0.5, y + 0.5) and c.g[y][x] == ".":
                c.m(x, y, "2")
    for x in range(0, 6):                      # bright upper edge of each blade
        for y in range(24):
            if c.g[y][x] == "2" and y > 0 and c.g[y - 1][x] == ".":
                c.m(x, y, "1")
    for y in (9,):
        if True:
            for x in list(range(0, 5)) + list(range(11, 16)):
                if c.g[y][x] in "12":
                    c.g[y][x] = "."
    # projected floating diamond
    for y, (a, b) in {19: (7, 8), 20: (5, 10), 21: (1, 14), 22: (5, 10), 23: (7, 8)}.items():
        c.r(a, y, b, y, "1" if y in (20, 21) else "2")
    c.r(2, 21, 3, 21, "2"); c.r(12, 21, 13, 21, "2")
    return c.out()


def agolgot():
    c = C()
    # bulging, irregular back: several lumps of different size stacked on the right
    for (x, y, rx, ry) in [(11.5, 7.2, 3.0, 2.8), (7.6, 6.6, 2.0, 1.8), (14, 11.5, 1.9, 2.6),
                           (9.5, 12, 5.0, 3.8), (12.5, 15.5, 3.0, 3.0), (6.5, 16.5, 5.2, 3.0)]:
        c.ell(x, y, rx, ry, "2")
    # sagging belly folds: hanging lobes with notches between them
    for (x, y, rx, ry) in [(4.5, 19.5, 1.9, 1.7), (8.2, 20.3, 1.8, 1.6), (11.6, 19.8, 1.8, 1.5), (14, 18.5, 1.2, 1.5)]:
        c.ell(x, y, rx, ry, "2")
    # slumped head, low and forward-left, with a heavy brow and a drooping lip
    c.ell(4.2, 13.8, 3.6, 3.0, "2")
    c.r(1, 14, 2, 17, "2")
    # carve notches so the back outline is lumpy and broken, not a smooth dome
    for (x, y) in [(9, 5), (9, 6), (10, 4), (13, 5), (14, 7), (15, 8), (15, 9), (15, 10), (13, 13), (15, 14), (14, 14),
                   (2, 10), (6, 8), (6, 9), (7, 10), (6, 11), (6, 20), (7, 20), (10, 21), (11, 21), (9, 21)]:
        c.p(x, y, ".")
    c.r(14, 9, 14, 9, "2"); c.p(14, 8, "2")
    # knobbly growths breaking the outline of the back and the left flank
    for (x, y, rx, ry, ch) in [(8.8, 3.6, 1.4, 1.3, "2"), (13.8, 5.0, 1.3, 1.4, "2"), (5.2, 6.8, 1.3, 1.2, "2"),
                               (0.8, 12.0, 1.1, 1.2, "2"), (15, 8.4, 0.9, 1.1, "2")]:
        c.ell(x, y, rx, ry, ch)
    for (x, y) in [(5, 6), (9, 3), (13, 4)]:
        c.p(x, y, "1")
    for (x, y) in [(7, 5), (11, 3), (14, 6), (10, 3)]:     # keep gaps between the growths
        c.p(x, y, ".")
    # light on the upper-left of each lump
    for (x, y, rx, ry) in [(10.8, 6.4, 1.8, 1.5), (7.2, 6.0, 1.0, 0.9), (13.6, 10.8, 0.9, 1.3),
                           (8.4, 11, 3.0, 2.2), (4.0, 12.6, 2.2, 1.5), (5.5, 16, 2.6, 1.2)]:
        c.ell(x, y, rx, ry, "1")
    # dark folds and creases between the lumps
    for a_, b_ in [((8, 8), (9, 10)), ((9, 9), (12, 10)), ((12, 9), (14, 9)), ((11, 14), (14, 13)),
                   ((8, 14), (11, 17)), ((4, 17), (8, 16)), ((7, 17), (6, 19)), ((10, 17), (10, 19)),
                   ((13, 15), (13, 18))]:
        c.line(a_[0], a_[1], b_[0], b_[1], "3")
    c.r(9, 19, 13, 19, "3"); c.r(3, 18, 6, 18, "3")
    c.line(7, 12, 7, 17, "3"); c.p(6, 11, "3")
    # shadowed right flank
    c.r(14, 14, 15, 17, "3"); c.p(15, 12, "3"); c.p(15, 13, "3")
    # stump legs, one splayed
    c.r(3, 21, 5, 22, "3"); c.r(8, 22, 10, 22, "3"); c.r(12, 21, 14, 22, "3"); c.p(2, 22, "3")
    # one dragging claw arm on the right, short stub on the left
    c.line(15, 12, 15, 19, "3"); c.p(14, 20, "3"); c.p(15, 21, "3"); c.p(14, 22, "3")
    c.line(1, 16, 0, 19, "3")
    # eye, brow, mouth
    c.p(3, 13, "O"); c.r(2, 12, 4, 12, "3")
    c.r(0, 16, 3, 16, "O"); c.p(1, 17, "3"); c.p(2, 17, "3")
    # wattle: folds sagging from the chin with long drips
    c.r(1, 18, 3, 18, "5"); c.r(1, 19, 2, 19, "5"); c.p(1, 20, "5"); c.p(1, 21, "4")
    c.p(0, 20, "5"); c.p(5, 19, "5"); c.p(5, 20, "4"); c.p(6, 21, "5")
    c.p(2, 23, "5"); c.p(6, 23, "4")
    # warts: a few clustered on the back, not scattered
    for x, y in [(10, 6), (12, 7), (11, 9), (13, 6), (14, 9), (8, 12), (10, 13), (4, 15), (3, 12)]:
        c.p(x, y, "4" if x % 2 else "6")
    for x, y in [(12, 8), (9, 11), (3, 14)]:
        c.p(x, y, "5")
    c.shadow(0, 15, 22)
    c.shadow(0, 15, 23)
    return c.out()


def bethsaida():
    c = C()
    # raw humps: right one higher, left one broader
    c.ell(4.8, 9, 4.2, 4.2, "2")
    c.ell(11, 7, 4.2, 5.4, "2")
    c.ell(8, 12, 4.4, 4.6, "2")
    c.ell(4, 7.6, 2.4, 2.4, "1"); c.ell(10.5, 5, 2.8, 2.8, "1")
    # sunk head, nares only
    c.r(6, 8, 8, 10, "3"); c.p(7, 9, "O"); c.p(6, 10, "O")
    c.p(6, 7, "w") if False else None
    # lower body and short legs, a squat central stance so the hands have room either side
    c.r(5, 14, 10, 17, "3")
    c.r(6, 15, 9, 17, "2")
    c.r(6, 18, 9, 20, "3"); c.r(7, 18, 8, 18, "2"); c.p(7, 19, "2")
    c.p(6, 21, "3"); c.p(9, 21, "3")
    # very long, thick arms down to the ground
    c.r(0, 10, 2, 11, "2")
    for y in range(11, 18):
        c.r(0, y, 1, y, "2"); c.p(2, y, "3")
    c.r(13, 9, 15, 10, "2")
    for y in range(10, 18):
        c.p(13, y, "3"); c.r(14, y, 15, y, "2")
    # big forked hands: a wide palm, then two thick spread digits per hand with a 2-pixel gap,
    # a fork split in each, and dark nails; drawn for the left, mirrored for the right
    for X in (lambda x: x, lambda x: 15 - x):
        for x in range(0, 6):
            c.p(X(x), 18, "2")
        c.p(X(0), 17, "2"); c.p(X(1), 17, "2")
        c.r(X(0), 19, X(1), 22, "1") if X(0) < X(1) else c.r(X(1), 19, X(0), 22, "1")
        for (x, y) in ((4, 19), (5, 19), (4, 20), (5, 20), (4, 21), (5, 21), (5, 22)):
            c.p(X(x), y, "1")
        c.p(X(1), 20, "3"); c.p(X(1), 21, "3"); c.p(X(5), 20, "3")     # knuckle shade, thicker on the outer edge
        c.p(X(0), 23, "6"); c.p(X(1), 23, "6"); c.p(X(4), 22, "6"); c.p(X(5), 23, "6")  # nails
    # the middle of the palm is shaded where the digits meet it
    c.p(2, 18, "3"); c.p(3, 18, "3"); c.p(13, 18, "3"); c.p(12, 18, "3")
    # capillary lines over the hide
    for a, b in [((4, 5), (5, 8)), ((5, 8), (3, 11)), ((5, 8), (7, 12)), ((11, 3), (11, 8)),
                 ((11, 8), (13, 11)), ((11, 8), (9, 12)), ((8, 12), (8, 16)), ((8, 14), (6, 16)),
                 ((8, 14), (10, 16)), ((12, 5), (14, 7))]:
        c.line(a[0], a[1], b[0], b[1], "5")
    # writhing hair and nails rising from the humps
    for pts in [[(3, 5), (2, 3), (3, 1), (2, 0)], [(5, 6), (6, 4), (5, 2)], [(9, 3), (8, 1), (9, 0)],
                [(11, 2), (12, 0)], [(13, 3), (14, 1), (13, 0)], [(10, 3), (11, 1)]]:
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1], "6")
        c.p(pts[-1][0], pts[-1][1], "4")
    c.shadow(0, 15, 22)
    c.shadow(0, 15, 23)
    return c.out()


def _rows(rows):
    assert len(rows) == 24, len(rows)
    for r in rows:
        assert len(r) == 16, r
    return rows


def _robe_body(c, top=9, hem=20, left=3, right=11, flare=2):
    """tattered robe body (roles 1-3) from the shoulders down: light left, dark right, vertical folds."""
    for y in range(top, hem + 1):
        t = (y - top) / (hem - top)
        l = round(left - flare * t); r = round(right + flare * t)
        c.r(l, y, r, y, "2")
        c.r(l, y, l + 1 + (1 if t > 0.5 else 0), y, "1")
        c.r(r - 1 - (1 if t > 0.4 else 0), y, r, y, "3")


def wight_agolgot():
    """Gyre wight of Agolgot: a slumped votary in sodden, tattered orchid robes (roles 1-3); flesh that
    shows (wattle, warts, drips) is in the detail roles; filth-black nails (O) at the sleeves.
    Echoes the Nephal: lopsided hump, head hung low, sagging wattle, warts. Smaller and leaner."""
    c = C()
    # back hump rising behind the right shoulder
    c.ell(10.3, 8.4, 3.0, 3.4, "2"); c.ell(9.6, 7.4, 1.8, 1.8, "1")
    # slumped torso, lopsided: left shoulder low
    _robe_body(c, top=9, hem=20, left=4, right=11, flare=2)
    c.r(3, 9, 4, 9, "1"); c.r(11, 10, 12, 10, "3")
    # drooping hood, hung forward to the left
    c.ell(5.2, 5.6, 3.4, 3.4, "2"); c.ell(4.5, 4.8, 2.1, 2.0, "1")
    c.ell(3.6, 7.0, 2.4, 2.4, "3")                       # deep shadow under the hood
    c.r(2, 6, 5, 8, "5"); c.p(2, 6, "3"); c.p(5, 8, "3")  # bare, grey-green flesh showing
    c.p(3, 6, "O")                                       # one small sunk eye, no highlight
    c.p(4, 7, "6"); c.p(2, 7, "4")                       # warts
    c.line(2, 8, 5, 8, "6")
    # wattle sagging from the chin down over the chest, with drips
    c.r(3, 9, 4, 9, "5"); c.r(3, 10, 4, 11, "5"); c.p(3, 12, "5"); c.p(4, 11, "4"); c.p(3, 13, "4")
    c.p(2, 10, "4"); c.p(5, 10, "5")
    # warts on the hood and the hump
    for (x, y) in ((6, 3), (7, 5), (10, 6), (12, 8), (11, 10)):
        c.p(x, y, "4")
    c.p(9, 5, "6")
    # long sleeves hanging, hands clear of the robe, filth-black nails
    for y in range(11, 18):
        c.p(2, y, "1"); c.p(3, y, "2")
        c.p(13, y, "2"); c.p(14, y, "3")
    c.line(4, 11, 4, 18, "3"); c.line(12, 11, 12, 18, "3"); c.line(13, 11, 13, 17, "1")
    for (x, y) in ((8, 3), (9, 3), (9, 4), (8, 4)):
        c.p(x, y, ".")                                   # notch: head and hump read as two masses
    c.p(1, 18, "O"); c.p(2, 18, "2"); c.p(3, 18, "O"); c.p(2, 19, "O")
    c.p(12, 18, "O"); c.p(13, 18, "3"); c.p(14, 18, "O"); c.p(13, 19, "O")
    # folds and sodden dark stains low on the robe
    for x, y0, y1 in ((6, 13, 19), (9, 12, 19)):
        c.line(x, y0, x, y1, "3")
    c.p(7, 15, "6"); c.p(8, 17, "6"); c.p(5, 18, "6")
    # ragged hem: tatters and rank drips
    c.r(1, 20, 14, 20, "3"); c.r(1, 20, 4, 20, "2")
    for x in (2, 5, 6, 9, 12):
        c.p(x, 21, "3" if x > 6 else "2")
    c.p(4, 21, "."); c.p(8, 21, ".")
    for x, y, ch in ((3, 21, "4"), (3, 22, "5"), (7, 21, "5"), (10, 22, "4"), (13, 21, "5"), (13, 22, "4")):
        c.p(x, y, ch)
    c.shadow(1, 14, 22)
    c.shadow(1, 14, 23)
    return c.out()


def wight_bethsaida():
    """Gyre wight of Bethsaida: a tall, raw votary in damp orchid robes (roles 1-3) laced with capillary
    lines, long forked hands reaching from the sleeves, writhing strands lifting from the hood, and a
    cool wet sheen (white glints). Echoes the Nephal: capillaries, long forked hands, strands."""
    c = C()
    # robe, leaner and more upright than the Agolgot wight
    _robe_body(c, top=9, hem=20, left=5, right=10, flare=3)
    c.r(4, 9, 11, 9, "2"); c.r(4, 9, 6, 9, "1")
    # hood: narrow, pointed forward, shadowed opening without a face
    c.ell(7.6, 5.4, 3.0, 3.5, "2"); c.ell(6.8, 4.6, 1.9, 2.1, "1")
    c.ell(7.8, 6.6, 1.7, 2.2, "3")
    c.p(7, 6, "O"); c.p(8, 7, "O")                         # two small dark nares, nothing more
    # writhing strands rising from the crown and the back of the hood
    for pts in ([(6, 2), (4, 1), (3, 0)], [(8, 2), (9, 0)], [(10, 3), (12, 2), (13, 0)],
                [(11, 5), (13, 5), (14, 3)], [(5, 3), (3, 4), (2, 3)]):
        for a_, b_ in zip(pts, pts[1:]):
            c.line(a_[0], a_[1], b_[0], b_[1], "6")
        c.p(pts[-1][0], pts[-1][1], "4")
    # capillary lines on the raw hide of the robe and hood
    for a_, b_ in (((7, 10), (7, 14)), ((7, 12), (5, 14)), ((7, 12), (9, 14)), ((9, 14), (10, 17)),
                   ((5, 14), (4, 17)), ((7, 14), (7, 19)), ((6, 3), (6, 5)), ((9, 4), (10, 6))):
        c.line(a_[0], a_[1], b_[0], b_[1], "5")
    # cool wet glints
    for (x, y) in ((6, 10), (5, 13), (9, 11), (4, 16), (10, 15), (5, 4)):
        c.p(x, y, "w")
    # sleeves with long forked hands: wide palm, then two spread digits with a 2-pixel gap
    for X in (lambda x: x, lambda x: 15 - x):
        for y in range(10, 18):
            c.p(X(3), y, "1" if X(0) == 0 else "2"); c.p(X(4), y, "3")
        c.r(min(X(0), X(3)), 18, max(X(0), X(3)), 18, "4")
        c.line(X(0), 19, X(0), 22, "4"); c.line(X(3), 19, X(3), 21, "4")
        c.p(X(0), 23, "6"); c.p(X(3), 22, "6")
        c.p(X(1), 18, "5") if False else None
    # damp, tattered hem
    c.r(2, 20, 13, 20, "3"); c.r(2, 20, 5, 20, "2")
    for x in (3, 5, 7, 10, 12):
        c.p(x, 21, "3" if x > 7 else "2")
    c.p(7, 22, "5"); c.p(11, 22, "4")
    c.shadow(2, 13, 22)
    c.shadow(2, 13, 23)
    return c.out()


def dogthorn(seed):
    """Dogthorn tree: "the bark is splintered into pointy spines ... a tangled nest of roots". A crooked splintered
    trunk under a thin, broken crown of greasy leaves, with thorns breaking the outline. No lollipop."""
    import random
    from terrain3_1 import new, put, line, rows
    rnd = random.Random(seed)
    g = new(".")
    lean = 1 if seed % 2 else -1
    for (cx, cy, n) in ((3, 8, 13), (12, 7, 13), (8, 3, 15), (7, 9, 10), (11, 11, 6)):       # broken leaf clumps
        for _ in range(n):
            x, y = cx + rnd.randint(-3, 3), cy + rnd.randint(-2, 2)
            put(g, x, y, rnd.choice("1223"))
    for (x0, y0, x1, y1) in ((8, 13, 3, 7), (8, 12, 13, 6), (8, 12, 8, 3)):                  # bare boughs through the crown
        line(g, x0, y0, x1, y1, "n")
    x = 8
    for y in range(11, 21):                                                                  # crooked trunk
        put(g, x, y, "n"); put(g, x + 1, y, "N")
        if y % 3 == 0:
            x += lean if y < 16 else -lean
    for (tx, ty, dx) in ((7, 13, -1), (10, 15, 1), (7, 17, -1), (10, 18, 1)):                # bark splinters
        put(g, tx, ty, "w"); put(g, tx + dx, ty - 1, "w")
    for (tx, ty, dx, dy) in ((0, 6, -1, -1), (15, 5, 1, -1), (4, 0, -1, -1), (12, 1, 1, -1), (0, 10, -1, 1),
                             (15, 10, 1, 1), (8, 0, 0, -1), (5, 12, -1, 1), (13, 13, 1, 1)):  # thorns past the outline
        put(g, tx, ty, "w"); put(g, tx - dx, ty - dy, "N")
    for (x0, x1, y1) in ((8, 3, 22), (9, 13, 21), (8, 6, 22), (9, 11, 22)):                  # tangled roots
        line(g, x0, 20, x1, y1, "N")
    return rows(g)


SPRITES = {
    "dogthorn1": dogthorn(1), "dogthorn2": dogthorn(2),
    "feral_dog": feral_dog(), "dreadroot": dreadroot(), "lagroot": lagroot(),
    "elder_lagroot": elder_lagroot(), "shekhinah_hologram": shekhinah_hologram(),
    "agolgot": agolgot(), "bethsaida": bethsaida(),
    "wight_agolgot": wight_agolgot(), "wight_bethsaida": wight_bethsaida(),
}
