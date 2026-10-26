// Paper doll: the player drawn from what they wear (docs/PAPERDOLL_BRIEF.md). The game thread turns the
// player's gear + mutations into a short description ("brightqudpaperdoll|layer,fg,detail;...|c<coat>");
// Recolor resolves it like any tile and stacks the layers (brightquddoll/<layer>) when it builds the texture.
// The description only changes when gear, mutations or a coating change, so the picture is built once.
using System;
using System.Collections.Generic;
using System.Text;
using UnityEngine;
using XRL;
using XRL.World;
using XRL.World.Anatomy;
using GameObject = XRL.World.GameObject;
using QudColor = ConsoleLib.Console.ColorUtility;

namespace BrightQud
{
    public static class Doll
    {
        public const string Prefix = "brightqudpaperdoll|";
        public const string LayerPrefix = "brightquddoll/";

        static volatile string current;
        static int lastTick;
        static string lastPlayerId;

        // Latest description for the player, readable from any thread (UI portraits).
        public static string Current => current;

        // Game thread, while the player's cell renders. shownFg = the colour the game draws the player in
        // (a liquid coating or freezing changes it).
        public static string Update(GameObject player, Color shownFg)
        {
            int now = Environment.TickCount;
            if (current != null && player.ID == lastPlayerId && unchecked(now - lastTick) < 250) return current;
            lastTick = now;
            lastPlayerId = player.ID;
            try
            {
                current = Describe(player, shownFg);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Doll", e);
                current = null;
            }
            return current;
        }

        struct Layer
        {
            public string Key;
            public Color Fg, Detail;
        }

