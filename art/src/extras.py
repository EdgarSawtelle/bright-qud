"""Small one-off sprites drawn during review (Opus)."""

E = "................"

# Natural weapon "flap" (wing buffet of winged creatures): one feathered wing, shown as an item.
WING_FLAP = [E] * 7 + [
    "...........44...",
    ".........44554..",
    ".......4455554..",
    ".....445555654..",
    "...44555566554..",
    "..4555665565 4..".replace(" ", "5"),
    ".45565556656 4..".replace(" ", "5"),
    ".4656656565654..",
    "..4.5.5.5.5.54..",
    "....4.4.4.4.4...",
    E, E, E, E, E, E, E,
]

SPRITES = {"wing_flap": WING_FLAP}
KEYS = {"creatures/natural-weapon-flap": "wing_flap"}
