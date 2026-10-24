"""B3 family redraw: reptiles (low, long, splayed legs, tails). Crocs, newts, lizards, drakes, tortoises."""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from style_b3 import C  # noqa: E402
from b3_wilds import tube  # noqa: E402

HUMANOID = set()

KEYS = {
    "creatures/sw/croc": "croc",
    "creatures/sw/sultan/croc": "sultan_croc",
    "creatures/sw/salamander": "salamander",
    "creatures/sw/chameleon": "chameleon",
    "creatures/sw/basilisk": "basilisk",
    "creatures/rimewyk": "rimewyk",
    "creatures/sw/dawnglider": "dawnglider",
    "creatures/sw/golem/dawnglider": "golem_dawnglider",
    "creatures/sw/tortoise": "tortoise",
    "creatures/chiliad-tortoise": "tortoise",
    "creatures/sw/golem/tortoise": "golem_tortoise",
    "creatures/sw/cherub/tortoise": "cherub_tortoise",
    "creatures/sw/cherub/tortoise/mechanical": "cherub_tortoise_mechanical",
}


def leg(c, x0, y0, x1, y1, ch="2", claw="w"):
    c.line(x0, y0, x1, y1, ch)
    c.p(x1, y1, claw)


def legs4(c, fx, rx, cy, up, dn, ch="2", sh="3", claw="w", reach=2):
    """splayed legs: front pair at fx, rear pair at rx; elbows out then down."""
    for x, d in ((fx, -1), (rx, 1)):
        c.line(x, cy - up + 2, x + d * 1, cy - up, ch)
        c.line(x + d * 1, cy - up, x + d * (1 + reach), cy - up, ch)
        c.p(x + d * (1 + reach), cy - up, claw)
        c.p(x + d * (2 + reach), cy - up + 1, claw) if False else None
        c.line(x, cy + dn - 2, x + d * 1, cy + dn, sh)
        c.line(x + d * 1, cy + dn, x + d * (1 + reach), cy + dn, sh)
        c.p(x + d * (1 + reach), cy + dn, claw)


# ------------------------------------------------------------------ crocodilians
def poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            ins = False
            j = n - 1
            for i in range(n):
                xi, yi = pts[i]; xj, yj = pts[j]
                if (yi > y) != (yj > y) and x < (xj - xi) * (y - yi) / (yj - yi) + xi:
                    ins = not ins
                j = i
            if ins:
                c.p(x, y, ch)


def croc_body(c, big):
    """diagonal crocodilian: head lower-left, tail rising to the upper right."""
    if not big:
        tube(c, [(10, 14), (13, 12), (15, 9)], 2.2, 0.5, "2")
        tube(c, [(5, 16), (10, 14)], 3.3, 3.3, "2")
        tube(c, [(5, 18), (10, 16)], 1.3, 1.3, "1")
        tube(c, [(6, 13), (10, 11)], 0.9, 0.9, "3") if False else None
    else:
        tube(c, [(10, 13), (13, 11), (15, 8)], 3.4, 0.6, "2")
        tube(c, [(5, 15), (10, 13)], 4.6, 4.6, "2")
        tube(c, [(5, 18), (10, 16)], 1.8, 1.8, "1")


def croc():
    c = C()
    croc_body(c, False)
    # splayed legs with claws
    for x0, y0, x1, y1 in [(6, 13, 4, 11), (11, 12, 13, 14), (7, 19, 5, 21), (11, 18, 13, 20)]:
        leg(c, x0, y0, x1, y1, "3")
    c.p(3, 11, "w"); c.p(4, 10, "w"); c.p(14, 14, "w"); c.p(4, 21, "w"); c.p(5, 22, "w"); c.p(14, 20, "w"); c.p(13, 21, "w")
    # long snout with jaw line and teeth
    c.r(0, 16, 6, 17, "2"); c.r(1, 15, 5, 15, "2"); c.r(1, 19, 5, 19, "1")
    c.r(0, 18, 6, 18, "O")
    for x in (1, 3, 5):
        c.p(x, 18, "w")
    c.p(0, 17, "3"); c.p(0, 19, "3") if False else None
    c.r(5, 14, 6, 15, "1"); c.p(6, 15, "O"); c.p(5, 14, "w")
    # one row of dorsal scutes along the spine
    for x, y in [(7, 15), (9, 14), (11, 13), (13, 11)]:
        c.p(x, y, "4"); c.p(x, y + 1, "5")
    c.shadow(0, 15, 22)
    c.shadow(2, 13, 21)
    return c.out()


