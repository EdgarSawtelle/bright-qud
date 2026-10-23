"""Style A - heroic proportions: small head (~5px), full body, gear-driven silhouettes."""


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

    def shadow(s, x0=3, x1=12, y=22):
        for yy, a, b in ((y, x0, x1), (y + 1, x0 + 2, x1 - 2)):
            for x in range(a, b + 1):
                if s.g[yy][x] == ".":
                    s.g[yy][x] = "x"

    def out(s):
        return ["".join(r) for r in s.g]


def head(c, hair="3", face="s", dx=0, y=2):
    c.row(y, 6 + dx, hair * 4)
    c.row(y + 1, 5 + dx, hair + face * 4 + hair)
    c.row(y + 2, 5 + dx, face + "O" + face * 2 + "O" + face)
    c.row(y + 3, 5 + dx, face * 6)
    c.row(y + 4, 6 + dx, "S" + face * 2 + "S")
    c.row(y + 5, 7 + dx, "SS")


def legs(c, a="2", b="3", boot="6", y=15):
    c.r(5, y, 7, y + 5, a)
    c.r(8, y, 10, y + 5, b)
    c.r(7, y, 7, y + 5, b)
    c.r(5, y + 4, 7, y + 6, boot)
    c.r(8, y + 4, 10, y + 6, boot)
    c.p(4, y + 6, boot); c.p(11, y + 6, boot)
    c.r(5, y + 4, 5, y + 4, "5")


def torso(c, y0=8, y1=14, l="1", m="2", d="3"):
    c.r(4, y0, 11, y0, l)      # shoulders
    c.r(5, y0 + 1, 10, y1, m)
    c.r(5, y0 + 1, 6, y1, l)
    c.r(9, y0 + 1, 10, y1, d)
    c.r(5, y1, 10, y1, d)
    c.r(4, y0 + 1, 4, y0 + 1, l); c.r(11, y0 + 1, 11, y0 + 1, d)


def arm_down(c, x, left, y0=9, y1=14, sl="1", sd="3"):
    c.r(x, y0, x + 1, y1, sl if left else sd)
    c.r(x, y1 + 1, x + 1, y1 + 1, "s")


def human():
    c = C()
    head(c)
    torso(c)
    legs(c)
    return c


def gunslinger():
    c = C()
    # coat flaps (flared) behind legs
    c.r(3, 15, 12, 19, "2")
    c.r(3, 15, 5, 19, "1")
    c.r(10, 15, 12, 19, "3")
    c.r(3, 20, 4, 20, "2"); c.r(11, 20, 12, 20, "3")
    c.r(7, 15, 8, 20, "3")
    c.r(5, 20, 7, 21, "6"); c.r(8, 20, 10, 21, "6")
    c.p(5, 21, "6"); c.p(10, 21, "6")
    torso(c, 8, 14)
    c.r(7, 9, 8, 14, "w")   # shirt
    c.r(5, 13, 10, 13, "5")  # belt
    c.p(7, 13, "y")
    # head under hat
    c.row(4, 6, "ssss"); c.row(5, 5, "sOssOs"); c.row(6, 5, "ssssss"); c.row(7, 6, "SssS")
    c.row(5, 5, "sOssOs")
    # hat
    c.r(2, 3, 13, 3, "5")
    c.r(1, 4, 14, 4, "6") if False else None
    c.r(6, 0, 9, 2, "4"); c.r(5, 1, 5, 2, "5") if False else None
    c.r(6, 0, 7, 2, "4"); c.r(8, 0, 9, 2, "5")
    c.r(6, 2, 9, 2, "6")
    c.r(2, 3, 13, 3, "5"); c.r(1, 4, 3, 4, "5"); c.r(12, 4, 14, 4, "6")
    c.r(4, 4, 11, 4, "6")
    c.r(6, 3, 9, 3, "4")
    # arms out holding pistols
    c.r(1, 9, 4, 10, "1"); c.r(11, 9, 14, 10, "3")
    c.r(0, 9, 0, 10, "s"); c.r(15, 9, 15, 10, "s")
    c.r(0, 6, 1, 8, "L"); c.r(14, 6, 15, 8, "L")   # pistols pointing up-out
    c.r(0, 5, 0, 5, "l"); c.r(15, 5, 15, 5, "l")
    c.p(1, 8, "N"); c.p(14, 8, "N")
    c.shadow(2, 13)
    return c.out()


