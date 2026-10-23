"""Style E = the CURRENT Bright Qud characters (big-head caricature), for side-by-side comparison."""
from kit import CREATURES as CR, MUTATIONS, human, player_looks, compose
from tiles import SPRITES as S


def _mutant(name):
    layer, ov = MUTATIONS[name]
    base = human()
    if layer == "front":
        return compose(base, ov)
    back = compose(["." * 16] * 24, ov)
    return [''.join(b if h == "." else h for h, b in zip(hr, br)) for hr, br in zip(base, back)]


CHARACTERS = {
    "gunslinger": player_looks(S)["Gunslinger"],
    "winged": _mutant("Wings"), "horned": _mutant("Horns"), "four_arms": _mutant("MultipleArms"),
    "carapace": _mutant("Carapace"), "mehmet": CR["mehmet"], "farmer": S["farmer"], "snapjaw": S["snapjaw"],
    "snapjaw_hunter": CR["snapjaw_hunter"], "glowfish": S["glowfish"], "girshling": CR["girshling"],
    "dog": CR["dog"], "salthopper": CR["salthopper"], "croc": CR["croc"],
}
