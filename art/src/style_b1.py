"""Style B1 - True to the creature: believable anatomy, natural posture."""
import re, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b import C


def human(c, top=3, body="2", legs="3", arms=True, sleeve=None):
    sl = sleeve or body
    c.r(6, top, 9, top + 4, "s")           # head
    c.r(6, top + 4, 9, top + 4, "S")
    c.p(7, top + 2, "O"); c.p(9, top + 2, "O")
    c.r(7, top + 5, 8, top + 5, "S")       # neck
    c.r(4, top + 6, 11, top + 12, body)    # torso
    c.r(4, top + 6, 5, top + 9, "1")
    c.r(10, top + 9, 11, top + 12, "3")
    c.r(4, top + 12, 11, top + 12, "3")
    c.r(5, top + 13, 7, 21, legs); c.r(9, top + 13, 10, 21, legs)
    c.r(8, top + 13, 8, 21, "O") if False else None
    c.r(5, 22, 7, 22, "O"); c.r(9, 22, 11, 22, "O")
    if arms:
        c.r(3, top + 6, 3, top + 12, sl); c.r(12, top + 6, 12, top + 12, sl)
        c.p(3, top + 13, "s"); c.p(12, top + 13, "s")
    c.shadow(4, 12)


def gunslinger():
    c = C()
    human(c, top=4, arms=False)
    c.r(5, 1, 10, 3, "2"); c.r(5, 3, 10, 3, "4")      # crown + band
    c.r(1, 4, 14, 4, "3"); c.r(2, 3, 13, 3, "2") if False else None
    c.r(6, 4, 9, 4, "3")
    c.r(3, 10, 12, 11, "2")                           # long coat shoulders
    c.r(2, 12, 3, 13, "2"); c.r(12, 12, 13, 13, "2")  # arms bent out
    c.r(1, 13, 2, 14, "s"); c.r(13, 13, 14, 14, "s")
    c.r(0, 11, 1, 12, "l"); c.r(0, 12, 0, 14, "N")    # pistols
    c.r(14, 11, 15, 12, "l"); c.r(15, 12, 15, 14, "N")
    c.r(4, 17, 11, 20, "2"); c.r(4, 17, 11, 17, "5")  # coat skirt, belt
    c.r(5, 21, 6, 21, "3"); c.r(9, 21, 10, 21, "3")
    c.r(7, 11, 8, 17, "4")                            # coat opening
    return c.out()


def winged():
    c = C()
    # wings behind, raised
    for y, (a, b) in enumerate([(0, 2), (0, 3), (1, 3), (1, 4), (2, 4), (3, 4), (4, 4)]):
        pass
    c.mr(0, 4, 3, 7, "4"); c.mr(0, 8, 3, 12, "4"); c.mr(1, 13, 3, 15, "5")
    c.mr(0, 2, 1, 3, "4"); c.mr(0, 6, 0, 6, "6")
    c.mr(2, 9, 3, 10, "5"); c.mr(1, 5, 2, 5, "5"); c.mr(1, 12, 3, 12, "6")
    human(c, top=4, body="2", arms=False)
    c.mr(3, 10, 3, 15, "2")
    c.p(3, 16, "s"); c.p(12, 16, "s")
    return c.out()


def horned():
    c = C()
    human(c, top=6, body="2")
    for (x, y) in [(5,6),(4,5),(3,5),(2,4),(2,3),(1,2),(1,1),(1,0)]:
        c.m(x, y, "4"); c.m(x+1, y, "5") if x < 5 else None
    c.m(5, 7, "5")
    c.r(5, 17, 10, 17, "5")
    return c.out()


