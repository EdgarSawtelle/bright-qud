"""Zone review #14 Six Day Stilt: the game's real map (StiltGroundFloor.rpm), cathedral crop, as the original game,
Bright Qud today and the proposal: the patterned cathedral floor as it is, light blue outer walls, white marble inside,
fluted columns with gold bands, distinct statues, a joined dais and a deep well. Local output only.

Usage: .venv/bin/python -I tools/review_stilt.py -> mockups/local/zones/review_stilt.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

BOX = (17, 0, 59, 25)
WALLS = {"SixDayStiltWall1": "concrete", "SixDayStiltWall2": "stiltmarble",
         "SixDayStiltPillarWall1": "stiltpillar", "SixDayStiltPillarWall2": "stiltpillar", "IronFence": "ironbars"}
TONES = {"concrete": (0x8f, 0xbc, 0xcb), "stiltmarble": (0xe6, 0xe1, 0xd4), "stiltpillar": (0xe6, 0xe1, 0xd4),
         "ironbars": (0x5c, 0x5e, 0x62)}
CYAN = {"Relief": (0xd2, 0xcd, 0xbf), "Marble Dais": (0xa4, 0xb9, 0xc6)}


def h(x, y):
    return ((x * 73856093) ^ (y * 19349663)) & 0x7fffffff


def swap(name, x, y, cells):
    """The game's StiltTile part shows its cathedral tiles (patterned floor, unchanged); walls joined N/E/S/W."""
    if name == "StiltTile":
        return f"terrain_sw_cathedral{1 + h(x, y) % 2}"
    if name not in WALLS:
        return None
    same = lambda dx, dy: any(WALLS.get(o) == WALLS[name] for o in cells.get((x + dx, y + dy), []))
    return f"brightqudwall_{WALLS[name]}-" + "".join("1" if same(*d) else "0" for d in ((0, -1), (1, 0), (0, 1), (-1, 0)))


def calm(t, target):
    """As Ground.Apply: the game's c/C glare neon on large areas; marble keeps its gold."""
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a > 200 and b > r + 30:
                v = max(g, b) / 255
                px[x, y] = tuple(int(c * (0.45 + 0.6 * v)) for c in target) + (a,)
    return t


def post(name, t):
    for k, target in CYAN.items():
        if k in name:
            return calm(t, target)
    if name not in WALLS:
        return t
    target = TONES[WALLS[name]]
    t = t.copy()
    px = t.load()
    for y in range(t.height):
        for x in range(t.width):
            r, g, b, a = px[x, y]
            if a < 200 or max(r, g, b) < 40 or (r > 200 and b < 110):      # ink outline and gold band stay
                continue
            v = (r + g + b) / 3 / 255
            px[x, y] = tuple(min(255, int(c * (0.62 + 0.5 * v))) for c in target) + (a,)
    return t


def main():
    panels = [("Original game", MR.render("StiltGroundFloor", "vanilla", BOX)),
              ("Bright Qud today", MR.render("StiltGroundFloor", "new", BOX, ground=flat("salt", "a"), bare=bare("salt"))),
              ("Proposal", MR.render("StiltGroundFloor", "new", BOX, ground=flat("salt", "a"), bare=bare("salt"), swap=swap, post=post))]
    pw, ph = panels[0][1].size
    pad = 16
    out = Image.new("RGB", (pw + 2 * pad, 80 + 3 * (ph + 34) + 90), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '14. Six Day Stilt - "rises from the dunes like a petrified kraken corpse"', pad, 14, pw, font(22), (240, 236, 220))
    y = 60
    for label, im in panels:
        d.text((pad, y), label, font=font(18), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (pad, y + 26))
        y += ph + 34
    wrap(d, "The game's patterned floor, unchanged. Light blue outer walls, white marble inside, fluted columns with gold "
         "bands, six distinct Argent Fathers, one joined gold-edged dais, a deep black well, carved friezes.", pad, y + 6, pw, font(16))
    path = os.path.join(zm.OUT, "review_stilt.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
