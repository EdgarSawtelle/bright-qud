"""Concept mockup: characters dressed by what they wear (paper doll), user request 2026-10-26.

Rows: (1) gear shows on the body, coloured by each item's own game colours / material;
(2) a liquid coating overrides everything (slimed, bloody, oily); (3) the many-mutations mutant
today (one-colour blob) vs a proposal where mutations shape the body: carapace = shell behind the
back, extra legs in front, extra arms bare-skinned, horns bone, gear layered on top.

Usage: .venv/bin/python -I tools/review_paperdoll.py -> mockups/local/paperdoll_concept.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
import b3kit as K  # noqa: E402
from mockup import font  # noqa: E402

OUT = os.path.join(ROOT, "mockups", "local")
Z = 5
GROUND = (0x6e, 0x5c, 0x42)  # earth family (Joppa)
METAL = {"l": "1", "L": "3", "w": "1"}  # fixed steel letters -> the item's own colours


def part(fn, remap=None, **kw):
    c = K.C()
    fn(c, **kw)
    g = c.out()
    if remap:
        g = ["".join(remap.get(ch, ch) for ch in row) for row in g]
    return g


def grid_of(rows):
    c = K.C()
    c.rows(rows)
    return c.out()


def doll(layers):
    """layers: [(grid, fg, detail)] bottom to top -> RGBA tile. Each pixel keeps its own layer's colours;
    outline and shadow come from the combined silhouette."""
    comp = [["."] * 16 for _ in range(24)]
    owner = [[0] * 16 for _ in range(24)]
    for i, (g, _, _) in enumerate(layers):
        for y in range(24):
            for x in range(16):
                ch = g[y][x]
                if ch == "_":
                    comp[y][x], owner[y][x] = ".", 0
                elif ch not in ".x":
                    comp[y][x], owner[y][x] = ch, i
    for x in range(3, 13):
        if comp[23][x] == ".":
            comp[23][x] = "x"
    grid = ["".join(r) for r in comp]
    renders = [B.render(grid, "object", fg=fg, detail=dt) for _, fg, dt in layers]
    out = renders[0].copy()
    px = out.load()
    for y in range(24):
        for x in range(16):
            if comp[y][x] not in ".x":
                px[x, y] = renders[owner[y][x]].getpixel((x, y))
    return out


def tint(img, rgb, k=0.75):
    """Liquid coating: every solid pixel pulled toward the liquid colour, shading kept."""
    out = img.copy()
    px = out.load()
    for y in range(24):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a < 255 or (r + g + b) < 60:
                continue
            lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            t = tuple(round(c * (0.45 + lum * 0.9)) for c in rgb)
            px[x, y] = tuple(round(o * (1 - k) + n * k) for o, n in zip((r, g, b), t)) + (a,)
    return out


BODY = K.person(face="face", sash=False)
PLAIN = K.person(face="face")


def body(**kw):
    return K.person(**kw)


# ---------------------------------------------------------------- proposed mutation shapes

def shell_back():
    """Carapace as a domed chitin shell behind the back: pale rim over the shoulders, banded plates
    showing on both sides of the body (fixed chitin colours, never the clothes' colours)."""
    c = K.C()
    c.ell(7.5, 13.5, 7.4, 8.2, "n")
    for y in (10, 13, 16, 19):
        c.r(0, y, 15, y, "N")
    c.ell(7.5, 6.8, 4.2, 1.6, "t")
    c.ell(7.5, 7.2, 3.2, 1.0, "n")
    g = c.out()
    return [row if y >= 5 else "." * 16 for y, row in enumerate(g)]


def front_legs():
    """Two jointed chitin legs stepping out in front, at both sides of the hem."""
    c = K.C()
    for x0, d in ((3, -1), (12, 1)):
        c.r(x0 + d, 17, x0 + 2 * d, 18, "N")
        c.r(x0 + 2 * d, 19, x0 + 2 * d, 21, "N")
        c.p(x0 + 2 * d, 22, "O")
        c.p(x0 + 2 * d - d, 22, "O")
        c.p(x0 + d, 17, "t")
    return c.out()


def upper_arms():
    """Second pair of arms raised from the shoulders, bare skin, sleeves in the body colour."""
    c = K.C()
    c.r(2, 9, 3, 10, "2"); c.r(12, 9, 13, 10, "3")
    c.r(1, 6, 2, 8, "s"); c.r(13, 6, 14, 8, "S")
    c.p(1, 5, "s"); c.p(14, 5, "S")
    return c.out()


def horns_bone():
    c = K.C()
    c.mr(4, 2, 4, 3, "w")
    c.mr(3, 1, 3, 1, "w")
    c.mr(3, 2, 3, 2, "t")
    return c.out()


def today_mutant():
    g = K.person(face="face")
    for name in ("Carapace", "MultipleArms", "MultipleLegs"):
        _, ov = K.MUTATIONS[name]
        g = ["".join(b if b != "." else a for a, b in zip(row, ov.get(y, "." * 16))) for y, row in enumerate(g)]
    return g


# ---------------------------------------------------------------- the sheet

def figures():
    leather = [(body(face="face", sash=False), "w", "w"), (part(K.cap), "w", "y"), (part(K.pistol), "c", "w")]
    # material table: chain/steel -> our steel greys (the game colours chain mail plain white)
    chain = [(body(face="face", sash=False, body="l", lite="w", dark="L", trim="L"), "y", "Y"), (part(K.helmet), "Y", "y"),
             (part(K.shield, a="L", b="l", rim="O"), "Y", "y"), (part(K.sword), "Y", "y")]
    carbide = [(body(face="mask", sash=False, trim="4", goggles="g"), "b", "K"), (part(K.armor, METAL), "b", "B"),
               (part(K.rifle, METAL), "C", "w")]
    robe = [(body(face="face"), "m", "y"), (part(K.hood), "m", "M"), (part(K.staff, head="gem"), "w", "Y")]
    today = [(PLAIN, "Y", "y")]
    row1 = [("today: any NPC/you\n(gear doesn't show)", doll(today)),
            ("leather armour + cap\n+ chain pistol", doll(leather)),
            ("chain mail + steel helm\n+ long sword + buckler", doll(chain)),
            ("carbide plate + gas mask\n+ laser rifle", doll(carbide)),
            ("painted silk robe + hood\n+ staff", doll(robe))]
    base = doll(chain)
    row2 = [("chain-mail fighter", base), ("slimed: all green", tint(base, (90, 210, 70))),
            ("bloody", tint(base, (200, 40, 40), 0.6)), ("oily", tint(base, (40, 36, 44), 0.7)),
            ("frozen", tint(base, (150, 220, 255), 0.6))]
    mut_layers = [(shell_back(), "w", "W"), (body(face="face", sash=False), "w", "w"), (upper_arms(), "w", "w"),
                  (front_legs(), "w", "w"), (horns_bone(), "w", "w"), (part(K.pistol), "c", "w")]
    row3 = [("TODAY: arms + legs\n+ carapace (white blob)", B.render(today_mutant(), "object", fg="Y", detail="y")),
            ("PROPOSAL: shell on the\nback, legs in front", doll(mut_layers[:4] + mut_layers[5:])),
            ("+ horns\n(bone, fixed colour)", doll(mut_layers)),
            ("same body in chain\nmail + helm", doll([mut_layers[0],
                                                     (body(face="face", sash=False, body="l", lite="w", dark="L", trim="L"), "y", "Y"),
                                                     (upper_arms(), "y", "Y"), mut_layers[3],
                                                     (part(K.helmet), "Y", "y"), (part(K.sword), "Y", "y")]))]
    return [("1. Gear shows on the body, coloured by the item's own material", row1),
            ("2. A coating overrides everything", row2),
            ("3. Mutations give the shape, gear sits on top", row3)]


def main():
    rows = figures()
    cw, ch = 16 * Z, 24 * Z
    colw = 32 * Z + 60
    W = 30 + 5 * colw
    rowh = 40 + ch + 60
    img = Image.new("RGB", (W, 20 + len(rows) * rowh), (26, 26, 30))
    d = ImageDraw.Draw(img)
    for r, (title, items) in enumerate(rows):
        y = 20 + r * rowh
        d.text((20, y), title, font=font(20), fill=(240, 232, 205))
        for i, (label, tile) in enumerate(items):
            x = 20 + i * colw
            cell = Image.new("RGBA", (16 * 3, 24), GROUND + (255,))
            cell.alpha_composite(tile, (16, 0))
            big = cell.crop((8, 0, 40, 24)).resize((32 * Z, 24 * Z), Image.NEAREST)
            img.paste(big.convert("RGB"), (x, y + 32))
            for j, line in enumerate(label.split("\n")):
                d.text((x + 6, y + 40 + ch + j * 17), line, font=font(14), fill=(205, 200, 185))
    os.makedirs(OUT, exist_ok=True)
    p = os.path.join(OUT, "paperdoll_concept.png")
    img.save(p)
    print(p)


if __name__ == "__main__":
    main()
