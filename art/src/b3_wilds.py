"""B3 restyle: kit2 wild creatures, machines and plants (non-humanoid)."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402


def tube(c, pts, r0, r1, ch):
    """Thick polyline whose radius goes r0 -> r1."""
    d = [0.0]
    for (a, b), (e, f) in zip(pts, pts[1:]):
        d.append(d[-1] + ((e - a) ** 2 + (f - b) ** 2) ** 0.5)
    tot = d[-1] or 1
    n = int(tot * 2) + 1
    for i in range(n + 1):
        t = i / n * tot
        k = 1
        while k < len(d) - 1 and d[k] < t:
            k += 1
        u = (t - d[k - 1]) / ((d[k] - d[k - 1]) or 1)
        x = pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * u
        y = pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * u
        r = r0 + (r1 - r0) * t / tot
        c.ell(x, y, r, r, ch)


def hexp(c, x, y, a="4", b="5"):
    c.r(x, y, x + 1, y, a)
    c.r(x, y + 1, x + 1, y + 1, b)


# ---------------------------------------------------------------- animals
def puma():
    c = C()
    tube(c, [(12, 15), (14, 12), (14, 8), (12, 6)], 1.0, 1.0, "2")
    c.p(12, 6, "3"); c.p(11, 6, "3"); c.p(14, 8, "3")
    c.ell(8, 14, 5.3, 3.3, "2")
    c.ell(8, 17, 4.5, 1.2, "3")
    c.ell(8, 12, 4.5, 1.5, "1")
    for x, y in [(5, 11), (7, 10), (9, 10), (11, 11), (7, 12), (9, 12)]:
        hexp(c, x, y)
    c.ell(3, 11, 2.8, 2.6, "2")
    c.r(0, 11, 2, 13, "1")
    c.r(0, 12, 0, 12, "O"); c.p(1, 13, "3")
    c.r(2, 8, 2, 9, "3"); c.r(3, 8, 3, 8, "3"); c.r(5, 8, 5, 9, "3"); c.p(4, 8, "3")
    c.p(2, 10, "y"); c.p(4, 10, "y")
    c.r(4, 16, 5, 20, "2"); c.r(6, 17, 6, 20, "3")
    c.r(10, 16, 12, 20, "2"); c.r(9, 17, 9, 20, "3")
    c.r(3, 21, 6, 21, "1"); c.r(9, 21, 12, 21, "1")
    c.shadow(1, 14)
    return c.out()


def honey_skunk():
    c = C()
    # honey mist
    for x, y in [(2, 6), (5, 4), (9, 3), (12, 5), (14, 9), (1, 11), (3, 8)]:
        c.p(x, y, "y")
    for x, y in [(4, 6), (8, 5), (13, 7), (11, 3)]:
        c.p(x, y, "t")
    # bushy tail
    c.ell(11, 11, 3, 5.5, "1")
    c.r(10, 6, 12, 14, "1")
    c.line(11, 6, 11, 16, "4")
    c.r(10, 8, 12, 8, "4"); c.r(10, 11, 12, 11, "4")
    c.p(12, 12, "2"); c.p(13, 13, "2")
    # body
    c.ell(7, 16, 4.5, 3.2, "2")
    c.ell(7, 14.5, 3.5, 1.5, "1")
    c.line(4, 14, 10, 14, "4")
    # head
    c.ell(3, 15, 2.5, 2.3, "2")
    c.r(1, 16, 2, 17, "4"); c.p(0, 16, "O")
    c.p(3, 13, "3"); c.p(4, 13, "3"); c.p(2, 13, "3")
    c.p(3, 14, "y"); c.p(3, 15, "O")
    # legs
    c.r(4, 18, 5, 20, "3"); c.r(9, 18, 10, 20, "3")
    c.r(3, 21, 5, 21, "2"); c.r(9, 21, 11, 21, "2")
    c.shadow(2, 13)
    return c.out()


def chameleon():
    c = C()
    # coiled tail
    tube(c, [(11, 14), (14, 16), (13, 20), (10, 19), (10, 17)], 1.3, 0.8, "2")
    c.p(11, 17, "3")
    c.ell(8, 14, 4.2, 3.2, "2")
    c.ell(8, 12.5, 3.5, 1.5, "1")
    # shifting crystal diamonds
    for x, y in [(6, 12), (8, 11), (10, 12), (7, 14), (9, 14)]:
        c.p(x, y, "4"); c.p(x, y + 1, "5"); c.p(x - 1, y + 1, "6") if False else None
    c.r(5, 17, 11, 17, "3")
    # head with bone horn
    c.ell(3.5, 12, 2.6, 2.2, "2")
    c.line(2, 10, 0, 6, "w"); c.p(1, 8, "w")
    c.r(0, 13, 2, 13, "3")
    c.r(3, 10, 5, 11, "1")
    c.r(3, 10, 4, 11, "y"); c.p(4, 11, "O")      # big turret eye
    # legs gripping
    c.line(5, 16, 3, 19, "3"); c.line(6, 17, 6, 20, "3")
    c.line(10, 16, 12, 19, "3"); c.line(9, 17, 8, 20, "3")
    c.r(2, 19, 4, 20, "1"); c.r(5, 20, 7, 21, "1"); c.r(11, 19, 13, 20, "1"); c.r(7, 21, 9, 21, "1")
    c.shadow(1, 14)
    return c.out()


def frog_base(c, s):
    pass


def frog():
    c = C()
    # hind legs folded
    c.r(2, 13, 4, 18, "3"); c.r(11, 13, 13, 18, "3")
    c.r(3, 13, 3, 17, "2"); c.r(12, 13, 12, 17, "2")
    c.r(0, 19, 4, 20, "1"); c.r(11, 19, 15, 20, "1")
    c.ell(8, 14, 4.5, 4.5, "2")
    c.ell(8, 12.5, 3.2, 2.6, "1")
    c.p(6, 15, "4"); c.p(9, 14, "4"); c.p(8, 17, "4"); c.p(5, 12, "4")
    # front legs
    c.r(4, 17, 5, 20, "2"); c.r(10, 17, 11, 20, "2")
    # head with bulging eyes
    c.ell(8, 8, 4, 2.6, "2")
    c.r(5, 9, 10, 9, "3")
    c.r(3, 5, 5, 7, "1"); c.r(10, 5, 12, 7, "1")
    c.r(4, 6, 4, 6, "O"); c.r(11, 6, 11, 6, "O")
    c.p(4, 5, "w"); c.p(11, 5, "w")
    # frost tufts
    c.p(7, 6, "w"); c.p(8, 6, "w"); c.p(7, 5, "w"); c.p(9, 4, "w") if False else None
    c.p(6, 4, "W") if False else None
    c.r(7, 4, 8, 5, "5")
    c.shadow(0, 15)
    return c.out()


def giant_frog():
    c = C()
    # wide, flat, squat body filling the tile width
    c.ell(8, 15, 8, 5.5, "2")
    c.ell(8, 14, 7, 4, "1")
    c.ell(8, 17, 5.5, 2.8, "w")
    c.ell(8, 17.5, 4.5, 2, "1")
    for x, y in [(3, 12), (7, 12), (11, 12), (13, 15), (1, 15)]:
        c.r(x, y, x + 1, y + 1, "5"); c.p(x, y, "4")
    # folded legs at the sides
    c.ell(2, 17, 2.4, 3.2, "3"); c.ell(13, 17, 2.4, 3.2, "3")
    c.ell(2.5, 16.5, 1.4, 2, "2"); c.ell(12.5, 16.5, 1.4, 2, "2")
    c.r(0, 20, 4, 21, "2"); c.r(11, 20, 15, 21, "2")
    # head with big eye bumps and wide mouth
    c.ell(8, 9, 5, 2.6, "2")
    c.r(3, 6, 6, 8, "1"); c.r(9, 6, 12, 8, "1")
    c.r(4, 7, 5, 8, "y"); c.r(10, 7, 11, 8, "y")
    c.p(5, 8, "O"); c.p(10, 8, "O")
    c.r(2, 10, 13, 10, "O")
    c.p(2, 9, "O"); c.p(13, 9, "O")
    c.shadow(0, 15)
    return c.out()


def salamander():
    c = C()
    tube(c, [(8, 3), (8, 8), (10, 12), (7, 16), (6, 20), (9, 22)], 3.0, 0.9, "2")
    tube(c, [(8, 7), (9.5, 11), (7.5, 15)], 1.4, 1.2, "1")
    # chunky legs with toes
    for (x0, y0, x1, y1) in [(6, 8, 2, 8), (10, 8, 14, 8), (10, 15, 14, 16), (5, 16, 1, 17)]:
        tube(c, [(x0, y0), (x1, y1)], 1.4, 1.1, "3")
        c.r(x1 - 1, y1 - 1, x1 + 1, y1 + 1, "2")
    c.p(0, 8, "3") if False else None
    # island-chain spots
    for x, y in [(8, 6), (9, 9), (9, 12), (7, 15), (6, 18)]:
        c.r(x, y, x + 1, y + 1, "4")
        c.p(x + 1, y + 1, "5")
    c.p(7, 3, "O"); c.p(9, 3, "O"); c.p(7, 2, "y"); c.p(9, 2, "y")
    c.r(7, 0, 9, 0, "3")
    c.shadow(1, 14)
    return c.out()


def tortoise():
    c = C()
    # head toward the left, stumpy legs
    c.r(0, 15, 3, 18, "4"); c.r(12, 16, 15, 19, "4")
    c.r(1, 19, 4, 20, "5"); c.r(12, 19, 15, 20, "5")
    c.r(5, 18, 7, 21, "5"); c.r(10, 18, 12, 21, "5")
    c.ell(2.5, 11, 2.8, 2.6, "4")
    c.r(0, 11, 1, 12, "5"); c.p(0, 12, "O")
    c.p(2, 10, "O"); c.p(3, 9, "5")
    # dome shell
    c.ell(9, 13, 7, 6.5, "3")
    c.ell(9, 12.5, 6.3, 5.8, "2")
    c.ell(9, 11.5, 5, 4, "1")
    c.line(9, 7, 9, 17, "3"); c.line(4, 11, 14, 11, "3"); c.line(3, 15, 15, 15, "3")
    c.line(5, 8, 6, 11, "3"); c.line(13, 8, 12, 11, "3")
    for x, y in [(6, 8), (12, 8), (7, 13), (11, 13), (9, 9), (5, 16), (13, 16)]:
        c.p(x, y, "w"); c.p(x, y - 1, "w")
    c.shadow(0, 15)
    return c.out()


def equimax():
    c = C()
    tube(c, [(12, 9), (14, 12), (13, 17)], 1.2, 0.9, "4")
    c.p(13, 18, "5")
    c.ell(9, 11, 4.5, 3, "2")
    c.ell(9, 9.5, 3.8, 1.2, "1")
    c.r(4, 5, 6, 10, "2"); c.r(3, 6, 4, 9, "1")
    c.ell(3, 4.5, 2.5, 1.8, "2")
    c.r(0, 5, 2, 7, "1"); c.p(0, 6, "O")
    c.p(3, 4, "O"); c.p(3, 2, "3"); c.p(4, 2, "3"); c.p(4, 3, "3")
    c.line(5, 3, 7, 9, "4"); c.line(6, 3, 8, 9, "5")
    c.r(5, 2, 5, 3, "4")
    for x, h in [(4, 0), (6, 1), (10, 1), (12, 0)]:
        c.r(x, 13, x, 19, "2" if h == 0 else "3")
        c.r(x + 1, 13, x + 1, 19, "2" if h == 0 else "3")
        c.r(x, 20, x + 1, 20, "O")
        c.p(x - 1, 20, "4"); c.p(x + 2, 20, "4"); c.p(x - 1, 21, "5"); c.p(x + 2, 21, "5")
    c.shadow(1, 14)
    return c.out()


def crow():
    c = C()
    # tail feathers
    c.line(11, 15, 14, 19, "3"); c.line(12, 14, 15, 18, "3"); c.line(10, 16, 12, 20, "3")
    c.ell(8, 13, 4.5, 4, "2")
    # glowing skin under feathers
    c.ell(6, 14, 2, 2.5, "4"); c.p(5, 14, "5"); c.p(6, 16, "5"); c.p(7, 13, "5")
    # wing folded
    c.ell(10, 13, 2.8, 4, "3"); c.line(9, 10, 12, 17, "2")
    c.r(8, 10, 11, 10, "1")
    # head + hooked beak
    c.ell(4.5, 8, 2.5, 2.5, "2")
    c.r(2, 8, 2, 9, "w"); c.p(1, 8, "w"); c.p(0, 9, "w"); c.p(1, 9, "w")
    c.p(4, 7, "y"); c.p(4, 8, "O")
    c.p(5, 5, "3"); c.p(4, 5, "3")
    # legs
    c.line(7, 17, 7, 20, "w"); c.line(9, 17, 9, 20, "w")
    c.r(5, 21, 7, 21, "w"); c.r(9, 21, 11, 21, "w")
    c.shadow(3, 12)
    return c.out()


def twohead_boar():
    c = C()
    # one boar body, side view, facing left
    c.ell(10, 15, 5.5, 3.6, "2")
    c.ell(10, 13.5, 4.5, 1.6, "1")
    for x in range(7, 15, 2):
        c.p(x, 11, "3"); c.p(x, 10, "3")
    c.line(14, 13, 15, 10, "3")
    # legs
    c.r(6, 17, 7, 20, "3"); c.r(9, 18, 9, 20, "3"); c.r(12, 17, 14, 20, "3"); c.r(11, 18, 11, 20, "3")
    c.r(5, 21, 8, 21, "1"); c.r(11, 21, 14, 21, "1")
    # two necks splitting at the front
    c.r(5, 11, 7, 15, "2"); c.r(3, 9, 5, 12, "2"); c.r(3, 14, 5, 17, "2")
    # upper head
    c.ell(2.5, 7, 2.6, 2.2, "2")
    c.r(0, 7, 1, 9, "1"); c.p(0, 8, "O")
    c.p(3, 6, "y"); c.p(3, 4, "3"); c.p(4, 5, "3")
    c.p(0, 10, "w"); c.p(1, 10, "w")
    # lower head
    c.ell(2.5, 19, 2.6, 2.2, "2")
    c.r(0, 19, 1, 21, "1"); c.p(0, 20, "O")
    c.p(3, 18, "y"); c.p(3, 16, "3"); c.p(4, 17, "3")
    c.p(0, 22, "w") if False else None
    c.p(0, 18, "w"); c.p(1, 18, "w")
    c.shadow(0, 15)
    return c.out()


def ogre_ape():
    c = C()
    # huge humped shoulders, small head sunk low, arms down to the knuckles
    c.ell(8, 9, 7.5, 4.2, "3")
    c.ell(8, 8.5, 6.5, 3, "2")
    c.r(2, 5, 13, 6, "1")
    c.r(4, 11, 11, 17, "3")
    c.r(5, 11, 10, 15, "2")
    c.r(0, 8, 3, 17, "3"); c.r(12, 8, 15, 17, "3")
    c.r(1, 8, 2, 14, "2"); c.r(13, 8, 14, 14, "2")
    c.r(0, 18, 3, 20, "4"); c.r(12, 18, 15, 20, "4")
    c.p(1, 18, "5"); c.p(2, 18, "5"); c.p(13, 18, "5"); c.p(14, 18, "5")
    c.p(0, 20, "5"); c.p(3, 20, "5"); c.p(12, 20, "5"); c.p(15, 20, "5")
    c.r(4, 18, 6, 21, "3"); c.r(9, 18, 11, 21, "3")
    # head: hairless sloping forehead, heavy brow, jaw
    c.r(5, 6, 10, 11, "3")
    c.r(6, 5, 9, 6, "4"); c.r(5, 7, 10, 7, "4")
    c.r(6, 8, 9, 8, "5")
    c.p(6, 8, "O"); c.p(9, 8, "O"); c.p(7, 8, "y") if False else None
    c.r(6, 9, 9, 10, "5"); c.p(7, 10, "w"); c.p(8, 10, "w")
    c.shadow(0, 15)
    return c.out()


def quartz_baboon():
    c = C()
    # tail
    c.line(12, 12, 14, 8, "3"); c.line(13, 12, 15, 9, "3")
    # body
    c.ell(9, 13, 5, 3.5, "2")
    c.ell(9, 17, 4, 1, "3")
    # crystals on back
    for x, y, h in [(6, 10, 3), (8, 9, 4), (10, 10, 3), (12, 11, 3), (7, 12, 2)]:
        for k in range(h):
            c.p(x, y - k, "w" if k > 0 else "1")
            c.p(x + 1, y - k + (1 if k == h - 1 else 0), "1" if k % 2 == 0 else "3") if k < h - 1 else None
    # red rump
    c.r(12, 14, 14, 16, "4"); c.p(13, 15, "5")
    # head with red muzzle
    c.ell(4, 11, 2.6, 2.6, "2")
    c.r(1, 12, 3, 14, "4"); c.p(1, 12, "O"); c.p(1, 13, "5")
    c.p(3, 10, "y"); c.p(5, 10, "y"); c.p(3, 9, "3"); c.p(5, 9, "3")
    c.p(3, 8, "1"); c.p(4, 7, "w"); c.p(4, 8, "1")      # quartz horn
    # legs
    c.r(4, 15, 5, 20, "2"); c.r(7, 16, 7, 20, "3")
    c.r(10, 16, 12, 20, "2"); c.r(9, 16, 9, 20, "3")
    c.r(3, 21, 6, 21, "1"); c.r(9, 21, 12, 21, "1")
    c.shadow(2, 14)
    return c.out()


def madpole():
    c = C()
    # side-view tadpole fiend: huge head with gaping, toothy jaw, tapering tail
    tube(c, [(9, 12), (12, 14), (14, 18), (13, 21)], 3.0, 0.8, "2")
    c.r(12, 19, 15, 22, "3") if False else None
    c.line(15, 15, 15, 21, "3"); c.line(14, 21, 14, 23, "3")
    c.ell(6, 12, 6, 5, "2")
    c.ell(6, 10, 5, 2.6, "1")
    c.r(10, 16, 12, 17, "3"); c.r(8, 17, 9, 18, "3")   # leg buds
    # open jaw
    c.r(0, 11, 8, 15, "O")
    c.r(1, 12, 7, 14, "R")
    for x in range(0, 9, 2):
        c.p(x, 11, "w"); c.p(x, 12, "w")
        c.p(x + 1, 15, "w"); c.p(x + 1, 14, "w")
    c.r(0, 8, 3, 10, "2"); c.r(0, 16, 3, 17, "2")
    c.p(7, 9, "y"); c.p(8, 9, "y"); c.p(8, 10, "O")
    c.shadow(0, 15)
    return c.out()


def sultan_croc():
    c = C()
    # big croc, whole tile, bony plate armour in detail colors
    c.r(4, 0, 11, 6, "2"); c.r(5, 0, 10, 0, "1")
    c.p(6, 1, "O"); c.p(9, 1, "O")
    for y in (2, 4):
        c.p(3, y, "w"); c.p(12, y, "w")
    c.r(3, 6, 12, 11, "2")
    # crown of bony spikes
    c.p(3, 7, "4"); c.p(12, 7, "4"); c.p(2, 8, "4"); c.p(13, 8, "4")
    c.r(5, 6, 10, 6, "5")
    c.p(5, 7, "y"); c.p(10, 7, "y"); c.p(5, 8, "O"); c.p(10, 8, "O")
    c.r(2, 12, 13, 18, "2")
    c.r(5, 12, 10, 23, "3")
    c.r(6, 19, 9, 23, "3")
    # bony plates in rows
    for y in range(7, 22, 2):
        w = 2 if y < 18 else (1 if y < 21 else 0)
        c.r(7 - w, y, 8 + w, y, "4")
        c.r(7 - w, y + 1, 8 + w, y + 1, "5")
    c.r(1, 13, 3, 14, "4"); c.r(12, 13, 14, 14, "4")
    c.r(1, 14, 3, 14, "5"); c.r(12, 14, 14, 14, "5")
    # legs
    c.r(0, 10, 2, 12, "3"); c.r(13, 10, 15, 12, "3")
    c.r(0, 12, 1, 13, "1"); c.r(14, 12, 15, 13, "1")
    c.r(0, 17, 2, 19, "3"); c.r(13, 17, 15, 19, "3")
    c.r(0, 19, 1, 20, "1"); c.r(14, 19, 15, 20, "1")
    c.shadow(0, 15, 23)
    return c.out()


def dawnglider():
    c = C()
    for x, y in [(1, 2), (14, 3), (0, 14), (15, 12), (3, 20), (12, 20), (7, 22), (1, 9), (14, 9)]:
        c.p(x, y, "4"); c.p(x, y + 1, "5")
    # wings as filled bat triangles
    for side in (0, 1):
        pts = [(5, 7), (0, 2), (1, 8), (2, 13), (5, 12)]
        poly = pts if side == 0 else [(15 - x, y) for x, y in pts]
        for y in range(2, 14):
            xs = []
            for x in range(16):
                # point in polygon test
                ins = False
                j = len(poly) - 1
                for i in range(len(poly)):
                    xi, yi = poly[i]; xj, yj = poly[j]
                    if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                        ins = not ins
                    j = i
                if ins:
                    c.p(x, y, "3" if y > 8 else "2")
        for (x0, y0), (x1, y1) in zip(poly, poly[1:]):
            c.line(x0, y0, x1, y1, "1")
    tube(c, [(8, 4), (6, 8), (9, 12), (7, 16), (9, 20)], 2.0, 0.8, "2")
    tube(c, [(8, 4), (7, 8), (9, 12)], 0.9, 0.9, "1")
    c.r(7, 1, 9, 3, "1"); c.p(6, 2, "w"); c.p(5, 3, "w")
    c.p(8, 2, "O"); c.p(9, 2, "y")
    c.p(7, 0, "4"); c.p(9, 0, "4")
    c.p(5, 2, "4"); c.p(4, 2, "4"); c.p(3, 1, "5"); c.p(3, 3, "5")
    c.shadow(4, 12)
    return c.out()


def glowmoth():
    c = C()
    # falling dust
    for x, y in [(3, 17), (6, 19), (9, 18), (12, 20), (5, 22), (10, 22), (2, 21), (13, 17)]:
        c.p(x, y, "4")
    # wings
    c.ell(4, 8, 4, 5, "2"); c.ell(12, 8, 4, 5, "2")
    c.ell(5, 15, 3, 3.5, "3"); c.ell(10, 15, 3, 3.5, "3")
    c.ell(4, 8, 2.8, 3.8, "1"); c.ell(12, 8, 2.8, 3.8, "1")
    c.m(4, 7, "4"); c.m(3, 7, "5"); c.m(4, 8, "5"); c.m(3, 8, "4")
    c.m(5, 15, "4")
    c.mr(1, 5, 1, 9, "3")
    # fuzzy body
    c.ell(7.5, 10, 1.6, 5, "3")
    c.r(7, 7, 8, 14, "3")
    c.r(7, 8, 8, 9, "w") if False else None
    # head + feathered antennae
    c.r(7, 4, 8, 6, "3"); c.p(6, 5, "y"); c.p(9, 5, "y")
    c.line(7, 4, 5, 0, "4"); c.line(8, 4, 10, 0, "4")
    c.p(4, 1, "5"); c.p(6, 1, "5"); c.p(11, 1, "5"); c.p(9, 1, "5")
    c.shadow(3, 12, 22)
    return c.out()


def ant_queen():
    c = C()
    # smoke plume
    for x, y in [(12, 12), (13, 10), (14, 8), (12, 7), (13, 5), (11, 3)]:
        c.r(x - 1, y, x, y, "y") if False else c.p(x, y, "L")
        c.p(x - 1, y, "l")
    # huge gaster
    c.ell(8, 17, 5.5, 5.5, "2")
    c.ell(7, 16, 4, 3.5, "1")
    c.ell(10, 20, 3, 2, "3")
    for x, y in [(6, 14), (9, 15), (7, 18), (10, 18), (5, 17), (8, 21)]:
        c.p(x, y, "4"); c.p(x, y + 1, "5")
    # thorax
    c.ell(8, 10, 3, 2.6, "2"); c.r(7, 9, 8, 10, "1")
    # legs
    for (x0, y0, x1, y1) in [(5, 9, 1, 6), (5, 11, 0, 12), (6, 13, 2, 18),
                             (10, 9, 14, 6), (10, 11, 15, 12), (10, 13, 14, 18)]:
        c.line(x0, y0, x1, y1, "3")
    # head, mandibles, feelers
    c.r(6, 4, 9, 7, "2"); c.r(6, 4, 9, 4, "1")
    c.p(6, 5, "y"); c.p(9, 5, "y")
    c.p(5, 7, "w"); c.p(5, 8, "w") if False else None
    c.p(10, 7, "w"); c.p(6, 8, "w"); c.p(9, 8, "w")
    c.line(7, 4, 4, 0, "4"); c.line(8, 4, 11, 1, "4")
    c.p(4, 1, "5"); c.p(11, 0, "5")
    c.shadow(2, 13)
    return c.out()


def quillipede():
    c = C()
    path = [(3, 3), (9, 4), (12, 8), (8, 11), (4, 14), (7, 18), (12, 20)]
    # legs first (many tiny)
    pts = []
    n = 26
    for i in range(n + 1):
        t = i / n * (len(path) - 1)
        k = min(int(t), len(path) - 2)
        u = t - k
        x = path[k][0] + (path[k + 1][0] - path[k][0]) * u
        y = path[k][1] + (path[k + 1][1] - path[k][1]) * u
        pts.append((x, y))
    for i in range(1, n, 2):
        x, y = pts[i]
        c.p(round(x), round(y) + 2, "3"); c.p(round(x), round(y) - 2, "3")
        c.p(round(x) + 2, round(y), "3") if False else None
    tube(c, path, 2.2, 1.0, "2")
    tube(c, [(3.5, 2.8), (9, 3.8), (11.5, 7.5), (8, 10.5), (4.5, 13.5), (7, 17.5)], 1.0, 0.5, "1")
    # quills (detail) tufts
    for i in range(3, n - 2, 3):
        x, y = pts[i]
        c.p(round(x), round(y) - 3, "4"); c.p(round(x), round(y) - 2, "5")
        c.p(round(x) + 1, round(y) - 3, "4")
    # segment seams
    for i in range(2, n - 1, 3):
        x, y = pts[i]
        c.p(round(x), round(y) + 1, "3")
    # head
    c.r(0, 2, 2, 5, "2"); c.p(0, 3, "y"); c.p(0, 4, "O"); c.p(1, 1, "4"); c.p(0, 1, "4")
    c.p(0, 6, "w"); c.p(2, 6, "w")
    c.shadow(1, 14, 22)
    return c.out()


def snail():
    c = C()
    # foot
    tube(c, [(2, 19), (8, 19), (13, 19)], 1.9, 1.3, "2")
    c.r(2, 20, 14, 20, "3")
    c.r(1, 15, 3, 18, "2")
    # shell spiral
    c.ell(9, 12, 5.5, 5.5, "2")
    c.ell(9, 12, 4.4, 4.4, "1")
    c.ell(9, 12, 3, 3, "2")
    c.ell(9.5, 12, 1.6, 1.6, "1")
    c.line(5, 16, 11, 17, "3"); c.line(12, 8, 14, 12, "3")
    c.p(9, 12, "3")
    # eyestalks and spark arc
    c.line(2, 15, 1, 10, "2"); c.line(3, 15, 5, 9, "2")
    c.p(1, 9, "O"); c.p(5, 8, "O")
    c.p(1, 8, "w"); c.p(5, 7, "w")
    c.p(1, 14, "O") if False else None
    for x, y in [(1, 7), (2, 6), (3, 7), (4, 6), (5, 6)]:
        c.p(x, y, "4")
    c.p(2, 5, "5"); c.p(4, 5, "5"); c.p(0, 6, "5"); c.p(6, 5, "5")
    c.p(3, 3, "4"); c.p(3, 4, "5")
    c.p(1, 17, "O") if False else None
    c.shadow(1, 14)
    return c.out()


def spitting_slug():
    c = C()
    # acid drips
    for x, y in [(0, 16), (1, 18), (0, 20)]:
        c.p(x, y, "h")
    # body: long keel
    tube(c, [(3, 16), (7, 15), (11, 17), (15, 20)], 3.0, 0.8, "2")
    c.ell(8, 13, 4, 3, "1")
    c.line(5, 12, 12, 17, "1")
    c.r(2, 19, 14, 20, "3")
    c.r(3, 19, 7, 19, "3")
    # spots
    for x, y in [(6, 12), (9, 13), (11, 16), (4, 15)]:
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    # head, eyestalks
    c.ell(3, 16, 2.6, 2.6, "2")
    c.p(0, 17, "O"); c.p(1, 18, "3")
    c.line(3, 14, 2, 9, "2"); c.line(5, 14, 6, 9, "2")
    c.p(2, 8, "y"); c.p(6, 8, "y"); c.p(2, 9, "O"); c.p(6, 9, "O")
    c.shadow(0, 15)
    return c.out()


def bloated_leech():
    c = C()
    path = [(12, 4), (13, 10), (9, 15), (5, 17), (3, 14)]
    tube(c, path, 2.2, 3.6, "2")
    tube(c, [(11, 5), (12, 10), (9, 14.5)], 1.0, 1.4, "1")
    c.ell(8, 18, 4.5, 3, "2")
    c.ell(7, 17, 3, 1.7, "1")
    # reticle dots
    for x, y in [(12, 7), (12, 11), (10, 14), (7, 17), (4, 18), (9, 19)]:
        c.r(x, y, x + 1, y, "4"); c.p(x, y + 1, "5")
    c.p(13, 5, "4"); c.p(5, 14, "4")
    # curve mark
    c.line(3, 12, 4, 17, "3")
    # sucker bell mouth
    c.ell(2.5, 11, 2.7, 2.7, "3")
    c.ell(2.5, 11, 1.8, 1.8, "R")
    c.p(2, 11, "O"); c.p(3, 11, "O")
    c.p(0, 9, "w"); c.p(1, 8, "w"); c.p(4, 8, "w"); c.p(0, 13, "w") if False else None
    c.p(2, 8, "w")
    c.shadow(1, 14)
    return c.out()


def woodsprog():
    c = C()
    # moss fur body, hunched, root toes
    c.ell(8, 15, 4.8, 5, "2")
    c.ell(8, 14, 3.8, 3.5, "1")
    for x, y in [(4, 13), (11, 13), (5, 17), (10, 17), (3, 16), (12, 16)]:
        c.p(x, y, "4"); c.p(x, y - 1, "5")
    # arms
    c.line(4, 13, 2, 19, "2"); c.line(11, 13, 13, 19, "2")
    c.line(5, 13, 3, 19, "2"); c.line(10, 13, 12, 19, "2")
    c.p(1, 20, "3"); c.p(2, 20, "3"); c.p(3, 20, "3")
    c.p(12, 20, "3"); c.p(13, 20, "3"); c.p(14, 20, "3")
    # legs / root toes
    c.r(5, 19, 6, 20, "3"); c.r(9, 19, 10, 20, "3")
    c.line(4, 21, 7, 21, "3"); c.line(8, 21, 11, 21, "3")
    c.p(3, 22, "3") if False else None
    # head with huge bright eyes
    c.ell(8, 8, 4, 3.4, "2")
    c.r(5, 5, 10, 5, "1")
    c.r(4, 7, 6, 9, "y"); c.r(9, 7, 11, 9, "y")
    c.p(5, 8, "O"); c.p(10, 8, "O"); c.p(5, 7, "w") if False else None
    c.r(7, 10, 8, 10, "3")
    # leaf ears / moss tufts
    c.r(2, 4, 4, 6, "4"); c.p(2, 3, "5"); c.p(3, 4, "5")
    c.r(11, 4, 13, 6, "4"); c.p(13, 3, "5"); c.p(12, 4, "5")
    c.p(7, 3, "5"); c.p(8, 3, "5"); c.p(7, 4, "4"); c.p(8, 4, "4")
    c.shadow(3, 12)
    return c.out()


def slumberling():
    c = C()
    # boulder shaped sleeper
    c.ell(8, 15, 7.2, 5.2, "3")
    c.ell(8, 14, 6.2, 4.3, "2")
    c.ell(7, 12, 4, 2, "1")
    # little paws
    c.r(1, 18, 4, 20, "2"); c.r(11, 18, 14, 20, "2")
    c.r(1, 20, 3, 20, "1"); c.r(12, 20, 14, 20, "1")
    # snout under, ears
    c.r(1, 14, 4, 17, "2"); c.r(0, 15, 1, 16, "1"); c.p(0, 15, "O")
    c.p(4, 10, "3"); c.p(5, 10, "3"); c.p(5, 9, "3")
    # crease = closed eye, faint breath
    c.line(3, 13, 5, 13, "O")
    c.p(2, 12, "3"); c.p(3, 12, "3")
    c.line(9, 10, 12, 14, "3")
    c.p(11, 9, "4"); c.p(12, 8, "4"); c.p(13, 6, "4"); c.p(12, 5, "5")
    c.shadow(0, 15)
    return c.out()


def deep_slumberling():
    c = C()
    # towering four-chamber dorsal hump, big paws with claws
    c.ell(8, 16, 7.5, 5, "3")
    c.ell(8, 15, 6.5, 4, "2")
    for cx in (3.5, 6.5, 9.5, 12.5):
        c.ell(cx, 8 + abs(cx - 8) * 0.5, 2.2, 3.5, "2")
        c.ell(cx, 9 + abs(cx - 8) * 0.5, 1.4, 2.4, "1")
        c.p(round(cx), 8 + round(abs(cx - 8) * 0.5), "4")
    for cx in (3.5, 6.5, 9.5, 12.5):
        c.p(round(cx), round(11 + abs(cx - 8) * 0.5), "5")
        c.line(round(cx) - 1, 12, round(cx) - 1, 14, "3")
    # muzzle and shag
    c.r(2, 15, 6, 18, "2"); c.r(1, 16, 2, 17, "1"); c.p(1, 16, "O")
    c.p(4, 15, "O"); c.p(5, 15, "O")
    for x in range(0, 16, 2):
        c.p(x, 19, "3")
    # huge paws, bowed claws
    c.r(0, 18, 4, 21, "2"); c.r(11, 18, 15, 21, "2")
    c.r(0, 20, 4, 20, "1"); c.r(11, 20, 15, 20, "1")
    for x in (0, 2, 4, 11, 13, 15):
        c.p(x, 21, "w"); c.p(x, 22, "w")
    c.shadow(0, 15)
    return c.out()


def lagroot():
    c = C()
    # bulbous tuber body with a face and five clear root legs
    for (x0, y0, x1, y1) in [(5, 14, 1, 17), (6, 15, 4, 20), (8, 16, 8, 21), (10, 15, 12, 20), (11, 14, 15, 17)]:
        tube(c, [(x0, y0), (x1, y1)], 1.2, 0.8, "3")
        c.p(x1, y1 + 1, "2")
    c.ell(8, 10, 5.5, 6, "2")
    c.ell(7, 8, 3.8, 3.6, "1")
    c.line(4, 13, 11, 14, "3")
    # face
    c.r(5, 9, 6, 10, "O"); c.r(9, 9, 10, 10, "O")
    c.p(5, 9, "y"); c.p(9, 9, "y")
    c.r(6, 12, 9, 12, "O")
    c.p(6, 13, "w"); c.p(8, 13, "w")
    # thorns and sprout tubers on top
    for x in (4, 7, 10, 12):
        c.p(x, 3 if x in (7,) else 4, "3")
    c.r(6, 0, 7, 3, "4"); c.r(10, 1, 11, 3, "4"); c.p(6, 1, "5"); c.p(11, 2, "5")
    c.line(7, 4, 7, 3, "3")
    c.shadow(1, 14)
    return c.out()


def breather_base(elder):
    c = C()
    s = 1 if elder else 0
    # tail
    tube(c, [(11, 16), (14, 18 + s), (15, 21)], 1.6, 0.7, "2")
    if elder:
        c.p(14, 19, "O"); c.p(15, 20, "."); c.p(14, 20, "O")
    # hunched body, rolling scales
    top = 6 - s * 2
    c.ell(8, 13, 5, 5.5 + s * 0.5, "2")
    c.ell(7, 11.5, 3.8, 3.2, "1")
    for y in range(top + 3, 20, 2):
        for x in range(4 + (y % 4 == 0), 13, 2):
            c.p(x, y, "3")
    # swollen chin with condensate motes
    c.ell(3, 13, 2.5, 2.4, "4")
    c.p(3, 14, "5"); c.p(2, 15, "w"); c.p(1, 16, "w") if False else None
    c.p(1, 17, "w"); c.p(3, 18, "w")
    # head
    c.ell(4, 9, 2.8, 2.5, "2")
    c.r(0, 9, 3, 10, "1"); c.p(0, 9, "O"); c.r(0, 11, 3, 11, "O"); c.p(1, 11, "w"); c.p(3, 11, "w")
    c.p(4, 8, "y"); c.p(4, 9, "O"); c.r(3, 7, 5, 7, "3")
    if elder:
        # frill, horns, cracked age
        c.line(5, 6, 7, 2, "w"); c.line(6, 6, 9, 3, "w")
        c.p(4, 6, "w"); c.p(3, 5, "w")
        c.line(7, 7, 11, 5, "3"); c.line(8, 7, 12, 8, "3")
        c.line(9, 9, 10, 18, "O")
    else:
        c.p(4, 6, "3"); c.p(5, 6, "3")
    # arms + legs
    c.line(4, 15, 3, 19, "3"); c.p(2, 19, "1"); c.p(3, 19, "1")
    c.r(5, 18, 7, 21, "3"); c.r(10, 18, 12, 21, "3")
    c.r(4, 21, 7, 21, "1"); c.r(9, 21, 12, 21, "1")
    c.shadow(2, 14)
    return c.out()


def breather():
    return breather_base(False)


def elder_breather():
    c = C()
    # bigger and hunched, huge sagging throat, spiny frill, cracked tail
    tube(c, [(12, 17), (14, 19), (15, 22)], 2.0, 0.8, "2")
    c.p(14, 20, "O"); c.p(15, 21, "O") if False else None
    c.p(13, 18, "O")
    c.ell(8, 14, 6.5, 6.5, "2")
    c.ell(9, 12, 4.5, 3.8, "1")
    for y in range(8, 20, 2):
        for x in range(3 + (y % 4 == 0), 14, 2):
            c.p(x, y, "3")
    c.line(10, 8, 11, 18, "O")
    c.line(7, 13, 8, 17, "O")
    # spine frill
    for x, y in [(8, 6), (10, 6), (12, 8), (13, 10), (6, 5)]:
        c.p(x, y, "w"); c.p(x, y - 1, "w")
    # huge throat sac (detail) with motes
    c.ell(3.5, 15, 3.4, 3.4, "4")
    c.ell(3.5, 16, 2.4, 2.2, "5")
    c.p(2, 14, "w"); c.p(5, 14, "w")
    for x, y in [(1, 19), (3, 20), (5, 19), (0, 17)]:
        c.p(x, y, "w")
    # head
    c.ell(5, 9, 3.3, 3, "2")
    c.r(0, 8, 4, 9, "1"); c.p(0, 8, "O"); c.r(0, 10, 4, 10, "O"); c.p(1, 10, "w"); c.p(3, 10, "w"); c.r(0, 11, 3, 11, "3"); c.r(3, 6, 6, 6, "3")
    c.p(5, 8, "y"); c.p(5, 9, "O")
    c.p(3, 6, "3"); c.p(4, 5, "w")
    # legs
    c.r(6, 19, 8, 21, "3"); c.r(11, 19, 14, 21, "3")
    c.r(5, 21, 8, 21, "1"); c.r(10, 21, 14, 21, "1")
    c.r(0, 19, 2, 20, "3")
    c.shadow(0, 15)
    return c.out()


def sap():
    c = C()
    # bat with wings spread wide, proboscis out front
    for side in (0, 1):
        def P(x, y, side=side):
            return (x if side == 0 else 15 - x, y)
        for pts, ch in (([(0, 3), (1, 6), (3, 8), (4, 11)], "3"),):
            pass
        # membrane fill: scalloped fan between finger bones
        for y in range(3, 15):
            for x in range(0, 6):
                lim = 5 - (y - 6) * 0.35 if y > 6 else 5
                top = 3 + x * 0.5 if x < 5 else 6
                scal = 11 + ((x % 2) * 2) - x * 0.4
                if y >= 4 and y <= scal and x <= lim:
                    c.p(*P(x, y), "2" if (x + y) % 4 else "3")
        for (x0, y0, x1, y1) in [(5, 7, 0, 3), (5, 8, 0, 8), (5, 9, 1, 13), (5, 10, 3, 15)]:
            c.line(*P(x0, y0), *P(x1, y1), "1") if side == 0 else c.line(*P(x0, y0), *P(x1, y1), "1")
    # body
    c.ell(8, 11, 2.5, 4.5, "3")
    c.r(7, 8, 8, 14, "2")
    c.line(7, 15, 6, 18, "3"); c.line(8, 15, 9, 18, "3")
    # head with big ears
    c.r(6, 3, 9, 7, "2")
    c.r(5, 0, 6, 3, "3"); c.r(9, 0, 10, 3, "3")
    c.p(5, 1, "1"); c.p(10, 1, "1")
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(6, 4, "5"); c.p(9, 4, "5")
    # proboscis
    c.line(7, 7, 7, 13, "l"); c.line(8, 7, 8, 14, "w")
    c.p(7, 14, "4"); c.p(8, 15, "4")
    c.shadow(3, 12)
    return c.out()


def livid_creeper():
    c = C()
    # ringed stems
    stems = [[(2, 22), (4, 17), (3, 12), (5, 7), (4, 3)], [(8, 22), (9, 16), (8, 11), (10, 6)],
             [(13, 22), (12, 17), (14, 12), (12, 8)]]
    for st in stems:
        tube(c, st, 1.7, 1.1, "2")
    for st in stems:
        tube(c, [(x - 0.4, y) for x, y in st], 0.6, 0.5, "1")
    # bruise rings (detail)
    for x, y in [(4, 18), (3, 14), (4, 9), (9, 16), (8, 12), (9, 8), (12, 17), (13, 13), (13, 10)]:
        c.r(x - 1, y, x + 1, y, "4")
        c.p(x, y + 1, "5")
    # fruiting spurs
    for x, y in [(6, 15), (6, 8), (11, 12), (1, 9), (14, 16), (10, 19)]:
        c.r(x, y, x + 1, y + 1, "5"); c.p(x, y, "4")
    # face bloom at top
    c.ell(5, 3, 3.2, 2.6, "3")
    c.r(3, 2, 7, 3, "5")
    c.p(3, 2, "y"); c.p(6, 2, "y"); c.p(3, 3, "O"); c.p(6, 3, "O")
    c.r(4, 5, 6, 5, "4"); c.p(5, 5, "O")
    c.p(2, 0, "4"); c.p(5, 0, "4"); c.p(8, 1, "4")
    c.shadow(1, 14, 22)
    return c.out()


def sap():
    c = C()
    # bat with wings spread wide, proboscis out front
    for side in (0, 1):
        def P(x, y, side=side):
            return (x if side == 0 else 15 - x, y)
        for pts, ch in (([(0, 3), (1, 6), (3, 8), (4, 11)], "3"),):
            pass
        # membrane fill: scalloped fan between finger bones
        for y in range(3, 15):
            for x in range(0, 6):
                lim = 5 - (y - 6) * 0.35 if y > 6 else 5
                top = 3 + x * 0.5 if x < 5 else 6
                scal = 11 + ((x % 2) * 2) - x * 0.4
                if y >= 4 and y <= scal and x <= lim:
                    c.p(*P(x, y), "2" if (x + y) % 4 else "3")
        for (x0, y0, x1, y1) in [(5, 7, 0, 3), (5, 8, 0, 8), (5, 9, 1, 13), (5, 10, 3, 15)]:
            c.line(*P(x0, y0), *P(x1, y1), "1") if side == 0 else c.line(*P(x0, y0), *P(x1, y1), "1")
    # body
    c.ell(8, 11, 2.5, 4.5, "3")
    c.r(7, 8, 8, 14, "2")
    c.line(7, 15, 6, 18, "3"); c.line(8, 15, 9, 18, "3")
    # head with big ears
    c.r(6, 3, 9, 7, "2")
    c.r(5, 0, 6, 3, "3"); c.r(9, 0, 10, 3, "3")
    c.p(5, 1, "1"); c.p(10, 1, "1")
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(6, 4, "5"); c.p(9, 4, "5")
    # proboscis
    c.line(7, 7, 7, 13, "l"); c.line(8, 7, 8, 14, "w")
    c.p(7, 14, "4"); c.p(8, 15, "4")
    c.shadow(3, 12)
    return c.out()


def livid_creeper():
    c = C()
    # ringed stems
    stems = [[(2, 22), (4, 17), (3, 12), (5, 7), (4, 3)], [(8, 22), (9, 16), (8, 11), (10, 6)],
             [(13, 22), (12, 17), (14, 12), (12, 8)]]
    for st in stems:
        tube(c, st, 1.7, 1.1, "2")
    for st in stems:
        tube(c, [(x - 0.4, y) for x, y in st], 0.6, 0.5, "1")
    # bruise rings (detail)
    for x, y in [(4, 18), (3, 14), (4, 9), (9, 16), (8, 12), (9, 8), (12, 17), (13, 13), (13, 10)]:
        c.r(x - 1, y, x + 1, y, "4")
        c.p(x, y + 1, "5")
    # fruiting spurs
    for x, y in [(6, 15), (6, 8), (11, 12), (1, 9), (14, 16), (10, 19)]:
        c.r(x, y, x + 1, y + 1, "5"); c.p(x, y, "4")
    # face bloom at top
    c.ell(5, 3, 3.2, 2.6, "3")
    c.r(3, 2, 7, 3, "5")
    c.p(3, 2, "y"); c.p(6, 2, "y"); c.p(3, 3, "O"); c.p(6, 3, "O")
    c.r(4, 5, 6, 5, "4"); c.p(5, 5, "O")
    c.p(2, 0, "4"); c.p(5, 0, "4"); c.p(8, 1, "4")
    c.shadow(1, 14, 22)
    return c.out()


def kraken():
    c = C()
    tents = [[(5, 11), (2, 13), (1, 17), (3, 20), (5, 19)], [(6, 12), (4, 17), (5, 21), (8, 21)],
             [(10, 11), (13, 13), (14, 17), (12, 20), (10, 19)], [(9, 12), (11, 17), (10, 21), (7, 21)],
             [(4, 10), (1, 10), (0, 14), (2, 15)], [(11, 10), (14, 10), (15, 14), (13, 15)]]
    for t in tents:
        tube(c, t, 1.6, 0.7, "2")
    for t in tents:
        for (x, y) in t[1:-1]:
            c.p(x, y, "4"); c.p(x + 1, y + 1, "4")
        c.p(t[-1][0], t[-1][1], "5")
    # bulbous mantle
    c.ell(8, 6, 5, 6, "2")
    c.ell(7, 4, 3, 3.2, "1")
    c.ell(8, 11, 4, 1.5, "3")
    c.p(9, 9, "3"); c.line(11, 2, 12, 6, "3")
    # two big eyes
    c.r(4, 8, 6, 10, "w"); c.r(9, 8, 11, 10, "w")
    c.r(5, 9, 5, 10, "O"); c.r(10, 9, 10, 10, "O")
    c.r(4, 8, 4, 8, "y")
    c.r(7, 11, 8, 11, "O")
    c.shadow(0, 15)
    return c.out()


# ---------------------------------------------------------------- machines
def sawhander():
    c = C()
    # treads
    c.r(2, 17, 13, 21, "L")
    c.r(2, 17, 13, 17, "l")
    for x in range(3, 13, 2):
        c.p(x, 19, "l"); c.p(x, 21, "O") if False else None
    c.r(2, 21, 13, 21, "O")
    c.r(6, 18, 9, 20, "l")
    # body: chrome spine + sensor
    c.r(5, 9, 10, 16, "l"); c.r(5, 9, 6, 16, "l"); c.r(9, 9, 10, 16, "L")
    c.r(7, 9, 8, 16, "L")
    c.line(7, 10, 7, 15, "O") if False else None
    c.r(5, 5, 10, 8, "l"); c.r(5, 5, 10, 5, "w")
    c.r(6, 6, 9, 7, "O"); c.r(7, 6, 8, 7, "4")
    # arms with rotary saws (foreground role colors)
    c.r(3, 11, 5, 12, "L"); c.r(10, 11, 12, 12, "L")
    for cx in (3, 12):
        c.ell(cx, 8, 3.2, 3.2, "2")
        c.ell(cx, 8, 2, 2, "1")
        c.p(cx, 8, "O")
        for dx, dy in [(-3, 0), (3, 0), (0, -3), (0, 3), (-2, -2), (2, 2), (-2, 2), (2, -2)]:
            c.p(cx + dx, 8 + dy, "3")
    c.r(1, 12, 4, 12, "L") if False else None
    c.shadow(1, 14)
    return c.out()


def miner():
    c = C()
    # four stilt pistons
    for (x0, y0, x1, y1) in [(5, 11, 1, 16), (10, 11, 14, 16), (6, 13, 4, 18), (9, 13, 11, 18)]:
        c.line(x0, y0, x1, y1, "L")
        c.line(x1, y1, x1, y1 + 4, "l")
        c.line(x1 + (1 if x1 > 7 else -1), y1, x1 + (1 if x1 > 7 else -1), y1 + 4, "l") if False else None
        c.p(x1, y1 + 5, "O") if y1 + 5 < 22 else None
    for x, y in [(1, 20), (14, 20), (4, 22), (11, 22)]:
        c.r(x - 1, y, x + 1, y, "l")
    # hull
    c.r(3, 6, 12, 13, "2")
    c.r(3, 6, 12, 7, "1")
    c.r(3, 12, 12, 13, "3")
    c.r(2, 8, 2, 11, "3"); c.r(13, 8, 13, 11, "3")
    # open hatch with a mine
    c.r(5, 3, 10, 6, "L"); c.r(6, 4, 9, 5, "O")
    c.ell(7.5, 4, 1.8, 1.4, "4"); c.p(7, 4, "5"); c.p(8, 3, "w") if False else None
    c.p(7, 2, "5"); c.p(8, 2, "5") if False else None
    # sensor lights
    c.p(5, 10, "y"); c.p(10, 10, "y")
    c.r(6, 9, 9, 10, "l"); c.r(7, 9, 8, 10, "O")
    c.shadow(0, 15)
    return c.out()


def turret():
    c = C()
    # splayed tripod
    c.line(7, 12, 2, 21, "L"); c.line(8, 12, 13, 21, "L"); c.line(7, 13, 7, 21, "l")
    c.line(8, 13, 8, 21, "L")
    c.line(6, 12, 1, 21, "l") if False else None
    c.r(0, 21, 3, 21, "l"); c.r(12, 21, 15, 21, "l"); c.r(6, 21, 9, 21, "l")
    # head housing
    c.r(4, 6, 11, 12, "2")
    c.r(4, 6, 11, 7, "1"); c.r(4, 11, 11, 12, "3")
    c.r(10, 7, 11, 11, "3")
    # sensor eye (cyan glow)
    c.r(5, 8, 7, 10, "O"); c.r(6, 9, 6, 9, "4"); c.p(5, 8, "5") if False else None
    c.r(5, 8, 6, 9, "4"); c.p(6, 9, "w")
    # twin barrels pointing left
    c.r(0, 7, 3, 8, "l"); c.r(0, 10, 3, 11, "l")
    c.r(0, 7, 0, 8, "L"); c.r(0, 10, 0, 11, "L")
    c.r(3, 9, 4, 9, "L")
    # ammo box
    c.r(11, 5, 14, 9, "L"); c.r(11, 5, 14, 5, "l")
    c.p(12, 7, "4"); c.p(13, 7, "4")
    c.shadow(0, 15)
    return c.out()


def mortar():
    c = C()
    # hoofed kickers
    for x in (2, 10):
        c.r(x, 15, x + 3, 19, "l")
        c.r(x + 2, 15, x + 3, 19, "L")
        c.r(x - 1, 20, x + 4, 21, "O")
        c.r(x, 20, x + 3, 20, "L")
    # gyro ring
    c.ell(7.5, 14, 6, 3, "L")
    c.ell(7.5, 14, 5, 2, "l")
    c.ell(7.5, 14, 3, 1.3, "L")
    # angled mortar tube (up-right)
    for i in range(10):
        c.r(4 + i // 2, 12 - i, 8 + i // 2, 12 - i, "2")
    for i in range(10):
        c.p(4 + i // 2, 12 - i, "1"); c.p(5 + i // 2, 12 - i, "1")
        c.p(8 + i // 2, 12 - i, "3")
    c.r(8, 1, 12, 2, "L"); c.r(9, 1, 11, 1, "O")
    c.r(7, 3, 13, 3, "3")
    # fire blisters (detail)
    for x, y in [(6, 9), (9, 7), (7, 5), (10, 5), (6, 12)]:
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    c.shadow(0, 15)
    return c.out()


OVERRIDES = {"kit2": {
    "puma": puma(), "honey_skunk": honey_skunk(), "chameleon": chameleon(), "frog": frog(),
    "giant_frog": giant_frog(), "salamander": salamander(), "tortoise": tortoise(), "equimax": equimax(),
    "crow": crow(), "twohead_boar": twohead_boar(), "ogre_ape": ogre_ape(), "quartz_baboon": quartz_baboon(),
    "madpole": madpole(), "sultan_croc": sultan_croc(), "dawnglider": dawnglider(), "glowmoth": glowmoth(),
    "ant_queen": ant_queen(), "quillipede": quillipede(), "snail": snail(), "spitting_slug": spitting_slug(),
    "bloated_leech": bloated_leech(), "woodsprog": woodsprog(), "slumberling": slumberling(),
    "deep_slumberling": deep_slumberling(), "lagroot": lagroot(), "breather": breather(),
    "elder_breather": elder_breather(), "sap": sap(), "livid_creeper": livid_creeper(), "kraken": kraken(),
    "sawhander": sawhander(), "miner": miner(), "turret": turret(), "mortar": mortar(),
}}
