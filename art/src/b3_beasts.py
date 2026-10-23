"""B3 beasts batch: snapjaw family (one shared base + parts), animals, insects, primates."""
from style_b3 import C, SNAP, dog as _dog, croc as _croc, salthopper as _salthopper
from style_b3 import girshling as _girshling, glowfish as _glowfish


# ---------------------------------------------------------------- snapjaws
def base():
    c = C()
    for y, row in enumerate(SNAP):
        for x, ch in enumerate(row):
            if ch != ".":
                c.p(x, y, ch)
    return c


def finish(c):
    c.shadow(1, 14)
    return c.out()


def club(c, x=13):
    c.line(x, 7, x, 20, "n")
    c.r(x - 1, 4, x + 1, 7, "N")
    c.p(x, 3, "l"); c.p(x - 1, 5, "l"); c.p(x + 1, 6, "l")
    c.p(12, 12, "s"); c.p(11, 12, "s")


def snapjaw():
    c = base(); club(c)
    return finish(c)


def snapjaw_hunter():
    c = base()
    for y, x in [(5, 14), (6, 14), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 14), (14, 14), (15, 13)]:
        c.p(x, y, "n")
    c.line(13, 5, 13, 15, "w")
    c.p(12, 11, "s"); c.p(11, 12, "s"); c.p(12, 12, "s")
    # feather cap
    c.p(5, 2, "g"); c.p(6, 2, "4"); c.p(9, 2, "4"); c.p(10, 2, "4")
    c.p(9, 0, "g"); c.p(10, 0, "g"); c.p(10, 1, "g"); c.p(11, 0, "h")
    # quiver on back
    c.r(9, 9, 10, 13, "N"); c.p(9, 8, "w"); c.p(10, 8, "w")
    return finish(c)


def snapjaw_brute():
    c = base()
    c.r(3, 8, 11, 13, "2"); c.r(4, 8, 6, 12, "1"); c.r(9, 9, 11, 13, "3")
    c.r(1, 7, 4, 9, "4"); c.r(10, 7, 13, 9, "4")       # pauldrons
    c.p(1, 7, "6"); c.p(13, 7, "6"); c.p(2, 6, "4"); c.p(12, 6, "4")
    c.r(1, 10, 2, 12, "s"); c.r(11, 10, 12, 12, "s")
    c.r(4, 13, 10, 14, "5"); c.r(4, 14, 10, 14, "4")
    c.r(4, 15, 7, 21, "2"); c.r(9, 15, 12, 21, "2"); c.r(4, 15, 5, 20, "1")
    c.r(3, 22, 7, 22, "O"); c.r(9, 22, 13, 22, "O")
    # maul
    c.line(14, 6, 14, 19, "n")
    c.r(12, 1, 15, 6, "L"); c.r(12, 1, 15, 2, "l"); c.p(13, 4, "l"); c.p(14, 3, "l")
    c.p(12, 11, "s"); c.p(13, 11, "s"); c.p(13, 12, "s")
    c.shadow(1, 15)
    return c.out()


def snapjaw_warrior():
    c = base()
    # round shield (role 4/5) on left arm, short sword right
    c.ell(2.5, 12, 3, 3.5, "4"); c.ell(2.5, 12, 2, 2.5, "5"); c.p(2, 12, "l"); c.p(3, 12, "l")
    c.p(2, 11, "L")
    c.line(13, 1, 13, 11, "l"); c.line(14, 2, 14, 10, "L"); c.p(13, 0, "w")
    c.r(11, 12, 15, 12, "y"); c.r(12, 13, 14, 13, "n")
    c.p(11, 11, "s"); c.p(12, 11, "s")
    # helmet crest
    c.r(5, 2, 9, 2, "l"); c.r(6, 1, 9, 1, "L"); c.r(7, 0, 8, 0, "4")
    c.shadow(0, 14)
    return c.out()


def snapjaw_warlord():
    c = base()
    # cape behind
    c.r(2, 8, 3, 20, "4"); c.r(11, 8, 12, 20, "6"); c.r(2, 18, 3, 20, "5")
    c.r(3, 8, 4, 12, "5")
    # feather headdress, fan of tall feathers
    c.r(4, 0, 12, 2, ".")
    for x, ch, top in [(4, "4", 1), (5, "r", 0), (6, "y", 0), (7, "4", 0), (8, "r", 0), (9, "y", 0), (10, "4", 0), (11, "r", 1)]:
        for y in range(top, 3):
            c.p(x, y, ch)
    c.r(5, 2, 11, 2, "y"); c.p(8, 2, "R")
    c.p(12, 3, "3")
    # gold collar + gem
    c.r(4, 8, 10, 8, "y"); c.p(7, 9, "R")
    # greatsword with red gem
    c.line(13, 1, 13, 12, "l"); c.line(14, 3, 14, 11, "L"); c.p(13, 0, "w")
    c.r(11, 13, 15, 13, "y"); c.p(13, 13, "R"); c.line(13, 14, 13, 16, "n")
    c.p(12, 12, "s"); c.p(11, 12, "s")
    c.shadow(1, 14)
    return c.out()


def snapjaw_spearthrower():
    c = base()
    c.line(14, 4, 11, 20, "n")                          # held spear (long)
    c.p(14, 3, "l"); c.p(14, 2, "L"); c.p(13, 3, "l"); c.p(15, 3, "l"); c.p(14, 1, "w")
    c.p(12, 12, "s"); c.p(11, 12, "s")
    # spears on back, tips over shoulder
    c.line(11, 8, 8, 1, "n") if False else None
    c.line(9, 9, 12, 1, "N")
    c.p(12, 0, "l"); c.p(9, 8, "n")
    c.line(8, 9, 10, 0, "n")
    c.p(10, 0, "l")
    c.r(5, 8, 9, 8, "4"); c.line(5, 8, 10, 13, "4")     # bandolier
    c.shadow(2, 13)
    return c.out()


