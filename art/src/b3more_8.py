"""B3 remaining creatures, batch 8: golems, cherubs, slynth, robots, oddities."""
import os
import sys
from functools import partial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from b3more_keys import MORE_KEYS  # noqa: E402
import b3kit as K  # noqa: E402
from b3kit import C, back, person, hair_bun, hair_short, wrench, hood, staff, lantern  # noqa: E402

KEYS = MORE_KEYS[8]
SPRITES = {}
HUMANOID = set()


def tube(c, pts, r0, r1, ch):
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


def reg(name, humanoid=False):
    def deco(fn):
        SPRITES[name] = fn()
        if humanoid:
            HUMANOID.add(name)
        return fn
    return deco


def halo(c, a="4", b="5", y=0):
    """small floating cherub ring."""
    c.r(6, y, 9, y, a)
    c.p(5, y + 1, a); c.p(10, y + 1, a)
    c.p(6, y + 1, b); c.p(9, y + 1, b)
    c.p(7, y + 1, b); c.p(8, y + 1, b) if False else None


# =============================================================================== humanoids
@back
def chair_frame(c):
    c.r(3, 1, 12, 2, "n")
    c.r(3, 1, 12, 1, "w")
    c.r(3, 3, 4, 15, "n")
    c.r(11, 3, 12, 15, "N")
    for x in (5, 10):
        c.r(x, 3, x, 8, "N")
    c.p(3, 0, "n"); c.p(12, 0, "N")


def chair_legs(c):
    c.r(3, 16, 12, 21, ".")
    c.r(2, 16, 13, 17, "4")
    c.r(2, 16, 13, 16, "5") if False else None
    c.r(2, 18, 13, 18, "6")
    c.r(2, 16, 3, 16, "5")
    c.r(3, 19, 4, 22, "n"); c.r(11, 19, 12, 22, "N")
    c.r(6, 19, 6, 22, "n"); c.r(9, 19, 9, 22, "N")
    c.r(3, 20, 12, 20, "n")
    c.r(7, 19, 8, 21, "L")
    c.r(3, 22, 4, 22, "N"); c.r(11, 22, 12, 22, "N")
    c.r(5, 22, 10, 22, ".")
    c.r(6, 22, 6, 22, "N"); c.r(9, 22, 9, 22, "N")
    c.p(7, 17, "w"); c.p(8, 17, "w")


@reg("chair", True)
def _():
    return person(chair_frame, chair_legs, face="face", sash=False, skin=("n", "N"))


def mech_cherub_robe(c):
    c.r(2, 9, 3, 10, "l"); c.r(12, 9, 13, 10, "L")
    c.p(2, 9, "w")
    c.r(6, 10, 9, 13, "l"); c.r(9, 10, 9, 13, "L")
    c.p(7, 11, "4"); c.p(8, 11, "4"); c.p(7, 12, "5"); c.p(8, 12, "5")
    c.p(4, 12, "l"); c.p(11, 12, "L"); c.p(4, 14, "L"); c.p(11, 14, "L")
    c.r(7, 17, 8, 20, "L")


def mech_halo(c):
    c.r(5, 0, 10, 0, "4")
    c.p(4, 1, "5"); c.p(11, 1, "5"); c.p(5, 1, "4"); c.p(10, 1, "4")
    c.p(3, 2, "4"); c.p(12, 2, "5")


def mech_hood(c):
    K.hood(c, a="l", lite="w", dark="L")
    c.r(6, 4, 9, 7, "L")
    c.r(6, 5, 9, 5, "O"); c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(7, 5, "5"); c.p(8, 5, "5")
    c.r(7, 7, 8, 7, "l")


def hermit_lamp(c):
    K.lantern(c, glow="4")
    c.r(0, 12, 0, 12, "L")


@reg("cherub_hermit_mechanical", True)
def _():
    return person(mech_cherub_robe, mech_hood, mech_halo, hermit_lamp, face="none",
                  sash=False, skin=("L", "L"), body="1", lite="1", dark="2")


def dirt_smears(c):
    for x, y in ((6, 11), (9, 13), (5, 16), (8, 19), (10, 17), (7, 14)):
        c.p(x, y, "e")
    c.r(5, 3, 6, 3, "e"); c.p(9, 6, "e")


@reg("daughter", True)
def _():
    return person(hair_bun, dirt_smears, wrench, face="face", sash=False,
                  body="1", lite="1", dark="2", trim="4")


@back
def boulder_back(c):
    pass


def boulder(c):
    c.ell(2.5, 6, 3.2, 3.6, "L")
    c.ell(2.2, 5.5, 2.4, 2.6, "l")
    c.p(1, 4, "w"); c.p(2, 4, "w")
    c.p(3, 7, "4"); c.p(1, 7, "5"); c.p(4, 5, "4"); c.p(2, 9, "4")
    c.p(4, 10, "s"); c.p(4, 9, "L")
    c.r(4, 8, 5, 10, "2")


