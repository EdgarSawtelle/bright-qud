"""B3 remaining creatures, batch 5."""
from functools import partial
import b3kit as K
from b3kit import (C, back, overlay, person, hat_wide, hat_straw, hood, hair_wild, hair_long, hair_mohawk,
                   stubble, armor, tunic, staff, spear, shield, wrench, scroll, apron, club, jug, cap,
                   scarf, veil, blindfold, sword, rifle)
from b3_people import (bear_head, white_fur, fingers, bone_necklace, bone_club, fangs, huge_arm, goat_head,
                       goat_legs, bare_chest, deer_body, deer_ears, small_antlers, mail_coif, tabard,
                       closed_eyes, eyes, hide_poncho)
from b3more_keys import MORE_KEYS

KEYS = MORE_KEYS[5]
P = person


# ======================================================================= humanoid parts
def wings_small(c):
    """small feathered cherub wings behind the shoulders."""
    for x0, x1, y0, y1, ch in ((1, 4, 7, 10, "w"), (0, 3, 10, 13, "w"), (1, 3, 13, 14, "l")):
        c.mr(x0, y0, x1, y1, ch)
    c.mr(0, 10, 1, 13, "l"); c.mr(1, 7, 1, 8, "l")
    c.m(0, 11, "L")


def halo_gold(c):
    c.r(5, 0, 10, 0, "4"); c.p(4, 1, "5"); c.p(11, 1, "5"); c.r(5, 1, 5, 1, "."); c.r(10, 1, 10, 1, ".")
    c.r(5, 2, 10, 2, "."); 


def boulder(c):
    """huge rock hugged against the left hip."""
    c.ell(2.6, 14, 3.4, 3.8, "l")
    c.ell(3.3, 15, 2.6, 2.8, "L")
    c.ell(2, 12.8, 1.8, 1.6, "w")
    c.p(2, 15, "O"); c.p(3, 16, "O"); c.p(1, 14, "L")
    c.r(4, 14, 4, 15, "S")


def moss_hair(c):
    """long root-braided hair."""
    c.r(5, 2, 10, 3, "h"); c.r(4, 3, 4, 9, "g"); c.r(11, 3, 11, 9, "h")
    c.p(7, 2, "g"); c.p(9, 2, "G"); c.p(3, 7, "G"); c.p(12, 8, "g")


def shawl_roses(c):
    """shawl over the head swathing the lower face, five roses."""
    c.r(4, 2, 11, 3, "5"); c.r(4, 4, 4, 9, "5"); c.r(11, 4, 11, 9, "6")
    c.r(5, 2, 10, 2, "4")
    c.r(5, 6, 10, 6, "4"); c.r(6, 7, 9, 8, "5"); c.p(10, 6, "5")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    for x, y in ((5, 3), (8, 1), (10, 3), (4, 11), (11, 12)):
        c.p(x, y, "r"); c.p(x + 1, y, "R") if x + 1 < 16 else None
    c.p(8, 1, "r"); c.p(9, 1, "R"); c.p(7, 1, "R")
    c.p(5, 3, "r"); c.p(6, 3, "R"); c.p(10, 3, "r")


def ape_head(c):
    """stitched ape head: heavy brow, jaw, big fangs."""
    c.r(4, 3, 11, 8, "2")
    c.r(4, 3, 11, 3, "1"); c.r(10, 4, 11, 8, "3")
    c.r(5, 5, 10, 5, "3")
    c.p(6, 5, "O"); c.p(9, 5, "y") ; c.p(7, 5, "3")
    c.r(5, 6, 10, 8, "S"); c.r(6, 6, 9, 6, "s")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.p(6, 8, "w"); c.p(9, 8, "w")
    c.line(5, 3, 7, 4, "O"); c.p(8, 4, "O")


def stitches(c):
    for (x, y) in ((4, 11), (11, 12), (7, 13), (8, 17), (5, 19), (10, 20)):
        c.p(x, y, "O"); c.p(x + 1, y + 1, "O") if x < 14 else None
    c.r(7, 10, 8, 10, "O") if False else None
    c.line(6, 10, 9, 10, "O") if False else None


def patch(c):
    c.r(5, 13, 7, 14, "6"); c.r(8, 17, 10, 18, "5")
    c.line(5, 13, 7, 14, "O") if False else None


def leaf_brim(c):
    """broad leaf drooping over the head, blossom on top."""
    c.r(6, 0, 9, 0, "4"); c.r(5, 1, 10, 1, "5")
    c.r(7, 0, 8, 0, "4")
    c.r(3, 2, 12, 2, "g"); c.r(1, 3, 14, 3, "g"); c.r(2, 4, 13, 4, "h")
    c.r(3, 2, 6, 2, "G"); c.r(1, 3, 5, 3, "G")
    c.line(8, 2, 8, 3, "h"); c.p(2, 4, "h")
    c.p(7, 1, "w"); c.p(8, 0, "w")


def slynth_face(c):
    c.p(6, 5, "m"); c.p(9, 5, "m")


def hindren_tabard(c):
    """spotless white tabard with long tails front and back."""
    c.r(6, 10, 9, 21, "w")
    c.r(9, 10, 9, 21, "l")
    c.r(6, 15, 9, 15, "4")
    c.r(6, 16, 6, 16, "5")
    c.p(7, 12, "4"); c.p(8, 12, "4")
    c.r(7, 21, 8, 21, "l")


def hat_leather(c):
    """beaten leather hat pulled low over the eyes."""
    c.r(6, 1, 9, 1, "n"); c.r(5, 2, 10, 2, "n"); c.r(5, 3, 10, 4, "N")
    c.r(3, 4, 12, 4, "N"); c.r(3, 3, 3, 3, "n"); c.r(12, 3, 12, 3, "n")
    c.r(5, 2, 10, 2, "n"); c.r(6, 2, 7, 2, "t")
    c.p(6, 5, "O"); c.p(9, 5, "O")


def scruff(c):
    c.r(5, 6, 5, 7, "n"); c.r(10, 6, 10, 7, "N"); c.r(6, 7, 9, 7, "n"); c.p(7, 8, "N")


def amoeba_bucket(c):
    """bucket of green amoeba on the left."""
    c.r(0, 15, 4, 19, "n"); c.r(0, 15, 4, 15, "N"); c.r(0, 19, 4, 19, "N")
    c.r(1, 12, 3, 14, "G"); c.p(2, 11, "G"); c.r(1, 13, 2, 13, "w") if False else None
    c.p(1, 12, "w"); c.p(3, 13, "g"); c.p(2, 14, "g")
    c.r(1, 16, 3, 17, "t") if False else None
    c.r(4, 15, 4, 15, "s")


def beet_arm(c):
    pass


def titan_shoulders(c):
    """immense body: trapezii swelling to the tile edges."""
    c.r(0, 8, 15, 11, "2")
    c.r(1, 7, 14, 8, "2")
    c.r(0, 8, 15, 8, "1")
    c.r(1, 7, 6, 7, "1")
    c.r(10, 9, 15, 11, "3")
    c.r(2, 9, 3, 10, "1") if False else None
    for x in (3, 5, 9, 11, 13):
        c.p(x, 10, "6")
    c.p(2, 9, "5"); c.p(12, 9, "5")
    # forked hand-feet
    c.r(0, 12, 2, 15, "2"); c.r(13, 12, 15, 15, "3")
    c.line(0, 16, 0, 20, "S") if False else None
    for x in (0, 1, 2):
        c.p(x, 16, "S"); c.p(x, 17, "S") if x != 1 else None
    for x in (13, 14, 15):
        c.p(x, 16, "S"); c.p(x, 17, "S") if x != 14 else None
    c.p(0, 18, "S"); c.p(2, 18, "S"); c.p(13, 18, "S"); c.p(15, 18, "S")


def titan_head(c):
    c.r(5, 2, 10, 8, "3")
    c.r(5, 2, 10, 2, "2")
    c.r(10, 3, 10, 8, "O") if False else None
    c.p(6, 5, "y"); c.p(9, 5, "y")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    # vapor from the nares
    c.p(7, 8, "y"); c.p(8, 8, "w") if False else None
    c.p(6, 9, "5") if False else None
    c.p(12, 3, "y"); c.p(13, 1, "w"); c.p(3, 3, "y"); c.p(2, 1, "w")
    c.line(5, 1, 4, 0, "5") if False else None


def ribbons(c):
    """sidewise ribbons streaming from the cowl."""
    c.line(11, 4, 15, 3, "4"); c.line(11, 5, 15, 5, "5"); c.line(11, 6, 15, 8, "4")
    c.p(15, 2, "5"); c.p(15, 9, "5")


