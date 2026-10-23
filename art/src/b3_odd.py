"""B3 restyle: odd creatures (plants, oozes, robots, misc)."""
from style_b3 import C


def blob(c, cx, cy, rx, ry, lt, md, dk, hl=None):
    """shaded ellipse: light top-left, dark bottom-right rim."""
    for y in range(24):
        for x in range(16):
            u = (x - cx) / rx
            v = (y - cy) / ry
            d = u * u + v * v
            if d <= 1:
                t = (u + v) / 2
                ch = md
                if d > 0.55 and t > 0.15:
                    ch = dk
                elif t < -0.18 and d < 0.9:
                    ch = lt
                c.p(x, y, ch)
    if hl:
        c.p(int(cx - rx * 0.45), int(cy - ry * 0.5), hl)
        c.p(int(cx - rx * 0.45) + 1, int(cy - ry * 0.5), hl)
        c.p(int(cx - rx * 0.45), int(cy - ry * 0.5) + 1, hl)


def glowpad():
    c = C()
    # round pad with a notch, a bloom with an eye and a lure bulb
    blob(c, 7.5, 15, 7.5, 5, "1", "2", "3")
    c.r(7, 11, 8, 15, ".")   # notch (mouth edge)
    c.r(7, 13, 8, 15, "3")
    c.p(7, 15, "O"); c.p(8, 15, "O")
    for x, y in ((3, 14), (12, 14), (4, 17), (11, 17), (7, 18), (2, 16)):
        c.p(x, y, "4")
    # puffed bloom: glowing orb on stalk
    c.line(8, 12, 8, 7, "3")
    c.line(7, 12, 6, 8, "3")
    blob(c, 7.5, 5, 3.5, 3.5, "4", "5", "6")
    c.p(6, 4, "w"); c.p(7, 4, "w")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.r(3, 1, 3, 1, "4"); c.p(12, 2, "4"); c.p(7, 0, "4"); c.p(1, 4, "4"); c.p(14, 5, "4")
    c.shadow(0, 15)
    return c.out()


def qudzu():
    c = C()
    # matted frond mound with a toothy maw flower
    for (x0, y0, x1, y1) in ((7, 14, 0, 8), (7, 15, 0, 14), (7, 16, 1, 20), (6, 12, 3, 4), (7, 11, 6, 2)):
        c.line(x0, y0, x1, y1, "3", mirror=True)
        c.line(x0 + (1 if x0 < 7 else 0), y0, x1 + 1, y1, "2", mirror=True)
    blob(c, 7.5, 16, 6, 4.5, "2", "2", "3")
    c.r(3, 15, 5, 16, "1")
    for x, y in ((2, 9), (1, 14), (2, 19), (4, 4), (6, 3)):
        c.m(x, y, "1")
    # maw
    blob(c, 7.5, 12, 4, 3.5, "5", "5", "6")
    c.r(5, 11, 10, 13, "O")
    for x in (5, 7, 9):
        c.p(x, 11, "w"); c.p(x + 1, 13, "w")
    c.p(7, 12, "4"); c.p(8, 12, "4")
    c.m(2, 7, "4"); c.m(4, 4, "4")
    c.shadow(1, 14)
    return c.out()


def dreadroot():
    c = C()
    # shoots on top
    for x0, x1, yt in ((5, 3, 1), (7, 7, 0), (10, 12, 2)):
        c.line(x0, 8, x1, yt, "6")
        c.p(x1, yt, "4")
    c.p(3, 0, "4"); c.p(12, 1, "5")
    # tuber belly
    blob(c, 7.5, 13, 6.5, 6, "1", "2", "3")
    # face
    c.r(4, 10, 6, 11, "O"); c.r(9, 10, 11, 11, "O")
    c.p(5, 10, "4"); c.p(10, 10, "4")
    c.r(5, 14, 10, 15, "O")
    for x in (5, 7, 9):
        c.p(x, 14, "w")
    c.p(6, 15, "w"); c.p(8, 15, "w")
    # rootlets
    for x0, x1 in ((4, 1), (6, 4), (9, 11), (11, 14)):
        c.line(x0, 18, x1, 21, "3")
    c.line(7, 19, 7, 22, "3"); c.line(8, 19, 9, 22, "3")
    c.p(1, 21, "6"); c.p(14, 21, "6")
    c.shadow(0, 15)
    return c.out()


def seed_vine():
    c = C()
    # curled tendrils hugging a central seed pod that spits upward
    for r_, ch in ((6.5, "2"), (5, "1")):
        pass
    blob(c, 7.5, 15, 7, 6, "1", "2", "3")
    blob(c, 7.5, 15, 4.5, 4, "3", "3", "3")
    # tendril spirals on the ring
    for x, y in ((2, 12), (3, 10), (5, 9), (3, 15), (2, 18), (4, 20), (13, 12), (12, 10), (10, 9)):
        c.p(x, y, "1")
    c.line(2, 18, 6, 21, "1"); c.line(13, 18, 9, 21, "2")
    c.line(2, 12, 0, 8, "2"); c.line(0, 8, 2, 6, "2"); c.p(2, 5, "1")
    c.line(13, 12, 15, 8, "2"); c.line(15, 8, 13, 6, "2"); c.p(13, 5, "1")
    # pod
    blob(c, 7.5, 14, 3, 3, "4", "5", "6")
    c.r(7, 8, 8, 12, "5")
    c.r(6, 6, 9, 8, "6"); c.r(7, 7, 8, 8, "O")     # spitting muzzle
    c.p(6, 6, "4"); c.p(9, 6, "4")
    c.p(7, 3, "w"); c.p(8, 1, "w"); c.p(7, 4, "4")   # flying seeds
    c.p(6, 13, "w"); c.p(7, 13, "w")
    c.shadow(0, 15)
    return c.out()


