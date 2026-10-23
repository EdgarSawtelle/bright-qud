#!/usr/bin/env bash
# Copy the built mod into the game's Mods folder (the only script that writes there).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
DEST="$HOME/.config/unity3d/Freehold Games/CavesOfQud/Mods/BrightQud"
[ -d "$(dirname "$DEST")" ] || { echo "Mods folder not found: $(dirname "$DEST")"; exit 1; }
mkdir -p "$DEST"
rsync -a --delete "$ROOT/mod/BrightQud/" "$DEST/"
echo "synced to $DEST ($(find "$DEST" -type f | wc -l) files)"
