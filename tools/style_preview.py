"""Render a style-exploration module (art/src/style_*.py) as a lineup, for review.

Usage: .venv/bin/python -I tools/style_preview.py <module> <out.png>

The module must define CHARACTERS = {name: 24 rows of 16 chars} for every name in ROSTER.
Each sprite is rendered with the real pipeline (style C: outline + drop shadow) in the demo colors
below, on the outdoor ground color, at 6x zoom, with its name. Grid problems are printed as ERROR.
"""
import importlib, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
from mockup import font  # noqa: E402
from preview_sprites import check  # noqa: E402

EARTH = (0x3b, 0x33, 0x26)
# name: (fg letter, detail letter, what it is)
ROSTER = {
    "gunslinger": ("w", "y", "player mutant: wide hat, long coat, a pistol in each hand"),
    "winged": ("B", "W", "mutant with big feathered wings"),
    "horned": ("r", "Y", "mutant with large horns"),
    "four_arms": ("g", "w", "mutant with four arms"),
    "carapace": ("c", "C", "mutant with a hard shell/carapace on back and shoulders"),
    "mehmet": ("w", "g", "village elder farmer, beard, hoe"),
    "farmer": ("g", "w", "watervine farmer, simple clothes, sickle"),
    "snapjaw": ("w", "r", "snapjaw: hyena-headed humanoid scavenger"),
    "snapjaw_hunter": ("w", "g", "snapjaw hunter with a bow"),
    "glowfish": ("C", "Y", "glowing fish"),
    "girshling": ("M", "K", "girshling: small many-legged spider/solifuge"),
    "dog": ("w", "y", "dog"),
    "salthopper": ("y", "w", "salthopper: big grasshopper"),
    "croc": ("g", "w", "crocodile"),
}


def render_all(mod):
    m = importlib.import_module(mod)
    chars = m.CHARACTERS
    out, errors = {}, []
    for name, (fg, det, _) in ROSTER.items():
        if name not in chars:
            errors.append(f"{name}: missing")
            continue
        errs = check(name, chars[name])
        if errs:
            errors += errs
            continue
        out[name] = B.render(chars[name], "object", fg=fg, detail=det)
    return out, errors


def main():
    mod, path = sys.argv[1:3]
    tiles, errors = render_all(mod)
    cols = 7
    sheet = Image.new("RGB", (cols * 104 + 8, 2 * 168 + 8), (30, 30, 34))
    d = ImageDraw.Draw(sheet)
    for i, name in enumerate(ROSTER):
        if name not in tiles:
            continue
        cell = Image.new("RGBA", (16, 24), EARTH + (255,))
        cell.alpha_composite(tiles[name])
        x, y = 8 + (i % cols) * 104, 8 + (i // cols) * 168
        sheet.paste(cell.resize((96, 144), Image.NEAREST), (x, y))
        d.text((x, y + 146), name, fill=(230, 230, 230), font=font(12))
    sheet.save(path)
    print(f"{len(tiles)} sprites -> {path}")
    for e in errors:
        print("ERROR", e)


if __name__ == "__main__":
    main()
