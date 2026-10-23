"""Style B4 - chunky action poses: stocky figures caught doing their thing."""


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

    def mr(s, x0, y0, x1, y1, ch):
        s.r(x0, y0, x1, y1, ch)
        s.r(15 - x1, y0, 15 - x0, y1, ch)

    def m(s, x, y, ch):
        s.p(x, y, ch)
        s.p(15 - x, y, ch)

    def line(s, x0, y0, x1, y1, ch):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            s.p(round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n), ch)

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


def stocky(c, top, body="2", legs="3", hi="1"):
    """stocky human: small head rows top..top+4, broad torso, thick legs."""
    c.r(5, top, 10, top + 4, "s")
    c.r(5, top + 4, 10, top + 4, "S")
    c.m(6, top + 2, "O")
    c.r(3, top + 5, 12, top + 12, body)
    c.r(3, top + 5, 5, top + 6, hi)
    c.r(3, top + 12, 12, top + 12, "3")
    c.r(4, top + 13, 7, top + 16, legs)
    c.r(8, top + 13, 11, top + 16, legs)
    c.r(7, top + 13, 8, top + 15, "O")
    c.mr(4, top + 17, 7, top + 17, "O")


def gunslinger():
    c = C()
    stocky(c, 4)
    c.r(4, 0, 11, 2, "2")
    c.r(4, 0, 11, 0, "1")
    c.r(4, 2, 11, 2, "4")
    c.r(1, 3, 14, 3, "2")
    c.r(0, 4, 15, 4, "3")
    c.r(1, 4, 14, 4, "3")
    c.r(4, 4, 11, 4, "3")
    # coat tails
    c.mr(3, 21, 4, 22, "2")
    # arms out, guns aiming both ways
    c.mr(1, 10, 3, 12, "2")
    c.mr(0, 8, 2, 9, "l")
    c.mr(0, 9, 0, 9, "L")
    c.mr(2, 9, 3, 11, "L")
    c.mr(0, 7, 1, 7, "4")
    c.mr(0, 8, 0, 8, "y")
    c.r(7, 11, 8, 15, "4")
    c.shadow(3, 12)
    return c.out()


def winged():
    c = C()
    stocky(c, 3, body="2")
    cols = {0: (0, 6), 1: (1, 8), 2: (3, 10), 3: (6, 11)}
    for x, (y0, y1) in cols.items():
        c.mr(x, y0, x, y1, "4")
        c.mr(x, y0 + 1, x, y1 - 1, "5")
    c.mr(0, 2, 0, 3, "4")
    c.mr(1, 5, 1, 5, "6"); c.mr(2, 7, 2, 7, "6")
    c.mr(0, 7, 0, 7, ".")
    c.mr(1, 9, 1, 9, ".")
    c.shadow(4, 11, 22)
    c.shadow(4, 11, 23)
    return c.out()


def horned():
    c = C()
    c.r(3, 6, 12, 14, "2")
    c.r(3, 6, 5, 7, "1")
    c.r(3, 13, 12, 14, "3")
    c.r(5, 7, 10, 11, "s")        # head lowered into shoulders
    c.r(5, 11, 10, 11, "S")
    c.m(6, 9, "O")
    c.mr(3, 6, 4, 8, "4")         # horn bases
    c.mr(1, 7, 3, 8, "4")
    c.mr(0, 8, 1, 11, "4")
    c.mr(0, 11, 0, 12, "1")
    c.mr(1, 8, 1, 8, "1")
    c.mr(0, 9, 0, 9, "5")
    c.r(2, 10, 3, 13, "2")
    c.r(2, 14, 3, 14, "s")
    c.r(4, 15, 7, 18, "3")        # charging stride
    c.r(8, 15, 11, 17, "3")
    c.r(3, 19, 6, 21, "3")
    c.r(10, 18, 13, 19, "3")
    c.r(2, 22, 6, 22, "O")
    c.r(10, 20, 14, 20, "O")
    c.shadow(2, 14, 22)
    c.shadow(2, 14, 23)
    return c.out()


def four_arms():
    c = C()
    stocky(c, 3, body="2")
    # upper arms raised, lower arms out
    c.mr(1, 7, 2, 9, "2")
    c.mr(0, 5, 1, 7, "2")
    c.mr(0, 4, 1, 5, "s")
    c.mr(0, 11, 2, 13, "4")
    c.mr(0, 13, 1, 14, "s")
    c.mr(1, 9, 2, 10, "2")
    c.shadow(3, 12)
    return c.out()


