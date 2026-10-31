"""Build mod/BrightQud: tiles at the game's own tile keys, role masks, mutation overlays, and
Generated.cs (data the runtime script needs).

Every target is identified by the game's tile KEY (lowercase, extension dropped, '_' -> '/',
e.g. "creatures/sw/farmer"). Files are written with flat names that normalise to that key
("creatures_sw_farmer.png"), so they replace the tile for every object that uses it, including
seed-generated ones. Default colors (used if scripting is off) come from a blueprint using the tile.

Usage: .venv/bin/python -I tools/build_mod.py
"""
import collections, importlib, os, re, shutil, sys

ROOT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..")
sys.path.insert(0, os.path.join(ROOT, "tools"))
sys.path.insert(0, os.path.join(ROOT, "art", "src"))
from PIL import Image, ImageOps  # noqa: E402
import build_tiles as B  # noqa: E402
import colors as C  # noqa: E402
import doll_palette as DP  # noqa: E402
import items as IT  # noqa: E402
import items2 as I2  # noqa: E402
import effects as FX  # noqa: E402
import kit as K  # noqa: E402
import kit2 as K2  # noqa: E402
import legend  # noqa: E402
import palette as P  # noqa: E402
import terrain2 as T2  # noqa: E402
import tiles as T  # noqa: E402
from qudxml import Blueprints  # noqa: E402
from tile_priority import add_random_tiles, key, tiles_of  # noqa: E402

MOD = os.path.join(ROOT, "mod", "BrightQud")
REF = os.path.join(ROOT, "reference", "tiles")
CR, S, IS = K.CREATURES, T.SPRITES, IT.ITEMS

# Tiles drawn on the HUMAN kit layout: mutation overlays line up with these.
# Agent-drawn art modules that passed review (only these are built).
APPROVED_BATCHES = {"items3", "kit3a", "kit3b", "items4_7", "items4_6", "items4_5", "items4_8", "b3more_4", "items4_3", "b3more_8", "b3more_5", "items4_4", "b3more_6", "b3more_7", "b3more_2", "items4_2", "items4_1", "b3more_1", "b3more_3", "fixtures_1", "fixtures_3", "terrain3_2", "terrain3_4", "fixtures_2", "terrain3_1", "terrain3_3", "extras"}
# B3 character restyle (docs/B3_RESTYLE_BRIEF.md): modules whose OVERRIDES replace the old sprites.
# b3kit also replaces the player looks and mutation overlays.
B3_BATCHES = ["b3kit", "b3_castes", "b3_beasts", "b3_odd", "b3_deep", "b3_wilds", "b3_people"]
# Family redraws (docs/b3_worklists/families.md) and zone sets: built last, they replace earlier
# sprites by tile key.
FAMILY_BATCHES = ["fam_frogs", "fam_reptiles", "fam_templars", "moonstair", "fam_feedback", "fam_stilt"]
RESTYLED = set()  # names whose hand-drawn idle frame no longer matches


def apply_b3():
    """Swap old character sprites for approved B3 ones, in place in the source dicts."""
    import kit3a, kit3b
    groups = {"kit": K.CREATURES, "kit2": K2.CREATURES2, "kit3a": kit3a.CREATURES3A, "kit3b": kit3b.CREATURES3B,
              "castes": K.CASTES, "tiles": S}
    n = 0
    for mod_name in B3_BATCHES:
        m = importlib.import_module(mod_name)
        for group, sprites in getattr(m, "OVERRIDES", {}).items():
            for name, grid in sprites.items():
                assert name in groups[group], (mod_name, group, name)
                groups[group][name] = grid
                RESTYLED.add(name)
                n += 1
    if "b3kit" in B3_BATCHES:
        import b3kit
        K.MUTATIONS.clear()
        K.MUTATIONS.update(b3kit.MUTATIONS)
    print(f"B3 restyle: {n} sprites from {len(B3_BATCHES)} batches")

HUMANOID = {"creatures/sw/gunwing", "creatures/farmer/convert", "creatures/npc-mehmet", "creatures/npc-argyve",
            "creatures/npc-irudad", "creatures/npc-yrame", "creatures/npc-nima-ruda", "creatures/sw/craigsmench",
            "creatures/naphtaali/forager", "creatures/sw/templar", "creatures/sw/templar/gunner",
            "creatures/sw/templar/squire", "creatures/sw/barathrumite", "creatures/sw/farmer"}
HUMANOID |= {f"creatures/sw/farmer{i}" for i in range(1, 7)}


def ref_index():
    out = collections.defaultdict(list)
    for f in os.listdir(REF):
        out[key(f[:-4])].append(f)
    return out


