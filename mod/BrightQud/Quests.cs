// Quest helper (Options → Mods → "quest banner"):
//   - "Quests" list (LT + left stick click, F4, or the Controls reminder): every active quest with its
//     current step and roughly where it is, nearest first. Pick one to follow it.
//   - Banner: a short yellow line under the top status bar with the followed quest's next step and
//     direction, e.g. "> Travel to Grit Gate - 3 regions NE".
// Where a step happens, in this order (never guessed):
//   1. village "find a site" quests: the zone the game stored for that step;
//   2. a revealed map note whose name appears in the step (e.g. "Grit Gate" in "Travel to Grit Gate");
//   3. "Return ..." steps (and quests ready to turn in): the quest giver's zone.
// Nothing goes into the save: the followed quest is remembered in a small file next to the game's
// local data (one "game id <tab> quest id" line per game).

using System;
using System.Collections.Generic;
using System.IO;
using System.Linq;
using HarmonyLib;
using Qud.API;
using Qud.UI;
using TMPro;
using UnityEngine;
using UnityEngine.UI;
using XRL;
using XRL.Core;
using XRL.World;
using GameObject = UnityEngine.GameObject;
using XRL.World.ZoneBuilders;
using QudColor = ConsoleLib.Console.ColorUtility;

namespace BrightQud
{
    public static class Quests
    {
        public const string Command = "CmdBrightQudQuests";
        const int CompleteNoticeTurns = 30;

        struct Info
        {
            public Quest Quest;
            public string Step;     // what to do next
            public string Where;    // "3 regions NE", "here", "location unknown"
            public int Distance;    // in zones; int.MaxValue = unknown
        }

        // ---- the followed quest, per game, outside the save ----
        static string loadedGame, followed;
        static string completeName;
        static long completeTurn;

        static string FilePath => DataManager.LocalPath("BrightQud/mainquest.txt");

