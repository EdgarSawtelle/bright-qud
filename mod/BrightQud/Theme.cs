// UI colour themes (Options → Mods → "interface colours").
//
// The game's menus are teal: frame/background sprites (polat-frame*, panelBgTile, ...) and flat
// teal Image colours. A theme remaps every teal-ish colour (hue 140-215°) to its own hue; the light
// "Tan parchment" theme also flips brightness (dark panels become light) and recolours every text
// mesh to dark ink so it stays readable. Item/creature icons are not teal UI art and
// are left alone (only sprites whose name looks like UI chrome are recoloured).
//
// Recoloured sprites are copies: the texture is read back through a RenderTexture (game textures are
// not CPU-readable), remapped once per texture and theme, and cached.

using System;
using System.Collections.Generic;
using HarmonyLib;
using TMPro;
using UnityEngine;
using UnityEngine.UI;

namespace BrightQud
{
    public static class Theme
    {
        struct Def { public float Hue, Sat, SatAdd; public bool Light; }

        static readonly Dictionary<string, Def> Defs = new Dictionary<string, Def>
        {
            { "Tan parchment", new Def { Hue = 36, Sat = 0.45f, SatAdd = 0.10f, Light = true } },
            { "Amber", new Def { Hue = 38, Sat = 1.0f, SatAdd = 0.05f } },
            { "Rust", new Def { Hue = 12, Sat = 1.0f, SatAdd = 0.05f } },
            { "Violet", new Def { Hue = 272, Sat = 0.9f } },
            { "Slate", new Def { Hue = 215, Sat = 0.45f } },
        };

        static string current = "";
        static Def def;
        static bool active;
        static readonly Dictionary<int, Texture2D> textures = new Dictionary<int, Texture2D>();
        static readonly Dictionary<int, Sprite> sprites = new Dictionary<int, Sprite>();
        // Our themed copy -> the game's sprite (kept across theme changes).
        static readonly Dictionary<int, Sprite> originalOf = new Dictionary<int, Sprite>();
        // Original values, so switching back to "Qud teal" restores them.
        static readonly Dictionary<int, Color> origColor = new Dictionary<int, Color>();
        static readonly Dictionary<int, Color> mappedColor = new Dictionary<int, Color>();
        static bool busy;

        public static bool Light => Check() && def.Light;

        static float nextTick;

        // Called every frame from always-running UI code: menus are shown/hidden by toggling their
        // canvas, so Image.OnEnable alone never notices an option change.
        public static void Tick()
        {
            if (!Fonts.OnMainThread) return;
            if (Time.unscaledTime < nextTick) return;
            nextTick = Time.unscaledTime + 1f;
            try { Check(); }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Theme.Tick", e); }
        }

        // Re-reads the option; on change re-themes everything on screen.
        static bool Check()
        {
            string choice = Settings.UiTheme;
            if (choice != current)
            {
                current = choice;
                active = Defs.TryGetValue(choice, out def);
                Debug.Log("BrightQud theme option: '" + choice + "' active=" + active);
                textures.Clear();
                sprites.Clear();
                RestyleAll();
            }
            return active;
        }

        // neutrals: also turn dark greys light (sprite pixels only; flat Image colours may be faders).
        public static Color Map(Color c, bool neutrals = false)
        {
            if (!Check()) return c;
            Color.RGBToHSV(c, out float h, out float s, out float v);
            float deg = h * 360f;
            bool teal = s > 0.08f && deg >= 140f && deg <= 215f;
            if (!teal && !(neutrals && def.Light && s <= 0.08f && v < 0.35f)) return c;
            float s2 = Mathf.Clamp01(s * def.Sat + def.SatAdd);
            float v2 = def.Light ? Mathf.Clamp(1.0f - 0.85f * v, 0.15f, 0.93f) : v;
            var o = Color.HSVToRGB(def.Hue / 360f, s2, v2);
            o.a = c.a;
            return o;
        }

