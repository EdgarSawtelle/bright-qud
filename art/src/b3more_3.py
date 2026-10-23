"""B3 remaining creatures, batch more_3: humanoid oddities, chiliad beasts, cherubs, golems, machines."""
import math
from functools import partial
from b3more_keys import MORE_KEYS
from b3kit import (C, back, person, tunic, hood, halo, armor, apron, goggles_up, wrench, hammer, hoe, staff,
                   cape, hair_wild, veil, scarf, pack, sickle, spear, club, shoulder_scrap, belt_pouches)

KEYS = MORE_KEYS[3]
HUMANOID = {"baboon", "cherub_baboon", "chime", "dromad", "goatfolk", "golem_hindren", "gyrewight",
            "mechanimist_paladin", "naphtaali_tinker", "rokhas", "slynth_grit_gate", "stranger", "urshiib"}


def tube(c, pts, r0, r1, ch):
    d = [0.0]
    for (a, b), (e, f) in zip(pts, pts[1:]):
        d.append(d[-1] + ((e - a) ** 2 + (f - b) ** 2) ** 0.5)
    tot = d[-1] or 1
    n = int(tot * 3) + 1
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


def poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            ins = False
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    ins = not ins
            if ins:
                c.p(x, y, ch)


def fin(c, sh=(1, 14)):
    c.shadow(sh[0], sh[1])
    return c.out()


def halo_c(c, x=8):
    """cherub halo, floating."""
    c.r(x - 2, 0, x + 1, 0, "4")
    c.p(x - 3, 1, "4"); c.p(x + 2, 1, "4")
    c.p(x - 2, 1, "5"); c.p(x + 1, 1, "5")


# ================================================================== HUMANOIDS
# ---- baboon -----------------------------------------------------------------------------------
def baboon_head(c, mane="1"):
    c.r(5, 2, 10, 2, "3")
    c.r(6, 1, 9, 1, "3")
    c.r(5, 3, 10, 3, "2")
    c.r(5, 4, 10, 4, "3")           # heavy brow
    c.r(7, 4, 8, 4, "2")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "4")            # long red muzzle
    c.r(7, 6, 8, 6, "5")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.r(6, 7, 9, 7, "5"); c.p(7, 7, "w"); c.p(8, 7, "w")
    c.p(5, 6, "2"); c.p(10, 6, "3"); c.p(5, 7, "3"); c.p(10, 7, "3")
    c.r(3, 8, 12, 10, mane)         # fur mantle
    c.r(10, 8, 12, 10, "2"); c.r(3, 8, 5, 8, "1")
    c.r(7, 8, 8, 8, "3")
    for x in (3, 5, 7, 9, 11):
        c.p(x, 11, mane)


@back
def baboon_tail(c):
    tube(c, [(11, 19), (14, 17), (15, 12), (13, 8)], 0.9, 0.7, "3")
    c.p(13, 7, "5"); c.p(12, 7, "5")


@back
def wing_small(c, a="w", b="l"):
    c.line(5, 9, 0, 3, a, mirror=True)
    c.line(5, 10, 0, 4, a, mirror=True)
    c.line(5, 11, 0, 7, a, mirror=True)
    c.r(1, 5, 3, 8, a); c.r(12, 5, 14, 8, a)
    c.r(1, 8, 2, 11, b); c.r(13, 8, 14, 11, b)
    c.m(0, 3, "w"); c.m(1, 4, "w"); c.m(2, 6, "w")


