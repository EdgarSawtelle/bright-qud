// Bright Qud runtime recolor.
//
// The mod's tiles are truecolor (modconfig.json shadermode 1), which normally ignores the colors the
// game gives each object. Many objects share one tile with different colors, and the world seed
// generates creatures/villages with random colors, so this script restores that:
//
//   1. ConsoleChar.Set (the single point where each map cell receives its tile + final colors) is
//      patched. If the tile is one of ours (it has a role mask), the cell's tile is swapped for a
//      virtual path "brightqud:<key>|<fg>|<detail>".
//   2. SpriteManager.TryGetTextureInfo resolves those virtual paths: it builds (once, cached) a copy
//      of our tile whose recolorable pixels take the game's foreground/detail colors.
//   3. Cells the player remembers but can't see (RenderEvent.Visible false or Lit <= 1, the same test
//      Cell.Render uses) get a dim, desaturated version, so "visible vs remembered" still reads.
//   4. Ground: instead of the default near-black cell background, every explored cell gets a ground
//      color (outdoor: from the color the game painted on the cell; enclosed rooms: warm floor;
//      underground/inside zones: stone). See Ground below. Swimmers get the water drawn under them.
//   5. Auto-style: vanilla tiles we haven't drawn get brighter colors plus the walkability tiers
//      (outline/drop shadow for creatures and items), so the whole world matches.
//   6. Mutations: horns, extra arms, wings, ... are composited onto humanoid-kit tiles of creatures
//      that have them; Photosynthetic Skin / Albino tint the skin.
//   7. Idle animation: creatures alternate two frames on a shared beat (a 1px bob, or a hand-drawn
//      second frame "brightqudframe/<key>" such as wings up); the Wings mutation flaps.
//   8. Map HUD (toggleable): red/green rings under hostile/allied creatures, health bars when hurt.
//
// Color math mirrors art/src/colors.py (QUD, BRIGHT, Ramp). Keep them in sync.

using System;
using System.Collections.Generic;
using ConsoleLib.Console;
using HarmonyLib;
using QudColor = ConsoleLib.Console.ColorUtility;
using Kobold;
using UnityEngine;
using XRL;
using XRL.World;

namespace BrightQud
{
    public static class Recolor
    {
        public const string Prefix = "brightqud:";
        const string MaskDir = "BrightQudMask/";
        const int MaxCache = 8192;

        // Game palette -> Bright Qud palette (colors.py QUD/BRIGHT).
        static readonly string[,] Bright =
        {
            { "a64a2e", "c8503a" }, { "d74200", "f05a28" }, { "f15f22", "ff7030" }, { "e99f10", "ffb020" },
            { "98875f", "b08a5a" }, { "cfc041", "ffd23a" }, { "009403", "3fae3a" }, { "00c420", "6fe04a" },
            { "0048bd", "2a62d6" }, { "0096ff", "3fb4ff" }, { "40a4b9", "4fc8d8" }, { "77bfcf", "8fe4f0" },
            { "b154cf", "c04ad8" }, { "da5bd6", "ff7ae8" }, { "0f3b3a", "1a4a48" }, { "155352", "2e6a68" },
            { "b1c9c3", "d0dcd8" }, { "ffffff", "f8f8f0" },
        };

        class TileInfo
        {
            public exTextureInfo Base;
            public Color[] BasePixels;
            public Color[] MaskPixels;
        }

        struct Request
        {
            public string Key;
            public Color Fg, Detail;
            public bool Memory;
            public bool ClearMemory;
            public string UnderKey; // optional terrain drawn underneath (e.g. water under a swimmer)
            public Color Under;
            public int Style;       // auto-style for vanilla tiles (Style* constants)
            public int Mutations;   // bit i = MutationOrder[i] is present (humanoid-kit tiles only)
            public int Frame;       // idle animation frame (0/1) for creatures
            public int Hud;         // map HUD: bits 0-1 ring (1 hostile, 2 ally), bits 2-4 health bucket,
                                    // bit 5 item sparkle
        }

        // Visible mutations: overlay parts first, then skin tints (see Generated.cs).
        public static readonly string[] MutationOrder = BuildMutationOrder();

        static string[] BuildMutationOrder()
        {
            var list = new List<string>(Generated.Mutations.Keys);
            list.AddRange(Generated.SkinTints.Keys);
            return list.ToArray();
        }

        // Auto-style for tiles we haven't drawn: brighter colors plus the walkability tiers.
        public const int StyleNone = 0;   // leave vanilla tiles alone (UI, unknown context)
        public const int StyleObject = 1; // creatures, items, furniture: ink outline + drop shadow
        public const int StyleTall = 2;   // walk-through but blocks sight (trees...): outline only
        public const int StyleFlat = 3;   // floors, walls, liquids: colors only
        public const int StyleProjectile = 9; // our tile in flight: no ground/drop shadow (it spins)

        static readonly object Lock = new object();
        static readonly Dictionary<string, TileInfo> Tiles = new Dictionary<string, TileInfo>();
        static readonly HashSet<string> NotOurs = new HashSet<string>();
        static readonly Dictionary<string, Request> Requests = new Dictionary<string, Request>();
        // (tile, fg, detail, remembered) -> virtual path or null. Avoids allocating strings for every cell redraw.
        static readonly Dictionary<(string, uint, uint, bool, bool, string, uint, int, int, int, int), string> Resolved =
            new Dictionary<(string, uint, uint, bool, bool, string, uint, int, int, int, int), string>();
        static readonly Dictionary<string, exTextureInfo> Built = new Dictionary<string, exTextureInfo>();
        static int destroyedCount;

        // Same normalisation as SpriteManager.GetKey (which uses a shared, non thread-safe buffer).
        public static string Key(string path)
        {
            var chars = new char[path.Length];
            int n = 0;
            foreach (char c in path)
            {
                if (c == '.') break;
                chars[n++] = c == '\\' || c == '_' ? '/' : char.ToLowerInvariant(c);
            }
            var key = new string(chars, 0, n);
            const string prefix = "assets/content/textures/";
            return WallAlias(key.StartsWith(prefix, StringComparison.Ordinal) ? key.Substring(prefix.Length) : key);
        }

        // Painted wall families we draw with one material: the game's 8-direction mask
        // (N NE E SE S SW W NW) becomes our 4-direction variant, e.g. tiles/wall/wood-10101010 ->
        // brightqudwall/wood-1111.
        static string WallAlias(string key)
        {
            int dash = key.LastIndexOf('-');
            if (dash < 0 || key.Length - dash != 9) return key;
            if (!Generated.WallAliases.TryGetValue(key.Substring(0, dash + 1), out string material)) return key;
            string m = key.Substring(dash + 1);
            for (int i = 0; i < 8; i++)
                if (m[i] != '0' && m[i] != '1') return key;
            return "brightqudwall/" + material + "-" + m[0] + m[2] + m[4] + m[6];
        }

        static string Hex(Color c)
        {
            Color32 c32 = c;
            return c32.r.ToString("x2") + c32.g.ToString("x2") + c32.b.ToString("x2");
        }

        static bool? active;

        // Virtual tiles only resolve if our TryGetTextureInfo prefix is really installed. If any
        // patch failed to apply, stay out of the way (plain mod PNGs) instead of drawing blanks.
        static bool Active
        {
            get
            {
                if (active.HasValue) return active.Value;
                bool ok = false;
                try
                {
                    var info = Harmony.GetPatchInfo(AccessTools.Method(typeof(SpriteManager), nameof(SpriteManager.TryGetTextureInfo)));
                    if (info != null)
                        foreach (var patch in info.Prefixes)
                            if (patch.PatchMethod.DeclaringType == typeof(TryGetTextureInfoPatch)) ok = true;
                }
                catch (Exception e)
                {
                    MetricsManager.LogException("BrightQud.Active", e);
                }
                if (!ok) MetricsManager.LogWarning("BrightQud: texture patch not installed, runtime recolor disabled.");
                else UnityEngine.Debug.Log("BrightQud: runtime recolor active");
                active = ok;
                return ok;
            }
        }

        static uint Pack(Color c)
        {
            Color32 c32 = c;
            return (uint)(c32.r << 16 | c32.g << 8 | c32.b);
        }

        // Called from ConsoleChar.Set (game thread) for every map cell on every redraw: keep it cheap.
        // memory = the cell is remembered but not currently seen (or too dark): drawn dim.
        // under/underColor: terrain tile to draw beneath this one (null for none).
        // style: auto-style tier for vanilla tiles (StyleNone keeps them vanilla).
        public static string Resolve(string tile, Color fg, Color detail, bool memory, string under = null,
            Color underColor = default, int style = StyleNone, int mutations = 0, int frame = 0, int hud = 0)
        {
            if (tile == null || tile.StartsWith(Prefix, StringComparison.Ordinal) || !Active) return null;
            bool clearMemory = memory && Settings.ClearMemory;
            var cacheKey = (tile, Pack(fg), Pack(detail), memory, clearMemory, under, Pack(underColor), style, mutations,
                frame, hud);
            lock (Lock)
            {
                if (Resolved.TryGetValue(cacheKey, out string cached)) return cached;
            }
            string virt = Compute(tile, fg, detail, memory, clearMemory, under, underColor, style, mutations, frame, hud);
            lock (Lock)
            {
                if (Resolved.Count > 20000) Resolved.Clear();
                Resolved[cacheKey] = virt;
            }
            return virt;
        }

        public static bool Exists(string key) => IsOurs(key);

        static bool IsOurs(string key)
        {
            lock (Lock)
            {
                if (NotOurs.Contains(key)) return false;
                if (Tiles.ContainsKey(key)) return true;
                // Our tiles ship a mask; anything else is left to the game.
                if (!SpriteManager.TryGetTextureInfo(MaskDir + key, out exTextureInfo _))
                {
                    NotOurs.Add(key);
                    return false;
                }
                Tiles[key] = null; // pixels are read later, on the UI thread
                return true;
            }
        }

        static string Compute(string tile, Color fg, Color detail, bool memory, bool clearMemory, string under,
            Color underColor, int style,
            int mutations, int frame, int hud)
        {
            string key = Key(tile);
            string underKey = under != null ? Key(under) : null;
            if (underKey != null && !IsOurs(underKey)) underKey = null;
            bool ours = IsOurs(key);
            if (style == StyleProjectile && !ours) return null; // vanilla projectiles are fine as they are
            if (ours && style != StyleProjectile) style = StyleNone; // hand-drawn tiles carry their own style
            if (!ours || !Generated.HumanoidKeys.Contains(key)) mutations = 0;
            // Vanilla tiles are taken over to auto-style them or to compose them onto our terrain.
            if (!ours && underKey == null && style == StyleNone) return null;
            string virt = Prefix + key + "|" + Hex(fg) + "|" + Hex(detail) + (memory ? clearMemory ? "|mc" : "|m" : "")
                + (underKey != null ? "|u:" + underKey + "|" + Hex(underColor) : "")
                + (style != StyleNone ? "|s" + style : "")
                + (mutations != 0 ? "|mu" + mutations : "")
                + (frame != 0 ? "|f" + frame : "")
                + (hud != 0 ? "|h" + hud : "");
            lock (Lock)
            {
                Requests[virt] = new Request
                {
                    Key = key, Fg = fg, Detail = detail, Memory = memory, ClearMemory = clearMemory, UnderKey = underKey, Under = underColor,
                    Style = style, Mutations = mutations, Frame = frame, Hud = hud
                };
            }
            return virt;
        }

        // Menus/panels (UIThreeColorProperties) draw tiles with a 3-color UI material, which garbles
        // truecolor art. For our tiles they get a recolored sprite instead (UI thread only).
        public static Sprite UISprite(string tile, Color fg, Color detail)
        {
            string virt = Resolve(tile, fg, detail, false);
            if (virt == null || !GameManager.IsOnUIContext() || !TryGet(virt, out exTextureInfo info)) return null;
            return SpriteManager.GetUnitySprite(info);
        }

        // Called from SpriteManager.TryGetTextureInfo. Texture work only happens on the UI thread.
        public static bool TryGet(string path, out exTextureInfo info)
        {
            lock (Lock)
            {
                if (Built.TryGetValue(path, out info))
                {
                    // Unity may destroy runtime textures (e.g. Resources.UnloadUnusedAssets during the
                    // game's memory cleanup); a destroyed one compares equal to null. Rebuild it.
                    if (info != null && info.texture != null) return true;
                    Built.Remove(path);
                    if (++destroyedCount <= 5)
                        UnityEngine.Debug.Log("BrightQud: rebuilt destroyed texture " + path);
                }
                if (!Requests.TryGetValue(path, out Request req)) { info = null; return false; }
                if (!GameManager.IsOnUIContext())
                {
                    // Not allowed to create textures here: fall back to the uncolored tile for now.
                    info = SpriteManager.GetTextureInfo(req.Key);
                    return true;
                }
                if (Built.Count > MaxCache) Built.Clear();
                try
                {
                    info = Build(req);
                }
                catch (Exception e)
                {
                    // Never leave a blank cell: fall back to the plain tile (ours or vanilla).
                    MetricsManager.LogException("BrightQud.Build " + req.Key, e);
                    info = SpriteManager.GetTextureInfo(req.Key);
                }
                Built[path] = info;
                return true;
            }
        }