def winged():
    c = C()
    # wings spread above shoulders
    for side in (0, 1):
        def X(x): return x if side == 0 else 15 - x
        sh = "4" if side == 0 else "5"
        feather = [(0, 3, 4), (0, 4, 5), (0, 5, 6), (1, 2, 4), (1, 3, 5), (1, 4, 6), (2, 4, 7), (3, 5, 8), (4, 6, 9)]
        for x, ya, yb in feather:
            pass
        # wing as stacked feather rows
        spans = {2: (1, 3), 3: (0, 4), 4: (0, 4), 5: (0, 4), 6: (0, 4), 7: (0, 4), 8: (1, 4), 9: (2, 4), 10: (3, 4), 11: (3, 4)}
        for y, (a, b) in spans.items():
            for x in range(a, b + 1):
                c.p(X(x), y, "4" if (x + y) % 3 else "5" if side == 0 else "5")
        for y in (5, 7, 9):
            for x in range(0, 4):
                if c.g[y][X(x)] != ".":
                    c.p(X(x), y, "6" if side else "5")
        c.r(X(1), 3, X(1), 3, "4")
    head(c, hair="3", y=4)
    c.r(4, 10, 11, 10, "1")
    c.r(5, 11, 10, 16, "2"); c.r(5, 11, 6, 16, "1"); c.r(9, 11, 10, 16, "3")
    c.r(4, 11, 4, 12, "1"); c.r(11, 11, 11, 12, "3")
    c.r(3, 12, 4, 15, "1"); c.r(11, 12, 12, 15, "3")
    c.r(3, 16, 4, 16, "s"); c.r(11, 16, 12, 16, "s")
    c.r(5, 15, 10, 15, "5")
    # shorter legs
    c.r(5, 17, 7, 21, "2"); c.r(8, 17, 10, 21, "3"); c.r(7, 17, 7, 21, "3")
    c.r(5, 20, 7, 21, "6"); c.r(8, 20, 10, 21, "6")
    c.p(4, 21, "6"); c.p(11, 21, "6")
    c.shadow(3, 12)
    return c.out()


def horned():
    c = C()
    head(c, hair="3", y=4)
    # horns sweeping up and out past the head
    for pts, ch in (([(5, 5), (4, 4), (3, 3), (2, 2), (2, 1), (3, 0)], "4"), ([(10, 5), (11, 4), (12, 3), (13, 2), (13, 1), (12, 0)], "5")):
        for x, y in pts:
            c.p(x, y, ch)
    c.r(5, 4, 5, 4, "4"); c.r(10, 4, 10, 4, "5")
    for x, y in ((3, 2), (3, 1), (12, 2), (12, 1), (4, 3), (11, 3), (4, 4), (11, 4)):
        c.p(x, y, "6" if x > 7 else "4")
    c.p(3, 1, "4"); c.p(12, 1, "6")
    # bulky torso
    c.r(3, 10, 12, 10, "1")
    c.r(4, 11, 11, 16, "2"); c.r(4, 11, 6, 16, "1"); c.r(9, 11, 11, 16, "3")
    c.r(1, 11, 3, 15, "1"); c.r(12, 11, 14, 15, "3")
    c.r(1, 16, 3, 16, "s"); c.r(12, 16, 14, 16, "s")
    c.r(4, 15, 11, 15, "5")
    c.r(7, 11, 8, 14, "6")
    c.r(5, 17, 7, 21, "2"); c.r(8, 17, 10, 21, "3")
    c.r(5, 20, 7, 21, "6"); c.r(8, 20, 10, 21, "6")
    c.p(4, 21, "6"); c.p(11, 21, "6")
    c.shadow(2, 13)
    return c.out()


