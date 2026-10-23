"""Style B2 - shape language."""


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


def rhead(c, top, x0=5, x1=10, h=6, skin="s"):
    """soft rounded head"""
    c.r(x0, top, x1, top + h - 1, skin)
    for x, y in [(x0, top), (x1, top), (x0, top + h - 1), (x1, top + h - 1)]:
        c.p(x, y, ".")
    c.r(x0, top + h - 1, x1, top + h - 1, "S") if False else None
    c.r(x0 + 1, top + h - 1, x1 - 1, top + h - 1, "S")


def pillar(c, top=2, body="2", x0=5, x1=10, legs="3", arms=True, round_=True):
    """tall vertical pillar person; soft corners."""
    rhead(c, top, 5, 10, 6)
    c.m(6, top + 3, "O")
    b0 = top + 6
    c.r(x0, b0, x1, 19, body)
    c.r(x0, b0, x0 + 1, b0 + 4, "1")
    c.r(x1 - 1, 15, x1, 19, "3")
    if round_:
        c.m(x0, b0, "."); c.m(x0, 19, ".")
        c.m(x0, b0 + 1, body) if False else None
    c.r(6, 20, 7, 22, legs)
    c.r(8, 20, 9, 22, legs)
    c.p(7, 20, "O") if False else None
    c.r(6, 22, 9, 22, "O")
    c.p(7, 22, "."); c.p(8, 22, ".") if False else None
    if arms:
        c.r(x0 - 2, b0 + 1, x0 - 1, 17, body)
        c.r(x1 + 1, b0 + 1, x1 + 2, 17, body)
        c.m(x0 - 2, 18, "s"); c.m(x0 - 1, 18, "s")
        c.m(x0 - 2, b0, "."); 
    c.shadow(4, 11)


def gunslinger():
    c = C()
    pillar(c, top=4, arms=False)
    # tall hat: pillar crown, thin brim
    c.r(5, 0, 10, 3, "2")
    c.r(5, 0, 6, 3, "1")
    c.r(5, 3, 10, 3, "4")
    c.r(2, 4, 13, 4, "3")
    c.r(7, 11, 8, 19, "4")
    # arms straight down holding long guns pointing down: two vertical lines
    c.mr(3, 10, 4, 17, "2")
    c.mr(3, 18, 4, 18, "s")
    c.mr(2, 18, 2, 22, "l")
    c.mr(2, 21, 3, 22, "N")
    return c.out()


def winged():
    c = C()
    # wide wings break the pillar
    for i, w in enumerate([0, 1, 2, 3, 4, 5, 5, 5, 5, 4, 4, 3, 3, 2, 1]):
        y = 6 + i
        for x in range(0, w + 1):
            c.m(x, y, "5" if x else "4")
    c.mr(0, 3, 0, 8, "4")
    c.mr(0, 1, 0, 2, "5")
    c.mr(1, 5, 1, 8, "6")
    for y in (11, 14):
        c.mr(1, y, 3, y, "6")
    pillar(c, top=3, arms=False)
    c.mr(3, 10, 4, 17, "2")
    c.mr(3, 18, 4, 18, "s")
    return c.out()


def horned():
    c = C()
    pillar(c, top=5)
    # horns sweep up and out from the head, tall
    for (x, y) in [(4, 5), (3, 4), (3, 3), (2, 2), (2, 1), (1, 0)]:
        c.m(x, y, "5")
    for (x, y) in [(4, 4), (3, 2), (2, 0)]:
        c.m(x, y, "4")
    c.m(4, 6, "5")
    c.m(3, 5, "5")
    c.m(2, 3, "5")
    c.m(1, 1, "6")
    c.r(7, 13, 8, 17, "4")
    return c.out()


def four_arms():
    c = C()
    pillar(c, top=3, arms=False)
    c.line(5, 10, 0, 5, "5", mirror=True, th=2)
    c.line(5, 14, 0, 16, "5", mirror=True, th=2)
    c.line(5, 9, 1, 4, "4", mirror=True)
    c.line(5, 13, 1, 15, "4", mirror=True)
    c.m(0, 4, "s"); c.m(0, 3, "s"); c.m(0, 16, "s"); c.m(0, 17, "s")
    c.m(1, 3, "s"); c.m(1, 17, "s")
    return c.out()


