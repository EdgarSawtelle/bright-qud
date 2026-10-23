"""Batch 3a: villagers, robots, wights and misc creatures. Humanoids use kit.human() + new overlays."""
from kit import E, compose, human, HOOD, ROBE, STAFF, BOW, HOE, WRENCH, BALD, APRON, GEAR, BOOK
from kit2 import body as _body


def body(rows, **kw):
    return _body([r[:16] for r in rows], **kw)

# ---------------- humanoid parts (HUMAN: head rows 4-13, eyes 10-11, torso 14-18, feet 20) ----------------
# Mechanimist: hooded robe, white trim, cog on chest
MECH_ROBE = {14: "...2222442222...", 15: "..s2224552222s..", 16: "..s2222442222s..", 17: "...3222222223...",
             18: "...2222222222...", 19: "...3333333333...", 20: "....xNNxxNNx...."}
MECH_HOOD = {2: "......4444......", 3: "....44444444....", 4: "...4222222224...", 5: "..422222222224..",
             6: "..322222222223..", 7: "..32........23..", 8: "..32........23..", 9: "..32........23..",
             10: "..32........23..", 11: "..32........23..", 12: "..32........23..", 13: "..33........33.."}
CHORAL = {9: "..............w.", 10: ".............wOw", 11: "..............w."}
# Preacher: tall mitre, long robe, gear staff
MITRE = {0: ".......44.......", 1: "......4444......", 2: ".....445544.....", 3: ".....455554.....",
         4: "....45555554....", 5: "...4444444444...", 6: "...5555555555..."}
PREACH_ROBE = {13: "....44444444....", 14: "...2224444222...", 15: "..s2222442222s..", 16: "..s2222222222s..",
               17: "...3222222223...", 18: "...2222222222...", 19: "...3333333333...", 20: "...xNNNxxNNNx..."}
GEAR_STAFF = {y: "..............n." for y in range(8, 22)} | {4: "............44..", 5: "...........4554.",
              6: "............44.." , 7: "..............n."}
# Hindren: deer-folk (fur from fg roles, antlers straw)
HIND_HEAD = {1: "..t..t....t..t..", 2: "...t.tt..tt.t...", 3: "....tt....tt....",
             4: ".....222222.....", 5: "....22222222....", 6: ".22.22222222.22.", 7: ".2s222222222s2s.",
             8: "..22222222222...".replace("...", "2.."), 9: "...2222222222...",
             12: "....s1NNNN1s....", 13: ".....SSSSSS....."}
HIND_HEAD[8] = "..2222222222222.."[:16]
HIND_HEAD[7] = ".22222222222222."
HIND_TUNIC = {14: "....22222222....", 15: "...s21111222s...", 16: "...s22222222s...", 17: "....33444433....",
              18: "....44444444...."}
HIND_SHAWL = {13: "...4444444444...", 14: "..445555555544..", 15: "..4.22222222.4..", 16: "..s.22222222.s.."}
HIND_SHORT = {1: "......t..t......", 2: ".....tt..tt.....", 3: ".....t....t....."}
STRAW_HAT = {2: "......tttt......", 3: "....tttttttt....", 4: ".tttttttttttttt.", 5: "...tttttttttt..."}
CLOAK = {13: "..666666666666..", 14: "..633222222336..", 15: "..632222222236..", 16: "..632222222236..",
         17: "..633322222336..", 18: "..633333333336.."}
# Mopango: mushroom cap
CAP = {0: "......1111......", 1: "....11111111....", 2: "...1111w1111w...", 3: "..111111111111..",
       4: "..222w22222222..", 5: ".22222222222w222", 6: ".33333333333333.", 7: "....ssssssss....",
       8: "................"}
CAP[2] = "...1111w1111w1..."[:16]
CAP[5] = ".2222w22222222w."
CAP[4] = "..2222222w22222.."[:16]
CAP[7] = "...ssssssssss..."[:16]
CAP[8] = "...ssssssssss..."[:16]
MOP_ROBE = {14: "....55555555....", 15: "...s54444455s...", 16: "...s55555555s...", 17: "....55555555....",
            18: "....44444444....", 19: "....55555555....", 20: "....xNNxxNNx...."}