def four_arms():
    c = C()
    head(c, y=2)
    c.r(4, 8, 11, 8, "1")
    c.r(5, 9, 10, 15, "2"); c.r(5, 9, 6, 15, "1"); c.r(9, 9, 10, 15, "3")
    c.r(5, 14, 10, 14, "5")
    # upper arms raised out and up
    c.r(3, 8, 4, 8, "1"); c.r(2, 7, 3, 7, "1"); c.r(1, 5, 2, 6, "1"); c.r(0, 3, 1, 4, "s")
    c.r(11, 8, 12, 8, "3"); c.r(12, 7, 13, 7, "3"); c.r(13, 5, 14, 6, "3"); c.r(14, 3, 15, 4, "s")
    # lower arms out and down
    c.r(3, 10, 4, 10, "1"); c.r(2, 11, 3, 11, "1"); c.r(1, 12, 2, 13, "1"); c.r(0, 14, 1, 15, "s")
    c.r(11, 10, 12, 10, "3"); c.r(12, 11, 13, 11, "3"); c.r(13, 12, 14, 13, "3"); c.r(14, 14, 15, 15, "s")
    # arm bands
    c.p(1, 5, "4"); c.p(14, 5, "6"); c.p(2, 12, "4"); c.p(13, 12, "6")
    c.r(5, 16, 7, 21, "2"); c.r(8, 16, 10, 21, "3"); c.r(7, 16, 7, 21, "3")
    c.r(5, 20, 7, 21, "6"); c.r(8, 20, 10, 21, "6")
    c.p(4, 21, "6"); c.p(11, 21, "6")
    c.shadow(3, 12)
    return c.out()


def carapace():
    c = C()
    # domed shell behind/over shoulders
    shell = {3: (5, 10), 4: (3, 12), 5: (2, 13), 6: (1, 14), 7: (1, 14), 8: (1, 14), 9: (1, 14), 10: (2, 13), 11: (2, 13), 12: (3, 12)}
    for y, (a, b) in shell.items():
        for x in range(a, b + 1):
            ch = "4" if (x - y < 0 and x < 8) else "6" if x > 10 or y > 10 else "5"
            c.p(x, y, ch)
    for x, y in ((4, 5), (5, 4), (6, 4), (3, 6), (4, 6)):
        c.p(x, y, "4")
    for y in range(6, 12):
        c.p(7, y, "6"); 
    c.r(2, 9, 13, 9, "6") if False else None
    head(c, y=3)
    c.row(8, 5, "SSSSSS") if False else None
    c.r(4, 8, 11, 8, "1")
    c.r(5, 9, 10, 15, "2"); c.r(5, 9, 6, 15, "1"); c.r(9, 9, 10, 15, "3")
    c.r(3, 9, 4, 14, "5"); c.r(11, 9, 12, 14, "6")   # shoulder plates
    c.r(2, 10, 3, 14, "4") if False else None
    c.r(3, 15, 4, 15, "s"); c.r(11, 15, 12, 15, "s")
    c.r(5, 14, 10, 14, "6")
    c.r(5, 15, 7, 21, "2"); c.r(8, 15, 10, 21, "3"); c.r(7, 15, 7, 21, "3")
    c.r(5, 19, 7, 21, "5"); c.r(8, 19, 10, 21, "6")
    c.p(4, 21, "6"); c.p(11, 21, "6")
    c.shadow(2, 13)
    return c.out()


def mehmet():
    c = C()
    head(c, hair="w", y=2)
    c.row(6, 5, "wwwwww"); c.row(7, 5, "wwwwww"); c.row(8, 6, "wwww")   # beard
    c.r(4, 9, 11, 9, "1")
    c.r(5, 10, 10, 16, "2"); c.r(5, 10, 6, 16, "1"); c.r(9, 10, 10, 16, "3")
    c.r(4, 10, 4, 15, "1"); c.r(11, 10, 11, 15, "3")
    c.r(4, 16, 4, 16, "s"); c.r(11, 16, 11, 16, "s")
    c.r(5, 14, 10, 14, "5")
    # hoe in right hand
    c.r(13, 4, 13, 17, "n"); c.r(12, 17, 12, 17, "s")
    c.r(11, 3, 14, 3, "l"); c.r(11, 4, 11, 4, "l")
    c.r(11, 16, 12, 16, "s")
    c.r(5, 17, 7, 21, "2"); c.r(8, 17, 10, 21, "3")
    c.r(5, 20, 7, 21, "N"); c.r(8, 20, 10, 21, "N")
    c.p(4, 21, "N"); c.p(11, 21, "N")
    c.shadow(3, 14)
    return c.out()