def sultan_croc():
    c = C()
    croc_body(c, True)
    for x0, y0, x1, y1 in [(6, 11, 3, 9), (12, 10, 14, 12), (6, 20, 4, 22), (12, 19, 14, 21)]:
        c.line(x0, y0, x1, y1, "3"); c.line(x0 + 1, y0, x1 + 1, y1, "3")
    for x, y in [(2, 9), (3, 8), (4, 9), (15, 12), (14, 13), (3, 22), (4, 23), (5, 22), (15, 21), (14, 22)]:
        c.p(x, y, "w")
    # heavy head: stone brow, pick teeth
    c.r(0, 15, 7, 17, "2"); c.r(1, 14, 6, 14, "2"); c.r(1, 19, 6, 20, "1")
    c.r(0, 18, 7, 18, "O"); c.r(0, 15, 7, 15, "3") if False else None
    for x in (1, 3, 5, 7):
        c.p(x, 18, "w"); c.p(x, 17, "w")
    for x in (2, 4, 6):
        c.p(x, 19, "w")
    c.r(6, 12, 8, 14, "1"); c.p(7, 13, "O"); c.p(6, 12, "w"); c.p(8, 14, "3")
    # big bony back plates in one row
    for x, y in [(8, 15), (10, 13), (12, 11), (14, 9)]:
        c.r(x, y, x + 1, y + 1, "4"); c.p(x, y + 2, "6"); c.p(x + 1, y + 2, "6")
    c.p(7, 16, "5"); c.p(5, 20, "3") if False else None
    c.shadow(0, 15, 23)
    return c.out()


def salamander():
    c = C()
    c.r(2, 22, 13, 22, "x")
    # long slender body in an S
    tube(c, [(4, 13), (7, 15), (10, 16), (12, 18), (14, 21)], 1.9, 0.6, "2")
    tube(c, [(4, 14), (7, 16), (10, 17), (12, 19)], 0.8, 0.5, "1")
    # legs
    leg(c, 5, 13, 3, 11, "2"); c.p(2, 11, "y"); c.p(2, 10, "y")
    leg(c, 5, 16, 3, 19, "3"); c.p(2, 19, "y")
    leg(c, 10, 15, 12, 12, "2"); c.p(13, 12, "y"); c.p(13, 11, "y")
    leg(c, 10, 18, 9, 20, "3"); c.p(9, 21, "y")
    # head, small and wide
    c.ell(2, 14, 2.3, 1.9, "2")
    c.r(0, 14, 1, 15, "2")
    c.p(1, 13, "O"); c.p(1, 12, "w") if False else None
    c.p(0, 15, "O")
    # spots
    for x, y, ch in [(5, 13, "4"), (7, 14, "y"), (8, 15, "r"), (10, 16, "4"), (4, 15, "r"), (6, 16, "y"),
                     (11, 17, "y"), (12, 19, "r"), (13, 20, "4"), (3, 13, "y"), (9, 17, "r")]:
        c.p(x, y, ch)
    c.shadow(0, 14, 22)
    return c.out()


# ------------------------------------------------------------------ lizards






