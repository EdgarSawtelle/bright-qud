"""B3 remaining creatures, batch 1: odd Qud people (humanoid layout) + chiliad/golem/cherub creatures."""
import os
import sys
from functools import partial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b3kit as K  # noqa: E402
from b3kit import (C, back, overlay, person, hat_pointy, hood, hair_long, beard, spectacles, apron,
                   sun_halo, halo, staff, wrench, belt_pouches, lantern, bow, quiver, veil, crown,
                   horn_headdress, scarf, book)  # noqa: E402
from b3_wilds import tube  # noqa: E402
from b3_people import moss_fur, goat_legs  # noqa: E402
from b3more_keys import MORE_KEYS  # noqa: E402

KEYS = MORE_KEYS[1]
P = person
HUMANOID = set()


# ================================================================= humanoid parts
def flask(c):
    """glowing alembic flask held at the left hip."""
    c.r(1, 12, 2, 13, "L")
    c.p(0, 12, "l") if False else None
    c.r(0, 14, 3, 17, "4")
    c.r(0, 17, 3, 17, "5")
    c.p(0, 14, "w"); c.p(1, 15, "w")
    c.p(3, 14, "5"); c.p(3, 16, "5")
    c.p(2, 11, "w"); c.p(1, 10, "4")      # bubbles
    c.p(4, 15, "s"); c.p(3, 15, "s") if False else None
    c.p(2, 12, "L")


@back
def ape_wings(c):
    c.rows(K.MUTATIONS["Wings"][1])


def ape_head(c):
    """heavy-browed ape: fur cap, dark face, muzzle."""
    c.r(5, 2, 10, 3, "1")
    c.r(6, 2, 9, 2, "2")
    c.r(4, 4, 5, 7, "1"); c.r(10, 4, 11, 7, "3")      # cheek fur
    c.r(6, 4, 9, 4, "3")                               # brow ridge
    c.r(6, 5, 9, 7, "S")
    c.r(6, 6, 9, 7, "s")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.r(7, 6, 8, 6, "S")
    c.p(7, 8, "3"); c.p(8, 8, "3")


def long_arms(c):
    """arms hang almost to the knees, knuckle-walker."""
    c.r(3, 10, 3, 17, "2"); c.r(12, 10, 12, 17, "3")
    c.r(2, 12, 3, 12, "1") if False else None
    c.p(4, 15, "2"); c.p(11, 15, "3")
    c.r(2, 18, 3, 19, "S"); c.r(12, 18, 13, 19, "S")
    c.p(2, 19, "O") if False else None


def cherub_halo(c):
    halo(c, "4", "5")


def blind_glow(c):
    """hooded stranger: glowing eyes only."""
    c.r(5, 4, 10, 7, "O")
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(7, 5, "w") if False else None
    c.p(6, 6, "5") if False else None


def stranger_cloak(c):
    c.r(3, 10, 4, 18, "3"); c.r(11, 10, 12, 18, "3")
    c.r(3, 19, 12, 20, "3")
    c.p(8, 12, "4"); c.p(8, 14, "4"); c.p(8, 16, "4")   # star studs down the front


def spool_hat(c):
    """habit shaped like a frustum, spools of hair bunched beneath."""
    c.r(6, 0, 9, 0, "1")
    c.r(5, 1, 10, 1, "2")
    c.r(4, 2, 11, 2, "2")
    c.r(4, 2, 11, 2, "4") if False else None
    c.r(5, 2, 10, 2, "4")
    c.p(11, 1, "3"); c.r(10, 2, 11, 2, "3") if False else None
    c.r(4, 3, 11, 3, "N")
    c.p(5, 1, "1")
    c.mr(3, 4, 4, 6, "n")
    c.mr(3, 4, 3, 4, "N")
    c.mr(3, 5, 4, 5, "N")
    c.m(4, 6, "N"); c.m(3, 6, "n")
    c.p(5, 6, "R"); c.p(10, 6, "R")                    # smeared round cheeks


def glitter_crown(c):
    """crystal shards with a glittering corona."""
    c.p(5, 0, "w"); c.p(8, 0, "w"); c.p(10, 0, "4")
    c.r(5, 1, 10, 1, "4"); c.p(7, 1, "w"); c.p(6, 0, "4")
    c.r(5, 2, 10, 2, "1")
    c.r(5, 3, 10, 3, "4")
    c.p(7, 0, "1"); c.p(9, 1, "w")
    c.p(3, 2, "w"); c.p(12, 3, "w"); c.p(4, 1, "4"); c.p(11, 1, "4")


def glitter(c):
    for (x, y) in ((1, 6), (14, 9), (2, 13), (13, 15), (1, 19), (14, 20)):
        c.p(x, y, "w")
        c.p(x - 1, y, "4"); c.p(x + 1, y, "4"); c.p(x, y - 1, "4"); c.p(x, y + 1, "4")
    for (x, y) in ((6, 12), (9, 17), (5, 19), (10, 11), (7, 14), (8, 20)):
        c.p(x, y, "w")


def glitter_gem(c):
    """a great cut gem held up in the left hand."""
    c.r(1, 10, 3, 10, "w")
    c.r(0, 11, 4, 12, "4")
    c.r(1, 13, 3, 13, "5")
    c.p(2, 14, "5")
    c.p(2, 11, "w"); c.p(1, 11, "w")
    c.p(3, 12, "5"); c.p(4, 12, "5")
    c.p(4, 15, "s")


def camel_head(c):
    """camel-folk: narrow head on a long inked neck, split-lip muzzle, ringed ears, lashes."""
    c.r(6, 2, 9, 3, "1")
    c.r(6, 4, 9, 6, "2")
    c.r(9, 3, 9, 7, "3")
    c.r(5, 6, 10, 8, "1")                  # broad muzzle
    c.r(5, 8, 10, 8, "2")
    c.r(7, 9, 8, 12, "2"); c.p(8, 9, "3"); c.p(8, 11, "3")   # long neck
    c.r(5, 9, 10, 9, "2") if False else None
    c.p(6, 7, "O"); c.p(9, 7, "O"); c.p(8, 8, "O")           # nostrils, lip split
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(6, 4, "O"); c.p(9, 4, "O")                           # lashes
    c.mr(3, 2, 5, 3, "2")
    c.m(3, 2, "1"); c.m(3, 3, "3")
    c.m(3, 4, "y"); c.m(4, 4, "y")                           # gilded ear rings
    c.p(7, 10, "y"); c.p(8, 11, "y"); c.p(7, 12, "y")        # ink dulla patterns
    c.mr(4, 12, 5, 12, "2")


def camel_hump(c):
    """hump rising behind the shoulders."""
    c.r(8, 6, 13, 8, "2")
    c.r(7, 7, 14, 12, "2")
    c.r(11, 8, 14, 12, "3")
    c.r(8, 7, 10, 8, "1")
    c.p(12, 9, "y"); c.p(13, 11, "y"); c.p(10, 10, "y")


def golem_cracks(c):
    for (x, y) in ((5, 12), (6, 13), (9, 17), (8, 18), (6, 19)):
        c.p(x, y, "3")
    c.p(7, 14, "y"); c.p(8, 15, "y")
    c.p(7, 15, "y") if False else None


def newfather_face(c):
    """overly jawed face, big drooping white lips, heavy lids."""
    c.r(5, 4, 10, 4, "O") if False else None
    c.r(6, 4, 9, 4, "S")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(6, 4, "O") if False else None
    c.r(5, 7, 10, 9, "S")
    c.r(6, 10, 9, 10, "S")
    c.r(10, 7, 10, 10, "s") if False else None
    c.r(6, 8, 9, 9, "w")
    c.r(7, 9, 8, 9, "R")
    c.r(6, 10, 9, 10, "w")
    c.p(9, 10, "l"); c.p(9, 9, "l")
    c.p(5, 8, "S"); c.p(10, 8, "S")


def crutch(c):
    c.line(13, 8, 13, 22, "n")
    c.r(11, 7, 14, 7, "n")
    c.p(11, 8, "N"); c.p(14, 8, "N")
    c.p(12, 15, "s"); c.p(11, 15, "s")


def diodes(c):
    """blinking diodes studding the hood."""
    c.p(7, 1, "4"); c.p(5, 3, "4"); c.p(10, 3, "5"); c.p(4, 6, "5"); c.p(11, 7, "4")
    c.p(8, 1, "5") if False else None
    c.p(6, 9, "4") if False else None


