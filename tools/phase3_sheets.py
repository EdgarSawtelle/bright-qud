"""Contact sheets of the ORIGINAL tiles proposed for each Phase 3 batch (local review only:
they contain extracted game art and must not be shared).

Usage: .venv/bin/python -I tools/phase3_sheets.py -> mockups/phase3_batch<N>_originals.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from PIL import Image, ImageDraw  # noqa: E402
from phase3_batches import BATCHES  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from tile_priority import key  # noqa: E402
from mockup import font  # noqa: E402

REF = os.path.join(ROOT, "reference", "tiles")
QUD = {"r": "a64a2e", "R": "d74200", "o": "f15f22", "O": "e99f10", "w": "98875f", "W": "cfc041",
       "g": "009403", "G": "00c420", "b": "0048bd", "B": "0096ff", "c": "40a4b9", "C": "77bfcf",
       "m": "b154cf", "M": "da5bd6", "k": "0f3b3a", "K": "155352", "y": "b1c9c3", "Y": "ffffff"}


def rgb(letter):
    h = QUD.get(letter, "b1c9c3")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


def index():
    out = {}
    for f in os.listdir(REF):
        out.setdefault(key(f[:-4]), f)
    return out


def find(idx, k):
    if k.endswith("-*"):  # painted family: show the isolated variant
        k = k[:-2] + "-00000000"
    return idx.get(k)


def colors(bp, obj):
    cs = bp.part(obj, "Render", "ColorString") or "&y"
    tc = bp.part(obj, "Render", "TileColor")
    fg = (tc or cs).split("&")[-1][:1] if "&" in (tc or cs) else "y"
    bg = cs.split("^")[-1][:1] if "^" in cs else "k"
    det = (bp.part(obj, "Render", "DetailColor") or fg)[:1]
    return rgb(fg), rgb(det), rgb(bg)


def three_color(path, fg, det, bg, scale=3):
    src = Image.open(path).convert("RGBA")
    out = Image.new("RGB", src.size)
    sp, op = src.load(), out.load()
    for y in range(src.height):
        for x in range(src.width):
            r, _, _, a = sp[x, y]
            t, al = r / 255, a / 255
            op[x, y] = tuple(round((f * (1 - t) + d * t) * al + b * (1 - al)) for f, d, b in zip(fg, det, bg))
    return out.resize((src.width * scale, src.height * scale), Image.NEAREST)


NEW = os.path.join(ROOT, "mod", "BrightQud", "Textures")


def new_tile(k, bg=(0x3b, 0x33, 0x26), scale=3):
    if k.endswith("-*"):
        k = k[:-2] + "-00000000"
    path = os.path.join(NEW, k.replace("/", "_") + ".png")
    if not os.path.exists(path):
        return None
    t = Image.open(path).convert("RGBA")
    cell = Image.new("RGBA", t.size, bg + (255,))
    cell.alpha_composite(t)
    return cell.convert("RGB").resize((t.width * scale, t.height * scale), Image.NEAREST)


def main():
    bp = Blueprints()
    idx = index()
    missing = []
    for n, (title, items) in enumerate(BATCHES, 1):
        cols, cw, ch = 5, 300, 96
        rows = (len(items) + cols - 1) // cols
        sheet = Image.new("RGB", (cols * cw + 20, rows * ch + 60), (30, 30, 34))
        d = ImageDraw.Draw(sheet)
        d.text((10, 12), f"Batch {title}  -  original (left) vs Bright Qud (right). Local only.",
               fill=(240, 240, 240), font=font(20))
        for i, (label, k, obj) in enumerate(items):
            x, y = 10 + (i % cols) * cw, 50 + (i // cols) * ch
            f = find(idx, k)
            if f:
                sheet.paste(three_color(os.path.join(REF, f), *colors(bp, obj)), (x, y))
            else:
                missing.append(k)
                d.rectangle((x, y, x + 47, y + 71), outline=(200, 60, 60))
            nt = new_tile(k)
            if nt:
                sheet.paste(nt, (x + 52, y))
            tx = x + 104
            d.text((tx, y + 6), f"{i + 1}.", fill=(150, 155, 160), font=font(14))
            words, line, lines = label.split(), "", []
            for w in words:
                if len(line + " " + w) > 20:
                    lines.append(line)
                    line = w
                else:
                    line = (line + " " + w).strip()
            lines.append(line)
            for j, ln in enumerate(lines[:4]):
                d.text((tx, y + 24 + j * 16), ln, fill=(225, 225, 225), font=font(14))
        sheet.save(os.path.join(ROOT, "mockups", f"phase3_batch{n}_compare.png"))
    print("missing:", missing or "none")


if __name__ == "__main__":
    main()
