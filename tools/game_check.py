"""Has Caves of Qud changed since we last looked? Run at the start of every change request.

Compares the installed game with the last snapshot (reference/game_snapshot.json, local only):
Steam build id, Assembly-CSharp.dll checksum, mutation classes, skill/power classes and the tile
keys used by blueprints. Also lists what Bright Qud doesn't cover yet:
  - tile keys used by blueprints with no Bright Qud tile,
  - new mutations / skills (Explain.cs falls back to the game's text for mutations; new fight
    skills may deserve a SkillHelp line).

Usage: .venv/bin/python -I tools/game_check.py [--update]
  --update  save the current state as the new snapshot (do it after reviewing the changes).
Exit code 0 = unchanged, 1 = the game changed since the snapshot (or no snapshot yet).
"""
import glob, hashlib, json, os, re, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path[:0] = [os.path.join(ROOT, "tools"), os.path.join(ROOT, "art", "src")]
from qudxml import Blueprints, _parse  # noqa: E402
from tile_priority import BASE, add_random_tiles, tiles_of  # noqa: E402

STEAM = os.path.expanduser("~/.local/share/Steam/steamapps")
GAME = os.path.join(STEAM, "common", "Caves of Qud")
SNAPSHOT = os.path.join(ROOT, "reference", "game_snapshot.json")
MOD = os.path.join(ROOT, "mod", "BrightQud")


def build_info():
    info = {}
    acf = os.path.join(STEAM, "appmanifest_333640.acf")
    if os.path.exists(acf):
        txt = open(acf, encoding="utf-8", errors="replace").read()
        for k in ("buildid", "LastUpdated"):
            m = re.search(r'"%s"\s+"(\d+)"' % k, txt)
            if m:
                info[k] = m.group(1)
    dll = os.path.join(GAME, "CoQ_Data", "Managed", "Assembly-CSharp.dll")
    if os.path.exists(dll):
        info["dll_sha"] = hashlib.sha256(open(dll, "rb").read()).hexdigest()[:16]
    return info


def classes(xml, tag):
    return sorted({e.get("Class") for e in _parse(os.path.join(BASE, xml)).iter(tag) if e.get("Class")})


def tile_keys():
    bp = Blueprints()
    add_random_tiles(bp)
    keys = set()
    for name, o in bp.objs.items():
        if "BaseObject" not in o["tags"]:
            keys.update(tiles_of(bp, name))
    return sorted(keys)


def current():
    return {
        "build": build_info(),
        "mutations": sorted(set(classes("Mutations.xml", "mutation") + classes("HiddenMutations.xml", "mutation"))),
        "skills": sorted(set(classes("Skills.xml", "skill") + classes("Skills.xml", "power"))),
        "tiles": tile_keys(),
    }


def help_keys(table):
    src = open(os.path.join(MOD, "Explain.cs"), encoding="utf-8").read()
    body = src.split(table, 1)[1].split("};", 1)[0]
    return set(re.findall(r'\{ "([A-Za-z0-9_]+)",', body))


def show(title, items, limit=40):
    if not items:
        return
    print(f"  {title} ({len(items)}):")
    for x in items[:limit]:
        print("    " + x)
    if len(items) > limit:
        print(f"    ... +{len(items) - limit} more")


def main():
    now = current()
    old = json.load(open(SNAPSHOT)) if os.path.exists(SNAPSHOT) else None
    b = now["build"]
    print(f"Caves of Qud build {b.get('buildid', '?')} (dll {b.get('dll_sha', '?')})")
    changed = old is None or old["build"] != b
    if old is None:
        print("No snapshot yet: run with --update to record this version.")
    elif not changed:
        print("Game unchanged since the snapshot.")
    else:
        ob = old["build"]
        print(f"GAME UPDATED: build {ob.get('buildid', '?')} -> {b.get('buildid', '?')}")
    if old is not None:
        for key in ("mutations", "skills", "tiles"):
            a, o = set(now[key]), set(old[key])
            show(f"new {key}", sorted(a - o))
            show(f"removed {key}", sorted(o - a))
            changed |= a != o

    # Keys like "tiles/fence-*" are connection templates, and a few point at images the game doesn't
    # ship: only keys with an extracted game image count.
    import build_mod as BM
    idx = BM.ref_index()
    built = {f[:-4] for f in os.listdir(os.path.join(MOD, "Textures")) if f.endswith(".png")}
    uncovered = [k for k in now["tiles"] if k in idx and k.replace("/", "_") not in built]
    print(f"Tiles used by the game: {len(now['tiles'])}, without a Bright Qud tile: {len(uncovered)}")
    show("uncovered tiles (draw them)", uncovered)
    if old is not None:
        show("new tile keys with no extracted image (rerun tools/extract_ref.py, then check again)",
             [k for k in now["tiles"] if k not in idx and k not in set(old["tiles"])])
        new_skills = [s for s in now["skills"] if s not in set(old["skills"])]
        show("new mutations without a MutationHelp line (they use the game's text)",
             [m for m in now["mutations"] if m not in set(old["mutations"]) and m not in help_keys("MutationHelp")])
        show("new skills (add a SkillHelp line if they matter in a fight)", new_skills)

    if "--update" in sys.argv:
        os.makedirs(os.path.dirname(SNAPSHOT), exist_ok=True)
        json.dump(now, open(SNAPSHOT, "w"), indent=1)
        print("Snapshot saved:", os.path.relpath(SNAPSHOT, ROOT))
        changed = False
    sys.exit(1 if changed else 0)


if __name__ == "__main__":
    main()