def glitter(c):
    c.r(5, 10, 10, 10, "w")
    for x, y in ((6, 11), (9, 12), (7, 14), (8, 9), (10, 11), (5, 13), (11, 13), (6, 17), (9, 19), (7, 20)):
        c.p(x, y, "4")
    for x, y in ((8, 11), (6, 15), (9, 16), (5, 19)):
        c.p(x, y, "w")
    c.p(6, 3, "w"); c.p(9, 4, "4")
    c.r(11, 9, 12, 11, "w"); c.p(12, 11, "l")


@reg("glittermensch_boulderer", True)
def _():
    return person(boulder, glitter, face="face", sash=False, skin=("w", "l"),
                  body="2", lite="1", dark="3")


def crystal_head(c):
    # octahedron head
    c.r(7, 0, 8, 0, "1")
    c.r(6, 1, 9, 1, "1")
    c.r(5, 2, 10, 2, "2")
    c.r(4, 3, 11, 5, "2")
    c.r(5, 6, 10, 6, "2")
    c.r(6, 7, 9, 7, "3")
    c.r(7, 8, 8, 8, "3")
    c.r(4, 3, 6, 4, "1"); c.r(9, 4, 11, 5, "3")
    c.r(8, 6, 10, 6, "3")
    c.line(4, 4, 11, 4, "w") if False else None
    c.p(7, 4, "4"); c.p(8, 4, "4"); c.p(7, 5, "5"); c.p(8, 5, "5")
    c.p(7, 1, "w"); c.p(5, 3, "w")
    c.p(7, 8, "3")


def crystal_body(c):
    c.mr(3, 9, 4, 11, "1"); c.p(3, 9, "w")
    c.mr(2, 10, 2, 10, "2")
    c.r(6, 10, 9, 12, "1"); c.r(8, 10, 9, 12, "2")
    c.line(7, 9, 7, 16, "w")
    c.p(11, 13, "3"); c.p(4, 13, "1")
    c.p(7, 13, "4"); c.p(8, 13, "5"); c.p(8, 15, "5")
    c.mr(3, 15, 3, 18, "5") if False else None
    c.m(2, 18, "4"); c.m(3, 20, "5")
    c.p(11, 16, "3")


@reg("golem_crystal_being", True)
def _():
    return person(crystal_head, crystal_body, face="none", sash=False, skin=("1", "3"),
                  body="2", lite="1", dark="3")


def bear_head(c):
    c.r(4, 2, 5, 3, "w"); c.r(10, 2, 11, 3, "L")     # round ears
    c.p(4, 2, "l"); c.p(5, 3, "L")
    c.r(5, 3, 10, 7, "w"); c.r(10, 3, 10, 7, "l")
    c.r(6, 6, 9, 8, "l")
    c.r(7, 7, 8, 8, "O")
    c.p(7, 7, "R") if False else None
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(6, 4, "L"); c.p(9, 4, "L")


def urshiib_fur(c):
    # hunched back, tufts + needle quills, long triple-jointed fingers
    c.r(3, 8, 11, 12, "w")
    c.r(2, 9, 3, 12, "w"); c.p(12, 9, "l")
    c.r(9, 9, 11, 12, "l")
    for x in range(3, 12):
        c.p(x, 8, "L" if x % 2 else "w")
    for x, y0 in ((2, 4), (4, 3), (7, 1), (10, 3), (12, 4), (13, 6)):
        c.line(x, y0, x, y0 + 4, "L") if x not in (7,) else None
    c.p(1, 6, "L"); c.p(2, 6, "w"); c.p(1, 8, "L"); c.p(0, 10, "L"); c.p(13, 7, "L"); c.p(14, 9, "L")
    c.line(3, 9, 0, 6, "L"); c.line(11, 9, 14, 6, "L")
    c.p(0, 6, "w"); c.p(14, 6, "w")
    # long fingers
    for dx in (0, 1, 2):
        c.line(4 - dx, 14, 3 - dx * 1, 19, "L")
        c.line(11 + dx, 14, 12 + dx, 19, "L") if 11 + dx < 15 else None
    c.p(3, 20, "w"); c.p(2, 20, "w"); c.p(12, 20, "w")
    c.p(7, 13, "5"); c.p(8, 13, "5")


@reg("golem_urshiib", True)
def _():
    return person(urshiib_fur, bear_head, face="none", sash=False, skin=("w", "l"),
                  body="2", lite="1", dark="3")


