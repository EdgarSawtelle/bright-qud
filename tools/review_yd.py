"""Zone review #22 Yd Freehold: the real map (YdFreehold.rpm), today and with glass pipework, reef floor, algal water
and iron bars. The coral and strut spawners draw nothing here, so the reef growth is not shown. Local output only.

Usage: .venv/bin/python -I tools/review_yd.py -> mockups/local/zones/review_yd.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
import map_render as MR  # noqa: E402
import review_ruins as RR  # noqa: E402
import review_hinnom2 as H  # noqa: E402
import zone_mockup as zm  # noqa: E402
from zone_review import wrap  # noqa: E402
from review_redrock import bare  # noqa: E402

BOX = (20, 8, 64, 25)
PIPE = "YdFreeholdGlassHydraulicPipe1"
RR.MAT[PIPE] = "ydglass"
RR.TONE[PIPE] = ("8fb84a", "c9a84a")
RR.MAT["IronFence"] = "ironbars"
RR.TONE["IronFence"] = ("5c5e62", "3a3b3f")
GROUND = lambda x, y: (0x20, 0x3a, 0x3b)


def post(name, t):
    if name in ("AlgaePool", "AlgalWaterDeepPool"):
        return H.post(H.LIQ, t)
    return RR.real(name, t) if name in RR.TONE else t


def main():
    rows = [("Today", MR.render("YdFreehold", "new", BOX, ground=GROUND, bare=bare("reef"))),
            ("Proposal", MR.render("YdFreehold", "new", BOX, ground=GROUND, bare=bare("reef"), swap=RR.recording, post=post))]
    pw, ph = rows[0][1].size
    pad = 14
    out = Image.new("RGB", (pw + 2 * pad, 60 + 2 * (ph + 32)), (24, 24, 28))
    d = ImageDraw.Draw(out)
    wrap(d, '22. Yd Freehold - "dyed pipework topology mounted in the spongebed"', pad, 12, pw, font(22), (240, 236, 220))
    for i, (label, im) in enumerate(rows):
        y = 54 + i * (ph + 32)
        d.text((pad, y), label, font=font(17), fill=(235, 205, 140))
        out.paste(im.convert("RGB"), (pad, y + 24))
    path = os.path.join(zm.OUT, "review_yd.png")
    out.save(path)
    print(path)


if __name__ == "__main__":
    main()