def carapace():
    c = C()
    c.ell(7.5, 8.5, 7.6, 5.6, "4")   # hunched shell dome
    c.ell(7.5, 8, 6, 4, "5")
    c.r(2, 5, 13, 5, "6")
    c.r(5, 4, 10, 4, "4")
    c.r(7, 4, 8, 8, "6")
    c.r(3, 9, 12, 15, "2")
    c.r(5, 5, 10, 9, "s")          # low head
    c.r(5, 9, 10, 9, "S")
    c.m(6, 7, "O")
    c.r(5, 5, 10, 5, "4")
    c.mr(1, 8, 3, 9, "4")          # pauldrons
    c.mr(1, 8, 1, 8, "1")
    c.mr(2, 10, 4, 12, "s")        # fists up
    c.mr(2, 10, 4, 10, "4")
    c.mr(2, 13, 3, 14, "2")
    c.r(3, 15, 12, 15, "3")
    c.mr(2, 16, 5, 20, "3")        # braced wide stance
    c.mr(1, 21, 5, 21, "O")
    c.shadow(1, 14)
    return c.out()


def mehmet():
    c = C()
    # leaning pose: body shifted slightly left, hoe planted right
    stocky(c, 3, body="2")
    c.r(5, 8, 10, 11, "w")        # beard
    c.r(6, 11, 9, 12, "w")
    c.r(5, 3, 10, 4, "w")         # white hair
    c.m(6, 5, "O")
    c.r(5, 5, 10, 7, "s")
    c.m(6, 6, "O")
    c.r(6, 8, 9, 8, "w")
    c.r(12, 11, 13, 13, "s")      # hand on hoe
    # hoe handle
    c.r(13, 4, 13, 22, "n")
    c.r(14, 4, 14, 22, "N")
    c.r(11, 2, 14, 3, "l")        # hoe blade
    c.r(11, 3, 12, 4, "L")
    c.r(3, 10, 3, 14, "2")
    c.shadow(3, 14)
    return c.out()


def farmer():
    c = C()
    stocky(c, 4, body="2")
    c.r(4, 2, 11, 3, "t")         # straw hat
    c.r(3, 4, 12, 4, "t")
    c.r(5, 1, 10, 1, "t")
    c.r(4, 3, 11, 3, "4")
    # right arm swinging up with sickle
    c.r(12, 7, 13, 9, "2")
    c.r(13, 4, 14, 6, "s")
    c.line(13, 3, 15, 1, "l")
    c.r(14, 0, 15, 0, "l")
    c.p(15, 1, "w")
    c.p(14, 2, "L")
    c.p(13, 3, "L")
    c.r(1, 10, 2, 12, "2")
    c.r(1, 13, 2, 13, "s")
    c.shadow(3, 12)
    return c.out()


def hyena(c, x, y):
    """snapjaw head (rows y..y+6 from x), snout pointing left, ears up."""


def snapjaw():
    c = C()
    # mid-lunge: hunched forward, head low-left, club raised high right
    c.r(10, 1, 14, 4, "N")
    c.r(11, 1, 13, 2, "n")
    c.r(11, 5, 12, 9, "n")
    c.r(10, 8, 12, 10, "S")       # fist
    # ears
    for x, y in [(4,1),(4,2),(3,3),(4,3),(3,4),(4,4),(5,4),(7,1),(7,2),(7,3),(8,3),(6,4),(7,4),(8,4)]:
        c.p(x, y, "3" if x in (3, 8) else "2")
    # head: long snout left, mane
    c.r(3, 5, 8, 7, "2")
    c.r(0, 6, 4, 8, "2")
    c.r(0, 8, 5, 9, "w")          # teeth jaw
    c.r(0, 9, 5, 9, "R")
    c.p(1, 8, "w"); c.p(3, 8, "w"); c.p(5, 8, "w")
    c.p(1, 9, "R")
    c.p(5, 6, "y"); c.p(5, 5, "O")
    c.p(0, 6, "O")
    c.r(6, 4, 10, 6, "3")         # mane
    # torso hunched
    c.r(4, 10, 11, 16, "2")
    c.r(4, 10, 6, 11, "1")
    c.r(8, 10, 10, 13, "3")
    c.r(4, 15, 11, 18, "4")       # loincloth
    c.r(4, 18, 11, 18, "6")
    c.r(4, 19, 6, 22, "2")        # legs wide
    c.r(9, 19, 11, 22, "3")
    c.r(2, 22, 6, 22, "O")
    c.r(9, 22, 13, 22, "O")
    c.r(2, 11, 3, 14, "2")        # left arm swung back
    c.shadow(2, 13)
    return c.out()


