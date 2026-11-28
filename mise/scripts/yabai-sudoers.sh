#!/bin/sh
# Lets yabai load its scripting addition without a password prompt.
# Run once with sudo, and again after each yabai upgrade (the hash changes).
set -eu
YABAI="$(readlink -f "${HOME:-/Users/$SUDO_USER}/.local/share/mise/installs/github-asmvik-yabai/latest/bin/yabai")"
[ -x "$YABAI" ] || { echo "yabai not found at $YABAI" >&2; exit 1; }
USER_NAME="${SUDO_USER:-$(id -un)}"
HASH="$(shasum -a 256 "$YABAI" | cut -d' ' -f1)"
LINE="$USER_NAME ALL=(root) NOPASSWD: sha256:$HASH $YABAI --load-sa"
TMP="$(mktemp /etc/sudoers.d/.yabai.XXXXXX)"
echo "$LINE" > "$TMP"
visudo -cf "$TMP"
chmod 0440 "$TMP"
mv "$TMP" /etc/sudoers.d/yabai
echo "wrote /etc/sudoers.d/yabai for $YABAI"
