"""One-page overview of the zone study (docs/zone_study/*.md): every place's palette, mood and fan-art
status, grouped by ground family. Output: mockups/local/zones/study_overview.png (local only).

Usage: .venv/bin/python -I tools/study_overview.py
"""
import glob, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402

LABS = ("ground", "accent", "material", "plants", "water", "light", "night")
# Human fan art of the place itself (checked by hand from the studies).
FAN = {"01_joppa": "fan art", "03_redrock": "fan art", "05_jungle": "fan art", "07_gritgate": "sketch",
       "12_canyons": "fan art", "13_saltdunes": "fan art", "15_ruins": "near match", "16_golgotha": "fan art",
       "24_bethesdasusa": "fan art", "30_moonstair": "painting", "31_eynroj": "painting", "32_brightsheol": "fan art",
       "09_beylah": "people only"}
GROUPS = [
    ("A. Pale salt and sand (bright ground)", ["13_saltdunes", "14_sixdaystilt", "08_flowerfields", "11_hills_mountains",
                                               "20_lakehinnom", "21_palladiumreef", "22_ydfreehold"]),
    ("B. Warm earth: villages and old stone", ["01_joppa", "09_beylah", "25_villages", "06_kyakukya", "26_historic_sites",
                                               "15_ruins"]),
    ("C. Rust and red rock", ["03_redrock", "04_rustwells", "12_canyons", "24_bethesdasusa", "17_asphaltmines"]),
    ("D. Green shade and water", ["02_saltmarsh", "05_jungle", "10_deepjungle", "16_golgotha", "18_bananagrove",
                                  "19_rivers", "28_omonporch", "23_rainbowwood"]),
    ("E. Dark teal: sacred, technological, underground", ["07_gritgate", "27_caves", "29_spindle", "30_moonstair",
                                                          "31_eynroj", "32_brightsheol", "33_northsheva"]),
]


def parse(path):
    t = open(path).read()
    title = re.search(r"^# (.+)$", t, re.M).group(1)
    m = re.search(r"^- \**Palette[^:]*:\**(.*?)(?=^- |^## |\Z)", t, re.M | re.S)
    pal = {}
    for lab in LABS:
        mm = re.search(lab + r"[^#]{0,60}?(#[0-9a-fA-F]{6})", m.group(1) if m else "")
        if mm:
            pal[lab] = mm.group(1)
    mood = re.search(r"^- \**Mood\**:\s*(.*?)(?=^- |^## |\Z)", t, re.M | re.S)
    return title, pal, " ".join(mood.group(1).split()) if mood else ""


def main():
    rows = {os.path.basename(f)[:-3]: parse(f) for f in glob.glob(os.path.join(ROOT, "docs", "zone_study", "*.md"))}
    W, rh, x0 = 1500, 46, 290
    out = Image.new("RGB", (W, 4000), (24, 24, 28))
    d = ImageDraw.Draw(out)
    d.text((20, 14), "Bright Qud zone study: 33 places grouped by ground family (palettes from the research)",
           font=font(26), fill=(240, 236, 220))
    for i, lab in enumerate(LABS):
        d.text((x0 + i * 56, 56), lab, font=font(12), fill=(170, 170, 160))
    y = 80
    for gname, keys in GROUPS:
        y += 14
        d.text((20, y), gname, font=font(20), fill=(235, 205, 140))
        y += 34
        for k in keys:
            title, pal, mood = rows[k]
            d.text((20, y + 12), title[:30], font=font(15), fill=(225, 220, 205))
            for i, lab in enumerate(LABS):
                if lab in pal:
                    d.rectangle((x0 + i * 56, y + 2, x0 + i * 56 + 50, y + rh - 6), fill=pal[lab], outline=(70, 70, 70))
            d.text((x0 + 7 * 56 + 14, y + 6), mood.split(";")[0][:95], font=font(14), fill=(200, 200, 190))
            tag = FAN.get(k, "no fan art")
            d.text((x0 + 7 * 56 + 14, y + 24), tag, font=font(12),
                   fill=(130, 200, 140) if tag != "no fan art" else (130, 130, 125))
            y += rh
    path = os.path.join(ROOT, "mockups", "local", "zones", "study_overview.png")
    out.crop((0, 0, W, y + 20)).save(path)
    print(path)


if __name__ == "__main__":
    main()
