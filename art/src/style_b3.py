"""Style B3 - weird retro sci-fi: lanky robed humanoids, goggles/masks, glowing accents, alien beasts."""


class C:
    def __init__(s):
        s.g = [["."] * 16 for _ in range(24)]

    def p(s, x, y, ch):
        if 0 <= x < 16 and 0 <= y < 24:
            s.g[y][x] = ch

    def m(s, x, y, ch):
        s.p(x, y, ch)
        s.p(15 - x, y, ch)

    def r(s, x0, y0, x1, y1, ch):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                s.p(x, y, ch)

    def mr(s, x0, y0, x1, y1, ch):
        s.r(x0, y0, x1, y1, ch)
        s.r(15 - x1, y0, 15 - x0, y1, ch)

    def line(s, x0, y0, x1, y1, ch, mirror=False):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            x = round(x0 + (x1 - x0) * i / n)
            y = round(y0 + (y1 - y0) * i / n)
            (s.m if mirror else s.p)(x, y, ch)

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


def robed(c, top=2, body="2", lite="1", dark="3", goggles="c", wrap="4", arms=True):
    """lanky robed figure: narrow head with goggles + face wrap, long flaring robe."""
    c.r(6, top, 9, top + 4, "s")
    c.r(6, top + 4, 9, top + 4, wrap)           # face wrap / mask
    c.r(6, top + 5, 9, top + 5, wrap)
    c.r(6, top + 2, 9, top + 2, goggles)        # goggle band
    c.m(6, top + 2, goggles)
    c.m(7, top + 2, "O") if False else None
    c.p(7, top + 2, "w" if goggles == "c" else goggles)
    c.p(8, top + 2, "w" if goggles == "c" else goggles)
    # robe
    c.r(5, top + 6, 10, 21, body)
    c.r(4, 16, 11, 21, body)
    c.r(3, 19, 12, 21, body)
    c.r(5, top + 6, 6, 15, lite)
    c.r(10, 14, 11, 21, dark)
    c.r(3, 21, 12, 21, dark)
    # sash accent
    c.line(5, top + 7, 10, 15, wrap)
    c.line(5, top + 8, 10, 16, wrap)
    if arms:
        c.r(4, top + 7, 4, 14, body)
        c.r(11, top + 7, 11, 14, dark)
        c.m(4, 15, "s")
    c.r(5, 22, 6, 22, "O")
    c.r(9, 22, 10, 22, "O")
    c.shadow(3, 12)


def gunslinger():
    c = C()
    robed(c, top=3, wrap="4")
    c.r(3, 1, 12, 1, "2")      # wide brim
    c.r(5, 0, 10, 0, "2")
    c.r(5, 2, 10, 2, "3")
    c.r(1, 1, 2, 1, "3"); c.r(13, 1, 14, 1, "3")
    # arms out with big chrome pistols
    c.r(2, 10, 4, 11, "2"); c.r(11, 10, 13, 11, "2")
    c.r(0, 9, 2, 9, "l"); c.r(13, 9, 15, 9, "l")
    c.r(0, 10, 1, 10, "L"); c.r(14, 10, 15, 10, "L")
    c.p(0, 8, "4"); c.p(15, 8, "4")
    c.p(2, 10, "s"); c.p(13, 10, "s")
    return c.out()


def winged():
    c = C()
    # big feathered wings behind
    for y in range(4, 17):
        w = 5 if y < 12 else 5 - (y - 11)
        c.r(max(0, 5 - w), y, 4, y, "4")
        c.r(11, y, min(15, 10 + w), y, "4")
    c.r(0, 4, 2, 9, "5"); c.r(13, 4, 15, 9, "5")
    c.r(0, 3, 1, 3, "4"); c.r(14, 3, 15, 3, "4")
    c.r(0, 10, 1, 13, "6"); c.r(14, 10, 15, 13, "6")
    robed(c, top=2, wrap="4", goggles="c")
    return c.out()


def horned():
    c = C()
    robed(c, top=4, goggles="O", wrap="6")
    # big ram-like horns curling out and up
    c.mr(4, 5, 5, 6, "w")
    c.mr(2, 4, 3, 5, "w")
    c.mr(1, 2, 2, 4, "w")
    c.mr(2, 1, 3, 2, "w")
    c.mr(4, 0, 4, 1, "W") if False else None
    c.m(1, 4, "L"); c.m(2, 5, "L"); c.m(3, 6, "L")
    c.p(7, 6, "r"); c.p(8, 6, "r")
    return c.out()