def snapjaw_netter():
    c = base()
    # net spread held up: lattice
    for y in range(2, 11):
        for x in range(10, 16):
            if (x + y) % 2 == 0:
                c.p(x, y, "4")
    for x in range(10, 16):
        c.p(x, 2, "5")
    c.p(10, 2, "l"); c.p(15, 2, "l"); c.p(12, 10, "l"); c.p(14, 10, "l")
    c.line(11, 11, 11, 12, "5"); c.p(11, 12, "s"); c.p(10, 12, "s")
    c.line(12, 11, 12, 12, "4")
    # coiled rope at belt
    c.r(4, 15, 8, 15, "4"); c.r(4, 16, 8, 16, "5"); c.p(3, 15, "4")
    c.shadow(1, 14)
    return c.out()


def snapjaw_howler():
    c = base()
    # erase head, redraw thrown back (snout skyward, jaws open)
    c.r(0, 0, 15, 7, ".")
    # ears swept back to the right
    c.p(11, 2, "3"); c.p(12, 1, "3"); c.p(10, 2, "2"); c.p(11, 3, "2"); c.p(12, 2, "3"); c.p(13, 0, "3")
    # head block
    c.r(6, 3, 10, 7, "2"); c.r(6, 3, 8, 4, "1")
    c.p(9, 4, "y")                                       # eye
    # upper jaw pointing up-left
    c.r(5, 1, 7, 3, "e"); c.r(4, 0, 6, 1, "e"); c.p(3, 0, "E"); c.p(4, 0, "O")
    c.p(5, 3, "E"); c.p(5, 2, "E")
    # lower jaw dropped back
    c.r(2, 3, 4, 4, "e"); c.r(1, 4, 3, 5, "e"); c.p(0, 5, "E")
    c.r(3, 2, 4, 2, "R")                                 # open mouth
    c.p(4, 3, "R"); c.p(3, 3, "R"); c.p(2, 2, "w"); c.p(5, 1, "w"); c.p(2, 4, "w"); c.p(4, 4, "w")
    # throat + mane
    c.r(5, 5, 7, 7, "2"); c.r(8, 6, 11, 7, "3")
    c.p(7, 7, "2")
    # sound waves
    c.p(0, 1, "4"); c.p(1, 0, "4"); c.p(0, 3, "4")
    c.p(2, 0, "4") if False else None
    c.line(8, 7, 11, 8, "3") if False else None
    # raised arm
    c.line(3, 9, 2, 5, "s") if False else None
    c.shadow(1, 14)
    return c.out()


def snapjaw_feeder():
    c = base()
    # huge belly and drooping bib
    c.ell(7, 13, 5.5, 4.5, "2"); c.ell(6, 12, 3, 2.5, "1")
    c.r(3, 14, 11, 15, "5"); c.r(4, 16, 10, 16, "4")
    c.p(5, 13, "R"); c.p(6, 14, "R"); c.p(8, 12, "R")     # stains
    c.p(3, 10, "s"); c.p(3, 11, "s")
    c.r(2, 11, 3, 12, "s")
    # big bone with knobs
    c.line(13, 6, 13, 16, "w")
    c.r(12, 4, 14, 5, "w"); c.p(12, 3, "w"); c.p(14, 3, "w")
    c.r(12, 17, 14, 18, "w"); c.p(12, 19, "w"); c.p(14, 19, "w")
    c.p(12, 11, "s"); c.p(11, 11, "s"); c.p(11, 12, "s")
    c.r(6, 17, 7, 21, "2"); c.r(9, 17, 10, 21, "2")
    c.r(5, 22, 7, 22, "O"); c.r(9, 22, 11, 22, "O")
    c.shadow(1, 14)
    return c.out()


def snapjaw_gunner():
    c = base()
    # shotgun held across the body
    c.r(6, 10, 15, 10, "L"); c.r(6, 11, 15, 11, "l")
    c.r(2, 10, 5, 12, "n"); c.r(3, 12, 4, 13, "N")
    c.p(8, 12, "n"); c.r(10, 12, 11, 12, "N")
    c.p(10, 11, "s"); c.p(11, 11, "s"); c.p(5, 11, "s")
    c.p(15, 10, "O")
    # bandolier with shells
    c.line(4, 8, 10, 13, "4")
    for i, (x, y) in enumerate([(5, 9), (7, 11), (9, 12)]):
        c.p(x, y, "r")
    c.shadow(1, 14)
    return c.out()


# ---------------------------------------------------------------- animals
def dromad():
    c = C()
    # camel-person standing: long neck, hump, ringed ears
    c.r(1, 3, 6, 6, "2"); c.r(0, 5, 3, 7, "1"); c.p(0, 6, "O"); c.p(0, 7, "O")      # head+muzzle
    c.p(3, 4, "O"); c.p(2, 4, "w")
    c.r(4, 1, 5, 2, "3"); c.p(4, 0, "3"); c.p(5, 2, "y"); c.p(4, 3, "y")             # ear + gold ring
    c.r(6, 2, 7, 3, "3")
    c.r(5, 6, 7, 11, "2"); c.r(5, 6, 5, 11, "1")                                     # neck
    for y in (7, 9, 11):
        c.p(6, y, "4"); c.p(7, y - 1, "4")                                           # ink dulla
    c.r(4, 11, 11, 18, "2"); c.r(4, 11, 7, 12, "1")                                  # torso
    c.r(8, 7, 12, 11, "1"); c.r(9, 6, 11, 6, "1"); c.r(9, 8, 11, 9, "2")             # hump
    c.r(10, 12, 12, 18, "3")
    c.r(4, 13, 11, 14, "5"); c.r(4, 14, 11, 14, "4")                                 # sash
    c.p(7, 15, "4"); c.p(8, 16, "4")
    c.r(2, 12, 3, 17, "2"); c.r(2, 17, 3, 17, "s")                                   # arm
    c.r(13, 12, 14, 16, "3")                                                         # tail tuft
    c.p(13, 17, "4"); c.p(14, 17, "4")
    c.r(5, 19, 6, 21, "2"); c.r(9, 19, 10, 21, "3")
    c.r(4, 22, 7, 22, "O"); c.r(8, 22, 11, 22, "O")
    c.shadow(2, 13)
    return c.out()