def family_keys(idx, prefix):
    """All keys of a painted family, e.g. prefix 'tiles/wall/rock-' or 'tiles/fence/'."""
    return sorted(k for k in idx if k.startswith(prefix) and re.fullmatch(r"[01]{8}|[nsew]*", k[len(prefix):]))


def targets(idx):
    """(key, grid, kind, flip, example blueprint or None)."""
    t = []

    def add(k, grid, kind, flip=False, example=None):
        t.append((k, grid, kind, flip, example))

    # --- Phase 2 set ---
    add("creatures/sw/gunwing", S["gunwing"], "object")
    for k in ["creatures/sw/farmer"] + [f"creatures/sw/farmer{i}" for i in range(1, 7)]:
        add(k, S["farmer"], "object", example="WatervineFarmerJoppa")
    add("creatures/sw/snapjaw", S["snapjaw"], "object")
    add("creatures/sw/glowfish", S["glowfish"], "object")
    add("tiles/sw/chest", S["chest"], "object")
    add("tiles/sw/torch/nofire", S["torch_lit"], "object")
    add("terrain/sw/fattree1", S["tree"], "tall")
    add("terrain/sw/fattree2", S["tree"], "tall", flip=True)
    add("tiles/tile-dirt1", T.ground(1), "terrain")
    add("tiles/tile-grass1", T.grass(1), "terrain")
    for i in (1, 2, 3):
        add(f"tiles/sw/watervine{i}", T.shifted(S["watervine"], (i - 1) * 5), "terrain")
        add(f"terrain/sw/grass{i}", T.grass(i + 1), "terrain")
    for i in (1, 2, 3, 4):
        add(f"terrain/sw/ground/dots{i}", T.floor(i), "terrain")
    for k in family_keys(idx, "walls/wall/brinestalk-"):
        add(k, T.wall(k[-8:]), "terrain", example="BrinestalkWall")
    for k in family_keys(idx, "liquids/water/deep-"):
        add(k, T.water(k[-8:], deep=True), "terrain", example="Pond")
    for k in family_keys(idx, "liquids/water/shallow-"):
        add(k, T.water(k[-8:], deep=False), "terrain", example="Pond")

    # --- Batch 1: terrain & walls ---
    for prefix, material, ex in (("tiles/wall/rock-", "rock", "Shale"), ("tiles/wall/marble-", "salt", "Halite"),
                                 ("tiles/wall/metal-", "metal", "RustedMetalWall"), ("tiles/wall/mud-", "slab", "Fulcrete"),
                                 ("tiles/wall/brick-", "canvas", "CanvasWall")):
        for k in family_keys(idx, prefix):
            add(k, T2.painted_wall(material, k[-8:]), "terrain", example=ex)
    for k in family_keys(idx, "tiles/fence/"):
        add(k, T2.fence(k[len("tiles/fence/"):]), "object", example="BrinestalkFence")
    for k in family_keys(idx, "tiles/tent/"):
        add(k, T2.tent(k[len("tiles/tent/"):]), "object", example="CanvasWall")
    add("tiles/tile-0-13", T2.painted_wall("rock"), "terrain", example="Shale")
    add("tiles/sw/doorclosed", T2.door_closed(), "terrain", example="Door")
    add("tiles/sw/dooropen", T2.door_open(), "terrain", example="Door")
    add("tiles/tile-brinestalk", T2.brinestalk(), "tall", example="Brinestalk")
    for i in (1, 2, 3, 4):
        add(f"liquids/water/puddle/{i}", T2.puddle(i), "terrain", example="FreshWaterPuddle")
    for m in range(16):   # small shallow liquids, picked at runtime (BrightQud.cs LiquidTile)
        add(f"liquids/trickle/{m}", T2.trickle(m), "terrain", example="FreshWaterPuddle")
    for i in range(1, 13):
        add(f"terrain/sw/ground/desert/{i}", T2.dune(i), "terrain")
    add("terrain/sw/starappletree", T2.starapple_tree(), "tall", example="Starapple Tree")
    add("terrain/sw/fattree3", T2.witchwood_tree(), "tall", example="Witchwood Tree")
    add("items/sw/smallboulder", T2.boulder(), "object", example="SmallBoulder")
    add("terrain/sw/crack", T2.crack(), "terrain")

    # --- Batches 3-5: creatures ---
    creatures = {
        "creatures/farmer/convert": "convert", "creatures/npc-mehmet": "mehmet", "creatures/npc-argyve": "argyve",
        "creatures/npc-irudad": "irudad", "creatures/npc-yrame": "yrame", "creatures/npc-nima-ruda": "nima",
        "creatures/sw/dromad": "dromad", "creatures/sw/kitty": "cat", "creatures/sw/dog": "dog",
        "creatures/sw/goat": "goat", "creatures/sw/glowpad": "glowpad", "creatures/sw/giantdragonfly": "dragonfly",
        "creatures/sw/qudzu": "qudzu", "creatures/sw/dreadroot": "dreadroot", "creatures/sw/bat": "bat",
        "creatures/sw/seed/spitting/vine": "seed_vine", "creatures/sw/young/ivory": "young_ivory",
        "creatures/sw/plant": "plant", "creatures/sw/croc": "croc", "creatures/sw/salthopper": "salthopper",
        "creatures/sw/snapjaw/hunter": "snapjaw_hunter", "creatures/sw/snapjaw/bruiser": "snapjaw_brute",
        "creatures/sw/snapjaw/warrior": "snapjaw_warrior", "creatures/sw/snapjaw/rogue": "snapjaw_warlord",
        "creatures/sw/snapjaw/spearthrower": "snapjaw_spearthrower", "creatures/sw/snapjaw/netter": "snapjaw_netter",
        "creatures/sw/snapjaw/howler": "snapjaw_howler", "creatures/sw/snapjaw/feeder": "snapjaw_feeder",
        "creatures/sw/snapjaw/gunner": "snapjaw_gunner", "creatures/sw/solifuge": "girshling",
        "creatures/sw/spider": "spider", "creatures/sw/beetle": "beetle", "creatures/sw/centipede": "centipede",
        "creatures/sw/amoeba": "jel", "creatures/sw/leech": "leech", "creatures/sw/scorpiock": "scorpiock",
        "creatures/sw/baboon": "baboon", "creatures/sw/angrybear": "bear", "creatures/sw/boar": "boar",
        "creatures/sw/crab": "crab", "creatures/sw/sparktick": "sparktick",
        "creatures/sw/craigsmench": "cannibal", "creatures/naphtaali/forager": "naphtaali",
        "creatures/sw/templar": "templar", "creatures/sw/templar/gunner": "templar_gunner",
        "creatures/sw/templar/squire": "templar_squire", "creatures/sw/barathrumite": "barathrumite",
        "creatures/sw/mushroom": "mushroom", "creatures/sw/prickler": "prickler", "creatures/sw/urchin": "urchin",
        "creatures/sw/fish/school/1": "fish_school", "creatures/sw/palm": "palm", "creatures/sw/aloe/solo": "aloe",
        "creatures/sw/yonderbrush": "yonderbrush", "creatures/sw/waydroid": "waydroid",
        "creatures/albino-ape": "albino_ape", "creatures/sw/flower": "asphodelyte", "creatures/sw/bugbear": "cragmensch",
        "creatures/sw/voider": "voider", "creatures/sw/ant": "ant", "creatures/sw/knollworm": "knollworm",
        "creatures/sw/flybot": "flybot", "creatures/sw/tombbot/large/2": "tombbot",
    }
    for k, name in creatures.items():
        add(k, CR[name], "object")
    add("creatures/sw/fish/school/2", CR["fish_school"], "object", flip=True)
    for i in (1, 2, 3, 4):
        add(f"creatures/sw/reef/urchin/{i}", CR["urchin"], "object", flip=bool(i % 2))

    # --- Phase 4 (A): calling / caste / pregen player sprites ---
    for k, grid in K.CASTES.items():
        add(k, grid, "object")
        HUMANOID.add(k)

    # --- Batch 2: furniture & items ---
    simple = {"items/sw/bed": "bed", "items/sw/basket": "basket", "tiles/sw/table": "table", "items/sw/chair": "chair",
              "items/sw/floor/cushion": "cushion", "items/sw/dresser": "dresser",
              "items/sw/table/low/drawers": "book_table", "items/sw/bedroll": "bedroll", "items/sw/jug": "vase",
              "items/sw/jug2": "bottle", "tiles/tile-7-3": "garbage", "items/bit11": "scrap",
              "items/sw/waterskin": "waterskin", "items/sw/canteen": "canteen", "items/sw/torch": "torch_item",
              "items/sw/torch/lit": "torch_item_lit", "items/sw/vinewafer": "vinewafer",
              "items/sw/chest/hightier1": "chest_fine", "items/sw/chest/hightier2": "chest_fine",
              "items/sw/sign/pepper": "sign", "items/sw/sign/graveyard": "sign", "items/sw/sign/datadisc": "sign",
              "items/sw/oven": "oven"}
    for k, name in simple.items():
        add(k, IS[name], "object")
    # --- Region batch 6: jungles, hills, canyons, flower fields, ruins, dunes, water (art/src/kit2.py) ---
    for k, (name, kind) in K2.KEYS2.items():
        if k in idx:
            add(k, K2.CREATURES2.get(name) or K2.PLANTS2[name], kind)
            if name in K2.HUMANOID2:
                HUMANOID.add(k)
    for k in ("terrain/sw/talltree1", "terrain/sw/talltree2"):
        add(k, T2.witchwood_tree(), "tall", flip=k.endswith("2"), example="Witchwood Tree")
    # --- Agent-drawn batches (art/src/items3.py, kit3a.py, kit3b.py): (module, sprites, keys, humanoids) ---
    batches = ((("items3", "ITEMS3", "KEYS3", None),
                                                        ("kit3a", "CREATURES3A", "KEYS3A", "HUMANOID3A"),
                                                        ("kit3b", "CREATURES3B", "KEYS3B", "HUMANOID3B"))
                                                       + tuple((f"b3more_{i}", "SPRITES", "KEYS", "HUMANOID") for i in range(1, 9))
               + tuple((f"items4_{i}", "SPRITES", "KEYS", None) for i in range(1, 9))
               + tuple((f"fixtures_{i}", "SPRITES", "KEYS", None) for i in range(1, 4))
               + tuple((f"terrain3_{i}", "SPRITES", "KEYS", None) for i in range(1, 5))
               + (("extras", "SPRITES", "KEYS", None),))
    for mod_name, sprites_attr, keys_attr, hum_attr in batches:
        if mod_name not in APPROVED_BATCHES:
            continue
        m = importlib.import_module(mod_name)
        sprites, keys = getattr(m, sprites_attr), getattr(m, keys_attr)
        humans = getattr(m, hum_attr, set()) if hum_attr else set()
        for k, v in keys.items():
            name, kind = v if isinstance(v, tuple) else (v, "object")
            kind = getattr(m, "KINDS", {}).get(name, kind)
            if k in idx and k not in {x[0] for x in t} and name in sprites:
                add(k, sprites[name], kind)
                if name in humans:
                    HUMANOID.add(k)
    # --- Item batch 1: most-seen weapons, armor, food, loot (art/src/items2.py) ---
    for k, name in I2.KEYS.items():
        if k in idx:
            add(k, I2.ITEMS2[name], "object")
    for i in (1, 2, 3, 4):
        add(f"items/sw/cushion{i}", IS["cushion"], "object", example="Floor Cushion")
        add(f"items/sw/trash/{i}", IS["garbage"], "object", flip=bool(i % 2), example="Garbage")
    for n in (1, 2, 3):
        for k in family_keys(idx, f"tiles/sw/axle/{n}/"):
            add(k, IT.axle(k[len(f"tiles/sw/axle/{n}/"):]), "object", example="WoodenMechanicalTransmission")
    # --- Family redraws (art/src/fam_*.py): replace whatever drew these keys before ---
    for mod_name in FAMILY_BATCHES:
        m = importlib.import_module(mod_name)
        humans = getattr(m, "HUMANOID", set())
        for k, v in m.KEYS.items():
            if k not in idx:
                continue
            name, kind = v if isinstance(v, tuple) else (v, "object")
            t[:] = [x for x in t if x[0] != k]
            add(k, m.SPRITES[name], kind)
            if name in humans:
                HUMANOID.add(k)
            else:
                HUMANOID.discard(k)
    return t