def deer_head(c):
    c.line(5, 3, 2, 0, "w"); c.line(10, 3, 13, 0, "w")
    c.p(3, 2, "w"); c.p(2, 1, "w"); c.p(12, 2, "w"); c.p(13, 1, "w")
    c.p(1, 0, "w"); c.p(14, 0, "w"); c.p(4, 1, "w"); c.p(11, 1, "w")
    c.r(3, 4, 4, 4, "g"); c.r(11, 4, 12, 4, "G")    # ears
    c.p(2, 4, "g"); c.p(13, 4, "G")
    c.r(5, 3, 10, 3, "g")
    c.r(5, 4, 10, 6, "w"); c.r(10, 4, 10, 6, "l")
    c.r(6, 7, 9, 7, "w"); c.p(7, 7, "O") if False else None
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(7, 7, "O"); c.p(8, 7, "O") if False else None
    c.p(5, 4, "G"); c.p(8, 3, "h")


def lulihart_limbs(c):
    # strip the robe: thin legs + patchy fur
    c.r(3, 9, 12, 22, ".")
    c.r(7, 8, 8, 8, "w")
    c.r(6, 9, 9, 14, "w"); c.r(9, 9, 9, 14, "l")
    for x, y in ((6, 10), (8, 12), (7, 13), (9, 9)):
        c.p(x, y, "g")
    c.r(4, 10, 5, 10, "w"); c.r(10, 10, 11, 10, "l")
    c.line(4, 10, 3, 17, "w"); c.line(11, 10, 12, 17, "l")
    c.p(3, 18, "w"); c.p(12, 18, "l"); c.p(2, 18, "1"); c.p(13, 18, "1")
    c.r(6, 15, 9, 16, "1"); c.r(9, 15, 9, 16, "2")
    c.r(6, 17, 6, 21, "w"); c.r(9, 17, 9, 21, "l")
    c.p(5, 14, "g"); c.p(10, 14, "G") if False else None
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.p(7, 11, "g"); c.p(6, 19, "g"); c.p(8, 15, "3")
    c.p(8, 18, "3") if False else None
    c.shadow(3, 12)


@reg("lulihart", True)
def _():
    return person(lulihart_limbs, deer_head, face="none", sash=False, sleeves=False, feet=False,
                  skin=("w", "l"), body="1", lite="1", dark="2")


def jeer_gear(c):
    # moss-fur along shoulders and hem, fixed minyan mask
    c.r(3, 9, 5, 10, "g"); c.r(10, 9, 12, 10, "G")
    c.p(3, 11, "h"); c.p(12, 11, "G"); c.p(4, 11, "g")
    for x in range(3, 13):
        c.p(x, 20, "g" if x % 2 else "h")
        c.p(x, 21, "G" if x % 2 else "g")
    c.p(6, 15, "h"); c.p(9, 17, "g")
    # mask: pale face plate with bright scanning eyes and a crest
    c.r(5, 2, 10, 2, "w"); c.p(7, 1, "w"); c.p(8, 1, "w")
    c.r(5, 3, 10, 7, "w"); c.r(10, 3, 10, 7, "l")
    c.r(6, 5, 9, 5, "O")
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(7, 5, "5") if False else None
    c.r(6, 4, 9, 4, "l")
    c.p(7, 7, "L"); c.p(8, 7, "L")
    c.mr(4, 4, 4, 7, "g")
    c.p(4, 3, "g"); c.p(11, 3, "G")


@reg("naphtaali_jeer", True)
def _():
    return person(jeer_gear, hair_short, face="none", sash=True, trim="4",
                  body="2", lite="1", dark="3")


def ape_mass(c):
    c.r(2, 8, 13, 13, "w")
    c.r(1, 9, 3, 15, "w"); c.r(12, 9, 14, 15, "l")
    c.r(10, 8, 13, 13, "l")
    c.r(2, 8, 4, 9, "w")
    for x, y in ((3, 10), (12, 11), (6, 11), (9, 12), (4, 13)):
        c.p(x, y, "l")
    c.r(5, 14, 10, 16, "w"); c.r(9, 14, 10, 16, "l")
    c.r(0, 14, 3, 17, "w"); c.r(12, 14, 15, 17, "l")
    c.p(0, 17, "L"); c.p(15, 17, "L"); c.p(1, 18, "s"); c.p(14, 18, "S")
    c.r(1, 18, 3, 19, "L") if False else None
    c.r(6, 9, 9, 10, "M") if False else None
    c.p(7, 10, "5"); c.p(8, 10, "5"); c.p(7, 11, "4"); c.p(8, 11, "4")
    c.r(3, 17, 4, 20, "w") if False else None
    c.r(3, 18, 5, 21, "w"); c.r(10, 18, 12, 21, "l")
    c.r(3, 22, 5, 22, "O"); c.r(10, 22, 12, 22, "O")