def four_arms():
    c = C()
    human(c, top=3, body="2", arms=False)
    c.r(3, 9, 3, 13, "2"); c.r(12, 9, 12, 13, "2")      # upper arms
    c.r(1, 12, 3, 13, "2"); c.r(12, 12, 14, 13, "2")    # lower arms reach out
    c.p(1, 14, "s"); c.p(14, 14, "s"); c.p(0, 12, "s"); c.p(15, 12, "s")
    c.r(2, 8, 3, 8, "s"); c.r(12, 8, 13, 8, "s")
    c.p(2, 7, "s"); c.p(13, 7, "s")   # raised upper hands
    c.r(2, 9, 2, 10, "2"); c.r(13, 9, 13, 10, "2")
    c.r(4, 16, 11, 16, "5")
    return c.out()


def carapace():
    c = C()
    human(c, top=4, body="2", arms=True)
    c.r(2, 9, 13, 10, "4"); c.r(3, 8, 12, 8, "4")      # big shoulder plates
    c.r(2, 10, 13, 10, "6")
    c.r(4, 11, 11, 15, "5"); c.r(5, 12, 10, 14, "4")  # shell
    c.r(7, 11, 8, 15, "6")
    c.r(1, 9, 2, 11, "5"); c.r(13, 9, 14, 11, "5")
    c.p(2, 7, "4"); c.p(13, 7, "4"); c.p(5, 7, "4"); c.p(10, 7, "4"); c.p(7, 9, "4"); c.p(8, 9, "4")
    c.r(6, 8, 9, 8, "4"); c.p(1, 8, "6"); c.p(14, 8, "6")
    c.r(3, 11, 3, 15, "2"); c.r(12, 11, 12, 15, "2")
    return c.out()


def mehmet():
    c = C()
    human(c, top=3, body="2", arms=True)
    c.r(6, 2, 9, 2, "w")                       # white hair
    c.r(5, 3, 5, 5, "w"); c.r(10, 3, 10, 5, "w")
    c.r(6, 6, 9, 9, "w"); c.r(7, 9, 8, 10, "w")  # long beard
    c.p(7, 5, "S"); c.p(8, 5, "S")
    c.r(4, 15, 11, 15, "5")
    # hoe on right
    c.r(14, 6, 14, 20, "n"); c.r(14, 5, 15, 6, "l"); c.r(12, 5, 13, 5, "l") if False else None
    c.r(12, 5, 15, 5, "l")
    c.p(13, 14, "s"); c.p(14, 14, "s")
    c.r(3, 13, 3, 13, "2")
    return c.out()


def farmer():
    c = C()
    human(c, top=3, body="2", arms=True)
    c.r(4, 2, 11, 2, "t"); c.r(5, 1, 10, 1, "t"); c.r(3, 3, 12, 3, "t")  # straw hat
    c.r(5, 3, 10, 3, "t")
    c.p(6, 3, "e"); c.p(9, 3, "e")
    c.r(4, 15, 11, 15, "5")
    c.r(5, 19, 10, 21, "3")
    c.r(5, 22, 7, 22, "O"); c.r(9, 22, 11, 22, "O")
    # sickle at right
    c.r(13, 12, 13, 14, "n"); c.r(14, 9, 15, 10, "l"); c.p(15, 11, "l"); c.p(14, 12, "l")
    c.p(14, 8, "l"); c.p(13, 8, "l") if False else None
    c.p(13, 13, "s")
    return c.out()


