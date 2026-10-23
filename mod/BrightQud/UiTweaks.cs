// Bright Qud UI tweaks (each one has its own switch in Options → Mods):
//   1. Font: swaps the game's UI text font for a clearer one shipped in Fonts/ (SIL OFL fonts).
//   2. Ability bar: narrower buttons, so more abilities fit without paging.
//   3. Ability help: a small panel above the ability bar explains the ability under the pointer or
//      the one just selected with the controller.

using System;
using System.Collections;
using System.Collections.Generic;
using System.Reflection.Emit;
using System.Runtime.CompilerServices;
using HarmonyLib;
using Qud.UI;
using TMPro;
using UnityEngine;
using UnityEngine.EventSystems;
using UnityEngine.TextCore.LowLevel;
using UnityEngine.UI;
using XRL;
using XRL.UI;
using XRL.World.Parts;

namespace BrightQud
{
    public static class Fonts
    {
        static string loaded = "";
        static TMP_FontAsset asset;
        static readonly ConditionalWeakTable<TMP_Text, TMP_FontAsset> originals = new ConditionalWeakTable<TMP_Text, TMP_FontAsset>();
        static readonly HashSet<string> seen = new HashSet<string>();

        static readonly string Prefill = BuildPrefill();

        static string BuildPrefill()
        {
            var sb = new System.Text.StringBuilder();
            for (char c = (char)32; c < 127; c++) sb.Append(c);
            for (char c = (char)160; c < 384; c++) sb.Append(c);
            sb.Append("–—‘’“”•…←↑→↓↔·×÷°±²³");
            return sb.ToString();
        }

        static string FileFor(string choice) =>
            choice.EqualsNoCase("Clear mono") ? "IBMPlexMono-Medium.ttf"
            : choice.EqualsNoCase("Readable") ? "AtkinsonHyperlegible-Regular.ttf" : null;

        // The font to use now, or null for the game's own.
        static int mainThread = -1;

        // Called from code that always runs on Unity's main thread.
        public static void MarkMainThread() => mainThread = System.Threading.Thread.CurrentThread.ManagedThreadId;

        public static bool OnMainThread => mainThread == System.Threading.Thread.CurrentThread.ManagedThreadId;

        public static TMP_FontAsset Current
        {
            get
            {
                // Building the atlas off the main thread corrupts glyphs; wait for a main-thread call.
                if (!OnMainThread) return loaded == Settings.Font ? asset : null;
                string choice = Settings.Font;
                if (choice != loaded)
                {
                    loaded = choice;
                    asset = null;
                    string file = FileFor(choice);
                    if (file != null)
                    {
                        try
                        {
                            string path = System.IO.Path.Combine(ModManager.GetMod("BrightQud").Path, "Fonts", file);
                            // One big atlas filled up front: glyphs added later to a second atlas
                            // rendered with a different weight (mixed-looking letters).
                            asset = TMP_FontAsset.CreateFontAsset(path, 0, 72, 9, GlyphRenderMode.SDFAA, 2048, 2048);
                            if (asset != null)
                            {
                                asset.name = "BrightQud " + choice;
                                asset.isMultiAtlasTexturesEnabled = false;
                                asset.TryAddCharacters(Prefill, out string missing);
                                Debug.Log("BrightQud font '" + choice + "': " + asset.characterLookupTable.Count
                                    + " characters, " + asset.atlasTextureCount + " atlas, missing [" + missing + "]");
                            }
                            else MetricsManager.LogError("BrightQud.Fonts: could not load " + path);
                        }
                        catch (Exception e)
                        {
                            MetricsManager.LogException("BrightQud.Fonts", e);
                        }
                    }
                    RestyleAll();
                }
                return asset;
            }
        }

        // Icon fonts (controller buttons, keyboard glyphs) are left alone.
        static bool IsIconFont(TMP_FontAsset f)
        {
            string n = f?.name ?? "";
            return n.Contains("Xbox") || n.Contains("PS5") || n.Contains("PS4") || n.Contains("Switch") || n.Contains("PC-")
                || n.Contains("Glyph") || n.Contains("Icon") || n.Contains("Keyboard");
        }

        public static void Apply(TMP_Text t)
        {
            if (t == null || !OnMainThread) return;
            var font = Current;
            if (font == null)
            {
                if (originals.TryGetValue(t, out var orig) && orig != null && t.font != orig) t.font = orig;
                return;
            }
            if (t.font == font) return;
            if (originals.TryGetValue(t, out _) == false)
            {
                if (IsIconFont(t.font)) return;
                if (t.font != null && seen.Add(t.font.name)) Debug.Log("BrightQud: replacing UI font " + t.font.name);
                originals.Add(t, t.font);
                // Glyphs our font lacks (box drawing, symbols) still come from the game's font.
                if (font.fallbackFontAssetTable == null) font.fallbackFontAssetTable = new List<TMP_FontAsset>();
                if (t.font != null && !font.fallbackFontAssetTable.Contains(t.font)) font.fallbackFontAssetTable.Add(t.font);
            }
            t.font = font;
        }

