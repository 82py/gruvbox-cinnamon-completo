#!/usr/bin/env bash
set -euo pipefail
SCRIPT_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
if [[ -f "$SCRIPT_DIR/.gruvbox-theme-package" && -f "$SCRIPT_DIR/scripts/folder_colors.py" ]]; then
    ENGINE="$SCRIPT_DIR/scripts/folder_colors.py"
else
    ENGINE="$HOME/.local/share/gruvbox-cinnamon/folder_colors.py"
fi
exec /usr/bin/python3 "$ENGINE" "$@"