        static string Describe(GameObject player, Color shownFg)
        {
            var layers = new List<Layer>();
            Material("linen", out Color linenFg, out Color linenDet);
            layers.Add(new Layer { Key = "body/base", Fg = linenFg, Detail = linenDet });
            ItemColors(player, out Color selfFg, out Color selfDet);

            // Gear: one layer per worn item; weapons go in the hands.
            Color bodyFg = linenFg, bodyDet = linenDet;
            string right = null, off = null, two = null, shield = null;
            Color rightFg = default, rightDet = default, offFg = default, offDet = default, twoFg = default, twoDet = default,
                shieldFg = default, shieldDet = default;
            var missiles = new List<GameObject>();
            var seen = new HashSet<GameObject>();
            XRL.World.Parts.Body body = player.Body;
            if (body != null)
                foreach (BodyPart part in body.LoopParts())
                {
                    GameObject o = part.Equipped;
                    if (o == null || !seen.Add(o)) continue; // two-slot items sit on several parts
                    if (part.Type == "Missile Weapon")
                    {
                        if (DollTable.Gear.ContainsKey(o.Blueprint)) missiles.Add(o);
                        continue;
                    }
                    if (!DollTable.Gear.TryGetValue(o.Blueprint, out string[] g)) continue;
                    Colors(o, g[1], out Color fg, out Color det);
                    string key = g[0];
                    if (part.Type == "Hand")
                    {
                        if (key.StartsWith("two/", StringComparison.Ordinal)) { two = key; twoFg = fg; twoDet = det; }
                        else if (key.StartsWith("left/", StringComparison.Ordinal)) { shield = key; shieldFg = fg; shieldDet = det; }
                        else if (part.Primary && right == null) { right = key; rightFg = fg; rightDet = det; }
                        else if (off == null) { off = key; offFg = fg; offDet = det; }
                        else if (right == null) { right = key; rightFg = fg; rightDet = det; }
                        continue;
                    }
                    // Garments only from garment slots (a dagger in the thrown-weapon slot is not in hand).
                    if (!(key.StartsWith("body/") || key.StartsWith("head/") || key.StartsWith("face/")
                        || key.StartsWith("back/") || key.StartsWith("hands/") || key.StartsWith("feet/"))) continue;
                    if (key.StartsWith("body/", StringComparison.Ordinal)) { bodyFg = fg; bodyDet = det; }
                    layers.Add(new Layer { Key = key, Fg = fg, Detail = det });
                }
            // Guns and bows live in their own slots: shown in a free hand (two pistols = one in each).
            foreach (GameObject o in missiles)
            {
                if (two != null) break;
                string[] g = DollTable.Gear[o.Blueprint];
                Colors(o, g[1], out Color fg, out Color det);
                if (g[0].StartsWith("two/", StringComparison.Ordinal))
                {
                    if (right == null && off == null && shield == null) { two = g[0]; twoFg = fg; twoDet = det; }
                }
                else if (right == null) { right = g[0]; rightFg = fg; rightDet = det; }
                else if (off == null && shield == null) { off = g[0]; offFg = fg; offDet = det; }
            }
            if (two != null) layers.Add(new Layer { Key = two, Fg = twoFg, Detail = twoDet });
            else
            {
                if (right != null) layers.Add(new Layer { Key = right, Fg = rightFg, Detail = rightDet });
                if (shield != null) layers.Add(new Layer { Key = shield, Fg = shieldFg, Detail = shieldDet });
                else if (off != null && off.StartsWith("right/", StringComparison.Ordinal))
                    layers.Add(new Layer { Key = "offhand/" + off.Substring(6), Fg = offFg, Detail = offDet });
            }

            // Mutations give the shape: chitin in this character's own colour pair, arms in the body garment's
            // colours, wings/fur in the character's own colours; horns, beak and claws are drawn as bone/gold.
            int pal = Stable(player.ID) % DollTable.Chitin.Length;
            Color shell = Hex(DollTable.Chitin[pal][0]), legs = Hex(DollTable.Chitin[pal][1]);
            foreach (var kv in DollTable.Mutations)
            {
                if (!player.HasPart(kv.Key)) continue;
                Layer l = new Layer { Key = kv.Value, Fg = selfFg, Detail = selfDet };
                if (DollTable.ChitinLayers.Contains(kv.Value)) { l.Fg = shell; l.Detail = legs; }
                else if (kv.Value == "mutfront/arms" || kv.Value == "mutfront/twoheads") { l.Fg = bodyFg; l.Detail = bodyDet; }
                layers.Add(l);
            }

            layers.Sort((a, b) => Rank(a.Key).CompareTo(Rank(b.Key)));
            var sb = new StringBuilder(Prefix);
            for (int i = 0; i < layers.Count; i++)
            {
                if (i > 0) sb.Append(';');
                sb.Append(layers[i].Key).Append(',').Append(Hex(layers[i].Fg)).Append(',').Append(Hex(layers[i].Detail));
            }
            // A coating (slime, blood, oil...) or frost overrides every colour.
            if (player.HasEffect<XRL.World.Effects.LiquidCovered>() || player.HasEffect<XRL.World.Effects.Frozen>())
                sb.Append("|c").Append(Hex(shownFg));
            return sb.ToString();
        }

        static int Rank(string key)
        {
            if (key == "body/base") return Array.IndexOf(DollTable.Order, "body/base");
            int slash = key.IndexOf('/');
            int r = Array.IndexOf(DollTable.Order, slash < 0 ? key : key.Substring(0, slash));
            return r < 0 ? 0 : r;
        }

        // FNV-1a: the same chitin pair for a character every session.
        static int Stable(string s)
        {
            uint h = 2166136261;
            foreach (char c in s ?? "") h = (h ^ c) * 16777619;
            return (int)(h & 0x7fffffff);
        }

        // An item's colours: its material when the table names one (the game paints chain mail and steel plain
        // white), else the item's own game colours.
        static void Colors(GameObject o, string material, out Color fg, out Color det)
        {
            ItemColors(o, out fg, out det, out char fgChar);
            if (material == "metal" && (fgChar == 'y' || fgChar == 'Y')) material = "steel";
            if (!material.IsNullOrEmpty() && Material(material, out Color mf, out Color md))
            {
                fg = mf;
                det = md;
            }
        }

