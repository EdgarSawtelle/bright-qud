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


def halo(c, a="y", b="t", y=0):
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
    c.r(3, 17, 12, 21, "w"); c.r(9, 17, 12, 21, "l")
    for x, y in ((5, 18), (8, 20), (11, 19), (4, 20)):
        c.p(x, y, "l")
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


# =============================================================================== quadrupeds
def legs4(c, top=15, bot=21, a="2", b="3", hl="1", xs=(4, 6, 10, 12), w=1):
    for i, x in enumerate(xs):
        ch = b if i % 2 == 0 else a
        c.r(x, top, x + w - 1, bot, ch)
        c.r(x - 1, bot, x + w, bot, "O" if False else hl)
    return c


def stitch(c, x0, y0, x1, y1):
    n = max(abs(x1 - x0), abs(y1 - y0))
    for i in range(n + 1):
        x = round(x0 + (x1 - x0) * i / n); y = round(y0 + (y1 - y0) * i / n)
        c.p(x, y, "O" if i % 2 == 0 else "4")


def bolt(c, x, y):
    c.p(x, y, "L"); c.p(x + 1, y, "l"); c.p(x, y - 1, "l"); c.p(x + 1, y + 1, "L")


@reg("golem_dog")
def _():
    c = C()
    c.line(12, 10, 14, 6, "3"); c.line(13, 10, 15, 6, "3"); c.p(14, 5, "4")
    c.ell(8, 13, 5.2, 3.4, "2")
    c.r(4, 10, 11, 11, "1"); c.r(9, 14, 12, 16, "3")
    c.r(2, 6, 7, 11, "2"); c.r(2, 6, 5, 7, "1")
    c.r(0, 9, 3, 11, "1"); c.r(0, 11, 3, 11, "3")
    c.p(0, 9, "O"); c.p(0, 10, "O")
    c.r(1, 11, 3, 11, "w"); c.p(1, 12, "w"); c.p(3, 12, "w")
    c.p(3, 7, "4"); c.p(4, 7, "5")
    c.r(2, 3, 3, 5, "3"); c.r(6, 4, 7, 6, "3")
    c.p(2, 3, "4")
    stitch(c, 7, 6, 8, 12)
    stitch(c, 5, 14, 11, 14)
    bolt(c, 6, 9)
    c.r(3, 15, 4, 21, "3"); c.r(6, 15, 7, 21, "2"); c.r(10, 16, 11, 21, "3"); c.r(12, 15, 13, 21, "2")
    for x0, x1 in ((2, 5), (5, 8), (9, 12), (11, 14)):
        c.r(x0, 21, x1, 21, "1")
    c.p(4, 18, "4"); c.p(12, 18, "5")
    c.shadow(0, 14)
    return c.out()


@reg("golem_goat")
def _():
    c = C()
    c.r(13, 8, 14, 9, "2"); c.p(14, 7, "1")
    c.r(4, 9, 12, 15, "2"); c.r(4, 9, 12, 10, "1"); c.r(10, 12, 12, 15, "3")
    c.r(3, 8, 5, 12, "2")
    c.r(1, 5, 5, 9, "w") if False else None
    c.r(1, 5, 5, 10, "2"); c.r(1, 5, 4, 6, "1")
    c.r(0, 8, 3, 10, "1"); c.p(0, 9, "O")
    c.r(1, 11, 2, 13, "w"); c.p(2, 14, "w")                 # beard
    c.p(3, 7, "4"); c.p(4, 7, "5")
    c.line(2, 4, 0, 1, "w"); c.line(5, 4, 8, 1, "w"); c.line(3, 4, 1, 3, "w")
    c.p(0, 0, "L"); c.p(8, 0, "L"); c.p(9, 1, "w"); c.p(1, 2, "L")
    c.r(6, 6, 7, 5, "3")
    stitch(c, 6, 10, 8, 15); bolt(c, 10, 11)
    c.r(4, 16, 5, 21, "3"); c.r(7, 16, 8, 21, "2"); c.r(10, 16, 11, 21, "3"); c.r(12, 16, 12, 21, "2")
    c.r(4, 21, 5, 21, "5"); c.r(7, 21, 8, 21, "5"); c.r(10, 21, 11, 21, "5"); c.p(12, 21, "5")
    c.r(3, 15, 5, 15, "4")
    c.shadow(0, 14)
    return c.out()


@reg("golem_reptile")
def _():
    c = C()
    tube(c, [(11, 13), (13, 16), (14, 19), (12, 21)], 2.0, 0.6, "3")
    c.ell(8, 12, 5, 4, "2")
    c.r(4, 8, 11, 10, "1")
    for x in range(5, 12, 2):                               # dorsal spines
        c.line(x, 8, x, 5, "5"); c.p(x, 4, "4")
    c.r(1, 6, 5, 12, "2"); c.r(1, 6, 4, 7, "1")             # head
    c.r(0, 9, 3, 12, "1"); c.r(0, 12, 3, 12, "3")
    c.p(0, 10, "O"); c.p(3, 7, "O"); c.p(3, 8, "4"); c.p(4, 7, "5")
    c.p(0, 11, "w"); c.p(2, 12, "w"); c.p(1, 13, "w")
    stitch(c, 6, 8, 7, 15); bolt(c, 9, 11)
    c.r(2, 14, 4, 15, "3"); c.r(1, 16, 2, 19, "3"); c.r(0, 20, 3, 20, "1"); c.r(1, 19, 1, 20, "3")
    c.r(5, 15, 6, 20, "2"); c.r(4, 20, 7, 20, "1")
    c.r(9, 15, 10, 20, "3"); c.r(8, 20, 11, 20, "1")
    c.r(12, 14, 13, 18, "2"); c.r(12, 19, 14, 19, "1") if False else None
    c.shadow(0, 15)
    return c.out()


