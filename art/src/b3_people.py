"""B3 named NPCs and townsfolk (humanoid layout), built on b3kit.person()."""
from functools import partial
import b3kit as K
from b3kit import (C, back, overlay, person, hat_wide, hat_straw, hat_pointy, cap, hood, turban, helmet,
                   helmet_visor, crown, halo, horn_headdress, hair_short, hair_long, hair_wild, hair_mohawk,
                   hair_bun, beard, stubble, spectacles, goggles_up, veil, blindfold, scarf, apron, armor,
                   tunic, cape, pack, quiver, shoulder_scrap, belt_pouches, poncho, staff, spear, bow, sword,
                   hammer, pistol, rifle, club, axe, wrench, gear, book, hoe, sickle, shield, lantern, jug,
                   trident, scroll)
from b3_castes import taur_body, robot_head, flame_staff

P = person


def _tr(ov, table):
    return {y: row.translate(str.maketrans(table)) for y, row in ov.items()}


# ---- parts ---------------------------------------------------------------------------------
def eyes(c, col="c"):
    c.p(6, 5, col); c.p(9, 5, col)


def closed_eyes(c):
    c.p(6, 5, "S"); c.p(9, 5, "S"); c.p(6, 6, "S") if False else None


def mushroom_beard(c, a="w", b="l", s1="r", s2="y", s3="c"):
    """huge mushroom-cloud beard, flecked with trash-sea grit."""
    c.ell(7.5, 8.2, 6.4, 2.8, a)
    c.r(6, 11, 9, 14, a)
    c.r(2, 9, 13, 9, a)
    c.r(10, 9, 13, 10, b)
    c.r(8, 11, 9, 14, b)
    c.r(3, 10, 4, 10, "l") if False else None
    for (x, y, ch) in ((3, 8, s1), (5, 7, s2), (11, 8, s3), (9, 7, s1), (4, 9, s3), (12, 9, s2), (7, 12, s1),
                       (6, 10, s2), (9, 13, s3)):
        c.p(x, y, ch)


def chrome_joints(c):
    c.mr(3, 9, 4, 10, "l")
    c.mr(3, 9, 3, 9, "w")
    c.p(4, 12, "l"); c.p(11, 12, "L"); c.p(4, 14, "L"); c.p(11, 14, "L")
    c.p(3, 15, "l")
    c.r(6, 17, 6, 18, "L"); c.r(9, 17, 9, 18, "L")


def goat_head(c, horn="w", shade="L"):
    """goat head: curling horns, long snout, side ears, goatee."""
    c.r(5, 3, 10, 7, "2")
    c.r(5, 3, 10, 3, "1")
    c.r(10, 4, 10, 7, "3")
    c.r(6, 6, 9, 8, "1")
    c.r(7, 8, 8, 8, "O") if False else None
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.p(6, 5, "y"); c.p(9, 5, "y")
    c.p(6, 4, "O") if False else None
    c.mr(2, 5, 4, 5, "3")
    c.p(3, 6, "S"); c.p(12, 6, "S")
    c.mr(4, 3, 5, 3, horn)
    c.mr(3, 2, 4, 2, horn)
    c.mr(2, 1, 3, 1, horn)
    c.mr(1, 2, 2, 2, shade) if False else None
    c.mr(2, 0, 2, 0, horn)
    c.m(2, 2, shade); c.m(4, 4, shade)
    c.r(7, 9, 8, 10, "w")
    c.p(8, 10, "l")
    c.r(7, 8, 8, 8, "1")


def goat_legs(c, fur="2", dk="3"):
    """fur kilt, thick thighs, hoofed digitigrade legs."""
    c.r(3, 16, 12, 21, ".")
    c.r(4, 16, 11, 17, fur)
    c.r(4, 16, 4, 17, "1"); c.r(11, 16, 11, 17, dk)
    c.r(4, 18, 6, 19, dk); c.r(9, 18, 11, 19, dk)
    c.r(5, 20, 5, 21, dk); c.r(10, 20, 10, 21, dk)
    c.r(4, 22, 5, 22, "O"); c.r(10, 22, 11, 22, "O")
    c.r(3, 22, 3, 22, "O") if False else None


