"""B3 remaining creatures, batch 6."""
from functools import partial
import b3kit as K
from b3kit import (C, back, overlay, person, hat_wide, hat_straw, hat_pointy, cap, hood, turban, helmet,
                   crown, halo, hair_short, hair_long, hair_wild, hair_mohawk, hair_bun, beard, stubble,
                   goggles_up, veil, blindfold, scarf, apron, armor, tunic, cape, pack, staff, club,
                   hoe, sickle, jug, wrench, gear, lantern, sword)
import b3_people as BP
from b3_wilds import tube
from b3more_keys import MORE_KEYS

KEYS = MORE_KEYS[6]
P = person
SPRITES = {}
HUMANOID = set()


def hum(name, *a, **k):
    SPRITES[name] = person(*a, **k)
    HUMANOID.add(name)


# ============================================================ humanoid parts
def cleaver(c):
    c.line(13, 8, 13, 17, "n")
    c.r(12, 4, 15, 8, "l"); c.r(12, 4, 15, 4, "w"); c.r(15, 5, 15, 8, "L"); c.p(13, 6, "O")
    c.p(12, 15, "s"); c.p(11, 15, "S")


def fur_mane(c, a="N", b="n"):
    c.r(4, 2, 11, 3, a); c.r(3, 4, 3, 6, a); c.r(12, 4, 12, 6, a)
    c.p(5, 1, a); c.p(10, 1, a); c.p(7, 1, b); c.p(3, 3, b)


def chrome_arm(c):
    c.r(11, 10, 12, 14, "l"); c.r(12, 10, 12, 14, "L"); c.p(11, 10, "w")
    c.r(11, 15, 13, 16, "L"); c.p(13, 16, "4"); c.p(12, 16, "4")


def eye_lamp(c, col="4"):
    c.p(6, 5, col); c.p(9, 5, col)
    c.p(6, 4, col) if False else None


def baboon_head(c):
    """stony baboon head: dropped muzzle with wet nostrils, heavy brow."""
    c.r(5, 2, 10, 3, "2"); c.r(4, 3, 4, 5, "3"); c.r(11, 3, 11, 5, "3")
    c.r(5, 3, 10, 3, "3")
    c.r(5, 4, 10, 6, "2"); c.r(10, 4, 10, 7, "3")
    c.r(5, 2, 7, 2, "1")
    c.p(6, 4, "O"); c.p(9, 4, "O"); c.p(6, 5, "y"); c.p(9, 5, "y")     # eyes under brow
    c.r(6, 6, 9, 8, "5"); c.r(6, 6, 9, 6, "4")                          # red muzzle
    c.p(6, 7, "O"); c.p(9, 7, "O")                                       # nostrils
    c.r(7, 8, 8, 8, "O")
    c.p(4, 5, "1"); c.p(11, 5, "3")


def snap_head(c):
    """hyena head in profile facing left, ears up."""
    c.r(6, 0, 6, 2, "3"); c.r(9, 0, 9, 2, "3"); c.p(6, 0, "1")
    c.r(6, 3, 10, 3, "2")
    c.r(5, 3, 10, 6, "2"); c.r(10, 3, 10, 7, "3")
    c.r(1, 5, 5, 6, "1")
    c.r(1, 7, 5, 7, "6")                       # open jaw
    c.r(0, 5, 0, 6, "O")                        # nose
    c.p(2, 7, "w"); c.p(4, 7, "w"); c.p(1, 6, "w"); c.p(3, 6, "w") if False else None
    c.p(6, 4, "y"); c.p(7, 4, "O")
    c.r(6, 7, 9, 8, "2"); c.r(8, 7, 9, 8, "3")
    c.r(8, 1, 10, 3, "3"); c.p(10, 2, "1")      # mane tuft
    c.r(5, 8, 5, 9, "5") if False else None
    c.p(7, 3, "1")


def snap_fur(c):
    for (x, y) in ((4, 9), (3, 10), (11, 9), (12, 10), (3, 12), (12, 12), (4, 14), (11, 14), (6, 9), (9, 9)):
        c.p(x, y, "1" if x < 8 else "3")


def hunch(c):
    c.r(3, 9, 12, 10, "2"); c.r(3, 9, 4, 10, "1"); c.r(11, 9, 12, 10, "3")


def jaw_big(c, a="1"):
    """overly jawed face with pale, hanging lips."""
    c.r(5, 6, 10, 8, "s")
    c.r(4, 7, 11, 9, "w") if False else None
    c.r(5, 7, 10, 9, a)
    c.r(6, 8, 9, 8, "w"); c.r(6, 9, 9, 9, "w")       # white lips
    c.p(5, 9, "S"); c.p(10, 9, "S")
    c.p(7, 9, "O") if False else None
    c.r(6, 7, 9, 7, "S"); c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 4, 9, 4, "S") if False else None


def leaf_crown(c, a="g", b="G", core="y"):
    """leaves that camber toward a glowing core above the head."""
    c.p(7, 0, core); c.p(8, 0, core); c.r(7, 1, 8, 1, "w")
    c.line(5, 3, 2, 0, a); c.line(6, 2, 4, 0, b); c.line(10, 3, 13, 0, a); c.line(9, 2, 11, 0, b)
    c.r(5, 3, 10, 3, a); c.r(6, 2, 9, 2, b)
    c.p(7, 2, "h"); c.p(8, 2, "h")
    c.p(6, 1, b); c.p(9, 1, b)


def core_bulb(c):
    """verdurous glowing core in the chest."""
    c.r(6, 11, 9, 14, "G"); c.r(7, 11, 8, 14, "y"); c.r(7, 12, 8, 13, "w")
    c.p(5, 12, "g"); c.p(10, 12, "g"); c.line(5, 10, 3, 8, "g"); c.line(10, 10, 12, 8, "g")


def scrap_habit(c):
    """habit of trash plates and rust flakes."""
    c.r(5, 9, 10, 15, "2")
    for (x, y, ch) in ((5, 10, "4"), (6, 11, "5"), (8, 10, "5"), (9, 12, "4"), (6, 14, "5"), (9, 15, "4"),
                       (7, 13, "6"), (4, 17, "5"), (7, 18, "4"), (10, 17, "5"), (5, 20, "4"), (10, 20, "5"),
                       (8, 19, "6"), (3, 19, "5"), (11, 19, "4")):
        c.r(x, y, x + 1, y, ch)
    c.r(4, 21, 11, 21, "6")


def prayer_beads(c, a="4"):
    for (x, y) in ((6, 9), (5, 10), (5, 11), (6, 12), (9, 9), (10, 10), (10, 11), (9, 12)):
        c.p(x, y, a)
    c.p(7, 13, "y"); c.p(8, 13, "y")


def fat_belly(c, a="2", hi="1", dk="3"):
    c.r(3, 11, 12, 18, a); c.r(3, 11, 5, 17, hi); c.r(10, 11, 12, 18, dk); c.r(3, 18, 12, 18, dk)
    c.r(4, 10, 11, 10, a)


def metal_fat(c):
    """strange metallic fat: chrome rolls over the torso."""
    c.r(2, 9, 13, 17, "2"); c.r(2, 9, 5, 16, "1"); c.r(10, 9, 13, 17, "3")
    for y in (11, 14, 17):
        c.r(2, y, 13, y, "3")
    c.r(3, 10, 6, 10, "l"); c.r(4, 13, 7, 13, "l"); c.r(3, 16, 6, 16, "l")
    c.r(9, 12, 12, 12, "L"); c.r(9, 15, 12, 15, "L")
    c.p(5, 10, "w"); c.p(5, 13, "w")
    c.mr(1, 12, 1, 15, "2"); c.m(1, 16, "S")


def palanquin(c):
    """seat poles + canopy behind the baron."""
    c.r(0, 9, 0, 22, "n"); c.r(15, 9, 15, 22, "N")
    c.r(0, 8, 15, 8, "4"); c.r(1, 7, 14, 7, "5"); c.r(2, 6, 13, 6, "4")
    c.line(2, 8, 2, 11, "5") if False else None
    for x in (2, 5, 8, 11, 13):
        c.p(x, 9, "6")
    c.r(1, 16, 14, 17, "N")


def walker_legs(c):
    """the palanquin walker's long legs beneath the robe."""
    c.r(3, 19, 12, 21, ".")
    c.r(3, 19, 12, 20, "2"); c.r(3, 19, 5, 20, "1"); c.r(10, 19, 12, 20, "3")
    c.r(2, 21, 2, 22, "n"); c.r(13, 21, 13, 22, "N"); c.r(5, 21, 5, 22, "n"); c.r(10, 21, 10, 22, "N")
    c.r(1, 22, 3, 22, "O"); c.r(12, 22, 14, 22, "O"); c.r(4, 22, 6, 22, "O"); c.r(9, 22, 11, 22, "O")


def big_hat_gem(c):
    turban(c, "4", "5", "y")


def thawb(c):
    """white fringed thawb, embroidered border in the detail colour; hem fringe."""
    c.r(5, 9, 10, 9, "4")
    for y in (12, 15, 18):
        c.r(5 if y < 16 else 4, y, 10 if y < 16 else 11, y, "4")
    for x in (3, 5, 7, 9, 11):
        c.p(x, 21, "5")
    c.p(7, 16, "5"); c.p(8, 16, "6"); c.p(7, 19, "5"); c.p(6, 13, "5")


def neckdress(c):
    c.r(5, 8, 10, 9, "4"); c.r(6, 10, 9, 10, "5"); c.p(7, 11, "4"); c.p(8, 11, "6")


def head_cloth(c, a="2", b="1", band="4"):
    """white head cloth with red agal band."""
    c.r(6, 1, 9, 1, a); c.r(5, 2, 10, 2, a); c.r(4, 3, 11, 3, a)
    c.r(4, 4, 4, 8, a); c.r(11, 4, 11, 8, "3")
    c.r(5, 2, 10, 2, a); c.r(5, 3, 10, 3, band); c.p(6, 1, b)
    c.r(4, 8, 5, 9, a)