def four_arms():
    c = C()
    robed(c, top=2)
    # upper arms raised, lower arms out
    c.r(2, 8, 4, 9, "2"); c.r(11, 8, 13, 9, "2")
    c.r(1, 5, 2, 8, "2"); c.r(13, 5, 14, 8, "2")
    c.m(1, 4, "s"); c.m(2, 4, "s")
    c.r(1, 13, 4, 14, "3"); c.r(11, 13, 14, 14, "3")
    c.m(0, 14, "s"); c.m(1, 15, "s") if False else None
    c.m(0, 13, "s")
    # accent bangles
    c.m(1, 7, "4"); c.m(2, 13, "4")
    return c.out()


def carapace():
    c = C()
    robed(c, top=3, body="3", lite="2", dark="3", wrap="4", goggles="c")
    # hard shell plates
    c.mr(1, 8, 4, 12, "4")
    c.mr(2, 7, 4, 7, "4")
    c.mr(0, 9, 1, 11, "5")
    c.mr(1, 12, 3, 13, "5")
    c.r(4, 8, 4, 9, "1"); c.r(11, 8, 11, 9, "6")
    c.r(5, 8, 10, 9, "4")   # collar plate
    c.r(5, 8, 10, 8, "1")
    c.r(6, 14, 9, 17, "5")  # belly plates
    c.r(6, 14, 9, 14, "4"); c.r(6, 16, 9, 16, "4")
    return c.out()


def mehmet():
    c = C()
    robed(c, top=3, body="2", wrap="4", goggles="s", arms=True)
    # clean face again: no goggles, white beard + turban
    c.r(6, 5, 9, 5, "s"); c.p(7, 5, "O"); c.p(8, 5, "O")
    c.r(6, 6, 9, 8, "w"); c.r(7, 9, 8, 9, "w")
    c.r(6, 2, 9, 3, "4"); c.r(5, 3, 10, 3, "4"); c.r(7, 1, 8, 1, "5")
    c.r(6, 4, 9, 4, "s")
    # hoe in right hand
    c.line(13, 6, 13, 21, "n")
    c.r(11, 5, 14, 5, "l"); c.p(11, 6, "L")
    c.p(12, 14, "s")
    return c.out()


def farmer():
    c = C()
    robed(c, top=3, body="2", wrap="5", goggles="c")
    # straw hat
    c.r(4, 3, 11, 3, "t"); c.r(5, 2, 10, 2, "t"); c.r(6, 1, 9, 1, "t")
    c.r(5, 3, 10, 3, "y")
    # sickle
    c.line(13, 17, 13, 10, "n")
    c.p(12, 9, "l"); c.p(11, 8, "l"); c.p(12, 8, "L"); c.p(13, 8, "l")
    c.p(13, 9, "L")
    c.p(12, 15, "s")
    c.m(5, 17, "4") if False else None
    return c.out()


SNAP = [
    ".....3....3.....",
    ".....23...23....",
    ".....22..222....",
    "...eeE2222223...",
    ".OeeeEy22221133.",
    ".wOwOwEE221.133.",
    "..eeEe...21.33..",
    "....e.22211.3...",
    "....2212223.3...",
    "...s2112223.3...",
    "...s211222......",
    "....21122.s.....",
    "....22222.s.....",
    "....5555555.....",
    "....4545455.....",
    ".....5.5.5......",
    ".....22.22......",
    ".....22..22.....",
    "....22....22....",
    "....2......2....",
    "....22....22....",
    "....22....22....",
    "...OOO...OOO....",
    "................",
]


def _snap(hunter=False):
    c = C()
    for y, row in enumerate(SNAP):
        for x, ch in enumerate(row):
            if ch != ".":
                c.p(x, y, ch)
    if not hunter:
        c.line(13, 7, 13, 20, "n")
        c.r(12, 4, 14, 7, "N")
        c.p(13, 3, "l"); c.p(12, 5, "l"); c.p(14, 6, "l")
        c.p(12, 12, "s"); c.p(11, 12, "s")
        c.r(5, 12, 12, 12, "2") if False else None
    else:
        for y, x in [(5, 14), (6, 14), (7, 15), (8, 15), (9, 15), (10, 15), (11, 15), (12, 15), (13, 14), (14, 14), (15, 13)]:
            c.p(x, y, "n")
        c.line(13, 5, 13, 15, "w")
        c.p(12, 11, "s")
        c.p(11, 12, "s"); c.p(12, 12, "s")
        c.p(5, 2, "g"); c.p(6, 2, "4"); c.p(9, 2, "4"); c.p(10, 2, "4")
        c.p(9, 0, "g"); c.p(10, 0, "g"); c.p(10, 1, "g"); c.p(11, 0, "h")
        c.r(9, 9, 10, 13, "N"); c.p(9, 8, "w"); c.p(10, 8, "w")
    c.shadow(2, 12)
    return c.out()