        static bool IsChrome(Sprite s)
        {
            if (s == null) return false;
            string n = (s.name + " " + (s.texture != null ? s.texture.name : "")).ToLowerInvariant();
            if (n.Contains("brightqud") || n.Contains("tile") && !n.Contains("paneltile") && !n.Contains("bgtile")) return false;
            return n.Contains("polat") || n.Contains("frame") || n.Contains("border") || n.Contains("panel")
                || n.Contains("bg") || n.Contains("background") || n.Contains("button") || n.Contains("tab")
                || n.Contains("scrollbar") || n.Contains("dialog") || n.Contains("highlight") || n.Contains("corner")
                || n.Contains("dotted") || n.Contains("header") || n.Contains("divider") || n.Contains("window");
        }

        static Texture2D Recolor(Texture2D src)
        {
            if (textures.TryGetValue(src.GetInstanceID(), out var done)) return done;
            Texture2D copy = null;
            var rt = RenderTexture.GetTemporary(src.width, src.height, 0, RenderTextureFormat.ARGB32, RenderTextureReadWrite.sRGB);
            var prev = RenderTexture.active;
            try
            {
                Graphics.Blit(src, rt);
                RenderTexture.active = rt;
                copy = new Texture2D(src.width, src.height, TextureFormat.RGBA32, false, false);
                copy.ReadPixels(new Rect(0, 0, src.width, src.height), 0, 0);
                var px = copy.GetPixels32();
                var memo = new Dictionary<int, Color32>();
                for (int i = 0; i < px.Length; i++)
                {
                    var p = px[i];
                    if (p.a == 0) continue;
                    int key = (p.r << 16) | (p.g << 8) | p.b;
                    if (!memo.TryGetValue(key, out var m))
                    {
                        m = Map(new Color32(p.r, p.g, p.b, 255), true);
                        memo[key] = m;
                    }
                    px[i] = new Color32(m.r, m.g, m.b, p.a);
                }
                copy.SetPixels32(px);
                copy.filterMode = src.filterMode;
                copy.wrapMode = src.wrapMode;
                copy.Apply(false, true);
                copy.name = src.name + " (BrightQud theme)";
            }
            finally
            {
                RenderTexture.active = prev;
                RenderTexture.ReleaseTemporary(rt);
            }
            textures[src.GetInstanceID()] = copy;
            return copy;
        }

        static Sprite Themed(Sprite src)
        {
            if (sprites.TryGetValue(src.GetInstanceID(), out var done)) return done;
            var tex = Recolor(src.texture);
            var r = src.rect;
            var t = Sprite.Create(tex, r, new Vector2(src.pivot.x / r.width, src.pivot.y / r.height), src.pixelsPerUnit, 0,
                SpriteMeshType.FullRect, src.border);
            t.name = src.name;
            sprites[src.GetInstanceID()] = t;
            originalOf[t.GetInstanceID()] = src;
            return t;
        }

        public static void Apply(Image img)
        {
            if (img == null || busy) return;
            Fonts.MarkMainThread();
            bool on = Check();
            busy = true;
            try
            {
                int id = img.GetInstanceID();
                var s = img.sprite;
                // Always theme from the game's own sprite, even when a previous theme's copy is shown.
                var src = s != null && originalOf.TryGetValue(s.GetInstanceID(), out var o) ? o : s;
                // The game changed the colour since we themed it: that is the new original.
                if (mappedColor.TryGetValue(id, out var mc) && img.color != mc) { origColor.Remove(id); mappedColor.Remove(id); }
                if (!on)
                {
                    if (src != s) img.sprite = src;
                    if (origColor.TryGetValue(id, out var oc)) img.color = oc;
                    origColor.Remove(id);
                    mappedColor.Remove(id);
                    return;
                }
                bool chrome = src != null && IsChrome(src);
                if (src == null || chrome)
                {
                    if (!origColor.ContainsKey(id)) origColor[id] = img.color;
                    var c = Map(origColor[id]);
                    mappedColor[id] = c;
                    if (img.color != c) img.color = c;
                }
                if (chrome && src.texture != null)
                {
                    var t = Themed(src);
                    if (s != t) img.sprite = t;
                }
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Theme", e);
            }
            finally
            {
                busy = false;
            }
        }