def bloody_apron(c):
    c.r(6, 11, 9, 20, "2"); c.r(6, 11, 6, 20, "1"); c.r(9, 11, 9, 20, "3")
    for (x, y, ch) in ((7, 12, "4"), (8, 13, "5"), (6, 15, "5"), (9, 16, "4"), (7, 18, "5"), (8, 19, "6")):
        c.p(x, y, ch)
    c.p(5, 10, "6"); c.p(10, 10, "6"); c.p(6, 10, "6"); c.p(9, 10, "6")


def goggles_orb(c, glass="4"):
    """big orbed goggles smeared with blood."""
    c.r(4, 4, 11, 4, "L")
    c.r(4, 5, 7, 6, "l"); c.r(8, 5, 11, 6, "l")
    c.r(5, 5, 6, 6, glass); c.r(9, 5, 10, 6, glass)
    c.p(5, 5, "w"); c.p(9, 5, "w"); c.p(6, 6, "O") if False else None
    c.p(8, 5, "L"); c.p(7, 5, "L")
    c.p(6, 6, "5"); c.p(10, 6, "6")


def gut_tray(c):
    c.r(0, 14, 4, 17, "l"); c.r(0, 17, 4, 17, "L")
    c.p(1, 15, "R"); c.p(2, 14, "r"); c.p(3, 15, "R"); c.p(2, 16, "r"); c.p(4, 15, "s")


def robe_loose(c, a="2"):
    c.r(2, 11, 3, 20, a); c.r(12, 11, 13, 20, "3")


def hood_deep(c, a="2", lite="1", dark="3"):
    hood(c, a, lite, dark)
    c.r(5, 3, 10, 3, a); c.r(5, 4, 10, 4, dark) if False else None


def hum_all():
    hum("cannibal", hair_short, BP.bone_necklace, BP.bare_chest, tunic, BP.fangs, BP.bone_club,
        face="face", sash=False)
    hum("cherub_cannibal_mechanical", BP.cylinder_head, BP.chrome_joints, BP.bare_chest if False else chrome_arm,
        halo, BP.pistons, face="none", sash=False)
    hum("farmer", hat_straw, tunic, hoe, face="face", sash=False)
    hum("golem_baboon", BP.bare_chest, baboon_head, BP.fingers, tunic, face="none", sash=False)
    hum("golem_snapjaw", snap_fur, hunch, snap_head, BP.club if False else club, tunic, face="none", sash=False)
    hum("issachari", head_cloth, thawb, neckdress, staff, face="face", sash=False)
    hum("merchant_tech", bloody_apron, goggles_orb, gut_tray, face="none", sash=False)
    hum("newfather", hood, jaw_big, face="none", trim="4")
    hum("sightless_master", metal_fat, blindfold, halo, face="face", trim="4", sash=False)
    hum("slynth_mopango", leaf_crown, core_bulb, face="face", sash=False)
    hum("trash_monk", hood, scrap_habit, prayer_beads, staff, face="face", sash=False)
    hum("water_baron", palanquin, walker_legs, fat_belly, turban, jug, face="face", sash=False)


hum_all()


# ============================================================ free-form helpers
def poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            px, py = x + 0.5, y + 0.5
            ins = False
            j = n - 1
            for i in range(n):
                xi, yi = pts[i]
                xj, yj = pts[j]
                if (yi > py) != (yj > py) and px < (xj - xi) * (py - yi) / (yj - yi) + xi:
                    ins = not ins
                j = i
            if ins:
                c.p(x, y, ch)


def done(c, x0=0, x1=15):
    c.shadow(x0, x1)
    return c.out()


def feet(c, xs, y=22, w=2):
    for x in xs:
        c.r(x, y, x + w - 1, y, "O")


def S(name):
    def deco(fn):
        SPRITES[name] = fn()
        return fn
    return deco


# ---------------------------------------------------------------- gelatin prismatoids
@S("antiprism")
def _():
    c = C()
    # square antiprism: top square turned against the bottom one, triangle facets between
    poly(c, [(8, 3), (13, 6), (14, 11), (12, 17), (8, 20), (3, 17), (1, 11), (3, 6)], "2")
    poly(c, [(8, 3), (13, 6), (8, 9), (3, 6)], "1")                       # top face
    poly(c, [(3, 6), (8, 9), (6, 14), (1, 11)], "2")
    poly(c, [(8, 9), (13, 6), (14, 11), (10, 14)], "3")
    poly(c, [(1, 11), (6, 14), (3, 17)], "3")
    poly(c, [(6, 14), (10, 14), (8, 20), (3, 17)], "2")
    poly(c, [(10, 14), (14, 11), (12, 17), (8, 20)], "3")
    c.r(6, 5, 9, 5, "w"); c.p(5, 6, "w")
    # facet edges + digested bits
    c.line(8, 9, 6, 14, "6"); c.line(8, 9, 10, 14, "6"); c.line(6, 14, 10, 14, "6")
    c.line(3, 6, 8, 9, "6") if False else None
    c.r(7, 11, 8, 12, "5"); c.p(7, 11, "4"); c.p(5, 12, "4"); c.p(11, 12, "5"); c.p(9, 16, "4")
    c.p(7, 15, "O"); c.p(9, 15, "O"); c.p(2, 9, "4") if False else None
    c.r(5, 21, 11, 21, "3")
    return done(c, 1, 14)


@S("frustum")
def _():
    c = C()
    # truncated pyramid: narrow flat top, flaring base, wobbling slumped
    poly(c, [(5, 6), (11, 6), (14, 20), (1, 20)], "2")
    poly(c, [(5, 6), (11, 6), (11, 9), (5, 9)], "1")                      # top face
    poly(c, [(5, 9), (11, 9), (14, 20), (1, 20)], "2")
    poly(c, [(5, 9), (5, 9), (1, 20), (3, 20)], "1")
    poly(c, [(11, 9), (13, 20), (14, 20), (12, 9)], "3")
    c.r(1, 20, 14, 21, "3"); c.r(2, 21, 13, 21, "6")
    c.r(5, 6, 11, 6, "w"); c.p(6, 7, "w")
    c.r(6, 12, 9, 15, "5"); c.r(7, 12, 8, 13, "4")                        # glowing gut
    c.p(5, 17, "4"); c.p(11, 16, "4"); c.p(9, 18, "5"); c.p(4, 14, "5") if False else None
    c.p(6, 8, "O"); c.p(9, 8, "O")
    c.p(2, 18, "w") if False else None
    c.line(5, 9, 11, 9, "3")
    return done(c, 0, 15)


# ---------------------------------------------------------------- bug
@S("bug")
def _():
    c = C()
    # angled glass shell
    for sx in (0, 1):
        f = (lambda x: 15 - x) if sx else (lambda x: x)
        for (x, y, ch) in ((1, 10, "3"), (0, 14, "3"), (1, 17, "3"), (1, 8, "3"), (2, 19, "3")):
            pass
    c.line(3, 11, 0, 13, "3", mirror=True); c.line(3, 14, 0, 17, "3", mirror=True)
    c.line(3, 17, 1, 21, "3", mirror=True); c.line(0, 13, 0, 17, "3", mirror=True) if False else None
    c.ell(8, 6, 2.6, 2.2, "3")
    c.m(6, 4, "3"); c.m(5, 2, "3"); c.m(5, 1, "3"); c.m(4, 0, "y")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.ell(8, 14, 5, 7, "L")
    poly(c, [(8, 7), (13, 10), (13, 19), (8, 22), (3, 19), (3, 10)], "2")
    poly(c, [(8, 7), (3, 10), (3, 19), (8, 14)], "1")                      # light shard
    poly(c, [(8, 7), (13, 10), (13, 19), (8, 14)], "3")                    # dark shard
    poly(c, [(8, 14), (3, 19), (8, 22)], "2")
    poly(c, [(8, 14), (13, 19), (8, 22)], "1")
    c.line(8, 7, 8, 22, "O")
    c.p(5, 10, "w"); c.p(4, 12, "w"); c.p(6, 11, "w"); c.p(10, 17, "w"); c.p(11, 15, "4"); c.p(5, 18, "4")
    c.p(10, 9, "4") if False else None
    return done(c, 2, 13)


# ---------------------------------------------------------------- cherubs: plump infant chimeras
def cherub_dress(c, wy=5):
    """halo + tiny feathered wings."""
    c.r(6, 0, 9, 0, "y"); c.p(5, 1, "y"); c.p(10, 1, "y"); c.p(6, 1, "4") if False else None
    for sx in (0, 1):
        for (x, y) in ((2, wy), (1, wy + 1), (2, wy + 1), (0, wy + 2), (1, wy + 2), (2, wy + 2), (1, wy + 3),
                       (2, wy + 3), (3, wy + 3)):
            c.p(15 - x if sx else x, y, "w")
        c.p(15 - 0 if sx else 0, wy + 2, "L")
        c.p(15 - 1 if sx else 1, wy + 3, "L")


@S("cherub_bear")
def _():
    c = C()
    c.ell(8, 16, 6, 4.6, "2"); c.ell(8, 15, 4.5, 3, "1")
    c.r(3, 19, 5, 21, "2"); c.r(10, 19, 12, 21, "3"); feet(c, (3, 10), 22, 3)
    c.ell(8, 9, 4.2, 3.6, "2"); c.m(4, 5, "2"); c.m(5, 5, "2"); c.m(4, 4, "w") if False else None
    c.m(4, 6, "1")
    c.r(6, 9, 9, 11, "1"); c.p(7, 10, "O"); c.p(8, 10, "O"); c.p(7, 9, "O") if False else None
    c.p(6, 7, "O"); c.p(9, 7, "O")
    c.p(5, 9, "4"); c.p(10, 9, "4")                    # rosy cheeks
    c.p(8, 12, "4") if False else None
    c.r(6, 2, 9, 2, "y"); c.p(5, 3, "y"); c.p(10, 3, "y")
    c.r(7, 13, 8, 14, "w")
    for sx in (0, 1):
        for (x, y) in ((2, 11), (1, 12), (2, 12), (1, 13), (0, 13), (2, 13)):
            c.p(15 - x if sx else x, y, "w")
        c.p(15 if sx else 0, 14, "L"); c.p(14 if sx else 1, 14, "L")
    return done(c)


