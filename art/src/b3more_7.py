"""B3 remaining creatures, batch 7."""
import os
import sys
from functools import partial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b3kit as K  # noqa: E402
from b3kit import (C, person, hat_wide, hood, helmet, scarf, tunic, cape, staff, sword, club, halo, beard,
                   hair_short, hair_wild, hair_long, overlay, back, poncho, armor, goggles_up)  # noqa: E402
from b3_people import (bundle, hide_poncho, moss_fur, mail_coif, tabard, keffiyeh)  # noqa: E402
from b3more_keys import MORE_KEYS  # noqa: E402

KEYS = MORE_KEYS[7]
P = person


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
        c.ell(x, y, r0 + (r1 - r0) * t / tot, r0 + (r1 - r0) * t / tot, ch)


def blob(c, cx, cy, rx, ry, a="2", b="3", h="1"):
    c.ell(cx, cy, rx, ry, b)
    c.ell(cx - 0.6, cy - 0.6, rx - 1.0, ry - 1.0, a)
    c.ell(cx - 1.4, cy - 1.6, max(rx * 0.45, 1), max(ry * 0.35, 1), h)


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


def new():
    return C()


# =============================================================== humanoids
def bone_knife(c):
    c.line(13, 11, 13, 17, "w")
    c.p(13, 10, "w"); c.p(14, 11, "l")
    c.r(12, 18, 14, 18, "n")
    c.p(12, 15, "s"); c.p(11, 15, "s")
    c.p(13, 19, "N")


def fangs_small(c):
    c.p(6, 7, "w"); c.p(9, 7, "w")


def knapsack(c):
    c.r(11, 10, 14, 16, "N")
    c.r(12, 10, 14, 11, "n")
    c.p(13, 13, "y")
    c.r(11, 10, 11, 14, "n")


def banner(c):
    c.line(13, 3, 13, 22, "n")
    c.r(14, 4, 15, 9, "4")
    c.r(14, 4, 15, 4, "5")
    c.p(15, 10, "4"); c.p(14, 11, "5"); c.p(15, 8, ".")
    c.p(12, 15, "s"); c.p(11, 15, "s")
    c.p(13, 2, "y")


def bone_trim(c):
    for x in (5, 7, 9):
        c.p(x, 9, "w")
    c.p(6, 10, "w"); c.p(8, 10, "w")
    c.p(6, 7, "w"); c.p(9, 7, "w")
    c.r(3, 19, 12, 19, "r") if False else None


def cannibal_convert():
    return P(hood, knapsack, tunic, scarf, bone_knife, bone_trim, face="face", sash=False, trim="4")


def issachari_convert():
    return P(hood, cape, tunic, banner, scarf, face="face", sash=False, trim="4")


def halo_gold(c):
    halo(c, "y", "t")


def hermit_robe(c):
    c.r(3, 19, 12, 21, "1")
    for x in range(3, 13, 2):
        c.p(x, 21, ".")
    c.p(4, 12, "1")


def cherub_hermit():
    return P(halo_gold, beard, hermit_robe, staff, hair_wild_none if False else (lambda c: None), face="face",
             sash=True, trim="L", body="1", lite="w", dark="2")


def grass_hem(c):
    for x, y, ch in ((3, 20, "g"), (4, 19, "G"), (5, 21, "h"), (7, 20, "g"), (9, 21, "G"), (11, 19, "g"),
                     (12, 21, "h"), (3, 21, "G"), (10, 20, "h"), (6, 22, "g"), (11, 22, "G")):
        c.p(x, y, ch)


def crow_buttons(c):
    for y in (11, 13, 15):
        c.p(7, y, "4"); c.p(8, y, "5"); c.p(7, y - 1, "6") if False else None
    c.p(7, 10, "r"); c.p(8, 10, "R")
    # fern shoulder fronds
    c.line(4, 9, 2, 12, "G"); c.line(11, 9, 13, 12, "g")
    c.p(2, 13, "h"); c.p(13, 13, "h"); c.p(3, 12, "g")
    # mushroom cap on the hood top
    c.r(6, 0, 9, 0, "4"); c.r(5, 1, 10, 1, "5"); c.p(7, 0, "w")
    # ivy liripipe
    c.line(11, 3, 12, 8, "g"); c.line(12, 8, 12, 15, "h")
    c.p(13, 10, "G"); c.p(11, 12, "G"); c.p(13, 14, "G"); c.p(12, 16, "g")


def crowsong():
    return P(hood, grass_hem, crow_buttons, face="face", sash=False, body="2", trim="4")


def facets(c):
    for x, y in ((6, 11), (9, 13), (5, 16), (10, 18), (7, 20)):
        c.p(x, y, "w")
    c.line(5, 10, 9, 14, "w") if False else None


def crystal_shards(c):
    # crown of spikes
    for x, h in ((5, 2), (7, 1), (9, 0), (10, 2)):
        c.r(x, h, x, 3, "1")
        c.p(x, h, "w")
    # shoulder shards
    c.line(3, 9, 1, 5, "1"); c.line(4, 9, 3, 6, "w")
    c.line(12, 9, 14, 5, "3"); c.line(11, 9, 12, 6, "1")
    c.p(1, 5, "w"); c.p(14, 5, "w")
    for x, y in ((6, 11), (9, 13), (6, 16), (9, 18), (7, 20), (4, 13)):
        c.p(x, y, "w")
    c.line(5, 10, 10, 15, "4"); c.line(6, 10, 10, 14, "5")
    c.p(6, 5, "4"); c.p(9, 5, "4")


def glittermensch():
    return P(crystal_shards, face="face", sash=False, skin=("1", "2"), body="2", lite="1", dark="3",
             trim="4")


def rubble_body(c):
    c.mr(2, 8, 4, 12, "L")
    c.mr(2, 8, 3, 9, "l")
    c.mr(1, 11, 3, 15, "L")
    c.m(1, 15, "S") if False else None
    c.mr(1, 15, 3, 16, "l")
    # crystal cluster on the shoulders
    for x, y0 in ((2, 4), (13, 5)):
        c.r(x, y0, x, 8, "B"); c.p(x, y0, "w"); c.p(x - 1 if x < 8 else x + 1, y0 + 2, "c")
        c.r(x + (1 if x < 8 else -1), y0 + 2, x + (1 if x < 8 else -1), 8, "b")
    # roots
    c.line(5, 12, 4, 21, "n"); c.line(10, 12, 11, 21, "N")
    for x in (5, 8, 10):
        c.p(x, 3, "g")
    c.p(6, 2, "G"); c.p(8, 2, "g"); c.p(7, 2, "h")
    c.r(6, 9, 9, 9, "G"); c.p(7, 10, "g"); c.p(9, 10, "h")


def golem_cragsmensch():
    return P(rubble_body, face="face", sash=False, skin=("l", "L"), body="2", lite="1", dark="3")


def tusks(c):
    c.p(5, 7, "w"); c.p(10, 7, "w"); c.p(5, 6, "w"); c.p(10, 6, "w")
    c.r(6, 7, 9, 7, "O")
    c.p(7, 7, "w"); c.p(9, 7, "w")
    c.r(5, 4, 10, 4, "N")  # heavy brow
    c.p(6, 5, "y"); c.p(9, 5, "y")


def hulk(c):
    c.mr(2, 8, 4, 13, "S")
    c.mr(1, 11, 3, 16, "S")
    c.mr(2, 8, 4, 9, "s")
    c.mr(0, 14, 3, 17, "s")
    c.mr(0, 17, 1, 17, "S")


def stitches(c):
    for y in (10, 12, 14):
        c.p(6, y, "O"); c.p(8, y, "O"); c.p(7, y, "w")
    c.line(3, 11, 4, 13, "O", mirror=True) if False else None
    c.p(2, 11, "O"); c.p(13, 12, "O"); c.p(2, 13, "w"); c.p(13, 14, "w")
    c.p(9, 3, "l"); c.p(10, 3, "L")  # bolt
    c.p(5, 20, "N"); c.p(10, 18, "N")


def loincloth(c):
    c.r(5, 15, 10, 17, "N")
    c.r(6, 16, 9, 19, "n")
    c.p(8, 20, "n")


def golem_troll():
    return P(hulk, tusks, stitches, loincloth, club, face="none", sash=False, skin=("2", "3"), body="2",
             lite="1", dark="3")


def clay_cracks(c):
    for x, y in ((6, 10), (7, 11), (8, 12), (7, 13), (9, 15), (4, 12), (11, 10)):
        c.p(x, y, "3")
    c.line(3, 11, 4, 14, "3") if False else None


