// Look / hover descriptions (Options → Mods → "explain mutations and skills when looking"):
// one short plain-words line per mutation and per fight-relevant skill, added by LookStatsPatch.
//   - Mutations: hand-written line from MutationHelp (key = mutation class), else the game's own
//     description cut to its first sentence ("You beguile..." becomes "can beguile...").
//   - Skills: only the powers listed in SkillHelp (key = skill part name); everything else is
//     noise in a fight.
//   - Status: active, visible effects (stunned, on fire...).
// Names: mutations magenta, skills cyan.
// Colour: R = dangerous to you, W = be careful, null = harmless / good to know.

using System;
using System.Collections.Generic;
using System.Text.RegularExpressions;
using XRL.World;
using XRL.World.Parts;
using XRL.World.Parts.Mutation;
using XRL.World.Parts.Skill;
using QudColor = ConsoleLib.Console.ColorUtility;

namespace BrightQud
{
    public static class Explain
    {
        // Panel budget on the Deck: mutations first, skills fill what is left.
        const int MaxMutations = 5, MaxSkills = 3, MaxLines = 7, MaxEffects = 4, FallbackChars = 60;

        static readonly Dictionary<string, (string text, string color)> MutationHelp =
            new Dictionary<string, (string, string)>
        {
            // Physical
            { "AdrenalControl2", ("can boost its own speed in a pinch", "W") },
            { "Beak", ("extra peck attack", null) },
            { "BurrowingClaws", ("digs through walls; claw attacks", null) },
            { "Burrowing", ("digs through walls", null) },
            { "Carapace", ("hard shell: high armor", null) },
            { "CorrosiveGasGeneration", ("breathes out acid gas - keep away", "R") },
            { "HeightenedStrength", ("very strong: hits harder", "W") },
            { "ElectricalGeneration", ("builds up charge and zaps you", "R") },
            { "ElectromagneticPulse", ("EMP: shuts down your gadgets", "W") },
            { "FlamingRay", ("ranged fire beam, sets you alight", "R") },
            { "FreezingRay", ("ranged cold beam, can freeze you solid", "R") },
            { "HeightenedHearing", ("hears you coming", null) },
            { "HeightenedSmell", ("smells you from far away", null) },
            { "HeightenedSpeed", ("fast: acts more often than you", "W") },
            { "Horns", ("gores with horns, makes you bleed", "W") },
            { "MultiHorns", ("gores with many horns", "W") },
            { "MultipleArms", ("extra arms: more attacks", "W") },
            { "MultipleLegs", ("moves fast", null) },
            { "DarkVision", ("sees in the dark", null) },
            { "NightVision", ("sees in the dark", null) },
            { "Phasing", ("can walk through walls", "W") },
            { "PhotosyntheticSkin", ("heals in sunlight", null) },
            { "Quills", ("quills hurt you when you hit it", "W") },
            { "Regeneration", ("heals quickly, regrows limbs", "W") },
            { "SleepGasGeneration", ("breathes out sleep gas", "R") },
            { "PoisonGasGeneration", ("breathes out poison gas", "R") },
            { "ConfusionGasGeneration", ("breathes out confusion gas", "R") },
            { "NormalityGasGeneration", ("gas that switches off mutations", "W") },
            { "PlasmaGeneration", ("spews burning plasma", "R") },
            { "SlimeGlands", ("spits slime that makes you slip", null) },
            { "AcidSlimeGlands", ("spits burning acid slime", "R") },
            { "Spinnerets", ("spins webs that trap you", "W") },
            { "SpiderWebs", ("spins webs that trap you", "W") },
            { "FrostWebs", ("spins freezing webs", "W") },
            { "Stinger", ("venomous sting", "R") },
            { "StickyTongue", ("pulls you in with its tongue", "W") },
            { "SporePuffer", ("spores can infect you with fungus", "R") },
            { "MagneticPulse", ("pulls metal gear toward it", "W") },
            { "ThickFur", ("thick fur: resists cold", null) },
            { "HeightenedAgility", ("nimble: hard to hit", null) },
            { "TwoHeaded", ("two heads: shrugs off mental attacks", null) },
            { "TwoHearted", ("two hearts: tough", null) },
            { "Wings", ("flies over water and pits", null) },
            { "Gills", ("breathes underwater", null) },
            { "StoneGaze", ("its gaze turns you to stone", "R") },
            { "FearAura", ("makes you flee in fear", "R") },
            { "LiquidSpitter", ("spits liquid at you", "W") },
            { "FireBreather", ("breathes fire in a cone", "R") },
            { "IceBreather", ("breathes ice in a cone", "R") },
            { "FreezeBreath", ("freezing breath, freezes you solid", "R") },
            { "CorrosiveBreather", ("breathes acid in a cone", "R") },
            { "PoisonBreather", ("breathes poison in a cone", "R") },
            { "ConfusionBreather", ("its breath confuses you", "R") },
            { "StunBreather", ("its breath stuns you", "R") },
            { "SleepBreather", ("its breath puts you to sleep", "R") },
            { "NormalityBreather", ("breath switches off mutations", "W") },
            { "Invisibility", ("can turn invisible", "W") },
            // Mental
            { "Beguiling", ("can charm a creature into serving it", "W") },
            { "Burgeoning", ("makes plants burst from the ground", "W") },
            { "Clairvoyance", ("sees far-off places", null) },
            { "Confusion", ("can confuse you (you stumble around)", "R") },
            { "Cryokinesis", ("freezes an area from afar", "R") },
            { "Disintegration", ("disintegrates everything around it", "R") },
            { "Domination", ("can take over your body", "R") },
            { "WillForce", ("boosts its own stats for a while", null) },
            { "ForceBubble", ("shields itself in a force bubble", null) },
            { "ForceWall", ("raises force walls to block you", "W") },
            { "Kindle", ("can set you on fire", "W") },
            { "LightManipulation", ("makes light; fires laser beams", "W") },
            { "MassMind", ("recharges its powers faster", null) },
            { "MentalMirror", ("reflects mental attacks back", "W") },
            { "Precognition", ("can survive one killing blow", "W") },
            { "Psychometry", ("understands artifacts by touch", null) },
            { "Pyrokinesis", ("sets an area on fire from afar", "R") },
            { "SensePsychic", ("senses psychic beings", null) },
            { "SpacetimeVortex", ("opens a vortex that flings you away", "R") },
            { "StunningForce", ("telekinetic blast that stuns you", "R") },
            { "SunderMind", ("psychic attack on your mind", "R") },
            { "LifeDrain", ("drains your life to heal itself", "R") },
            { "Telepathy", ("reads minds, talks from afar", null) },
            { "Teleportation", ("teleports around", null) },
            { "TeleportOther", ("can teleport you somewhere random", "W") },
            { "TimeDilation", ("slows down everyone near it", "W") },
            { "TemporalFugue", ("makes copies of itself", "R") },
        };

