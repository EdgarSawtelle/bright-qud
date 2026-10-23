"""B3 restyle: deep-dwelling / weird creatures of kit3b (non-humanoid)."""
import math
from style_b3 import C


def worm3b():
    c = C()
    cx = lambda y: 8 + 2.6 * math.sin(y / 3.3)
    for y in range(5, 23):
        x0 = round(cx(y))
        w = 3 if y < 20 else 2
        sh = ("1", "2", "2", "3")[y % 4] if y % 3 else "3"
        c.r(x0 - w, y, x0 + w, y, sh)
        c.p(x0 - w, y, "1" if y % 3 else "3")
        c.p(x0 + w, y, "3")
    # collagen bubbles (detail)
    for y, side in ((7, -1), (10, 1), (13, -1), (16, 1), (19, -1)):
        bx = round(cx(y)) + side * 4
        c.r(bx - 1, y, bx, y + 1, "4"); c.p(bx - 1, y, "w"); c.p(bx, y + 1, "5")
    # head with round toothed mouth
    c.ell(cx(3), 3.2, 4, 3, "1")
    c.r(round(cx(3)) - 4, 4, round(cx(3)) + 4, 5, "2")
    hx = round(cx(3))
    c.ell(hx, 3, 2.5, 2, "O")
    c.ell(hx, 3, 1.2, 1, "6")
    for dx in (-2, 2):
        c.p(hx + dx, 2, "w"); c.p(hx + dx, 4, "w")
    c.p(hx, 1, "w"); c.p(hx, 5, "w")
    c.p(hx - 4, 1, "O"); c.p(hx + 4, 1, "O")
    c.shadow(3, 13)
    return c.out()


def crab3b():
    c = C()
    # legs (detail), pointed
    for sx in (0, 1):
        m = (lambda x, y, ch: c.p(15 - x if sx else x, y, ch))
    for (x0, y0, x1, y1) in [(5, 13, 1, 12), (5, 15, 1, 17), (6, 17, 3, 22), (6, 11, 3, 8)]:
        c.line(x0, y0, x1, y1, "5", mirror=True)
        c.line(x0, y0 + 1, x1, y1 + 1, "6", mirror=True)
    c.m(1, 12, "4"); c.m(1, 17, "4"); c.m(3, 22, "4")
    # shell
    c.ell(7.5, 14, 5.5, 4.5, "2")
    c.ell(7.5, 13, 4.5, 3, "1")
    c.r(3, 17, 12, 18, "3")
    c.r(5, 12, 10, 12, "2"); c.r(6, 15, 9, 15, "3")
    # eyestalk husks with moss
    c.mr(5, 8, 5, 10, "w"); c.mr(5, 7, 5, 7, "g"); c.mr(4, 7, 4, 7, "G")
    c.m(5, 6, "g"); c.m(6, 6, "h")
    c.m(5, 10, "2")
    # monolith claw (left, huge pincer) and small right claw
    c.r(0, 0, 2, 5, "4"); c.r(4, 0, 6, 5, "4"); c.r(0, 0, 0, 5, "5"); c.r(6, 0, 6, 5, "6")
    c.r(0, 5, 6, 9, "4"); c.r(0, 5, 1, 9, "5"); c.r(5, 5, 6, 9, "6"); c.r(0, 9, 6, 9, "6")
    c.p(3, 3, "6"); c.p(3, 2, "6"); c.p(1, 1, "w"); c.p(4, 1, "w"); c.p(2, 6, "w"); c.p(2, 7, "w")
    c.r(2, 10, 5, 11, "2"); c.r(5, 10, 6, 11, "1")
    c.r(12, 8, 15, 11, "4"); c.r(12, 7, 12, 8, "4"); c.r(15, 7, 15, 8, "5"); c.r(14, 11, 15, 11, "6")
    c.p(13, 8, "O")
    c.p(12, 12, "2"); c.p(12, 11, "1")
    c.shadow(0, 15)
    return c.out()


def fish3b():
    c = C()
    # kite-sail dorsal fin
    c.line(5, 11, 8, 1, "4"); c.line(12, 11, 8, 1, "4")
    for y in range(2, 12):
        a = round(8 - (y - 1) * 0.35 - 0.5 * (y > 6)); b = round(8 + (y - 1) * 0.7)
        c.r(a, y, b, y, "4" if y < 7 else "5")
    c.line(8, 1, 12, 11, "6"); c.line(9, 3, 9, 11, "w"); c.line(10, 5, 10, 11, "5")
    # body facing left, broad head
    c.ell(7, 15, 6.5, 4.5, "2")
    c.ell(6, 14, 5, 3, "1")
    c.r(3, 18, 11, 19, "3")
    # tail
    c.r(12, 13, 14, 17, "2"); c.r(14, 10, 15, 20, "1"); c.p(15, 10, "3"); c.p(15, 20, "3")
    c.r(13, 15, 13, 15, "3")
    # broad face: eye, mouth, gill
    c.r(1, 14, 1, 16, "3")
    c.r(2, 17, 5, 17, "O")
    c.ell(3, 13, 1.8, 1.8, "w")
    c.p(3, 13, "O"); c.p(2, 13, "O")
    c.r(6, 13, 6, 17, "3"); c.p(5, 15, "3")
    c.r(8, 15, 11, 15, "5"); c.r(8, 13, 10, 13, "5")
    c.r(5, 20, 8, 21, "5")
    c.shadow(1, 15)
    return c.out()


def fly3b():
    c = C()
    # wings (translucent-looking detail)
    for sx in (0,):
        c.ell(3.5, 9, 3.5, 6, "4"); c.ell(3.5, 9, 2.2, 4.5, "5")
        c.ell(12.5, 9, 3.5, 6, "4"); c.ell(12.5, 9, 2.2, 4.5, "5")
    c.line(3, 4, 6, 12, "6", mirror=True)
    # legs
    for (x0, y0, x1, y1) in [(6, 10, 1, 13), (6, 12, 2, 18), (6, 14, 4, 21)]:
        c.line(x0, y0, x1, y1, "3", mirror=True)
    # abdomen striped
    c.ell(7.5, 17, 3.5, 5, "2")
    for y in (14, 16, 18, 20):
        c.r(5, y, 10, y, "3")
    c.r(6, 13, 7, 19, "1") if False else None
    c.p(6, 15, "1"); c.p(6, 17, "1"); c.p(6, 19, "1")
    # thorax
    c.ell(7.5, 10, 3, 2.5, "1"); c.r(6, 9, 9, 9, "w")
    c.r(7, 11, 8, 12, "2")
    # head with huge red holoptic eyes
    c.r(5, 4, 10, 7, "2")
    c.ell(5, 5.5, 2.5, 2.5, "R"); c.ell(10, 5.5, 2.5, 2.5, "R")
    c.p(4, 4, "r"); c.p(11, 4, "r"); c.p(5, 6, "r"); c.p(10, 6, "r")
    c.p(4, 4, "w"); c.p(11, 4, "w")
    c.r(7, 7, 8, 8, "3")
    c.line(6, 3, 4, 1, "3"); c.line(9, 3, 11, 1, "3")
    c.shadow(1, 14)
    return c.out()