def young_ivory():
    c = C()
    # shale rents with blooming spinescent ivory shoots + an eye bud
    c.r(1, 18, 14, 21, "E")
    c.r(1, 18, 14, 18, "e")
    c.r(0, 20, 15, 21, "E")
    spikes = [(7, 17, 7, 1, 2), (4, 18, 1, 5, 2), (11, 18, 14, 4, 2), (5, 18, 4, 8, 1), (10, 18, 11, 8, 1), (2, 19, 0, 11, 1), (13, 19, 15, 10, 1)]
    for x0, y0, x1, y1, w in spikes:
        c.line(x0, y0, x1, y1, "2")
        if w == 2:
            c.line(x0 + 1, y0, x1 + (1 if x1 >= x0 else 0), y1 + 1, "3")
            c.line(x0 - 1, y0, x1 - 1, y1 + 1, "1")
        c.p(x1, y1, "w")
    c.line(7, 17, 7, 1, "w")
    # eye bud in the middle
    blob(c, 7.5, 14, 3.5, 3.5, "1", "2", "3")
    c.r(6, 13, 9, 14, "O"); c.p(7, 13, "4"); c.p(8, 13, "4"); c.p(7, 14, "6")
    c.p(7, 8, "4"); c.p(5, 11, "4"); c.p(10, 11, "4")
    c.shadow(0, 15)
    return c.out()


def plant():
    c = C()
    # jilted lover: thorny cirri reaching up like arms with a weeping red bloom
    blob(c, 7.5, 16, 4.5, 5, "1", "2", "3")
    c.r(5, 21, 10, 21, "3")
    c.r(4, 20, 11, 21, "3")
    for x0, y0, x1, y1 in ((5, 13, 2, 8), (2, 8, 3, 3), (4, 15, 0, 12), (0, 12, 0, 6)):
        c.line(x0, y0, x1, y1, "2"); c.line(x0 + 1, y0, x1 + 1, y1, "3")
        c.line(15 - x0, y0, 15 - x1, y1, "2"); c.line(14 - x0, y0, 14 - x1, y1, "3")
    # thorns
    for x, y in ((1, 10), (4, 6), (1, 4), (3, 12)):
        c.m(x, y, "4")
    c.m(3, 2, "5"); c.m(0, 5, "5")
    # face with weeping eyes + bloom
    c.r(5, 11, 6, 12, "O"); c.r(9, 11, 10, 12, "O")
    c.p(5, 11, "w"); c.p(10, 11, "w")
    c.p(5, 13, "5"); c.p(10, 13, "5")
    c.r(6, 15, 9, 15, "O"); c.p(7, 16, "5")
    blob(c, 7.5, 7, 3, 3, "4", "5", "6")
    c.p(6, 6, "w"); c.p(7, 4, "4"); c.p(8, 4, "4")
    c.p(7, 7, "3"); c.p(8, 7, "3")
    c.shadow(0, 15)
    return c.out()


def jel():
    c = C()
    blob(c, 7.5, 14, 7.5, 7, "1", "2", "3")
    c.r(1, 18, 4, 20, "3"); c.r(11, 19, 14, 20, "3")
    blob(c, 7.5, 14, 7.5, 7, "1", "2", "3")
    # shoal of eels under the membrane (bright detail), each with an eye
    for pts in (((3, 11), (4, 11), (5, 10), (6, 10), (7, 11), (8, 11)),
                ((5, 15), (6, 16), (7, 16), (8, 15), (9, 15), (10, 16)),
                ((9, 12), (10, 12), (11, 13), (11, 14))):
        for x, y in pts:
            c.p(x, y, "4"); c.p(x, y + 1, "5")
        c.p(pts[0][0] - 1, pts[0][1], "w")
    # glossy highlight
    c.r(3, 8, 6, 8, "w"); c.p(2, 9, "w"); c.p(2, 10, "w"); c.p(11, 9, "w")
    c.shadow(0, 15)
    return c.out()


def mushroom():
    c = C()
    # puffer: wide cap with gills, stem, eyes, spore cloud
    c.r(5, 15, 10, 21, "w")
    c.r(5, 15, 6, 21, "y"); c.r(10, 15, 10, 21, "S")
    c.r(4, 21, 11, 21, "S")
    blob(c, 7.5, 9, 7.5, 6, "1", "2", "3")
    c.r(0, 10, 15, 12, ".")
    c.r(1, 10, 14, 11, "3")
    c.r(1, 12, 14, 12, "O")
    for x in range(2, 14, 2):
        c.p(x, 12, "3"); c.p(x, 13, "5")
    c.r(3, 13, 12, 13, "6")
    c.r(2, 10, 13, 10, "2")
    # spots
    for x, y in ((4, 5), (8, 4), (11, 7), (6, 8)):
        c.p(x, y, "4"); c.p(x + 1, y, "4"); c.p(x, y + 1, "5")
    # eyes on stem
    c.p(6, 17, "O"); c.p(9, 17, "O"); c.r(7, 19, 8, 19, "O")
    # spores
    for x, y in ((0, 6), (14, 3), (1, 2), (11, 0), (15, 9), (3, 0), (15, 6)):
        c.p(x, y, "4")
    c.shadow(2, 13)
    return c.out()


def prickler():
    c = C()
    # spiky ball on a short stalk, with a face and long radiating spines
    import math
    for k in range(12):
        a = k * math.pi / 6
        x0 = 7.5 + math.cos(a) * 5; y0 = 9 + math.sin(a) * 5
        x1 = 7.5 + math.cos(a) * 9; y1 = 9 + math.sin(a) * 9
        c.line(round(x0), round(y0), round(x1), round(y1), "w")
        c.p(round(x1), round(y1), "4")
    c.r(6, 15, 9, 21, "2"); c.r(6, 15, 6, 21, "1"); c.r(9, 16, 9, 21, "3")
    c.r(4, 21, 11, 21, "3"); c.r(5, 20, 10, 20, "2")
    blob(c, 7.5, 9, 5, 5, "1", "2", "3")
    for x, y in ((4, 5), (11, 6), (3, 10), (12, 11), (6, 14), (9, 3)):
        c.p(x, y, "5")
    c.r(5, 7, 6, 8, "O"); c.r(9, 7, 10, 8, "O")
    c.p(5, 7, "4"); c.p(9, 7, "4"); c.p(6, 8, "w"); c.p(10, 8, "w")
    c.r(6, 11, 9, 12, "O"); c.p(6, 11, "w"); c.p(8, 11, "w"); c.p(7, 12, "w"); c.p(9, 12, "w")
    c.shadow(0, 15)
    return c.out()