def cat():
    c = C()
    # prowling, low, long; tail curling up
    c.r(5, 11, 12, 17, "2"); c.r(5, 11, 12, 12, "1")
    for x in (6, 8, 10):
        c.r(x, 13, x, 16, "4")                                                       # tabby stripes
    c.r(2, 7, 7, 12, "2"); c.r(2, 7, 5, 8, "1")                                      # head
    c.p(1, 9, "1"); c.p(1, 10, "1"); c.p(3, 9, "y"); c.p(5, 9, "y")                  # eyes (astral glow)
    c.p(2, 11, "R"); c.p(3, 12, "w")
    c.p(2, 6, "3"); c.p(2, 5, "3"); c.p(3, 6, "3"); c.p(6, 6, "3"); c.p(6, 5, "3"); c.p(5, 6, "3")  # ears
    c.p(3, 5, "4") if False else None
    c.line(12, 15, 14, 12, "2"); c.line(13, 15, 15, 12, "2"); c.line(14, 11, 14, 7, "2"); c.line(15, 11, 15, 8, "2")
    c.p(14, 6, "4"); c.p(15, 6, "4"); c.p(14, 9, "4")
    c.r(5, 18, 6, 20, "2"); c.r(11, 18, 12, 20, "3"); c.r(3, 13, 4, 19, "3")
    c.r(2, 20, 4, 20, "1"); c.r(5, 21, 7, 21, "1"); c.r(10, 21, 13, 21, "1")
    c.shadow(1, 15)
    return c.out()


def goat():
    c = C()
    # side view facing left
    c.r(5, 9, 13, 15, "2"); c.r(5, 9, 12, 10, "1"); c.r(11, 12, 13, 15, "3")
    c.r(2, 6, 6, 11, "2"); c.r(0, 9, 3, 11, "1"); c.p(0, 9, "O"); c.p(0, 10, "O")   # head + muzzle
    c.p(3, 8, "O"); c.p(2, 8, "w")
    c.r(1, 12, 2, 14, "4"); c.p(2, 15, "4")                                          # beard
    # curling horns
    c.line(5, 6, 6, 2, "w"); c.line(6, 6, 7, 2, "w"); c.line(7, 2, 9, 1, "w"); c.p(9, 2, "y")
    c.p(4, 5, "3"); c.p(3, 5, "3")
    c.line(13, 10, 15, 8, "2"); c.p(15, 7, "4")
    # legs
    for x in (5, 7, 11, 13):
        c.line(x, 16, x, 21, "3")
    c.r(5, 16, 5, 21, "2"); c.r(11, 16, 11, 21, "2")
    c.r(4, 22, 5, 22, "O"); c.r(6, 22, 7, 22, "O"); c.r(10, 22, 12, 22, "O"); c.r(13, 22, 14, 22, "O")
    c.shadow(2, 14)
    return c.out()


def bat():
    c = C()
    # wings spread, scalloped; body in the middle
    for y in range(5, 16):
        w = 7 - abs(y - 9) // 2 - (1 if y > 12 else 0)
        c.r(max(0, 7 - w), y, 5, y, "2"); c.r(10, y, min(15, 8 + w), y, "2")
    c.r(0, 6, 3, 8, "2")
    c.line(5, 8, 0, 5, "3", mirror=True); c.line(5, 9, 0, 11, "3", mirror=True); c.line(5, 10, 2, 15, "3", mirror=True)
    for x, y in [(1, 14), (3, 16), (5, 15)]:
        c.m(x, y, ".")
    c.r(6, 8, 9, 15, "1"); c.r(7, 8, 8, 8, "2")
    c.r(6, 6, 9, 9, "1"); c.mr(5, 3, 5, 6, "3"); c.mr(6, 2, 6, 5, "3")             # ears
    c.m(7, 7, "R") if False else None
    c.p(6, 7, "R"); c.p(9, 7, "R")
    c.r(7, 9, 8, 9, "w"); c.p(7, 10, "w"); c.p(8, 10, "w") if False else None
    c.r(7, 16, 8, 18, "3")
    c.line(7, 12, 7, 12, "4")
    c.mr(5, 11, 5, 11, "4")
    c.shadow(1, 14)
    return c.out()


# ---------------------------------------------------------------- bugs & crawlers
def spider():
    c = C()
    # abdomen + cephalothorax + 8 jointed legs
    legs = [(5, 9, 1, 5, 0, 10), (5, 10, 1, 9, 0, 14), (5, 12, 1, 14, 0, 19), (5, 13, 2, 17, 1, 21)]
    for (x0, y0, kx, ky, ex, ey) in legs:
        c.line(x0, y0, kx, ky, "3", mirror=True)
        c.line(kx, ky, ex, ey, "3", mirror=True)
    for (x0, y0, kx, ky, ex, ey) in legs:
        c.m(kx, ky, "2")
    c.ell(7.5, 15.5, 3.5, 4.5, "2"); c.ell(7.5, 14.5, 2, 2.5, "1")
    c.r(6, 13, 9, 13, "4"); c.r(7, 16, 8, 17, "4"); c.r(7, 19, 8, 19, "5")           # marking
    c.ell(7.5, 9.5, 2.5, 2.5, "3"); c.r(6, 8, 9, 10, "2")
    c.m(6, 8, "G"); c.m(7, 8, "G")  # eyes
    c.m(6, 7, "G") if False else None
    c.m(6, 11, "w")
    c.m(5, 11, "L") if False else None
    c.shadow(0, 15)
    return c.out()


def beetle():
    c = C()
    # blimp abdomen with blue wing covers, small head
    c.ell(7.5, 14, 6, 7, "2"); c.ell(7, 12, 3.5, 4, "1")
    c.r(7, 8, 8, 21, "3")                                                             # wing seam
    c.mr(2, 9, 6, 18, "4")
    c.mr(3, 10, 5, 16, "5") if False else None
    for y in range(10, 19, 2):
        c.mr(2, y, 6, y, "5")
    c.mr(2, 9, 3, 11, "4")
    c.ell(7.5, 5, 2.5, 2.5, "3"); c.r(6, 4, 9, 6, "2")
    c.p(6, 5, "R"); c.p(9, 5, "R")
    c.line(6, 3, 3, 0, "3", mirror=True); c.m(3, 0, "4")
    c.r(6, 7, 9, 7, "3")
    # legs
    for y, x in [(10, 0), (13, 0), (16, 1)]:
        c.line(3 + (1 if x else 0), y, x, y + 2, "3", mirror=True)
    c.shadow(0, 15)
    return c.out()