def snap_body(c, bow=False):
    # hunched hyena-man facing right: long snout, toothy jaw, upright ears
    c.p(6, 0, "3"); c.r(6, 1, 7, 2, "1"); c.p(7, 1, "3")      # ears
    c.p(10, 1, "3"); c.r(9, 2, 10, 2, "1")
    c.r(5, 3, 10, 6, "1")                                      # skull
    c.r(11, 4, 15, 5, "2")                                     # upper snout
    c.r(11, 6, 15, 6, "R")                                     # open mouth
    c.r(11, 7, 14, 7, "3")                                     # lower jaw
    c.p(15, 4, "O"); c.p(15, 5, "O")                           # nose
    c.p(9, 4, "y"); c.p(10, 4, "O")                            # eye
    for x in (11, 13, 15): c.p(x, 6, "w")                      # fangs
    c.p(12, 7, "w"); c.p(14, 7, "w")
    c.r(4, 3, 5, 5, "3"); c.r(3, 5, 4, 8, "3"); c.r(2, 8, 3, 11, "3")  # mane
    c.r(6, 7, 10, 8, "1")
    c.r(4, 9, 10, 13, "1"); c.r(4, 12, 10, 13, "2")
    c.p(6, 10, "3"); c.p(8, 11, "3"); c.p(5, 12, "3"); c.p(9, 9, "3")
    c.r(11, 9, 11, 13, "2"); c.p(10, 14, "2")
    c.r(5, 14, 9, 16, "4"); c.r(5, 16, 9, 16, "5"); c.p(6, 16, "4"); c.p(8, 16, "4")
    c.r(5, 17, 6, 20, "2"); c.r(9, 17, 10, 20, "2")
    c.r(4, 21, 6, 22, "3"); c.r(9, 21, 12, 22, "3")
    c.r(4, 22, 6, 22, "O"); c.r(9, 22, 12, 22, "O")
    c.shadow(3, 13)


def snapjaw():
    c = C()
    snap_body(c)
    # long arm and club
    c.r(10, 9, 11, 12, "1"); c.r(11, 12, 12, 14, "1")
    c.r(13, 6, 14, 15, "n"); c.r(12, 4, 15, 7, "N"); c.r(13, 3, 14, 3, "N")
    c.p(12, 14, "1")
    return c.out()


def snapjaw_hunter():
    c = C()
    snap_body(c)
    c.r(6, 3, 10, 3, "5"); c.r(5, 3, 5, 3, "5"); c.p(5, 4, "4"); c.p(4, 5, "4")  # headband+feather
    c.p(4, 4, "4")
    # quiver on back
    c.r(2, 5, 3, 12, "N"); c.p(2, 4, "w"); c.p(3, 3, "w"); c.p(1, 4, "w")
    # bow held in front
    c.r(12, 8, 12, 9, "1")
    for y, x in [(5, 14), (6, 15), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 14)]:
        c.p(x, y, "n")
    c.p(15, 8, "N")
    c.line(14, 5, 14, 12, "w") if False else None
    return c.out()


def glowfish():
    c = C()
    # sparse halo of light specks (no solid frame)
    for y in range(24):
        for x in range(16):
            d = ((x - 7.5) / 8) ** 2 + ((y - 11.5) / 7) ** 2
            if 0.5 < d <= 1 and x % 3 == 0 and y % 3 == 0:
                c.p(x, y, "4")
            if 0.3 < d <= 0.5 and (x + y) % 2 == 0:
                c.p(x, y, "4")
    c.ell(8, 11.5, 5.5, 3.8, "1")
    c.r(5, 13, 11, 14, "2")
    c.r(1, 8, 3, 9, "5"); c.r(2, 10, 3, 13, "5"); c.r(1, 14, 3, 15, "5"); c.p(3, 11, "1")
    c.r(6, 7, 9, 7, "5"); c.r(7, 6, 8, 6, "5"); c.r(6, 16, 9, 16, "5")
    c.p(11, 10, "w"); c.p(12, 10, "O")
    c.p(9, 11, "3"); c.p(9, 12, "3")
    c.p(13, 12, "3")
    c.p(11, 7, "w"); c.p(12, 6, "w"); c.p(13, 5, "w")
    return c.out()