def bare_chest(c, fur="2", hi="1", dk="3"):
    """swollen bare chest and arms."""
    c.r(3, 9, 12, 9, fur)
    c.r(5, 10, 10, 15, fur)
    c.r(3, 10, 4, 14, fur); c.r(11, 10, 12, 14, dk)
    c.r(5, 10, 7, 11, hi)
    c.r(8, 10, 10, 11, fur)
    c.p(7, 12, dk); c.p(8, 12, dk)
    c.r(4, 15, 4, 15, "S"); c.r(11, 15, 11, 15, "S")
    c.p(3, 15, "S"); c.p(12, 15, "S")


def braid_satchel(c, a="N", b="n"):
    c.line(5, 9, 10, 15, a)
    c.line(6, 9, 10, 14, b)
    c.r(2, 15, 4, 17, "n"); c.r(2, 15, 4, 15, "N"); c.p(3, 16, "y")


def horn_instrument(c, a="t", b="w"):
    """long curved horn blown to the right of the head."""
    c.r(8, 7, 11, 8, a)
    c.r(11, 6, 13, 7, a)
    c.r(13, 4, 15, 6, b)
    c.p(15, 3, b); c.r(14, 5, 14, 5, "L")
    c.p(11, 15, "s") if False else None
    c.r(11, 9, 12, 14, "s") if False else None
    c.line(11, 9, 11, 12, "S")


def feather_bonnet(c, a="4", b="5", skull="w"):
    """shaman's skull-and-feather headdress."""
    c.r(5, 3, 10, 3, skull)
    c.p(6, 3, "O"); c.p(9, 3, "O")
    c.p(3, 0, a); c.p(4, 1, a); c.p(4, 0, b); c.p(11, 0, a); c.p(11, 1, a); c.p(12, 0, b)
    c.p(5, 2, b); c.p(10, 2, b); c.p(7, 0, a); c.p(8, 1, a)
    c.r(5, 2, 10, 2, "n")


def seed_bag(c):
    c.r(0, 12, 3, 16, "t")
    c.r(1, 11, 2, 11, "n")
    c.r(0, 16, 3, 16, "n")
    c.p(1, 13, "g"); c.p(2, 14, "G"); c.p(1, 14, "y")
    c.p(4, 15, "s")


def antlers(c, a="n", b="t"):
    c.line(5, 3, 2, 0, a, mirror=True)
    c.line(4, 2, 1, 1, a, mirror=True)
    c.line(5, 2, 3, 0, a, mirror=True) if False else None
    c.m(3, 0, b); c.m(1, 0, b); c.m(0, 1, b)
    c.m(4, 1, b) if False else None
    c.m(5, 3, a)


def small_antlers(c, a="n"):
    c.line(5, 3, 3, 1, a, mirror=True)
    c.m(2, 1, "t"); c.m(4, 1, "t") if False else None
    c.m(5, 3, a)


def deer_ears(c, a="n", b="S"):
    c.mr(2, 4, 4, 4, a)
    c.mr(3, 5, 4, 5, a)
    c.m(3, 4, b)
    c.m(1, 3, a)


def deer_body(c, a="2", b="3", hi="1", spot="4"):
    """deer-folk: slender deer barrel and four long thin legs."""
    c.r(3, 16, 12, 21, ".")
    c.r(1, 15, 13, 18, a)
    c.r(3, 14, 12, 14, a)
    c.r(1, 15, 13, 15, hi)
    c.r(11, 16, 13, 18, b)
    c.r(1, 18, 13, 18, b)
    for (x, y) in ((3, 16), (6, 17), (9, 16), (5, 16), (11, 17)):
        c.p(x, y, spot)
    for x in (1, 3, 10, 12):
        c.r(x, 19, x, 21, "n" if x < 5 else "N")
        c.p(x, 22, "O")
    c.r(14, 15, 15, 16, "w")
    c.p(15, 17, "w")
    c.shadow(0, 15)


