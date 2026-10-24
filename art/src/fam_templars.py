"""Putus Templar family: chain-mailed crusader knights on the B3 humanoid (b3kit.person)."""
from functools import partial
from b3kit import person, back, tunic

KEYS = {
    "creatures/sw/templar": "templar_knight",
    "creatures/sw/templar/gunner": "templar_gunner",
    "creatures/sw/templar/bearer": "templar_bearer",
    "creatures/sw/templar/leader": "templar_commander",
    "creatures/sw/templar/squire": "templar_squire",
    "creatures/chiliad-templar": "templar_chiliad",
}


def P(*parts, **kw):
    kw.setdefault("sash", False)
    return person(*parts, **kw)


# ---- body ------------------------------------------------------------------------------------
def mail(c, hem=False):
    """light chain-mail texture over the steel body (rows 9-21)."""
    for y in range(10, 22):
        for x in range(3, 13):
            if c.g[y][x] == "l" and (x + 2 * y) % 4 == 0:
                c.g[y][x] = "L"
            elif c.g[y][x] == "l" and (x + 2 * y) % 8 == 3 and x < 8:
                c.g[y][x] = "w"
    c.r(5, 9, 10, 9, "L")
    c.r(6, 9, 7, 9, "l")
    if hem:
        for y in (15, 18, 20):
            c.r(4 if y == 15 else 3, y, 11 if y == 15 else 12, y, "L")
            for x in range(4, 12, 2):
                c.p(x, y + 1 if y != 20 else y, "l")


def tabard(c, a="2", lo="1", dk="3", end=20, belt=True):
    c.r(6, 10, 9, end, a)
    c.r(6, 10, 6, end, lo)
    c.r(9, 10, 9, end, dk)
    c.p(7, end, dk); c.p(8, end, dk)
    c.r(6, end + 1, 9, end + 1, ".") if False else None
    if belt:
        c.r(5, 15, 10, 15, "N")
        c.p(7, 15, "y"); c.p(8, 15, "y")


def rhombus(c, y=11, big=True):
    """Holy Rhombus: faceted filled diamond in the detail colour (cols 6-9)."""
    c.r(7, y, 8, y, "4")
    c.r(6, y + 1, 9, y + 1, "4")
    c.r(6, y + 2, 9, y + 2, "5")
    c.r(7, y + 3, 8, y + 3, "5")
    c.p(9, y + 2, "6"); c.p(8, y + 3, "6")


def pauldrons(c, big=False):
    c.mr(3, 9, 4, 10, "l")
    c.p(3, 9, "w"); c.p(12, 9, "L"); c.p(11, 10, "L"); c.p(12, 10, "L"); c.p(11, 9, "L")
    c.p(3, 10, "L")
    if big:
        c.mr(2, 9, 2, 10, "l"); c.p(13, 9, "L"); c.p(13, 10, "L"); c.p(2, 8, "l"); c.p(13, 8, "L")
        c.p(2, 9, "w")


# ---- heads -----------------------------------------------------------------------------------
def coif_helm(c):
    """open nasal helm over a mail coif; pale sneering face with a jutting jaw."""
    c.r(6, 2, 9, 2, "l")
    c.r(5, 3, 10, 3, "l")
    c.p(6, 2, "w"); c.p(5, 3, "w")
    c.p(10, 3, "L"); c.p(9, 2, "L")
    c.r(7, 3, 8, 4, "L")          # nasal bar
    c.p(7, 4, "l") if False else None
    c.r(4, 4, 5, 8, "L")          # coif sides
    c.r(10, 4, 11, 8, "L")
    c.p(4, 5, "l"); c.p(5, 6, "l"); c.p(4, 7, "l"); c.p(11, 6, "l"); c.p(10, 5, "l")
    c.p(5, 4, "l")
    c.r(6, 4, 6, 7, "s"); c.r(9, 4, 9, 7, "S")
    c.p(7, 5, "s"); c.p(8, 5, "s")
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(7, 6, 8, 6, "s")
    c.r(7, 7, 8, 7, "R")          # wet rosy sneer
    c.p(6, 7, "s"); c.p(9, 7, "S")
    c.r(5, 8, 10, 8, "L")
    c.p(7, 8, "l"); c.p(8, 8, "S")
    c.p(6, 8, "S")                # jutting chin catches the edge


