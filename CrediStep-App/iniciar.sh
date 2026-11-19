#!/usr/bin/env bash
# Arranque de CrediStep en macOS / Linux
set -e
cd "$(dirname "$0")/backend"
PY=$(command -v python3 || command -v python)
[ -d .venv ] || "$PY" -m venv .venv
if [ -f .venv/bin/python ]; then VPY=.venv/bin/python; else VPY=.venv/Scripts/python; fi
"$VPY" -m pip install -q --disable-pip-version-check -r requirements.txt
echo "CrediStep corriendo en http://localhost:8000  (demo@credistep.co / CrediStep2026)"
"$VPY" -m uvicorn app.main:app --host 127.0.0.1 --port 8000
