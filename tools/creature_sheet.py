"""Creature review sheet: original game tile next to the Bright Qud sprite, both with the game's colours.
Uses extracted vanilla tiles, so the output stays local (mockups/local/zones/creatures.png).
Usage: .venv/bin/python -I tools/creature_sheet.py
"""
import os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
from mockup import font  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from zone_mockup import key_of, vanilla, ours, q, OUT  # noqa: E402

GROUPS = [
    ("Joppa and the salt", ["Snapjaw", "Snapjaw Hunter", "Glowfish", "Salthopper", "Dromad", "Girshling", "Young Ivory", "Equimax"]),
    ("Jungle and canyons", ["Albino ape", "Ogre Ape", "Qudzu", "Goatfolk Yurtwarden", "Chitinous Puma", "Slugsnout", "Rustacean", "Cragmensch"]),
    ("Rainbow Wood", ["Spotted Shagspook", "Dandy Cap", "FungusPuffer1", "Slynth Wanderer", "Leech", "Glowcrow", "Ray Cat", "Horned Chameleon"]),
    ("Lake Hinnom", ["White Esh", "Giant Clam", "Prism Perch", "Sultan Croc", "Svardym Jut", "Svardym Eld", "Svardym Scrounge", "Ixlthyxl"]),
    ("Palladium Reef", ["Reef Hermit", "Enigma Snail", "Tongue Tyrant", "Plasma Jelly", "Galgal", "Kaleidoslug", "Trining Lamprey", "Junk Dollar"]),
    ("Deep and late game", ["Star Kraken", "Memory Eater", "Quatravolt Glider", "Elder Lagroot", "Interdictor", "Voider", "Leering Stalker", "Chrome Pyramid"]),
    ("Omonporch and legends", ["Asphodel", "Asphodelyte", "Electrofuge", "Bethsaida", "Agolgot", "Qas", "Qon", "Templar"]),
]
FAMILIES = [
    ("Frogs (svardym)", ["Svardym Hatchling", "Svardym Jut", "Svardym Scrounge", "Svardym Eld", "Bep", "Krka", "Goek", "Geeub"]),
    ("Other frogs", ["Ice frog", "Bloated Pearlfrog", "Frogs Cherub", "Chiliad Creature Frogs", "Frog Golem", "Svardym Golem", "Chiliad Creature Svardym"]),
    ("Reptiles", ["Croc", "Sultan Croc", "Salamander", "Horned Chameleon", "Molting Basilisk", "Lithofex", "Dawnglider", "Rimewyk"]),
    ("Tortoises", ["IrritableTortoise", "Great Saltback", "Tortoises Cherub", "Chiliad Creature Tortoises", "Tortoise Golem"]),
    ("Templars", ["Templar Squire", "Knight Templar", "Gunner-Knight Templar", "Banner-Knight Templar", "Knight Commander of the Holy Temple", "Wraith-Knight Templar", "Chiliad Creature Templar"]),
    ("Temple mecha", ["VehicleTemplarMech1", "VehicleTemplarMech2", "VehicleTemplarMech3"]),
]
S = 4


def colors(bp, n):
    r = bp.render(n)
    cs = r["TileColor"] or r["ColorString"] or "&y"
    fg = cs[cs.rfind("&") + 1] if "&" in cs else "y"
    return r["Tile"], fg, r["DetailColor"] or "k", r["DisplayName"]


def main():
    global GROUPS
    out_name = "creatures.png"
    if "--families" in sys.argv:
        GROUPS, out_name = FAMILIES, "families.png"
    bp = Blueprints()
    cw, chh = 16 * S, 24 * S
    colw = 2 * cw + 40
    rowh = chh + 50
    w = 220 + 8 * colw
    h = 20 + len(GROUPS) * rowh
    img = Image.new("RGB", (w, h), (24, 24, 28))
    d = ImageDraw.Draw(img)
    bg = (0x2A, 0x2A, 0x30)
    for gi, (gname, names) in enumerate(GROUPS):
        y = 20 + gi * rowh
        d.text((12, y + chh // 2 - 10), gname, font=font(17), fill=(235, 230, 210))
        for i, n in enumerate(names):
            x = 220 + i * colw
            tile, fg, dt, disp = colors(bp, n)
            if fg not in "rRoOwWgGbBcCmMkKyY":
                fg = "y"
            if dt not in "rRoOwWgGbBcCmMkKyY":
                dt = "k"
            k = key_of(tile)
            for j, t in enumerate((vanilla(k, fg, dt) if fg else None, ours(k, fg, dt))):
                cell = Image.new("RGBA", (16, 24), (q("k") if j == 0 else bg) + (255,))
                if t is not None:
                    cell.alpha_composite(t)
                img.paste(cell.convert("RGB").resize((cw, chh), Image.NEAREST), (x + j * (cw + 6), y))
            label = (disp or n) if "[" not in (disp or "[") else n
            label = label.replace("FungusPuffer1", "brooding puff").replace("=creatureRegionNoun=", "(chiliad)")
            d.text((x, y + chh + 4), label[:20], font=font(13), fill=(210, 205, 190))
    p = os.path.join(OUT, out_name)
    img.save(p)
    print(p)


if __name__ == "__main__":
    main()