@S("cherub_dog")
def _():
    c = C()
    c.ell(7, 16, 5.5, 3.6, "2"); c.ell(7, 15, 4, 2.2, "1")
    c.r(3, 18, 4, 21, "2"); c.r(9, 18, 10, 21, "3"); c.r(2, 18, 2, 19, "1") if False else None
    feet(c, (3, 9), 22, 2)
    tube(c, [(12, 15), (14, 13), (14, 11)], 1.1, 0.8, "1")
    c.ell(7, 9, 3.6, 3, "2")
    c.r(2, 9, 6, 11, "1"); c.r(1, 10, 2, 11, "O"); c.p(1, 10, "O")
    c.p(4, 8, "O"); c.p(8, 8, "O")
    c.r(9, 6, 11, 11, "3"); c.r(10, 7, 11, 10, "2") if False else None   # floppy ear
    c.r(3, 6, 4, 8, "3")
    c.r(2, 11, 4, 12, "4"); c.p(3, 12, "R")
    c.r(5, 2, 9, 2, "y"); c.p(4, 3, "y"); c.p(10, 3, "y")
    c.line(4, 12, 5, 14, "4") if False else None
    for (x, y) in ((11, 11), (13, 12), (12, 10)):
        c.p(x, y, "w")
    c.r(11, 12, 13, 13, "w"); c.p(12, 12, "L"); c.p(14, 12, "w")
    c.r(10, 10, 14, 11, "w") if False else None
    c.r(12, 9, 14, 11, "w"); c.p(13, 10, "L")
    return done(c)


@S("cherub_frog")
def _():
    c = C()
    c.r(1, 17, 4, 21, "3"); c.r(11, 17, 14, 21, "3")
    c.ell(8, 15, 6, 4.5, "2"); c.ell(8, 14, 4.5, 3, "1")
    c.r(0, 21, 4, 21, "2"); c.r(11, 21, 15, 21, "2"); feet(c, (0, 12), 22, 4)
    c.ell(8, 9, 5, 3, "2")
    c.r(3, 5, 5, 7, "1"); c.r(10, 5, 12, 7, "1"); c.p(4, 6, "O"); c.p(11, 6, "O"); c.p(4, 5, "w"); c.p(11, 5, "w")
    c.r(4, 10, 11, 10, "O"); c.p(3, 9, "O"); c.p(12, 9, "O")
    c.r(6, 8, 9, 8, "4") if False else None
    c.p(6, 8, "O"); c.p(9, 8, "O")
    c.r(7, 12, 8, 14, "w")
    c.r(6, 1, 9, 1, "y"); c.p(5, 2, "y"); c.p(10, 2, "y")
    c.r(2, 12, 3, 14, "w"); c.r(12, 12, 13, 14, "w")
    c.p(2, 15, "L"); c.p(13, 15, "L")
    return done(c)


@S("cherub_mollusk")
def _():
    c = C()
    # snail-ish slug with hands and a baby face, shell on back
    c.ell(6, 17, 6.5, 3.8, "2"); c.r(0, 20, 13, 21, "3"); c.ell(6, 16.5, 5, 2.6, "1")
    c.ell(9, 13, 4.5, 4.5, "w"); c.ell(9, 13, 3.4, 3.4, "L"); c.ell(9, 13, 2.2, 2.2, "w"); c.p(9, 13, "L")
    c.ell(12, 14, 3, 5, "w") if False else None
    c.ell(3, 12, 2.8, 3.8, "2"); c.r(1, 10, 4, 14, "2"); c.r(2, 10, 3, 14, "1")
    c.p(2, 10, "O"); c.p(4, 10, "O"); c.r(2, 12, 3, 12, "4"); c.p(1, 9, "w") if False else None
    c.p(1, 7, "L"); c.p(1, 8, "w"); c.p(5, 7, "L"); c.p(5, 8, "w")                  # eyestalks
    c.r(1, 7, 1, 9, "2"); c.r(5, 7, 5, 9, "2"); c.p(1, 7, "O"); c.p(5, 7, "O")
    c.r(1, 3, 4, 3, "y"); c.p(0, 4, "y"); c.p(5, 4, "y")
    c.r(0, 16, 2, 17, "s"); c.p(0, 15, "s")
    c.r(12, 17, 14, 19, "3") if False else None
    c.line(9, 8, 11, 6, "w") if False else None
    return done(c, 0, 14)


@S("cherub_robot")
def _():
    c = C()
    c.r(2, 17, 13, 22, "L"); c.r(2, 17, 13, 18, "l")
    for x in range(2, 14, 2):
        c.p(x, 20, "O"); c.p(x + 1, 21, "O")
    c.r(2, 19, 13, 19, "L") if False else None
    c.r(4, 10, 11, 17, "2"); c.r(4, 10, 6, 17, "1"); c.r(10, 10, 11, 17, "3")
    c.r(7, 12, 8, 14, "y"); c.p(7, 12, "w")
    c.r(1, 11, 3, 13, "l"); c.r(12, 11, 14, 13, "L"); c.r(1, 14, 1, 15, "L"); c.r(14, 14, 14, 15, "L")
    c.ell(8, 7, 4, 3.2, "w"); c.ell(8, 7.5, 3.6, 2.6, "l")
    c.r(5, 7, 10, 7, "O"); c.p(6, 7, "y"); c.p(9, 7, "y"); c.p(6, 6, "y") if False else None
    c.p(8, 3, "L"); c.p(8, 2, "L")
    c.r(6, 0, 9, 0, "y"); c.p(5, 1, "y"); c.p(10, 1, "y")
    c.r(3, 9, 12, 9, "L") if False else None
    c.shadow(1, 14)
    return c.out()


@S("cherub_tortoise")
def _():
    c = C()
    c.r(0, 15, 3, 18, "2"); c.r(12, 16, 15, 19, "3")
    c.r(1, 19, 4, 21, "2"); c.r(11, 19, 14, 21, "3"); feet(c, (1, 11), 22, 4)
    c.ell(2.5, 11, 3, 3, "2"); c.r(0, 11, 2, 13, "1"); c.p(1, 10, "O"); c.p(3, 10, "O"); c.r(1, 12, 2, 12, "4")
    c.ell(9, 14, 6.5, 5, "w"); c.ell(9, 13.5, 5.5, 4, "1"); c.ell(9, 13, 3.5, 2.6, "2")
    c.line(9, 9, 9, 18, "L"); c.line(4, 13, 14, 13, "L")
    c.r(8, 6, 11, 6, "y") if False else None
    c.r(1, 4, 4, 4, "y"); c.p(0, 5, "y"); c.p(5, 5, "y")
    for (x, y) in ((6, 11), (12, 11), (6, 16), (12, 16)):
        c.p(x, y, "w")
    c.m(3, 9, "w") if False else None
    c.r(8, 8, 10, 8, "w") if False else None
    return done(c)


@S("cherub_winged_mammal")
def _():
    c = C()
    # bat-baby: round furry body, huge membrane wings spread
    for sx in (0, 1):
        def P(x, y, ch, sx=sx):
            c.p(15 - x if sx else x, y, ch)
        for (x0, x1, y) in ((0, 4, 6), (0, 5, 7), (0, 5, 8), (0, 6, 9), (1, 6, 10), (1, 6, 11), (2, 6, 12),
                            (3, 6, 13), (4, 6, 14)):
            for x in range(x0, x1 + 1):
                P(x, y, "2" if x > x0 + 1 else "3")
        for y in range(6, 15):
            P(0 if y < 9 else y - 9, y, "w") if False else None
        P(0, 6, "w"); P(0, 4, "w"); P(1, 5, "w"); P(2, 6, "w") if False else None
        for x, y in ((0, 5), (1, 4), (2, 4), (3, 5)):
            P(x, y, "w")
        c.line(0, 6, 5, 12, "L") if False else None
    c.line(5, 11, 1, 8, "L", mirror=True); c.line(5, 12, 1, 12, "L", mirror=True)
    c.ell(8, 15, 3.8, 5, "2"); c.ell(8, 15, 2.5, 3.5, "1")
    c.r(6, 20, 7, 21, "3"); c.r(8, 20, 9, 21, "3"); feet(c, (6, 8), 22, 2)
    c.ell(8, 8, 3.2, 2.8, "2")
    c.r(5, 3, 5, 5, "3"); c.r(10, 3, 10, 5, "3"); c.p(5, 3, "1"); c.p(10, 3, "1")
    c.p(6, 8, "O"); c.p(9, 8, "O"); c.r(7, 10, 8, 10, "w") if False else None
    c.p(7, 10, "w"); c.p(8, 10, "w"); c.r(6, 9, 9, 9, "1")
    c.p(6, 8, "O"); c.p(9, 8, "O")
    c.r(6, 1, 9, 1, "y"); c.p(5, 2, "y"); c.p(10, 2, "y")
    return done(c)


# ---------------------------------------------------------------- crab, mollusk
@S("crab")
def _():
    c = C()
    # hovering crab (no legs on the ground), scissor claws snipping grass
    c.ell(8, 14, 5, 3.4, "2"); c.ell(8, 13, 3.6, 2, "1"); c.r(4, 16, 11, 16, "3")
    c.m(6, 10, "3"); c.m(6, 9, "3"); c.p(6, 8, "O"); c.p(9, 8, "O"); c.p(6, 7, "w"); c.p(9, 7, "w")
    for sx in (0, 1):
        def P(x, y, ch, sx=sx):
            c.p(15 - x if sx else x, y, ch)
        for (x, y) in ((3, 13), (2, 12), (2, 11), (1, 10)):
            P(x, y, "3")
        # scissor claw: two blades
        c.line(1, 9, 0, 3, "1") if False else None
        for (x, y) in ((0, 9), (1, 9), (2, 9), (0, 8), (1, 8), (2, 8), (0, 7), (1, 7), (2, 7)):
            P(x, y, "2")
        for (x, y) in ((0, 6), (0, 5), (0, 4), (0, 3), (1, 6), (1, 5), (1, 4)):
            P(x, y, "1")
        for (x, y) in ((3, 6), (3, 5), (4, 4), (4, 3), (3, 7)):
            P(x, y, "1")
        P(2, 4, "3") if False else None
        P(0, 2, "w"); P(4, 2, "w")
        P(1, 3, "O") if False else None
        P(2, 7, "3"); P(2, 6, "O"); P(2, 5, "O")
    for i, y in enumerate((17, 18, 19)):
        c.line(4, y, 1, y + 1, "3", mirror=True)
    c.r(3, 20, 12, 20, "x") if False else None
    # grass blades
    for x, y in ((6, 19), (9, 20), (3, 21), (12, 21)):
        c.p(x, y, "g")
    c.p(7, 1, "g"); c.p(8, 0, "g"); c.p(8, 1, "h")
    return done(c)