        static TileInfo Load(string key)
        {
            if (Tiles.TryGetValue(key, out TileInfo t) && t != null) return t;
            exTextureInfo baseInfo = SpriteManager.GetTextureInfo(key);
            exTextureInfo maskInfo = SpriteManager.GetTextureInfo(MaskDir + key);
            t = new TileInfo
            {
                Base = baseInfo,
                BasePixels = baseInfo.texture.GetPixels(baseInfo.x, baseInfo.y, baseInfo.width, baseInfo.height),
                MaskPixels = maskInfo.texture.GetPixels(maskInfo.x, maskInfo.y, maskInfo.width, maskInfo.height),
            };
            Tiles[key] = t;
            return t;
        }

        // Our tile recolored with the game's colors (Ramp over the role mask).
        static Color[] Recolored(string key, Color gameFg, Color gameDetail)
        {
            TileInfo t = Load(key);
            var px = new Color[t.BasePixels.Length];
            Color fg = Brighten(gameFg), detail = Brighten(gameDetail);
            for (int i = 0; i < px.Length; i++)
            {
                Color c = t.BasePixels[i];
                Color m = t.MaskPixels[i];
                if (m.a > 0.5f)
                {
                    int shade = Mathf.RoundToInt(m.g * 255f / 127f);
                    c = Ramp(m.r * 255f < 150f ? fg : detail, shade, c.a);
                }
                px[i] = c;
            }
            return px;
        }

        // A vanilla 3-color tile converted to truecolor pixels with the dual-color shader's math:
        // rgb = mix(fg, detail, tex.r), alpha = tex.a.
        static Color[] Vanilla(string key, Color fg, Color detail)
        {
            exTextureInfo info = SpriteManager.GetTextureInfo(key);
            if (info.width != 16 || info.height != 24) throw new InvalidOperationException("not a 16x24 tile");
            Color[] src = info.texture.GetPixels(info.x, info.y, info.width, info.height);
            // Another mod's truecolor tile: its pixels are final colors, keep them (auto-style then
            // only adds outlines/shadows).
            if (info.ShaderMode == 1) return src;
            var px = new Color[src.Length];
            for (int i = 0; i < src.Length; i++)
            {
                Color c = Color.Lerp(fg, detail, src[i].r);
                c.a = src[i].a;
                px[i] = c;
            }
            return px;
        }

        static Color Over(Color top, Color under)
        {
            float a = top.a + under.a * (1f - top.a);
            if (a <= 0f) return Color.clear;
            Color c = (top * top.a + under * under.a * (1f - top.a)) / a;
            c.a = a;
            return c;
        }

        static readonly Color Ink = new Color(0x10 / 255f, 0x14 / 255f, 0x1f / 255f, 1f);

        // Style C pipeline (tools/build_tiles.py) applied at runtime to a vanilla tile:
        // 8-neighbour ink outline, plus a soft drop shadow for objects.
        static Color[] Stylize(Color[] px, int w, int h, int style)
        {
            if (style != StyleObject && style != StyleTall) return px;
            var outp = (Color[])px.Clone();
            bool Solid(int x, int y) => x >= 0 && y >= 0 && x < w && y < h && px[y * w + x].a > 0.5f;
            if (style == StyleObject)
                for (int y = 0; y < h; y++)
                    for (int x = 0; x < w; x++)
                    {
                        if (Solid(x, y)) continue;
                        // Unity pixel rows go bottom-up: "down-right" on screen is (x-1, y+1) as the source.
                        if (Solid(x - 1, y + 1) || Solid(x - 2, y + 2))
                            outp[y * w + x] = new Color(Ink.r, Ink.g, Ink.b, 110f / 255f);
                    }
            for (int y = 0; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    if (Solid(x, y)) continue;
                    int src = -1;
                    for (int dx = -1; dx <= 1 && src < 0; dx++)
                        for (int dy = -1; dy <= 1 && src < 0; dy++)
                            if ((dx != 0 || dy != 0) && Solid(x + dx, y + dy)) src = (y + dy) * w + x + dx;
                    if (src < 0) continue;
                    // Walk-through plants: soft outline in their own darker shade; ink is for things
                    // you interact with (same rule as tools/build_tiles.py).
                    Color o = style == StyleTall ? px[src] * 0.45f : Ink;
                    o.a = 1f;
                    outp[y * w + x] = o;
                }
            return outp;
        }

        static Color HexColor(string h)
        {
            UnityEngine.ColorUtility.TryParseHtmlString("#" + h, out Color c);
            return c;
        }

        static bool SameRgb(Color a, Color b) =>
            Mathf.Abs(a.r - b.r) < 0.01f && Mathf.Abs(a.g - b.g) < 0.01f && Mathf.Abs(a.b - b.b) < 0.01f;

        // Visible mutations on humanoid-kit tiles: skin tints, then overlays behind/in front of the body.
        static Color[] WithMutations(Color[] px, Request req)
        {
            for (int b = 0; b < MutationOrder.Length; b++)
            {
                if ((req.Mutations & (1 << b)) == 0) continue;
                string name = MutationOrder[b];
                if (!Generated.SkinTints.TryGetValue(name, out string[] tint)) continue;
                Color s0 = HexColor(Generated.Skin[0]), s1 = HexColor(Generated.Skin[1]);
                Color t0 = HexColor(tint[0]), t1 = HexColor(tint[1]);
                for (int i = 0; i < px.Length; i++)
                {
                    if (px[i].a <= 0f) continue;
                    if (SameRgb(px[i], s0)) px[i] = new Color(t0.r, t0.g, t0.b, px[i].a);
                    else if (SameRgb(px[i], s1)) px[i] = new Color(t1.r, t1.g, t1.b, px[i].a);
                }
            }
            for (int pass = 0; pass < 2; pass++) // 0 = behind the body, 1 = in front
                for (int b = 0; b < MutationOrder.Length; b++)
                {
                    if ((req.Mutations & (1 << b)) == 0) continue;
                    string name = MutationOrder[b];
                    if (!Generated.Mutations.TryGetValue(name, out bool behind) || behind != (pass == 0)) continue;
                    string overlayKey = "brightqudmut/" + name.ToLowerInvariant();
                    if (!IsOurs(overlayKey)) continue;
                    Color[] ov = Recolored(overlayKey, req.Fg, req.Detail);
                    if (name == "Wings" && req.Frame == 1 && ov.Length == 16 * 24) ov = ShiftUp(ov, 16, 24, 2); // flap
                    if (ov.Length != px.Length) continue;
                    for (int i = 0; i < px.Length; i++) px[i] = behind ? Over(px[i], ov[i]) : Over(ov[i], px[i]);
                }
            return px;
        }

        // Idle "bob" for frame 1: everything solid moves down one pixel; translucent ground shadows stay.
        // (Unity pixel rows go bottom-up, so screen-down is index - width.)
        static Color[] Bob(Color[] px, int w, int h)
        {
            var outp = new Color[px.Length];
            for (int i = 0; i < px.Length; i++) if (px[i].a < 0.6f) outp[i] = px[i];
            for (int y = 1; y < h; y++)
                for (int x = 0; x < w; x++)
                {
                    Color c = px[y * w + x];
                    if (c.a >= 0.6f) outp[(y - 1) * w + x] = c;
                }
            return outp;
        }

        static readonly Color Hostile = new Color(1f, 0.25f, 0.22f, 1f);
        static readonly Color Ally = new Color(0.3f, 1f, 0.42f, 1f);

        // Map HUD drawn into creature tiles (screen rows: 0 = top). Unity rows are bottom-up.
        // hud bits: 1 hostile ring, 2 ally ring, 4-28 health bucket, 32 item sparkle, 64 player ring,
        // 128 low-health pulse (player ring turns red), 256 talk bubble, 512 interact marker,
        // 1024 faded talk bubble (already talked to), 2048 flames (burning), 4096 flame flicker frame.
        static void DrawHud(Color[] px, int hud)
        {
            int ring = hud & 3, health = (hud >> 2) & 7;
            if ((hud & 2048) != 0) Flames(px, (hud & 4096) != 0);
            if ((hud & 256) != 0)
            {
                // Small white speech bubble at the top-left: "you can talk to me".
                Color w = new Color(1f, 1f, 1f, 1f), o = new Color(0.05f, 0.05f, 0.08f, 1f);
                string[] bubble = { ".ooooo.", "owwwwwo", "owowowo", "owwwwwo", ".owoooo", ".oo...." };
                Stamp(px, bubble, 0, 0, w, o);
            }
            else if ((hud & 1024) != 0)
            {
                // Already talked: same bubble, grey and see-through.
                Color w = new Color(0.75f, 0.78f, 0.8f, 0.45f), o = new Color(0.05f, 0.05f, 0.08f, 0.35f);
                string[] bubble = { ".ooooo.", "owwwwwo", "owowowo", "owwwwwo", ".owoooo", ".oo...." };
                Stamp(px, bubble, 0, 0, w, o);
            }
            if ((hud & 512) != 0)
            {
                // Gold corner marker at the top-right: something to open or use.
                Color g = new Color(1f, 0.82f, 0.25f, 1f), o = new Color(0.05f, 0.05f, 0.08f, 1f);
                string[] corner = { "oooooo", ".wwwwo", "..wwwo", "...wwo", "....wo", ".....o" };
                Stamp(px, corner, 10, 0, g, o);
            }
            if ((hud & 64) != 0 && ring == 0)
            {
                // The player: a warm white ring (red and pulsing when health is low).
                Color c = (hud & 128) != 0 ? Hostile : new Color(1f, 0.93f, 0.6f, 1f);
                FeetRing(px, c, (hud & 128) != 0 ? 0.5f : 0.62f);
            }
            if ((hud & 32) != 0)
            {
                // Small 4-point glint near the top-right of an item lying on the ground.
                Color g = new Color(1f, 1f, 0.85f, 1f);
                foreach (var (x, row) in new[] { (12, 8), (11, 9), (12, 9), (13, 9), (12, 10) })
                    px[(23 - row) * 16 + x] = g;
            }
            if (ring != 0) FeetRing(px, ring == 1 ? Hostile : Ally, 0.62f);
            if (health != 0)
            {
                // 10px bar on the top row: dark track, filled part green > yellow > red.
                int filled = health * 2;
                Color fill = health >= 4 ? Ally : health >= 2 ? new Color(1f, 0.85f, 0.2f, 1f) : Hostile;
                for (int x = 3; x < 13; x++)
                {
                    int i = 23 * 16 + x;
                    px[i] = x - 3 < filled ? fill : new Color(0.06f, 0.08f, 0.12f, 1f);
                }
            }
        }

        // Flame tongues on both sides and above, only where the object itself doesn't cover them.
        static readonly string[] Flame = { "...y..", "..yy..", ".yoy..", ".yooy.", "yooory", "yoorr.", "oorrr.", ".rrr.." };
        static void Flames(Color[] px, bool alt)
        {
            FlameAt(px, 0, alt ? 8 : 11);
            FlameAt(px, 10, alt ? 11 : 7);
            FlameAt(px, 5, alt ? 1 : 0);
        }

        static void FlameAt(Color[] px, int x0, int row0)
        {
            Color y = new Color(1f, 0.92f, 0.35f, 1f), o = new Color(1f, 0.55f, 0.12f, 1f),
                r = new Color(0.85f, 0.18f, 0.1f, 1f);
            for (int rr = 0; rr < Flame.Length; rr++)
                for (int x = 0; x < Flame[rr].Length; x++)
                {
                    char ch = Flame[rr][x];
                    int tx = x0 + x, ty = row0 + rr;
                    if (ch == '.' || tx < 0 || tx >= 16 || ty < 0 || ty >= 24) continue;
                    int i = (23 - ty) * 16 + tx;
                    if (px[i].a < 0.6f) px[i] = ch == 'y' ? y : ch == 'o' ? o : r;
                }
        }

        // Ellipse at the feet, only where the creature itself doesn't cover it. inner < 0.62 = thicker.
        static void FeetRing(Color[] px, Color c, float inner)
        {
            for (int row = 19; row <= 23; row++)
                for (int x = 0; x < 16; x++)
                {
                    float dx = (x - 7.5f) / 7f, dy = (row - 21.2f) / 1.9f;
                    float d = dx * dx + dy * dy;
                    if (d < inner || d > 1.05f) continue;
                    int i = (23 - row) * 16 + x;
                    if (px[i].a < 0.6f) px[i] = new Color(c.r, c.g, c.b, 0.95f);
                }
        }