def farmer():
    c = C()
    c.r(6, 1, 9, 1, "t"); c.r(4, 2, 11, 2, "t"); c.r(5, 2, 10, 2, "t")
    c.row(3, 5, "t" + "ssss" + "t"); c.row(4, 5, "sOssOs"); c.row(5, 5, "ssssss"); c.row(6, 6, "SssS"); c.row(7, 7, "SS")
    c.r(4, 8, 11, 8, "1")
    c.r(5, 9, 10, 15, "2"); c.r(5, 9, 6, 15, "1"); c.r(9, 9, 10, 15, "3")
    c.r(3, 9, 4, 14, "s"); c.r(11, 9, 12, 13, "s")
    c.r(3, 15, 4, 15, "s")
    c.r(5, 14, 10, 14, "n")
    # sickle
    c.r(12, 12, 12, 14, "n"); c.r(12, 10, 13, 11, "l"); c.p(14, 10, "l"); c.p(14, 9, "l")
    c.r(5, 15, 7, 21, "e"); c.r(8, 15, 10, 21, "E"); c.r(7, 15, 7, 21, "E")
    c.r(5, 15, 7, 17, "2"); c.r(8, 15, 10, 17, "3")
    c.r(5, 20, 7, 21, "N"); c.r(8, 20, 10, 21, "N")
    c.p(4, 21, "N"); c.p(11, 21, "N")
    c.shadow(3, 13)
    return c.out()


def snapjaw_base(c, hunter=False):
    # hyena head with snout
    c.row(2, 5, "1 1".replace(" ", "1")) if False else None
    c.row(1, 5, "11"); c.row(1, 9, "11")    # ears
    c.row(2, 5, "111111")
    c.row(3, 5, "1O11O1")
    c.row(4, 4, "111111111") if False else c.row(4, 5, "122221")
    c.row(5, 4, "wwwwwwwww"[:6] ) if False else c.row(5, 5, "1wRRw1")
    c.row(4, 2, "2222"); c.row(5, 2, "OwRw"); c.row(6, 3, "ww")
    c.row(6, 6, "11")
    c.row(7, 7, "22")
    c.r(4, 8, 11, 8, "2")
    c.r(5, 9, 10, 15, "5"); c.r(5, 9, 6, 15, "4"); c.r(9, 9, 10, 15, "6")   # hide armor
    c.r(5, 12, 10, 12, "n") if False else None
    c.r(5, 14, 10, 14, "N")
    c.r(3, 9, 4, 14, "2"); c.r(11, 9, 12, 14, "3")
    c.r(3, 15, 4, 15, "1"); c.r(11, 15, 12, 15, "3")
    c.r(5, 15, 7, 21, "2"); c.r(8, 15, 10, 21, "3"); c.r(7, 15, 7, 21, "3")
    c.r(5, 20, 7, 21, "N"); c.r(8, 20, 10, 21, "N")


def snapjaw():
    c = C()
    snapjaw_base(c)
    # crude club
    c.r(13, 8, 13, 17, "n"); c.r(12, 5, 14, 8, "N"); c.p(13, 5, "n")
    c.r(12, 14, 13, 15, "1")
    c.shadow(3, 14)
    return c.out()