def troll_grass(c):
    # hair & grass on head and shoulders
    c.r(5, 2, 10, 3, "g"); c.r(6, 1, 9, 1, "G")
    c.p(5, 4, "g"); c.p(10, 4, "h")
    for x, y in ((3, 8), (5, 8), (11, 8), (12, 9), (3, 9), (7, 9), (9, 9)):
        c.p(x, y, "g"); c.p(x, y - 1, "G")
    c.p(2, 10, "h"); c.p(13, 10, "h")
    c.p(4, 13, "g"); c.p(11, 12, "G")


def troll_hulk(c):
    c.mr(2, 8, 4, 13, "2")
    c.mr(2, 8, 3, 9, "1")
    c.mr(1, 11, 3, 16, "2")
    c.m(1, 12, "3"); c.m(2, 14, "3")
    c.mr(0, 15, 3, 18, "1")
    c.mr(0, 18, 1, 18, "3")
    c.r(5, 4, 10, 4, "3")
    c.p(6, 5, "y"); c.p(9, 5, "y")
    c.r(6, 7, 9, 7, "3"); c.p(5, 7, "w"); c.p(10, 7, "w")


def troll():
    return P(troll_hulk, clay_cracks, troll_grass, loincloth, face="none", sash=False, skin=("1", "2"),
             body="2", lite="1", dark="3")


def moss_berries(c):
    for x, y in ((3, 11), (12, 13), (4, 16), (11, 17), (6, 20), (9, 19)):
        c.p(x, y, "r")
    c.p(3, 12, "R")
    c.p(6, 5, "c"); c.p(9, 5, "c")


def naphtaali():
    return P(moss_fur, hood, K.veil, moss_berries, face="face", trim="4", sash=False)


def ape_face(c):
    c.r(5, 3, 10, 7, "1")
    c.r(10, 3, 10, 7, "2")
    c.r(6, 4, 9, 7, "s")
    c.r(6, 4, 9, 4, "S")
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.p(6, 5, "O")
    c.p(7, 6, "S"); c.p(8, 6, "S")
    c.r(7, 7, 8, 7, "S")
    c.p(5, 5, "1"); c.p(10, 5, "2")


def ape_body(c):
    c.mr(2, 8, 4, 13, "1")
    c.mr(1, 11, 3, 16, "1")
    c.m(1, 14, "w"); c.m(2, 10, "w")
    c.mr(1, 16, 3, 17, "S")
    c.mr(1, 17, 2, 17, "N")
    # toga
    c.line(5, 9, 10, 18, "4"); c.line(6, 9, 10, 17, "4"); c.line(5, 10, 9, 18, "5")
    c.r(5, 15, 10, 20, "4"); c.r(5, 20, 10, 20, "5")
    c.line(5, 14, 10, 14, "5")


def nuntu():
    return P(ape_body, ape_face, partial(hat_wide, a="t", d="y", band="4"), staff if False else sword if False else (lambda c: None),
             face="none", sash=False, skin=("1", "2"), body="4", lite="4", dark="5", trim="4")


def marble_veins(c):
    c.p(6, 11, "M"); c.p(7, 12, "M"); c.p(7, 13, "m") if False else None
    c.p(9, 14, "M"); c.p(8, 15, "M")
    c.p(6, 4, "M"); c.p(9, 4, "M")   # blush
    c.p(5, 6, "M"); c.p(10, 6, "M")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(7, 7, "M"); c.p(8, 7, "M")
    c.r(6, 2, 9, 2, "w")  # wreath
    c.p(5, 3, "M"); c.p(10, 3, "M"); c.p(7, 2, "M")
    c.p(4, 12, "M"); c.p(3, 17, "M"); c.p(12, 19, "M")
    c.line(11, 9, 14, 16, "M"); c.line(12, 9, 14, 14, "m")


def skybear():
    return P(marble_veins, face="none", sash=True, skin=("1", "2"), body="1", lite="1", dark="2", trim="4")


def petals(c):
    # flower head: petals around the face
    for (x, y) in ((4, 2), (5, 1), (7, 0), (8, 0), (10, 1), (11, 2), (3, 4), (12, 4), (3, 6), (12, 6), (4, 8),
                   (11, 8)):
        c.p(x, y, "4")
    for (x, y) in ((5, 2), (6, 1), (9, 1), (10, 2), (4, 4), (11, 4), (4, 6), (11, 6)):
        c.p(x, y, "5")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 6, "5"); c.r(7, 7, 8, 7, "5")


def brooch_leaf(c):
    c.r(7, 9, 8, 10, "l"); c.p(7, 9, "w"); c.p(8, 10, "L")
    for x, y in ((3, 12), (12, 13), (2, 14), (13, 15)):
        c.p(x, y, "G"); c.p(x, y + 1, "g")
    # dry petals clasped in hands
    c.r(1, 12, 3, 14, "4"); c.p(2, 13, "5"); c.p(4, 15, "s"); c.p(3, 15, "4"); c.p(1, 11, "4")
    # stilts: long legs
    c.r(3, 19, 12, 21, ".");
    c.r(5, 16, 10, 17, "2")
    c.r(5, 18, 6, 22, "g"); c.r(9, 18, 10, 22, "h")
    c.r(5, 18, 5, 22, "G")
    c.r(4, 22, 7, 22, "O"); c.r(8, 22, 11, 22, "O")
    c.p(4, 16, "1"); c.p(11, 16, "3")


def slynth_stilt():
    return P(hood, petals, brooch_leaf, face="none", sash=False, skin=("4", "5"), body="2", trim="4")


def bark_skin(c):
    c.r(5, 3, 10, 7, "n")
    c.r(10, 3, 10, 7, "N")
    c.r(6, 3, 9, 3, "N")
    c.p(7, 4, "N"); c.p(8, 6, "N"); c.p(6, 6, "N")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(7, 7, "N"); c.p(8, 7, "N")
    # twig crown
    c.line(5, 3, 3, 0, "N"); c.line(7, 3, 7, 0, "n"); c.line(10, 3, 12, 0, "N"); c.p(3, 1, "G"); c.p(12, 1, "g")
    c.p(5, 1, "g")
    # gnarled hands gripping the sword hilt
    c.r(4, 15, 4, 16, "n"); c.r(11, 15, 11, 16, "N")
    # tattered tabard strips
    c.r(6, 10, 9, 20, "1")
    c.r(7, 10, 8, 14, "3")
    for x in (6, 8):
        c.p(x, 20, ".")
    c.p(7, 17, "."); c.p(9, 16, ".")
    c.p(6, 13, "3")
    c.p(5, 12, "n"); c.p(10, 11, "N")
    # sword planted point down in front
    c.r(7, 14, 8, 14, "y")
    c.r(7, 15, 8, 15, "N")
    c.line(7, 16, 7, 22, "l"); c.line(8, 16, 8, 22, "L")
    c.p(6, 14, "y"); c.p(9, 14, "y")
    c.p(6, 15, "n"); c.p(9, 15, "N")


def zothom():
    return P(bark_skin, face="none", sash=False, skin=("n", "N"), body="2", lite="1", dark="3", trim="4")


HUMANOID = {"cannibal_convert", "cherub_hermit", "crowsong", "glittermensch", "golem_cragsmensch", "golem_troll",
            "issachari_convert", "naphtaali", "nuntu", "skybear", "slynth_stilt", "troll", "zothom"}


# =============================================================== creatures
def baetyl():
    c = new()
    # hover pads
    c.r(4, 21, 11, 21, "L"); c.r(5, 20, 10, 20, "l")
    c.r(6, 22, 9, 22, "4"); c.r(7, 22, 8, 22, "w")
    # crystal sphere
    c.ell(8, 11, 6.2, 7, "3")
    c.ell(7.5, 10.5, 5.4, 6.2, "2")
    c.ell(6, 8, 3, 3.6, "1")
    c.p(5, 6, "w"); c.p(6, 5, "w"); c.p(5, 7, "w")
    c.line(8, 5, 12, 11, "1") if False else None
    # facets
    c.line(8, 6, 8, 16, "3"); c.line(3, 11, 13, 11, "3")
    # moss blouse
    c.ell(8, 17, 6.4, 3.3, "g")
    c.r(2, 16, 14, 16, "g")
    for x in range(2, 14):
        c.p(x, 14 + (x * 3 % 3 == 0), "g")
    c.r(3, 18, 12, 19, "h")
    for x, y in ((4, 15), (7, 14), (10, 15), (12, 17), (5, 18), (9, 18)):
        c.p(x, y, "G")
    c.p(7, 11, "4"); c.p(9, 11, "4"); c.p(8, 11, "5")  # glow eyes in the crystal
    c.shadow(2, 13)
    return c.out()