        // Draws a small pattern ('w' = color, 'o' = outline) with its top-left at (x0, row0 from the top).
        static void Stamp(Color[] px, string[] rows, int x0, int row0, Color w, Color o)
        {
            for (int r = 0; r < rows.Length; r++)
                for (int x = 0; x < rows[r].Length; x++)
                {
                    char ch = rows[r][x];
                    int tx = x0 + x, ty = row0 + r;
                    if (ch == '.' || tx < 0 || tx >= 16 || ty < 0 || ty >= 24) continue;
                    px[(23 - ty) * 16 + tx] = ch == 'w' ? w : o;
                }
        }

        // Water stays bright; other liquids (blood, salt, slime, oil...) can cover big areas, so they're
        // drawn a little darker and less saturated to keep creatures and items readable on top.
        static void ToneLiquid(Color[] px)
        {
            for (int i = 0; i < px.Length; i++)
            {
                Color c = px[i];
                if (c.a <= 0f) continue;
                Color.RGBToHSV(c, out float h, out float sat, out float v);
                if (h > 0.45f && h < 0.72f) continue; // blues and cyans: water
                Color o = Color.HSVToRGB(h, sat * 0.75f, v * 0.72f);
                px[i] = new Color(o.r, o.g, o.b, c.a);
            }
        }

        static Color[] ShiftUp(Color[] px, int w, int h, int n)
        {
            var outp = new Color[px.Length];
            for (int y = 0; y + n < h; y++)
                for (int x = 0; x < w; x++) outp[(y + n) * w + x] = px[y * w + x];
            return outp;
        }

        static readonly Color NightTint = new Color(0.08f, 0.1f, 0.18f, 1f);

        static exTextureInfo Build(Request req)
        {
            // Frame 1: brightqudframe/<key>; ambient tiles also have frames 2-3 (brightqudframe2/, 3/).
            string frameKey = (req.Frame <= 1 ? "brightqudframe/" : "brightqudframe" + req.Frame + "/") + req.Key;
            bool altFrame = req.Frame >= 1 && IsOurs(frameKey);
            Color[] px = altFrame ? Recolored(frameKey, req.Fg, req.Detail)
                : IsOurs(req.Key) ? Recolored(req.Key, req.Fg, req.Detail)
                : req.Style != StyleNone ? Stylize(Vanilla(req.Key, Brighten(req.Fg), Brighten(req.Detail)), 16, 24, req.Style)
                : Vanilla(req.Key, req.Fg, req.Detail);
            if (req.Key.StartsWith("liquids/", StringComparison.Ordinal)) ToneLiquid(px);
            if (req.Style == StyleProjectile)
                for (int i = 0; i < px.Length; i++)
                    if (px[i].a < 0.6f) px[i] = Color.clear; // drop the baked ground/drop shadow
            if (req.Mutations != 0) px = WithMutations(px, req);
            if (req.Frame == 1 && !altFrame && px.Length == 16 * 24) px = Bob(px, 16, 24);
            if (req.Hud != 0 && px.Length == 16 * 24) DrawHud(px, req.Hud);
            if (req.UnderKey != null)
            {
                Color[] under = Recolored(req.UnderKey, req.Under, req.Under);
                if (req.UnderKey.StartsWith("liquids/", StringComparison.Ordinal)) ToneLiquid(under);
                if (under.Length == px.Length)
                    for (int i = 0; i < px.Length; i++) px[i] = Over(px[i], under[i]);
            }
            if (req.Memory)
            {
                Color memoryTint = QudColor.ColorMap['K'];
                bool clear = req.ClearMemory;
                for (int i = 0; i < px.Length; i++)
                {
                    Color c = px[i];
                    if (c.a <= 0f) continue;
                    if (clear)
                    {
                        // Dim but still in colour (out of sight, or too dark to see): 65% of the
                        // saturation, 70% of the brightness, a light night-blue tint.
                        Color.RGBToHSV(c, out float h, out float s, out float v);
                        Color m = Color.Lerp(Color.HSVToRGB(h, s * 0.65f, v * 0.7f), NightTint, 0.15f);
                        px[i] = new Color(m.r, m.g, m.b, c.a);
                        continue;
                    }
                    float lum = 0.3f * c.r + 0.59f * c.g + 0.11f * c.b;
                    float f = 0.45f + lum * 0.9f;
                    px[i] = new Color(memoryTint.r * f, memoryTint.g * f, memoryTint.b * f, c.a);
                }
            }
            var tex = new Texture2D(16, 24, TextureFormat.ARGB32, false)
            {
                filterMode = UnityEngine.FilterMode.Point
            };
            if (px.Length != 16 * 24) tex.Reinitialize(px.Length / 24, 24);
            tex.SetPixels(px);
            tex.Apply();
            // Keep runtime textures alive through Resources.UnloadUnusedAssets.
            tex.hideFlags = HideFlags.DontUnloadUnusedAsset;
            var info = ScriptableObject.CreateInstance<exTextureInfo>();
            info.hideFlags = HideFlags.DontUnloadUnusedAsset;
            info.texture = tex;
            info.width = tex.width;
            info.height = tex.height;
            info.x = 0;
            info.y = 0;
            info.ShaderMode = 1;
            return info;
        }

        static Color Brighten(Color c)
        {
            string hex = Hex(c);
            for (int i = 0; i < Bright.GetLength(0); i++)
            {
                if (Close(hex, Bright[i, 0]))
                {
                    UnityEngine.ColorUtility.TryParseHtmlString("#" + Bright[i, 1], out Color b);
                    return b;
                }
            }
            return c;
        }

        static bool Close(string a, string b)
        {
            for (int i = 0; i < 6; i += 2)
                if (Math.Abs(Convert.ToInt32(a.Substring(i, 2), 16) - Convert.ToInt32(b.Substring(i, 2), 16)) > 3)
                    return false;
            return true;
        }

        // shade 0 = light, 1 = mid, 2 = dark (colors.py ramp).
        static Color Ramp(Color c, int shade, float alpha)
        {
            Color.RGBToHSV(c, out float h, out float s, out float v);
            if (shade == 0) { s *= 0.85f; v = Mathf.Min(1f, v * 1.2f + 0.06f); }
            else if (shade == 2) { s = Mathf.Min(1f, s * 1.1f); v *= 0.62f; }
            Color o = Color.HSVToRGB(h, s, v);
            o.a = alpha;
            return o;
        }
    }

    [HarmonyPatch(typeof(ConsoleChar), nameof(ConsoleChar.Set), new Type[] { typeof(RenderEvent) })]
    public static class ConsoleCharSetPatch
    {
        static void Postfix(ConsoleChar __instance, RenderEvent Event)
        {
            try
            {
                // Cell.Render: a cell is drawn as remembered when not visible or lit at level <= 1.
                bool memory = !Event.Visible || (int)Event.Lit <= 1;
                Ground.Apply(__instance, Event, memory, out string under, out Color underColor, out int style,
                    out int mutations, out int frame, out bool isPlayer, out int hud);
                string tile = isPlayer ? Settings.PlayerTile(__instance._Tile) : __instance._Tile;
                string virt = Recolor.Resolve(tile, __instance.Foreground, __instance.Detail, memory, under,
                    underColor, style, mutations, frame, hud);
                if (virt != null) __instance._Tile = virt;
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Resolve", e);
            }
        }
    }

    // "Bright Qud: legend" button in Options → Mods (Options.xml OnClick="BrightQud.Legend.Show").
    public static class Legend
    {
        static readonly string[,] Rows =
        {
            { "player", "{{Y|Warm ring}}: you. It turns {{R|red and pulses}} at 25% health or less." },
            { "lowhealth", "{{R|Red pulsing ring}} under you: low health, be careful." },
            { "enemy", "{{R|Red ring}}: hostile to you." },
            { "ally", "{{G|Green ring}}: your companion or follower." },
            { "hurt", "Bar on top: health of a hurt creature ({{G|green}} > {{W|yellow}} > {{R|red}})." },
            { "sparkle", "{{Y|Twinkle}}: an item lying on the ground you can pick up." },
            { "talk", "{{Y|White speech bubble}}: merchant, named character or quest giver you haven't talked to yet (or with a quest still open)." },
            { "talked", "{{K|Faded bubble}}: already talked, nothing new (you can still trade or chat)." },
            { "interact", "{{W|Gold corner}}: stairs, or a chest/container that still holds items." },
            { "solid", "Thick black outline + shadow: creatures, items, furniture (you bump into them)." },
            { "plant", "Soft outline, no shadow: plants you can walk through." },
            { "wall", "Dark base line: a wall. It blocks you." },
            { "ground", "Brown ground: outdoors. Warm wood: inside a building. Grey: underground." },
            { "memory", "Faded colors: remembered area, not in sight right now." },
            { "danger", "World map: {{W|orange}} tint = region tougher than your level, {{R|red}} = much tougher. Look at a region to see its level." },
            { "fire", "Flames around something: it's burning." },
        };

        public static async System.Threading.Tasks.Task<bool> Show()
        {
            try
            {
                var lines = new List<string>();
                var icons = new List<IRenderable>();
                for (int i = 0; i < Rows.GetLength(0); i++)
                {
                    lines.Add(Rows[i, 1]);
                    icons.Add(new Renderable("brightqudlegend/" + Rows[i, 0], " ", "&y", "&y", 'y'));
                }
                await XRL.UI.Popup.PickOptionAsync("Bright Qud legend",
                    "What the map markers mean (each one can be turned off below).", "", lines, null, icons,
                    MaxWidth: 78, AllowEscape: true);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Legend", e);
            }
            return false;
        }
    }

    // Controls reminder: LT + View on the Deck (mod Commands.xml), or Options → Mods. Shows the player's
    // own current buttons; picking a line runs that command (game thread only).
    public static class Controls
    {
        public const string Command = "CmdBrightQudControls";
        public const string MarkersCommand = "CmdBrightQudMarkers";

        // { command ids ("+" joins two), text }. Empty id = a heading or a tip.
        static readonly string[,] Rows =
        {
            { "", "{{W|BRIGHT QUD}}" },
            { "CmdBrightQudMarkers", "Item sparkle (+) and gold corners on stairs/containers: on / off" },
            { "", "{{W|EXPLORING}}" },
            { "CmdBrightQudQuests", "Quests: your quests nearest first; pick one to follow (banner on screen)" },
            { "CmdAutoExplore", "Autoexplore: walk to unexplored places, stops when something shows up" },
            { "CmdMoveToPointOfInterest", "Go to a point of interest: stairs, buildings, people you've found here" },
            { "CmdMoveToEdge", "Walk to the edge of the zone (to leave it)" },
            { "CmdMoveU+CmdMoveD", "Up / down: stairs; on the surface, up opens the world map" },
            { "LookDirection", "Look around: what is that? (move the cursor, Accept for details)" },
            { "Highlight", "Show labels over everything on screen" },
            { "CmdZoomIn+CmdZoomOut", "Zoom the map in / out" },
            { "", "{{W|INTERACTING}}" },
            { "CmdGetFrom", "Interact nearby: talk, open, take, from a square next to you" },
            { "CmdUse", "Use / confirm" },
            { "CmdCompanions", "Give orders to your companions" },
            { "", "{{W|FIGHTING}}" },
            { "Take A Step", "Step (or attack) in the left-stick direction" },
            { "ForceAttack", "Attack in the left-stick direction even if it's not hostile" },
            { "CmdFire+CmdReload", "Fire / reload your missile weapon" },
            { "CmdThrow", "Throw your thrown weapon" },
            { "Use Ability", "Use the selected ability on the bar" },
            { "Previous Ability+Next Ability", "Select previous / next ability on the bar" },
            { "CmdAbilities", "All abilities (and bind them to buttons)" },
            { "", "{{W|RESTING}}" },
            { "CmdWaitUntilHealed", "Rest until healed (stops if an enemy appears)" },
            { "CmdWaitMenu", "Wait menu: wait N turns, until morning (sleep), until the party is healed" },
            { "", "Make Camp (ability bar): cook, eat and use recipes" },
            { "", "{{W|CHARACTER & GAME}}" },
            { "CmdCharacter", "Character sheet: inventory, equipment, skills, quests, journal (LB/RB to switch)" },
            { "CmdMessageHistory", "Message history" },
            { "CmdSystemMenu", "System menu: save, quit, options, controls" },
            { "CmdHelp", "Game help" },
            { "", "{{W|TIPS}}" },
            { "", "LT is the 'Alt' button: hold it, then press the other button" },
            { "", "Rest until healed before stairs or a fight; eat and drink when the status bar says so" },
            { "", "Bright Qud map markers: Options → Mods → show legend" },
        };

        static string Binding(string ids)
        {
            var parts = new List<string>();
            foreach (string id in ids.Split('+'))
            {
                string b = null;
                try { b = ControlManager.getCommandInputFormatted(id); } catch (Exception) { }
                parts.Add(b.IsNullOrEmpty() || b.Contains("NEEDUICONTEXT") ? "{{K|-}}" : b);
            }
            return string.Join(" / ", parts);
        }

        static List<string> Lines()
        {
            var lines = new List<string>();
            for (int i = 0; i < Rows.GetLength(0); i++)
                lines.Add(Rows[i, 0].Length == 0 ? Rows[i, 1] : Binding(Rows[i, 0]) + "  " + Rows[i, 1]);
            return lines;
        }