def cyclops3b():
    c = C()
    # long arms to the ground
    for sx in (0,):
        c.r(1, 8, 3, 17, "2"); c.r(0, 10, 1, 18, "1")
        c.r(12, 8, 14, 17, "2"); c.r(14, 10, 15, 18, "3")
    c.r(0, 18, 3, 20, "1"); c.r(12, 18, 15, 20, "3")
    c.m(1, 21, "5"); c.m(3, 21, "5")
    c.m(0, 20, "5") if False else None
    # torso
    c.r(4, 9, 11, 17, "2"); c.r(4, 9, 6, 16, "1"); c.r(10, 10, 11, 17, "3")
    c.r(6, 13, 9, 15, "1")
    c.r(7, 14, 8, 15, "4") if False else None
    # legs
    c.r(5, 18, 7, 21, "2"); c.r(9, 18, 11, 21, "3"); c.r(4, 21, 7, 21, "5"); c.r(9, 21, 12, 21, "5")
    # head
    c.r(4, 1, 11, 8, "2"); c.r(5, 0, 10, 0, "1"); c.r(4, 1, 5, 3, "1")
    c.r(3, 3, 3, 6, "3") ; c.r(12, 3, 12, 6, "3")
    c.r(5, 3, 10, 8, "4")      # naked face
    c.r(5, 3, 10, 3, "5")
    c.r(6, 4, 9, 6, "w")
    c.r(7, 4, 8, 6, "r") ; c.p(7, 5, "O"); c.p(8, 5, "O") ; c.p(7, 4, "R"); 
    c.r(6, 7, 9, 7, "O"); c.p(7, 7, "w"); c.p(9, 7, "w")
    c.r(5, 8, 10, 8, "5")
    c.shadow(2, 13)
    return c.out()


def basilisk3b():
    c = C()
    # stone lizard, top-down, head up
    c.r(5, 0, 10, 5, "2"); c.r(6, 0, 9, 0, "1"); c.r(4, 5, 11, 9, "2")
    c.p(4, 3, "1"); c.p(11, 3, "3"); c.p(6, 4, "y"); c.p(9, 4, "y"); c.p(6, 5, "y"); c.p(9, 5, "y")
    c.p(7, 1, "O"); c.p(8, 1, "O")
    c.line(7, 6, 7, 9, "4"); c.line(9, 6, 9, 9, "4") if False else None
    # crest spikes
    c.m(3, 7, "1"); c.m(2, 8, "1"); c.m(3, 8, "2")
    c.r(3, 10, 12, 16, "2"); c.r(4, 10, 6, 15, "1"); c.r(10, 11, 12, 16, "3")
    # cracks revealing pale inside
    c.line(7, 11, 8, 14, "4"); c.line(8, 14, 6, 16, "4"); c.p(9, 12, "5"); c.p(5, 13, "5")
    c.line(10, 6, 11, 8, "5") ; c.p(5, 2, "5")
    # tail
    c.r(6, 17, 9, 19, "2"); c.r(6, 17, 7, 19, "1"); c.r(7, 20, 8, 22, "3"); c.p(7, 23, "3") if False else None
    c.p(9, 22, "3") ; c.p(10, 23, "x")
    # legs splayed with claws
    for (a, b) in ((1, 11), (1, 16)):
        c.r(a, b, a + 3, b + 2, "3"); c.r(a - 1 if a > 0 else 0, b + 1, a, b + 3, "1")
        c.r(11, b, 14, b + 2, "3") ; c.r(14, b + 1, 15, b + 3, "2")
        c.p(a - 1 if a > 0 else 0, b + 3, "w"); c.p(15, b + 3, "w")
    c.m(0, 13, "w") if False else None
    # dust specks below
    c.p(4, 22, "5"); c.p(12, 21, "5"); c.p(2, 21, "5")
    c.shadow(0, 15)
    return c.out()


def dacca3b():
    c = C()
    # stiff fronds fanning from the crown
    c.line(8, 7, 0, 2, "1", mirror=False); c.line(7, 7, 0, 1, "2")
    c.line(7, 7, 7, 0, "1"); c.line(8, 7, 8, 0, "2")
    c.line(8, 7, 15, 2, "2"); c.line(7, 7, 15, 1, "3")
    c.line(7, 7, 2, 5, "2"); c.line(8, 7, 13, 5, "3")
    c.line(7, 6, 3, 8, "3"); c.line(8, 6, 12, 8, "3")
    c.r(6, 6, 9, 8, "2"); c.r(6, 6, 7, 8, "1")
    # trunk
    c.r(5, 9, 10, 16, "2"); c.r(5, 9, 6, 16, "1"); c.r(10, 9, 10, 16, "3")
    c.r(5, 12, 10, 12, "3"); c.r(5, 15, 10, 15, "3")
    # bunch of unbananas hanging in a pattern (detail)
    for i, (x, y) in enumerate([(3, 8), (5, 9), (10, 9), (12, 8), (4, 11), (11, 11)]):
        c.r(x, y, x + 1, y + 3, "4"); c.p(x, y, "w") if False else None
        c.p(x + 1, y + 2, "6"); c.p(x + 1, y + 3, "6"); c.p(x, y + 3, "5")
    c.r(7, 10, 8, 11, "5"); c.p(7, 10, "4")
    # inverted hands as legs: palm up top, fingers down
    for sx in (0,):
        c.r(4, 17, 6, 18, "5"); c.r(9, 17, 11, 18, "5")
        for x in (3, 4, 5, 6):
            c.line(x, 19, x - 1 if x < 5 else x, 22, "5")
        for x in (9, 10, 11, 12):
            c.line(x, 19, x + 1 if x > 10 else x, 22, "5")
    c.r(3, 19, 7, 19, "4") if False else None
    c.p(2, 22, "6") ; c.p(13, 22, "6")
    c.shadow(1, 14)
    return c.out()