        static void ItemColors(GameObject o, out Color fg, out Color det) => ItemColors(o, out fg, out det, out char _);

        static void ItemColors(GameObject o, out Color fg, out Color det, out char fgChar)
        {
            fgChar = 'y';
            char detChar = 'K';
            var r = o.Render;
            if (r != null)
            {
                string cs = !r.TileColor.IsNullOrEmpty() ? r.TileColor : r.ColorString;
                int amp = cs?.LastIndexOf('&') ?? -1;
                if (amp >= 0 && amp + 1 < cs.Length) fgChar = cs[amp + 1];
                if (!r.DetailColor.IsNullOrEmpty()) detChar = r.DetailColor[0];
            }
            fg = QudColor.ColorMap.TryGetValue(fgChar, out Color f) ? f : Color.gray;
            det = QudColor.ColorMap.TryGetValue(detChar, out Color d) ? d : Color.gray;
        }

        static bool Material(string name, out Color fg, out Color det)
        {
            fg = det = default;
            if (!DollTable.Materials.TryGetValue(name, out string[] m)) return false;
            fg = Hex(m[0]);
            det = Hex(m[1]);
            return true;
        }

        static Color Hex(string h)
        {
            UnityEngine.ColorUtility.TryParseHtmlString("#" + h, out Color c);
            return c;
        }

        static string Hex(Color c) => UnityEngine.ColorUtility.ToHtmlStringRGB(c).ToLowerInvariant();

        // ---------------------------------------------------------------- texture side (UI thread)

        // "layer,fg,detail;...|c<coat>" -> stacked pixels, outlined like any creature, coating applied.
        public static Color[] Compose(string description, Func<string, Color, Color, Color[]> recolored,
            Func<Color[], Color[]> outline)
        {
            string body = description.Substring(Prefix.Length);
            string coat = null;
            int bar = body.IndexOf("|c", StringComparison.Ordinal);
            if (bar >= 0)
            {
                coat = body.Substring(bar + 2);
                body = body.Substring(0, bar);
            }
            var px = new Color[16 * 24];
            foreach (string entry in body.Split(';'))
            {
                string[] f = entry.Split(',');
                if (f.Length != 3) continue;
                string key = f[0];
                bool mirror = key.StartsWith("offhand/", StringComparison.Ordinal);
                if (mirror) key = "right/" + key.Substring(8);
                Color[] lp = recolored(LayerPrefix + key, Hex(f[1]), Hex(f[2]));
                if (lp == null || lp.Length != px.Length) continue;
                for (int y = 0; y < 24; y++)
                    for (int x = 0; x < 16; x++)
                    {
                        Color c = lp[y * 16 + (mirror ? 15 - x : x)];
                        if (c.a <= 0f) continue;
                        int i = y * 16 + x;
                        px[i] = c.a >= 1f ? c : Color.Lerp(px[i], new Color(c.r, c.g, c.b, 1f), c.a);
                    }
            }
            px = outline(px);
            // Translucent ground shadow under the feet (screen row 23 = Unity row 0), like every creature.
            for (int x = 3; x <= 12; x++)
                if (px[x].a <= 0f) px[x] = new Color(0.06f, 0.08f, 0.12f, 120f / 255f);
            if (coat != null) Coat(px, Hex(coat));
            return px;
        }

        static void Coat(Color[] px, Color coat)
        {
            for (int i = 0; i < px.Length; i++)
            {
                Color c = px[i];
                if (c.a < 0.99f || c.r + c.g + c.b < 0.24f) continue; // keep the ink outline
                float lum = 0.3f * c.r + 0.59f * c.g + 0.11f * c.b;
                float k = 0.45f + lum * 0.9f;
                Color t = new Color(coat.r * k, coat.g * k, coat.b * k, 1f);
                px[i] = Color.Lerp(c, t, 0.75f);
            }
        }
    }
}