@reg("golem_wheeled_robot")
def _():
    c = C()
    c.r(5, 2, 10, 6, "l"); c.r(5, 2, 10, 2, "w"); c.r(10, 3, 10, 6, "L")
    c.r(6, 3, 9, 4, "O"); c.p(7, 3, "4"); c.p(8, 3, "5"); c.p(7, 4, "4")
    c.r(7, 1, 8, 1, "L"); c.p(7, 0, "4")
    c.r(6, 7, 9, 7, "L")
    c.r(3, 8, 12, 15, "l"); c.r(3, 8, 12, 8, "w"); c.r(10, 9, 12, 15, "L")
    c.r(4, 9, 9, 14, "2"); c.r(4, 9, 9, 10, "1"); c.r(8, 9, 9, 14, "3")
    c.p(6, 12, "4"); c.p(7, 12, "5"); c.p(6, 13, "5")
    stitch(c, 4, 11, 9, 12)
    c.r(0, 9, 2, 10, "L"); c.r(0, 11, 1, 15, "l"); c.r(0, 15, 2, 16, "L"); c.p(0, 16, "w")
    c.r(13, 9, 15, 10, "L"); c.r(14, 11, 15, 14, "L"); c.r(13, 15, 15, 16, "l")
    c.r(6, 16, 9, 17, "L")
    c.ell(7.5, 19.5, 3.4, 2.7, "L")
    c.ell(7.5, 19.5, 2.2, 1.7, "l")
    c.p(7, 19, "4"); c.p(8, 19, "w")
    c.r(2, 21, 13, 21, "O") if False else None
    c.r(3, 22, 12, 22, "O") if False else None
    c.shadow(2, 13)
    return c.out()


@reg("golem_bipedal_robot")
def _():
    c = C()
    c.r(5, 1, 10, 6, "l"); c.r(5, 1, 10, 1, "w"); c.r(10, 2, 10, 6, "L")
    c.r(6, 3, 9, 4, "O"); c.p(6, 3, "4"); c.p(9, 3, "4"); c.p(7, 4, "5"); c.p(8, 4, "5")
    c.r(7, 0, 8, 0, "L"); c.p(8, 0, "4")
    c.r(7, 7, 8, 7, "L")
    c.r(4, 8, 11, 14, "l"); c.r(4, 8, 11, 8, "w"); c.r(10, 9, 11, 14, "L")
    c.r(5, 9, 9, 13, "2"); c.r(5, 9, 9, 10, "1"); c.r(8, 9, 9, 13, "3")
    c.p(6, 11, "4"); c.p(7, 11, "5"); c.p(7, 12, "6")
    stitch(c, 5, 13, 9, 9)
    c.r(1, 8, 3, 10, "L"); c.p(1, 8, "w"); c.r(1, 11, 2, 15, "l"); c.r(1, 15, 3, 17, "L")
    c.r(12, 8, 14, 10, "L"); c.r(13, 11, 14, 15, "L"); c.r(12, 15, 14, 17, "l")
    c.p(2, 17, "4"); c.p(13, 17, "5")
    c.r(5, 15, 10, 15, "L")
    c.r(5, 16, 6, 20, "l"); c.r(9, 16, 10, 20, "L")
    c.r(5, 16, 5, 20, "w")
    c.r(4, 21, 7, 22, "L"); c.r(8, 21, 11, 22, "L"); c.r(4, 21, 6, 21, "l"); c.r(8, 21, 10, 21, "l")
    c.p(6, 18, "4"); c.p(9, 18, "5")
    c.shadow(3, 12)
    return c.out()


@reg("golem_table")
def _():
    c = C()
    # tabletop in perspective
    for y in range(5, 13):
        off = (12 - y) // 3
        c.r(1 + off, y, 14 - off, y, "1" if y < 8 else "2")
    c.r(1, 13, 14, 14, "3")
    c.r(1, 13, 14, 13, "2")
    for x, y in ((4, 7), (9, 9), (6, 10), (12, 7), (3, 11)):
        c.p(x, y, "3")
    c.r(7, 8, 8, 9, "3")                          # big knots = glowing eyes
    c.r(4, 7, 5, 8, "3"); c.r(10, 7, 11, 8, "3")
    c.p(5, 8, "4"); c.p(10, 8, "4"); c.p(7, 9, "4"); c.p(8, 9, "4")
    c.p(5, 7, "5"); c.p(10, 7, "5")
    c.line(2, 5, 13, 5, "1")
    c.p(3, 6, "n"); c.p(12, 6, "n")
    c.r(6, 14, 9, 14, "4")
    # legs, with root-like feet
    for x in (1, 13):
        c.r(x, 15, x + 1, 20, "2"); c.p(x, 16, "1"); c.r(x + 1, 15, x + 1, 20, "3")
    for x in (4, 10):
        c.r(x, 15, x + 1, 19, "3")
    c.r(0, 21, 3, 21, "3"); c.r(12, 21, 15, 21, "3"); c.r(3, 20, 6, 20, "3"); c.r(9, 20, 12, 20, "3")
    c.p(0, 20, "2"); c.p(15, 20, "3")
    c.p(7, 3, "g"); c.p(8, 2, "h") if False else None
    c.r(6, 2, 9, 4, ".") if False else None
    c.shadow(0, 15)
    return c.out()


@reg("cherub_antelope")
def _():
    c = C()
    halo(c)
    c.line(2, 11, 0, 4, "w")      # long swept horns
    c.line(3, 11, 2, 3, "y") if False else None
    c.line(4, 8, 6, 3, "w") if False else None
    c.p(1, 7, "w"); c.p(1, 5, "l")
    c.line(5, 8, 7, 3, "l"); c.p(8, 3, "w")
    c.r(5, 11, 12, 16, "2"); c.r(5, 11, 12, 12, "1"); c.r(10, 13, 12, 16, "3")
    c.r(3, 7, 6, 13, "1")                          # neck
    c.r(1, 8, 4, 10, "2"); c.r(0, 9, 2, 10, "1"); c.p(0, 9, "O")
    c.p(3, 8, "4")
    c.line(12, 12, 14, 14, "2"); c.p(14, 15, "3")
    for x, ch in ((5, "3"), (7, "2"), (10, "3"), (12, "2")):
        c.r(x, 17, x, 21, ch)
    c.r(4, 21, 8, 21, "1") if False else None
    c.p(5, 21, "1"); c.p(7, 21, "1"); c.p(10, 21, "1"); c.p(12, 21, "1")
    c.r(6, 13, 9, 14, "4"); c.p(7, 14, "5")
    c.shadow(1, 14)
    return c.out()


@reg("cherub_equine")
def _():
    c = C()
    halo(c)
    c.line(13, 12, 15, 17, "5"); c.line(12, 12, 14, 18, "4")        # tail
    c.r(5, 10, 12, 16, "2"); c.r(5, 10, 12, 11, "1"); c.r(10, 12, 12, 16, "3")
    c.r(3, 6, 6, 12, "1"); c.r(3, 5, 6, 5, "1")
    c.r(1, 5, 5, 8, "2"); c.r(0, 7, 2, 10, "1"); c.p(0, 9, "O")
    c.p(3, 6, "4"); c.p(3, 4, "1"); c.p(5, 4, "1"); c.p(4, 3, "w") if False else None
    c.r(6, 5, 6, 12, "5"); c.r(5, 4, 5, 9, "4")                    # mane
    for x, ch in ((5, "3"), (7, "2"), (10, "3"), (12, "2")):
        c.r(x, 17, x, 21, ch)
    for x in (5, 7, 10, 12):
        c.p(x, 21, "w")
    c.r(7, 12, 9, 13, "4") if False else None
    c.shadow(1, 15)
    return c.out()