def rimewyk():
    c = C()
    tube(c, [(11, 15), (13, 17), (15, 17)], 2.0, 0.6, "2")
    tube(c, [(11, 14), (13, 16), (15, 16)], 1.0, 0.4, "3")
    leg(c, 5, 12, 3, 10, "3"); c.p(2, 10, "w")
    leg(c, 11, 12, 13, 10, "3"); c.p(14, 10, "w")
    leg(c, 5, 18, 3, 20, "3"); c.p(2, 20, "w")
    leg(c, 11, 18, 13, 20, "3"); c.p(14, 20, "w")
    c.ell(8, 15, 5.3, 3.2, "2")
    c.ell(8, 17, 4.6, 1.3, "1")
    # frost-marbled belly stripe
    c.r(6, 16, 8, 16, "w"); c.r(10, 17, 11, 17, "w")
    # spiky dorsal crest
    for x in range(4, 14, 2):
        c.p(x, 11, "4"); c.p(x, 12, "5") if False else None
        c.p(x + 1, 12, "5"); c.p(x, 12, "4")
    # head profile
    c.r(1, 13, 5, 16, "2"); c.r(0, 14, 1, 16, "2"); c.r(1, 13, 4, 13, "1")
    c.r(0, 16, 4, 16, "1")
    c.p(0, 15, "O"); c.p(1, 15, "O"); c.p(3, 14, "O"); c.p(4, 14, "w")
    c.p(1, 14, "4")
    # dewlap under jaw
    c.r(1, 17, 5, 18, "4"); c.r(2, 19, 4, 19, "5"); c.p(3, 20, "5")
    c.p(2, 18, "w"); c.p(4, 18, "w"); c.p(3, 19, "w")
    c.shadow(0, 15, 22)
    c.shadow(2, 13, 21)
    return c.out()


# ------------------------------------------------------------------ drake
def dawnglider(golem=False):
    c = C()
    wing = "3" if golem else "4"
    wing2 = "2" if golem else "5"
    vein = "4" if golem else "6"
    # far wing (darker) and near wing, leathery
    poly(c, [(8, 13), (4, 3), (9, 2), (11, 8)], wing2)
    poly(c, [(9, 14), (10, 5), (15, 3), (15, 11), (13, 14)], wing)
    c.line(9, 13, 10, 5, vein); c.line(10, 13, 15, 4, vein); c.line(8, 12, 5, 4, vein)
    # simple S-body: head, neck, belly curve, curling tail
    tube(c, [(5, 11), (6, 13), (9, 15), (11, 17), (9, 19), (5, 20), (3, 18)], 1.8, 0.5, "2")
    tube(c, [(6, 12), (8, 14), (10, 16)], 0.6, 0.6, "1")
    if golem:
        c.line(6, 13, 9, 15, "4"); c.line(10, 17, 8, 19, "4"); c.p(5, 20, "4")
    else:
        for x, y in [(7, 13), (9, 15), (10, 17), (8, 19), (5, 20)]:
            c.p(x, y, "4")
    # small drake head with eye, horn and ember puff
    c.r(3, 9, 6, 11, "2"); c.r(1, 10, 3, 11, "2"); c.r(1, 11, 3, 11, "1")
    c.p(5, 9, "O"); c.p(4, 9, "w") if False else None
    c.p(6, 8, wing); c.p(7, 7, wing)
    c.p(1, 12, "w") if False else None
    c.p(0, 10, "y"); c.p(0, 11, "r"); c.p(0, 9, "r")
    # legs tucked
    c.p(7, 16, "3"); c.p(8, 17, "w")
    c.shadow(4, 11, 22)
    c.shadow(4, 11, 23)
    return c.out()


