"""Lake Hinnom: today (solid green) against the new algal water (Palladium's blue water with strands of algae).
Keep STRANDS in sync with Recolor.Strands in BrightQud.cs. Local output only.

Usage: .venv/bin/python -I tools/review_hinnom.py <out.png>
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "art", "src")]
from PIL import Image  # noqa: E402
import colors as C  # noqa: E402

STRANDS = [[(2, 4, 4), (10, 9, 3), (4, 15, 5), (12, 19, 1), (7, 1, 1)],
           [(9, 2, 5), (1, 8, 3), (11, 14, 3), (3, 20, 4), (6, 12, 1)],
           [(5, 6, 4), (12, 3, 1), (1, 13, 4), (9, 17, 5), (13, 11, 1)],
           [(0, 2, 3), (7, 7, 5), (2, 18, 3), (10, 21, 4), (4, 11, 1)]]
TEX = os.path.join(ROOT, "mod/BrightQud/Textures")


def tile(fg, strands=None):
    name = "liquids_water_deep-11111111.png"
    im = Image.open(os.path.join(TEX, name)).convert("RGBA")
    mask = Image.open(os.path.join(TEX, "BrightQudMask", name)).convert("RGBA")
    a, m = im.load(), mask.load()
    for y in range(24):
        for x in range(16):
            if m[x, y][3] > 127:
                r, g, b = C.ramp(fg, round(m[x, y][1] / 127))
                a[x, y] = (r, g, b, a[x, y][3])
    for s in strands or []:
        for i in range(s[2]):
            x, row = s[0] + i, s[1] + (i // 2) % 2
            if x < 16 and row < 24:
                a[x, row] = C.hex_rgb("4f9a55" if i == 1 else "377a4c") + (255,)
    return im


def lake(fg, specks):
    W, H, Z = 13, 6, 3
    out = Image.new("RGB", (W * 16, H * 24))
    for y in range(H):
        for x in range(W):
            h = ((x * 73856093) ^ (y * 19349663)) & 0x7fffffff
            out.paste(tile(fg, STRANDS[h % 4] if specks else None), (x * 16, y * 24))
    return out.resize((W * 16 * Z, H * 24 * Z), Image.NEAREST)


if __name__ == "__main__":
    a = lake(C.hex_rgb("3fae3a"), False)
    b = lake(C.hex_rgb("3a8fb4"), True)
    sheet = Image.new("RGB", (a.width * 2 + 12, a.height), (20, 20, 20))
    sheet.paste(a, (0, 0))
    sheet.paste(b, (a.width + 12, 0))
    sheet.save(sys.argv[1])
