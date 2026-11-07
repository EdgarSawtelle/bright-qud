"""Visible mutations for the GAME's character sprites (creature look = Game / Game + outline / Game + depth).

Flat two-colour parts in the game's own manner (only roles 2 = the character's colour and 5 = its detail
colour), drawn for the game's front-facing 16x24 humanoids: body in columns 1-14, rows 1-21, head around
columns 4-9, rows 2-7, shoulders row 8, hands rows 12-14, feet row 21. Parts behind the body reach past
its edges and show through its gaps (wings, shell, quills, tail, extra arms/legs, second head); parts in
front sit on it (horns, beak, claws, fur).
Built as brightqudmutg/<name>; layer order comes from Generated.Mutations (behind = true/false).
"""
from vkit import Canvas


def _mirror(c, fn):
    fn(c, False)
    fn(c, True)


def _x(x, m):
    return 15 - x if m else x


def wings():
    c = Canvas()
    def wing(c, m):
        X = lambda x: _x(x, m)
        c.poly([(X(3), 9), (X(3), 1), (X(0), 0), (X(0), 13), (X(1), 11), (X(2), 13)], "2")
        c.erase_line([(X(0), 6), (X(1), 8)], w=0.6)               # scalloped trailing edge
        c.line([(X(3), 9), (X(3), 1), (X(0), 0)], "5", w=0.9)     # leading bone
        c.line([(X(2), 1), (X(1), 11)], "5", w=0.6)               # finger bone
    _mirror(c, wing)
    c.erase_poly([(4, 0), (11, 0), (11, 23), (4, 23)])            # never under the body's middle
    return c.grid(0.4)


def carapace():
    c = Canvas()
    c.ellipse(7.5, 11, 7.2, 6.5, "5")                       # shell rim around the back
    c.erase_poly([(4, 6), (11, 6), (11, 16), (4, 16)])      # the body covers the middle
    for y in (7, 11, 15):                                   # plate seams
        c.px(0, y, "2"); c.px(15, y, "2")
    return c.grid(0.45)


def quills():
    c = Canvas()
    for (x0, y0, x1, y1) in ((5, 7, 0, 0), (6, 6, 3, 0), (9, 6, 12, 0), (10, 7, 15, 0), (4, 9, 0, 5), (11, 9, 15, 5),
                             (4, 11, 0, 10), (11, 11, 15, 10)):
        c.line([(x0, y0), (x1, y1)], "5", w=0.7)
    return c.grid(0.35)


def stinger():
    c = Canvas()
    c.line([(11, 18), (14, 16), (15, 11), (15, 6), (13, 3)], "2", w=1.8)  # thick segmented tail from the hip
    for (x, y) in ((15, 14), (15, 10), (15, 7)):
        c.px(x, y, "5")
    c.poly([(13, 3), (11, 0), (10, 2), (12, 4)], "5")                   # barb
    return c.grid(0.4)


def two_headed():
    c = Canvas()
    c.ellipse(12.5, 2.5, 2.4, 2.4, "2")                      # second head, behind the right shoulder
    c.line([(12, 4), (11, 8)], "2", w=1.4)
    c.px(12, 2, "5"); c.px(14, 2, "5")                       # eyes
    return c.grid(0.4)


def multiple_arms():
    c = Canvas()
    def arm(c, m):
        X = lambda x: _x(x, m)
        c.line([(X(3), 9), (X(0), 11), (X(0), 15)], "2", w=1.1)
        c.px(X(0), 16, "5")
    _mirror(c, arm)
    return c.grid(0.4)


def multiple_legs():
    c = Canvas()
    def leg(c, m):
        X = lambda x: _x(x, m)
        c.line([(X(4), 16), (X(1), 18), (X(1), 21)], "2", w=1.1)
        c.px(X(0), 21, "5")
    _mirror(c, leg)
    return c.grid(0.4)


def horns():
    c = Canvas()
    def horn(c, m):
        X = lambda x: _x(x, m)
        c.line([(X(5), 3), (X(3), 1), (X(2), 0), (X(1), 1)], "5", w=0.9)
    _mirror(c, horn)
    return c.grid(0.4)


def beak():
    c = Canvas()
    c.poly([(5, 5), (10, 5), (8, 9), (7, 9)], "5")           # hooked beak over the mouth
    c.px(7, 6, "2")
    return c.grid(0.4)


def burrowing_claws():
    c = Canvas()
    def claw(c, m):
        X = lambda x: _x(x, m)
        for dy in (0, 2, 4):
            c.line([(X(2), 12 + dy), (X(0), 13 + dy)], "5", w=0.8)
    _mirror(c, claw)
    return c.grid(0.4)


def thick_fur():
    c = Canvas()
    for (x, y) in ((1, 8), (0, 9), (1, 11), (0, 13), (1, 15), (14, 8), (15, 9), (14, 11), (15, 13), (14, 15),
                   (4, 1), (6, 1), (9, 1), (11, 1)):
        c.px(x, y, "2")
    return c.grid()


SPRITES = {
    "Wings": wings(), "Carapace": carapace(), "Quills": quills(), "Stinger": stinger(), "TwoHeaded": two_headed(),
    "MultipleArms": multiple_arms(), "MultipleLegs": multiple_legs(), "Horns": horns(), "Beak": beak(),
    "BurrowingClaws": burrowing_claws(), "ThickFur": thick_fur(),
}
BEHIND = {"Wings", "Carapace", "Quills", "Stinger", "TwoHeaded", "MultipleArms", "MultipleLegs"}
