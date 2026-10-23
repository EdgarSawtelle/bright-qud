"""B3 humanoid kit: the shared lanky figure (style_b3) + parts + mutation overlays + player looks.

    person(*parts, face="face", sash=True, ...)  -> 24-row grid of 16-char strings

ANCHORS (every humanoid uses these; mutation overlays are drawn against them). x = column, y = row.
  head      rows 3-7: row 3 cols 6-9 (forehead), rows 4-6 cols 5-10, row 7 cols 6-9 (chin)
  eyes      row 5, cols 6 and 9 (`O`)           [goggles: row 5 band; wrap: rows 6-7]
  hat zone  rows 0-3 (hats sit on rows 1-3, brims on row 3); halo floats on rows 0-1
  neck      row 8, cols 7-8
  shoulders row 9, cols 4-11
  arms      left sleeve col 4, right sleeve col 11, rows 10-14
  hands     row 15: left hand (4,15), right hand (11,15) [+ grip pixel (12,15)]
  held item right hand: shaft at col 13 (rows vary); left hand items hang at cols 0-3, rows 13-17
  torso     rows 9-15 cols 5-10; robe flares rows 16-18 cols 4-11, rows 19-21 cols 3-12
  robe hem  row 21 (cols 3-12, dark)
  feet      row 22, cols 5-6 and 9-10 (`O`)
  shadow    row 23, cols 3-12 (`x`)

PARTS are plain functions `part(c, **options)`; pass them to person() in drawing order, or use
functools.partial(part, col="5") to change options. Parts marked back=True are drawn behind the
body (cape, pack, wings...). Overlay-dict style also works: person(..., overlay({row: "16 chars"})).

Colors: roles 1/2/3 = body light/mid/dark, 4/5/6 = detail light/mid/dark. Fixed letters only for
skin (s/S), eyes (O), steel (l/L), wood (n/N), gold (y), bone/white (w), hair.
"""
from functools import partial


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

    def rows(s, d):
        """stamp a {row: 16-char string} overlay ('.' keeps, '_' erases)."""
        for y, row in d.items():
            assert len(row) == 16, (y, row)
            for x, ch in enumerate(row):
                if ch == "_":
                    s.g[y][x] = "."
                elif ch != ".":
                    s.g[y][x] = ch

    def shadow(s, x0, x1, y=23):
        for x in range(x0, x1 + 1):
            if s.g[y][x] == ".":
                s.g[y][x] = "x"

    def out(s):
        return ["".join(r) for r in s.g]


def back(fn):
    fn.back = True
    return fn


def overlay(d, behind=False):
    def f(c):
        c.rows(d)
    f.back = behind
    return f


def _is_back(p):
    return getattr(p, "back", False) or getattr(getattr(p, "func", None), "back", False)


# --------------------------------------------------------------------------------------------
# base figure
# --------------------------------------------------------------------------------------------
def person(*parts, face="face", sash=True, sleeves=True, feet=True, skin=("s", "S"),
           body="2", lite="1", dark="3", trim="4", goggles="c"):
    """lanky robed figure. face: "face" (skin + eyes), "goggles", "wrap" (face wrap over mouth, eyes
    visible), "mask" (wrap + goggles), "none" (blank skin, no eyes)."""
    c = C()
    for p in parts:
        if _is_back(p):
            p(c)
    s, S = skin
    # robe
    c.r(5, 9, 10, 15, body)
    c.r(4, 16, 11, 18, body)
    c.r(3, 19, 12, 21, body)
    c.r(4, 9, 11, 9, body)
    c.r(5, 9, 6, 15, lite)
    c.r(4, 16, 5, 18, lite)
    c.r(3, 19, 5, 21, lite)
    c.r(10, 9, 10, 15, dark)
    c.r(10, 16, 11, 18, dark)
    c.r(10, 19, 12, 21, dark)
    c.r(8, 18, 8, 21, dark)
    c.r(3, 21, 12, 21, dark)
    if sash:
        c.line(5, 10, 10, 14, trim)
        c.line(5, 11, 10, 15, trim)
    if sleeves:
        c.r(4, 10, 4, 14, body)
        c.r(11, 10, 11, 14, dark)
        c.p(4, 15, s)
        c.p(11, 15, S)
    if feet:
        c.r(5, 22, 6, 22, "O")
        c.r(9, 22, 10, 22, "O")
    c.r(7, 8, 8, 8, S)
    # head
    c.r(6, 3, 9, 3, s)
    c.r(5, 4, 10, 6, s)
    c.r(6, 7, 9, 7, s)
    c.r(10, 4, 10, 6, S)
    c.r(8, 7, 9, 7, S)
    if face in ("face", "wrap"):
        c.p(6, 5, "O")
        c.p(9, 5, "O")
    if face in ("goggles", "mask"):
        c.r(5, 5, 10, 5, "L")
        c.p(6, 5, goggles)
        c.p(9, 5, goggles)
        c.p(6, 4, "L")
        c.p(9, 4, "L")
        c.p(5, 4, "L") if False else None
    if face in ("wrap", "mask"):
        c.r(5, 6, 10, 6, trim)
        c.r(6, 7, 9, 7, "5" if trim == "4" else trim)
    for p in parts:
        if not _is_back(p):
            p(c)
    c.shadow(3, 12)
    return c.out()