def flamingo3b():
    c = C()
    # facing left; S-neck, bent beak
    c.line(4, 2, 4, 2, "1")
    c.r(2, 1, 5, 3, "1"); c.p(2, 2, "O") if False else None
    c.p(4, 2, "O")
    # beak (detail) hooked downward
    c.r(0, 2, 2, 3, "6"); c.p(0, 3, "5"); c.p(0, 4, "5"); c.p(1, 4, "5") ; c.r(1, 2, 2, 2, "4")
    c.r(2, 3, 2, 3, "w") if False else None
    # neck
    c.r(5, 3, 6, 4, "1"); c.r(6, 4, 7, 6, "1"); c.r(5, 6, 6, 8, "2") ; c.r(4, 8, 5, 9, "1")
    c.r(5, 9, 6, 10, "1")
    # body
    c.ell(9.5, 13, 5, 3.5, "1")
    c.r(5, 12, 13, 13, "1"); c.r(6, 15, 13, 16, "2")
    c.r(11, 12, 15, 14, "2"); c.r(13, 11, 15, 11, "3"); c.r(14, 14, 15, 16, "3")
    # wing coral tint
    c.r(8, 12, 12, 14, "2"); c.r(9, 13, 11, 14, "5"); c.p(8, 12, "1"); c.r(10, 12, 12, 12, "4")
    c.p(12, 15, "5"); c.p(14, 15, "6")
    # legs (orchid)
    c.line(9, 16, 9, 21, "5"); c.line(11, 16, 12, 21, "5")
    c.r(7, 21, 9, 21, "4"); c.r(11, 21, 14, 21, "4")
    c.p(9, 19, "6"); c.p(12, 19, "6")
    c.shadow(5, 15)
    return c.out()


def catapult3b():
    c = C()
    # fulcrete blocks stack (bottom right feed rail)
    c.r(11, 15, 15, 19, "e") ; c.r(11, 15, 15, 15, "E")
    c.r(12, 17, 14, 18, "E") if False else None
    c.r(12, 16, 14, 18, "e"); c.line(12, 16, 14, 16, "E")
    c.r(0, 15, 3, 18, "e") if False else None
    # base platform
    c.r(2, 17, 13, 20, "2"); c.r(2, 17, 13, 17, "1"); c.r(2, 20, 13, 20, "3")
    c.r(3, 18, 12, 19, "3") if False else None
    c.r(4, 18, 5, 19, "4"); c.p(5, 18, "w"); c.p(10, 18, "4")
    # wheels
    for x in (3, 8, 12):
        c.ell(x, 21, 2, 1.8, "L"); c.p(x, 21, "l")
    c.r(1, 21, 14, 21, "L") if False else None
    # arm: chrome, rising up-left
    c.r(6, 11, 9, 16, "2"); c.r(6, 11, 6, 16, "1")
    c.line(8, 12, 3, 3, "l"); c.line(9, 12, 4, 3, "L"); c.line(7, 12, 2, 3, "l")
    # bucket (chrome)
    c.r(0, 1, 6, 1, "l"); c.r(0, 2, 0, 4, "l"); c.r(6, 2, 6, 3, "L")
    c.r(1, 4, 5, 5, "L"); c.r(1, 2, 5, 3, "O")
    c.r(1, 3, 4, 3, "e"); c.r(1, 2, 3, 2, "E")
    c.r(1, 1, 5, 1, "w")
    # lights
    c.p(7, 13, "R"); c.p(8, 13, "R"); c.p(7, 14, "4"); c.p(8, 14, "4")
    c.r(7, 8, 9, 10, "L") if False else None
    c.r(9, 9, 11, 11, "l"); c.r(10, 10, 11, 11, "L") ; c.p(9, 9, "w")
    c.shadow(0, 15)
    return c.out()


def cupola3b():
    c = C()
    # gelatin cupola: octagonal base prism, smaller top face
    c.r(4, 4, 11, 6, "1")                    # top face
    c.r(4, 4, 11, 4, "w") if False else None
    c.r(5, 3, 10, 3, "1")
    c.r(1, 7, 14, 8, "2")                    # shoulder band
    c.r(2, 6, 13, 6, "2")
    c.r(0, 9, 15, 20, "2")
    c.r(1, 21, 14, 21, "3")
    # facet shading
    c.r(0, 9, 4, 20, "1"); c.r(11, 9, 15, 20, "3")
    c.r(5, 9, 10, 20, "2")
    c.line(4, 4, 1, 8, "3"); c.line(11, 4, 14, 8, "3")
    c.line(4, 7, 4, 20, "3") ; c.line(11, 7, 11, 20, "3")
    c.r(5, 7, 10, 7, "3")
    # specular glints
    c.p(6, 4, "w"); c.p(7, 4, "w"); c.p(1, 10, "w"); c.p(1, 11, "w")
    # internal debris & bubbles (detail)
    c.r(6, 16, 7, 17, "4"); c.p(6, 16, "5"); c.p(9, 18, "5"); c.p(13, 15, "4"); c.p(2, 18, "5")
    c.p(12, 11, "4") ; c.p(3, 14, "5")
    # hungry face: twin eyes, gaping mouth
    c.r(5, 11, 6, 12, "O"); c.r(9, 11, 10, 12, "O")
    c.p(5, 11, "4"); c.p(9, 11, "4")
    c.r(6, 14, 9, 15, "O"); c.p(6, 14, "w"); c.p(9, 14, "w")
    c.shadow(0, 15)
    return c.out()


def slynth3b():
    c = C()
    # wide brimmed hat with lantern
    c.r(1, 3, 14, 4, "2"); c.r(0, 4, 15, 4, "3"); c.r(2, 3, 13, 3, "1")
    c.r(4, 0, 11, 2, "2"); c.r(4, 0, 7, 2, "1"); c.r(10, 1, 11, 2, "3")
    c.r(5, 2, 10, 2, "4")
    # lantern hanging from hat, glowing
    c.line(13, 5, 13, 7, "O")
    c.r(12, 8, 14, 11, "4"); c.p(13, 9, "w"); c.p(13, 10, "5"); c.r(12, 8, 14, 8, "6"); c.r(12, 12, 14, 12, "6")
    c.p(11, 10, "5"); c.p(15, 10, "5")
    # face under brim (wrong eyes)
    c.r(6, 5, 9, 8, "S") if False else None
    c.r(6, 5, 9, 8, "3"); c.p(6, 6, "y"); c.p(9, 6, "y"); c.p(7, 6, "y") if False else None
    c.p(6, 6, "w"); c.p(9, 6, "w"); c.p(7, 6, "O"); c.p(8, 6, "O") if False else None
    c.r(7, 8, 8, 8, "O")
    # long draped body
    c.r(5, 9, 10, 19, "2"); c.r(4, 14, 11, 20, "2"); c.r(5, 9, 6, 19, "1"); c.r(10, 10, 11, 20, "3")
    c.r(3, 19, 12, 21, "2"); c.r(3, 21, 12, 21, "3"); c.r(3, 19, 4, 20, "1")
    # arms, one long reaching to lantern
    c.r(11, 9, 12, 12, "2"); c.r(4, 10, 4, 15, "1")
    c.p(12, 7, "2") if False else None
    # sash
    c.line(5, 12, 10, 16, "5"); c.line(5, 13, 10, 17, "4")
    c.p(5, 22, "O"); c.p(10, 22, "O")
    c.shadow(3, 12)
    return c.out()