def baboon():
    return person(baboon_tail, baboon_head, partial(tunic, a="5", b="6", legs="3"),
                  face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


def cherub_baboon():
    return person(wing_small, baboon_head, partial(tunic, a="5", b="6", legs="3"), halo,
                  face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


# ---- chime: octahedron crystal -----------------------------------------------------------------
def chime_head(c):
    # floating octahedron: apex at row 0, waist row 4, base row 8
    rows = {0: (7, 8), 1: (6, 9), 2: (5, 10), 3: (4, 11), 4: (4, 11), 5: (5, 10), 6: (5, 10), 7: (6, 9), 8: (7, 8)}
    for y, (a, b) in rows.items():
        c.r(a, y, b, y, "2")
    # facets
    for y in range(0, 5):
        c.r(rows[y][0], y, 7, y, "1")
        c.r(9, y, rows[y][1], y, "3")
    c.r(7, 0, 7, 8, "w")
    for y in range(5, 8):
        c.r(rows[y][0], y, 7, y, "2")
        c.r(8, y, rows[y][1], y, "3")
    c.r(4, 3, 11, 3, "w")
    c.p(6, 2, "w")
    c.p(9, 5, "O"); c.p(6, 5, "O")
    c.p(4, 3, "1"); c.p(11, 3, "3")
    c.p(2, 1, "4"); c.p(13, 6, "4"); c.p(3, 7, "4")      # refracted light
    c.p(7, 8, "S"); c.p(8, 8, "S")


def chime_body(c):
    c.r(5, 9, 10, 9, "6")
    c.r(7, 8, 8, 8, "L")


def chime():
    g = person(chime_head, chime_body, face="none", sash=True, trim="4", body="2", lite="1", dark="3")
    return g


# ---- dromad: camel --------------------------------------------------------------------------------
@back
def hump(c):
    c.ell(12.5, 11, 3, 4, "2")
    c.ell(12, 9.5, 2, 2.5, "1")
    c.r(14, 10, 15, 14, "3")


def dromad_head(c):
    c.r(5, 2, 6, 3, "2"); c.r(9, 2, 10, 3, "2")       # ears
    c.p(5, 1, "3"); c.p(10, 1, "3")
    c.r(6, 3, 9, 3, "2")
    c.r(5, 4, 10, 5, "2"); c.r(10, 4, 10, 5, "3")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "1")                              # long muzzle
    c.r(7, 6, 8, 6, "2")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.r(6, 6, 6, 7, "1"); c.p(9, 7, "3")
    c.r(7, 8, 8, 8, "2")
    c.r(6, 4, 9, 4, "3") if False else None
    c.p(7, 3, "1"); c.p(8, 3, "1")
    c.r(7, 2, 8, 2, "3")                              # topknot tuft


def dromad():
    return person(hump, dromad_head, partial(scarf, a="4", b="5"), face="none", skin=("2", "3"),
                  body="2", lite="1", dark="3", trim="4")


# ---- goatfolk ---------------------------------------------------------------------------------------
def goat_horns(c):
    c.mr(3, 3, 4, 3, "w")
    c.mr(2, 2, 3, 2, "w")
    c.mr(1, 0, 2, 1, "w")
    c.m(2, 3, "w"); c.m(1, 2, "L"); c.m(2, 1, "L"); c.m(1, 0, "t")
    c.m(3, 4, "L")


def goat_face(c):
    c.r(6, 2, 9, 2, "2")
    c.r(5, 3, 10, 3, "1")
    c.r(5, 4, 10, 5, "2")
    c.r(10, 4, 10, 6, "3")
    c.mr(3, 4, 4, 5, "2")                              # side ears
    c.m(3, 5, "3")
    c.p(6, 5, "y"); c.p(9, 5, "y")
    c.p(6, 4, "O"); c.p(9, 4, "O") if False else None
    c.r(6, 6, 9, 7, "1")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.r(7, 8, 8, 10, "w")                              # goatee
    c.p(7, 11, "w"); c.p(8, 11, "L")


def goatfolk():
    return person(goat_horns, goat_face, partial(tunic, a="2", b="3", legs="3"), partial(hoe),
                  face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


# ---- golem_hindren ------------------------------------------------------------------------------------
def hindren_parts(c):
    # lumpy mismatched head, one eye socket, one diode, stitched mouth, bolt
    c.r(5, 3, 10, 7, "2")
    c.r(6, 2, 8, 2, "2"); c.r(4, 4, 4, 6, "1"); c.p(9, 2, "1")
    c.r(5, 3, 5, 6, "1"); c.r(10, 3, 10, 7, "3"); c.r(5, 7, 9, 7, "3")
    c.p(6, 4, "O"); c.p(7, 4, "O"); c.r(9, 5, 9, 5, "4"); c.p(9, 4, "O"); c.p(10, 5, "O") if False else None
    c.p(6, 5, "w")
    c.r(6, 6, 9, 6, "O")
    for x in (6, 8):
        c.p(x, 7, "O")
    c.p(11, 5, "L"); c.p(12, 5, "l")                   # neck bolt
    c.p(11, 3, "L"); c.p(4, 5, "l"); c.p(4, 4, "L")
    # patch of scrap plate on the body, big mismatched right arm
    c.r(5, 10, 7, 12, "l"); c.r(5, 10, 7, 10, "w"); c.r(7, 11, 7, 12, "L")
    c.p(5, 12, "O"); c.p(6, 11, "O") if False else None
    c.r(11, 9, 13, 16, "2"); c.r(12, 9, 13, 11, "1"); c.r(13, 12, 13, 16, "3")
    c.r(11, 17, 14, 18, "3"); c.r(11, 16, 14, 16, "2")
    c.line(8, 13, 9, 15, "O"); c.p(8, 14, "w") if False else None
    c.p(8, 11, "4"); c.p(9, 12, "5")                   # diodes
    c.r(3, 10, 4, 13, "3") if False else None
    c.p(4, 13, "L"); c.p(4, 14, "l")
    c.r(3, 16, 4, 16, "L")                             # small arm stub
    c.p(11, 10, "O"); c.p(11, 13, "O")


def golem_hindren():
    return person(hindren_parts, face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


# ---- gyrewight ---------------------------------------------------------------------------------------
@back
def snood(c):
    c.r(3, 3, 12, 19, "6")
    c.r(2, 10, 13, 20, "6")
    c.r(1, 15, 14, 22, "6")
    c.r(1, 15, 3, 22, "5")
    c.r(12, 15, 14, 22, "6")
    c.p(14, 22, "5"); c.p(1, 22, "4"); c.p(4, 22, "4")


def spiral_sigil(c):
    c.r(7, 11, 9, 13, "4")
    c.p(8, 12, "6"); c.p(9, 12, "O") if False else None
    c.p(7, 11, "w"); c.p(8, 13, "w") if False else None
    c.p(9, 13, "5"); c.p(8, 12, "6")
    c.r(7, 15, 8, 15, "4")


def gyrewight():
    return person(snood, hood, spiral_sigil, face="face", sash=False, body="2", lite="1", dark="3", trim="4")


# ---- mechanimist_paladin --------------------------------------------------------------------------------
def ladder_braids(c):
    for x0 in (3, 11):
        c.r(x0, 4, x0, 13, "4")
        c.r(x0 + 1, 4, x0 + 1, 13, "4")
        for y in range(5, 14, 2):
            c.r(x0, y, x0 + 1, y, "6")
        c.p(x0, 14, "5"); c.p(x0 + 1, 14, "5")
    c.p(3, 3, "4"); c.p(12, 3, "4")


def paladin_armor(c):
    c.mr(2, 9, 4, 10, "w")                  # broad pauldrons
    c.mr(2, 9, 2, 9, "w")
    c.mr(3, 10, 4, 10, "l")
    c.mr(2, 11, 3, 11, "4")
    c.r(6, 11, 9, 13, "5")
    c.r(6, 11, 9, 11, "4")
    c.p(7, 12, "w"); c.p(8, 12, "w")
    c.r(5, 15, 10, 15, "4")
    c.p(7, 15, "w"); c.p(8, 15, "w")


def mechanimist_paladin():
    return person(ladder_braids, paladin_armor, partial(hammer), face="face", sash=False,
                  body="1", lite="1", dark="2", trim="4")


# ---- naphtaali_tinker ----------------------------------------------------------------------------------
def moss_fur(c):
    c.r(4, 8, 11, 10, "1")
    for x in (4, 6, 8, 10):
        c.p(x, 11, "1")
    c.p(11, 11, "2")
    c.mr(4, 2, 5, 3, "2")                   # round fur ears
    c.mr(4, 2, 4, 2, "1")
    c.r(5, 3, 10, 3, "1")
    c.r(5, 4, 5, 7, "1"); c.r(10, 4, 10, 7, "2")
    c.p(6, 5, "c"); c.p(9, 5, "c")          # big scanning eyes
    c.p(6, 4, "O"); c.p(9, 4, "O")
    c.r(6, 6, 9, 7, "4"); c.r(6, 7, 9, 7, "5")   # minyan mask
    c.p(7, 6, "O"); c.p(8, 6, "O") if False else None
    c.p(8, 8, "6")


def naphtaali_tinker():
    return person(moss_fur, apron, partial(wrench, glow="c"), face="none", sash=False,
                  body="2", lite="1", dark="3", skin=("1", "2"))


# ---- rokhas ----------------------------------------------------------------------------------------------
def rokhas_head(c):
    c.r(6, 2, 9, 2, "S"); c.r(5, 3, 10, 3, "s")
    c.r(5, 3, 10, 3, "s")
    c.p(6, 4, "O"); c.p(7, 4, "O"); c.p(8, 4, "O"); c.p(9, 4, "O")      # heavy brow
    c.p(6, 5, "O"); c.p(9, 5, "O")
    for x, y in ((5, 5), (7, 3), (9, 6), (6, 7), (10, 4)):             # salt pocks
        c.p(x, y, "w")
    c.r(6, 7, 9, 7, "S"); c.r(7, 7, 8, 7, "O")                           # dour mouth
    c.r(4, 8, 11, 8, "5")
    c.r(5, 9, 10, 10, "5"); c.r(5, 10, 10, 10, "6")                      # slouch shawl
    c.r(10, 9, 10, 10, "6")
    c.p(7, 9, "4"); c.p(8, 9, "4")


def rokhas():
    return person(rokhas_head, partial(hoe), face="face", sash=False, body="2", lite="1", dark="3", trim="4")


# ---- slynth_grit_gate ------------------------------------------------------------------------------------
def slynth_parts(c):
    c.p(7, 0, "1"); c.p(5, 1, "2"); c.p(10, 1, "2"); c.r(6, 1, 9, 1, "1")  # leaf crest
    c.r(5, 2, 10, 2, "2"); c.p(4, 2, "1"); c.p(11, 2, "1"); c.p(3, 1, "1"); c.p(12, 1, "1")
    c.p(6, 5, "4"); c.p(9, 5, "4")
    c.r(7, 6, 8, 6, "3")
    # long finger stems on both hands + root feet
    c.line(4, 16, 2, 19, "2"); c.line(3, 16, 1, 18, "2"); c.line(5, 16, 4, 19, "3")
    c.line(11, 16, 13, 19, "2"); c.line(11, 16, 12, 19, "3") if False else None
    c.p(2, 20, "1"); c.p(1, 19, "1")
    c.r(4, 22, 6, 22, "3"); c.r(9, 22, 11, 22, "3")
    c.p(3, 22, "2"); c.p(12, 22, "2"); c.p(4, 23, "x") if False else None


def slynth_grit_gate():
    return person(slynth_parts, partial(wrench, glow="4"), face="none", sash=True, skin=("1", "2"),
                  body="5", lite="4", dark="6", trim="2")


# ---- stranger ---------------------------------------------------------------------------------------------
@back
def tassel_cape(c):
    c.r(3, 9, 12, 20, "3")
    c.r(2, 13, 13, 21, "3")
    c.r(2, 13, 3, 21, "2")
    c.r(12, 13, 13, 21, "3")
    for x in range(2, 14, 2):
        c.p(x, 22, "4"); c.p(x, 23, "x") if False else None
    for x in range(3, 14, 2):
        c.p(x, 22, "5")
    c.r(2, 21, 13, 21, "6")


def stranger_face(c):
    c.r(6, 4, 9, 6, "O")
    c.p(6, 5, "w"); c.p(9, 5, "w")


def stranger():
    return person(tassel_cape, hood, stranger_face, scarf, face="none", sash=False, body="1", lite="1", dark="2",
                  trim="4")


# ---- urshiib -----------------------------------------------------------------------------------------------
@back
def urshiib_quills(c):
    for x0, y0, x1, y1 in ((4, 10, 0, 3), (5, 9, 2, 1), (7, 8, 6, 0), (9, 8, 9, 0), (11, 9, 13, 1), (11, 10, 15, 4),
                           (11, 11, 15, 8), (4, 12, 0, 8)):
        c.line(x0, y0, x1, y1, "w")
        c.p(x1, y1, "4")
    for x, y in ((3, 6), (12, 5), (14, 11)):
        c.p(x, y, "L")


def urshiib_head(c):
    c.r(6, 2, 9, 2, "2")
    c.r(5, 3, 10, 3, "1")
    c.r(5, 4, 10, 5, "2"); c.r(10, 4, 10, 6, "3")
    c.p(5, 3, "L"); c.p(10, 3, "L")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "1"); c.r(7, 7, 8, 7, "2")
    c.p(7, 7, "w"); c.p(8, 7, "O")                     # buck tooth
    c.p(8, 6, "O")
    c.p(7, 3, "L"); c.p(8, 2, "L")
    c.r(4, 8, 11, 9, "2")                              # slumped shoulders
    c.p(4, 8, "1")


def urshiib():
    return person(urshiib_quills, urshiib_head, partial(tunic, a="2", b="3", legs="3"), partial(spear),
                  face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


# ================================================================== CREATURES
def aloe_volta():
    c = C()
    cx, cy = 8, 14
    leaves = []
    for i in range(10):
        a = i * math.tau / 10
        leaves.append((cx + 7.2 * math.cos(a), cy + 5.4 * math.sin(a), i))
    # back leaves first (upper), front leaves last
    leaves.sort(key=lambda t: t[1])
    for x, y, i in leaves:
        ch = "2" if i % 2 else "1"
        tube(c, [(cx, cy), (cx + (x - cx) * .6, cy + (y - cy) * .6 - 1), (x, y)], 1.6, 0.4, ch)
        tube(c, [(cx, cy + 1), (cx + (x - cx) * .6, cy + (y - cy) * .6), (x, y + 1)], 0.5, 0.2, "3") if False else None
    for x, y, i in leaves:
        c.p(round(x), round(y), "3")
    for x, y in ((5, 12), (11, 13), (7, 17), (10, 10), (4, 15), (12, 16), (8, 11)):
        c.p(x, y, "3")
    c.ell(8, 14, 1.6, 1.3, "3"); c.p(8, 14, "4")
    # sizzling sparks
    for x, y in ((2, 9), (13, 8), (1, 18), (14, 19), (6, 4), (10, 21), (7, 20)):
        c.p(x, y, "c")
    for x, y in ((3, 8), (12, 8), (2, 17), (13, 20)):
        c.p(x, y, "w")
    return fin(c, (1, 14))


def bird():
    c = C()
    c.line(11, 14, 15, 17, "3"); c.line(11, 13, 15, 15, "3"); c.line(11, 15, 14, 19, "3")
    tube(c, [(7, 13), (5, 9), (5, 6), (4, 3)], 1.5, 1.0, "2")
    c.ell(9.5, 14, 4.8, 3.7, "2")
    c.ell(9, 12.5, 3.8, 1.8, "1")
    c.ell(11, 15, 3, 2.5, "3")
    c.line(8, 12, 12, 16, "1") if False else None
    c.ell(3.5, 2.5, 2.2, 1.9, "2")
    c.p(3, 2, "O"); c.p(3, 1, "3"); c.p(4, 1, "3")
    c.r(0, 3, 2, 3, "4"); c.r(1, 4, 2, 4, "4"); c.r(0, 2, 2, 2, "5") if False else None   # crunching muzzle
    c.r(0, 2, 1, 2, "4"); c.p(0, 5, "5"); c.r(1, 5, 2, 5, "5")
    c.p(0, 3, "O")
    c.p(5, 3, "w"); c.p(7, 2, "w"); c.p(1, 7, "w")          # gnats
    c.line(5, 17, 5, 21, "5"); c.line(10, 17, 10, 21, "5")
    c.r(3, 21, 6, 21, "4"); c.r(8, 21, 11, 21, "4")
    c.p(3, 20, "4"); c.p(8, 20, "4")
    return fin(c, (2, 12))


# ---- cherub machines --------------------------------------------------------------------------------
def cherub_arachnid_mechanical():
    c = C()
    for sx in (0, 1):
        for (x0, y0, x1, y1, x2, y2) in ((6, 9, 3, 5, 1, 9), (5, 11, 1, 9, 0, 14), (5, 14, 1, 14, 1, 20),
                                         (6, 16, 3, 18, 3, 22)):
            if sx:
                x0, x1, x2 = 15 - x0, 15 - x1, 15 - x2
            c.line(x0, y0, x1, y1, "l"); c.line(x1, y1, x2, y2, "L")
            c.p(x1, y1, "w")
    c.ell(8, 17, 3.2, 3.6, "2")
    c.ell(8, 16, 2.2, 2, "1")
    c.r(6, 19, 9, 20, "3")
    c.r(7, 15, 8, 15, "4")
    c.ell(8, 11, 3, 2.6, "2")
    c.r(6, 9, 9, 9, "1")
    c.r(5, 12, 10, 12, "3")
    c.p(6, 10, "4"); c.p(7, 10, "4"); c.p(8, 10, "4"); c.p(9, 10, "4")
    c.p(7, 11, "5"); c.p(8, 11, "5")
    c.p(8, 18, "5"); c.p(7, 17, "6") if False else None
    halo_c(c, 8)
    c.r(7, 2, 8, 3, "L") if False else None
    return fin(c, (1, 14))


def cherub_cat_mechanical():
    c = C()
    tube(c, [(12, 15), (15, 13), (14, 8)], 0.9, 0.9, "l")
    c.p(14, 7, "4")
    c.r(3, 12, 12, 17, "2")
    c.r(3, 12, 12, 13, "1")
    c.r(10, 14, 12, 17, "3"); c.r(3, 17, 12, 17, "3")
    for x in (5, 8, 11):
        c.r(x, 13, x, 16, "3") if False else None
    c.r(6, 13, 6, 16, "L"); c.r(9, 13, 9, 16, "L")      # plate seams
    c.r(2, 9, 6, 13, "2"); c.r(2, 9, 6, 9, "1")
    c.p(2, 8, "l"); c.p(5, 8, "l"); c.p(2, 7, "L"); c.p(5, 7, "w")
    c.r(0, 11, 2, 13, "1"); c.p(0, 12, "O")
    c.p(3, 10, "4"); c.p(5, 10, "4")
    c.p(1, 13, "5")
    c.r(3, 18, 4, 21, "3"); c.r(10, 18, 11, 21, "3"); c.r(7, 18, 7, 21, "L") if False else None
    c.r(2, 21, 5, 21, "l"); c.r(9, 21, 12, 21, "l")
    c.p(3, 18, "w"); c.p(10, 18, "w")
    halo_c(c, 4)
    return fin(c, (1, 14))


def cherub_fish_mechanical():
    c = C()
    c.line(12, 14, 15, 10, "5"); c.line(12, 14, 15, 18, "5"); c.r(14, 12, 15, 16, "4") if False else None
    c.r(13, 12, 15, 16, "4"); c.r(14, 13, 15, 15, "5")
    c.ell(7.5, 14, 6.3, 3.9, "2")
    c.ell(7, 12.5, 5, 1.6, "1")
    c.r(6, 15, 11, 17, "3")
    c.r(9, 11, 9, 17, "L")
    c.r(11, 11, 11, 17, "L") if False else None
    c.r(4, 8, 8, 10, "4"); c.r(5, 8, 7, 8, "5") if False else None
    c.p(4, 10, "5"); c.p(8, 8, "5")
    c.p(2, 13, "4"); c.p(2, 12, "O") if False else None
    c.p(3, 13, "O"); c.p(3, 12, "4")
    c.line(1, 15, 5, 15, "L")
    for x in (6, 8, 10, 12):
        c.p(x, 14, "l")
    c.r(7, 18, 9, 19, "5"); c.p(8, 20, "5")
    halo_c(c, 5)
    return fin(c, (1, 14))


def cherub_grazing_mechanical():
    c = C()
    c.p(14, 9, "l"); c.line(13, 11, 14, 9, "L")
    c.ell(9.5, 11, 4.5, 2.7, "2")
    c.r(6, 9, 13, 9, "1")
    c.r(11, 11, 13, 13, "3")
    c.r(6, 12, 6, 13, "L") if False else None
    # neck bowed down to graze
    c.r(3, 9, 6, 12, "2"); c.r(3, 9, 5, 10, "1")
    c.r(0, 12, 3, 14, "1"); c.p(0, 13, "O"); c.p(0, 14, "4")
    c.p(3, 10, "4")
    c.p(1, 11, "L"); c.p(2, 11, "l")                          # horn-antenna
    c.p(1, 10, "4")
    for x, h in ((4, 0), (6, 1), (10, 0), (12, 1)):
        c.r(x, 13, x, 20, "L" if h else "l")
        c.r(x + 1, 13, x + 1, 20, "3" if h else "2")
        c.p(x, 16, "w")
        c.r(x, 21, x + 1, 21, "l")
    c.r(0, 20, 2, 20, "6") if False else None
    c.p(1, 15, "6"); c.p(0, 15, "5"); c.p(2, 15, "5") if False else None
    halo_c(c, 8)
    return fin(c, (3, 13))


def cherub_ooze_mechanical():
    c = C()
    c.ell(8, 16, 6.5, 4.4, "2")
    c.ell(8, 14.5, 5.5, 2.6, "1")
    c.r(2, 18, 13, 20, "3"); c.ell(8, 18.5, 5.5, 2.2, "3") if False else None
    # gears inside
    for (gx, gy, r) in ((6, 15, 2), (10, 17, 1.6)):
        c.ell(gx, gy, r, r, "l")
        c.ell(gx, gy, r - 1, r - 1, "L")
        c.p(gx, gy, "5")
        for (dx, dy) in ((0, -r - 1), (0, r + 1), (-r - 1, 0), (r + 1, 0)):
            c.p(round(gx + dx), round(gy + dy), "l")
    c.p(4, 13, "w"); c.p(5, 12, "w")
    c.p(3, 17, "4"); c.p(12, 15, "4")
    c.ell(8, 8, 1.2, 1.4, "4") if False else None
    halo_c(c, 8)
    c.p(8, 4, "1") if False else None
    return fin(c, (1, 14))


def cherub_succulent_mechanical():
    c = C()
    # fractus: stacked ribbed paddles joined by chrome collars
    def paddle(cx, cy, rx, ry):
        c.ell(cx, cy, rx, ry, "2")
        c.ell(cx - .5, cy - .5, rx - 1, ry - 1, "1")
        c.r(round(cx + rx - 1), round(cy - ry + 1), round(cx + rx), round(cy + ry - 1), "3") if False else None
        c.line(round(cx + rx * .7), round(cy - ry * .5), round(cx + rx * .7), round(cy + ry * .6), "3")
        c.p(round(cx), round(cy), "4")
    paddle(8, 18, 4.5, 3.4)
    c.r(7, 15, 9, 15, "l")
    paddle(4.5, 12, 3.2, 3.2)
    paddle(11.5, 11, 3.2, 3.4)
    c.r(5, 14, 6, 15, "l"); c.r(10, 14, 11, 14, "L")
    paddle(8, 7, 2.6, 2.4)
    c.r(7, 9, 9, 10, "l") if False else None
    for x, y in ((4, 8), (3, 9), (12, 7), (13, 8), (8, 4), (1, 12), (15, 11)):
        c.p(x, y, "w")
    c.r(5, 21, 11, 21, "3")
    halo_c(c, 8)
    return fin(c, (2, 13))


def cherub_urchin_mechanical():
    c = C()
    cx, cy = 8, 13
    for i in range(12):
        a = i * math.tau / 12
        x1, y1 = cx + 7 * math.cos(a), cy + 7 * math.sin(a) * .95
        c.line(round(cx + 2.5 * math.cos(a)), round(cy + 2.5 * math.sin(a)), round(x1), round(y1), "l")
        c.p(round(x1), round(y1), "w")
    c.ell(cx, cy, 4, 4, "2")
    c.ell(cx - .8, cy - .8, 2.8, 2.6, "1")
    c.r(cx + 2, cy - 1, cx + 3, cy + 3, "3")
    c.r(7, 12, 9, 14, "L"); c.p(8, 13, "4"); c.p(8, 12, "5")
    c.r(5, 16, 11, 16, "3") if False else None
    halo_c(c, 8)
    return fin(c, (3, 12))


# ---- chutecrab -------------------------------------------------------------------------------------------
def chutecrab():
    c = C()
    for (x0, y0, x1, y1) in ((5, 13, 1, 12), (5, 15, 1, 17), (6, 17, 3, 21)):
        c.line(x0, y0, x1, y1, "5", mirror=True)
        c.m(x1, y1, "4")
    # shell: stacked rings like a chute / vent, geometric
    c.ell(8, 14, 5.8, 4.8, "2")
    c.ell(8, 13, 4.8, 3.4, "1")
    c.r(4, 17, 11, 18, "3")
    for y in (11, 13, 15):
        c.r(5, y, 10, y, "3")
    c.r(7, 11, 8, 15, "O")                 # vent opening
    c.r(7, 12, 8, 12, "L") ; c.r(7, 14, 8, 14, "L")
    c.p(3, 14, "l"); c.p(12, 14, "l")      # rivets
    c.p(5, 16, "l"); c.p(10, 16, "l")
    # claws
    for sx in (0, 1):
        pass
    c.r(1, 6, 3, 9, "5"); c.p(2, 6, "O"); c.r(1, 5, 1, 6, "4")
    c.r(12, 6, 14, 9, "5"); c.p(13, 6, "O"); c.r(14, 5, 14, 6, "4")
    c.r(2, 9, 4, 10, "4"); c.r(11, 9, 13, 10, "4")
    c.r(4, 10, 5, 11, "2"); c.r(10, 10, 11, 11, "2")
    # eyes on stalks
    c.r(5, 7, 5, 11, "5"); c.r(10, 7, 10, 11, "5")
    c.ell(5, 6, 1.4, 1.4, "w"); c.ell(10, 6, 1.4, 1.4, "w")
    c.p(5, 6, "O"); c.p(10, 6, "O")
    return fin(c, (0, 15))


# ---- diplomacy_droid -------------------------------------------------------------------------------------
def diplomacy_droid():
    c = C()
    # hovering chrome-fabric robe, folds, tapers to a hover glow
    c.r(4, 10, 11, 12, "l")
    c.r(3, 13, 12, 16, "l")
    c.r(4, 17, 11, 19, "l")
    c.r(6, 20, 9, 20, "L")
    for x, y0, y1 in ((4, 11, 19), (7, 11, 20), (10, 11, 19), (12, 13, 16), (3, 13, 16)):
        c.r(x, y0, x, y1, "L")
    c.r(5, 10, 6, 17, "w") if False else None
    c.line(5, 10, 5, 18, "w"); c.line(8, 12, 8, 19, "w") ; c.line(11, 13, 11, 17, "w") if False else None
    c.r(4, 9, 11, 9, "l"); c.r(5, 9, 6, 9, "w")
    c.p(3, 13, "w"); c.p(12, 14, "L")
    # sash/accents
    c.line(4, 11, 11, 15, "2"); c.line(4, 12, 11, 16, "3")
    # sleeves: draped, hands
    c.r(2, 11, 3, 14, "l"); c.r(12, 11, 13, 14, "L")
    c.r(2, 15, 3, 15, "L") if False else None
    c.r(2, 15, 3, 16, "2"); c.r(12, 15, 13, 16, "2")
    # head: faceplate with neutral visage
    c.r(5, 2, 10, 8, "l")
    c.r(5, 2, 10, 2, "w")
    c.r(10, 3, 10, 8, "L"); c.r(6, 8, 9, 8, "L")
    c.r(6, 4, 9, 7, "w")
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.p(6, 4, "4") ; c.p(9, 4, "4") if False else None
    c.r(7, 7, 8, 7, "O")
    c.p(7, 6, "l") if False else None
    c.p(7, 1, "L"); c.p(8, 1, "L") ; c.p(7, 0, "4"); c.p(8, 0, "4")
    # hover glow
    c.r(5, 21, 10, 21, "4"); c.r(6, 22, 9, 22, "5")
    c.r(7, 23, 8, 23, "x")
    c.shadow(4, 11, 23)
    return c.out()


# ---- fish ---------------------------------------------------------------------------------------------------
def fish():
    c = C()
    # soft ray ribbons trailing
    for (y0, y1, ch) in ((10, 6, "4"), (14, 14, "5"), (18, 21, "4"), (12, 9, "5")):
        tube(c, [(10, 14), (13, y0), (15, y1)], 0.8, 0.5, ch)
    tube(c, [(8, 9), (10, 5), (14, 3)], 0.8, 0.5, "4")
    tube(c, [(7, 18), (9, 21), (13, 22)], 0.8, 0.5, "5")
    c.ell(6.5, 14, 6, 3.6, "2")
    c.ell(6, 12.5, 5, 1.5, "1")
    c.r(4, 16, 9, 17, "3")
    # flat head, curious eye
    c.r(0, 13, 3, 15, "2"); c.r(0, 13, 2, 13, "1")
    c.p(2, 12, "w"); c.p(2, 13, "w"); c.p(3, 12, "O") if False else None
    c.ell(3, 13, 1.1, 1.1, "w"); c.p(3, 13, "O")
    c.line(5, 11, 5, 16, "3") ; c.p(5, 15, "3")
    c.line(8, 12, 8, 16, "3") if False else None
    c.p(0, 15, "O")
    # ray ribbons from the sides
    tube(c, [(7, 17), (5, 20), (3, 22)], 0.7, 0.4, "4")
    return fin(c, (0, 13))


# ---- gnu ------------------------------------------------------------------------------------------------------
def gnu():
    c = C()
    c.line(13, 13, 15, 17, "3"); c.line(14, 13, 15, 16, "3")
    c.ell(9.5, 13, 4.5, 3, "2")
    c.ell(9.5, 15.5, 4, 1.4, "3")
    # great mane over shoulders and neck
    c.ell(5.5, 11.5, 4.2, 4.4, "5")
    c.ell(5, 10, 3.2, 3, "4")
    c.line(3, 15, 3, 17, "5"); c.line(5, 15, 5, 17, "5"); c.line(7, 15, 7, 16, "5")
    c.r(8, 10, 9, 11, "5") if False else None
    c.line(7, 9, 10, 11, "4") if False else None
    for x, y in ((8, 11), (9, 11), (10, 12)):
        c.p(x, y, "5")
    # head low
    c.r(0, 9, 3, 12, "2"); c.r(0, 9, 3, 9, "1")
    c.r(0, 11, 0, 12, "1")
    c.p(1, 10, "O"); c.p(0, 12, "3")
    c.p(2, 12, "3") if False else None
    c.p(2, 8, "3"); c.p(4, 8, "3") if False else None
    # forked antlers
    c.line(2, 8, 2, 4, "w"); c.line(2, 5, 0, 2, "w"); c.line(2, 4, 3, 1, "w"); c.p(1, 3, "w") if False else None
    c.line(4, 8, 5, 5, "w"); c.line(5, 5, 4, 2, "w"); c.line(5, 5, 7, 3, "w")
    c.p(2, 4, "L") ; c.p(5, 6, "L")
    # legs
    for x, ch in ((4, "3"), (6, "2"), (11, "3"), (13, "2")):
        c.r(x, 16, x, 20, ch)
        c.r(x - 1 if x < 8 else x + 1, 17, x - 1 if x < 8 else x + 1, 20, "3") if False else None
        c.p(x, 21, "O"); c.p(x + 1, 21, "O") if False else None
    c.r(4, 21, 5, 21, "O"); c.r(6, 21, 7, 21, "O"); c.r(11, 21, 12, 21, "O"); c.r(13, 21, 14, 21, "O")
    c.r(5, 16, 5, 20, "2") ; c.r(12, 16, 12, 20, "2") ; c.r(14, 16, 14, 20, "3") if False else None
    return fin(c, (0, 15))


# ---- golems ---------------------------------------------------------------------------------------------------
def _seams(c, pts):
    for x, y in pts:
        c.p(x, y, "O")


def golem_antelope():
    c = C()
    c.line(13, 11, 15, 14, "3")
    c.ell(9.5, 12, 4.6, 2.7, "2")
    c.r(6, 10, 13, 10, "1")
    c.r(11, 12, 13, 14, "3")
    # neck + head
    c.line(5, 11, 3, 6, "2"); c.line(6, 11, 4, 6, "2"); c.line(5, 10, 4, 6, "1")
    c.r(1, 4, 4, 7, "2"); c.r(0, 6, 2, 8, "1"); c.p(1, 6, "O")
    c.p(3, 5, "4")
    # spiral horns from scrap
    c.line(3, 4, 3, 0, "L"); c.line(4, 4, 5, 0, "l")
    c.p(2, 2, "L"); c.p(4, 2, "l"); c.p(5, 1, "L")
    # scrap plate, bolts, stitches
    c.r(7, 11, 10, 13, "l"); c.r(7, 11, 10, 11, "w"); c.r(10, 12, 10, 13, "L")
    c.p(7, 12, "O"); c.p(9, 12, "O") ; c.p(8, 12, "4")
    _seams(c, [(5, 12), (5, 13), (11, 11)])
    # long mismatched legs (one chrome piston)
    for x, ch in ((5, "2"), (7, "3"), (11, "3")):
        c.r(x, 14, x, 20, ch)
    c.r(12, 14, 12, 20, "L"); c.r(12, 16, 12, 17, "l")
    for x in (5, 7, 11, 12):
        c.p(x, 21, "O")
    c.r(4, 21, 5, 21, "O"); c.r(7, 21, 8, 21, "O"); c.r(11, 21, 13, 21, "O")
    return fin(c, (0, 14))


def golem_cat():
    c = C()
    tube(c, [(12, 14), (15, 12), (14, 7)], 1.0, 1.0, "2")
    c.line(14, 7, 13, 5, "O"); c.p(14, 8, "O")
    c.r(14, 6, 14, 6, "4")
    c.ell(8, 14, 5.2, 3.3, "2")
    c.ell(8, 12.5, 4.5, 1.5, "1")
    c.r(3, 17, 12, 17, "3")
    c.r(10, 12, 12, 16, "3") if False else None
    c.r(7, 11, 10, 14, "l"); c.r(7, 11, 10, 11, "w"); c.r(9, 12, 10, 14, "L")
    c.p(8, 12, "O"); c.p(8, 13, "4")
    _seams(c, [(5, 11), (5, 12), (5, 13), (11, 15)])
    # head
    c.ell(3, 11, 2.8, 2.6, "2")
    c.r(0, 11, 2, 13, "1"); c.p(0, 12, "O")
    c.r(2, 7, 2, 9, "3"); c.r(3, 7, 3, 8, "3") if False else None
    c.r(5, 8, 5, 9, "L"); c.p(5, 7, "l")          # scrap ear
    c.p(4, 8, "3")
    c.p(2, 10, "4"); c.p(4, 10, "4"); c.p(1, 11, "5") if False else None
    # legs
    c.r(4, 16, 5, 20, "2"); c.r(6, 17, 6, 20, "3")
    c.r(10, 16, 12, 20, "2"); c.r(9, 17, 9, 20, "3")
    c.r(11, 17, 12, 19, "L"); c.p(11, 18, "l") if False else None
    c.r(3, 21, 6, 21, "1"); c.r(9, 21, 12, 21, "1")
    return fin(c, (1, 14))


def golem_fish():
    c = C()
    c.r(13, 11, 15, 17, "L"); c.r(14, 12, 15, 16, "l"); c.line(12, 14, 15, 10, "L")
    c.line(12, 14, 15, 18, "L")
    c.ell(7.5, 14, 6.5, 4, "2")
    c.ell(7, 12.5, 5.3, 1.6, "1")
    c.r(5, 16, 11, 17, "3")
    c.r(7, 11, 10, 17, "l"); c.r(7, 11, 10, 11, "w"); c.r(10, 12, 10, 17, "L")
    c.p(8, 13, "O"); c.p(9, 15, "4"); c.p(8, 14, "O") if False else None
    c.p(8, 15, "O")
    _seams(c, [(5, 13), (5, 14), (5, 15), (12, 14)])
    c.r(4, 8, 8, 10, "L"); c.p(5, 8, "l"); c.p(4, 9, "l")     # scrap dorsal
    c.r(5, 18, 7, 20, "2")
    c.p(2, 13, "w"); c.p(2, 14, "O"); c.p(3, 13, "O"); c.p(3, 12, "4")
    c.line(0, 15, 4, 15, "O")
    return fin(c, (0, 15))


def golem_humanoid_robot():
    c = C()
    # blocky clay-and-scrap humanoid
    c.r(5, 9, 10, 16, "2"); c.r(5, 9, 6, 16, "1"); c.r(9, 9, 10, 16, "3")
    c.r(4, 8, 11, 9, "3"); c.r(4, 8, 6, 8, "2")
    c.r(6, 11, 9, 14, "l"); c.r(6, 11, 9, 11, "w"); c.r(9, 12, 9, 14, "L")
    c.p(7, 12, "4"); c.p(8, 13, "5"); c.p(7, 13, "O") if False else None
    c.r(2, 9, 4, 17, "2"); c.r(2, 9, 3, 12, "1"); c.r(4, 10, 4, 17, "3")
    c.r(1, 15, 4, 18, "3"); c.r(1, 15, 4, 15, "2")
    c.r(11, 9, 12, 14, "L"); c.r(11, 9, 12, 9, "l")
    c.r(11, 15, 12, 17, "3"); c.p(12, 18, "3") ; c.p(11, 18, "3")
    # head
    c.r(5, 2, 10, 7, "2"); c.r(5, 2, 10, 2, "1"); c.r(10, 3, 10, 7, "3")
    c.p(6, 4, "O"); c.p(7, 4, "O"); c.p(9, 4, "4")
    c.r(6, 6, 9, 6, "O")
    c.p(11, 4, "L"); c.p(4, 3, "l"); c.p(11, 3, "L")
    c.line(8, 0, 8, 1, "L"); c.p(8, 0, "4")
    # legs
    c.r(5, 17, 7, 21, "3"); c.r(9, 17, 10, 21, "L"); c.r(5, 17, 5, 21, "2")
    c.r(4, 22, 7, 22, "O"); c.r(9, 22, 11, 22, "O")
    _seams(c, [(5, 12), (5, 14), (3, 13), (10, 11)])
    return fin(c, (2, 13))


def golem_mound():
    c = C()
    c.ell(8, 17, 7.3, 4.8, "3")
    c.ell(8, 15, 6.4, 5.5, "2")
    c.ell(7, 12.5, 4.5, 3.4, "1")
    # soldering board
    c.r(8, 11, 13, 15, "G"); c.r(8, 11, 13, 11, "g"); c.r(13, 12, 13, 15, "h")
    for x, y in ((9, 12), (11, 12), (10, 14), (12, 14), (9, 14)):
        c.p(x, y, "y")
    c.line(9, 13, 12, 13, "w")
    # magnets, vane pumps
    c.r(2, 14, 4, 16, "R"); c.r(2, 14, 2, 14, "l"); c.r(4, 14, 4, 14, "l"); c.r(3, 14, 3, 15, "2")
    c.r(2, 13, 2, 14, "l"); c.r(4, 13, 4, 14, "w")
    c.r(10, 17, 13, 19, "L"); c.r(10, 17, 13, 17, "l"); c.p(11, 18, "O"); c.p(12, 18, "O"); c.p(12, 17, "w")
    c.line(13, 18, 15, 20, "L")
    # diode flowers
    for (x, y, col) in ((5, 9, "4"), (8, 8, "5"), (12, 9, "4"), (3, 11, "5"), (6, 17, "4"), (9, 20, "5")):
        c.p(x, y, col)
        c.p(x, y + 1, "h") if y < 15 else None
    c.line(5, 10, 6, 11, "h") if False else None
    c.p(7, 8, "G") if False else None
    for x in (3, 5, 9, 12):
        c.p(x, 20, "1")
    return fin(c, (0, 15))


def golem_snail():
    c = C()
    # soft clay body
    c.r(0, 17, 14, 20, "2"); c.r(0, 17, 5, 18, "1"); c.r(0, 20, 14, 20, "3")
    c.r(0, 14, 2, 17, "2"); c.r(0, 14, 1, 16, "1")
    # eyestalks with diodes
    c.line(0, 14, 0, 10, "2"); c.line(2, 14, 3, 9, "2")
    c.p(0, 9, "4"); c.p(3, 8, "4"); c.p(0, 10, "w") if False else None
    c.p(1, 16, "O")
    # shell of clay + scrap
    c.ell(9, 12, 5.5, 5.5, "3")
    c.ell(8.5, 11.5, 4.7, 4.7, "2")
    c.ell(8, 11, 3.2, 3.2, "1")
    c.ell(8, 11, 1.6, 1.6, "2")
    c.p(8, 11, "3")
    c.r(10, 8, 13, 11, "l"); c.r(10, 8, 13, 8, "w"); c.r(13, 9, 13, 11, "L")
    c.p(11, 10, "4")
    _seams(c, [(5, 8), (4, 9), (13, 14), (12, 15)])
    c.p(6, 7, "w") if False else None
    c.r(0, 21, 14, 21, "3") if False else None
    return fin(c, (0, 15))


def golem_tripedal_robot():
    c = C()
    # three splayed legs
    for (x0, y0, x1, y1, x2, y2) in ((6, 12, 2, 14, 2, 20), (10, 12, 14, 14, 14, 20), (8, 14, 8, 17, 8, 21)):
        c.line(x0, y0, x1, y1, "L"); c.line(x1, y1, x2, y2, "l")
        c.p(x1, y1, "w")
    c.r(1, 21, 3, 21, "O"); c.r(13, 21, 15, 21, "O"); c.r(7, 22, 9, 22, "O")
    # dome body
    c.ell(8, 10, 5.5, 4.6, "3")
    c.ell(8, 9, 5, 4, "2")
    c.ell(7, 8, 3.6, 2.6, "1")
    c.r(3, 12, 12, 13, "3")
    c.r(8, 10, 11, 12, "l"); c.r(8, 10, 11, 10, "w") ; c.r(11, 11, 11, 12, "L")
    c.p(9, 11, "O") ; c.p(10, 11, "4")
    # single eye/diode and antenna
    c.r(5, 8, 6, 9, "O"); c.p(5, 8, "4"); c.p(6, 8, "5")
    c.line(8, 5, 8, 1, "L"); c.p(8, 1, "4"); c.p(7, 0, "5") if False else None
    _seams(c, [(3, 9), (4, 11), (12, 9)])
    return fin(c, (0, 15))


def humor():
    c = C()
    c.ell(8, 18, 7, 3.6, "3")
    c.ell(8, 17, 6.5, 3.4, "2")
    c.ell(7, 15.8, 4.4, 1.8, "1")
    # rising drop with a bright core
    c.ell(8, 11, 3.2, 4.6, "2")
    c.line(8, 4, 8, 6, "2"); c.p(8, 4, "1"); c.ell(8, 7, 1.8, 2.5, "2")
    c.ell(7, 10, 1.8, 3.2, "1")
    c.r(10, 10, 11, 13, "3") if False else None
    c.line(10, 8, 11, 13, "3")
    c.ell(8, 12, 1.5, 1.5, "4"); c.p(8, 12, "w") ; c.p(8, 13, "5")
    # dust chips and brine drops
    for x, y in ((2, 9), (13, 8), (3, 13), (13, 14), (5, 5), (11, 4)):
        c.p(x, y, "4")
    for x, y in ((2, 8), (12, 13), (4, 4)):
        c.p(x, y, "c")
    c.p(12, 20, "c"); c.p(3, 19, "1")
    return fin(c, (0, 15))


def mimic():
    c = C()
    cx, cy = 8, 12
    pts = []
    for i in range(6):
        a = -math.pi / 2 + i * math.tau / 6
        pts.append(a)
    for a in pts:
        ex, ey = cx + 8 * math.cos(a), cy + 10 * math.sin(a)
        mx = cx + 4.5 * math.cos(a + .45)
        my = cy + 5.5 * math.sin(a + .45)
        tube(c, [(cx, cy), (mx, my), (ex, ey)], 2.0, 0.6, "2")
    for a in pts:
        ex, ey = cx + 8 * math.cos(a), cy + 10 * math.sin(a)
        mx = cx + 4.5 * math.cos(a + .45)
        my = cy + 5.5 * math.sin(a + .45)
        tube(c, [(cx, cy), (mx - .6, my - .8), (ex, ey)], 0.9, 0.2, "1")
        # mirror photon scales
        sx = cx + 5.2 * math.cos(a + .3); sy = cy + 6.6 * math.sin(a + .3)
        c.p(round(sx), round(sy), "w")
        c.p(round(ex), round(ey), "l")
    c.ell(cx, cy, 2.4, 2.4, "3")
    c.ell(cx, cy, 1.5, 1.5, "w")
    c.p(cx, cy, "4"); c.p(cx - 1, cy - 1, "Y") if False else None
    c.r(7, 11, 8, 12, "4") if False else None
    return fin(c, (0, 15))


def moss_monster():
    c = C()
    # calcified trellis: bone ribs rising to hooked tips
    for x0, x1, top in ((3, 1, 3), (6, 5, 1), (9, 10, 2), (12, 14, 4)):
        c.line(x0, 21, x1, top, "w")
        c.line(x0 + 1, 21, x1 + 1, top, "L") if False else None
    c.line(2, 18, 13, 18, "L") ; c.line(3, 13, 12, 14, "L") if False else None
    for x, y in ((1, 3), (5, 1), (10, 2), (14, 4)):
        c.p(x, y, "w"); c.p(x + 1, y - 1, "w") if x < 8 else c.p(x - 1, y - 1, "w")
    # red moss carpet
    c.ell(8, 16, 7, 5, "3")
    c.ell(8, 15, 6.3, 4.3, "2")
    c.ell(7, 13.5, 4.5, 2.5, "1")
    for x, y in ((3, 12), (5, 11), (10, 11), (12, 13), (7, 9), (13, 17), (2, 17), (9, 20), (5, 20)):
        c.p(x, y, "2"); c.p(x, y - 1, "1")
    c.line(3, 21, 3, 15, "w") if False else None
    # sporophytes: white stalks with bulbs
    for x, y, h in ((4, 14, 4), (8, 12, 6), (11, 14, 4), (6, 18, 3), (13, 18, 3), (2, 19, 3)):
        c.line(x, y, x, y - h, "4")
        c.p(x, y - h - 1, "w") ; c.p(x - 1, y - h, "5") ; c.p(x + 1, y - h, "5")
    return fin(c, (0, 15))


# ---- natural weapons --------------------------------------------------------------------------------------
def natural_weapon_claw():
    c = C()
    for x0, tip in ((4, (2, 4)), (8, (7, 2)), (12, (12, 4))):
        # curved crescent claw
        pts = [(x0, 20), (x0 + (-1 if x0 < 8 else 1 if x0 > 8 else 0), 14), (x0 + (tip[0] - x0) * .5, 9), tip]
        tube(c, pts, 1.8, 0.4, "2")
        tube(c, [(p[0] - .8, p[1]) for p in pts], 0.8, 0.2, "1")
        c.p(tip[0], tip[1], "w")
    c.r(2, 19, 13, 21, "3")
    c.r(2, 19, 13, 19, "2")
    c.p(7, 19, "1"); c.p(3, 19, "1")
    for x in (4, 8, 12):
        c.p(x, 20, "1")
    return fin(c, (1, 14))


def natural_weapon_insect_leg():
    c = C()
    # segmented diagonal foreleg with barbs
    segs = [((1, 21), (4, 15)), ((4, 15), (8, 9)), ((8, 9), (12, 6)), ((12, 6), (15, 3))]
    for i, ((x0, y0), (x1, y1)) in enumerate(segs):
        tube(c, [(x0, y0), (x1, y1)], 1.8 - i * .3, 1.4 - i * .3, "2")
        tube(c, [(x0 - .5, y0 - .5), (x1 - .5, y1 - .5)], .8, .6, "1")
        c.p(x1, y1, "3")
    for (x, y) in ((6, 15), (9, 12), (11, 11), (13, 8), (5, 18)):
        c.line(x, y, x - 1, y + 3, "w") if False else None
    for (x, y, dx, dy) in ((3, 16, -2, -1), (6, 11, -2, -1), (7, 13, 2, 2), (10, 8, -2, -2), (11, 8, 1, 3),
                           (13, 5, -1, -2)):
        c.line(x, y, x + dx, y + dy, "w")
    c.p(15, 3, "w"); c.p(14, 2, "w")
    c.r(0, 20, 2, 22, "3")
    return fin(c, (0, 14))


def natural_weapon_pseudopod():
    c = C()
    tube(c, [(8, 22), (7, 17), (9, 12), (7, 7), (8, 3)], 3.4, 0.9, "2")
    tube(c, [(7, 22), (6, 17), (8, 12), (6, 8)], 1.4, 0.4, "1")
    c.line(10, 20, 10, 14, "3")
    c.ell(8, 3, 1.6, 1.8, "2")
    c.p(7, 2, "w")
    for x, y in ((3, 10), (12, 8), (13, 14), (3, 16), (10, 1)):
        c.p(x, y, "4")
    c.p(8, 5, "4") ; c.p(7, 14, "4")
    c.p(8, 6, "5") ; c.p(9, 9, "5") if False else None
    c.p(12, 9, "4")
    return fin(c, (3, 13))


def nephilim_qas():
    c = C()
    # tresses of potential energy streaming from the back
    for pts in (((12, 9), (14, 6), (15, 2)), ((11, 8), (13, 4), (14, 0)), ((13, 12), (15, 9), (15, 5))):
        tube(c, list(pts), 0.8, 0.4, "4")
    c.line(10, 8, 11, 3, "5") if False else None
    c.p(12, 4, "5"); c.p(14, 8, "5"); c.p(15, 5, "5")
    # immense body
    c.ell(10, 13, 5.5, 4.4, "2")
    c.ell(10, 11, 4.8, 2.2, "1")
    c.r(9, 16, 14, 17, "3")
    c.r(11, 10, 15, 15, "3") if False else None
    # blocky behemoth head
    c.r(0, 7, 6, 15, "2"); c.r(0, 7, 6, 8, "1"); c.r(0, 14, 6, 15, "3")
    c.r(0, 9, 0, 13, "1")
    c.r(0, 12, 3, 13, "3")                            # square muzzle seam
    c.p(1, 10, "4"); c.p(4, 9, "4"); c.p(2, 10, "O") if False else None
    c.r(1, 10, 2, 10, "4")
    c.r(4, 9, 5, 10, "O") if False else None
    c.p(4, 10, "5") if False else None
    c.p(4, 9, "O")
    c.r(1, 13, 5, 13, "O") if False else None
    c.p(1, 14, "w"); c.p(3, 14, "w"); c.p(5, 14, "w")
    c.r(2, 5, 3, 6, "3"); c.r(5, 5, 6, 6, "3")        # ears
    # glowing sigil on flank
    c.r(10, 12, 11, 13, "4"); c.p(10, 12, "w")
    # legs
    c.r(3, 15, 5, 20, "2"); c.r(6, 16, 6, 20, "3")
    c.r(12, 16, 14, 20, "2"); c.r(10, 16, 10, 20, "3")
    c.r(2, 21, 6, 21, "1"); c.r(9, 21, 14, 21, "1")
    return fin(c, (0, 15))


def plastronoid():
    c = C()
    # invisible gyroscope: dotted orbit ring
    for i in range(24):
        a = i * math.tau / 24
        x = 8 + 7 * math.cos(a)
        y = 12 + 5.5 * math.sin(a)
        c.p(round(x), round(y), "5" if i % 2 else "4")
    for i in range(16):
        a = i * math.tau / 16 + .4
        x = 8 + 3 * math.cos(a)
        y = 12 + 8.5 * math.sin(a)
        if i % 2 == 0:
            c.p(round(x), round(y), "5")

    def ball(cx, cy, r):
        c.ell(cx, cy, r, r, "L")
        c.ell(cx - r * .2, cy - r * .2, r - .8, r - .8, "l")
        c.p(round(cx - r * .5), round(cy - r * .5), "w")
        c.r(round(cx) - 1, round(cy) + 1, round(cx) , round(cy) + 1, "4") if r > 2 else None
    ball(8, 12, 3.4)
    c.p(8, 12, "4"); c.p(9, 12, "4") if False else None
    ball(2, 12, 2)
    ball(14, 12, 2)
    ball(8, 3.5, 2.2)
    ball(8, 21, 2.2)
    return fin(c, (1, 14))


def rhinox():
    c = C()
    tube(c, [(13, 11), (15, 13), (15, 17)], 0.7, 0.5, "3")
    c.ell(10, 13, 5.7, 4.5, "2")
    c.ell(10, 11.5, 5, 2.2, "1")
    c.ell(10, 15.5, 5, 1.8, "3")
    # steel-thick jacket plates, bullet scars
    c.r(6, 9, 13, 12, "l"); c.r(6, 9, 13, 9, "w"); c.r(12, 10, 13, 12, "L"); c.r(6, 12, 13, 12, "L")
    c.r(9, 9, 9, 12, "L")
    c.p(7, 10, "O"); c.p(11, 11, "O"); c.p(10, 10, "L") if False else None
    c.p(13, 14, "L") ; c.p(13, 15, "l")
    # giant skull encasing the three heads
    c.r(0, 6, 7, 14, "2")
    c.r(1, 5, 6, 5, "w"); c.r(0, 6, 7, 6, "w")
    c.r(0, 6, 0, 13, "w") if False else None
    c.r(0, 7, 6, 7, "L")
    c.r(1, 8, 6, 9, "2") ; c.r(0, 10, 6, 14, "3")
    c.r(0, 9, 0, 14, "1")
    c.r(2, 4, 3, 5, "w") ; c.p(1, 3, "w"); c.p(1, 2, "w") if False else None
    # parietal plates
    c.line(2, 6, 2, 13, "O") if False else None
    c.p(2, 8, "Y") if False else None
    # three heads' eyes
    c.p(1, 10, "5"); c.p(3, 10, "5"); c.p(5, 10, "5")
    c.p(1, 10, "O") ; c.p(3, 10, "O") ; c.p(5, 10, "O")
    c.p(1, 11, "4"); c.p(3, 11, "4"); c.p(5, 11, "4")
    c.r(0, 13, 6, 13, "L") ; c.p(2, 14, "w"); c.p(4, 14, "w")
    # legs
    c.r(3, 15, 5, 20, "3"); c.r(9, 16, 12, 20, "3") ; c.r(6, 16, 7, 20, "2")
    c.r(2, 21, 6, 21, "L"); c.r(8, 21, 13, 21, "L")
    return fin(c, (0, 15))


def scorpion():
    c = C()
    # legs
    for (x0, y0, x1, y1) in ((6, 10, 2, 9), (6, 12, 1, 13), (6, 14, 2, 18), (7, 16, 4, 21)):
        c.line(x0, y0, x1, y1, "5", mirror=True)
        c.m(x1, y1, "4")
    # pincer arms
    c.line(6, 8, 3, 5, "2", mirror=True); c.line(6, 9, 3, 6, "3", mirror=True)
    c.mr(1, 1, 3, 5, "2") if False else None
    c.mr(1, 2, 4, 5, "2"); c.mr(1, 2, 1, 5, "3") if False else None
    c.mr(3, 2, 4, 3, "1")
    c.m(1, 2, "w"); c.m(2, 2, "w") if False else None
    c.mr(2, 4, 3, 5, "3") if False else None
    c.m(3, 4, "O") ; c.m(2, 5, "O") if False else None
    # body
    c.ell(8, 9, 3.3, 3, "2")
    c.r(6, 7, 9, 8, "1")
    c.p(6, 8, "O"); c.p(9, 8, "O")
    c.ell(8, 14, 3.4, 3.6, "2")
    c.ell(8, 13, 2.4, 2, "1")
    for y in (12, 14, 16):
        c.r(5, y, 10, y, "3")
    # tail
    tube(c, [(8, 17), (8, 20), (12, 21), (14, 17), (13, 11), (10, 6)], 1.3, 1.0, "2")
    tube(c, [(8, 17), (8, 20), (12, 21), (14, 17)], .5, .5, "1") if False else None
    c.p(13, 14, "3"); c.p(14, 18, "1"); c.p(10, 21, "1")
    c.p(10, 5, "w"); c.p(9, 4, "w"); c.p(9, 5, "4")
    return fin(c, (1, 14))


def star_kraken():
    c = C()
    cx, cy = 8, 12
    tips = []
    for i in range(5):
        a = -math.pi / 2 + i * math.tau / 5
        tips.append((cx + 7.4 * math.cos(a), cy + 10.2 * math.sin(a), a))
    for x, y, a in tips:
        tube(c, [(cx, cy), ((cx + x) / 2, (cy + y) / 2), (x, y)], 3.2, 0.7, "2")
    for x, y, a in tips:
        tube(c, [(cx, cy - .6), ((cx + x) / 2 - .6, (cy + y) / 2 - .6), (x - .4, y)], 1.7, 0.3, "1")
        mx, my = (cx + x) / 2, (cy + y) / 2
        c.p(round(mx + .8), round(my + 1), "3")
        c.p(round(x), round(y), "w")
        c.p(round((mx + x) / 2 + 1), round((my + y) / 2), "4")
    c.ell(cx, cy, 3.3, 3.3, "3")
    c.ell(cx, cy, 2.4, 2.4, "4")
    c.ell(cx, cy, 1.3, 1.3, "O")
    c.p(cx, cy - 1, "5")
    c.p(7, 11, "w") if False else None
    for dx, dy in ((-3, -3), (3, -3), (-3, 4), (3, 4), (0, 5)):
        c.p(round(cx + dx), round(cy + dy), "w")
    return fin(c, (0, 15))


def svardym_jut():
    c = C()
    # young raptor-like hatchling: crest, tail, clutching a coral spear
    tube(c, [(10, 15), (13, 17), (15, 21)], 1.6, 0.5, "2")
    c.p(14, 18, "3")
    c.ell(8, 14, 3.8, 3.2, "2")
    c.ell(7.5, 13, 3, 1.6, "1")
    c.r(9, 14, 11, 17, "3")
    # neck + head, facing left
    tube(c, [(6, 12), (5, 8), (4, 6)], 1.4, 1.1, "2")
    c.ell(3.5, 5.5, 2.5, 2.1, "2")
    c.r(0, 5, 2, 6, "1"); c.p(0, 6, "w"); c.p(1, 6, "w") if False else None
    c.p(0, 5, "O") if False else None
    c.p(3, 5, "O"); c.p(3, 4, "y")
    c.r(0, 6, 2, 6, "1"); c.p(1, 7, "w"); c.p(3, 7, "w")
    # crest
    for x, y in ((4, 3), (5, 2), (6, 3), (5, 4), (7, 4)):
        c.p(x, y, "4")
    c.p(5, 1, "5"); c.p(6, 2, "5")
    # legs
    c.r(6, 16, 7, 20, "3"); c.r(9, 17, 10, 20, "2")
    c.r(4, 21, 7, 21, "1"); c.r(9, 21, 12, 21, "1")
    c.p(4, 20, "w") ; c.p(9, 20, "w") if False else None
    # coral spear in a small hand
    c.line(2, 19, 6, 11, "n")
    c.line(2, 19, 0, 23, "n") if False else None
    c.line(6, 11, 8, 8, "n") if False else None
    c.r(3, 15, 5, 15, "s") if False else None
    c.r(5, 12, 6, 13, "s") if False else None
    c.line(12, 4, 12, 20, "n")
    c.p(12, 3, "4"); c.p(11, 2, "4"); c.p(13, 2, "4"); c.p(12, 2, "5"); c.p(12, 1, "4")
    c.p(11, 5, "5"); c.p(13, 5, "5")
    c.r(10, 12, 12, 12, "s") ; c.p(11, 13, "s")
    return fin(c, (0, 14))


def tree():
    c = C()
    # little feet
    c.r(4, 21, 6, 22, "O"); c.r(9, 21, 11, 22, "O")
    # glazed pot
    c.r(3, 14, 12, 15, "5")
    c.r(4, 16, 11, 20, "4")
    c.r(4, 16, 6, 20, "4"); c.r(5, 16, 5, 20, "5") if False else None
    c.r(9, 16, 11, 20, "6")
    c.r(4, 19, 11, 20, "6") if False else None
    c.r(3, 14, 12, 14, "4")
    c.r(4, 17, 11, 17, "5")
    c.p(7, 18, "y"); c.p(8, 18, "y")
    c.p(6, 19, "4") ; c.p(9, 19, "5") if False else None
    c.p(4, 16, "4")
    # trunk
    c.r(7, 9, 8, 14, "n"); c.r(8, 9, 8, 14, "N")
    # trimmed, rounded canopy
    c.ell(8, 6, 6.2, 5.4, "3")
    c.ell(7.5, 5.5, 5.4, 4.5, "2")
    c.ell(6.5, 4.5, 3.4, 2.6, "1")
    for x, y in ((4, 7), (11, 8), (8, 9), (10, 3)):
        c.p(x, y, "3")
    for x, y in ((6, 4), (9, 6), (3, 5)):
        c.p(x, y, "w") if False else None
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.r(7, 7, 8, 7, "O")      # doting little face
    c.p(5, 3, "1") ; c.p(12, 5, "3")
    return fin(c, (3, 12))


def vantabloom():
    c = C()
    # petals
    for a, rx in ((-2.4, 2), (-1.6, 1), (-.7, 2), (0.2, 2.4)):
        pass
    petals = [((8, 11), (2, 5), 2.4), ((8, 11), (14, 5), 2.4), ((8, 12), (1, 11), 2.2), ((8, 12), (15, 11), 2.2),
              ((8, 13), (3, 17), 2.2), ((8, 13), (13, 17), 2.2)]
    for (s, e, r) in petals:
        tube(c, [s, ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2 - 1.5), e], r, 0.7, "2")
    for (s, e, r) in petals:
        tube(c, [(s[0], s[1] - .6), ((s[0] + e[0]) / 2, (s[1] + e[1]) / 2 - 2), (e[0], e[1] - .4)], r - 1.1, 0.3, "1")
    c.ell(8, 12, 4.6, 3.2, "3")
    c.ell(8, 12, 3.3, 2.1, "O")
    # light that drips off the rim and seeps into the void
    for x, y in ((3, 9), (13, 9), (2, 15), (14, 15), (8, 8)):
        c.p(x, y, "4")
    c.line(5, 16, 5, 18, "4"); c.p(5, 19, "5")
    c.line(11, 16, 11, 20, "4"); c.p(11, 21, "5")
    c.line(8, 15, 8, 17, "4"); c.p(8, 18, "5")
    c.p(8, 12, "5") if False else None
    c.p(7, 12, "6") if False else None
    c.p(8, 11, "6") ; c.p(9, 13, "6") if False else None
    c.line(2, 18, 2, 20, "4") ; c.p(2, 21, "5")
    return fin(c, (1, 14))


def worm_of_the_earth():
    c = C()
    segs = [(11, 21, 3.0), (6, 20, 3.4), (3, 16, 3.6), (5, 12, 3.8), (10, 10, 3.9), (12, 6, 3.7)]
    # body segments from tail (bottom right) to head (top)
    path = [(13, 21), (8, 21), (3, 18), (4, 13), (9, 10), (11, 6)]
    for i, (x, y) in enumerate(path):
        c.ell(x, y, 3.0 + i * .12, 2.8 + i * .12, "3")
    for i, (x, y) in enumerate(path):
        c.ell(x - .3, y - .3, 2.5 + i * .12, 2.3 + i * .12, "2")
        c.ell(x - .8, y - .8, 1.5, 1.3, "1")
    # honeycomb rings
    for (x, y) in path[:-1]:
        c.p(round(x) + 1, round(y) + 1, "5"); c.p(round(x) - 1, round(y) + 1, "5")
        c.p(round(x), round(y) - 1, "5") ; c.p(round(x), round(y), "4")
    # gaping honeycomb maw
    c.ell(11.5, 4.5, 3.9, 3.7, "3")
    c.ell(11.5, 4.5, 3.1, 2.9, "O")
    c.ell(11.5, 4.5, 2.3, 2.1, "4")
    for x, y in ((10, 4), (12, 3), (13, 5), (11, 6), (10, 3), (12, 5)):
        c.p(x, y, "6")
    c.p(11, 4, "O") ; c.p(12, 4, "O") if False else None
    for ang in range(0, 360, 45):
        a = math.radians(ang)
        c.p(round(11.5 + 3.4 * math.cos(a)), round(4.5 + 3.2 * math.sin(a)), "w")
    return fin(c, (0, 15))


# ---------------------------------------------------------------- round 2 redraws (override earlier drafts)
def ring(c, cx, cy, rx, ry, ch):
    for i in range(48):
        a = i * math.tau / 48
        c.p(round(cx + rx * math.cos(a)), round(cy + ry * math.sin(a)), ch)


def chime_head(c):
    rows = {0: (7, 8), 1: (6, 9), 2: (5, 10), 3: (4, 11), 4: (4, 11), 5: (5, 10), 6: (5, 10), 7: (6, 9), 8: (7, 8)}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            top = y <= 3
            left = x <= 7
            c.p(x, y, ("w" if left else "1") if top else ("2" if left else "3"))
    c.line(4, 3, 11, 3, "l"); c.line(7, 0, 7, 8, "l")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(6, 1, "Y") if False else None
    for x, y in ((1, 2), (14, 5), (2, 8), (13, 1)):
        c.p(x, y, "4")
    for x, y in ((0, 5), (15, 9), (3, 0)):
        c.p(x, y, "c")
    # floating shards
    for sx in (1, 14):
        c.p(sx, 12, "w"); c.r(sx - 1, 13, sx + 1, 13, "1"); c.p(sx, 14, "3"); c.p(sx, 13, "w")


def chime_body(c):
    c.r(5, 9, 10, 9, "6")
    c.mr(3, 9, 4, 10, "w"); c.mr(3, 10, 3, 10, "1"); c.p(4, 9, "4"); c.p(11, 9, "4")
    c.r(7, 8, 8, 8, "L")


def chime():
    return person(chime_body, chime_head, face="none", sash=True, trim="4", body="2", lite="1", dark="3")


def hindren_parts(c):
    c.r(5, 3, 10, 7, "2"); c.r(6, 2, 8, 2, "2"); c.r(9, 1, 10, 2, "2"); c.p(4, 4, "2")
    c.r(5, 3, 5, 6, "1"); c.r(10, 3, 10, 7, "3"); c.r(5, 7, 9, 7, "3")
    c.r(8, 4, 9, 5, "4"); c.p(8, 4, "w")                 # one big glowing eye
    c.p(6, 4, "O"); c.p(6, 5, "O")
    c.r(6, 6, 9, 6, "O"); c.p(6, 7, "O"); c.p(8, 7, "O")
    c.r(5, 2, 6, 2, "l"); c.p(5, 2, "w"); c.p(11, 5, "L"); c.p(12, 5, "l"); c.p(4, 6, "L")
    c.r(5, 10, 8, 13, "l"); c.r(5, 10, 8, 10, "w"); c.r(8, 11, 8, 13, "L")
    c.p(5, 13, "O"); c.p(6, 11, "O"); c.p(7, 12, "4")
    c.line(9, 10, 10, 15, "O"); c.line(8, 14, 10, 12, "O")
    # long clay arm dragging, scrap fist; tiny withered arm
    c.r(11, 9, 13, 20, "2"); c.r(11, 9, 12, 12, "1"); c.r(13, 12, 13, 20, "3")
    c.r(11, 20, 14, 22, "L"); c.r(11, 20, 12, 20, "l")
    c.r(3, 10, 4, 12, "3"); c.p(4, 13, "L")
    c.p(11, 14, "O"); c.p(12, 17, "O"); c.p(11, 11, "4")


def golem_hindren():
    return person(hindren_parts, face="none", sash=False, skin=("2", "3"), body="2", lite="1", dark="3")


def cherub_grazing_mechanical():
    c = C()
    c.p(15, 9, "l"); c.line(13, 10, 15, 9, "L")
    c.ell(10, 11, 4.6, 2.8, "2"); c.r(7, 9, 13, 9, "1"); c.r(11, 11, 13, 13, "3")
    c.line(6, 10, 3, 15, "2"); c.line(6, 11, 3, 16, "2"); c.line(5, 10, 3, 14, "1")
    c.r(0, 15, 3, 18, "1"); c.r(0, 18, 3, 18, "3"); c.p(2, 16, "O"); c.p(0, 17, "4")
    c.line(3, 14, 2, 10, "l"); c.line(4, 14, 5, 10, "L"); c.p(2, 10, "4"); c.p(5, 10, "4")
    for x, a in ((7, "l"), (8, "2"), (12, "L"), (13, "2")):
        c.r(x, 13, x, 20, a); c.p(x, 16, "w"); c.p(x, 21, "O")
    c.r(7, 21, 8, 21, "O"); c.r(12, 21, 13, 21, "O")
    c.r(6, 12, 6, 12, "5")
    halo_c(c, 9)
    return fin(c, (0, 14))


def cherub_succulent_mechanical():
    c = C()
    c.r(6, 5, 9, 20, "2"); c.r(6, 5, 7, 20, "1"); c.r(9, 5, 9, 20, "3")
    c.r(5, 6, 10, 6, "2") ; c.r(6, 4, 9, 4, "2")
    for y in (8, 12, 16, 20):
        c.r(5, y, 10, y, "l"); c.p(5, y, "w")
    # arms
    c.r(2, 12, 5, 13, "2"); c.r(2, 7, 3, 12, "2"); c.r(2, 7, 2, 11, "1"); c.r(3, 12, 3, 13, "3")
    c.r(10, 10, 13, 11, "2"); c.r(12, 5, 13, 10, "2"); c.r(13, 6, 13, 10, "3"); c.r(12, 5, 12, 9, "1")
    c.r(2, 6, 3, 6, "4"); c.r(12, 4, 13, 4, "4"); c.r(7, 3, 8, 3, "4")
    for x, y in ((1, 9), (4, 8), (14, 7), (11, 7), (5, 15), (10, 14), (7, 10), (8, 18), (4, 11)):
        c.p(x, y, "w")
    c.r(4, 21, 11, 21, "3")
    halo_c(c, 8)
    return fin(c, (3, 12))


def chutecrab():
    c = C()
    for (x0, y0, x1, y1) in ((5, 13, 1, 13), (5, 15, 1, 18), (6, 17, 3, 22)):
        c.line(x0, y0, x1, y1, "5", mirror=True); c.m(x1, y1, "4")
    c.ell(8, 15, 6.2, 4.3, "3")
    c.ell(8, 14.5, 5.5, 3.7, "2")
    ring(c, 8, 14.5, 4, 2.6, "1"); ring(c, 8, 14.5, 2, 1.3, "3")
    c.r(7, 14, 8, 15, "O")
    c.p(3, 16, "l"); c.p(12, 16, "l"); c.p(4, 12, "l"); c.p(11, 12, "l")
    # claws raised
    c.mr(0, 6, 3, 10, "4"); c.mr(0, 6, 1, 8, "5"); c.mr(2, 6, 2, 8, "O") if False else None
    c.m(1, 5, "4"); c.m(3, 5, "5"); c.m(2, 7, "O")
    c.mr(2, 10, 4, 11, "4")
    c.m(5, 7, "w"); c.mr(5, 8, 5, 10, "5") if False else None
    c.r(6, 9, 6, 11, "5"); c.r(9, 9, 9, 11, "5")
    c.r(5, 6, 6, 7, "w"); c.r(9, 6, 10, 7, "w"); c.p(5, 6, "O"); c.p(10, 6, "O")
    return fin(c, (0, 15))


def fish():
    c = C()
    tube(c, [(12, 14), (14, 11), (15, 9)], 1.0, 0.5, "4"); tube(c, [(12, 14), (14, 17), (15, 19)], 1.0, 0.5, "4")
    c.r(12, 12, 13, 16, "2")
    tube(c, [(7, 10), (9, 6), (12, 3), (14, 4)], 0.8, 0.5, "4")
    tube(c, [(9, 10), (11, 7), (13, 7)], 0.6, 0.4, "5")
    tube(c, [(6, 18), (7, 21), (11, 22)], 0.8, 0.5, "4")
    tube(c, [(8, 18), (11, 20), (14, 22)], 0.6, 0.4, "5")
    c.ell(7, 14, 6, 4, "2"); c.ell(6.5, 12.5, 5, 1.7, "1"); c.r(4, 16, 10, 17, "3")
    c.r(0, 13, 2, 16, "2"); c.r(0, 13, 2, 13, "1")
    c.ell(3, 13, 1.4, 1.4, "w"); c.p(3, 13, "O")
    c.line(5, 11, 5, 17, "3"); c.line(0, 16, 2, 16, "O")
    c.line(4, 17, 2, 20, "4")
    return fin(c, (0, 14))


def gnu():
    c = C()
    c.line(13, 13, 15, 17, "3"); c.line(14, 12, 15, 15, "3")
    c.ell(9.5, 13, 5, 3, "2"); c.ell(9.5, 15.5, 4, 1.4, "3")
    c.ell(6, 11, 3.6, 3.8, "5"); c.ell(6, 10, 2.8, 2.5, "4")
    for x, y in ((9, 10), (10, 11), (11, 12), (9, 12)):
        c.p(x, y, "5")
    c.line(3, 13, 3, 16, "5"); c.line(5, 14, 5, 17, "5")
    c.r(0, 11, 3, 14, "2"); c.r(0, 11, 3, 11, "1"); c.r(0, 13, 0, 14, "1")
    c.p(1, 12, "O"); c.p(0, 14, "3"); c.r(1, 15, 1, 16, "5")
    c.line(2, 10, 1, 6, "w"); c.line(1, 7, 0, 4, "w"); c.line(1, 6, 3, 3, "w"); c.p(3, 2, "w"); c.p(0, 3, "w")
    c.line(5, 9, 6, 6, "w"); c.line(6, 6, 4, 3, "w"); c.line(6, 6, 8, 4, "w"); c.p(4, 2, "w"); c.p(8, 3, "w")
    for x, ch in ((4, "3"), (7, "2"), (11, "3"), (13, "2")):
        c.r(x, 16, x, 20, ch); c.r(x, 21, x + 1, 21, "O")
    return fin(c, (0, 15))


def golem_snail():
    c = C()
    c.r(0, 17, 14, 20, "2"); c.r(0, 17, 5, 18, "1"); c.r(0, 20, 14, 20, "3")
    c.r(0, 14, 2, 17, "2"); c.r(0, 14, 1, 16, "1")
    c.line(0, 14, 0, 10, "2"); c.line(2, 14, 3, 9, "2")
    c.p(0, 9, "4"); c.p(3, 8, "4"); c.p(1, 16, "O")
    c.ell(9, 11, 5.6, 5.8, "3"); c.ell(8.5, 10.5, 4.8, 5, "2")
    ring(c, 8.5, 10.5, 3.2, 3.4, "3"); ring(c, 8.5, 10.5, 1.5, 1.6, "3")
    c.ell(7, 8, 2, 1.5, "1")
    c.r(11, 12, 14, 16, "l"); c.r(11, 12, 14, 12, "w"); c.r(14, 13, 14, 16, "L"); c.p(12, 14, "4"); c.p(13, 15, "O")
    for x, y in ((4, 9), (5, 13), (3, 12)):
        c.p(x, y, "O")
    return fin(c, (0, 15))


def moss_monster():
    c = C()
    c.ell(8, 16, 7, 5, "3"); c.ell(8, 15, 6.3, 4.3, "2"); c.ell(7, 13.5, 4.5, 2.5, "1")
    for x, y in ((3, 12), (5, 11), (10, 11), (12, 13), (13, 17), (2, 17), (9, 20), (5, 20)):
        c.p(x, y, "1")
    for x, y, h in ((6, 13, 5), (10, 14, 4), (8, 12, 6), (4, 16, 3), (12, 17, 3)):
        c.line(x, y, x, y - h, "4"); c.p(x, y - h - 1, "w"); c.p(x - 1, y - h, "5"); c.p(x + 1, y - h, "5")
    for x0 in (1, 4, 11, 14):
        mx = x0 + (8 - x0) * .2
        c.line(x0, 21, round(mx), 8, "w"); c.line(round(mx), 8, round(x0 + (8 - x0) * .55), 3, "w")
        c.p(round(x0 + (8 - x0) * .55), 3, "L")
    c.line(2, 17, 13, 17, "L") if False else None
    return fin(c, (0, 15))


def rhinox():
    c = C()
    tube(c, [(13, 11), (15, 13), (15, 17)], 0.7, 0.5, "3")
    c.ell(10, 12, 5.7, 4.6, "2"); c.ell(10, 10, 5, 2.2, "1"); c.ell(10, 15, 5, 2, "3")
    c.r(6, 8, 9, 14, "l"); c.r(6, 8, 9, 8, "w"); c.r(9, 9, 9, 14, "L")
    c.r(12, 8, 14, 12, "l"); c.r(14, 9, 14, 12, "L"); c.p(7, 10, "O"); c.p(13, 10, "O")
    # giant skull with horn
    c.r(0, 8, 6, 15, "w"); c.r(0, 8, 6, 8, "Y") if False else None
    c.r(0, 14, 6, 15, "L"); c.r(5, 9, 6, 13, "l")
    c.r(1, 7, 5, 7, "w"); c.r(1, 7, 3, 7, "w")
    c.line(1, 8, 0, 2, "w"); c.line(2, 8, 1, 3, "w"); c.p(0, 1, "l")
    c.line(4, 7, 4, 4, "w"); c.p(4, 3, "l")
    for x in (1, 3, 5):
        c.p(x, 11, "O"); c.p(x, 12, "4")
    c.line(2, 9, 2, 10, "L"); c.line(4, 9, 4, 10, "L")
    c.r(0, 13, 6, 13, "L")
    c.r(3, 16, 5, 20, "3"); c.r(9, 16, 12, 20, "3"); c.r(6, 16, 7, 20, "2")
    c.r(2, 21, 6, 21, "L"); c.r(8, 21, 13, 21, "L")
    return fin(c, (0, 15))


def worm_of_the_earth():
    c = C()
    path = [(13, 21), (8, 21), (3, 18), (4, 13), (9, 10)]
    for i, (x, y) in enumerate(path):
        c.ell(x, y, 3.2 + i * .1, 3.0 + i * .1, "3")
        c.ell(x - .3, y - .3, 2.5 + i * .1, 2.3 + i * .1, "2")
        c.ell(x - .8, y - .8, 1.4, 1.2, "1")
        c.p(round(x) + 1, round(y) + 1, "4")
    c.ell(11, 5, 4.6, 4.2, "3"); c.ell(11, 5, 3.9, 3.5, "w")
    c.ell(11, 5, 3.0, 2.7, "O"); c.ell(11, 5, 1.8, 1.6, "4"); c.p(11, 5, "O")
    for ang in range(0, 360, 60):
        a = math.radians(ang)
        c.p(round(11 + 2.4 * math.cos(a)), round(5 + 2.1 * math.sin(a)), "6")
    return fin(c, (0, 15))


SPRITES = {
    "baboon": baboon(), "cherub_baboon": cherub_baboon(), "chime": chime(), "dromad": dromad(),
    "goatfolk": goatfolk(), "golem_hindren": golem_hindren(), "gyrewight": gyrewight(),
    "mechanimist_paladin": mechanimist_paladin(), "naphtaali_tinker": naphtaali_tinker(), "rokhas": rokhas(),
    "slynth_grit_gate": slynth_grit_gate(), "stranger": stranger(), "urshiib": urshiib(),
    "aloe_volta": aloe_volta(), "bird": bird(),
    "cherub_arachnid_mechanical": cherub_arachnid_mechanical(), "cherub_cat_mechanical": cherub_cat_mechanical(),
    "cherub_fish_mechanical": cherub_fish_mechanical(), "cherub_grazing_mechanical": cherub_grazing_mechanical(),
    "cherub_ooze_mechanical": cherub_ooze_mechanical(), "cherub_succulent_mechanical": cherub_succulent_mechanical(),
    "cherub_urchin_mechanical": cherub_urchin_mechanical(), "chutecrab": chutecrab(),
    "diplomacy_droid": diplomacy_droid(), "fish": fish(), "gnu": gnu(), "golem_antelope": golem_antelope(),
    "golem_cat": golem_cat(), "golem_fish": golem_fish(), "golem_humanoid_robot": golem_humanoid_robot(),
    "golem_mound": golem_mound(), "golem_snail": golem_snail(), "golem_tripedal_robot": golem_tripedal_robot(),
    "humor": humor(), "mimic": mimic(), "moss_monster": moss_monster(),
    "natural_weapon_claw": natural_weapon_claw(), "natural_weapon_insect_leg": natural_weapon_insect_leg(),
    "natural_weapon_pseudopod": natural_weapon_pseudopod(), "nephilim_qas": nephilim_qas(),
    "plastronoid": plastronoid(), "rhinox": rhinox(), "scorpion": scorpion(), "star_kraken": star_kraken(),
    "svardym_jut": svardym_jut(), "tree": tree(), "vantabloom": vantabloom(),
    "worm_of_the_earth": worm_of_the_earth(),
}
