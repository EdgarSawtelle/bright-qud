"""Preview a B3 restyle module (art/src/b3_*.py) next to the sprites it replaces.

Usage: .venv/bin/python -I tools/b3_preview.py <module> <out.png>

The module defines OVERRIDES = {group: {sprite name: grid}} (groups and names: art/src/b3keys.py).
Each pair (old | new) is rendered with the real pipeline in the colors of the first game object that
uses the sprite's tile, on the outdoor ground, at 4x. Grid problems print as ERROR lines.
Optional: MUTATIONS = {name: (layer, overlay rows)} are shown composited on the B3 humanoid
`b3kit.person()` when the module is b3kit.
"""
import importlib, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
from build_mod import color_letters, users_by_key  # noqa: E402
from b3_worklist import GROUPS  # noqa: E402
from b3keys import KEYS  # noqa: E402
from mockup import font  # noqa: E402
from preview_sprites import check  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from tile_priority import add_random_tiles  # noqa: E402

EARTH = (0x3b, 0x33, 0x26)
Z = 4


def cell(img):
    c = Image.new("RGBA", (16, 24), EARTH + (255,))
    c.alpha_composite(img)
    return c.resize((16 * Z, 24 * Z), Image.NEAREST)


def main():
    mod, path = sys.argv[1:3]
    m = importlib.import_module(mod)
    bp = Blueprints()
    add_random_tiles(bp)
    users = users_by_key(bp)
    items, errors = [], []
    for group, sprites in getattr(m, "OVERRIDES", {}).items():
        if group not in KEYS:
            errors.append(f"unknown group {group}")
            continue
        for name, grid in sprites.items():
            if name not in KEYS[group]:
                errors.append(f"{group}: unknown sprite name {name}")
                continue
            errs = check(name, grid)
            if errs:
                errors += errs
                continue
            ex = next((sorted(users[k])[0] for k in KEYS[group][name] if users.get(k)), None)
            fg, det = color_letters(bp, ex) if ex else ("y", "w")
            old = B.render(GROUPS[group][name], "object", fg=fg, detail=det)
            new = B.render(grid, "object", fg=fg, detail=det)
            items.append((name.split("/")[-1] if group != "castes" else name.replace("creatures/", ""), old, new))
    muts = getattr(m, "MUTATIONS", None)
    if muts and hasattr(m, "person"):
        from kit import compose, E
        base = m.person()
        for name, (layer, ov) in muts.items():
            o = compose([E] * 24, ov)
            if layer == "back":
                g = [''.join(b if b != "." else a for a, b in zip(orow, brow)) for orow, brow in zip(o, base)]
            else:
                g = compose(base, {y: r for y, r in enumerate(o)})
            errs = check(name, g)
            if errs:
                errors += errs
                continue
            items.append((name, B.render(base, "object", fg="y", detail="w"), B.render(g, "object", fg="y", detail="w")))
    cols = 6
    w, h = (2 * 16 * Z + 12), (24 * Z + 22)
    rows = max(1, -(-len(items) // cols))
    sheet = Image.new("RGB", (cols * w + 8, rows * h + 8), (30, 30, 34))
    d = ImageDraw.Draw(sheet)
    for i, (name, old, new) in enumerate(items):
        x, y = 8 + (i % cols) * w, 8 + (i // cols) * h
        sheet.paste(cell(old), (x, y))
        sheet.paste(cell(new), (x + 16 * Z + 2, y))
        d.text((x, y + 24 * Z + 2), name[:22], fill=(230, 230, 230), font=font(12))
    sheet.save(path)
    print(f"{len(items)} sprites (old | new) -> {path}")
    for e in errors:
        print("ERROR", e)


if __name__ == "__main__":
    main()
