"""Paper doll gear layers: head/*, face/*, back/*. Role digits = the item's colours."""
from b3kit import C

LAYERS = {}


def _poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            inside = False
            for i in range(n):
                x1, y1 = pts[i]
                x2, y2 = pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    inside = not inside
            if inside:
                c.p(x, y, ch)


def reg(name):
    def deco(fn):
        c = C()
        fn(c)
        LAYERS[name] = c.out()
        return fn
    return deco


# ------------------------------------------------------------------ head
@reg("head/cap")
def _(c):
    c.r(6, 0, 9, 0, "2")
    c.r(5, 1, 10, 1, "2")
    c.r(5, 2, 10, 2, "2")
    c.r(5, 3, 10, 3, "3")           # band hugging the head
    c.r(11, 3, 13, 3, "3")          # short peak to the right
    c.r(11, 4, 12, 4, "3")
    c.r(6, 0, 7, 0, "1"); c.r(5, 1, 7, 1, "1"); c.p(5, 2, "1"); c.p(6, 2, "1")
    c.p(9, 1, "3"); c.p(10, 1, "3"); c.p(10, 2, "3"); c.p(9, 2, "3")
    c.p(8, 0, "4")                   # button
    c.r(5, 3, 6, 3, "4"); c.r(7, 3, 10, 3, "5")
    c.p(12, 3, "6")


@reg("head/hat")
def _(c):
    c.r(6, 0, 9, 0, "2")
    c.r(5, 1, 10, 1, "2")
    c.r(5, 2, 10, 2, "4")
    c.r(6, 0, 7, 0, "1")
    c.p(5, 1, "1")
    c.p(9, 1, "3"); c.p(10, 1, "3")
    c.r(1, 3, 14, 3, "2")           # wide brim
    c.r(1, 3, 4, 3, "1")
    c.r(11, 3, 14, 3, "3")
    c.p(0, 4, "3"); c.p(15, 4, "3")  # drooping tips
    c.p(1, 4, "2"); c.p(14, 4, "3")
    c.p(8, 2, "5"); c.p(9, 2, "5")


@reg("head/helmet")
def _(c):
    c.r(6, 1, 9, 1, "1")
    c.r(5, 2, 10, 2, "2")
    c.r(5, 3, 10, 3, "2")
    c.r(4, 3, 4, 7, "2")            # cheek guards down both sides
    c.r(11, 3, 11, 7, "3")
    c.r(5, 4, 5, 6, "2")
    c.r(10, 4, 10, 6, "3")
    c.p(4, 7, "3")
    c.p(11, 8, "3")
    c.r(7, 3, 8, 6, "1")            # nasal guard
    c.p(7, 3, "1"); c.p(8, 3, "2")
    c.r(8, 4, 8, 6, "2")
    c.p(6, 1, "1"); c.p(6, 2, "1")
    c.p(9, 2, "3"); c.p(10, 2, "3")
    c.p(7, 0, "4"); c.p(8, 0, "5")  # little crest knob
    c.p(7, 2, "4"); c.p(8, 2, "4")  # brow stud
    c.p(7, 1, "2"); c.p(8, 1, "2")
    c.p(9, 1, "3")


@reg("head/coif")
def _(c):
    # mail hood: dome, wraps sides of face and drapes onto shoulders
    c.r(6, 1, 9, 1, "2")
    c.r(5, 2, 10, 2, "2")
    c.r(4, 3, 11, 3, "2")
    c.r(4, 4, 5, 7, "2")
    c.r(10, 4, 11, 7, "2")
    c.r(3, 8, 12, 8, "2")           # mail collar on shoulders
    c.r(3, 9, 4, 9, "2")
    c.r(11, 9, 12, 9, "3")
    c.r(6, 8, 9, 8, "2")
    c.r(7, 4, 8, 4, ".")
    # mail texture: checker of light/dark
    for y in range(1, 10):
        for x in range(3, 13):
            ch = c.g[y][x]
            if ch in "2":
                if (x + y) % 2 == 0:
                    c.g[y][x] = "1"
    for y in range(3, 10):
        for x in (10, 11, 12):
            if c.g[y][x] in "12":
                c.g[y][x] = "3" if (x + y) % 2 == 0 else "2"
    c.r(6, 4, 9, 7, ".")
    c.r(6, 3, 9, 3, "3") if False else None
    # rim line of the face opening
    for y in range(4, 8):
        c.p(5, y, "3")
    c.p(6, 3, "3"); c.p(7, 3, "3"); c.p(8, 3, "3"); c.p(9, 3, "3")
    c.p(10, 4, "3"); c.p(10, 5, "3"); c.p(10, 6, "3"); c.p(10, 7, "3")
    c.p(6, 8, "3"); c.p(9, 8, "3")
    c.p(7, 8, "."); c.p(8, 8, ".")  # neck shows