def bare_coif(c):
    """no nasal bar: soft mail hood."""
    c.r(7, 3, 8, 4, "l")
    c.r(6, 2, 9, 2, "L")
    c.p(6, 2, "l"); c.p(7, 2, "w")


def great_helm(c, slit="w"):
    """closed flat-topped great helm, cross-shaped slit, rhombus on the brow."""
    c.r(6, 1, 9, 1, "L")
    c.r(5, 2, 10, 7, "l")
    c.r(10, 2, 10, 7, "L")
    c.r(5, 7, 10, 7, "L")
    c.r(6, 1, 7, 1, "l")
    c.p(5, 2, "w"); c.p(6, 2, "w"); c.p(5, 3, "w")
    c.r(6, 5, 9, 5, "O")          # eye slit
    c.r(7, 3, 8, 7, "O") if False else None
    c.p(7, 4, "O"); c.p(7, 6, "O"); c.p(7, 7, "O")    # vertical slit (cross)
    c.p(9, 7, "L")
    c.p(6, 5, slit); c.p(9, 5, slit)
    c.r(4, 8, 11, 8, "L")
    c.r(5, 8, 10, 8, "l")
    c.p(10, 8, "L")
    c.p(8, 3, "5")  # tiny rhombus tip


def plume(c, a="4", b="5"):
    c.r(7, 0, 8, 1, a)
    c.r(5, 1, 6, 2, b)
    c.p(9, 1, b); c.p(10, 2, b)
    c.p(7, 0, "w")
    c.r(7, 2, 8, 2, "L")
    c.p(4, 3, b) if False else None


def sqhair(c):
    c.r(6, 2, 9, 2, "n")
    c.r(5, 3, 10, 3, "n")
    c.p(5, 4, "n"); c.p(10, 4, "N")
    c.p(6, 2, "t"); c.p(7, 2, "t"); c.p(8, 3, "N")
    c.p(6, 3, "t")
    c.r(7, 7, 8, 7, "R")
    c.p(6, 7, "s"); c.p(9, 7, "S")
    c.p(7, 8, "S"); c.p(8, 8, "S")   # chin poked out


def old_helm(c):
    great_helm(c, slit="w")
    c.r(7, 2, 8, 2, "5")
    c.r(6, 3, 9, 3, "5")
    c.r(7, 4, 8, 4, "5")
    c.p(7, 3, "6") if False else None
    c.p(7, 3, "6"); c.p(8, 3, "6")


# ---- gear ------------------------------------------------------------------------------------
def kite_shield(c, y0=10):
    """kite shield on the left arm, rhombus on the face."""
    for y in range(y0, y0 + 6):
        c.r(0, y, 4, y, "2")
    for y, (a, b) in zip(range(y0 + 6, y0 + 10), ((1, 3), (1, 3), (2, 3), (2, 2))):
        c.r(a, y, b, y, "2")
    c.r(0, y0, 0, y0 + 5, "1")
    c.r(4, y0, 4, y0 + 5, "3")
    c.r(3, y0 + 6, 3, y0 + 8, "3")
    c.r(0, y0, 4, y0, "L")
    c.p(0, y0, "w")
    c.p(2, y0 + 1, "4")
    c.p(1, y0 + 2, "4"); c.p(3, y0 + 2, "5")
    c.p(1, y0 + 3, "4"); c.p(3, y0 + 3, "5")
    c.p(2, y0 + 4, "5")
    c.p(4, y0 + 5, "s")
    c.p(4, y0 + 5, "S")


def longsword(c, up=True):
    c.line(13, 3, 13, 13, "l")
    c.line(14, 5, 14, 13, "L")
    c.p(13, 2, "w"); c.p(13, 3, "w")
    c.r(12, 14, 14, 14, "y")
    c.r(13, 15, 13, 17, "N")
    c.p(13, 18, "y")
    c.p(12, 15, "S"); c.p(11, 15, "S")


def short_sword(c):
    c.line(13, 8, 13, 13, "l")
    c.line(14, 9, 14, 13, "L")
    c.p(13, 7, "w")
    c.r(12, 14, 14, 14, "y")
    c.r(13, 15, 13, 16, "N")
    c.p(12, 15, "s"); c.p(11, 15, "s")