def centipede():
    c = C()
    # S-curved segmented trunk, many legs
    pts = []
    for i in range(11):
        t = i / 10
        y = 20 - i * 1.6
        x = 8 + 4.2 * __import__("math").sin(t * 6.28 - 0.3)
        pts.append((round(x), round(y)))
    for i, (x, y) in enumerate(pts):
        c.line(x - 3, y, x + 3, y, "4" if i % 2 == 0 else "5")                       # legs
    for i, (x, y) in enumerate(pts):
        c.r(x - 1, y - 1, x + 1, y + 1, "2" if i % 2 else "1")
        c.p(x, y, "1" if i % 2 else "2")
        c.p(x + 1, y + 1, "3")
    hx, hy = pts[-1]
    c.r(hx - 2, hy - 2, hx + 2, hy, "3"); c.r(hx - 1, hy - 3, hx + 1, hy - 1, "2")
    c.p(hx - 1, hy - 2, "y"); c.p(hx + 1, hy - 2, "y")
    c.p(hx - 2, hy - 4, "r"); c.p(hx + 2, hy - 4, "r"); c.p(hx - 1, hy - 3, "r"); c.p(hx + 1, hy - 3, "r")
    c.line(hx - 1, hy - 3, hx - 4, hy - 5, "4") if False else None
    tx, ty = pts[0]
    c.line(tx - 1, ty + 2, tx - 2, ty + 3, "4"); c.line(tx + 1, ty + 2, tx + 2, ty + 3, "4")
    c.shadow(0, 15)
    return c.out()


def leech():
    c = C()
    # fat worm S-curve, sucker bell at the head, dotted back
    import math
    pts = [(round(7.5 + 3.5 * math.sin(i * 0.55 + 0.4)), 21 - i) for i in range(0, 17)]
    for i, (x, y) in enumerate(pts):
        wd = 2 if i < 14 else 1
        c.r(x - wd, y, x + wd, y, "2")
        c.p(x - wd, y, "1"); c.p(x + wd, y, "3")
        if i % 3 == 1:
            c.p(x, y, "4"); 
    for i, (x, y) in enumerate(pts):
        if i % 3 == 1:
            c.p(x - 1, y, "5") if False else None
    hx, hy = pts[-1]
    c.ell(hx, hy - 1, 3.5, 2.5, "3"); c.ell(hx, hy - 1, 2, 1.5, "R"); c.p(hx, hy - 1, "O")
    for dx in (-3, 0, 3):
        c.p(hx + dx, hy - 3, "w")
    c.p(hx - 3, hy - 1, "w"); c.p(hx + 3, hy - 1, "w")
    c.shadow(2, 13)
    return c.out()


def scorpiock():
    c = C()
    # claws forward, body, tail curling up over the back, stinger
    c.line(5, 7, 2, 4, "2"); c.line(10, 7, 13, 4, "2")
    c.r(1, 1, 4, 4, "1"); c.r(11, 1, 14, 4, "1")
    c.p(2, 2, "."); c.p(13, 2, ".")
    c.p(1, 1, "4") ; c.p(14, 1, "4") ; c.p(4, 3, "3"); c.p(11, 3, "3")
    c.ell(7.5, 10, 3, 2.5, "2"); c.r(6, 8, 9, 9, "1")
    c.p(6, 9, "y"); c.p(9, 9, "y")
    c.r(5, 12, 10, 17, "2"); c.r(5, 12, 10, 13, "1")
    for y in (14, 16):
        c.r(5, y, 10, y, "3")
    c.r(7, 12, 8, 17, "1") if False else None
    # legs
    for y in (11, 13, 15, 17):
        c.line(5, y, 1, y + 2, "3"); c.line(10, y, 14, y + 2, "3")
    # tail up the back
    c.r(7, 18, 8, 19, "2"); c.r(6, 20, 9, 21, "2"); c.r(7, 21, 8, 21, "3")
    c.p(11, 19, "4")
    c.line(10, 21, 13, 21, "2") if False else None
    c.r(10, 19, 12, 21, "2"); c.p(12, 18, "2")
    c.line(13, 18, 13, 14, "4") if False else None
    c.p(13, 15, "5"); c.p(13, 16, "4"); c.p(13, 17, "5"); c.p(13, 18, "4")
    c.p(12, 14, "y"); c.p(12, 13, "y"); c.p(13, 14, "y")
    # salt motes
    c.p(0, 8, "w"); c.p(15, 10, "w"); c.p(3, 20, "w"); c.p(8, 22, "w") if False else None
    c.shadow(0, 15)
    return c.out()


def crab():
    c = C()
    # eyeless: no eyes; broad shell, big claws raised, stubby stalk nubs
    c.ell(7.5, 14, 6, 4.5, "2"); c.ell(7.5, 13, 4.5, 3, "1")
    c.r(5, 15, 10, 16, "3")
    c.mr(2, 12, 3, 12, "3")
    c.mr(6, 9, 6, 9, "3")
    # claws
    c.line(3, 10, 2, 6, "2"); c.line(4, 10, 3, 6, "2")
    c.line(12, 10, 13, 6, "2"); c.line(11, 10, 12, 6, "2")
    c.mr(0, 3, 4, 6, "1"); c.mr(0, 1, 1, 2, "1"); c.mr(3, 1, 4, 2, "1")
    c.mr(0, 0, 1, 0, "4"); c.mr(3, 0, 4, 0, "4"); c.mr(2, 3, 2, 3, "3"); c.mr(2, 4, 2, 4, "3")
    c.mr(0, 5, 4, 6, "2")
    # legs
    for y in range(12, 19, 3):
        c.line(2, y, 0, y + 4, "3", mirror=True)
    c.mr(1, 19, 1, 21, "3")
    c.m(6, 17, "4"); c.m(5, 18, "4") if False else None
    c.shadow(0, 15)
    return c.out()


