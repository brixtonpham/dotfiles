#!/usr/bin/env bash
# Shows "index · name" for the focused Space; an unnamed one shows its index.
space="$(yabai -m query --spaces --space 2>/dev/null)" || { sketchybar --set "$NAME" label="yabai off"; exit 0; }
idx="$(jq -r .index <<<"$space")"
label="$(jq -r .label <<<"$space")"
if [[ -z "$label" ]]; then
  if [[ "$(jq -r '."is-native-fullscreen"' <<<"$space")" == true ]]; then label="fullscreen"; else label="Desktop $idx"; fi
  sketchybar --set "$NAME" label="$idx · $label" label.color=0xff6c7086
else
  sketchybar --set "$NAME" label="$idx · $label" label.color=0xff89b4fa
fi