def urchin():
    c = C()
    import math
    # radial penta-cake: five-lobed star, velvet hairs, gleaming mouth
    for y in range(24):
        for x in range(16):
            dx = (x - 7.5) / 1.0
            dy = (y - 12) / 1.25
            r = math.hypot(dx, dy)
            th = math.atan2(dy, dx) + math.pi / 2
            R = 5.6 + 2.6 * math.cos(5 * th)
            if r <= R:
                ch = "2"
                if r > R - 1.3:
                    ch = "3" if (dx + dy) > 0 else "1"
                elif dy < -1 and dx < 2:
                    ch = "1"
                c.p(x, y, ch)
    for k in range(5):
        a = -math.pi / 2 + k * 2 * math.pi / 5
        x = 7.5 + math.cos(a) * 6.3
        y = 12 + math.sin(a) * 7.7
        c.p(round(x), round(y), "4")
        c.p(round(7.5 + math.cos(a) * 4.2), round(12 + math.sin(a) * 5.2), "5")
    c.ell(7.5, 12, 2.5, 2.8, "O")
    c.r(7, 11, 8, 12, "4"); c.p(7, 11, "w")
    c.shadow(0, 15)
    return c.out()


def _fish(c, x, y, f="1", m="2", d="4", right=False):
    sgn = -1 if right else 1
    c.r(x, y, x + 3 * sgn if sgn > 0 else x - 3, y + 1, m)
    c.p(x, y, f)
    # tail
    tx = x + 4 * sgn
    c.p(tx, y - 1, d); c.p(tx, y, d); c.p(tx, y + 1, d); c.p(tx + sgn, y - 1, d); c.p(tx + sgn, y + 1, d)
    c.p(x + sgn, y, "w")        # unlidded eye
    c.p(x + sgn, y + 1, "3")
    c.p(x + 2 * sgn, y - 1, f)


def _fish(c, x, y, left=True):
    s = 1 if left else -1
    def P(dx, dy, ch):
        c.p(x + s * dx, y + dy, ch)
    for dx in (1, 2, 3, 4):
        P(dx, 0, "1"); P(dx, 1, "2"); P(dx, 2, "3")
    P(0, 1, "2"); P(1, -1, "1"); P(2, -1, "1")
    P(1, 3, "3")
    P(2, 1, "4"); P(3, 1, "4")
    P(5, 0, "5"); P(5, 1, "5"); P(5, 2, "5"); P(6, -1, "5"); P(6, 3, "5")
    P(1, 0, "w"); P(1, 1, "O")


def _fish(c, x, y):
    # big fish swimming left: x,y = nose
    rows = {0: (2, 6), 1: (1, 7), 2: (1, 7), 3: (2, 6)}
    for dy, (a, b) in rows.items():
        for dx in range(a, b + 1):
            c.p(x + dx - 1, y + dy, "1" if dy == 0 else "2" if dy < 3 else "3")
    c.p(x, y + 1, "2"); c.p(x, y + 2, "3")
    c.r(x + 3, y + 1, x + 5, y + 1, "4")     # stripe
    c.p(x + 5, y - 1, "1"); c.p(x + 4, y - 1, "1")  # dorsal
    for dy in range(-1, 5):
        c.p(x + 7, y + dy, "5")
        if dy in (0, 3):
            c.p(x + 8, y + dy - 1 if dy == 0 else y + dy + 1, "5")
    c.p(x + 8, y + 1, "5"); c.p(x + 8, y + 2, "5")
    c.p(x + 1, y + 1, "w"); c.p(x + 1, y + 2, "O")   # unlidded eye


def fish_school():
    c = C()
    _fish(c, 0, 2)
    _fish(c, 5, 9)
    _fish(c, 1, 15)
    _fish(c, 6, 21 - 1) if False else None
    c.shadow(0, 15)
    return c.out()


def palm():
    c = C()
    # melted-star trunk with an eye knot and drooping fronds
    c.r(6, 11, 9, 21, "n")
    c.r(6, 11, 6, 21, "N") if False else None
    c.r(9, 11, 9, 21, "N")
    c.r(4, 19, 11, 21, "n"); c.r(3, 21, 12, 21, "N")
    c.r(5, 14, 5, 14, "n")
    for y in (13, 16, 19):
        c.r(6, y, 9, y, "N")
    c.r(7, 15, 8, 17, "N"); c.p(7, 16, "O"); c.p(8, 16, "O")
    c.p(7, 15, "4"); c.p(8, 15, "4")
    c.r(7, 14, 8, 14, "n")
    # crown fronds
    fr = [(7, 10, 0, 6), (7, 9, 1, 2), (8, 9, 14, 2), (8, 10, 15, 6), (7, 9, 5, 0), (8, 9, 10, 0)]
    for x0, y0, x1, y1 in fr:
        c.line(x0, y0, x1, y1, "2")
        c.line(x0 + 1, y0, x1 + 1, y1, "1")
    for x0, y0, x1, y1 in ((2, 3, 0, 9), (13, 3, 15, 9), (1, 7, 1, 12), (14, 7, 14, 12)):
        c.line(x0, y0, x1, y1, "3")
    c.r(6, 8, 9, 10, "2"); c.r(6, 8, 7, 9, "1")
    # glowing fruit
    c.p(6, 11, "5"); c.p(9, 11, "5"); c.p(7, 11, "4"); c.p(8, 11, "4")
    c.shadow(2, 13)
    return c.out()


