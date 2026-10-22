#!/usr/bin/env bash
set -euo pipefail
BASE="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
exec /usr/bin/python3 "$BASE/gui.py" --operation apply "$@"
