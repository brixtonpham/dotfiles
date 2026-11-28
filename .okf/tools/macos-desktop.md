---
type: Reference
title: "macOS desktop setup (hotkeys, Hyper key, menu bar, terminal, preferences)"
description: "The macOS desktop tools beyond Spaceward: the Karabiner Hyper key, Thaw, Stats, Ghostty, Homerow, the declared macOS preferences and login items, and why Magnet was dropped."
tags: [macos, spaceward, karabiner, ghostty, thaw, stats, homerow, defaults, launchd]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-28T10:10:00Z }
stale_after: 2027-02-28
sources:
  - id: karabiner
    resource: https://karabiner-elements.pqrs.org/docs/manual/misc/configuration-file-path/
    title: Karabiner-Elements, configuration file path (link the directory, not the file)
  - id: mise-defaults
    resource: https://github.com/jdx/mise/blob/main/docs/bootstrap/macos-defaults.md
    title: mise docs, macOS defaults and login items
---

# Pieces

| Tool | Job | Declared in | Config |
|------|-----|-------------|--------|
| Karabiner-Elements | Caps Lock held = Hyper (cmd+alt+ctrl+shift); tapped = Caps Lock, which still switches between Vietnamese Telex and ABC | `brew-cask:karabiner-elements` (pkg cask: needs sudo from a terminal) | `home/karabiner/karabiner.json`, linked as the whole `~/.config/karabiner` directory because Karabiner replaces a linked file when it saves |
| Spaceward | Hyper hotkeys, window grid, Space names, free RAM | `github:brixtonpham/spaceward` | `home/.config/spaceward/config.json`; see [Space names](spaces.md) |
| Thaw | Menu bar manager for the notch; Ice is broken on macOS 26 | `brew-cask:thaw` | in the app |
| Stats | Memory pressure and swap in the menu bar | `brew-cask:stats` | in the app |
| Ghostty | Terminal for agent panes | `brew-cask:ghostty` | `home/.config/ghostty/config` |
| Homerow | Keyboard hints to click anything (paid) | `brew-cask:homerow` | in the app |

skhd.zig and the `wm` script were used for hotkeys until Spaceward replaced them on 2026-11-28.

# Hotkeys (Hyper = hold Caps Lock)

| Keys | Action |
|------|--------|
| Hyper + ← / → / ↑ / ↓ | left / right / top / bottom half |
| Hyper + Return | maximize |
| Hyper + C | center (4/6 of the screen) |
| Hyper + U / I / J / K | quarters: top-left, top-right, bottom-left, bottom-right |
| Hyper + N | name the current Space |
| Hyper + T / B / H | Ghostty, Brave, Herdr |

# Preferences and login items

`mise/config.toml` declares `[bootstrap.settings.macos]`: Dock autohide with no delay and a 0.15 s animation, `mru-spaces` off, `expose-group-apps` on, `KeyRepeat` 2 and `InitialKeyRepeat` 15, window animations off, and macOS edge tiling off. Apply with `mise bootstrap macos defaults apply`, then `killall Dock`. Login items add Stats, Thaw and Homerow (additive; other items stay).

Magnet was dropped: Spaceward places windows from the hotkeys, and two window managers fight over the same window. It was quit and removed from login items; the app is still installed.

# Permissions (by hand, once)

* Spaceward: allow it in Privacy & Security → Accessibility for the window grid; hotkeys work without it.
* Karabiner: approve its driver extension and allow Input Monitoring when it asks.
* Homerow, Thaw and Stats ask for Accessibility or similar access on first launch.
