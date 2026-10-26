"""Paper doll preview: real loadouts stacked from the doll layers (art/src/doll_*.py), each layer in its
item's own colours (material table for metals etc.). Used by art agents and for user mockups.

Usage: .venv/bin/python -I tools/doll_preview.py <out.png> [--big]
Layers that don't exist yet are skipped. Brief: docs/PAPERDOLL_BRIEF.md.
"""
import importlib, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
import colors as C  # noqa: E402
from mockup import font  # noqa: E402
from preview_sprites import check  # noqa: E402

from doll_palette import ORDER, MATERIALS, CHITIN, CHITIN_LAYERS, CHITIN_ROLES  # noqa: E402


def col(c):
    """'steel' (material), 'w' (game colour letter) or 'a0b0c0' (hex) -> rgb."""
    if c in MATERIALS:
        return C.hex_rgb(MATERIALS[c][0])
    if len(c) == 1:
        return C.brighten(C.hex_rgb(C.QUD[c]))
    return C.hex_rgb(c)


def pair(spec):
    """'steel' -> both material colours; ('w', 'y') -> game letters/hex."""
    if isinstance(spec, str):
        m = MATERIALS[spec]
        return C.hex_rgb(m[0]), C.hex_rgb(m[1])
    return col(spec[0]), col(spec[1])


def load_layers():
    layers, errors = {}, []
    for mod in ("doll_base", "doll_body", "doll_gear", "doll_weapons", "doll_mutations", "doll_specials"):
        try:
            m = importlib.import_module(mod)
        except ModuleNotFoundError:
            continue
        for k, g in getattr(m, "LAYERS", {}).items():
            errs = check(k, g)
            if errs:
                errors += errs
            else:
                layers[k] = g
    return layers, errors


def mirror(g):
    return [row[::-1] for row in g]


def rank(key):
    if key == "body/base":
        return ORDER.index("body/base")
    return ORDER.index(key.split("/")[0])


def stack(layers, loadout, chitin=None):
    """loadout: [(layer key, colour spec)] -> RGBA tile. 'offhand/<piece>' mirrors right/<piece>.
    chitin: (shell hex, legs hex) recolours the shell/legs/stinger's fixed chitin letters."""
    items = []
    for key, spec in loadout:
        g = layers.get(key)
        if chitin and key in CHITIN_LAYERS and g:
            g = ["".join(CHITIN_ROLES.get(ch, ch) for ch in row) for row in g]
            spec = chitin
        if key.startswith("offhand/"):
            g = layers.get("right/" + key.split("/", 1)[1])
            g = mirror(g) if g else None
        if g is not None:
            items.append((rank(key), key, g, pair(spec)))
    items.sort(key=lambda t: t[0])
    comp = [["."] * 16 for _ in range(24)]
    owner = [[None] * 16 for _ in range(24)]
    for _, _, g, cols in items:
        for y in range(24):
            for x in range(16):
                ch = g[y][x]
                if ch not in ".x_":
                    comp[y][x], owner[y][x] = ch, cols
    for x in range(3, 13):
        if comp[23][x] == ".":
            comp[23][x] = "x"
    grid = ["".join(r) for r in comp]
    img = B.render(grid, "object", fg="y", detail="y")
    px = img.load()
    for y in range(24):
        for x in range(16):
            ch = comp[y][x]
            if ch in C.ROLE_DIGITS:
                which, shade = C.ROLE_DIGITS[ch]
                fg, det = owner[y][x]
                px[x, y] = C.ramp(fg if which == "fg" else det, shade) + (255,)
    return img


def coat(img, rgb, k=0.75):
    out = img.copy()
    px = out.load()
    for y in range(24):
        for x in range(16):
            r, g, b, a = px[x, y]
            if a < 255 or r + g + b < 60:
                continue
            lum = (0.3 * r + 0.59 * g + 0.11 * b) / 255
            t = tuple(round(c * (0.45 + lum * 0.9)) for c in rgb)
            px[x, y] = tuple(round(o * (1 - k) + n * k) for o, n in zip((r, g, b), t)) + (a,)
    return out


