"""Paper doll weapons + shield. Role 1-3 = main material (blade/barrel/head), 4-6 = grip/fittings."""
from b3kit import C


def _mk(f):
    c = C()
    f(c)
    return c.out()


def dagger(c):
    c.r(12, 8, 12, 13, "1"); c.r(13, 10, 13, 13, "2"); c.p(12, 7, "1")
    c.r(11, 14, 13, 14, "5"); c.p(11, 14, "4")
    c.p(12, 15, "s"); c.p(12, 16, "6")


def sword(c):
    c.r(12, 3, 12, 13, "1"); c.r(13, 4, 13, 13, "2"); c.p(12, 2, "1"); c.p(12, 3, "w")
    c.r(10, 14, 14, 14, "5"); c.p(10, 14, "4"); c.p(14, 14, "6")
    c.p(12, 15, "s"); c.p(12, 16, "6"); c.p(12, 17, "4")


def axe(c):
    c.line(12, 6, 12, 20, "5")
    c.r(13, 5, 15, 10, "2"); c.r(13, 5, 15, 5, "1"); c.p(15, 5, "."); c.p(15, 10, ".")
    c.r(15, 6, 15, 9, "1"); c.r(13, 6, 13, 9, "3")
    c.p(12, 5, "6"); c.p(12, 11, "6")
    c.p(12, 15, "s")


def mace(c):
    c.line(12, 8, 12, 19, "5")
    c.r(10, 3, 14, 7, "2"); c.r(11, 2, 13, 2, "2"); c.r(11, 8, 13, 8, "2")
    c.p(10, 3, "."); c.p(14, 3, "."); c.p(10, 7, "."); c.p(14, 7, ".")
    c.r(11, 3, 12, 4, "1"); c.r(13, 6, 13, 7, "3"); c.r(11, 7, 12, 7, "3")
    c.p(12, 5, "4"); c.p(10, 5, "3"); c.p(14, 5, "3"); c.p(12, 9, "6")
    c.p(12, 15, "s")


def hammer(c):
    c.line(12, 7, 12, 20, "5")
    c.r(10, 3, 14, 7, "2"); c.r(10, 3, 14, 3, "1"); c.r(10, 7, 14, 7, "3")
    c.p(12, 5, "6"); c.p(10, 3, "w")
    c.p(12, 15, "s")


def staff(c):
    c.line(12, 4, 12, 22, "5")
    c.r(11, 1, 13, 3, "2"); c.p(12, 0, "1"); c.p(11, 1, "1"); c.p(12, 4, "6"); c.p(12, 3, "3")
    c.p(11, 4, "6"); c.p(13, 4, "6")
    c.p(12, 15, "s")


def whip(c):
    c.r(12, 14, 12, 16, "5"); c.p(12, 15, "s"); c.p(12, 17, "6"); c.p(12, 14, "4")
    for x, y, r in ((13, 17, "2"), (14, 18, "2"), (14, 19, "3"), (13, 20, "2"), (12, 21, "3"),
                    (12, 22, "2"), (13, 22, "2"), (14, 22, "3"), (14, 21, "2"), (15, 21, "1")):
        c.p(x, y, r)


def pistol(c):
    c.r(11, 12, 15, 13, "2"); c.r(11, 12, 15, 12, "1"); c.p(15, 13, "3")
    c.r(10, 13, 10, 13, "3")
    c.r(11, 14, 12, 16, "5"); c.p(12, 15, "s"); c.p(11, 16, "6")
    c.p(13, 14, "6"); c.p(14, 11, "4")


def shield(c):
    c.r(0, 10, 5, 19, "4")
    c.r(1, 11, 4, 18, "2")
    c.r(1, 11, 2, 18, "1")
    for p in ((0, 10), (5, 10), (0, 19), (5, 19)):
        c.p(*p, ".")
    c.r(2, 14, 3, 15, "5"); c.p(2, 14, "6") if False else None
    c.r(3, 12, 4, 18, "3") if False else None
    c.p(3, 16, "3"); c.p(4, 17, "3"); c.p(4, 18, "3"); c.p(3, 18, "3")
    c.p(4, 15, "s")


def t_sword(c):
    # greatsword held diagonally across the body, point up-right, both hands low
    c.line(14, 0, 8, 12, "1"); c.line(15, 1, 9, 13, "2")
    c.line(14, 1, 9, 12, "1")
    c.line(7, 12, 11, 12, "5"); c.line(6, 13, 11, 13, "5"); c.p(11, 13, "4"); c.p(6, 13, "6")
    c.line(7, 14, 5, 18, "5"); c.line(8, 14, 6, 18, "6")
    c.p(4, 15, "s"); c.p(11, 15, "s"); c.p(4, 19, "4")