        static void RestyleAll()
        {
            try
            {
                foreach (var t in UnityEngine.Object.FindObjectsByType<TextMeshProUGUI>(FindObjectsInactive.Include, FindObjectsSortMode.None))
                    Apply(t);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.Fonts.RestyleAll", e);
            }
        }
    }

    [HarmonyPatch(typeof(UITextSkin), nameof(UITextSkin.Apply), new Type[] { })]
    public static class UITextSkinFontPatch
    {
        static void Postfix(UITextSkin __instance)
        {
            try { Theme.Tick(); var t = __instance.GetComponent<TextMeshProUGUI>(); Fonts.Apply(t); Theme.Apply(t); }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Fonts.Apply", e); }
        }
    }

    [HarmonyPatch(typeof(TextMeshProUGUI), "OnEnable", new Type[] { })]
    public static class TmpEnableFontPatch
    {
        static void Postfix(TextMeshProUGUI __instance)
        {
            try { Fonts.MarkMainThread(); Fonts.Apply(__instance); Theme.Apply(__instance); }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Fonts.OnEnable", e); }
        }
    }

    // ---------------- ability bar ----------------

    [HarmonyPatch(typeof(AbilityBar), nameof(AbilityBar.Update), new Type[] { })]
    public static class AbilityBarPatch
    {
        const int GameWidth = 175;

        // Button width in "Full" ability bar mode (the game divides the bar width by this).
        public static int Width()
        {
            string mode = Settings.AbilityBar;
            return mode.EqualsNoCase("Most") ? 104 : mode.EqualsNoCase("More") ? 128 : GameWidth;
        }

        static IEnumerable<CodeInstruction> Transpiler(IEnumerable<CodeInstruction> instructions)
        {
            var width = AccessTools.Method(typeof(AbilityBarPatch), nameof(Width));
            foreach (var ins in instructions)
            {
                if ((ins.opcode == OpCodes.Ldc_I4 || ins.opcode == OpCodes.Ldc_I4_S) && Convert.ToInt32(ins.operand) == GameWidth)
                {
                    var call = new CodeInstruction(OpCodes.Call, width);
                    call.labels.AddRange(ins.labels);
                    call.blocks.AddRange(ins.blocks);
                    yield return call;
                }
                else yield return ins;
            }
        }

        static int lastWidth = GameWidth;

        static void Postfix(AbilityBar __instance)
        {
            try
            {
                Fonts.MarkMainThread();
                Theme.Tick();
                if (__instance.ButtonArea == null) return;
                int w = Options.AbilityBarMode == 1 ? -1 : Width();
                if (w > 0 && (w != GameWidth || lastWidth != GameWidth)) Resize(__instance.ButtonArea, w);
                lastWidth = w > 0 ? w : GameWidth;
                AbilityHelp.Update(__instance);
                QuestBanner.Update(__instance.ButtonArea.GetComponentInChildren<AbilityBarButton>(true)?.Text?.font);
            }
            catch (Exception e)
            {
                MetricsManager.LogException("BrightQud.AbilityBar", e);
            }
        }

        static void Resize(RectTransform area, int w)
        {
            var grid = area.GetComponent<GridLayoutGroup>();
            if (grid != null && grid.cellSize.x != w) grid.cellSize = new Vector2(w, grid.cellSize.y);
            foreach (Transform child in area)
            {
                var button = child.GetComponent<AbilityBarButton>();
                if (button == null) continue;
                var le = child.GetComponent<LayoutElement>() ?? child.gameObject.AddComponent<LayoutElement>();
                if (le.preferredWidth != w)
                {
                    le.preferredWidth = w;
                    le.minWidth = w;
                    le.flexibleWidth = 0;
                    var rt = (RectTransform)child;
                    rt.sizeDelta = new Vector2(w, rt.sizeDelta.y);
                    if (button.Text != null)
                    {
                        if (!button.Text.enableAutoSizing) button.Text.fontSizeMax = button.Text.fontSize;
                        button.Text.enableAutoSizing = w != GameWidth;
                        button.Text.fontSizeMin = 9;
                    }
                }
                AbilityHelp.Hook(button);
            }
        }
    }

    [HarmonyPatch(typeof(AbilityBar), nameof(AbilityBar.MoveSelection), new Type[] { typeof(int) })]
    public static class AbilitySelectionPatch
    {
        static void Postfix(AbilityBar __instance)
        {
            try { AbilityHelp.ShowSelected(__instance); }
            catch (Exception e) { MetricsManager.LogException("BrightQud.AbilityHelp", e); }
        }
    }

    public static class AbilityHelp
    {
        static GameObject panel;
        static TextMeshProUGUI text;
        static string hovered;            // command of the button under the pointer
        static string shown;              // command currently in the panel
        static float showUntil;
        static long shownTurn;
        static int shownFrame;
        static readonly HashSet<int> hooked = new HashSet<int>();