# ------------------------------------------------------------------ tortoises
def tort(kind="plain"):
    c = C()
    shell, sh_l, sh_d = "2", "1", "3"
    if kind == "mech":
        shell, sh_l, sh_d = "l", "w", "L"
    skin = "s" if False else "2"
    if kind == "mech":
        skin = "L"
    # tail
    c.r(14, 17, 15, 18, skin)
    # legs: four stubby
    c.r(3, 17, 5, 20, skin if kind != "plain" else "3"); c.r(3, 20, 5, 20, "w" if kind == "plain" else sh_l)
    c.r(11, 17, 13, 20, "3" if kind != "mech" else "L"); c.r(11, 20, 13, 20, "w" if kind == "plain" else sh_l)
    c.r(6, 18, 7, 20, "3" if kind != "mech" else "L")
    c.r(9, 18, 10, 20, "3" if kind != "mech" else "L")
    # head
    c.r(0, 14, 4, 17, skin); c.r(0, 15, 0, 16, skin)
    c.r(0, 17, 3, 17, "3" if kind != "mech" else "L")
    c.r(1, 13, 3, 13, skin)
    c.p(2, 14, "O"); c.p(3, 14, "w") if kind == "plain" else None
    c.p(0, 16, "O")
    if kind == "mech":
        c.p(2, 14, "c"); c.p(3, 14, "c")
    # dome shell
    c.ell(9, 13, 6.2, 5.0, sh_d)
    c.ell(8.5, 12.4, 5.6, 4.3, shell)
    c.ell(8, 11, 3.6, 2.4, sh_l)
    # plates
    pl = "4"
    pm = "5"
    if kind == "mech":
        pl, pm = "L", "L"
    c.r(7, 10, 9, 12, pl); c.r(8, 11, 8, 11, pm)
    for x, y in [(4, 11), (12, 11), (6, 14), (10, 14), (3, 13), (14, 13), (8, 15), (5, 9), (11, 9)]:
        c.p(x, y, pm); c.p(x + 1, y, pm) if kind == "plain" else None
    c.line(5, 12, 7, 11, sh_d); c.line(11, 12, 9, 11, sh_d); c.line(8, 13, 8, 15, sh_d)
    if kind == "mech":
        for x, y in [(5, 10), (11, 10), (4, 14), (13, 14), (8, 8)]:
            c.p(x, y, "c")
    return c.out()


def tortoise():
    c = C()
    g = tort("plain")
    return g


def cherub_tortoise():
    g = tort("plain")
    c = C()
    c.g = [list(r) for r in g]
    c.r(5, 2, 10, 2, "y"); c.r(5, 4, 10, 4, "y"); c.p(4, 3, "y"); c.p(11, 3, "y")
    c.r(6, 3, 9, 3, ".")
    c.p(10, 14, "y"); c.p(6, 10, "w") if False else None
    c.p(3, 14, "y")
    # serene closed eye
    c.p(2, 14, "O")
    return c.out()


def cherub_tortoise_mechanical():
    g = tort("mech")
    c = C()
    c.g = [list(r) for r in g]
    c.r(5, 2, 10, 2, "y"); c.r(5, 4, 10, 4, "y"); c.p(4, 3, "y"); c.p(11, 3, "y")
    return c.out()


def golem_tortoise():
    g = tort("plain")
    c = C()
    c.g = [list(r) for r in g]
    # clay seams and glowing glass arteries
    for x, y in [(8, 9), (8, 10), (7, 12), (9, 12), (6, 13), (10, 13)]:
        c.p(x, y, "4")
    c.line(8, 13, 8, 15, "4")
    c.line(5, 13, 3, 13, "4"); c.line(11, 13, 14, 13, "4")
    c.p(2, 14, "4"); c.p(1, 15, "O")
    c.r(3, 19, 5, 19, "O"); c.r(11, 19, 13, 19, "O")
    c.p(4, 18, "4"); c.p(12, 18, "4")
    for yy in range(24):
        for xx in range(16):
            if c.g[yy][xx] == "5":
                c.g[yy][xx] = "3"
    return c.out()