def snapjaw_hunter():
    c = C()
    snapjaw_base(c)
    # bow on left, arrow string
    c.r(1, 5, 1, 17, "n") if False else None
    for x, y in ((2, 4), (1, 5), (1, 6), (0, 7), (0, 8), (0, 9), (0, 10), (0, 11), (0, 12), (1, 13), (1, 14), (2, 15)):
        c.p(x, y, "n")
    for y in range(5, 15):
        c.p(2 if 6 <= y <= 12 else 3, y, "w") if False else None
    c.p(2, 5, "w"); c.p(2, 14, "w")
    for y in range(6, 14):
        c.p(2, y, "w") if y in (6, 13) else None
    c.r(2, 9, 4, 9, "l")   # arrow
    c.p(5, 9, "2") if False else None
    c.r(3, 9, 4, 12, "1") if False else None
    c.r(3, 10, 4, 11, "1")
    c.p(2, 9, "g"); c.p(2, 10, "g")
    c.shadow(3, 12)
    return c.out()


def glowfish():
    c = C()
    # aura dots
    for x, y in ((2, 5), (13, 4), (7, 2), (1, 12), (14, 11), (4, 16), (12, 17), (8, 19), (3, 9), (11, 8)):
        c.p(x, y, "4")
    for x, y in ((6, 3), (10, 14), (2, 15)):
        c.p(x, y, "5")
    # body
    rows = {8: (5, 10), 9: (3, 12), 10: (2, 13), 11: (2, 13), 12: (2, 13), 13: (3, 12), 14: (5, 10)}
    for y, (a, b) in rows.items():
        for x in range(a, b + 1):
            c.p(x, y, "1" if y < 10 else "2" if y < 13 else "3")
    c.r(4, 10, 6, 10, "1") 
    # tail (right) and fins
    c.r(13, 9, 14, 9, "2"); c.r(14, 8, 15, 8, "2"); c.r(14, 14, 15, 14, "2"); c.r(14, 10, 14, 13, "2")
    c.r(15, 7, 15, 8, "5"); c.r(15, 14, 15, 15, "5")
    c.r(6, 6, 9, 7, "5"); c.r(7, 5, 8, 5, "4")   # dorsal
    c.r(7, 15, 9, 16, "5")
    c.p(3, 11, "w"); c.p(3, 12, "O") if False else None
    c.p(3, 10, "O"); c.p(2, 12, "w") if False else None
    c.r(8, 10, 9, 12, "4")   # glow belly
    c.p(5, 12, "5")
    c.shadow(3, 13, 20)
    return c.out()


def girshling():
    c = C()
    # small spider/solifuge: round body, eight legs
    c.r(5, 9, 10, 9, "1"); c.r(4, 10, 11, 13, "2"); c.r(5, 14, 10, 14, "3")
    c.r(4, 10, 6, 11, "1"); c.r(9, 12, 11, 13, "3")
    c.r(6, 6, 9, 8, "1"); c.r(6, 8, 9, 8, "2")   # head
    c.p(6, 7, "O"); c.p(9, 7, "O"); c.p(7, 6, "w"); c.p(8, 6, "w")
    c.r(6, 5, 6, 5, "4"); c.r(9, 5, 9, 5, "4")
    c.r(7, 9, 8, 9, "4") if False else None
    c.r(6, 11, 9, 12, "4"); c.r(7, 13, 8, 13, "5")
    for side in (0, 1):
        def X(x): return x if side == 0 else 15 - x
        for pts in (
            [(3, 9), (2, 8), (1, 7), (1, 6)],
            [(3, 10), (2, 10), (1, 10), (0, 11)],
            [(3, 12), (2, 13), (1, 14), (1, 15)],
            [(4, 14), (3, 15), (3, 16), (2, 17)],
        ):
            for x, y in pts:
                c.p(X(x), y, "6")
    c.shadow(2, 13, 19)
    return c.out()