def t_axe(c):
    # halberd: long shaft vertical at col 8-9 in front, big crescent head
    c.line(8, 4, 8, 22, "5"); c.line(9, 4, 9, 22, "6")
    c.r(9, 1, 13, 7, "2"); c.r(9, 1, 13, 1, "1"); c.r(13, 2, 14, 6, "1"); c.r(11, 3, 12, 5, "3")
    c.p(14, 2, "w"); c.p(13, 7, "."); c.p(9, 7, "3"); c.p(10, 7, "3"); c.p(14, 4, "1")
    c.p(8, 0, "1"); c.p(8, 1, "1"); c.p(8, 2, "1"); c.p(8, 3, "3")
    c.p(8, 8, "4"); c.p(9, 8, "4")
    c.p(11, 15, "s"); c.p(4, 12, "s"); c.r(5, 12, 7, 12, "5") 


def t_hammer(c):
    c.line(8, 7, 8, 22, "5"); c.line(9, 7, 9, 22, "6")
    c.r(5, 1, 12, 6, "2"); c.r(5, 1, 12, 1, "1"); c.r(5, 6, 12, 6, "3")
    c.r(5, 2, 5, 5, "1"); c.r(12, 2, 12, 5, "3")
    c.p(8, 3, "4"); c.p(9, 3, "4"); c.p(8, 4, "6"); c.p(9, 4, "6")
    c.p(11, 15, "s"); c.p(4, 12, "s"); c.r(5, 12, 7, 12, "5")


def t_rifle(c):
    # long barrel across the chest, short slim stock at the right shoulder
    c.line(0, 9, 10, 12, "1"); c.line(0, 10, 10, 13, "2")
    c.r(8, 12, 11, 14, "5"); c.r(8, 12, 11, 12, "4"); c.r(8, 14, 11, 14, "6")
    c.r(12, 12, 14, 13, "6"); c.p(14, 12, "5")
    c.r(5, 14, 6, 15, "5")
    c.p(3, 10, "4"); c.p(9, 11, "4")
    c.p(5, 13, "s"); c.p(4, 13, "s"); c.p(4, 12, "s"); c.p(11, 15, "s"); c.p(11, 14, "s")


def t_bow(c):
    # tall recurve bow held vertical in front of the left side, string drawn
    c.line(6, 1, 3, 6, "5"); c.line(3, 6, 3, 17, "5"); c.line(3, 17, 6, 22, "5")
    c.line(7, 1, 7, 21, "6")
    c.p(2, 11, "4"); c.p(2, 12, "4"); c.p(3, 18, "4"); c.p(3, 5, "4")
    c.line(8, 11, 13, 11, "5"); c.p(14, 11, "1"); c.p(15, 11, "1"); c.p(14, 10, "1"); c.p(14, 12, "1")
    c.p(8, 10, "4"); c.p(8, 12, "4")
    c.p(4, 12, "s"); c.p(11, 15, "s"); c.p(7, 11, "s")


def t_heavy(c):
    # bulky cannon on the hip/shoulder: big barrel block, ammo drum
    c.r(0, 9, 12, 14, "2"); c.r(0, 9, 12, 9, "1"); c.r(0, 14, 12, 14, "3")
    c.r(0, 10, 1, 13, "3"); c.p(0, 8, "6"); c.p(1, 8, "6"); c.p(0, 15, ".")
    c.r(3, 10, 3, 13, "6"); c.r(8, 10, 8, 13, "6")
    c.r(5, 15, 9, 18, "5"); c.r(5, 15, 9, 15, "4"); c.r(5, 18, 9, 18, "6"); c.p(7, 16, "6")
    c.r(11, 15, 13, 16, "6"); c.r(13, 10, 15, 13, "5"); c.p(15, 10, "4")
    c.p(10, 11, "4")
    c.p(4, 15, "s"); c.p(11, 15, "s"); c.p(11, 16, "s")


LAYERS = {
    "right/dagger": _mk(dagger), "right/sword": _mk(sword), "right/axe": _mk(axe),
    "right/mace": _mk(mace), "right/hammer": _mk(hammer), "right/staff": _mk(staff),
    "right/whip": _mk(whip), "right/pistol": _mk(pistol), "left/shield": _mk(shield),
    "two/sword": _mk(t_sword), "two/axe": _mk(t_axe), "two/hammer": _mk(t_hammer),
    "two/rifle": _mk(t_rifle), "two/bow": _mk(t_bow), "two/heavy": _mk(t_heavy),
}