@S("mollusk")
def _():
    c = C()
    # open bivalve shell with a hatchet of fleshy tissue
    c.ell(8, 8, 7, 5.5, "3"); c.r(0, 9, 15, 13, "."); c.r(1, 9, 14, 9, "3")
    c.ell(8, 8.5, 6, 4.5, "2")
    for x in (2, 4, 6, 8, 10, 12):
        c.line(8, 12, x, 5, "3") if False else None
    for x in (2, 4, 6, 9, 11, 13):
        c.line(x, 9, x if x < 8 else x, 4, "3")
    c.r(4, 9, 11, 9, "1") if False else None
    c.ell(8, 18, 7, 4, "3"); c.ell(8, 17.5, 6.2, 3.2, "2"); c.r(2, 17, 13, 17, "1")
    for x in (2, 4, 6, 9, 11, 13):
        c.line(x, 15, x, 20, "3")
    c.r(1, 21, 14, 21, "3")
    # hatchet of tissue
    c.r(5, 10, 10, 14, "5"); c.r(6, 9, 9, 9, "5"); c.r(4, 12, 11, 14, "5")
    c.r(5, 10, 7, 12, "4"); c.r(9, 12, 10, 14, "6")
    c.r(3, 12, 3, 13, "5"); c.r(12, 12, 12, 13, "6")
    c.p(7, 11, "O"); c.p(9, 11, "O"); c.p(6, 10, "w") if False else None
    # machine scrape marks
    c.line(3, 4, 6, 6, "l"); c.line(11, 3, 12, 6, "L"); c.p(10, 6, "l")
    c.p(8, 6, "w"); c.p(5, 3, "w") if False else None
    return done(c)


# ---------------------------------------------------------------- drillbot
@S("drillbot")
def _():
    c = C()
    # four-legged plate body, spinning burls on back, antennae, drills on arm stumps
    c.ell(8, 14, 5.6, 4.2, "2"); c.ell(8, 13, 4.4, 2.6, "1"); c.r(3, 17, 12, 17, "3")
    for (x, y) in ((6, 12), (10, 13), (8, 15)):
        c.ell(x, y, 1.5, 1.5, "l"); c.p(x, y, "O"); c.p(x - 1, y - 1, "w")
    c.line(8, 10, 7, 4, "w"); c.line(9, 10, 11, 4, "w"); c.p(7, 4, "y"); c.p(11, 4, "y")
    c.r(7, 9, 9, 10, "3")
    # drill arms
    for sx in (0, 1):
        def P(x, y, ch, sx=sx):
            c.p(15 - x if sx else x, y, ch)
        for (x, y) in ((3, 12), (2, 11), (2, 12), (3, 13)):
            P(x, y, "L")
        for (x, y, ch) in ((1, 9, "4"), (2, 9, "5"), (1, 8, "4"), (0, 10, "5"), (1, 10, "4"), (2, 10, "5"),
                           (1, 7, "5"), (1, 6, "4"), (0, 8, "6"), (2, 8, "6")):
            P(x, y, ch)
        P(1, 11, "4")
    c.r(1, 13, 2, 18, "L") if False else None
    for x in (3, 5, 10, 12):
        c.r(x, 18, x, 21, "L" if x < 8 else "l")
    feet(c, (2, 4, 9, 11), 22, 2)
    c.p(7, 8, "R") if False else None
    c.p(7, 12, "y") if False else None
    return done(c, 1, 14)


# ---------------------------------------------------------------- goathorn
@S("goathorn")
def _():
    c = C()
    # big curling horn, wind-etched, gilded rim and band, scarlet tassels
    pts = [(12, 3), (9, 6), (7, 10), (7, 14), (9, 18), (12, 19)]
    tube(c, [(11, 5), (8, 8), (6, 12), (6, 16), (8, 19)], 3.0, 1.2, "w")
    tube(c, [(11, 5), (8, 8), (6, 12), (6, 15)], 1.4, 0.9, "t")
    c.line(4, 12, 4, 15, "L") if False else None
    c.ell(12, 3, 2.6, 2.6, "y"); c.ell(12, 3, 1.4, 1.4, "O"); c.p(11, 2, "y")
    c.r(5, 12, 9, 12, "y"); c.r(4, 14, 8, 14, "y") if False else None
    c.p(7, 9, "L"); c.p(5, 14, "L"); c.p(6, 17, "L"); c.p(7, 11, "L")
    for x, ch in ((4, "R"), (6, "r"), (8, "R")):
        c.r(x, 19, x, 22, ch)
    c.p(5, 20, "R") if False else None
    c.r(3, 17, 3, 20, "R"); c.p(3, 21, "r")
    c.r(8, 19, 9, 19, "y")
    return done(c, 2, 13)


# ---------------------------------------------------------------- golems: stitched clay amalgams
def stitch_h(c, x0, x1, y):
    for x in range(x0, x1 + 1):
        c.p(x, y, "O" if (x - x0) % 2 == 0 else "w")


@S("golem_bear")
def _():
    c = C()
    c.r(2, 9, 13, 18, "2"); c.r(1, 10, 14, 17, "2"); c.r(2, 9, 5, 17, "1"); c.r(11, 10, 14, 17, "3")
    c.r(1, 18, 14, 18, "3")
    c.r(2, 17, 5, 21, "2"); c.r(10, 17, 13, 21, "3"); feet(c, (2, 10), 22, 4)
    c.r(2, 17, 3, 20, "1")
    # lumpy head, mismatched ears, stitched muzzle
    c.ell(8, 6, 4.5, 3.6, "2"); c.r(4, 2, 5, 3, "2"); c.r(11, 1, 12, 3, "1"); c.p(5, 2, "3")
    c.r(6, 6, 10, 9, "1"); c.r(6, 8, 9, 8, "O"); c.p(8, 6, "O")
    c.p(6, 4, "y"); c.p(6, 5, "O"); c.r(10, 3, 11, 5, "y"); c.p(10, 4, "O")      # one small, one big eye
    stitch_h(c, 3, 9, 12); c.r(8, 9, 8, 14, "O"); c.p(8, 10, "w"); c.p(8, 12, "w")
    c.r(10, 14, 12, 15, "5"); c.p(11, 14, "4"); c.p(4, 15, "4"); c.p(5, 14, "5")      # patches of other hide
    c.r(0, 13, 0, 16, "3") if False else None
    for (x, y) in ((3, 10), (12, 11), (4, 20), (11, 19)):
        c.p(x, y, "4")
    return done(c)


@S("golem_crab")
def _():
    c = C()
    c.ell(8, 15, 6, 4, "2"); c.ell(8, 14, 4.4, 2.6, "1"); c.r(3, 18, 12, 18, "3")
    # one huge claw, one tiny wrong claw
    c.r(0, 3, 5, 9, "2"); c.r(1, 2, 4, 2, "2"); c.r(0, 3, 2, 8, "1"); c.r(2, 4, 3, 7, "."); c.p(3, 3, "."); c.p(3, 2, ".")
    c.r(2, 9, 4, 10, "2"); c.r(4, 10, 6, 12, "2")
    c.r(13, 8, 14, 10, "2"); c.r(12, 10, 13, 11, "2"); c.p(14, 7, "3"); c.p(13, 7, "1"); c.p(15, 8, "1")
    c.r(10, 12, 12, 13, "2")
    c.m(6, 11, "3") if False else None
    c.r(6, 9, 6, 11, "3"); c.r(10, 8, 10, 11, "3"); c.p(6, 8, "y"); c.p(10, 7, "y"); c.p(10, 6, "y"); c.p(10, 7, "O")
    c.p(6, 8, "O")
    stitch_h(c, 5, 10, 15); c.r(8, 12, 8, 17, "O") if False else None
    c.r(5, 16, 7, 17, "5"); c.p(5, 16, "4"); c.p(11, 14, "4"); c.p(10, 17, "5")
    for (x0, y) in ((4, 17), (4, 19)):
        c.line(x0, y, 1, y + 3, "3", mirror=True)
    c.line(5, 20, 3, 22, "3", mirror=True) if False else None
    return done(c)


@S("golem_frog")
def _():
    c = C()
    c.ell(8, 15, 7, 5, "2"); c.ell(8, 14, 6, 3.6, "1"); c.ell(8, 18, 5, 2.2, "3")
    c.r(0, 18, 3, 21, "3"); c.r(12, 18, 15, 21, "3"); feet(c, (0, 12), 22, 4)
    c.r(0, 19, 2, 20, "2")
    # mismatched bulging eyes, stitched wide mouth
    c.r(2, 7, 5, 10, "2"); c.r(9, 6, 13, 10, "2"); c.r(3, 8, 4, 9, "y"); c.p(3, 9, "O")
    c.r(10, 6, 12, 8, "y"); c.p(11, 7, "O"); c.p(10, 6, "w")
    c.r(2, 11, 13, 12, "2"); stitch_h(c, 2, 13, 12)
    c.p(7, 9, "3"); c.p(8, 9, "3")
    for (x, y) in ((4, 15), (9, 14), (6, 17), (11, 16), (13, 14)):
        c.p(x, y, "4")
    c.r(7, 14, 9, 15, "5"); c.p(7, 14, "4")
    c.line(8, 13, 8, 17, "O") if False else None
    return done(c)