def shroom_crown(c):
    """flower crown with a troop of little mushrooms."""
    c.r(4, 2, 11, 3, "6")
    for x, y, h in ((4, 1, "r"), (7, 0, "r"), (10, 1, "r")):
        c.r(x - 1, y, x + 1, y, h); c.p(x, y + 1, "w")
    c.p(7, 0, "R") ; c.p(4, 1, "R"); c.p(10, 1, "R")
    c.p(6, 0, "w"); c.p(11, 1, "w")
    c.p(5, 2, "4"); c.p(8, 2, "4"); c.p(10, 2, "5")
    c.p(6, 5, "y"); c.p(9, 5, "y")


def cider_pot(c):
    """steaming pot hung at the left hip with a stirring ladle."""
    c.r(0, 15, 4, 19, "O"); c.r(1, 16, 3, 18, "L")
    c.r(1, 16, 3, 16, "l"); c.r(0, 15, 4, 15, "L")
    c.line(2, 15, 3, 10, "n"); c.line(3, 15, 4, 11, "N") if False else None
    c.p(1, 13, "w"); c.p(3, 12, "w"); c.p(2, 11, "l")
    c.p(2, 17, "r"); c.p(3, 17, "R")


def banner(c):
    """banner pole with a flag."""
    c.line(13, 0, 13, 17, "n")
    c.r(14, 1, 15, 8, "2"); c.r(14, 1, 15, 2, "1"); c.r(14, 7, 15, 8, "3")
    c.r(10, 1, 12, 7, "2"); c.r(10, 1, 12, 2, "1"); c.r(11, 7, 12, 8, "3")
    c.r(11, 3, 12, 5, "4"); c.p(11, 4, "5")
    c.p(13, 0, "y")
    c.p(12, 15, "s")


def warden_pauld(c):
    c.mr(3, 9, 4, 10, "l"); c.m(3, 9, "w"); c.p(11, 10, "L")
    c.mr(2, 3, 3, 3, ".") if False else None
    c.p(6, 3, "y") if False else None


def mane(c):
    c.r(4, 2, 11, 2, "5"); c.r(3, 3, 4, 9, "5"); c.r(11, 3, 12, 9, "6"); c.r(5, 2, 10, 2, "4")


def ape_arms(c):
    c.r(3, 9, 12, 9, "2"); c.r(1, 10, 4, 18, "2"); c.r(11, 10, 14, 18, "3")
    c.r(1, 10, 2, 16, "1"); c.r(0, 19, 4, 20, "S"); c.r(11, 19, 15, 20, "S")
    c.p(0, 20, "O"); c.p(4, 20, "O"); c.p(11, 20, "O"); c.p(15, 20, "O")
    c.r(1, 14, 4, 14, "O") if False else None
    c.p(2, 12, "O"); c.p(3, 13, "O"); c.p(12, 13, "O"); c.p(13, 14, "O")
    c.r(4, 15, 4, 15, ".") if False else None


def plain(c):
    pass


BEARMAN = P(white_fur, bear_head, wrench, face="none", sash=False)
CHERUB_CANNIBAL = P(wings_small, halo_gold, hair_mohawk, bone_necklace, tunic, bone_club, fangs, face="face",
                    sash=False)
CRAG = P(boulder, huge_arm, moss_hair, tunic, face="face", sash=False)
ESTHERS = P(shawl_roses, spear, face="none", trim="4")
GOLEM_APE = P(ape_arms, ape_head, stitches, face="none", sash=False)
GOLEM_SLYNTH = P(leaf_brim, slynth_face, stitches, face="none", sash=False)
HINDREN = P(deer_body, deer_ears, small_antlers, hindren_tabard, face="face", sash=False)
MERCHANT = P(hat_leather, scruff, amoeba_bucket, tunic, face="none", sash=False)
BETHSAIDA = P(titan_shoulders, titan_head, face="none", sash=False)
SEEKER = P(hood, ribbons, closed_eyes, scroll, face="face", trim="4")
KYAKUKYA = P(shroom_crown, cider_pot, face="none", sash=False)
BEARER = P(banner, mail_coif, armor, tabard, face="face", sash=False)
WARDEN = P(goat_legs, bare_chest, goat_head, mane if False else plain, warden_pauld, spear, shield,
           face="none", sash=False)


# ======================================================================= free-form creatures
def halo(c, y=0, x0=5, x1=10):
    """small golden cherub halo."""
    c.r(x0, y, x1, y, "4"); c.p(x0 - 1, y + 1, "5"); c.p(x1 + 1, y + 1, "5")
    c.p(x0, y + 1, "5") if False else None


def seg(c, pts, ch, r=1):
    for i in range(len(pts) - 1):
        (a, b), (e, f) = pts[i], pts[i + 1]
        n = max(abs(e - a), abs(f - b), 1)
        for k in range(n + 1):
            c.r(round(a + (e - a) * k / n), round(b + (f - b) * k / n),
                round(a + (e - a) * k / n) + r - 1, round(b + (f - b) * k / n) + r - 1, ch)


def anemone():
    c = C()
    # splash of saliva
    c.r(2, 21, 13, 22, "x") if False else None
    for x, y in ((2, 21), (4, 22), (11, 22), (13, 21), (7, 22), (9, 22)):
        c.p(x, y, "B")
    # rubber trunk rings
    for i, (y, w, dx) in enumerate(((20, 5, 0), (17, 4, 1), (14, 4, 0), (11, 3, 1))):
        x0 = 8 - w // 2 + dx - (1 if w % 2 == 0 else 0) + (1 if i == 0 else 0)
        c.r(x0, y, x0 + w + 1, y + 2, "2")
        c.r(x0, y, x0 + 1, y + 2, "1")
        c.r(x0 + w, y, x0 + w + 1, y + 2, "3")
        c.r(x0, y + 2, x0 + w + 1, y + 2, "3")
    # titan tongues
    for (pts, ch) in (([(8, 11), (5, 8), (3, 4), (3, 1)], "4"), ([(8, 11), (7, 7), (7, 3), (6, 0)], "5"),
                      ([(9, 11), (10, 7), (11, 3), (10, 0)], "4"), ([(9, 11), (12, 8), (13, 5), (14, 2)], "5"),
                      ([(8, 11), (3, 10), (1, 8), (0, 6)], "5")):
        seg(c, pts, ch, 2)
    for x, y in ((3, 2), (7, 4), (10, 2), (13, 4), (1, 7), (5, 7), (11, 6)):
        c.p(x, y, "6")
    for x, y in ((3, 1), (6, 0), (10, 0), (14, 2), (0, 6)):
        c.p(x, y, "6")
    c.shadow(0, 15)
    return c.out()


def boosterbot():
    c = C()
    # treads
    c.r(4, 19, 11, 21, "L"); c.r(4, 19, 11, 19, "l"); c.r(4, 21, 11, 21, "O")
    c.r(6, 20, 9, 20, "l")
    # torso
    c.r(5, 12, 10, 18, "l"); c.r(5, 12, 6, 18, "w") if False else None
    c.r(9, 12, 10, 18, "L"); c.r(5, 12, 10, 12, "w")
    c.r(6, 14, 9, 16, "2"); c.r(6, 14, 9, 14, "1"); c.r(9, 14, 9, 16, "3")
    c.p(7, 15, "4"); c.p(8, 15, "4")
    # shackle + saddle-face screen
    c.r(7, 10, 8, 11, "L")
    c.r(3, 3, 12, 9, "L"); c.r(3, 3, 12, 3, "l"); c.r(3, 3, 3, 9, "l")
    c.r(4, 4, 11, 8, "O")
    c.r(5, 5, 6, 7, "4"); c.p(5, 6, "5") if False else None   # pictograph: cross + spiral
    c.p(5, 6, "O") if False else None
    c.r(8, 5, 10, 5, "4"); c.p(9, 6, "4"); c.r(8, 7, 10, 7, "4"); c.p(10, 6, "4")
    c.p(5, 4, "5"); c.p(4, 8, "5") if False else None
    # chrome arms with booster-groove hands
    c.r(2, 11, 4, 12, "L"); c.r(11, 11, 13, 12, "L")
    c.r(1, 12, 3, 17, "l"); c.r(12, 12, 14, 17, "L")
    c.r(0, 17, 3, 19, "2"); c.r(12, 17, 15, 19, "3")
    c.p(1, 18, "4"); c.p(2, 18, "4"); c.p(13, 18, "4"); c.p(14, 18, "4")
    c.shadow(0, 15)
    return c.out()


