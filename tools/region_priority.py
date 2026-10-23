"""Rank tiles of the regions after Joppa (jungles, ruins, hills, mountains, flower fields, deeper
caves...) that Bright Qud hasn't redrawn yet. Same scoring as tile_priority.py.

Usage: .venv/bin/python -I tools/region_priority.py [N] -> docs/region_ranking.csv, prints top N
"""
import collections, csv, os, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from qudxml import Blueprints  # noqa: E402
from tile_priority import add_random_tiles, expand, load_tables, tiles_of  # noqa: E402

ROOTS = [
    ("JungleZoneGlobals", 1.0), ("JunglePerSector", 1.0), ("JungleCaveGlobals", 0.6),
    ("DeepJungleZoneGlobals", 0.6), ("DeepJunglePerSector", 0.6),
    ("RuinsZoneGlobals", 0.8), ("RuinsPerSector", 0.8), ("BaroqueRuinsZoneGlobals", 0.4),
    ("BaroqueRuinsPerSector", 0.4),
    ("HillsZoneGlobals", 0.7), ("HillsPerSector", 0.7), ("HillCaveGlobals", 0.5),
    ("MountainsZoneGlobals", 0.5), ("MountainsPerSector", 0.5), ("MountainCaveGlobals", 0.4),
    ("FlowerFieldGlobals", 0.5), ("FlowerfieldCaveGlobals", 0.3),
    ("Tier1CaveGlobals", 0.7), ("Tier2CaveGlobals", 0.7), ("Tier3CaveGlobals", 0.5),
    ("WaterCaveGlobals", 0.4), ("FungalJunglePopulation", 0.3),
]
TEX = os.path.join(ROOT, "mod", "BrightQud", "Textures")


def main():
    top = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    built = {f[:-4] for f in os.listdir(TEX)}
    bp = Blueprints()
    add_random_tiles(bp)
    tables = load_tables()
    counts = collections.Counter()
    missing = [n for n, _ in ROOTS if n not in tables]
    for name, w in ROOTS:
        if name in tables:
            expand(tables, tables[name], w, counts)
    scores, users = collections.Counter(), collections.defaultdict(list)
    for name, n in counts.items():
        if name not in bp.objs:
            continue
        ks = tiles_of(bp, name)
        for k in ks:
            scores[k] += n / len(ks)
            users[k].append(name)

    def done(k):
        if k.endswith("-*"):
            k = k[:-2] + "-00000000"
        return k.replace("/", "_") in built
    rows = [(k, s) for k, s in scores.most_common() if not done(k)]
    with open(os.path.join(ROOT, "docs", "region_ranking.csv"), "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "tile_key", "score", "objects"])
        for i, (k, s) in enumerate(rows, 1):
            w.writerow([i, k, round(s, 1), "; ".join(sorted(set(users[k]))[:6])])
    if missing:
        print("tables not found:", missing)
    for i, (k, s) in enumerate(rows[:top], 1):
        print(f"{i:3} {s:7.1f} {k:42} {'; '.join(sorted(set(users[k]))[:4])}")


if __name__ == "__main__":
    main()