        static readonly Dictionary<string, (string text, string color)> SkillHelp =
            new Dictionary<string, (string, string)>
        {
            { "Axe_Cleave", ("its axe hits lower your armor", "W") },
            { "Axe_Dismember", ("can cut off your limbs", "R") },
            { "Axe_Decapitate", ("can behead you", "R") },
            { "Axe_Berserk", ("goes berserk, cuts off limbs", "R") },
            { "Axe_HookAndDrag", ("hooks you and drags you along", "W") },
            { "Cudgel_Bludgeon", ("club hits daze you", "W") },
            { "Cudgel_Slam", ("slams you back up to 3 cells", "W") },
            { "Cudgel_ChargingStrike", ("charges at you", "W") },
            { "Tactics_Charge", ("charges at you", "W") },
            { "Tactics_Juke", ("can swap places with you", null) },
            { "LongBladesLunge", ("lunges at you", "W") },
            { "LongBladesSwipe", ("hits everyone around it", "W") },
            { "ShortBlades_Bloodletter", ("makes you bleed", "W") },
            { "ShortBlades_Hobble", ("hobbles you: halves your speed", "W") },
            { "Shield_Block", ("blocks hits with its shield", null) },
            { "Shield_Slam", ("shield slam knocks you down", "W") },
            { "Persuasion_Intimidate", ("can scare you into fleeing", "W") },
            { "Pistol_Akimbo", ("fires two pistols at once", "W") },
            { "Pistol_DisarmingShot", ("its shots can disarm you", "W") },
            { "Rifle_WoundingFire", ("rifle shots make you bleed", "W") },
            { "Rifle_FlatteningFire", ("shots knock you down, disarm you", "W") },
            { "HeavyWeapons_Sweep", ("sprays a cone of gunfire", "R") },
            { "Tinkering_DeployTurret", ("can set up turrets", "W") },
            { "Tinkering_LayMine", ("can lay mines and bombs", "W") },
        };