def great_taur(c, a="2", b="3", hi="1"):
    """big four-legged warden body."""
    c.r(3, 16, 12, 21, ".")
    c.r(0, 13, 14, 18, a)
    c.r(2, 12, 13, 12, a)
    c.r(0, 13, 14, 13, hi)
    c.r(10, 14, 14, 18, b)
    c.r(0, 18, 14, 18, b)
    c.r(5, 15, 9, 16, "5")
    for x in (0, 3, 10, 13):
        c.r(x, 19, x + 1, 21, a if x < 5 else b)
        c.r(x, 22, x + 1, 22, "O")
    c.r(15, 14, 15, 18, "6")
    c.p(14, 19, "6"); c.p(15, 19, "6")
    c.shadow(0, 15)


def great_horns(c, a="w", b="L"):
    """huge branching antler-horns spanning the whole tile."""
    c.r(5, 3, 5, 3, a); c.r(10, 3, 10, 3, a)
    c.line(4, 3, 1, 3, a, mirror=True)
    c.line(1, 3, 0, 1, a, mirror=True)
    c.line(2, 3, 2, 0, a, mirror=True)
    c.line(4, 3, 4, 0, a, mirror=True)
    c.line(3, 2, 3, 1, b, mirror=True)
    c.m(0, 0, b)
    c.m(1, 4, b)
    c.m(1, 3, b)


def crown_mane(c, a="n"):
    c.r(5, 3, 10, 3, "N")
    c.r(4, 4, 4, 8, a); c.r(11, 4, 11, 8, a)
    c.r(5, 8, 10, 8, a)


def scars(c):
    c.p(10, 6, "R"); c.p(9, 6, "R")


def bear_head(c):
    """bear snout, round ears."""
    c.r(5, 2, 10, 2, "2") if False else None
    c.mr(4, 2, 5, 3, "2")
    c.m(5, 3, "S") if False else None
    c.r(5, 3, 10, 7, "2")
    c.r(10, 4, 10, 7, "3")
    c.r(6, 6, 9, 8, "1")
    c.r(7, 6, 8, 7, "O") if False else None
    c.p(7, 7, "O"); c.p(8, 7, "O"); c.p(7, 8, "L") if False else None
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.m(4, 2, "3")


def fingers(c):
    """long triple-jointed fingers."""
    c.p(3, 15, "S"); c.p(2, 16, "S"); c.p(3, 17, "S"); c.p(1, 17, "S") if False else None
    c.p(12, 15, "S"); c.p(13, 16, "S"); c.p(12, 17, "S")
    c.p(4, 16, "S"); c.p(11, 16, "S")


def pointy_hood(c, a="2", lite="1", dark="3"):
    hood(c, a, lite, dark)


