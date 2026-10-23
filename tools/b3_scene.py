"""Joppa-like scene with the built B3 character tiles (mod Textures, our art only) at Deck 2x zoom.

Usage: .venv/bin/python -I tools/b3_scene.py -> mockups/b3_scene.png
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image  # noqa: E402
from style_scene import background, ring, tex, RING, W, H  # noqa: E402

CAST = [("creatures_sw_gunwing.png", 5, 3, "player"), ("creatures_npc-mehmet.png", 1, 1, None),
        ("creatures_npc-argyve.png", 3, 2, None), ("creatures_sw_farmer.png", 12, 1, None),
        ("creatures_sw_dog.png", 6, 5, "ally"), ("creatures_sw_snapjaw.png", 10, 3, "hostile"),
        ("creatures_sw_snapjaw_hunter.png", 11, 4, "hostile"), ("creatures_sw_snapjaw_bruiser.png", 9, 2, "hostile"),
        ("creatures_sw_glowfish.png", 12, 5, None), ("creatures_sw_solifuge.png", 9, 5, "hostile"),
        ("creatures_sw_salthopper.png", 4, 1, None), ("creatures_sw_croc.png", 13, 3, "hostile"),
        ("creatures_sw_young_ivory.png", 7, 4, "hostile"), ("creatures_sw_angrybear.png", 2, 4, "hostile"),
        ("creatures_sw_dromad.png", 8, 1, None), ("creatures_sw_goat.png", 3, 5, None)]


def main():
    img = background()
    for name, x, y, r in CAST:
        t = tex(name)
        if t is None:
            print("missing", name)
            continue
        if r:
            ring(t, RING[r])
        img.alpha_composite(t, (x * 16, y * 24))
    img.resize((W * 32, H * 48), Image.NEAREST).save(os.path.join(ROOT, "mockups", "b3_scene.png"))
    print("done")


if __name__ == "__main__":
    main()