def aloe():
    c = C()
    # squat agave: thick fleshy toothed leaves pointing up and out from a short base
    leaves = [(7, 16, 7, 1), (6, 16, 3, 3), (9, 16, 12, 3), (5, 17, 0, 8), (10, 17, 15, 8), (4, 18, 0, 14), (11, 18, 15, 14)]
    for x0, y0, x1, y1 in leaves:
        n = max(abs(x1 - x0), abs(y1 - y0))
        for i in range(n + 1):
            t = i / n
            x = x0 + (x1 - x0) * t
            y = y0 + (y1 - y0) * t
            w = 2.3 * (1 - t) + 0.4
            for dx in range(-3, 4):
                if abs(dx) <= w:
                    ch = "2"
                    if dx < -w + 1:
                        ch = "1"
                    elif dx > w - 1:
                        ch = "3"
                    c.p(round(x) + dx, round(y), ch)
                    if abs(dx) > w - 1 and i % 3 == 1:
                        c.p(round(x) + dx + (1 if dx > 0 else -1), round(y), "w")
    c.r(3, 17, 12, 21, "2"); c.r(3, 17, 12, 17, "1"); c.r(10, 18, 12, 21, "3")
    c.r(5, 21, 10, 21, "3")
    for x in (4, 7, 10):
        c.p(x, 19, "3")
    c.p(7, 2, "4"); c.p(3, 3, "4"); c.p(12, 3, "4"); c.p(0, 8, "4"); c.p(15, 8, "4")
    blob(c, 7.5, 15, 2, 2, "4", "5", "6"); c.p(7, 15, "O"); c.p(8, 15, "O")
    c.shadow(0, 15)
    return c.out()


def yonderbrush():
    c = C()
    stems = [(3, 21, 2, 6), (6, 21, 6, 3), (8, 21, 9, 5), (11, 21, 12, 8), (13, 21, 14, 11), (1, 21, 0, 12)]
    for x0, y0, x1, y1 in stems:
        c.line(x0, y0, x1, y1, "3")
    for x0, y0, x1, y1 in stems:
        # panicle: fuzzy plume
        c.r(x1 - 1, y1 - 1, x1 + 1, y1 + 2, "5")
        c.p(x1, y1 - 2, "4"); c.p(x1, y1 - 1, "4")
        c.p(x1 - 1, y1 - 1, "5"); c.p(x1 + 1, y1 - 1, "4")
        c.p(x1, y1 + 3, "6")
    for x, y in ((4, 2), (8, 1), (11, 4), (14, 7), (1, 8), (4, 12), (10, 11)):
        c.p(x, y, "4")
    # eye at the base
    c.r(4, 19, 11, 21, "2"); c.r(5, 18, 10, 18, "1")
    c.r(6, 19, 9, 20, "O"); c.p(7, 19, "4"); c.p(8, 19, "w")
    c.shadow(0, 15)
    return c.out()


def waydroid():
    c = C()
    # dormant: slumped chrome droid, visor dark with one dim light
    c.r(4, 3, 11, 9, "l")
    c.r(4, 3, 11, 3, "w"); c.r(4, 3, 4, 9, "w")
    c.r(11, 4, 11, 9, "L")
    c.r(5, 5, 10, 7, "O")
    c.p(6, 6, "4"); c.p(7, 6, "5")
    c.p(7, 1, "L"); c.p(7, 2, "L"); c.p(8, 0, "4")
    c.r(6, 10, 9, 10, "L")
    # torso hunched
    c.r(3, 11, 12, 18, "l")
    c.r(3, 11, 12, 12, "w")
    c.r(10, 12, 12, 18, "L")
    c.r(5, 13, 10, 16, "L")
    c.r(6, 14, 9, 15, "O")
    c.p(7, 14, "4"); c.p(8, 14, "5")
    # arms drooped
    c.r(1, 11, 2, 19, "l"); c.r(13, 11, 14, 19, "L")
    c.r(1, 19, 2, 20, "L"); c.r(13, 19, 14, 20, "O")
    # folded legs
    c.r(4, 19, 6, 21, "L"); c.r(9, 19, 11, 21, "L")
    c.r(3, 21, 7, 21, "O"); c.r(8, 21, 12, 21, "O")
    c.p(5, 19, "l"); c.p(10, 19, "l")
    c.shadow(0, 15)
    return c.out()


def asphodelyte():
    c = C()
    # alluring bloom with a lipped maw, swaying anthers, leaf arms
    c.r(7, 13, 8, 21, "2")
    c.r(7, 13, 7, 21, "1")
    c.line(7, 20, 2, 15, "2"); c.line(8, 20, 13, 15, "3")
    c.line(7, 21, 2, 17, "1"); c.line(8, 21, 13, 17, "2")
    c.line(2, 15, 0, 13, "2"); c.line(13, 15, 15, 13, "3")
    # petals
    for k, (x, y, w, h) in enumerate(((0, 4, 4, 6), (12, 4, 4, 6), (2, 1, 4, 5), (10, 1, 4, 5), (5, 0, 6, 4), (3, 6, 3, 6), (10, 6, 3, 6))):
        c.r(x, y, x + w - 1, y + h - 1, "4" if k % 2 == 0 else "5")
    c.r(4, 3, 11, 12, "5")
    c.r(4, 3, 11, 3, "4")
    c.r(4, 11, 11, 12, "6")
    # maw
    c.r(5, 5, 10, 10, "O")
    c.r(6, 4, 9, 4, "6")
    for x in (5, 7, 9):
        c.p(x, 5, "w"); c.p(x + 1, 10, "w")
    # anthers
    c.line(7, 5, 6, 0, "y"); c.line(8, 5, 10, 0, "y")
    c.p(6, 0, "y"); c.p(10, 0, "y")
    c.p(7, 8, "r"); c.p(8, 8, "r")
    c.r(6, 13, 9, 13, "3")
    c.shadow(0, 15)
    return c.out()


def _voider(c, big=False):
    # long anxious legs, central stomach-orb
    legs = [(5, 12, 0, 4, 1), (5, 13, 0, 11, 2), (5, 15, 1, 19, 3), (6, 16, 3, 22, 4)]
    if big:
        legs = [(5, 11, 0, 3, 1), (5, 12, 0, 9, 2), (5, 14, 0, 15, 3), (5, 16, 1, 21, 4), (6, 17, 4, 22, 5)]
    for x0, y0, x1, y1, _ in legs:
        c.line(x0, y0, x1, y1, "2", mirror=True)
        c.line(x0, y0 + 1, x1, y1 + 1, "3", mirror=True)
    for x0, y0, x1, y1, _ in legs:
        c.m(x1, y1, "1")
    # orb abdomen
    blob(c, 7.5, 13, 4.5, 5, "1", "2", "3")
    c.ell(7.5, 14, 2.5, 3, "5")
    c.p(6, 13, "4"); c.p(7, 13, "w"); c.p(7, 15, "6"); c.p(8, 15, "6"); c.p(9, 16, "5")
    # head segment with fangs
    c.r(5, 5, 10, 9, "2"); c.r(5, 5, 10, 5, "1"); c.r(9, 7, 10, 9, "3")
    c.p(6, 6, "4"); c.p(9, 6, "4")
    c.r(6, 6, 6, 7, "4"); c.r(9, 6, 9, 7, "4")
    c.p(6, 6, "w"); c.p(9, 6, "w")
    c.m(5, 10, "w") if not big else None
    c.line(6, 9, 5, 12, "w"); c.line(9, 9, 10, 12, "w")
    if big:
        c.line(5, 9, 4, 13, "w"); c.line(10, 9, 11, 13, "w")
        c.p(5, 14, "4"); c.p(10, 14, "4"); c.p(7, 11, "4")
    c.shadow(0, 15)


