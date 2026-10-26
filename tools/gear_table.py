"""Paper doll gear table: every wearable item / weapon blueprint -> (slot, piece, material).

The runtime looks items up by blueprint name (no work per redraw). Pieces are the shapes we draw on the
character (art/src/paperdoll.py); material picks the colours when the game's own colours don't say it
(the game paints chain mail and steel plain white).

Usage: .venv/bin/python -I tools/gear_table.py [--report] -> build/gear_table.json (+ coverage report)
"""
import json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools")]
from qudxml import Blueprints  # noqa: E402

OUT = os.path.join(ROOT, "build", "gear_table.json")

# (slot, [(piece, name regex)]) first match wins; None = not drawn (too small / not a garment).
RULES = {
    "Body": [("plate", r"plate|cask|flange"), ("chain", r"chain|ring mail|shardmail|flake"),
             ("fur", r"\bfurs?\b|pelt"), ("leather", r"leather|bark|hide|carapace|quills"),
             ("tunic", r"tunic|vest|overalls|apron|suit|smock"),
             ("robe", r"robe|gown|toga|frock|mantle|cloth|chime|cone|.")],
    "Head": [("horns", r"horn|antler|spur|knollworm|snail shell"), ("crown", r"coronet|crown|wreath|halo"),
             ("techhelm", r"miner|lamp|psychodyne|teleprojector|aggregator|gentling cone|enigma"),
             ("helmet", r"helm|armet|casque"), ("coif", r"coif"), ("hat", r"\bhat\b"),
             ("veil", r"veil"), ("cap", r".")],
    "Face": [("goggles", r"goggles|interpolator|mirrorshades|spectacles|monocle|lens"),
             ("mask", r"mask|face|veil|sap"), (None, r".")],
    "Back": [("wings", r"wing|flier|sail"), ("banner", r"banner"), ("exo", r"exoskeleton"),
             ("pack", r"pack|bladder|tumbler|tank|hive|laser|netting"),
             ("cloak", r".")],
    "Hands": [("claws", r"claw|fingers"), ("gauntlets", r"gauntlet|fist"), ("gloves", r".")],
    "Feet": [("sandals", r"sandal|moccasin|slipper|sneaker|croccasin|krakow|hooks"), ("boots", r".")],
}
WEAPONS = {"Cudgel": [("staff", r"staff|stick|horn|conch|pestle"), ("hammer", r"hammer|maul"),
                      ("mace", r".")],
           "ShortBlades": [("dagger", r".")], "LongBlades": [("sword", r".")], "Axe": [("axe", r".")],
           "Chain": [("whip", r".")], "Whip": [("whip", r".")],
           "Pistol": [("pistol", r".")], "Rifle": [("bow", r"\bbow|turbow|electrobow"), ("rifle", r".")],
           "HeavyWeapons": [("heavy", r".")]}

# Material words -> our colour pair (palette letters fg, detail). Order matters (folded carbide > carbide).
MATERIALS = [("crysteel", "crysteel"), ("zetachrome", "zetachrome"), ("fullerite", "fullerite"),
             ("folded carbide", "carbide"), ("carbide", "carbide"), ("plastifer", "plastifer"),
             ("elastyne", "elastyne"), ("bronze", "bronze"), ("iron", "iron"), ("steel", "steel"),
             ("chain", "steel"), ("ring mail", "steel"), ("leather", "leather"), ("studded", "leather"),
             ("fur", "fur"), ("bark", "wood"), ("wood", "wood"), ("cloth", "cloth"), ("silk", "cloth")]


def plain(name):
    """Display name without colour markup."""
    prev = None
    while prev != name:
        prev = name
        name = re.sub(r"\{\{[^|{}]*\|([^{}]*)\}\}", r"\1", name)
    return re.sub(r"&[A-Za-z]|\^[A-Za-z]", "", name).strip()


