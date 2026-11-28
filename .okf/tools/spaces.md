---
type: Reference
title: "Space names (yabai + SketchyBar)"
description: "How macOS Spaces get names here: yabai holds the labels, the space-name script stores them by Space UUID, SketchyBar shows them in a bottom bar; install, launchd agents, permissions and limits."
resource: https://github.com/asmvik/yabai
tags: [macos, spaces, yabai, sketchybar, launchd, mise]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-28T10:00:00Z }
stale_after: 2027-02-28
sources:
  - id: yabai
    resource: https://github.com/asmvik/yabai
    title: yabai (renamed from koekeishiya/yabai in December 2025), v7.1.25
  - id: sketchybar
    resource: https://github.com/FelixKratz/SketchyBar
    title: SketchyBar v2.24.1
  - id: mise-launchd
    resource: https://github.com/jdx/mise/blob/main/docs/bootstrap/launchd.md
    title: mise docs, macOS LaunchAgents
---

# What it does

macOS has no way to rename a desktop: Mission Control always says "Desktop N", and a full-screen Space shows its window title. Here the names live outside Mission Control:

| Part | Role | Source in this repository |
|------|------|---------------------------|
| yabai | Holds a label per Space. Layout is `float`, so it does not move windows. | `home/.config/yabai/yabairc` |
| `space-name` | Names the focused Space and stores the name by Space UUID in `~/.local/state/space-name/names.tsv` (machine-local, not committed) | `home/.local/bin/space-name` |
| SketchyBar | A 26 px bar at the bottom of the screen (the Dock autohides there): Space name, front app, free RAM, time | `home/.config/sketchybar/` |

```sh
space-name work      # name the focused Space
space-name           # list Spaces and names
space-name -d        # remove the focused Space's name
space-name --apply   # re-apply stored names (yabairc and yabai signals run it)
```

Names are keyed by UUID, not index, so adding or moving desktops does not shift them. A full-screen Space gets a new UUID each time the app enters full screen, so its name does not survive that.

The RAM item colors free memory yellow under 30% and red under 20%, the thresholds of the hub rule `browser-hygiene.md`.

# Install

* yabai: `"github:asmvik/yabai"` in `mise/config.toml` (macOS only).
* SketchyBar: `"brew:felixkratz/formulae/sketchybar"` in `mise/conf.d/dotfiles.toml`; mise builds it from the tap.
* Both run as LaunchAgents from `[bootstrap.macos.launchd.agents]` in `mise/config.toml` (`dev.mise.yabai`, `dev.mise.sketchybar`). Apply with `mise bootstrap macos launchd-agents apply`. Logs are in `~/Library/Logs/{yabai,sketchybar}{,.err}.log`.
* The agents get no mise activation, so their `PATH` lists `~/.local/bin`, the mise shims and `/opt/homebrew/bin`.

# Permissions and limits

* **Accessibility (by hand, once).** yabai exits with "could not access accessibility features" until `~/.local/share/mise/installs/github-asmvik-yabai/latest/bin/yabai` is allowed in System Settings → Privacy & Security → Accessibility. Then run `launchctl kickstart -k gui/$(id -u)/dev.mise.yabai`. A yabai upgrade changes the binary, so the permission may need to be granted again.
* **No scripting addition.** Labels work without it. Focusing a Space by name (`yabai -m space --focus work`), and creating or moving Spaces, need the scripting addition: SIP is already off on this Mac, but it also needs the boot-arg `-arm64e_preview_abi` (`sudo nvram`, then a reboot) and a sudoers entry for `yabai --load-sa`. Not set up.
* Mission Control's own labels stay "Desktop N".