def snapjaw_hunter():
    c = C()
    # head and torso (side-ish), bow held out to the left
    c.p(8, 1, "3"); c.p(8, 2, "2"); c.p(9, 2, "2")
    c.p(11, 2, "2")
    c.r(7, 4, 12, 7, "2")
    c.r(5, 5, 9, 7, "2")
    c.r(4, 6, 8, 8, "2")
    c.r(4, 8, 8, 8, "w")
    c.r(4, 9, 8, 9, "R")
    c.p(5, 8, "w"); c.p(7, 8, "w")
    c.p(8, 6, "y"); c.p(8, 5, "O"); c.p(4, 7, "O")
    c.r(7, 4, 12, 4, "4")         # feathered headband
    c.r(12, 1, 12, 4, "4")
    c.p(13, 0, "w"); c.p(13, 1, "w")
    c.r(9, 3, 11, 3, "3")
    c.r(4, 10, 12, 16, "2")
    c.r(4, 10, 6, 11, "1")
    c.r(8, 10, 12, 12, "3")
    c.r(11, 9, 14, 16, "5")       # quiver
    c.r(13, 8, 14, 9, "4")
    c.r(4, 16, 11, 18, "4")
    c.r(5, 19, 7, 22, "2")
    c.r(9, 19, 11, 22, "3")
    c.r(4, 22, 7, 22, "O")
    c.r(9, 22, 12, 22, "O")
    # bow at left, drawn string to hand
    c.line(2, 3, 0, 8, "N")
    c.line(0, 8, 0, 13, "N")
    c.line(0, 13, 2, 19, "N")
    c.p(0, 9, "n"); c.p(0, 10, "n"); c.p(0, 11, "n"); c.p(0, 12, "n")
    c.line(2, 3, 6, 11, "w")
    c.line(2, 19, 6, 11, "w")
    c.line(0, 11, 6, 11, "L")     # arrow
    c.p(0, 11, "w")
    c.r(5, 10, 7, 12, "S")        # draw hand
    c.shadow(1, 13)
    return c.out()


def glowfish():
    c = C()
    c.ell(7.5, 12, 7, 5, "5")      # halo
    c.ell(7.5, 12, 5.5, 3.6, "4")
    c.ell(7.5, 12, 4.5, 2.8, "1")
    c.r(1, 9, 3, 15, ".")
    c.r(1, 10, 3, 14, "2")        # tail
    c.r(0, 8, 1, 9, "2"); c.r(0, 15, 1, 16, "2")
    c.r(4, 11, 4, 13, "1")
    c.r(6, 8, 10, 9, "2")         # fin
    c.r(7, 15, 9, 16, "2")
    c.r(11, 11, 11, 11, "O")
    c.p(12, 12, "w")
    c.shadow(3, 12)
    return c.out()


def girshling():
    c = C()
    # low wide arachnid from above: 4 legs per side, big forward jaws
    legs = [(5, 8, 0, 6), (5, 10, 0, 10), (5, 12, 0, 14), (5, 14, 1, 19)]
    for x0, y0, x1, y1 in legs:
        c.line(x0, y0, x1, y1, "3")
        c.line(x0, y0, x1, y1, "3")
        c.line(15 - x0, y0, 15 - x1, y1, "3")
    for x0, y0, x1, y1 in legs:
        c.line(x0 - 1, y0 - 1, x1, y1, "3")
        c.line(15 - x0 + 1, y0 - 1, 15 - x1, y1, "3")
    c.ell(7.5, 15, 4, 4.5, "2")    # abdomen
    c.r(5, 13, 10, 14, "1")
    c.r(7, 15, 8, 19, "4")
    c.r(6, 17, 9, 17, "5")
    c.r(5, 8, 10, 12, "2")         # cephalothorax
    c.r(5, 8, 10, 9, "1")
    c.m(6, 10, "O"); c.m(5, 9, "O")
    # jaws
    c.mr(4, 4, 6, 8, "w")
    c.mr(4, 6, 5, 8, "R")
    c.mr(5, 3, 5, 4, "w")
    c.mr(6, 2, 7, 3, "w")
    c.mr(6, 4, 7, 6, "R")
    c.shadow(0, 15, 21)
    return c.out()