def chameleon():
    c = C()
    # branch with a twig
    c.r(0, 19, 15, 19, "n"); c.r(0, 20, 15, 20, "N"); c.p(12, 18, "n"); c.p(13, 17, "n"); c.p(13, 16, "g"); c.p(14, 16, "g")
    # big curled tail
    tube(c, [(11, 14), (14, 14), (14, 17), (12, 17), (12, 15)], 1.1, 0.6, "2")
    c.p(13, 14, "1"); c.p(13, 15, "3"); c.p(13, 16, "3")
    # body: tall compressed oval
    c.ell(8, 14, 4.6, 3.4, "2")
    c.ell(8, 16, 3.6, 1.3, "1")
    c.r(5, 10, 11, 10, "3"); c.r(4, 11, 12, 11, "3")
    for x, y, ch in [(5, 12, "4"), (7, 12, "5"), (9, 12, "4"), (11, 13, "5"), (6, 14, "5"), (8, 14, "4"), (10, 15, "4"), (7, 16, "5")]:
        c.p(x, y, ch)
    # gripping feet
    c.r(5, 16, 6, 18, "3"); c.r(4, 18, 7, 18, "3"); c.p(4, 19, "3") if False else None
    c.r(10, 16, 11, 18, "3"); c.r(9, 18, 12, 18, "3")
    # head: low, long snout; casque rising behind; bone horn
    c.r(0, 13, 5, 15, "2"); c.r(1, 12, 5, 12, "2"); c.r(0, 15, 4, 15, "1")
    c.r(3, 9, 6, 11, "1"); c.r(4, 8, 6, 8, "1"); c.p(6, 9, "3"); c.p(6, 10, "3"); c.p(5, 8, "4")
    c.r(3, 12, 5, 12, "3")
    c.line(1, 12, 0, 8, "w"); c.p(1, 11, "w"); c.p(1, 10, "L") if False else None
    c.p(3, 13, "3"); c.p(3, 11, "2"); c.p(4, 11, "2")
    c.p(3, 12, "w"); c.p(4, 12, "O") ; c.p(3, 12, "O"); c.p(4, 11, "w")
    c.r(0, 14, 2, 14, "O")
    c.shadow(0, 15, 22)
    c.shadow(2, 13, 21)
    return c.out()


def basilisk():
    c = C()
    # stone tail, stiff and straight
    tube(c, [(11, 16), (13, 17), (15, 19)], 2.0, 0.6, "2")
    c.p(13, 16, "O"); c.p(14, 18, "O")
    # stiff splayed legs, blocky
    c.r(4, 11, 5, 13, "3"); c.r(2, 10, 4, 11, "3"); c.p(1, 10, "w"); c.p(2, 9, "w")
    c.r(11, 11, 12, 13, "3"); c.r(12, 10, 14, 11, "3"); c.p(15, 10, "w"); c.p(14, 9, "w")
    c.r(4, 18, 5, 20, "3"); c.r(2, 20, 5, 21, "3"); c.p(1, 21, "w"); c.p(2, 22, "w")
    c.r(11, 18, 12, 20, "3"); c.r(11, 20, 14, 21, "3"); c.p(15, 21, "w"); c.p(14, 22, "w")
    # flat slab body of cracked stone
    c.r(5, 12, 12, 19, "2"); c.r(4, 13, 13, 18, "2")
    c.r(5, 12, 12, 13, "1"); c.r(5, 19, 12, 19, "3"); c.r(12, 14, 13, 18, "3")
    for x, y in [(6, 14), (9, 14), (6, 17), (10, 17)]:
        c.r(x, y, x + 1, y + 1, "4")
    c.p(7, 15, "5"); c.p(10, 15, "5"); c.p(7, 18, "5") if False else None
    c.line(8, 12, 8, 16, "O"); c.line(8, 16, 11, 19, "O"); c.p(5, 18, "O")
    # heavy head: brow slab over a glaring eye, grim jaw
    c.r(0, 13, 6, 18, "2"); c.r(0, 13, 6, 13, "3"); c.r(0, 18, 6, 18, "3")
    c.r(0, 14, 6, 14, "1"); c.r(2, 15, 5, 15, "3")
    c.p(3, 16, "r"); c.p(4, 16, "O"); c.p(2, 16, "O")
    c.r(0, 17, 1, 17, "O"); c.p(2, 18, "w"); c.p(4, 18, "w")
    c.p(1, 15, "O")
    c.r(2, 12, 5, 12, "3")
    # a few falling dust motes beside the head
    for x, y in [(0, 20), (2, 21)]:
        c.p(x, y, "e")
    c.shadow(0, 15, 22)
    c.shadow(2, 13, 21)
    return c.out()


SPRITES = {
    "croc": croc(),
    "sultan_croc": sultan_croc(),
    "salamander": salamander(),
    "chameleon": chameleon(),
    "basilisk": basilisk(),
    "rimewyk": rimewyk(),
    "dawnglider": dawnglider(),
    "golem_dawnglider": dawnglider(True),
    "tortoise": tortoise(),
    "golem_tortoise": golem_tortoise(),
    "cherub_tortoise": cherub_tortoise(),
    "cherub_tortoise_mechanical": cherub_tortoise_mechanical(),
}