def voider():
    c = C()
    _voider(c)
    return c.out()


def voider_greater():
    c = C()
    _voider(c, True)
    c.r(4, 4, 11, 4, "3")
    c.p(7, 3, "4"); c.p(8, 3, "4"); c.p(5, 2, "4"); c.p(10, 2, "4")
    return c.out()


def flybot():
    c = C()
    # filament wings (detail), chrome thorax, segmented abdomen, pincer
    for x0, y0, x1, y1 in ((5, 8, 0, 2), (5, 9, 0, 6), (5, 10, 0, 11), (5, 9, 2, 0)):
        c.line(x0, y0, x1, y1, "4", mirror=True)
    for x0, y0, x1, y1 in ((4, 9, 1, 4), (4, 10, 1, 8)):
        c.line(x0, y0, x1, y1, "5", mirror=True)
    # head
    c.r(5, 2, 10, 5, "l"); c.r(5, 2, 10, 2, "w")
    c.m(5, 3, "4"); c.m(6, 3, "4"); c.m(5, 4, "5")
    c.m(6, 3, "w")
    c.r(7, 5, 8, 6, "L")
    c.line(5, 2, 3, 0, "L"); c.line(10, 2, 12, 0, "L")
    # thorax
    c.r(5, 7, 10, 11, "l"); c.r(5, 7, 10, 7, "w"); c.r(9, 8, 10, 11, "L")
    c.r(7, 8, 8, 10, "L"); c.p(7, 9, "4"); c.p(8, 9, "4")
    # legs
    c.line(5, 10, 2, 14, "L"); c.line(10, 10, 13, 14, "L")
    c.line(5, 9, 2, 8, "L") if False else None
    # abdomen
    for i, y in enumerate(range(12, 19, 2)):
        wd = 3 - i // 2
        c.r(8 - wd, y, 7 + wd, y, "l")
        c.r(8 - wd, y + 1, 7 + wd, y + 1, "L")
    c.p(7, 12, "w")
    # pincer claw
    c.line(7, 19, 5, 22, "L"); c.line(8, 19, 10, 22, "L")
    c.p(5, 22, "4"); c.p(10, 22, "4"); c.p(6, 22, "L"); c.p(9, 22, "L")
    c.shadow(0, 15)
    return c.out()


def tombbot():
    c = C()
    # mirrored chrome colossus, seated: broad shoulders, slit eye, loose sequins
    c.r(5, 1, 10, 6, "l"); c.r(5, 1, 10, 1, "w"); c.r(5, 1, 5, 6, "w"); c.r(10, 2, 10, 6, "L")
    c.r(5, 3, 10, 4, "O"); c.r(6, 3, 9, 3, "4"); c.p(7, 4, "5"); c.p(8, 4, "5")
    c.p(7, 0, "L"); c.p(8, 0, "4")
    c.r(6, 7, 9, 7, "L")
    # shoulders
    c.r(0, 8, 5, 11, "l"); c.r(10, 8, 15, 11, "L")
    c.r(0, 8, 5, 8, "w"); c.r(10, 8, 15, 8, "l")
    c.r(1, 9, 1, 10, "w")
    c.p(2, 10, "4"); c.p(13, 10, "5")
    # torso
    c.r(4, 8, 11, 16, "l"); c.r(4, 8, 11, 8, "w"); c.r(9, 9, 11, 16, "L")
    c.r(6, 10, 9, 13, "L"); c.r(7, 11, 8, 12, "4")
    c.p(7, 11, "w")
    c.r(5, 15, 10, 15, "O")
    # arms
    c.r(0, 12, 3, 17, "L"); c.r(12, 12, 15, 17, "L")
    c.r(0, 12, 1, 17, "l"); c.r(0, 18, 3, 19, "l"); c.r(12, 18, 15, 19, "l")
    c.r(0, 19, 3, 19, "O") if False else None
    # seated legs
    c.r(3, 17, 12, 20, "l"); c.r(3, 17, 12, 17, "w"); c.r(9, 18, 12, 20, "L")
    c.r(2, 21, 13, 21, "L"); c.r(2, 21, 5, 21, "l")
    c.r(7, 17, 8, 20, "L")
    # sequins
    for x, y in ((3, 6), (13, 5), (1, 3), (14, 14), (2, 22)):
        c.p(x, y, "w")
    c.p(14, 7, "4"); c.p(1, 6, "5")
    c.shadow(0, 15)
    return c.out()


# ------------------------------------------------------------------ kit3a

def rifle_turret():
    c = C()
    # splayed tripod under a boxy body with a long rifle
    c.line(6, 14, 0, 21, "L"); c.line(9, 14, 15, 21, "L"); c.line(7, 15, 7, 21, "L"); c.line(8, 15, 8, 21, "L")
    c.line(5, 14, 0, 20, "l"); c.line(10, 14, 15, 20, "l")
    c.r(0, 21, 2, 21, "O"); c.r(13, 21, 15, 21, "O"); c.r(6, 21, 9, 21, "O")
    c.r(2, 8, 13, 15, "l"); c.r(2, 8, 13, 8, "w"); c.r(2, 8, 2, 15, "w"); c.r(10, 9, 13, 15, "L")
    c.r(4, 10, 9, 14, "L"); c.r(5, 11, 8, 13, "O")
    c.r(5, 11, 6, 12, "4"); c.p(5, 11, "w"); c.p(8, 12, "5")
    c.r(11, 10, 12, 11, "4"); c.p(11, 10, "5") if False else None
    # rifle: barrel with shroud and muzzle glow
    c.r(6, 1, 9, 8, "l"); c.r(9, 1, 9, 8, "L"); c.r(6, 1, 6, 8, "w")
    c.r(5, 5, 10, 6, "L"); c.r(7, 0, 8, 0, "4")
    c.r(7, 1, 8, 2, "O"); c.p(7, 1, "5")
    c.r(1, 6, 3, 7, "L"); c.p(1, 6, "4")
    c.shadow(0, 15)
    return c.out()