DELVER_LAMP = {2: "......yyyy......", 3: "......yww y.....".replace(" ", "y")}
PICK = {y: ".............n.." for y in range(8, 20)} | {7: "...........lll..", 6: "..........l..l.."}
# Wight: crowned bone-faced revenant, tattered robe with glowing gem
WIGHT_HEAD = {2: "....4..44..4....", 3: "....4444444444..".replace("4444444444..", "44444444....")[:16],
              4: "....44y44y44....", 5: "...wwwwwwwwww...", 6: "...wwwwwwwwww...", 7: "...wlwwwwwwlw...",
              8: "...wwwwwwwwww...", 9: "...wwwwwwwwww...", 10: "...wOO4wwO4Ow...", 11: "...wOO4wwO4Ow...",
              12: "....wwOOOOww....", 13: ".....wOwOwO....."}
WIGHT_HEAD[3] = "....44444444...."
WIGHT_ROBE = {14: "...3222222223...", 15: "..l2224552222l..", 16: "..l2224442222l..", 17: "..w3222222223w..",
              18: "...2223322223...", 19: "...3.33333.33...", 20: "....xNNxxNNx...."}
WIGHT_SKELHANDS = {15: "..w...........w.", 16: "..w...........w.", 17: "..w.............".replace("w.............", "w...........w.")[:16]}
WIGHT_SKELHANDS[17] = "..w...........w."
# Merchants
TOPHAT = {0: "....33333333....", 1: "....35555553....", 2: "....35555553....", 3: "....35555553....",
          4: "..3333333333333.".replace("3", "3")[:16], 5: "................"}
TOPHAT[4] = "..333333333333.."
COAT_Y = {13: "....22222222....", 14: "..sL22yy2222Ls..", 15: "..sL21yy1222Ls..".replace("yy", "2y"), 16: "..s222222222 s..".replace(" ", "2"),
          17: "...3222222223...", 18: "...2222222222...", 19: "...3333333333...", 20: "....xNNxxNNx...."}
COAT_Y[14] = "...2222222222...".replace("2222222222", "22y44y2222")
COAT_Y[15] = "..s2222yy2222.s.".replace("..s", "..s")[:16]
COAT_Y[15] = "..s222y44y222s.."
COAT_Y[16] = "..s222222222.s.."
COAT_Y[14] = "..s2y44444y22s.."
GEMS = {13: "....4wy44y4w....".replace("....", "....")[:16]}
CHAIN = {13: "....yy..yy......".replace("yy..yy", "y.yy.y")[:16]}
CAPFLAT = {3: "....555555555...", 4: "...55444444555..", 5: "...5555555555...", 6: "..666666666666.."}
LEATHER_APRON = {14: "...nnnnnnnnnn...", 15: "...n22222222n...", 16: "...n2222222n....".replace("n....", "nn..")[:16],
                 17: "...nnn2222nnn...", 18: "....22222222...."}
SHOE = {16: ".NN.............", 17: "NnnN............", 18: "NNNNN..........."}
# Tau pilgrim: hooded, third eye, extra arms
TAU_HOOD = {3: "......3333......", 4: "....33333333....", 5: "...332222O233...".replace("O2", "wO")[:16],
            6: "..332222222233..", 7: "..322222222223..", 8: "..32........23.."}
TAU_ARMS = {14: ".s2222222222s...", 15: "s.2222222222.s..", 16: "s.2222222222.s..", 17: ".s.2222222...s.."}
TAU_ARMS = {15: "s..2222222222..s", 16: "s..2222222222..s", 17: ".s.3222222223.s."}
# Novice of the Sightless Way
BLIND = {10: "...44444444444...".replace("4444444444", "444444444")[:16], 11: "...45555555554..."[:16]}
BLIND = {10: "...4444444444..4", 11: "...4555555554.44"}
NOV_ROBE = {14: "...2222222222...", 15: "..s2211221222s..".replace("1122", "2222")[:16], 16: "..s2222222222s..",
            17: "...3222222223...", 18: "...2222444422...", 19: "...3333333333...", 20: "....xNNxxNNx...."}
NOV_HANDS = {15: "..ss..........ss.", }
NOV_HANDS = {16: "..ss.........ss."}
CANE = {y: "...........n...." for y in range(11, 21)}

# ---------------- non-humanoids ----------------
CREATURES3A = {}
HUMANOID3A = set()


def H(name, *parts):
    parts = [{y: r.ljust(16, ".")[:16] for y, r in d.items()} for d in parts]
    CREATURES3A[name] = human(*parts)
    HUMANOID3A.add(name)