# --------------------------------------------------------------------------------------------
# headwear
# --------------------------------------------------------------------------------------------
def hat_wide(c, a="2", d="3", band="4"):
    """wide-brim hat (brim row 3, cols 2-13)."""
    c.r(6, 0, 9, 0, a)
    c.r(5, 1, 10, 1, a)
    c.r(5, 2, 10, 2, band)
    c.r(2, 3, 13, 3, a)
    c.r(2, 3, 4, 3, d)
    c.r(11, 3, 13, 3, d)
    c.p(6, 1, "1" if a == "2" else a)


def hat_straw(c, a="t", d="y", band="4"):
    """conical straw hat."""
    c.r(7, 0, 8, 0, a)
    c.r(6, 1, 9, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(2, 3, 13, 3, a)
    c.r(2, 3, 3, 3, d)
    c.r(12, 3, 13, 3, d)
    c.r(5, 2, 10, 2, band)
    c.line(4, 2, 4, 2, a)
    c.p(6, 1, "w")


def hat_pointy(c, a="2", d="3", band="4"):
    """tall pointed hat with brim."""
    c.p(8, 0, a)
    c.p(9, 0, d)
    c.r(7, 1, 9, 1, a)
    c.r(6, 2, 9, 2, band)
    c.r(3, 3, 12, 3, a)
    c.r(10, 3, 12, 3, d)
    c.p(7, 1, "1")


def cap(c, a="2", band="4"):
    """soft cap with a peak."""
    c.r(6, 1, 9, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(5, 3, 10, 3, band)
    c.r(10, 3, 12, 3, band)
    c.p(6, 1, "1")


def hood(c, a="2", lite="1", dark="3"):
    """cowl: wraps the head, face opening cols 6-9 (eyes stay visible)."""
    c.r(7, 1, 8, 1, a)
    c.r(6, 2, 9, 2, a)
    c.r(5, 3, 10, 3, a)
    c.r(4, 4, 5, 8, a)
    c.r(10, 4, 11, 8, a)
    c.r(4, 8, 11, 8, a)
    c.r(4, 3, 4, 8, lite)
    c.r(11, 3, 11, 8, dark)
    c.r(10, 4, 10, 7, dark)
    c.r(5, 4, 5, 7, a)
    c.p(7, 1, lite)
    c.p(6, 2, lite)
    c.p(9, 2, dark)
    c.p(5, 3, lite)
    c.p(10, 3, dark)


def turban(c, a="4", b="5", gem="y"):
    """wrapped turban with a gem."""
    c.r(6, 0, 9, 0, b)
    c.r(5, 1, 10, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(5, 3, 10, 3, a)
    c.line(5, 3, 9, 0, b)
    c.line(6, 3, 10, 1, b)
    c.line(5, 2, 8, 0, b) if False else None
    c.r(5, 3, 10, 3, b)
    c.r(5, 3, 6, 3, a)
    c.p(7, 2, gem)
    c.p(10, 3, b)
    c.r(11, 3, 11, 6, b)   # hanging tail
    c.p(11, 7, a)


def helmet(c, crest=False, plume="4"):
    """steel helm with cheek guards. crest=True adds a tall plume."""
    c.r(6, 2, 9, 2, "l")
    c.r(5, 3, 10, 3, "l")
    c.r(5, 4, 5, 6, "L")
    c.r(10, 4, 10, 6, "L")
    c.r(5, 4, 10, 4, "l")
    c.p(6, 2, "w")
    c.p(7, 4, "L")
    c.p(8, 4, "L")
    c.p(10, 3, "L")
    c.p(9, 2, "L")
    if crest:
        c.r(7, 0, 8, 1, plume)
        c.p(7, 2, plume)
        c.p(8, 2, plume)
        c.p(6, 1, "5")
        c.p(9, 1, "6") if False else None


def helmet_visor(c, glow="c"):
    """closed helm: only a glowing visor slit shows (replaces eyes)."""
    c.r(5, 2, 10, 2, "l") if False else None
    c.r(6, 2, 9, 2, "l")
    c.r(5, 3, 10, 7, "l")
    c.r(10, 3, 10, 7, "L")
    c.r(6, 7, 9, 7, "L")
    c.r(6, 5, 9, 5, "O")
    c.p(6, 5, glow)
    c.p(9, 5, glow)
    c.p(6, 2, "w")


def crown(c, a="y", gem="4"):
    """gold crown with gem."""
    c.p(5, 1, a)
    c.p(7, 1, a)
    c.p(8, 1, a)
    c.p(10, 1, a)
    c.r(5, 2, 10, 2, a)
    c.r(5, 3, 10, 3, a)
    c.p(7, 2, gem)
    c.p(8, 2, gem)
    c.p(5, 3, "w") if False else None
    c.p(10, 3, "S") if False else None


def halo(c, a="4", b="5"):
    """glowing ring floating above the head."""
    c.r(6, 0, 9, 0, a)
    c.p(5, 1, a)
    c.p(10, 1, a)
    c.p(6, 1, b)
    c.p(9, 1, b)
    c.r(7, 1, 8, 1, ".")


def sun_halo(c, a="4", b="5"):
    """sun with rays around the head."""
    c.r(6, 0, 9, 0, a)
    c.r(5, 1, 10, 1, b)
    c.r(7, 1, 8, 1, ".")
    c.p(3, 0, a); c.p(12, 0, a); c.p(2, 2, a); c.p(13, 2, a)
    c.p(4, 1, a); c.p(11, 1, a); c.p(4, 3, a) if False else None
    c.p(1, 4, a); c.p(14, 4, a)
    c.p(4, 2, b); c.p(11, 2, b)


def moon_crown(c, a="l"):
    """silver crescent on the brow."""
    c.p(6, 0, a)
    c.p(9, 0, a)
    c.p(5, 1, a)
    c.p(10, 1, a)
    c.r(5, 2, 10, 2, "L")
    c.r(6, 2, 9, 2, a)
    c.p(7, 2, "w")
    c.p(8, 2, "w")
    c.p(6, 1, "w")
    c.p(9, 1, "w")
    c.r(5, 3, 10, 3, a)


def horn_headdress(c, a="w", b="L", band="5"):
    """bull-horn headdress with brow band."""
    c.r(5, 3, 10, 3, band)
    c.mr(3, 3, 4, 3, a)
    c.mr(2, 2, 3, 2, a)
    c.mr(2, 0, 2, 1, a)
    c.mr(3, 0, 3, 0, b) if False else None
    c.mr(3, 1, 3, 1, b)
    c.mr(3, 3, 3, 3, b)
    c.p(7, 3, "4"); c.p(8, 3, "4")


def hair_short(c, col="N", hi="n"):
    c.r(6, 2, 9, 2, col)
    c.r(5, 3, 10, 3, col)
    c.r(5, 4, 5, 4, col)
    c.r(10, 4, 10, 4, col)
    c.r(7, 3, 8, 3, col)
    c.p(7, 2, hi); c.p(8, 2, hi)
    c.p(6, 3, hi) if False else None


def hair_long(c, col="N", hi="n"):
    hair_short(c, col, hi)
    c.r(4, 4, 4, 11, col)
    c.r(11, 4, 11, 11, col)
    c.r(5, 5, 5, 7, col)
    c.r(10, 5, 10, 7, col)
    c.r(4, 12, 4, 12, hi); c.r(11, 12, 11, 12, hi)


def hair_wild(c, col="l", hi="w"):
    """wild bristling hair."""
    c.p(5, 0, col); c.p(8, 0, col); c.p(10, 0, col)
    c.r(5, 1, 10, 1, col)
    c.r(4, 2, 11, 2, col)
    c.r(4, 3, 11, 3, col)
    c.p(4, 4, col); c.p(11, 4, col)
    c.p(7, 1, hi); c.p(9, 2, hi); c.p(5, 2, hi)
    c.p(3, 2, col); c.p(12, 2, col)


def hair_mohawk(c, col="r", hi="y"):
    c.r(7, 0, 8, 1, col)
    c.r(7, 2, 8, 3, col)
    c.p(8, 0, hi)
    c.r(6, 3, 9, 3, "N") if False else None


def hair_bun(c, col="N", hi="n"):
    hair_short(c, col, hi)
    c.r(7, 0, 8, 1, col)
    c.p(7, 0, hi)


def bald_shine(c):
    c.p(7, 3, "w")


def beard(c, col="w", shade="l"):
    """full beard over chin and neck."""
    c.r(5, 6, 5, 7, col)
    c.r(10, 6, 10, 7, shade)
    c.r(6, 7, 9, 7, col)
    c.r(6, 8, 9, 8, col)
    c.r(7, 9, 8, 9, col)
    c.p(9, 8, shade); c.p(8, 9, shade)
    c.r(6, 6, 9, 6, "." ) if False else None
    c.r(6, 6, 6, 6, col); c.r(9, 6, 9, 6, shade)


def stubble(c, col="N"):
    """short goatee / mustache."""
    c.r(6, 6, 9, 6, col)
    c.r(7, 7, 8, 7, col)


def spectacles(c):
    for x, y in ((5, 5), (7, 5), (8, 5), (10, 5), (6, 4), (9, 4), (6, 6), (9, 6)):
        c.p(x, y, "L")
    c.p(7, 5, "l"); c.p(8, 5, "l")


def goggles_up(c, lens="c"):
    """goggles pushed up onto the forehead."""
    c.r(5, 3, 10, 3, "L")
    c.p(6, 3, lens); c.p(9, 3, lens)
    c.p(5, 4, "L") if False else None


def veil(c, a="4", b="5"):
    """veil across the lower face (eyes show)."""
    c.r(5, 6, 10, 6, a)
    c.r(6, 7, 9, 8, b)
    c.p(10, 6, b)


def blindfold(c, a="4"):
    """cloth over the eyes."""
    c.r(5, 4, 10, 5, a)
    c.r(5, 5, 10, 5, "5")
    c.p(6, 5, a); c.p(9, 5, a)
    c.p(11, 5, "5"); c.p(12, 6, "5")


def scarf(c, a="4", b="5"):
    """scarf at the neck with a trailing end."""
    c.r(6, 8, 9, 8, a)
    c.r(5, 9, 10, 9, b)
    c.r(10, 10, 10, 12, a)
    c.p(10, 13, b)


# --------------------------------------------------------------------------------------------
# clothing
# --------------------------------------------------------------------------------------------
def apron(c, a="5", b="4", strap="6"):
    """work apron over the robe."""
    c.r(6, 11, 9, 20, a)
    c.r(6, 11, 9, 11, b)
    c.r(6, 11, 6, 20, b)
    c.p(5, 10, strap); c.p(10, 10, strap)
    c.p(6, 10, strap); c.p(9, 10, strap)
    c.r(7, 15, 8, 16, strap)
    c.r(6, 20, 9, 20, strap)


def armor(c, pauld="l", plate="l", shade="L", belt="4"):
    """steel breastplate, pauldrons, belt."""
    c.r(6, 10, 9, 14, plate)
    c.r(6, 10, 7, 11, "w") if False else None
    c.r(9, 10, 9, 14, shade)
    c.r(6, 14, 9, 14, shade)
    c.p(6, 10, "w")
    c.r(7, 11, 7, 12, "l")
    c.mr(3, 9, 4, 10, pauld)
    c.p(3, 9, "w"); c.p(4, 10, shade) if False else None
    c.r(11, 9, 12, 10, shade)
    c.r(5, 15, 10, 15, belt)
    c.p(7, 15, "y"); c.p(8, 15, "y")
    c.r(5, 16, 6, 18, shade)
    c.r(9, 16, 10, 18, shade) if False else None


def tunic(c, a="2", b="3", legs="3"):
    """short tunic with visible legs (replaces the long robe skirt)."""
    c.r(3, 16, 12, 21, ".")
    c.r(4, 16, 11, 16, a)
    c.r(5, 17, 10, 17, a)
    c.r(4, 16, 4, 16, "1"); c.r(11, 16, 11, 16, b)
    c.r(5, 18, 6, 21, legs)
    c.r(9, 18, 10, 21, legs)
    c.r(5, 18, 5, 21, "N")
    c.r(5, 22, 6, 22, "O"); c.r(9, 22, 10, 22, "O")
    c.r(5, 21, 6, 21, "N"); c.r(9, 21, 10, 21, "N")
    c.r(5, 17, 10, 17, b)


@back
def cape(c, a="6", b="5"):
    """cloak behind the body, wider than the robe."""
    c.r(3, 9, 12, 19, a)
    c.r(2, 12, 13, 21, a)
    c.r(1, 15, 14, 21, a)
    c.r(1, 21, 14, 21, b)
    c.r(2, 12, 3, 21, b)
    c.p(1, 15, "."); c.p(14, 15, ".")


@back
def pack(c, a="N", b="n", roll="4"):
    """bedroll + pack behind the shoulder, sticking out on the left."""
    c.r(1, 8, 4, 16, a)
    c.r(1, 8, 2, 16, b)
    c.r(0, 9, 0, 15, a) if False else None
    c.r(2, 8, 12, 9, roll)
    c.r(1, 7, 3, 8, roll)
    c.r(2, 13, 4, 14, "y") if False else None
    c.p(3, 12, "y")
    c.r(1, 17, 3, 18, a)


@back
def quiver(c):
    """quiver of arrows slanting over the right shoulder."""
    c.line(12, 12, 14, 4, "N")
    c.line(11, 12, 13, 4, "n")
    c.line(12, 12, 15, 3, "N") if False else None
    c.p(13, 3, "w"); c.p(14, 3, "r"); c.p(15, 4, "w")


def shoulder_scrap(c):
    """scavenged shoulder plate."""
    c.r(3, 9, 5, 11, "L")
    c.r(3, 9, 4, 10, "l")
    c.p(3, 11, "n")
    c.p(4, 10, "w")


def belt_pouches(c, a="N", b="n"):
    c.r(5, 14, 10, 14, a)
    c.r(5, 15, 6, 16, b)
    c.p(8, 14, "y")


def poncho(c, a="2", b="1", c3="3", trim="4"):
    """poncho/duster over the shoulders."""
    c.r(3, 9, 12, 12, a)
    c.r(4, 13, 11, 14, a)
    c.r(3, 9, 5, 12, b)
    c.r(10, 9, 12, 14, c3)
    c.r(3, 12, 12, 12, trim)
    c.r(4, 14, 11, 14, trim)
    c.r(6, 9, 9, 9, "s") if False else None
    c.r(7, 9, 8, 10, "S")


# --------------------------------------------------------------------------------------------
# held items (right hand: shaft at col 13) -- hand grip pixel is added by each item
# --------------------------------------------------------------------------------------------
def _grip(c, y=15):
    c.p(12, y, "s")
    c.p(11, y, "s")


def staff(c, head="orb", col="4"):
    """tall staff: head = orb | crook | gem | none."""
    c.line(13, 5, 13, 22, "n")
    c.line(14, 7, 14, 21, "N") if False else None
    if head == "orb":
        c.r(12, 1, 14, 3, col)
        c.p(13, 0, col); c.p(13, 4, "n")
        c.p(12, 1, "w")
    elif head == "crook":
        c.p(13, 4, "n"); c.p(13, 3, "n"); c.p(12, 2, "n"); c.p(13, 2, "n"); c.p(11, 3, "n")
        c.p(11, 4, "n")
    elif head == "gem":
        c.r(12, 2, 14, 3, "y"); c.p(13, 1, "y"); c.p(13, 3, col); c.p(13, 2, col)
    _grip(c)


def spear(c, col="4"):
    """long spear with tassel."""
    c.line(13, 4, 13, 22, "n")
    c.p(13, 0, "w"); c.r(12, 1, 14, 2, "l"); c.p(13, 3, "l"); c.p(14, 2, "L")
    c.p(12, 4, col); c.p(14, 5, col) if False else None
    c.r(12, 5, 12, 6, col)
    _grip(c)


def bow(c, string="w"):
    """big recurve bow, string toward the body."""
    c.line(13, 5, 14, 9, "n"); c.line(14, 9, 14, 15, "n"); c.line(14, 15, 13, 19, "n")
    c.p(12, 4, "n"); c.p(12, 20, "n")
    c.line(12, 5, 12, 19, string) if False else None
    c.line(13, 6, 13, 18, string)
    c.p(14, 12, "N")
    c.p(12, 15, "s"); c.p(11, 15, "s"); c.p(13, 15, "s")


def sword(c, hilt="y"):
    """upright blade."""
    c.line(13, 2, 13, 13, "l")
    c.line(14, 4, 14, 13, "L")
    c.p(13, 1, "w"); c.p(13, 2, "w")
    c.r(12, 14, 14, 14, hilt)
    c.r(13, 15, 13, 17, "N")
    c.p(13, 18, hilt)
    _grip(c)


def hammer(c):
    """big smith hammer."""
    c.line(13, 9, 13, 21, "n")
    c.r(11, 5, 15, 8, "L")
    c.r(11, 5, 15, 5, "l")
    c.p(11, 5, "w")
    _grip(c)


def pistol(c, glow="4"):
    """single pistol held forward."""
    c.r(12, 13, 15, 14, "L")
    c.r(13, 13, 15, 13, "l")
    c.p(12, 15, "N"); c.p(12, 16, "N")
    c.p(14, 14, glow)
    c.p(11, 15, "s"); c.p(12, 14, "s") if False else None
    c.p(12, 15, "s")


def dual_pistols(c, glow="4"):
    """arms thrown out wide, a chrome pistol in each hand (replaces the hanging arms)."""
    c.r(4, 10, 4, 15, ".")
    c.r(11, 10, 11, 15, ".")
    c.r(1, 10, 4, 11, "2")
    c.r(11, 10, 14, 11, "3")
    c.r(1, 10, 4, 10, "1")
    c.r(0, 8, 2, 8, "l"); c.r(13, 8, 15, 8, "l")
    c.r(0, 9, 1, 9, "L"); c.r(14, 9, 15, 9, "L")
    c.p(2, 9, "L"); c.p(13, 9, "L")
    c.p(0, 7, glow); c.p(15, 7, glow)
    c.p(1, 10, "s"); c.p(14, 10, "s")
    c.p(2, 9, "s"); c.p(13, 9, "s")
    c.p(4, 12, "1"); c.p(11, 12, "3")
    c.p(4, 12, "2"); c.p(11, 12, "3")


def rifle(c, glow="4"):
    """long rifle carried at an angle."""
    c.line(14, 3, 11, 13, "l")
    c.line(15, 3, 12, 13, "L")
    c.line(11, 13, 10, 17, "n")
    c.line(12, 13, 11, 17, "N")
    c.p(14, 2, glow); c.p(15, 2, glow) if False else None
    c.p(13, 8, glow)
    c.p(12, 14, "s"); c.p(12, 15, "s"); c.p(11, 15, "s")


def club(c, spikes=True):
    """knobbed wooden club."""
    c.line(13, 9, 13, 21, "n")
    c.r(12, 4, 14, 9, "N")
    c.p(13, 3, "N"); c.p(12, 5, "n"); c.p(12, 6, "n")
    if spikes:
        c.p(11, 5, "l"); c.p(15, 6, "l"); c.p(11, 8, "l"); c.p(15, 4, "l") if False else None
        c.p(13, 2, "l")
    _grip(c)


def axe(c):
    """big single-bit axe."""
    c.line(13, 5, 13, 22, "n")
    c.r(14, 3, 15, 8, "l")
    c.r(13, 4, 13, 7, "L")
    c.r(15, 3, 15, 8, "w")
    c.p(14, 2, "l") if False else None
    c.p(14, 8, "L")
    _grip(c)


def wrench(c, glow="4"):
    """oversized wrench."""
    c.line(13, 9, 13, 21, "l")
    c.line(14, 10, 14, 20, "L")
    c.r(12, 6, 14, 8, "l")
    c.p(13, 6, ".")
    c.p(13, 5, ".") if False else None
    c.p(12, 5, "l"); c.p(14, 5, "l")
    c.p(13, 17, glow); c.p(13, 15, glow)
    _grip(c)


def gear(c, a="l", glow="4"):
    """big cog held aloft in the left hand."""
    c.r(1, 12, 3, 14, a)
    c.p(2, 13, glow)
    c.p(2, 11, a); c.p(0, 13, a); c.p(4, 13, a) if False else None
    c.p(0, 12, "L"); c.p(0, 14, "L"); c.p(4, 12, "L") if False else None
    c.p(2, 15, a); c.p(1, 11, "L"); c.p(3, 11, "L")
    c.p(3, 15, "s") if False else None
    c.p(4, 15, "s"); c.p(3, 15, "s")


def book(c, cover="4", edge="w"):
    """thick book held at the left hip."""
    c.r(0, 13, 3, 17, cover)
    c.r(1, 13, 3, 13, edge)
    c.r(0, 17, 3, 17, "5")
    c.p(0, 14, "y"); c.p(0, 15, "y")
    c.r(1, 14, 2, 16, "5")
    c.p(2, 15, edge)
    c.p(4, 15, "s"); c.p(3, 15, "s")


def hoe(c):
    c.line(13, 5, 13, 22, "n")
    c.r(11, 3, 15, 3, "l")
    c.r(11, 4, 12, 4, "L")
    c.p(15, 4, "L")
    _grip(c)


def sickle(c):
    c.line(13, 9, 13, 18, "n")
    c.p(13, 8, "l"); c.p(14, 7, "l"); c.p(14, 6, "l"); c.p(13, 5, "l"); c.p(12, 4, "l")
    c.p(13, 6, "L"); c.p(13, 7, "L"); c.p(12, 5, "L")
    c.p(12, 4, "w")
    _grip(c, 14)


def shield(c, a="5", b="4", rim="6"):
    """round shield on the left arm."""
    c.r(0, 11, 4, 17, rim)
    c.r(1, 12, 3, 16, a)
    c.r(1, 12, 3, 12, b)
    c.p(2, 14, "y")
    c.p(2, 13, b); c.p(2, 15, b)
    c.p(0, 11, "."); c.p(4, 11, "."); c.p(0, 17, "."); c.p(4, 17, ".")


def lantern(c, glow="4"):
    """hand lantern, glowing."""
    c.r(1, 12, 3, 12, "L")
    c.r(1, 13, 3, 16, glow)
    c.p(2, 14, "w")
    c.r(1, 17, 3, 17, "L")
    c.p(2, 11, "L")
    c.p(4, 15, "s"); c.p(3, 15, glow) if False else None


def jug(c, a="b", b="B"):
    """water jug carried at the left hip."""
    c.r(0, 14, 3, 18, a)
    c.r(1, 12, 2, 13, a)
    c.p(1, 11, "N"); c.p(2, 11, "N")
    c.r(0, 14, 0, 18, b)
    c.p(1, 15, b)
    c.p(4, 15, "s"); c.p(3, 15, a)


def trident(c, col="4"):
    c.line(13, 5, 13, 22, "n")
    c.r(11, 1, 11, 3, "l"); c.r(13, 0, 13, 3, "l"); c.r(15, 1, 15, 3, "l")
    c.r(11, 4, 15, 4, "l")
    c.p(13, 0, "w"); c.p(11, 1, "w"); c.p(15, 1, "w")
    c.p(12, 6, col)
    _grip(c)


def scroll(c, a="w"):
    c.r(1, 13, 3, 17, a)
    c.r(0, 13, 4, 13, "t"); c.r(0, 17, 4, 17, "t")
    c.r(1, 15, 3, 15, "4")
    c.p(4, 15, "s")


# --------------------------------------------------------------------------------------------
# build a MUTATIONS table from drawings
# --------------------------------------------------------------------------------------------
def _ov(c):
    g = c.out()
    return {y: row for y, row in enumerate(g) if row.strip(".")}


def _poly(c, pts, ch):
    n = len(pts)
    for y in range(24):
        for x in range(16):
            inside = False
            for i in range(n):
                (x1, y1), (x2, y2) = pts[i], pts[(i + 1) % n]
                if (y1 > y) != (y2 > y) and x < (x2 - x1) * (y - y1) / (y2 - y1) + x1:
                    inside = not inside
            if inside:
                c.m(x, y, ch)


def _wings():
    c = C()
    # big swept wings: leading bone up and out, feather fan hanging below
    _poly(c, [(5, 9), (3, 5), (0, 0), (0, 12), (1, 16), (2, 15), (3, 18), (4, 17)], "4")
    for (x1, y1) in ((0, 12), (1, 15), (2, 17)):
        c.line(4, 10, x1, y1, "5", mirror=True)
    c.line(5, 9, 0, 0, "6", mirror=True)
    c.line(5, 10, 1, 2, "6", mirror=True)
    c.m(0, 12, "5"); c.m(1, 16, "5"); c.m(3, 18, "5")
    c.m(0, 1, "w"); c.m(1, 3, "w")
    return _ov(c)

def _horns():
    c = C()
    c.mr(4, 4, 5, 5, "w")
    c.mr(2, 3, 3, 4, "w")
    c.mr(1, 1, 2, 3, "w")
    c.mr(2, 0, 3, 1, "w")
    c.m(4, 5, "L"); c.m(2, 4, "L"); c.m(1, 3, "L"); c.m(3, 1, "L")
    c.m(5, 4, "t")
    return _ov(c)


def _multi_arms():
    c = C()
    # upper pair raised
    c.mr(2, 9, 3, 10, "2")
    c.r(3, 10, 3, 10, "2")
    c.r(1, 6, 2, 9, "2"); c.r(13, 6, 14, 9, "3")
    c.r(2, 9, 3, 10, "1"); c.r(12, 9, 13, 10, "3")
    c.m(1, 5, "s"); c.m(2, 5, "s"); c.m(1, 4, "S")
    c.p(14, 4, "S"); c.p(1, 4, "s")
    c.m(1, 7, "4")
    # lower pair out at the waist
    c.r(1, 13, 4, 14, "2"); c.r(11, 14, 14, 14, "3"); c.r(11, 13, 14, 13, "3")
    c.m(0, 13, "s"); c.m(0, 14, "s"); c.m(0, 15, "S")
    c.m(2, 13, "4")
    return _ov(c)


def _carapace():
    c = C()
    c.mr(0, 9, 4, 12, "4")
    c.mr(2, 8, 4, 8, "4")
    c.mr(0, 11, 3, 14, "5")
    c.mr(1, 14, 3, 15, "6")
    c.r(5, 9, 10, 10, "4")
    c.r(5, 9, 10, 9, "1")
    c.r(6, 11, 9, 11, "5")
    c.r(6, 13, 9, 13, "5")
    c.r(6, 15, 9, 17, "5")
    c.r(6, 15, 9, 15, "4"); c.r(6, 17, 9, 17, "4")
    c.r(5, 12, 10, 12, "4"); c.r(5, 14, 10, 14, "4")
    c.m(1, 10, "1")
    c.r(7, 18, 8, 19, "6")
    return _ov(c)


def _quills():
    c = C()
    for (x1, y1) in ((1, 0), (0, 4), (0, 8), (0, 12), (1, 16)):
        c.line(4, 11, x1, y1, "w", mirror=True)
        c.line(5, 11, x1 + 1, y1, "L", mirror=True)
    c.line(6, 9, 4, 0, "w", mirror=True)
    c.line(7, 9, 6, 0, "L", mirror=True) if False else None
    for (x, y) in ((1, 0), (0, 4), (0, 8), (0, 12), (1, 16), (4, 0)):
        c.m(x, y, "t")
    return _ov(c)

def _stinger():
    c = C()
    # thick segmented scorpion tail up the left, arching over the head with a barb
    path = [(2, 20), (1, 18), (0, 16), (0, 14), (0, 12), (0, 10), (0, 8), (0, 6), (1, 4), (3, 2), (5, 1), (7, 1)]
    for i, (x, y) in enumerate(path):
        c.r(x, y, x + 1, y + 1, "5" if i % 2 else "4")
        c.p(x, y + 1, "6") if i % 2 else None
    c.r(8, 1, 9, 2, "w")
    c.p(9, 3, "w"); c.p(9, 4, "r")
    c.p(8, 0, "r") if False else None
    return _ov(c)

def _two_headed():
    c = C()
    c.r(11, 9, 12, 10, "S")
    c.r(12, 5, 14, 5, "s")
    c.r(11, 6, 15, 9, "s")
    c.r(12, 10, 14, 10, "s")
    c.r(15, 6, 15, 9, "S")
    c.r(13, 10, 14, 10, "S")
    c.p(12, 7, "O"); c.p(14, 7, "O")
    c.p(12, 4, "N"); c.p(13, 4, "N"); c.p(14, 4, "N")
    c.r(12, 5, 14, 5, "N")
    c.r(11, 6, 11, 6, "N")
    c.r(14, 8, 14, 8, "S") if False else None
    c.p(13, 9, "R")
    return _ov(c)


def _beak():
    c = C()
    c.r(7, 5, 8, 5, "y")
    c.r(6, 6, 9, 7, "y")
    c.r(7, 8, 8, 8, "y")
    c.p(8, 9, "y")
    c.r(6, 7, 9, 7, "t")
    c.p(7, 6, "O") if False else None
    c.p(6, 6, "w"); c.p(7, 5, "w")
    c.p(8, 8, "t"); c.p(8, 9, "t")
    c.p(9, 6, "t")
    return _ov(c)

def _claws():
    c = C()
    # fat hands with three long digging claws fanning down and out
    c.mr(2, 14, 4, 16, "s")
    c.mr(2, 16, 4, 16, "S")
    c.line(3, 17, 0, 21, "w", mirror=True)
    c.line(4, 17, 2, 22, "w", mirror=True)
    c.line(2, 17, 0, 18, "w", mirror=True)
    c.line(3, 18, 1, 22, "L", mirror=True) if False else None
    c.m(0, 21, "L"); c.m(2, 22, "L"); c.m(0, 18, "L")
    c.m(1, 20, "L") if False else None
    return _ov(c)

def _fur():
    c = C()
    c.mr(2, 8, 5, 12, "n")
    c.r(6, 9, 9, 10, "n")
    c.mr(1, 10, 3, 14, "n")
    c.mr(2, 8, 4, 8, "N")
    for y in range(9, 16, 2):
        c.m(1, y, "N")
        c.m(2, y + 1, "N")
    c.m(0, 12, "n"); c.m(0, 15, "n"); c.m(1, 16, "n")
    c.r(6, 11, 9, 11, "N")
    for x in range(3, 13):
        c.p(x, 20, "n" if x % 2 else "N")
        c.p(x, 21, "N" if x % 2 else "n")
    for x in (2, 13):
        c.p(x, 20, "n")
    c.m(4, 13, "n"); c.m(4, 14, "N")
    return _ov(c)

def _legs():
    c = C()
    # two extra pairs of jointed insect legs splayed from the hips
    for (pts) in (((4, 16), (1, 15), (0, 18), (0, 22)), ((4, 18), (2, 18), (1, 20), (1, 22))):
        for a, b in zip(pts, pts[1:]):
            c.line(a[0], a[1], b[0], b[1], "5", mirror=True)
            c.line(a[0], a[1] + 1, b[0], b[1] + 1, "6", mirror=True) if False else None
    c.m(1, 15, "4"); c.m(2, 18, "4")
    c.m(0, 22, "6"); c.m(1, 22, "6")
    c.m(0, 19, "6"); c.m(0, 20, "5"); c.m(1, 21, "6")
    return _ov(c)


MUTATIONS = {
    "Horns": ("front", _horns()),
    "MultipleArms": ("front", _multi_arms()),
    "Wings": ("back", _wings()),
    "Carapace": ("front", _carapace()),
    "Quills": ("back", _quills()),
    "Stinger": ("back", _stinger()),
    "TwoHeaded": ("front", _two_headed()),
    "Beak": ("front", _beak()),
    "BurrowingClaws": ("front", _claws()),
    "ThickFur": ("front", _fur()),
    "MultipleLegs": ("front", _legs()),
}


# --------------------------------------------------------------------------------------------
# player looks
# --------------------------------------------------------------------------------------------
LOOKS = {
    "Gunslinger": person(hat_wide, dual_pistols, face="wrap", trim="4"),
    "Adventurer": person(cape, pack, hair_short, sword, face="face", sash=False, trim="5"),
    "Mystic": person(hood, staff, face="face", trim="4"),
    "Tinker": person(hair_wild, goggles_up, apron, wrench, face="face", sash=False),
    "Scavenger": person(pack, hair_mohawk, shoulder_scrap, club, face="wrap", sash=False, trim="5"),
    "Warden": person(partial(helmet, crest=True), armor, shield, spear, face="face", sash=False),
    "Pilgrim": person(turban, beard, scarf, staff, book, face="face", trim="4"),
    "Hunter": person(quiver, hair_long, tunic, bow, face="face", sash=False),
}