def templar_mech_1():
    c = C()
    # heavy chrome walker: great shoulder-cannon on one side, helm slit
    c.r(5, 1, 10, 6, "l"); c.r(5, 1, 10, 1, "w"); c.r(9, 2, 10, 6, "L")
    c.r(6, 3, 9, 4, "O"); c.p(6, 3, "4"); c.p(7, 3, "4"); c.p(8, 3, "4"); c.p(9, 3, "4")
    c.p(7, 0, "4"); c.p(8, 0, "4"); c.p(7, 1, "4")
    # shoulders w/ cross
    c.r(1, 7, 5, 11, "l"); c.r(10, 7, 14, 11, "L")
    c.r(1, 7, 5, 7, "w")
    c.p(3, 8, "4"); c.p(2, 9, "4"); c.p(3, 9, "4"); c.p(4, 9, "4"); c.p(3, 10, "4")
    c.r(11, 8, 13, 10, "O"); c.p(12, 9, "4")
    # torso
    c.r(5, 7, 10, 15, "l"); c.r(5, 7, 10, 7, "w"); c.r(9, 8, 10, 15, "L")
    c.r(6, 9, 9, 12, "L"); c.r(7, 10, 8, 11, "5")
    # arms: left holds a hammer, right the cannon
    c.r(0, 11, 2, 17, "l"); c.r(0, 11, 0, 17, "w")
    c.r(13, 11, 15, 16, "L"); c.r(14, 16, 15, 20, "l")
    c.r(14, 21, 15, 21, "4") if False else None
    c.p(15, 21, "4"); c.p(14, 21, "4")
    c.r(0, 18, 2, 20, "L")
    # legs
    c.r(4, 16, 6, 21, "l"); c.r(9, 16, 11, 21, "L")
    c.r(4, 16, 4, 21, "w")
    c.r(3, 21, 6, 21, "O"); c.r(9, 21, 12, 21, "O")
    c.r(7, 15, 8, 16, "O")
    c.shadow(0, 15)
    return c.out()


def templar_mech_2():
    c = C()
    # lighter striding mech: tall visor dome, shield on arm, blade-arm
    c.r(6, 0, 9, 5, "l"); c.r(6, 0, 9, 0, "w"); c.r(9, 1, 9, 5, "L")
    c.r(5, 2, 10, 2, "L")
    c.r(6, 3, 9, 3, "4"); c.r(7, 3, 8, 3, "w")
    c.r(7, 6, 8, 6, "L")
    # shoulders + spikes
    c.r(2, 7, 5, 9, "l"); c.r(10, 7, 13, 9, "L")
    c.p(1, 6, "w"); c.p(2, 5, "L"); c.p(14, 6, "L"); c.p(13, 5, "L")
    # torso w/ lights
    c.r(5, 7, 10, 14, "l"); c.r(5, 7, 10, 7, "w"); c.r(9, 8, 10, 14, "L")
    c.r(6, 9, 9, 10, "O"); c.p(6, 9, "4"); c.p(8, 9, "4"); c.p(7, 10, "5"); c.p(9, 10, "5")
    c.r(6, 12, 9, 13, "L")
    # shield on left
    c.r(0, 9, 3, 16, "L"); c.r(1, 10, 2, 15, "l"); c.r(1, 10, 1, 15, "w"); c.p(2, 12, "4"); c.p(2, 13, "4")
    # blade arm right
    c.r(11, 10, 12, 14, "l"); c.line(14, 8, 14, 21, "w"); c.line(15, 10, 15, 20, "l")
    c.r(13, 15, 15, 15, "L")
    c.p(14, 7, "w")
    # legs, wide stance
    c.r(4, 15, 6, 17, "l"); c.r(9, 15, 11, 17, "L")
    c.line(4, 18, 2, 21, "l"); c.line(5, 18, 3, 21, "L")
    c.line(11, 18, 13, 21, "L"); c.line(10, 18, 12, 21, "L")
    c.r(1, 21, 4, 21, "O"); c.r(11, 21, 14, 21, "O")
    c.shadow(0, 15)
    return c.out()


def scrapbot():
    c = C()
    # boxy tracked normality bot with a glowing eye and a sweeping arm
    c.r(3, 17, 12, 21, "L"); c.r(3, 17, 12, 17, "l")
    for x in range(3, 13, 2):
        c.p(x, 19, "O"); c.p(x, 20, "O")
    c.r(2, 21, 13, 21, "O")
    c.r(4, 6, 11, 16, "l"); c.r(4, 6, 11, 6, "w"); c.r(4, 6, 4, 16, "w"); c.r(10, 7, 11, 16, "L")
    # head with eye
    c.r(5, 1, 10, 5, "l"); c.r(5, 1, 10, 1, "w"); c.r(9, 2, 10, 5, "L")
    c.r(6, 2, 9, 4, "O"); c.r(7, 3, 8, 3, "4"); c.p(7, 2, "w"); c.p(6, 3, "5") ; c.p(9, 3, "5")
    c.line(8, 0, 11, 0, "L"); c.p(12, 0, "4"); c.p(8, 0, "L")
    c.r(6, 5, 9, 5, "O") if False else None
    # chest plate with lights
    c.r(5, 8, 9, 13, "L"); c.r(6, 9, 8, 12, "O")
    c.p(6, 9, "4"); c.p(7, 9, "5"); c.p(8, 9, "4"); c.p(6, 11, "5"); c.p(8, 11, "4")
    c.p(7, 11, "O")
    # arms: one claw, one sweeper
    c.r(2, 7, 3, 12, "l"); c.r(0, 12, 3, 13, "L"); c.r(0, 14, 1, 15, "l"); c.r(2, 14, 3, 15, "l")
    c.r(12, 7, 13, 9, "L"); c.line(14, 9, 14, 15, "l"); c.r(13, 15, 15, 16, "L"); c.p(14, 17, "4")
    c.shadow(0, 15)
    return c.out()