def sparktick():
    c = C()
    # round bloated tick, six legs, crackling palps
    c.ell(7.5, 14, 4.5, 5.5, "2"); c.ell(7, 13, 3, 3.5, "1")
    c.ell(7.5, 8, 2, 2, "3"); c.r(6, 7, 9, 9, "3")
    c.p(6, 8, "y"); c.p(9, 8, "y")
    for i, y in enumerate((11, 14, 17)):
        c.line(4, y, 1, y - 1 + i * 2, "5", mirror=True)
        c.line(1, y - 1 + i * 2, 1, y + 2 + i * 2, "4", mirror=True)
    # palps with sparks
    c.line(6, 6, 4, 3, "4", mirror=True)
    for p in [(3, 1), (4, 2), (2, 2), (4, 0), (5, 1)]:
        c.m(p[0], p[1], "w")
    c.m(3, 1, "y"); c.m(2, 3, "y"); c.m(1, 5, "w") ; c.m(0, 8, "w") if False else None
    c.m(0, 3, "w"); c.m(1, 13, "w") if False else None
    c.m(1, 8, "w")
    c.line(7, 12, 8, 14, "y") ; c.line(8, 14, 6, 16, "y"); c.p(7, 17, "y")   # lightning on back
    c.shadow(0, 15)
    return c.out()


def ant():
    c = C()
    # head, thorax, big gaster with glowing pores and smoke wisp
    c.ell(7.5, 7, 2.5, 2.5, "2"); c.r(6, 6, 9, 8, "2"); c.r(6, 6, 9, 6, "1")
    c.p(5, 7, "y"); c.p(10, 7, "y")
    c.line(6, 9, 4, 10, "r"); c.line(9, 9, 11, 10, "r")                             # mandibles
    c.line(6, 5, 3, 3, "3"); c.line(3, 3, 3, 1, "3"); c.line(9, 5, 12, 3, "3"); c.line(12, 3, 12, 1, "3")
    c.p(3, 1, "4"); c.p(12, 1, "4")
    c.r(6, 10, 9, 13, "1"); c.r(6, 10, 9, 10, "2")                                  # thorax
    c.ell(7.5, 18, 4, 4, "2"); c.ell(7, 17, 2.5, 2.5, "1"); c.r(5, 22, 10, 22, ".")
    for (x, y) in [(6, 16), (9, 17), (7, 19), (9, 20), (5, 19)]:
        c.p(x, y, "4")
    c.r(6, 14, 9, 14, "3")
    for y in (11, 12, 13):
        c.line(5, y, 1, y + (y - 11) * 3 + 1, "3", mirror=True)
    c.mr(0, 19, 1, 20, "6") if False else None
    c.p(8, 22, "4")
    # smoke plume
    c.p(10, 14, "y"); c.p(11, 13, "y"); c.p(12, 12, "L") if False else None
    c.shadow(0, 15)
    return c.out()


def knollworm():
    c = C()
    # thick bristly segmented worm erupting from a dirt mound, beaked head
    c.r(1, 19, 14, 22, "e"); c.r(3, 17, 12, 19, "e"); c.r(2, 20, 5, 22, "E"); c.r(11, 20, 14, 22, "E")
    c.r(3, 18, 5, 18, "E"); c.p(12, 18, "E")
    import math
    for i in range(14):
        y = 18 - i
        x = round(7.5 + 2.5 * math.sin(i * 0.5))
        wd = 3 if i < 11 else 2
        col = "1" if i % 2 == 0 else "2"
        c.r(x - wd, y, x + wd, y, col)
        c.p(x - wd, y, "3") if i % 2 else None
        c.p(x + wd, y, "3")
        if i % 2 == 0:
            c.p(x - wd - 1, y, "4"); c.p(x + wd + 1, y, "4")                         # bristles
    hx = round(7.5 + 2.5 * math.sin(13 * 0.5)); hy = 5
    c.r(hx - 2, hy - 1, hx + 2, hy, "2")
    c.line(hx - 2, hy - 2, hx - 1, 0, "w"); c.line(hx + 2, hy - 2, hx + 1, 0, "w")  # split beak
    c.p(hx - 1, hy - 2, "y"); c.p(hx + 1, hy - 2, "y")
    c.p(hx - 2, hy - 1, "O"); c.p(hx + 2, hy - 1, "O")
    c.shadow(0, 15)
    return c.out()


def dragonfly():
    c = C()
    # four veined wings spread, slim body, big eyes
    for cy, rx in ((7, 7.5), (12, 6.5)):
        c.ell(3.5, cy - (1 if cy < 10 else 0), 4, 2, "5"); c.ell(12, cy - (1 if cy < 10 else 0), 4, 2, "5")
        c.line(6, cy, 1, cy, "4"); c.line(9, cy, 14, cy, "4")
        c.line(5, cy - 1, 2, cy - 1, "4") if False else None
        c.p(1, cy - 1, "4"); c.p(14, cy - 1, "4")
    c.r(7, 3, 8, 21, "2"); c.r(7, 3, 7, 21, "1"); c.r(8, 12, 8, 21, "3")
    c.r(7, 9, 8, 10, "3")
    for y in range(14, 21, 2):
        c.r(7, y, 8, y, "6")
    c.r(6, 0, 9, 3, "2"); c.mr(5, 1, 6, 3, "G")                                      # eyes
    c.mr(5, 1, 5, 1, "g")
    c.p(7, 3, "3"); c.p(8, 3, "3")
    c.m(7, 5, "3") if False else None
    c.shadow(0, 15)
    return c.out()