def color_letters(bp, name):
    cs = bp.part(name, "Render", "ColorString") or ""
    tc = bp.part(name, "Render", "TileColor") or ""
    src = tc if "&" in tc else cs
    fg = src[src.rindex("&") + 1] if "&" in src else "y"
    det = (bp.part(name, "Render", "DetailColor") or fg)[:1]
    fg = fg if fg in C.QUD else "y"
    det = det if det in C.QUD else fg
    return fg, det


def users_by_key(bp):
    out = collections.defaultdict(list)
    for name, o in bp.objs.items():
        if "BaseObject" in o["tags"]:
            continue
        for k in tiles_of(bp, name):
            out[k].append(name)
    return out


def write(img, rel):
    dest = os.path.join(MOD, "Textures", rel)
    os.makedirs(os.path.dirname(dest), exist_ok=True)
    img.save(dest)


def flat_name(k):
    """Flat file name that the game normalises back to key k ('/' -> '_')."""
    return k.replace("/", "_") + ".png"


def main():
    apply_b3()
    idx = ref_index()
    bp = Blueprints()
    add_random_tiles(bp)
    users = users_by_key(bp)
    shutil.rmtree(os.path.join(MOD, "Textures"), ignore_errors=True)
    built, missing_ref = [], []
    for k, grid, kind, flip, example in targets(idx):
        if k not in idx:
            missing_ref.append(k)
        ex = example if example in bp.objs else (sorted(users.get(k, []))[:1] or [None])[0]
        fg, det = color_letters(bp, ex) if ex else ("y", "w")
        img, mask = B.render(grid, kind, fg=fg, detail=det, with_mask=True)
        if flip:
            img, mask = ImageOps.mirror(img), ImageOps.mirror(mask)
        write(img, flat_name(k))
        write(mask, "BrightQudMask/" + flat_name(k))
        built.append(k)
    # Idle-animation second frames for some creatures (others get an automatic bob).
    frame_keys = {"gunwing": ["creatures/sw/gunwing"], "bat": ["creatures/sw/bat"],
                  "dragonfly": ["creatures/sw/giantdragonfly"], "flybot": ["creatures/sw/flybot"]}
    for name, grid in K.frames(S).items():
        if name in RESTYLED:
            continue
        for k in frame_keys[name]:
            ex = (sorted(users.get(k, []))[:1] or [None])[0]
            fg, det = color_letters(bp, ex) if ex else ("y", "K")
            img, mask = B.render(grid, "object", fg=fg, detail=det, with_mask=True)
            write(img, flat_name("brightqudframe/" + k))
            write(mask, "BrightQudMask/" + flat_name("brightqudframe/" + k))
    # Slow ambient frames (Moon Stair floor twinkle): frames 1-3 as brightqudframe{,2,3}/<key>;
    # the runtime cycles them with a per-cell offset.
    import moonstair
    for k, frames in moonstair.FRAMES.items():
        ex = (sorted(users.get(k, []))[:1] or [None])[0]
        fg, det = color_letters(bp, ex) if ex else ("m", "m")
        for i, grid in enumerate(frames, 1):
            fk = ("brightqudframe" if i == 1 else f"brightqudframe{i}") + "/" + k
            img, mask = B.render(grid, "terrain", fg=fg, detail=det, with_mask=True)
            write(img, flat_name(fk))
            write(mask, "BrightQudMask/" + flat_name(fk))
    # Zone floor tiles the runtime picks per cell (Rainbow Wood lush moss, Joppa earth) and their frames.
    import rainbowwood, groundsets
    for k, grid in rainbowwood.SPRITES.items():
        frames = [grid] + rainbowwood.FRAMES.get(k, [])
        for i, fr in enumerate(frames):
            fk = k if i == 0 else ("brightqudframe" if i == 1 else f"brightqudframe{i}") + "/" + k
            img, mask = B.render(fr, "terrain", fg="g", detail="g", with_mask=True)
            write(img, flat_name(fk))
            write(mask, "BrightQudMask/" + flat_name(fk))
    # Ground family textures (exact colours, never recoloured: an empty role mask).
    for k, im in groundsets.all_tiles().items():
        write(im, flat_name(k))
        write(Image.new("RGBA", im.size, (0, 0, 0, 0)), "BrightQudMask/" + flat_name(k))
    # Player looks, chosen in the game's Options (see Options.xml, written below).
    looks = K.player_looks(S)
    if "b3kit" in B3_BATCHES:
        import b3kit
        looks = dict(b3kit.LOOKS)
    for name, grid in looks.items():
        k = "brightqudlook/" + name.lower()
        img, mask = B.render(grid, "object", fg="y", detail="K", with_mask=True)
        write(img, flat_name(k))
        write(mask, "BrightQudMask/" + flat_name(k))
        built.append(k)
        HUMANOID.add(k)
    write_options(list(looks))
    # Mutation overlays (front/back layers composited at runtime).
    for name, (layer, ov) in K.MUTATIONS.items():
        img, mask = B.render(K.compose([K.E] * 24, ov), "overlay", fg="y", detail="K", with_mask=True)
        k = "brightqudmut/" + name.lower()
        write(img, flat_name(k))
        write(mask, "BrightQudMask/" + flat_name(k))
    # Paper doll layers (player built from worn gear, docs/PAPERDOLL_BRIEF.md): brightquddoll/<layer key>,
    # no outline/shadow (the runtime outlines the stacked figure). Chitin letters become roles 1-6 so the
    # runtime can give each character its own chitin pair.
    doll = doll_layers()
    for key, grid in doll.items():
        if key in DP.CHITIN_LAYERS:
            grid = ["".join(DP.CHITIN_ROLES.get(ch, ch) for ch in row) for row in grid]
        img, mask = B.render([row.replace("x", ".") for row in grid], "terrain", fg="y", detail="K", with_mask=True)
        write(img, flat_name("brightquddoll/" + key))
        write(mask, "BrightQudMask/" + flat_name("brightquddoll/" + key))
    write_doll_table(bp, doll)
    # Aliased wall families: 16 N/E/S/W variants per material (runtime maps the game's 256 masks).
    for mat in sorted(set(T2.ALIAS_FAMILIES.values()) | set(T2.EXTRA_WALL_MATERIALS)):
        for suffix, mask8 in T2.alias_variants():
            k = f"brightqudwall/{mat}-{suffix}"
            img, mask = B.render(T2.painted_wall(mat, mask8), "terrain", fg="w", detail="c", with_mask=True)
            write(img, flat_name(k))
            write(mask, "BrightQudMask/" + flat_name(k))
    # Gas clouds (soft translucent puffs, 4 animation frames).
    for i in range(4):
        img, mask = FX.gas(i)
        write(img, flat_name(f"tiles2/gas/{i}"))
        write(mask, "BrightQudMask/" + flat_name(f"tiles2/gas/{i}"))
    # Legend icons (Options → Mods → show legend), empty mask = shown as drawn.
    for name, img in legend.build(os.path.join(MOD, "Textures")).items():
        k = "brightqudlegend/" + name
        write(img, flat_name(k))
        write(Image.new("RGBA", (16, 24), (0, 0, 0, 0)), "BrightQudMask/" + flat_name(k))
    write_generated(built)
    print(f"built {len(built)} tiles + {len(K.MUTATIONS)} mutation overlays")
    if missing_ref:
        print("WARNING keys not found in the game's tiles:", missing_ref)