@reg("zebra")
def _():
    c = C()
    c.line(13, 11, 15, 17, "3"); c.line(12, 11, 14, 18, "1")
    c.r(5, 9, 12, 15, "1"); c.r(10, 11, 12, 15, "2")
    for x in range(5, 13, 2):                                      # stripes
        c.r(x, 9, x, 15, "3") if x != 11 else c.r(x, 9, x, 15, "3")
    c.r(3, 5, 6, 11, "1")
    c.r(1, 5, 5, 8, "1"); c.r(0, 7, 2, 10, "1"); c.p(0, 9, "O")
    c.p(1, 6, "3"); c.p(3, 5, "3"); c.p(4, 7, "3"); c.p(2, 8, "3")
    c.p(3, 6, "O")
    c.r(5, 3, 6, 4, "1"); c.p(5, 3, "3")
    c.r(6, 4, 6, 10, "3"); c.r(4, 3, 4, 6, "3") if False else None
    for x, ch in ((5, "3"), (7, "1"), (10, "3"), (12, "1")):
        c.r(x, 16, x, 21, ch)
    for y in (17, 19):
        c.r(5, y, 5, y, "1"); c.r(10, y, 10, y, "1"); c.r(7, y, 7, y, "3"); c.r(12, y, 12, y, "3")
    c.r(5, 21, 5, 21, "O"); c.r(7, 21, 7, 21, "O"); c.r(10, 21, 10, 21, "O"); c.r(12, 21, 12, 21, "O")
    c.shadow(0, 15)
    return c.out()


# =============================================================================== cherubs
@reg("cherub_bird")
def _():
    c = C()
    halo(c, y=1)
    c.ell(8, 14, 4.5, 4.5, "2")
    c.ell(7, 12, 3.5, 3, "1")
    c.r(6, 6, 9, 9, "1"); c.r(5, 5, 9, 7, "1")      # head
    c.r(9, 6, 9, 9, "2")
    c.r(2, 7, 5, 7, "y") if False else None
    c.r(2, 7, 4, 8, "y"); c.p(1, 8, "y"); c.p(2, 8, "t")  # beak
    c.p(6, 6, "O")
    c.p(7, 4, "1"); c.p(8, 4, "2") if False else None
    c.line(11, 13, 14, 21, "2"); c.line(12, 12, 15, 20, "3"); c.line(10, 14, 13, 21, "1")   # tail
    c.line(4, 12, 9, 17, "3"); c.line(5, 12, 10, 17, "2")                                   # folded wing
    c.r(5, 13, 8, 14, "1")
    c.r(6, 19, 6, 21, "y"); c.r(9, 19, 9, 21, "y")
    c.r(5, 21, 7, 21, "y"); c.r(8, 21, 10, 21, "y")
    c.p(6, 16, "4"); c.p(7, 16, "5")
    c.shadow(2, 14)
    return c.out()


@reg("cherub_fungus")
def _():
    c = C()
    halo(c)
    c.ell(7.5, 10, 7, 4.5, "1")
    c.r(0, 11, 15, 14, ".")
    c.r(1, 11, 14, 13, "3")
    for x in range(2, 14, 2):
        c.p(x, 12, "2")
    c.r(2, 6, 12, 8, "1")
    c.r(10, 7, 14, 10, "2")
    for x, y in ((4, 6), (8, 5), (11, 7), (6, 8)):
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    c.r(5, 14, 10, 21, "w"); c.r(5, 14, 6, 21, "w"); c.r(9, 14, 10, 21, "l")
    c.r(7, 14, 8, 21, "w")
    c.p(6, 16, "O"); c.p(9, 16, "O"); c.r(7, 18, 8, 18, "O")
    c.p(6, 15, "O") if False else None
    c.r(4, 21, 11, 21, "L")
    c.shadow(2, 13)
    return c.out()


@reg("cherub_newly_sentient_being")
def _():
    c = C()
    halo(c, y=1)
    c.ell(7.5, 14, 5.3, 6.2, "2")
    c.ell(6.5, 13, 3.8, 5, "1")
    c.r(5, 5, 10, 7, "3"); c.r(6, 4, 9, 4, "2")            # rim/neck
    c.r(5, 5, 10, 5, "1")
    c.r(5, 12, 10, 12, "4"); c.r(5, 13, 10, 13, "5")       # painted band
    c.p(6, 9, "O"); c.p(9, 9, "O"); c.r(7, 10, 8, 10, "O") if False else None
    c.r(7, 11, 8, 11, "O")
    c.p(6, 9, "O"); c.p(9, 9, "O")
    c.line(8, 14, 9, 20, "O") if False else None
    c.p(9, 16, "O"); c.p(8, 17, "O"); c.p(9, 18, "O")      # crack
    c.r(1, 12, 2, 15, "2"); c.r(13, 12, 14, 15, "3")       # handles
    c.p(1, 11, "1"); c.p(14, 11, "2")
    c.r(5, 20, 10, 21, "3")
    c.shadow(1, 14)
    return c.out()


@reg("cherub_root")
def _():
    c = C()
    halo(c)
    c.ell(7.5, 12, 4, 4, "1")
    c.r(5, 9, 10, 11, "1"); c.r(9, 10, 10, 14, "2")
    c.p(6, 10, "O"); c.p(9, 10, "O"); c.r(7, 12, 8, 12, "O")
    # twisting roots as limbs
    c.line(4, 13, 1, 17, "2"); c.line(1, 17, 0, 21, "2"); c.line(5, 13, 3, 20, "1"); c.line(3, 20, 3, 22, "1")
    c.line(11, 13, 14, 17, "3"); c.line(14, 17, 15, 21, "3"); c.line(10, 14, 12, 20, "2")
    c.line(7, 15, 7, 21, "1"); c.line(8, 15, 9, 21, "2")
    c.line(5, 8, 3, 4, "2"); c.line(10, 8, 12, 4, "3"); c.line(7, 8, 7, 5, "1")
    c.p(3, 3, "4"); c.p(12, 3, "4"); c.p(7, 4, "5")
    c.r(2, 21, 5, 21, "3"); c.r(10, 21, 13, 21, "3")
    c.shadow(0, 15)
    return c.out()


