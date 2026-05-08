#!/bin/zsh

cd "$(dirname "$0")" || exit 1

if [ ! -d ".venv" ]; then
    python3 -m venv .venv
fi

source .venv/bin/activate

pip install -r requirements.txt

mkdir -p /private/tmp/codex_mpl
export MPLCONFIGDIR=/private/tmp/codex_mpl

python drowsiness_detection.py