def cat():
    c = new()
    # tail
    tube(c, [(13, 16), (15, 13), (14, 8), (12, 6)], 0.9, 0.7, "2")
    c.p(12, 6, "4"); c.p(14, 8, "4"); c.p(15, 11, "4")
    # body
    c.ell(9, 15, 5.5, 3.2, "3")
    c.ell(9, 14.5, 5, 2.8, "2")
    c.ell(8.5, 13.5, 3.5, 1.2, "1")
    for x in (7, 9, 11):
        c.r(x, 12, x, 13, "4")
    # legs
    c.r(4, 16, 5, 21, "2"); c.r(6, 17, 6, 21, "3"); c.r(11, 17, 12, 21, "2"); c.r(10, 17, 10, 21, "3")
    c.r(3, 21, 6, 21, "1"); c.r(10, 21, 13, 21, "1")
    c.r(3, 22, 6, 22, "O"); c.r(10, 22, 13, 22, "O")
    # head
    c.ell(3.5, 12, 3, 2.6, "2")
    c.ell(3, 11.5, 2.2, 1.8, "1")
    c.p(2, 8, "2"); c.p(2, 9, "2"); c.p(3, 9, "2"); c.p(5, 8, "3"); c.p(5, 9, "3"); c.p(4, 9, "2")
    c.p(2, 8, "4"); c.p(5, 8, "5")
    c.p(1, 12, "y"); c.p(4, 12, "y"); c.p(1, 13, "O") if False else None
    c.p(2, 13, "O"); c.p(0, 13, "O") if False else None
    c.p(2, 14, "w"); c.p(0, 12, "w"); c.p(0, 14, "w")
    c.shadow(2, 14)
    return c.out()


def halo_at(c, x, y, w=4):
    c.r(x, y, x + w - 1, y, "4")
    c.p(x - 1, y + 1, "5"); c.p(x + w, y + 1, "5")
    c.r(x, y + 2, x + w - 1, y + 2, "5") if False else None


def mech_bear():
    c = new()
    halo_at(c, 3, 3)
    c.p(3, 4, "5"); c.p(8, 4, "5")
    # body
    blob(c, 10, 13, 5.5, 4, "l", "L", "w")
    c.r(7, 11, 13, 12, "2"); c.r(7, 11, 13, 11, "1"); c.r(9, 12, 13, 12, "3")
    # legs
    for x0 in (4, 12):
        c.r(x0, 16, x0 + 2, 21, "L"); c.r(x0, 16, x0, 21, "l")
        c.r(x0 - 1, 21, x0 + 3, 21, "l"); c.r(x0 - 1, 22, x0 + 3, 22, "O")
    # head
    c.ell(4, 11, 3.3, 3, "l"); c.ell(3.5, 10.5, 2.4, 2, "w")
    c.ell(2, 7.5, 1.2, 1.2, "L"); c.ell(6, 7.5, 1.2, 1.2, "L")
    c.p(2, 7, "4"); c.p(6, 7, "4")
    c.r(1, 12, 3, 13, "L"); c.p(1, 12, "O"); c.p(0, 12, "O")
    c.p(3, 10, "4"); c.p(5, 10, "O")
    c.r(3, 14, 5, 14, "L")
    # rivets and cog
    c.p(9, 14, "4"); c.p(12, 15, "4"); c.p(14, 12, "5")
    c.shadow(0, 15)
    return c.out()


def mech_dog():
    c = new()
    halo_at(c, 1, 5)
    c.p(1, 6, "5"); c.p(6, 6, "5")
    # tail antenna
    c.line(13, 12, 15, 6, "L"); c.p(15, 5, "4")
    # body long and lean
    tube(c, [(12, 14), (7, 14)], 3, 2.6, "L")
    c.ell(9.5, 13.2, 5.5, 2.8, "l")
    c.r(6, 11, 13, 11, "2"); c.r(7, 12, 12, 12, "3")
    c.r(5, 10, 12, 10, "1") if False else None
    # legs
    for x0 in (5, 11):
        c.r(x0, 15, x0 + 1, 21, "L"); c.r(x0, 15, x0, 21, "l")
        c.r(x0 - 1, 21, x0 + 2, 21, "l"); c.r(x0 - 1, 22, x0 + 2, 22, "O")
    # head with long snout
    c.ell(3.5, 11.5, 3, 2.4, "l")
    c.r(0, 12, 2, 14, "l"); c.r(0, 14, 2, 14, "L"); c.p(0, 12, "O")
    c.p(3, 10, "4"); c.p(3, 11, "4")
    c.p(2, 8, "L"); c.p(2, 9, "L"); c.p(3, 9, "L"); c.p(5, 8, "l"); c.p(5, 9, "l"); c.p(4, 9, "L")
    c.p(2, 8, "w")
    c.r(5, 14, 6, 14, "L")
    c.p(9, 14, "4"); c.p(11, 13, "5")
    c.shadow(0, 15)
    return c.out()


def mech_frog():
    c = new()
    halo_at(c, 5, 0, 6)
    c.p(4, 1, "5"); c.p(11, 1, "5")
    # eye domes on top
    c.ell(4.5, 6, 2.6, 2.6, "L"); c.ell(11.5, 6, 2.6, 2.6, "L")
    c.ell(4.5, 6, 1.7, 1.7, "O"); c.ell(11.5, 6, 1.7, 1.7, "O")
    c.p(4, 6, "4"); c.p(5, 6, "4"); c.p(11, 6, "4"); c.p(12, 6, "4")
    c.p(3, 5, "w"); c.p(10, 5, "w")
    # wide head
    c.ell(8, 10, 6.4, 3, "L")
    c.ell(8, 9.6, 5.6, 2.4, "l")
    c.r(3, 11, 12, 11, "O"); c.p(6, 11, "w"); c.p(9, 11, "w")
    # hind legs folded
    c.ell(2.5, 16, 2.4, 3.6, "L"); c.ell(13.5, 16, 2.4, 3.6, "L")
    c.ell(2.5, 15.5, 1.4, 2.4, "l")
    c.r(0, 20, 4, 21, "l"); c.r(11, 20, 15, 21, "l"); c.r(0, 22, 4, 22, "O"); c.r(11, 22, 15, 22, "O")
    # body
    c.ell(8, 16, 4.6, 3.6, "2"); c.ell(7.6, 15.4, 3.4, 2.4, "1")
    c.r(5, 18, 11, 19, "3")
    c.p(8, 16, "4"); c.p(7, 16, "4")
    # front feet
    c.r(5, 20, 6, 21, "l"); c.r(9, 20, 10, 21, "l"); c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.shadow(0, 15)
    return c.out()


def mech_mollusk():
    c = new()
    halo_at(c, 2, 6)
    c.p(1, 7, "5"); c.p(6, 7, "5")
    # slug body
    tube(c, [(3, 17), (8, 18), (13, 18)], 3.2, 2.5, "L")
    c.r(2, 19, 14, 20, "L"); c.r(2, 20, 14, 20, "l") if False else None
    c.r(2, 16, 4, 19, "l")
    c.ell(4, 14, 2.6, 3, "l")
    c.p(3, 13, "4"); c.p(5, 13, "4"); c.p(3, 12, "O") if False else None
    # eyestalks
    c.line(3, 12, 2, 9, "l"); c.line(5, 12, 6, 9, "l"); c.p(2, 8, "4"); c.p(6, 8, "4")
    # gear-shaped shell
    c.ell(10, 12, 4.8, 5, "L")
    c.ell(10, 12, 3.8, 4, "2")
    c.ell(9.5, 11.5, 2.4, 2.6, "1")
    c.ell(10, 12, 1.2, 1.2, "L")
    c.p(10, 12, "4")
    for x, y in ((10, 6), (10, 18), (5, 12), (15, 12), (6, 8), (14, 8), (6, 16), (14, 16)):
        c.p(x, y, "l")
    c.line(10, 8, 12, 12, "3") if False else None
    # little hands
    c.r(0, 17, 1, 18, "l"); c.p(0, 19, "L"); c.p(1, 19, "4")
    c.r(1, 15, 2, 16, "L")
    c.shadow(0, 15)
    return c.out()