def write_options(looks):
    values = ",".join(["Worn gear", "Game default"] + looks)
    src = f'''<?xml version="1.0" encoding="utf-8" ?>
<!-- GENERATED by tools/build_mod.py - do not edit by hand. -->
<options>
  <option ID="OptionBrightQudPlayerLook" DisplayText="Bright Qud: player look (Worn gear = your character shows what you wear)" Category="Mods" Type="Combo" Values="{values}" Default="Worn gear"></option>
  <option ID="OptionBrightQudNpcDoll" DisplayText="Bright Qud: human NPCs show the gear they wear" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudAnimation" DisplayText="Bright Qud: creature animation (bobbing, flapping wings)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudTileAnimation" DisplayText="Bright Qud: animated tiles (twinkles, glows, torch flicker; off by default)" Category="Mods" Type="Checkbox" Default="No"></option>
  <option ID="OptionBrightQudAutoStyle" DisplayText="Bright Qud: restyle tiles that aren't redrawn yet" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesCreatures" DisplayText="Bright Qud: new creature sprites (off = the game's sprites, with the outline)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesPlants" DisplayText="Bright Qud: new plant and tree sprites (off = the game's sprites)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesItems" DisplayText="Bright Qud: new item sprites (off = the game's sprites)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesFurniture" DisplayText="Bright Qud: new furniture and statue sprites (off = the game's sprites)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesWalls" DisplayText="Bright Qud: new wall sprites (off = the game's sprites)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudSpritesLiquids" DisplayText="Bright Qud: new liquid sprites and zone liquid colours (off = the game's sprites)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudShowMutations" DisplayText="Bright Qud: show mutations on characters (wings, horns, extra arms...)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudGround" DisplayText="Bright Qud: colored ground instead of black" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudThreatRings" DisplayText="Bright Qud: red/green rings under enemies/allies" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudHealthBars" DisplayText="Bright Qud: health bars over hurt creatures" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudItemSparkle" DisplayText="Bright Qud: sparkle on items lying on the ground" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudPlayerMarker" DisplayText="Bright Qud: ring under your character" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudLowHealth" DisplayText="Bright Qud: red pulsing ring when your health is low" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudTalkMarkers" DisplayText="Bright Qud: speech bubble on merchants and named characters" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudInteractMarkers" DisplayText="Bright Qud: gold corner on stairs and filled containers (F6 toggles this and the sparkle)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudClearMemory" DisplayText="Bright Qud: clearer remembered areas (out of sight)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudFireOverlay" DisplayText="Bright Qud: draw flames on burning things (instead of a flashing square)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudEffectGround" DisplayText="Bright Qud: ground instead of black squares behind effect tiles" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudDangerTint" DisplayText="Bright Qud: world map tints regions too dangerous for your level (orange/red)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudLookStatsMode" DisplayText="Bright Qud: key stats on look / hover (With scanning = creature stats need bio, tech or structure scanning)" Category="Mods" Type="Combo" Values="With scanning,Always,Off" Default="With scanning"></option>
  <option ID="OptionBrightQudQuestBanner" DisplayText="Bright Qud: quest banner (follow a quest from the Quests list: LT + left stick click)" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudExplainPowers" DisplayText="Bright Qud: explain mutations and skills when looking" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudFont" DisplayText="Bright Qud: text font (Clear mono = detailed and aligned, Readable = easiest to read)" Category="Mods" Type="Combo" Values="Game default,Clear mono,Readable" Default="Clear mono"></option>
  <option ID="OptionBrightQudTheme" DisplayText="Bright Qud: interface colours (Tan parchment = light, experimental)" Category="Mods" Type="Combo" Values="Qud teal,Tan parchment,Amber,Rust,Violet,Slate" Default="Qud teal"></option>
  <option ID="OptionBrightQudAbilityBar" DisplayText="Bright Qud: abilities shown at once on the ability bar" Category="Mods" Type="Combo" Values="Game default,More,Most" Default="More"></option>
  <option ID="OptionBrightQudAbilityHelp" DisplayText="Bright Qud: explain abilities when pointed at or selected" Category="Mods" Type="Checkbox" Default="Yes"></option>
  <option ID="OptionBrightQudControls" DisplayText="Bright Qud: controls reminder (in game: LT + View)" Category="Mods" Type="Button" OnClick="BrightQud.Controls.Show"></option>
  <option ID="OptionBrightQudLegend" DisplayText="Bright Qud: show legend (what the markers mean)" Category="Mods" Type="Button" OnClick="BrightQud.Legend.Show"></option>
</options>
'''
    with open(os.path.join(MOD, "Options.xml"), "w") as fh:
        fh.write(src)
    import xml.etree.ElementTree as ET
    ET.fromstring(src)  # a malformed Options.xml silently drops every option after the error