def snapjaw():
    return _snap(False)


def snapjaw_hunter():
    return _snap(True)


def glowfish():
    c = C()
    # sparkle halo
    for y in range(24):
        for x in range(16):
            d = ((x - 7.5) / 8.0) ** 2 + ((y - 12) / 6.5) ** 2
            if 0.75 <= d <= 1.0 and (x + y) % 2 == 0:
                c.p(x, y, "4")
            elif 0.5 <= d < 0.75:
                c.p(x, y, "5")
    c.ell(7.5, 12, 8, 7, "5") if False else None
    # body facing left
    c.ell(6.5, 12, 5.5, 3.5, "1")
    c.r(3, 13, 10, 14, "2")
    c.ell(6, 14, 3, 1, "w")
    # tail
    c.r(11, 10, 13, 14, "2"); c.r(13, 8, 15, 16, "2")
    c.p(15, 8, "1"); c.p(15, 16, "1"); c.r(11, 11, 12, 13, "1")
    # dorsal / pelvic fins
    c.r(5, 8, 9, 9, "2"); c.r(6, 7, 8, 7, "3")
    c.r(5, 16, 8, 17, "2")
    # eye and gill
    c.p(2, 11, "w"); c.p(2, 12, "O"); c.p(4, 12, "3"); c.p(4, 13, "3")
    for x in (6, 8, 10):
        c.p(x, 12, "5")
    # lure orb
    c.line(3, 9, 2, 6, "3")
    c.r(1, 3, 3, 5, "4"); c.p(2, 4, "w"); c.p(0, 4, "4"); c.p(4, 4, "4"); c.p(2, 2, "4"); c.p(2, 6, "4") if False else None
    c.shadow(1, 14)
    return c.out()


def girshling():
    c = C()
    # splayed spindly legs
    legs = [(5, 8, 0, 4), (5, 10, 0, 9), (5, 13, 0, 15), (5, 15, 1, 20),
            ]
    for (x0, y0, x1, y1) in legs:
        c.line(x0, y0, x1, y1, "3", mirror=True)
    for (x0, y0, x1, y1) in legs:
        c.line(x0, y0 - 1 if False else y0, x1 + 1, y1, "3", mirror=True) if False else None
    # body: small head w/ huge jaws up front, bulbous abdomen behind
    c.ell(7.5, 16, 3.5, 4.5, "2")
    c.ell(7.5, 16, 2, 3, "1")
    c.r(6, 15, 7, 16, "1")
    c.ell(7.5, 10, 3, 2.5, "3")
    c.r(6, 9, 9, 10, "2")
    # eyes (glowing)
    c.m(6, 9, "4") if False else None
    c.p(6, 9, "y"); c.p(9, 9, "y")
    # chelicerae big jaws
    c.line(6, 7, 4, 4, "w") ; c.line(9, 7, 11, 4, "w")
    c.line(6, 8, 5, 5, "6") if False else None
    c.m(5, 4, "r"); c.m(6, 7, "w")
    c.m(4, 3, "w")
    c.p(7, 7, "R"); c.p(8, 7, "R")
    # abdomen stripe accent
    c.r(6, 14, 9, 14, "4"); c.r(6, 17, 9, 17, "4"); c.r(7, 19, 8, 19, "5")
    c.shadow(1, 14)
    return c.out()