# ---------------------------------------------------------------- big mammals
def baboon():
    c = C()
    # hunched primate, knuckle-walking: dropped snout, brow, round ears, long arms, red rump + tail
    c.ell(7, 6, 3.5, 3.5, "2"); c.r(4, 3, 9, 7, "2")
    c.r(1, 5, 5, 9, "1"); c.r(0, 6, 1, 9, "S")                                       # dropped muzzle
    c.p(0, 7, "O"); c.p(1, 8, "O")                                                   # nostrils
    c.r(3, 4, 6, 4, "3")                                                             # heavy brow
    c.p(4, 5, "y"); c.p(5, 5, "O")
    c.mr(0, 0, 0, 0, ".")
    c.p(8, 3, "1"); c.p(9, 3, "1"); c.p(9, 4, "1")                                   # round ear
    # mantle of long fur
    c.r(4, 9, 11, 14, "1"); c.r(5, 8, 10, 9, "1"); c.r(9, 10, 12, 15, "2")
    c.r(10, 12, 12, 16, "3")
    c.line(4, 10, 4, 14, "2")
    # long arms, knuckle-walking, fingered hands
    c.r(2, 10, 3, 17, "2"); c.r(2, 18, 4, 19, "S"); c.p(2, 20, "S"); c.p(4, 20, "S"); c.p(3, 20, "S") if False else None
    c.r(6, 15, 7, 18, "2"); c.r(6, 19, 8, 19, "S"); c.p(6, 20, "S"); c.p(8, 20, "S")
    # hind legs + red rump
    c.r(10, 17, 12, 20, "2"); c.r(11, 21, 14, 21, "S"); c.r(12, 18, 13, 20, "3")
    c.r(12, 14, 14, 16, "4"); c.r(13, 15, 13, 15, "5")
    # tail
    c.line(14, 14, 15, 9, "2"); c.p(15, 8, "3")
    c.shadow(1, 15)
    return c.out()


def bear():
    c = C()
    # rearing bear facing us: round head, short snout, huge shoulders, claws up, stumpy legs
    c.ell(7.5, 4, 3.5, 3.5, "2"); c.r(5, 2, 10, 6, "2"); c.r(5, 1, 10, 2, "1")
    c.ell(4.5, 1.5, 1.2, 1.2, "3"); c.ell(11.5, 1.5, 1.2, 1.2, "3")                 # round ears
    c.r(6, 5, 9, 7, "1"); c.r(7, 5, 8, 5, "O")                                       # muzzle + nose
    c.p(5, 3, "y"); c.p(10, 3, "y"); c.p(5, 4, "O"); c.p(10, 4, "O")
    c.p(6, 7, "w"); c.p(9, 7, "w"); c.p(7, 7, "R"); c.p(8, 7, "R")                   # fangs
    # bulk
    c.r(3, 8, 12, 19, "2"); c.r(2, 9, 13, 16, "2"); c.r(1, 8, 4, 13, "1"); c.r(11, 8, 14, 13, "2")
    c.r(5, 9, 10, 15, "1") ; c.r(6, 10, 9, 14, "2")
    c.r(10, 12, 13, 19, "3")
    # arms raised with claws
    c.r(0, 6, 2, 12, "2"); c.r(13, 6, 15, 12, "3"); c.r(0, 7, 0, 11, "1")
    c.p(0, 4, "w"); c.p(1, 5, "w"); c.p(2, 5, "w"); c.p(13, 5, "w"); c.p(14, 5, "w"); c.p(15, 4, "w")
    c.r(0, 5, 2, 5, "3") if False else None
    # bark / wood chips caught in fur (detail color)
    for (x, y) in [(4, 12), (9, 11), (6, 15), (11, 15), (3, 16)]:
        c.p(x, y, "4")
    c.r(7, 8, 8, 8, "5")
    # stumpy legs
    c.r(3, 19, 6, 21, "2"); c.r(9, 19, 12, 21, "3")
    c.r(2, 22, 6, 22, "O"); c.r(9, 22, 13, 22, "O")
    c.p(3, 22, "w") if False else None
    c.shadow(1, 14)
    return c.out()


def boar():
    c = C()
    # side view facing left: wedge body, bristle ridge, big snout, tusks
    c.r(5, 9, 14, 16, "2"); c.r(6, 10, 10, 13, "1"); c.r(11, 12, 14, 16, "3")
    c.r(2, 9, 7, 15, "2"); c.r(0, 12, 3, 15, "1"); c.r(0, 13, 0, 14, "O")            # head + snout
    c.p(4, 11, "y"); c.p(4, 12, "O")
    c.p(2, 15, "w"); c.p(3, 16, "w"); c.p(1, 16, "w"); c.p(0, 15, "w")               # tusks
    c.p(4, 8, "3"); c.p(5, 7, "3"); c.p(6, 8, "3")                                   # ear
    # bristle ridge
    for x in range(5, 15):
        c.p(x, 8, "4"); 
        if x % 2: c.p(x, 7, "4")
    c.p(14, 12, "2"); c.p(15, 11, "2"); c.p(15, 10, "3")
    for x in (5, 7, 12, 14):
        c.r(x, 17, x, 21, "3")
    c.r(5, 17, 5, 21, "2"); c.r(12, 17, 12, 21, "2")
    c.r(4, 22, 5, 22, "O"); c.r(7, 22, 8, 22, "O"); c.r(11, 22, 12, 22, "O"); c.r(14, 22, 15, 22, "O")
    c.shadow(0, 15)
    return c.out()


def albino_ape():
    c = C()
    # hulking gorilla: small slumped head between huge shoulders, red eyes, knuckles down, fist to chest
    c.r(5, 3, 10, 6, "1"); c.r(6, 2, 9, 2, "1"); c.r(4, 4, 5, 5, "2"); c.r(10, 4, 11, 5, "2")
    c.r(5, 5, 10, 8, "s"); c.r(6, 4, 9, 4, "s")
    c.p(6, 5, "R"); c.p(9, 5, "R"); c.r(6, 4, 9, 4, "3") if False else None
    c.r(6, 7, 9, 7, "S"); c.p(7, 8, "O"); c.p(8, 8, "O") if False else None
    c.r(6, 4, 9, 4, "1")
    c.r(1, 8, 14, 11, "1"); c.r(0, 9, 15, 12, "1"); c.r(2, 7, 13, 8, "2")            # shoulders
    c.r(3, 12, 12, 19, "2"); c.r(5, 12, 10, 18, "1"); c.r(10, 12, 12, 19, "3")
    c.r(6, 13, 9, 14, "s")                                                           # chest patch
    c.r(0, 12, 3, 19, "2"); c.r(12, 12, 15, 19, "3"); c.r(0, 12, 1, 18, "1")         # arms
    c.r(0, 20, 3, 21, "s"); c.r(12, 20, 15, 21, "s")                                 # knuckles
    c.p(1, 22, "S") if False else None
    c.r(7, 11, 8, 12, "4") if False else None
    c.r(3, 19, 6, 21, "3"); c.r(9, 19, 12, 21, "3")                                  # short legs
    c.r(5, 22, 6, 22, "S"); c.r(9, 22, 10, 22, "S")
    for (x, y) in [(2, 14), (13, 14), (4, 10), (11, 10)]:
        c.p(x, y, "4")
    c.shadow(0, 15)
    return c.out()