        const string Intro = "Your current buttons ({{K|-}} = not bound; change them in Options → Controls). "
            + "Pick a line to do it now.";

        // From the map (game thread): picking a line runs that command.
        public static void ShowFromGame()
        {
            int pick = XRL.UI.Popup.PickOption("Controls reminder", Intro, "", "Sounds/UI/ui_notification",
                Lines(), null, null, null, null, null, null, 0, 78, 0, -1, AllowEscape: true);
            if (pick < 0 || pick >= Rows.GetLength(0)) return;
            string id = Rows[pick, 0];
            if (id.Length == 0 || id.Contains("+") || id == "Take A Step" || id == "ForceAttack"
                || id == "LookDirection" || id == "Use Ability" || id == "Previous Ability+Next Ability") return;
            ConsoleLib.Console.Keyboard.PushMouseEvent("Command:" + id);
        }

        // From Options → Mods (UI thread).
        public static async System.Threading.Tasks.Task<bool> Show()
        {
            try
            {
                await XRL.UI.Popup.PickOptionAsync("Controls reminder",
                    "Your current buttons ({{K|-}} = not bound). In game: LT + View opens this.", "", Lines(),
                    MaxWidth: 78, AllowEscape: true);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Controls", e);
            }
            return false;
        }
    }

    [HarmonyPatch(typeof(CommandEvent), nameof(CommandEvent.Send),
        new Type[] { typeof(XRL.World.GameObject), typeof(string), typeof(XRL.World.GameObject), typeof(Cell),
            typeof(int), typeof(bool), typeof(bool), typeof(XRL.World.GameObject) })]
    public static class ControlsCommandPatch
    {
        static bool Prefix(XRL.World.GameObject Actor, string Command, ref bool __result)
        {
            if (Command != Controls.Command && Command != Quests.Command && Command != Controls.MarkersCommand) return true;
            try
            {
                if (Actor != null && Actor.IsPlayer())
                {
                    if (Command == Quests.Command) Quests.ShowFromGame();
                    else if (Command == Controls.MarkersCommand) Settings.ToggleMapMarkers();
                    else Controls.ShowFromGame();
                }
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Controls", e);
            }
            __result = true;
            return false;
        }
    }

    // The reminder also works on the world map.
    [HarmonyPatch(typeof(XRL.UI.AbilityManager), nameof(XRL.UI.AbilityManager.IsWorldMapUsable),
        new Type[] { typeof(string) })]
    public static class ControlsWorldMapPatch
    {
        static void Postfix(string AbilityCommand, ref bool __result)
        {
            if (AbilityCommand == Controls.Command || AbilityCommand == Quests.Command
                || AbilityCommand == Controls.MarkersCommand) __result = true;
        }
    }

    // Speech bubbles: 256 = bright (worth talking to), 1024 = faded (already talked, nothing pending).
    public static class Talk
    {
        public const string TalkedProperty = "BrightQudTalked";
        static readonly Dictionary<XRL.World.GameObject, (long turn, int bits)> Cache =
            new Dictionary<XRL.World.GameObject, (long, int)>();

        public static int Bubble(XRL.World.GameObject o)
        {
            long turn = The.CurrentTurn;
            lock (Cache)
            {
                if (Cache.TryGetValue(o, out var c) && c.turn == turn) return c.bits;
            }
            int bits = Compute(o);
            lock (Cache)
            {
                if (Cache.Count > 500) Cache.Clear();
                Cache[o] = (turn, bits);
            }
            return bits;
        }

        static int Compute(XRL.World.GameObject o)
        {
            var cs = o.GetPart<XRL.World.Parts.ConversationScript>();
            if (cs == null) return 0;
            bool merchant = o.HasPart("GenericInventoryRestocker");
            bool questGiver = !cs.Quest.IsNullOrEmpty();
            if (!merchant && !o.HasProperName && !questGiver) return 0;
            if (o.GetIntProperty(TalkedProperty) == 0) return 256;
            if (questGiver && !The.Game.HasFinishedQuest(cs.Quest)) return 256;
            if (HasOpenQuestFrom(o)) return 256;
            return 1024;
        }

        // A quest you're still doing that this character gave you (you'll want to report back).
        static bool HasOpenQuestFrom(XRL.World.GameObject o)
        {
            var quests = The.Game?.Quests;
            if (quests == null || quests.Count == 0) return false;
            string name = QudColor.StripFormatting(o.BaseDisplayName ?? "");
            if (name.Length == 0) return false;
            foreach (var q in quests.Values)
            {
                if (q == null || q.Finished || q.QuestGiverName.IsNullOrEmpty()) continue;
                string giver = QudColor.StripFormatting(q.QuestGiverName);
                if (giver.IndexOf(name, StringComparison.OrdinalIgnoreCase) >= 0
                    || name.IndexOf(giver, StringComparison.OrdinalIgnoreCase) >= 0) return true;
            }
            return false;
        }
    }

    // Remembers who you've talked to (an int property on that character, saved with it).
    [HarmonyPatch(typeof(AfterConversationEvent), nameof(AfterConversationEvent.Send),
        new Type[] { typeof(XRL.World.GameObject), typeof(XRL.World.GameObject), typeof(XRL.World.GameObject),
            typeof(XRL.World.GameObject), typeof(XRL.World.Conversations.Conversation), typeof(bool), typeof(bool),
            typeof(bool) })]
    public static class AfterConversationPatch
    {
        static void Postfix(XRL.World.GameObject Actor, XRL.World.GameObject SpeakingWith)
        {
            try
            {
                if (Actor != null && Actor.IsPlayer() && SpeakingWith != null)
                    SpeakingWith.SetIntProperty(Talk.TalkedProperty, 1);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Talk", e);
            }
        }
    }

    // Tile particles (thrown items without VFX, ability blips...) paint a black background behind their
    // tile and skip the recolor. Afterwards: ground color behind them and the Bright Qud tile.
    [HarmonyPatch(typeof(XRL.UI.ParticleManager), nameof(XRL.UI.ParticleManager.Render),
        new Type[] { typeof(ScreenBuffer) })]
    public static class ParticlePatch
    {
        [ThreadStatic] static List<(int x, int y, string tile)> drawn;

        static void Prefix(XRL.UI.ParticleManager __instance)
        {
            if (drawn == null) drawn = new List<(int, int, string)>();
            drawn.Clear();
            try
            {
                if (!Settings.EffectGround) return;
                foreach (var t in __instance.TileParticles)
                    if (t != null && !t.Tile.IsNullOrEmpty())
                        drawn.Add((Convert.ToInt32(t.x), Convert.ToInt32(t.y), t.Tile));
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Particles", e);
            }
        }

        static void Postfix(ScreenBuffer Buffer)
        {
            if (drawn == null || drawn.Count == 0) return;
            try
            {
                foreach (var (x, y, tile) in drawn)
                {
                    if (x < 0 || y < 0 || x > 79 || y > 24) continue;
                    ConsoleChar ch = Buffer.Buffer[x, y];
                    if (ch == null || ch._Tile != tile) continue;
                    Color b = ch.Background;
                    if (b.r < 0.06f && b.g < 0.06f && b.b < 0.06f) ch.Background = Ground.GroundAt(x, y);
                    string virt = Recolor.Resolve(tile, ch.Foreground, ch.Detail, false, null, default,
                        Settings.AutoStyle ? Recolor.StyleObject : Recolor.StyleNone);
                    if (virt != null) ch._Tile = virt;
                }
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Particles", e);
            }
            drawn.Clear();
        }
    }

    // Thrown items and missiles fly as a separate rotating sprite (ProjectileRenderer). Our tiles have
    // their ground shadow baked in, which smeared a dark patch around the spinning projectile: give the
    // projectile a shadow-free Bright Qud texture instead.
    [HarmonyPatch(typeof(ProjectileRenderer), nameof(ProjectileRenderer.LoadFields),
        new Type[] { typeof(Dictionary<string, string>) })]
    public static class ProjectilePatch
    {
        static void Postfix(ProjectileRenderer __instance, Dictionary<string, string> Values)
        {
            try
            {
                if (__instance?.Projectile == null) return;
                if (!__instance.TryGetInheritable(Values, "Tile", "RenderTile", out string tile) || tile.IsNullOrEmpty())
                    return;
                string virt = Recolor.Resolve(tile, __instance.Foreground, __instance.Detail, false, null, default,
                    Recolor.StyleProjectile);
                if (virt != null && Recolor.TryGet(virt, out exTextureInfo info))
                {
                    __instance.Projectile.textureInfo = info;
                    __instance.Projectile.shader = SpriteManager.GetShaderMode(info.ShaderMode);
                }
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Projectile", e);
            }
        }
    }

    // Look / hover tooltip: a short plain-words summary of what matters, above the flavour text.
    [HarmonyPatch(typeof(XRL.UI.Look), nameof(XRL.UI.Look.GenerateTooltipInformation),
        new Type[] { typeof(XRL.World.GameObject) })]
    public static class LookStatsPatch
    {
        static void Postfix(XRL.World.GameObject go, ref XRL.UI.Look.TooltipInformation __result)
        {
            try
            {
                if (go == null || !Settings.LookStats) return;
                string summary = go.Brain != null && !go.IsPlayer() ? Creature(go) : go.Brain == null ? Region(go) ?? Item(go) : null;
                if (!summary.IsNullOrEmpty())
                    __result.LongDescription = summary + "\n\n" + __result.LongDescription;
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.LookStats", e);
            }
        }

        static string Words(string id) =>
            System.Text.RegularExpressions.Regex.Replace(id ?? "", "(?<=[a-z])(?=[A-Z])", " ");

        static string Name(XRL.World.GameObject o) => QudColor.StripFormatting(o.ShortDisplayNameStripped ?? "");

        static string Creature(XRL.World.GameObject o)
        {
            var sb = new System.Text.StringBuilder();
            sb.Append("{{W|Level ").Append(o.Level).Append("}}  HP ").Append(o.hitpoints).Append('/')
              .Append(o.baseHitpoints).Append("  {{c|AV}} ").Append(o.GetStatValue("AV"))
              .Append("  {{g|DV}} ").Append(o.GetStatValue("DV"));
            var melee = new List<string>();
            string ranged = null;
            // Each part is optional: plants and turrets have a brain but no body or mutations.
            try { Gear(o, melee, ref ranged); } catch (Exception e) { MetricsManager.LogException("BrightQud.LookStats.Gear", e); }
            if (melee.Count > 0) sb.Append("\n{{R|Attacks:}} ").Append(string.Join(", ", melee));
            if (ranged != null) sb.Append("\n{{R|Ranged:}} ").Append(ranged);
            try
            {
                if (Settings.ExplainPowers) Explain.Append(o, sb);
                else Mutations(o, sb);
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.LookStats.Mutations", e); }
            return sb.ToString();
        }

        static void Gear(XRL.World.GameObject o, List<string> melee, ref string ranged)
        {
            foreach (var eq in o.GetEquippedObjects() ?? new List<XRL.World.GameObject>())
            {
                if (eq == null) continue;
                var mw = eq.GetPart<XRL.World.Parts.MeleeWeapon>();
                // Clothes have an improvised MeleeWeapon too: only real or natural weapons count.
                bool weapon = eq.GetInventoryCategory() == "Melee Weapons"
                    || eq.HasTag("NaturalGear") && !eq.HasPart<XRL.World.Parts.Armor>();
                if (mw != null && weapon && melee.Count < 3)
                {
                    string m = Name(eq) + " " + mw.BaseDamage;
                    if (!melee.Contains(m)) melee.Add(m);
                }
                if (ranged == null && eq.HasPart("MissileWeapon")) ranged = Name(eq);
            }
        }

        static void Mutations(XRL.World.GameObject o, System.Text.StringBuilder sb)
        {
            var muts = o.GetPart<XRL.World.Parts.Mutations>();
            if (muts?.MutationList != null && muts.MutationList.Count > 0)
            {
                var names = new List<string>();
                foreach (var m in muts.MutationList)
                    if (m != null && names.Count < 5) names.Add(QudColor.StripFormatting(m.GetDisplayName(false)));
                sb.Append("\n{{M|Mutations:}} ").Append(string.Join(", ", names));
            }
        }

        // World-map terrain: which levels the region suits, against yours (same tiers as the danger tint).
        static string Region(XRL.World.GameObject o)
        {
            string t = o.GetTag("RegionTier", null);
            if (t == null || !int.TryParse(t, out int tier) || The.Player == null) return null;
            tier = Math.Max(1, tier);
            int level = The.Player.Stat("Level");
            int from = (tier - 1) * 5 + 1, to = tier * 5;
            int d = tier - Ground.SuitedTier(level);
            string verdict = d >= 2 ? "{{R|much tougher than you}}" : d == 1 ? "{{W|tougher than you}}"
                : d == 0 ? "{{G|right for your level}}" : "{{g|easy for you}}";
            return "{{W|Region: about level " + from + "-" + (tier >= 8 ? "40+" : to.ToString()) + "}}  (you: " + level + ") - " + verdict;
        }

        static string Item(XRL.World.GameObject o)
        {
            if (!o.IsTakeable()) return null;
            var lines = new List<string>();
            if (!o.Understood())
                lines.Add("{{K|Not identified yet: examine it or ask a tinker.}}");
            else
            {
                var mw = o.GetPart<XRL.World.Parts.MeleeWeapon>();
                if (mw != null && !o.HasTag("NaturalGear") && o.GetInventoryCategory() == "Melee Weapons")
                    lines.Add("{{R|Melee:}} " + mw.BaseDamage + " damage"
                        + (mw.PenBonus != 0 ? ", +" + mw.PenBonus + " penetration" : "")
                        + " ({{K|" + Words(mw.Skill) + "}})");
                var miss = o.GetPart<XRL.World.Parts.MissileWeapon>();
                if (miss != null)
                    lines.Add("{{R|Ranged weapon}} ({{K|" + Words(miss.Skill) + "}}"
                        + (miss.ShotsPerAction > 1 ? ", " + miss.ShotsPerAction + " shots" : "") + ")");
                var armor = o.GetPart<XRL.World.Parts.Armor>();
                if (armor != null)
                {
                    string a = "{{c|Armor:}} AV " + armor.AV + ", DV " + armor.DV + " (worn on " + armor.WornOn + ")";
                    if (armor.Heat != 0) a += ", heat " + armor.Heat;
                    if (armor.Cold != 0) a += ", cold " + armor.Cold;
                    if (armor.Elec != 0) a += ", electric " + armor.Elec;
                    if (armor.Acid != 0) a += ", acid " + armor.Acid;
                    lines.Add(a);
                }
                var shield = o.GetPart<XRL.World.Parts.Shield>();
                if (shield != null) lines.Add("{{c|Shield:}} AV " + shield.AV + ", DV " + shield.DV);
                var cell = o.GetPart<XRL.World.Parts.EnergyCell>();
                if (cell != null) lines.Add("{{Y|Charge:}} " + cell.Charge + "/" + cell.MaxCharge);
                var liquid = o.GetPart<XRL.World.Parts.LiquidVolume>();
                if (liquid != null && liquid.MaxVolume > 0)
                    lines.Add("{{B|Holds:}} " + (liquid.Volume > 0
                        ? QudColor.StripFormatting(liquid.GetLiquidDescription()) : "empty")
                        + " (max " + liquid.MaxVolume + " drams)");
                if (o.HasPart("Food")) lines.Add("{{G|Food}}: eat it to stay sated");
            }
            lines.Add("{{K|Weight " + o.Weight + " lbs}}");
            string compare = ItemCompare.Block(o);
            if (compare != null) lines.Add(compare);
            return string.Join("\n", lines);
        }
    }

