#!/usr/bin/env bash
# v2 teaser: 2D motion graphics (canvas) main + 3D ring element (Blender) + BGM
# Usage: ./build.sh <work_dir>   (needs: blender, xvfb-run, node+playwright, ffmpeg, python3)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"; WORK="${1:-$HERE/work}"; mkdir -p "$WORK/obj"
[ -f "$WORK/obj/o_0450.png" ] || xvfb-run -a -s "-screen 0 1280x1024x24" blender -b -P "$HERE/object.py" -- "$WORK/obj/o_" 1 450
NODE_PATH=$(npm root -g) node "$HERE/capture.js" "$HERE/mg.html" "$WORK/obj" "$WORK/mg" 0 449
python3 "$HERE/../bgm.py" "$WORK/bgm.wav"
ffmpeg -y -framerate 30 -i "$WORK/mg/m_%04d.png" -i "$WORK/bgm.wav" -map 0:v -map 1:a \
  -c:v libx264 -preset slow -crf 20 -pix_fmt yuv420p -c:a aac -b:a 192k -shortest -movflags +faststart \
  "$HERE/nakagawa_teaser_v2_15s.mp4"
