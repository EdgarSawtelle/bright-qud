"""B3 remaining creatures, batch 2."""
import os
import sys
from functools import partial

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import b3kit as K  # noqa: E402
from b3kit import (C, back, overlay, person, hood, hat_pointy, halo, goggles_up, staff, club as kclub,
                   scroll, lantern, scarf, blindfold, tunic, book, _grip)  # noqa: E402
from b3_people import (goat_head, goat_legs, bare_chest, braid_satchel, orchids, wide_sleeves, pipes,
                       dervish_skirt, arms_out, pointed_turban, moss_fur, hang_pouches)  # noqa: E402
from b3_castes import robot_head, shell  # noqa: E402
from b3more_keys import MORE_KEYS  # noqa: E402

KEYS = MORE_KEYS[2]
P = person


def tube(c, pts, r0, r1, ch):
    d = [0.0]
    for (a, b), (e, f) in zip(pts, pts[1:]):
        d.append(d[-1] + ((e - a) ** 2 + (f - b) ** 2) ** 0.5)
    tot = d[-1] or 1
    n = int(tot * 2) + 1
    for i in range(n + 1):
        t = i / n * tot
        k = 1
        while k < len(d) - 1 and d[k] < t:
            k += 1
        u = (t - d[k - 1]) / ((d[k] - d[k - 1]) or 1)
        x = pts[k - 1][0] + (pts[k][0] - pts[k - 1][0]) * u
        y = pts[k - 1][1] + (pts[k][1] - pts[k - 1][1]) * u
        r = r0 + (r1 - r0) * t / tot
        c.ell(x, y, r, r, ch)


def fin(c, x0=1, x1=14):
    c.shadow(x0, x1)
    return c.out()


# =============================================================== humanoid parts
def ape_body(c, f="2", hi="1", dk="3"):
    """squatting ape: broad furry torso, long knuckle arms, bowed short legs."""
    c.r(3, 16, 12, 21, ".")
    c.r(3, 9, 12, 9, f)
    c.r(4, 10, 11, 15, f)
    c.r(2, 10, 3, 17, f)
    c.r(12, 10, 13, 17, dk)
    c.r(4, 10, 6, 12, hi)
    c.r(7, 11, 8, 13, "S")           # bare chest
    c.p(7, 11, "s")
    c.r(3, 16, 12, 18, f)
    c.r(3, 16, 5, 17, hi)
    c.r(10, 16, 12, 18, dk)
    c.r(2, 18, 3, 18, "S"); c.r(12, 18, 13, 18, "S")      # knuckles
    c.r(2, 19, 3, 19, "S"); c.r(12, 19, 13, 19, "S")
    c.r(3, 19, 5, 21, dk); c.r(10, 19, 12, 21, dk)
    c.r(3, 22, 6, 22, "O"); c.r(9, 22, 12, 22, "O")
    c.shadow(1, 14)


def ape_head(c, f="2", dk="3", tuft="4", tuft2="5"):
    c.r(5, 2, 10, 3, dk)            # brow ridge fur
    c.r(5, 4, 10, 4, dk)
    c.r(6, 3, 9, 3, f)
    c.r(5, 5, 10, 7, "s")
    c.r(5, 5, 5, 7, f); c.r(10, 5, 10, 7, dk)
    c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "S")
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.r(6, 7, 9, 7, "S"); c.p(7, 7, "O"); c.p(8, 7, "O")
    c.p(7, 7, "S"); c.p(8, 7, "S")
    # colored cheek tufts
    c.mr(3, 5, 4, 5, tuft); c.mr(2, 6, 4, 6, tuft); c.mr(3, 7, 4, 7, tuft2); c.mr(4, 8, 5, 8, tuft2)
    c.mr(2, 4, 2, 4, tuft2)
    c.r(7, 8, 8, 8, "S")


@back
def cherub_wings(c, a="4", b="5", d="6"):
    for sgn_x in (0, 1):
        pass
    c.line(4, 10, 0, 4, a, mirror=True)
    c.line(4, 11, 0, 6, a, mirror=True)
    c.line(4, 12, 0, 8, b, mirror=True)
    c.mr(0, 4, 3, 4, a)
    c.mr(1, 5, 3, 7, b)
    c.mr(1, 8, 3, 9, a)
    c.mr(2, 10, 3, 11, d)
    c.m(0, 3, d)
    c.mr(1, 5, 1, 5, a)
    c.mr(3, 6, 3, 8, d)


def cherub_robe(c):
    """small chrome cherub: shiny panels on the robe and little gem on chest."""
    c.r(7, 11, 8, 12, "4"); c.p(7, 11, "w")
    c.r(5, 17, 10, 17, "l") if False else None
    c.r(4, 20, 11, 20, "l")
    c.r(3, 21, 12, 21, "L")


def ape_machine_head(c):
    """chrome ape skull: heavy brow, muzzle plate, round ears, cyan eyes."""
    c.r(5, 3, 10, 7, "l")
    c.r(5, 3, 10, 3, "w")
    c.r(10, 4, 10, 7, "L")
    c.r(5, 4, 10, 4, "L")
    c.p(6, 5, "c"); c.p(9, 5, "c")
    c.r(6, 6, 9, 7, "w")
    c.r(10, 6, 10, 7, "L")
    c.p(7, 6, "O"); c.p(8, 6, "O"); c.r(6, 7, 9, 7, "l"); c.r(7, 7, 8, 7, "O")
    c.mr(3, 4, 4, 5, "l"); c.mr(3, 5, 3, 5, "L"); c.mr(3, 4, 3, 4, "w")
    c.r(7, 8, 8, 8, "L")


def stranger_machine_head(c):
    """smooth chrome mask-face with a glowing slit, tall domed crown."""
    c.r(6, 2, 9, 2, "w")
    c.r(5, 3, 10, 7, "l")
    c.r(5, 3, 10, 3, "w")
    c.r(10, 3, 10, 7, "L")
    c.r(6, 5, 9, 5, "O"); c.r(6, 5, 9, 5, "O")
    c.p(6, 5, "c"); c.p(7, 5, "c"); c.p(8, 5, "c"); c.p(9, 5, "c")
    c.p(7, 7, "L"); c.p(8, 7, "L")
    c.r(7, 6, 8, 6, "w")
    c.r(6, 7, 6, 7, "l")
    c.r(7, 8, 8, 8, "L")


def spindle_arms(c, f="2"):
    """thin dervish limbs raised: one arm up, one out."""
    c.r(4, 10, 4, 15, ".")
    c.r(11, 10, 11, 15, ".")
    c.line(5, 10, 1, 6, f); c.line(5, 11, 1, 7, "1")
    c.p(0, 5, "s"); c.p(1, 5, "s")
    c.line(10, 10, 14, 13, f); c.line(10, 11, 14, 14, "3")
    c.p(15, 13, "S"); c.p(15, 14, "S")


def eye_crown(c, a="4", b="5"):
    """sightless-way crown: tall spiral spire with an eye-pattern band."""
    c.r(5, 3, 10, 3, a)
    c.r(6, 2, 9, 2, b)
    c.r(7, 1, 8, 1, a); c.p(7, 0, b); c.p(8, 0, a)
    c.p(6, 3, "O"); c.p(9, 3, "O"); c.p(7, 3, "w"); c.p(8, 3, "w")
    c.p(6, 5, a); c.p(9, 5, a)
    c.p(5, 5, b); c.p(10, 5, b)
    c.p(6, 4, "S"); c.p(9, 4, "S")


def spiral_irises(c):
    c.p(6, 5, "4"); c.p(9, 5, "4"); c.p(6, 6, "5"); c.p(9, 6, "5")
    c.p(5, 5, "5"); c.p(10, 5, "5")


def bloated_belly(c, a="2", b="1", d="3"):
    c.r(3, 16, 12, 21, ".")
    c.ell(7.5, 15.5, 6, 4.2, a)
    c.ell(6.5, 14.5, 3.5, 2.5, b)
    c.r(10, 13, 12, 18, d)
    c.ell(7.5, 19, 4.5, 2.2, d)
    c.r(5, 15, 6, 15, "5") if False else None
    for (x, y) in ((6, 15), (9, 17), (5, 18), (8, 13)):
        c.p(x, y, "h")
    c.p(7, 16, "5"); c.p(8, 16, "6")
    c.r(5, 20, 6, 21, d); c.r(9, 20, 10, 21, d)
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.shadow(2, 13)


def folded_limbs(c):
    c.r(4, 10, 4, 15, ".")
    c.r(11, 10, 11, 15, ".")
    c.r(3, 10, 4, 12, "2"); c.r(11, 10, 12, 12, "3")
    c.r(3, 13, 5, 14, "3"); c.r(10, 13, 12, 14, "3")
    c.p(5, 14, "s") ; c.p(10, 14, "S")
    c.r(5, 12, 6, 13, "1") if False else None


def stitches(c, pts, ch="O"):
    for (x, y) in pts:
        c.p(x, y, ch)


def golem_scars(c):
    # patch of mismatched hide + stitches over the chest and thigh
    c.r(6, 11, 9, 13, "5")
    c.r(6, 11, 9, 11, "4")
    for x in (6, 7, 8, 9):
        c.p(x, 14 if False else 11, "O") if x % 2 else None
    c.p(6, 12, "O"); c.p(9, 12, "O"); c.p(6, 13, "O") if False else None
    c.line(7, 10, 8, 14, "O") if False else None
    c.p(7, 13, "O"); c.p(8, 13, "O") if False else None
    # head seam
    c.p(8, 4, "O"); c.p(8, 3, "O") if False else None
    c.p(5, 6, "O")
    c.p(11, 11, "O"); c.p(12, 11, "O") if False else None
    c.p(4, 16, "O"); c.p(6, 17, "O") if False else None
    c.p(10, 17, "O"); c.p(11, 18, "O") if False else None
    c.p(5, 12, "4") if False else None


def jester_cap(c, a="2", b="5", bell="y"):
    """archway cap: two curling points ending in bells."""
    c.r(5, 3, 10, 3, a)
    c.r(5, 2, 7, 2, a); c.r(8, 2, 10, 2, b)
    c.line(5, 2, 2, 0, a); c.line(6, 2, 3, 0, a)
    c.line(10, 2, 13, 0, b); c.line(9, 2, 12, 0, b)
    c.p(1, 0, bell); c.p(1, 1, bell); c.p(14, 0, bell); c.p(14, 1, bell)
    c.p(1, 2, "O") if False else None
    c.p(7, 3, bell); c.p(8, 3, bell)
    c.p(6, 1, a); c.p(9, 1, b)
    c.p(4, 3, bell) if False else None