def ape_head(c):
    c.r(5, 3, 10, 3, "w")
    c.r(4, 4, 11, 7, "w"); c.r(10, 4, 11, 7, "l")
    c.r(5, 5, 10, 5, "L")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "s"); c.p(7, 7, "O"); c.p(8, 7, "O") if False else None
    c.p(6, 2, "w"); c.p(9, 2, "w"); c.p(7, 2, "w"); c.p(8, 2, "l")
    c.p(4, 3, "w"); c.p(11, 3, "l")


@reg("oboroqoru", True)
def _():
    return person(ape_mass, ape_head, face="none", sash=False, sleeves=False, feet=False,
                  skin=("w", "l"), body="1")


def petals(c, big=True):
    ink = "t"
    if big:
        for x, y in ((5, 2), (8, 0), (4, 0), (11, 0), (2, 1), (13, 2), (6, 1), (9, 1), (3, 3), (12, 3)):
            c.p(x, y, ink)
        c.r(4, 2, 11, 2, ink); c.r(5, 1, 10, 1, "y")
        c.mr(2, 1, 3, 3, "t") if False else None
        c.p(2, 2, "y"); c.p(13, 2, "y"); c.p(7, 0, "y"); c.p(6, 0, "t")
    c.r(5, 3, 10, 3, "t")
    c.p(7, 3, "y")


def slynth_skin(c):
    # leafy fronds on shoulders and rooted hind-legs
    c.r(3, 9, 4, 10, "g"); c.r(11, 9, 12, 10, "G")
    c.p(2, 10, "h"); c.p(13, 10, "G"); c.p(2, 11, "g")
    c.r(2, 21, 4, 21, "e"); c.r(11, 21, 13, 21, "e")
    c.p(1, 22, "e"); c.p(14, 22, "E"); c.p(3, 22, "e"); c.p(12, 22, "E")


def scout_gear(c):
    c.line(13, 2, 13, 22, "n")
    c.p(13, 1, "t"); c.p(12, 2, "t"); c.p(14, 2, "t"); c.p(13, 0, "y")
    c.p(12, 15, "g"); c.p(11, 15, "g")
    c.line(5, 10, 10, 15, "5"); c.line(5, 11, 10, 16, "4")


@reg("slynth_bey_lah", True)
def _():
    return person(slynth_skin, petals, scout_gear, face="face", sash=False,
                  skin=("g", "G"), body="2", lite="1", dark="3")


def leaf_apron(c):
    # triangle apron knitted from the overgrowth
    for i in range(10):
        w = 4 - i // 3
        c.r(8 - w, 11 + i, 7 + w, 11 + i, "g" if i % 2 else "h")
    c.r(7, 11, 8, 20, "G")
    c.p(5, 10, "5"); c.p(10, 10, "5")
    c.p(6, 12, "t"); c.p(9, 15, "t")


def sprout(c):
    c.p(7, 2, "g"); c.p(8, 1, "g"); c.p(9, 2, "h"); c.p(6, 2, "G"); c.p(10, 3, "g")
    c.r(5, 3, 10, 3, "g"); c.p(8, 0, "h"); c.p(9, 1, "t")
    c.p(5, 4, "G"); c.p(10, 4, "G") if False else None


@reg("slynth_villager", True)
def _():
    return person(slynth_skin, leaf_apron, sprout, face="face", sash=False,
                  skin=("g", "G"), body="1", lite="1", dark="2", trim="4")


def foal_body(c):
    # hunched, burred shoulders, arms too long
    c.r(3, 8, 12, 9, "2"); c.r(3, 8, 5, 8, "1")
    for x in (3, 5, 7, 10, 12):
        c.p(x, 7, "3")
    c.p(2, 9, "3"); c.p(13, 9, "3"); c.p(4, 7, "N") if False else None
    c.r(3, 10, 3, 19, "2"); c.r(12, 10, 12, 19, "3")
    c.r(4, 10, 4, 14, "2")
    c.r(2, 18, 4, 20, "s"); c.r(11, 18, 13, 20, "S")
    c.p(2, 20, "w"); c.p(4, 20, "w"); c.p(11, 20, "w"); c.p(13, 20, "w")
    c.p(3, 15, "4"); c.p(12, 15, "5")
    c.r(6, 11, 9, 12, "4") if False else None
    c.p(7, 10, "4"); c.p(8, 11, "5")
    c.r(5, 3, 10, 7, "s") if False else None


def foal_head(c):
    c.r(5, 2, 10, 3, "N"); c.p(6, 2, "n")
    c.p(4, 4, "s"); c.p(11, 4, "S")
    c.r(6, 6, 9, 7, "S"); c.r(6, 7, 9, 7, "S")
    c.p(7, 7, "w"); c.p(9, 7, "w"); c.p(6, 7, "S")


@reg("troll_foal", True)
def _():
    return person(foal_body, foal_head, face="face", sash=False, sleeves=False,
                  skin=("s", "S"), body="2", lite="1", dark="3", trim="4")