def field_straps(c):
    c.line(5, 9, 10, 14, "L")
    c.line(10, 9, 5, 14, "L")
    c.p(7, 11, "4"); c.p(8, 12, "5")


def bone_mask(c):
    c.r(5, 3, 10, 7, "w")
    c.r(10, 3, 10, 7, "l")
    c.r(6, 7, 9, 7, "l")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.p(6, 5, "O"); c.p(5, 5, "O") if False else None
    c.p(7, 5, "y") if False else None
    c.r(6, 4, 6, 4, "O"); c.p(9, 4, "O")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.p(7, 3, "5"); c.p(8, 3, "5")
    c.p(5, 5, "y"); c.p(10, 5, "y")


def moss_ears(c):
    c.p(4, 3, "g"); c.p(5, 2, "g"); c.p(11, 3, "g"); c.p(10, 2, "h")
    c.r(6, 2, 9, 2, "g"); c.r(5, 3, 10, 3, "g")
    c.p(7, 2, "h"); c.p(9, 2, "h")


def salt_hair(c):
    """long salted locks."""
    c.r(6, 2, 9, 2, "w")
    c.r(5, 3, 10, 3, "w")
    c.r(4, 4, 5, 13, "w"); c.r(10, 4, 11, 13, "l")
    c.p(5, 4, "w"); c.p(10, 4, "l")
    c.p(7, 2, "l"); c.p(6, 3, "l"); c.p(4, 8, "l"); c.p(5, 11, "l"); c.p(10, 7, "w"); c.p(11, 11, "w")
    c.p(4, 14, "w"); c.p(11, 14, "l"); c.p(4, 5, "l")


def number_beads(c):
    """left hand counts glowing numerals on a ring of beads."""
    c.line(1, 10, 3, 14, "4")
    c.p(1, 10, "w"); c.p(1, 12, "4"); c.p(2, 12, "w") if False else None
    c.p(0, 11, "5"); c.p(2, 11, "w"); c.p(0, 13, "5"); c.p(3, 13, "w"); c.p(1, 14, "5")
    c.p(4, 15, "s"); c.p(3, 15, "5") if False else None
    c.p(1, 9, "4"); c.p(3, 9, "5")


def numeral_hem(c):
    c.r(5, 12, 10, 12, "5")
    for x in (5, 7, 9):
        c.p(x, 13, "4")
    c.r(5, 20, 10, 20, "5")
    for x in (4, 6, 8, 10):
        c.p(x, 19, "4")


def flower_crown(c, petal="4", petal2="5", gem="c"):
    """slynth crown: petals around a glowing crystal in place of eyes."""
    c.r(6, 0, 9, 0, petal)
    c.r(4, 1, 11, 1, petal)
    c.r(5, 1, 10, 1, petal)
    c.p(5, 0, petal2); c.p(10, 0, petal2)
    c.r(4, 2, 11, 2, petal2)
    c.r(5, 3, 10, 3, "1")
    c.r(5, 2, 10, 2, "1")
    c.p(4, 2, petal); c.p(11, 2, petal2); c.p(4, 3, petal2); c.p(11, 3, petal2); c.p(3, 3, petal)
    c.p(12, 3, petal)
    c.p(3, 2, "1") if False else None
    c.p(7, 1, "y"); c.p(8, 1, "y")


def forehead_crystal(c):
    c.r(7, 3, 8, 7, "B")
    c.r(7, 4, 8, 6, "c")
    c.r(7, 4, 7, 5, "w")
    c.p(6, 5, "B"); c.p(9, 5, "B")
    c.p(8, 7, "b")
    c.p(6, 4, "c"); c.p(9, 6, "c")


def vibrate(c):
    for y in (11, 14, 17):
        c.p(2, y, "w"); c.p(1, y + 1, "4"); c.p(13, y, "w"); c.p(14, y + 1, "4")


def leaf_dress(c):
    c.r(3, 19, 12, 21, "3")
    for x in range(3, 13, 2):
        c.p(x, 22, "2"); c.p(x, 21, "1")
    c.line(4, 12, 1, 15, "2"); c.line(11, 12, 14, 15, "3")
    c.p(1, 14, "1"); c.p(14, 14, "1")
    c.p(2, 15, "1"); c.p(13, 16, "1")


def flute(c):
    c.line(7, 8, 14, 9, "n")
    c.line(7, 9, 14, 10, "N") if False else None
    c.r(9, 8, 9, 8, "O"); c.r(11, 9, 11, 9, "O"); c.r(13, 9, 13, 9, "O")
    c.p(14, 8, "y"); c.p(14, 10, "y") if False else None
    c.p(7, 7, "n")
    c.p(10, 10, "1"); c.p(12, 10, "1"); c.p(11, 11, "1"); c.p(9, 10, "1")  # finger stems
    c.p(11, 10, "1")
    c.line(11, 10, 11, 14, "1") if False else None


def pleat_roots(c):
    c.r(3, 19, 12, 20, "3")
    for x in (3, 5, 7, 9, 11):
        c.line(x, 20, x + (-1 if x < 8 else 1), 22, "3")
        c.p(x + 1, 21, "N")
    c.p(2, 22, "N"); c.p(13, 22, "N")
    c.p(2, 21, "3") if False else None


def godling_spine(c):
    for y in (9, 11, 13, 15):
        c.p(3, y, "w"); c.p(2, y + 1, "L")
    for y in (10, 12, 14):
        c.p(12, y, "w")
    c.p(7, 8, "w"); c.p(8, 8, "w")


def godling_face(c):
    c.p(6, 5, "4"); c.p(9, 5, "4")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.r(7, 7, 8, 7, "R"); c.r(8, 8, 8, 9, "R"); c.p(9, 10, "R"); c.p(9, 11, "r")


def godling_sheen(c):
    for (x, y) in ((5, 10), (9, 12), (6, 14), (10, 10), (8, 17), (5, 18)):
        c.p(x, y, "4" if (x + y) % 2 else "5")
    c.p(8, 13, "w")


def godling_hooves(c):
    goat_legs(c, "2", "3")
    c.r(4, 22, 5, 22, "w"); c.r(10, 22, 11, 22, "w")


SPRITES = {}


def H(name, grid):
    SPRITES[name] = grid
    HUMANOID.add(name)


H("alchemist", P(hat_pointy, spectacles, beard, apron, flask, face="face", sash=False))
H("cherub_ape", P(ape_wings, ape_head, long_arms, cherub_halo, face="none", sash=False))
H("cherub_stranger", P(ape_wings, hood, blind_glow, stranger_cloak, cherub_halo, face="none", trim="4"))
H("daughter_wrench", P(spool_hat, wrench, face="face", trim="4"))
H("glittermensch_luminary", P(glitter_crown, glitter, glitter_gem, face="face", sash=False))
H("golem_dromad", P(camel_hump, golem_cracks, camel_head, face="none", sash=True, trim="4"))
H("grand_newfather", P(hood, newfather_face, crutch, face="face", sash=False))
H("mechanimist", P(hood, diodes, belt_pouches, field_straps, lantern, face="goggles", sash=False))
H("naphtaali_nimrod", P(quiver, moss_fur, moss_ears, bone_mask, bow, face="none", sash=False))
H("preacher", P(salt_hair, numeral_hem, number_beads, face="face", sash=False, trim="4"))
H("slynth_chavvah", P(leaf_dress, flower_crown, forehead_crystal, vibrate, face="none", sash=False, skin=("1", "3")))
H("slynth_yd", P(pleat_roots, flute, partial(flower_crown, petal="4", petal2="5"), face="face", sash=False, skin=("1", "3")))
H("true_godling", P(ape_wings, godling_hooves, K.hair_wild if False else horn_headdress, godling_spine, godling_face, godling_sheen, face="none", sash=False))


# ================================================================= creature helpers
def path_pts(pts, step=0.5):
    d = [0.0]
    for (a, b), (e, f) in zip(pts, pts[1:]):
        d.append(d[-1] + ((e - a) ** 2 + (f - b) ** 2) ** 0.5)
    tot = d[-1] or 1
    n = max(1, int(tot / step))
    out = []
    for i in range(n + 1):
        t = i / n * tot
        k = 1
        while k < len(d) - 1 and d[k] < t:
            k += 1
        u = (t - d[k - 1]) / ((d[k] - d[k - 1]) or 1)
        out.append((pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * u,
                    pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * u, t / tot))
    return out