BASE = [("body/base", "linen")]
LOADOUTS = [
    ("bare (no gear)", BASE),
    ("leather armour, cap,\nboots, chain pistol", BASE + [("body/leather", "leather"), ("head/cap", "leather"),
                                                         ("feet/boots", "leather"), ("right/pistol", ("c", "w"))]),
    ("chain mail, steel helm,\nlong sword, buckler", BASE + [("body/chain", "steel"), ("head/helmet", "steel"),
                                                             ("feet/boots", "steel"), ("right/sword", "steel"),
                                                             ("left/shield", "steel")]),
    ("carbide plate, gas mask,\ngauntlets, laser rifle", BASE + [("body/plate", "carbide"), ("face/mask", ("G", "K")),
                                                                 ("hands/gauntlets", "carbide"), ("two/rifle", ("C", "w"))]),
    ("silk robe, wreath,\nsandals, staff", BASE + [("body/robe", ("m", "W")), ("head/crown", "wood"),
                                                  ("feet/sandals", "leather"), ("right/staff", "wood")]),
    ("furs, fur hat, cloak,\nbattle axe (2-handed)", BASE + [("body/fur", "fur"), ("head/hat", "fur"),
                                                            ("back/cloak", "leather"), ("two/axe", "iron")]),
    ("gunslinger: hat, goggles,\ntunic, cloak, 2 pistols", BASE + [("body/tunic", ("r", "W")), ("head/hat", ("w", "W")),
                                                                   ("face/goggles", "bronze"), ("back/cloak", ("K", "y")),
                                                                   ("right/pistol", ("Y", "c")), ("offhand/pistol", ("Y", "c"))]),
    ("tinker: techhelm, pack,\napron, hammer", BASE + [("body/leather", "leather"), ("head/techhelm", ("y", "C")),
                                                     ("back/pack", ("w", "W")), ("right/hammer", "steel"),
                                                     ("hands/gloves", "leather")]),
    ("MUTANT: carapace, arms,\nlegs, horns + leather, pistol", BASE + [("mutback/carapace", ("w", "W")),
                                                                      ("mutfront/arms", "linen"), ("mutfront/legs", ("w", "W")),
                                                                      ("muthead/horns", ("Y", "y")), ("body/leather", "leather"),
                                                                      ("right/pistol", ("c", "w"))]),
    ("MUTANT 2: wings, beak,\nquills + robe, bow", BASE + [("mutback/wings", ("Y", "C")), ("mutfront/beak", ("W", "y")),
                                                         ("mutback/quills", ("Y", "y")), ("body/robe", ("b", "Y")),
                                                         ("two/bow", "wood")]),
    ("MUTANT 3: two heads,\nclaws, stinger + plate", BASE + [("mutfront/twoheads", "linen"), ("mutfront/claws", ("Y", "y")),
                                                            ("mutback/stinger", ("r", "R")), ("body/plate", "bronze")]),
]
COATS = [("slimed", (90, 210, 70), 0.75), ("bloody", (200, 40, 40), 0.6), ("frozen", (150, 220, 255), 0.6)]


def specials():
    """--specials: every piece listed in docs/doll_specials_facehead.md, in its game colours, on a tunic body."""
    import re
    rows = []
    for line in open(os.path.join(ROOT, "docs", "doll_specials_facehead.md")):
        m = re.match(r"\| `([^`]+)` \| ([^|]+) \|[^|]*\| &(\w)/(\S+) \|", line)
        if m:
            det = m.group(4) if m.group(4) in C.QUD else "y"
            rows.append((m.group(1), m.group(2).strip(), m.group(3), det))
    return [(f"{name[:24]}", BASE + [("body/tunic", "linen"), (key, (fg, det))]) for key, name, fg, det in rows]


def main():
    out = sys.argv[1]
    z = 6 if "--big" in sys.argv else 5
    layers, errors = load_layers()
    if "--chitin" in sys.argv:
        mutant = LOADOUTS[8][1]
        knight = BASE + [("mutback/carapace", None), ("mutfront/arms", "linen"), ("mutfront/legs", None),
                         ("body/chain", "steel"), ("head/helmet", "steel"), ("right/sword", "steel"), ("mutback/stinger", None)]
        tiles = [(f"{n}", stack(layers, mutant, (a, b))) for n, a, b in CHITIN]
        tiles += [(f"{n} (chain mail)", stack(layers, knight, (a, b))) for n, a, b in CHITIN]
        return sheet(out, z, tiles, layers, errors)
    if "--specials" in sys.argv:
        tiles = [(label, stack(layers, lo)) for label, lo in specials()]
        return sheet(out, z, tiles, layers, errors)
    tiles = [(label, stack(layers, lo)) for label, lo in LOADOUTS]
    chain = stack(layers, LOADOUTS[2][1])
    tiles += [(name, coat(chain, rgb, k)) for name, rgb, k in COATS]
    sheet(out, z, tiles, layers, errors)


def sheet(out, z, tiles, layers, errors):
    cols = 6
    cw, ch = 32 * z, 24 * z
    W, H = cols * (cw + 24) + 16, ((len(tiles) + cols - 1) // cols) * (ch + 60) + 16
    sheet = Image.new("RGB", (W, H), (26, 26, 30))
    d = ImageDraw.Draw(sheet)
    for i, (label, t) in enumerate(tiles):
        x, y = 16 + (i % cols) * (cw + 24), 16 + (i // cols) * (ch + 60)
        cell = Image.new("RGBA", (32, 24), (0x6e, 0x5c, 0x42, 255))
        cell.alpha_composite(t, (8, 0))
        sheet.paste(cell.resize((cw, ch), Image.NEAREST).convert("RGB"), (x, y))
        for j, line in enumerate(label.split("\n")):
            d.text((x, y + ch + 4 + j * 16), line, font=font(13), fill=(210, 205, 190))
    sheet.save(out)
    print(f"{len(layers)} layers, {len(tiles)} figures -> {out}")
    for e in errors:
        print("ERROR", e)


if __name__ == "__main__":
    main()