def pick(rules, text):
    for piece, rx in rules:
        if re.search(rx, text, re.I):
            return piece
    return None


def material(bp, n, text):
    for word, mat in MATERIALS:
        if word in text.lower():
            return mat
    return "metal" if bp.part(n, "Metal", "Name") is not None or any("Metal" in o["parts"] for o in bp._walk(n)) else None


def special_key(slot, text):
    """Item-specific piece name (docs/doll_specials_facehead.md), e.g. face/earth_face; drawn ones win."""
    if slot not in ("Face", "Head"):
        return None
    key = re.sub(r"[^a-z0-9]+", "_", text.lower()).strip("_").replace("flawless_", "")
    return f"{slot.lower()}/{key}"


SLOT_LAYER = {"Body": "body", "Head": "head", "Face": "face", "Back": "back", "Hands": "hands", "Feet": "feet",
              "Shield": "left", "Hand": "right"}


def doll_rows(t, layers):
    """[(blueprint, layer key, material, two-handed)] for the runtime; special pieces when drawn."""
    rows = []
    for n, e in sorted(t.items()):
        if e["special"] and e["special"] in layers:
            key = e["special"]
        else:
            key = ("two" if e["slot"] == "Hand" and e["two"] else SLOT_LAYER[e["slot"]]) + "/" + e["piece"]
        key = {"two/mace": "two/hammer", "two/pistol": "right/pistol", "right/rifle": "two/rifle",
               "two/dagger": "right/dagger", "two/whip": "right/whip", "two/staff": "right/staff"}.get(key, key)
        if key in layers:
            rows.append((n, key, e["mat"] or "", e["two"]))
    return rows


def table():
    bp = Blueprints()
    out = {}
    for n, o in bp.objs.items():
        if o["tags"].get("BaseObject") is not None:
            continue
        raw = bp.render(n)["DisplayName"] or n
        text = plain(raw)
        two = bp.part(n, "Physics", "UsesTwoSlots") == "true"
        entry = None
        cat = bp.part(n, "Physics", "Category")
        if cat == "Natural Armor":
            continue  # mutation body parts (carapace, horns, wings...): drawn by the mutation layer
        if bp.part(n, "Shield", "AV") is not None and "horn" not in text.lower():
            entry = ("Shield", "shield")
        elif (w := bp.part(n, "Armor", "WornOn")) in RULES:
            entry = (w, pick(RULES[w], text))
        else:
            skill = bp.part(n, "MissileWeapon", "Skill")
            if skill is None and bp.part(n, "Physics", "Takeable") != "false":
                # real weapons only (the MeleeWeapon base sets this tag; natural fists/fangs don't)
                skill = bp.part(n, "MeleeWeapon", "Skill") if bp.tag(n, "MeleeWeapon") is not None else None
            if skill in WEAPONS and (cat == "Melee Weapons" or bp.part(n, "MissileWeapon", "Skill") is not None):
                entry = ("Hand", pick(WEAPONS[skill], text))
        if not entry or entry[1] is None:
            continue
        out[n] = {"slot": entry[0], "piece": entry[1], "mat": material(bp, n, text), "two": two, "name": text,
                  "special": special_key(entry[0], text)}
    return out


def main():
    t = table()
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    json.dump(t, open(OUT, "w"), indent=1, sort_keys=True)
    print(f"{len(t)} items -> {OUT}")
    if "--report" in sys.argv:
        from collections import defaultdict
        groups = defaultdict(list)
        for n, e in t.items():
            groups[(e["slot"], e["piece"])].append(f'{e["name"]}[{e["mat"] or "-"}{",2h" if e["two"] else ""}]')
        for k in sorted(groups):
            v = sorted(set(groups[k]))
            print(f"{k[0]:7} {k[1]:9} {len(v):3}  " + "; ".join(v[:14]) + (" ..." if len(v) > 14 else ""))


if __name__ == "__main__":
    main()
