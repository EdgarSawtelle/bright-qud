"""Preview: human NPCs as paper dolls in the gear their blueprints give them (inventoryobject entries),
base clothes in their own colours. Usage: .venv/bin/python -I tools/review_npcdoll.py <out.png>"""
import glob, os, re, sys
ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from PIL import Image, ImageDraw  # noqa: E402
import doll_preview as DV  # noqa: E402
import gear_table as GT  # noqa: E402
from qudxml import Blueprints, BASE, _parse  # noqa: E402
from mockup import font  # noqa: E402

NPCS = ["Issachari Raider", "Issachari Rifler", "Mechanimist Zealot", "Knight Templar", "Gunner-Knight Templar",
        "Cannibal", "WatervineFarmer", "Mysterious Gunslinger", "Arconaut", "Scrap-clad Hermit", "Trash Monk",
        "Mechanimist Warden"]


def inventories():
    inv = {}
    for f in glob.glob(BASE + "/ObjectBlueprints/*.xml"):
        for o in _parse(f).iter("object"):
            items = [i.get("Blueprint") for i in o.iter("inventoryobject")]
            if items:
                inv[o.get("Name")] = items
    return inv


def letters(bp, n):
    r = bp.render(n)
    cs = r["TileColor"] or r["ColorString"] or "&y"
    fg = cs[cs.rfind("&") + 1] if "&" in cs else "y"
    det = (r["DetailColor"] or "K")[0]
    return (fg if fg in DV.C.QUD else "y"), (det if det in DV.C.QUD else "K")


def main():
    bp = Blueprints()
    inv = inventories()
    layers, _ = DV.load_layers()
    rows = {n: (k, m, two) for n, k, m, two in GT.doll_rows(GT.table(), layers)}
    tiles = []
    for npc in NPCS:
        f, d = letters(bp, npc)
        base = (f, d) if f not in "yYkK" else (d, f) if d not in "yYkK" else "linen"
        lo = [("body/base", base)]
        right = off = None
        names = []
        for item in inv.get(npc, []):
            if item not in rows:
                continue
            k, m, two = rows[item]
            spec = m if m in DV.MATERIALS else letters(bp, item)
            if m == "metal" and letters(bp, item)[0] in "yY":
                spec = "steel"
            names.append(item)
            if k.startswith(("right/", "two/")):
                if right is None:
                    right = (k, spec)
                elif off is None and k.startswith("right/") and not right[0].startswith("two/"):
                    off = ("offhand/" + k[6:], spec)
                continue
            lo.append((k, spec))
        lo += [x for x in (right, off) if x]
        tiles.append((npc + "\n" + ", ".join(names)[:34], DV.stack(layers, lo)))
    DV.sheet(sys.argv[1], 5, tiles, layers, [])


if __name__ == "__main__":
    main()
