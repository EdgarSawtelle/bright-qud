"""Re-does Doll.Compose + Recolored (mod/BrightQud/Doll.cs, BrightQud.cs) on the BUILT textures, to check the
build output stacks right before installing. Usage: .venv/bin/python -I tools/doll_runtime_check.py <out.png>"""
import os, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image  # noqa: E402
from colors import ramp, brighten, hex_rgb  # noqa: E402

TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")
INK = (0x10, 0x14, 0x1f)


def recolored(key, fg, det):
    flat = key.replace("/", "_") + ".png"
    base = Image.open(os.path.join(TEX, flat)).convert("RGBA")
    mask = Image.open(os.path.join(TEX, "BrightQudMask", flat)).convert("RGBA")
    bp, mp = base.load(), mask.load()
    for y in range(24):
        for x in range(16):
            mr, mg, _, ma = mp[x, y]
            if ma > 127:
                bp[x, y] = ramp(brighten(fg if mr < 150 else det), round(mg / 127)) + (bp[x, y][3],)
    return base


def compose(desc):
    body = desc[len("brightqudpaperdoll|"):]
    coat = None
    if "|c" in body:
        body, coat = body.split("|c")
    img = Image.new("RGBA", (16, 24))
    for entry in body.split(";"):
        key, f, d = entry.split(",")
        mirror = key.startswith("offhand/")
        if mirror:
            key = "right/" + key[8:]
        lay = recolored("brightquddoll/" + key, hex_rgb(f), hex_rgb(d))
        if mirror:
            lay = lay.transpose(Image.FLIP_LEFT_RIGHT)
        img.alpha_composite(lay)
    px = img.load()
    solid = {(x, y) for y in range(24) for x in range(16) if px[x, y][3] > 127}
    out = img.copy()
    op = out.load()
    for x, y in solid:  # drop shadow down-right, then ink outline (Stylize)
        for k in (1, 2):
            if (x + k, y + k) not in solid and x + k < 16 and y + k < 24:
                op[x + k, y + k] = INK + (110,)
    for x, y in solid:
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                n = (x + dx, y + dy)
                if n not in solid and 0 <= n[0] < 16 and 0 <= n[1] < 24:
                    op[n] = INK + (255,)
    for x in range(3, 13):
        if op[x, 23][3] == 0:
            op[x, 23] = (15, 20, 31, 120)
    return out


DESCS = [
    "brightqudpaperdoll|body/base,d8c8a0,9a8a68;feet/boots,a06a3a,5a3a1e;body/leather,a06a3a,5a3a1e;head/cap,a06a3a,5a3a1e;right/pistol,40a4b9,98875f",
    "brightqudpaperdoll|back/cloak,155352,b1c9c3;body/base,d8c8a0,9a8a68;body/tunic,a64a2e,cfc041;face/goggles,c08a48,7a5428;head/hat,98875f,cfc041;right/pistol,ffffff,40a4b9;offhand/pistol,ffffff,40a4b9",
    "brightqudpaperdoll|mutback/carapace,4a52b8,c8402e;body/base,d8c8a0,9a8a68;body/chain,a8b0b8,5c6470;mutfront/arms,a8b0b8,5c6470;mutfront/legs,4a52b8,c8402e;face/earth_face,0096ff,155352;muthead/horns,ffffff,b1c9c3;right/sword,a8b0b8,5c6470",
    "brightqudpaperdoll|body/base,d8c8a0,9a8a68;body/chain,a8b0b8,5c6470;head/helmet,a8b0b8,5c6470;left/shield,a8b0b8,5c6470;right/sword,a8b0b8,5c6470",
]

if __name__ == "__main__":
    sheet = Image.new("RGBA", (len(DESCS) * 40 * 6, 24 * 6), (0x6e, 0x5c, 0x42, 255))
    for i, d in enumerate(DESCS):
        sheet.alpha_composite(compose(d).resize((96, 144), Image.NEAREST), (i * 240 + 60, 0))
    sheet.save(sys.argv[1])
    print(sys.argv[1])
