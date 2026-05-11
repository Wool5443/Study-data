#!/usr/bin/env bash
set -e

ARCHIVE="dz2_work.zip"

rm -f "$ARCHIVE"

zip -r "$ARCHIVE" \
  work/data/db.xlsx \
  work/data/*.pick \
  work/scripts/*.py \
  work/scripts/*.ini \
  work/library/*.py \
  work/notes \
  work/output/*.xlsx \
  work/graphics/*.png \
  -x "work/.venv/*" "*/__pycache__/*" "*.pyc" "*.pyo" ".DS_Store"

echo "Created $ARCHIVE"
zipinfo -1 "$ARCHIVE"