def mech_robot():
    c = new()
    halo_at(c, 5, 0, 6)
    c.p(4, 1, "5"); c.p(11, 1, "5")
    # head dome
    c.ell(8, 6, 3.2, 2.8, "l"); c.r(5, 7, 10, 8, "l"); c.r(10, 5, 10, 8, "L")
    c.r(6, 6, 9, 6, "O"); c.p(6, 6, "4"); c.p(9, 6, "4")
    c.p(6, 4, "w")
    c.r(7, 9, 8, 9, "L")
    # torso
    c.r(4, 10, 11, 16, "2"); c.r(4, 10, 11, 10, "1"); c.r(10, 10, 11, 16, "3")
    c.r(6, 12, 9, 14, "L"); c.r(7, 13, 8, 13, "4")
    # arms
    c.r(2, 10, 3, 15, "l"); c.r(12, 10, 13, 15, "L")
    c.r(1, 15, 3, 16, "L"); c.r(12, 15, 14, 16, "L")
    c.p(2, 16, "4")
    # treads
    c.r(2, 17, 13, 21, "L")
    c.r(2, 17, 13, 17, "l")
    for x in range(3, 13, 2):
        c.r(x, 18, x, 20, "l")
    c.r(2, 22, 13, 22, "O")
    c.r(4, 17, 4, 17, "w")
    c.shadow(1, 14)
    return c.out()


def mech_tortoise():
    c = new()
    halo_at(c, 0, 8)
    c.p(-1, 9, "5") if False else None
    c.p(0, 9, "5"); c.p(3, 9, "5")
    # head
    c.ell(2.5, 13, 2.5, 2.3, "l"); c.p(1, 12, "4"); c.p(0, 14, "O")
    c.r(0, 14, 3, 15, "L")
    # legs
    c.r(1, 17, 4, 20, "L"); c.r(12, 17, 15, 20, "L")
    c.r(5, 18, 7, 21, "l"); c.r(10, 18, 12, 21, "l")
    c.r(0, 21, 4, 21, "l"); c.r(12, 21, 15, 21, "l")
    # shell of panels
    c.ell(9, 13, 6.5, 6, "L")
    c.ell(9, 12.6, 5.7, 5.3, "2")
    c.ell(8.5, 11.5, 4.3, 3.6, "1")
    c.line(9, 7, 9, 18, "3"); c.line(4, 11, 15, 11, "3"); c.line(4, 15, 14, 15, "3")
    for x, y in ((6, 9), (12, 9), (6, 13), (12, 13), (9, 13)):
        c.p(x, y, "4")
    c.p(9, 9, "w"); c.p(7, 17, "l"); c.p(11, 17, "l")
    c.shadow(0, 15)
    return c.out()


def mech_bat():
    c = new()
    halo_at(c, 6, 2, 4)
    c.p(5, 3, "5"); c.p(10, 3, "5")
    # wings: struts + panels
    for side in (0, 1):
        pts = [(5, 11), (0, 8), (0, 18), (3, 15), (5, 17)]
        pp = pts if side == 0 else [(15 - x, y) for x, y in pts]
        poly(c, pp, "2" if side == 0 else "3")
    c.line(5, 11, 0, 8, "l", mirror=True)
    c.line(5, 12, 0, 12, "l", mirror=True); c.line(5, 13, 1, 17, "L", mirror=True)
    c.line(5, 14, 0, 18, "l", mirror=True) if False else None
    c.m(0, 8, "w"); c.m(0, 12, "4")
    # body
    c.ell(8, 14, 2.6, 4, "l"); c.r(9, 11, 10, 17, "L") if False else None
    c.r(7, 16, 8, 19, "L")
    c.r(7, 12, 8, 14, "4") if False else None
    c.p(7, 14, "4"); c.p(8, 14, "5")
    # head with big ears
    c.ell(8, 8, 2.4, 2.2, "l")
    c.line(6, 7, 5, 4, "L"); c.line(7, 7, 6, 4, "l"); c.line(10, 7, 11, 4, "L"); c.line(9, 7, 10, 4, "l")
    c.p(5, 4, "w"); c.p(11, 4, "w")
    c.p(7, 8, "4"); c.p(9, 8, "4"); c.p(8, 10, "w")
    c.shadow(4, 11, 22)
    return c.out()


def crypt_ferret():
    c = new()
    # long body running left to right
    tube(c, [(4, 14), (8, 14), (12, 15), (14, 17)], 3, 1.2, "3")
    tube(c, [(4, 13.5), (8, 13.5), (12, 14.5)], 2.5, 1.0, "2")
    tube(c, [(5, 12.5), (9, 12.5), (12, 13.5)], 1.2, 0.8, "1")
    # dark mask bands
    for x in (7, 9, 11):
        c.r(x, 11, x, 12, "4")
    # grave moss stipples
    for x, y in ((6, 11), (8, 10), (10, 11), (12, 13), (9, 12)):
        c.p(x, y, "g")
    c.p(8, 11, "G"); c.p(10, 12, "h")
    # legs
    for x0 in (4, 6, 10, 12):
        c.r(x0, 16, x0, 20, "3")
    c.r(3, 20, 7, 20, "2") if False else None
    for x0 in (3, 5, 9, 11):
        c.p(x0, 21, "1")
    c.r(3, 21, 7, 21, "2"); c.r(9, 21, 13, 21, "2")
    c.r(3, 22, 7, 22, "O"); c.r(9, 22, 13, 22, "O")
    # head: spade nose
    c.ell(3, 12, 2.6, 2.4, "2")
    c.r(0, 12, 2, 14, "1")
    c.r(0, 13, 0, 14, "w") if False else None
    c.p(0, 12, "O"); c.p(0, 13, "O")
    c.p(3, 10, "O"); c.p(1, 11, "4")
    c.p(3, 9, "3"); c.p(4, 9, "3"); c.p(5, 10, "3")
    c.p(1, 14, "w"); c.p(2, 14, "w")
    c.shadow(0, 15)
    return c.out()


def _holo(rows_fn, scan=True):
    """scanline-ize a figure: even rows light, odd rows mid."""
    g = rows_fn()
    out = []
    for y, row in enumerate(g):
        s = ""
        for ch in row:
            if ch in ".xO":
                s += ch
            else:
                s += "1" if y % 2 == 0 else "2"
        out.append(s)
    return out


def _scan(c, hair_rows=(), keep=()):
    g = c.out()
    out = []
    for y, row in enumerate(g):
        out.append([("2" if y % 3 == 2 else "1") if ch == "1" else ch for ch in row])
    return out


def eater():
    c = new()
    # projector disc
    c.r(3, 21, 12, 21, "L"); c.r(4, 22, 11, 22, "l"); c.r(5, 21, 10, 21, "l")
    # hair (dark), face
    c.r(6, 1, 9, 1, "3"); c.r(5, 2, 10, 3, "3"); c.p(5, 4, "3"); c.p(10, 4, "3"); c.r(4, 4, 4, 9, "3")
    c.r(6, 3, 9, 3, "1"); c.r(6, 4, 9, 7, "1")
    c.r(7, 8, 8, 8, "1")
    # coat and arms
    c.r(5, 9, 10, 16, "1"); c.r(3, 10, 4, 17, "1"); c.r(11, 10, 12, 17, "1")
    c.r(7, 10, 8, 16, "2")
    # legs
    c.r(5, 17, 7, 20, "1"); c.r(9, 17, 11, 20, "1")
    c.r(5, 16, 11, 16, "2")
    g = _scan(c)
    g[5][6] = "O"; g[5][9] = "O"; g[7][7] = "O"
    # glitch: two bands shifted sideways
    for y, d in ((11, 1), (12, 1), (18, -1)):
        row = g[y]
        g[y] = ([row[-1]] + row[:-1]) if d > 0 else (row[1:] + [row[0]])
    res = ["".join(r) for r in g]
    res[23] = "".join("x" if 3 <= i <= 12 else "." for i in range(16))
    return res


