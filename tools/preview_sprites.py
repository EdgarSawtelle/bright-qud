"""Preview sprites from an art module before they're wired into the build (used by art agents).

Usage: .venv/bin/python -I tools/preview_sprites.py <module> <SPRITES_DICT> <KEYS_DICT> <out.png>
  module       art/src module name, e.g. items3
  SPRITES_DICT name of the dict {sprite name: 24 rows of 16 chars}
  KEYS_DICT    name of the dict {game tile key: sprite name | (sprite name, kind)}

Each sprite is rendered with the real pipeline (build_tiles.render, style C) in the colors of the
first game object that uses its tile key, on the outdoor ground color, at 6x zoom, with its name.
It also validates every grid (24 rows x 16 chars, known characters) and prints problems.
"""
import importlib, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
import colors as C  # noqa: E402
import palette as P  # noqa: E402
from build_mod import color_letters, users_by_key  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from tile_priority import add_random_tiles  # noqa: E402
from mockup import font  # noqa: E402

EARTH = (0x3b, 0x33, 0x26)
VALID = set(P.PALETTE) | set(C.ROLE_DIGITS) | {".", "x"}


def check(name, grid):
    errs = []
    if len(grid) != 24:
        errs.append(f"{name}: {len(grid)} rows (need 24)")
    for i, r in enumerate(grid):
        if len(r) != 16:
            errs.append(f"{name}: row {i} has {len(r)} chars (need 16): {r!r}")
        bad = set(r) - VALID
        if bad:
            errs.append(f"{name}: row {i} unknown chars {sorted(bad)}")
    return errs


def main():
    mod, sprites_name, keys_name, out = sys.argv[1:5]
    m = importlib.import_module(mod)
    sprites, keys = getattr(m, sprites_name), getattr(m, keys_name)
    bp = Blueprints()
    add_random_tiles(bp)
    users = users_by_key(bp)
    errors, cells = [], []
    seen = set()
    for k, v in keys.items():
        name, kind = (v if isinstance(v, tuple) else (v, "object"))
        kind = getattr(m, "KINDS", {}).get(name, kind)
        if name in seen:
            continue
        seen.add(name)
        if name not in sprites:
            errors.append(f"{k}: sprite {name!r} missing")
            continue
        errs = check(name, sprites[name])
        errors += errs
        if errs:
            continue
        ex = (sorted(users.get(k, [])) or [None])[0]
        fg, det = color_letters(bp, ex) if ex else ("y", "w")
        img = B.render(sprites[name], kind, fg=fg, detail=det)
        cell = Image.new("RGBA", (16, 24), EARTH + (255,))
        cell.alpha_composite(img)
        cells.append((f"{name} ({fg}/{det})", cell.resize((96, 144), Image.NEAREST)))
    cols = 8
    rows = max(1, (len(cells) + cols - 1) // cols)
    sheet = Image.new("RGB", (cols * 104 + 8, rows * 168 + 8), (30, 30, 34))
    d = ImageDraw.Draw(sheet)
    for i, (label, c) in enumerate(cells):
        x, y = 8 + (i % cols) * 104, 8 + (i // cols) * 168
        sheet.paste(c, (x, y))
        d.text((x, y + 146), label[:16], fill=(230, 230, 230), font=font(12))
    sheet.save(out)
    print(f"{len(cells)} sprites -> {out}")
    for e in errors:
        print("ERROR", e)


if __name__ == "__main__":
    main()