    // In-game switches (mod Options.xml, "Mods" section). Read at most once per second.
    public static class Settings
    {
        static int lastCheck;
        static bool refreshed;
        static bool animation = true, tileAnimation = false, autoStyle = true, ground = true, threatRings = true, healthBars = true,
            itemSparkle = true, playerMarker = true, lowHealth = true, talkMarkers = true,
            interactMarkers = true, clearMemory = true, fireOverlay = true, effectGround = true, dangerTint = true, lookStats = true,
            abilityHelp = true, compareItems = true, explainPowers = true, questBanner = true;
        static string playerLook = null, font = "Clear mono", abilityBar = "More", uiTheme = "Qud teal";

        static void Refresh()
        {
            // (lastCheck starts at MinValue: now - MinValue overflows to a negative number, which made
            // this throttle skip every refresh on a machine with a long uptime.)
            int now = Environment.TickCount;
            if (refreshed && unchecked(now - lastCheck) < 1000) return;
            refreshed = true;
            lastCheck = now;
            try
            {
                animation = XRL.UI.Options.GetOption("OptionBrightQudAnimation", "Yes").EqualsNoCase("Yes");
                tileAnimation = XRL.UI.Options.GetOption("OptionBrightQudTileAnimation", "No").EqualsNoCase("Yes"); // off by default (user rule)
                autoStyle = XRL.UI.Options.GetOption("OptionBrightQudAutoStyle", "Yes").EqualsNoCase("Yes");
                ground = XRL.UI.Options.GetOption("OptionBrightQudGround", "Yes").EqualsNoCase("Yes");
                threatRings = XRL.UI.Options.GetOption("OptionBrightQudThreatRings", "Yes").EqualsNoCase("Yes");
                healthBars = XRL.UI.Options.GetOption("OptionBrightQudHealthBars", "Yes").EqualsNoCase("Yes");
                itemSparkle = XRL.UI.Options.GetOption("OptionBrightQudItemSparkle", "Yes").EqualsNoCase("Yes");
                playerMarker = XRL.UI.Options.GetOption("OptionBrightQudPlayerMarker", "Yes").EqualsNoCase("Yes");
                lowHealth = XRL.UI.Options.GetOption("OptionBrightQudLowHealth", "Yes").EqualsNoCase("Yes");
                talkMarkers = XRL.UI.Options.GetOption("OptionBrightQudTalkMarkers", "Yes").EqualsNoCase("Yes");
                interactMarkers = XRL.UI.Options.GetOption("OptionBrightQudInteractMarkers", "Yes").EqualsNoCase("Yes");
                clearMemory = XRL.UI.Options.GetOption("OptionBrightQudClearMemory", "Yes").EqualsNoCase("Yes");
                fireOverlay = XRL.UI.Options.GetOption("OptionBrightQudFireOverlay", "Yes").EqualsNoCase("Yes");
                effectGround = XRL.UI.Options.GetOption("OptionBrightQudEffectGround", "Yes").EqualsNoCase("Yes");
                dangerTint = XRL.UI.Options.GetOption("OptionBrightQudDangerTint", "Yes").EqualsNoCase("Yes");
                lookStats = XRL.UI.Options.GetOption("OptionBrightQudLookStats", "Yes").EqualsNoCase("Yes");
                abilityHelp = XRL.UI.Options.GetOption("OptionBrightQudAbilityHelp", "Yes").EqualsNoCase("Yes");
                compareItems = XRL.UI.Options.GetOption("OptionBrightQudCompareItems", "Yes").EqualsNoCase("Yes");
                explainPowers = XRL.UI.Options.GetOption("OptionBrightQudExplainPowers", "Yes").EqualsNoCase("Yes");
                questBanner = XRL.UI.Options.GetOption("OptionBrightQudQuestBanner", "Yes").EqualsNoCase("Yes");
                font = XRL.UI.Options.GetOption("OptionBrightQudFont", "Clear mono") ?? "Game default";
                abilityBar = XRL.UI.Options.GetOption("OptionBrightQudAbilityBar", "More") ?? "Game default";
                uiTheme = XRL.UI.Options.GetOption("OptionBrightQudTheme", "Qud teal") ?? "Qud teal";
                string look = XRL.UI.Options.GetOption("OptionBrightQudPlayerLook", "Game default");
                playerLook = look.IsNullOrEmpty() || look.EqualsNoCase("Game default") ? null
                    : "brightqudlook/" + look.ToLowerInvariant();
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Settings", e);
            }
        }

        public static bool Animation { get { Refresh(); return animation; } }
        public static bool TileAnimation { get { Refresh(); return tileAnimation; } }

        // One press (F6, or from the controls reminder): item sparkle and gold corners all off, or all on.
        public static void ToggleMapMarkers()
        {
            bool on = !(ItemSparkle || InteractMarkers);
            XRL.UI.Options.SetOption("OptionBrightQudItemSparkle", on);
            XRL.UI.Options.SetOption("OptionBrightQudInteractMarkers", on);
            refreshed = false;
            XRL.Messages.MessageQueue.AddPlayerMessage(on
                ? "Bright Qud: item sparkle and gold corners {{G|on}}."
                : "Bright Qud: item sparkle and gold corners {{R|off}} (F6 or the controls reminder to turn back on).");
        }
        public static bool AutoStyle { get { Refresh(); return autoStyle; } }
        public static bool Ground { get { Refresh(); return ground; } }
        public static bool ThreatRings { get { Refresh(); return threatRings; } }
        public static bool HealthBars { get { Refresh(); return healthBars; } }
        public static bool ItemSparkle { get { Refresh(); return itemSparkle; } }
        public static bool PlayerMarker { get { Refresh(); return playerMarker; } }
        public static bool LowHealthWarning { get { Refresh(); return lowHealth; } }
        public static bool TalkMarkers { get { Refresh(); return talkMarkers; } }
        public static bool InteractMarkers { get { Refresh(); return interactMarkers; } }
        public static bool ClearMemory { get { Refresh(); return clearMemory; } }
        public static bool FireOverlay { get { Refresh(); return fireOverlay; } }
        public static bool EffectGround { get { Refresh(); return effectGround; } }
        public static bool DangerTint { get { Refresh(); return dangerTint; } }
        public static bool LookStats { get { Refresh(); return lookStats; } }
        public static bool ExplainPowers { get { Refresh(); return explainPowers; } }
        public static bool QuestBanner { get { Refresh(); return questBanner; } }
        public static bool AbilityHelp { get { Refresh(); return abilityHelp; } }
        public static bool CompareItems { get { Refresh(); return compareItems; } }
        // "Game default", "Clear mono" or "Readable" (UiTweaks.cs Fonts).
        public static string Font { get { Refresh(); return font; } }
        // "Game default", "More" or "Most" abilities per page.
        public static string AbilityBar { get { Refresh(); return abilityBar; } }
        // "Qud teal" (game colours) or a Theme.cs theme name.
        public static string UiTheme { get { Refresh(); return uiTheme; } }

        // Tile key of the chosen player look, or null for the game's own tile.
        public static string PlayerLook { get { Refresh(); return playerLook; } }

        // The tile to draw for the player: the chosen look if it exists, else the game's tile.
        public static string PlayerTile(string gameTile)
        {
            string look = PlayerLook;
            return look != null && Recolor.Exists(look) ? look : gameTile;
        }

        public static bool IsPlayerTile(string tile)
        {
            var player = The.Player;
            return tile != null && player?.Render != null && player.Render.Tile == tile;
        }
    }

    // Ground color behind every tile (the cell background the shaders blend with transparent pixels).
    public static class Ground
    {
        static readonly Color Earth = Hex("3b3326");
        static readonly Color Indoor = Hex("54402c");
        static readonly Color Stone = Hex("2c2f35");
        const int RefreshTurns = 25;
        static float MemoryFade => Settings.ClearMemory ? 0.35f : 0.55f;
        // Remembered ground fades toward a dark night blue (the game's teal 'k' cast everything teal).
        static Color MemoryGround => Settings.ClearMemory ? Hex("10141e") : QudColor.ColorMap['k'];
        // Never-seen cells: near black instead of the game's teal, so what you know stands out.
        static readonly Color Unexplored = Hex("0a0c10");

        // Set by the Cell.Render postfix, consumed by the ConsoleChar.Set postfix that Zone.Render
        // calls right after it with the same RenderEvent.
        [ThreadStatic] static RenderEvent pendingEvent;
        [ThreadStatic] static Cell pendingCell;
        [ThreadStatic] static bool pendingExplored;

        static Zone cachedZone;
        static long cachedTurn = -1;
        static bool[,] enclosed;
        static Color[,] outdoor; // smoothed outdoor ground per cell

        static Color Hex(string h)
        {
            UnityEngine.ColorUtility.TryParseHtmlString("#" + h, out Color c);
            return c;
        }

        public static void Remember(Cell cell, RenderEvent e, bool explored)
        {
            pendingCell = cell;
            pendingEvent = e;
            pendingExplored = explored;
        }