def girshling():
    c = C()
    # body: abdomen + cephalothorax, top-down, head at bottom (facing down)
    c.ell(7.5, 8.5, 3.5, 4.5, "1")
    c.r(5, 8, 10, 8, "3"); c.r(5, 10, 10, 10, "3")
    c.ell(7.5, 14, 3, 2.5, "2")
    c.r(6, 15, 9, 16, "2")
    # big chelicerae
    c.r(5, 17, 6, 19, "5"); c.r(9, 17, 10, 19, "5")
    c.p(5, 20, "4"); c.p(10, 20, "4"); c.p(6, 19, "w"); c.p(9, 19, "w")
    c.p(6, 14, "O"); c.p(9, 14, "O")
    # eight legs splayed
    for (y0, y1, x1) in [(11, 8, 0), (13, 12, 0), (15, 17, 0), (16, 21, 1)]:
        pass
    c.line(5, 11, 2, 9, "3"); c.line(2, 9, 0, 11, "3")
    c.line(5, 13, 1, 13, "3"); c.line(1, 13, 0, 16, "3")
    c.line(5, 15, 1, 17, "3"); c.line(1, 17, 0, 20, "3")
    c.line(5, 9, 3, 5, "3"); c.line(3, 5, 1, 4, "3")
    c.line(10, 11, 13, 9, "3"); c.line(13, 9, 15, 11, "3")
    c.line(10, 13, 14, 13, "3"); c.line(14, 13, 15, 16, "3")
    c.line(10, 15, 14, 17, "3"); c.line(14, 17, 15, 20, "3")
    c.line(10, 9, 12, 5, "3"); c.line(12, 5, 14, 4, "3")
    c.shadow(2, 13, 22)
    return c.out()


def dog():
    c = C()
    # side view facing right, four legs
    c.r(3, 9, 10, 14, "1")              # body
    c.r(3, 13, 10, 14, "2")
    c.r(10, 7, 13, 11, "1")             # head
    c.r(13, 9, 15, 11, "2")             # snout
    c.p(15, 9, "O"); c.p(12, 8, "O")
    c.p(14, 12, "5")                    # tongue
    c.r(10, 4, 11, 7, "3"); c.p(10, 4, "3")  # ear
    c.r(11, 12, 12, 13, "5")            # collar
    c.r(1, 8, 3, 9, "1"); c.p(0, 6, "1"); c.p(0, 7, "1"); c.p(1, 7, "1")  # tail up
    c.r(3, 15, 4, 20, "2"); c.r(5, 15, 6, 19, "3")
    c.r(8, 15, 9, 20, "2"); c.r(10, 15, 11, 19, "3")
    c.r(3, 21, 4, 21, "O"); c.r(5, 20, 6, 20, "O"); c.r(8, 21, 9, 21, "O"); c.r(10, 20, 11, 20, "O")
    c.r(5, 9, 7, 10, "3")               # saddle patch
    c.shadow(2, 12, 22)
    return c.out()


def salthopper():
    c = C()
    c.r(11, 9, 14, 13, "1"); c.r(14, 10, 14, 13, "2")
    c.p(12, 10, "O"); c.p(13, 10, "w")
    c.r(13, 14, 14, 14, "5")
    c.line(12, 9, 13, 3, "3"); c.line(13, 3, 15, 1, "3")
    c.line(13, 9, 15, 5, "3")
    c.r(8, 8, 10, 14, "2"); c.r(8, 8, 10, 9, "1")
    c.r(1, 10, 7, 14, "1"); c.r(1, 13, 7, 14, "2")
    for x in (3, 5, 7): c.r(x, 10, x, 14, "3")
    c.r(0, 11, 0, 13, "3")
    c.r(2, 9, 7, 9, "4"); c.r(3, 8, 6, 8, "5")
    c.line(7, 12, 4, 6, "5", th=2)
    c.line(4, 6, 3, 18, "6")
    c.r(2, 19, 4, 19, "6")
    c.r(2, 20, 4, 20, "O")
    c.line(9, 14, 9, 20, "3"); c.line(11, 14, 12, 20, "3")
    c.r(9, 21, 10, 21, "O"); c.r(12, 21, 13, 21, "O")
    c.shadow(0, 13, 22)
    return c.out()