def beads(c, pts, r0, r1, cols, step=1.1):
    """segmented tube: alternating coloured balls along a path."""
    sm = path_pts(pts, step)
    for i, (x, y, t) in enumerate(sm):
        r = r0 + (r1 - r0) * t
        c.ell(x, y, r, r, cols[(i // 2) % len(cols)])
    return sm


def ring(c, x0, y=0):
    """glowing cherub halo, 6 wide."""
    c.r(x0 + 1, y, x0 + 4, y, "4")
    c.p(x0, y + 1, "4"); c.p(x0 + 5, y + 1, "4")
    c.p(x0 + 1, y + 1, "5"); c.p(x0 + 4, y + 1, "5")
    c.p(x0 + 2, y + 1, "."); c.p(x0 + 3, y + 1, ".")


def clear(c, x0, y0, x1, y1):
    c.r(x0, y0, x1, y1, ".")


def grid_from(rows):
    assert len(rows) == 24, len(rows)
    return [r.ljust(16, ".") for r in rows]


# ================================================================= creatures
def agolmaggot():
    c = C()
    tube(c, [(5, 5), (9, 9), (8, 15), (8, 20)], 3.0, 3.8, "2")
    tube(c, [(4.5, 5), (8, 9), (7, 15), (7, 19)], 1.2, 1.6, "1")
    tube(c, [(7, 7), (10.5, 10), (10, 15), (10, 20)], 0.6, 1.0, "3")
    for y in (9, 12, 15, 18):
        for x in range(2, 14):
            if c.g[y][x] in "12":
                c.g[y][x] = "3"
    # head, mouth
    c.r(2, 3, 3, 5, "3"); c.p(2, 4, "O"); c.p(2, 5, "O"); c.p(3, 3, "w"); c.p(1, 6, "w") if False else None
    c.p(4, 3, "O") if False else None
    c.p(5, 3, "w"); c.p(3, 6, "w")
    for (x, y) in ((6, 10), (9, 13), (6, 16), (9, 18), (7, 7)):
        c.r(x, y, x + 1, y + 1, "5")
        c.p(x, y, "4"); c.p(x + 1, y + 1, "6") if False else None
    for (x, y) in ((12, 9), (13, 7), (12, 14), (13, 12), (4, 12), (3, 15), (11, 19)):
        c.p(x, y, "h"); c.p(x + 1, y - 1, "g") if False else None
    c.p(11, 11, "g"); c.p(12, 17, "g")
    c.shadow(2, 13)
    return c.out()


def bear():
    c = C()
    # winged: folded wings on the back
    c.r(2, 16, 4, 21, "3"); c.r(5, 17, 7, 21, "2")
    c.r(11, 17, 13, 21, "3"); c.r(8, 17, 10, 21, "2")
    c.ell(9.5, 13, 6, 4.6, "2")
    c.ell(9.5, 11.5, 5, 2.8, "1")
    c.ell(10, 15.5, 5, 1.8, "3")
    # great furry wings laid across the back
    c.ell(11, 10, 4.2, 2.6, "4")
    c.ell(9, 12, 4.5, 2.2, "5")
    c.line(7, 12, 14, 8, "6")
    c.line(8, 13, 14, 11, "6")
    c.p(14, 9, "4"); c.p(14, 12, "5"); c.p(13, 13, "4")
    # head
    c.ell(3.5, 11, 3.2, 3.0, "2")
    c.r(0, 11, 2, 13, "1"); c.p(0, 11, "O"); c.p(0, 12, "O")
    c.p(3, 10, "O")
    c.ell(2.5, 7.8, 1.5, 1.5, "3"); c.ell(5.5, 8.2, 1.4, 1.3, "3")
    # ear-wing flapping at the bugs
    c.line(2, 6, 0, 2, "4"); c.line(3, 6, 2, 1, "5"); c.line(4, 6, 5, 2, "4")
    c.p(0, 0, "O") if False else None
    c.p(7, 3, "O"); c.p(8, 4, "O")   # bugs
    c.r(2, 21, 4, 21, "w"); c.r(11, 21, 13, 21, "w")
    c.r(5, 21, 7, 21, "w"); c.r(8, 21, 10, 21, "w")
    c.shadow(1, 14)
    return c.out()


# ---- cherub machines
def cherub_antelope_mechanical():
    c = C()
    ring(c, 9)
    c.ell(9, 12, 4.8, 2.8, "2"); c.ell(8.5, 11, 4, 1.4, "1")
    c.r(10, 13, 13, 14, "3")
    # neck + head
    c.line(5, 9, 4, 6, "2"); c.line(6, 9, 5, 6, "2"); c.line(6, 8, 5, 6, "1")
    c.ell(3.5, 5.5, 2.2, 1.7, "2")
    c.r(0, 6, 2, 7, "1"); c.p(0, 6, "O")
    c.p(3, 5, "4"); c.p(4, 5, "5") if False else None
    # long straight horns
    c.line(4, 4, 8, 0, "l"); c.line(3, 4, 6, 0, "L")
    c.p(5, 3, "w"); c.p(7, 1, "w")
    c.p(2, 3, "L"); c.p(1, 2, "L")
    # thin legs with chrome knees
    for x, a in ((5, "2"), (7, "3"), (11, "2"), (13, "3")):
        c.r(x, 14, x, 21, a)
        c.p(x, 17, "l"); c.p(x, 22, "O")
    c.r(14, 10, 15, 11, "3")                       # tail
    c.p(8, 11, "4"); c.p(9, 11, "4")
    c.r(6, 13, 12, 13, "3")
    c.shadow(2, 15)
    return c.out()


def cherub_equine_mechanical():
    c = C()
    ring(c, 0)
    tube(c, [(13, 10), (15, 14), (14, 19)], 1.3, 0.8, "4")
    c.ell(9, 12, 5.2, 3.4, "2"); c.ell(8.5, 10.5, 4.3, 1.5, "1")
    c.r(11, 13, 14, 15, "3")
    c.r(4, 6, 7, 11, "2"); c.r(3, 7, 4, 10, "1")
    c.ell(3, 5.5, 2.6, 1.9, "2")
    c.r(0, 6, 2, 8, "1"); c.p(0, 7, "O"); c.p(3, 5, "4")
    c.p(3, 3, "3"); c.p(4, 3, "3"); c.p(4, 4, "3")
    c.line(5, 3, 8, 10, "4"); c.line(6, 3, 9, 10, "5"); c.line(4, 3, 7, 9, "4")
    c.ell(10, 12, 1.6, 1.6, "l"); c.p(10, 12, "4"); c.p(9, 11, "w")    # flank gear
    for x, h in ((4, "2"), (6, "3"), (11, "2"), (13, "3")):
        c.r(x, 14, x + 1, 20, h)
        c.r(x, 17, x + 1, 17, "l")
        c.r(x, 21, x + 1, 21, "O")
    c.shadow(1, 15, 22)
    return c.out()


def cherub_bird_mechanical():
    c = C()
    ring(c, 2)
    c.ell(8.5, 14, 4.2, 4, "2"); c.ell(7.5, 12.5, 3, 2, "1")
    c.ell(5, 8.5, 2.4, 2.4, "2"); c.ell(4.5, 8, 1.5, 1.4, "1")
    c.r(1, 8, 3, 9, "4"); c.p(0, 9, "5")
    c.p(5, 7, "w"); c.p(5, 8, "O")
    c.line(5, 10, 7, 12, "2")
    # wing plates
    c.ell(11, 13.5, 3, 3.6, "3")
    for y in (11, 13, 15):
        c.line(10, y, 14, y + 1, "l")
    c.p(13, 17, "L")
    # tail feathers
    c.line(11, 17, 14, 21, "l"); c.line(10, 18, 12, 22, "L"); c.line(12, 16, 15, 19, "l")
    c.p(14, 21, "4"); c.p(12, 22, "4")
    c.p(7, 15, "4")
    # legs
    c.line(7, 18, 7, 21, "l"); c.line(10, 18, 10, 21, "l")
    c.r(5, 21, 8, 21, "L"); c.r(9, 21, 12, 21, "L")
    c.shadow(2, 14)
    return c.out()


def cherub_fungus_mechanical():
    c = C()
    ring(c, 5)
    c.ell(8, 9, 7, 5.2, "2")
    c.ell(7, 7.5, 5, 2.8, "1")
    clear(c, 0, 12, 15, 13)
    c.r(1, 12, 14, 12, "3")
    for x in range(2, 14, 2):
        c.p(x, 13, "3")
    c.r(2, 12, 13, 12, "l")
    c.p(2, 12, "w")
    for (x, y) in ((4, 7), (8, 5), (11, 8), (6, 9), (10, 5)):
        c.p(x, y, "4"); c.p(x + 1, y, "5")
    c.r(6, 13, 9, 19, "1"); c.r(9, 13, 9, 19, "3")
    c.r(6, 14, 9, 14, "l")
    c.p(7, 16, "O"); c.p(8, 16, "O"); c.p(7, 16, "4"); c.p(8, 16, "4")
    c.r(7, 18, 8, 18, "O")
    c.r(4, 19, 11, 21, "3"); c.r(5, 19, 8, 19, "2")
    c.p(2, 20, "L"); c.p(13, 20, "L")
    c.shadow(2, 13)
    return c.out()


def cherub_newly_sentient_being_mechanical():
    c = C()
    ring(c, 5)
    c.r(6, 4, 9, 5, "2"); c.r(5, 3, 10, 3, "l"); c.r(5, 3, 10, 3, "l")
    c.ell(8, 13, 5.2, 6, "2")
    c.ell(6.5, 11.5, 3, 4, "1")
    clear(c, 4, 6, 11, 6) if False else None
    c.r(6, 4, 9, 7, "2"); c.r(6, 4, 7, 7, "1")
    c.r(4, 9, 11, 9, "l"); c.r(4, 16, 11, 16, "l")
    c.p(5, 9, "w"); c.p(10, 16, "L"); c.p(11, 9, "L")
    c.r(11, 10, 11, 15, "3") if False else None
    c.p(6, 12, "4"); c.p(9, 12, "4"); c.p(6, 13, "O") if False else None
    c.r(7, 14, 8, 14, "O")
    # handles -> little chrome arms
    c.line(3, 10, 1, 13, "L"); c.line(1, 13, 3, 15, "L")
    c.line(12, 10, 14, 13, "L"); c.line(14, 13, 12, 15, "L")
    c.p(1, 13, "l"); c.p(14, 13, "l")
    c.r(5, 19, 6, 21, "L"); c.r(9, 19, 10, 21, "L")
    c.r(4, 21, 6, 21, "l"); c.r(9, 21, 11, 21, "l")
    c.shadow(2, 13)
    return c.out()


def cherub_root_mechanical():
    c = C()
    ring(c, 5)
    c.r(4, 17, 11, 20, "3"); c.r(3, 20, 12, 21, "3")
    c.r(5, 17, 7, 18, "2")
    for (pts, ch) in (([(8, 19), (6, 14), (3, 10), (3, 6)], "2"),
                      ([(8, 19), (8, 13), (8, 8), (6, 5)], "2"),
                      ([(8, 19), (10, 14), (13, 11), (13, 6)], "3"),
                      ([(7, 19), (4, 16), (1, 14)], "3"),
                      ([(9, 19), (12, 16), (14, 15)], "2")):
        tube(c, pts, 1.3, 0.8, ch)
    tube(c, [(8, 18), (7, 13), (8, 8)], 0.5, 0.4, "1")
    c.r(7, 13, 9, 15, "L"); c.r(7, 13, 9, 13, "l"); c.p(8, 14, "4")
    for (x, y) in ((3, 5), (6, 4), (13, 5), (1, 13), (14, 14)):
        c.p(x, y, "4")
    c.p(11, 10, "l"); c.p(5, 11, "l")
    c.shadow(1, 14)
    return c.out()


def cherub_tree_mechanical():
    c = C()
    ring(c, 5)
    c.r(6, 11, 9, 20, "2"); c.r(6, 11, 7, 20, "1"); c.r(9, 11, 9, 20, "3")
    c.r(5, 19, 10, 21, "2"); c.r(3, 21, 12, 21, "3")
    c.r(6, 15, 9, 15, "l"); c.r(6, 18, 9, 18, "l")
    c.p(8, 13, "4"); c.p(7, 16, "4")
    c.line(6, 12, 3, 9, "L"); c.line(9, 12, 12, 9, "L")
    c.ell(8, 8, 6.5, 4.4, "3")
    for (x, y, ch) in ((4, 8, "2"), (8, 5, "2"), (11, 8, "1"), (7, 8, "1"), (5, 6, "1"), (10, 6, "2")):
        c.ell(x, y, 2.1, 1.6, ch)
    for (x, y) in ((3, 8), (6, 5), (9, 9), (12, 7), (8, 6)):
        c.p(x, y, "4")
    c.p(2, 11, "l") if False else None
    c.shadow(2, 13)
    return c.out()


def cherub_worm_mechanical():
    c = C()
    ring(c, 4)
    sm = beads(c, [(3, 20), (8, 21), (12, 17), (8, 13), (5, 10), (7, 6)], 2.3, 2.0, ["2", "1", "2", "3"])
    for i in range(1, len(sm) - 1, 4):
        x, y, t = sm[i]
        c.p(round(x), round(y), "l")
    # head
    c.p(6, 6, "4"); c.p(8, 6, "4")
    c.p(7, 4, "L"); c.p(7, 3, "l")
    c.r(3, 19, 4, 21, "L") if False else None
    for (x, y) in ((11, 17), (9, 21), (6, 12)):
        c.p(x, y, "4")
    c.shadow(1, 14)
    return c.out()


def dagasha():
    c = C()
    # hexapod, no mouth, wicked points sheeting the whole body
    for (x0, y0, x1, y1) in [(5, 9, 1, 6), (5, 12, 0, 13), (5, 15, 2, 21)]:
        c.line(x0, y0, x1, y1, "3", mirror=True)
        c.line(x0 + 1, y0, x1 + 1, y1, "3", mirror=True) if False else None
    for (x, y) in ((1, 6), (0, 13), (2, 21)):
        c.m(x, y, "4")
    c.m(3, 8, "5"); c.m(2, 12, "5"); c.m(3, 17, "5")
    c.ell(7.5, 13, 3.8, 6, "2")
    c.ell(6.5, 11, 1.8, 3.5, "1")
    c.r(10, 10, 11, 17, "3")
    c.ell(7.5, 6.5, 2.4, 2.4, "2"); c.r(6, 5, 7, 6, "1")
    # sheet of spikes
    for (x, y) in ((3, 10), (3, 14), (4, 17), (2, 15), (4, 7)):
        c.m(x, y, "4")
    for (x, y) in ((6, 12), (7, 15), (9, 11), (6, 18), (8, 19)):
        c.p(x, y, "4"); c.p(x, y - 1, "5")
    c.p(7, 3, "4"); c.p(7, 2, "4"); c.p(5, 3, "5"); c.p(10, 3, "5")
    c.p(6, 1, "5") if False else None
    # scream arcs
    c.r(5, 0, 6, 0, "4"); c.r(9, 0, 10, 0, "4"); c.p(4, 1, "4"); c.p(11, 1, "4")
    c.p(7, 0, "w") if False else None
    c.p(7, 6, "O"); c.p(8, 6, "O") if False else None
    c.shadow(1, 14)
    return c.out()


def entropic_being():
    c = C()
    spines = [
        ([(8, 12), (8, 6), (6, 0)], "2"),
        ([(8, 12), (11, 8), (15, 6)], "3"),
        ([(8, 12), (13, 12), (15, 17)], "2"),
        ([(8, 12), (10, 17), (9, 22)], "3"),
        ([(8, 12), (5, 17), (2, 21)], "2"),
        ([(8, 12), (3, 12), (0, 10)], "3"),
        ([(8, 12), (4, 8), (3, 2)], "2"),
        ([(8, 12), (10, 4), (12, 1)], "3"),
    ]
    for pts, ch in spines:
        tube(c, pts, 1.7, 0.4, ch)
    c.p(15, 6, "4"); c.p(6, 0, "4"); c.p(15, 17, "4"); c.p(9, 22, "4")
    c.p(2, 21, "4"); c.p(0, 10, "4"); c.p(3, 2, "4"); c.p(12, 1, "4")
    for (x, y) in ((7, 4), (13, 8), (12, 14), (9, 18), (5, 16), (4, 11)):
        c.p(x, y, "5")
    c.ell(8, 12, 3.4, 3.4, "2"); c.ell(7.3, 11, 2, 2, "1")
    c.r(7, 11, 9, 13, "w"); c.p(8, 12, "O")
    c.p(9, 11, "4") if False else None
    c.shadow(2, 13)
    return c.out()


def girshling():
    from style_b3 import girshling as g0
    c = C()
    for y, row in enumerate(g0()):
        for x, ch in enumerate(row):
            c.p(x, y, ch)
    # star orchid saliva dripping from the fangs, blossom on the back
    for (x, y) in ((3, 2), (12, 2)):
        c.p(x, y, "w"); c.p(x, y - 1, "5")
    for (x, y) in ((4, 1), (11, 1)):
        c.p(x, y, "4")
    c.p(2, 4, "w"); c.p(13, 4, "w"); c.p(1, 3, "5") if False else None
    c.p(3, 5, "w") if False else None
    c.r(7, 20, 8, 21, "w"); c.p(6, 20, "4"); c.p(9, 20, "4"); c.p(7, 19, "4"); c.p(8, 22, "4")
    c.p(7, 20, "y")
    return c.out()


def godhed2_unplanished():
    c = C()
    c.p(8, 1, "l"); c.p(8, 2, "L"); c.p(8, 0, "4")
    c.ell(8, 10, 5.4, 8, "2")
    c.ell(6, 8, 2.2, 4.5, "1")
    c.r(11, 6, 13, 14, "3") if False else None
    c.ell(10.5, 12, 2.4, 5, "3")
    # greeble plates
    c.r(3, 13, 5, 14, "l"); c.r(11, 14, 13, 15, "L"); c.p(3, 13, "w")
    c.r(4, 17, 6, 17, "L")
    # glass pane with unfinished circuit
    c.r(6, 5, 10, 12, "d"); c.r(6, 5, 10, 5, "B")
    c.line(7, 12, 7, 8, "4"); c.line(7, 8, 9, 8, "4"); c.p(9, 7, "4"); c.p(9, 10, "5")
    c.p(8, 10, "5"); c.p(7, 6, "5")
    c.p(6, 5, "w")
    c.p(5, 5, "w"); c.p(11, 5, "w"); c.p(5, 12, "w"); c.p(11, 12, "w")
    # welded woodsprog sprigs
    c.p(12, 10, "n"); c.p(13, 9, "n"); c.p(14, 8, "g"); c.p(13, 8, "h")
    # hover jets
    c.r(5, 18, 11, 19, "L"); c.r(5, 18, 11, 18, "l")
    c.r(6, 20, 9, 20, "c"); c.r(7, 21, 8, 21, "w")
    c.p(5, 20, "B"); c.p(10, 20, "B")
    c.shadow(3, 12)
    return c.out()


def golem_bird():
    c = C()
    c.ell(9, 14, 4.8, 4.2, "2"); c.ell(8, 12.5, 3.2, 2, "1")
    c.r(3, 8, 5, 12, "2"); c.r(3, 8, 4, 12, "1")
    c.ell(4, 6.5, 2.7, 2.3, "1"); c.p(5, 8, "3")
    c.r(0, 6, 1, 7, "5"); c.p(0, 7, "4") if False else None
    c.p(2, 5, "O"); c.r(3, 5, 4, 6, "w"); c.p(3, 5, "O")        # huge eye
    c.p(5, 4, "O")                                              # small eye
    c.p(4, 3, "3"); c.p(5, 2, "3")                              # sparse tuft
    # mismatched wing: scrap plate
    c.r(10, 12, 13, 16, "l"); c.r(11, 12, 13, 12, "w"); c.r(10, 16, 13, 16, "L")
    c.p(11, 14, "4")
    c.line(13, 12, 15, 10, "L")
    # tail
    c.line(13, 13, 15, 9, "3"); c.line(13, 14, 15, 13, "2")
    # stitches
    c.line(6, 11, 9, 17, "4")
    for (x, y) in ((6, 12), (7, 14), (8, 15), (9, 17)):
        c.p(x - 1, y, "5") if False else None
        c.p(x + 1, y, "4") if (x + y) % 2 else None
    c.p(4, 10, "l"); c.p(4, 11, "w")   # neck bolt
    # mismatched legs
    c.r(7, 18, 7, 21, "L"); c.r(10, 18, 11, 21, "n")
    c.r(5, 21, 8, 21, "L"); c.r(9, 21, 12, 21, "N")
    c.shadow(2, 13)
    return c.out()


def golem_door():
    c = C()
    c.r(3, 1, 12, 21, "2")
    c.r(3, 1, 4, 21, "1"); c.r(11, 1, 12, 21, "3")
    c.r(5, 3, 10, 9, "3"); c.r(6, 4, 9, 8, "2")
    c.r(5, 12, 10, 19, "3"); c.r(6, 13, 9, 18, "2")
    # glowing peephole eye and mail slot mouth
    c.r(7, 5, 8, 6, "O"); c.p(7, 5, "4"); c.p(8, 5, "5"); c.p(7, 6, "w") if False else None
    c.r(6, 16, 9, 16, "O"); c.p(7, 16, "4")
    # rust hinges, flakes
    for y in (3, 10, 18):
        c.r(2, y, 3, y + 1, "R"); c.p(2, y, "r")
    for (x, y) in ((1, 6), (0, 13), (1, 20)):
        c.p(x, y, "r")
    # knob
    c.p(10, 11, "y"); c.p(10, 10, "w")
    # handprints
    for (x, y) in ((7, 11), (8, 11), (7, 10)):
        c.p(x, y, "1")
    c.p(11, 5, "1") if False else None
    # feet
    c.r(4, 22, 6, 22, "O"); c.r(9, 22, 11, 22, "O")
    c.r(4, 21, 6, 21, "3"); c.r(9, 21, 11, 21, "3")
    c.shadow(2, 13)
    return c.out()


def golem_hexapodel_robot():
    c = C()
    legs = [[(5, 9), (2, 8), (1, 12)], [(5, 12), (1, 13), (0, 18)], [(5, 15), (2, 17), (2, 21)]]
    for pts in legs:
        for (a, b), (e, f) in zip(pts, pts[1:]):
            c.line(a, b, e, f, "3", mirror=True)
        c.m(pts[1][0], pts[1][1], "l")
        c.m(pts[2][0], pts[2][1], "L")
    c.r(4, 8, 11, 16, "2"); c.r(4, 8, 7, 9, "1"); c.r(10, 9, 11, 16, "3")
    c.r(5, 12, 7, 15, "l"); c.r(5, 12, 7, 12, "w"); c.r(8, 11, 10, 13, "L")
    c.ell(7.5, 6, 2.8, 2.2, "1")
    c.r(7, 5, 8, 6, "O"); c.p(7, 5, "4"); c.p(8, 6, "5") if False else None
    c.line(11, 7, 13, 1, "l"); c.p(13, 0, "4")
    c.p(5, 10, "4"); c.p(10, 14, "4"); c.p(8, 15, "5")
    c.r(6, 16, 9, 18, "3")
    c.line(5, 13, 10, 10, "w") if False else None
    c.p(9, 12, "w"); c.p(9, 13, "w")                       # stitches
    c.shadow(0, 15)
    return c.out()


def golem_mopango():
    c = C()
    # tail
    tube(c, [(11, 15), (14, 17), (14, 21)], 1.2, 0.6, "3")
    # legs
    c.r(5, 17, 7, 21, "3"); c.r(9, 17, 11, 21, "2")
    c.r(4, 22, 7, 22, "O"); c.r(9, 22, 12, 22, "O")
    # hunched shelled back
    c.ell(8, 12, 5, 5.5, "2"); c.ell(9, 10, 3.5, 3.6, "1")
    c.r(9, 12, 12, 16, "3")
    for y in (8, 10, 12, 14):
        c.line(6, y, 11, y + 1, "l")
    c.p(11, 9, "w")
    # arms
    c.r(2, 12, 3, 16, "3"); c.p(2, 17, "S") if False else None
    c.p(2, 17, "w"); c.p(3, 17, "w")
    # head with mandibles
    c.ell(4.5, 7.5, 2.8, 2.4, "1")
    c.p(3, 7, "y"); c.p(5, 6, "y")
    c.p(2, 9, "w"); c.p(3, 10, "w"); c.p(6, 9, "w"); c.p(5, 10, "w")
    c.p(4, 8, "O")
    # stitches
    c.line(5, 12, 9, 15, "4"); c.p(7, 12, "4"); c.p(8, 14, "4") if False else None
    c.p(6, 15, "4"); c.p(9, 17, "4")
    c.shadow(2, 14)
    return c.out()


def golem_root():
    c = C()
    for pts in ([(6, 17), (3, 20), (2, 22)], [(8, 18), (8, 22)], [(10, 17), (13, 20), (14, 22)]):
        tube(c, pts, 1.4, 0.7, "3")
    tube(c, [(8, 18), (8, 11)], 3.2, 2.8, "2")
    tube(c, [(7, 17), (7, 12)], 1.2, 1.0, "1")
    for pts in ([(6, 11), (2, 13), (1, 18)], [(10, 11), (14, 13), (15, 18)]):
        tube(c, pts, 1.5, 0.9, "2")
    c.p(1, 19, "w"); c.p(15, 19, "w"); c.p(0, 19, "3") if False else None
    c.ell(8, 6.5, 3.4, 3.2, "2"); c.ell(7, 5.5, 1.8, 1.6, "1")
    c.p(6, 6, "w"); c.p(9, 6, "w"); c.p(6, 7, "O") if False else None
    c.r(7, 8, 8, 8, "O")
    c.line(5, 4, 3, 1, "3"); c.line(11, 4, 12, 0, "3"); c.p(2, 2, "3"); c.p(13, 2, "3")
    c.line(5, 11, 10, 16, "4")
    for (x, y) in ((6, 12), (8, 14), (9, 16)):
        c.p(x, y + 1, "5") if False else None
    c.p(7, 14, "4"); c.p(9, 12, "4") if False else None
    c.p(11, 14, "5")
    c.shadow(0, 15)
    return c.out()


def golem_tortoise():
    c = C()
    c.r(0, 15, 3, 18, "2"); c.r(12, 16, 15, 19, "L")           # mismatched: steel hind leg
    c.r(1, 19, 4, 20, "3"); c.r(12, 19, 15, 20, "l")
    c.r(5, 18, 7, 21, "3"); c.r(10, 18, 12, 21, "3")
    c.ell(2.5, 11, 2.8, 2.6, "1")
    c.r(0, 11, 1, 12, "2"); c.p(0, 12, "O")
    c.p(2, 10, "y"); c.p(3, 9, "3")
    c.p(2, 12, "w") if False else None
    c.ell(9, 13, 7, 6.5, "3")
    c.ell(9, 12.5, 6.3, 5.8, "2")
    c.r(3, 9, 9, 17, "2")
    c.ell(7, 12, 3.5, 4.5, "1")
    c.r(9, 8, 14, 17, "L") if False else None
    c.r(10, 9, 14, 13, "l"); c.r(10, 9, 14, 9, "w"); c.r(10, 13, 14, 13, "L")
    c.line(9, 7, 9, 17, "3"); c.line(3, 14, 15, 14, "3")
    for (x, y) in ((11, 10), (13, 12), (6, 9), (5, 14), (8, 16)):
        c.p(x, y, "w")
    c.line(4, 10, 9, 16, "4")
    for (x, y) in ((5, 11), (7, 13), (9, 15)):
        c.p(x + 1, y, "5") if False else None
    c.p(12, 15, "4"); c.p(6, 17, "4")
    c.shadow(0, 15)
    return c.out()


def golem_worm():
    c = C()
    sm = beads(c, [(3, 5), (9, 4), (12, 8), (8, 12), (4, 16), (9, 20)], 2.3, 1.7, ["2", "1", "L", "3"])
    # stitched seams
    for i in range(2, len(sm) - 1, 4):
        x, y, t = sm[i]
        c.p(round(x), round(y), "4"); c.p(round(x) + 1, round(y) - 1, "4")
    for i in range(4, len(sm) - 1, 6):
        x, y, t = sm[i]
        c.p(round(x), round(y) + 1, "w")
    # head: one big eye, stitched mouth
    c.ell(2.5, 5.2, 2.6, 2.6, "1")
    c.r(1, 4, 2, 5, "w"); c.p(1, 4, "O")
    c.p(4, 3, "O")
    c.r(1, 7, 4, 7, "O"); c.p(2, 6, "4"); c.p(3, 6, "4") if False else None
    c.p(2, 8, "4") if False else None
    c.p(8, 21, "3") if False else None
    c.shadow(1, 14)
    return c.out()


def lurking_beth():
    c = C()
    c.ell(8, 16, 7, 5, "3")
    c.ell(7, 14.5, 5, 3, "2")
    c.ell(6, 13, 2.5, 1.5, "1")
    # spiny mineral nodules
    for (x0, y0, x1, y1, ch) in ((3, 12, 1, 7, "1"), (6, 11, 5, 4, "2"), (9, 11, 10, 3, "1"),
                                 (12, 13, 15, 8, "2"), (2, 17, 0, 14, "2"), (14, 18, 15, 15, "1")):
        tube(c, [(x0, y0), (x1, y1)], 1.5, 0.3, ch)
    for (x, y) in ((1, 7), (5, 4), (10, 3), (15, 8)):
        c.p(x, y, "w")
    for (x, y) in ((4, 15), (9, 14), (11, 17), (6, 18), (3, 18), (8, 20)):
        c.p(x, y, "1"); c.p(x + 1, y + 1, "3")
    # watching red eyes
    c.p(6, 15, "4"); c.p(10, 15, "4"); c.p(6, 16, "5") if False else None
    c.p(7, 17, "O"); c.p(8, 17, "O")
    # holographic flicker
    for y in (13, 19):
        for x in range(2, 14, 2):
            if c.g[y][x] != ".":
                c.g[y][x] = "c"
    c.shadow(0, 15)
    return c.out()


def mopango_rider():
    c = C()
    # low chassis
    c.r(1, 14, 14, 19, "3"); c.r(1, 14, 14, 15, "2"); c.r(1, 14, 3, 15, "1")
    c.r(12, 15, 14, 18, "L") if False else None
    c.p(14, 16, "4"); c.p(15, 16, "4"); c.p(14, 17, "5")
    # pair of pristine wheels
    for cx in (4, 11):
        c.ell(cx, 19, 3.2, 3.2, "O")
        c.ell(cx, 19, 2.4, 2.4, "L")
        c.ell(cx, 19, 1.3, 1.3, "l")
        c.p(cx, 19, "w")
    # hunched glowing plated creature
    c.ell(8, 10, 3.6, 4, "2"); c.ell(7, 9, 2, 2.5, "1")
    c.mr(3, 8, 4, 10, "1")
    c.r(11, 8, 12, 10, "3")
    c.r(7, 11, 9, 11, "3")
    c.line(5, 9, 11, 9, "l") if False else None
    c.ell(8, 4.6, 2.6, 2.4, "1")
    c.r(6, 4, 9, 5, "1")
    c.p(6, 5, "4"); c.p(9, 5, "4")
    c.p(5, 6, "w"); c.p(10, 6, "w")
    c.p(5, 3, "4"); c.p(10, 3, "4"); c.p(8, 1, "4"); c.p(7, 1, "5") if False else None
    c.p(3, 5, "5"); c.p(12, 5, "5")
    c.r(7, 8, 8, 8, "4")
    c.shadow(1, 14)
    return c.out()


def natural_weapon_bite():
    return grid_from([
        "................",
        "................",
        "................",
        "................",
        "................",
        ".....222222.....",
        "...2222222222...",
        "..211222222222..",
        "..2.w.w.w.w.w2..",
        "...2.........2..",
        "....OOOOOOOOO...",
        "....OOOOOOOOO...",
        "...2.........2..",
        "..3.w.w.w.w.w3..",
        "..3333333333333.",
        "...3333333333...",
        ".....333333.....",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
    ])


def natural_weapon_hoof():
    return grid_from([
        "................",
        "................",
        "................",
        "....1.....1.....",
        "...12....12.....",
        "..122...122.....",
        "..1222.1222.....",
        "..12222.2222....",
        "..122222222.....",
        "..L2222222223...",
        "..LL22222223....",
        "..LL222.22233...",
        "..LLL22.22233...",
        "...LLL.2.2333...",
        "....LL...233....",
        "................",
        ".w..............",
        "..w.w...w.......",
        "...w..w.w.......",
        "................",
        "................",
        "................",
        "................",
        "................",
    ])


def natural_weapon_paw():
    return grid_from([
        "................",
        "................",
        "................",
        "................",
        "...w.....w......",
        "...ww....ww..w..",
        "....w.....w..w..",
        "....ww....ww.w..",
        ".....w.....w.ww.",
        ".....ww....ww.w.",
        "......w.....w...",
        "......ww..222...",
        ".......2.22222..",
        "....2.2.2222222.",
        "...222.2.222222.",
        "...2222..22222..",
        "...22222.3333...",
        "....2222333.....",
        ".....33333......",
        "................",
        "................",
        "................",
        "................",
        "................",
    ])


def natural_weapon_webbed_foot():
    return grid_from([
        "................",
        "................",
        "................",
        "................",
        "................",
        "....2....2....2.",
        "...222..222..222",
        "...2.2..2.2..2.2",
        "...2.2222.2222.2",
        "..12.2...22...22",
        "..1.2222.2222.2.",
        "..12111222222222",
        "...1222222222222",
        "...1222222222...",
        "....222222222...",
        ".....3333333....",
        "......33333.....",
        "......3333......",
        ".......33.......",
        "................",
        "................",
        "................",
        "................",
        "................",
    ])


def panhumor():
    c = C()
    c.ell(8, 15, 6.8, 5.6, "2")
    c.ell(6, 12, 3.5, 2.5, "2")
    c.ell(11, 11.5, 3, 2.2, "2")
    c.ell(7, 13.5, 4.5, 3, "1")
    c.ell(9, 18, 6, 2.5, "3")
    clear(c, 0, 21, 15, 22)
    # eroded bits: shale flakes, grit, brine, dew
    bits = [(4, 15, "L"), (6, 17, "e"), (9, 14, "w"), (11, 16, "E"), (7, 12, "c"), (5, 13, "l"),
            (10, 12, "L"), (12, 14, "e"), (8, 17, "c"), (3, 17, "E"), (9, 19, "l"), (6, 10, "w"),
            (11, 10, "e"), (8, 15, "L"), (13, 17, "w"), (5, 19, "e")]
    for (x, y, ch) in bits:
        c.p(x, y, ch)
    c.p(12, 11, "c"); c.p(7, 11, "w")
    c.p(14, 20, "c"); c.p(14, 21, "c") if False else None
    c.p(2, 19, "c"); c.p(2, 20, "c")
    c.shadow(1, 14)
    return c.out()


def reptile():
    c = C()
    tube(c, [(8, 15), (10, 19), (7, 22)], 2.0, 0.5, "2")
    for pts in ([(5, 9), (2, 9), (1, 13)], [(5, 15), (2, 15), (2, 20)]):
        for (a, b), (e, f) in zip(pts, pts[1:]):
            c.line(a, b, e, f, "3", mirror=True)
        c.m(pts[-1][0], pts[-1][1] + 1, "w")
        c.m(pts[-1][0] - 1, pts[-1][1] + 1, "w") if False else None
    c.ell(8, 11, 3.6, 5, "2"); c.ell(7, 10, 1.6, 3.5, "1")
    c.ell(8, 4.5, 2.6, 2.8, "2"); c.r(7, 2, 8, 3, "1")
    c.r(7, 1, 8, 2, "2")
    c.p(6, 4, "y"); c.p(9, 4, "y")
    c.p(7, 1, "O") if False else None
    c.line(8, 5, 8, 17, "4")
    for y in range(6, 17, 2):
        c.p(7, y, "5"); c.p(9, y, "5")
    c.p(8, 0, "R"); c.p(7, 0, "R") if False else None
    c.p(7, 0, "R"); c.p(9, 0, "R") if False else None
    c.shadow(1, 14)
    return c.out()


def root():
    c = C()
    # gnarled mass
    tube(c, [(8, 21), (8, 16)], 4.5, 3.5, "3")
    for pts in ([(5, 19), (2, 21)], [(11, 19), (14, 21)], [(8, 20), (8, 22)]):
        tube(c, pts, 1.3, 0.7, "3")
    tube(c, [(8, 20), (8, 15)], 3.2, 2.8, "2")
    tube(c, [(7, 19), (7, 15)], 1.2, 1, "1")
    # three inverted sponge spirals tasting the air
    def spiral(cx, cy, r0, rot, flip, ch):
        pts = []
        import math
        for i in range(0, 23):
            a = rot + i * 0.42 * flip
            r = r0 * (1 - i / 26)
            pts.append((cx + r * math.cos(a), cy + r * math.sin(a)))
        for (x, y) in pts:
            c.ell(x, y, 1.0, 1.0, ch)
    tube(c, [(6, 16), (4, 12), (3, 9)], 1.1, 0.9, "2")
    tube(c, [(8, 16), (8, 11), (8, 8)], 1.2, 1.0, "1")
    tube(c, [(10, 16), (12, 12), (13, 9)], 1.1, 0.9, "2")
    spiral(3.5, 6.5, 3.2, 1.5, 1, "2")
    spiral(8, 4.8, 3.6, 1.5, -1, "1")
    spiral(12.5, 6.5, 3.2, 1.5, 1, "2")
    # sponge pores
    for (x, y) in ((4, 5), (8, 3), (12, 5), (3, 8), (7, 7), (13, 8), (6, 14), (10, 15), (8, 18)):
        if c.g[y][x] != ".":
            c.g[y][x] = "3"
    # blossom at the base
    c.p(6, 18, "w"); c.p(7, 17, "w") if False else None
    c.p(10, 19, "w"); c.p(10, 18, "4"); c.p(9, 19, "4"); c.p(11, 19, "4"); c.p(10, 20, "4")
    c.shadow(1, 14)
    return c.out()


def spoken_ionic():
    c = C()
    # faceted trunk
    c.r(7, 11, 9, 21, "2"); c.r(7, 11, 7, 21, "1"); c.r(9, 11, 9, 21, "3")
    c.r(6, 20, 10, 21, "2"); c.r(4, 21, 12, 21, "3")
    c.p(7, 15, "w"); c.p(8, 18, "w") if False else None
    # geometric twigs: strict star arrangement
    for (x1, y1) in ((8, 0), (2, 3), (14, 3), (0, 9), (15, 9), (3, 13), (13, 13)):
        c.line(8, 9, x1, y1, "1" if x1 < 8 else "2")
    c.line(8, 9, 8, 0, "w")
    # glass ribbons (detail colour) hanging off the twigs
    c.line(2, 3, 1, 12, "4"); c.line(14, 3, 15, 12, "5")
    c.line(0, 9, 0, 17, "5") if False else None
    c.line(3, 13, 4, 18, "4"); c.line(13, 13, 12, 18, "5")
    c.line(8, 0, 6, 5, "4") if False else None
    # luminous star at the core
    c.r(7, 8, 9, 10, "w"); c.p(8, 7, "w"); c.p(8, 11, "w"); c.p(6, 9, "w"); c.p(10, 9, "w")
    c.p(8, 9, "w")
    for (x, y) in ((2, 3), (14, 3), (8, 0), (0, 9), (15, 9)):
        c.p(x, y, "4")
    c.shadow(3, 12)
    return c.out()


def svardym_eld():
    c = C()
    # thick legs
    c.r(4, 18, 7, 21, "3"); c.r(9, 18, 12, 21, "3"); c.r(4, 18, 5, 21, "2")
    c.r(3, 22, 7, 22, "O"); c.r(9, 22, 13, 22, "O")
    # heavy body
    c.r(3, 9, 12, 17, "2"); c.r(3, 9, 6, 17, "1"); c.r(10, 9, 12, 17, "3")
    c.mr(1, 9, 3, 12, "2"); c.m(1, 9, "1")
    c.r(11, 9, 14, 12, "3") if False else None
    # long arms, big hands, walking staff
    c.r(1, 12, 2, 18, "2"); c.r(13, 12, 14, 18, "3")
    c.r(0, 18, 3, 19, "S"); c.r(12, 18, 15, 19, "S")
    c.line(14, 6, 14, 22, "n")
    # rag wrap
    c.line(4, 10, 11, 16, "5"); c.line(4, 11, 11, 17, "4")
    # wart-brained dome head
    c.ell(8, 5.5, 4.4, 3.8, "2"); c.ell(6.5, 4, 2.5, 1.8, "1")
    for (x, y) in ((6, 2), (9, 2), (11, 4), (5, 5), (8, 3)):
        c.r(x, y, x, y, "4")
        c.p(x, y - 1, "4") if False else None
    c.p(6, 3, "4"); c.p(10, 3, "5")
    c.r(6, 6, 9, 7, "1")
    c.p(6, 6, "O"); c.p(9, 6, "O"); c.p(7, 8, "O")
    c.p(6, 5, "y") if False else None
    # wispy beard
    c.r(6, 8, 9, 9, "w"); c.p(7, 10, "w"); c.p(8, 10, "l"); c.p(9, 9, "l")
    c.shadow(0, 15)
    return c.out()


def tiny_crabs():
    c = C()

    def crab(cx, cy):
        c.ell(cx, cy, 3, 2.2, "2")
        c.r(cx - 2, cy - 1, cx, cy - 1, "1")
        c.p(cx + 2, cy + 1, "3"); c.p(cx + 1, cy + 1, "3")
        c.p(cx - 1, cy - 3, "4"); c.p(cx + 1, cy - 3, "4")
        c.p(cx - 1, cy - 2, "L"); c.p(cx + 1, cy - 2, "L")
        # claws
        c.p(cx - 4, cy - 2, "l"); c.p(cx - 5, cy - 3, "l"); c.p(cx - 3, cy - 3, "l")
        c.p(cx + 4, cy - 2, "l"); c.p(cx + 5, cy - 3, "l"); c.p(cx + 3, cy - 3, "l")
        c.p(cx - 3, cy - 1, "L"); c.p(cx + 3, cy - 1, "L")
        # legs
        c.p(cx - 4, cy + 1, "3"); c.p(cx - 4, cy + 2, "3"); c.p(cx + 4, cy + 1, "3"); c.p(cx + 4, cy + 2, "3")
        c.p(cx - 2, cy + 3, "3"); c.p(cx + 2, cy + 3, "3")
        c.p(cx, cy, "5")
    crab(4, 7)
    crab(11, 12)
    crab(5, 18)
    c.shadow(0, 15)
    return c.out()


def urnduster():
    c = C()
    # vessel on the flat top
    c.ell(8, 4.2, 2.8, 2.6, "w"); c.r(7, 1, 9, 2, "w"); c.r(7, 1, 9, 1, "l")
    c.r(5, 6, 10, 7, "L") if False else None
    c.r(6, 3, 6, 5, "w") if False else None
    c.p(6, 3, "w"); c.p(7, 4, "w") if False else None
    c.r(7, 4, 9, 4, "5")
    c.p(10, 5, "l")
    # barrel body
    c.r(3, 8, 12, 9, "L"); c.r(3, 8, 12, 8, "l")
    c.ell(8, 14, 5.2, 6, "2")
    c.r(3, 8, 12, 9, "l")
    c.r(4, 10, 6, 17, "1"); c.r(10, 11, 12, 17, "3")
    c.r(3, 11, 12, 11, "3") if False else None
    c.r(3, 12, 12, 12, "L") if False else None
    # hoops / spin belts
    c.r(3, 11, 12, 11, "L"); c.r(3, 17, 12, 17, "L")
    c.p(5, 11, "w"); c.p(5, 17, "w")
    for x in (4, 6, 8, 10):
        c.p(x, 14, "4")
    c.r(7, 13, 8, 14, "O") if False else None
    c.r(6, 15, 9, 15, "5")
    # inurnment arms folded: tongs and brush
    c.line(2, 12, 0, 16, "l"); c.p(0, 17, "w"); c.p(1, 17, "w")
    c.line(13, 12, 15, 16, "l"); c.p(15, 17, "4"); c.p(14, 17, "4")
    c.p(7, 12, "c") if False else None
    # glowing dial
    c.p(7, 12, "4"); c.p(8, 12, "4")
    # little treads
    c.r(4, 19, 6, 21, "L"); c.r(9, 19, 11, 21, "L")
    c.r(3, 21, 6, 22, "O"); c.r(9, 21, 12, 22, "O")
    c.p(4, 21, "l"); c.p(10, 21, "l")
    c.shadow(2, 13)
    return c.out()


def weep():
    c = C()
    for (cx, cy, rx, ry, ch) in ((4.5, 17, 4, 3, "2"), (11.5, 17, 4, 3, "2"), (8, 19.5, 4.5, 2.5, "3"),
                                 (3.5, 12, 3.2, 2.6, "2"), (12.5, 12, 3.2, 2.6, "1"), (8, 14, 4.5, 3.4, "1"),
                                 (8, 8.5, 3.2, 2.6, "2")):
        c.ell(cx, cy, rx, ry, ch)
    # veins
    for (x0, y0, x1, y1) in ((8, 14, 4, 17), (8, 14, 12, 17), (8, 14, 8, 8), (4, 17, 3, 12), (12, 17, 12, 12)):
        c.line(x0, y0, x1, y1, "3")
    # lobe edge accents
    for (x, y) in ((1, 12), (14, 12), (8, 6), (1, 17), (14, 17)):
        c.p(x, y, "4")
    c.p(7, 8, "1"); c.p(5, 16, "1"); c.p(11, 11, "1")
    # liquid: beaded drops and drips
    for (x, y) in ((2, 15), (13, 15), (6, 10), (10, 10), (8, 12), (5, 20), (11, 20), (8, 17)):
        c.p(x, y, "c"); c.p(x, y - 1, "w") if (x + y) % 2 else None
    c.p(3, 21, "c"); c.p(3, 22, "B")
    c.p(12, 22, "c"); c.p(8, 22, "B")
    c.shadow(0, 15)
    return c.out()


def zerojell():
    c = C()
    import random
    rnd = random.Random(7)
    c.ell(8, 14, 7.2, 6.8, "1")
    c.ell(8, 15, 5.8, 5.4, "3")
    clear(c, 0, 21, 15, 22)
    for _ in range(36):
        x, y = rnd.randint(3, 12), rnd.randint(10, 20)
        if c.g[y][x] == "3":
            c.p(x, y, rnd.choice("4455w2"))
    for (x, y) in ((4, 9), (6, 8), (9, 8), (11, 9), (3, 11)):
        c.p(x, y, "w")
    c.line(3, 11, 5, 8, "w")
    c.r(6, 8, 10, 8, "w")
    # popping particles
    for (x, y) in ((1, 6), (14, 5), (8, 4), (15, 15), (0, 17), (4, 3), (12, 2)):
        c.p(x, y, "4")
    c.p(8, 3, "w"); c.p(1, 5, "5") if False else None
    c.shadow(0, 15)
    return c.out()


SPRITES.update({
    "agolmaggot": agolmaggot(), "bear": bear(),
    "cherub_antelope_mechanical": cherub_antelope_mechanical(),
    "cherub_bird_mechanical": cherub_bird_mechanical(),
    "cherub_equine_mechanical": cherub_equine_mechanical(),
    "cherub_fungus_mechanical": cherub_fungus_mechanical(),
    "cherub_newly_sentient_being_mechanical": cherub_newly_sentient_being_mechanical(),
    "cherub_root_mechanical": cherub_root_mechanical(),
    "cherub_tree_mechanical": cherub_tree_mechanical(),
    "cherub_worm_mechanical": cherub_worm_mechanical(),
    "dagasha": dagasha(), "entropic_being": entropic_being(), "girshling": girshling(),
    "godhed2_unplanished": godhed2_unplanished(),
    "golem_bird": golem_bird(), "golem_door": golem_door(),
    "golem_hexapodel_robot": golem_hexapodel_robot(), "golem_mopango": golem_mopango(),
    "golem_root": golem_root(), "golem_tortoise": golem_tortoise(), "golem_worm": golem_worm(),
    "lurking_beth": lurking_beth(), "mopango_rider": mopango_rider(),
    "natural_weapon_bite": natural_weapon_bite(), "natural_weapon_hoof": natural_weapon_hoof(),
    "natural_weapon_paw": natural_weapon_paw(), "natural_weapon_webbed_foot": natural_weapon_webbed_foot(),
    "panhumor": panhumor(), "reptile": reptile(), "root": root(), "spoken_ionic": spoken_ionic(),
    "svardym_eld": svardym_eld(), "tiny_crabs": tiny_crabs(), "urnduster": urnduster(),
    "weep": weep(), "zerojell": zerojell(),
})

# KEYS defined above