        // Also reports terrain to draw under the cell's top tile: the game shows only one object per
        // cell, so a swimmer would otherwise sit on a flat colored square instead of the water.
        public static void Apply(ConsoleChar ch, RenderEvent e, bool memory, out string under, out Color underColor,
            out int style, out int mutations, out int frame, out bool isPlayer, out int hud)
        {
            isPlayer = false;
            hud = 0;
            under = null;
            underColor = default;
            style = Recolor.StyleNone;
            mutations = 0;
            frame = 0;
            if (!ReferenceEquals(e, pendingEvent) || pendingCell == null) return;
            Cell cell = pendingCell;
            pendingCell = null;
            pendingEvent = null;
            if (!pendingExplored)
            {
                if (Settings.Ground && Settings.ClearMemory && IsDefault(ch.Background) && cell.ParentZone != null
                    && !cell.ParentZone.IsWorldMap())
                {
                    ch.Background = Unexplored;
                    if (ch._Tile == null && ch.Char == ' ') ch.Foreground = Unexplored;
                }
                return;
            }
            style = StyleOf(cell, e.Tile, out mutations, out bool creature, out isPlayer, out hud);
            XRL.World.GameObject top = lastTop;
            if (memory) hud = 0;
            if (!isPlayer && Settings.Ground && cell.ParentZone != null && cell.ParentZone.IsWorldMap())
            {
                ch.Foreground = WorldTone(ch.Foreground);
                ch.Detail = WorldTone(ch.Detail);
            }
            // Idle animation, creatures bob on a shared beat (~1 per second).
            int beat = (XRL.Core.XRLCore.CurrentFrame / 31) % 2;
            // Burning: flames drawn around the object instead of a flickering yellow/black square;
            // the object keeps its own colors.
            bool burning = lastBurning && !memory;
            if (burning)
            {
                int flicker = (XRL.Core.XRLCore.CurrentFrame / 8) % 2;
                hud |= 2048 | (flicker == 1 ? 4096 : 0);
                ch.Foreground = lastBaseFg;
                ch.Background = QudColor.ColorMap['k'];
            }
            if (creature && !memory && Settings.Animation) frame = beat;
            if (lastCrystal) ch.Foreground = Color.Lerp(ch.Foreground, Lavender, 0.35f);
            // Black marble: cool dark stone with pale lavender-grey veins (the game's veins are tan).
            if (lastMarble)
            {
                ch.Foreground = MarbleStone;
                ch.Detail = MarbleVein;
            }
            // Rainbow Wood: the painted grass/dirt becomes lush moss, tufts and tiny mushrooms.
            bool lush = false;
            if (top == null && Settings.Ground && e.Tile != null && e.Tile == cell.PaintTile && ZoneKind(cell) == KindFungal)
            {
                int h = Hash(cell.X, cell.Y);
                int v = h % 100 < 35 ? (h / 100) % 2 : 2 + (h / 100) % 14;
                ch._Tile = LushTiles[v];
                lush = v >= 13;
            }
            if (Settings.Ground && cell.ParentZone != null && !cell.ParentZone.IsWorldMap())
            {
                int kind = ZoneKind(cell);
                bool bare = top == null && (e.Tile != null ? e.Tile == cell.PaintTile : ch.Char == ' ' || ch.Char == '.');
                if (kind == KindJoppa && bare)
                {
                    // Joppa's salt-spangled earth: the warm-earth family tiles on every bare cell.
                    ch._Tile = FamilyTiles[1][Hash(cell.X, cell.Y) % 16];
                }
                else if (kind == KindFamily && bare)
                    ch._Tile = FamilyTiles[zoneFamily][Hash(cell.X, cell.Y) % 16];
                else if ((kind == KindFamily || kind == KindJoppa || kind == KindSalt) && top != null
                    && top.Render.RenderLayer == 0 && top.LiquidVolume == null && top.Brain == null
                    && top.Blueprint != "DirtPath" && top.Blueprint != "DirtFloor")
                {
                    // Floors placed as objects stay low-contrast with the zone's ground (zone average:
                    // few distinct colours, so few cached textures).
                    ch.Foreground = Scale(zoneGround, 1.14f);
                    ch.Detail = Scale(zoneGround, 0.86f);
                }
                else if ((kind == KindJoppa || kind == KindFamily) && top != null && (top.Blueprint == "DirtPath" || top.Blueprint == "DirtFloor"))
                {
                    // packed paths, a little darker than the open ground
                    ch.Foreground = kind == KindJoppa ? PathLight : Scale(zoneGround, 1.06f);
                    ch.Detail = kind == KindJoppa ? PathDark : Scale(zoneGround, 0.78f);
                }
                else if (kind == KindSalt && bare)
                {
                    // The game leaves many salt cells bare; on light ground they read as flat squares.
                    // Every bare cell gets one of the 12 dune ripple tiles, as soft darker-ivory lines.
                    ch._Tile = DuneTiles[Hash(cell.X, cell.Y) % DuneTiles.Length];
                    ch.Foreground = ch.Detail = SaltShadow;
                }
                else if (top == null && !lush && e.Tile != null && e.Tile == cell.PaintTile && kind != KindFungal)
                {
                    if (kind == KindSalt)
                        ch.Foreground = ch.Detail = SaltShadow;
                    else
                    {
                        // Zone average, not the cell's own ground: few distinct colours, so few cached textures.
                        ch.Foreground = Calm(ch.Foreground, zoneGround);
                        ch.Detail = Calm(ch.Detail, zoneGround);
                    }
                }
                else if (top != null && top.LiquidVolume != null && kind != KindPlain)
                {
                    ch.Foreground = ZoneLiquid(kind, ch.Foreground, false);
                    ch.Detail = ZoneLiquid(kind, ch.Detail, true);
                }
                else if (top != null && (top.Blueprint.Contains("Fulcrete") || top.Blueprint == "TombSultan6Wall"))
                {
                    ch.Foreground = FulcreteGravel;
                    ch.Detail = FulcreteBitumen;
                }
                else if (top != null && top.Blueprint == "Verdigris")
                {
                    // Tarnished chrome: dull green-grey metal, not glossy cyan.
                    ch.Foreground = VerdigrisMetal;
                    ch.Detail = VerdigrisPatina;
                }
            }
            // Ambient floor: one step every ~1.2 s, offset per cell so the diamonds don't pulse together.
            if ((lastAmbient || lush) && !creature && !memory && Settings.TileAnimation)
                frame = (XRL.Core.XRLCore.CurrentFrame / 75 + cell.X * 3 + cell.Y * 5) % 4;
            // Item sparkle twinkles on the beat (only on frame 1).
            if ((hud & 32) != 0 && beat == 0) hud &= ~32;
            // Low-health pulse: red on one beat, the normal player ring (if on) on the other.
            if ((hud & 128) != 0 && beat == 0)
            {
                hud &= ~128;
                if (!Settings.PlayerMarker) hud &= ~64;
            }
            if (!Settings.AutoStyle) style = Recolor.StyleNone;
            XRL.World.GameObject liquid = cell.GetFirstObjectWithPart("LiquidVolume");
            string liquidTile = liquid?.Render?.Tile;
            if (liquidTile != null && e.Tile != null && e.Tile != liquidTile)
            {
                under = liquidTile;
                // Same color as the neighbouring water cells: LiquidVolume keeps the (mixed) liquid color
                // on its Render part. Fallback: the liquid tint the game put in the cell background.
                string cs = liquid.Render.ColorString;
                int amp = cs?.LastIndexOf('&') ?? -1;
                if (amp >= 0 && amp + 1 < cs.Length && QudColor.ColorMap.TryGetValue(cs[amp + 1], out Color lc))
                    underColor = lc;
                else
                    underColor = IsDefault(ch.Background) ? QudColor.ColorMap['B'] : ch.Background;
                underColor = ZoneLiquid(ZoneKind(cell), underColor, false);
                // The game tints the whole cell with the liquid color; with the liquid drawn as a tile
                // underneath, the rest of the cell should show the normal ground (puddles are small).
                Color ground = ColorFor(cell);
                ch.Background = memory ? Color.Lerp(ground, MemoryGround, MemoryFade) : ground;
                return;
            }
            if (!Settings.Ground) return;
            // Keep backgrounds an object asks for explicitly (anything but the default black 'k').
            if (!IsDefault(ch.Background)) return;
            Color g = ColorFor(cell);
            if (memory) g = Color.Lerp(g, MemoryGround, MemoryFade);
            else g = Lit(g, cell);
            ch.Background = g;
            // Empty text cells draw their "background" from Foreground (text shader swaps them).
            if (ch._Tile == null && ch.Char == ' ') ch.Foreground = g;
        }

        // Walkability tier of the object whose tile the cell shows (same tiers as the hand-drawn art).
        [ThreadStatic] static bool lastBurning;
        [ThreadStatic] static bool lastAmbient; // Moon Stair floor: diamonds twinkle (4 slow frames)
        [ThreadStatic] static bool lastMarble; // black marble walls and walkways
        [ThreadStatic] static XRL.World.GameObject lastTop; // object the cell shows, null for bare ground
        [ThreadStatic] static bool lastCrystal; // Moon Stair crystal or its floor: colors pulled toward lavender
        [ThreadStatic] static Color lastBaseFg;

        // The object's own foreground color (effects like Burning flicker the drawn one).
        static Color BaseColor(XRL.World.GameObject o)
        {
            string cs = o.Render.TileColor.IsNullOrEmpty() ? o.Render.ColorString : o.Render.TileColor;
            int amp = cs?.LastIndexOf('&') ?? -1;
            if (amp >= 0 && amp + 1 < cs.Length && QudColor.ColorMap.TryGetValue(cs[amp + 1], out Color c)) return c;
            return QudColor.ColorMap['y'];
        }

        public static Color GroundAt(int x, int y)
        {
            Zone zone = The.ActiveZone;
            Cell cell = zone?.GetCell(x, y);
            return cell != null ? ColorFor(cell) : Earth;
        }

        static int StyleOf(Cell cell, string tile, out int mutations, out bool creature, out bool player, out int hud)
        {
            lastBurning = false;
            lastAmbient = false;
            lastCrystal = false;
            lastMarble = false;
            lastTop = null;
            mutations = 0;
            creature = false;
            player = false;
            hud = 0;
            if (tile == null) return Recolor.StyleNone;
            XRL.World.GameObject top = null;
            for (int i = 0; i < cell.Objects.Count; i++)
            {
                var o = cell.Objects[i];
                if (o?.Render != null && o.Render.Tile == tile && (top == null || o.Render.RenderLayer > top.Render.RenderLayer))
                    top = o;
            }
            if (top == null) return Recolor.StyleNone;
            lastTop = top;
            lastAmbient = top.Blueprint == "SmallHexFloor";
            lastCrystal = lastAmbient || top.Blueprint == "CrystalWall";
            lastMarble = top.Blueprint == "Black Marble" || top.Blueprint == "BlackMarbleWalkway";
            lastBurning = Settings.FireOverlay && top.HasEffect<XRL.World.Effects.Burning>();
            if (lastBurning) lastBaseFg = BaseColor(top);
            if (top.Brain != null)
            {
                creature = true;
                player = top.IsPlayer();
                hud = player ? PlayerHud(top) : HudOf(top);
                // Mutations are parts named after their class (Horns, MultipleArms, Wings, ...).
                for (int b = 0; b < Recolor.MutationOrder.Length; b++)
                    if (top.HasPart(Recolor.MutationOrder[b])) mutations |= 1 << b;
                return Recolor.StyleObject;
            }
            bool container = top.HasPart("Container");
            if (Settings.InteractMarkers && (top.HasPart("StairsUp") || top.HasPart("StairsDown")
                || (container && top.Inventory != null && top.Inventory.Objects.Count > 0)))
                hud |= 512;
            if (top.IsTakeable())
            {
                if (Settings.ItemSparkle && !container) hud |= 32;
                return Recolor.StyleObject;
            }
            if (top.IsWall() || top.Physics?.Solid == true || top.HasPart("LiquidVolume")) return Recolor.StyleFlat;
            if (top.Render.Occluding) return Recolor.StyleTall;
            return top.Render.RenderLayer >= 5 ? Recolor.StyleObject : Recolor.StyleFlat;
        }

        // Threat ring + health bucket for a creature (see Recolor.DrawHud). Toggleable in Options.
        static int HudOf(XRL.World.GameObject o)
        {
            int hud = 0;
            var player = The.Player;
            bool hostile = player != null && o.IsHostileTowards(player), led = o.IsPlayerLed();
            if (Settings.ThreatRings && player != null)
            {
                if (led) hud |= 2;
                else if (hostile) hud |= 1;
            }
            // Talk bubble on people worth talking to: merchants, named characters, quest givers.
            if (Settings.TalkMarkers && !hostile && !led) hud |= Talk.Bubble(o);
            if (Settings.HealthBars)
            {
                int pct = o.GetHPPercent();
                if (pct < 100) hud |= Math.Max(1, Math.Min(5, (pct + 19) / 20)) << 2;
            }
            return hud;
        }

        // Ring under the player so you can find yourself at a glance; red pulse at <= 25% health.
        static int PlayerHud(XRL.World.GameObject p)
        {
            int hud = 0;
            if (Settings.PlayerMarker) hud |= 64;
            if (Settings.LowHealthWarning && p.GetHPPercent() <= 25) hud |= 64 | 128;
            return hud;
        }

        static bool IsDefault(Color c)
        {
            Color k = QudColor.ColorMap['k'];
            return (Mathf.Abs(c.r - k.r) < 0.02f && Mathf.Abs(c.g - k.g) < 0.02f && Mathf.Abs(c.b - k.b) < 0.02f)
                || (c.r < 0.02f && c.g < 0.02f && c.b < 0.02f);
        }

        static Color ColorFor(Cell cell)
        {
            Zone zone = cell.ParentZone;
            if (zone == null) return Earth;
            // (Inside zones are refreshed too: their fixed lights cast warm pools on the stone.)
            Refresh(zone);
            if (zone.IsInside() && !(underground && zoneKind == KindFamily)) return Stone;
            int x = cell.X, y = cell.Y;
            if (x < 0 || y < 0 || x >= enclosed.GetLength(0) || y >= enclosed.GetLength(1)) return Earth;
            if (enclosed[x, y]) return Indoor;
            Color c = outdoor[x, y];
            if (danger != null && Settings.DangerTint)
            {
                int d = danger[x, y];
                if (d >= 2) c = Color.Lerp(c, DangerHigh, 0.22f);
                else if (d == 1) c = Color.Lerp(c, DangerMid, 0.12f);
            }
            return c;
        }