def dog():
    c = C()
    # long low dog facing the viewer's left, 3/4
    c.r(4, 9, 12, 9, "1")
    c.r(3, 10, 13, 14, "2"); c.r(3, 10, 13, 11, "1"); c.r(3, 13, 13, 14, "3")
    # tail up
    c.r(13, 6, 14, 9, "2"); c.p(14, 5, "2"); c.p(14, 6, "1")
    # head
    c.r(1, 6, 5, 10, "1"); c.r(0, 9, 2, 11, "1"); c.r(0, 10, 1, 11, "2")
    c.p(0, 10, "O"); c.p(3, 7, "O")
    c.r(1, 5, 2, 6, "3"); c.r(4, 5, 5, 6, "3")  # ears
    c.p(1, 10, "O") if False else None
    c.r(0, 11, 1, 11, "w") if False else None
    c.r(2, 10, 3, 10, "5")   # collar
    # legs
    c.r(3, 15, 4, 18, "2"); c.r(6, 15, 7, 18, "3"); c.r(9, 15, 10, 18, "2"); c.r(12, 15, 13, 18, "3")
    c.r(3, 18, 4, 18, "1"); c.r(6, 18, 7, 18, "2"); c.r(9, 18, 10, 18, "1"); c.r(12, 18, 13, 18, "2")
    c.r(3, 15, 13, 15, "3") if False else None
    c.shadow(1, 14, 19)
    return c.out()


def salthopper():
    c = C()
    # big hind legs, body low, antennae, wings
    c.r(1, 3, 1, 5, "6"); c.r(2, 2, 2, 2, "6"); c.r(6, 3, 6, 6, "6"); c.p(5, 2, "6")
    c.r(3, 6, 6, 9, "1"); c.r(3, 6, 4, 7, "w") if False else None
    c.p(4, 7, "O"); c.p(6, 7, "O") if False else None
    c.r(2, 7, 3, 9, "1"); c.p(3, 7, "O")
    c.r(2, 9, 2, 9, "5")
    c.r(5, 8, 12, 12, "2"); c.r(5, 8, 12, 9, "1"); c.r(5, 12, 12, 12, "3")
    c.r(8, 8, 13, 10, "4"); c.r(9, 9, 14, 10, "5")   # wing cover
    c.r(6, 11, 9, 11, "5") if False else None
    # big jumping legs: thigh up, shin down
    c.r(10, 9, 12, 14, "1") if False else None
    c.r(9, 11, 13, 14, "2"); c.r(10, 12, 13, 14, "3")
    c.r(13, 14, 14, 17, "3"); c.r(14, 17, 15, 19, "6"); c.p(15, 19, "6")
    c.r(11, 15, 12, 15, "3") if False else None
    # front legs
    c.r(3, 12, 4, 17, "3"); c.r(6, 12, 7, 17, "2")
    c.r(2, 17, 4, 18, "6"); c.r(5, 17, 7, 18, "6")
    c.shadow(1, 14, 19)
    return c.out()


def croc():
    c = C()
    # low and long, seen from above-front, head left
    c.r(0, 9, 5, 11, "1"); c.r(0, 11, 5, 12, "2")      # snout
    c.r(0, 12, 4, 12, "w"); c.p(0, 12, "w"); c.p(2, 12, "w"); c.p(4, 12, "w")
    c.r(4, 7, 8, 13, "1"); c.p(5, 7, "O"); c.p(7, 7, "O") if False else None
    c.p(5, 7, "O"); c.p(8, 7, "O")
    c.r(5, 6, 5, 6, "4"); c.r(8, 6, 8, 6, "4")
    c.r(8, 8, 12, 13, "2"); c.r(8, 8, 13, 9, "1"); c.r(8, 12, 12, 13, "3")
    c.r(12, 9, 14, 12, "3"); c.r(14, 10, 15, 11, "3"); c.p(15, 11, "3")
    # back ridges
    for x in range(5, 14, 2):
        c.p(x, 8 if x < 12 else 9, "4")
    c.p(9, 9, "5"); c.p(11, 9, "5"); c.p(7, 8, "4")
    # stubby legs splayed
    c.r(4, 13, 5, 16, "3"); c.r(9, 13, 10, 16, "2"); c.r(2, 14, 3, 16, "2"); c.r(11, 14, 12, 16, "3")
    c.r(1, 16, 5, 17, "5"); c.r(9, 16, 13, 17, "6")
    c.shadow(0, 15, 18)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(), "four_arms": four_arms(),
    "carapace": carapace(), "mehmet": mehmet(), "farmer": farmer(), "snapjaw": snapjaw(),
    "snapjaw_hunter": snapjaw_hunter(), "glowfish": glowfish(), "girshling": girshling(),
    "dog": dog(), "salthopper": salthopper(), "croc": croc(),
}
