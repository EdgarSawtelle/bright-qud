"""B3 callings / castes / special humanoids + the player tiles, all built on b3kit.person()."""
from functools import partial
from b3kit import (C, back, person, LOOKS, hat_wide, hat_straw, hat_pointy, cap, hood, turban, helmet,
                   helmet_visor, crown, halo, sun_halo, moon_crown, horn_headdress, hair_short, hair_long,
                   hair_wild, hair_mohawk, hair_bun, beard, stubble, spectacles, goggles_up, veil, blindfold,
                   scarf, apron, armor, tunic, cape, pack, quiver, shoulder_scrap, belt_pouches, poncho,
                   staff, spear, bow, sword, hammer, pistol, dual_pistols, rifle, club, axe, wrench, gear,
                   book, hoe, sickle, shield, lantern, jug, trident, scroll)


# ---- local parts used by a few special castes -------------------------------------------------
def leaf_hair(c, a="g", b="G", d="h"):
    """crown of leaves."""
    c.p(5, 0, b); c.p(8, 0, b); c.p(10, 0, b)
    c.r(4, 1, 11, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(5, 3, 10, 3, d)
    c.p(7, 0, a); c.p(6, 1, b); c.p(9, 1, b); c.p(3, 2, a); c.p(12, 2, a); c.p(4, 3, a); c.p(11, 3, a)
    c.p(4, 4, d); c.p(11, 4, d); c.p(3, 3, b); c.p(12, 3, b)


def flame_hair(c):
    """hair of living flame."""
    c.p(5, 0, "r"); c.p(8, 0, "y"); c.p(10, 0, "r")
    c.r(4, 1, 11, 1, "r")
    c.p(6, 1, "y"); c.p(9, 1, "y")
    c.r(4, 2, 11, 2, "r")
    c.r(6, 2, 9, 2, "y")
    c.r(5, 3, 10, 3, "r")
    c.p(7, 3, "y"); c.p(8, 3, "y")
    c.p(3, 1, "y"); c.p(12, 2, "y"); c.p(3, 3, "r"); c.p(12, 3, "r"); c.p(4, 4, "r"); c.p(11, 4, "r")
    c.p(7, 0, "y")


def fish_fins(c, a="c", b="B"):
    """head fins and gills of the deep."""
    c.r(6, 1, 9, 1, a); c.r(7, 0, 8, 0, a); c.r(5, 2, 10, 2, b)
    c.p(7, 1, b); c.p(8, 1, b)
    c.mr(3, 4, 4, 6, a)
    c.m(3, 5, b)
    for y in (10, 12, 14):
        c.m(5, y, a)


def star_eye(c):
    """one great glowing star-shaped eye replaces the face."""
    c.r(5, 4, 10, 7, "S")
    c.r(6, 4, 9, 7, "s")
    c.r(6, 5, 9, 6, "4")
    c.r(7, 4, 8, 7, "4")
    c.r(7, 5, 8, 6, "w")
    c.p(7, 5, "O"); c.p(8, 6, "O") if False else None
    c.p(5, 5, "4"); c.p(10, 5, "4")
    c.p(7, 3, "4"); c.p(8, 3, "4")
    c.p(7, 8, "4") if False else None


def robot_head(c, glow="4"):
    """boxy chrome head, glowing visor."""
    c.r(5, 2, 10, 8, "l")
    c.r(5, 2, 10, 2, "w")
    c.r(10, 3, 10, 8, "L")
    c.r(5, 8, 10, 8, "L")
    c.r(6, 4, 9, 6, "O")
    c.r(6, 5, 9, 5, glow)
    c.p(7, 5, "w"); c.p(7, 8, "O"); c.p(8, 8, "O")
    c.r(7, 7, 8, 7, "L")
    c.p(7, 0, "L"); c.p(7, 1, "L"); c.p(7, 0, glow)
    c.r(7, 8, 8, 8, "L")


@back
def shell(c, a="5", b="4", d="6"):
    """big domed tortoise shell behind the shoulders."""
    c.ell(7.5, 14.5, 8.3, 7.2, d)
    c.ell(7.5, 14.5, 7.4, 6.3, a)
    for (x, y) in ((4, 11), (7, 10), (11, 11), (3, 15), (7, 14), (12, 15), (5, 18), (10, 18)):
        c.r(x - 1, y, x + 1, y + 1, b)
    c.p(7, 10, "w")


def taur_body(c, a="2", b="3", lt="1"):
    """horse-like barrel and four legs instead of a robe skirt."""
    c.r(3, 16, 12, 21, ".")
    c.r(1, 15, 14, 19, a)
    c.r(2, 14, 13, 14, a)
    c.r(1, 15, 14, 15, lt)
    c.r(11, 16, 14, 19, b)
    c.r(1, 19, 14, 19, b)
    c.r(1, 20, 2, 22, a); c.r(4, 20, 5, 22, b)
    c.r(10, 20, 11, 22, a); c.r(13, 20, 14, 22, b)
    c.r(1, 22, 2, 22, "O"); c.r(4, 22, 5, 22, "O"); c.r(10, 22, 11, 22, "O"); c.r(13, 22, 14, 22, "O")
    c.p(0, 15, b); c.p(15, 16, b); c.p(15, 17, b)  # tail
    c.shadow(1, 14)


def flame_staff(c):
    staff(c, head="none")
    c.r(12, 1, 14, 3, "r"); c.p(13, 0, "y"); c.p(13, 1, "y"); c.p(13, 2, "y"); c.p(12, 4, "r"); c.p(14, 4, "r")
    c.p(13, 3, "y")


def praetorian_helm(c):
    helmet(c, crest=True, plume="r")


def sun_star(c):
    """gold sun emblem on the chest."""
    c.r(7, 11, 8, 12, "y")
    c.p(6, 11, "y"); c.p(9, 12, "y"); c.p(7, 10, "w")


def moon_chest(c):
    c.p(7, 11, "l"); c.p(7, 12, "l"); c.p(8, 10, "l"); c.p(8, 13, "l")


def circlet(c, a="y", gem="4"):
    """jeweled circlet with a tall plume."""
    c.r(5, 3, 10, 3, a)
    c.p(7, 3, gem); c.p(8, 3, gem)
    c.r(7, 0, 8, 2, gem)
    c.p(7, 0, "w")
    c.p(6, 2, a); c.p(9, 2, a)


def tabard(c, a="5", b="4"):
    c.r(6, 10, 9, 20, a)
    c.r(7, 10, 8, 20, b)
    c.p(7, 13, "y"); c.p(8, 13, "y")


# ---- the callings ----------------------------------------------------------------------------
P = person
CASTES = {
    # Horticulturist: leafy crown, apron, hoe
    "creatures/caste/1": P(leaf_hair, apron, hoe),
    # Priest of All Suns: radiant sun halo, bald, staff
    "creatures/caste/2": P(sun_halo, sun_star, staff, trim="4"),
    # Priest of All Moons: long hair, moon crown, book
    "creatures/caste/3": P(hair_long, moon_crown, moon_chest, book, trim="5"),
    # Syzygyrior: steel helm, armor, long cape, sword
    "creatures/caste/4": P(cape, partial(helmet, crest=False), armor, sword, sash=False),
    # Artifex: goggles, apron, big cog
    "creatures/caste/5": P(hair_short, goggles_up, apron, gear, face="face", sash=False),
    # Consul: crown, rich cape, scroll
    "creatures/caste/6": P(cape, crown, scroll, face="face", trim="4"),
    # Praetorian: crested helm, armor, shield, spear
    "creatures/caste/7": P(praetorian_helm, armor, shield, spear, sash=False),
    # Eunuch: veiled, bald, soft robe + scarf
    "creatures/caste/8": P(circlet, veil, scarf, trim="4", sash=True),
    # Child of the Hearth (Armorer): flame hair, apron, hammer
    "creatures/caste/9": P(flame_hair, apron, hammer, sash=False),
    # Child of the Wheel: goggles, armor, wrench
    "creatures/caste/10": P(hair_short, armor, wrench, face="goggles", sash=False),
    # Child of the Deep: hood, fins, trident
    "creatures/caste/11": P(hood, fish_fins, trident, trim="5"),
    # Fuming God-Child: flame hair, flaring cape, fire in the hands
    "creatures/caste/12": P(cape, flame_hair, flame_staff, trim="4"),
    # Apostle (sightless): blindfolded, hooded, staff
    "creatures/caste/13": P(hood, blindfold, staff, face="none", trim="5"),
    # Arconaut: hooded, goggles, scrap pack, lantern
    "creatures/caste/14": P(pack, hood, lantern, belt_pouches, face="goggles", sash=False),
    # Greybeard: bald, long white beard, book (Apothecary)
    "creatures/caste/15": P(beard, book, face="face", trim="5"),
    # Gunslinger: low hat, wrapped, poncho, pistol
    "creatures/caste/16": P(poncho, hat_wide, pistol, face="wrap", sash=False),
    # Marauder: horned headdress, wild armor, axe
    "creatures/caste/17": P(horn_headdress, shoulder_scrap, belt_pouches, axe, face="face", sash=False),
    # Pilgrim
    "creatures/caste-pilgrim": P(turban, scarf, staff, face="face", trim="5"),
    # Nomad: wide hat, face wrap, pack, spear
    "creatures/caste/19": P(pack, hat_wide, spear, face="wrap", trim="5"),
    # Scholar: spectacles, hair, robe, scroll + book
    "creatures/caste/20": P(hair_bun, spectacles, book, face="face", trim="4"),
    # Tinker: wild grey hair, goggles up, apron, wrench
    "creatures/caste/21": P(pack, hair_wild, goggles_up, apron, wrench, face="face", sash=False),
    # Warden: peaked cap, long bow, quiver
    "creatures/caste/22": P(quiver, cap, bow, shoulder_scrap, face="face", sash=True, trim="5"),
    # Water Merchant: turban, waterjug, patchwork cloak
    "creatures/caste/23": P(cape, turban, jug, face="face", trim="5"),
    # Watervine Farmer: straw hat, apron, hoe
    "creatures/caste/24": P(hat_straw, tunic, hoe, face="face", sash=False),
    "creatures/sw/praetorian/prime": P(cape, crown, armor, shield, spear, sash=False),
    "creatures/sw/first/horticulturalist": P(leaf_hair, beard, hoe, face="face", trim="5"),
    "creatures/sw/first/child/of/the/hearth": P(flame_hair, flame_staff, apron, sash=False),
    "creatures/sw/marsh/taur": P(taur_body, hair_long, spear, face="face", sash=False),
    "creatures/sw/dream/tortoise": P(shell, hair_bun, staff, face="face", trim="4"),
    "creatures/sw/stareye/esper": P(hood, star_eye, face="none", trim="4"),
    "creatures/sw/firefrond": P(leaf_hair, flame_hair, face="face", trim="5"),
    "creatures/sw/bzzzt": P(robot_head, armor, rifle, face="none", sash=False),
}

TILES = {
    "gunwing": LOOKS["Gunslinger"],
    "adventurer": LOOKS["Adventurer"],
    "farmer": P(hat_straw, apron, sickle, face="face", sash=False),
}

OVERRIDES = {"castes": CASTES, "tiles": TILES}