def doll_layers():
    import importlib
    layers = {}
    for m in ("doll_base", "doll_body", "doll_gear", "doll_weapons", "doll_mutations", "doll_specials"):
        layers.update(importlib.import_module(m).LAYERS)
    return layers


def write_doll_table(bp, layers):
    """DollTable.cs: blueprint -> doll layer, materials, chitin palettes, layer order, mutation layers."""
    import gear_table as GT
    rows = GT.doll_rows(GT.table(), layers)
    gear = "\n".join(f'            {{ "{n}", new[] {{ "{k}", "{m}", "{"1" if two else ""}" }} }},' for n, k, m, two in rows)
    mats = "\n".join(f'            {{ "{k}", new[] {{ "{a}", "{b}" }} }},' for k, (a, b) in DP.MATERIALS.items())
    chit = "\n".join(f'            new[] {{ "{a}", "{b}" }},' for _, a, b in DP.CHITIN)
    order = ", ".join(f'"{o}"' for o in DP.ORDER)
    muts = {"Carapace": "mutback/carapace", "Wings": "mutback/wings", "Quills": "mutback/quills",
            "Stinger": "mutback/stinger", "MultipleArms": "mutfront/arms", "MultipleLegs": "mutfront/legs",
            "TwoHeaded": "mutfront/twoheads", "Beak": "mutfront/beak", "BurrowingClaws": "mutfront/claws",
            "ThickFur": "mutfront/fur", "Horns": "muthead/horns"}
    mut = "\n".join(f'            {{ "{p}", "{k}" }},' for p, k in muts.items() if k in layers)
    chitin_layers = ", ".join(f'"{k}"' for k in DP.CHITIN_LAYERS)
    src = f'''// GENERATED by tools/build_mod.py (tools/gear_table.py, tools/doll_preview.py) - do not edit by hand.
using System.Collections.Generic;

namespace BrightQud
{{
    public static class DollTable
    {{
        // Stacking order, bottom to top: a layer key's prefix ("body/base" is its own rank).
        public static readonly string[] Order = {{ {order} }};

        // Item blueprint -> {{ layer key, material ("" = item's own colours), two-handed ("1") }}.
        public static readonly Dictionary<string, string[]> Gear = new Dictionary<string, string[]>
        {{
{gear}
        }};

        // Material -> {{ main, detail }} colours.
        public static readonly Dictionary<string, string[]> Materials = new Dictionary<string, string[]>
        {{
{mats}
        }};

        // Chitin pairs {{ shell, legs/stinger }}; one per character from its ID.
        public static readonly string[][] Chitin =
        {{
{chit}
        }};
        public static readonly HashSet<string> ChitinLayers = new HashSet<string> {{ {chitin_layers} }};

        // Mutation part name -> its doll layer.
        public static readonly Dictionary<string, string> Mutations = new Dictionary<string, string>
        {{
{mut}
        }};
    }}
}}
'''
    with open(os.path.join(MOD, "DollTable.cs"), "w") as fh:
        fh.write(src)