def motley(c):
    """thousand-year motley: diamond harlequin patches and a ruff."""
    for y in range(10, 22):
        for x in range(3, 13):
            if c.g[y][x] in "123":
                if ((x + y) // 2) % 2 == 0:
                    c.g[y][x] = {"1": "4", "2": "5", "3": "6"}[c.g[y][x]]
    c.r(5, 9, 10, 9, "w")
    c.p(5, 9, "y"); c.p(10, 9, "y")
    c.p(7, 9, "y")
    c.p(3, 21, "y") ; c.p(12, 21, "y")
    c.p(3, 20, "y") if False else None


def mitre(c, a="2", gold="y"):
    """tall machine mitre: stacked cog crown."""
    c.r(5, 3, 10, 3, a)
    c.r(5, 2, 10, 2, gold)
    c.r(6, 0, 9, 1, gold)
    c.p(6, 0, "."); c.p(9, 0, ".")
    c.p(7, 0, "w") ; c.p(8, 0, "4")
    c.p(7, 1, "O"); c.p(8, 1, "O")
    c.p(7, 2, "4"); c.p(8, 2, "4")
    c.p(4, 2, gold); c.p(11, 2, gold) ; c.p(4, 3, gold); c.p(11, 3, gold)
    c.p(5, 1, gold); c.p(10, 1, gold)


def regalia(c):
    """long machinic mantle: gold pipes down the chest, gear at the heart."""
    c.r(5, 9, 10, 10, "y")
    c.p(7, 9, "w")
    c.r(7, 11, 8, 12, "l")
    c.p(7, 11, "y"); c.p(8, 12, "y"); c.p(8, 11, "O") if False else None; c.p(7, 12, "O")
    c.line(6, 13, 6, 21, "y"); c.line(9, 13, 9, 21, "y")
    c.r(6, 21, 9, 21, "y")
    c.r(3, 21, 12, 21, "y") if False else None
    c.mr(3, 17, 3, 21, "5")


def gear_staff(c):
    staff(c, head="none")
    c.r(12, 1, 14, 3, "l")
    c.p(13, 2, "O"); c.p(13, 0, "y"); c.p(11, 2, "y"); c.p(15, 2, "y"); c.p(13, 4, "y")
    c.p(12, 1, "y"); c.p(14, 1, "y"); c.p(12, 3, "y"); c.p(14, 3, "y")


def sap_mask(c, a="4", b="5"):
    """spiral minyan mask: eyes peer out of a roped root spiral."""
    c.r(5, 3, 10, 3, "2")
    c.r(5, 4, 10, 4, a)
    c.r(5, 5, 10, 5, b)
    c.p(6, 5, "c"); c.p(9, 5, "c"); c.p(7, 5, a); c.p(8, 5, a)
    c.r(5, 6, 10, 7, a)
    c.p(7, 6, b); c.p(8, 7, b); c.p(6, 7, b); c.p(9, 6, b)
    c.p(7, 4, b); c.p(8, 4, b) if False else None


def root_pack(c):
    """spiral-root rolled across the back, small sprig."""
    c.r(12, 8, 14, 14, "n")
    c.r(13, 8, 14, 14, "N")
    c.r(11, 15, 15, 17, "n") if False else None
    c.p(12, 8, "g"); c.p(13, 7, "G")
    c.p(12, 11, "N")


def metronome_staff(c):
    """metronome pyramid on a pole, red bio-clock pendulum."""
    c.line(13, 8, 13, 21, "l")
    c.r(12, 4, 14, 8, "L")
    c.r(11, 7, 15, 8, "L")
    c.line(13, 2, 13, 7, "R")
    c.p(13, 1, "R"); c.p(12, 3, "w") if False else None
    c.p(13, 8, "w"); c.p(12, 7, "w")
    c.p(11, 3, "4") if False else None
    _grip(c)


def wheel_chest(c):
    """ragwheel over the chest, wire tendons."""
    c.ell(7.5, 12.5, 2.2, 2.2, "L")
    c.p(7, 12, "w"); c.p(8, 12, "w"); c.p(7, 11, "R"); c.p(8, 13, "R")
    c.p(7, 12, "R")
    for (x, y) in ((4, 11), (4, 13), (11, 11), (11, 13), (4, 14), (11, 14)):
        c.p(x, y, "R")
    c.line(6, 15, 5, 20, "R"); c.line(9, 15, 10, 20, "R")


def psy_goggles(c):
    c.r(5, 5, 10, 5, "L")
    c.r(6, 4, 6, 6, "L") if False else None
    c.p(6, 5, "R"); c.p(9, 5, "R")
    c.p(6, 4, "l"); c.p(9, 4, "l")
    c.p(7, 3, "R"); c.p(8, 3, "R")
    c.p(5, 3, "l"); c.p(10, 3, "l")
    c.r(6, 3, 9, 3, "l")
    c.p(7, 3, "R"); c.p(8, 3, "R")


def flower_veil(c, a="5", b="4", leaf="g", leaf2="G"):
    """flower crown that streams over the shoulder as a sideways veil."""
    c.r(5, 2, 10, 3, leaf)
    c.p(5, 2, "."); c.p(10, 2, ".")
    for x, ch in ((5, a), (7, b), (9, a)):
        c.p(x, 2, ch); c.p(x, 1, b) if x != 7 else c.p(x, 1, a)
    c.p(8, 3, b); c.p(6, 3, a)
    c.r(4, 3, 4, 8, leaf2); c.r(3, 5, 3, 10, leaf)
    c.r(2, 7, 2, 12, leaf2)
    for (x, y, ch) in ((4, 4, a), (3, 7, b), (2, 10, a), (3, 12, b), (4, 8, b)):
        c.p(x, y, ch)
    c.r(1, 12, 1, 13, leaf2)
    c.p(10, 4, leaf2)


def stem_fingers(c):
    c.p(11, 15, "g"); c.p(12, 15, "G"); c.p(12, 14, "g") if False else None
    c.p(13, 14, "g") if False else None


def cathode(c):
    """glinting glass cathode tube."""
    c.r(12, 9, 14, 16, "b")
    c.r(12, 9, 12, 16, "B")
    c.r(13, 10, 13, 15, "c")
    c.p(13, 12, "w"); c.p(13, 11, "w")
    c.r(12, 8, 14, 8, "L"); c.r(12, 17, 14, 17, "L")
    c.p(13, 7, "4")
    c.p(11, 14, "s"); c.p(11, 15, "g"); c.p(12, 15, "g") if False else None
    c.p(11, 16, "g") if False else None


def snap_head(c, f="2", mane="3", hi="1"):
    """hyena profile, long toothy snout pointing left, tall pointed ears, spiky mane."""
    c.r(5, 3, 10, 8, ".")
    # skull + snout
    c.r(5, 3, 9, 6, f)
    c.r(2, 5, 6, 7, f)
    c.r(1, 6, 4, 7, hi)
    c.r(5, 3, 8, 3, hi)
    c.p(0, 6, "O"); c.p(1, 5, "O")
    # jaw with teeth
    c.r(1, 8, 5, 8, "3")
    c.p(2, 8, "w"); c.p(4, 8, "w"); c.p(1, 7, "w"); c.p(3, 7, "w")
    c.p(2, 8, "w")
    c.p(7, 4, "4"); c.p(6, 4, "O")   # eye
    c.p(6, 4, "y")
    c.p(5, 4, "O")
    # ears
    c.r(7, 1, 8, 2, f); c.p(7, 0, f); c.r(9, 1, 10, 3, mane); c.p(10, 0, mane); c.p(9, 0, mane)
    c.p(8, 1, "S")
    # mane spikes
    c.r(9, 4, 11, 8, mane)
    c.p(11, 3, mane); c.p(12, 5, mane); c.p(12, 7, mane); c.p(10, 9, mane)
    c.r(6, 7, 9, 8, f)
    c.r(6, 8, 9, 8, mane)


def snap_body(c, f="2", dk="3", hi="1"):
    """lean hunched body, spiked pauldron, fur kilt."""
    c.r(3, 16, 12, 21, ".")
    c.r(4, 9, 11, 9, f)
    c.r(5, 10, 10, 15, f)
    c.r(5, 10, 6, 13, hi)
    c.r(9, 10, 10, 15, dk)
    c.r(4, 10, 4, 14, f); c.r(11, 10, 11, 14, dk)
    c.p(4, 15, "s"); c.p(11, 15, "S")
    c.r(3, 8, 5, 9, "4"); c.p(3, 7, "4"); c.p(4, 7, "6")   # spike pauldron
    c.p(3, 8, "6"); c.p(2, 8, "4") if False else None
    c.r(9, 8, 11, 9, "5"); c.p(11, 7, "4"); c.p(12, 8, "4")
    c.r(5, 14, 10, 14, "5"); c.r(5, 14, 10, 14, "5")
    c.r(4, 16, 11, 17, f); c.r(4, 16, 11, 16, hi) if False else None
    c.r(10, 16, 11, 17, dk)
    c.r(5, 18, 6, 21, dk); c.r(9, 18, 10, 21, dk)
    c.p(4, 18, f) if False else None
    c.r(4, 22, 6, 22, "O"); c.r(9, 22, 11, 22, "O")


def stick(c):
    c.line(13, 3, 13, 21, "n")
    c.r(12, 3, 14, 5, "N")
    c.p(13, 2, "l"); c.p(11, 4, "l") if False else None
    c.p(12, 3, "l"); c.p(14, 5, "l")
    _grip(c)


def scrap_coat(c):
    """heavy coat of scrap plates draped to the knees."""
    c.r(3, 9, 12, 9, "l")
    c.r(4, 10, 11, 15, "2")
    c.r(3, 16, 12, 21, "2")
    for (x0, y0, x1, y1, ch) in ((3, 9, 6, 11, "l"), (9, 9, 12, 11, "L"), (4, 13, 7, 15, "l"),
                                 (8, 14, 11, 16, "L"), (3, 17, 6, 19, "L"), (9, 18, 12, 20, "l"),
                                 (6, 19, 8, 21, "1")):
        c.r(x0, y0, x1, y1, ch)
        c.p(x0, y0, "w")
    c.p(5, 10, "O"); c.p(10, 10, "O"); c.p(5, 14, "O"); c.p(10, 15, "O"); c.p(4, 18, "O"); c.p(11, 19, "O")
    c.r(3, 21, 12, 21, "3")
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")


def beast_mask(c):
    """horned beast mask over the whole face: snout, fangs, glass eyes."""
    c.r(5, 2, 10, 7, "l")
    c.r(5, 2, 10, 2, "w")
    c.r(10, 3, 10, 7, "L")
    c.p(6, 4, "4"); c.p(9, 4, "4"); c.p(6, 5, "O"); c.p(9, 5, "O")
    c.r(6, 6, 9, 7, "L")
    c.p(7, 6, "O"); c.p(8, 6, "O"); c.p(6, 7, "w"); c.p(9, 7, "w")
    c.line(5, 2, 3, 0, "w"); c.line(10, 2, 12, 0, "w")
    c.p(3, 1, "w"); c.p(12, 1, "w")
    c.p(4, 3, "L"); c.p(11, 3, "L"); c.p(4, 4, "L"); c.p(11, 4, "L")


def wheel_fiddle(c):
    """hand-cranked wheel-fiddle held across the body."""
    c.r(1, 12, 5, 17, "N")
    c.r(1, 12, 5, 12, "n")
    c.r(2, 13, 4, 16, "n")
    c.ell(3, 14.5, 1.5, 1.5, "w")
    c.p(3, 14, "y"); c.p(3, 15, "O") if False else None
    c.line(5, 13, 5, 9, "N")
    c.r(4, 8, 6, 9, "y") if False else None
    c.p(0, 15, "y") ; c.p(0, 16, "y"); c.p(5, 16, "y")
    c.p(6, 17, "O") if False else None
    c.p(4, 15, "s"); c.p(6, 15, "s") if False else None


H_KIT = {
    "ape": P(ape_body, ape_head, face="none", sash=False),
    "cherub_ape_mechanical": P(cherub_wings, cherub_robe, ape_machine_head, halo, body="l", lite="w", dark="L",
                                face="none", sash=False, trim="4"),
    "cherub_stranger_mechanical": P(cherub_wings, cherub_robe, stranger_machine_head, halo, body="l", lite="w",
                                    dark="L", face="none", sash=False, trim="4"),
    "dervish": P(dervish_skirt, spindle_arms, eye_crown, spiral_irises, face="face", sash=False),
    "glowwight_apotheote": P(hood, bloated_belly, folded_limbs, orchids, face="face", sash=False, trim="4"),
    "golem_goatfolk": P(goat_legs, bare_chest, goat_head, braid_satchel, golem_scars, face="none", sash=False),
    "gyre_fool": P(jester_cap, motley, face="face", sash=False),
    "mechanimist_archpriest": P(pipes, wide_sleeves, regalia, mitre, gear_staff, book, face="face", sash=False,
                                trim="4"),
    "naphtaali_sap": P(moss_fur, root_pack, sap_mask, face="none", sash=False, trim="4"),
    "psyber": P(wheel_chest, psy_goggles, metronome_staff, face="mask", sash=False, trim="4"),
    "slynth_ezra": P(flower_veil, cathode, stem_fingers, face="face", skin=("g", "G"), sash=False, trim="4"),
    "snapjaw": P(snap_body, snap_head, stick, face="none", sash=False),
    "une": P(scrap_coat, beast_mask, wheel_fiddle, face="none", sash=False),
}
HUMANOID = set(H_KIT)
SPRITES = {name: kit for name, kit in H_KIT.items()}


# =============================================================== creatures (free-form)
def agolzvuv():
    c = C()
    # wings glued to the sides as a second skin (detail colour, wet sheen)
    c.ell(3.2, 13, 2.6, 6.5, "5"); c.ell(12.8, 13, 2.6, 6.5, "6")
    c.line(3, 8, 3, 18, "4"); c.line(12, 8, 12, 18, "5")
    c.line(2, 10, 4, 16, "6") if False else None
    # legs
    for (x0, y0, x1, y1) in ((5, 12, 1, 15), (5, 14, 1, 19), (6, 16, 3, 21)):
        c.line(x0, y0, x1, y1, "3", mirror=True)
    # abdomen
    c.ell(7.5, 16, 3.3, 4.8, "2"); c.ell(6.8, 15, 1.8, 3, "1")
    for y in (14, 17, 20):
        c.r(5, y, 10, y, "3")
    # thorax
    c.ell(7.5, 10, 3.4, 2.6, "2"); c.ell(6.8, 9.5, 1.8, 1.4, "1")
    # head with big compound eyes
    c.ell(7.5, 5.5, 2.6, 2.2, "2")
    c.mr(4, 4, 6, 6, "O"); c.m(5, 4, "R"); c.m(5, 5, "r")
    c.r(7, 7, 8, 7, "3")
    # pus-moist barbed mitten forelegs, raised
    for sx in (0, 1):
        pass
    c.line(5, 9, 2, 5, "3", mirror=True)
    c.mr(1, 2, 3, 5, "2")
    c.mr(0, 1, 1, 3, "y")
    c.m(0, 1, "w"); c.m(2, 1, "y"); c.m(0, 4, "y")
    c.m(3, 3, "y")
    return fin(c)


def biographer_bot():
    c = C()
    # thin pinion legs
    c.line(6, 17, 5, 21, "L"); c.line(9, 17, 10, 21, "L")
    c.r(4, 22, 6, 22, "O"); c.r(9, 22, 11, 22, "O")
    c.r(4, 21, 6, 21, "l"); c.r(9, 21, 11, 21, "l")
    # cloth-like metal tunic, furrowed
    c.r(4, 10, 11, 17, "2")
    c.r(3, 15, 12, 18, "2")
    c.r(4, 10, 6, 17, "1"); c.r(10, 10, 11, 17, "3"); c.r(10, 15, 12, 18, "3")
    for x in (6, 8, 9):
        c.r(x, 12, x, 17, "3")
    c.r(7, 11, 7, 16, "1")
    c.r(3, 18, 12, 18, "3")
    c.r(5, 10, 10, 10, "w")
    # belt / sash detail
    c.r(4, 13, 11, 13, "5"); c.p(7, 13, "4")
    # pinion arms: thin, long, holding a book + quill
    c.line(4, 10, 2, 15, "L"); c.line(11, 10, 13, 14, "L")
    c.p(3, 10, "l"); c.p(12, 10, "l")
    c.r(0, 14, 3, 17, "N"); c.r(1, 14, 3, 16, "w"); c.r(0, 17, 3, 17, "n")
    c.p(2, 15, "O"); c.p(1, 15, "O")
    c.line(13, 14, 14, 6, "w"); c.p(14, 5, "4"); c.p(15, 4, "4"); c.p(13, 13, "l")
    # large cask head
    c.r(4, 1, 11, 9, "l")
    c.r(5, 0, 10, 0, "L")
    c.r(4, 1, 5, 9, "w"); c.r(10, 1, 11, 9, "L")
    c.r(4, 3, 11, 3, "L"); c.r(4, 7, 11, 7, "L")     # barrel hoops
    c.r(4, 4, 11, 4, "l") if False else None
    c.r(6, 4, 9, 6, "O"); c.r(6, 5, 9, 5, "4"); c.p(6, 5, "w")
    c.r(7, 9, 8, 9, "L")
    c.p(7, 10, "L"); c.p(8, 10, "L")
    return fin(c)


def _cherub_extras(c, wing_col="w", yoff=0):
    c.r(5, 0, 10, 0, "4") if False else None


def _halo(c, cx=7.5, y=0):
    c.r(5, y, 10, y, "4")
    c.p(4, y + 1, "4"); c.p(11, y + 1, "4")
    c.r(6, y + 1, 9, y + 1, ".")
    c.p(5, y + 1, "5"); c.p(10, y + 1, "5")


def _wings_small(c, x0, y0, flip=False):
    pass


def cherub_arachnid():
    c = C()
    for (x0, y0, x1, y1, x2, y2) in ((6, 14, 2, 13, 0, 19), (6, 15, 3, 17, 1, 22), (6, 16, 4, 19, 3, 22),
                                     (6, 13, 3, 10, 0, 13)):
        c.line(x0, y0, x1, y1, "3", mirror=True); c.line(x1, y1, x2, y2, "2", mirror=True)
    c.ell(7.5, 17, 3.6, 3.6, "2"); c.ell(6.8, 16, 2, 1.8, "1"); c.r(7, 19, 8, 20, "3")
    c.p(7, 17, "O"); c.p(8, 18, "O")
    c.ell(7.5, 12, 2.4, 2, "1"); c.ell(7.5, 10, 2.1, 1.7, "2")
    c.m(6, 9, "O"); c.m(5, 10, "O")
    c.ell(3.2, 14, 1.8, 2.8, "w"); c.ell(11.8, 14, 1.8, 2.8, "w")
    c.p(3, 14, "L"); c.p(12, 14, "L")
    _halo(c, y=4)
    return fin(c)


def cherub_cat():
    c = C()
    # tail curling up
    tube(c, [(13, 14), (15, 11), (14, 7)], 0.9, 0.7, "2")
    # body
    c.ell(9, 15, 5.5, 3.2, "2"); c.ell(8.5, 13.7, 4, 1.4, "1")
    c.r(11, 15, 14, 17, "3") if False else None
    for x in (5, 7, 11, 13):
        c.r(x, 17, x + 1, 20, "2" if x < 9 else "3"); c.r(x, 21, x + 1, 21, "w")
    # little feathered wings
    c.line(8, 13, 4, 8, "w"); c.line(10, 13, 9, 7, "w")
    c.line(9, 13, 6, 8, "w") if False else None
    c.ell(7, 10.5, 3, 3, "w"); c.line(6, 8, 5, 12, "L") ; c.line(8, 8, 8, 12, "L") if False else None
    c.p(7, 12, "L") if False else None
    c.line(6, 9, 6, 12, "L"); c.line(8, 9, 8, 12, "L")
    # head with ears
    c.ell(3.5, 13, 3, 2.7, "1")
    c.p(1, 10, "1"); c.p(2, 10, "2"); c.p(1, 11, "1"); c.p(5, 10, "2"); c.p(5, 11, "2"); c.p(6, 10, "3") if False else None
    c.p(2, 12, "O"); c.p(5, 12, "O"); c.p(3, 14, "R"); c.p(3, 13, "3") if False else None
    c.p(1, 14, "w"); c.p(5, 14, "w")
    # halo
    c.r(1, 6, 5, 6, "4"); c.p(0, 7, "4"); c.p(6, 7, "4"); c.r(1, 7, 5, 7, ".")
    c.p(1, 7, "5"); c.p(5, 7, "5")
    c.r(2, 7, 4, 7, ".")
    return fin(c, 0, 15)


def cherub_fish():
    c = C()
    # fish with tail on right, little wings top, halo
    c.ell(7, 14, 6, 3.4, "2"); c.ell(6.5, 12.7, 4.8, 1.4, "1")
    c.ell(7, 16, 4.5, 1.2, "3")
    c.r(11, 11, 15, 17, "2") if False else None
    c.line(12, 14, 15, 10, "2"); c.line(12, 14, 15, 18, "2"); c.line(12, 14, 15, 14, "1")
    c.line(13, 12, 15, 10, "1") if False else None
    c.p(15, 11, "1"); c.p(15, 17, "3"); c.p(15, 13, "1"); c.p(15, 15, "2")
    # wing feathers
    c.line(7, 12, 3, 5, "w"); c.line(8, 12, 7, 4, "w"); c.line(7, 12, 5, 4, "w") if False else None
    c.ell(5.5, 7.5, 2.4, 3.2, "w"); c.line(5, 5, 5, 9, "L") if False else None
    c.line(5, 6, 5, 10, "L")
    c.line(7, 12, 11, 5, "w") if False else None
    c.ell(9.5, 8, 2, 3.4, "w"); c.line(9, 6, 9, 10, "L")
    c.p(2, 13, "O"); c.p(3, 13, "O") if False else None
    c.p(3, 13, "w")
    c.p(1, 15, "O"); c.p(0, 15, "L") if False else None
    c.r(0, 15, 1, 15, "3")
    for x in (7, 8):
        c.p(x, 15, "3"); c.p(x, 13, "3") if False else None
    c.p(11, 13, "3"); c.p(11, 16, "3")
    # halo
    c.r(3, 1, 8, 1, "4"); c.p(2, 2, "4"); c.p(9, 2, "4"); c.r(3, 2, 8, 2, ".")
    c.p(3, 2, "5"); c.p(8, 2, "5")
    c.r(4, 2, 7, 2, ".")
    return fin(c, 0, 15)


def cherub_grazing():
    c = C()
    # antelope-like prey: slender legs, tiny horns, wings, halo
    tube(c, [(13, 11), (15, 13)], 0.8, 0.8, "5")
    c.ell(9, 13, 5, 3, "2"); c.ell(8.5, 12, 3.8, 1.3, "1")
    c.r(12, 14, 14, 15, "3")
    for x in (5, 7, 11, 13):
        c.r(x, 15, x, 20, "2" if x < 9 else "3")
        c.r(x, 21, x, 21, "O")
    # neck/head to the left
    c.line(4, 12, 2, 8, "2"); c.line(5, 12, 3, 8, "2"); c.line(5, 11, 3, 8, "1") if False else None
    c.ell(2.5, 9, 2.2, 1.8, "1")
    c.r(0, 9, 1, 10, "1"); c.p(0, 10, "O"); c.p(2, 8, "O")
    c.line(3, 7, 2, 4, "5"); c.line(4, 7, 4, 4, "5"); c.p(2, 3, "4"); c.p(4, 3, "4")
    # wings
    c.line(9, 12, 6, 6, "w"); c.line(10, 12, 12, 5, "w"); c.line(8, 12, 9, 5, "w")
    c.ell(9, 8.5, 3.8, 3.8, "w"); c.line(7, 6, 8, 12, "L") ; c.line(11, 6, 10, 12, "L")
    c.p(9, 6, "L"); c.p(9, 7, "L") if False else None
    c.r(6, 0, 11, 0, "4"); c.p(5, 1, "4"); c.p(12, 1, "4"); c.p(6, 1, "5"); c.p(11, 1, "5")
    c.r(6, 1, 11, 1, ".") if False else None
    c.p(5, 1, "4"); c.p(12, 1, "4")
    return fin(c, 0, 15)


def cherub_ooze():
    c = C()
    c.ell(7.5, 16.5, 6.8, 4.8, "3")
    c.ell(7.5, 16, 6, 4, "2")
    c.ell(6.5, 14.5, 3.5, 2, "1")
    c.r(1, 19, 14, 20, "3")
    c.p(3, 20, "2"); c.p(12, 21, "3") if False else None
    # bubbles + eyes
    c.r(5, 15, 6, 17, "O"); c.r(9, 15, 10, 17, "O"); c.p(5, 15, "w"); c.p(9, 15, "w")
    c.r(7, 18, 8, 18, "O")
    c.p(2, 17, "w"); c.p(13, 15, "1"); c.p(11, 13, "w")
    # small wings
    c.line(2, 14, 0, 9, "w"); c.line(13, 14, 15, 9, "w"); c.line(3, 14, 1, 11, "w") if False else None
    c.ell(2, 11.5, 1.8, 3, "w"); c.ell(13, 11.5, 1.8, 3, "w")
    c.p(2, 11, "L"); c.p(13, 11, "L")
    # halo
    c.r(4, 5, 11, 5, "4"); c.p(3, 6, "4"); c.p(12, 6, "4"); c.p(3, 7, "5") if False else None
    c.p(4, 6, "5"); c.p(11, 6, "5"); c.p(4, 7, "5") if False else None
    c.p(7, 11, "2") if False else None
    c.r(5, 11, 10, 11, "2") if False else None
    return fin(c, 0, 15)


def cherub_succulent():
    c = C()
    # fractal cactus rosette, wings, halo
    c.r(5, 18, 10, 21, "N") if False else None
    c.r(4, 20, 11, 21, "3")
    c.r(5, 8, 10, 20, "2"); c.r(5, 8, 6, 20, "1"); c.r(9, 9, 10, 20, "3")
    c.line(7, 9, 7, 20, "3"); c.line(8, 9, 8, 20, "3") if False else None
    c.r(2, 12, 4, 14, "2"); c.r(2, 9, 3, 12, "2"); c.r(2, 9, 2, 12, "1")
    c.r(11, 13, 13, 15, "3"); c.r(12, 10, 13, 13, "2"); c.r(13, 10, 13, 13, "3")
    c.p(12, 10, "1")
    # spines
    for (x, y) in ((4, 10), (4, 16), (11, 11), (11, 18), (6, 8), (9, 8), (1, 10), (14, 11), (3, 8), (12, 8)):
        c.p(x, y, "w")
    # face + flower
    c.p(6, 13, "O"); c.p(9, 13, "O"); c.r(7, 15, 8, 15, "O")
    c.p(7, 7, "4"); c.p(8, 7, "5") if False else None
    # wings
    c.line(5, 16, 0, 15, "w"); c.line(5, 17, 0, 18, "w"); c.p(1, 16, "w"); c.p(1, 17, "w")
    c.line(10, 16, 15, 15, "w") if False else None
    c.r(0, 16, 1, 17, "w")
    c.line(10, 18, 15, 18, "w"); c.r(14, 17, 15, 18, "w")
    # halo
    c.r(5, 1, 10, 1, "4"); c.p(4, 2, "4"); c.p(11, 2, "4"); c.p(5, 2, "5"); c.p(10, 2, "5")
    c.r(6, 2, 9, 2, ".")
    c.p(7, 5, "4"); c.p(8, 5, "4"); c.p(7, 4, "5") ; c.p(8, 4, "5") if False else None
    c.r(7, 6, 8, 6, "5") if False else None
    return fin(c)


def cherub_urchin():
    c = C()
    c.ell(7.5, 15, 4.6, 4.6, "2"); c.ell(6.5, 13.5, 2.6, 2.2, "1")
    c.ell(8.5, 17, 2.8, 2, "3")
    # spines all round
    import math
    for k in range(14):
        a = k * math.pi * 2 / 14
        x0, y0 = 7.5 + math.cos(a) * 4.5, 15 + math.sin(a) * 4.5
        x1, y1 = 7.5 + math.cos(a) * 7.2, 15 + math.sin(a) * 6.4
        c.line(round(x0), round(y0), round(x1), round(y1), "w")
    c.p(6, 14, "O"); c.p(9, 14, "O"); c.r(7, 16, 8, 16, "O")
    # wings
    c.line(5, 11, 1, 6, "w"); c.line(10, 11, 14, 6, "w"); c.r(0, 4, 2, 7, "w"); c.r(13, 4, 15, 7, "w")
    c.p(1, 5, "L"); c.p(14, 5, "L")
    # halo
    c.r(5, 0, 10, 0, "4"); c.p(4, 1, "4"); c.p(11, 1, "4"); c.p(5, 1, "5"); c.p(10, 1, "5")
    c.r(6, 1, 9, 1, ".")
    c.r(7, 8, 8, 9, "5") if False else None
    return fin(c)


def chromeling_special():
    c = C()
    # little chrome humanoid under an oversized dissymmetric ruffled scrap coat
    c.r(5, 17, 6, 21, "L"); c.r(9, 17, 10, 21, "L")
    c.r(4, 22, 6, 22, "O"); c.r(9, 22, 11, 22, "O"); c.r(4, 21, 6, 21, "l"); c.r(9, 21, 11, 21, "l")
    # head
    c.r(5, 4, 10, 9, "l"); c.r(5, 4, 10, 4, "w"); c.r(10, 5, 10, 9, "L")
    c.r(6, 6, 9, 7, "O"); c.p(6, 6, "4"); c.p(9, 6, "4"); c.p(6, 7, "4") if False else None
    c.r(7, 9, 8, 9, "L")
    c.p(7, 2, "L"); c.p(7, 3, "L"); c.p(7, 1, "4"); c.p(8, 3, "L") if False else None
    # coat: left side long and jagged, right side short
    c.r(2, 10, 10, 15, "2")
    c.r(1, 12, 7, 20, "2")
    c.r(9, 11, 14, 17, "3")
    c.r(2, 10, 5, 12, "1"); c.r(1, 13, 3, 20, "1")
    c.r(13, 13, 15, 15, "3") if False else None
    # ruffles: scrap plates
    for (x, y, w) in ((0, 14, 2), (0, 17, 2), (1, 20, 3), (4, 21, 3), (13, 15, 2), (12, 17, 2), (10, 18, 2)):
        c.r(x, y, x + w, y, "l"); c.p(x + w, y, "L")
    c.r(1, 21, 3, 21, "L") if False else None
    for (x, y) in ((3, 12), (5, 14), (3, 17), (6, 19), (11, 13), (12, 15)):
        c.p(x, y, "4")
    for (x, y) in ((2, 11), (11, 12), (7, 16)):
        c.p(x, y, "O")
    c.line(8, 10, 8, 20, "3") if False else None
    c.r(9, 10, 12, 10, "3")
    # dissymmetric collar spikes
    c.p(3, 9, "l"); c.p(2, 9, "w"); c.p(13, 10, "l"); c.p(12, 9, "L")
    return fin(c, 0, 15)


def decarbonizer():
    c = C()
    # splayed chrome legs
    c.line(6, 15, 2, 21, "L"); c.line(9, 15, 13, 21, "L"); c.line(7, 16, 7, 21, "l"); c.line(8, 16, 8, 21, "L")
    c.r(1, 21, 4, 21, "l"); c.r(11, 21, 14, 21, "l"); c.r(6, 21, 9, 21, "l")
    # chrome chassis (sphere) with elliptical cavity
    c.ell(7.5, 9, 6.6, 6.6, "L"); c.ell(7.5, 9, 6, 6, "l"); c.ell(6.5, 7, 3.5, 3, "w")
    c.ell(7.5, 9.5, 4.8, 3.4, "O")
    # molecular orrery: nucleus + orbit + particles
    c.ell(7.5, 9.5, 3.8, 2.4, "L") if False else None
    c.p(7, 9, "c"); c.p(8, 9, "c"); c.p(7, 10, "w"); c.p(8, 10, "c")
    for (x, y, ch) in ((4, 8, "R"), (11, 11, "R"), (6, 11, "4"), (10, 7, "4"), (4, 10, "4"), (11, 9, "R"),
                       (8, 7, "R")):
        c.p(x, y, ch)
    c.line(4, 9, 6, 7, "L") if False else None
    # engine vent + red hazard
    c.r(5, 15, 10, 15, "R"); c.r(6, 14, 9, 14, "L")
    c.p(7, 15, "w") if False else None
    c.r(6, 15, 9, 15, "R"); c.p(7, 15, "r"); c.p(8, 15, "r") if False else None
    # intake snout
    c.r(0, 8, 2, 11, "L"); c.r(0, 8, 1, 8, "l"); c.r(0, 9, 1, 10, "O")
    c.p(2, 10, "R") if False else None
    c.p(14, 4, "R"); c.p(15, 3, "R")
    return fin(c, 0, 15)


def feral_lah():
    c = C()
    # stem + leaves
    c.line(7, 21, 7, 13, "G"); c.line(8, 21, 8, 13, "g")
    c.line(7, 19, 2, 16, "G"); c.line(8, 17, 13, 15, "g"); c.r(1, 15, 3, 16, "g"); c.r(12, 14, 14, 15, "G")
    # petals: wide sheets fanning out
    c.ell(3, 7, 3, 4, "2"); c.ell(12, 7, 3, 4, "3")
    c.ell(7.5, 3.8, 3.4, 3.6, "1")
    c.ell(4.5, 11, 3.6, 2.8, "2"); c.ell(11, 11, 3.6, 2.8, "3")
    c.ell(7.5, 12, 2.6, 2.4, "2")
    # petal veins
    c.line(3, 4, 4, 11, "R"); c.line(12, 4, 11, 11, "R") ; c.line(7, 1, 7, 7, "4") if False else None
    c.line(7, 1, 7, 6, "R"); c.line(8, 1, 8, 6, "R") if False else None
    c.line(1, 6, 5, 9, "R") if False else None
    # centre + tongue-like stamen
    c.ell(7.5, 8.5, 2.4, 2.4, "4"); c.ell(7.5, 8.5, 1.4, 1.4, "5")
    for (x, y) in ((6, 6), (7, 5), (8, 5), (9, 6), (5, 8), (10, 8), (6, 11), (9, 11)):
        c.p(x, y, "5" if (x + y) % 2 else "R")
    c.p(7, 8, "w"); c.p(8, 9, "y") if False else None
    c.p(7, 8, "y")
    return fin(c)


def girshworm():
    c = C()
    # segmented fat worm, curved; out-sophagus tube stiff and raised
    pts = [(13, 19), (10, 17), (6, 17), (3, 14), (3, 10)]
    tube(c, pts, 2.2, 3.0, "2")
    tube(c, [(13, 18), (10, 16), (6, 16), (3, 13)], 1.0, 1.5, "1")
    # segment rings
    for (x, y) in ((11, 18), (9, 17), (7, 17), (5, 16), (4, 14), (4, 12)):
        c.r(x - 1, y - 1, x - 1, y + 1, "3") if y > 15 else c.r(x - 1, y, x + 1, y, "3")
    # nephridia spots
    for (x, y) in ((10, 20), (8, 19), (6, 19), (4, 17), (2, 13), (4, 11)):
        c.p(x, y, "4"); c.p(x + 1, y, "5") if False else None
    # setae
    for (x, y) in ((12, 21), (10, 21), (8, 20), (6, 20), (5, 19), (1, 15), (1, 12), (6, 15)):
        c.p(x, y, "w")
    # head + stiff out-sophagus tube
    c.ell(3, 8.5, 2.6, 2.6, "2")
    c.r(2, 0, 4, 7, "w"); c.r(2, 0, 2, 7, "l"); c.r(4, 1, 4, 7, "L") if False else None
    c.r(1, 0, 5, 1, "4"); c.p(3, 0, "O"); c.p(0, 1, "5") if False else None
    c.p(2, 3, "L"); c.p(4, 5, "L")
    c.p(2, 9, "O") if False else None
    c.p(1, 9, "O"); c.p(4, 9, "O")
    c.p(3, 10, "O")
    c.r(14, 20, 15, 21, "3")
    return fin(c, 0, 15)


def godhed3_unplanished():
    c = C()
    # hover jets
    c.r(5, 20, 6, 20, "4"); c.r(9, 20, 10, 20, "4"); c.r(7, 21, 8, 21, "5") if False else None
    c.p(5, 21, "5"); c.p(10, 21, "5"); c.p(7, 21, "5"); c.p(8, 21, "5")
    c.r(4, 19, 11, 19, "L")
    # greebled egg
    c.ell(7.5, 11, 6, 8.4, "L"); c.ell(7.5, 11, 5.4, 7.8, "l"); c.ell(6, 8, 2.4, 3.6, "w")
    c.r(4, 14, 11, 14, "L")
    # blank sensory pane (circuited glass, unplanished)
    c.r(5, 6, 10, 11, "O"); c.r(6, 7, 9, 10, "b") if False else None
    c.r(6, 7, 9, 10, "B")
    c.line(6, 8, 8, 8, "c"); c.line(8, 8, 8, 10, "c"); c.p(9, 7, "c"); c.p(6, 10, "c")
    # greebles
    c.p(3, 9, "L"); c.p(12, 8, "L"); c.r(2, 11, 3, 12, "L"); c.r(12, 11, 13, 12, "L")
    c.p(2, 11, "4"); c.p(13, 12, "4")
    c.r(6, 3, 9, 3, "L"); c.p(7, 3, "4"); c.p(8, 3, "w")
    c.p(7, 1, "L"); c.p(7, 2, "L") ; c.p(7, 0, "4")
    # woodsprog bits: bone/ wood mounted on lower half
    c.r(5, 15, 6, 17, "n"); c.r(9, 15, 10, 17, "N"); c.p(5, 17, "w"); c.p(10, 17, "w")
    c.p(7, 16, "4"); c.p(8, 16, "4")
    return fin(c)


def golem_bush():
    c = C()
    # legs
    c.r(4, 19, 5, 21, "3"); c.r(10, 19, 11, 21, "3"); c.r(3, 22, 5, 22, "O"); c.r(10, 22, 12, 22, "O")
    # lumpy bush mass
    for (x, y, rx, ry, ch) in ((7.5, 13, 7, 6.5, "3"), (4, 11, 3.8, 3.6, "2"), (11, 11, 3.8, 3.6, "2"),
                               (7.5, 8, 4.5, 4, "2"), (5, 15, 4, 3.5, "2"), (11, 15, 3.6, 3.5, "3")):
        c.ell(x, y, rx, ry, ch)
    c.ell(5.5, 7, 3, 2.8, "1"); c.ell(3.5, 10.5, 2, 2, "1"); c.ell(9, 6.5, 2, 1.8, "1")
    # leaf highlights
    for (x, y) in ((2, 12), (13, 9), (6, 4), (10, 4), (12, 14), (5, 17)):
        c.p(x, y, "1")
    # face: one huge eye, crooked mouth with stitches
    c.ell(6.5, 10, 2.1, 2.1, "w"); c.p(6, 10, "O"); c.p(7, 10, "O"); c.p(6, 9, "O") if False else None
    c.p(10, 9, "O"); c.p(11, 9, "O"); c.p(10, 8, "w") if False else None
    c.line(5, 14, 11, 15, "O")
    for x in (6, 8, 10):
        c.p(x, 14 if x < 8 else 15, "w"); c.p(x, 15 if x < 8 else 16, "O") if False else None
    # patch + stitches + thorns
    c.r(11, 11, 13, 13, "5"); c.p(11, 12, "O"); c.p(13, 12, "O"); c.p(12, 11, "O") if False else None
    c.p(12, 12, "4")
    for (x, y) in ((2, 8), (7, 3), (14, 12)):
        c.p(x, y, "w")
    c.p(3, 4, "5"); c.p(4, 3, "4"); c.p(3, 3, "5")  # bloom
    return fin(c)


def golem_equine():
    c = C()
    # stitched horse: patchwork hide, exposed rib bones
    c.ell(9, 12, 5.8, 3.6, "2"); c.ell(8.5, 10.5, 4.4, 1.6, "1")
    c.r(3, 11, 6, 13, "2")
    # neck + head left
    c.line(4, 11, 2, 6, "2"); c.line(5, 11, 3, 6, "2"); c.line(6, 10, 4, 6, "2")
    c.r(1, 3, 4, 7, "2"); c.r(0, 6, 2, 9, "1"); c.p(0, 8, "O"); c.p(3, 4, "O"); c.p(3, 5, "y")
    c.p(2, 2, "3"); c.p(3, 2, "3"); c.p(4, 2, "3"); c.p(4, 3, "3")
    # mane of rope
    c.line(5, 4, 6, 10, "3"); c.line(6, 4, 7, 10, "4") if False else None
    # legs
    for x in (4, 6, 11, 13):
        c.r(x, 15, x, 20, "2" if x < 9 else "3")
        c.r(x, 21, x, 21, "O")
    c.r(3, 21, 3, 21, "O") if False else None
    # exposed ribs (bone)
    for x in (7, 9, 11):
        c.p(x, 11, "w"); c.p(x, 12, "w"); c.p(x, 13, "l")
    # patch + stitches
    c.r(9, 9, 11, 10, "5"); c.p(9, 9, "O"); c.p(11, 10, "O")
    c.r(4, 12, 5, 13, "4"); c.p(4, 12, "O"); c.p(5, 13, "O")
    # tail of cord
    tube(c, [(14, 11), (15, 14), (15, 18)], 0.8, 0.6, "3")
    c.p(15, 19, "4")
    # stitch seam along belly
    for x in range(5, 14, 2):
        c.p(x, 15, "O")
    return fin(c, 0, 15)


def golem_hover_robot():
    c = C()
    # jets
    c.r(4, 20, 6, 20, "5"); c.r(9, 20, 11, 20, "5"); c.p(5, 21, "4"); c.p(10, 21, "4")
    # mismatched scrap body
    c.r(3, 9, 12, 19, "2")
    c.r(3, 9, 12, 10, "1"); c.r(10, 11, 12, 19, "3"); c.r(3, 18, 12, 19, "3")
    c.r(4, 11, 7, 14, "l"); c.r(4, 11, 7, 11, "w")
    c.r(8, 12, 11, 16, "5"); c.r(8, 12, 11, 12, "4")
    # stitches + rivets
    for (x, y) in ((7, 12), (7, 14), (8, 17), (10, 17), (4, 16), (6, 16), (3, 12), (12, 14)):
        c.p(x, y, "O")
    # head: mismatched pan
    c.r(5, 3, 10, 8, "L"); c.r(5, 3, 10, 3, "l"); c.r(5, 3, 6, 6, "l")
    c.r(6, 5, 7, 6, "O"); c.p(6, 5, "y"); c.r(9, 5, 9, 5, "y"); c.p(9, 6, "O")
    c.r(6, 7, 9, 7, "O"); c.p(7, 7, "w"); c.p(9, 7, "w")
    c.line(7, 3, 7, 1, "L"); c.p(7, 0, "y")
    # arms: cable dangling
    c.r(1, 10, 2, 16, "L"); c.r(13, 10, 14, 14, "l"); c.r(0, 16, 2, 17, "w"); c.p(14, 15, "w"); c.p(14, 16, "w")
    c.p(1, 12, "O"); c.p(13, 12, "O")
    return fin(c, 0, 15)


def golem_mopango_charioteer():
    c = C()
    # wheeled creature: two big spoked wheels and a chassis with a carapaced driver
    for cx in (3.5, 12):
        c.ell(cx, 17.5, 3.6, 3.6, "n"); c.ell(cx, 17.5, 2.6, 2.6, "N"); c.ell(cx, 17.5, 0.8, 0.8, "w")
        c.line(round(cx), 14, round(cx), 21, "n"); c.line(round(cx - 3), 17, round(cx + 3), 17, "n")
    c.r(2, 21, 14, 21, "O") if False else None
    c.r(0, 21, 15, 22, "x") if False else None
    # axle + cart
    c.r(3, 17, 12, 17, "L")
    c.r(2, 13, 13, 16, "3"); c.r(2, 13, 13, 13, "2"); c.r(2, 14, 4, 16, "2")
    c.r(3, 14, 12, 14, "w") if False else None
    c.p(7, 15, "O") ; c.p(5, 15, "O"); c.p(10, 15, "O") if False else None
    # mopango torso: carapaced body
    c.r(5, 7, 10, 12, "2"); c.r(5, 7, 7, 9, "1"); c.r(9, 8, 10, 12, "3")
    c.r(5, 9, 10, 9, "3") if False else None
    c.mr(4, 8, 4, 8, "5"); c.r(5, 10, 10, 10, "4")
    # head with mandible helmet and glowing eye
    c.r(6, 2, 9, 6, "w"); c.r(6, 2, 9, 2, "w"); c.p(6, 3, "O"); c.p(9, 3, "O"); c.p(6, 4, "y"); c.p(9, 4, "y")
    c.r(7, 5, 8, 6, "O") if False else None
    c.p(7, 6, "O"); c.p(8, 6, "O")
    c.line(5, 2, 3, 0, "w"); c.line(10, 2, 12, 0, "w")
    # reins/arms + whip
    c.line(4, 9, 1, 12, "y"); c.line(11, 9, 14, 5, "y"); c.p(15, 4, "l")
    # stitches
    for (x, y) in ((4, 14), (7, 14), (10, 14), (7, 8), (7, 11)):
        c.p(x, y, "O")
    return fin(c, 0, 15)


def golem_slug():
    c = C()
    tube(c, [(3, 16), (7, 15), (11, 17), (15, 20)], 3.0, 0.8, "2")
    c.ell(8, 14, 4.4, 3.2, "1")
    c.line(5, 13, 12, 18, "1")
    c.r(2, 19, 14, 20, "3")
    # patchwork + stitches
    c.r(8, 13, 11, 16, "5"); c.r(8, 13, 11, 13, "4")
    for (x, y) in ((8, 14), (11, 15), (9, 16), (10, 13)):
        c.p(x, y, "O")
    for x in range(5, 13, 2):
        c.p(x, 17, "O") if x < 8 else None
    c.line(5, 12, 5, 15, "O") if False else None
    c.p(5, 12, "O"); c.p(5, 14, "O"); c.p(6, 15, "O")
    c.ell(3, 16, 2.6, 2.6, "2")
    c.p(0, 17, "O"); c.p(1, 18, "3")
    c.line(3, 14, 2, 9, "2"); c.line(5, 14, 6, 9, "2")
    c.p(2, 8, "y"); c.p(6, 8, "y"); c.p(2, 9, "O"); c.p(6, 9, "O")
    # stray fangs sewn on
    c.p(1, 19, "w"); c.p(3, 19, "w")
    return fin(c, 0, 15)


def golem_tree():
    c = C()
    # root legs
    c.line(5, 17, 2, 21, "3"); c.line(6, 17, 5, 21, "3"); c.line(9, 17, 11, 21, "3"); c.line(10, 17, 14, 21, "3")
    c.r(1, 21, 3, 21, "2"); c.r(13, 21, 15, 21, "2")
    # trunk
    c.r(5, 8, 10, 18, "2"); c.r(5, 8, 7, 18, "1") ; c.r(9, 8, 10, 18, "3")
    c.line(6, 11, 6, 15, "3") if False else None
    # canopy
    for (x, y, rx, ry, ch) in ((7.5, 4, 6.5, 4, "3"), (4, 5, 3.4, 3, "2"), (11, 5, 3.4, 3, "3"), (7.5, 3, 4, 2.5, "2")):
        c.ell(x, y, rx, ry, ch)
    c.ell(5, 3, 2.5, 1.6, "1")
    # branch arms
    c.line(5, 10, 1, 12, "2"); c.line(10, 10, 14, 8, "3"); c.p(0, 13, "2"); c.p(1, 14, "2")
    c.p(14, 7, "2"); c.p(15, 6, "w"); c.p(0, 11, "2")
    # face in trunk
    c.r(6, 11, 6, 12, "O"); c.r(9, 11, 9, 12, "O"); c.p(6, 11, "y"); c.p(9, 11, "y")
    c.r(6, 14, 9, 14, "O"); c.p(7, 14, "w"); c.p(9, 14, "w")
    # patch + stitches
    c.r(7, 16, 9, 18, "5"); c.p(7, 16, "O"); c.p(9, 18, "O")
    c.p(10, 12, "O"); c.p(10, 14, "O"); c.p(5, 15, "O")
    # fruit
    c.p(3, 6, "4"); c.p(12, 4, "4"); c.p(8, 1, "5")
    return fin(c, 0, 15)


def gyrohumor():
    c = C()
    # drifting blob, swirling gyre inside, droplets/dust flung round it
    c.ell(7.5, 14, 6.6, 5.6, "3"); c.ell(7.5, 13.5, 5.8, 4.8, "2"); c.ell(6, 11.5, 3.2, 2.2, "1")
    # spiral
    for (x, y) in ((5, 14), (6, 15), (8, 15), (10, 14), (10, 12), (9, 11), (7, 11), (6, 12), (7, 13), (8, 13)):
        c.p(x, y, "4")
    c.p(8, 14, "w"); c.p(7, 14, "w") if False else None
    # eyes
    c.p(5, 12, "O"); c.p(10, 12, "O")
    # droplets / dust
    for (x, y, ch) in ((2, 8, "1"), (3, 5, "w"), (13, 6, "1"), (12, 9, "w"), (6, 4, "5"), (9, 2, "1"), (1, 12, "5"),
                       (14, 13, "w"), (7, 7, "5")):
        c.p(x, y, ch)
    c.r(2, 4, 3, 4, ".") if False else None
    c.p(9, 3, "w"); c.p(8, 3, "1") if False else None
    c.r(1, 19, 14, 19, "3"); c.p(4, 20, "2"); c.p(11, 20, "2"); c.p(7, 21, "2") if False else None
    c.p(3, 21, "1") if False else None
    return fin(c, 0, 15)


def magmacrab():
    c = C()
    # legs
    for (x0, y0, x1, y1, x2, y2) in ((5, 14, 2, 15, 0, 20), (5, 16, 2, 18, 1, 22), (6, 17, 4, 20, 4, 22)):
        c.line(x0, y0, x1, y1, "3", mirror=True); c.line(x1, y1, x2, y2, "2", mirror=True)
    # claws raised
    c.line(5, 11, 2, 8, "2", mirror=True)
    for sx in (0, 1):
        pass
    c.mr(0, 3, 4, 8, "2")
    c.mr(1, 3, 1, 5, "1"); c.mr(0, 5, 0, 7, "1") if False else None
    c.mr(2, 3, 2, 4, ".") ; c.mr(3, 5, 3, 7, "O") if False else None
    c.mr(2, 5, 2, 6, "3") ; c.mr(2, 4, 2, 4, "3")
    c.mr(4, 7, 4, 8, "R") if False else None
    c.mr(1, 4, 1, 4, "y")
    # shell with glowing magma cracks
    c.ell(7.5, 14, 5.8, 5, "3"); c.ell(7.5, 13.5, 5.2, 4.5, "2"); c.ell(6.5, 11.5, 3, 2.2, "1")
    c.line(5, 12, 8, 14, "y"); c.line(8, 14, 6, 17, "y"); c.line(8, 14, 11, 13, "4") if False else None
    c.line(8, 14, 11, 12, "y"); c.line(11, 12, 12, 15, "4") if False else None
    c.p(5, 12, "R") ; c.p(6, 17, "4") ; c.p(11, 15, "4")
    c.p(8, 13, "w") if False else None
    # eyes on stalks
    c.p(6, 9, "O"); c.p(9, 9, "O"); c.p(6, 8, "y"); c.p(9, 8, "y")
    c.r(5, 19, 10, 19, "3") if False else None
    return fin(c, 0, 15)


def _moss_mat(seed):
    import random
    rnd = random.Random(seed)
    c = C()
    n = 5
    for k in range(n):
        cx = rnd.uniform(3, 12); cy = rnd.uniform(11, 20)
        rx = rnd.uniform(3.0, 5.0); ry = rnd.uniform(2.0, 3.4)
        c.ell(cx, cy, rx, ry, "2")
    # highlights top-left, shade bottom-right, brittle holes
    g = c.g
    for y in range(24):
        for x in range(16):
            if g[y][x] == "2":
                up = y > 0 and g[y - 1][x] == "."
                dn = y < 23 and g[y + 1][x] == "."
                lf = x > 0 and g[y][x - 1] == "."
                if up or lf:
                    g[y][x] = "1"
                elif dn:
                    g[y][x] = "3"
    for k in range(10):
        x = rnd.randrange(2, 14); y = rnd.randrange(10, 21)
        if g[y][x] in "123":
            g[y][x] = rnd.choice("3.1w")
    for k in range(5):
        x = rnd.randrange(2, 14); y = rnd.randrange(10, 21)
        if g[y][x] in "123":
            g[y][x] = "R"   # dark red bloom
    return fin(c, 0, 15)


def moss():
    return _moss_mat(3)


def natural_weapon_cable():
    c = C()
    # writhing cable: thick coiled snake of cable with plug head and sparks
    tube(c, [(2, 20), (3, 14), (8, 12), (11, 16), (9, 19)], 1.9, 1.6, "2")
    tube(c, [(2, 19), (3, 14), (8, 11), (10, 14)], 0.8, 0.8, "1")
    for (x, y) in ((3, 17), (5, 12), (10, 14), (10, 18)):
        c.r(x - 1, y, x + 1, y, "3")
    tube(c, [(9, 18), (11, 11), (13, 6)], 1.4, 1.1, "2")
    c.line(10, 17, 12, 10, "1")
    c.r(12, 3, 15, 6, "L"); c.r(12, 3, 15, 3, "l"); c.p(13, 2, "w"); c.p(14, 2, "w")
    c.p(13, 4, "4"); c.p(14, 5, "4")
    c.p(11, 1, "4"); c.p(15, 0, "4"); c.p(10, 4, "5")
    return fin(c, 0, 15)


def natural_weapon_hull():
    c = C()
    # slab of machine hull plating with rivets and a jagged edge
    c.r(2, 6, 13, 18, "2")
    c.r(2, 6, 13, 7, "1"); c.r(12, 8, 13, 18, "3"); c.r(2, 17, 13, 18, "3")
    c.r(3, 9, 7, 15, "l"); c.r(3, 9, 7, 9, "w"); c.r(6, 9, 7, 15, "L") if False else None
    c.r(8, 9, 11, 15, "L"); c.r(8, 9, 11, 9, "l")
    # jagged torn edge
    for (x, y) in ((1, 8), (1, 11), (14, 10), (14, 14), (13, 5), (4, 5), (9, 5), (2, 19), (6, 19), (11, 19)):
        c.p(x, y, "2" if y < 12 else "3")
    for (x, y) in ((3, 7), (12, 7), (3, 17), (12, 17), (7, 12), (10, 12)):
        c.p(x, y, "O")
    c.line(4, 12, 6, 14, "O") if False else None
    c.r(5, 11, 6, 12, "4"); c.p(5, 11, "5")
    c.p(10, 16, "4")
    return fin(c, 0, 15)


def natural_weapon_pincer():
    c = C()
    # one big crab-like pincer, pointing up
    c.r(5, 15, 10, 21, "2"); c.r(5, 15, 7, 21, "1"); c.r(9, 15, 10, 21, "3")
    c.ell(7.5, 12, 5, 4, "2"); c.ell(6.5, 11, 3, 2.4, "1")
    # fixed finger (left) and moving finger (right)
    c.line(4, 10, 3, 3, "2"); c.line(5, 9, 5, 3, "2"); c.line(6, 8, 6, 4, "3") if False else None
    c.r(3, 3, 5, 8, "2"); c.r(3, 3, 3, 9, "1"); c.p(3, 2, "w"); c.p(4, 1, "w")
    c.line(10, 10, 12, 3, "3"); c.line(9, 9, 10, 3, "3")
    c.r(10, 3, 12, 8, "3"); c.p(12, 2, "w"); c.p(11, 1, "w")
    c.r(6, 4, 9, 8, "O") if False else None
    c.line(6, 7, 6, 3, "O") if False else None
    # teeth between
    for (x, y) in ((6, 5), (6, 7), (9, 4), (9, 6)):
        c.p(x, y, "w")
    c.r(7, 5, 8, 9, "O")
    c.r(5, 21, 10, 21, "3")
    return fin(c, 0, 15)


def nephilim_ehalcodon():
    c = C()
    # god-light rays + halo behind
    for (x, y) in ((1, 1), (3, 0), (7, 0), (11, 0), (14, 1), (0, 4), (15, 5), (2, 7)):
        c.p(x, y, "w")
    c.line(7, 0, 7, 3, "w"); c.line(8, 0, 8, 3, "Y") if False else None
    c.line(2, 1, 4, 4, "w", mirror=True)
    c.line(0, 4, 3, 5, "w", mirror=True)
    # immense quadruped (sketched by radiation): big body, spindle-glitter haunches
    c.ell(8.5, 13, 6.4, 4.4, "3"); c.ell(8.5, 12.5, 5.8, 3.8, "2"); c.ell(7, 10.5, 3.8, 1.6, "1")
    c.r(1, 11, 4, 14, "2")
    # neck/head left with antlers of light
    c.line(3, 11, 2, 6, "2"); c.line(4, 11, 3, 6, "2")
    c.ell(2.5, 6, 2.3, 2, "1"); c.p(1, 6, "O"); c.p(3, 5, "w"); c.p(2, 7, "O") if False else None
    c.line(2, 4, 0, 1, "w"); c.line(3, 4, 5, 1, "w"); c.p(1, 2, "Y") if False else None
    # legs
    for x in (3, 5, 11, 13):
        c.r(x, 16, x + 1, 20, "2" if x < 9 else "3"); c.r(x, 21, x + 1, 21, "O")
    # glitter dusting haunches
    for (x, y) in ((11, 10), (12, 12), (10, 14), (13, 14), (9, 11), (12, 16), (11, 18), (7, 14)):
        c.p(x, y, "w")
    c.p(10, 12, "Y") if False else None
    # many eyes on the flank
    c.p(7, 12, "O"); c.p(8, 12, "w")
    c.line(14, 10, 15, 14, "1") ; c.p(15, 15, "w")
    return fin(c, 0, 15)


def pax_klanq():
    c = C()
    # humanoid-shaped erumpent heap of organ knots
    # legs
    c.ell(5, 19, 2.4, 2.8, "2"); c.ell(10.5, 19, 2.4, 2.8, "3")
    # torso heap
    c.ell(7.5, 13, 5, 5.6, "2"); c.ell(6.5, 11.5, 3, 3, "1"); c.ell(10, 15, 2.6, 3, "3")
    # arms: bulbous tubers
    c.ell(2.5, 12, 1.8, 3.2, "2"); c.ell(13, 12, 1.8, 3.2, "3")
    c.ell(2, 16, 1.4, 1.6, "1"); c.ell(13.5, 16, 1.4, 1.6, "3")
    # head: mass of knots
    c.ell(7.5, 5, 3.2, 3.2, "2"); c.ell(6.5, 4, 1.6, 1.6, "1")
    # organs: tubes and bulbs (pink/red)
    for (x, y, ch) in ((5, 11, "R"), (9, 10, "r"), (7, 14, "R"), (10, 16, "r"), (4, 15, "r"), (6, 18, "R"),
                       (11, 12, "R"), (8, 8, "r")):
        c.r(x, y, x + 1, y + 1, ch); c.p(x, y, "w") if (x + y) % 3 == 0 else None
    c.line(5, 13, 8, 16, "r"); c.line(9, 12, 10, 14, "R")
    # eyes / mouths scattered
    c.p(6, 5, "O"); c.p(9, 5, "O"); c.r(7, 7, 8, 7, "O")
    c.p(6, 4, "w") if False else None
    c.p(5, 14, "O"); c.p(11, 13, "O") if False else None
    c.p(8, 12, "O"); c.p(8, 11, "w") if False else None
    # spore caps
    c.p(4, 3, "4"); c.p(11, 3, "4"); c.p(7, 1, "4"); c.p(8, 1, "5"); c.p(13, 8, "4"); c.p(2, 8, "5")
    return fin(c, 0, 15)


def resheph():
    c = C()
    # hologram: scanline gaps, sun disc halo, drape over one shoulder
    # sun disc
    c.ell(7.5, 6, 5.5, 5.5, "y"); c.ell(7.5, 6, 4.2, 4.2, "O") if False else None
    c.ell(7.5, 6, 4.4, 4.4, "w")
    c.ell(7.5, 6, 3.6, 3.6, "y")
    # rays
    for (x, y) in ((7, 0), (8, 0), (1, 1), (14, 1), (0, 6), (15, 6), (3, 11), (12, 11)):
        c.p(x, y, "y")
    # robed body
    c.r(5, 9, 10, 20, "1")
    c.r(4, 15, 11, 21, "1")
    c.r(10, 9, 11, 20, "2")
    c.r(10, 15, 11, 21, "2")
    c.r(3, 20, 12, 21, "2")
    # drape from shoulder
    c.line(4, 9, 11, 18, "3"); c.line(5, 9, 11, 17, "2") if False else None
    c.line(4, 10, 10, 18, "w") if False else None
    c.r(4, 9, 6, 10, "w")
    c.line(5, 11, 9, 17, "3")
    # head
    c.r(6, 4, 9, 8, "w"); c.p(6, 6, "O"); c.p(9, 6, "O")
    c.r(7, 8, 8, 8, "1")
    # scanlines
    for y in (2, 5, 8, 11, 14, 17, 20):
        for x in range(16):
            if c.g[y][x] in "123wy":
                c.g[y][x] = "."
    return fin(c, 2, 13)


def santalalotze():
    c = C()
    # puffed bladder bulb on a tangle of vines, soaking up soft light
    for (x0, y0, x1, y1) in ((7, 21, 2, 19), (8, 21, 13, 19), (7, 20, 0, 15), (8, 20, 15, 15), (6, 21, 5, 22)):
        tube(c, [(x0, y0), (x1, y1)], 0.9, 0.7, "3")
    c.line(2, 19, 0, 15, "3") if False else None
    c.ell(7.5, 12, 6.2, 6.6, "3"); c.ell(7.5, 11.5, 5.6, 6, "2"); c.ell(6, 9.5, 3.2, 3.2, "1")
    # ribs of the bladder
    c.line(7, 6, 7, 18, "3"); c.line(4, 7, 4, 17, "3") if False else None
    c.line(4, 8, 5, 17, "3"); c.line(11, 8, 10, 17, "3")
    # face: contented
    c.p(5, 11, "O"); c.p(10, 11, "O"); c.p(6, 14, "O"); c.p(9, 14, "O"); c.r(7, 15, 8, 15, "O")
    c.p(4, 13, "4"); c.p(11, 13, "4")
    # leaves and tendrils with buds
    c.r(3, 3, 5, 4, "g") if False else None
    c.line(6, 6, 3, 2, "G"); c.line(9, 6, 12, 2, "G"); c.p(2, 1, "4"); c.p(13, 1, "4")
    c.p(7, 5, "4"); c.p(8, 4, "5"); c.p(7, 3, "w")
    c.p(1, 7, "w"); c.p(14, 8, "w"); c.p(4, 0, "w")
    c.r(0, 15, 1, 15, "g"); c.r(14, 15, 15, 15, "g")
    return fin(c, 0, 15)


def sprouting_orb():
    c = C()
    # carbon orb with green ringlet sprouts
    c.ell(7.5, 14, 5.4, 5.4, "O"); c.ell(7.5, 14, 4.8, 4.8, "L"); c.ell(6.2, 12.2, 2.4, 2.2, "l")
    c.p(5, 11, "w")
    # ringlets (loops) around
    def ring(cx, cy, r, ch, ch2):
        c.ell(cx, cy, r, r, ch); c.ell(cx, cy, r - 1.1, r - 1.1, ".")
        c.p(round(cx - r + 0.6), round(cy - r + 0.6), ch2)
    ring(3, 7, 2.6, "g", "w"); ring(12, 7, 2.6, "G", "w"); ring(2, 16, 2.2, "G", "w"); ring(13.5, 16, 2.2, "g", "w")
    ring(7.5, 3, 2.4, "g", "w")
    c.r(7, 5, 8, 8, "g") if False else None
    c.line(4, 9, 4, 10, "g"); c.line(11, 9, 11, 10, "G"); c.line(7, 5, 7, 8, "G")
    c.line(4, 17, 2, 17, "G"); c.line(11, 17, 13, 17, "g") if False else None
    c.p(11, 17, "G"); c.p(12, 17, "G")
    # tiny leaves with pale buds
    c.p(0, 4, "h"); c.p(15, 4, "h"); c.p(5, 0, "h"); c.p(10, 0, "h")
    c.p(7, 2, "4"); c.p(3, 6, "4") if False else None
    c.p(7, 3, "w") if False else None
    return fin(c, 0, 15)


def svardym_hatchling():
    c = C()
    # oversized glistening feet
    c.r(0, 19, 5, 21, "2"); c.r(0, 21, 5, 21, "3"); c.r(10, 19, 15, 21, "2"); c.r(10, 21, 15, 21, "3")
    for x in (0, 2, 4, 10, 12, 14):
        c.p(x, 22, "w")
    c.r(0, 19, 5, 19, "1"); c.r(10, 19, 15, 19, "1")
    c.p(1, 20, "w"); c.p(11, 20, "w")
    # legs
    c.r(3, 16, 4, 19, "2"); c.r(11, 16, 12, 19, "3")
    # round body
    c.ell(7.5, 13, 5, 4.4, "3"); c.ell(7.5, 12.5, 4.4, 3.8, "2"); c.ell(6.5, 11, 2.6, 1.8, "1")
    c.r(6, 14, 9, 16, "w") if False else None
    c.ell(7.5, 15, 2.4, 1.5, "w")
    # big head, huge mouth open and hungry
    c.ell(7.5, 6, 4.2, 3.6, "2"); c.ell(6.5, 5, 2.4, 1.6, "1")
    c.r(5, 5, 6, 6, "w"); c.r(9, 5, 10, 6, "w"); c.p(6, 6, "O"); c.p(9, 6, "O")
    c.r(5, 8, 10, 9, "O"); c.p(6, 8, "w"); c.p(8, 8, "w"); c.p(10, 8, "w") if False else None
    c.p(7, 9, "R"); c.p(8, 9, "R")
    # eggshell cap + crest
    c.r(5, 2, 10, 2, "w"); c.p(6, 1, "w"); c.p(9, 1, "w"); c.p(7, 2, "L") ; c.p(11, 2, "w")
    # tail
    c.line(11, 15, 15, 14, "3")
    c.p(15, 13, "2")
    return fin(c, 0, 15)


def tortoise():
    c = C()
    # ancient tortoise: smooth stone plastron, weathered shell, sour smile
    c.r(0, 15, 3, 18, "4"); c.r(12, 16, 15, 19, "4")
    c.r(1, 19, 4, 20, "5"); c.r(12, 19, 15, 20, "5")
    c.r(5, 18, 7, 21, "5"); c.r(10, 18, 12, 21, "5")
    c.ell(2.5, 11, 2.9, 2.8, "4"); c.r(0, 10, 2, 13, "4")
    c.p(2, 9, "5"); c.p(3, 9, "5")
    c.p(2, 10, "O"); c.p(1, 10, "w") if False else None
    # sour smile: downturned mouth line
    c.p(0, 13, "O"); c.p(1, 12, "O"); c.p(2, 12, "O")
    c.p(0, 12, "5") ; c.p(3, 13, "O")
    c.r(2, 7, 4, 8, "5") if False else None
    c.ell(9, 13, 7, 6.5, "3"); c.ell(9, 12.5, 6.3, 5.8, "2"); c.ell(9, 11.5, 5, 4, "1")
    c.line(9, 7, 9, 17, "3"); c.line(4, 11, 14, 11, "3"); c.line(3, 15, 15, 15, "3")
    c.line(5, 8, 6, 11, "3"); c.line(13, 8, 12, 11, "3")
    # eroded patches / cracks
    for x, y in [(6, 8), (12, 8), (7, 13), (11, 13), (9, 9), (5, 16), (13, 16)]:
        c.p(x, y, "w")
    c.p(8, 13, "4"); c.p(10, 17, "5") ; c.p(4, 13, "L") if False else None
    # lichen
    c.p(12, 7, "g"); c.p(11, 7, "G")
    return fin(c, 0, 15)


def vaam():
    c = C()
    # brush-shaped legs on each side
    for i, y in enumerate((14, 16, 18)):
        c.r(0, y, 3, y + 1, "4"); c.r(12, y, 15, y + 1, "5")
        c.p(0, y, "c"); c.p(15, y + 1, "c")
        c.r(1, y + 1, 2, y + 1, "5") if False else None
    c.r(3, 20, 4, 21, "5"); c.r(11, 20, 12, 21, "5")
    # shell arches: huddled pill bug
    c.ell(7.5, 13.5, 6, 7, "3")
    for k, (ry, ch) in enumerate(((7, "2"), (5.8, "1"))):
        pass
    c.ell(7.5, 13, 5.4, 6.2, "2")
    for y in (8, 11, 14, 17):
        c.r(3 if y > 8 else 5, y, 12 if y > 8 else 10, y, "3")
    c.r(5, 8, 10, 9, "1") ; c.r(4, 10, 9, 10, "1") if False else None
    c.r(4, 10, 6, 13, "1"); c.r(4, 14, 5, 16, "1")
    for (x, y) in ((6, 9), (7, 12), (6, 15)):
        c.p(x, y, "w")
    # shy face
    c.r(5, 18, 10, 20, "3")
    c.p(6, 19, "c"); c.p(9, 19, "c")
    c.p(7, 19, "O") if False else None
    # antennae brushes
    c.line(6, 17, 4, 21, "4") if False else None
    c.p(7, 3, "4") if False else None
    return fin(c, 0, 15)


def worm():
    c = C()
    # skinny pale worm, arched; rope of spittle to the ground
    tube(c, [(14, 20), (12, 19), (8, 19), (5, 16), (5, 12), (8, 8), (11, 6)], 1.9, 1.9, "2")
    tube(c, [(14, 19), (12, 18), (8, 18), (5, 15), (5, 11), (8, 7)], 0.8, 0.8, "1")
    # rings
    for (x, y) in ((13, 19), (11, 19), (9, 19), (7, 18), (5, 15), (5, 13), (6, 10), (8, 8)):
        c.p(x, y + 1 if x > 8 else y, "3")
    for (x, y) in ((12, 20), (10, 20), (8, 20), (6, 19), (4, 17), (4, 14), (5, 10)):
        c.p(x, y, "3")
    # head with peristome mouth
    c.ell(11.5, 5.5, 2.6, 2.6, "1"); c.p(12, 5, "O"); c.p(13, 5, "O"); c.p(13, 6, "O"); c.p(11, 4, "w")
    c.p(13, 6, "O")
    # rope of dissolving spittle
    for y in range(7, 21):
        c.p(13 if y % 3 else 14, y, "w") if y > 7 else None
    c.p(14, 20, "w"); c.p(13, 21, "w"); c.p(12, 21, "w")
    # dissolve drips at ground
    c.p(11, 21, "w") ; c.p(15, 21, "w")
    return fin(c, 0, 15)


GROUND = {
    "agolzvuv": agolzvuv, "biographer_bot": biographer_bot, "cherub_arachnid": cherub_arachnid,
    "cherub_cat": cherub_cat, "cherub_fish": cherub_fish, "cherub_grazing": cherub_grazing,
    "cherub_ooze": cherub_ooze, "cherub_succulent": cherub_succulent, "cherub_urchin": cherub_urchin,
    "chromeling_special": chromeling_special, "decarbonizer": decarbonizer, "feral_lah": feral_lah,
    "girshworm": girshworm, "godhed3_unplanished": godhed3_unplanished, "golem_bush": golem_bush,
    "golem_equine": golem_equine, "golem_hover_robot": golem_hover_robot,
    "golem_mopango_charioteer": golem_mopango_charioteer, "golem_slug": golem_slug, "golem_tree": golem_tree,
    "gyrohumor": gyrohumor, "magmacrab": magmacrab, "moss": moss,
    "natural_weapon_cable": natural_weapon_cable, "natural_weapon_hull": natural_weapon_hull,
    "natural_weapon_pincer": natural_weapon_pincer, "nephilim_ehalcodon": nephilim_ehalcodon,
    "pax_klanq": pax_klanq, "resheph": resheph, "santalalotze": santalalotze, "sprouting_orb": sprouting_orb,
    "svardym_hatchling": svardym_hatchling, "tortoise": tortoise, "vaam": vaam, "worm": worm,
}
for _n, _f in GROUND.items():
    SPRITES[_n] = _f()