def godhed():
    c = C()
    # greebled egg of metal with a big circuited-glass pane, on small legs
    blob(c, 7.5, 11, 6.5, 9.5, "l", "l", "L")
    c.r(2, 4, 4, 5, ".")
    for p in ((2, 4), (3, 4), (2, 5)):
        pass
    c.r(1, 12, 14, 12, "L")
    # glass pane
    c.ell(7.5, 9.5, 4, 5, "O")
    c.ell(7.5, 9.5, 3, 4, "4")
    c.r(5, 8, 10, 11, "5")
    c.r(6, 9, 9, 10, "4")
    c.p(7, 9, "w"); c.p(7, 10, "w")
    c.p(5, 6, "w"); c.p(6, 5, "w")
    # circuit lines
    c.line(4, 10, 4, 14, "L") if False else None
    c.p(6, 7, "6"); c.p(9, 12, "6"); c.p(5, 11, "6")
    # greebles
    c.r(2, 3, 3, 3, "w"); c.p(12, 4, "L"); c.r(12, 14, 13, 15, "L"); c.r(2, 15, 3, 16, "w")
    c.p(13, 6, "O"); c.p(2, 8, "O")
    c.line(7, 2, 7, 0, "L"); c.p(8, 0, "4")
    c.line(5, 2, 3, 0, "L") ; c.p(3, 0, "4")
    # rim lights
    c.p(3, 12, "4"); c.p(12, 12, "4")
    # stubby legs
    c.r(4, 19, 5, 21, "L"); c.r(10, 19, 11, 21, "L"); c.r(7, 20, 8, 21, "L")
    c.r(3, 21, 6, 21, "O"); c.r(9, 21, 12, 21, "O")
    c.shadow(0, 15)
    return c.out()


def interdictor():
    c = C()
    import math
    # space inverter core with radial handles
    c.ell(7.5, 12, 6.5, 8, "O")
    c.ell(7.5, 12, 5.5, 7, "L")
    c.ell(7.5, 12, 4.5, 6, "l")
    c.ell(7.5, 12, 3, 4, "O")
    c.ell(7.5, 12, 2, 3, "5")
    c.r(6, 11, 9, 13, "4")
    c.p(7, 12, "w")
    c.r(4, 8, 6, 8, "w")
    # handles radial
    for k in range(8):
        a = k * math.pi / 4 + math.pi / 8
        x0 = 7.5 + math.cos(a) * 6
        y0 = 12 + math.sin(a) * 7.5
        x1 = 7.5 + math.cos(a) * 8
        y1 = 12 + math.sin(a) * 10.5
        c.line(round(x0), round(y0), round(x1), round(y1), "L")
        c.p(round(x1), round(y1), "4")
    c.shadow(0, 15)
    return c.out()


def kaleidoslug():
    c = C()
    # banded glass slug with eyestalks, glow
    segs = [(7.5, 7, 3.5, 3, "1"), (7.5, 11, 5, 4, "2"), (7.5, 16, 5.5, 4.5, "1"), (7.5, 20, 4, 2.5, "2")]
    for cx, cy, rx, ry, ch in segs:
        blob(c, cx, cy, rx, ry, "1", ch if ch == "2" else "2", "3")
    # kaleido stripes
    for y, ch in ((9, "4"), (13, "5"), (15, "4"), (18, "5"), (20, "4")):
        c.r(4, y, 11, y, ch)
    c.r(7, 8, 8, 21, "5") if False else None
    # glassy highlight
    c.p(4, 12, "w"); c.p(4, 13, "w"); c.p(5, 17, "w"); c.p(5, 16, "w"); c.p(6, 5, "w")
    # eyestalks
    c.line(6, 5, 4, 1, "2"); c.line(9, 5, 11, 1, "2")
    c.r(3, 0, 4, 1, "w"); c.r(11, 0, 12, 1, "w")
    c.p(3, 0, "O"); c.p(12, 0, "O")
    c.p(7, 7, "O"); c.p(8, 7, "O")
    c.shadow(0, 15)
    return c.out()


def sludge():
    c = C()
    blob(c, 7.5, 15, 7.5, 6.5, "1", "2", "3")
    # drips and pseudopods
    c.r(0, 17, 1, 20, "2"); c.r(14, 18, 15, 20, "3"); c.r(3, 21, 4, 22, "3"); c.r(10, 21, 12, 21, "3")
    c.r(6, 4, 9, 9, "2"); c.r(5, 8, 10, 9, "2"); c.r(6, 4, 7, 6, "1"); c.r(7, 3, 8, 3, "2")
    c.r(10, 7, 10, 9, "3")
    # bubbles
    for x, y, d in ((4, 13, "5"), (11, 15, "5"), (7, 18, "4"), (3, 17, "4"), (12, 12, "4")):
        c.p(x, y, d); c.p(x + 1, y, d); c.p(x, y + 1, "6")
    c.p(4, 13, "w")
    # glossy highlights
    c.r(2, 11, 4, 11, "w"); c.p(2, 12, "w"); c.p(6, 4, "w"); c.p(7, 5, "w")
    # eye-like glow
    c.p(7, 8, "O"); c.p(9, 8, "O")
    c.shadow(0, 15)
    return c.out()


