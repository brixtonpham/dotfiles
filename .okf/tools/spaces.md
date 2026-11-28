---
type: Reference
title: "Space names, window grid and hotkeys (Spaceward)"
description: "Spaceward, the menu-bar app that names macOS Spaces by UUID, places windows on a grid and binds Hyper hotkeys: install through mise, the /Applications link, config in dotfiles, permissions, and what it replaced (yabai, skhd.zig, SketchyBar)."
resource: https://github.com/brixtonpham/spaceward
tags: [macos, spaces, spaceward, hotkeys, mise]
status: stable
generated: { by: claude-code/claude-opus-5-5, at: 2026-11-28T10:40:00Z }
stale_after: 2027-02-28
sources:
  - id: spaceward
    resource: https://github.com/brixtonpham/spaceward
    title: Spaceward (v0.1.0)
---

# What it does

macOS has no way to rename a desktop. Spaceward is one menu-bar app that:

* names Spaces and stores the names by Space UUID in `~/.config/spaceward/names.json` (machine-local, not committed);
* shows `<index> · <name>` and free RAM in the menu bar (RAM yellow under 30%, red under 20%, the thresholds of the hub rule `browser-hygiene.md`);
* places the focused window on a grid and opens apps from Hyper hotkeys (Carbon hotkeys, no permission needed);
* has a CLI: `spaceward list | name NAME | name --delete | grid R:C:X:Y:W:H | ram`.

It replaced yabai (labels and grid), skhd.zig (hotkeys) and SketchyBar (the bar) on 2026-11-28.

# Install

* `"github:brixtonpham/spaceward"` in `mise/config.toml`, with `strip_components = 0` so the release zip keeps `Spaceward.app` whole, and `minimum_release_age = "0s"` because it is our own release.
* `/Applications/Spaceward.app` links to the mise install (`[dotfiles]` entry in `mise/conf.d/dotfiles.toml`), and `login_items` starts it at login.
* Hotkeys and RAM thresholds: `home/.config/spaceward/config.json`. The menu's "Reload Config" picks up edits.
* Hyper is Caps Lock held, from Karabiner; see [macOS desktop setup](macos-desktop.md).

# Permissions and limits

* **Accessibility** is needed only for the window grid. The release is ad-hoc signed, so each update needs the grant again.
* Thaw may put the menu-bar item in its hidden section; drag it out once in Thaw.
* Mission Control still shows "Desktop N". Spaceward's unnamed label uses the same N.
* It reads Spaces through a private SkyLight call (`CGSCopyManagedDisplaySpaces`), which a macOS update can break.
* Releases are arm64 only.
