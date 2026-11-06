"""Zone review #25 generated villages: one wall style is rolled per village. Today most styles are one speckled block in a neon tint;
the proposal gives each style its material, from the game's descriptions, in calm colours. Canvas, planks and bone show one rolled
example. Local output only.

Usage: .venv/bin/python -I tools/review_villages.py -> mockups/local/zones/review_villages.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import zone_mockup as zm  # noqa: E402
from review_redrock import flat, bare  # noqa: E402

W, H = 13, 6
# label, blueprint, material, colours as Ground.Apply sets them
STYLES = (("Brick", "BrickWall", "brick", "a8644c", "6a4436"), ("Stone (slate)", "Slate", "stone", "8c969c", "5a6268"),
          ("Granite", "Granite", "rock", "6a7072", "3c4244"), ("Canvas (rolled colour)", "CanvasWall", "canvas", "a08a68", "8a5a48"),
          ("Sheet metal", "MetalWall", "metal", "84908f", "8a5a3c"), ("Thatch", "ThatchedWall", "thatch", "b49a62", "7a6238"),
          ("Plank hedge (rolled colour)", "BrinestalkWall", "wood", "9c8a5c", "6e6a48"), ("Bone (rolled colour)", "BaseSedimentaryRock", "bone", "c4bba4", "7a6e58"),
          ("Marble", "Marble", "stiltmarble", "e6e1d4", "b9b4a8"), ("Foamcrete", "Foamcrete", "concrete", "9aa4a0", "6c7672"))


def hut(wall):
    c = {(x, y): [] for x in range(W) for y in range(H)}
    for x in range(2, 11):
        for y in range(1, 5):
            if x in (2, 10) or y in (1, 4):
                c[x, y] = [wall]
    c[6, 4] = []
    return c


def main():
    panels = []
    for label, wall, material, fg, det in STYLES:
        RR.MAT[wall], RR.TONE[wall] = material, (fg, det)
        c = hut(wall)
        panels.append((label, MR.render(c, "new", (0, 0, W, H), ground=flat("jungle", "b"), bare=bare("jungle")),
                       MR.render(c, "new", (0, 0, W, H), ground=flat("jungle", "b"), bare=bare("jungle"), swap=RR.recording, post=RR.real)))
    pw, ph = panels[0][1].size
    pad, cols = 12, 2
    rows = (len(panels) + 1) // cols
    out = Image.new("RGB", (pad + cols * (2 * pw + 2 * pad), 50 + rows * (ph + 30)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    d.text((pad, 12), "25. Generated villages: wall styles, today (left) and proposal (right)", font=font(22), fill=(240, 236, 220))
    for i, (label, a, b) in enumerate(panels):
        x, y = pad + (i % cols) * (2 * pw + 2 * pad), 50 + (i // cols) * (ph + 30)
        d.text((x, y), label, font=font(16), fill=(235, 205, 140))
        out.paste(a.convert("RGB"), (x, y + 22))
        out.paste(b.convert("RGB"), (x + pw + 6, y + 22))
    path = os.path.join(zm.OUT, "review_villages.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
