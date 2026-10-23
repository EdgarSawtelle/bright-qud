// UI colour themes (Options → Mods → "interface colours").
//
// The game's menus are teal: frame/background sprites (polat-frame*, panelBgTile, ...) and flat
// teal Image colours. A theme remaps every teal-ish colour (hue 140-215°) to its own hue; the light
// "Tan parchment" theme also flips brightness (dark panels become light) and darkens all text through
// the text materials' face colour so it stays readable. Item/creature icons are not teal UI art and
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
        static readonly HashSet<int> ours = new HashSet<int>();
        // Original values, so switching back to "Qud teal" restores them.
        static readonly Dictionary<int, Sprite> origSprite = new Dictionary<int, Sprite>();
        static readonly Dictionary<int, Color> origColor = new Dictionary<int, Color>();
        static readonly Dictionary<int, Color> mappedColor = new Dictionary<int, Color>();
        static readonly Dictionary<Material, Color> origFace = new Dictionary<Material, Color>();
        static bool busy;

        public static bool Light => Check() && def.Light;

        // Re-reads the option; on change re-themes everything on screen.
        static bool Check()
        {
            string choice = Settings.UiTheme;
            if (choice != current)
            {
                current = choice;
                active = Defs.TryGetValue(choice, out def);
                textures.Clear();
                sprites.Clear();
                ours.Clear();
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

        static Sprite Themed(Sprite s)
        {
            if (sprites.TryGetValue(s.GetInstanceID(), out var done)) return done;
            var tex = Recolor(s.texture);
            var r = s.rect;
            var t = Sprite.Create(tex, r, new Vector2(s.pivot.x / r.width, s.pivot.y / r.height), s.pixelsPerUnit, 0,
                SpriteMeshType.FullRect, s.border);
            t.name = s.name;
            sprites[s.GetInstanceID()] = t;
            ours.Add(t.GetInstanceID());
            return t;
        }

        public static void Apply(Image img)
        {
            if (img == null || busy) return;
            bool on = Check();
            busy = true;
            try
            {
                int id = img.GetInstanceID();
                var s = img.sprite;
                bool oursNow = s != null && ours.Contains(s.GetInstanceID());
                // The game changed the colour since we themed it: that is the new original.
                if (mappedColor.TryGetValue(id, out var mc) && img.color != mc) { origColor.Remove(id); mappedColor.Remove(id); }
                if (!oursNow) origSprite.Remove(id);
                if (!on)
                {
                    if (oursNow && origSprite.TryGetValue(id, out var os)) img.sprite = os;
                    if (origColor.TryGetValue(id, out var oc)) img.color = oc;
                    origSprite.Remove(id);
                    origColor.Remove(id);
                    mappedColor.Remove(id);
                    return;
                }
                if (s == null || IsChrome(s) || oursNow)
                {
                    if (!origColor.ContainsKey(id)) origColor[id] = img.color;
                    var c = Map(origColor[id]);
                    mappedColor[id] = c;
                    if (img.color != c) img.color = c;
                }
                if (s != null && !oursNow && IsChrome(s) && s.texture != null)
                {
                    img.sprite = Themed(s);
                    origSprite[id] = s;
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

        // Light theme: dark text (vertex colours are multiplied by the material's face colour).
        public static void Apply(TMP_Text t)
        {
            var mat = t?.fontSharedMaterial;
            if (mat == null || !mat.HasProperty(ShaderUtilities.ID_FaceColor)) return;
            bool light = Light;
            if (light && !origFace.ContainsKey(mat))
            {
                origFace[mat] = mat.GetColor(ShaderUtilities.ID_FaceColor);
                mat.SetColor(ShaderUtilities.ID_FaceColor, new Color(0.22f, 0.17f, 0.12f, 1f));
            }
            else if (!light && origFace.TryGetValue(mat, out var face))
            {
                mat.SetColor(ShaderUtilities.ID_FaceColor, face);
                origFace.Remove(mat);
            }
        }

        static void RestyleAll()
        {
            try
            {
                foreach (var img in UnityEngine.Object.FindObjectsByType<Image>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                    Apply(img);
                foreach (var t in UnityEngine.Object.FindObjectsByType<TextMeshProUGUI>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                    Apply(t);
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

    [HarmonyPatch(typeof(Image), nameof(Image.sprite), MethodType.Setter)]
    public static class ImageSpriteThemePatch
    {
        static void Postfix(Image __instance) => Theme.Apply(__instance);
    }
}
