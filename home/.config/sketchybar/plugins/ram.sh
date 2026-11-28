#!/usr/bin/env bash
# Free RAM as macOS memory_pressure reports it. Colors follow the RAM rule:
# under 30% free start nothing heavy (yellow), under 20% close things (red).
free="$(memory_pressure 2>/dev/null | awk -F': ' '/free percentage/ { gsub("%", "", $2); print $2 }')"
[[ -n "$free" ]] || exit 0
if   (( free < 20 )); then color=0xfff38ba8
elif (( free < 30 )); then color=0xfff9e2af
else                       color=0xffa6e3a1
fi
sketchybar --set "$NAME" label="${free}% free" label.color="$color" icon.color="$color"