def rebekah():
    c = new()
    # head tilted, hair + veil sideways
    c.r(6, 2, 10, 2, "3"); c.r(5, 3, 10, 3, "3"); c.r(5, 4, 5, 7, "3")
    c.r(6, 4, 10, 7, "1")
    c.r(10, 2, 14, 4, "2"); c.r(12, 5, 14, 12, "2"); c.r(14, 12, 15, 14, "2")
    c.r(6, 8, 9, 8, "1")
    c.r(5, 9, 10, 10, "1")
    for y in range(11, 21):
        w = 2.2 + (y - 11) * 0.6
        c.r(max(int(7.5 - w), 0), y, min(int(7.5 + w), 15), y, "1")
    c.r(3, 20, 12, 20, "2")
    # raised hand with motes
    c.r(3, 9, 4, 13, "1"); c.r(1, 6, 3, 8, "1")
    g = _scan(c)
    for (x, y) in ((0, 3), (2, 2), (1, 0), (4, 4), (0, 6)):
        g[y][x] = "1"
    g[5][7] = "O"; g[5][9] = "O"
    g[21] = ["1" if ch in "12" else ch for ch in g[21]]
    res = ["".join(r) for r in g]
    res[22] = "..LLLLLLLLLL...".ljust(16, ".")
    res[23] = "".join("x" if 3 <= i <= 12 else "." for i in range(16))
    return res


def fungus():
    c = new()
    # hyphae licking the mud
    for x0, y0, x1, y1 in ((8, 19, 1, 21), (8, 19, 14, 21), (7, 20, 3, 22), (9, 20, 12, 22), (8, 20, 6, 22)):
        c.line(x0, y0, x1, y1, "4")
    for x, y in ((1, 21), (14, 21), (3, 22), (12, 22)):
        c.p(x, y, "5")
    c.p(0, 20, "5"); c.p(15, 20, "5")
    # stalk
    c.r(6, 12, 9, 19, "w"); c.r(6, 12, 6, 19, "t") if False else None
    c.r(9, 12, 9, 19, "t")
    c.r(7, 17, 8, 17, "t")
    # cap
    c.ell(8, 8.5, 7.3, 5.2, "3")
    c.ell(8, 8, 6.7, 4.6, "2")
    c.ell(7, 6.8, 4.5, 2.6, "1")
    c.r(1, 10, 14, 10, "3")
    for x, y in ((4, 7), (10, 6), (7, 9), (12, 9), (2, 9)):
        c.p(x, y, "4"); c.p(x + 1, y, "5") if x < 12 else None
    # eyes/mouth beneath the cap
    c.p(7, 13, "O"); c.p(8, 13, "O")
    c.p(7, 15, "O"); c.p(8, 15, "O")
    c.shadow(0, 15)
    return c.out()


def godhed():
    c = new()
    # hover legs
    c.r(4, 20, 11, 20, "L"); c.r(5, 21, 10, 21, "l"); c.r(6, 22, 9, 22, "4"); c.p(7, 22, "w"); c.p(8, 22, "w")
    # egg of metal
    c.ell(8, 11, 6, 8, "L")
    c.ell(7.6, 10.6, 5.2, 7.2, "l")
    c.ell(6.5, 6.5, 2.4, 2.6, "w")
    # glass pane
    c.ell(8.5, 12, 3.2, 4.2, "O")
    c.ell(8.5, 12, 2.5, 3.5, "2")
    c.ell(8, 11, 1.5, 2.3, "1")
    c.p(7, 10, "w"); c.p(7, 11, "w")
    c.p(10, 14, "3"); c.p(9, 14, "3")
    # greeble bits and welds
    c.line(3, 7, 13, 7, "L"); c.line(2, 15, 13, 15, "L")
    for x, y in ((3, 7), (12, 7), (3, 15), (12, 15), (8, 3)):
        c.p(x, y, "4")
    # welded woodsprog roots / branches
    c.line(2, 12, 0, 8, "n"); c.line(0, 8, 0, 5, "N"); c.p(0, 4, "g"); c.p(1, 5, "G"); c.p(0, 6, "h")
    c.line(14, 12, 15, 9, "n"); c.p(15, 8, "g")
    c.p(8, 2, "g"); c.p(8, 1, "G") if False else None
    c.p(11, 5, "N"); c.p(12, 5, "n")
    c.shadow(2, 13)
    return c.out()


def golem_bed():
    c = new()
    # four posts
    for x in (1, 6, 9, 14):
        c.r(x, 15, x, 21, "n")
        c.r(x, 22, x, 22, "O")
    c.r(1, 21, 1, 21, "N"); c.r(14, 21, 14, 21, "N")
    # headboard
    c.r(0, 5, 4, 12, "n"); c.r(0, 5, 4, 5, "t"); c.r(1, 6, 3, 11, "N")
    c.p(0, 4, "t"); c.p(4, 4, "t")
    c.p(2, 8, "4"); c.p(2, 9, "4") if False else None
    # mattress
    c.r(2, 13, 15, 17, "2")
    c.r(2, 13, 15, 14, "1"); c.r(2, 17, 15, 17, "3")
    c.r(14, 13, 15, 17, "3")
    # pillow face
    c.r(3, 9, 7, 12, "w"); c.r(3, 9, 7, 9, "w"); c.r(7, 10, 7, 12, "l")
    c.p(4, 10, "O"); c.p(6, 10, "O"); c.p(4, 11, "R") if False else None
    c.r(4, 12, 6, 12, "O")
    c.p(5, 12, "w")
    # blanket flopping with arms
    c.r(8, 13, 15, 18, "5")
    c.r(8, 13, 15, 13, "4")
    c.r(8, 18, 15, 18, "6")
    for x in (9, 11, 13):
        c.p(x, 19, "5")
    c.line(8, 14, 8, 17, "6")
    # stuffing and spring
    c.p(2, 17, "w"); c.p(1, 18, "w"); c.p(5, 18, "l"); c.p(4, 19, "L")
    c.shadow(0, 15)
    return c.out()


def golem_dawnglider():
    c = new()
    # flame aura wisps
    for x, y in [(2, 1), (13, 2), (1, 12), (14, 14), (3, 20), (12, 21), (6, 0), (9, 22)]:
        c.p(x, y, "4"); c.p(x, y + 1, "5")
    # bat wings
    for side in (0, 1):
        pts = [(6, 9), (0, 5), (1, 11), (3, 15), (6, 14)]
        pp = pts if side == 0 else [(15 - x, y) for x, y in pts]
        poly(c, pp, "3" if side else "2")
    c.line(6, 9, 0, 5, "1", mirror=True); c.line(6, 10, 1, 11, "1", mirror=True)
    c.line(6, 11, 3, 15, "1", mirror=True)
    # S-shaped body
    tube(c, [(8, 6), (10, 9), (6, 13), (5, 17), (9, 20), (12, 21)], 2.0, 0.9, "2")
    tube(c, [(8, 6), (9, 9), (6, 12)], 0.9, 0.9, "1")
    # plumage crest
    c.p(6, 2, "4"); c.p(8, 1, "w"); c.p(10, 2, "4"); c.p(7, 3, "w"); c.p(9, 3, "w") if False else None
    # head
    c.r(6, 3, 9, 6, "1"); c.r(9, 4, 9, 6, "2")
    c.p(10, 5, "y"); c.p(11, 5, "w"); c.p(7, 4, "O"); c.p(8, 4, "y")
    c.p(5, 5, "w"); c.p(5, 6, "4")
    c.p(10, 12, "w"); c.p(5, 14, "w"); c.p(6, 19, "w")
    c.shadow(4, 12)
    return c.out()


