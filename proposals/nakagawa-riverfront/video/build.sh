#!/usr/bin/env bash
# Build the 15s teaser: Blender frames + motion typography + BGM -> mp4
# Usage: ./build.sh <work_dir>   (needs: blender, xvfb-run, ffmpeg, python3)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="${1:-$HERE/work}"; mkdir -p "$WORK/frames"
[ -f "$WORK/frames/f_0450.png" ] || xvfb-run -a -s "-screen 0 1920x1080x24" blender -b -P "$HERE/scene.py" -- "$WORK/frames/f_" 1 450 100
python3 "$HERE/bgm.py" "$WORK/bgm.wav"
python3 "$HERE/titles.py" "$HERE/../fonts" "$WORK/txt" "$WORK/titles.ffscript"
ffmpeg -y -framerate 30 -i "$WORK/frames/f_%04d.png" -i "$WORK/bgm.wav" \
  -filter_complex_script "$WORK/titles.ffscript" -map "[v]" -map 1:a \
  -c:v libx264 -preset slow -crf 18 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  "$HERE/nakagawa_teaser_15s.mp4"