@S("golem_iron_maiden")
def _():
    c = C()
    # upright iron sarcophagus, face on the lid, lid swung open on spikes
    c.r(3, 1, 12, 21, "L"); c.r(2, 5, 13, 18, "L"); c.r(4, 0, 11, 0, "L")
    c.r(3, 1, 4, 21, "l"); c.r(2, 5, 3, 18, "l")
    c.r(5, 2, 10, 20, "O")                                    # dark interior
    # spikes
    for y in range(4, 20, 3):
        c.r(5, y, 6, y, "l"); c.r(9, y + 1, 10, y + 1, "l"); c.p(7, y, "w"); c.p(8, y + 1, "w")
        c.p(6, y + 1, "y") if False else None
    for (x, y) in ((5, 6), (9, 10), (6, 13), (10, 17), (5, 16)):
        c.p(x, y, "e")                                        # rust
    c.p(7, 9, "R"); c.p(8, 15, "R")
    # lid face, half-open at the left
    c.r(11, 1, 12, 21, "K") if False else None
    c.r(10, 2, 13, 20, "L"); c.r(11, 2, 12, 20, "l")
    c.p(11, 5, "O"); c.p(12, 5, "O"); c.r(11, 6, 12, 6, "L"); c.r(11, 9, 12, 9, "O")
    # rivets, rust flakes
    for y in (3, 8, 12, 16, 19):
        c.p(2, y, "w"); c.p(13, y, "L") if False else None
    for (x, y) in ((3, 7), (3, 14), (12, 11), (12, 17), (4, 20), (11, 4)):
        c.p(x, y, "E")
    c.r(4, 21, 11, 21, "L")
    return done(c, 1, 14)


@S("golem_ooze")
def _():
    c = C()
    c.ell(8, 16, 7.5, 5, "2"); c.ell(8, 15, 6.5, 3.8, "1"); c.ell(8, 8, 3.6, 4, "2"); c.ell(8, 7.5, 2.6, 3, "1")
    c.r(1, 19, 14, 21, "3"); c.r(0, 20, 15, 21, "3"); c.r(3, 19, 12, 19, "2")
    c.r(11, 8, 13, 16, "3") if False else None
    # mismatched eyes, stitches, bubbles and drips
    c.p(7, 6, "y"); c.p(7, 7, "O"); c.r(9, 5, 10, 6, "y"); c.p(9, 6, "O")
    c.p(8, 9, "O"); c.r(7, 9, 9, 9, "O") if False else None
    c.line(4, 12, 11, 12, "O") if False else None
    stitch_h(c, 4, 11, 13)
    for (x, y, r_) in ((3, 16, 1), (11, 17, 1), (6, 17, 1), (9, 15, 1)):
        c.ell(x, y, r_ + 0.3, r_ + 0.3, "5"); c.p(x, y, "4")
    c.p(1, 17, "w"); c.p(14, 16, "w") if False else None
    for x in (2, 6, 12):
        c.r(x, 22, x, 22, "3")
    c.p(5, 11, "4"); c.p(12, 14, "4")
    return done(c, 0, 15)


@S("golem_svardym")
def _():
    c = C()
    # hulking four-armed brute, sunk head, moss growing on stone hide
    c.r(3, 8, 12, 16, "2"); c.r(2, 9, 13, 14, "2"); c.r(3, 8, 6, 15, "1"); c.r(11, 9, 13, 15, "3")
    c.r(5, 3, 10, 8, "2"); c.r(5, 3, 7, 4, "1"); c.r(10, 4, 10, 8, "3")
    c.r(5, 5, 10, 5, "3"); c.p(6, 6, "y"); c.p(9, 6, "y"); c.p(7, 6, "O"); c.p(8, 6, "O") if False else None
    c.r(6, 7, 9, 7, "O"); c.p(6, 7, "w"); c.p(9, 7, "w")
    c.p(4, 2, "w"); c.p(5, 1, "w"); c.p(11, 2, "w"); c.p(10, 1, "w")             # little horns
    c.r(5, 2, 10, 2, "G"); c.p(7, 1, "g"); c.p(9, 1, "h")                          # moss
    # four arms
    for sx in (0, 1):
        def P(x, y, ch, sx=sx):
            c.p(15 - x if sx else x, y, ch)
        for y in range(9, 13):
            for x in range(0, 3):
                P(x, y, "2" if sx == 0 else "3")
        for y in range(13, 19):
            for x in range(0, 3):
                P(x, y, "2" if sx == 0 else "3")
        P(0, 9, "1") if sx == 0 else P(0, 9, "3")
        for y in range(19, 21):
            for x in range(0, 3):
                P(x, y, "1")
        P(2, 12, "G"); P(1, 17, "G"); P(0, 12, "G")
    c.r(0, 13, 1, 14, "3") if False else None
    c.r(5, 16, 10, 16, "3"); c.r(4, 17, 11, 21, "2"); c.r(4, 17, 6, 20, "1"); c.r(10, 17, 11, 21, "3")
    c.r(8, 18, 8, 21, "3"); feet(c, (3, 9), 22, 4)
    c.p(5, 11, "G"); c.p(10, 14, "g"); c.p(7, 10, "h"); c.p(6, 13, "g"); c.p(9, 12, "G")
    c.r(2, 21, 4, 21, "G") if False else None
    return done(c, 1, 14)


@S("golem_vine")
def _():
    c = C()
    # tangle of thick vines in a man-shape, thorns, a flower for a face
    for pts in ([(8, 22), (5, 18), (7, 14), (5, 10)], [(9, 22), (11, 18), (9, 14), (11, 10)],
                [(7, 14), (3, 12), (1, 8), (2, 4)], [(9, 14), (13, 12), (14, 8), (13, 4)],
                [(6, 12), (8, 8), (7, 5)], [(9, 12), (8, 8), (9, 5)]):
        tube(c, pts, 1.7, 1.0, "G")
        tube(c, [(x - 0.4, y) for x, y in pts], 1.0, 0.6, "g")
    c.ell(8, 5, 3.4, 3.4, "G")
    c.r(6, 3, 9, 6, "g"); c.p(6, 4, "O"); c.p(9, 4, "O"); c.p(7, 4, "y"); c.p(8, 4, "y") if False else None
    c.r(7, 6, 8, 6, "O")
    c.p(7, 1, "w"); c.p(8, 1, "w"); c.p(6, 2, "w"); c.p(9, 2, "w"); c.p(7, 0, "y"); c.p(8, 0, "y")
    c.p(7, 2, "y"); c.p(8, 2, "y")
    for (x, y) in ((4, 17), (11, 16), (6, 9), (10, 10), (2, 6), (13, 7), (3, 12), (12, 12), (8, 17), (5, 20), (10, 20)):
        c.p(x, y, "w")
    c.p(1, 3, "h"); c.p(14, 3, "h"); c.p(0, 9, "h"); c.p(15, 9, "h")
    c.r(5, 21, 10, 21, "h") if False else None
    return done(c, 2, 13)


def brow_jaw(c):
    """cragmensch: heavy brow, small eyes, jutting tusked jaw."""
    c.r(4, 3, 11, 4, "3"); c.r(5, 5, 10, 5, "S"); c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(4, 6, 11, 7, "s"); c.r(5, 8, 10, 8, "S"); c.r(5, 7, 10, 7, "O"); c.p(5, 6, "w"); c.p(10, 6, "w")
    c.p(6, 6, "w") if False else None
    c.r(7, 6, 8, 6, "S")


def lumen_crest(c):
    """luminary: sun of light around the brow, glowing lamp-bulb held up."""
    K.sun_halo(c, "4", "5")


def glow_lamp(c):
    c.line(13, 10, 13, 17, "n"); c.r(11, 5, 15, 9, "4"); c.r(12, 6, 14, 8, "w"); c.r(12, 5, 14, 5, "5") if False else None
    c.p(11, 5, "5"); c.p(15, 5, "5"); c.p(11, 9, "6"); c.p(15, 9, "6")
    c.p(13, 3, "4"); c.p(13, 2, "5"); c.p(9, 7, "5") if False else None
    c.p(12, 15, "s")


hum("cragmensch_luminary", hair_wild, BP.bare_chest, tunic, brow_jaw, glow_lamp, face="none", sash=False)
SPRITES["cragmensch_luminary"] = person(hair_wild, BP.bare_chest, tunic, brow_jaw, K.sun_halo, glow_lamp,
                                        face="none", sash=False)


# ---------------------------------------------------------------- kudu
@S("kudu")
def _():
    c = C()
    tube(c, [(12, 10), (14, 12), (14, 15)], 1.1, 0.8, "3")
    c.ell(9, 12, 5, 3.2, "2"); c.ell(9, 10.8, 4.2, 1.4, "1")
    c.r(10, 10, 12, 14, "3")
    for x in (7, 9, 11):
        c.r(x, 9, x, 14, "4")
    c.r(4, 6, 6, 11, "2"); c.r(3, 7, 4, 10, "1")
    c.ell(3, 5.5, 2.5, 1.8, "2"); c.r(0, 6, 2, 8, "1"); c.p(0, 7, "O")
    c.p(3, 5, "O"); c.p(5, 4, "3"); c.p(6, 4, "3")                    # ears
    # great spiral horns
    for (x, y) in ((4, 3), (5, 2), (4, 1), (5, 0), (6, 1), (7, 0), (6, 3)):
        c.p(x, y, "w")
    c.p(3, 4, "w"); c.p(4, 2, "L"); c.p(5, 1, "L"); c.p(6, 0, "L") if False else None
    c.line(4, 4, 3, 1, "w"); c.line(5, 4, 6, 2, "w"); c.p(4, 2, "L"); c.p(7, 0, "w"); c.p(2, 0, "w"); c.p(6, 1, "L")
    c.r(5, 4, 5, 4, "w")
    for x, hi in ((4, 0), (6, 1), (10, 1), (12, 0)):
        c.r(x, 14, x, 20, "2" if hi == 0 else "3")
        c.r(x, 21, x + 1, 21, "O")
    c.p(3, 21, "4") if False else None
    c.r(4, 14, 5, 15, "2") if False else None
    return done(c, 1, 14)