def dog():
    c = C()
    # 3/4 top-down: body horizontal-ish, head left-up, tail up right
    c.r(5, 9, 12, 15, "2")
    c.r(5, 9, 12, 10, "1")
    c.r(10, 12, 12, 15, "3")
    c.r(2, 4, 7, 9, "2")           # head
    c.r(2, 4, 5, 5, "1")
    c.r(0, 6, 3, 8, "1")           # muzzle
    c.p(0, 6, "O"); c.p(0, 7, "O")  # nose
    c.p(4, 5, "O")
    c.p(2, 3, "3"); c.p(3, 2, "3"); c.p(2, 2, "3")   # ears
    c.p(6, 3, "3"); c.p(6, 2, "3"); c.p(7, 3, "3")
    c.r(3, 9, 5, 10, "4")           # collar accent
    # tail
    c.line(12, 10, 14, 5, "2"); c.line(13, 10, 15, 6, "2")
    # legs
    c.r(5, 16, 6, 20, "2"); c.r(11, 16, 12, 20, "2")
    c.r(3, 15, 4, 19, "3"); c.r(9, 16, 9, 19, "3")
    c.r(4, 20, 6, 21, "3") if False else None
    c.r(2, 20, 4, 20, "1"); c.r(5, 21, 7, 21, "1"); c.r(10, 21, 13, 21, "1")
    c.shadow(1, 14)
    return c.out()


def salthopper():
    c = C()
    c.line(5, 4, 2, 0, "w"); c.line(10, 4, 13, 0, "w")
    c.r(5, 4, 10, 8, "2"); c.r(5, 4, 10, 4, "1")
    c.r(4, 5, 5, 7, "4"); c.r(10, 5, 11, 7, "4")
    c.p(4, 5, "w"); c.p(11, 5, "w")
    c.r(6, 8, 9, 9, "3"); c.p(6, 9, "w"); c.p(9, 9, "w")
    # armored segments with dark seams
    for i, y in enumerate((10, 12, 14, 16, 18)):
        wd = 3 if i < 4 else 2
        c.r(8 - wd, y, 7 + wd, y, "1" if i % 2 == 0 else "2")
        c.r(8 - wd, y + 1, 7 + wd, y + 1, "3")
    c.r(7, 10, 8, 19, "6")
    # thick bent hind legs: 2px inverted V each side
    c.line(4, 13, 2, 8, "5"); c.line(5, 13, 3, 8, "5")
    c.line(2, 8, 1, 20, "5"); c.line(3, 8, 2, 20, "5")
    c.p(2, 7, "6"); c.p(3, 7, "6"); c.r(0, 20, 2, 21, "6")
    c.line(11, 13, 13, 8, "5"); c.line(10, 13, 12, 8, "5")
    c.line(13, 8, 14, 20, "5"); c.line(12, 8, 13, 20, "5")
    c.p(12, 7, "6"); c.p(13, 7, "6"); c.r(13, 20, 15, 21, "6")
    c.p(4, 14, "3"); c.p(3, 15, "3"); c.p(11, 14, "3"); c.p(12, 15, "3")
    c.shadow(0, 15)
    return c.out()


def croc():
    c = C()
    # top-down croc, snout up, tail down; scutes accent
    c.r(5, 0, 10, 6, "2")           # snout
    c.r(6, 0, 9, 0, "1")
    c.p(6, 1, "O"); c.p(9, 1, "O")  # nostrils
    c.r(4, 6, 11, 11, "2")          # skull
    c.p(5, 7, "y"); c.p(10, 7, "y"); c.p(5, 8, "O"); c.p(10, 8, "O")
    c.p(4, 6, "w"); c.p(4, 3, "w"); c.p(5, 4, "w") ; c.p(10, 4, "w"); c.p(11, 3, "w")
    c.r(3, 12, 12, 17, "2")         # body
    c.r(6, 12, 9, 22, "3")          # tail core
    c.r(7, 18, 8, 23, "3")
    c.r(5, 18, 10, 19, "2")
    c.r(6, 20, 9, 21, "2")
    for y in range(7, 21, 2):
        c.p(7, y, "4"); c.p(8, y, "4")        # scutes (accent)
    c.r(7, 12, 8, 13, "5") if False else None
    # legs splayed
    c.r(1, 11, 3, 13, "3"); c.r(12, 11, 14, 13, "3")
    c.r(0, 13, 2, 14, "1"); c.r(13, 13, 15, 14, "1")
    c.r(1, 16, 3, 18, "3"); c.r(12, 16, 14, 18, "3")
    c.r(0, 18, 2, 19, "1"); c.r(13, 18, 15, 19, "1")
    c.shadow(0, 15, 23)
    return c.out()


CHARACTERS = {
    "gunslinger": gunslinger(), "winged": winged(), "horned": horned(),
    "four_arms": four_arms(), "carapace": carapace(), "mehmet": mehmet(),
    "farmer": farmer(), "snapjaw": snapjaw(), "snapjaw_hunter": snapjaw_hunter(),
    "glowfish": glowfish(), "girshling": girshling(), "dog": dog(),
    "salthopper": salthopper(), "croc": croc(),
}