def prefix_group(k):
    """Same rules as SpriteSets.GroupOf in BrightQud.cs."""
    for pre, g in (("liquids/", 6), ("creatures/", 1), ("items/", 3), ("furniture/", 4), ("walls", 5)):
        if k.startswith(pre):
            return g
    return 5 if re.search(r"-[^-]{8}$", k) else 0


PLANT_BASES = {"BasePlant", "Plant", "Tree", "Bush", "BaseTree", "MutatedFlower", "MutatedBush", "Grass", "Vine"}


def sprite_groups(built):
    """Shipped tile key -> sprite set, for the keys the folder gets wrong."""
    bp = Blueprints()
    add_random_tiles(bp)
    out = {}
    for name, o in bp.objs.items():
        chain, n = set(), name
        while n in bp.objs and n not in chain:
            chain.add(n)
            n = bp.objs[n]["inh"]
        group = (2 if chain & PLANT_BASES else 1 if "Creature" in chain else 5 if "Wall" in chain
                 else 4 if "Furniture" in chain or "Statue" in chain else 3 if "Item" in chain else 0)
        if not group:
            continue
        for t in tiles_of(bp, name):
            k = key(t)
            if k in built and not k.startswith("brightqud") and prefix_group(k) != group:
                # a tile used by several kinds of object: the first plant or creature wins
                out.setdefault(k, group)
    return out