        static string Line(string name, string text, string color, string nameColor = "M") =>
            "{{" + nameColor + "|" + name + "}} - " + (color != null ? "{{" + color + "|" + text + "}}" : text);

        // "You beguile a creature into serving you." -> "can beguile a creature into serving it"
        static string Fallback(BaseMutation m)
        {
            string d = QudColor.StripFormatting(m.GetDescription() ?? "").Replace('\n', ' ').Trim();
            if (d.Length == 0 || d.StartsWith("<")) return null;
            int dot = d.IndexOf(". ", StringComparison.Ordinal);
            if (dot > 0) d = d.Substring(0, dot);
            d = d.TrimEnd('.');
            if (d.StartsWith("You ", StringComparison.Ordinal))
            {
                d = "can " + d.Substring(4);
                d = Regex.Replace(d, @"\byourself\b", "itself");
                d = Regex.Replace(d, @"\byour\b", "its");
                d = Regex.Replace(d, @"\byou\b", "it");
            }
            if (d.Length > FallbackChars) d = d.Substring(0, FallbackChars - 3).TrimEnd() + "...";
            return d;
        }

        public static void Append(GameObject o, System.Text.StringBuilder sb)
        {
            int lines = 0;
            var muts = o.GetPart<Mutations>()?.MutationList;
            if (muts != null)
            {
                int shown = 0;
                foreach (var m in muts)
                {
                    if (m == null) continue;
                    if (shown == MaxMutations) { sb.Append("\n{{K|+").Append(muts.Count - shown).Append(" more mutations}}"); break; }
                    string name = QudColor.StripFormatting(m.GetDisplayName(false));
                    string text = null, color = null;
                    string cls = m.GetMutationClass() ?? m.Name;
                    if (cls != null && MutationHelp.TryGetValue(cls, out var help)) (text, color) = help;
                    else
                    {
                        try { text = Fallback(m); } catch (Exception) { text = null; }
                    }
                    sb.Append('\n').Append(text != null ? Line(name, text, color) : "{{M|" + name + "}}");
                    shown++;
                }
                lines += shown;
            }

            var skills = o.GetPart<Skills>()?.SkillList;
            if (skills != null)
            {
                int room = Math.Min(MaxSkills, MaxLines - lines), shown = 0;
                foreach (var s in skills)
                {
                    if (shown >= room) break;
                    if (s == null || !SkillHelp.TryGetValue(s.Name, out var help)) continue;
                    sb.Append('\n').Append(Line(s.DisplayName, help.text, help.color, "C"));
                    shown++;
                }
            }

            var states = new List<string>();
            foreach (var e in o.Effects)
            {
                if (e == null || e.SuppressInLookDisplay()) continue;
                string d = QudColor.StripFormatting(e.GetDescription() ?? "").Trim();
                if (d.Length > 0 && !states.Contains(d) && states.Count < MaxEffects) states.Add(d);
            }
            if (states.Count > 0) sb.Append("\n{{Y|Status:}} ").Append(string.Join(", ", states));
        }
    }
}