        public static void Hook(AbilityBarButton button)
        {
            if (!hooked.Add(button.GetInstanceID())) return;
            var trigger = button.gameObject.GetComponent<EventTrigger>() ?? button.gameObject.AddComponent<EventTrigger>();
            var enter = new EventTrigger.Entry { eventID = EventTriggerType.PointerEnter };
            enter.callback.AddListener(_ => { hovered = button.command; shown = null; });
            var exit = new EventTrigger.Entry { eventID = EventTriggerType.PointerExit };
            exit.callback.AddListener(_ => { if (hovered == button.command) hovered = null; });
            trigger.triggers.Add(enter);
            trigger.triggers.Add(exit);
        }

        public static void ShowSelected(AbilityBar bar)
        {
            var entry = bar.currentlySelectedAbility;
            if (entry == null || !Settings.AbilityHelp) return;
            Show(bar, entry);
        }

        static ActivatedAbilityEntry Find(AbilityBar bar, string command)
        {
            if (command == null) return null;
            if (Traverse.Create(bar).Field("abilities").GetValue() is IList list)
                foreach (var d in list)
                {
                    var e = Traverse.Create(d).Field("Entry").GetValue<ActivatedAbilityEntry>();
                    if (e?.Command == command) return e;
                }
            return null;
        }

        // The panel closes after a few seconds, when a turn passes (moving, using an ability), or on
        // any other key or click; pointing at a button again shows it again.
        public static void Update(AbilityBar bar)
        {
            bool onStage = GameManager.Instance?.CurrentGameView == "Stage";
            if (!Settings.AbilityHelp || !onStage)
            {
                hovered = null;
                Hide();
                return;
            }
            if (hovered != null && hovered != shown) Show(bar, Find(bar, hovered));
            if (shown == null) return;
            bool input = false;
            if (Time.frameCount > shownFrame + 1)
                try { input = Input.anyKeyDown || Input.GetMouseButtonDown(0) || Input.GetMouseButtonDown(1); }
                catch (InvalidOperationException) { }
            if (input || The.CurrentTurn != shownTurn || Time.unscaledTime > showUntil)
            {
                hovered = null;
                Hide();
            }
        }

        static void Hide()
        {
            if (panel != null && panel.activeSelf) panel.SetActive(false);
            shown = null;
        }

        static void Build(AbilityBar bar)
        {
            panel = new GameObject("BrightQudAbilityHelp", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            panel.GetComponent<LayoutElement>().ignoreLayout = true;
            panel.transform.SetParent(bar.ButtonArea.parent, false);
            var bg = panel.GetComponent<Image>();
            bg.color = new Color(0.03f, 0.11f, 0.12f, 0.94f);
            bg.raycastTarget = false;
            var go = new GameObject("Text", typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(panel.transform, false);
            text = go.GetComponent<TextMeshProUGUI>();
            text.raycastTarget = false;
            text.richText = true;
            text.fontSize = 16;
            text.color = new Color(0.69f, 0.78f, 0.76f);
            text.textWrappingMode = TextWrappingModes.Normal;
            var sample = bar.ButtonArea.GetComponentInChildren<AbilityBarButton>(true)?.Text;
            if (sample != null) text.font = sample.font;
            var trt = (RectTransform)go.transform;
            trt.anchorMin = Vector2.zero;
            trt.anchorMax = Vector2.one;
            trt.offsetMin = new Vector2(10, 6);
            trt.offsetMax = new Vector2(-10, -6);
        }

        static void Show(AbilityBar bar, ActivatedAbilityEntry entry)
        {
            if (entry == null) { Hide(); return; }
            if (panel == null) Build(bar);
            Fonts.Apply(text);
            var sb = new System.Text.StringBuilder();
            sb.Append("{{W|").Append(entry.DisplayName).Append("}}");
            if (!entry.Class.IsNullOrEmpty()) sb.Append("  {{K|").Append(entry.Class).Append("}}");
            if (entry.Toggleable) sb.Append(entry.ToggleState ? "  {{g|[on]}}" : "  {{y|[off]}}");
            if (entry.Cooldown > 0) sb.Append("  {{C|ready in ").Append(entry.CooldownDescription).Append("}}");
            if (!entry.Enabled) sb.Append("  {{K|[disabled]}}");
            string desc = entry.Description;
            sb.Append('\n').Append(desc.IsNullOrEmpty() ? "{{K|No description. Open the abilities screen for details.}}" : desc);
            text.text = RTF.FormatToRTF(sb.ToString());
            shown = entry.Command;
            shownTurn = The.CurrentTurn;
            shownFrame = Time.frameCount;
            showUntil = Time.unscaledTime + 6f;

            // Sit just above the ability buttons, as wide as the bar.
            var rt = (RectTransform)panel.transform;
            var area = bar.ButtonArea;
            var corners = new Vector3[4];
            area.GetWorldCorners(corners);
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0, 0);
            float scale = Mathf.Max(0.0001f, rt.lossyScale.x);
            float width = Mathf.Min(720f, (corners[2].x - corners[1].x) / scale);
            float height = text.GetPreferredValues(text.text, width - 20, 0).y + 14;
            rt.sizeDelta = new Vector2(width, height);
            rt.position = corners[1] + new Vector3(0, 6 * scale, 0);
            panel.transform.SetAsLastSibling();
            if (!panel.activeSelf) panel.SetActive(true);
        }
    }
}