def croc():
    c = C()
    # top-down 3/4, head at right, long tail left
    c.r(10, 9, 15, 13, "1")             # snout
    c.r(13, 8, 15, 8, "1")
    c.r(11, 13, 15, 14, "2")
    c.p(10, 8, "w") if False else None
    c.p(11, 8, "O"); c.p(12, 8, "O") if False else None
    c.p(13, 10, "O"); c.p(15, 9, "O")
    for x in (11, 13, 15):
        c.p(x, 14, "w")
    c.r(4, 8, 10, 14, "1")              # body
    c.r(4, 12, 10, 14, "2")
    for x in (5, 7, 9):
        c.p(x, 8, "3"); c.p(x, 9, "3")  # back ridges
    c.r(0, 10, 4, 12, "1"); c.r(0, 12, 3, 12, "2")   # tail
    c.p(0, 11, "3"); c.p(0, 12, "3")
    c.r(1, 9, 2, 9, "3") if False else None
    # legs splayed
    c.r(5, 15, 6, 17, "2"); c.r(4, 17, 6, 18, "3")
    c.r(9, 15, 10, 17, "2"); c.r(9, 17, 11, 18, "3")
    c.r(6, 5, 7, 8, "2"); c.r(5, 5, 7, 5, "3")
    c.r(10, 6, 11, 8, "2"); c.r(10, 5, 12, 5, "3")
    c.shadow(0, 15, 19)
    return c.out()


def snap2(c, bow=False):
    # tall pointed ears
    c.p(8, 0, "3"); c.r(8, 1, 8, 3, "1"); c.r(9, 2, 9, 3, "1")
    c.p(11, 1, "3"); c.r(11, 2, 11, 3, "1"); c.p(10, 3, "1")
    # head profile facing right
    c.r(8, 3, 11, 6, "1")
    c.r(12, 4, 15, 5, "2"); c.p(15, 4, "O")
    c.p(10, 4, "y"); c.p(11, 4, "O")
    c.r(12, 6, 15, 6, "R")
    c.p(12, 6, "w"); c.p(14, 6, "w")
    c.r(11, 7, 14, 7, "3"); c.p(12, 7, "w"); c.p(14, 7, "w")
    # spiky mane
    for x, y in [(7, 2), (6, 3), (7, 4), (5, 5), (7, 6), (5, 7), (6, 8), (4, 9), (5, 10), (4, 12)]:
        c.p(x, y, "3")
    c.r(7, 5, 7, 5, "3")
    c.r(8, 7, 10, 8, "1")
    rows = {9: (7, 10), 10: (7, 10), 11: (6, 9), 12: (6, 9), 13: (5, 8), 14: (5, 8), 15: (5, 7)}
    for y, (a, b) in rows.items():
        c.r(a, y, b, y, "1")
        c.r(a, y, a, y, "2")
        if y < 15:
            c.r(b - 1, y, b, y, "4")
    c.r(4, 15, 7, 17, "5"); c.r(4, 17, 7, 17, "6"); c.p(5, 17, "5")
    for x, y in [(6, 18), (5, 19), (5, 20), (6, 21)]:
        c.p(x, y, "2")
    c.r(6, 22, 8, 22, "O")
    for x, y in [(7, 18), (8, 19), (9, 20), (9, 21)]:
        c.p(x, y, "2")
    c.r(9, 22, 11, 22, "O")
    c.shadow(3, 12)


def snapjaw():
    c = C()
    snap2(c)
    c.line(10, 10, 12, 16, "1")
    c.p(12, 17, "1")
    c.line(12, 16, 14, 8, "n")
    c.r(13, 5, 15, 8, "N"); c.p(14, 4, "N")
    return c.out()


def snapjaw_hunter():
    c = C()
    snap2(c)
    c.r(8, 3, 11, 3, "5"); c.p(7, 3, "5"); c.p(6, 2, "w"); c.p(5, 1, "w"); c.p(6, 1, "4")
    c.r(2, 8, 3, 14, "N"); c.p(2, 7, "w"); c.p(3, 6, "w"); c.p(1, 7, "w")
    c.line(10, 10, 12, 13, "1")
    for x, y in [(13, 9), (14, 10), (15, 11), (15, 12), (15, 13), (15, 14), (14, 15), (13, 16)]:
        c.p(x, y, "n")
    c.line(13, 10, 13, 15, "w")
    c.p(12, 13, "s") if False else None
    return c.out()