@reg("head/crown")
def _(c):
    # thin circlet with three tall points and a gem
    for y in (0, 1):
        c.p(5, y, "1"); c.p(10, y, "2")
    c.p(7, 0, "1"); c.p(8, 0, "4")
    c.p(7, 1, "1"); c.p(8, 1, "2")
    c.p(6, 1, "2"); c.p(9, 1, "2")
    c.p(6, 2, "1"); c.p(9, 2, "2"); c.p(7, 2, "1"); c.p(8, 2, "2")
    c.r(4, 2, 4, 2, "1") if False else None
    c.r(5, 2, 5, 2, "1"); c.p(10, 2, "3")
    c.r(5, 3, 10, 3, "2")
    c.r(5, 3, 6, 3, "1"); c.r(9, 3, 10, 3, "3")
    c.p(7, 3, "4"); c.p(8, 3, "5")   # gem


@reg("head/techhelm")
def _(c):
    c.r(7, 0, 8, 0, "1")
    c.r(6, 1, 9, 1, "1")
    c.r(5, 2, 10, 2, "2")
    c.r(4, 3, 11, 3, "4")            # visor-rim band in the detail colour
    c.r(4, 4, 4, 6, "3"); c.r(11, 4, 11, 6, "3")   # ear pods
    c.r(5, 4, 5, 4, "3"); c.p(10, 4, "3")
    c.p(6, 1, "w"); c.p(6, 2, "1"); c.p(5, 2, "1")
    c.r(9, 1, 10, 2, "3"); c.p(10, 2, "3")
    c.p(7, 2, "c"); c.p(8, 2, "c")   # lamp
    c.p(7, 0, "c") if False else None
    c.line(11, 2, 12, 0, "3")        # antenna
    c.p(12, 0, "c"); c.p(12, 1, "3"); c.p(13, 0, "c")
    c.p(4, 5, "5"); c.p(11, 5, "5")


@reg("head/horns")
def _(c):
    c.r(5, 3, 10, 3, "3")            # brow band
    c.p(7, 3, "4"); c.p(8, 3, "4")
    c.p(5, 3, "2") if False else None
    c.mr(3, 3, 4, 3, "2")
    c.mr(2, 2, 3, 2, "2")
    c.mr(1, 1, 2, 1, "2")
    c.mr(1, 0, 1, 0, "1")
    c.mr(0, 0, 0, 0, "1")
    c.mr(2, 3, 2, 3, "3")
    c.mr(3, 2, 3, 2, "1")
    c.mr(4, 2, 4, 2, ".") if False else None
    c.mr(2, 1, 2, 1, "1")
    c.mr(3, 3, 3, 3, "1")
    c.mr(4, 3, 4, 3, "3")
    c.mr(2, 2, 2, 2, "3")
    c.mr(1, 1, 1, 1, "3")
    c.mr(1, 0, 1, 0, "1")