def cherub_baetyl_mechanical():
    c = C()
    halo(c, 0)
    # floating egg-stone
    c.ell(7.5, 11, 5, 7, "2")
    c.ell(6.5, 9.5, 3.2, 5, "1")
    c.r(10, 6, 12, 16, "3") if False else None
    for y in range(5, 17):
        c.p(12 if 7 < y < 15 else 11, y, "3")
    c.r(3, 11, 12, 12, "L"); c.r(3, 11, 12, 11, "l")
    c.r(6, 11, 9, 12, "4"); c.p(7, 11, "w"); c.p(8, 12, "5")
    c.ell(7.5, 6, 2, 1.2, "L") if False else None
    # rune ticks
    c.p(6, 7, "5"); c.p(9, 8, "5"); c.p(6, 15, "5"); c.p(9, 14, "6")
    # thruster glow
    c.r(5, 18, 10, 18, "L"); c.r(6, 19, 9, 19, "5"); c.r(7, 20, 8, 20, "4")
    c.p(7, 21, "w") if False else None
    c.p(2, 14, "l"); c.p(13, 14, "L")
    c.shadow(2, 13)
    return c.out()


def cherub_crab_mechanical():
    c = C()
    halo(c, 1, 5, 10)
    # claws
    for s in (1, -1):
        def X(x):
            return x if s == 1 else 15 - x
        c.line(X(4), 11, X(2), 8, "L", ); c.line(X(5), 11, X(3), 8, "l")
        c.r(min(X(0), X(3)), 4, max(X(0), X(3)), 7, "2")
        c.r(min(X(0), X(1)), 4, max(X(0), X(1)), 7, "3") if s == 1 else c.r(14, 4, 15, 7, "3")
        c.p(X(2), 3, "l"); c.p(X(0), 2, "l") if False else None
        c.p(X(1), 4, "O"); c.p(X(1), 5, "O")
    # body
    c.ell(7.5, 14, 6, 4.2, "2")
    c.ell(6.5, 12.5, 4, 2.5, "1")
    c.r(10, 13, 13, 16, "3")
    c.r(5, 15, 10, 15, "3")
    c.r(5, 10, 6, 10, "O"); c.r(9, 10, 10, 10, "O")
    c.p(5, 9, "4"); c.p(10, 9, "4") ; c.p(5, 8, "l") if False else None
    c.p(7, 13, "4"); c.p(8, 13, "5")
    # legs
    for y, x in ((17, 1), (19, 0), (21, 1)):
        c.line(3 + (x == 0), y - 1 if y > 17 else y, x, y + 1, "L", mirror=True)
    c.shadow(0, 15)
    return c.out()


def cherub_flower_mechanical():
    c = C()
    halo(c, 0, 5, 10)
    # gear petals around a glowing core
    cx, cy = 7.5, 8
    for dx, dy in ((0, -4.2), (0, 4.2), (-4.4, 0), (4.4, 0), (-3.1, -3.1), (3.1, -3.1), (-3.1, 3.1), (3.1, 3.1)):
        c.ell(cx + dx, cy + dy + 1, 2, 2, "2")
    c.ell(cx, cy + 1, 4.2, 4.2, "1")
    c.ell(cx + 0.6, cy + 1.6, 3.4, 3.4, "2")
    c.r(10, 8, 12, 12, "3") if False else None
    for dx, dy in ((4.4, 0), (3.1, 3.1), (0, 4.2), (-3.1, 3.1)):
        c.p(round(cx + dx + 1), round(cy + dy + 2), "3")
    c.ell(cx, cy + 1, 2.2, 2.2, "L")
    c.ell(cx, cy + 1, 1.5, 1.5, "4"); c.p(7, 8, "w"); c.p(8, 9, "5")
    # stem and leaf blades
    c.r(7, 14, 8, 21, "L"); c.r(7, 14, 7, 21, "l")
    c.r(2, 17, 6, 18, "l"); c.r(1, 16, 2, 16, "l"); c.r(9, 19, 13, 20, "L"); c.r(13, 18, 14, 18, "l")
    c.p(4, 17, "w"); c.p(11, 19, "l")
    c.r(5, 21, 10, 21, "L")
    c.shadow(2, 13)
    return c.out()


def cherub_insect_mechanical():
    c = C()
    halo(c, 0, 5, 10)
    # wings
    c.ell(3.5, 10, 3.2, 4.5, "l"); c.ell(11.5, 10, 3.2, 4.5, "L")
    c.ell(3.5, 10, 2.2, 3.4, "w") if False else None
    c.line(5, 7, 2, 12, "w"); c.line(10, 7, 13, 12, "l")
    # abdomen / thorax / head
    c.ell(7.5, 17, 3, 4, "2"); c.ell(6.8, 16, 1.8, 2.5, "1")
    c.r(9, 15, 10, 19, "3"); c.r(6, 19, 9, 19, "3") if False else None
    c.r(5, 18, 10, 18, "3")
    c.r(5, 11, 10, 14, "2"); c.r(5, 11, 7, 14, "1"); c.r(9, 12, 10, 14, "3")
    c.r(6, 6, 9, 9, "L"); c.r(6, 6, 9, 6, "l")
    c.p(6, 8, "4"); c.p(9, 8, "4"); c.p(7, 8, "w") if False else None
    c.line(6, 6, 4, 3, "L"); c.line(9, 6, 11, 3, "L")
    c.p(4, 3, "5"); c.p(11, 3, "5")
    c.p(7, 17, "4"); c.p(8, 20, "5")
    # legs
    for y, x in ((12, 2), (14, 1), (16, 2)):
        c.line(5, y, x, y + 3, "L", mirror=True)
        c.p(x, y + 4, "l"); c.p(15 - x, y + 4, "l")
    c.shadow(1, 14)
    return c.out()


def cherub_reptile_mechanical():
    c = C()
    halo(c, 2, 2, 7)
    # head left, tail right curling
    c.r(0, 6, 5, 9, "2"); c.r(0, 6, 5, 6, "1"); c.r(0, 9, 5, 9, "3")
    c.p(3, 7, "4"); c.p(4, 7, "w") if False else None
    c.r(0, 8, 0, 8, "O")
    c.r(1, 10, 2, 10, "w")
    # jointed body
    for i, x in enumerate(range(4, 12, 2)):
        c.r(x, 10, x + 2, 16, "2" if i % 2 == 0 else "3")
        c.r(x, 10, x + 2, 11, "1" if i % 2 == 0 else "2")
    c.r(4, 12, 11, 12, "L") if False else None
    c.p(6, 13, "4"); c.p(8, 13, "4"); c.p(10, 13, "5")
    # legs
    for x in (3, 10):
        c.r(x, 17, x + 1, 20, "L"); c.r(x - 1, 20, x + 2, 20, "l")
        c.r(x + 3 if x == 3 else x - 2, 16, x + 4 if x == 3 else x - 1, 19, "L")
    c.r(2, 17, 3, 20, "L") if False else None
    # tail
    seg(c, [(11, 12), (13, 13), (14, 16), (13, 19), (11, 20)], "2", 2)
    c.p(11, 20, "4"); c.p(12, 20, "5")
    c.shadow(0, 15)
    return c.out()


def cherub_swine_mechanical():
    c = C()
    halo(c, 3, 3, 8)
    # barrel body (side view, facing left)
    c.ell(9, 14, 6, 4.5, "2"); c.ell(8, 12.5, 4.5, 2.4, "1")
    c.r(12, 14, 15, 17, "3"); c.r(6, 17, 14, 17, "3")
    # head + snout disc
    c.r(1, 10, 5, 16, "2"); c.r(1, 10, 5, 10, "1"); c.r(1, 16, 5, 16, "3")
    c.r(0, 12, 1, 15, "l"); c.p(0, 13, "O"); c.p(0, 14, "O"); c.p(1, 12, "w")
    c.p(3, 12, "4"); c.p(4, 12, "w") if False else None
    c.r(3, 8, 5, 9, "L"); c.r(3, 8, 3, 8, "l")
    # ribs / plates
    c.p(8, 13, "4"); c.p(10, 14, "5"); c.p(12, 13, "4")
    # spring tail
    c.p(15, 11, "l"); c.p(14, 10, "L"); c.p(15, 9, "l"); c.p(14, 8, "L")
    # trotters
    for x in (3, 6, 10, 13):
        c.r(x, 18, x + 1, 21, "L" if x < 8 else "3"); c.r(x, 21, x + 1, 21, "O")
    c.shadow(0, 15)
    return c.out()