        static Dictionary<string, string> ReadAll()
        {
            var map = new Dictionary<string, string>();
            try
            {
                if (File.Exists(FilePath))
                    foreach (string line in File.ReadAllLines(FilePath))
                    {
                        int tab = line.IndexOf('\t');
                        if (tab > 0) map[line.Substring(0, tab)] = line.Substring(tab + 1);
                    }
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Quests.Read", e); }
            return map;
        }

        static string Followed()
        {
            string game = The.Game?.GameID;
            if (game == null) return null;
            if (game != loadedGame)
            {
                loadedGame = game;
                completeName = null;
                ReadAll().TryGetValue(game, out followed);
            }
            return followed;
        }

        static void SetFollowed(string questId)
        {
            string game = The.Game?.GameID;
            if (game == null) return;
            loadedGame = game;
            followed = questId;
            completeName = null;
            try
            {
                var map = ReadAll();
                if (questId == null) map.Remove(game); else map[game] = questId;
                Directory.CreateDirectory(Path.GetDirectoryName(FilePath));
                File.WriteAllLines(FilePath, map.Select(kv => kv.Key + "\t" + kv.Value));
            }
            catch (Exception e) { MetricsManager.LogException("BrightQud.Quests.Write", e); }
        }

        // ---- where things are ----
        // Global zone coordinates: 3x3 zones per world-map cell (parasang); Z 10 = surface.
        static bool Coords(string zoneId, out int x, out int y, out int z)
        {
            x = y = z = 0;
            if (zoneId.IsNullOrEmpty() || !ZoneID.Parse(zoneId, out int px, out int py, out int zx, out int zy, out int zz))
                return false;
            x = px * 3 + zx;
            y = py * 3 + zy;
            z = zz;
            return true;
        }

        static bool PlayerCoords(out int x, out int y, out int z)
        {
            x = y = z = 0;
            var player = The.Player;
            var zone = player?.CurrentZone;
            if (zone == null) return false;
            if (zone.IsWorldMap())
            {
                var cell = player.CurrentCell;
                x = cell.X * 3 + 1;
                y = cell.Y * 3 + 1;
                z = 10;
                return true;
            }
            return Coords(zone.ZoneID, out x, out y, out z);
        }

        static string Compass(int dx, int dy)
        {
            double a = Math.Atan2(-dy, dx) * 180 / Math.PI;     // 0 = east, 90 = north
            string[] dirs = { "E", "NE", "N", "NW", "W", "SW", "S", "SE" };
            return dirs[(int)Math.Round(((a + 360) % 360) / 45) % 8];
        }

        static string Describe(string zoneId, out int distance)
        {
            distance = int.MaxValue;
            if (!Coords(zoneId, out int tx, out int ty, out int tz) || !PlayerCoords(out int px, out int py, out int pz))
                return "{{K|location unknown}}";
            int dx = tx - px, dy = ty - py;
            distance = Math.Max(Math.Abs(dx), Math.Abs(dy));
            string where;
            if (distance == 0) where = "here";
            else if (distance < 3) where = "close, " + Compass(dx, dy);
            else
            {
                int regions = (distance + 1) / 3;
                where = regions + (regions == 1 ? " region " : " regions ") + Compass(dx, dy);
            }
            int depth = tz - pz;
            if (depth != 0 && (tz > 10 || pz > 10))
                where += ", " + Math.Abs(depth) + (Math.Abs(depth) == 1 ? " level " : " levels ") + (depth > 0 ? "down" : "up");
            return where;
        }

        static string Plain(string s) => QudColor.StripFormatting(s ?? "").Trim();

        static QuestStep CurrentStep(Quest q)
        {
            if (q.StepsByID == null) return null;
            return q.StepsByID.Values
                .Where(s => s != null && !s.Finished && !s.Failed && !s.Hidden && !s.Optional)
                .OrderBy(s => s.Ordinal)
                .FirstOrDefault();
        }

        static string SiteZone(Quest q, QuestStep step)
        {
            var sys = The.Game.GetSystem<FindASiteDynamicQuestManager.FindASiteDynamicQuestManagerSystem>();
            if (sys?.quests == null) return null;
            foreach (var e in sys.quests)
                if (e != null && e.questID == q.ID && (step == null || e.questStepID == step.ID)) return e.zoneID;
            return null;
        }

        static string NoteZone(string text)
        {
            if (text.IsNullOrEmpty()) return null;
            string hay = " " + text.ToLowerInvariant() + " ";
            JournalMapNote best = null;
            int bestLen = 0;
            foreach (var note in JournalAPI.MapNotes)
            {
                if (note == null || !note.Revealed) continue;
                string name = Plain(note.Text).ToLowerInvariant();
                if (name.StartsWith("the ")) name = name.Substring(4);
                if (name.Length < 4 || name.Length <= bestLen) continue;
                int i = hay.IndexOf(name, StringComparison.Ordinal);
                if (i > 0 && !char.IsLetter(hay[i - 1]) && !char.IsLetter(hay[i + name.Length]))
                {
                    best = note;
                    bestLen = name.Length;
                }
            }
            return best?.ZoneID;
        }

        static Info Analyse(Quest q)
        {
            var info = new Info { Quest = q, Distance = int.MaxValue };
            var step = CurrentStep(q);
            string zone = null;
            if (step != null)
            {
                info.Step = Plain(step.Name);
                zone = SiteZone(q, step)
                    ?? NoteZone(Plain(step.Name) + " " + Plain(step.Text))
                    ?? (info.Step.StartsWith("Return", StringComparison.OrdinalIgnoreCase) ? q.QuestGiverLocationZoneID : null);
            }
            else
            {
                info.Step = q.QuestGiverName.IsNullOrEmpty() ? "Turn it in" : "Return to " + Plain(q.QuestGiverName);
                zone = q.QuestGiverLocationZoneID;
            }
            info.Where = zone != null ? Describe(zone, out info.Distance) : "{{K|location unknown}}";
            return info;
        }

        static List<Info> All()
        {
            var list = new List<Info>();
            if (The.Game?.Quests == null) return list;
            foreach (var kv in The.Game.Quests)
                if (kv.Value != null && !kv.Value.Finished && !The.Game.HasFinishedQuest(kv.Key))
                    list.Add(Analyse(kv.Value));
            string f = Followed();
            return list.OrderBy(i => i.Quest.ID == f ? 0 : 1).ThenBy(i => i.Distance).ThenBy(i => Plain(i.Quest.Name)).ToList();
        }

        // ---- banner text (game thread, every player turn) ----
        public static volatile string Banner;

        public static void Refresh()
        {
            if (!Settings.QuestBanner || The.Game == null) { Banner = null; return; }
            string f = Followed();
            if (f == null)
            {
                Banner = completeName != null && The.Game.Turns - completeTurn < CompleteNoticeTurns
                    ? "{{G|Main quest complete: " + completeName + ". Pick another one in Quests (LT + L3 / F4).}}" : null;
                return;
            }
            if (The.Game.Quests.TryGetValue(f, out var q) && q != null && !q.Finished && !The.Game.HasFinishedQuest(f))
            {
                var info = Analyse(q);
                Banner = "{{W|> " + info.Step + "}} {{K|-}} {{Y|" + info.Where + "}}";
                return;
            }
            // Not active (e.g. an older save of this game): no banner, but keep it.
            if (!The.Game.HasFinishedQuest(f)) { Banner = null; return; }
            // Finished: one notice, then forget it.
            string name = The.Game.FinishedQuests.TryGetValue(f, out var fq) ? Plain(fq?.Name) : null;
            SetFollowed(null);
            completeName = name ?? "done";
            completeTurn = The.Game.Turns;
            Refresh();
        }

        // ---- the list (game thread) ----
        public static void ShowFromGame()
        {
            var quests = All();
            if (quests.Count == 0)
            {
                XRL.UI.Popup.Show("You have no active quests. Talk to people (speech bubbles) to find some.");
                return;
            }
            string f = Followed();
            var lines = quests.Select(i => (i.Quest.ID == f ? "{{W|*}} " : "  ") + "{{W|" + Plain(i.Quest.Name) + "}}\n    "
                + i.Step + " {{K|-}} " + i.Where).ToList();
            int pick = XRL.UI.Popup.PickOption("Quests", "Nearest first. Pick one to follow it: the banner under the "
                + "status bar then shows its next step.", "", "Sounds/UI/ui_notification", lines, null, null, null, null,
                null, null, 0, 78, 0, -1, AllowEscape: true, RespectOptionNewlines: true);
            if (pick < 0 || pick >= quests.Count) return;
            var chosen = quests[pick].Quest;
            bool following = chosen.ID == f;
            var actions = new List<string> { following ? "Stop following" : "Follow this quest", "Show in journal", "Back" };
            int act = XRL.UI.Popup.PickOption(Plain(chosen.Name), null, "", "Sounds/UI/ui_notification", actions,
                AllowEscape: true);
            if (act == 0)
            {
                SetFollowed(following ? null : chosen.ID);
                Refresh();
            }
            else if (act == 1) ConsoleLib.Console.Keyboard.PushMouseEvent("Command:CmdQuests");
        }
    }