@reg("head/veil")
def _(c):
    # headcloth with a hanging sheer veil that flares over the shoulders + lower-face veil
    c.r(7, 0, 8, 0, "4")
    c.r(6, 1, 9, 1, "4")
    c.r(5, 2, 10, 2, "4")
    c.r(5, 3, 10, 3, "5")
    c.r(4, 3, 4, 5, "5"); c.r(11, 3, 11, 5, "6")
    c.r(3, 6, 4, 9, "5"); c.r(11, 6, 12, 9, "6")
    c.r(2, 10, 3, 12, "5"); c.r(12, 10, 13, 12, "6")
    c.p(2, 12, "4"); c.p(13, 12, "5")
    c.p(6, 1, "w"); c.p(7, 3, "y"); c.p(8, 3, "y")
    c.p(7, 0, "1") if False else None
    c.r(5, 6, 10, 6, "5"); c.r(6, 7, 9, 7, "4"); c.p(7, 8, "6"); c.p(8, 8, "6")
    c.p(10, 6, "6"); c.p(5, 6, "4"); c.p(9, 7, "6")


# ------------------------------------------------------------------ face
@reg("face/goggles")
def _(c):
    c.r(5, 3, 6, 3, "3"); c.r(9, 3, 10, 3, "3")
    c.r(5, 6, 6, 6, "3"); c.r(9, 6, 10, 6, "3")
    c.r(5, 4, 6, 5, "c"); c.r(9, 4, 10, 5, "c")
    c.p(5, 4, "w"); c.p(9, 4, "w")
    c.p(6, 5, "c"); c.p(10, 5, "c")
    c.r(7, 4, 8, 4, "2")             # bridge
    c.p(4, 4, "3"); c.p(4, 5, "3"); c.p(11, 4, "3"); c.p(11, 5, "3")  # strap
    c.p(4, 3, "2") if False else None
    c.p(7, 5, "3"); c.p(8, 5, "3") if False else None


@reg("face/mask")
def _(c):
    c.r(5, 3, 10, 3, "2")            # full face mask with eye slits
    c.r(5, 4, 10, 4, "2")
    c.r(5, 5, 10, 5, "2")
    c.r(5, 6, 10, 7, "2") if False else None
    c.r(5, 6, 10, 6, "2")
    c.r(6, 7, 9, 7, "2")
    c.r(5, 3, 10, 3, "1")
    c.p(10, 4, "3"); c.p(10, 5, "3"); c.p(10, 6, "3"); c.r(8, 7, 9, 7, "3")
    c.p(5, 4, "1"); c.p(5, 5, "1")
    c.p(6, 5, "O"); c.p(9, 5, "O")   # eyes show through slits
    c.p(6, 4, "3"); c.p(9, 4, "3")  # brow ridge over the eyes
    c.p(7, 5, "3"); c.p(8, 5, "3")  # nose
    c.r(7, 6, 8, 6, "4"); c.p(7, 7, "5"); c.p(8, 7, "6")   # mouth grille
    c.p(5, 6, "4"); c.p(10, 6, "5")  # cheek vents
    c.p(4, 5, "3"); c.p(11, 5, "3")  # straps


# ------------------------------------------------------------------ back (behind body)
@reg("back/cloak")
def _(c):
    c.r(4, 8, 11, 8, "2")
    c.r(3, 9, 12, 15, "2")
    c.r(2, 16, 13, 18, "2")
    c.r(1, 19, 14, 22, "2")
    c.r(1, 19, 3, 22, "1"); c.r(2, 16, 3, 18, "1"); c.r(3, 9, 3, 15, "1")
    c.r(11, 9, 12, 15, "3"); c.r(12, 16, 13, 18, "3"); c.r(12, 19, 14, 22, "3")
    c.r(1, 22, 14, 22, "4")          # trim hem
    c.p(1, 22, "5"); c.p(14, 22, "6")
    c.r(4, 8, 5, 8, "4"); c.r(10, 8, 11, 8, "5")   # collar edge
    c.p(3, 9, "4"); c.p(12, 9, "5")  # clasp-ish
    c.p(0, 21, "3") if False else None


