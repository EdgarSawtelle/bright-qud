"""Family redraw after player feedback: drop the cute look. Lean feral dog, face-less root plants,
scanline hologram, and the two Nephal as repulsive slumped / raw-humped masses."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402

HUMANOID = set()

KEYS = {
    "creatures/sw/dog": "feral_dog",
    "creatures/sw/dreadroot": "dreadroot",
    "creatures/sw/lagroot": "lagroot",
    "creatures/sw/elder/lagroot": "elder_lagroot",
    "items/sw/shekhinah/hologram": "shekhinah_hologram",
    "creatures/nephilim/agolgut": "agolgot",
    "creatures/nephilim/bethsaida": "bethsaida",
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
    # swept wings with a gap to the body
    for y in range(3, 16):
        xl = round(0 + (y - 3) * 0.35)
        c.r(xl, y, xl + 2 + (y - 3) // 4, y, "2")
        c.r(15 - xl - 2 - (y - 3) // 4, y, 15 - xl, y, "2")
    c.line(0, 3, 0, 8, "1"); c.line(15, 3, 15, 8, "1")
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
    # projected floating diamond
    for y, (a, b) in {19: (7, 8), 20: (5, 10), 21: (1, 14), 22: (5, 10), 23: (7, 8)}.items():
        c.r(a, y, b, y, "1" if y in (20, 21) else "2")
    c.r(2, 21, 3, 21, "2"); c.r(12, 21, 13, 21, "2")
    return c.out()


def agolgot():
    c = C()
    # smashed, lopsided mass: one big hump high on the right, body sagging left
    c.ell(10, 9, 5.6, 5.2, "2")
    c.ell(9, 15, 7.2, 5.0, "2")
    c.ell(11, 7, 3.2, 3.2, "1")
    # slumped head, low, forward-left, no neck
    c.ell(4.6, 14.5, 4.6, 4.0, "2")
    c.ell(3.8, 13.2, 3.0, 2.4, "1")
    c.r(1, 17, 7, 18, "3")
    # shadowed underside
    c.r(5, 19, 14, 20, "3")
    c.r(13, 13, 15, 18, "3")
    c.ell(13, 17, 2.5, 2.5, "3")
    # lopsided stump legs
    c.r(2, 19, 6, 21, "3"); c.r(3, 20, 5, 21, "2")
    c.r(10, 20, 12, 21, "3"); c.r(13, 21, 14, 21, "3")
    # single dragging claw arm on right, short stub on left
    c.line(14, 12, 15, 17, "3"); c.line(15, 17, 15, 20, "3"); c.p(14, 21, "3")
    c.line(1, 15, 0, 18, "3")
    # tiny sunk eye
    c.p(3, 13, "O")
    # wattle: sagging from the chin with drips
    c.r(2, 18, 6, 18, "5")
    c.r(3, 19, 6, 19, "5")
    c.p(4, 20, "5"); c.p(5, 20, "4"); c.p(3, 21, "4")
    c.p(2, 22, "5"); c.p(5, 22, "4"); c.p(4, 23, "5")
    # mouth hint
    c.r(1, 17, 3, 17, "O")
    # warts and freckles, scattered
    for x, y in [(5, 11), (6, 14), (3, 15), (7, 12), (9, 7), (12, 5), (10, 10), (13, 9), (8, 16), (11, 14), (6, 17), (4, 12), (12, 12), (9, 18)]:
        c.p(x, y, "4" if (x + y) % 2 else "6")
    for x, y in [(2, 14), (8, 9), (11, 3)]:
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
    # lower body and short legs
    c.r(5, 14, 11, 17, "3")
    c.r(6, 15, 9, 17, "2")
    c.r(5, 18, 7, 21, "3"); c.r(9, 18, 10, 21, "3"); c.p(4, 21, "3"); c.p(11, 21, "3"); c.p(5, 18, "2"); c.p(9, 18, "2")
    # very long arms, thick, reaching the ground
    c.r(0, 10, 2, 11, "2")
    for y in range(11, 19):
        c.r(0, y, 1, y, "2"); c.p(2, y, "3")
    c.r(13, 9, 15, 10, "2")
    for y in range(10, 19):
        c.p(13, y, "3"); c.r(14, y, 15, y, "2")
    # hands: many forked digits spreading along the ground
    c.r(0, 19, 2, 19, "3"); c.r(13, 19, 15, 19, "3")
    for tx in (0, 1, 3, 4):
        c.line(1, 19, tx, 21, "3")
    for tx in (11, 12, 14, 15):
        c.line(14, 19, tx, 21, "3")
    for x in (0, 1, 3, 4, 11, 12, 14, 15):
        c.p(x, 21, "1")
    c.p(2, 21, "3"); c.p(13, 21, "3")
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


SPRITES = {
    "feral_dog": feral_dog(), "dreadroot": dreadroot(), "lagroot": lagroot(),
    "elder_lagroot": elder_lagroot(), "shekhinah_hologram": shekhinah_hologram(),
    "agolgot": agolgot(), "bethsaida": bethsaida(),
}