H("mopango_delver", CAP, MOP_ROBE, DELVER_LAMP, PICK)
H("mopango_villager", CAP, MOP_ROBE)
H("mechanimist", MECH_HOOD, MECH_ROBE)
H("mechanimist_preacher", MITRE, PREACH_ROBE, GEAR_STAFF)
H("hindren_villager", HIND_HEAD, HIND_TUNIC, HIND_SHAWL)
H("hindren_farmer", HIND_HEAD, HIND_TUNIC, STRAW_HAT, HOE)
H("hindren_scout", HIND_HEAD, HIND_TUNIC, CLOAK, BOW)
H("gyre_wight", WIGHT_HEAD, WIGHT_ROBE, WIGHT_SKELHANDS)
H("merchant_hatter", TOPHAT, COAT_Y, CHAIN)
H("merchant_shoemaker", CAPFLAT, LEATHER_APRON, SHOE, HAIR := {})
H("tau", TAU_HOOD, TAU_ARMS, ROBE)
H("novice", BALD, BLIND, NOV_ROBE, NOV_HANDS, CANE)

CREATURES3A["rifle_turret"] = body([
    "....LLLLLLLLLL..",
    "....LLwLLLLLLLLL",
    "...LL11111LLLLLL",
    "..L11112222LLLLL",
    "..L12222222L4cc.",
    "..L2222222LL.cc.",
    "..L2332233LL....",
    "...L333333L.....",
    "....L3223L......",
    "...LL.L.LL......",
    "..LL..L..LL.....",
    ".LL...L...LL....",
])

CREATURES3A["voider"] = body([
    "...3......3....",
    "..3.3.33.3.3...",
    ".3..322223..3..",
    "3..32211122..3.",
    "3.3211O11O112.3",
    "..321w1wwww12..",
    "3.32111111123.3",
    "..3322222233.3.",
    ".3..3322233..3.",
    "3..3..333..3..3",
    "...3..3.3..3...",
], bottom=20)

CREATURES3A["templar_mech_2"] = body([
    "......LLLL......",
    ".....L1111L.....",
    "....L1wwww1L....",
    "....L1wccw1L....",
    "..LL.L1111L.LL..",
    ".L11LL2222LL11L.",
    ".L12L122221L21L.",
    ".LL2L222222L2LL.",
    ".rr.L233332L.rr.",
    ".r5.L222222L.5r.",
    "....L333333L....",
    "...LL33..33LL...",
    "...L22....22L...",
    "..LLL3....3LLL..",
    "..L222....222L..",
    ".LLLLL....LLLLL.",
])
CREATURES3A["templar_mech_1"] = body([
    "................",
    "....LL....LL....",
    "...L55LLLL55L...",
    "..L5111111115L..",
    "..L1wwwwwwww1L..",
    "..L1wccwwccw1L..",
    "..L2111111112L..",
    ".L2222222222222L",
    ".L2233333333322L".replace("L", "L")[:16],
    "LL23rrrrrrrr32LL",
    "L.L2333333332L.L",
    "L.LL.L3333L.LL.L",
    "L.L..L.LL.L..L.L",
    "LL...L....L...LL",
    "L....LL..LL....L",
])

CREATURES3A["scrapbot"] = body([
    ".....y..........",
    "......y..LL.....",
    "..4444444444....",
    ".4555555555544..",
    ".4wOw5555wOw54..".replace("4..", "4.."),
    ".45Ow55555Ow54..",
    ".4555555555554..",
    "..4444444444....",
    ".L.1222222221.L.",
    "LL.2222112222.LL",
    "L..2332222332..L",
    "...3333333333...",
    "...L33....33L...",
    "..LLL3....3LLL..",
])

CREATURES3A["godhed"] = body([
    "...2222222222...",
    ".22111111111122.",
    "2111111111111112",
    "211w11111111w112",
    "11wOOw1111wOOw13",
    "111OOw1111wOOw13",
    "1111111221111113",
    "2111112222111113",
    "2111221111221123",
    "2112222222222123",
    ".21122OOOOOO2213.",
    ".3212wOwOwOwO213.",
    "..3322222222333.",
    "...3333333333...",
], bottom=18)

CREATURES3A["interdictor"] = body([
    "......LL........",
    "....1111111.....",
    "...112222211....",
    "..11wwwwww211...",
    "..12wOrrOw2213..",
    "..12wwwwww223...",
    "...2233333333...",
    ".LL.4555555.LL..",
    "L1L.2222222.L1L.",
    "LL.32222222.LLL.",
    "...33322233.....",
    "....3.33.3......",
    "...LL....LL.....",
    "...LL....LL.....",
])