@reg("back/pack")
def _(c):
    c.r(2, 9, 13, 17, "2")           # pack body, sticks out both sides
    c.r(2, 9, 3, 17, "1")
    c.r(12, 9, 13, 17, "3")
    c.r(1, 13, 2, 17, "5")           # side pouches
    c.r(13, 13, 14, 17, "6")
    c.r(1, 13, 1, 17, "4")
    c.r(2, 6, 13, 8, "4")            # bedroll across the top
    c.r(2, 6, 13, 6, "4")
    c.r(2, 7, 13, 7, "5")
    c.r(2, 8, 13, 8, "6")
    c.p(2, 6, "w") if False else None
    c.p(1, 7, "5"); c.p(14, 7, "6")
    c.r(3, 6, 3, 8, "6"); c.r(12, 6, 12, 8, "6")   # straps round the roll
    c.p(1, 15, "y"); c.p(14, 15, "y")
    c.r(3, 18, 4, 18, "3"); c.r(11, 18, 12, 18, "3")
    c.p(3, 12, "3"); c.p(12, 12, "3")


@reg("back/wings")
def _(c):
    # rigid mechanical wing blades, mirrored
    for sx in (0, 1):
        def X(x, sx=sx):
            return 15 - x if sx else x
        _poly(c, [(X(4), 8), (X(0), 0), (X(0), 14), (X(2), 17), (X(4), 14)], "2")
        # blade gaps
        for (x1, y1) in ((0, 5), (0, 9), (1, 13)):
            c.line(X(4), 10, X(x1), y1 + 1, "3")
        c.line(X(4), 8, X(0), 0, "1")      # leading edge
        c.line(X(3), 8, X(0), 2, "1")
        c.line(X(4), 8, X(4), 14, "3")
        for (x, y) in ((0, 1), (0, 6), (0, 10), (1, 14)):
            c.p(X(x), y, "4")              # glow tips
        c.p(X(3), 9, "5"); c.p(X(3), 11, "5")
        c.p(X(2), 16, "6")
    c.r(3, 8, 4, 9, "3"); c.r(11, 8, 12, 9, "3")   # root joints
    c.p(3, 8, "4"); c.p(12, 8, "4")


@reg("back/banner")
def _(c):
    for y in range(0, 10):
        c.p(11, y, "3")
    for y in range(10, 21):
        c.p(12, y, "3")
    c.p(11, 0, "1"); c.p(11, 1, "1")
    c.r(12, 0, 15, 5, "2")
    c.r(12, 0, 15, 0, "1")
    c.r(12, 5, 15, 5, "3")
    c.r(13, 6, 13, 7, "2"); c.p(15, 6, "2"); c.p(14, 6, "3") if False else None
    c.p(12, 6, "3"); c.p(14, 6, ".")
    c.r(13, 2, 14, 3, "4")           # emblem
    c.p(14, 3, "5"); c.p(13, 2, "6") if False else None
    c.p(15, 3, "4") if False else None
    c.p(11, 2, "y"); c.p(11, 6, "y")


@reg("back/exo")
def _(c):
    # exoskeleton frame: outboard struts, shoulder pylons, hip bar, knee joints, foot plates
    c.r(2, 4, 2, 21, "2"); c.r(13, 4, 13, 21, "3")
    c.r(3, 4, 3, 21, "1") if False else None
    c.r(2, 4, 2, 9, "1")
    c.r(2, 8, 5, 9, "2"); c.r(10, 8, 13, 9, "3")          # shoulder yoke
    c.r(2, 8, 5, 8, "1"); c.r(10, 8, 13, 8, "2")
    c.r(2, 14, 5, 15, "2"); c.r(10, 14, 13, 15, "3")      # hip clamps
    c.r(1, 17, 3, 18, "3"); c.r(12, 17, 14, 18, "3")      # knee joints
    c.p(2, 17, "1"); c.p(1, 17, "1")
    c.r(1, 21, 4, 22, "2"); c.r(11, 21, 14, 22, "3")      # foot plates
    c.p(1, 21, "1"); c.p(1, 22, "1")
    for (x, y) in ((2, 4), (13, 4), (2, 12), (13, 12), (2, 19), (13, 19)):
        c.p(x, y, "4")                                    # joint lights
    c.p(2, 6, "5"); c.p(13, 6, "6")
    c.p(4, 7, "3"); c.p(11, 7, "3"); c.p(4, 8, "3"); c.p(11, 8, "3")
    c.p(2, 3, "4"); c.p(13, 3, "4")                       # pylon tips