def raised_sword(c):
    c.r(11, 12, 11, 14, "l") if False else None
    c.line(13, 0, 13, 10, "l")
    c.line(14, 2, 14, 10, "L")
    c.p(13, 0, "w"); c.p(13, 1, "w")
    c.r(11, 11, 15, 11, "y")
    c.r(13, 12, 13, 13, "N")
    c.p(14, 14, "y") if False else None
    c.p(12, 12, "S"); c.p(11, 12, "S"); c.p(12, 13, "S") if False else None
    c.p(11, 10, "3") if False else None
    c.r(11, 13, 11, 15, ".") if False else None


def planted_sword(c):
    """old knight leaning on a point-down sword."""
    c.r(11, 8, 15, 8, "y")
    c.p(13, 7, "y"); c.p(13, 6, "w")
    c.line(13, 9, 13, 22, "l")
    c.line(14, 10, 14, 21, "L")
    c.r(12, 15, 12, 15, "S"); c.p(11, 15, "S")
    c.r(12, 9, 12, 9, "S")
    c.p(11, 12, "L") if False else None


def long_rifle(c):
    """long rifle held diagonally across the body."""
    c.line(2, 18, 6, 14, "n")
    c.line(3, 18, 7, 14, "N")
    c.line(6, 14, 15, 7, "l")
    c.line(6, 15, 15, 8, "L")
    c.r(7, 13, 8, 13, "L") if False else None
    c.p(9, 11, "4"); c.p(10, 10, "4")
    c.p(15, 7, "w")
    c.p(11, 12, "S"); c.p(10, 12, "S")
    c.p(5, 15, "S"); c.p(4, 15, "s")


def banner(c):
    """tall pole, banner of the Holy Rhombus hanging from a crossbar above the head."""
    c.line(13, 0, 13, 22, "n")
    c.r(11, 0, 15, 0, "N")
    c.p(13, 0, "y")
    for y in range(1, 10):
        c.r(11, y, 15, y, "2")
    c.r(11, 1, 11, 9, "1")
    c.r(15, 1, 15, 9, "3")
    c.p(11, 10, "2"); c.p(12, 10, "2"); c.p(14, 10, "3"); c.p(15, 10, "3")
    c.p(11, 11, "1"); c.p(15, 11, "3")
    c.p(13, 10, "n")
    c.p(13, 3, "4")
    c.r(12, 4, 14, 5, "4")
    c.p(13, 6, "5"); c.p(12, 5, "5") if False else None
    c.p(13, 4, "5") if False else None
    c.p(13, 6, "4")
    c.p(12, 15, "S"); c.p(11, 15, "S")


@back
def short_cape(c, a="3", b="2"):
    c.r(3, 9, 12, 19, a)
    c.r(2, 12, 13, 20, a)
    c.r(2, 12, 3, 20, b)
    c.r(3, 20, 12, 20, "3") if False else None
    for x in (2, 4, 7, 11, 13):
        c.p(x, 21, a)


@back
def cloth_tail(c):
    c.r(3, 9, 12, 12, "3")


# ---- sprites ---------------------------------------------------------------------------------
def knight():
    return P(partial(mail), pauldrons, coif_helm, tabard, rhombus, kite_shield, longsword,
             body="l", lite="l", dark="L", face="none")


def gunner():
    return P(partial(mail), pauldrons, great_helm, tabard, rhombus, long_rifle,
             body="l", lite="l", dark="L", face="none")


def bearer():
    return P(partial(mail), pauldrons, coif_helm, bare_coif, tabard, rhombus, banner,
             body="l", lite="l", dark="L", face="none")


def commander():
    return P(short_cape, partial(mail), partial(pauldrons, big=True), coif_helm, plume,
             tabard, partial(rhombus, y=11), raised_sword,
             body="l", lite="l", dark="L", face="none")


def squire():
    return P(tunic, sqhair, partial(tabard, a="3", lo="3", dk="3", end=17, belt=False), partial(rhombus, y=10), short_sword,
             body="1", lite="1", dark="2", face="face")


def chiliad():
    return P(partial(mail, hem=True), partial(pauldrons, big=True), old_helm,
             partial(tabard, end=18), partial(rhombus, y=11), planted_sword,
             body="l", lite="l", dark="L", face="none")


SPRITES = {
    "templar_knight": knight(),
    "templar_gunner": gunner(),
    "templar_bearer": bearer(),
    "templar_commander": commander(),
    "templar_squire": squire(),
    "templar_chiliad": chiliad(),
}
HUMANOID = set(SPRITES)
