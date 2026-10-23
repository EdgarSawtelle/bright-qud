// Item comparison (Options → Mods → "compare items with what you wear"):
//   - Inventory, pick-up ("get") and trade lists: a short coloured difference after the item's name,
//     e.g. "AV +1 DV -1" or "dmg +1.5", against what you have in that slot (the game's own
//     getComparisonBodypart: same hand, body, head, shield arm...).
//   - Look / tooltip descriptions: a "Compared with your ..." block (added by LookStatsPatch).

using System;
using System.Collections.Generic;
using HarmonyLib;
using Qud.UI;
using XRL;
using XRL.UI;
using XRL.World;
using XRL.World.Parts;
using QudColor = ConsoleLib.Console.ColorUtility;

namespace BrightQud
{
    public static class ItemCompare
    {
        // The item it would replace (or the natural weapon / empty slot), or null if not comparable.
        static bool Target(GameObject item, out GameObject current, out string slot)
        {
            current = null;
            slot = null;
            var player = The.Player;
            if (item == null || player == null || !Settings.CompareItems || !item.Understood()) return false;
            if (item.Equipped == player) return false;
            if (!item.HasPart<MeleeWeapon>() && !item.HasPart<Armor>() && !item.HasPart<Shield>()
                && !item.HasPart<MissileWeapon>()) return false;
            var part = player.getComparisonBodypart(item);
            if (part == null) return false;
            slot = part.Name;
            current = part.Equipped ?? part.DefaultBehavior;
            return current != item;
        }

        // Average roll of a dice string like "1d6", "2d4+1", "5".
        public static double Average(string dice)
        {
            if (dice.IsNullOrEmpty()) return 0;
            double total = 0;
            foreach (var raw in dice.Replace("-", "+-").Split('+'))
            {
                string t = raw.Trim();
                if (t.Length == 0) continue;
                int sign = 1;
                if (t[0] == '-') { sign = -1; t = t.Substring(1); }
                int d = t.IndexOf('d');
                if (d > 0 && int.TryParse(t.Substring(0, d), out int n) && int.TryParse(t.Substring(d + 1), out int sides))
                    total += sign * n * (sides + 1) / 2.0;
                else if (int.TryParse(t, out int k))
                    total += sign * k;
            }
            return total;
        }

        static string Delta(string label, double diff, string unit = "", bool lowerIsBetter = false)
        {
            if (Math.Abs(diff) < 0.05) return null;
            string n = (diff > 0 ? "+" : "") + (Math.Abs(diff % 1) < 0.05 ? ((int)Math.Round(diff)).ToString() : diff.ToString("0.0"));
            bool better = lowerIsBetter ? diff < 0 : diff > 0;
            return "{{" + (better ? "G" : "R") + "|" + label + " " + n + unit + "}}";
        }

        static int AV(GameObject o) => o?.GetPart<Armor>()?.AV ?? o?.GetPart<Shield>()?.AV ?? 0;
        static int DV(GameObject o) => o?.GetPart<Armor>()?.DV ?? o?.GetPart<Shield>()?.DV ?? 0;

        static List<string> Diffs(GameObject item, GameObject current)
        {
            var list = new List<string>();
            void Add(string s) { if (s != null) list.Add(s); }
            var mw = item.GetPart<MeleeWeapon>();
            if (mw != null && !item.HasPart<Armor>() && !item.HasPart<Shield>())
            {
                var cw = current?.GetPart<MeleeWeapon>();
                Add(Delta("dmg", Average(mw.BaseDamage) - Average(cw?.BaseDamage)));
                Add(Delta("pen", mw.PenBonus - (cw?.PenBonus ?? 0)));
            }
            if (item.HasPart<Armor>() || item.HasPart<Shield>())
            {
                Add(Delta("AV", AV(item) - AV(current)));
                Add(Delta("DV", DV(item) - DV(current)));
                var a = item.GetPart<Armor>();
                var c = current?.GetPart<Armor>();
                if (a != null)
                {
                    Add(Delta("heat", a.Heat - (c?.Heat ?? 0)));
                    Add(Delta("cold", a.Cold - (c?.Cold ?? 0)));
                    Add(Delta("elec", a.Elec - (c?.Elec ?? 0)));
                    Add(Delta("acid", a.Acid - (c?.Acid ?? 0)));
                }
            }
            return list;
        }

        // Short tag for list lines, or null.
        public static string Tag(GameObject item)
        {
            try
            {
                if (!Target(item, out var current, out _)) return null;
                if (current == null || current.HasTag("NaturalGear") && !item.HasPart<MeleeWeapon>())
                    return "{{G|[free slot]}}";
                var d = Diffs(item, current);
                return d.Count == 0 ? "{{K|[same]}}" : "{{K|[}}" + string.Join(" ", d) + "{{K|]}}";
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Compare.Tag", e);
                return null;
            }
        }

        // Block for the look / tooltip description, or null.
        public static string Block(GameObject item)
        {
            if (!Target(item, out var current, out string slot)) return null;
            if (current == null) return "{{C|Compared with your " + slot.ToLowerInvariant() + ":}} nothing there now.";
            var d = Diffs(item, current);
            string name = QudColor.StripFormatting(current.ShortDisplayNameStripped ?? "");
            string head = "{{C|Compared with your " + name + "}} {{K|(" + slot.ToLowerInvariant() + ")}}{{C|:}} ";
            string weight = Delta("weight", item.Weight - current.Weight, " lbs", lowerIsBetter: true);
            if (weight != null) d.Add(weight);
            return head + (d.Count == 0 ? "the same." : string.Join(", ", d));
        }

        public static void Append(UITextSkin text, GameObject item)
        {
            if (text == null) return;
            string tag = Tag(item);
            if (tag != null && !text.text.EndsWith(tag)) text.SetText(text.text + " " + tag);
        }
    }

    [HarmonyPatch(typeof(InventoryLine), nameof(InventoryLine.setData), new Type[] { typeof(XRL.UI.Framework.FrameworkDataElement) })]
    public static class InventoryLineComparePatch
    {
        static void Postfix(InventoryLine __instance, XRL.UI.Framework.FrameworkDataElement data)
        {
            try
            {
                if (data is InventoryLineData d && !d.category && d.go != null) ItemCompare.Append(__instance.text, d.go);
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Compare.Inventory", e); }
        }
    }

    [HarmonyPatch(typeof(PickGameObjectLine), nameof(PickGameObjectLine.setData), new Type[] { typeof(XRL.UI.Framework.FrameworkDataElement) })]
    public static class PickLineComparePatch
    {
        static void Postfix(PickGameObjectLine __instance, XRL.UI.Framework.FrameworkDataElement data)
        {
            try
            {
                if (data is PickGameObjectLineData d && d.go != null) ItemCompare.Append(__instance.text, d.go);
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Compare.Pick", e); }
        }
    }

    [HarmonyPatch(typeof(TradeLine), nameof(TradeLine.setData), new Type[] { typeof(XRL.UI.Framework.FrameworkDataElement) })]
    public static class TradeLineComparePatch
    {
        static void Postfix(TradeLine __instance, XRL.UI.Framework.FrameworkDataElement data)
        {
            try
            {
                if (data is TradeLineData d && d.type == TradeLineDataType.Item && d.traderInventory && d.go != null)
                    ItemCompare.Append(__instance.text, d.go);
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Compare.Trade", e); }
        }
    }
}