def carapace():
    c = C()
    # shell dome over the pillar
    c.ell(7.5, 13, 7.6, 8.8, "5")
    c.r(0, 14, 15, 22, ".")
    c.ell(7.5, 12, 6.0, 7.0, "4")
    c.r(0, 14, 15, 14, ".") if False else None
    for i in range(3):
        c.line(2 + i * 0, 6 + i * 3, 13, 6 + i * 3, "6") if False else None
    c.line(7, 5, 7, 20, "6"); c.line(8, 5, 8, 20, "6")
    c.r(3, 10, 12, 10, "6"); c.r(2, 14, 13, 14, "6")
    c.r(5, 3, 10, 8, ".") if False else None
    # head sticks out the top, in front
    rhead(c, 1, 5, 10, 6)
    c.r(4, 7, 11, 8, "5")
    c.m(6, 4, "O")
    c.r(5, 7, 10, 7, "S") if False else None
    c.mr(0, 12, 1, 18, "5")
    c.r(4, 19, 11, 19, "5")
    c.r(5, 20, 6, 22, "3"); c.r(9, 20, 10, 22, "3")
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.shadow(0, 15)
    return c.out()


def mehmet():
    c = C()
    pillar(c, top=2)
    c.r(5, 2, 10, 3, "w")
    c.r(4, 4, 4, 9, "w"); c.r(11, 4, 11, 9, "w")
    c.r(5, 7, 10, 12, "w")
    c.r(6, 13, 9, 13, "w")
    c.r(6, 5, 9, 6, "s")
    c.m(6, 5, "O")
    c.r(7, 9, 8, 9, "S")
    c.r(14, 4, 14, 22, "N")
    c.r(12, 3, 15, 4, "5"); c.p(12, 5, "5"); c.p(12, 6, "4") if False else None
    c.r(12, 3, 12, 3, "4")
    c.r(13, 17, 13, 18, "s")
    return c.out()


def farmer():
    c = C()
    pillar(c, top=4)
    # round soft straw hat dome
    c.r(5, 1, 10, 3, "t"); c.m(5, 1, ".")
    c.r(3, 4, 12, 4, "t"); c.m(3, 4, ".")
    c.r(6, 11, 9, 14, "1")
    c.r(13, 11, 13, 18, "N")
    c.r(13, 9, 14, 9, "5"); c.r(14, 8, 14, 10, "5"); c.p(15, 8, "4"); c.p(15, 9, "5") if False else None
    c.p(14, 7, "4")
    return c.out()


def snap_head(c, top=1):
    pass


def snapjaw(bow=False):
    c = C()
    G = [
        "................",
        "....2.....2.....",
        "...323...323....",
        "...32222222.....",
        "..3222222221....",
        "..322O2222111111",
        "...2222221111111",
        "..32222.OwwOwwO.",
        "..3222...O.O.O..",
        ".32222222222....",
        ".3222222222221..",
        "..322222222211..",
        "...3222222221...",
        "...32222222.....",
        "...3555555553...",
        "....55555555....",
        "....5.5.5.5.5...",
        "....22....22....",
        "....22....22....",
        "....33....33....",
        "....3O....3O....",
        "................",
        "................",
        "................",
    ]
    return None