def four_arms():
    c = C()
    human(c, top=3, body="2", arms=False)
    c.line(3, 10, 1, 7, "2", mirror=True); c.line(4, 10, 2, 7, "2", mirror=True); c.mr(3, 9, 3, 10, "2")
    c.mr(0, 5, 1, 6, "s")
    c.mr(1, 13, 3, 14, "2"); c.mr(0, 12, 0, 14, "s")
    c.r(4, 16, 11, 16, "5")
    return c.out()


def horned():
    c = C()
    human(c, top=6, body="2")
    for x, y in [(5, 8), (4, 8), (3, 7), (2, 6), (2, 5), (2, 4), (3, 3), (4, 2), (5, 2)]:
        c.m(x, y, "4")
        if (x, y) not in [(5, 2)] and c.g[y + 1][x] == ".":
            c.m(x, y + 1, "5")
    c.m(3, 4, "5"); c.m(3, 5, "5"); c.m(3, 6, "5")
    c.r(5, 17, 10, 17, "5")
    return c.out()


def salthopper():
    c = C()
    # facing left, single colour family
    c.r(1, 10, 3, 13, "1"); c.p(1, 14, "3"); c.p(2, 11, "O")
    c.r(4, 10, 7, 13, "1"); c.r(4, 13, 7, 13, "2")
    c.r(8, 11, 12, 13, "2"); c.r(8, 11, 12, 11, "1")
    c.r(13, 12, 15, 13, "2"); c.r(13, 12, 13, 12, "2")
    for x in (9, 11, 13): c.r(x, 11, x, 13, "3")
    c.line(2, 10, 0, 3, "3"); c.line(3, 10, 6, 2, "3")
    c.line(7, 13, 10, 6, "2", th=2)
    c.line(10, 6, 14, 20, "3")
    c.p(12, 13, "3") if False else None
    c.r(13, 21, 15, 21, "O")
    c.line(4, 14, 3, 20, "3"); c.line(6, 14, 6, 20, "3")
    c.r(2, 21, 3, 21, "O"); c.r(5, 21, 6, 21, "O")
    c.shadow(0, 15, 22)
    return c.out()


def dog():
    c = C()
    c.r(3, 10, 10, 14, "1"); c.r(3, 13, 10, 14, "2")
    c.r(9, 8, 11, 11, "1")                 # neck
    c.r(10, 6, 13, 10, "1")                # round head
    c.r(13, 8, 15, 10, "2"); c.p(15, 8, "O")  # short snout
    c.p(12, 7, "O"); c.p(14, 11, "5")
    c.r(10, 3, 10, 5, "3"); c.r(11, 4, 11, 5, "3"); c.r(12, 4, 12, 5, "3") if False else None
    c.r(12, 5, 12, 6, "3")
    c.r(10, 11, 11, 11, "5")
    for x, y in [(3, 10), (2, 9), (1, 8), (1, 7), (1, 6), (2, 5)]:
        c.p(x, y, "1"); c.p(x + 1 if y > 7 else x, y, "1")
    c.p(2, 5, "2"); c.p(1, 6, "2")
    c.r(3, 15, 4, 20, "2"); c.r(5, 15, 6, 19, "3")
    c.r(8, 15, 9, 20, "2"); c.r(10, 15, 11, 19, "3")
    c.r(3, 21, 4, 21, "O"); c.r(5, 20, 6, 20, "O"); c.r(8, 21, 9, 21, "O"); c.r(10, 20, 11, 20, "O")
    c.r(5, 10, 7, 11, "3")
    c.shadow(1, 12, 22)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(),
    "four_arms": four_arms(), "carapace": carapace(), "mehmet": mehmet(),
    "farmer": farmer(), "snapjaw": snapjaw(), "snapjaw_hunter": snapjaw_hunter(),
    "glowfish": glowfish(), "girshling": girshling(), "dog": dog(),
    "salthopper": salthopper(), "croc": croc(),
}