def golem_fungus():
    c = new()
    # stitched trunk of stacked shelf fungi with stub arms
    c.r(5, 11, 10, 20, "2"); c.r(5, 11, 6, 20, "1"); c.r(10, 11, 10, 20, "3")
    c.r(4, 21, 11, 21, "3"); c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    # shelves
    for y, w in ((12, 7), (15, 7), (18, 7)):
        c.r(8 - w // 2 - 1, y, 8 + w // 2, y + 1, "4")
        c.r(8 - w // 2 - 1, y + 1, 8 + w // 2, y + 1, "5")
        c.p(8 - w // 2 - 1, y, "w")
    # arms
    c.r(2, 12, 4, 13, "2"); c.r(11, 13, 13, 14, "3")
    c.r(1, 14, 2, 15, "1"); c.r(13, 15, 14, 16, "1")
    # big cap head
    c.ell(8, 6, 6.6, 4.6, "3")
    c.ell(8, 5.6, 6, 4, "2")
    c.ell(7, 4.5, 4, 2.2, "1")
    c.r(2, 9, 13, 10, "3")
    for x, y in ((4, 5), (10, 4), (8, 7), (12, 7)):
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    c.p(7, 12, "O") if False else None
    c.p(6, 10, "y"); c.p(9, 10, "y")
    c.r(6, 13, 9, 13, "O"); c.p(7, 13, "w"); c.p(9, 13, "w")
    # stitches
    for y in (16, 19):
        c.p(7, y, "O"); c.p(8, y, "w")
    c.shadow(2, 13)
    return c.out()


def golem_jelly():
    c = new()
    c.ell(8, 14, 7, 7, "3")
    c.ell(8, 13.5, 6.2, 6.2, "2")
    c.ell(6.5, 11, 3.5, 3.2, "1")
    c.r(2, 19, 13, 20, "3")
    c.p(4, 8, "w"); c.p(5, 8, "w"); c.p(4, 9, "w")
    # embedded oddments: bone, eye, key
    c.r(9, 15, 12, 15, "w"); c.p(8, 14, "w"); c.p(8, 16, "w"); c.p(13, 14, "w"); c.p(13, 16, "w")
    c.ell(6, 16, 1.6, 1.6, "w"); c.p(6, 16, "O"); c.p(5, 16, "4")
    c.p(10, 10, "L"); c.p(11, 11, "l"); c.p(12, 12, "L")
    c.p(4, 13, "4"); c.p(3, 14, "5")
    # face
    c.p(7, 11, "O"); c.p(10, 11, "O")
    c.r(7, 13, 10, 13, "O") if False else None
    c.shadow(1, 14)
    return c.out()


def golem_quad_robot():
    c = new()
    # body box
    c.r(3, 9, 12, 14, "2"); c.r(3, 9, 12, 10, "1"); c.r(3, 13, 12, 14, "3"); c.r(11, 9, 12, 14, "3")
    c.r(2, 11, 3, 12, "L")
    # head sensor on the left
    c.r(0, 8, 3, 12, "l"); c.r(0, 8, 3, 8, "w"); c.r(0, 12, 3, 12, "L")
    c.r(1, 9, 2, 10, "O"); c.p(1, 9, "4"); c.p(2, 10, "4")
    c.p(1, 7, "L"); c.p(2, 6, "L"); c.p(2, 5, "4")
    # vent and panel
    for x in (6, 8, 10):
        c.r(x, 11, x, 12, "O")
    c.p(5, 10, "4")
    # legs
    for x0, x1 in ((3, 1), (5, 6), (10, 9), (12, 14)):
        c.line(x0, 14, x1, 21, "L"); c.line(x0 + 1, 14, x1 + 1, 21, "l")
        c.r(x1 - 1, 21, x1 + 2, 21, "l"); c.r(x1 - 1, 22, x1 + 2, 22, "O")
    # antenna and exhaust pipes
    c.line(10, 9, 13, 5, "l"); c.p(13, 4, "4")
    c.r(7, 7, 8, 8, "L"); c.p(7, 6, "l")
    c.shadow(0, 15)
    return c.out()


def golem_swine():
    c = new()
    # body
    c.ell(9, 14, 6.4, 4.4, "3")
    c.ell(9, 13.5, 5.8, 3.9, "2")
    c.ell(8, 11.5, 3.8, 1.8, "1")
    # stitches
    for x in (8, 10, 12):
        c.p(x, 11, "O"); c.p(x, 13, "w") if False else None
    c.line(11, 11, 11, 17, "O")
    for y in (12, 14, 16):
        c.p(10, y, "w"); c.p(12, y, "w")
    # legs
    for x0 in (4, 6, 11, 13):
        c.r(x0, 17, x0, 21, "3")
    c.r(3, 21, 7, 21, "2"); c.r(10, 21, 14, 21, "2")
    c.r(3, 22, 7, 22, "O"); c.r(10, 22, 14, 22, "O")
    # curly tail
    c.p(15, 11, "1"); c.p(15, 12, "1"); c.p(14, 10, "1"); c.p(13, 10, "2")
    # head with snout and tusks
    c.ell(3.5, 13, 3.2, 3, "2")
    c.ell(3, 12.5, 2.2, 1.8, "1")
    c.r(0, 13, 2, 15, "1"); c.p(0, 14, "O"); c.p(1, 14, "O") if False else None
    c.p(0, 13, "O")
    c.p(1, 16, "w"); c.p(3, 16, "w") if False else None
    c.p(4, 11, "y"); c.p(4, 12, "O")
    c.p(3, 9, "3"); c.p(2, 10, "3"); c.p(5, 9, "3"); c.p(6, 10, "3")
    # patchwork patch
    c.r(7, 15, 9, 16, "5"); c.r(7, 15, 9, 15, "4")
    c.shadow(2, 14)
    return c.out()


def golem_wall():
    c = new()
    # legs
    c.r(3, 20, 6, 21, "L"); c.r(9, 20, 12, 21, "L"); c.r(2, 22, 6, 22, "O"); c.r(9, 22, 13, 22, "O")
    # slab of brick
    c.r(2, 2, 13, 19, "2")
    c.r(2, 2, 13, 3, "1"); c.r(12, 2, 13, 19, "3"); c.r(2, 18, 13, 19, "3")
    for y in range(4, 19, 3):
        c.r(2, y, 13, y, "3")
    for y, off in ((2, 0), (5, 3), (8, 0), (11, 3), (14, 0), (17, 3)):
        for x in range(3 + off, 13, 6):
            c.r(x, y + 1, x, y + 2, "3") if y + 2 < 19 else None
    # arms
    c.r(0, 6, 2, 12, "l"); c.r(13, 6, 15, 12, "L")
    c.r(0, 12, 2, 14, "1"); c.r(13, 12, 15, 14, "3")
    # eyes (gap in bricks) and mouth
    c.r(4, 6, 6, 8, "O"); c.r(9, 6, 11, 8, "O")
    c.p(5, 7, "y"); c.p(10, 7, "y"); c.p(5, 6, "w") if False else None
    c.r(5, 12, 10, 12, "O"); c.p(6, 12, "w"); c.p(9, 12, "w")
    c.r(2, 3, 5, 3, "1")
    c.shadow(1, 14)
    return c.out()


def lamprey():
    c = new()
    # mirrored double, ghosted, behind
    tube(c, [(12, 7), (13, 11), (9, 15), (11, 19), (8, 22)], 1.9, 0.8, "6")
    c.p(12, 9, "5"); c.p(11, 14, "5"); c.p(10, 18, "5")
    # main ribbon body S-curve
    tube(c, [(5, 7), (3, 11), (7, 15), (5, 19), (8, 22)], 2.3, 0.8, "2")
    tube(c, [(4.5, 8), (3, 11), (6, 14.5)], 0.9, 0.9, "1")
    for x, y in ((3, 12), (6, 15), (4, 18)):
        c.p(x, y, "3")
    # round mouth with triangle teeth
    c.ell(6, 4.5, 4.2, 4, "3")
    c.ell(6, 4.5, 2.6, 2.6, "O")
    for x, y in ((6, 0), (3, 1), (9, 1), (2, 4), (10, 4), (3, 8), (9, 8), (6, 9)):
        c.p(x, y, "w")
    for x, y in ((6, 1), (4, 2), (8, 2), (3, 4), (9, 4), (4, 7), (8, 7), (6, 8)):
        c.p(x, y, "w")
    c.p(6, 4, "R"); c.p(5, 4, "r") if False else None
    c.p(8, 4, "4") if False else None
    # mirror double mouth
    c.ell(12, 4, 2.4, 2.4, "5")
    c.p(12, 4, "O"); c.p(11, 3, "g"); c.p(13, 3, "g"); c.p(12, 2, "g"); c.p(12, 6, "g")
    c.shadow(2, 13, 23)
    return c.out()


def monad():
    c = new()
    # outer triangle
    poly(c, [(8, 2), (15, 19), (0, 19)], "L")
    poly(c, [(8, 4), (13, 17), (3, 17)], "w")
    poly(c, [(8, 6), (11, 15), (5, 15)], "l")
    # inverted inner triangle
    poly(c, [(5, 9), (11, 9), (8, 15)], "M")
    poly(c, [(6, 10), (10, 10), (8, 13)], "m")
    c.p(8, 11, "O")
    # corner glows
    for x, y in ((8, 2), (15, 19), (0, 19)):
        c.p(x, y, "M")
    c.p(8, 3, "m"); c.p(14, 19, "m"); c.p(1, 19, "m")
    c.line(8, 5, 8, 8, "w")
    c.r(4, 20, 11, 20, "m") if False else None
    c.shadow(3, 12, 22)
    return c.out()


def natural_weapon_bands():
    c = new()
    # three coiled crushing bands, diagonal
    for i, (x0, y0) in enumerate(((1, 3), (2, 9), (3, 15))):
        tube(c, [(x0, y0 + 3), (x0 + 5, y0 + 5), (x0 + 11, y0 + 3)], 1.6, 1.6, "2")
        tube(c, [(x0, y0 + 2.4), (x0 + 5, y0 + 4.2), (x0 + 11, y0 + 2.4)], 0.8, 0.8, "1")
        c.p(x0 + 11, y0 + 4, "3"); c.p(x0 + 10, y0 + 5, "3")
        c.p(x0 + 2, y0 + 5, "3"); c.p(x0 + 5, y0 + 6, "3")
    c.shadow(2, 13, 22)
    return c.out()


def natural_weapon_fist():
    c = new()
    # clenched fist seen from the front, wrist below
    c.r(5, 17, 11, 21, "3"); c.r(5, 17, 8, 21, "2"); c.r(5, 17, 6, 21, "1")
    c.r(3, 9, 12, 16, "2"); c.r(3, 9, 12, 10, "1"); c.r(11, 10, 12, 16, "3"); c.r(3, 15, 12, 16, "3")
    for x0 in (3, 6, 9):
        c.r(x0, 7, x0 + 2, 8, "2"); c.r(x0, 7, x0 + 1, 7, "1"); c.p(x0 + 2, 8, "3")
    c.r(12, 8, 12, 8, "3")
    for x in (5, 8, 11):
        c.r(x, 10, x, 13, "3")
    # thumb across the front
    c.r(2, 13, 9, 15, "1"); c.r(3, 15, 9, 15, "2"); c.p(2, 14, "2"); c.r(9, 13, 10, 14, "2")
    c.p(3, 13, "w"); c.p(4, 8, "w")
    c.shadow(3, 12, 22)
    return c.out()


def natural_weapon_mandible():
    c = new()
    # two curved pincer jaws
    tube(c, [(1, 4), (3, 10), (7, 15), (11, 19)], 2.3, 0.9, "2")
    tube(c, [(14, 4), (12, 10), (8, 15), (4, 19)], 2.3, 0.9, "3")
    tube(c, [(1.5, 4), (3, 9), (6, 13.5)], 0.9, 0.7, "1")
    # teeth
    for x, y in ((4, 11), (5, 13), (6, 15), (7, 17), (11, 11), (10, 13), (9, 15), (8, 17)):
        c.p(x, y, "w")
    c.p(11, 19, "N"); c.p(4, 19, "N")
    c.r(6, 20, 9, 21, "N") if False else None
    c.shadow(2, 13, 22)
    return c.out()


def natural_weapon_tail():
    c = new()
    # wet ringed tail of shuddering muscle: base lower left, puckered tip upper right
    import math
    n = 9
    for i in range(n):
        t = i / (n - 1)
        x = 3 + 9 * t
        y = 20 - 14 * t - 3.5 * math.sin(t * math.pi)
        r = 3.2 - 1.2 * t
        c.ell(x, y, r, r * 0.9, "3")
        c.ell(x - 0.3, y - 0.3, r - 0.8, (r - 0.8) * 0.9, "2" if i % 2 == 0 else "1")
    # glistening wet spots
    for i in (1, 3, 5, 7):
        t = i / (n - 1)
        c.p(round(2.2 + 9 * t), round(18.6 - 14 * t - 3.5 * math.sin(t * math.pi)), "w")
    # orifice tip
    c.ell(13, 5, 2.6, 2.6, "3")
    c.ell(13, 5, 1.6, 1.6, "O")
    c.p(13, 5, "R"); c.p(12, 4, "r")
    c.p(14, 2, "w"); c.p(11, 2, "w"); c.p(15, 3, "w")
    c.shadow(0, 14, 22)
    return c.out()


def oboroqoru_statue():
    c = new()
    # plinth
    c.r(1, 20, 14, 21, "L"); c.r(1, 20, 14, 20, "l"); c.r(1, 22, 14, 22, "O")
    # crossed legs
    c.r(2, 17, 13, 19, "2"); c.r(2, 17, 13, 17, "1"); c.r(10, 18, 13, 19, "3")
    c.r(3, 19, 6, 19, "1")
    # torso
    c.r(5, 8, 10, 16, "2"); c.r(5, 8, 6, 16, "1"); c.r(10, 8, 10, 16, "3")
    c.r(6, 13, 9, 13, "3")
    # three pairs of arms, hands gripping each other
    for y, h in ((8, 2), (11, 2), (14, 2)):
        c.r(2, y, 4, y + h - 1, "2"); c.r(11, y, 13, y + h - 1, "3")
    c.r(3, 8, 3, 15, "1"); c.r(12, 8, 12, 15, "3") if False else None
    c.r(5, 10, 10, 10, "1") if False else None
    for y in (9, 12, 15):
        c.r(6, y, 9, y, "l"); c.p(7, y, "w"); c.p(8, y, "w")
    c.r(2, 16, 4, 16, "3"); c.r(11, 16, 13, 16, "3")
    # head: ape brow and jaw
    c.r(5, 2, 10, 2, "2"); c.r(4, 3, 11, 7, "2"); c.r(4, 3, 7, 3, "1")
    c.r(11, 3, 11, 7, "3")
    c.r(4, 4, 11, 4, "3")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 6, "1"); c.p(7, 6, "3"); c.p(8, 6, "3")
    c.r(5, 7, 10, 7, "3"); c.p(6, 7, "w"); c.p(9, 7, "w")
    # moss
    for x, y in ((4, 2), (11, 8), (3, 18), (12, 17), (7, 19), (5, 9), (9, 12), (2, 12), (13, 10)):
        c.p(x, y, "g")
    c.p(4, 3, "h"); c.p(12, 19, "G"); c.p(1, 20, "g") if False else None
    c.shadow(0, 15)
    return c.out()


def rocket_turret():
    c = new()
    # tripod
    c.line(7, 12, 2, 21, "L"); c.line(8, 12, 13, 21, "L"); c.line(7, 13, 7, 21, "l")
    c.line(8, 13, 8, 21, "L")
    c.r(0, 21, 3, 21, "l"); c.r(12, 21, 15, 21, "l"); c.r(6, 21, 9, 21, "l")
    c.r(0, 22, 3, 22, "O") if False else None
    # head housing
    c.r(5, 8, 12, 13, "2"); c.r(5, 8, 12, 9, "1"); c.r(5, 12, 12, 13, "3"); c.r(11, 9, 12, 12, "3")
    # sensor eye
    c.r(6, 10, 8, 12, "O"); c.p(7, 11, "4"); c.p(6, 10, "5"); c.p(8, 10, "4") if False else None
    # rocket pod barrels (two stacked) with red warheads
    c.r(0, 4, 5, 6, "L"); c.r(0, 4, 5, 4, "l")
    c.r(0, 8, 4, 10, "L") if False else None
    c.r(0, 5, 0, 6, "O")
    c.r(1, 5, 2, 5, "R"); c.p(0, 5, "r")
    c.r(2, 7, 5, 8, "L"); c.r(0, 7, 4, 8, "l")
    c.p(0, 7, "r"); c.p(0, 8, "R"); c.p(1, 7, "R")
    c.r(5, 5, 5, 7, "L")
    # ammo racks on top
    c.r(7, 4, 11, 7, "L"); c.r(7, 4, 11, 4, "l")
    c.p(8, 5, "r"); c.p(10, 5, "r"); c.p(8, 6, "R"); c.p(10, 6, "R")
    c.p(13, 9, "L"); c.p(14, 9, "4"); c.line(13, 10, 13, 12, "L")
    c.shadow(0, 15)
    return c.out()


def slug():
    c = new()
    # slime trail
    c.r(0, 21, 4, 21, "6"); c.p(0, 20, "5")
    # soft mound
    c.ell(9, 16, 7, 4.6, "3")
    c.ell(9, 15.4, 6.4, 4, "2")
    c.ell(8, 13.5, 4.5, 2.2, "1")
    c.r(2, 19, 15, 20, "3")
    c.r(3, 19, 15, 19, "2") if False else None
    # glistening spots (blue)
    for x, y in ((7, 15), (10, 14), (12, 17), (5, 17), (9, 18)):
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    # head and eyestalks
    c.ell(3, 16, 2.4, 2.8, "2")
    c.p(1, 17, "O"); c.p(2, 18, "3")
    c.line(2, 14, 1, 9, "2"); c.line(4, 14, 6, 9, "2")
    c.ell(1, 8, 1.3, 1.3, "1"); c.ell(6, 8, 1.3, 1.3, "1")
    c.p(1, 8, "O"); c.p(6, 8, "O")
    # steam of hot life
    c.p(11, 11, "w"); c.p(12, 9, "w"); c.p(10, 8, "l")
    c.shadow(0, 15)
    return c.out()


def succulent():
    c = new()
    # clay pot
    c.r(3, 16, 12, 17, "n")
    c.r(4, 18, 11, 21, "n"); c.r(11, 18, 11, 21, "N"); c.r(3, 16, 12, 16, "t")
    c.r(5, 21, 10, 21, "N")
    c.r(4, 22, 11, 22, "O") if False else None
    c.line(6, 17, 7, 21, "N"); c.p(7, 19, "O"); c.p(6, 18, "O") if False else None
    # soil
    c.r(4, 15, 11, 15, "e")
    # cactus body
    c.r(6, 5, 9, 15, "2"); c.r(6, 5, 7, 15, "1"); c.r(9, 5, 9, 15, "3")
    c.r(7, 4, 8, 4, "1")
    for y in (7, 10, 13):
        c.p(7, y, "3")
    # arms (channeled, waggling)
    c.r(2, 9, 5, 10, "2"); c.r(2, 5, 3, 9, "2"); c.r(2, 5, 2, 9, "1"); c.p(2, 4, "1")
    c.r(10, 8, 13, 9, "2"); c.r(12, 4, 13, 8, "3"); c.p(13, 3, "2")
    c.r(12, 12, 14, 13, "2") if False else None
    # thorns and flowers
    c.p(5, 6, "w"); c.p(10, 12, "w"); c.p(4, 11, "w") if False else None
    c.p(7, 3, "4"); c.p(8, 3, "4"); c.p(7, 2, "5")
    c.p(2, 3, "4"); c.p(13, 2, "4")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.shadow(2, 13)
    return c.out()


def thirst_thistle():
    c = new()
    # triangular leaves splayed at the base
    poly(c, [(8, 21), (0, 12), (4, 20)], "2")
    poly(c, [(8, 21), (15, 12), (11, 20)], "3")
    poly(c, [(8, 21), (3, 15), (7, 12)], "1")
    poly(c, [(8, 21), (12, 15), (9, 12)], "2")
    c.line(8, 21, 1, 12, "1"); c.line(8, 21, 14, 12, "2")
    c.r(7, 22, 8, 22, "L") if False else None
    # stalk
    c.r(7, 8, 8, 20, "2"); c.r(7, 8, 7, 20, "1"); c.r(8, 8, 8, 20, "3")
    # thistle head
    c.ell(8, 5.5, 3.4, 3, "5")
    c.ell(8, 5.2, 2.6, 2.2, "4")
    for x, y in ((8, 0), (5, 1), (11, 1), (3, 3), (13, 3), (2, 6), (14, 6), (4, 9), (12, 9)):
        c.p(x, y, "w")
    for x, y in ((8, 1), (6, 2), (10, 2), (4, 4), (12, 4), (3, 6), (13, 6)):
        c.p(x, y, "4")
    c.p(7, 5, "O"); c.p(9, 5, "O")
    c.shadow(1, 14)
    return c.out()


def urchin():
    c = new()
    cx, cy = 8, 13
    # spines like gear teeth
    import math
    for i in range(14):
        a = i * math.tau / 14
        x1 = cx + math.cos(a) * 6.4; y1 = cy + math.sin(a) * 6.6
        x0 = cx + math.cos(a) * 4; y0 = cy + math.sin(a) * 4
        c.line(round(x0), round(y0), round(x1), round(y1), "4" if i % 2 else "5")
        c.p(round(cx + math.cos(a) * 7.2), round(cy + math.sin(a) * 7.4), "w" if i % 2 else "4")
    c.ell(cx, cy, 5, 5.2, "3")
    c.ell(cx - 0.3, cy - 0.4, 4.4, 4.5, "2")
    c.ell(cx - 1.4, cy - 1.8, 2.4, 1.8, "1")
    c.p(6, 13, "O"); c.p(10, 13, "O"); c.r(7, 16, 9, 16, "O")
    c.shadow(1, 14)
    return c.out()


def wedge():
    c = new()
    # prismatoid gelatin wedge
    poly(c, [(1, 20), (7, 6), (14, 20)], "5")
    poly(c, [(3, 19), (7, 8), (12, 19)], "2")
    poly(c, [(7, 8), (12, 19), (8, 19)], "3")
    poly(c, [(4, 17), (7, 10), (7, 17)], "1")
    c.line(1, 20, 14, 20, "6"); c.r(1, 20, 14, 21, "5")
    c.r(2, 21, 13, 21, "6")
    c.line(7, 6, 7, 20, "4")
    c.p(7, 5, "4") if False else None
    # inclusions and eyes
    c.p(6, 14, "O"); c.p(9, 14, "O")
    c.r(6, 17, 9, 17, "O"); c.p(7, 17, "w"); c.p(8, 17, "w")
    c.p(5, 12, "w"); c.p(6, 11, "w")
    c.p(10, 16, "4"); c.p(5, 18, "4")
    # extruded pseudopod
    c.r(13, 18, 15, 19, "5"); c.p(15, 17, "4")
    c.shadow(0, 15, 22)
    return c.out()


def yurl():
    c = new()
    # coiled vine base
    tube(c, [(2, 21), (7, 20), (13, 21)], 1.2, 1.2, "g")
    tube(c, [(4, 19), (9, 17), (12, 14)], 1.0, 0.8, "g")
    c.p(2, 18, "G"); c.p(13, 19, "G"); c.p(5, 21, "h"); c.p(10, 21, "h")
    # leaves
    poly(c, [(3, 17), (0, 13), (5, 14)], "g")
    poly(c, [(13, 18), (15, 14), (11, 15)], "g")
    c.line(3, 17, 1, 14, "G")
    # puffed bulb
    c.ell(8, 9, 6.5, 6.2, "3")
    c.ell(8, 8.7, 5.8, 5.5, "2")
    c.ell(6.5, 6.5, 3.4, 2.4, "1")
    c.p(5, 5, "w"); c.p(6, 4, "w")
    c.line(8, 14, 8, 17, "g")
    # eyes (basking) and mouth
    c.p(5, 9, "O"); c.p(6, 9, "O"); c.p(10, 9, "O"); c.p(11, 9, "O")
    c.r(7, 12, 9, 12, "O")
    c.p(3, 7, "4"); c.p(12, 6, "4"); c.p(8, 3, "4") if False else None
    # tendrils on top
    c.line(8, 3, 6, 1, "G"); c.line(8, 3, 11, 0, "G"); c.p(6, 1, "4"); c.p(11, 0, "4")
    c.shadow(1, 14, 22)
    return c.out()


# =============================================================== table
def _mk():
    d = {
        "cannibal_convert": cannibal_convert(), "cherub_hermit": cherub_hermit(), "crowsong": crowsong(),
        "glittermensch": glittermensch(), "golem_cragsmensch": golem_cragsmensch(),
        "golem_troll": golem_troll(), "issachari_convert": issachari_convert(), "naphtaali": naphtaali(),
        "nuntu": nuntu(), "skybear": skybear(), "slynth_stilt": slynth_stilt(), "troll": troll(),
        "zothom": zothom(),
        "baetyl": baetyl(), "cat": cat(), "cherub_bear_mechanical": mech_bear(),
        "cherub_dog_mechanical": mech_dog(), "cherub_frog_mechanical": mech_frog(),
        "cherub_mollusk_mechanical": mech_mollusk(), "cherub_robot_mechanical": mech_robot(),
        "cherub_tortoise_mechanical": mech_tortoise(), "cherub_winged_mammal_mechanical": mech_bat(),
        "crypt_ferret": crypt_ferret(), "eater": eater(), "fungus": fungus(), "godhed": godhed(),
        "golem_bed": golem_bed(), "golem_dawnglider": golem_dawnglider(), "golem_fungus": golem_fungus(),
        "golem_jelly": golem_jelly(), "golem_quadrupedal_robot": golem_quad_robot(),
        "golem_swine": golem_swine(), "golem_wall": golem_wall(), "lamprey": lamprey(), "monad": monad(),
        "natural_weapon_bands": natural_weapon_bands(), "natural_weapon_fist": natural_weapon_fist(),
        "natural_weapon_mandible": natural_weapon_mandible(), "natural_weapon_tail": natural_weapon_tail(),
        "oboroqoru_statue": oboroqoru_statue(), "rebekah": rebekah(), "rocket_turret": rocket_turret(),
        "slug": slug(), "succulent": succulent(), "thirst_thistle": thirst_thistle(), "urchin": urchin(),
        "wedge": wedge(), "yurl": yurl(),
    }
    return d


SPRITES = _mk()