def write_generated(built):
    v = B.VARIANTS[B.CHOSEN]
    pal = {k: B.adjust(P.rgb(h), v["sat"], v["light"]) for k, h in P.PALETTE.items()}
    hx = lambda rgb: "%02x%02x%02x" % rgb
    humanoid = sorted(k for k in HUMANOID if k in built)
    groups = "\n".join(f'            {{ "{k}", {g} }},' for k, g in sorted(sprite_groups(set(built)).items()))
    muts = "\n".join(f'            {{ "{n}", {"true" if layer == "back" else "false"} }},'
                     for n, (layer, _) in K.MUTATIONS.items())
    tints = "\n".join(f'            {{ "{n}", new[] {{ "{hx(pal[a])}", "{hx(pal[b])}" }} }},'
                      for n, (a, b) in K.SKIN_TINTS.items())
    keys = "\n".join(f'            "{k}",' for k in humanoid)
    aliases = "\n".join(f'            {{ "{p}", "{m}" }},' for p, m in sorted(T2.ALIAS_FAMILIES.items()))
    src = f'''// GENERATED by tools/build_mod.py - do not edit by hand.
using System.Collections.Generic;

namespace BrightQud
{{
    public static class Generated
    {{
        // Tiles drawn on the kit's HUMAN layout: mutation overlays line up with these.
        public static readonly HashSet<string> HumanoidKeys = new HashSet<string>
        {{
{keys}
        }};

        // Mutation part name -> drawn behind the body (true) or in front (false).
        // Overlay texture key: "brightqudmut/" + name.ToLower().
        public static readonly Dictionary<string, bool> Mutations = new Dictionary<string, bool>
        {{
{muts}
        }};

        // Painted wall family prefix -> our material ("brightqudwall/<material>-<nesw>").
        public static readonly Dictionary<string, string> WallAliases = new Dictionary<string, string>
        {{
{aliases}
        }};

        // Sprite set of the tiles whose folder doesn't tell (SpriteSets.GroupOf): 1 creatures, 2 plants, 3 items,
        // 4 furniture, 5 walls, 6 liquids.
        public static readonly Dictionary<string, int> SpriteGroups = new Dictionary<string, int>
        {{
{groups}
        }};

        // Skin colors in our tiles ('s' light, 'S' shadow) and their replacements per mutation.
        public static readonly string[] Skin = {{ "{hx(pal['s'])}", "{hx(pal['S'])}" }};
        public static readonly Dictionary<string, string[]> SkinTints = new Dictionary<string, string[]>
        {{
{tints}
        }};
    }}
}}
'''
    with open(os.path.join(MOD, "Generated.cs"), "w") as fh:
        fh.write(src)


if __name__ == "__main__":
    main()