def snapjaw(bow=False):
    c = C()
    G = [
        "................",
        "....3.....3.....",
        "....23...23.....",
        "....222..222....",
        "...32222222111..",
        "..3222O2222111O.",
        "..32222222111111",
        "..3.2222.OwOwOw.",
        "..32222....3333.",
        ".3322222........",
        "..3.22211.......",
        "..3.22213.......",
        "...322211.......",
        "....22213.......",
        "....2222........",
        "....55555.......",
        "....5555........",
        "....5.5.5.......",
        "................",
        "................",
        "................",
        "................",
        "................",
        "................",
    ]
    for y, row in enumerate(G):
        for x, ch in enumerate(row):
            if ch != ".":
                c.p(x, y, ch)
    c.p(1, 10, "3"); c.p(1, 12, "3"); c.p(2, 14, "3"); c.p(3, 13, "3")   # mane spikes
    c.p(1, 8, "3")
    # thin legs, knees bent
    c.line(5, 17, 4, 22, "3"); c.line(7, 17, 8, 22, "3")
    c.line(8, 22, 9, 22, "O"); c.line(3, 22, 4, 22, "O")
    c.p(5, 20, "3"); c.p(7, 20, "3")
    # thin arm forward
    c.line(8, 10, 12, 13, "2")
    c.p(12, 13, "s"); c.p(13, 13, "s")
    if bow:
        for (x, y) in [(13, 5), (14, 6), (15, 8), (15, 9), (15, 10), (15, 11), (15, 12), (15, 13), (15, 14), (15, 15), (15, 16), (15, 17), (14, 18), (13, 19)]:
            c.p(x, y, "N")
        c.p(14, 5, "N"); c.p(14, 19, "N")
        c.line(13, 6, 13, 18, "w")
        c.p(13, 13, "s")
        c.p(12, 13, "s")
        c.r(0, 15, 1, 20, "N") if False else None
        c.r(2, 7, 2, 7, "3") if False else None
        c.p(0, 9, "N"); c.p(0, 10, "N"); c.p(0, 11, "N"); c.p(0, 12, "N") if False else None
        c.p(0, 6, "4"); c.p(1, 7, "5"); c.p(0, 7, "4"); c.p(1, 8, "N")
        c.r(4, 4, 9, 4, "4")      # headband
        c.p(3, 4, "5"); c.p(3, 3, "4")
    else:
        c.r(14, 9, 14, 22, "N")
        c.r(13, 6, 15, 9, "5"); c.p(14, 5, "4"); c.p(12, 7, "4"); c.p(15, 6, "4")
        c.p(12, 13, "s"); c.p(13, 13, "s"); c.p(14, 13, "s")
    c.shadow(2, 10)
    return c.out()


def glowfish():
    c = C()
    # soft glow halo: dotted
    for (x, y) in [(2, 6), (7, 4), (12, 6), (14, 11), (13, 17), (8, 19), (3, 18), (1, 12), (5, 5), (10, 5), (11, 19), (4, 19)]:
        c.p(x, y, "4")
    # teardrop: round head right, tapering tail left
    c.ell(9.5, 12, 5.6, 4.8, "2")
    c.ell(9.5, 11, 4.4, 3, "1")
    c.line(5, 12, 1, 12, "2", th=1)
    c.r(3, 11, 6, 13, "2")
    c.r(1, 9, 2, 15, "5")                  # tail fin
    c.r(0, 8, 0, 16, "5") if False else None
    c.p(2, 8, "5"); c.p(2, 16, "5") ; c.p(1, 8, "4"); c.p(1, 16, "4")
    c.r(8, 7, 11, 7, "4"); c.r(8, 6, 10, 6, "4") ; c.p(9, 5, "4") if False else None
    c.r(8, 17, 10, 17, "5")
    c.p(12, 10, "O"); c.p(13, 10, "O") if False else None
    c.p(12, 11, "O")
    c.r(14, 13, 14, 13, "O")
    c.r(9, 11, 9, 14, "3")
    return c.out()


def girshling():
    c = C()
    c.ell(7.5, 12.5, 2.6, 3.4, "2")                   # small body
    c.r(6, 10, 9, 10, "1")
    c.r(6, 15, 9, 15, "3")
    c.m(6, 11, "O")
    # jointed ^ legs splayed wide
    for pts in [[(5, 10), (2, 5), (0, 9)], [(5, 12), (1, 9), (0, 14)],
                [(5, 14), (1, 15), (0, 21)], [(6, 16), (3, 19), (2, 23)]]:
        for (a, b) in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1], "5", mirror=True)
        c.m(pts[1][0], pts[1][1], "4")
        c.m(pts[2][0], pts[2][1], "6")
    # big pincer jaws forward
    for (x, y) in [(6, 9), (5, 8), (5, 7), (4, 6), (4, 5), (4, 4), (5, 3), (6, 3), (6, 4)]:
        c.m(x, y, "4")
    for (x, y) in [(5, 4), (5, 5), (5, 6), (6, 8)]:
        c.m(x, y, "5")
    c.m(6, 2, "w"); c.m(7, 3, "w")
    c.shadow(1, 14, 23)
    return c.out()