# ---------------------------------------------------------------- natural weapons
@S("natural_weapon_arc")
def _():
    c = C()
    # crackling electric arc
    c.line(1, 2, 6, 7, "1"); c.line(6, 7, 3, 10, "1"); c.line(3, 10, 10, 15, "1"); c.line(10, 15, 8, 18, "1")
    c.line(8, 18, 14, 22, "1")
    c.line(2, 2, 7, 7, "2"); c.line(7, 7, 4, 10, "2"); c.line(4, 10, 11, 15, "2"); c.line(11, 15, 9, 18, "2")
    c.line(9, 18, 15, 21, "2")
    c.line(1, 2, 6, 7, "w"); c.line(6, 7, 3, 10, "w"); c.line(3, 10, 10, 15, "w"); c.line(10, 15, 8, 18, "w")
    c.line(8, 18, 14, 22, "w")
    c.line(6, 7, 12, 5, "1"); c.line(12, 5, 14, 2, "2"); c.line(10, 15, 14, 12, "1"); c.line(3, 10, 0, 13, "1")
    for (x, y) in ((12, 2), (14, 5), (0, 15), (5, 17), (15, 10), (2, 6)):
        c.p(x, y, "y")
    for (x, y) in ((1, 3), (7, 8)):
        c.p(x, y, "3")
    return done(c, 2, 13)


@S("natural_weapon_finned_tail")
def _():
    c = C()
    # curved blade-fin: long ridged fin with a point
    poly(c, [(9, 1), (14, 8), (12, 17), (7, 22), (6, 15), (8, 8)], "2")
    poly(c, [(9, 1), (11, 6), (8, 8)], "1")
    poly(c, [(9, 7), (14, 8), (12, 17), (7, 22), (6, 15), (9, 12)], "3")
    poly(c, [(8, 8), (9, 7), (9, 12), (6, 15)], "1")
    for (x0, y0, x1, y1) in ((9, 8, 13, 9), (9, 11, 13, 14), (8, 14, 11, 19)):
        c.line(x0, y0, x1, y1, "w")
    c.line(8, 4, 8, 20, "L") if False else None
    c.r(5, 21, 8, 22, "5"); c.r(4, 19, 6, 21, "4"); c.p(5, 20, "w")        # stalk base
    c.line(6, 15, 4, 19, "1")
    c.p(10, 2, "w"); c.p(8, 8, "w")
    return done(c, 3, 13)


@S("natural_weapon_mallet")
def _():
    c = C()
    # bot mallet: chrome head with a rubber striking face, stout handle
    c.r(7, 9, 8, 22, "L"); c.r(7, 9, 7, 22, "l"); c.r(6, 19, 9, 20, "4")
    c.r(1, 2, 14, 9, "l"); c.r(1, 2, 14, 3, "w"); c.r(1, 8, 14, 9, "L"); c.r(11, 4, 14, 7, "L")
    c.r(0, 3, 1, 8, "3"); c.r(14, 3, 15, 8, "3"); c.r(0, 4, 0, 7, "1")
    c.r(1, 4, 4, 7, "2") if False else None
    c.r(3, 5, 5, 6, "5"); c.p(3, 5, "4"); c.r(10, 5, 12, 6, "6") if False else None
    c.p(8, 5, "O"); c.p(8, 6, "4") if False else None
    c.p(2, 4, "w"); c.p(3, 4, "w")
    c.p(7, 10, "O") if False else None
    c.r(4, 9, 11, 10, "L")
    c.p(7, 6, "4"); c.p(8, 6, "5")
    return done(c, 3, 12)


@S("natural_weapon_starfish_arm")
def _():
    c = C()
    # cyclopean arm: a thick curled starfish tentacle with suckers and a single eye on the tip
    pts = [(4, 22), (5, 17), (9, 14), (10, 9), (7, 5)]
    tube(c, pts, 3.2, 1.6, "2")
    tube(c, [(3.5, 22), (4.5, 17), (8.5, 14), (9.5, 9), (6.8, 5)], 1.8, 0.8, "1")
    for (x, y) in ((6, 19), (7, 16), (11, 13), (12, 10), (8, 8)):
        c.r(x, y, x + 1, y + 1, "5"); c.p(x, y, "4")
    for (x, y) in ((2, 20), (3, 17), (6, 14), (7, 11), (5, 7)):
        c.p(x, y, "5")
    c.ell(7, 4, 2.4, 2.4, "w"); c.p(7, 4, "4"); c.p(7, 5, "O"); c.p(6, 3, "w")
    c.ell(7, 4, 1.2, 1.2, "4") if False else None
    c.p(7, 4, "O"); c.p(6, 4, "4") if False else None
    c.r(3, 21, 7, 22, "3")
    c.r(12, 3, 14, 3, "5"); c.p(13, 2, "4") if False else None
    return done(c, 1, 8)


# ---------------------------------------------------------------- nephilim worm
@S("nephilim_shugruith")
def _():
    c = C()
    # colossal ringed worm rearing up, shale dust, starspines across its back, round maw
    pts = [(6, 22), (6, 18), (9, 14), (8, 9), (8, 5)]
    tube(c, pts, 4.0, 3.4, "2")
    tube(c, [(5, 22), (5, 18), (8, 14), (7, 9), (7, 5)], 2.5, 2.0, "1")
    tube(c, [(9, 20), (11, 16), (11, 12), (10, 8)], 1.6, 1.5, "3")
    for y in range(7, 23, 3):
        for x in range(2, 14):
            if c.g[y][x] in "123":
                c.p(x, y, "3")
    # starspines
    for (x, y) in ((11, 5), (12, 8), (12, 12), (11, 16), (10, 20)):
        c.r(x, y, x + 2, y, "w"); c.p(x + 1, y - 1, "w"); c.p(x + 1, y + 1, "4"); c.p(x + 2, y, "y") if False else None
    c.p(14, 4, "w") if False else None
    # maw
    c.ell(8, 3, 3.8, 3, "3"); c.ell(8, 3, 2.6, 2, "O"); c.p(6, 2, "w"); c.p(10, 2, "w"); c.p(8, 4, "w"); c.p(8, 1, "w")
    c.p(5, 1, "m"); c.p(11, 1, "m")
    c.p(4, 0, "e"); c.p(12, 0, "e"); c.p(7, 0, "e"); c.p(0, 4, "E"); c.p(14, 1, "E")
    c.r(9, 5, 10, 5, "2")
    return done(c, 2, 14)


# ---------------------------------------------------------------- magnet turret
@S("pulsed_field_magnet")
def _():
    c = C()
    # chrome obelisk, glowing coil bands, horseshoe crown, scrap pulled to the base
    poly(c, [(7, 0), (9, 0), (11, 4), (12, 18), (4, 18), (5, 4)], "l")
    poly(c, [(8, 0), (9, 0), (11, 4), (12, 18), (9, 18)], "L")
    c.r(5, 4, 6, 18, "w"); c.r(4, 18, 12, 20, "L"); c.r(4, 18, 12, 18, "l"); c.r(3, 20, 13, 21, "L")
    for y in (7, 11, 15):
        c.r(5, y, 11, y + 1, "2"); c.r(5, y, 8, y, "1"); c.r(9, y + 1, 11, y + 1, "3")
    c.r(7, 4, 9, 5, "4"); c.p(8, 4, "w")
    # field arcs
    for (x, y) in ((2, 6), (1, 10), (13, 8), (14, 12), (2, 14), (14, 16), (3, 2), (12, 3)):
        c.p(x, y, "4")
    for (x, y) in ((1, 6), (0, 11), (14, 9), (15, 13)):
        c.p(x, y, "5")
    # scrap bits
    for (x, y, ch) in ((1, 19, "w"), (2, 21, "e"), (13, 19, "l"), (14, 21, "E"), (0, 21, "L"), (15, 20, "w"),
                       (3, 22, "E"), (12, 22, "l")):
        c.p(x, y, ch)
    return done(c, 0, 15)


# ---------------------------------------------------------------- factory arm
@S("robot_arm")
def _():
    c = C()
    # base plate, upper arm rising, elbow joint, forearm bending over, claw hand
    c.r(1, 20, 9, 22, "L"); c.r(1, 20, 9, 20, "l")
    c.r(3, 12, 8, 19, "2"); c.r(3, 12, 5, 19, "1"); c.r(7, 12, 8, 19, "3")
    c.r(4, 14, 7, 15, "L"); c.p(4, 14, "w")
    c.ell(7, 10, 3.2, 3.2, "l"); c.ell(7, 10, 1.6, 1.6, "L"); c.p(7, 10, "4"); c.p(5, 8, "w")
    c.r(8, 4, 13, 8, "2"); c.r(8, 4, 13, 5, "1"); c.r(8, 8, 13, 8, "3"); c.r(10, 5, 11, 7, "3") if False else None
    c.r(9, 6, 12, 6, "L")
    c.r(11, 4, 14, 4, "L") if False else None
    # claw
    c.r(12, 8, 15, 10, "L"); c.r(14, 11, 15, 13, "l"); c.r(12, 11, 12, 13, "l"); c.r(13, 10, 13, 10, "O")
    c.p(12, 13, "w"); c.p(15, 13, "w")
    c.p(13, 5, "4"); c.p(13, 6, "5"); c.p(5, 17, "4"); c.p(5, 18, "5")
    for x in (1, 9):
        c.p(x, 21, "w")
    c.p(4, 2, "w") if False else None
    return done(c, 0, 10)


# ---------------------------------------------------------------- slog
@S("slog")
def _():
    c = C()
    c.ell(8, 15, 7.6, 5.6, "2"); c.ell(8, 14, 6.4, 3.8, "1"); c.r(1, 19, 14, 21, "3"); c.r(2, 18, 13, 18, "3")
    # stinking broth bubbles on breathing pores
    for (x, y, r_) in ((4, 12, 1.5), (8, 11, 1.2), (12, 13, 1.5), (6, 15, 1), (10, 16, 1.2), (3, 16, 0.9)):
        c.ell(x, y, r_ + 0.5, r_ + 0.5, "G"); c.ell(x, y, r_, r_, "g"); c.p(round(x - 0.5), round(y - 0.5), "w")
    # trashlike fifth-phase leakage
    for (x, y, ch) in ((13, 17, "6"), (14, 18, "5"), (1, 19, "4"), (7, 20, "5"), (12, 20, "6"), (0, 21, "5")):
        c.p(x, y, ch)
    # head with eyestalks
    c.ell(8, 5, 2.8, 2.6, "2"); c.r(6, 2, 6, 4, "3"); c.r(10, 2, 10, 4, "3")
    c.p(6, 1, "w"); c.p(10, 1, "w"); c.p(6, 2, "O"); c.p(10, 2, "O")
    c.r(7, 6, 9, 6, "3"); c.r(7, 5, 9, 5, "1"); c.p(8, 6, "O")
    c.r(7, 8, 9, 9, "2")
    return done(c, 0, 15)