def cragmensch():
    c = C()
    # hulking cave brute, upright: tiny low head with massive brow + jaw, huge arms, hide kilt, stone club
    c.r(5, 2, 10, 6, "1"); c.r(4, 1, 11, 3, "N"); c.r(4, 3, 4, 5, "N"); c.r(11, 3, 11, 4, "N"); c.p(6, 1, "n"); c.p(9, 0, "N")
    c.r(5, 4, 10, 4, "3"); c.p(6, 5, "y"); c.p(9, 5, "y")                            # brow ridge
    c.r(5, 6, 10, 7, "1"); c.r(6, 7, 9, 7, "O") ; c.p(6, 7, "w"); c.p(9, 7, "w")     # jaw w/ tusks
    c.r(2, 8, 13, 11, "2"); c.r(1, 9, 14, 12, "2"); c.r(2, 8, 13, 9, "1")            # shoulders
    c.r(4, 12, 11, 17, "2"); c.r(5, 12, 7, 16, "1"); c.r(10, 12, 11, 17, "3")
    c.r(0, 11, 3, 18, "2"); c.r(12, 11, 15, 18, "3"); c.r(0, 11, 1, 17, "1")         # arms
    c.r(0, 19, 3, 20, "1"); c.r(12, 19, 15, 20, "1") if False else None
    # club (stone head) in the right hand
    c.line(14, 8, 14, 20, "n"); c.r(12, 3, 15, 8, "L"); c.r(12, 3, 14, 4, "l"); c.p(13, 6, "O"); c.p(15, 2, "L"); c.p(12, 2, "L"); c.p(11, 5, "l")
    c.r(13, 18, 15, 19, "2")
    c.r(0, 19, 3, 20, "2")
    # hide kilt (detail color)
    c.r(4, 16, 11, 19, "5"); c.r(4, 16, 11, 16, "4"); c.p(5, 19, "4"); c.p(8, 19, "4"); c.p(10, 19, "4")
    c.r(4, 20, 6, 21, "2"); c.r(9, 20, 11, 21, "3")
    c.r(3, 22, 6, 22, "O"); c.r(9, 22, 12, 22, "O")
    c.shadow(1, 14)
    return c.out()


def crab():
    c = C()
    c.ell(7.5, 15, 5.5, 3.8, "2"); c.ell(7.5, 14, 4, 2.4, "1"); c.r(5, 17, 10, 18, "3")
    # eyestalks
    c.m(6, 11, "3"); c.m(6, 10, "3"); c.m(6, 9, "O"); c.m(5, 9, "w") if False else None
    # C-shaped pincers forward
    for sx in (0, 1):
        def P(x, y, ch, sx=sx):
            c.p(15 - x if sx else x, y, ch)
        for y in range(2, 9):
            for x in range(0, 6):
                d = ((x - 2.5) / 2.8) ** 2 + ((y - 5) / 3.2) ** 2
                if d <= 1:
                    P(x, y, "1")
        for y in range(2, 9):
            for x in range(0, 6):
                d = ((x - 3) / 1.1) ** 2 + ((y - 5) / 1.6) ** 2
                if d <= 1:
                    P(x, y, ".")
        for (x, y) in [(4, 2), (5, 3), (4, 3), (5, 4), (4, 4)]:
            P(x, y, ".")
        for (x, y) in [(2, 8), (3, 8), (1, 7), (0, 6), (1, 3), (2, 2)]:
            P(x, y, "2")
        P(5, 5, "4") if False else None
        P(0, 4, "4"); P(1, 3, "4"); P(1, 7, "4")
        # arm to body
        for (x, y) in [(4, 10), (3, 9), (4, 11), (5, 12)]:
            P(x, y, "2")
    # jointed legs, 3 per side
    for i, y in enumerate((14, 16, 18)):
        c.line(3, y, 1, y - 1, "3", mirror=True)
        c.line(1, y - 1, 0, y + 3, "3", mirror=True)
    c.shadow(0, 15)
    return c.out()


def knollworm():
    c = C()
    # dirt mound with dark hole
    c.ell(7.5, 21, 7.5, 3, "e"); c.ell(7.5, 22, 5, 1.5, "E"); c.ell(7.5, 20, 4.5, 1.8, "O")
    c.p(2, 20, "E"); c.p(13, 20, "E"); c.p(4, 18, "e"); c.p(11, 18, "e")
    # fat ringed body rising from the hole
    import math
    for i in range(11):
        y = 19 - i
        x = round(7.5 + 1.3 * math.sin(i * 0.6))
        wd = 3 if i > 1 else 3
        col = "1" if i % 2 == 0 else "2"
        c.r(x - wd, y, x + wd, y, col)
        c.p(x + wd, y, "3"); c.p(x - wd, y, "3") if i % 2 else None
        if i % 2 == 0:
            c.p(x - wd - 1, y, "4"); c.p(x + wd + 1, y, "4")
    # big round mouth with ring of teeth
    c.ell(7.5, 6, 5, 4.2, "2"); c.ell(7.5, 6, 4, 3.3, "3"); c.ell(7.5, 6, 3, 2.4, "R"); c.ell(7.5, 6, 1.4, 1.2, "O")
    for a in range(0, 360, 40):
        x = round(7.5 + 3.4 * math.cos(math.radians(a))); y = round(6 + 2.8 * math.sin(math.radians(a)))
        c.p(x, y, "w")
    c.shadow(0, 15)
    return c.out()


