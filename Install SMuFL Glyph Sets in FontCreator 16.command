#!/bin/bash
# © 2026 Nor Eddine Bahha — NorFonts | https://norfont.com
# Installs only missing Glyph Set files in the current user's FontCreator 16 folder.
# Never modifies app bundles, fonts, or existing .glyphset files.
cd "$(dirname "$0")" || exit 1
printf '\n==============================================================\n'
printf ' SMuFL Glyph Sets for FontCreator 16 — NorFonts\n'
printf ' Copyright © 2026 Nor Eddine Bahha — https://norfont.com\n'
printf ' ADD ONLY • NO OVERWRITES • NO DELETIONS • NO BACKUPS\n'
printf '==============================================================\n'
printf ' Destination: ~/Library/High-Logic/FontCreator/16.0/GlyphSets/\n'
printf ' Quit FontCreator before installing.\n\n'
if ! command -v python3 >/dev/null 2>&1; then
    printf 'ERROR: Python 3.9 or newer is required.\n'
    read -r -p 'Press Return to close...' _
    exit 1
fi
python3 -B -c 'import sys; sys.exit(0 if sys.version_info >= (3,9) else 1)'
if [ "$?" -ne 0 ]; then
    printf 'ERROR: Python 3.9 or newer is required.\n'
    read -r -p 'Press Return to close...' _
    exit 1
fi
printf ' 1: PREVIEW changes (read-only)\n'
printf ' 2: ADD ONE: Accidentals only\n'
printf ' 3: ADD ALL: all 23 groups; existing files are skipped\n'
printf ' Anything else: cancel\n\n'
read -r -p 'Choice: ' choice
case "$choice" in
  1) args=--preview ;;
  2) args=--add-one ;;
  3) args=--add-all ;;
  *) printf 'Cancelled. No changes.\n'; read -r -p 'Press Return to close...' _; exit 0 ;;
esac
printf '\n'
python3 -B './smufl_fontcreator16.py' "$args"
status=$?
if [ "$status" -eq 0 ]; then
    printf '\nFinished. Restart FontCreator 16 to see the Glyph Sets.\n'
else
    printf '\nERROR: Existing glyphsets were not intentionally modified.\n'
fi
read -r -p 'Press Return to close...' _
exit "$status"
