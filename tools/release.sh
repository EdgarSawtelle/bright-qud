#!/usr/bin/env bash
# Build tiles, compile-check the C#, verify every Harmony patch target, then install.
# Nothing is installed unless all checks pass.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MANAGED="$HOME/.local/share/Steam/steamapps/common/Caves of Qud/CoQ_Data/Managed"
export DOTNET_ROOT="$ROOT/.tools/dotnet" DOTNET_CLI_TELEMETRY_OPTOUT=1 DOTNET_NOLOGO=1
DOTNET="$ROOT/.tools/dotnet/dotnet"

"$ROOT/.venv/bin/python" -I "$ROOT/tools/build_mod.py"
(cd "$ROOT/tools/cscheck" && "$DOTNET" build -nologo -v q | grep -E ' error |Error\(s\)' | sort -u)
grep -q ' 0 Error(s)' <(cd "$ROOT/tools/cscheck" && "$DOTNET" build -nologo -v q) || { echo "compile failed"; exit 1; }
(cd "$ROOT/tools/patchlint" && "$DOTNET" run -v q -- "$ROOT/tools/cscheck/bin/Debug/netstandard2.0/check.dll" "$MANAGED")
"$ROOT/tools/sync_mod.sh"
