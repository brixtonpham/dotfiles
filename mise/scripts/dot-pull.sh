#!/bin/bash

# =============================================================================
# Pull the latest main from origin (mise run dot:pull). On main, local commits
# from dot:save are rebased on top and uncommitted edits are stashed around the
# pull. On any other branch, main is fast-forwarded without switching to it.
# On a fork with an `upstream` remote, upstream's main is then merged in (a
# merge, not a rebase, so commits already on origin keep their hashes and
# dot:push never needs a force push). The origin pull uses --rebase=merges so
# an unpushed upstream merge is kept, not flattened into replayed commits.
# =============================================================================

set -euo pipefail

DOTFILES_DIR="$HOME/.dotfiles"
BRANCH="main"

current="$(git -C "$DOTFILES_DIR" symbolic-ref --short -q HEAD || true)"
if [ "$current" = "$BRANCH" ]; then
    git -C "$DOTFILES_DIR" pull --rebase=merges --autostash origin "$BRANCH"
    if git -C "$DOTFILES_DIR" remote get-url upstream >/dev/null 2>&1; then
        git -C "$DOTFILES_DIR" pull --no-rebase --no-edit --autostash upstream "$BRANCH"
    fi
else
    # Refuses a non-fast-forward rather than rewriting the local branch.
    git -C "$DOTFILES_DIR" fetch origin "$BRANCH:$BRANCH"
    echo "Updated $BRANCH; still on ${current:-a detached HEAD}."
fi
git -C "$DOTFILES_DIR" log --oneline -1 "$BRANCH"
