"""Rank game tiles by how often a player in the starting region sees them (Phase 3 planning).

Score = expected object count, from:
  - the hand-made Joppa map (weighted up: players spend a lot of time there),
  - population tables of the regions around Joppa (salt marsh, salt dunes, canyons, Rust Wells...),
    expanded recursively with expected counts (chance x average number).
Objects are mapped to tiles via Render.Tile, RandomTile builders and painted wall/fence families.

Usage: .venv/bin/python -I tools/tile_priority.py  -> docs/phase3_ranking.csv
"""
import collections, csv, os, random, re, sys
import xml.etree.ElementTree as ET

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
from qudxml import BASE, Blueprints, _parse  # noqa: E402

# (population table, weight). Weights reflect how much time an early player spends there.
ROOTS = [
    ("SaltMarshZoneGlobals", 1.0), ("SaltMarshPerSector", 1.0), ("StandardSurfaceGlobals", 1.0),
    ("Joppa Outskirts", 1.0), ("Joppa Tunnel", 0.6),
    ("SaltDesertZoneGlobals", 0.6), ("SaltDesertPerSector", 0.6), ("SaltDuneCreatures", 0.6),
    ("SaltDuneCaveGlobals", 0.5), ("SaltDuneCavePopulation", 0.5),
    ("DesertCanyonZoneGlobals", 0.5), ("DesertCanyonPerSector", 0.5), ("DesertCanyonCreatures", 0.5),
    ("DesertCanyonCaveGlobals", 0.5), ("DesertCanyonCavePopulation", 0.5),
    ("Rustwells Surface", 0.5), ("Rustwells 1", 0.5), ("Rustwells 2", 0.4), ("Rustwells 3", 0.3),
    ("HillsZoneGlobals", 0.3), ("HillsPerSector", 0.3),
]
STATIC_MAPS = [("Joppa.rpm", 3.0)]


def expected_number(spec):
    if not spec:
        return 1.0
    spec = spec.strip()
    m = re.fullmatch(r"(\d+)-(\d+)", spec)
    if m:
        return (int(m.group(1)) + int(m.group(2))) / 2
    m = re.fullmatch(r"(\d*)d(\d+)([+-]\d+)?", spec)
    if m:
        n = int(m.group(1) or 1)
        return n * (int(m.group(2)) + 1) / 2 + int(m.group(3) or 0)
    try:
        return float(spec)
    except ValueError:
        return 1.0


def chance(el):
    c = el.get("Chance")
    if not c:
        return 1.0
    try:
        # "100,2" = chance per roll + rolls in some tables; use the first number.
        return float(re.split(r"[,:]", c)[0]) / 100
    except ValueError:
        return 1.0


def load_tables():
    root = _parse(os.path.join(BASE, "PopulationTables.xml"))
    return {p.get("Name"): p for p in root.iter("population")}


def expand(tables, el, factor, out, depth=0):
    """Accumulate expected blueprint counts below a <population>/<group> element."""
    if depth > 12:
        return
    children = [c for c in el if c.tag in ("object", "table", "group")]
    if el.tag == "group" and (el.get("Style") or "").lower() == "pickone" and children:
        weights = [float(c.get("Weight", 1)) for c in children]
        total = sum(weights)
        pairs = [(c, factor * w / total) for c, w in zip(children, weights)]
    else:
        pairs = [(c, factor) for c in children]
    for c, f in pairs:
        f = f * chance(c) * expected_number(c.get("Number"))
        if c.tag == "object" and c.get("Blueprint"):
            out[c.get("Blueprint")] += f
        elif c.tag == "table" and c.get("Name") in tables:
            expand(tables, tables[c.get("Name")], f, out, depth + 1)
        elif c.tag == "group":
            expand(tables, c, f, out, depth + 1)


def tiles_of(bp, name):
    """All tile keys an object can show (lowercased, extension-free, '_' -> '/', like the game)."""
    found = set()
    t = bp.part(name, "Render", "Tile")
    if t:
        found.add(t)
    raw = None
    seen = 0
    n = name
    while n in bp.objs and seen < 50 and raw is None:
        raw = bp.objs[n].get("random_tiles")
        n = bp.objs[n]["inh"]
        seen += 1
    for t in raw or []:
        found.add(t)
    for tag, prefix in (("PaintedWall", "Walls/"), ("PaintedFence", "Walls/")):
        v = bp.tag(name, tag)
        if v:
            atlas = bp.tag(name, tag + "Atlas") or "Tiles/"
            found.add(f"{atlas}{v}-*")
    return {key(t) for t in found}


def key(path):
    k = path.split(".")[0].replace("\\", "/").replace("_", "/").lower()
    return k[len("assets/content/textures/"):] if k.startswith("assets/content/textures/") else k


def add_random_tiles(bp):
    """Attach RandomTile builder lists to blueprints (qudxml doesn't read builders)."""
    import glob
    for f in glob.glob(BASE + "/ObjectBlueprints/*.xml"):
        for o in _parse(f).iter("object"):
            for b in o.findall("builder"):
                if b.get("Name") == "RandomTile" and b.get("Tiles"):
                    bp.objs[o.get("Name")]["random_tiles"] = b.get("Tiles").split(",")


def main():
    bp = Blueprints()
    add_random_tiles(bp)
    tables = load_tables()
    counts = collections.Counter()
    for name, w in ROOTS:
        if name in tables:
            expand(tables, tables[name], w, counts)
    for rpm, w in STATIC_MAPS:
        for o in _parse(os.path.join(BASE, rpm)).iter("object"):
            counts[o.get("Name")] += w
    scores = collections.Counter()
    users = collections.defaultdict(list)
    for name, n in counts.items():
        if name not in bp.objs:
            continue
        ks = tiles_of(bp, name)
        for k in ks:
            scores[k] += n / len(ks)
            users[k].append(name)
    out = os.path.join(ROOT, "docs", "phase3_ranking.csv")
    with open(out, "w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["rank", "tile_key", "score", "objects"])
        for i, (k, s) in enumerate(scores.most_common(), 1):
            w.writerow([i, k, round(s, 1), "; ".join(sorted(set(users[k]))[:6])])
    print(f"{len(scores)} tiles ranked -> {os.path.relpath(out, ROOT)}")


if __name__ == "__main__":
    main()