        // World map: the game's terrain colors are full brightness (white salt, neon jungle) and a whole
        // screen of them glares. Calmer, a little warmer, never pure white.
        static Color WorldTone(Color c)
        {
            Color.RGBToHSV(c, out float h, out float s, out float v);
            if (s < 0.2f) return Color.HSVToRGB(0.11f, 0.12f, Mathf.Min(v, 0.68f));
            return Color.HSVToRGB(h, s * 0.72f, Mathf.Min(v, 0.8f));
        }

        static readonly Color DangerHigh = new Color(0.85f, 0.12f, 0.1f, 1f);
        static readonly Color DangerMid = new Color(0.95f, 0.55f, 0.1f, 1f);
        static int[,] danger; // world map only: region tier minus the tier that suits the player's level

        // Region tier (RegionTier tag of the terrain object, 1-8) vs the player's level: roughly one
        // tier per 5 levels (level 1-5 -> tier 1, 6-10 -> tier 2, ...).
        public static int SuitedTier(int level) => Math.Min(8, 1 + Math.Max(0, level - 1) / 5);

        static int[,] ComputeDanger(Zone zone)
        {
            var player = The.Player;
            if (player == null) return null;
            int suited = SuitedTier(player.Stat("Level"));
            var d = new int[zone.Width, zone.Height];
            for (int x = 0; x < zone.Width; x++)
                for (int y = 0; y < zone.Height; y++)
                {
                    Cell c = zone.GetCell(x, y);
                    int tier = 1;
                    if (c != null)
                        foreach (var o in c.Objects)
                        {
                            string t = o.GetTag("RegionTier", null);
                            if (t != null && int.TryParse(t, out int v) && v > tier) tier = v;
                        }
                    d[x, y] = tier - suited;
                }
            return d;
        }

        static void Refresh(Zone zone)
        {
            long turn = The.CurrentTurn;
            if (zone == cachedZone && enclosed != null && turn - cachedTurn < RefreshTurns && turn >= cachedTurn) return;
            zoneKind = KindOf(zone);
            underground = !zone.IsWorldMap() && zone.Z > 10;
            // Moon Stair surface: lavender ground everywhere (crystal clusters are not buildings);
            // underground family zones: caves are not buildings either.
            bool moon = zoneKind == KindMoon;
            enclosed = moon || (underground && zoneKind == KindFamily) ? new bool[zone.Width, zone.Height] : ComputeEnclosed(zone);
            outdoor = moon ? Marble(zone) : zoneKind == KindFungal ? Moss(zone)
                : zoneKind == KindSalt ? Flat(zone, SaltDark, SaltLight)
                : zoneKind == KindReef ? Flat(zone, ReefDark, ReefLight)
                : zoneKind == KindJoppa ? Flat(zone, JoppaDark, JoppaLight)
                : zoneKind == KindFamily ? Flat(zone, FamilyDark[zoneFamily], FamilyLight[zoneFamily]) : ComputeOutdoor(zone);
            ComputeLight(zone);
            danger = zone.IsWorldMap() ? ComputeDanger(zone) : null;
            Color sum = Color.clear;
            foreach (Color c in outdoor) sum += c;
            zoneGround = sum / outdoor.Length;
            zoneGround = new Color(Mathf.Round(zoneGround.r * 32f) / 32f, Mathf.Round(zoneGround.g * 32f) / 32f,
                Mathf.Round(zoneGround.b * 32f) / 32f, 1f);
            cachedZone = zone;
            cachedTurn = turn;
        }

        // Dusky lavender slate, after the community's painting of the Stair (pastel crystals, cool light).
        static readonly Color MarbleDark = Hex("2c2840");
        static readonly Color MarbleLight = Hex("352f4c");
        static readonly Color Lavender = Hex("b4a0ff");
        static readonly Color MarbleStone = Hex("221e30");
        static readonly Color MarbleVein = Hex("8c86b8");

        const int KindPlain = 0, KindMoon = 1, KindFungal = 2, KindSalt = 3, KindReef = 4, KindJoppa = 5, KindFamily = 6;

        // Ground families (docs/ZONE_STUDY_ALL.md): each has a calm ground colour and 16 textured tiles
        // (art/src/groundsets.py: low contrast, rich small detail) drawn on every bare cell.
        static int zoneFamily;
        static readonly string[] FamilyNames = { "salt", "earth", "rust", "green", "teal", "marsh", "redrock", "redcave",
            "rustwell", "rustcave" };
        static readonly Color[] FamilyDark = { Hex("a2967e"), Hex("6e5c42"), Hex("8c4e36"), Hex("3d3a28"), Hex("1e2c2c"), Hex("4e5040"),
            Hex("9b3f2b"), Hex("3b2622"), Hex("874a33"), Hex("2f2723") };
        static readonly Color[] FamilyLight = { Hex("ab9f87"), Hex("756247"), Hex("93543a"), Hex("433f2b"), Hex("233232"), Hex("54564a"),
            Hex("a1452e"), Hex("412a25"), Hex("8d4f37"), Hex("352c27") };
        const int FamilyRedRock = 6, FamilyRedCave = 7, FamilyRustWell = 8, FamilyRustCave = 9;
        // Fulcrete: "islands of carbon gravel in an ocean of bitumen" - tar-dark with pale gravel.
        static readonly Color FulcreteGravel = Hex("8a857c"), FulcreteBitumen = Hex("2a2826");
        static bool underground; // cached zone is below the surface (lights are always "at night")
        const int FamilyMarsh = 5;
        // Salt marsh water: silvery brackish grey-blue, as in real salt marshes (zone study 02).
        static readonly Color MarshWater = Hex("8fa6a8"), MarshWaterLight = Hex("c4d2d2");
        static readonly string[][] FamilyTiles = BuildFamilyTiles();

        static string[][] BuildFamilyTiles()
        {
            var t = new string[FamilyNames.Length][];
            for (int f = 0; f < t.Length; f++) t[f] = BuildTiles("brightqudground/" + FamilyNames[f] + "/", 16);
            return t;
        }

        static int FamilyOf(string bp)
        {
            switch (bp)
            {
                case "TerrainSixDayStilt": case "TerrainHills": case "TerrainMountains": case "TerrainMountainsSpindleShadow":
                    return 0;
                case "TerrainRedRock":
                    return FamilyRedRock;   // "a naturally reddened outcropping": redder than the canyon
                case "TerrainRustWell":
                    return FamilyRustWell;  // rust dust with flakes shed by the qudzu
                case "TerrainBethesdaSusa": case "TerrainRustedArchway":
                    return 2;
                case "TerrainJungle": case "TerrainDeepJungle": case "TerrainGolgotha": case "TerrainOmonporch":
                    return 3;
                case "TerrainGritGate":
                    return 4;
                case "TerrainSaltmarsh": case "TerrainSaltmarsh2": case "TerrainWatervine": case "TerrainJoppaRedrockChannel":
                    return FamilyMarsh;
            }
            if (bp.StartsWith("TerrainDesertCanyon", StringComparison.Ordinal)) return 2;
            if (bp.StartsWith("TerrainBananaGrove", StringComparison.Ordinal)) return 3;
            return -1;
        }
        static int zoneKind;
        static Color zoneGround; // average outdoor ground of the cached zone (rounded)
        static readonly Color MossDark = Hex("202116");
        static readonly Color MossLight = Hex("2a2b1c");
        static readonly Color MossWarm = Hex("4a2e1a"); // a few lava-lit patches

        // Surface zones with their own look: the Moon Stair and the Rainbow Wood.
        static int KindOf(Zone zone)
        {
            if (zone.IsWorldMap() || zone.Z < 10) return KindPlain;
            try
            {
                string bp = zone.GetTerrainObject()?.Blueprint;
                if (zone.Z > 10)
                {
                    // Underground: Red Rock's four strata get their red-brown rubble floor.
                    if (bp == "TerrainRedRock" || bp == "TerrainRustWell")
                    {
                        zoneFamily = bp == "TerrainRedRock" ? FamilyRedCave : FamilyRustCave;
                        return KindFamily;
                    }
                    return KindPlain;
                }
                if (bp == "TerrainMoonStair") return KindMoon;
                if (bp == "TerrainJoppa" || bp == "TerrainJoppaRuins") return KindJoppa;
                if (bp != null && bp.StartsWith("TerrainFungal", StringComparison.Ordinal)) return KindFungal;
                if (bp != null && (bp.StartsWith("TerrainSaltdunes", StringComparison.Ordinal)
                    || bp == "TerrainTremblezone")) return KindSalt;
                if (bp != null && bp.StartsWith("TerrainPalladiumReef", StringComparison.Ordinal)) return KindReef;
                int family = bp != null ? FamilyOf(bp) : -1;
                if (family >= 0)
                {
                    zoneFamily = family;
                    return KindFamily;
                }
            }
            catch (Exception) { }
            return KindPlain;
        }

        // Zone kind of the active zone (refreshes the cached ground like ColorFor does).
        static int ZoneKind(Cell cell)
        {
            Zone zone = cell.ParentZone;
            if (zone == null) return KindPlain;
            Refresh(zone);
            return zone.IsInside() && !(underground && zoneKind == KindFamily) ? KindPlain : zoneKind;
        }

        // Rainbow Wood: dark olive moss where the sun does not reach, a few warm patches.
        static Color[,] Moss(Zone zone)
        {
            var result = new Color[zone.Width, zone.Height];
            for (int x = 0; x < zone.Width; x++)
                for (int y = 0; y < zone.Height; y++)
                {
                    int h = Hash(x, y);
                    Color c = Color.Lerp(MossDark, MossLight, (h % 7) / 6f);
                    result[x, y] = h % 100 < 12 ? Color.Lerp(c, MossWarm, 0.5f) : c;
                }
            return result;
        }

        static readonly string[] LushTiles = BuildLushTiles(); // no string building per cell per frame

        static readonly string[] DuneTiles = BuildDuneTiles();

        static string[] BuildDuneTiles()
        {
            var t = new string[12];
            for (int i = 0; i < t.Length; i++) t[i] = "Terrain/sw_ground_dune_" + (i + 1) + ".png";
            return t;
        }

        static string[] BuildLushTiles()
        {
            var t = new string[16];
            for (int i = 0; i < t.Length; i++) t[i] = "brightqudlush/" + i;
            return t;
        }

        // Salt desert: sun-bleached ivory (the shared formula made it dark grey). Reef: the dark teal
        // islands of the official map art, so the sky-blue water and red coral stand out.
        static readonly Color SaltDark = Hex("a2967e"), SaltLight = Hex("ab9f87"), SaltShadow = Hex("877c66");
        static readonly Color ReefDark = Hex("1d3536"), ReefLight = Hex("233f40");
        // Joppa: "the salt-spangled earth" - pale sun-dried earth, darker packed paths.
        static readonly Color JoppaDark = Hex("6e5c42"), JoppaLight = Hex("756247");
        static readonly Color PathLight = Hex("8a7656"), PathDark = Hex("5e4c36");

        // Warm pools of light around fixed light sources (torch posts, campfires...) at night.
        static float[,] light;
        static bool night;
        static readonly Color TorchWarm = Hex("ffaa5a");

        static void ComputeLight(Zone zone)
        {
            light = null;
            try { night = underground || !XRL.World.Calendar.IsDay(); } catch (Exception) { night = underground; }
            if (!night || zone.IsWorldMap()) return;
            var l = new float[zone.Width, zone.Height];
            bool any = false;
            foreach (XRL.World.GameObject o in zone.GetObjectsWithPart("LightSource"))
            {
                var src = o.GetPart<XRL.World.Parts.LightSource>();
                Cell c = o.CurrentCell;
                if (src == null || !src.Lit || c == null || o.Brain != null) continue; // fixed lights only
                int r = Math.Min(Math.Max(src.Radius, 2), 6);
                for (int dx = -r; dx <= r; dx++)
                    for (int dy = -r; dy <= r; dy++)
                    {
                        int x = c.X + dx, y = c.Y + dy;
                        if (x < 0 || y < 0 || x >= zone.Width || y >= zone.Height) continue;
                        float d = Mathf.Sqrt(dx * dx + dy * dy) / r;
                        if (d >= 1f) continue;
                        float f = Mathf.Pow(1f - d, 1.5f);
                        if (f > l[x, y]) l[x, y] = f;
                        any = true;
                    }
            }
            light = any ? l : null;
        }