    [HarmonyPatch(typeof(PlayerStatusBar), "BeginEndTurn", new Type[] { typeof(XRLCore) })]
    public static class QuestBannerTurnPatch
    {
        static void Postfix()
        {
            try { Quests.Refresh(); }
            catch (Exception e)
            {
                Quests.Banner = null;
                MetricsManager.LogException("BrightQud.Quests", e);
            }
        }
    }

    // Drawn from AbilityBarPatch (UI thread, every frame): a strip just under the top status bar.
    public static class QuestBanner
    {
        static GameObject panel;
        static TextMeshProUGUI text;
        static PlayerStatusBar bar;
        static string shown;

        public static void Update(TMP_FontAsset font)
        {
            string banner = Quests.Banner;
            bool onStage = GameManager.Instance?.CurrentGameView == "Stage";
            if (banner == null || !onStage)
            {
                if (panel != null && panel.activeSelf) panel.SetActive(false);
                return;
            }
            if (bar == null) bar = UnityEngine.Object.FindObjectOfType<PlayerStatusBar>();
            if (bar == null) return;
            if (panel == null) Build(font);
            Fonts.Apply(text);
            if (banner != shown)
            {
                text.text = RTF.FormatToRTF(banner);
                shown = banner;
            }
            var rt = (RectTransform)panel.transform;
            var corners = new Vector3[4];
            ((RectTransform)bar.transform).GetWorldCorners(corners);
            float scale = Mathf.Max(0.0001f, rt.lossyScale.x);
            float width = Mathf.Min(text.GetPreferredValues(text.text, 2000, 0).x + 20, (corners[2].x - corners[0].x) / scale * 0.7f);
            rt.anchorMin = rt.anchorMax = new Vector2(0.5f, 0.5f);
            rt.pivot = new Vector2(0, 1);
            rt.sizeDelta = new Vector2(width, 26);
            rt.position = corners[0] + new Vector3(8 * scale, -4 * scale, 0);
            panel.transform.SetAsLastSibling();
            if (!panel.activeSelf) panel.SetActive(true);
        }

        static void Build(TMP_FontAsset font)
        {
            panel = new GameObject("BrightQudQuestBanner", typeof(RectTransform), typeof(Image), typeof(LayoutElement));
            panel.GetComponent<LayoutElement>().ignoreLayout = true;
            panel.transform.SetParent(bar.transform.parent, false);
            var bg = panel.GetComponent<Image>();
            bg.color = new Color(0.03f, 0.11f, 0.12f, 0.88f);
            bg.raycastTarget = false;
            var go = new GameObject("Text", typeof(RectTransform), typeof(TextMeshProUGUI));
            go.transform.SetParent(panel.transform, false);
            text = go.GetComponent<TextMeshProUGUI>();
            text.raycastTarget = false;
            text.richText = true;
            text.fontSize = 17;
            text.color = new Color(0.69f, 0.78f, 0.76f);
            text.textWrappingMode = TextWrappingModes.NoWrap;
            text.overflowMode = TextOverflowModes.Ellipsis;
            text.alignment = TextAlignmentOptions.MidlineLeft;
            if (font != null) text.font = font;
            var trt = (RectTransform)go.transform;
            trt.anchorMin = Vector2.zero;
            trt.anchorMax = Vector2.one;
            trt.offsetMin = new Vector2(10, 2);
            trt.offsetMax = new Vector2(-10, -2);
        }
    }
}