@reg("cherub_tree")
def _():
    c = C()
    halo(c, y=0)
    c.ell(7.5, 6, 6.5, 4.2, "1")
    c.r(2, 7, 13, 8, "2"); c.r(9, 4, 13, 8, "2")
    for x, y in ((4, 5), (8, 3), (11, 6), (6, 7)):
        c.p(x, y, "4"); c.p(x + 1, y + 1, "5")
    c.r(6, 9, 9, 21, "w"); c.r(6, 9, 7, 21, "w"); c.r(9, 9, 9, 21, "l"); c.r(8, 9, 8, 21, "w") if False else None
    c.r(3, 19, 6, 21, "w"); c.r(9, 19, 12, 21, "l")
    c.line(6, 11, 2, 13, "w"); c.line(9, 11, 13, 13, "l")
    c.p(2, 14, "w"); c.p(13, 14, "l")
    c.p(6, 13, "O"); c.p(9, 13, "O"); c.r(7, 16, 8, 16, "O")
    c.p(7, 15, "O") if False else None
    c.shadow(2, 13)
    return c.out()


@reg("cherub_worm")
def _():
    c = C()
    halo(c, y=1)
    pts = [(5, 21), (10, 19), (6, 16), (10, 13), (7, 10), (7, 7)]
    tube(c, pts, 2.4, 2.8, "2")
    tube(c, [(p[0] - 0.8, p[1] - 0.5) for p in pts], 1.4, 1.6, "1")
    for (x, y) in ((8, 20), (9, 17), (8, 14), (9, 11), (7, 12), (6, 18)):
        c.r(x - 2, y, x + 1, y, "3") if False else None
    for y in (19, 16, 13, 10):
        for x in range(2, 14):
            if c.g[y][x] in "12":
                c.g[y][x] = "3" if (x + y) % 3 else "5"
    c.r(5, 4, 9, 8, "1"); c.r(5, 8, 9, 8, "2")
    c.r(6, 5, 6, 5, "O"); c.p(9, 5, "O") if False else None
    c.p(8, 5, "O"); c.p(6, 5, "O")
    c.r(6, 7, 8, 7, "O")
    c.shadow(2, 13)
    return c.out()


# =============================================================================== oddities
@reg("agolfly")
def _():
    c = C()
    # wings (veined glass), legs, thorax with glowing sac, abdomen
    c.ell(3.5, 10, 3.6, 5, "l"); c.ell(12.5, 10, 3.6, 5, "L")
    c.ell(3.5, 9.5, 2.4, 3.8, "w"); c.ell(12.5, 9.5, 2.4, 3.8, "l")
    c.line(5, 11, 1, 7, "L"); c.line(10, 11, 14, 7, "L")
    for y, x0, x1 in ((12, 4, 1), (14, 4, 2), (16, 5, 3)):
        c.line(x0, y, x1, y + 4, "6"); c.line(15 - x0, y, 15 - x1, y + 4, "6")
        c.p(x1, y + 5, "6"); c.p(15 - x1, y + 5, "6")
    c.ell(7.5, 11, 3.2, 3.2, "2")
    c.ell(7.5, 11, 2.2, 2.2, "4"); c.p(7, 10, "w"); c.p(8, 11, "5")
    c.ell(7.5, 17, 2.6, 3.8, "2"); c.r(8, 15, 9, 20, "3")
    for y in (15, 17, 19):
        c.r(6, y, 9, y, "3")
    for x, y in ((5, 9), (10, 9), (5, 12), (10, 13), (7, 20)):
        c.p(x, y, "5")                                       # warty sacs
    c.ell(7.5, 6, 2.4, 2, "1")
    c.p(6, 5, "R"); c.p(9, 5, "R"); c.p(5, 6, "R"); c.p(10, 6, "R"); c.r(7, 7, 8, 7, "3")
    c.p(6, 3, "O"); c.p(9, 3, "O")
    c.shadow(2, 13)
    return c.out()


@reg("bat")
def _():
    c = C()
    # wide membrane wings with scalloped edge
    for side in (0, 1):
        def X(x):
            return x if side == 0 else 15 - x
        for x in range(0, 6):
            top = 5 + (5 - x) // 2 if x < 3 else 6 + (x - 3)
            bot = (13, 15, 12, 14, 11, 12)[x]
            for y in range(top, bot + 1):
                c.p(X(x), y, "2" if y < bot - 1 else "3")
        c.line(X(5), 8, X(0), 4, "1"); c.line(X(5), 9, X(1), 6, "1") if False else None
        c.p(X(0), 5, "1")
        for x, y in ((2, 8), (3, 9), (1, 7)):
            c.p(X(x), y, "5")
    c.ell(7.5, 11, 2.8, 4.5, "2")
    c.r(8, 9, 9, 15, "3")
    c.r(5, 4, 6, 7, "3"); c.r(9, 4, 10, 7, "3")           # ears
    c.p(5, 4, "5"); c.p(10, 4, "5")
    c.r(5, 7, 10, 10, "1") if False else None
    c.ell(7.5, 8, 3, 2.6, "1")
    c.r(5, 6, 6, 8, "w"); c.r(9, 6, 10, 8, "w")           # broad eyes
    c.p(6, 7, "O"); c.p(9, 7, "O"); c.p(5, 7, "O") if False else None
    c.r(7, 9, 8, 9, "w"); c.p(7, 9, "O") if False else None
    c.p(7, 9, "R"); c.p(8, 9, "R") if False else None
    c.line(6, 15, 4, 17, "3"); c.line(9, 15, 11, 17, "3")
    c.shadow(2, 13)
    return c.out()


