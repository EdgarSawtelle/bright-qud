"""Style C - side-view action: everything in profile facing right, mid-stride."""


class Cv:
    def __init__(self):
        self.g = [["."] * 16 for _ in range(24)]

    def p(self, c, x, y):
        if 0 <= x < 16 and 0 <= y < 24:
            self.g[y][x] = c
        return self

    def r(self, c, x0, y0, x1, y1):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.p(c, x, y)
        return self

    def l(self, c, x0, y0, x1, y1):
        n = max(abs(x1 - x0), abs(y1 - y0), 1)
        for i in range(n + 1):
            self.p(c, round(x0 + (x1 - x0) * i / n), round(y0 + (y1 - y0) * i / n))
        return self

    def shadow(self, x0=3, x1=13, y=22):
        for x in range(x0, x1 + 1):
            if self.g[y][x] == ".":
                self.g[y][x] = "x"
        return self

    def out(self):
        return ["".join(r) for r in self.g]


def human(body="1", shade="2", dark="3", hair="N", lean=1, stride=3, boots="3"):
    """Base humanoid in profile. Returns canvas. lean shifts upper body forward."""
    c = Cv()
    # legs (back leg, front leg)
    c.l(dark, 6, 14, 6 - stride, 20).l(dark, 7, 14, 6 - stride, 20)
    c.l(shade, 8, 14, 8 + stride, 20).l(body, 9, 14, 9 + stride, 20)
    c.r(boots, 6 - stride - 1, 21, 6 - stride + 1, 21)
    c.r(boots, 8 + stride, 21, 8 + stride + 3, 21)
    c.r(boots, 9 + stride, 20, 9 + stride, 20)
    # torso
    for y in range(7, 15):
        sh = lean if y < 10 else (lean // 2 if y < 12 else 0)
        c.r(body, 5 + sh, y, 9 + sh, y)
        c.p(dark, 5 + sh, y)
        c.p(shade, 6 + sh, y)
    # head
    c.r("s", 7 + lean, 2, 10 + lean, 6)
    c.p("S", 7 + lean, 6)
    c.p("s", 11 + lean, 5)       # nose
    c.p("O", 10 + lean, 4)       # eye
    c.r(hair, 6 + lean, 1, 10 + lean, 2)
    c.r(hair, 6 + lean, 3, 7 + lean, 5)
    c.p("S", 8 + lean, 7)
    return c


def arm_fwd(c, sx, sy, ex, ey, col="1", hand="s"):
    c.l(col, sx, sy, ex, ey)
    c.p(hand, ex, ey)


# ---------------------------------------------------------------- characters
def gunslinger():
    c = human("1", "2", "3", hair="N", lean=1, stride=3, boots="N")
    # long coat flapping behind
    c.r("2", 4, 12, 8, 17).r("3", 3, 14, 5, 18).l("3", 3, 18, 2, 19)
    c.r("1", 6, 9, 9, 13)
    # hat: brim juts forward
    c.r("N", 6, 1, 10, 1).r("N", 7, 0, 10, 0).r("n", 5, 2, 13, 2)
    c.p("n", 14, 2)
    # belt + gun on hip
    c.r("4", 6, 13, 9, 13)
    c.r("l", 5, 14, 6, 14).p("L", 5, 15)
    # aiming arm forward with pistol
    c.r("1", 8, 9, 11, 9).r("2", 8, 10, 10, 10)
    c.p("s", 12, 9)
    c.r("L", 13, 8, 15, 8).r("l", 13, 9, 14, 9).p("L", 13, 10)
    c.p("4", 12, 8)
    return c.shadow().out()


def winged():
    c = human("1", "2", "3", hair="N", lean=1, stride=3, boots="3")
    # big wing raised behind back
    c.l("4", 4, 9, 0, 1).l("4", 4, 9, 1, 0).l("4", 5, 8, 3, 0)
    for y in range(1, 9):
        c.r("5", 1 + (8 - y) // 3, y, 4, y)
    c.l("6", 0, 2, 4, 9).l("6", 2, 1, 5, 7)
    c.p("4", 1, 1).p("4", 2, 0).p("4", 3, 0).p("4", 4, 1)
    c.l("4", 1, 4, 3, 8)
    # arm
    c.r("1", 8, 9, 11, 9).p("s", 12, 9)
    c.r("4", 6, 13, 9, 13)
    return c.shadow().out()


def horned():
    c = human("1", "2", "3", hair="3", lean=1, stride=3, boots="3")
    # horns curving back
    c.r("4", 8, 0, 9, 1).r("4", 6, 0, 7, 0).r("5", 5, 1, 7, 1).r("5", 3, 0, 4, 0).r("5", 2, 1, 3, 2).p("6", 2, 3)
    c.p("4", 4, 1).p("6", 5, 2)
    c.r("4", 6, 13, 9, 13)
    # arm raised, fist forward
    c.r("1", 8, 9, 11, 10).r("s", 12, 9, 12, 10)
    c.r("5", 7, 8, 9, 8)
    return c.shadow().out()


def four_arms():
    c = human("1", "2", "3", hair="3", lean=1, stride=3, boots="3")
    # upper pair up and forward, lower pair forward/low
    c.l("4", 8, 8, 12, 5).l("4", 8, 9, 12, 6).r("s", 13, 4, 13, 5)
    c.l("5", 7, 8, 9, 3).l("5", 8, 8, 10, 3).r("s", 9, 1, 10, 2)
    c.r("4", 8, 11, 12, 11).r("5", 8, 12, 11, 12).r("s", 13, 11, 13, 12)
    c.l("5", 7, 12, 10, 15).l("5", 6, 12, 9, 15).p("s", 11, 16)
    c.r("4", 6, 13, 9, 13)
    return c.shadow().out()


def carapace():
    c = human("1", "2", "3", hair="3", lean=1, stride=3, boots="3")
    # big shell on the back
    c.r("4", 1, 6, 5, 13).r("4", 2, 5, 4, 5).r("4", 5, 7, 5, 12)
    c.r("5", 1, 9, 5, 13).r("6", 1, 12, 4, 14).p("6", 2, 14)
    c.l("6", 3, 5, 3, 13).l("6", 1, 9, 5, 9)
    c.r("4", 2, 6, 3, 7).p("w", 2, 6)
    # pauldron
    c.r("4", 7, 7, 9, 8).r("5", 7, 8, 9, 8)
    c.r("1", 8, 10, 11, 10).p("s", 12, 10)
    c.r("5", 6, 13, 9, 13)
    return c.shadow().out()


def mehmet():
    c = human("1", "2", "3", hair="w", lean=1, stride=2, boots="N")
    # white hair on head & long beard
    c.r("w", 6 + 1, 1, 11, 2).r("w", 7, 3, 8, 5)
    c.r("w", 10, 6, 12, 8).r("w", 11, 9, 11, 9)
    c.p("s", 11, 5).p("O", 11, 4)
    c.r("4", 6, 13, 9, 13)
    # hoe held forward
    c.l("N", 9, 11, 14, 5).l("n", 8, 12, 9, 11)
    c.r("4", 13, 4, 15, 4).p("L", 15, 5)
    c.r("s", 10, 10, 10, 10)
    c.r("1", 8, 9, 10, 10)
    return c.shadow().out()


def farmer():
    c = human("1", "2", "3", hair="t", lean=1, stride=2, boots="N")
    # straw hat
    c.r("t", 6, 0, 10, 1).r("t", 5, 2, 12, 2).p("y", 5, 2)
    c.r("4", 6, 13, 9, 13)
    # sickle in forward hand
    c.r("1", 8, 9, 11, 10).p("s", 12, 9)
    c.l("N", 12, 9, 13, 8)
    c.r("l", 13, 4, 14, 4).l("l", 14, 5, 15, 7).l("l", 13, 4, 13, 7).p("L", 15, 8)
    c.p("l", 14, 6)
    return c.shadow().out()


def snapjaw():
    c = human("1", "2", "3", hair="3", lean=1, stride=3, boots="N")
    # replace head with hyena snout, hunched
    for y in range(0, 8):
        for x in range(5, 16):
            if y <= 6:
                c.p(".", x, y)
    c.r("e", 7, 3, 10, 7).r("E", 7, 6, 10, 7)
    c.r("e", 11, 5, 14, 7)
    c.r("E", 11, 7, 14, 7)
    c.p("O", 14, 5)  # nose
    c.p("r", 12, 7).p("R", 13, 7)
    c.p("w", 12, 8).p("w", 14, 8)
    c.p("O", 10, 4)
    c.r("e", 7, 2, 9, 2).p("E", 8, 1).p("E", 7, 1).p("e", 6, 3)  # ear/mane
    c.r("5", 7, 8, 9, 9)
    c.r("1", 8, 10, 11, 10).p("s", 12, 10)
    c.l("N", 12, 10, 14, 6)
    c.r("l", 14, 3, 14, 5).p("L", 14, 2)
    c.r("4", 6, 13, 9, 13)
    return c.shadow().out()


def snapjaw_hunter():
    c = snapjaw_base()
    return c


def snapjaw_base():
    c = human("1", "2", "3", hair="3", lean=2, stride=3, boots="N")
    for y in range(0, 8):
        for x in range(5, 16):
            if y <= 6:
                c.p(".", x, y)
    c.r("e", 8, 3, 11, 7).r("E", 8, 6, 11, 7).r("e", 12, 5, 14, 7).r("E", 12, 7, 14, 7)
    c.p("O", 14, 5).p("O", 11, 4).p("r", 13, 7).p("w", 13, 8)
    c.r("e", 8, 2, 10, 2).p("E", 8, 1).p("E", 9, 1).p("e", 7, 3)
    c.r("4", 6, 13, 9, 13)
    # quiver
    c.l("N", 4, 7, 3, 4).l("n", 5, 8, 4, 5).p("w", 3, 3).p("w", 4, 4)
    # bow drawn: bow vertical arc at right, string back to hand
    c.r("1", 9, 9, 12, 9).p("s", 13, 9)
    c.l("N", 13, 5, 14, 9).l("N", 14, 9, 13, 13)
    c.p("N", 14, 6).p("N", 14, 12)
    c.l("w", 13, 5, 10, 9).l("w", 13, 13, 10, 9)  # string
    c.r("l", 10, 8, 14, 8).p("L", 15, 8)  # arrow
    return c.shadow().out()


snapjaw_hunter = snapjaw_base  # noqa: F811


def glowfish():
    c = Cv()
    # body ellipse swimming right
    body = [(2, 9, 12), (3, 7, 13), (4, 5, 14), (5, 4, 14), (6, 4, 14), (7, 5, 13), (8, 7, 12), (9, 9, 11)]
    for i, (y, a, b) in enumerate(body):
        y += 4
        c.r("1", a, y, b, y)
    # shading belly
    c.r("2", 5, 17, 13, 17).r("3", 8, 18, 12, 18)
    c.r("4", 5, 14, 12, 14)
    # tail
    c.l("2", 4, 15, 1, 12).l("2", 4, 16, 1, 19).r("5", 1, 12, 1, 19).r("2", 2, 13, 3, 18)
    c.r("5", 1, 13, 2, 18)
    # dorsal fin
    c.l("5", 7, 12, 9, 9).l("5", 10, 12, 10, 10).r("5", 8, 11, 10, 11)
    # eye, mouth
    c.p("w", 12, 15).p("O", 12, 15).p("O", 14, 17)
    # glow dots
    for x, y in [(6, 16), (8, 17), (10, 16), (4, 15)]:
        c.p("4", x, y)
    c.p("4", 11, 7).p("4", 13, 9).p("4", 3, 8)
    return c.shadow(2, 14, 22).out()


def girshling():
    c = Cv()
    # abdomen (rear) and cephalothorax, legs splayed
    c.r("1", 3, 11, 7, 15).r("2", 3, 14, 7, 16).r("3", 3, 16, 6, 16)
    c.r("1", 8, 12, 12, 15).r("2", 9, 15, 12, 15)
    c.r("1", 12, 11, 14, 14).p("O", 13, 12).p("O", 14, 13)
    c.r("4", 5, 10, 6, 10).r("4", 4, 12, 5, 12)
    # jaws
    c.p("5", 15, 14).p("5", 14, 15).p("w", 15, 15)
    # legs: splayed 4 visible
    for x0, x1 in [(4, 1), (6, 3), (9, 8), (11, 12)]:
        c.l("5", x0, 16, x1, 18).l("5", x1, 18, x1 - 1 if x1 < 6 else x1 + 1, 21)
    c.l("5", 8, 16, 9, 18).l("5", 9, 18, 8, 21)
    c.l("6", 11, 15, 14, 18).l("6", 14, 18, 15, 21)
    c.l("6", 5, 16, 6, 18).l("6", 6, 18, 5, 21)
    # front pincers
    c.l("5", 13, 14, 15, 12)
    return c.shadow(1, 15, 22).out()


def dog():
    c = Cv()
    # trotting dog
    c.r("1", 4, 9, 11, 13).r("2", 4, 12, 11, 13).r("3", 5, 13, 10, 13)
    c.r("1", 11, 6, 14, 10).r("2", 11, 9, 14, 10)  # head
    c.r("1", 14, 8, 15, 10).p("O", 15, 8)  # snout/nose
    c.p("O", 13, 7).p("3", 11, 5).p("3", 12, 5).p("3", 11, 6)  # eye, ear
    c.p("r", 14, 11)
    c.r("1", 11, 8, 12, 11)  # neck
    # tail up/back
    c.l("1", 4, 9, 1, 6).p("2", 1, 5)
    # collar
    c.r("4", 11, 10, 12, 10)
    # legs trotting: diagonal pairs
    c.r("1", 11, 13, 12, 16).l("2", 12, 16, 14, 19).r("w", 14, 20, 15, 20).p("w", 14, 19)
    c.r("2", 9, 13, 10, 16).l("3", 9, 16, 8, 20).r("w", 7, 20, 8, 20)
    c.r("1", 5, 13, 6, 16).l("2", 5, 16, 3, 19).r("w", 2, 20, 3, 20)
    c.r("3", 3, 13, 4, 15).l("3", 3, 15, 4, 20).r("w", 4, 20, 5, 20)
    return c.shadow(1, 15, 21).out()


def salthopper():
    c = Cv()
    # crouched grasshopper, big back legs
    c.r("1", 5, 10, 11, 14).r("2", 5, 13, 11, 14).r("3", 6, 14, 10, 14)
    c.r("1", 4, 11, 5, 13)
    c.r("1", 11, 8, 14, 13).r("2", 11, 12, 14, 13)  # head
    c.p("O", 13, 10).p("O", 14, 12).p("5", 14, 13).p("w", 15, 13)
    c.l("4", 13, 8, 15, 4).l("4", 12, 8, 13, 3)  # antennae
    # wing on back
    c.l("4", 5, 10, 1, 7).l("5", 6, 11, 1, 9).r("4", 2, 8, 6, 10)
    # big hind leg: femur up, tibia down
    c.l("2", 6, 13, 3, 9).l("2", 7, 13, 4, 9).l("1", 4, 9, 1, 19).l("3", 3, 10, 0, 19)
    c.l("5", 1, 20, 3, 21)
    # front legs
    c.l("2", 10, 14, 12, 21).l("3", 9, 14, 8, 21)
    c.r("5", 11, 21, 13, 21).r("5", 7, 21, 9, 21)
    return c.shadow(0, 14, 22).out()


def croc():
    c = Cv()
    # low body, open jaws to the right
    c.r("1", 4, 12, 10, 16).r("2", 4, 15, 10, 16).r("3", 5, 16, 9, 16)
    c.r("4", 5, 11, 9, 11)  # back ridges
    for x in (5, 7, 9):
        c.p("5", x, 10)
    # tail sweep
    c.l("1", 4, 14, 0, 17).l("2", 4, 15, 0, 18).p("3", 0, 18)
    c.l("5", 3, 13, 1, 15)
    # head: upper jaw & lower jaw open
    c.r("1", 10, 11, 15, 12).r("2", 10, 13, 12, 14)
    c.p("O", 11, 11)
    c.r("3", 12, 13, 15, 13)  # mouth interior
    c.r("r", 12, 14, 15, 14).r("2", 10, 15, 15, 16)
    c.p("w", 13, 13).p("w", 15, 13).p("w", 14, 15).p("w", 12, 15)
    # legs
    c.r("2", 5, 17, 6, 19).r("5", 4, 20, 7, 20)
    c.r("1", 9, 17, 10, 19).r("5", 9, 20, 12, 20)
    c.r("2", 3, 17, 4, 18).r("2", 11, 17, 11, 18)
    return c.shadow(0, 15, 21).out()


CHARACTERS = {
    "gunslinger": gunslinger(),
    "winged": winged(),
    "horned": horned(),
    "four_arms": four_arms(),
    "carapace": carapace(),
    "mehmet": mehmet(),
    "farmer": farmer(),
    "snapjaw": snapjaw(),
    "snapjaw_hunter": snapjaw_base(),
    "glowfish": glowfish(),
    "girshling": girshling(),
    "dog": dog(),
    "salthopper": salthopper(),
    "croc": croc(),
}