        // Light theme: dark "ink" text. Every text mesh is recoloured right after TextMeshPro builds
        // it (rich-text colour tags included), keeping each colour's hue.
        static bool hooked;
        static readonly Dictionary<int, Color32> inkMemo = new Dictionary<int, Color32>();

        static Color32 Ink(Color32 c)
        {
            int key = (c.r << 16) | (c.g << 8) | c.b;
            if (!inkMemo.TryGetValue(key, out var o))
            {
                Color.RGBToHSV(c, out float h, out float sat, out float v);
                Color d = sat < 0.2f ? new Color(0.22f, 0.17f, 0.12f)
                    : Color.HSVToRGB(h, Mathf.Max(sat, 0.6f), Mathf.Min(v, 0.45f));
                o = d;
                inkMemo[key] = o;
            }
            o.a = c.a;
            return o;
        }

        static void OnTextChanged(UnityEngine.Object obj)
        {
            try
            {
                if (!(obj is TextMeshProUGUI t) || !active || !def.Light || !Fonts.OnMainThread) return;
                var info = t.textInfo;
                if (info?.meshInfo == null) return;
                bool changed = false;
                for (int m = 0; m < info.meshInfo.Length; m++)
                {
                    var colors = info.meshInfo[m].colors32;
                    if (colors == null) continue;
                    int n = Math.Min(info.meshInfo[m].vertexCount, colors.Length);
                    for (int i = 0; i < n; i++) colors[i] = Ink(colors[i]);
                    changed |= n > 0;
                }
                if (changed) t.UpdateVertexData(TMP_VertexDataUpdateFlags.Colors32);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Theme.Text", e);
            }
        }

        public static void Apply(TMP_Text t)
        {
            if (!Fonts.OnMainThread) return;
            Check();
            if (!hooked)
            {
                hooked = true;
                TMPro_EventManager.TEXT_CHANGED_EVENT.Add(OnTextChanged);
            }
        }

        // One log line per theme change: what the menus are made of (for tuning IsChrome / Map).
        static void Report(Image[] images)
        {
            if (!active) return;
            int chrome = 0, flat = 0;
            var other = new Dictionary<string, int>();
            var colors = new Dictionary<string, int>();
            foreach (var img in images)
            {
                var s = img.sprite;
                if (s != null && originalOf.ContainsKey(s.GetInstanceID())) chrome++;
                else if (s == null) { flat++; string c = ColorUtility.ToHtmlStringRGBA(img.color); colors[c] = colors.TryGetValue(c, out int n) ? n + 1 : 1; }
                else { string k = s.name + "@" + (s.texture != null ? s.texture.name : "?"); other[k] = other.TryGetValue(k, out int n) ? n + 1 : 1; }
            }
            var sb = new System.Text.StringBuilder("BrightQud theme '" + current + "': " + images.Length + " images, "
                + chrome + " recoloured sprites, " + flat + " flat. Other sprites: ");
            foreach (var kv in other) sb.Append(kv.Key).Append(" x").Append(kv.Value).Append("; ");
            sb.Append(" Flat colours: ");
            foreach (var kv in colors) sb.Append(kv.Key).Append(" x").Append(kv.Value).Append("; ");
            Debug.Log(sb.ToString());
        }

        static void RestyleAll()
        {
            try
            {
                var images = UnityEngine.Object.FindObjectsByType<Image>(FindObjectsInactive.Include, FindObjectsSortMode.None);
                foreach (var img in images)
                    Apply(img);
                Report(images);
                foreach (var t in UnityEngine.Object.FindObjectsByType<TextMeshProUGUI>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                {
                    Apply(t);
                    if (t.isActiveAndEnabled) t.ForceMeshUpdate();
                }
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Theme.RestyleAll", e);
            }
        }
    }

    [HarmonyPatch(typeof(Image), "OnEnable", new Type[] { })]
    public static class ImageEnableThemePatch
    {
        static void Postfix(Image __instance) => Theme.Apply(__instance);
    }

    [HarmonyPatch(typeof(Image), "set_sprite", new Type[] { typeof(Sprite) })]
    public static class ImageSpriteThemePatch
    {
        static void Postfix(Image __instance) => Theme.Apply(__instance);
    }
}