def sitter3b():
    c = C()
    # eyeball
    c.ell(7.5, 8.5, 6.5, 6.5, "w")
    c.ell(7.5, 8.5, 6.5, 6.5, "w")
    c.r(1, 9, 3, 12, "y") if False else None
    c.ell(7.5, 9, 4.2, 4.2, "1")
    c.ell(7.5, 9, 3, 3, "2")
    c.ell(7.5, 9, 1.6, 1.6, "O")
    c.p(6, 8, "w")
    # gallium circuitry iris lines
    for (x, y) in [(4, 7), (4, 9), (3, 10), (11, 7), (12, 9), (11, 11), (7, 5), (9, 13), (6, 13)]:
        c.p(x, y, "4")
    # veins
    c.p(2, 6, "r"); c.p(1, 8, "r"); c.p(13, 5, "r"); c.p(14, 8, "r"); c.p(3, 12, "r"); c.p(12, 13, "r")
    # unlidded rim
    c.line(3, 3, 12, 3, "6") if False else None
    # three spider-thin legs
    c.line(5, 14, 1, 17, "6"); c.line(1, 17, 1, 22, "6")
    c.line(8, 15, 8, 22, "6"); c.line(7, 15, 7, 22, "6") if False else None
    c.line(10, 14, 14, 17, "6"); c.line(14, 17, 14, 22, "6")
    c.p(0, 22, "5"); c.p(2, 22, "5"); c.p(7, 22, "5"); c.p(9, 22, "5"); c.p(13, 22, "5"); c.p(15, 22, "5")
    c.shadow(0, 15)
    return c.out()


def wren3b():
    c = C()
    # frill (crest)
    c.line(5, 4, 5, 0, "4"); c.line(4, 4, 2, 1, "5"); c.line(6, 4, 8, 1, "4"); c.p(3, 3, "5")
    # head and beak
    c.r(3, 4, 7, 7, "1"); c.r(3, 4, 4, 4, "2") if False else None
    c.r(0, 6, 3, 6, "w"); c.p(0, 7, "w") if False else None
    c.p(4, 5, "O"); c.p(4, 5, "w") if False else None
    c.p(5, 5, "O")
    # neck/body
    c.r(4, 8, 9, 11, "1"); c.ell(9, 13, 5, 4, "2"); c.ell(8, 12, 3.5, 2.5, "1")
    c.r(5, 15, 11, 16, "3")
    # epaulet glowing
    c.r(7, 9, 9, 10, "4"); c.p(8, 9, "w"); c.p(7, 10, "5") if False else None
    # wing folded
    c.r(9, 11, 13, 15, "2"); c.r(10, 12, 13, 14, "3"); c.line(10, 12, 13, 12, "1")
    c.p(13, 15, "3")
    # long split tail draping down
    c.line(12, 14, 12, 22, "2"); c.line(13, 14, 14, 21, "1")
    c.line(12, 18, 10, 22, "2"); c.line(13, 18, 14, 22, "2") if False else None
    c.r(11, 15, 13, 16, "2")
    c.p(10, 22, "5"); c.p(12, 22, "5") ; c.p(11, 21, "4") ; c.p(14, 21, "5")
    c.line(12, 17, 11, 17, "2")
    # talons
    c.line(7, 17, 7, 19, "5"); c.line(9, 17, 9, 19, "5")
    c.r(5, 20, 8, 20, "5") if False else None
    c.r(6, 19, 8, 19, "4"); c.r(8, 19, 10, 19, "4")
    c.shadow(4, 15, 21)
    return c.out()


def snail3b():
    c = C()
    # cone shell tilted, whorls
    rows = [(7, 8, 0), (6, 9, 1), (6, 9, 2), (5, 10, 3), (5, 10, 4), (4, 11, 5), (4, 11, 6), (3, 12, 7),
            (3, 12, 8), (2, 13, 9), (2, 13, 10), (1, 14, 11), (1, 14, 12), (1, 14, 13)]
    for (a, b, y) in rows:
        k = y % 4
        ch = ("1", "1", "2", "3")[k]
        c.r(a, y, b, y, ch)
        c.p(a, y, "w" if k < 2 else "1")
        c.p(b, y, "3")
    for y in (3, 7, 11):
        pass
    for y in range(1, 14):
        if y % 4 == 3:
            c.r(2 + 0 * y, y, 13, y, "3") if False else None
    # dizzying disharmony band: odd stripes
    c.r(5, 8, 9, 8, "5") if False else None
    c.p(7, 4, "4"); c.p(8, 4, "4"); c.p(6, 8, "4"); c.p(7, 8, "4"); c.p(9, 8, "4"); c.p(5, 12, "4"); c.p(6, 12, "4")
    c.p(10, 12, "4"); c.p(11, 12, "4")
    # shell mouth
    c.r(1, 14, 14, 16, "2"); c.r(2, 14, 12, 14, "1"); c.r(3, 15, 11, 16, "O") if False else None
    c.r(1, 16, 14, 16, "3")
    # soft body (detail blue)
    c.r(0, 17, 15, 20, "5"); c.r(0, 17, 5, 18, "4"); c.r(0, 20, 15, 20, "6")
    c.r(0, 15, 2, 17, "5"); c.r(0, 12, 1, 14, "4")
    c.r(10, 17, 15, 17, "4") if False else None
    # head and eyestalks left
    c.r(0, 15, 1, 19, "4")
    c.line(0, 14, 0, 10, "5"); c.line(2, 14, 3, 10, "5") if False else None
    c.p(0, 9, "w"); c.p(0, 10, "O")
    c.p(2, 18, "O") ; c.p(2, 17, "w")
    c.r(1, 21, 15, 21, "6") if False else None
    c.shadow(0, 15, 21); c.shadow(0, 15, 22)
    return c.out()


def eater3b():
    c = C()
    # fat slug body below, tapering
    for y in range(11, 22):
        w = 6 if y < 18 else 6 - (y - 17)
        c.r(8 - w, y, 7 + w, y, "2")
        c.p(8 - w, y, "1"); c.p(7 + w, y, "3")
    c.r(2, 12, 4, 17, "1"); c.r(11, 14, 13, 18, "3")
    for y in (13, 15, 17, 19):
        c.r(4, y, 11, y, "3")
    # memory glands
    for (x, y) in [(3, 13), (12, 15), (2, 17), (11, 18)]:
        c.r(x, y, x + 1, y + 1, "M"); c.p(x, y, "w") if False else None
        c.p(x, y, "4")
    # head: ringed toothed sucker mouth
    c.ell(7.5, 6, 7, 6, "3")
    c.ell(7.5, 6, 6, 5, "w")
    c.ell(7.5, 6, 5, 4, "3")
    c.ell(7.5, 6, 4, 3.2, "w")
    c.ell(7.5, 6, 3, 2.4, "3")
    c.ell(7.5, 6, 2, 1.6, "w")
    c.ell(7.5, 6, 1.3, 1, "4")
    c.p(7, 6, "M"); c.p(8, 6, "O")
    # extra "teeth" spikes
    c.p(7, 0, "w"); c.p(8, 0, "w"); c.p(1, 6, "w") if False else None
    c.shadow(1, 14)
    return c.out()