def dog():
    c = C()
    # bounding dog facing right
    c.r(3, 9, 11, 14, "2")         # body
    c.r(4, 9, 10, 10, "1")
    c.r(3, 13, 11, 14, "3")
    c.r(10, 5, 14, 10, "2")        # head
    c.r(13, 7, 15, 9, "1")         # snout
    c.r(14, 9, 15, 9, "R")
    c.p(15, 7, "O"); c.p(12, 7, "O")
    c.r(9, 1, 11, 5, "3")          # ear up
    c.r(10, 1, 10, 3, "2")
    c.r(10, 10, 11, 10, "4")       # collar
    c.r(1, 3, 3, 9, "2")           # tail up
    c.r(0, 2, 1, 5, "2")
    c.r(11, 13, 15, 14, "2")       # front legs forward
    c.r(14, 14, 15, 15, "3")
    c.r(10, 14, 12, 16, "3")
    c.r(0, 14, 4, 15, "3")         # back legs back
    c.r(0, 15, 2, 17, "3")
    c.r(3, 15, 5, 17, "3")
    c.shadow(0, 15, 20)
    c.shadow(0, 15, 21)
    return c.out()


def salthopper():
    c = C()

    def tl(x0, y0, x1, y1, ch):
        c.line(x0, y0, x1, y1, ch)
        c.line(x0 + 1, y0, x1 + 1, y1, ch)
    # side view facing right
    c.r(1, 13, 11, 16, "1")        # long body
    c.r(1, 15, 11, 16, "2")
    for x in (3, 5, 7, 9):
        c.r(x, 13, x, 16, "6")
    c.r(11, 11, 15, 16, "1")       # head
    c.r(13, 14, 15, 16, "2")
    c.p(14, 12, "O"); c.p(13, 12, "O")
    # long antennae sweeping back
    c.line(12, 11, 8, 3, "6"); c.line(8, 3, 3, 1, "6")
    c.line(14, 11, 12, 3, "6"); c.line(12, 3, 8, 0, "6")
    # hind leg: inverted V above the body
    tl(6, 13, 4, 6, "3")
    tl(4, 6, 1, 14, "3")
    c.line(1, 14, 0, 20, "3")
    c.r(0, 20, 3, 21, "O")
    c.r(6, 11, 7, 13, "3")
    # thin front legs
    c.line(11, 17, 10, 21, "3"); c.line(13, 17, 14, 21, "3")
    c.r(9, 21, 11, 21, "O"); c.r(13, 21, 15, 21, "O")
    c.shadow(0, 15, 22)
    return c.out()


def croc():
    c = C()
    # top-down 3/4, facing right, head with jaws wide open, tail swung left
    c.r(0, 17, 3, 19, "3")
    c.r(2, 14, 6, 18, "2")
    c.r(5, 10, 11, 16, "2")       # body
    c.r(5, 10, 11, 11, "1")
    c.r(6, 11, 6, 14, "3"); c.r(9, 11, 9, 14, "3")
    c.r(7, 12, 8, 12, "3"); c.r(7, 14, 8, 14, "3")
    # upper jaw
    c.r(8, 3, 15, 5, "2")
    c.r(7, 2, 10, 4, "1")
    c.p(9, 2, "y"); c.p(9, 3, "O")
    c.r(8, 5, 15, 5, "w")
    c.p(10, 5, "O"); c.p(12, 5, "O"); c.p(14, 5, "O")
    # lower jaw
    c.r(8, 9, 15, 9, "w")
    c.r(8, 8, 15, 8, "R")
    c.r(8, 6, 15, 7, "R")
    c.r(9, 7, 14, 7, "r")
    c.r(8, 9, 15, 10, "3")
    # legs
    c.r(3, 11, 5, 13, "3"); c.r(11, 14, 13, 17, "3")
    c.r(3, 19, 5, 21, "3"); c.r(10, 17, 13, 19, "3")
    c.r(11, 18, 13, 20, "3")
    c.shadow(0, 15, 22)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(), "four_arms": four_arms(),
    "carapace": carapace(), "mehmet": mehmet(), "farmer": farmer(), "snapjaw": snapjaw(),
    "snapjaw_hunter": snapjaw_hunter(), "glowfish": glowfish(), "girshling": girshling(),
    "dog": dog(), "salthopper": salthopper(), "croc": croc(),
}