def dog():
    c = C()
    # wide low rounded wedge: big oval body, round head, soft floppy ear
    c.ell(6.5, 15, 6.4, 3.8, "2")
    c.ell(6.5, 14, 5.6, 2.2, "1")
    c.ell(12, 11, 3.4, 3.2, "2")
    c.r(12, 12, 15, 14, "1")
    c.p(15, 12, "O")
    c.p(13, 10, "O")
    c.ell(10, 9, 1.6, 2.3, "3")            # floppy ear
    c.r(9, 14, 13, 15, "5")                # collar
    c.p(9, 14, "4"); c.p(10, 14, "4")
    c.line(1, 14, 0, 9, "2"); c.line(2, 13, 1, 9, "2")   # curled tail
    c.p(0, 8, "1")
    c.r(2, 18, 3, 21, "3"); c.r(8, 18, 9, 21, "3"); c.r(11, 17, 12, 21, "3")
    c.r(2, 21, 3, 21, "O"); c.r(8, 21, 9, 21, "O"); c.r(11, 21, 12, 21, "O")
    c.shadow(0, 14, 22)
    return c.out()


def salthopper():
    c = C()
    # long antennae
    c.line(6, 4, 4, 2, "4"); c.line(4, 2, 2, 0, "4"); c.line(9, 4, 11, 2, "4"); c.line(11, 2, 13, 0, "4")
    c.r(6, 4, 9, 7, "2"); c.r(6, 4, 9, 4, "1")        # head
    c.p(5, 5, "O"); c.p(10, 5, "O"); c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(5, 8, 10, 11, "2"); c.r(5, 8, 6, 9, "1")      # thorax
    for y in range(12, 21):                            # long abdomen, tapering
        x0 = 6 if y < 17 else 7
        x1 = 9 if y < 17 else 8
        c.r(x0, y, x1, y, "2" if y % 2 == 0 else "4")
    c.r(7, 20, 8, 21, "3")
    c.r(7, 8, 8, 15, "1") if False else None
    # front legs
    c.line(5, 8, 3, 6, "5", mirror=True); c.line(3, 6, 1, 8, "5", mirror=True)
    c.line(5, 10, 2, 11, "5", mirror=True)
    # big hind legs: sharp zigzag out to the sides
    for pts in [[(5, 11), (0, 13), (3, 17), (0, 21)], [(5, 12), (1, 14), (3, 18), (1, 22)]]:
        for (a, b) in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1], "5", mirror=True)
    c.mr(0, 13, 0, 13, "6"); c.mr(3, 17, 3, 17, "6")
    c.shadow(0, 15, 22)
    return c.out()


def croc():
    c = C()
    c.r(0, 13, 9, 18, "2")                 # body
    c.r(9, 12, 15, 15, "2")                # snout wedge
    c.r(9, 12, 15, 12, "1")
    c.r(0, 13, 9, 13, "1")
    c.p(10, 11, "O"); c.p(10, 12, "O")
    c.p(15, 12, "O")
    c.r(9, 16, 15, 16, "O")                # mouth
    c.r(10, 17, 15, 17, "3")
    for x in (9, 11, 13, 15):
        c.p(x, 16, "w")
    for x in (10, 12, 14):
        c.p(x, 15, "w")
    for x in range(1, 9, 2):               # sawtooth ridge
        c.p(x, 12, "5"); c.p(x, 11, "4"); c.p(x + 1, 13, "5")
    c.r(0, 18, 8, 18, "5")
    c.r(0, 14, 0, 16, "3")
    c.line(0, 18, 0, 18, "3")
    c.line(2, 19, 0, 22, "3", th=2); c.line(7, 19, 9, 22, "3", th=2)
    c.line(11, 18, 13, 22, "3", th=2) if False else None
    c.shadow(0, 15, 22)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(),
    "four_arms": four_arms(), "carapace": carapace(), "mehmet": mehmet(),
    "farmer": farmer(), "snapjaw": snapjaw(), "snapjaw_hunter": snapjaw(True),
    "glowfish": glowfish(), "girshling": girshling(), "dog": dog(),
    "salthopper": salthopper(), "croc": croc(),
}
