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