def eel3b():
    c = C()
    ys = lambda x: 14 + 3 * math.sin(x / 3.0 + 0.6)
    for x in range(3, 16):
        y = ys(x)
        c.r(x, round(y) - 2, x, round(y) + 2, "2")
        c.p(x, round(y) - 2, "1"); c.p(x, round(y) - 1, "1"); c.p(x, round(y) + 2, "3")
        if x % 3 == 0:
            c.r(x, round(y) - 4, x, round(y) - 3, "5"); c.p(x, round(y) - 5, "4")
            c.p(x, round(y) + 3, "5")
    for x in range(10, 16):
        c.p(x, round(ys(x)), "3") if x % 2 else None
    # head
    hy = round(ys(3))
    c.r(1, hy - 2, 4, hy + 2, "1"); c.r(2, hy - 3, 3, hy - 3, "1")
    c.r(1, hy + 2, 4, hy + 2, "2")
    c.p(3, hy - 1, "O"); c.p(3, hy - 2, "w")
    c.r(0, hy + 1, 1, hy + 1, "O")
    # sizzling barbels
    c.line(0, hy, 0, hy - 3, "6"); c.p(0, hy - 4, "w"); c.p(1, hy - 5, "w"); c.p(2, hy - 6, "4")
    c.line(1, hy + 3, 0, hy + 5, "6"); c.p(0, hy + 6, "w")
    for (x, y) in [(5, 3), (8, 1), (12, 3), (14, 19), (8, 21), (2, 18), (13, 8)]:
        c.p(x, y, "w")
    c.shadow(2, 13, 23)
    return c.out()


