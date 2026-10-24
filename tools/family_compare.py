"""Original | Bright Qud now | new draft, for the family redraw modules (art/src/fam_*.py), in the game's
colours of one example creature per tile. Uses vanilla tiles, so output stays local.

Usage: .venv/bin/python -I tools/family_compare.py fam_frogs fam_reptiles fam_templars
  -> mockups/local/zones/<module>_compare.png
"""
import importlib, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import build_tiles as B  # noqa: E402
from build_mod import color_letters, users_by_key  # noqa: E402
from mockup import font  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from zone_mockup import vanilla, ours, q, OUT  # noqa: E402

S = 5
BG = (0x3B, 0x33, 0x26)


def cell(t, bg):
    c = Image.new("RGBA", (16, 24), bg + (255,))
    if t is not None:
        c.alpha_composite(t)
    return c.convert("RGB").resize((16 * S, 24 * S), Image.NEAREST)


def main():
    bp = Blueprints()
    users = users_by_key(bp)
    for mod_name in sys.argv[1:]:
        m = importlib.import_module(mod_name)
        rows = []
        for k, v in m.KEYS.items():
            name = v if isinstance(v, str) else v[0]
            ex = users.get(k, [None])[0]
            fg, dt = color_letters(bp, ex) if ex else ("y", "w")
            disp = (bp.render(ex)["DisplayName"] if ex else None) or k
            fname = k.replace("/", "_")
            rows.append((disp, vanilla(fname, fg, dt), ours(fname, fg, dt), B.render(m.SPRITES[name], "object", fg=fg, detail=dt)))
        cols = 4
        cw = 3 * (16 * S + 6) + 24
        ch = 24 * S + 40
        w, h = 20 + cols * cw, 70 + ((len(rows) + cols - 1) // cols) * ch
        img = Image.new("RGB", (w, h), (24, 24, 28))
        d = ImageDraw.Draw(img)
        d.text((20, 16), f"{mod_name}: original | Bright Qud now | new draft", font=font(24), fill=(240, 236, 220))
        for i, (disp, a, b, c) in enumerate(rows):
            x, y = 20 + (i % cols) * cw, 60 + (i // cols) * ch
            for j, t in enumerate((a, b, c)):
                img.paste(cell(t, q("k") if j == 0 else BG), (x + j * (16 * S + 6), y))
            label = disp.split("|")[-1].strip("{}")[:34]
            d.text((x, y + 24 * S + 6), label, font=font(15), fill=(215, 210, 195))
        p = os.path.join(OUT, mod_name + "_compare.png")
        img.save(p)
        print(p)


if __name__ == "__main__":
    main()
