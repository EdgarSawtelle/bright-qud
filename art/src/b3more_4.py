"""B3 remaining creatures, batch more_4: odd Qud humanoids, golems, cherubs, chiliad beasts."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from functools import partial  # noqa: E402
from b3kit import (C, back, overlay, person, hat_wide, hood, helmet, hair_short, hair_wild, beard,  # noqa: E402
                   spear, sword, shield, armor, cape, staff, hammer, sickle, book, lantern, scroll, MUTATIONS)
from b3more_keys import MORE_KEYS  # noqa: E402

KEYS = MORE_KEYS[4]
HUMANOID = set()


def fin(c, a=1, b=14):
    c.shadow(a, b)
    return c.out()


def hum(name, *a, **k):
    HUMANOID.add(name)
    return person(*a, **k)


def halo_y(c, cx=8, y=0):
    """small floating gold halo (cherubs)."""
    c.r(cx - 2, y, cx + 1, y, "y")
    c.p(cx - 3, y + 1, "y"); c.p(cx + 2, y + 1, "y")
    c.r(cx - 2, y + 1, cx + 1, y + 1, ".")
    c.p(cx - 1, y, "w")


def legs(c, xs, y0, y1, ch, foot=None):
    for x in xs:
        c.r(x, y0, x, y1, ch)
        if foot:
            c.p(x, y1 + 1, foot)


# ============================================================================ humanoids
def bear_head(c):
    c.r(5, 3, 10, 7, "2")
    c.r(5, 3, 10, 3, "1")
    c.r(10, 4, 10, 7, "3")
    c.r(4, 2, 5, 3, "2"); c.r(10, 2, 11, 3, "3")      # round ears
    c.p(4, 2, "1"); c.p(5, 3, "S")
    c.r(6, 6, 9, 7, "l")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(7, 6, 8, 6, "O")
    c.p(7, 7, "L"); c.p(8, 7, "L")
    c.r(4, 4, 5, 4, "L"); c.p(10, 4, "L")


@back
def quill_mane(c):
    # a meadow of white needles in every direction behind and over the back
    for (x, y) in ((1, 2), (3, 0), (6, 0), (9, 0), (12, 1), (14, 3), (0, 6), (15, 7), (1, 10), (14, 11),
                   (0, 14), (15, 15), (2, 17), (13, 18)):
        c.line(7 if x < 8 else 8, 9 if y < 12 else 13, x, y, "w")
        c.p(x, y, "t")
    c.ell(7.5, 12, 6, 4, "L")


def barathrum():
    return hum("barathrum", quill_mane, bear_head, partial(armor, pauld="2", plate="1", shade="3", belt="5"),
               face="none", skin=("2", "3"), sash=False)


def cherub_head(c):
    c.r(5, 3, 10, 7, "l")
    c.r(5, 3, 10, 3, "w")
    c.r(10, 4, 10, 7, "L")
    c.r(6, 6, 9, 8, "w")                    # baboon muzzle
    c.r(9, 7, 9, 8, "l")
    c.p(6, 7, "O"); c.p(9, 7, "O")
    c.r(6, 4, 9, 5, "O"); c.p(6, 5, "4"); c.p(9, 5, "4")
    c.p(7, 5, "5"); c.p(8, 5, "5")


@back
def cherub_wings(c):
    c.r(0, 6, 4, 13, "4"); c.r(11, 6, 15, 13, "5")
    c.r(1, 3, 3, 6, "4"); c.r(12, 3, 14, 6, "5")
    c.m(0, 10, "6"); c.m(2, 13, "6"); c.m(3, 14, "6")
    c.line(4, 9, 0, 6, "w", mirror=True)


def tail_pip(c):
    c.line(10, 19, 14, 17, "L"); c.p(15, 16, "4")
    c.p(14, 17, "l")


def cherub_baboon_mechanical():
    return hum("cherub_baboon_mechanical", cherub_wings, cherub_head,
               lambda c: halo_y(c, 8, 0), tail_pip, face="none", skin=("l", "L"), body="1", lite="w", dark="2",
               sash=True, trim="4")


def rock_shelf(c):
    c.r(3, 0, 11, 2, "2"); c.r(3, 0, 6, 0, "1"); c.r(10, 1, 11, 2, "3"); c.r(2, 2, 4, 3, "3")
    c.p(5, 3, "L"); c.p(10, 3, "L")
    c.r(2, 9, 6, 11, "2"); c.r(2, 9, 4, 9, "1"); c.r(5, 11, 6, 11, "3")     # shoulder shelf
    c.r(10, 10, 12, 12, "3"); c.p(11, 10, "2")
    c.p(1, 10, "3")
    c.line(5, 12, 10, 16, "w"); c.line(6, 12, 10, 15, "L")      # wire
    for x, y, ch in ((6, 13, "4"), (8, 14, "5"), (9, 15, "4"), (7, 12, "5"), (5, 10, "4"), (4, 11, "5"), (6, 11, "6")):
        c.p(x, y, ch)
    c.p(1, 12, "4"); c.p(1, 13, "5"); c.p(2, 14, "4")
    c.r(5, 8, 10, 8, "5"); c.p(7, 9, "4")                      # shawl at neck


def cragmensch():
    return hum("cragmensch", rock_shelf, face="face", skin=("L", "l"), body="3", lite="2", dark="3", sash=False)


def dromad_head(c):
    c.r(5, 3, 10, 7, "t")
    c.r(10, 3, 10, 7, "n")
    c.r(6, 6, 10, 7, "t")                     # long camel muzzle
    c.r(10, 6, 11, 7, "t")
    c.p(11, 7, "n"); c.p(10, 6, "O")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(5, 4, "w"); c.p(6, 4, "O"); c.p(9, 4, "O")           # lashes
    c.mr(4, 2, 4, 4, "n")                                      # ears
    c.m(4, 4, "y"); c.m(4, 3, "y")
    c.r(6, 8, 9, 8, "t")                                       # neck
    c.r(7, 9, 8, 9, "n")
    c.p(7, 8, "4"); c.p(9, 8, "5")


@back
def hump(c):
    c.ell(4, 11, 3.5, 4.5, "t"); c.ell(3.5, 10.5, 2, 3, "w")


def dromad_caravan_guard():
    return hum("dromad_caravan_guard", hump, dromad_head, partial(armor, pauld="l", plate="1", shade="3"),
               shield, spear, face="none", skin=("t", "n"), sash=False)


def spines_head(c):
    c.mr(4, 2, 5, 3, "4")
    for x, y in ((6, 2), (7, 1), (8, 0), (9, 1), (10, 2)):
        c.p(x, y, "4" if x % 2 else "5")
    c.line(5, 3, 3, 0, "w"); c.line(10, 3, 12, 0, "w")
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(6, 4, "O")


def godling_hooves(c):
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.r(5, 19, 5, 21, "3"); c.r(10, 19, 10, 21, "3")
    # prismatic aura of affect
    for x, y, ch in ((2, 7, "4"), (13, 7, "5"), (1, 14, "5"), (14, 14, "4"), (3, 19, "4"), (12, 19, "5")):
        c.p(x, y, ch)
    c.r(4, 15, 11, 15, "4")


def godling():
    w = overlay(MUTATIONS["Wings"][1], behind=True)
    return hum("godling", w, spines_head, godling_hooves, face="none", skin=("m", "M"), body="2", sash=True,
               trim="5")


def stitches(c):
    c.line(5, 4, 9, 6, "O"); c.line(6, 4, 8, 5, "O")
    for x, y in ((6, 4), (8, 5), (7, 12), (9, 13)):
        c.p(x, y, "O")
    c.p(6, 6, "O"); c.r(6, 7, 9, 7, "O"); c.p(7, 6, "3")      # sewn mouth
    c.p(4, 3, "l"); c.p(11, 3, "l")                            # neck bolts
    c.p(4, 8, "l"); c.p(11, 8, "l")
    c.r(5, 12, 6, 14, "3"); c.line(5, 11, 9, 15, "O")
    c.r(3, 15, 4, 17, "2"); c.r(11, 15, 12, 17, "3")           # long fists
    c.p(3, 17, "3")


def golem_human():
    return hum("golem_human", stitches, face="none", skin=("2", "3"), body="1", lite="2", dark="3", sash=False)


def bubble(c):
    c.ell(7.5, 5, 5.3, 5.3, "c")
    c.ell(7.5, 5, 4.3, 4.3, ".")
    c.p(4, 3, "w"); c.p(4, 4, "w"); c.p(5, 2, "w")
    c.p(11, 7, "b")
    c.r(5, 9, 10, 9, "c")
    c.r(3, 3, 5, 4, "g"); c.r(10, 8, 12, 12, "G"); c.line(11, 2, 13, 5, "g")     # kelp
    c.line(4, 10, 3, 14, "G"); c.p(2, 9, "g")


def hermit():
    def head(c):
        c.r(6, 4, 9, 7, "s"); c.r(9, 4, 9, 7, "S")
        c.p(6, 5, "O"); c.p(9, 5, "O"); c.r(6, 7, 9, 7, "w")
    return hum("hermit", head, bubble, face="none", skin=("s", "S"), body="3", lite="2", dark="3", sash=False)


def ladder_braids(c):
    for x in (4, 11):
        c.r(x, 4, x, 14, "N")
        for y in (5, 7, 9, 11, 13):
            c.p(x - 1, y, "n") if x < 8 else c.p(x + 1, y, "n")
    c.r(5, 3, 10, 3, "N")


def paladin_helm(c):
    c.r(5, 2, 10, 3, "l")
    c.p(6, 2, "w")
    c.r(7, 1, 8, 1, "5"); c.p(7, 0, "4"); c.p(8, 0, "4")
    c.r(4, 5, 5, 6, "L")


def mechanimist_temple_paladin():
    return hum("mechanimist_temple_paladin", cape, ladder_braids, partial(armor, pauld="4", plate="l",
               shade="L", belt="5"), hammer, face="face", sash=False, trim="4")


def big_head(c):
    c.ell(7.5, 4.5, 6.8, 4.8, "2")
    c.r(2, 2, 13, 3, "2")
    c.r(2, 2, 7, 2, "1")
    c.r(11, 4, 13, 8, "3")
    for x, y in ((4, 1), (9, 2), (11, 4), (3, 5), (6, 7), (12, 6), (5, 3)):
        c.p(x, y, "g")                                    # warts and freckles
    c.p(4, 5, "G"); c.p(10, 6, "G")
    c.p(5, 4, "O"); c.p(6, 4, "O"); c.p(9, 4, "O"); c.p(10, 4, "O")
    c.p(5, 5, "y"); c.p(10, 5, "y")
    c.r(6, 7, 9, 8, "3"); c.r(7, 7, 8, 7, "O")
    c.r(6, 9, 9, 11, "g"); c.p(7, 12, "G"); c.p(8, 13, "g"); c.p(7, 15, "g")      # wattle + sauce


def nephilim_agolgut():
    return hum("nephilim_agolgut", big_head, face="none", skin=("2", "3"), body="3", lite="2", dark="3",
               sash=False)


def hunch(c):
    c.ell(4, 11, 4.5, 4, "3")
    c.r(1, 12, 3, 14, "2")


def tatter_chin(c):
    c.r(6, 7, 9, 7, "w"); c.r(7, 8, 8, 10, "l"); c.p(6, 8, "L"); c.p(9, 8, "w"); c.p(8, 11, "L")
    c.p(5, 6, "l"); c.p(10, 6, "L")
    for x in (4, 6, 9, 11):
        c.p(x, 20, "O"); c.p(x, 21, "3")                  # tattered hem
    c.p(3, 21, ".")


def rummager():
    return hum("rummager", hunch, hood, tatter_chin, partial(lantern, glow="4"), face="face", sash=False,
               trim="5")


def leaf_hat(c):
    c.r(2, 1, 13, 1, "g")
    c.r(1, 2, 14, 3, "g"); c.r(0, 3, 15, 3, "G")
    c.r(5, 0, 10, 0, "g")
    c.line(7, 0, 8, 3, "h")
    c.p(0, 4, "G"); c.p(1, 4, "g"); c.p(14, 4, "G"); c.p(15, 5, "G"); c.p(0, 5, "g")


def vinereaper(c):
    c.line(13, 6, 13, 22, "n")
    c.line(13, 6, 13, 3, "n")
    c.line(13, 3, 15, 3, "L"); c.line(15, 3, 15, 7, "l"); c.p(14, 4, "l")
    c.p(12, 8, "g"); c.p(14, 10, "g"); c.p(12, 13, "h")                 # vines
    c.p(12, 15, "s"); c.p(11, 15, "s")


def slynth_joppa():
    def eyes(c):
        c.p(6, 5, "y"); c.p(9, 5, "y"); c.p(6, 6, "O") if False else None
    return hum("slynth_joppa", leaf_hat, eyes, vinereaper, face="face", skin=("h", "g"), body="2", lite="1",
               dark="3", sash=True, trim="4")


def sigil_tabard(c):
    c.r(6, 10, 9, 18, "4"); c.r(9, 10, 9, 18, "5")
    c.p(7, 13, "6"); c.p(8, 12, "6"); c.p(8, 14, "6"); c.p(7, 15, "6") if False else None
    c.p(7, 12, "6"); c.p(8, 13, "6"); c.p(7, 14, "6")
    c.r(3, 9, 4, 11, "l"); c.r(11, 9, 12, 11, "L")      # pauldrons


def templar_helm(c):
    c.r(5, 2, 10, 7, "l"); c.r(6, 1, 9, 1, "l"); c.r(10, 2, 10, 7, "L")
    c.r(5, 7, 10, 7, "L")
    c.r(6, 5, 9, 5, "O"); c.p(8, 4, "O"); c.p(8, 6, "O")
    c.p(6, 3, "L"); c.p(7, 2, "4"); c.p(8, 3, "4"); c.p(7, 4, "4") if False else None   # rhombus
    c.p(7, 3, "5"); c.p(7, 2, "L")
    c.p(6, 1, "w"); c.p(7, 0, "L")


def templar():
    return hum("templar", templar_helm, sigil_tabard, sword, face="none", body="1", lite="2", dark="3",
               sash=False)


def warden_hood(c):
    c.r(5, 1, 10, 2, "2")
    c.r(4, 3, 11, 4, "2"); c.r(4, 5, 4, 8, "2"); c.r(11, 5, 11, 8, "3")
    c.r(5, 2, 7, 2, "1")
    c.r(6, 6, 9, 7, "w"); c.p(6, 5, "O"); c.p(9, 5, "O")


def pike(c):
    c.line(13, 2, 13, 22, "n")
    c.r(12, 0, 14, 2, "l"); c.p(13, 0, "w"); c.p(13, 3, "L")
    c.p(12, 15, "s"); c.p(11, 15, "s"); c.p(12, 14, "s")
    c.p(4, 16, "s")


def warden():
    return hum("warden", cape, warden_hood, partial(armor, pauld="3", plate="2", shade="3", belt="5"),
               pike, face="none", sash=False)


# ============================================================================ creatures
def ancient_clam():
    c = C()
    c.ell(8, 6, 7, 5, "1"); c.ell(8, 7, 6, 4, "2")                 # raised back shell
    for x in (3, 5, 8, 11, 13):
        c.line(8, 9, x, 2, "3")
    c.r(1, 5, 14, 5, "1") if False else None
    c.ell(8, 15, 7.5, 5, "2"); c.ell(8, 15, 6.4, 3.8, "O")
    c.ell(8, 15.5, 4.3, 2.4, "m"); c.ell(8, 15, 2.5, 1.2, "M")     # soft organ
    for x, y in ((6, 14), (9, 13), (11, 16), (5, 16)):
        c.p(x, y, "w")
    c.p(8, 15, "y"); c.p(7, 15, "y")
    for x in (2, 4, 8, 11, 13):
        c.line(x, 19, x, 20, "3")
    c.r(1, 19, 14, 20, "3") if False else None
    c.r(2, 20, 13, 20, "3")
    c.p(3, 13, "1"); c.p(12, 13, "1"); c.p(1, 15, "1"); c.p(14, 15, "1")
    c.p(3, 2, "5"); c.p(13, 4, "4"); c.p(6, 17, "4")
    return fin(c, 1, 14)


def clam():
    c = C()
    c.ell(8, 8, 6, 4, "2"); c.ell(8, 8.5, 5, 3, "1")
    for x in (4, 6, 8, 10, 12):
        c.line(8, 11, x, 5, "3")
    c.ell(8, 15, 7, 4.5, "2"); c.ell(8, 15, 5.8, 3.4, "3")
    c.ell(8, 15, 3.5, 2, "S"); c.ell(8, 15, 1.6, 1, "s")           # portal muscle
    c.r(2, 19, 13, 19, "3")
    for x, y in ((3, 13), (12, 14), (11, 18), (4, 18), (7, 4), (10, 6)):
        c.p(x, y, "g")
    c.p(6, 15, "w")
    return fin(c, 1, 14)


def bone_worm_corpse():
    c = C()
    pts = [(2, 8), (5, 10), (8, 12), (11, 14), (9, 17), (5, 18), (3, 20)]
    for i, (x, y) in enumerate(pts):
        c.ell(x, y, 3.3, 2.4, "2" if i % 2 else "1")
        c.ell(x + 1, y + 0.7, 2.3, 1.3, "3")
        c.p(x - 2, y - 2, "w"); c.p(x + 2, y + 2, "w")
    c.r(0, 7, 2, 9, "1"); c.p(1, 8, "O"); c.p(0, 7, "O") if False else None  # crushed head
    c.p(2, 7, "O"); c.p(1, 9, "O")
    c.p(13, 13, "w"); c.p(14, 15, "w"); c.p(12, 12, "w")
    return fin(c, 1, 14)


def cherub_baetyl():
    c = C()
    halo_y(c, 8, 0)
    c.line(8, 3, 4, 9, "1"); c.line(8, 3, 12, 9, "1")
    c.line(4, 9, 8, 15, "2"); c.line(12, 9, 8, 15, "3")
    for y in range(4, 15):
        w = 5 - abs(y - 9)
        c.r(8 - w, y, 8 + w, y, "2")
        c.r(8 - w, y, 8 - w + 1, y, "1"); c.r(8 + w - 1, y, 8 + w, y, "3")
    c.r(6, 8, 10, 10, "O"); c.r(7, 9, 9, 9, "4"); c.p(8, 9, "w")
    c.p(2, 6, "l"); c.p(13, 12, "L"); c.p(1, 12, "l"); c.p(14, 5, "L")
    c.m(3, 17, "x") if False else None
    c.r(5, 18, 10, 18, "x")
    return fin(c, 2, 13)


def cherub_crab():
    c = C()
    halo_y(c, 8, 4)
    c.ell(8, 14, 5, 3.4, "2"); c.ell(8, 13, 4, 2, "1"); c.r(10, 15, 12, 16, "3")
    c.m(6, 10, "O"); c.m(6, 11, "l")
    c.m(2, 7, "2"); c.m(3, 7, "2"); c.m(2, 8, "1"); c.m(1, 9, "2"); c.m(1, 10, "3")      # claws
    c.m(3, 6, "3") if False else None
    c.line(5, 12, 2, 8, "2", mirror=True)
    c.m(0, 6, "1"); c.m(0, 7, "1"); c.m(1, 6, "O") if False else None
    for y in (15, 17, 19):
        c.line(4, y, 1, y + 3, "L", mirror=True)
    c.m(8, 14, "4") if False else None
    c.r(7, 13, 8, 14, "4")
    return fin(c, 1, 14)


def cherub_flower():
    c = C()
    halo_y(c, 8, 0)
    c.r(8, 10, 8, 20, "g"); c.line(8, 16, 4, 14, "g"); c.line(8, 18, 12, 16, "G")
    c.m(4, 14, "h")
    c.ell(8, 8, 5, 4.5, "2")
    for ang in range(0, 360, 60):
        import math
        c.ell(8 + 4.8 * math.cos(math.radians(ang)), 8 + 4 * math.sin(math.radians(ang)), 2, 1.8, "1")
    c.ell(8, 8, 2.2, 2, "4"); c.p(8, 8, "w"); c.p(7, 8, "5")
    c.r(6, 20, 10, 20, "G"); c.line(6, 21, 3, 22, "G"); c.line(10, 21, 13, 22, "G")
    return fin(c, 2, 13)


def cherub_insect():
    c = C()
    halo_y(c, 8, 0)
    c.ell(4, 9, 3.5, 5, "w") if False else None
    for s in (0, 1):
        x0 = 4 if s == 0 else 11
        c.ell(x0 - (1 if s == 0 else -1), 9, 3, 4.8, "4")
        c.ell(x0 - (1 if s == 0 else -1), 9, 1.7, 3.3, "5")
    c.ell(8, 8, 2.3, 2.6, "2")                                   # thorax
    c.ell(8, 15, 2.6, 4.5, "1"); c.r(7, 14, 9, 14, "3"); c.r(7, 17, 9, 17, "3"); c.r(8, 18, 8, 20, "3")
    c.ell(8, 4.5, 2, 1.6, "l"); c.p(7, 4, "4"); c.p(9, 4, "4")
    for y in (10, 12, 14):
        c.line(6, y, 2, y + 5, "L", mirror=True)
    return fin(c, 2, 13)


def cherub_reptile():
    c = C()
    halo_y(c, 4, 4)
    c.ell(8, 14, 4.8, 2.8, "2"); c.ell(8, 13, 4, 1.4, "1")
    c.ell(3, 12, 2.6, 2, "2"); c.r(0, 12, 1, 13, "1"); c.p(2, 11, "4"); c.p(0, 13, "O")
    c.line(12, 14, 15, 17, "2"); c.line(13, 17, 14, 20, "3"); c.p(14, 20, "1")
    for x in (6, 8, 10, 12):
        c.p(x, 11, "4")
    legs(c, (4, 5), 16, 19, "3"); legs(c, (11, 12), 16, 19, "3")
    c.r(3, 20, 6, 20, "1"); c.r(10, 20, 13, 20, "1")
    c.line(7, 10, 9, 12, "l") if False else None
    return fin(c, 1, 15)


def cherub_swine():
    c = C()
    halo_y(c, 6, 4)
    c.ell(9, 14, 5.2, 3.6, "2"); c.ell(9, 12.5, 4.4, 1.6, "1")
    c.ell(3.5, 13, 3, 2.8, "2")
    c.r(0, 13, 1, 15, "4"); c.p(0, 14, "O"); c.p(3, 11, "O")
    c.r(3, 9, 4, 10, "3"); c.p(5, 10, "3")
    c.p(14, 12, "3"); c.p(15, 11, "l"); c.p(14, 10, "l"); c.p(15, 9, "l")
    legs(c, (5, 6), 17, 20, "3"); legs(c, (12, 13), 17, 20, "3")
    c.r(5, 21, 6, 21, "O"); c.r(12, 21, 13, 21, "O")
    c.p(9, 14, "4"); c.p(10, 14, "5")
    return fin(c, 2, 15)


def cherub_vine():
    c = C()
    halo_y(c, 8, 0)
    pts = [(8, 21), (5, 18), (10, 15), (5, 12), (9, 9)]
    for a, b in zip(pts, pts[1:]):
        c.line(a[0], a[1], b[0], b[1], "2"); c.line(a[0] + 1, a[1], b[0] + 1, b[1], "3")
    c.ell(8, 6, 2.6, 2.6, "1"); c.p(7, 6, "O"); c.p(9, 6, "O"); c.r(7, 7, 9, 7, "3")
    for x, y in ((4, 16), (11, 13), (4, 10), (10, 18)):
        c.p(x, y, "l")
    c.r(2, 17, 4, 18, "g"); c.r(11, 14, 13, 15, "G"); c.r(3, 11, 4, 12, "g"); c.p(10, 19, "h")
    c.r(6, 21, 10, 21, "3")
    return fin(c, 3, 12)


def dog():
    c = C()
    c.ell(9, 14, 5.5, 3, "2"); c.ell(9, 12.5, 4.5, 1.4, "1"); c.r(11, 16, 13, 16, "3")
    c.ell(3.5, 11, 2.6, 2.3, "2"); c.r(0, 11, 2, 12, "1"); c.p(0, 11, "O"); c.p(2, 10, "3")
    c.p(3, 10, "O")
    c.line(3, 8, 4, 9, "3"); c.r(4, 8, 4, 9, "3"); c.p(5, 9, "3"); c.p(3, 8, "3")        # perked crescent ears
    c.p(5, 8, "3")
    c.line(14, 12, 15, 9, "2"); c.p(15, 8, "1"); c.p(14, 11, "2")
    legs(c, (4, 5), 16, 20, "2"); legs(c, (7, 8), 16, 20, "3")
    legs(c, (11, 12), 16, 20, "2"); legs(c, (13,), 16, 20, "3")
    c.r(3, 21, 5, 21, "1"); c.r(7, 21, 9, 21, "1") if False else None
    c.r(11, 21, 13, 21, "1")
    c.p(10, 15, "5"); c.p(2, 13, "w")
    return fin(c, 1, 15)


def goat():
    c = C()
    c.ell(9, 13.5, 5.5, 3.6, "2"); c.ell(9, 12, 4.5, 1.5, "1"); c.r(12, 15, 14, 17, "3")
    c.ell(3.5, 10, 2.4, 2.3, "2"); c.r(1, 11, 2, 13, "1"); c.p(2, 13, "w"); c.p(1, 10, "O"); c.p(3, 9, "O")
    c.line(3, 8, 5, 4, "w"); c.line(4, 8, 7, 5, "w"); c.p(5, 3, "t"); c.p(7, 4, "t")      # horns
    c.p(5, 9, "3")
    c.r(14, 11, 15, 12, "3")
    legs(c, (4, 5), 16, 20, "2"); legs(c, (7, 8), 16, 20, "3")
    legs(c, (11, 12), 16, 20, "2"); legs(c, (13,), 16, 20, "3")
    c.r(4, 21, 5, 21, "O"); c.r(11, 21, 13, 21, "O")
    c.p(12, 5, "O"); c.p(14, 7, "O"); c.p(11, 8, "O"); c.p(15, 4, "O")           # flies
    c.p(10, 11, "5"); c.p(13, 13, "5")
    return fin(c, 1, 15)


def flower():
    c = C()
    c.r(8, 11, 8, 20, "g"); c.r(9, 12, 9, 20, "G")
    c.line(8, 17, 3, 14, "g"); c.line(9, 15, 13, 12, "G"); c.p(2, 13, "h"); c.p(14, 11, "g")
    c.ell(8, 7, 6, 5, "3")
    for ang in range(0, 360, 45):
        import math
        c.ell(8 + 5 * math.cos(math.radians(ang)), 7 + 4.2 * math.sin(math.radians(ang)), 2.2, 2, "2" if ang % 90 else "1")
    c.ell(8, 7, 3, 2.6, "O"); c.ell(8, 7, 2, 1.6, "4")
    c.line(8, 6, 8, 0, "y"); c.p(8, 0, "w"); c.line(7, 6, 5, 1, "w"); c.line(9, 6, 11, 2, "w")        # stigma/style
    c.p(5, 1, "y"); c.p(11, 2, "y")
    c.r(6, 20, 10, 20, "G"); c.line(6, 21, 3, 22, "G"); c.line(10, 21, 13, 22, "G")
    return fin(c, 3, 12)


def insect():
    c = C()
    for s in (0, 1):
        x = 4 if s == 0 else 11
        c.ell(x, 8, 3.2, 5, "1"); c.ell(x, 8, 2, 3.8, "2")
        c.line(7 if s == 0 else 8, 10, x, 4, "3")
    c.ell(8, 11, 2.2, 3, "3")
    c.ell(8, 16, 3, 3.6, "c"); c.ell(8, 16, 1.8, 2.4, "w"); c.r(7, 13, 9, 13, "3")      # glassy bulb
    c.ell(8, 7, 2.2, 1.9, "3"); c.p(7, 7, "4"); c.p(9, 7, "4")
    c.line(7, 5, 4, 2, "3"); c.line(9, 5, 11, 2, "3")
    for y in (11, 13):
        c.line(6, y, 2, y + 5, "L", mirror=True)
    c.r(6, 20, 9, 20, "x") if False else None
    return fin(c, 2, 13)


def golem_baetyl():
    c = C()
    for y in range(1, 19):
        w = 6 - abs(y - 9) * 6 // 9
        c.r(8 - w, y, 7 + w, y, "2")
        c.r(8 - w, y, 8 - w + 1, y, "1"); c.r(6 + w, y, 7 + w, y, "3")
    c.line(2, 9, 13, 9, "O") if False else None
    c.line(4, 5, 11, 13, "O"); c.line(11, 5, 6, 15, "O")
    for x, y in ((5, 6), (7, 8), (9, 10), (10, 7), (8, 12)):
        c.p(x, y, "l")
    c.r(5, 7, 7, 9, "O"); c.p(6, 8, "y"); c.p(5, 7, "w")        # mismatched eye
    c.r(9, 11, 11, 11, "O"); c.p(9, 11, "w"); c.p(11, 11, "w")  # zipped mouth
    c.r(12, 8, 14, 9, "L"); c.p(14, 8, "w")                     # bolted-on scrap arm
    c.r(1, 12, 3, 13, "l")
    c.p(7, 19, "l"); c.p(8, 20, "L"); c.p(6, 20, "L")
    return fin(c, 2, 13)


def golem_chair():
    c = C()
    c.r(3, 1, 11, 11, "2")                                     # backrest
    c.r(3, 1, 11, 2, "1"); c.r(11, 1, 11, 11, "3")
    for x in (5, 7, 9):
        c.r(x, 4, x, 10, "K") if False else c.r(x, 4, x, 10, "3")
    c.r(2, 12, 13, 14, "1"); c.r(2, 14, 13, 14, "3"); c.r(2, 12, 13, 12, "1")
    c.p(6, 6, "O"); c.p(9, 6, "O"); c.p(6, 6, "y"); c.p(9, 6, "y"); c.r(6, 9, 9, 9, "O"); c.p(7, 9, "w"); c.p(8, 9, "w")
    for x in (3, 5, 9, 11):
        c.r(x, 15, x + 1, 21, "3" if x > 6 else "2")
        c.p(x, 21, "1")
    c.r(2, 7, 2, 10, "N"); c.r(12, 7, 12, 10, "N")           # arms
    c.line(4, 15, 12, 12, "O") if False else None
    c.p(8, 13, "N"); c.p(9, 13, "N"); c.p(3, 13, "l")        # nails
    c.p(10, 13, "l")
    return fin(c, 2, 13)


def golem_flower():
    c = C()
    c.r(7, 12, 8, 20, "g"); c.line(7, 15, 3, 14, "g"); c.line(8, 15, 12, 12, "G")
    c.ell(8, 7, 5.5, 5, "2")
    for ang in range(0, 360, 60):
        import math
        c.ell(8 + 5 * math.cos(math.radians(ang)), 7 + 4.4 * math.sin(math.radians(ang)), 2.2, 2, "1")
    c.ell(8, 7, 3.2, 3, "3")
    c.p(7, 6, "O"); c.p(9, 6, "O"); c.p(6, 6, "y") if False else None
    c.r(6, 8, 10, 8, "O"); c.p(7, 8, "w"); c.p(9, 8, "w")
    c.line(5, 3, 8, 10, "O") if False else None
    c.p(2, 7, "O"); c.p(13, 5, "O")                          # stitches
    c.line(4, 11, 11, 4, "5")
    c.r(3, 19, 5, 21, "g"); c.r(10, 19, 12, 21, "G"); c.r(6, 20, 9, 20, "g")
    c.p(5, 12, "l"); c.p(10, 11, "l")
    return fin(c, 2, 13)


def golem_infrastructure():
    c = C()
    c.r(4, 3, 11, 9, "2"); c.r(4, 3, 11, 4, "1"); c.r(10, 3, 11, 9, "3")        # girder body/head
    c.r(6, 5, 9, 6, "O"); c.p(6, 5, "w"); c.p(9, 5, "w")
    c.r(3, 10, 12, 18, "2"); c.r(3, 10, 5, 18, "1"); c.r(10, 10, 12, 18, "3")
    for y in (12, 15, 18):
        c.r(3, y, 12, y, "O") if y == 15 else c.r(3, y, 12, y, "3")
    c.line(4, 10, 11, 18, "L"); c.line(11, 10, 4, 18, "l")                      # lattice
    c.r(1, 6, 2, 17, "l"); c.r(13, 8, 14, 20, "L")                              # pipes as arms
    c.r(0, 6, 3, 6, "L") if False else None
    c.p(1, 5, "w"); c.p(14, 7, "w"); c.p(1, 18, "L"); c.p(14, 21, "L")
    c.r(4, 19, 6, 21, "3"); c.r(9, 19, 11, 21, "3")
    c.r(3, 21, 6, 21, "L"); c.r(9, 21, 12, 21, "L")
    c.p(8, 1, "l"); c.p(8, 2, "l"); c.p(7, 2, "L")
    return fin(c, 1, 14)


def golem_nest():
    c = C()
    c.ell(8, 15, 7, 5, "2"); c.ell(8, 14, 6, 3.5, "3")
    for i in range(14):
        c.line(1 + i, 18 - (i % 3), 3 + i, 12 + (i % 4), "1" if i % 2 else "2")
    c.ell(8, 14, 3.8, 2.2, "O")
    c.ell(6.5, 14, 1.4, 1.6, "w"); c.ell(10, 14, 1.4, 1.6, "w"); c.ell(8, 15.5, 1.2, 1, "w") if False else None
    c.p(6, 14, "y"); c.p(10, 14, "y")
    c.line(2, 12, 0, 8, "1"); c.line(13, 11, 15, 7, "1"); c.line(5, 11, 4, 5, "2"); c.line(11, 11, 12, 4, "2")
    c.p(4, 5, "5"); c.p(12, 4, "5")
    c.r(2, 19, 13, 19, "3")
    return fin(c, 1, 14)


def golem_spider():
    c = C()
    c.ell(8, 15, 3.3, 3.8, "3"); c.ell(8, 14, 2.4, 2.6, "2"); c.r(7, 12, 8, 13, "1")
    c.ell(8, 9, 2.4, 2.4, "2"); c.p(7, 8, "O"); c.p(9, 8, "O"); c.p(8, 9, "w")
    c.line(7, 10, 8, 10, "O")
    c.p(7, 7, "l"); c.p(9, 7, "l")
    for k, (y, ty) in enumerate(((10, 3), (12, 8), (14, 15), (16, 21))):
        c.line(6, y, 3, y - 3, "1", mirror=True); c.line(3, y - 3, 0, ty, "2", mirror=True)
    c.r(7, 17, 8, 18, "O")
    c.p(8, 15, "4"); c.p(6, 16, "5")
    c.p(2, 10, "l"); c.p(13, 13, "l")
    return fin(c, 0, 15)


def golem_turret():
    c = C()
    c.r(7, 11, 8, 12, "L")
    c.r(5, 7, 10, 11, "2"); c.r(5, 7, 10, 8, "1"); c.r(9, 8, 10, 11, "3")
    c.r(2, 9, 6, 10, "l"); c.r(0, 9, 2, 10, "L"); c.p(0, 9, "4")      # gun barrel
    c.r(6, 9, 8, 9, "4"); c.p(7, 8, "O")
    c.p(4, 12, "O") if False else None
    c.line(7, 12, 2, 20, "L"); c.line(8, 12, 13, 20, "l"); c.line(8, 12, 8, 21, "L")
    c.r(1, 21, 3, 21, "L"); c.r(12, 21, 14, 21, "l"); c.r(7, 21, 9, 21, "L")
    c.p(7, 6, "G"); c.p(8, 6, "g"); c.p(8, 5, "c"); c.p(6, 8, "c")
    c.p(10, 6, "g"); c.p(5, 6, "G")                                     # fused flora scraps
    return fin(c, 0, 15)


def mirror():
    c = C()
    pts = [(4, 2), (13, 5), (11, 20), (2, 17)]
    for y in range(24):
        for x in range(16):
            ins = False
            n = 4
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    ins = not ins
            if ins:
                c.p(x, y, "3")
    c.line(4, 2, 13, 5, "1"); c.line(13, 5, 11, 20, "2"); c.line(2, 17, 4, 2, "1")
    for k in range(5):
        c.line(4 + k, 15 - k, 8 + k, 7 - k * 0, "4") if False else None
    c.line(5, 16, 9, 6, "4"); c.line(6, 17, 10, 8, "4"); c.line(8, 17, 11, 11, "5")
    c.p(6, 5, "w"); c.p(10, 14, "w"); c.p(5, 9, "w")
    c.r(2, 17, 11, 20, "2") if False else None
    c.line(2, 17, 11, 20, "1"); c.line(2, 18, 11, 21, "2")
    return fin(c, 1, 13)


def moth():
    c = C()
    for s in (0, 1):
        def X(x):
            return x if s == 0 else 15 - x
        c.ell(X(3.5), 6, 3.8, 5.2, "2"); c.ell(X(3), 15, 3.2, 5, "3")
        c.ell(X(3.5), 6, 2.4, 3.5, "1")
        for (x, y) in ((2, 4), (4, 6), (3, 8), (2, 14), (4, 16), (1, 17), (3, 12)):
            c.p(X(x), y, "4"); c.p(X(x), y + 1, "5") if (x + y) % 3 == 0 else None
        c.line(X(5), 9, X(1), 3, "6") if False else None
    c.ell(8, 12, 1.8, 5, "K") if False else None
    c.ell(8, 13, 1.8, 5, "6"); c.r(7, 9, 8, 10, "5")
    c.ell(8, 8, 2, 1.8, "6"); c.p(7, 8, "w"); c.p(8, 8, "w")
    c.line(7, 6, 4, 0, "5", mirror=True); c.m(4, 0, "4"); c.m(5, 1, "4") if False else None
    c.m(6, 3, "4")
    c.m(2, 9, "w"); c.m(5, 11, "w")
    return fin(c, 2, 13)


def natural_weapon_drill():
    c = C()
    n = 14
    for k in range(n + 1):
        t = k / n
        x = 3.5 + 9.5 * t; y = 19.5 - 16 * t
        r = 3.4 * (1 - t) + 0.5
        # perpendicular stripe (bit flutes)
        dx, dy = 0.84, 0.54
        for u in (-r, -r / 2, 0, r / 2, r):
            c.p(round(x + dx * u), round(y + dy * u), "1" if k % 3 == 0 else ("3" if k % 3 == 1 else "2"))
    c.line(13, 3, 14, 1, "w"); c.p(14, 0, "w")
    c.r(0, 18, 5, 22, "3"); c.r(0, 18, 3, 19, "2"); c.r(1, 21, 4, 21, "O"); c.p(1, 19, "w")
    c.r(5, 19, 6, 20, "L")
    return fin(c, 1, 8)


def natural_weapon_knob():
    c = C()
    c.r(7, 12, 8, 21, "3"); c.r(7, 12, 7, 21, "2")
    c.ell(7.5, 8, 4, 4, "2"); c.ell(7, 7, 2.6, 2.6, "1"); c.p(6, 6, "w")
    c.r(10, 9, 11, 11, "3") if False else None
    c.r(5, 20, 10, 21, "3"); c.r(5, 20, 9, 20, "2")
    c.r(6, 13, 9, 14, "L") if False else None
    c.r(5, 12, 10, 12, "L"); c.p(5, 12, "l")
    return fin(c, 3, 12)


def natural_weapon_saw():
    c = C()
    import math
    for a in range(0, 360, 30):
        x = 8 + 6.8 * math.cos(math.radians(a)); y = 11 + 6.8 * math.sin(math.radians(a))
        c.ell(x, y, 1.3, 1.3, "2")
    c.ell(8, 11, 5.6, 5.6, "2"); c.ell(8, 11, 4.6, 4.6, "1")
    c.ell(8, 11, 1.8, 1.8, "3"); c.p(8, 11, "O")
    c.line(8, 11, 12, 8, "3"); c.line(8, 11, 4, 15, "3")
    c.p(5, 8, "5"); c.p(11, 14, "5"); c.p(7, 15, "4"); c.p(10, 7, "6")
    c.p(6, 7, "w")
    return fin(c, 3, 12)


def nephilim_qon():
    c = C()
    c.ell(8, 15, 6.5, 5.5, "2"); c.ell(8, 13, 5, 3, "1"); c.r(11, 16, 14, 19, "3")
    c.ell(6, 18, 3, 3, "3") if False else None
    # wing folded
    c.ell(11, 15, 3, 4.5, "3"); c.line(10, 12, 12, 19, "6")
    # neck corded
    c.r(5, 7, 7, 13, "2"); c.r(5, 7, 5, 13, "1"); c.line(5, 8, 7, 12, "3") if False else None
    for y in (9, 11):
        c.r(5, y, 7, y, "3")
    c.ell(5, 5, 2.6, 2.4, "1"); c.p(4, 4, "O"); c.p(5, 4, "y")
    c.r(0, 4, 2, 6, "4"); c.r(0, 5, 2, 5, "5"); c.p(0, 6, "6"); c.r(0, 6, 3, 6, "6")             # monadic bill
    c.p(5, 3, "m"); c.p(6, 2, "b"); c.p(4, 2, "b"); c.p(5, 1, "m")                              # crest
    c.p(7, 3, "b"); c.p(6, 3, "b")
    for x, y in ((9, 18), (11, 19), (13, 17)):
        c.p(x, y, "b")
    c.r(6, 20, 6, 21, "4"); c.r(10, 20, 10, 21, "4")
    c.r(4, 22, 7, 22, "5"); c.r(9, 22, 12, 22, "5")
    c.p(7, 11, "b"); c.p(8, 14, "b")
    return fin(c, 2, 14)


def plated_knollworm():
    c = C()
    pts = [(3, 5), (6, 8), (9, 11), (11, 14), (9, 17), (6, 19), (4, 21)]
    for i, (x, y) in enumerate(pts):
        r = 3.2 - i * 0.13
        c.ell(x, y, r, r - 0.5, "2" if i % 2 else "1")
        c.r(int(x - r + 1), int(y + r - 1.5), int(x + r - 1), int(y + r - 1.5), "3")
        c.p(round(x + r - 1), round(y - 1), "w"); c.p(round(x - r + 1), round(y + 1), "w")
    c.ell(2, 4, 2.6, 2.4, "3")                                  # cuspate head
    c.line(0, 1, 2, 3, "w"); c.line(4, 1, 3, 3, "w"); c.line(0, 4, 1, 6, "w"); c.line(4, 6, 3, 5, "w")
    c.p(2, 3, "O"); c.p(1, 4, "4")
    c.p(12, 12, "w"); c.p(13, 14, "w"); c.p(8, 20, "w"); c.p(1, 8, "w") if False else None
    c.p(10, 8, "w"); c.p(12, 16, "w")
    return fin(c, 1, 14)


def rimewyk():
    c = C()
    c.ell(9, 15, 5.5, 3, "2"); c.ell(9, 13.5, 4.5, 1.4, "1"); c.r(10, 17, 13, 17, "3")
    c.ell(3, 12, 3, 2.3, "2"); c.r(0, 12, 1, 13, "1"); c.p(0, 12, "O"); c.p(3, 11, "y")
    c.r(2, 14, 3, 17, "4"); c.r(2, 14, 2, 15, "5") if False else None; c.p(3, 17, "5"); c.p(2, 16, "w")     # dewlap
    c.p(1, 14, "4")
    for x in range(5, 14):
        c.p(x, 12 - (x % 2), "w")
        c.p(x, 11 - (x % 2), "w") if x % 2 == 0 else None
    c.line(14, 15, 15, 18, "2"); c.line(14, 17, 15, 20, "3") if False else None; c.p(15, 19, "3")
    c.p(14, 16, "2"); c.p(15, 17, "3")
    legs(c, (3, 4), 17, 20, "3"); legs(c, (6, 7), 18, 20, "2")
    legs(c, (11, 12), 17, 20, "2"); legs(c, (13,), 17, 20, "3")
    c.r(2, 21, 4, 21, "w"); c.r(10, 21, 13, 21, "w")
    c.p(8, 14, "w"); c.p(10, 15, "w"); c.p(6, 15, "w")
    return fin(c, 0, 15)


def sheyd():
    c = C()
    # gaunt hunched biped, oil-gray, diamond claws, long horns
    c.ell(8, 11, 4, 4.2, "2"); c.ell(7, 9.5, 3, 2.4, "1"); c.r(10, 12, 12, 15, "3")
    c.line(7, 15, 6, 19, "2"); c.line(9, 15, 10, 19, "3"); c.line(10, 19, 12, 19, "3"); c.line(6, 19, 4, 19, "2")
    c.r(3, 20, 5, 20, "w"); c.r(11, 20, 13, 20, "w")
    c.ell(6.5, 5, 2.4, 2.3, "2"); c.r(4, 6, 5, 7, "3")
    c.line(5, 3, 2, 0, "w"); c.line(8, 3, 11, 0, "w"); c.p(2, 0, "l"); c.p(11, 0, "l")
    c.p(5, 5, "M"); c.p(7, 5, "M"); c.p(5, 4, "O") if False else None
    c.line(5, 9, 2, 14, "2"); c.line(3, 14, 1, 20, "3"); c.line(11, 9, 14, 13, "2"); c.line(14, 13, 14, 19, "3")
    for x, y in ((0, 21), (1, 21), (2, 21), (13, 20), (14, 20), (15, 20)):
        c.p(x, y, "w")
    c.p(8, 8, "M"); c.p(9, 10, "4"); c.p(7, 12, "5"); c.p(10, 8, "3")      # whorls of oil
    c.p(6, 11, "5"); c.p(9, 13, "M")
    c.p(14, 11, "M")
    return fin(c, 0, 15)


def starshell():
    c = C()
    c.ell(9, 13, 6, 4.5, "2")
    import math
    for a in range(0, 360, 45):
        x = 9 + 6.3 * math.cos(math.radians(a)); y = 13 + 4.9 * math.sin(math.radians(a))
        c.p(round(x), round(y), "1")
    for x, y in ((9, 6), (13, 8), (5, 8), (4, 12), (14, 12), (9, 19), (6, 18), (12, 18)):
        c.p(x, y, "1"); c.p(x, y + 1, "2") if False else None
    c.line(9, 9, 9, 4, "1"); c.line(6, 10, 4, 6, "1"); c.line(12, 10, 14, 6, "1")
    c.p(9, 3, "w"); c.p(4, 5, "w"); c.p(14, 5, "w")
    c.r(7, 11, 11, 15, "3")
    c.line(7, 11, 11, 15, "4"); c.line(11, 11, 7, 15, "5"); c.p(9, 13, "w")
    c.ell(3, 14, 2.4, 2, "3"); c.p(2, 14, "O"); c.p(3, 13, "w")
    c.r(0, 14, 1, 15, "3"); c.p(1, 14, "O") if False else None
    legs(c, (4, 5), 17, 20, "3"); legs(c, (12, 13), 17, 20, "3"); legs(c, (7,), 17, 20, "2"); legs(c, (10,), 17, 20, "2")
    c.r(3, 21, 5, 21, "O"); c.r(11, 21, 14, 21, "O")
    c.p(15, 13, "3"); c.p(15, 14, "3")
    return fin(c, 1, 15)


def frog_bits(c, cx, top, w, h):
    pass


def svardym_scrounge():
    c = C()
    c.ell(8, 15, 5.5, 4.8, "2"); c.ell(8, 15.5, 3.8, 3.2, "1"); c.r(11, 15, 13, 19, "3")
    c.ell(8, 9, 5, 3.6, "2"); c.r(5, 6, 10, 6, "2")
    c.ell(5, 5.5, 2, 2, "1"); c.ell(11, 5.5, 2, 2, "1")
    c.p(5, 5, "O"); c.p(11, 5, "O"); c.p(4, 4, "w"); c.p(10, 4, "w")
    c.r(4, 10, 11, 10, "O"); c.p(7, 10, "w"); c.p(9, 10, "w") if False else None
    c.r(5, 8, 10, 8, "3") if False else None
    c.p(8, 3, "4"); c.p(7, 2, "5"); c.p(8, 2, "4")                   # crushed coral on brow
    for x, y, ch in ((5, 12, "y"), (7, 13, "w"), (9, 12, "y"), (10, 14, "w"), (6, 15, "y"), (8, 17, "w"), (4, 14, "w")):
        c.p(x, y, ch)                                                 # tinsel trinkets
    c.line(5, 11, 10, 11, "y")
    legs(c, (3, 4), 17, 20, "2"); legs(c, (12, 13), 17, 20, "3")
    c.r(2, 21, 5, 21, "1"); c.r(11, 21, 14, 21, "1")
    c.r(2, 13, 3, 16, "2"); c.r(13, 13, 14, 16, "3")
    return fin(c, 1, 14)


def tumbling_pod():
    c = C()
    c.ell(8, 12, 6, 6, "2"); c.ell(7, 11, 4, 4, "1"); c.r(11, 13, 13, 17, "3")
    for y in range(7, 18, 3):
        c.line(3, y, 12, y + 1, "3")
    c.p(6, 8, "w"); c.p(7, 8, "w")
    c.line(8, 6, 7, 2, "g"); c.line(8, 6, 11, 3, "G"); c.p(7, 1, "4"); c.p(11, 2, "5"); c.p(6, 1, "w")
    c.p(5, 3, "h")
    for x0, x1 in ((4, 1), (6, 3), (10, 13), (12, 15)):
        c.line(x0, 17, x1, 21, "g")
    c.p(2, 21, "G"); c.p(14, 21, "G")
    c.line(8, 18, 8, 21, "g")
    c.p(9, 10, "4"); c.p(10, 12, "5")
    return fin(c, 1, 14)


def vantabud():
    c = C()
    c.ell(8, 12, 6, 4.5, "O")
    for x, h, ch in ((2, 5, "3"), (4, 8, "2"), (6, 5, "1"), (9, 5, "2"), (11, 8, "3"), (13, 5, "2")):
        pass
    c.mr(1, 5, 3, 15, "3")
    c.mr(2, 3, 4, 12, "2")
    c.mr(4, 2, 5, 12, "3") if False else None
    c.mr(4, 4, 5, 9, "1")
    c.r(6, 9, 9, 17, "O")
    c.r(5, 13, 10, 17, "2"); c.r(5, 13, 6, 17, "1"); c.r(9, 13, 10, 17, "3")
    c.r(5, 12, 10, 12, "3")
    c.r(7, 8, 8, 12, "O")
    for x, y in ((7, 7), (9, 5), (6, 3), (8, 1), (10, 8), (5, 6)):
        c.p(x, y, "y" if (x + y) % 2 else "w")
    c.p(7, 11, "w"); c.p(8, 10, "y")
    c.r(7, 18, 8, 20, "g") if False else None
    c.r(7, 18, 8, 21, "3")
    c.line(7, 20, 3, 21, "3"); c.line(8, 20, 12, 21, "3")
    c.p(3, 15, "w") if False else None
    return fin(c, 2, 13)


def yd_elder_svardym():
    c = C()
    c.ell(8, 15, 6.5, 6, "2"); c.r(5, 20, 11, 21, "2")
    c.r(3, 14, 12, 21, "2")
    c.r(3, 14, 5, 21, "1"); c.r(11, 14, 12, 21, "3")
    c.r(4, 10, 11, 13, "2")
    c.ell(8, 6, 5.2, 3.6, "2"); c.r(4, 7, 11, 8, "2")
    c.ell(5, 3.3, 1.9, 1.9, "1"); c.ell(11, 3.3, 1.9, 1.9, "1")
    c.p(5, 3, "O"); c.p(11, 3, "O"); c.p(4, 2, "w"); c.p(10, 2, "w")
    c.r(4, 8, 11, 8, "O"); c.p(5, 9, "3"); c.p(10, 9, "3")
    # draped cloth and ornaments
    c.r(3, 10, 12, 12, "4"); c.r(3, 10, 12, 10, "5"); c.line(3, 11, 12, 13, "6")
    c.r(2, 13, 4, 20, "5"); c.r(11, 13, 13, 20, "6"); c.r(2, 13, 3, 20, "4")
    c.r(6, 14, 9, 21, "4"); c.r(6, 14, 9, 15, "5"); c.r(8, 16, 9, 21, "5")
    for x, y in ((6, 11), (8, 12), (10, 11), (5, 16), (10, 17), (7, 19)):
        c.p(x, y, "y")
    c.p(8, 0, "4"); c.p(7, 1, "5"); c.p(9, 1, "5")
    c.p(2, 12, "w"); c.p(13, 12, "w")
    c.r(2, 21, 5, 21, "1"); c.r(10, 21, 13, 21, "1")
    return fin(c, 1, 14)


SPRITES = {}
for _n, _v in list(globals().items()):
    if callable(_v) and _n in {v for v in KEYS.values()}:
        SPRITES[_n] = _v()