def cherub_vine_mechanical():
    c = C()
    halo(c, 0, 5, 10)
    # coiled steel cable up from the ground to a lamp bud
    pts = [(3, 21), (4, 18), (10, 17), (11, 14), (5, 12), (6, 8), (8, 5)]
    seg(c, pts, "L", 3)
    seg(c, pts, "l", 1)
    for x, y in ((5, 18), (9, 17), (10, 14), (6, 12)):
        c.p(x, y, "w")
    # leaf plates
    c.r(11, 19, 14, 20, "2"); c.r(11, 19, 13, 19, "1"); c.r(1, 14, 4, 15, "2"); c.r(1, 14, 3, 14, "1")
    c.r(12, 10, 14, 11, "2"); c.r(12, 10, 13, 10, "1")
    c.r(13, 15, 14, 15, "3") if False else None
    # lamp bud
    c.ell(8, 4, 2.6, 2.4, "L"); c.ell(8, 4, 1.8, 1.6, "4"); c.p(8, 4, "w")
    c.r(13, 21, 14, 21, "l") if False else None
    c.r(2, 21, 5, 21, "L")
    c.shadow(1, 14)
    return c.out()


def cloneling():
    c = C()
    # stemmed articulators fanning from the apex with scalpels
    for (x0, y0, x1, y1) in ((6, 9, 2, 3), (7, 8, 5, 1), (9, 8, 11, 1), (10, 9, 13, 3)):
        c.line(x0, y0, x1, y1, "L")
        c.p(x1, y1 - 1, "w") if y1 > 0 else None
        c.p(x1, y1, "l")
    c.p(2, 2, "w"); c.p(5, 0, "w"); c.p(11, 0, "w"); c.p(13, 2, "w")
    c.p(4, 6, "l") ; c.p(11, 5, "l")
    # pyramid
    for y in range(8, 20):
        w = (y - 8) // 2 + 1
        c.r(8 - w, y, 7 + w, y, "2")
        c.r(8 - w, y, 8 - w + max(1, w // 2), y, "1")
        c.r(7 + w - max(1, w // 3), y, 7 + w, y, "3")
    c.r(6, 19, 9, 19, "3") if False else None
    c.r(7, 11, 8, 13, "4"); c.p(7, 12, "w")
    c.r(6, 15, 9, 15, "L")
    # amniotic drip
    for x, y in ((2, 17), (13, 16), (5, 21), (10, 21)):
        c.p(x, y, "B"); c.p(x, y + 1, "b") if y < 21 else None
    c.p(7, 21, "B"); c.p(8, 20, "b")
    c.shadow(2, 13)
    return c.out()


def dreamcrungle_dead():
    c = C()
    # collapsed shanks
    for x0, y0, x1, y1 in ((3, 14, 0, 19), (12, 14, 15, 19), (5, 16, 2, 21), (10, 16, 13, 21), (7, 17, 5, 21)):
        c.line(x0, y0, x1, y1, "L")
        c.p(x1, y1, "l")
    # slagged saucer
    c.ell(7.5, 14, 7, 3.2, "3")
    c.ell(7.5, 13.5, 6, 2.4, "2")
    c.ell(6.5, 13, 3.5, 1.2, "1")
    for x, y in ((12, 15), (3, 15), (9, 16), (5, 16)):
        c.p(x, y, "3")
    c.p(14, 15, "O"); c.p(1, 14, "O")
    # steaming globe
    c.ell(7.5, 9, 3.4, 3.4, "2"); c.ell(6.5, 8, 2, 2, "1"); c.p(6, 7, "w")
    c.r(10, 8, 10, 11, "3")
    # steam
    for x, y, ch in ((5, 4, "w"), (7, 2, "l"), (9, 3, "w"), (8, 0, "l"), (6, 1, "w"), (11, 5, "l"), (4, 6, "l")):
        c.p(x, y, ch)
    c.shadow(0, 15)
    return c.out()


def frog():
    c = C()
    # folded hind legs, wide stance
    c.ell(3.5, 17, 3.2, 3.5, "3"); c.ell(12.5, 17, 3.2, 3.5, "3")
    c.ell(3.5, 16.5, 2, 2.4, "2"); c.ell(12.5, 16.5, 2, 2.4, "2")
    c.r(0, 20, 4, 21, "1"); c.r(11, 20, 15, 21, "1")
    c.p(0, 21, "3"); c.p(15, 21, "3")
    # body
    c.ell(7.5, 14, 4.2, 4.5, "2")
    c.ell(7, 12.5, 2.8, 3, "1")
    c.r(10, 12, 11, 17, "3")
    c.p(6, 15, "3"); c.p(9, 13, "3"); c.p(8, 17, "3"); c.p(5, 12, "3")
    # proud puffed throat
    c.r(5, 9, 10, 10, "w"); c.r(6, 11, 9, 11, "w") if False else None
    # head
    c.ell(7.5, 7, 4.6, 2.5, "2")
    c.r(4, 8, 11, 8, "3")
    c.r(6, 8, 9, 8, "O")
    # eyes
    c.r(3, 3, 5, 5, "2"); c.r(10, 3, 12, 5, "2")
    c.r(4, 3, 4, 4, "w"); c.r(11, 3, 11, 4, "w"); c.p(4, 4, "O"); c.p(11, 4, "O")
    c.p(7, 5, "3"); c.p(8, 5, "3")
    # front legs
    c.r(4, 15, 5, 19, "2"); c.r(10, 15, 11, 19, "2"); c.r(3, 19, 5, 19, "1"); c.r(10, 19, 12, 19, "1")
    c.shadow(0, 15)
    return c.out()


def goathead():
    c = C()
    # smoking charred slop mound
    c.ell(7.5, 18, 7, 3.4, "3"); c.ell(7.5, 17.5, 5.6, 2.4, "O")
    c.ell(5, 18, 2.4, 1.2, "3")
    c.p(2, 20, "L"); c.p(12, 20, "L"); c.p(9, 19, "L")
    # skull
    c.r(5, 9, 10, 15, "w"); c.r(4, 10, 11, 13, "w")
    c.r(10, 10, 11, 15, "l"); c.r(6, 15, 9, 17, "l")
    c.r(5, 11, 6, 12, "O"); c.r(9, 11, 10, 12, "O")
    c.p(7, 13, "O"); c.p(8, 13, "O"); c.p(6, 15, "O"); c.p(8, 15, "O") if False else None
    c.r(6, 16, 9, 16, "w"); c.p(7, 16, "O"); c.p(8, 16, "O") if False else None
    # horns
    for s in (1, -1):
        def X(x):
            return x if s == 1 else 15 - x
        c.line(X(4), 9, X(1), 6, "L"); c.line(X(5), 9, X(2), 6, "L")
        c.line(X(1), 6, X(0), 2, "l"); c.line(X(2), 6, X(1), 2, "l")
        c.p(X(0), 2, "L")
    # char on the bone and smoke
    c.p(7, 10, "L"); c.p(9, 14, "L"); c.p(5, 14, "R")
    for x, y, ch in ((1, 1, "l"), (14, 0, "l"), (0, 4, "L"), (15, 4, "L"), (2, 0, "L")):
        c.p(x, y, ch)
    c.p(3, 3, "R") if False else None
    c.shadow(0, 15)
    return c.out()


def golem_bat():
    c = C()
    # membrane wings splayed with stitched panels
    for s in (1, -1):
        def X(x):
            return x if s == 1 else 15 - x
        for (x0, y0, x1, y1) in ((4, 9, 0, 3), (4, 10, 0, 9), (5, 11, 1, 15)):
            c.line(X(x0), y0, X(x1), y1, "L")
        for y in range(4, 16):
            for x in range(0, 5):
                inside = y >= 5 + (x * 0) and True
        c.r(min(X(0), X(4)), 6, max(X(0), X(4)), 11, "2" if s == 1 else "3")
        c.r(min(X(1), X(4)), 11, max(X(1), X(4)), 14, "2" if s == 1 else "3")
        c.p(X(2), 8, "O"); c.p(X(3), 9, "O"); c.p(X(1), 12, "O"); c.p(X(2), 13, "O")
        c.p(X(0), 4, "L"); c.p(X(0), 3, "l")
        c.p(X(1), 5, "O") if False else None
    # body
    c.ell(7.5, 14, 2.8, 4, "2"); c.ell(7, 13, 1.5, 2.5, "1"); c.r(9, 12, 10, 16, "3")
    c.r(6, 11, 9, 11, "O") if False else None
    # head with huge ears
    c.r(5, 6, 10, 10, "2"); c.r(5, 6, 10, 6, "1"); c.r(10, 7, 10, 10, "3")
    c.r(4, 1, 5, 6, "2"); c.r(10, 1, 11, 6, "3"); c.p(4, 0, "l") if False else None
    c.r(5, 2, 5, 5, "S"); c.r(10, 2, 10, 5, "R")
    c.p(6, 7, "4"); c.p(9, 7, "4")
    c.r(6, 9, 9, 9, "w") if False else None
    c.p(6, 9, "w"); c.p(9, 9, "w"); c.p(7, 9, "O"); c.p(8, 9, "O")
    c.line(5, 6, 5, 6, "O")
    c.line(6, 12, 9, 12, "O") if False else None
    # feet
    c.r(6, 18, 6, 20, "L"); c.r(9, 18, 9, 20, "L"); c.p(6, 21, "l"); c.p(9, 21, "l")
    c.r(6, 18, 9, 18, "3")
    c.shadow(0, 15)
    return c.out()


def golem_clam():
    c = C()
    # lower shell
    c.ell(7.5, 16, 7.4, 4.8, "3"); c.ell(7.5, 15.5, 6.4, 3.6, "2")
    # open upper shell, ridged
    c.ell(7.5, 8.5, 7.2, 6.5, "2")
    c.r(0, 11, 15, 22, ".") if False else None
    c.r(0, 12, 15, 13, ".") if False else None
    c.r(1, 13, 14, 14, "O")
    c.ell(7.5, 8, 6, 5, "1")
    for x in (3, 6, 9, 12):
        c.line(7.5 if False else 7, 12, x, 4, "2")
    c.line(7, 12, 7, 3, "2") if False else None
    c.r(11, 6, 14, 11, "3")
    # interior body with an eye
    c.r(2, 14, 13, 17, "5"); c.r(3, 14, 12, 14, "4")
    c.ell(7.5, 15.5, 2.4, 1.6, "w"); c.p(7, 15, "O"); c.p(8, 15, "O") if False else None
    c.p(7, 16, "O") if False else None
    # teeth
    for x in range(2, 14, 2):
        c.p(x, 13, "w")
    for x in range(3, 13, 2):
        c.p(x, 18, "w") if False else None
    # stitches
    c.r(7, 17, 8, 21, "O") if False else None
    c.line(2, 20, 5, 19, "O"); c.line(10, 19, 13, 20, "O")
    c.p(3, 19, "w") if False else None
    c.shadow(0, 15)
    return c.out()


def golem_fractus():
    c = C()
    # fractal branching cactus, each arm forks again; stitched joints
    c.r(6, 12, 9, 21, "2"); c.r(6, 12, 7, 21, "1"); c.r(9, 12, 9, 21, "3")
    c.r(6, 11, 9, 11, "2")
    for (x0, y0, x1, y1, th) in ((6, 14, 2, 9, 2), (9, 14, 13, 9, 2), (7, 11, 5, 5, 2), (8, 11, 10, 5, 2)):
        seg(c, [(x0, y0), (x1, y1)], "2", th)
    # second-level forks
    for (x0, y0, x1, y1) in ((2, 9, 0, 5), (3, 9, 4, 5), (13, 9, 14, 5), (12, 9, 11, 5), (5, 5, 3, 2), (6, 5, 7, 2),
                             (10, 5, 12, 2), (9, 5, 8, 1)):
        c.line(x0, y0, x1, y1, "1" if x0 < 8 else "3")
        c.p(x1, y1, "1" if x0 < 8 else "3")
    # tips with flowers + stitches + spines
    for x, y in ((0, 5), (4, 5), (14, 5), (11, 5), (3, 2), (7, 2), (12, 2), (8, 1)):
        c.p(x, y - 1, "4")
    c.p(3, 1, "5") if False else None
    for x, y in ((6, 15), (8, 17), (7, 19), (9, 14)):
        c.p(x, y, "w")
    c.p(7, 15, "O"); c.p(8, 15, "O") ; c.p(7, 16, "O") if False else None
    c.line(6, 18, 9, 18, "O")
    c.p(7, 17, "O") if False else None
    c.r(3, 21, 12, 21, "3"); c.r(5, 20, 10, 20, "2")
    c.shadow(1, 14)
    return c.out()


def golem_insect():
    c = C()
    # stitched stag-beetle: domed wing-cases, huge pincers, mismatched legs
    for y, x in ((11, 0), (14, 0), (17, 1)):
        c.line(3, y, x, y + 1, "L"); c.line(x, y + 1, x + (1 if y == 17 else 0), y + 5, "l")
        c.line(12, y, 15 - x, y + 1, "L"); c.line(15 - x, y + 1, 15 - x - (1 if y == 17 else 0), y + 5, "l")
    c.ell(7.5, 16, 6, 5.6, "2"); c.ell(6.2, 14.6, 4, 3.4, "1")
    c.r(10, 12, 13, 20, "3")
    c.line(7, 11, 7, 21, "O"); c.line(8, 11, 8, 21, "3")
    c.r(8, 14, 12, 16, "5"); c.p(9, 15, "4"); c.p(11, 14, "4")
    c.p(9, 17, "O"); c.p(10, 18, "O"); c.p(3, 18, "O"); c.p(4, 19, "O")
    # head and pincers
    c.r(5, 6, 10, 10, "L"); c.r(5, 6, 10, 6, "l"); c.r(5, 6, 5, 10, "l")
    c.p(6, 8, "4"); c.p(9, 8, "O"); c.p(9, 7, "w") if False else None
    c.line(5, 7, 2, 4, "w"); c.line(2, 4, 4, 1, "w"); c.line(5, 8, 3, 6, "l")
    c.line(10, 7, 13, 4, "w"); c.line(13, 4, 11, 1, "w"); c.line(10, 8, 12, 6, "l")
    c.p(7, 5, "w"); c.p(8, 5, "w")
    c.shadow(0, 15)
    return c.out()


def golem_oddity():
    c = C()
    # amalgam: stacked lumps, a jar-eye, a stray arm, a cog; stitched
    c.ell(7.5, 18, 6, 3.4, "3"); c.ell(7.5, 17.5, 5, 2.6, "2")
    c.ell(6.5, 12.5, 4.4, 4, "2"); c.ell(5.5, 11.5, 2.4, 2.4, "1")
    c.r(9, 11, 10, 15, "3")
    c.ell(9, 6, 3, 2.8, "1"); c.ell(9.5, 6.4, 2.4, 2.2, "2")
    # eye
    c.ell(9, 6, 1.4, 1.4, "w"); c.p(9, 6, "O"); c.p(9, 5, "y") if False else None
    # extra arm with claw
    c.line(10, 12, 14, 9, "S"); c.line(10, 13, 14, 10, "s") if False else None
    c.p(15, 8, "S"); c.p(14, 8, "S"); c.p(15, 10, "S")
    # cog
    c.ell(3, 14, 2.4, 2.4, "l"); c.p(3, 14, "O")
    for x, y in ((3, 11), (3, 17), (0, 14), (6, 14)):
        c.p(x, y, "L")
    c.p(2, 13, "w")
    # small mouth
    c.r(5, 15, 8, 15, "O"); c.p(5, 16, "w"); c.p(7, 16, "w")
    c.p(5, 14, "y") if False else None
    c.p(6, 11, "4"); c.p(7, 10, "5")
    c.line(8, 9, 9, 8, "O")
    c.line(4, 19, 10, 19, "O") if False else None
    c.p(4, 18, "O"); c.p(5, 19, "O"); c.p(10, 18, "O"); c.p(9, 19, "O")
    c.shadow(0, 15)
    return c.out()


def golem_succulent():
    c = C()
    # rosette of fat leaves, stitched, a single eye in the heart
    leaves = ((7.5, 19, 2, 6), (3, 17, 3.6, 2), (12, 17, 3.6, 2), (2, 12, 2, 4), (13, 12, 2, 4),
              (4, 7, 2, 4), (11, 7, 2, 4), (7.5, 4, 2, 3.6))
    for (x, y, rx, ry) in leaves:
        c.ell(x, y, rx, ry, "3")
    for (x, y, rx, ry) in leaves:
        c.ell(x - 0.4, y - 0.4, rx - 0.7, ry - 0.7, "2")
    for (x, y, rx, ry) in leaves:
        c.p(round(x - 0.5), round(y - ry + 1), "1")
    c.ell(7.5, 12, 4.4, 5, "2"); c.ell(6.8, 11, 3, 3.6, "1"); c.r(10, 10, 11, 15, "3")
    c.ell(7.5, 12, 1.9, 1.9, "w"); c.p(7, 12, "O"); c.p(8, 12, "O"); c.p(8, 13, "O") if False else None
    c.r(7, 12, 8, 13, "O") if False else None
    c.p(7, 12, "O"); c.p(7, 13, "O")
    # thorns + stitches
    for x, y in ((3, 8), (12, 8), (1, 12), (14, 12), (5, 4), (10, 4), (8, 1)):
        c.p(x, y, "w")
    c.line(5, 15, 8, 17, "O") if False else None
    c.p(4, 18, "O"); c.p(5, 18, "O"); c.p(11, 17, "O"); c.p(12, 17, "O")
    c.p(7, 17, "4"); c.p(8, 7, "4")
    c.shadow(0, 15)
    return c.out()


def golem_urchin():
    c = C()
    import math
    # spines (all around)
    for k in range(16):
        a = k * math.tau / 16
        x0, y0 = 7.5 + math.cos(a) * 4, 12.5 + math.sin(a) * 4
        x1, y1 = 7.5 + math.cos(a) * 7.5, 12.5 + math.sin(a) * 8.2
        c.line(round(x0), round(y0), round(x1), round(y1), "w" if k % 2 else "l")
        c.p(round(x1), round(y1), "L") if y1 < 22 else None
    c.ell(7.5, 12.5, 5, 5.4, "2"); c.ell(6.5, 11, 3.4, 3.6, "1")
    c.r(10, 10, 12, 15, "3")
    # one big eye, maw, stitches
    c.ell(7.5, 11, 2.2, 2.2, "w"); c.p(7, 11, "4"); c.p(8, 11, "O") if False else None
    c.p(7, 11, "O"); c.p(8, 11, "O")
    c.r(5, 15, 10, 15, "O"); c.p(6, 15, "w"); c.p(8, 15, "w"); c.p(10, 15, "w")
    c.p(4, 10, "O"); c.p(11, 13, "O"); c.p(5, 8, "O") if False else None
    c.line(9, 8, 11, 9, "O")
    c.shadow(0, 15)
    return c.out()


def kah():
    c = C()
    # six glass piers
    for (x0, y0, x1, y1) in ((5, 12, 2, 15), (10, 12, 13, 15), (4, 13, 0, 17), (11, 13, 15, 17),
                             (6, 14, 4, 19), (9, 14, 11, 19)):
        c.line(x0, y0, x1, y1, "c")
        c.line(x1, y1, x1 + (1 if x1 > 7 else -1) * 0, 21 - (1 if y1 < 19 else 0), "c")
        c.p(x1, 21 - (1 if y1 < 19 else 0), "w")
    # body prism
    c.r(4, 10, 11, 16, "2"); c.r(4, 10, 6, 16, "1"); c.r(10, 11, 11, 16, "3")
    c.r(3, 12, 4, 14, "1"); c.r(11, 12, 12, 14, "3")
    c.r(7, 11, 8, 15, "4"); c.p(7, 12, "w")
    c.r(5, 16, 10, 16, "3")
    # astral spike head
    c.line(8, 9, 8, 0, "1"); c.line(7, 9, 7, 3, "2"); c.line(9, 9, 9, 3, "3")
    c.r(6, 7, 9, 9, "2"); c.p(8, 0, "w"); c.p(8, 1, "w")
    c.p(6, 8, "4"); c.p(9, 8, "4")
    c.shadow(0, 15)
    return c.out()


def mirthworm():
    c = C()
    # chain of silver barrels, one tearing in two
    def barrel(cx, cy, rx, ry):
        c.ell(cx, cy, rx, ry, "3"); c.ell(cx - 0.3, cy - 0.3, rx - 0.6, ry - 0.7, "2")
        c.ell(cx - 1, cy - 1, max(rx - 2, 1), max(ry - 2, 1), "1")
    barrel(11.5, 20, 3.4, 2.4)
    barrel(10, 16.6, 3.6, 2.6)
    # tearing: gap with strands
    c.p(8, 13, "w"); c.p(9, 13, "l"); c.p(8, 14, "l"); c.p(10, 14, "w")
    barrel(7, 11, 3.6, 2.6)
    barrel(6.6, 7.2, 3.6, 2.6)
    barrel(4, 3.6, 2.8, 2.4)
    # head: eye and grin on the top barrel
    c.p(3, 3, "O"); c.p(5, 3, "O"); c.r(3, 5, 5, 5, "O") if False else None
    c.p(3, 4, "w"); c.p(4, 4, "O"); c.p(5, 4, "w")
    c.r(5, 7, 5, 8, "4") if False else None
    # detail: segment lines
    c.p(9, 11, "5"); c.p(8, 7, "5"); c.p(11, 17, "5")
    # budding half
    c.ell(14, 12, 1.4, 1.6, "2"); c.p(14, 12, "1")
    c.shadow(0, 15)
    return c.out()


def nacham():
    c = C()
    # three digitigrade skin legs
    for (x0, y0, x1, y1, x2) in ((4, 12, 2, 17, 1), (11, 12, 13, 17, 14), (7, 14, 7, 18, 7)):
        c.line(x0, y0, x1, y1, "S"); c.line(x0 + 1, y0, x1 + 1, y1, "s")
        c.line(x1, y1, x2, 21, "S")
        c.r(x2 - 1, 21, x2 + 1, 21, "s")
    # braids of cordage
    for x in (4, 7, 10):
        c.line(x, 14, x - 1 if x < 8 else x + 1, 20, "4")
        c.p(x - 1 if x < 8 else x + 1, 20, "5")
    # floating three-banded carapace
    c.r(2, 4, 13, 6, "L"); c.r(1, 7, 14, 9, "L"); c.r(2, 10, 13, 12, "L")
    c.r(2, 4, 13, 4, "w"); c.r(1, 7, 14, 7, "l"); c.r(2, 10, 13, 10, "l")
    c.r(6, 5, 9, 5, "2"); c.r(5, 8, 10, 8, "2"); c.r(6, 11, 9, 11, "2")
    c.r(4, 5, 5, 6, "1") if False else None
    c.p(2, 6, "O"); c.p(13, 6, "O"); c.p(1, 9, "O"); c.p(14, 9, "O")
    c.r(7, 6, 8, 6, "3"); c.r(7, 9, 8, 9, "3")
    c.p(7, 8, "w"); c.p(8, 5, "w")
    # tension glints between bands
    c.p(4, 7, "c"); c.p(11, 7, "c"); c.p(5, 10, "c") if False else None
    c.p(3, 10, "c"); c.p(12, 10, "c")
    c.p(7, 3, "c"); c.p(8, 2, "c") if False else None
    c.shadow(0, 15)
    return c.out()


def natural_weapon_field():
    c = C()
    for rx, ry, ch in ((6.8, 9, "L"), (5.6, 7.6, "2"), (4.2, 6, "1"), (2.8, 4.2, "2"), (1.4, 2.2, "w")):
        c.ell(7.5, 12, rx, ry, ch)
    # warped ring cuts
    for (x, y) in ((3, 6), (12, 8), (2, 14), (13, 17), (6, 20), (9, 4)):
        c.p(x, y, "O")
    c.line(4, 9, 6, 8, "O"); c.line(9, 16, 11, 15, "O")
    c.p(7, 11, "O"); c.p(8, 12, "O")
    return c.out()


def natural_weapon_leaf():
    c = C()
    # flabby drooping leaf
    pts = [(3, 20), (4, 15), (6, 9), (10, 4), (13, 3)]
    seg(c, pts, "2", 5)
    c.ell(8.5, 10, 4.8, 7.5, "2")
    c.ell(7.5, 9.5, 3, 5.5, "1")
    c.r(11, 10, 12, 16, "3")
    for x in (4, 10):
        pass
    c.line(5, 19, 11, 4, "3")
    for y, dx in ((8, 2), (11, 3), (14, 3), (17, 2)):
        c.line(round(5 + (14 - y) * 0 + (19 - y) * 0.4), y, round(5 + (19 - y) * 0.4) - dx, y - 2, "3") if False else None
    for (x, y) in ((6, 15), (7, 12), (8, 9), (9, 7), (10, 14), (8, 17)):
        c.p(x, y, "3")
    c.r(3, 19, 4, 21, "3")
    c.shadow(1, 14)
    return c.out()


def natural_weapon_shovel():
    c = C()
    # cherubic spade, diagonal, with haloed gold trim
    c.line(2, 21, 11, 5, "n"); c.line(3, 21, 12, 5, "N")
    c.r(12, 1, 15, 4, "y") if False else None
    c.r(1, 20, 3, 21, "N")
    c.ell(11.5, 5.5, 2.4, 2.4, "y") if False else None
    # blade
    c.r(8, 0, 14, 2, "l") ; c.r(7, 3, 15, 8, "l")
    c.r(8, 9, 14, 10, "l"); c.r(9, 11, 13, 11, "l"); c.r(10, 12, 12, 12, "L")
    c.r(7, 0, 15, 0, "w"); c.r(7, 3, 8, 8, "w")
    c.r(12, 4, 15, 9, "L"); c.r(14, 3, 15, 8, "L")
    c.line(11, 3, 11, 11, "L")
    # gold wing ornament and halo
    c.p(5, 2, "y"); c.p(4, 3, "y"); c.p(6, 1, "y"); c.p(3, 4, "y") if False else None
    c.p(9, 5, "y"); c.p(10, 6, "y")
    c.r(1, 6, 5, 6, "y"); c.p(0, 5, "y"); c.p(6, 5, "y")
    c.shadow(0, 15)
    return c.out()


def nephilim_rermadon():
    c = C()
    # coral spines + star gas up top
    for x in range(3, 12, 2):
        c.line(x, 8, x - 1 + (x > 7) * 2, 3, "6")
        c.p(x - 1 + (x > 7) * 2, 3, "5")
        c.p(x - 1 + (x > 7) * 2, 2, "5") if x % 4 == 3 else None
    for x, y in ((2, 1), (6, 0), (10, 1), (13, 3), (8, 2)):
        c.p(x, y, "w")
    # fish body (side view, facing left) with big tail fin
    c.ell(7, 14, 7, 5.4, "2"); c.ell(6, 12.5, 5, 3, "1")
    c.r(8, 16, 12, 18, "3")
    # head and jaw
    c.r(0, 11, 3, 16, "2"); c.r(0, 15, 4, 17, "3"); c.r(0, 11, 2, 11, "1")
    c.p(2, 12, "y"); c.p(1, 12, "O") if False else None
    c.p(0, 16, "w"); c.p(1, 16, "w") if False else None
    c.p(3, 12, "O") if False else None
    # tail fin
    c.line(13, 12, 15, 8, "3"); c.line(13, 17, 15, 21, "3")
    c.r(13, 11, 15, 17, "G") if False else None
    c.r(13, 13, 15, 16, "2"); c.r(14, 10, 15, 12, "3"); c.r(14, 17, 15, 19, "3")
    # pectoral fin + scale marks
    c.r(5, 17, 8, 20, "5"); c.p(5, 20, "4")
    for x, y in ((5, 13), (7, 15), (9, 13), (11, 15), (4, 15)):
        c.p(x, y, "4")
    c.shadow(0, 15)
    return c.out()


def prism():
    c = C()
    # translucent gel block seen 3/4: lighter top face, two side faces, bubbles, wobbling base
    c.r(3, 8, 7, 19, "2"); c.r(8, 8, 12, 19, "3")
    c.r(3, 8, 7, 8, "1")
    # top diamond face
    for i, y in enumerate(range(3, 9)):
        w = min(i, 5 - i) if False else (i + 1 if i < 3 else 6 - i)
        c.r(7 - i if i < 3 else 4 + (i - 3), y, 8 + i if i < 3 else 11 - (i - 3), y, "1")
    c.r(4, 7, 11, 7, "1")
    c.line(8, 8, 8, 19, "w")
    c.line(3, 8, 8, 8, "w") if False else None
    c.line(7, 3, 3, 8, "w"); c.line(8, 3, 12, 8, "l")
    c.r(2, 19, 13, 20, "3"); c.r(2, 19, 7, 19, "2"); c.p(1, 20, "3"); c.p(14, 20, "3")
    # trapped bubbles and a half-digested bone
    c.p(5, 11, "w"); c.p(6, 14, "l"); c.p(10, 12, "l"); c.p(10, 16, "w"); c.p(5, 17, "l")
    c.r(9, 10, 11, 10, "w") if False else None
    c.r(5, 12, 6, 12, "w") if False else None
    # extruding pseudopod reaching right
    seg(c, [(12, 17), (14, 18), (15, 21)], "2", 2)
    c.p(15, 21, "1")
    c.p(3, 4, "w") if False else None
    c.shadow(0, 15)
    return c.out()


def robot():
    c = C()
    # cask boots
    c.r(3, 17, 7, 21, "L"); c.r(8, 17, 12, 21, "L")
    c.r(3, 17, 7, 17, "w"); c.r(8, 17, 12, 17, "w")
    c.r(3, 17, 4, 21, "l"); c.r(8, 17, 9, 21, "l")
    c.r(3, 19, 7, 19, "O"); c.r(8, 19, 12, 19, "O")
    # body
    c.r(5, 9, 10, 16, "2"); c.r(5, 9, 6, 16, "1"); c.r(9, 10, 10, 16, "3")
    c.r(7, 11, 8, 13, "4"); c.p(7, 11, "w")
    c.r(5, 15, 10, 15, "L")
    # arms
    c.r(2, 10, 3, 15, "l"); c.r(12, 10, 13, 15, "L"); c.r(2, 16, 3, 16, "O") if False else None
    c.r(1, 15, 3, 16, "2"); c.r(12, 15, 14, 16, "3")
    # shoulder radars
    for cx, a in ((3, 0), (12, 1)):
        c.r(cx - 1, 7, cx + 1, 9, "L"); c.p(cx, 6, "L")
        c.line(cx - 2, 6, cx + 2, 3, "l")
        c.line(cx - 2, 5, cx + 2, 2, "w") if False else None
        c.ell(cx, 3.5, 2.6, 1.4, "l") if False else None
        c.p(cx + 2, 3, "4")
    # head
    c.r(5, 3, 10, 8, "L"); c.r(5, 3, 10, 3, "l"); c.r(5, 3, 5, 8, "l")
    c.r(6, 4, 9, 6, "O"); c.p(7, 5, "4"); c.p(8, 5, "4")
    c.p(7, 2, "L"); c.p(8, 1, "L"); c.p(8, 0, "5")
    c.shadow(1, 14)
    return c.out()


def shroom():
    c = C()
    # slender bowed stalk
    seg(c, [(9, 21), (9, 17), (7, 13), (7, 10)], "w", 3)
    seg(c, [(9, 21), (9, 17), (7, 13), (7, 10)], "l", 1)
    c.r(11, 16, 11, 21, "l") if False else None
    c.r(7, 20, 11, 21, "w"); c.r(10, 17, 11, 21, "l")
    # dandy cap
    c.ell(7.5, 6, 7, 4.6, "2")
    c.ell(6.5, 4.5, 4.5, 2.6, "1")
    c.r(11, 5, 14, 8, "3")
    c.r(1, 8, 14, 9, "2")
    # gills puckering underneath
    c.r(1, 10, 13, 10, "6")
    for x in range(2, 14, 2):
        c.p(x, 10, "4"); c.p(x, 11, "5") if x in (4, 8, 12) else None
    # face-ish: two dark gill-eyes in stalk top
    c.p(6, 12, "O"); c.p(8, 12, "O")
    # spots in dye color
    for x, y in ((3, 5), (6, 3), (10, 4), (12, 7), (8, 7), (4, 8)):
        c.p(x, y, "4")
    c.p(7, 2, "w")
    # weep puddle
    c.r(2, 21, 5, 21, "5"); c.p(3, 20, "4")
    c.shadow(0, 15)
    return c.out()


def starshiib():
    c = C()
    # hologram: quills (calcite screws), long ears, hex grid, gyroscopic coat; scanline gaps
    # ears whipping
    c.line(5, 5, 2, 0, "w"); c.line(6, 5, 3, 0, "l"); c.line(10, 5, 13, 0, "w"); c.line(9, 5, 12, 0, "l")
    # quills screws down the back
    for (x0, y0, x1, y1) in ((4, 8, 0, 7), (4, 10, 0, 11), (4, 12, 0, 15), (11, 8, 15, 7), (11, 10, 15, 11),
                             (11, 12, 15, 15)):
        c.line(x0, y0, x1, y1, "l")
        c.p(x1, y1, "w")
    # head
    c.r(5, 4, 10, 9, "2"); c.r(5, 4, 10, 4, "1"); c.r(10, 5, 10, 9, "3")
    c.p(6, 6, "c"); c.p(9, 6, "c"); c.r(7, 8, 8, 9, "1")
    # gyroscopic coat: rings
    c.r(4, 10, 11, 20, "2"); c.r(4, 10, 6, 20, "1"); c.r(10, 11, 11, 20, "3")
    c.ell(7.5, 14, 3.8, 3.8, "1"); c.ell(7.5, 14, 2.6, 2.6, "2"); c.ell(7.5, 14, 1.2, 1.2, "w")
    c.r(3, 14, 12, 14, "l") if False else None
    c.line(2, 13, 13, 15, "4") if False else None
    c.r(5, 20, 6, 21, "L"); c.r(9, 20, 10, 21, "L")
    # hex grid dots
    for (x, y) in ((5, 11), (9, 11), (4, 17), (11, 17), (7, 19), (5, 7), (10, 8)):
        c.p(x, y, "c")
    # scanlines
    for y in (12, 18):
        for x in range(16):
            if c.g[y][x] not in (".",) and x % 2 == 0:
                c.g[y][x] = "."
    c.shadow(2, 13)
    return c.out()


def swine():
    c = C()
    # tilted pig, side view facing left, bare hammy rump
    c.ell(9, 13.5, 6.4, 4.8, "2"); c.ell(8, 12, 4.8, 2.6, "1")
    c.ell(13, 15, 3, 3.4, "S"); c.ell(12.6, 14.5, 2, 2.4, "s")
    c.r(1, 10, 5, 15, "2"); c.r(1, 10, 5, 10, "1"); c.r(1, 15, 5, 15, "3")
    c.r(0, 12, 1, 15, "s"); c.p(0, 13, "O"); c.p(0, 14, "O")
    c.r(3, 8, 5, 9, "2"); c.p(3, 8, "S"); c.p(4, 12, "O")
    c.p(2, 15, "w") if False else None
    c.r(14, 11, 15, 12, "S"); c.p(15, 10, "S")
    # spine hair
    for x in range(5, 12, 2):
        c.p(x, 9, "3")
    # legs: tilted stance, forehooves splayed holding a wrench
    c.r(3, 16, 4, 19, "3"); c.r(6, 17, 7, 20, "3"); c.r(11, 18, 12, 20, "S"); c.r(13, 18, 14, 20, "S")
    c.r(2, 19, 5, 19, "L") if False else None
    c.p(1, 20, "O"); c.p(5, 20, "O"); c.p(2, 20, "O"); c.p(3, 20, "O") if False else None
    c.r(2, 20, 4, 20, "O"); c.r(6, 21, 8, 21, "O"); c.r(11, 21, 14, 21, "O")
    # tool in the forehooves
    c.line(0, 17, 3, 19, "l"); c.p(0, 16, "l"); c.p(1, 16, "L") if False else None
    c.p(0, 18, "L")
    c.shadow(0, 15)
    return c.out()


def turret_mini():
    c = C()
    # splayed tripod, small
    c.line(7, 12, 2, 21, "L"); c.line(8, 12, 13, 21, "L"); c.line(7, 12, 7, 21, "l")
    c.r(1, 21, 3, 21, "l"); c.r(12, 21, 14, 21, "l"); c.r(6, 21, 9, 21, "l")
    # head
    c.r(4, 7, 11, 12, "2"); c.r(4, 7, 11, 8, "1"); c.r(10, 8, 11, 12, "3")
    c.r(5, 9, 7, 11, "O"); c.r(5, 9, 6, 10, "4"); c.p(6, 10, "w")
    # barrel
    c.r(0, 9, 4, 10, "l"); c.r(0, 9, 0, 10, "L"); c.r(0, 10, 4, 10, "L")
    # little ammo drum
    c.r(11, 5, 13, 8, "L"); c.r(11, 5, 13, 5, "l"); c.p(12, 7, "5")
    c.shadow(0, 15)
    return c.out()


def vine():
    c = C()
    # two leaf-beaked heads on vines facing each other, pruning
    # roots
    c.r(5, 20, 10, 21, "3"); c.r(5, 20, 8, 20, "2")
    # intertwined stems
    seg(c, [(6, 20), (5, 16), (4, 12), (4, 8)], "2", 2)
    seg(c, [(9, 20), (10, 16), (11, 12), (11, 8)], "3", 2)
    c.p(5, 16, "1"); c.p(4, 12, "1")
    # left head: leaf-beak pointing right
    c.ell(5, 6, 3, 2.4, "2"); c.r(7, 5, 10, 6, "1"); c.r(7, 7, 10, 7, "3")
    c.p(8, 6, "O") if False else None
    c.p(4, 5, "y"); c.p(5, 3, "1")
    c.r(1, 3, 3, 4, "g"); c.p(0, 2, "G")
    # right head
    c.ell(11, 5, 3, 2.4, "3"); c.r(6, 3, 9, 4, "2"); c.r(6, 4, 9, 4, "3") if False else None
    c.p(12, 4, "y")
    c.r(13, 1, 15, 2, "g"); c.p(15, 0, "G")
    # spit / seedpack
    c.p(7, 8, "4"); c.p(8, 10, "5"); c.p(7, 12, "4") if False else None
    c.p(8, 13, "4"); c.p(7, 15, "5") if False else None
    c.r(7, 9, 8, 9, "4") if False else None
    c.p(6, 17, "y") if False else None
    c.p(2, 14, "g"); c.p(1, 15, "G"); c.p(13, 15, "g"); c.p(14, 16, "G")
    c.shadow(2, 13)
    return c.out()


def yd_svardym():
    c = C()
    # splayed frog-like folk, flat, spotted limbs flapping unfolded
    for (x0, y0, x1, y1, x2, y2) in ((5, 11, 2, 8, 0, 11), (10, 11, 13, 8, 15, 11),
                                     (6, 15, 3, 18, 1, 21), (9, 15, 12, 18, 14, 21)):
        seg(c, [(x0, y0), (x1, y1), (x2, y2)], "2", 2)
        c.p(x2, y2, "1")
    for (x, y) in ((2, 9), (13, 9), (3, 18), (12, 18), (1, 20), (14, 20), (0, 11), (15, 10)):
        c.p(x, y, "4")
    # torso
    c.r(5, 10, 10, 16, "2"); c.r(5, 10, 6, 16, "1"); c.r(9, 11, 10, 16, "3")
    for (x, y) in ((6, 12), (9, 14), (7, 15), (8, 11)):
        c.p(x, y, "5")
    # orbed head with wide-set eyes + warty ridge
    c.ell(7.5, 6, 4.6, 3.6, "2"); c.ell(6.8, 5.4, 3, 2.2, "1"); c.r(10, 5, 12, 8, "3") if False else None
    c.ell(2.5, 4.6, 1.6, 1.6, "w"); c.ell(12.5, 4.6, 1.6, 1.6, "w")
    c.p(2, 5, "O"); c.p(13, 5, "O"); c.p(3, 5, "O") if False else None
    c.r(3, 5, 4, 5, "2"); c.r(11, 5, 12, 5, "3")
    c.r(7, 2, 8, 4, "6"); c.p(7, 1, "5"); c.p(8, 1, "6"); c.p(7, 3, "4")
    c.r(6, 8, 9, 8, "O"); c.p(8, 9, "3") if False else None
    c.p(6, 9, "3") if False else None
    c.shadow(0, 15)
    return c.out()


SPRITES = {
    "bearman": BEARMAN, "cherub_cannibal": CHERUB_CANNIBAL, "cragmensch_boulderer": CRAG, "esthers": ESTHERS,
    "golem_ape": GOLEM_APE, "golem_slynth": GOLEM_SLYNTH, "hindren": HINDREN, "merchant": MERCHANT,
    "nephilim_bethsaida": BETHSAIDA, "seeker": SEEKER, "slynth_kyakukya": KYAKUKYA, "templar_bearer": BEARER,
    "warden_goatfolk": WARDEN,
}
SPRITES.update({
    "anemone": anemone(), "boosterbot": boosterbot(), "cherub_baetyl_mechanical": cherub_baetyl_mechanical(),
    "cherub_crab_mechanical": cherub_crab_mechanical(), "cherub_flower_mechanical": cherub_flower_mechanical(),
    "cherub_insect_mechanical": cherub_insect_mechanical(),
    "cherub_reptile_mechanical": cherub_reptile_mechanical(),
    "cherub_swine_mechanical": cherub_swine_mechanical(), "cherub_vine_mechanical": cherub_vine_mechanical(),
    "cloneling": cloneling(), "dreamcrungle_dead": dreamcrungle_dead(), "frog": frog(), "goathead": goathead(),
    "golem_bat": golem_bat(), "golem_clam": golem_clam(), "golem_fractus": golem_fractus(),
    "golem_insect": golem_insect(), "golem_oddity": golem_oddity(), "golem_succulent": golem_succulent(),
    "golem_urchin": golem_urchin(), "kah": kah(), "mirthworm": mirthworm(), "nacham": nacham(),
    "natural_weapon_field": natural_weapon_field(), "natural_weapon_leaf": natural_weapon_leaf(),
    "natural_weapon_shovel": natural_weapon_shovel(), "nephilim_rermadon": nephilim_rermadon(),
    "prism": prism(), "robot": robot(), "shroom": shroom(), "starshiib": starshiib(), "swine": swine(),
    "turret_mini": turret_mini(), "vine": vine(), "yd_svardym": yd_svardym(),
})
HUMANOID = {"bearman", "cherub_cannibal", "cragmensch_boulderer", "esthers", "golem_ape", "golem_slynth",
            "hindren", "merchant", "nephilim_bethsaida", "seeker", "slynth_kyakukya", "templar_bearer",
            "warden_goatfolk"}