def chainlaser():
    c = C()
    # base mount + three barrels in a triangle, glowing
    c.r(3, 17, 12, 21, "L"); c.r(3, 17, 12, 17, "l"); c.r(2, 21, 13, 21, "O")
    c.r(6, 15, 9, 17, "l")
    for x in (4, 7, 10):
        c.p(x, 19, "4")
    # barrels
    c.r(4, 3, 6, 15, "l"); c.r(9, 3, 11, 15, "L"); c.r(6, 0, 9, 12, "l")
    c.r(4, 3, 4, 15, "w"); c.r(6, 0, 6, 12, "w") if False else None
    c.r(6, 0, 9, 1, "O"); c.r(7, 0, 8, 1, "4")
    c.r(4, 3, 6, 4, "O"); c.p(5, 3, "5"); c.r(9, 3, 11, 4, "O"); c.p(10, 3, "5")
    c.r(4, 9, 11, 9, "L"); c.r(4, 13, 11, 13, "L")
    c.r(7, 1, 8, 12, "l"); c.r(9, 1, 9, 12, "L")
    for y in (6, 11):
        c.p(5, y, "4"); c.p(10, y, "4"); c.p(7, y - 4 if y > 6 else y, "4") if False else None
    c.p(7, 5, "w"); c.p(8, 7, "4"); c.p(7, 11, "w")
    c.shadow(0, 15)
    return c.out()


def pig():
    c = C()
    # farm pig facing left: snout disc, floppy ears, pouch belly, curly tail
    blob(c, 9.5, 14, 6, 5.5, "1", "2", "3")
    # head
    blob(c, 4, 12, 3.6, 3.6, "1", "2", "3")
    c.r(0, 11, 1, 14, "S"); c.r(0, 11, 0, 14, "s")   # snout disc
    c.p(0, 12, "O"); c.p(0, 13, "O") if False else None
    c.p(1, 12, "O"); c.p(1, 13, "O")
    c.p(2, 12, "S") if False else None
    c.r(2, 7, 4, 9, "3"); c.p(2, 7, "2"); c.p(3, 7, "2")   # floppy ear
    c.r(5, 8, 6, 10, "3"); c.p(5, 8, "2")                  # second ear
    c.p(3, 11, "O"); c.p(2, 11, "w") if False else None
    # curly tail
    for x, y in ((15, 12), (15, 11), (14, 10), (13, 10), (13, 11)):
        c.p(x, y, "S")
    # trotters
    c.r(5, 18, 6, 21, "2"); c.r(11, 18, 12, 21, "3"); c.r(8, 19, 9, 20, "3")
    c.r(4, 21, 7, 21, "O"); c.r(10, 21, 13, 21, "O")
    for x, y in ((9, 11), (12, 13), (8, 16), (11, 17), (10, 9)):
        c.p(x, y, "5")
    c.shadow(0, 15)
    return c.out()


def chromeling():
    c = C()
    # scrap-metal likeness: lopsided can-head, plank torso, riveted limbs, one glowing eye
    c.r(4, 1, 10, 6, "l"); c.r(4, 1, 10, 1, "w"); c.r(4, 1, 4, 6, "w"); c.r(10, 2, 10, 6, "L")
    c.r(5, 3, 7, 4, "O"); c.p(6, 3, "4"); c.p(6, 4, "5")
    c.p(9, 4, "O")
    c.p(3, 2, "L"); c.p(2, 1, "l"); c.p(8, 0, "L"); c.p(11, 5, "L")
    c.r(6, 6, 9, 6, "O")
    # torso patchwork
    c.r(4, 7, 11, 15, "l"); c.r(4, 7, 11, 7, "w")
    c.r(8, 9, 11, 15, "L"); c.r(4, 11, 7, 13, "y")
    c.r(5, 8, 6, 9, "w"); c.p(10, 8, "w")
    for x, y in ((5, 12), (6, 14), (10, 11), (9, 14)):
        c.p(x, y, "O")
    c.p(7, 9, "4"); c.p(7, 15, "4")
    # arms mismatched
    c.r(1, 8, 3, 9, "L"); c.r(0, 10, 2, 16, "l"); c.r(0, 16, 3, 17, "y")
    c.r(12, 8, 14, 9, "l"); c.r(13, 10, 14, 15, "L"); c.r(12, 16, 15, 18, "l")
    # legs different lengths
    c.r(4, 16, 6, 21, "l"); c.r(9, 16, 11, 19, "L")
    c.r(9, 20, 10, 21, "y")
    c.r(3, 21, 7, 21, "O"); c.r(8, 21, 12, 21, "O")
    c.shadow(0, 15)
    return c.out()


def nest():
    c = C()
    # breathing nest-skin mound with dark cavities and glinting larvae
    blob(c, 7.5, 14, 7.5, 8, "1", "2", "3")
    c.r(0, 18, 15, 21, ".")
    c.ell(7.5, 17, 7.5, 4.5, "2")
    c.r(1, 19, 14, 21, "3")
    # plies
    for y, x0, x1 in ((9, 3, 12), (12, 1, 14), (16, 1, 14)):
        c.r(x0, y, x1, y, "3")
        c.r(x0 + 1, y - 1, x1 - 2, y - 1, "1")
    # cavities
    for cx, cy in ((5, 7), (10, 10), (4, 13), (9, 15), (12, 18), (6, 19)):
        c.r(cx - 1, cy, cx + 1, cy + 1, "O")
        c.p(cx, cy, "O")
        c.p(cx, cy + 1, "4"); c.p(cx + 1, cy, "5") if cx % 2 else None
    c.p(5, 7, "w"); c.p(10, 10, "w")
    c.p(7, 3, "1"); c.p(8, 3, "1")
    c.shadow(0, 15)
    return c.out()


OVERRIDES = {
    "kit": {
        "glowpad": glowpad(), "qudzu": qudzu(), "dreadroot": dreadroot(), "seed_vine": seed_vine(),
        "young_ivory": young_ivory(), "plant": plant(), "jel": jel(), "mushroom": mushroom(),
        "prickler": prickler(), "urchin": urchin(), "fish_school": fish_school(), "palm": palm(),
        "aloe": aloe(), "yonderbrush": yonderbrush(), "waydroid": waydroid(),
        "asphodelyte": asphodelyte(), "voider": voider(), "flybot": flybot(), "tombbot": tombbot(),
    },
    "kit3a": {
        "rifle_turret": rifle_turret(), "voider": voider_greater(), "templar_mech_2": templar_mech_2(),
        "templar_mech_1": templar_mech_1(), "scrapbot": scrapbot(), "godhed": godhed(),
        "interdictor": interdictor(), "kaleidoslug": kaleidoslug(), "sludge": sludge(),
        "chainlaser": chainlaser(), "pig": pig(), "chromeling": chromeling(), "nest": nest(),
    },
}
