"""Style D - tabletop miniatures: figures on round bases (base = detail color 4/5/6)."""


class C:
    def __init__(s):
        s.g = [["."] * 16 for _ in range(24)]

    def p(s, x, y, ch):
        if 0 <= x < 16 and 0 <= y < 24:
            s.g[y][x] = ch

    def r(s, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.p(x, y, ch)

    def row(s, y, x0, text):
        for i, ch in enumerate(text):
            if ch != " ":
                s.p(x0 + i, y, ch)

    def out(s):
        return ["".join(r) for r in s.g]


def base(c, small=False):
    a, b = (4, 11) if small else (2, 13)
    c.r(a + 1, 19, b - 1, 19, "4")
    c.r(a, 20, b, 20, "5")
    c.r(a + 1, 21, b - 1, 21, "5")
    c.r(a + 2, 22, b - 2, 22, "6")
    c.p(a, 20, "4"); c.p(b, 20, "6"); c.p(b - 1, 21, "6")
    c.r(a + 1, 23, b - 1, 23, "x")


def human(c, h=3, coat=0, hat=None):
    """Slim top-down-ish human. h = head top row."""
    t = h + 4  # torso top
    # head
    c.r(6, h, 9, h + 3, "s")
    c.p(9, h + 1, "S"); c.p(9, h + 2, "S"); c.r(7, h + 3, 9, h + 3, "S") if False else None
    c.p(6, h + 2, "O"); c.p(9, h + 2, "O")
    c.row(h + 3, 6, "SssS")
    # torso
    c.r(5, t, 10, t + 5, "1")
    c.r(10, t, 10, t + 5, "2")
    c.r(5, t + 5, 10, t + 5, "3")
    # arms
    c.r(4, t, 4, t + 3, "2"); c.r(11, t, 11, t + 3, "3")
    c.p(4, t + 4, "s"); c.p(11, t + 4, "S")
    # legs
    bot = 18
    ln = bot - (t + 6)
    c.r(6, t + 6, 7, bot, "3"); c.r(8, t + 6, 9, bot, "3")
    c.r(7, t + 6, 7, bot, "2") if False else None
    c.p(7, t + 7, "3") if False else None
    c.r(5, bot, 7, bot, "N"); c.r(8, bot, 10, bot, "N")
    c.p(8, t + 6, "O"); c.p(7, t + 6, "O") if False else None
    if coat:
        c.r(5, t + 6, 10, t + 8, "1")
        c.r(10, t + 6, 10, t + 8, "2")
        c.r(5, t + 8, 10, t + 8, "3")
        c.p(7, t + 7, "2"); c.p(8, t + 7, "2")


def gunslinger():
    c = C(); base(c)
    human(c, h=4, coat=1)
    # hat
    c.r(2, 4, 13, 4, "3"); c.r(3, 3, 12, 3, "3")
    c.r(5, 1, 10, 3, "2"); c.r(6, 0, 9, 0, "2")
    c.r(5, 3, 10, 3, "y"); c.p(10, 1, "3"); c.p(10, 2, "3")
    c.r(2, 4, 3, 4, "2")
    # crossed pistols on chest
    for i in range(4):
        c.p(5 + i, 11 - i if False else 8 + i, "l")
    c.p(5, 8, "N"); c.p(6, 9, "N"); c.p(7, 10, "l"); c.p(8, 11, "l"); c.p(9, 12, "l"); c.p(10, 12, "l")
    c.p(10, 8, "N"); c.p(9, 9, "N"); c.p(8, 10, "l"); c.p(7, 11, "l"); c.p(6, 12, "l"); c.p(5, 12, "l")
    c.p(7, 10, "L"); c.p(8, 10, "L")
    # belt buckle
    c.p(7, 13, "y"); c.p(8, 13, "y")
    c.r(5, 13, 10, 13, "3"); c.p(7, 13, "y"); c.p(8, 13, "y")
    return c.out()


def winged():
    c = C(); base(c)
    # folded wings rising behind shoulders
    for side in (0, 1):
        def X(x): return x if side == 0 else 15 - x
        for y, (a, b) in {0: (4, 4), 1: (3, 4), 2: (3, 4), 3: (2, 4), 4: (2, 4), 5: (1, 4),
                          6: (1, 4), 7: (1, 4), 8: (2, 4), 9: (3, 4), 10: (4, 4)}.items():
            for x in range(a, b + 1):
                c.p(X(x), y, "5")
            c.p(X(a), y, "6")
        for y in range(1, 8):
            c.p(X(4), y, "4")
        c.p(X(3), 4, "4"); c.p(X(3), 6, "4"); c.p(X(2), 5, "4")
    human(c, h=5)
    return c.out()


def horned():
    c = C(); base(c)
    human(c, h=5)
    # tall curved horns
    for side in (0, 1):
        def X(x): return x if side == 0 else 15 - x
        for (x, y) in [(5, 5), (5, 4), (4, 3), (4, 2), (4, 1), (4, 0)]:
            c.p(X(x), y, "5")
        for (x, y) in [(3, 1), (3, 0)]:
            c.p(X(x), y, "4")
        c.p(X(5), 4, "6"); c.p(X(5), 5, "6")
        c.p(X(4), 3, "4"); c.p(X(3), 2, "4")
        for (x, y) in [(3, 3), (3, 4), (4, 4), (2, 1), (2, 2)]:
            c.p(X(x), y, "5")
        c.p(X(2), 0, "4") if False else None
    # brow
    c.row(5, 6, "3  3") if False else None
    return c.out()


def four_arms():
    c = C(); base(c)
    human(c, h=4)
    # upper arms raised
    for side in (0, 1):
        def X(x): return x if side == 0 else 15 - x
        c.r(X(4), 8, X(4), 9, "1") if False else None
        for (x, y) in [(4, 8), (3, 7), (3, 6), (2, 5)]:
            c.p(X(x), y, "2")
        c.p(X(2), 4, "s"); c.p(X(3), 4, "s")
        # lower arms out
        for (x, y) in [(4, 11), (3, 12), (2, 12)]:
            c.p(X(x), y, "2")
        c.p(X(1), 12, "s")
        c.p(X(4), 8, "2")
        c.p(X(4), 9, "1") if False else None
    # bracers in detail color
    c.p(3, 6, "4"); c.p(12, 6, "4"); c.p(3, 12, "4"); c.p(12, 12, "4")
    c.p(2, 12, "5"); c.p(13, 12, "5")
    c.r(1, 11, 2, 11, "s"); c.r(13, 11, 14, 11, "s"); c.p(1, 12, "s"); c.p(14, 12, "s")
    c.r(1, 3, 2, 4, "s"); c.r(13, 3, 14, 4, "s")
    c.p(2, 5, "2"); c.p(13, 5, "2")
    return c.out()


def carapace():
    c = C(); base(c)
    # shell dome behind/around
    rows = {3: (6, 9), 4: (4, 11), 5: (3, 12), 6: (3, 12), 7: (2, 13), 8: (2, 13), 9: (2, 13), 10: (3, 12), 11: (4, 11)}
    for y, (a, b) in rows.items():
        c.r(a, y, b, y, "5")
        c.p(a, y, "6"); c.p(b, y, "6")
        c.p(a + 1, y, "4") if y < 8 else None
    c.r(7, 3, 8, 3, "4")
    # plate seams
    for y in (6, 9):
        c.r(4, y, 11, y, "6") if False else None
    c.p(2, 9, "6"); c.p(13, 9, "6")
    c.r(7, 4, 8, 4, "6"); c.p(5, 6, "6"); c.p(10, 6, "6"); c.p(4, 8, "6"); c.p(11, 8, "6")
    human(c, h=5)
    # shoulder plates
    c.r(3, 9, 4, 10, "4"); c.r(11, 9, 12, 10, "4")
    c.r(3, 10, 4, 10, "5"); c.r(11, 10, 12, 10, "6")
    c.p(3, 9, "4"); c.p(4, 9, "4")
    return c.out()


def mehmet():
    c = C(); base(c)
    human(c, h=4)
    c.r(6, 4, 9, 4, "w")  # bald with white brow hair
    c.r(6, 8, 9, 9, "w"); c.p(6, 8, "S"); c.p(9, 8, "S")  # beard
    c.p(7, 10, "w"); c.p(8, 10, "w")
    c.r(6, 8, 9, 8, "w")
    c.r(6, 7, 9, 7, "S") if False else None
    # hoe at right side
    c.r(13, 4, 13, 18, "N")
    c.r(11, 3, 14, 3, "l"); c.p(14, 4, "l"); c.p(11, 4, "L")
    c.p(12, 11, "s"); c.p(11, 11, "s")
    c.r(12, 9, 12, 11, "2") if False else None
    c.p(11, 8, "3")
    c.r(5, 13, 10, 13, "3")
    return c.out()


def farmer():
    c = C(); base(c)
    human(c, h=4)
    c.r(3, 4, 12, 4, "t"); c.r(5, 2, 10, 3, "t"); c.r(5, 3, 10, 3, "T") if False else None
    c.r(5, 3, 10, 3, "t"); c.r(5, 3, 10, 3, "t")
    c.r(5, 3, 10, 3, "t"); c.r(5, 3, 10, 3, "N") if False else None
    c.r(5, 3, 10, 3, "t")
    c.r(3, 4, 4, 4, "N") if False else None
    c.r(5, 3, 10, 3, "t"); c.r(5, 3, 10, 3, "t")
    c.row(3, 5, "NNNNNN")
    # sickle in right hand
    c.p(12, 10, "s"); c.p(12, 9, "N"); c.p(12, 8, "l"); c.p(13, 7, "l"); c.p(13, 6, "l"); c.p(12, 5, "L")
    c.p(11, 9, "3")
    c.r(5, 13, 10, 13, "N")
    return c.out()


def snapjaw_head(c, h):
    # hyena head: pointed ears, long muzzle, fur
    c.r(5, h + 1, 10, h + 4, "1")
    c.p(5, h, "2"); c.p(6, h, "2"); c.p(9, h, "2"); c.p(10, h, "2")
    c.p(4, h - 1, "3") if False else None
    c.p(5, h - 1, "3"); c.p(10, h - 1, "3")
    c.r(7, h + 1, 8, h + 1, "2")
    c.p(6, h + 2, "O"); c.p(9, h + 2, "O")
    c.r(6, h + 3, 9, h + 4, "S")
    c.row(h + 4, 6, "wSSw")
    c.r(10, h + 1, 10, h + 3, "2")


def snapjaw_body(c, h=4):
    t = h + 5
    snapjaw_head(c, h)
    c.r(4, t, 11, t + 4, "1")
    c.r(11, t, 11, t + 4, "2")
    c.r(4, t + 4, 11, t + 4, "3")
    c.r(3, t, 3, t + 3, "2"); c.r(12, t, 12, t + 3, "3")
    c.p(3, t + 4, "S"); c.p(12, t + 4, "S")
    # loincloth detail
    c.r(5, t + 4, 10, t + 5, "4"); c.r(6, t + 5, 9, t + 5, "5")
    c.r(6, t + 6, 7, 18, "2"); c.r(8, t + 6, 9, 18, "3")
    c.r(5, 18, 7, 18, "6"); c.r(8, 18, 10, 18, "6")


def snapjaw():
    c = C(); base(c)
    snapjaw_body(c)
    # club
    c.r(13, 8, 13, 13, "N"); c.r(12, 6, 14, 8, "n") if False else None
    c.r(12, 6, 14, 8, "N"); c.p(13, 7, "n"); c.p(12, 11, "S")
    c.p(12, 10, "S")
    return c.out()


def snapjaw_hunter():
    c = C(); base(c)
    snapjaw_body(c)
    # hood-cap in detail
    c.r(5, 3, 10, 3, "5"); c.r(5, 3, 6, 3, "4")
    # bow at left, string
    c.p(2, 6, "N"); c.p(1, 7, "N"); c.r(1, 8, 1, 13, "N"); c.p(1, 14, "N"); c.p(2, 15, "N")
    c.r(2, 7, 2, 14, "w") if False else None
    c.r(2, 8, 2, 13, "w") if False else None
    c.p(2, 7, "w") if False else None
    c.r(3, 7, 3, 14, "w") if False else None
    c.p(2, 9, "w"); c.p(2, 12, "w")
    # arrow
    c.p(4, 12, "S")
    return c.out()


def glowfish():
    c = C(); base(c, small=True)
    # stalk
    c.r(7, 13, 8, 18, "l"); c.r(8, 13, 8, 18, "L")
    c.r(6, 18, 9, 18, "L")
    # glow halo
    c.p(3, 3, "4"); c.p(12, 3, "4"); c.p(2, 8, "4"); c.p(13, 8, "4")
    # fish body (faces left)
    rows = {4: (5, 10), 5: (3, 12), 6: (2, 12), 7: (1, 12), 8: (2, 12), 9: (3, 12), 10: (5, 10)}
    for y, (a, b) in rows.items():
        c.r(a, y, b, y, "1")
    c.r(2, 9, 11, 10, "2") if False else None
    c.r(3, 9, 11, 9, "2"); c.r(5, 10, 10, 10, "3")
    c.r(2, 4, 2, 3, "5") if False else None
    c.r(6, 3, 9, 3, "4")  # dorsal
    c.r(5, 4, 5, 4, "4")
    c.r(13, 5, 14, 5, "5"); c.r(13, 6, 15, 6, "4"); c.r(13, 7, 15, 7, "5"); c.r(13, 8, 14, 8, "5")  # tail
    c.p(3, 6, "O"); c.p(3, 5, "w") if False else None
    c.p(2, 8, "S")
    c.r(7, 7, 8, 8, "4")  # glowing spot
    c.p(8, 11, "4"); c.p(7, 11, "5")
    return c.out()


def girshling():
    c = C(); base(c, small=True)
    # body: two segments
    c.r(6, 11, 9, 14, "1"); c.r(9, 11, 9, 14, "2"); c.r(6, 14, 9, 14, "3")
    c.r(5, 8, 10, 10, "1"); c.r(10, 8, 10, 10, "2"); c.r(5, 10, 10, 10, "2")
    c.p(6, 9, "O"); c.p(9, 9, "O")
    c.r(7, 11, 8, 12, "4")  # mark
    c.r(7, 7, 8, 7, "5")  # jaws
    c.p(6, 7, "4"); c.p(9, 7, "4")
    # legs
    for (x, y) in [(4, 9), (3, 10), (2, 12), (2, 14), (3, 16), (4, 17)]:
        c.p(x, y, "3"); c.p(15 - x, y, "3")
    for (x, y) in [(4, 12), (3, 13), (4, 15), (5, 16), (5, 17)]:
        c.p(x, y, "2"); c.p(15 - x, y, "2")
    c.p(5, 14, "3"); c.p(10, 14, "3")
    c.p(2, 9, "3"); c.p(13, 9, "3")
    c.p(5, 18, "3"); c.p(10, 18, "3"); c.p(3, 17, "3"); c.p(12, 17, "3")
    return c.out()


def dog():
    c = C(); base(c)
    # side view facing right
    c.r(3, 10, 10, 14, "1")
    c.r(3, 14, 10, 14, "2")
    c.r(3, 13, 10, 14, "2") if False else None
    c.r(9, 7, 12, 11, "1")  # head
    c.r(12, 9, 14, 10, "s") if False else None
    c.r(12, 9, 14, 10, "2"); c.p(14, 9, "O")
    c.p(10, 6, "3"); c.p(10, 7, "3"); c.p(9, 7, "3")  # ear
    c.p(11, 8, "O")
    c.p(11, 11, "4"); c.p(11, 12, "4")  # collar in detail
    c.r(10, 12, 11, 12, "5") if False else None
    c.r(3, 15, 4, 18, "2"); c.r(6, 15, 6, 18, "3")
    c.r(9, 15, 10, 18, "2"); c.r(12, 15, 12, 18, "3") if False else None
    c.r(8, 15, 8, 18, "3")
    # tail up
    c.p(2, 9, "1"); c.p(1, 8, "1"); c.p(1, 7, "2")
    c.r(3, 10, 4, 11, "1")
    c.p(14, 10, "O") if False else None
    c.r(5, 11, 7, 12, "2") if False else None
    return c.out()


def salthopper():
    c = C(); base(c)
    # head right-facing with antennae
    c.r(10, 7, 13, 11, "1"); c.p(13, 8, "O")
    c.p(11, 6, "4"); c.p(12, 5, "4"); c.p(13, 4, "4")
    c.p(10, 6, "4"); c.p(9, 5, "4"); c.p(8, 4, "4")
    # thorax and abdomen
    c.r(7, 9, 10, 13, "1"); c.r(7, 13, 10, 13, "2")
    c.r(1, 9, 7, 13, "2"); c.r(1, 12, 7, 13, "3")
    c.r(2, 9, 6, 9, "1")
    c.r(3, 10, 5, 10, "4") if False else None
    c.p(3, 10, "4"); c.p(5, 10, "4"); c.p(7, 10, "4")
    c.p(11, 12, "5")
    # big hind leg: thigh up, shin down
    c.r(4, 12, 7, 14, "1"); c.r(4, 14, 7, 14, "3")
    c.p(3, 15, "3"); c.p(2, 16, "3"); c.p(2, 17, "3"); c.p(1, 18, "3"); c.p(2, 18, "3")
    # front legs
    c.r(9, 14, 9, 18, "3"); c.r(11, 14, 11, 18, "3") if False else None
    c.r(11, 13, 11, 18, "3")
    c.p(12, 18, "3")
    return c.out()


def croc():
    c = C(); base(c)
    # long body facing right
    c.r(1, 12, 9, 16, "1"); c.r(1, 15, 9, 16, "2")
    c.r(1, 12, 9, 12, "1")
    # spines
    for x in range(2, 9, 2):
        c.p(x, 11, "4")
    c.r(10, 11, 15, 14, "1"); c.r(10, 14, 15, 14, "2")
    c.r(10, 11, 15, 11, "1")
    c.r(11, 14, 15, 15, "2")
    c.p(11, 10, "1"); c.p(11, 11, "1"); c.p(11, 10, "O"); c.p(12, 10, "1")
    c.r(11, 14, 15, 14, "w") if False else None
    c.p(12, 14, "w"); c.p(14, 14, "w"); c.p(13, 15, "w") if False else None
    # tail
    c.r(0, 13, 0, 15, "2") if False else None
    c.p(0, 14, "3"); c.p(0, 15, "3")
    # legs
    c.r(3, 17, 4, 18, "3"); c.r(8, 17, 9, 18, "3"); c.r(12, 16, 12, 18, "3") if False else None
    c.r(11, 16, 12, 18, "3")
    # belly
    c.r(2, 16, 9, 16, "3")
    c.p(3, 14, "4"); c.p(6, 14, "4"); c.p(9, 13, "4")
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(), "four_arms": four_arms(),
    "carapace": carapace(), "mehmet": mehmet(), "farmer": farmer(), "snapjaw": snapjaw(),
    "snapjaw_hunter": snapjaw_hunter(), "glowfish": glowfish(), "girshling": girshling(),
    "dog": dog(), "salthopper": salthopper(), "croc": croc(),
}