@reg("crystal")
def _():
    c = C()
    def prism(cx, top, bot, wd, base="2"):
        for y in range(top, bot + 1):
            t = (y - top) / max(1, bot - top)
            w = max(1, round(wd * min(1, 0.25 + t * 1.5)))
            c.r(cx - w, y, cx + w - 1, y, "2")
            c.r(cx - w, y, cx - 1, y, "1")
            c.r(cx + (w + 1) // 2, y, cx + w - 1, y, "3")
        c.line(cx, top + 1, cx, bot, "3")
        c.p(cx - 1, top + 1, "w"); c.p(cx - 1, top + 2, "w")
        c.p(cx, top, "w")
    prism(2, 10, 21, 2)
    prism(13, 9, 21, 2)
    prism(11, 12, 21, 2)
    prism(5, 11, 21, 3)
    prism(8, 1, 21, 3)
    c.p(8, 6, "4"); c.p(8, 10, "5"); c.p(5, 14, "4"); c.p(11, 15, "5"); c.p(8, 16, "4")
    c.p(2, 15, "5"); c.p(13, 14, "4"); c.p(9, 19, "w"); c.p(5, 18, "5")
    c.shadow(0, 15)
    return c.out()


@reg("eel")
def _():
    c = C()
    pts = [(13, 3), (11, 6), (5, 7), (3, 11), (9, 13), (12, 17), (6, 20)]
    tube(c, pts, 1.8, 2.8, "2") if False else None
    tube(c, list(reversed(pts)), 0.9, 2.6, "2")
    tube(c, [(x - 0.7, y - 0.6) for x, y in reversed(pts[1:])], 0.5, 1.6, "1")
    # dorsal fin ridge and belly
    for (x, y) in pts[1:6]:
        c.p(round(x + 1.5), round(y), "3")
    # head
    c.ell(13, 3.5, 2.8, 2.2, "2")
    c.r(13, 1, 15, 2, "2"); c.r(14, 4, 15, 5, "1")
    c.p(14, 2, "O"); c.p(11, 3, "O") if False else None
    c.r(13, 4, 15, 4, "O"); c.p(14, 5, "w") if False else None
    c.p(15, 3, "w") if False else None
    # circular gills
    for (x, y) in ((11, 5), (9, 7), (4, 9)):
        c.p(x, y, "4"); c.p(x + 1, y, "5"); c.p(x, y + 1, "5"); c.p(x + 1, y + 1, "4")
    c.line(6, 20, 3, 22, "3"); c.line(6, 20, 8, 22, "3")
    c.shadow(1, 14)
    return c.out()


@reg("galgal")
def _():
    c = C()
    def wheel(cx, cy, r):
        c.ell(cx, cy, r, r, "5")
        c.ell(cx, cy, r - 1.2, r - 1.2, ".")
        for dx, dy in ((1, 0), (0, 1), (-1, 0), (0, -1), (0.7, 0.7), (-0.7, -0.7), (0.7, -0.7), (-0.7, 0.7)):
            c.line(cx, cy, round(cx + dx * (r - 1)), round(cy + dy * (r - 1)), "l")
        c.p(round(cx), round(cy), "w")
    wheel(4, 5, 4); wheel(12, 5, 4); wheel(8, 18, 4.3)
    c.r(7, 8, 8, 14, "l") if False else None
    c.line(5, 6, 7, 11, "L"); c.line(11, 6, 9, 11, "L"); c.line(8, 14, 8, 15, "L")
    c.ell(7.5, 11, 3.6, 3.6, "2")
    c.ell(7, 10.5, 2.4, 2.4, "1")
    c.p(6, 9, "w"); c.p(8, 12, "4"); c.p(7, 13, "5")
    c.p(9, 10, "4"); c.p(6, 11, "w")
    c.p(7, 8, "w") if False else None
    c.shadow(2, 13)
    return c.out()


@reg("godhed1_unplanished")
def _():
    c = C()
    c.ell(7.5, 10.5, 5.2, 8, "l")
    c.ell(7, 9.5, 4, 6.5, "w") if False else None
    c.r(9, 6, 12, 15, "L")
    c.r(3, 6, 5, 14, "w")
    # sensory pane: dull glass window, unplanished
    c.r(5, 5, 10, 11, "O"); c.r(6, 6, 9, 10, "2")
    c.r(6, 6, 7, 7, "1"); c.p(7, 8, "5") if False else None
    c.p(8, 9, "3"); c.p(9, 10, "3")
    # circuit lines, glowing
    c.line(3, 13, 5, 13, "4"); c.line(5, 13, 5, 15, "4"); c.line(10, 12, 12, 12, "4"); c.line(12, 12, 12, 10, "5")
    c.p(8, 13, "4"); c.p(7, 14, "5"); c.p(9, 14, "4")
    c.r(6, 2, 9, 3, "L"); c.p(7, 2, "w")
    c.r(7, 0, 8, 1, "L"); c.p(7, 0, "4")
    c.r(4, 17, 11, 18, "L"); c.r(4, 17, 11, 17, "l")
    c.r(6, 19, 9, 19, "4"); c.r(7, 20, 8, 21, "5")
    c.r(3, 20, 3, 21, "4") if False else None
    c.shadow(2, 13)
    return c.out()




@reg("golem_lichen")
def _():
    c = C()
    # stooped lump-figure crusted in frilled lichen rosettes
    c.ell(7.5, 14, 6, 6.5, "2")
    c.ell(7.5, 6, 3.6, 3.2, "2")
    c.r(2, 9, 13, 11, "2")
    c.r(1, 12, 3, 19, "2"); c.r(12, 12, 14, 19, "3")        # arms
    c.r(4, 18, 6, 21, "3"); c.r(9, 18, 11, 21, "3")
    for (x, y, r) in ((4, 5, 1.6), (11, 6, 1.4), (3, 11, 2), (11, 12, 2), (7, 14, 2), (5, 17, 1.6), (10, 18, 1.5),
                      (2, 16, 1.2), (13, 16, 1.2), (8, 9, 1.4)):
        c.ell(x, y, r, r, "1")
        c.ell(x, y, r - 0.8, r - 0.8, "4") if r > 1.3 else None
        c.p(round(x), round(y), "5") if r > 1.5 else None
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.r(7, 7, 8, 7, "O")
    c.p(6, 5, "w"); c.p(9, 5, "w")
    c.r(2, 21, 5, 21, "1"); c.r(10, 21, 13, 21, "1")
    c.p(1, 19, "1"); c.p(14, 19, "1")
    c.shadow(0, 15)
    return c.out()


@reg("leering_stalker")
def _():
    c = C()
    c.line(4, 1, 6, 7, "L"); c.line(11, 1, 9, 7, "L")
    c.p(4, 0, "R"); c.p(11, 0, "R")
    # casket body
    c.r(3, 6, 12, 15, "l"); c.r(3, 6, 12, 7, "w"); c.r(10, 7, 12, 15, "L")
    c.r(4, 8, 9, 14, "2"); c.r(4, 8, 9, 9, "1"); c.r(8, 8, 9, 14, "3")
    # leering eye + grin slit
    c.r(5, 9, 8, 11, "O"); c.p(5, 10, "R"); c.p(8, 10, "R"); c.r(6, 9, 7, 11, "R"); c.p(6, 10, "w") if False else None
    c.p(7, 10, "O"); c.p(6, 10, "4")
    c.r(5, 13, 8, 13, "O"); c.p(5, 13, "4"); c.p(7, 13, "4")
    # four press legs
    for x in (0, 2, 11, 13):
        c.r(x, 12, x + 1, 16, "L")
    for x in (0, 13):
        c.r(x, 17, x + 2 if x == 13 else x + 1, 20, "l"); c.r(x - (0 if x == 0 else 0), 21, x + 2, 21, "L")
    c.r(2, 16, 3, 21, "l"); c.r(11, 16, 12, 21, "L")
    c.r(0, 21, 4, 22, "L"); c.r(11, 21, 15, 22, "L")
    c.r(1, 17, 1, 20, "l"); c.r(14, 17, 14, 20, "L")
    c.r(5, 16, 10, 17, "L")
    c.shadow(0, 15)
    return c.out()


@reg("mopango")
def _():
    c = C()
    # ruffled pelerine around the neck, scaled body with inner glow, tail
    tube(c, [(9, 15), (12, 17), (14, 20)], 1.8, 0.7, "2")
    c.r(5, 10, 10, 18, "2"); c.r(5, 10, 6, 18, "1"); c.r(9, 11, 10, 18, "3")
    for y in range(11, 18, 2):
        for x in range(6, 10):
            c.p(x, y, "5" if (x + y) % 2 else "4")
    c.r(7, 12, 8, 15, "4"); c.p(7, 13, "w")
    c.r(4, 11, 4, 14, "2"); c.r(11, 11, 11, 14, "3")
    c.p(3, 15, "S") if False else None
    c.r(3, 14, 4, 15, "w"); c.r(11, 14, 12, 15, "w")
    c.r(5, 3, 10, 6, "2"); c.r(5, 3, 10, 3, "1"); c.r(10, 3, 10, 6, "3")
    c.r(2, 5, 6, 7, "1") if False else None
    c.r(3, 5, 6, 6, "2"); c.p(2, 6, "1")                 # snout
    c.p(5, 4, "O"); c.p(8, 4, "O")
    c.p(3, 5, "O")
    c.p(3, 7, "w"); c.p(5, 7, "w")
    # frilled ruffle
    c.r(2, 8, 13, 9, "4"); c.r(3, 10, 12, 10, "5")
    for x in (2, 4, 6, 8, 10, 12):
        c.p(x, 7, "4"); c.p(x + 1, 10, "4")
    c.p(3, 8, "6"); c.p(9, 9, "6")
    c.r(5, 19, 6, 21, "2"); c.r(9, 19, 10, 21, "3")
    c.r(4, 21, 7, 21, "w"); c.r(8, 21, 11, 21, "w")
    c.shadow(2, 14)
    return c.out()


# ---- natural weapons: big, centred icons
@reg("natural_weapon_beak")
def _():
    c = C()
    # side-on hooked beak pointing down-left, open
    for y in range(3, 14):                                   # upper mandible
        x1 = 14 - round((y - 3) * 0.55)
        c.r(2 + (y > 9) * round((y - 9) * 0.8), y, x1, y, "2")
    c.r(2, 3, 14, 4, "1")
    c.r(2, 3, 9, 5, "1")
    c.r(11, 5, 14, 12, "3")
    c.p(8, 7, "O"); c.p(9, 7, "O")                           # nostril
    c.line(4, 6, 2, 11, "1") if False else None
    c.line(2, 5, 2, 10, "1"); c.p(3, 11, "1"); c.p(4, 12, "w"); c.p(4, 13, "w"); c.p(5, 14, "w")
    c.r(5, 15, 14, 17, "2"); c.r(2, 17, 14, 19, "2") if False else None
    c.r(3, 16, 14, 18, "3"); c.r(3, 16, 11, 16, "2"); c.r(2, 16, 4, 17, "1")
    c.r(7, 14, 12, 14, "O"); c.r(5, 14, 6, 15, "O")
    c.p(2, 15, "w"); c.p(3, 15, "w")
    c.p(6, 4, "w"); c.p(5, 4, "w")
    c.shadow(2, 13, y=21)
    return c.out()


@reg("natural_weapon_frond")
def _():
    c = C()
    for pts in (((8, 21), (6, 16), (8, 11), (5, 6), (7, 2)), ((8, 21), (11, 17), (10, 12), (13, 8), (11, 3))):
        tube(c, pts, 1.7, 0.7, "2")
    for pts in (((8, 21), (4, 18), (2, 13), (3, 9)),):
        tube(c, pts, 1.2, 0.6, "3")
    for x, y, ch in ((5, 14, "1"), (7, 9, "1"), (6, 5, "1"), (11, 11, "1"), (12, 6, "1"), (4, 11, "h"), (2, 11, "h")):
        c.r(x - 1, y, x + 1, y, ch)
        c.p(x + 1, y - 1, ch)
    for x, y in ((6, 17), (10, 15), (9, 8), (7, 13)):
        c.p(x, y, "h")
    c.p(7, 2, "h"); c.p(11, 3, "h")
    c.shadow(4, 11, y=22)
    return c.out()


@reg("natural_weapon_manipulator")
def _():
    c = C()
    c.r(5, 15, 10, 21, "l"); c.r(5, 15, 10, 15, "w"); c.r(9, 16, 10, 21, "L")
    c.r(6, 17, 9, 19, "2"); c.p(7, 18, "4"); c.p(8, 18, "5")
    # two pincer fingers + thumb
    c.r(4, 9, 6, 14, "l"); c.r(9, 9, 11, 14, "L")
    c.r(3, 4, 5, 9, "l"); c.r(10, 4, 12, 9, "L")
    c.r(4, 2, 5, 4, "w"); c.r(10, 2, 11, 4, "l")
    c.p(5, 9, "L"); c.p(10, 9, "l")
    c.r(7, 11, 8, 13, "L"); c.p(7, 12, "4")
    c.r(1, 13, 3, 14, "l"); c.p(0, 13, "w")                   # thumb
    c.p(4, 4, "L"); c.p(5, 6, "L") if False else None
    c.shadow(3, 12, y=22)
    c.r(5, 22, 10, 22, "L")
    return c.out()


@reg("natural_weapon_thorns")
def _():
    c = C()
    c.r(4, 11, 11, 20, "2"); c.r(4, 11, 6, 20, "1"); c.r(10, 11, 11, 20, "3")
    for y in (13, 16, 19):
        c.r(4, y, 11, y, "3")
    c.p(6, 15, "1"); c.p(8, 18, "1")
    for x, y0, dx in ((4, 10, -1), (7, 9, 0), (10, 10, 1), (5, 12, -2), (11, 14, 2)):
        pass
    c.line(5, 11, 3, 4, "w"); c.line(8, 11, 8, 2, "w"); c.line(10, 11, 13, 4, "w")
    c.line(4, 13, 0, 11, "w"); c.line(11, 14, 15, 11, "w"); c.line(4, 17, 1, 16, "w"); c.line(11, 18, 14, 17, "w")
    for x, y in ((3, 4), (8, 2), (13, 4), (0, 11), (15, 11), (1, 16), (14, 17)):
        c.p(x, y, "y")
    c.p(7, 14, "L") if False else None
    c.shadow(3, 12, y=21)
    return c.out()


@reg("ooze")
def _():
    c = C()
    c.ell(7.5, 13, 6.6, 7.4, "3")
    c.ell(7.5, 13, 5.6, 6.4, "2")
    c.ell(7, 12, 4.4, 5, "1")
    c.r(2, 18, 13, 20, "3"); c.r(3, 17, 12, 17, "2")
    c.r(1, 21, 14, 21, "3"); c.p(0, 21, "3") if False else None
    c.p(4, 8, "w"); c.p(5, 7, "w"); c.p(5, 8, "w"); c.p(4, 9, "w")      # glass glint
    for x, y, ch in ((9, 11, "4"), (6, 14, "4"), (10, 15, "5"), (8, 9, "5"), (7, 17, "4")):
        c.p(x, y, ch); c.p(x + 1, y, ch) if ch == "4" else None
        c.p(x, y + 1, "w") if ch == "4" else None
    c.p(11, 14, "5"); c.p(5, 12, "5")
    c.line(2, 21, 0, 22, "3") if False else None
    c.shadow(1, 14)
    return c.out()


@reg("reef_slug")
def _():
    c = C()
    pts = [(14, 18), (10, 16), (6, 15), (3, 13)]
    tube(c, pts, 3.2, 2.8, "2")
    tube(c, [(x, y - 1.2) for x, y in pts], 2.2, 2.0, "1")
    for x in range(3, 15, 3):                          # stripes
        c.line(x, 12 + (x < 7) - (x > 10) * 0, x + 1, 19, "4") if False else None
    for x, ch in ((5, "4"), (7, "5"), (9, "4"), (11, "5"), (13, "4")):
        for y in range(11, 21):
            if c.g[y][x] in "123":
                c.g[y][x] = ch
    c.r(2, 19, 15, 21, ".") if False else None
    c.r(2, 18, 14, 20, "3") if False else None
    for x in range(1, 16):
        if c.g[21][x] == "." and c.g[20][x] != ".":
            pass
    c.r(2, 19, 14, 20, "3")
    c.r(3, 20, 15, 21, "3") if False else None
    c.ell(3, 12, 2.4, 2.4, "1")
    c.line(2, 10, 1, 5, "2"); c.line(4, 10, 5, 4, "2")
    c.p(1, 4, "4"); c.p(5, 3, "4"); c.p(1, 5, "w") if False else None
    c.p(1, 4, "w"); c.p(5, 3, "w")
    c.p(3, 12, "O")
    c.p(14, 18, "3"); c.p(15, 18, "3") if False else None
    c.p(8, 11, "w"); c.p(12, 12, "w")
    c.shadow(0, 15)
    return c.out()


@reg("rodanis")
def _():
    c = C()
    # scrap giant: flange torso, wye-pipe shoulders, piston arms, tailstock legs on treads
    c.r(5, 1, 10, 5, "l"); c.r(5, 1, 10, 1, "w"); c.r(10, 2, 10, 5, "L")
    c.r(6, 3, 9, 3, "O"); c.p(6, 3, "4"); c.p(9, 3, "4"); c.p(7, 3, "5")
    c.p(7, 0, "L"); c.p(8, 0, "4")
    c.r(1, 6, 14, 8, "L"); c.r(1, 6, 14, 6, "l"); c.p(1, 6, "w")
    c.r(3, 9, 12, 15, "2"); c.r(3, 9, 12, 10, "1"); c.r(10, 11, 12, 15, "3")
    c.r(3, 9, 3, 15, "1")
    c.r(6, 11, 9, 13, "L"); c.p(7, 12, "4"); c.p(8, 12, "5")
    for x, y in ((4, 10), (11, 10), (4, 14), (11, 14), (7, 15), (8, 9)):
        c.p(x, y, "w")
    c.r(0, 8, 2, 8, "L") if False else None
    c.r(0, 9, 2, 13, "l"); c.r(0, 9, 0, 13, "w"); c.r(1, 14, 2, 18, "L"); c.r(0, 18, 3, 20, "L"); c.p(0, 20, "l")
    c.r(13, 9, 15, 13, "L"); c.r(13, 14, 14, 18, "l"); c.r(12, 18, 15, 21, "L")           # pressing plate
    c.p(12, 19, "l") if False else None
    c.r(4, 16, 11, 16, "L")
    c.r(5, 17, 6, 19, "l"); c.r(9, 17, 10, 19, "L")
    c.r(2, 20, 13, 22, "O"); c.r(2, 20, 13, 20, "L")
    for x in range(3, 13, 2):
        c.p(x, 21, "l")
    c.shadow(1, 14)
    return c.out()


@reg("sowerseed")
def _():
    c = C()
    c.ell(7.5, 14, 4.8, 6, "2")
    c.ell(7, 13, 3.6, 5, "1")
    c.r(9, 10, 12, 18, "3") if False else None
    c.ell(8, 15, 2, 2.6, "4"); c.p(8, 14, "w"); c.p(8, 16, "5")
    c.r(11, 12, 12, 19, "3")
    c.p(5, 9, "w"); c.p(5, 10, "w") if False else None
    c.line(7, 8, 7, 5, "g"); c.line(7, 5, 5, 3, "g"); c.line(7, 6, 10, 3, "h")
    c.r(3, 2, 5, 3, "g"); c.r(9, 2, 11, 3, "h"); c.p(5, 4, "h")
    c.p(3, 3, "G"); c.p(11, 3, "g")
    c.r(5, 20, 10, 20, "3")
    c.shadow(2, 13, y=21) if False else c.shadow(2, 13)
    return c.out()


@reg("svardym")
def _():
    c = C()
    # weary frogfolk: hunched, big sagging tympana, wide mouth, leaf-wet
    c.ell(7.5, 14, 5.5, 5.5, "2")
    c.r(4, 10, 11, 10, "2")
    c.r(3, 6, 12, 10, "2"); c.r(3, 6, 12, 6, "1"); c.r(10, 7, 12, 10, "3")
    c.p(4, 5, "1"); c.p(11, 5, "2")
    c.r(3, 4, 5, 5, "1"); c.r(10, 4, 12, 5, "2")                   # eye bumps
    c.p(4, 4, "w"); c.p(11, 4, "w"); c.p(4, 5, "O"); c.p(11, 5, "O")
    c.r(4, 9, 11, 9, "O") if False else None
    c.r(5, 9, 10, 9, "3"); c.p(5, 8, "O"); c.p(10, 8, "O")
    c.ell(2, 9.5, 1.6, 2.2, "4"); c.ell(13, 9.5, 1.6, 2.2, "5")   # sagging tympana
    c.ell(2, 10, 0.9, 1.3, "6"); c.ell(13, 10, 0.9, 1.3, "6")
    c.r(6, 13, 9, 18, "1"); c.r(7, 14, 8, 17, "w")
    c.r(2, 12, 3, 17, "2"); c.r(12, 12, 13, 17, "3")
    c.r(1, 18, 4, 18, "1"); c.r(11, 18, 14, 18, "1")
    c.p(1, 19, "1"); c.p(3, 19, "1"); c.p(12, 19, "1"); c.p(14, 19, "1")
    c.r(4, 18, 6, 20, "3"); c.r(9, 18, 11, 20, "3")
    c.r(2, 21, 6, 21, "2"); c.r(9, 21, 13, 21, "2")
    c.r(1, 22, 1, 22, "2") if False else None
    c.p(5, 12, "h"); c.p(10, 14, "h")
    c.shadow(0, 15)
    return c.out()


@reg("tillifergaewicz")
def _():
    c = C()
    # inflated pod-body on coiled vines, basking: soft glow patches
    c.ell(7.5, 10, 6.4, 6.2, "2")
    c.ell(6.5, 8.5, 4.6, 4.2, "1")
    c.r(10, 8, 13, 14, "3")
    c.ell(7.5, 10, 6.4, 6.2, "2") if False else None
    for x, y in ((5, 6), (9, 5), (11, 9), (4, 11), (8, 12), (7, 8)):
        c.p(x, y, "4"); c.p(x + 1, y, "5") if x < 8 else c.p(x, y + 1, "5")
    c.p(5, 5, "w"); c.p(6, 5, "w")
    c.p(6, 9, "O"); c.p(9, 9, "O") if False else None
    # vines coiled below
    tube(c, [(7, 16), (3, 17), (4, 20), (8, 21)], 1.1, 1.1, "G")
    tube(c, [(8, 16), (12, 17), (11, 20), (7, 21)], 1.1, 1.1, "g")
    c.r(6, 15, 9, 17, "g")
    c.line(2, 12, 0, 8, "G"); c.line(13, 12, 15, 8, "g")
    c.r(0, 7, 1, 7, "h"); c.r(14, 7, 15, 7, "h")
    c.p(5, 18, "h"); c.p(10, 19, "h")
    c.r(0, 15, 2, 16, "g"); c.r(13, 15, 15, 16, "G")
    c.shadow(1, 14)
    return c.out()


@reg("urchin_belcher")
def _():
    c = C()
    # mammoth fish dragging itself; gaping mouth on the left full of clinging urchins
    c.ell(9, 13, 6.5, 6, "2")
    c.r(7, 8, 13, 10, "1"); c.r(4, 10, 14, 11, "1") if False else None
    c.r(9, 16, 14, 19, "3")
    c.r(0, 8, 5, 18, "2")
    c.r(0, 8, 5, 8, "1")
    c.r(0, 10, 4, 16, "O")                                   # cavernous mouth
    c.r(0, 9, 5, 9, "w"); c.r(0, 17, 5, 17, "w")
    for x in (0, 2, 4):
        c.p(x, 10, "w"); c.p(x + 1, 16, "w") if False else None
    c.p(1, 16, "w"); c.p(3, 16, "w")
    def urchin(x, y, r=1.3):
        c.ell(x, y, r, r, "4")
        for dx, dy in ((-2, 0), (2, 0), (0, -2), (0, 2), (-1.5, -1.5), (1.5, 1.5), (1.5, -1.5), (-1.5, 1.5)):
            c.p(round(x + dx), round(y + dy), "5")
        c.p(round(x), round(y), "6")
    urchin(2, 12); urchin(4, 14, 1.0); urchin(2, 15, 0.8) if False else None
    c.p(6, 9, "w"); c.p(7, 9, "O")
    c.ell(8, 9, 1.2, 1.2, "w"); c.p(8, 9, "O")
    # soft-rayed fins
    c.line(11, 7, 13, 3, "3"); c.line(13, 8, 15, 4, "3"); c.line(9, 7, 11, 3, "1")
    c.line(14, 12, 15, 15, "3"); c.line(14, 16, 15, 19, "3")
    c.line(8, 18, 5, 21, "3"); c.line(10, 19, 9, 22, "3"); c.line(12, 19, 13, 22, "3")
    c.shadow(0, 15)
    return c.out()


@reg("weeds")
def _():
    c = C()
    blades = [(2, 13, "g"), (4, 8, "w"), (6, 11, "g"), (8, 5, "w"), (10, 10, "g"), (12, 7, "w"), (14, 12, "g"), (7, 14, "w"), (11, 15, "g"), (4, 16, "w"), (9, 3, "w")]
    for x, top, ch in blades:
        sway = 1 if x % 4 == 0 else -1
        for y in range(top, 22):
            xx = x + (sway if y < top + (22 - top) // 2 else 0)
            c.p(xx, y, ch if ch == "w" else "g")
            if y > 17:
                c.p(xx + 1, y, "w")
    # tips and foam
    for x, top, ch in blades:
        c.p(x + (1 if x % 4 == 0 else -1), top, "4")
    for x, y in ((3, 18), (6, 20), (9, 19), (12, 20), (5, 12), (10, 12), (7, 9), (13, 15), (2, 16)):
        c.p(x, y, "w"); c.p(x + 1, y - 1, "w") if y % 2 else None
    c.r(0, 21, 15, 21, "w") if False else None
    c.r(1, 21, 14, 21, "g")
    for x in range(1, 15, 3):
        c.p(x, 21, "w")
    c.shadow(0, 15)
    return c.out()