# ---------------------------------------------------------------- stem
@S("stem")
def _():
    c = C()
    # dried yuckwheat stem with elbowed forks and salt crystals
    c.line(8, 22, 7, 15, "2"); c.line(9, 22, 8, 15, "1"); c.line(7, 15, 8, 10, "2"); c.line(8, 15, 9, 10, "1")
    c.line(8, 10, 6, 5, "2"); c.line(9, 10, 7, 5, "1"); c.line(6, 5, 7, 1, "2")
    c.line(8, 14, 4, 12, "2"); c.line(4, 12, 3, 8, "2"); c.line(3, 8, 1, 6, "2")
    c.line(9, 12, 13, 11, "2"); c.line(13, 11, 13, 7, "2"); c.line(13, 7, 14, 4, "2")
    c.line(7, 7, 11, 5, "2") if False else None
    for (x, y) in ((7, 20), (8, 17), (8, 12), (7, 8), (4, 12), (3, 9), (13, 10), (13, 8)):
        c.r(x - 1, y, x + 1, y, "3")
    for (x, y) in ((4, 11), (3, 7), (1, 5), (12, 12), (12, 6), (14, 3), (6, 4), (7, 0), (5, 14), (10, 13)):
        c.p(x, y, "w"); c.p(x, y - 1, "W") if False else None
        c.p(x + 1, y - 1, "w")
    c.p(2, 7, "L") if False else None
    c.r(6, 22, 9, 22, "N") if False else None
    return done(c, 5, 10)


# ---------------------------------------------------------------- templar mech
@S("templar_mech_big")
def _():
    c = C()
    # giant godsuit of chrome: broad pauldrons, small visored head, red braids and a bloodoil cincture
    c.r(5, 0, 10, 4, "l"); c.r(5, 0, 6, 4, "w"); c.r(9, 0, 10, 4, "L"); c.r(6, 2, 9, 3, "O")
    c.p(6, 2, "4"); c.p(9, 2, "4"); c.p(7, 2, "c") if False else None
    c.r(3, 5, 12, 8, "1"); c.mr(0, 5, 3, 9, "2"); c.mr(0, 5, 1, 7, "1"); c.mr(0, 9, 3, 9, "3")
    c.r(4, 5, 11, 12, "2"); c.r(4, 5, 7, 12, "1"); c.r(10, 5, 11, 12, "3")
    c.r(6, 7, 9, 8, "L"); c.p(7, 7, "4"); c.p(8, 7, "4"); c.r(7, 8, 8, 8, "5") if False else None
    # arms
    c.r(0, 10, 3, 17, "L"); c.r(12, 10, 15, 17, "L"); c.r(0, 10, 1, 16, "l"); c.r(0, 17, 3, 19, "2"); c.r(12, 17, 15, 19, "3")
    c.r(0, 17, 1, 18, "1")
    # cincture of braids
    c.r(4, 12, 11, 13, "5"); c.r(4, 12, 11, 12, "4"); c.p(7, 13, "y"); c.p(8, 13, "y")
    for x in (5, 7, 9):
        c.r(x, 14, x, 17, "5"); c.p(x, 18, "6")
    c.r(6, 14, 6, 16, "4") if False else None
    # legs
    c.r(4, 14, 11, 15, "2") if False else None
    c.r(4, 14, 6, 21, "2"); c.r(9, 14, 11, 21, "3"); c.r(4, 14, 5, 21, "1"); c.r(7, 16, 8, 21, "O") if False else None
    c.r(4, 19, 6, 20, "L"); c.r(9, 19, 11, 20, "L")
    c.r(3, 21, 7, 22, "L"); c.r(8, 21, 12, 22, "L"); c.r(3, 21, 7, 21, "l"); c.r(8, 21, 12, 21, "l")
    # blood
    c.p(2, 12, "R"); c.p(13, 18, "R"); c.p(5, 21, "R"); c.p(10, 6, "R"); c.p(2, 8, "R")
    return done(c, 2, 13)


# ---------------------------------------------------------------- unimax
@S("unimax")
def _():
    c = C()
    # white horse with a spiral horn, magenta mane and tail streamers
    tube(c, [(11, 9), (14, 11), (15, 15), (13, 20)], 1.4, 1.0, "4")
    tube(c, [(12, 10), (14, 14), (13, 19)], 1.0, 0.7, "5")
    c.ell(9, 12, 4.8, 3.2, "2"); c.ell(9, 10.8, 4, 1.4, "1")
    c.r(4, 5, 6, 11, "2"); c.r(3, 6, 4, 10, "1")
    c.ell(3, 5, 2.4, 1.8, "2"); c.r(0, 6, 2, 8, "1"); c.p(0, 7, "O"); c.p(3, 4, "O")
    c.p(5, 3, "3"); c.p(6, 3, "3")
    # horn
    c.line(2, 3, 0, 0, "w"); c.line(3, 3, 1, 0, "L"); c.p(0, 0, "w")
    # mane streamers
    for (x0, y0, x1, y1, ch) in ((6, 3, 12, 6, "4"), (6, 4, 13, 8, "5"), (5, 5, 11, 10, "4"), (6, 6, 9, 11, "5")):
        c.line(x0, y0, x1, y1, ch)
    c.line(7, 3, 14, 4, "4")
    c.p(14, 5, "4"); c.p(12, 4, "5")
    for x, h in ((4, 0), (6, 1), (10, 1), (12, 0)):
        c.r(x, 14, x, 20, "2" if h == 0 else "3"); c.r(x + 1, 14, x + 1, 20, "2" if h == 0 else "3")
        c.r(x, 21, x + 1, 21, "O"); c.p(x, 20, "4") if False else None
        c.p(x, 20, "5")
    return done(c, 1, 14)


# ---------------------------------------------------------------- waveform worm
@S("waveform_worm")
def _():
    import math
    c = C()
    # ringed worm laid along a sine wave across the tile
    pts = []
    for i in range(0, 15):
        x = 1 + i
        y = 12 + 6 * math.sin(i / 14 * 2 * math.pi * 1.5 + 0.3)
        pts.append((x, y))
    for i, (x, y) in enumerate(pts):
        r_ = 2.2 if i > 0 else 2.6
        c.ell(x, y, r_, r_, "3" if i % 2 else "2")
        c.ell(x, y - 0.6, r_ - 0.9, r_ - 1.0, "1" if i % 2 == 0 else "2")
        if i % 3 == 0:
            c.p(round(x), round(y - 0.4), "R")
    # head at left
    x, y = pts[0]
    c.ell(x, y, 2.8, 2.8, "1"); c.p(round(x) + 1, round(y) - 1, "O"); c.p(round(x) + 1, round(y) + 1, "O")
    c.p(round(x), round(y) - 1, "w") if False else None
    c.r(round(x) - 2, round(y), round(x) - 1, round(y), "R")
    # ghost waveform trace
    for i in range(1, 15):
        px, py = pts[i]
        if i % 2 == 0:
            c.p(round(px), round(py) + 4 if round(py) < 14 else round(py) - 4, "R")
    return done(c, 0, 15)


# ---------------------------------------------------------------- young barathrum hologram
def yb_head(c):
    """bear-snouted young urshiib, short quill mane, bright face."""
    c.mr(4, 2, 5, 3, "2"); c.r(5, 3, 10, 7, "1"); c.r(10, 4, 10, 7, "2")
    c.r(6, 6, 9, 8, "w"); c.p(7, 7, "O"); c.p(8, 7, "O"); c.p(6, 5, "O"); c.p(9, 5, "O")
    for x in range(4, 12):
        c.p(x, 1, "2" if x % 2 else "w")
    for x in (5, 7, 9, 11):
        c.p(x, 0, "w")
    c.p(3, 3, "w"); c.p(12, 3, "w"); c.p(3, 4, "2") if False else None


def scan(c):
    for y in (7, 12, 17, 21):
        for x in range(2, 14):
            if c.g[y][x] not in ".x":
                c.p(x, y, "3" if c.g[y][x] != "O" else "O")


SPRITES["young_barathrum"] = person(BP.white_fur, yb_head, BP.fingers, tunic, scan,
                                    overlay(K.MUTATIONS["Quills"][1], behind=True), face="none", sash=False)


# ============================================================ round 2 refinements
def claw(c, side, cx, cy, rx, ry, ch="1", edge="2"):
    """C-shaped pincer (open toward the top)."""
    def P(x, y, v):
        c.p(15 - x if side else x, y, v)
    for y in range(24):
        for x in range(16):
            d = ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2
            d2 = ((x - cx - 0.8) / (rx * 0.45)) ** 2 + ((y - cy + 0.5) / (ry * 0.55)) ** 2
            if d <= 1 and d2 > 1:
                P(x, y, ch)
    for x in range(int(cx - rx) - 1, int(cx + rx) + 2):
        for y in range(int(cy - ry) - 1, int(cy) - 1):
            pass


@S("golem_crab")
def _():
    c = C()
    c.ell(8, 15, 6, 3.8, "2"); c.ell(8, 14, 4.6, 2.4, "1"); c.r(3, 18, 12, 18, "3")
    # huge claw (left), tiny wrong claw (right)
    c.ell(3, 7, 3.4, 4.2, "1"); c.ell(3.6, 5, 1.6, 2.4, "."); c.r(2, 0, 5, 3, ".") if False else None
    c.r(3, 1, 4, 4, "."); c.r(4, 0, 6, 1, ".")
    c.r(0, 6, 5, 10, "1"); c.r(0, 9, 5, 10, "2"); c.r(5, 3, 6, 8, "2") if False else None
    c.line(0, 4, 0, 9, "2"); c.p(1, 2, "2"); c.p(2, 1, "2")
    c.r(4, 10, 6, 12, "2")
    c.ell(13, 10, 1.6, 2, "1"); c.p(13, 9, "."); c.p(14, 8, "1"); c.p(14, 9, "."); c.r(12, 12, 12, 13, "2")
    c.r(10, 11, 12, 13, "2")
    c.p(14, 11, "O") if False else None
    c.r(6, 9, 6, 11, "3"); c.r(9, 9, 9, 11, "3"); c.p(6, 8, "y"); c.p(9, 7, "y"); c.p(9, 8, "3"); c.p(6, 7, "O")
    c.p(9, 6, "O")
    stitch_h(c, 4, 11, 15)
    c.r(5, 16, 7, 17, "5"); c.p(5, 16, "4"); c.p(11, 14, "4"); c.p(10, 17, "5")
    c.p(3, 8, "O"); c.p(2, 8, "w"); c.p(1, 7, "w")
    for y in (17, 19):
        c.line(4, y, 1, y + 3, "3", mirror=True)
    return done(c)


