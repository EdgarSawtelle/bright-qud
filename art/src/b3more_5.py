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
    c.p(6, 5, "W") ; c.p(9, 5, "W")
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

SPRITES = {
    "bearman": BEARMAN, "cherub_cannibal": CHERUB_CANNIBAL, "cragmensch_boulderer": CRAG, "esthers": ESTHERS,
    "golem_ape": GOLEM_APE, "golem_slynth": GOLEM_SLYNTH, "hindren": HINDREN, "merchant": MERCHANT,
    "nephilim_bethsaida": BETHSAIDA, "seeker": SEEKER, "slynth_kyakukya": KYAKUKYA, "templar_bearer": BEARER,
    "warden_goatfolk": WARDEN,
}
HUMANOID = set(SPRITES)
