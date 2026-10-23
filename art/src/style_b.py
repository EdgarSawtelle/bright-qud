"""Style B - bold silhouette icons. One dominant flat mass + one strong accent shape."""


class C:
    def __init__(s):
        s.g = [["."] * 16 for _ in range(24)]

    def p(s, x, y, ch):
        if 0 <= x < 16 and 0 <= y < 24:
            s.g[y][x] = ch

    def m(s, x, y, ch):  # mirrored pair
        s.p(x, y, ch)
        s.p(15 - x, y, ch)

    def r(s, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.p(x, y, ch)

    def mr(s, x0, y0, x1, y1, ch):
        s.r(x0, y0, x1, y1, ch)
        s.r(15 - x1, y0, 15 - x0, y1, ch)

    def line(s, x0, y0, x1, y1, ch, mirror=False, th=1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            for t in range(th):
                (s.m if mirror else s.p)(x + t, y, ch)

    def ell(s, cx, cy, rx, ry, ch):
        for y in range(24):
            for x in range(16):
                if ((x - cx) / rx) ** 2 + ((y - cy) / ry) ** 2 <= 1:
                    s.p(x, y, ch)

    def shadow(s, x0, x1, y=23):
        for x in range(x0, x1 + 1):
            if s.g[y][x] == ".":
                s.g[y][x] = "x"

    def out(s):
        return ["".join(r) for r in s.g]


def human(c, top=3, body="2", legs="3", arms=True):
    """front-facing person: head 3 rows top.., body, legs."""
    c.r(5, top, 10, top + 6, "s")
    c.r(5, top + 6, 10, top + 6, "S")
    c.m(6, top + 3, "O")
    c.r(4, top + 7, 11, 18, body)
    c.r(4, top + 7, 5, top + 10, "1")
    c.r(10, 15, 11, 18, "3")
    c.r(4, 18, 11, 18, "3")
    c.r(5, 19, 6, 21, legs)
    c.r(9, 19, 10, 21, legs)
    c.r(5, 22, 6, 22, "O")
    c.r(9, 22, 10, 22, "O")
    if arms:
        c.r(3, top + 8, 3, 16, body)
        c.r(12, top + 8, 12, 16, body)
        c.m(3, 17, "s")
    c.shadow(4, 11)


def gunslinger():
    c = C()
    human(c, top=4, arms=False)
    c.r(5, 0, 10, 2, "2")      # crown
    c.r(5, 2, 10, 2, "1")
    c.r(5, 3, 10, 3, "4")      # hat band
    c.r(0, 3, 15, 3, "2")      # brim
    c.r(0, 4, 15, 4, "3")
    c.r(5, 3, 10, 3, "4")
    c.mr(2, 11, 4, 13, "2")    # arms out sideways
    c.mr(3, 10, 4, 10, "2")
    c.mr(0, 9, 1, 11, "5")     # big guns
    c.mr(0, 8, 0, 8, "4")
    c.mr(0, 9, 3, 9, "4")
    c.mr(1, 12, 2, 13, "6")
    c.mr(0, 10, 0, 11, "5")
    c.m(2, 13, "s")
    c.r(7, 11, 8, 17, "4")     # coat line
    return c.out()


def winged():
    c = C()
    W = [1, 1, 2, 2, 3, 3, 4, 4, 4, 4, 4, 4, 4, 4, 3, 3, 2, 2, 1, 1, 0]
    for i, w in enumerate(W):
        y = 2 + i
        for x in range(0, w + 1):
            c.m(x, y, "5" if (x + i) % 5 else "6")
        c.m(0, y, "4")
    c.mr(0, 2, 0, 12, "4")
    for y in (7, 11, 15):
        c.mr(1, y, 3, y, "6")
    human(c, top=3, arms=False)
    c.r(5, 3, 10, 3, "3")
    c.mr(3, 11, 3, 15, "2")
    return c.out()


def horned():
    c = C()
    human(c, top=4)
    c.r(5, 4, 10, 4, "3")
    # giant horns
    for (x, y) in [(4, 5), (3, 4), (3, 3), (2, 2), (2, 1), (1, 0)]:
        c.m(x, y, "5")
    for (x, y) in [(4, 4), (4, 3), (3, 2), (3, 1), (2, 0)]:
        c.m(x, y, "4")
    c.mr(1, 1, 1, 2, "5")
    c.m(5, 5, "5")
    c.m(2, 3, "6")
    c.r(7, 12, 8, 14, "4")
    return c.out()


def four_arms():
    c = C()
    human(c, top=3, arms=False)
    c.r(6, 10, 9, 18, "2")
    c.r(6, 10, 7, 12, "1")
    c.r(8, 16, 9, 18, "3")
    c.r(5, 3, 10, 3, "3")
    c.line(5, 10, 0, 5, "5", mirror=True, th=2)   # upper arms up/out
    c.line(5, 13, 0, 15, "5", mirror=True, th=2)  # lower arms down/out
    c.line(5, 9, 1, 5, "4", mirror=True)
    c.line(5, 12, 1, 14, "4", mirror=True)
    c.m(0, 4, "s")
    c.m(0, 14, "s")
    c.m(0, 5, "s")
    c.m(0, 16, "s")
    return c.out()


def carapace():
    c = C()
    c.ell(7.5, 14, 7.6, 6.8, "5")
    c.ell(7.5, 13, 6.2, 5, "4")
    c.r(0, 14, 15, 19, "5")
    c.ell(7.5, 15, 7.6, 6, "5")
    c.r(2, 8, 13, 9, "4")
    c.r(1, 18, 14, 19, "6")
    c.r(3, 12, 12, 12, "6")
    c.line(7, 8, 7, 18, "6")
    c.line(8, 8, 8, 18, "6")
    c.r(5, 2, 10, 8, "s")
    c.r(5, 8, 10, 8, "S")
    c.m(6, 5, "O")
    c.r(4, 9, 11, 9, "2")
    c.r(5, 10, 10, 16, "2")
    c.r(5, 10, 6, 12, "1")
    c.r(9, 14, 10, 16, "3")
    c.mr(1, 9, 3, 11, "4")  # shoulder plates
    c.mr(1, 9, 2, 9, "5")
    c.r(5, 17, 6, 21, "3")
    c.r(9, 17, 10, 21, "3")
    c.r(5, 22, 6, 22, "O")
    c.r(9, 22, 10, 22, "O")
    c.shadow(3, 12)
    return c.out()


def mehmet():
    c = C()
    human(c, top=3)
    c.r(5, 3, 10, 4, "w")      # white hair
    c.r(4, 5, 4, 9, "w")
    c.r(11, 5, 11, 9, "w")
    c.r(5, 8, 10, 12, "w")     # big beard
    c.r(6, 13, 9, 13, "w")
    c.r(7, 6, 8, 6, "s")
    c.m(6, 6, "O")
    c.r(7, 9, 8, 9, "S")
    c.r(13, 5, 13, 22, "N")    # hoe
    c.r(12, 4, 15, 5, "5")
    c.r(14, 6, 15, 7, "5")
    c.r(12, 4, 12, 4, "4")
    c.r(13, 16, 13, 17, "s")
    return c.out()


def farmer():
    c = C()
    human(c, top=4)
    c.r(3, 2, 12, 3, "t")      # straw hat
    c.r(5, 1, 10, 1, "t")
    c.r(4, 4, 11, 4, "t")
    c.r(5, 4, 10, 4, "T") if False else None
    c.r(6, 11, 9, 13, "1")
    # sickle
    c.r(13, 11, 13, 17, "N")
    c.line(14, 10, 15, 8, "5")
    c.line(12, 9, 14, 8, "4")
    c.p(12, 10, "4"); c.p(12, 11, "4")
    c.p(13, 9, "4")
    c.p(14, 9, "5"); c.p(15, 9, "5")
    return c.out()


def snap_head(c, top=2):
    c.r(3, top + 3, 12, top + 8, "2")           # head
    c.r(4, top + 2, 11, top + 2, "2")
    for i in range(4):                          # big ears
        c.m(3 - i // 2, top + 2 - i, "2")
        c.m(4 - i // 2, top + 2 - i, "2")
    c.m(3, top + 1, "5")
    c.m(3, top + 2, "5")
    c.m(2, top, "2")
    c.r(5, top + 3, 10, top + 3, "3")
    c.m(5, top + 4, "O")
    c.r(4, top + 6, 11, top + 9, "1")           # big snout
    c.r(4, top + 8, 11, top + 9, "5")           # jaw/mouth
    c.r(6, top + 6, 9, top + 6, "O")            # nose
    c.m(5, top + 8, "w")
    c.m(7, top + 8, "w") if False else None
    c.p(7, top + 8, "w"); c.p(8, top + 8, "w")
    c.r(4, top + 10, 11, top + 10, "3")


def snapjaw(bow=False):
    c = C()
    snap_head(c, 2)
    c.r(4, 13, 11, 19, "2")
    c.r(3, 14, 3, 18, "2")
    c.r(12, 14, 12, 18, "2")
    c.r(4, 13, 5, 15, "1")
    c.r(10, 17, 11, 19, "3")
    c.r(4, 16, 11, 16, "5")                  # belt/trim
    c.r(5, 20, 6, 21, "3")
    c.r(9, 20, 10, 21, "3")
    c.r(5, 22, 6, 22, "O")
    c.r(9, 22, 10, 22, "O")
    c.mr(2, 19, 3, 19, "s") if False else None
    if bow:
        c.r(13, 6, 14, 6, "5")
        c.line(14, 7, 15, 11, "5", th=1)
        c.r(15, 11, 15, 16, "5")
        c.line(15, 17, 14, 21, "5")
        c.r(13, 22, 14, 22, "5")
        c.r(13, 7, 13, 21, "w")
        c.r(13, 14, 14, 14, "N")
        c.p(14, 5, "4"); c.p(14, 22, "4")
    else:
        c.r(13, 8, 13, 20, "N")
        c.r(12, 6, 14, 8, "5")
        c.p(13, 5, "4")
        c.p(13, 6, "4")
    c.shadow(3, 12)
    return c.out()


def glowfish():
    c = C()
    cx, cy = 7.5, 12
    for y in range(24):
        for x in range(16):
            d = ((x - cx) ** 2 + (y - cy) ** 2) ** 0.5
            if 6.2 <= d <= 7.7:
                c.p(x, y, "5")
            if 6.9 <= d <= 7.7 and y < 12 and x < 8:
                c.p(x, y, "4")
    c.line(2, 12, 2, 12, "4")
    c.ell(7.5, 12, 4.6, 3.2, "2")                 # body
    c.line(2, 9, 2, 15, "2")
    c.r(1, 10, 3, 14, "2")                        # tail
    c.r(1, 9, 1, 15, "3")
    c.r(10, 10, 11, 11, "1")
    c.r(11, 12, 11, 12, "2")
    c.p(10, 11, "O"); c.p(10, 10, "O") if False else None
    c.r(6, 9, 8, 9, "1")
    c.r(6, 15, 8, 15, "3")
    c.r(5, 11, 5, 13, "3")                        # gill
    c.r(7, 8, 8, 8, "4")                          # dorsal
    c.r(7, 7, 7, 7, "4")
    return c.out()


def girshling():
    c = C()
    c.ell(7.5, 12, 3.5, 3.3, "2")
    c.r(5, 10, 6, 10, "1")
    c.r(9, 14, 10, 14, "3")
    c.m(6, 11, "O")
    c.m(5, 12, "O") if False else None
    for (x, y) in [(0, 5), (0, 9), (0, 14), (1, 19), (3, 21)]:
        c.line(5, 12, x, y, "5", mirror=True)
    for (x, y) in [(0, 5), (0, 9), (0, 14), (1, 19), (3, 21)]:
        c.m(x, y, "4")
    c.line(7, 8, 7, 3, "4", mirror=True)
    c.m(6, 3, "4")
    c.shadow(2, 13)
    return c.out()


def dog():
    c = C()
    c.r(2, 10, 10, 15, "2")                 # body
    c.r(2, 10, 10, 11, "1")
    c.r(2, 15, 10, 15, "3")
    c.r(9, 5, 14, 11, "2")                  # head
    c.r(9, 5, 14, 6, "1")
    c.r(13, 9, 15, 11, "1")                 # snout
    c.p(15, 9, "O")
    c.p(12, 7, "O")
    c.r(8, 3, 9, 7, "3")                    # ear
    c.r(9, 3, 9, 3, "3")
    c.r(8, 3, 8, 6, "3")
    c.r(9, 11, 12, 12, "5")                 # collar accent
    c.r(9, 11, 12, 11, "4")
    c.r(3, 16, 4, 20, "3")
    c.r(8, 16, 9, 20, "3")
    c.r(3, 21, 4, 21, "O"); c.r(8, 21, 9, 21, "O")
    c.r(1, 6, 2, 11, "2")                   # tail up
    c.r(0, 5, 1, 5, "2")
    c.r(1, 6, 1, 8, "5")
    c.shadow(2, 13, 22)
    return c.out()


def salthopper():
    c = C()
    c.r(5, 9, 11, 13, "2")                  # body
    c.r(5, 9, 11, 9, "1")
    c.r(5, 13, 11, 13, "3")
    c.r(11, 8, 14, 12, "2")                 # head
    c.r(11, 8, 14, 8, "1")
    c.p(13, 10, "O"); c.p(13, 9, "O")
    c.line(13, 7, 15, 2, "4")               # antenna
    c.line(12, 7, 13, 3, "4")
    c.line(4, 9, 1, 5, "5", th=2)           # huge hind leg
    c.line(2, 6, 1, 19, "5", th=1)
    c.r(0, 20, 3, 20, "6")
    c.line(5, 13, 2, 17, "5", th=2)
    c.line(7, 14, 7, 20, "4")
    c.line(10, 14, 11, 20, "4")
    c.r(6, 20, 8, 20, "6")
    c.r(10, 20, 12, 20, "6")
    c.r(4, 10, 4, 12, "4")
    c.shadow(0, 14, 22)
    return c.out()


def croc():
    c = C()
    c.r(0, 13, 8, 16, "2")                  # body
    c.line(0, 13, 0, 13, "2")
    c.r(0, 12, 0, 14, "3")
    c.r(2, 11, 8, 12, "2")                  # back
    for x in range(2, 9, 2):
        c.p(x, 10, "5")                     # ridge accent
        c.p(x, 11, "4")
    c.r(8, 11, 15, 13, "2")                 # long upper jaw
    c.r(8, 9, 11, 13, "2")
    c.r(9, 9, 10, 9, "1")
    c.r(8, 11, 15, 11, "1")
    c.p(10, 10, "O")
    c.r(10, 14, 15, 15, "2")                # lower jaw
    c.r(10, 14, 15, 14, "w") if False else None
    c.r(9, 14, 15, 14, "O")
    for x in (10, 12, 14):
        c.p(x, 14, "w")
    c.p(15, 12, "O")
    c.r(1, 17, 3, 19, "3")
    c.r(7, 17, 9, 19, "3")
    c.r(1, 20, 3, 20, "O"); c.r(7, 20, 9, 20, "O")
    c.r(0, 15, 8, 16, "5")                  # belly accent
    c.r(0, 16, 8, 16, "4")
    c.shadow(0, 15, 22)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(),
    "four_arms": four_arms(), "carapace": carapace(), "mehmet": mehmet(),
    "farmer": farmer(), "snapjaw": snapjaw(), "snapjaw_hunter": snapjaw(True),
    "glowfish": glowfish(), "girshling": girshling(), "dog": dog(),
    "salthopper": salthopper(), "croc": croc(),
}