@S("slog")
def _():
    c = C()
    # huge slug facing left, shell-less, humped back of popping bubbles, trash leaking behind
    tube(c, [(14, 19), (10, 16), (6, 15), (3, 14)], 2.0, 4.2, "2")
    tube(c, [(13, 17), (9, 14), (6, 13)], 1.0, 2.6, "1")
    tube(c, [(14, 20), (10, 18), (6, 18)], 1.0, 2.2, "3")
    c.r(2, 19, 12, 21, "3"); c.r(1, 18, 5, 20, "3")
    c.ell(3, 10, 2.6, 4, "2"); c.r(1, 8, 4, 14, "2"); c.r(1, 8, 2, 13, "1")
    c.r(1, 3, 1, 7, "2"); c.r(5, 3, 5, 7, "2"); c.p(1, 2, "w"); c.p(5, 2, "w"); c.p(1, 3, "O"); c.p(5, 3, "O")
    c.r(1, 11, 3, 11, "O"); c.p(2, 12, "w")
    for (x, y, r_) in ((6, 11, 1.4), (9, 12, 1.6), (12, 15, 1.4), (8, 15, 1), (5, 15, 0.9)):
        c.ell(x, y, r_ + 0.5, r_ + 0.5, "G"); c.ell(x, y, r_, r_, "g"); c.p(round(x - 0.5), round(y - 0.5), "w")
    c.p(10, 14, "O") if False else None
    for (x, y, ch) in ((14, 20, "6"), (15, 21, "5"), (12, 22, "4"), (7, 22, "6"), (3, 22, "5"), (14, 17, "5"),
                       (15, 19, "4")):
        c.p(x, y, ch)
    return done(c)


@S("waveform_worm")
def _():
    import math
    c = C()
    pts = [(1.2 + i * 0.95, 12 + 7 * math.sin(i / 14.0 * 2 * math.pi * 1.25 + 0.5)) for i in range(15)]
    for i, (x, y) in enumerate(pts[1:], start=1):
        ch = "2" if (i // 1) % 2 else "3"
        c.ell(x, y, 1.9, 1.9, ch)
        c.ell(x, y - 0.5, 1.1, 1.0, "1" if i % 2 else "2")
    for i, (x, y) in enumerate(pts[1:], start=1):
        if i % 2 == 0:
            c.p(round(x), round(y) - 1, "R")
    x, y = pts[0]
    c.ell(x + 0.5, y, 2.7, 2.7, "1"); c.ell(x + 0.5, y, 2.7, 2.7, "1")
    c.p(round(x) + 1, round(y) - 1, "O"); c.p(round(x) + 1, round(y) + 1, "O"); c.p(round(x) - 1, round(y), "R")
    c.p(round(x) - 1, round(y) - 1, "R") if False else None
    # faint waveform guide line
    for i in range(0, 16, 2):
        px = i
        py = 12 + 7 * math.sin(i / 14.0 * 2 * math.pi * 1.25 + 0.5)
        yy = 22 if py < 12 else 1
        c.p(px, yy, "R")
    return done(c)


@S("mollusk")
def _():
    c = C()
    # open clam: raised upper valve behind, lower valve in front, hatchet of tissue between
    c.ell(8, 8, 7.4, 6.4, "3"); c.r(0, 9, 15, 12, ".")
    c.ell(8, 8.6, 6.4, 5.4, "2"); c.r(0, 9, 15, 12, ".")
    for x in (2, 4, 6, 8, 10, 12):
        c.line(8, 9, x + 1, 3 if 3 < x < 12 else 5, "3") if False else None
    for x in (1, 3, 5, 7, 9, 11, 13):
        c.line(8, 9, x, 3 if 2 < x < 12 else 5, "3")
    c.r(1, 9, 14, 10, "3"); c.r(3, 3, 5, 4, "1") if False else None
    c.p(5, 4, "1"); c.p(4, 5, "1"); c.p(3, 6, "1"); c.p(6, 3, "1")
    c.ell(8, 17, 7.6, 4.2, "3"); c.ell(8, 17, 6.6, 3.2, "2"); c.r(1, 12, 14, 14, ".") if False else None
    c.r(0, 15, 15, 15, "3") if False else None
    for x in (1, 3, 5, 7, 9, 11, 13):
        c.line(8, 15, x, 21, "3")
    c.r(1, 17, 7, 17, "1"); c.r(2, 16, 5, 16, "1")
    # tissue hatchet
    poly(c, [(4, 9), (12, 9), (14, 15), (8, 20), (2, 15)], "5")
    poly(c, [(4, 9), (8, 9), (8, 20), (2, 15)], "4")
    poly(c, [(12, 9), (14, 15), (8, 20), (8, 12)], "6")
    c.p(7, 12, "O"); c.p(10, 12, "O")
    c.p(8, 14, "O"); c.p(9, 14, "O")
    c.line(2, 18, 6, 20, "l"); c.line(13, 17, 11, 20, "L"); c.p(1, 14, "l"); c.p(14, 5, "l") if False else None
    c.line(2, 14, 4, 16, "l") if False else None
    return done(c)


@S("golem_ooze")
def _():
    c = C()
    # slumped mud heap of lumps, one swollen arm, mismatched eyes, stitches, rising bubbles
    c.ell(8, 17, 7.8, 4.6, "2"); c.ell(8, 16, 6.5, 3.4, "1"); c.r(0, 19, 15, 21, "3"); c.r(1, 19, 14, 19, "2")
    c.ell(7, 10, 4.2, 4.6, "2"); c.ell(6.5, 9.5, 3.2, 3.6, "1")
    c.ell(13, 14, 2.4, 3.6, "2"); c.ell(13, 13.5, 1.4, 2.2, "1"); c.ell(2, 15, 2, 2.6, "2")
    c.r(4, 7, 5, 8, "y"); c.p(4, 8, "O"); c.p(8, 6, "y"); c.p(8, 7, "O"); c.p(9, 6, "w") if False else None
    c.r(5, 11, 9, 11, "O")
    stitch_h(c, 3, 11, 15)
    for x in (5, 7, 9):
        c.p(x, 12, "w")
    for (x, y) in ((3, 17), (11, 18), (8, 18), (6, 13)):
        c.ell(x, y, 1.1, 1.1, "5"); c.p(x, y, "4")
    for x in (3, 7, 12):
        c.r(x, 22, x, 22, "3")
    c.p(10, 3, "5"); c.p(11, 1, "4"); c.p(11, 2, "5")
    return done(c)


@S("antiprism")
def _():
    c = C()
    poly(c, [(8, 2), (13, 5), (14, 11), (12, 17), (8, 20), (3, 17), (1, 11), (3, 5)], "2")
    poly(c, [(8, 2), (13, 5), (8, 8), (3, 5)], "1")
    poly(c, [(3, 5), (8, 8), (6, 13), (1, 11)], "1")
    poly(c, [(8, 8), (13, 5), (14, 11), (10, 13)], "3")
    poly(c, [(1, 11), (6, 13), (3, 17)], "2")
    poly(c, [(6, 13), (10, 13), (8, 20), (3, 17)], "3")
    poly(c, [(10, 13), (14, 11), (12, 17), (8, 20)], "2")
    for a, b in (((8, 8), (6, 13)), ((8, 8), (10, 13)), ((6, 13), (10, 13)), ((3, 5), (8, 8)), ((13, 5), (8, 8)),
                 ((1, 11), (6, 13)), ((14, 11), (10, 13)), ((3, 17), (6, 13)), ((12, 17), (10, 13)),
                 ((3, 17), (8, 20)), ((12, 17), (8, 20))):
        c.line(a[0], a[1], b[0], b[1], "4")
    c.r(6, 3, 9, 3, "w"); c.p(5, 4, "w")
    c.r(7, 9, 8, 11, "5"); c.p(7, 9, "w")
    c.p(7, 15, "O"); c.p(9, 15, "O"); c.p(8, 17, "5")
    c.r(4, 20, 11, 21, "3") if False else None
    return done(c, 1, 14)


@S("frustum")
def _():
    c = C()
    poly(c, [(5, 5), (11, 5), (14, 20), (1, 20)], "2")
    poly(c, [(5, 5), (11, 5), (12, 9), (4, 9)], "1")
    poly(c, [(4, 9), (12, 9), (14, 20), (1, 20)], "2")
    poly(c, [(4, 9), (7, 9), (6, 20), (1, 20)], "1")
    poly(c, [(12, 9), (14, 20), (10, 20), (9, 9)], "3")
    c.r(1, 20, 14, 21, "3")
    for a, b in (((4, 9), (1, 20)), ((12, 9), (14, 20)), ((7, 9), (6, 20)), ((9, 9), (10, 20)), ((4, 9), (12, 9))):
        c.line(a[0], a[1], b[0], b[1], "6")
    c.r(6, 5, 10, 5, "w"); c.p(5, 6, "w")
    c.r(6, 13, 9, 16, "5"); c.r(7, 13, 8, 14, "4"); c.p(5, 18, "4"); c.p(10, 18, "5"); c.p(12, 15, "4")
    return done(c, 0, 15)


@S("young_barathrum")
def _():
    c = person(BP.white_fur, yb_head, BP.fingers, tunic,
               overlay(K.MUTATIONS["Quills"][1], behind=True), face="none", sash=False)
    return c


SPRITES["cannibal"] = person(hair_mohawk, BP.bone_necklace, BP.bare_chest, tunic, BP.fangs, cleaver,
                             face="face", sash=False)