def keffiyeh(c, a="4", b="5", rope="O"):
    """head cloth with side drapes."""
    c.r(6, 1, 9, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(4, 3, 11, 3, a)
    c.r(4, 3, 11, 3, a)
    c.r(5, 3, 10, 3, rope)
    c.r(4, 4, 4, 9, a); c.r(11, 4, 11, 9, b)
    c.r(4, 8, 5, 9, b); c.p(10, 8, b)
    c.p(6, 1, "w")


def top_hat(c, a="2", band="4"):
    c.r(6, 0, 9, 2, a)
    c.r(6, 2, 9, 2, band)
    c.r(4, 3, 11, 3, a)
    c.p(6, 0, "1")


def bundle(c):
    """sheaf of watervine."""
    c.r(0, 12, 3, 17, "g")
    c.r(1, 11, 2, 11, "G")
    c.line(0, 12, 0, 16, "G")
    c.r(0, 15, 3, 15, "n")
    c.p(4, 15, "s"); c.p(3, 15, "n")
    c.p(2, 13, "h"); c.p(1, 16, "h")


def basket(c):
    c.r(0, 15, 4, 18, "n")
    c.r(0, 15, 4, 15, "N")
    c.r(1, 13, 3, 14, "r")
    c.p(2, 13, "w"); c.p(1, 14, "R"); c.p(3, 14, "R")
    c.p(4, 14, "s"); c.p(4, 13, "N")
    c.line(0, 15, 2, 12, "t") if False else None


def gloves(c):
    c.r(0, 13, 2, 16, "n"); c.r(1, 12, 1, 12, "n")
    c.p(0, 12, "N"); c.p(2, 12, "N")
    c.r(2, 14, 3, 17, "t")
    c.p(4, 15, "s")
    c.p(8, 7, "l") if False else None


def needle(c):
    c.line(10, 7, 14, 6, "l")
    c.p(14, 6, "w")


def gem_held(c, a="B"):
    c.p(2, 12, "w"); c.r(1, 13, 3, 14, a); c.p(2, 15, a); c.p(2, 13, "w")
    c.p(0, 13, "w") if False else None
    c.p(4, 15, "s"); c.p(3, 15, "s")


def hide_poncho(c):
    """patchwork of hides."""
    c.r(3, 9, 12, 14, "n")
    c.r(4, 15, 11, 17, "n")
    c.r(3, 9, 6, 11, "t"); c.r(9, 11, 12, 13, "N"); c.r(6, 12, 8, 14, "S"); c.r(4, 14, 6, 16, "N")
    c.r(9, 15, 11, 17, "t"); c.p(7, 10, "N")
    c.line(3, 9, 12, 17, "N") if False else None
    for x in (3, 5, 8, 10, 4, 11):
        c.p(x, 17 if x in (4, 11, 5, 8) else 14, "n")
    c.p(7, 9, "S"); c.p(8, 9, "S")


def bone_necklace(c, a="w"):
    for x in (5, 7, 9):
        c.p(x, 9, a)
    c.p(6, 10, a); c.p(8, 10, a); c.p(7, 11, a)


def bone_club(c):
    club(c, spikes=False)
    c.r(12, 4, 14, 9, "w")
    c.p(13, 3, "w"); c.p(12, 5, "t"); c.p(13, 7, "t"); c.p(14, 6, "l")
    c.p(11, 5, "w"); c.p(15, 6, "w")


def fangs(c):
    c.p(6, 7, "w"); c.p(9, 7, "w"); c.p(7, 7, "R"); c.p(8, 7, "R")


def huge_arm(c):
    """grotesquely swollen right arm."""
    c.r(10, 9, 14, 15, "S")
    c.r(11, 10, 13, 12, "s")
    c.r(10, 9, 14, 9, "s")
    c.p(14, 11, "R"); c.p(13, 14, "R"); c.p(12, 13, "S")
    c.r(11, 15, 14, 17, "S")
    c.line(11, 11, 14, 14, "R")


def moss_fur(c):
    c.rows(_tr(K.MUTATIONS["ThickFur"][1], {"n": "g", "N": "h"}))


def white_fur(c):
    c.rows(_tr(K.MUTATIONS["ThickFur"][1], {"n": "w", "N": "l"}))


def tabard(c, a="5", b="4"):
    c.r(6, 10, 9, 20, a)
    c.r(7, 10, 8, 20, b)
    c.r(6, 13, 9, 13, b)
    c.p(5, 10, "l") if False else None


def mail_coif(c):
    """chain coif with a salient jaw."""
    c.r(5, 2, 10, 3, "l"); c.r(4, 4, 5, 8, "L"); c.r(10, 4, 11, 8, "L")
    c.r(6, 2, 7, 2, "w"); c.p(5, 3, "w")
    c.r(6, 8, 9, 8, "L")
    for (x, y) in ((4, 5), (11, 6), (4, 7), (10, 4)):
        c.p(x, y, "l")


def tall_plume(c, a="4", b="5"):
    c.r(7, 0, 8, 1, a)
    c.p(6, 1, b); c.p(9, 1, b); c.p(7, 0, "w")
    c.p(5, 2, b); c.p(10, 2, b)


def hang_pouches(c):
    for (x, y) in ((4, 12), (11, 13), (5, 16), (10, 17)):
        c.r(x, y, x + 1, y + 1, "n"); c.p(x, y, "N")
    c.p(7, 14, "y")


def pistons(c):
    c.r(3, 16, 12, 21, ".")
    c.r(4, 16, 11, 17, "L")
    c.r(5, 18, 6, 21, "l"); c.r(9, 18, 10, 21, "l")
    c.r(5, 19, 6, 19, "L"); c.r(9, 19, 10, 19, "L")
    c.r(5, 21, 6, 21, "L"); c.r(9, 21, 10, 21, "L")
    c.r(4, 22, 7, 22, "O"); c.r(8, 22, 11, 22, "O")
    c.p(6, 18, "w"); c.p(9, 18, "w")


def cylinder_head(c):
    """cylindrical chrome head with a frilly crest."""
    c.r(5, 3, 10, 8, "l")
    c.r(10, 3, 10, 8, "L"); c.r(5, 8, 10, 8, "L")
    c.r(5, 3, 10, 3, "w")
    c.r(6, 5, 9, 5, "O"); c.p(6, 5, "R"); c.p(9, 5, "R")
    c.r(7, 6, 8, 7, "L")
    c.r(5, 2, 10, 2, "4")
    c.p(4, 1, "4"); c.p(5, 1, "5"); c.p(7, 0, "4"); c.p(8, 1, "5"); c.p(10, 1, "4"); c.p(11, 1, "5")
    c.p(6, 0, "5"); c.p(9, 0, "5"); c.p(7, 1, "4"); c.p(6, 1, "5") if False else None


def blast_cannon(c):
    c.r(10, 11, 15, 14, "L")
    c.r(10, 11, 15, 11, "l")
    c.r(14, 12, 15, 13, "O")
    c.p(11, 12, "R"); c.p(12, 12, "R")
    c.r(11, 15, 11, 15, "l")


def pipes(c):
    """organ choraler pipes behind the shoulders."""
    for x, y0 in ((1, 4), (2, 2), (3, 6)):
        c.m(x, y0, "w")
        c.r(x, y0 + 1, x, 11, "l"); c.r(15 - x, y0 + 1, 15 - x, 11, "L")
        c.p(x, y0, "w")
    c.m(2, 12, "O"); c.m(1, 11, "O") if False else None


def wide_sleeves(c, a="2", b="4", hi="1"):
    """long sleeves flaring out, arms held wide."""
    c.r(4, 10, 4, 15, ".") if False else None
    c.mr(1, 10, 4, 11, a)
    c.mr(0, 12, 3, 15, a)
    c.mr(1, 10, 3, 10, hi)
    c.r(0, 15, 3, 15, b); c.r(12, 15, 15, 15, b)
    c.m(1, 9, "s"); c.m(0, 9, "S")
    c.m(2, 16, "O") if False else None


def orchids(c):
    """star orchids on hood and hem."""
    for (x, y) in ((4, 2), (11, 3), (6, 1), (9, 8), (3, 18), (12, 17), (5, 21), (10, 20), (8, 14)):
        c.p(x, y, "M")
        c.p(x - 1, y, "m") if x > 0 else None
        c.p(x + 1, y, "m")
        c.p(x, y - 1, "m")
        c.p(x, y + 1, "m")
    c.p(11, 3, "y"); c.p(4, 2, "y"); c.p(3, 18, "y")


def crystal(c, a="B", b="c", d="b"):
    """eight-faceted crystal body with prism-limbs."""
    c.r(3, 9, 12, 21, ".")
    c.r(5, 3, 10, 8, ".")
    # faceted head
    for y, (x0, x1) in enumerate(((7, 8), (6, 9), (5, 10), (5, 10), (6, 9), (7, 8)), start=2):
        c.r(x0, y, x1, y, a)
    c.r(8, 4, 10, 6, b); c.r(8, 3, 9, 3, b)
    c.p(7, 4, "w"); c.p(6, 4, "w"); c.p(7, 5, "O"); c.p(9, 5, "O") if False else None
    c.p(6, 4, "O"); c.p(9, 4, "O") if False else None
    # diamond torso
    for y, (x0, x1) in enumerate(((7, 8), (5, 10), (4, 11), (4, 11), (5, 10), (5, 10), (6, 9), (6, 9), (7, 8),
                                  (7, 8), (6, 9), (5, 10)), start=9):
        c.r(x0, y, x1, y, a)
    c.r(8, 9, 11, 17, b)
    c.r(9, 10, 11, 14, d)
    c.line(4, 11, 7, 17, "w") if False else None
    c.p(6, 11, "w"); c.p(5, 12, "w"); c.p(7, 10, "w")
    c.p(7, 13, "4"); c.p(8, 13, "4"); c.p(7, 14, "4"); c.p(8, 14, "4")
    # prism limbs
    for (x0, y0, x1, y1) in ((4, 10, 0, 7), (4, 12, 0, 12), (4, 14, 1, 18), (5, 17, 3, 22), (6, 19, 6, 22)):
        c.line(x0, y0, x1, y1, a, mirror=True)
        c.line(x0 + 1, y0, x1 + 1, y1, b, mirror=True)
    c.m(0, 7, "w"); c.m(0, 12, "w"); c.m(1, 18, "w"); c.m(3, 22, "w")
    c.r(7, 20, 8, 22, a) if False else None
    c.shadow(2, 13)


def kittel_pleats(c, a="w", b="l"):
    """white pleated kittel."""
    c.r(4, 9, 11, 9, a)
    for x in (6, 8, 10):
        c.r(x, 16, x, 21, b)
    for x in (5, 7, 9):
        c.r(x, 10, x, 15, b) if False else None


def tallith(c):
    """strata-striped prayer shawl + circuit-board shoulder pads."""
    c.r(3, 9, 12, 11, "5")
    for y, ch in ((9, "4"), (10, "6"), (11, "4")):
        c.r(3, y, 12, y, ch)
    c.line(5, 12, 9, 20, "5"); c.line(6, 12, 10, 20, "6")
    c.r(3, 12, 4, 14, "4"); c.r(11, 12, 12, 14, "6")
    c.r(2, 9, 4, 10, "g"); c.r(11, 9, 13, 10, "g"); c.p(3, 9, "y"); c.p(12, 10, "y")
    c.p(4, 5, "c"); c.p(11, 5, "c")


def pointed_turban(c, a="w", b="l"):
    c.p(7, 0, b); c.p(8, 0, a)
    c.r(6, 1, 9, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(5, 3, 10, 3, b)
    c.p(7, 1, "4"); c.p(6, 2, "L") if False else None


def dervish_skirt(c, a="2", b="1"):
    """wide spinning skirt."""
    c.r(3, 16, 12, 21, ".")
    c.r(2, 15, 13, 17, a)
    c.r(1, 18, 14, 20, a)
    c.r(0, 21, 15, 21, b)
    c.r(0, 18, 3, 21, b)
    c.r(13, 18, 15, 21, "3")
    c.r(1, 19, 14, 19, "3") if False else None
    for x in (4, 7, 11):
        c.r(x, 17, x, 21, "3")
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.shadow(0, 15)


def arms_out(c):
    c.r(4, 10, 4, 15, ".")
    c.r(11, 10, 11, 15, ".")
    c.mr(0, 10, 4, 11, "2")
    c.m(0, 10, "s"); c.m(0, 11, "S")
    c.m(2, 12, "2") if False else None
    c.p(4, 12, "2"); c.p(11, 12, "3")


def hindren_tail(c):
    pass


# ---- the folk --------------------------------------------------------------------------------
KIT = {
    # kufiya cowl, sackcloth habit, watervine sheaf
    "convert": P(hood, tunic, bundle, scarf, trim="4"),
    # wind-carved vinereaper, turquoise eyes, hoe, turban
    "mehmet": P(pack if False else turban, beard, hoe, tunic, eyes, face="face", sash=False),
    # mushroom-cloud beard, chrome joints, goggles-up
    "argyve": P(hair_wild, goggles_up, chrome_joints, mushroom_beard, wrench, sash=False),
    # old, hunched smiling elder, white wild hair, drum-stick staff
    "irudad": P(hair_wild, staff, scarf, face="face", trim="4"),
    # big horned warden on four legs
    "yrame": P(great_taur, great_horns, crown_mane, armor, spear, sash=False),
    # scorpion tail + stinger, jade eyes, burned lips
    "nima": P(overlay(K.MUTATIONS["Stinger"][1], behind=True), hair_long, scars, poncho, eyes, sash=False),
    # pale cannibal: bone necklace, bone club, pelt kilt
    "cannibal": P(hair_mohawk, bone_necklace, tunic, bone_club, fangs, face="face", sash=False),
    # moss-fur forager in a mask
    "naphtaali": P(moss_fur, hood, veil, face="face", trim="4", sash=False),
    # knight: mail coif, tabard, sword
    "templar": P(mail_coif, armor, tabard, sword, sash=False),
    "templar_gunner": P(helmet_visor, armor, tabard, rifle, sash=False),
    "templar_squire": P(cap, tunic, tabard, lantern, face="face", sash=False),
    # bear-snouted, quilled
    "barathrumite": P(overlay(K.MUTATIONS["Quills"][1], behind=True), bear_head, white_fur, fingers, staff,
                      sash=False),
}

KIT2 = {
    "goatfolk": P(goat_legs, bare_chest, goat_head, braid_satchel, club, face="none", sash=False),
    "goatfolk_shaman": P(goat_legs, bare_chest, goat_head, feather_bonnet, staff, face="none", sash=False),
    "goatfolk_sower": P(goat_legs, bare_chest, goat_head, hat_straw, seed_bag, sickle, face="none", sash=False),
    "goatfolk_hunter": P(quiver, goat_legs, bare_chest, goat_head, bow, face="none", sash=False),
    "goatfolk_hornblower": P(goat_legs, bare_chest, goat_head, horn_instrument, face="none", sash=False),
    "hermit": P(hair_wild, hide_poncho, beard, staff, face="face", sash=False),
    "apple_daughter": P(hair_long, cap, basket, face="face", trim="4"),
    "raider": P(keffiyeh, sword, face="wrap", trim="4"),
    "raider_rifle": P(keffiyeh, poncho, rifle, face="wrap", trim="4", sash=False),
    "pilgrim": P(hat_wide, scarf, pack, staff, tunic, face="face", sash=False),
    "turret_tinker": P(pistons, cylinder_head, blast_cannon, face="none", sash=False),
}

KIT3A = {
    "mopango_delver": P(hood, hang_pouches, overlay(K.MUTATIONS["Carapace"][1]), lantern, face="face"),
    "mopango_villager": P(hood, overlay(K.MUTATIONS["Carapace"][1]), halo, staff, face="face"),
    "mechanimist": P(hood, gear, staff, face="mask", sash=True, trim="4"),
    "mechanimist_preacher": P(pipes, wide_sleeves, hat_pointy, book, face="face", trim="4"),
    "hindren_villager": P(deer_body, small_antlers, deer_ears, tunic if False else scarf, face="face", sash=False),
    "hindren_farmer": P(deer_body, antlers, deer_ears, hoe, face="face", sash=False),
    "hindren_scout": P(deer_body, deer_ears, bow, cap, face="face", sash=False),
    "gyre_wight": P(hood, orchids, wide_sleeves, face="face", trim="4"),
    "merchant_hatter": P(top_hat, apron, gem_held, spectacles, face="face", sash=False),
    "merchant_shoemaker": P(cap, apron, gloves, needle, face="face", sash=False),
    "tau": P(crystal, face="none", sash=False),
    "novice": P(closed_eyes, kittel_pleats, scarf, face="face", trim="5"),
}

KIT3B = {
    "rancher": P(hair_short, hat_straw, tunic, staff, face="face", sash=False),
    "cannibal": P(hair_mohawk, huge_arm, fangs, tunic, club, face="face", sash=False),
    "knight": P(cape, partial(helmet, crest=True), tall_plume, armor, tabard, sword, sash=False),
    "dervish": P(dervish_skirt, arms_out, pointed_turban, closed_eyes, face="face", sash=False),
    "abbot": P(tallith, hair_bun, beard, staff, face="face", sash=False),
    "disciple": P(hood, closed_eyes, kittel_pleats, staff, face="face", trim="5"),
}

OVERRIDES = {"kit": KIT, "kit2": KIT2, "kit3a": KIT3A, "kit3b": KIT3B}