CREATURES3A["kaleidoslug"] = body([
    "...2....2.......",
    "...2....2.......",
    "..O2w..O2w......",
    "..22222222......",
    ".2111222222222..",
    "2114122222522222",
    "21122244222222 2".replace(" ", "2"),
    "221222222445222.",
    ".332222222222233",
    "..33333333333333",
    "......wwwww.....",
])

CREATURES3A["sludge"] = body([
    "....4...........",
    "...454..4.......",
    ".....1111...4...",
    "...11111111.....",
    "..1112222221....",
    ".112O22222O2211.",
    ".12wO222O2w2221.",
    "1122222222222221",
    "1222544222522221",
    "3222222222222223",
    ".33333333333333.",
], bottom=19)

CREATURES3A["chainlaser"] = body([
    "..LLLLLLLLLLLL..",
    ".L111111111111L.",
    ".L122222222221L.",
    ".L4cc4LLLL4cc4L.",
    "LL5cc5L22L5cc5LL",
    "L.4cc4L22L4cc4.L",
    "L..LLLL33LLLL..L",
    "LL.L33333333L.LL",
    ".LLL3333333LLL..",
    "..LLLL.LL.LLLL..",
])

CREATURES3A["pig"] = body([
    "....2......2....",
    "...221....122...",
    "..22222222222...",
    ".2222222222222..",
    "2O2211222222222.",
    "2w2w1222222222 2".replace(" ", ""),
    "4442222222222222",
    "44O4222222222222".replace("2222222222222", "222221222222")[:16],
    "4444233222332222",
    ".w.w.3222223....",
    "....33.33.33.3..",
    "....5.5..5.5....",
], bottom=20)

CREATURES3A["chromeling"] = body([
    "..4......4......",
    "..4.2222.4......",
    "...2111122......",
    "..211wwww12.....",
    "..21wOOwO12.....",
    "..21wOOwO12.....",
    "..2211111222....",
    ".322222222223...",
    ".32222222222233.",
    ".3322222222333..",
    "..33.33.33.33...",
    "..L...L..L...L..",
], bottom=20)

CREATURES3A["nest"] = body([
    "......ww........",
    "...wwwwwwww.....",
    "..wwwwwwwwwww...",
    ".wwwEEEEEEwwww..",
    ".wwEEOrrOEEwww..",
    "wwwEErrrrEEwwww.",
    "wwwwEEEEEEwwwwww",
    "wEwwwwwwwwwwwEww",
    "ewwwwwwwwwwwwwwe",
    ".eeeeeeeeeeeeee.",
], bottom=20)

KEYS3A = {
    "creatures/sw/mopango/delver": "mopango_delver",
    "creatures/sw/rifle/turret": "rifle_turret",
    "creatures/sw/mechanimist": "mechanimist",
    "creatures/sw/hindren/1": "hindren_villager",
    "creatures/sw/preacher2": "mechanimist_preacher",
    "creatures/wight/agolgot": "gyre_wight",
    "creatures/sw/greater/voider": "voider",
    "creatures/sw/templar/mech/2": "templar_mech_2",
    "creatures/sw/templar/mech/1": "templar_mech_1",
    "creatures/merchant-1": "merchant_hatter",
    "creatures/sw/scrapbot": "scrapbot",
    "creatures/sw/hindren/6": "hindren_farmer",
    "creatures/sw/hindren/4": "hindren_scout",
    "creatures/godhed1": "godhed",
    "creatures/sw/interdictor": "interdictor",
    "creatures/wight/bethsaida": "gyre_wight",
    "creatures/wight/shugruith": "gyre_wight",
    "creatures/wight/rermadon": "gyre_wight",
    "creatures/wight/qas": "gyre_wight",
    "creatures/wight/qon": "gyre_wight",
    "creatures/sw/mopango/villager": "mopango_villager",
    "creatures/sw/reef/slug/1": "kaleidoslug",
    "creatures/merchant-3": "merchant_shoemaker",
    "creatures/sw/tau/body": "tau",
    "creatures/sw/sludge": "sludge",
    "creatures/sw/chainlaser/emplacement": "chainlaser",
    "creatures/sw/boar2": "pig",
    "creatures/sw/chromeling": "chromeling",
    "creatures/sw/nest": "nest",
    "creatures/sw/sightless/novice": "novice",
}
KEYS3A = {k: (v, "object") for k, v in KEYS3A.items()}