        // Ground under torch light: brighter and warmer, with a slow flicker.
        static Color Lit(Color g, Cell cell)
        {
            if (light == null || !Settings.Ground) return g;
            int x = cell.X, y = cell.Y;
            if (x < 0 || y < 0 || x >= light.GetLength(0) || y >= light.GetLength(1)) return g;
            float f = light[x, y];
            if (f <= 0f) return g;
            float flicker = Settings.TileAnimation ? 1f + 0.08f * Mathf.Sin(XRL.Core.XRLCore.CurrentFrame * 0.05f + x * 1.7f + y) : 1f;
            float k = f * 0.55f * flicker;
            Color b = new Color(Mathf.Min(1f, g.r * (1f + k * 1.2f)), Mathf.Min(1f, g.g * (1f + k * 1.2f)),
                Mathf.Min(1f, g.b * (1f + k * 1.2f)), 1f);
            return Color.Lerp(b, TorchWarm, k * 0.35f);
        }

        static string[] BuildTiles(string prefix, int n)
        {
            var t = new string[n];
            for (int i = 0; i < n; i++) t[i] = prefix + i;
            return t;
        }
        static readonly Color ReefWater = Hex("4aa8d8"), Algae = Hex("3fae3a");
        static readonly Color SoupTeal = Hex("2f6e66"), LavaLight = Hex("d8843c");
        static readonly Color VerdigrisMetal = Hex("5f857e"), VerdigrisPatina = Hex("4a6a4c");

        static Color[,] Flat(Zone zone, Color a, Color b)
        {
            var result = new Color[zone.Width, zone.Height];
            for (int x = 0; x < zone.Width; x++)
                for (int y = 0; y < zone.Height; y++)
                    result[x, y] = Color.Lerp(a, b, (Hash(x, y) % 5) / 4f);
            return result;
        }

        // Specks and ripples painted on bare ground take the ground's own hue: texture, not water.
        static Color Calm(Color c, Color ground)
        {
            Color.RGBToHSV(c, out float h, out float s, out float v);
            return Color.Lerp(Color.HSVToRGB(h, s * 0.5f, v), ground, 0.35f);
        }

        // Liquids in zones with their own look.
        static Color ZoneLiquid(int kind, Color c, bool detail)
        {
            if (kind == KindReef)
            {
                Color.RGBToHSV(c, out float h, out float _, out float _);
                bool algae = h > 0.17f && h < 0.45f;
                return detail ? (algae ? Algae : Color.Lerp(c, ReefWater, 0.3f)) : algae ? ReefWater : Color.Lerp(c, ReefWater, 0.5f);
            }
            if (kind == KindFamily && zoneFamily == FamilyMarsh)
                return detail ? Color.Lerp(c, MarshWaterLight, 0.5f) : Color.Lerp(c, MarshWater, 0.6f);
            if (kind == KindFungal) // primordial soup "cast in the light of lava"
                return detail ? Color.Lerp(c, LavaLight, 0.6f) : Color.Lerp(c, SoupTeal, 0.55f);
            return c;
        }

        static Color Scale(Color c, float k) => new Color(Mathf.Min(1f, c.r * k), Mathf.Min(1f, c.g * k), Mathf.Min(1f, c.b * k), 1f);

        static int Hash(int x, int y) => ((x * 73856093) ^ (y * 19349663)) & 0x7fffffff;

        static Color[,] Marble(Zone zone)
        {
            var result = new Color[zone.Width, zone.Height];
            for (int x = 0; x < zone.Width; x++)
                for (int y = 0; y < zone.Height; y++)
                    result[x, y] = Color.Lerp(MarbleDark, MarbleLight, ((x * 7 + y * 13) % 5) / 4f);
            return result;
        }

        // The game paints neighbouring cells randomly (grass/dirt), which gives a checkerboard if used
        // raw. Blend each cell with its 3x3 neighbourhood, then halfway toward the zone average.
        static Color[,] ComputeOutdoor(Zone zone)
        {
            int w = zone.Width, h = zone.Height;
            bool worldMap = zone.IsWorldMap();
            var raw = new Color[w, h];
            Color sum = Color.clear;
            for (int x = 0; x < w; x++)
                for (int y = 0; y < h; y++)
                {
                    Cell c = zone.GetCell(x, y);
                    // The world map has no painted ground: use each region's terrain color instead.
                    raw[x, y] = FromPaint(worldMap ? TerrainColor(c) : c?.PaintColorString);
                    sum += raw[x, y];
                }
            Color avg = sum / (w * h);
            var result = new Color[w, h];
            for (int x = 0; x < w; x++)
                for (int y = 0; y < h; y++)
                {
                    Color acc = Color.clear;
                    int n = 0;
                    for (int dx = -1; dx <= 1; dx++)
                        for (int dy = -1; dy <= 1; dy++)
                        {
                            int nx = x + dx, ny = y + dy;
                            if (nx < 0 || ny < 0 || nx >= w || ny >= h) continue;
                            acc += raw[nx, ny];
                            n++;
                        }
                    // World map regions are large and distinct: keep more of the local color there.
                    // (0.35: neighbouring cells differ less, so the ground doesn't show tile-sized squares)
                    Color c = Color.Lerp(avg, acc / n, worldMap ? 0.85f : 0.35f);
                    c.a = 1f;
                    result[x, y] = c;
                }
            return result;
        }

        // Color string of the terrain object a world-map cell shows (its top render layer).
        static string TerrainColor(Cell c)
        {
            if (c == null) return null;
            XRL.World.GameObject top = null;
            for (int i = 0; i < c.Objects.Count; i++)
            {
                var o = c.Objects[i];
                if (o?.Render != null && (top == null || o.Render.RenderLayer > top.Render.RenderLayer)) top = o;
            }
            if (top == null) return null;
            string tc = top.Render.TileColor;
            return !string.IsNullOrEmpty(tc) && tc.Contains("&") ? tc : top.Render.ColorString;
        }

        // Muted version of the painted ground color: same hue, low saturation and value, so it stays
        // well below creatures and items in brightness.
        static Color FromPaint(string colorString)
        {
            if (string.IsNullOrEmpty(colorString)) return Earth;
            int i = colorString.LastIndexOf('&');
            if (i < 0 || i + 1 >= colorString.Length) return Earth;
            if (!QudColor.ColorMap.TryGetValue(colorString[i + 1], out Color paint)) return Earth;
            Color.RGBToHSV(paint, out float h, out float s, out float v);
            if (s < 0.15f) return Earth; // greys/whites: plain earth
            return Color.HSVToRGB(h, Mathf.Min(s, 0.6f) * 0.55f, 0.25f);
        }

        // Cells not reachable from the zone edge without crossing walls or doors = inside a building.
        static bool[,] ComputeEnclosed(Zone zone)
        {
            int w = zone.Width, h = zone.Height;
            var barrier = new bool[w, h];
            var reached = new bool[w, h];
            var queue = new Queue<(int, int)>();
            for (int x = 0; x < w; x++)
                for (int y = 0; y < h; y++)
                {
                    Cell c = zone.GetCell(x, y);
                    barrier[x, y] = c != null && (c.HasWall() || c.HasObjectWithPart("Door"));
                    if ((x == 0 || y == 0 || x == w - 1 || y == h - 1) && !barrier[x, y])
                    {
                        reached[x, y] = true;
                        queue.Enqueue((x, y));
                    }
                }
            while (queue.Count > 0)
            {
                var (cx, cy) = queue.Dequeue();
                for (int dx = -1; dx <= 1; dx++)
                    for (int dy = -1; dy <= 1; dy++)
                    {
                        int nx = cx + dx, ny = cy + dy;
                        if (nx < 0 || ny < 0 || nx >= w || ny >= h || reached[nx, ny] || barrier[nx, ny]) continue;
                        // No squeezing diagonally between two barriers.
                        if (dx != 0 && dy != 0 && barrier[cx + dx, cy] && barrier[cx, cy + dy]) continue;
                        reached[nx, ny] = true;
                        queue.Enqueue((nx, ny));
                    }
            }
            var result = new bool[w, h];
            for (int x = 0; x < w; x++)
                for (int y = 0; y < h; y++)
                    result[x, y] = !reached[x, y] && !(barrier[x, y] && !zone.GetCell(x, y).HasObjectWithPart("Door"));
            return result;
        }
    }

    [HarmonyPatch(typeof(Cell), nameof(Cell.Render), new Type[] {
        typeof(RenderEvent), typeof(bool), typeof(LightLevel), typeof(bool), typeof(bool), typeof(bool), typeof(List<XRL.World.GameObject>) })]
    public static class CellRenderPatch
    {
        static void Postfix(Cell __instance, RenderEvent E, bool Explored)
        {
            Ground.Remember(__instance, E, Explored);
        }
    }

    // UI tiles (status bar portrait, look/inventory panels, ...).
    public static class UITiles
    {
        // UI images currently showing a Bright Qud sprite: their 3-color material must stay off.
        static readonly HashSet<int> Ours = new HashSet<int>();

        public static void Apply(UIThreeColorProperties ui, string tile, Color fg, Color detail)
        {
            if (ui == null || ui.image == null) return;
            int id = ui.GetInstanceID();
            Sprite sprite = tile == null ? null : Recolor.UISprite(tile, fg, detail);
            if (sprite == null)
            {
                if (Ours.Remove(id))
                {
                    // Back to a vanilla tile: let the game re-apply its own material and colors.
                    ui._currentForeground = new Color(1f, 2f, 3f, 4f);
                    ui.SetColors(ui.Foreground, ui.Detail, ui.Background);
                }
                return;
            }
            Ours.Add(id);
            ui.image.sprite = sprite;
            ui.image.material = null; // default UI material: draws the texture as-is
            ui.image.color = Color.white;
        }

        public static bool IsOurs(UIThreeColorProperties ui) => ui != null && Ours.Contains(ui.GetInstanceID());
    }

    [HarmonyPatch(typeof(UIThreeColorProperties), nameof(UIThreeColorProperties.FromRenderable))]
    public static class UIFromRenderablePatch
    {
        static void Postfix(UIThreeColorProperties __instance, IRenderable e)
        {
            try
            {
                if (e == null || e.getTile() == null) { UITiles.Apply(__instance, null, default, default); return; }
                ColorChars cc = e.getColorChars();
                string tile = Settings.IsPlayerTile(e.getTile()) ? Settings.PlayerTile(e.getTile()) : e.getTile();
                UITiles.Apply(__instance, tile, QudColor.colorFromChar(cc.foreground), QudColor.colorFromChar(cc.detail));
            }
            catch (Exception ex)
            {
                MetricsManager.LogException("BrightQud.UI", ex);
            }
        }
    }

    [HarmonyPatch(typeof(UIThreeColorProperties), nameof(UIThreeColorProperties.FromConsoleChar))]
    public static class UIFromConsoleCharPatch
    {
        static void Postfix(UIThreeColorProperties __instance, ConsoleChar c)
        {
            try
            {
                UITiles.Apply(__instance, c.Char == '\0' ? c.Tile : null, c.Foreground, c.Detail);
            }
            catch (Exception ex)
            {
                MetricsManager.LogException("BrightQud.UI", ex);
            }
        }
    }

    [HarmonyPatch(typeof(UIThreeColorProperties), "UpdateColors")]
    public static class UIUpdateColorsPatch
    {
        // Skip re-applying the 3-color material while one of our sprites is shown.
        static bool Prefix(UIThreeColorProperties __instance) => !UITiles.IsOurs(__instance);
    }

    // Animation sprites (jumps, thrown items: CombatJuiceEntryJump etc.) are separate pooled sprites
    // created from a tile path + colors, bypassing ConsoleChar.Set. Give them the recolored texture.
    [HarmonyPatch(typeof(SpriteManager), nameof(SpriteManager.GetPooledSprite), new Type[] {
        typeof(string), typeof(Color), typeof(Color), typeof(Color), typeof(bool), typeof(bool) })]
    public static class PooledSpritePatch
    {
        static void Postfix(ex3DSprite2 __result, string Path, Color Foreground, Color Detail)
        {
            try
            {
                if (__result == null || !GameManager.IsOnUIContext()) return;
                string tile = Settings.IsPlayerTile(Path) ? Settings.PlayerTile(Path) : Path;
                string virt = Recolor.Resolve(tile, Foreground, Detail, false, null, default, Recolor.StyleObject);
                if (virt == null || !Recolor.TryGet(virt, out exTextureInfo info) || info == null) return;
                __result.textureInfo = info;
                __result.shader = SpriteManager.GetShaderMode(info.ShaderMode);
            }
            catch (Exception ex)
            {
                MetricsManager.LogException("BrightQud.PooledSprite", ex);
            }
        }
    }

    [HarmonyPatch(typeof(SpriteManager), nameof(SpriteManager.TryGetTextureInfo))]
    public static class TryGetTextureInfoPatch
    {
        static bool Prefix(string Path, ref exTextureInfo Info, ref bool __result)
        {
            if (Path == null || !Path.StartsWith(Recolor.Prefix, StringComparison.Ordinal)) return true;
            try
            {
                __result = Recolor.TryGet(Path, out Info);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.TryGet", e);
                Info = null;
                __result = false;
            }
            return false;
        }
    }
}