def jelly3b():
    c = C()
    # glassy bell
    c.ell(7.5, 7, 7, 6, "1")
    c.r(0, 7, 15, 11, "1")
    c.ell(7.5, 7, 7, 6, "1")
    c.r(1, 10, 14, 11, "2")
    c.r(0, 11, 15, 12, "3") if False else None
    c.r(1, 12, 14, 12, "3")
    c.r(3, 13, 12, 13, "2") if False else None
    # inner burning rose
    c.ell(7.5, 7, 4, 3.5, "5"); c.ell(7.5, 7, 2.5, 2.2, "4"); c.p(7, 7, "w"); c.p(8, 7, "w")
    c.p(7, 6, "w") ; c.p(5, 6, "g") ; c.p(10, 8, "g"); c.p(7, 9, "g"); c.p(9, 5, "5")
    # glassy highlights
    c.p(2, 4, "w"); c.p(3, 3, "w"); c.p(4, 2, "w")
    # frilled rim
    for x in range(1, 15, 2):
        c.p(x, 13, "2")
    # four feelers
    for (x, wob) in ((3, 1), (6, -1), (9, 1), (12, -1)):
        for y in range(13, 23):
            xx = x + (1 if (y // 3) % 2 == 0 else 0) * wob * (1 if x < 8 else 1)
            c.p(xx, y, "5" if y % 4 else "4")
        c.p(x + wob, 23, "x")
    c.shadow(1, 14)
    return c.out()


def hermit3b():
    c = C()
    # hunched humanoid carrying a reef
    # head with polyps
    c.r(5, 4, 10, 8, "2"); c.r(5, 4, 7, 6, "1") ; c.r(9, 6, 10, 8, "3")
    c.p(6, 6, "w"); c.p(9, 6, "w"); c.p(6, 6, "w"); c.p(7, 6, "O") if False else None
    c.r(6, 8, 9, 8, "O")
    # polyp stalks on head (coral red)
    c.line(5, 4, 3, 1, "4"); c.line(8, 4, 8, 1, "5"); c.line(10, 4, 12, 1, "4")
    c.p(3, 0, "6"); c.p(8, 0, "4"); c.p(12, 0, "6") ; c.p(2, 1, "5") if False else None
    # torso/shoulders with reef (detail coral)
    c.r(3, 9, 12, 16, "2"); c.r(3, 9, 6, 15, "1"); c.r(10, 11, 12, 16, "3")
    c.r(1, 9, 4, 12, "5"); c.r(11, 9, 14, 12, "5"); c.r(1, 9, 3, 10, "4"); c.r(12, 9, 14, 10, "4")
    c.p(0, 10, "4"); c.p(15, 10, "4"); c.p(1, 8, "6"); c.p(14, 8, "6")
    c.p(2, 7, "4"); c.p(13, 7, "4")
    c.r(5, 11, 10, 12, "5"); c.p(6, 11, "4"); c.p(9, 12, "4")
    # fullerite/chrome/glass fins
    c.line(3, 13, 0, 15, "l"); c.line(12, 13, 15, 15, "L")
    c.p(1, 15, "w"); c.p(14, 15, "b")
    # arms
    c.r(2, 13, 3, 18, "2"); c.r(12, 13, 13, 18, "3"); c.p(2, 18, "5") ; c.p(13, 18, "5")
    # legs
    c.r(5, 17, 7, 21, "2"); c.r(9, 17, 11, 21, "3")
    c.r(4, 21, 7, 21, "5"); c.r(9, 21, 12, 21, "5")
    c.r(7, 17, 9, 18, "5")
    c.shadow(1, 14)
    return c.out()


def anemone3b():
    c = C()
    # trunk rings (rubbery yellow)
    c.r(3, 16, 12, 21, "2"); c.r(2, 19, 13, 21, "2")
    c.r(3, 16, 5, 21, "1"); c.r(11, 17, 13, 21, "3")
    c.r(1, 21, 14, 21, "3")
    for y in (16, 18, 20):
        c.r(4, y, 11, y, "3")
    c.p(3, 17, "1"); c.p(3, 19, "1")
    c.r(4, 12, 11, 15, "2"); c.r(4, 12, 5, 15, "1"); c.r(10, 12, 11, 15, "3")
    c.r(4, 14, 11, 14, "3")
    # bouquet of tongues
    tongues = [((5, 12), (1, 7), (1, 2)), ((7, 12), (5, 6), (4, 1)), ((8, 12), (10, 6), (11, 1)),
               ((10, 12), (14, 7), (14, 3)), ((6, 12), (3, 8), (0, 8)), ((9, 12), (12, 8), (15, 9))]
    for k, (a, b, d) in enumerate(tongues):
        for (p, q) in ((a, b), (b, d)):
            for off in (0, 1):
                c.line(p[0] + off, p[1], q[0] + off, q[1], "4" if k % 2 == 0 else "5")
        c.p(d[0], d[1], "w") if False else None
        c.r(d[0], d[1] - 1, d[0] + 1, d[1], "4")
        c.p(d[0], d[1] - 1, "w")
    # map-like spots
    for (x, y) in [(2, 5), (6, 3), (11, 4), (13, 6), (4, 8), (12, 9), (7, 9)]:
        c.p(x, y, "6")
    # saliva drops
    c.p(0, 11, "w"); c.p(15, 12, "w"); c.p(1, 14, "w") if False else None
    c.shadow(0, 15)
    return c.out()


def lamprey3b():
    c = C()
    cx = lambda y: 8 + 3.2 * math.sin(y / 3.0 + 1.0)
    # ribbon body with frilly fins
    for y in range(8, 23):
        x = round(cx(y))
        w = 2
        c.r(x - w, y, x + w, y, "2")
        c.p(x - w, y, "1"); c.p(x + w, y, "3")
        c.p(x - w - 1, y, "5" if y % 2 else "4") ; c.p(x + w + 1, y, "5" if y % 2 == 0 else "6")
        if y % 3 == 0:
            c.p(x - w - 2, y, "4"); c.p(x + w + 2, y, "6")
    # tail tip
    # mouth ring with triangle teeth at the top
    hx = round(cx(8))
    c.ell(hx, 4, 4.5, 4.5, "1")
    c.ell(hx, 4, 4.5, 4.5, "1")
    c.ell(hx, 4, 3.5, 3.5, "w")
    c.ell(hx, 4, 2.2, 2.2, "O")
    for a in range(0, 8):
        ang = a * math.pi / 4
        c.p(round(hx + 2.2 * math.cos(ang)), round(4 + 2.2 * math.sin(ang)), "M")
    c.p(hx, 4, "m") if False else None
    c.r(hx - 1, 8, hx + 1, 8, "2")
    c.p(hx - 4, 5, "3"); c.p(hx + 4, 5, "3") ; c.p(hx - 4, 2, "1")
    c.p(hx - 3, 1, "4") ; c.p(hx + 3, 1, "6")
    c.shadow(2, 13)
    return c.out()


def pyramid3b():
    c = C()
    # floating chrome pyramid
    for y in range(2, 17):
        w = (y - 2) * 0.55
        a = round(7.5 - w); b = round(7.5 + w)
        c.r(a, y, 7, y, "l")
        c.r(8, y, b, y, "L")
        c.p(a, y, "w") ; c.p(b, y, "O")
    c.line(7, 2, 7, 17, "w") if False else None
    c.r(0, 17, 15, 17, "L") if False else None
    # base edge
    c.line(0, 16, 7, 18, "w"); c.line(15, 16, 8, 18, "L")
    c.line(7, 18, 8, 18, "O")
    # glowing blue eye / gem in center
    c.ell(7.5, 11, 2.7, 2, "4"); c.ell(7.5, 11, 1.4, 1.2, "5"); c.p(7, 11, "w")
    c.p(7, 10, "w")
    c.p(4, 11, "6") ; c.p(11, 11, "6")
    # orbiting shards
    c.r(1, 5, 2, 6, "4"); c.p(1, 5, "w"); c.r(13, 8, 14, 9, "5"); c.p(14, 4, "4"); c.p(2, 14, "5")
    # shadow/floating
    c.shadow(2, 13, 21); c.shadow(3, 12, 22); c.shadow(4, 11, 23)
    for x in range(3, 13):
        c.p(x, 21, "x")
    return c.out()


def ape3b():
    c = C()
    # chrome-bang head with huge cheek pads
    c.r(5, 2, 10, 8, "2"); c.r(5, 2, 10, 3, "l"); c.r(4, 3, 11, 3, "L")
    c.mr(0, 4, 4, 8, "4"); c.mr(1, 3, 3, 3, "5"); c.mr(0, 5, 1, 7, "5")
    c.mr(3, 5, 4, 6, "4"); c.mr(0, 8, 3, 8, "6")
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.p(6, 4, "w") if False else None
    c.r(6, 6, 9, 8, "1"); c.r(7, 8, 8, 8, "O")
    c.r(6, 6, 9, 6, "3") if False else None
    # shoulders & torso
    c.r(2, 9, 13, 14, "2"); c.r(2, 9, 5, 11, "1"); c.r(9, 11, 13, 14, "3"); c.r(2, 13, 13, 14, "3")
    c.r(5, 12, 10, 15, "3"); c.r(6, 10, 9, 11, "1")
    # crushing chrome arms to the ground (knuckle-walking)
    c.r(0, 9, 3, 12, "l"); c.r(12, 9, 15, 12, "L")
    c.r(0, 13, 2, 19, "l"); c.r(13, 13, 15, 19, "L"); c.r(1, 13, 1, 19, "w") if False else None
    c.r(0, 12, 3, 12, "w") ; c.p(0, 15, "w") ; c.p(15, 15, "O") ; c.p(0, 17, "L") ; c.p(15, 17, "l")
    c.r(0, 20, 3, 21, "L") ; c.r(12, 20, 15, 21, "L"); c.r(0, 20, 2, 20, "l")
    c.p(2, 21, "4"); c.p(13, 21, "4")
    # legs
    c.r(4, 15, 6, 21, "3"); c.r(9, 15, 11, 21, "3"); c.r(3, 21, 7, 21, "3"); c.r(8, 21, 12, 21, "3")
    c.p(7, 13, "4") if False else None
    c.shadow(0, 15)
    return c.out()


def crungle3b():
    c = C()
    # anchor shanks (legs) with flukes
    for (x0, x1) in ((4, 2), (8, 8), (12, 13)):
        c.line(x0, 14, x1, 20, "2"); c.line(x0 + 1, 14, x1 + 1, 20, "3")
    for (fx) in (2, 8, 13):
        c.r(fx - 2, 21, fx + 3, 21, "3"); c.p(fx - 2, 20, "2"); c.p(fx + 3, 20, "2"); c.p(fx - 3, 19, "2") if False else None
        c.p(fx, 21, "5") if False else None
    c.r(0, 22, 15, 22, "5") if False else None
    c.p(5, 22, "5"); c.p(11, 22, "5"); c.p(1, 22, "5") ; c.p(14, 22, "5")
    # saucer, tilted
    c.ell(7.5, 13, 7.5, 3, "2")
    c.r(0, 11, 15, 13, "2")
    c.ell(7.5, 12, 6.5, 2, "O")
    c.ell(7.5, 12, 5.5, 1.3, "3")
    c.r(1, 14, 14, 15, "3") ; c.r(2, 15, 6, 15, "2") if False else None
    c.r(0, 12, 2, 13, "1"); c.p(0, 11, "1")
    # nubs on rim
    for x in (1, 4, 7, 10, 13):
        c.p(x, 10 + (1 if x in (1, 13) else 0), "4"); c.p(x, 9 + (1 if x in (1, 13) else 0), "5")
    # steamy globe
    c.ell(7.5, 7, 4.5, 4.5, "B"); c.ell(7.5, 7, 3.5, 3.5, "b") if False else None
    c.ell(7.5, 7.5, 3.3, 3.3, "4"); c.ell(7.5, 8, 2, 2, "5")
    c.p(6, 5, "w"); c.p(7, 5, "w"); c.p(5, 6, "w")
    c.r(5, 10, 10, 11, "3") if False else None
    # steam
    for (x, y) in [(5, 1), (6, 0), (10, 2), (9, 0), (8, 1), (11, 0)]:
        c.p(x, y, "w" if (x + y) % 2 else "4")
    c.shadow(0, 15)
    return c.out()


def chromeling3b():
    c = C()
    # head: rough box with visor slit and a bolt
    c.r(4, 1, 11, 7, "l"); c.r(4, 1, 11, 1, "w"); c.r(4, 1, 5, 7, "w") if False else None
    c.r(11, 2, 11, 7, "L"); c.r(4, 7, 11, 7, "L")
    c.r(5, 3, 10, 4, "O"); c.p(6, 3, "4"); c.p(9, 3, "4"); c.p(6, 4, "5"); c.p(9, 4, "5")
    c.p(4, 1, "O") ; c.p(11, 1, "O")
    c.p(7, 0, "L"); c.p(8, 0, "l") ; c.p(8, 1, "w")
    c.p(10, 6, "y") ; c.p(5, 6, "y")
    # torso: patchwork plates in role colors
    c.r(3, 8, 12, 16, "l"); c.r(3, 8, 3, 16, "w") if False else None
    c.r(3, 8, 7, 11, "1"); c.r(8, 8, 12, 11, "L"); c.r(3, 12, 7, 16, "L"); c.r(8, 12, 12, 16, "2")
    c.r(4, 9, 6, 10, "2") ; c.r(9, 13, 11, 15, "3")
    c.p(3, 8, "w"); c.p(12, 8, "O"); c.p(3, 16, "O")
    for (x, y) in [(4, 9), (11, 9), (4, 15), (11, 15), (7, 12), (8, 12)]:
        c.p(x, y, "y")
    c.line(3, 12, 12, 12, "O")
    c.r(7, 8, 8, 8, "4") if False else None
    c.r(6, 13, 9, 14, "O"); c.p(7, 13, "4"); c.p(8, 13, "4"); c.p(7, 14, "5"); c.p(8, 14, "5")
    # arms: mismatched
    c.r(0, 8, 2, 9, "1"); c.r(0, 10, 1, 17, "l"); c.r(1, 10, 1, 17, "L") ; c.r(0, 18, 2, 19, "L")
    c.r(13, 8, 15, 9, "L"); c.r(14, 10, 15, 14, "2"); c.r(13, 10, 13, 14, "l")
    c.r(12, 15, 15, 17, "L") ; c.p(15, 18, "L") ; c.p(12, 15, "w")
    # thin teetering legs
    c.r(5, 17, 6, 20, "L"); c.r(9, 17, 10, 21, "l"); c.r(4, 21, 7, 21, "L"); c.r(8, 21, 12, 21, "L")
    c.p(5, 20, "y") ; c.p(10, 19, "y")
    c.shadow(0, 15)
    return c.out()



def crab3b():
    c = C()
    # legs: 3 per side, pointed
    for (y0, x1, y1) in ((13, 0, 12), (15, 0, 17), (17, 1, 21)):
        c.line(5, y0, x1, y1, "5", mirror=True)
        c.line(5, y0 + 1, x1 + 1, y1, "6", mirror=True)
        c.m(x1, y1, "4")
    # shell
    c.ell(7.5, 14, 5.5, 4.2, "2"); c.ell(7.5, 13, 4.5, 2.8, "1")
    c.r(4, 17, 11, 18, "3"); c.r(6, 15, 9, 15, "3")
    # eye stalks (moss tipped)
    c.mr(5, 9, 5, 11, "w"); c.mr(5, 8, 5, 8, "g"); c.m(6, 8, "G"); c.m(5, 7, "h")
    # huge C pincer left, opening upward, 2px gap
    c.r(0, 0, 1, 4, "4"); c.r(4, 0, 5, 4, "4")
    c.r(0, 5, 5, 8, "4"); c.r(0, 0, 0, 8, "5"); c.r(5, 0, 5, 8, "6"); c.r(0, 8, 5, 8, "6")
    c.p(2, 4, "6"); c.p(3, 4, "6"); c.p(1, 6, "w"); c.p(1, 2, "w")
    c.r(4, 9, 6, 11, "2"); c.r(6, 10, 7, 11, "1")
    c.r(3, 9, 4, 9, "2")
    # small pincer right
    c.r(13, 8, 14, 10, "4"); c.p(15, 8, "4") if False else None
    c.r(12, 10, 15, 11, "4"); c.r(12, 7, 12, 9, "4"); c.r(15, 7, 15, 9, "5"); c.r(12, 11, 15, 11, "6")
    c.p(13, 8, "x") if False else None
    c.r(9, 12, 11, 12, "2")
    c.shadow(0, 15)
    return c.out()


def eel3b():
    c = C()
    xs = lambda y: 8 + 3 * math.sin((y - 4) / 3.2)
    for y in range(5, 23):
        x = round(xs(y)); w = 1 if y > 18 else 2 if y > 15 else 2
        c.r(x - w, y, x + w, y, "2"); c.p(x - w, y, "1"); c.p(x + w, y, "3")
        c.p(x + w + 1, y, "5" if y % 2 else "4")      # fin ridge
        if y % 4 == 0:
            c.p(x + w + 2, y, "6")
    # head
    hx = round(xs(4))
    c.r(hx - 3, 1, hx + 3, 5, "1"); c.r(hx - 2, 0, hx + 2, 0, "1")
    c.r(hx - 3, 4, hx + 3, 5, "2"); c.p(hx + 3, 1, "3"); c.r(hx + 3, 2, hx + 3, 5, "3")
    c.p(hx - 2, 2, "w"); c.p(hx - 2, 2, "O"); c.p(hx - 2, 1, "w")
    c.p(hx + 1, 2, "O"); c.p(hx + 1, 1, "w")
    c.r(hx - 1, 4, hx + 1, 5, "O"); c.p(hx - 1, 4, "w"); c.p(hx + 1, 4, "w")
    # barbels and sparks (accent)
    c.line(hx - 3, 2, hx - 6, 0, "6"); c.p(hx - 7, 0, "4") if hx - 7 >= 0 else None
    for (x, y) in [(1, 8), (14, 3), (2, 15), (14, 12), (13, 20)]:
        c.p(x, y, "4")
    c.shadow(3, 12, 23)
    return c.out()


def ape3b():
    c = C()
    # big shoulder mass
    c.ell(7.5, 10, 7.5, 4.8, "2"); c.r(1, 10, 14, 14, "2")
    c.r(2, 6, 6, 9, "1"); c.r(9, 12, 13, 14, "3"); c.r(2, 13, 13, 14, "3")
    # small head low between shoulders
    c.r(5, 5, 10, 9, "3"); c.r(6, 4, 9, 4, "3"); c.r(6, 5, 9, 5, "l")
    c.r(6, 6, 9, 8, "2"); c.p(6, 6, "w"); c.p(9, 6, "w"); c.p(7, 6, "O"); c.p(8, 6, "O")
    c.r(7, 8, 8, 8, "O")
    c.m(4, 7, "4"); c.m(3, 7, "5"); c.m(4, 8, "5")   # cheek pads
    # torso/belly
    c.r(5, 12, 10, 16, "3"); c.r(6, 11, 9, 12, "1")
    # long arms, chrome lower parts
    c.r(0, 8, 3, 13, "2"); c.r(12, 8, 15, 13, "3"); c.r(0, 8, 1, 10, "1")
    c.r(0, 13, 2, 19, "l"); c.r(13, 13, 15, 19, "L"); c.r(1, 14, 1, 18, "w"); c.r(14, 14, 14, 18, "l")
    c.r(0, 13, 3, 13, "L"); c.r(12, 13, 15, 13, "O")
    c.p(2, 16, "4"); c.p(13, 16, "4")
    c.r(0, 19, 3, 21, "2"); c.r(12, 19, 15, 21, "3"); c.r(0, 21, 3, 21, "3")
    # legs
    c.r(4, 16, 6, 21, "3"); c.r(9, 16, 11, 21, "3"); c.r(4, 21, 7, 21, "2"); c.r(8, 21, 11, 21, "2")
    c.shadow(0, 15)
    return c.out()


def hermit3b():
    c = C()
    # spiral shell on the back (detail), facing left
    c.ell(10, 9, 5.5, 7, "5")
    c.ell(10, 8.5, 4.5, 5.8, "4")
    c.ell(10, 9, 3, 4.3, "5"); c.ell(10, 9.5, 1.8, 2.6, "4"); c.p(10, 9, "6"); c.p(11, 9, "6"); c.p(11, 10, "6")
    c.p(8, 4, "w"); c.p(7, 6, "w")
    c.r(6, 13, 14, 16, "6"); c.r(7, 14, 13, 14, "5")
    c.line(7, 3, 8, 2, "6") if False else None
    c.line(5, 9, 6, 13, "6")
    # crab body poking out front-left
    c.r(1, 14, 7, 18, "2"); c.r(1, 14, 5, 15, "1"); c.r(5, 17, 7, 18, "3")
    c.p(2, 12, "2"); c.p(2, 13, "2"); c.p(5, 12, "2"); c.p(5, 13, "2")
    c.p(2, 11, "w"); c.p(5, 11, "w"); c.p(2, 12, "O"); c.p(5, 12, "O")
    c.r(2, 16, 4, 16, "O")
    # claws raised
    c.r(0, 9, 1, 13, "1") if False else None
    c.r(0, 15, 0, 19, "1"); c.r(0, 18, 1, 20, "1"); c.p(1, 17, "1")
    c.r(7, 18, 8, 18, "2")
    # legs
    for x in (3, 5, 7, 9):
        c.line(x, 18, x - 1 if x < 6 else x + 1, 22, "3")
    c.r(1, 19, 1, 20, "1") if False else None
    c.p(9, 17, "3")
    c.shadow(0, 14)
    return c.out()


def basilisk3b():
    c = C()
    # long low lizard, head left, tail right curling down
    # tail
    c.r(11, 12, 15, 13, "2"); c.r(13, 14, 15, 15, "3"); c.r(14, 16, 15, 18, "3"); c.p(15, 19, "3")
    # body
    c.r(4, 10, 12, 16, "2"); c.r(4, 10, 12, 11, "1"); c.r(4, 15, 12, 16, "3")
    for x in (5, 7, 9, 11):
        c.p(x, 10, "1"); c.p(x, 9, "3")                 # spine plates
    # belly bands/cracks (detail)
    c.line(6, 12, 8, 15, "4"); c.line(8, 15, 11, 13, "4"); c.p(10, 12, "5"); c.p(5, 14, "5")
    # head
    c.r(0, 8, 5, 13, "2"); c.r(0, 8, 5, 9, "1"); c.r(0, 12, 4, 13, "3")
    c.r(1, 6, 1, 7, "1"); c.r(3, 5, 3, 7, "1"); c.r(5, 6, 5, 7, "1"); c.p(3, 4, "1")  # crest
    c.p(2, 9, "3"); c.p(3, 9, "3"); c.p(4, 9, "3")           # brow
    c.p(2, 10, "y"); c.p(3, 10, "y"); c.p(3, 10, "R"); c.p(2, 10, "y")
    c.p(3, 11, "O") if False else None
    c.p(0, 11, "O"); c.p(0, 12, "w"); c.p(2, 13, "w")
    # four splayed legs with claws
    c.r(2, 15, 4, 16, "3"); c.r(0, 17, 3, 18, "2"); c.r(0, 19, 1, 19, "w"); c.p(3, 19, "w")
    c.r(10, 16, 13, 17, "3"); c.r(12, 18, 15, 19, "2") ; c.p(14, 20, "w"); c.p(12, 20, "w") if False else None
    c.r(5, 17, 6, 20, "3") if False else None
    c.r(3, 9, 4, 7, "1") if False else None
    c.r(6, 17, 8, 19, "3"); c.r(5, 20, 7, 20, "2"); c.p(5, 21, "w"); c.p(7, 21, "w")
    c.r(9, 7, 11, 9, "2") if False else None
    c.shadow(0, 15)
    return c.out()


OVERRIDES = {"kit3b": {
    "worm3b": worm3b(), "crab3b": crab3b(), "fish3b": fish3b(), "fly3b": fly3b(),
    "cyclops3b": cyclops3b(), "basilisk3b": basilisk3b(), "dacca3b": dacca3b(),
    "flamingo3b": flamingo3b(), "catapult3b": catapult3b(), "cupola3b": cupola3b(),
    "slynth3b": slynth3b(), "sitter3b": sitter3b(), "wren3b": wren3b(), "snail3b": snail3b(),
    "eater3b": eater3b(), "eel3b": eel3b(), "jelly3b": jelly3b(), "hermit3b": hermit3b(),
    "anemone3b": anemone3b(), "lamprey3b": lamprey3b(), "pyramid3b": pyramid3b(),
    "ape3b": ape3b(), "crungle3b": crungle3b(), "chromeling3b": chromeling3b(),
}}