def cragmensch():
    c = C()
    c.r(5, 1, 10, 2, "N"); c.p(4, 2, "N"); c.p(11, 2, "N"); c.p(7, 0, "N")       # scruffy hair
    c.r(5, 3, 10, 7, "1")                                                         # face
    c.r(4, 3, 11, 4, "3")                                                         # heavy brow
    c.p(6, 5, "y"); c.p(9, 5, "y"); c.p(7, 5, "3"); c.p(8, 5, "3")                # small eyes, nose
    c.r(3, 6, 11, 7, "2"); c.r(4, 7, 10, 8, "1")                                  # jutting jaw
    c.r(5, 7, 10, 7, "O"); c.p(5, 6, "w"); c.p(10, 6, "w")                        # mouth + tusks
    c.r(2, 9, 13, 12, "2"); c.r(1, 10, 14, 13, "2"); c.r(2, 9, 13, 10, "1")       # shoulders
    c.r(4, 13, 11, 18, "2"); c.r(5, 13, 7, 17, "1"); c.r(10, 13, 11, 18, "3")
    # long arms to the knees
    c.r(0, 11, 3, 20, "2"); c.r(0, 11, 1, 19, "1"); c.r(0, 20, 3, 21, "s")
    c.r(12, 11, 15, 17, "3")
    # stone club held up in right fist
    c.line(14, 18, 14, 5, "n"); c.line(15, 18, 15, 6, "N")
    c.r(12, 0, 15, 5, "L"); c.r(12, 0, 14, 1, "l"); c.p(13, 3, "O"); c.p(11, 2, "L"); c.p(11, 4, "l")
    c.r(13, 17, 15, 19, "s")
    # hide kilt
    c.r(4, 17, 11, 20, "5"); c.r(4, 17, 11, 17, "4"); c.p(5, 20, "4"); c.p(8, 20, "4"); c.p(10, 20, "4")
    c.r(4, 21, 6, 21, "2"); c.r(9, 21, 11, 21, "3")
    c.r(3, 22, 6, 22, "O"); c.r(9, 22, 12, 22, "O")
    c.shadow(1, 14)
    return c.out()


def dragonfly():
    c = C()
    # four long thin wings in an X
    for (x0, y0, x1, y1) in [(7, 7, 0, 2), (8, 7, 15, 2), (7, 10, 0, 17), (8, 10, 15, 17)]:
        c.line(x0, y0, x1, y1, "5")
        c.line(x0, y0 + 1, x1, y1 + 1, "5")
        c.line(x0, y0 - 1 if y1 < y0 else y0 + 2, x1, y1 - 1 if y1 < y0 else y1 + 2, "4")
    # slim segmented body
    c.r(7, 5, 8, 22, "1")
    for y in range(11, 23, 2):
        c.r(7, y, 8, y, "3")
    c.r(6, 6, 9, 10, "2"); c.r(6, 6, 9, 6, "1")
    # big eyes
    c.r(5, 2, 10, 4, "G"); c.r(6, 1, 9, 1, "G"); c.p(5, 3, "g"); c.p(10, 3, "g"); c.p(7, 3, "3"); c.p(8, 3, "3")
    c.p(6, 2, "w")
    c.shadow(0, 15)
    return c.out()


def snapjaw_howler():
    c = base()
    c.r(0, 0, 15, 7, ".")
    # head block + neck
    c.r(5, 5, 9, 7, "2"); c.r(6, 4, 10, 5, "2"); c.r(6, 4, 8, 4, "1")
    c.p(7, 5, "y")
    # ears swept back (left/down), snout pointing up-right
    c.p(3, 4, "3"); c.p(4, 3, "3"); c.p(4, 5, "3"); c.p(3, 3, "3"); c.p(2, 3, "3"); c.p(5, 4, "2")
    # upper jaw up-right
    c.line(9, 4, 13, 1, "e"); c.line(9, 5, 14, 2, "e"); c.line(8, 4, 12, 1, "e")
    c.p(14, 1, "O"); c.p(15, 1, "O")
    c.line(10, 3, 12, 2, "E") if False else None
    # lower jaw dropped
    c.line(9, 6, 14, 5, "e"); c.line(9, 7, 13, 6, "e"); c.p(14, 6, "E")
    c.line(10, 5, 14, 4, "R"); c.line(10, 4, 13, 3, "R") if False else None
    c.p(11, 3, "w"); c.p(13, 2, "w"); c.p(11, 6, "w"); c.p(13, 5, "w")
    # sound marks
    c.p(12, 0, "4"); c.p(14, 0, "4"); c.p(15, 3, "4"); c.p(15, 2, "4") if False else None
    c.p(10, 0, "4") if False else None
    c.shadow(1, 14)
    return c.out()


KIT = {
    "snapjaw_hunter": snapjaw_hunter, "snapjaw_brute": snapjaw_brute, "snapjaw_warrior": snapjaw_warrior,
    "snapjaw_warlord": snapjaw_warlord, "snapjaw_spearthrower": snapjaw_spearthrower,
    "snapjaw_netter": snapjaw_netter, "snapjaw_howler": snapjaw_howler, "snapjaw_feeder": snapjaw_feeder,
    "snapjaw_gunner": snapjaw_gunner,
    "dromad": dromad, "cat": cat, "dog": _dog, "goat": goat, "bat": bat, "croc": _croc,
    "salthopper": _salthopper, "girshling": _girshling, "spider": spider, "beetle": beetle,
    "centipede": centipede, "leech": leech, "scorpiock": scorpiock, "baboon": baboon, "bear": bear,
    "boar": boar, "crab": crab, "sparktick": sparktick, "albino_ape": albino_ape,
    "cragmensch": cragmensch, "ant": ant, "knollworm": knollworm, "dragonfly": dragonfly,
}

OVERRIDES = {
    "kit": {k: f() for k, f in KIT.items()},
    "tiles": {"snapjaw": snapjaw(), "glowfish": _glowfish()},
}
