#!/bin/sh
# Create a new module repo from this template.
#   ./new_module.sh <name> [hp] [parent_dir]
#   e.g. ./new_module.sh dual_lfo 8      -> ~/projects/dual_lfo
set -e
name=$1; hp=${2:-TBD}; parent=${3:-$HOME/projects}
[ -n "$name" ] || { echo "usage: $0 <name> [hp] [parent_dir]"; exit 1; }
echo "$name" | grep -qE '^[a-z0-9_]+$' || { echo "name: lowercase letters, digits, underscores"; exit 1; }
dest=$parent/$name
[ ! -e "$dest" ] || { echo "$dest already exists"; exit 1; }
src=$(cd "$(dirname "$0")" && pwd)
mkdir -p "$dest"
(cd "$src" && git ls-files 2>/dev/null || find . -type f -not -path './.git/*') | while read -r f; do
  case "$f" in ./.template|.template|./new_module.sh|new_module.sh) continue ;; esac
  mkdir -p "$dest/$(dirname "$f")"; cp -p "$src/$f" "$dest/$f"
done
cd "$dest"
grep -rlE '__MODULE__|__HP__' . | while read -r f; do
  sed -i '' -e "s/__MODULE__/$name/g" -e "s/__HP__/$hp/g" "$f"
done
[ "$hp" = TBD ] || sed -i '' "s/^# hp=.*/# hp=$hp/" docs/panel.csv
sed -i '' '/^## Using this template/,/^## /{/^## Using this template/d;/^## /!d;}' README.md
git init -q -b main
git config user.name "Tony Thayer-Osborne"; git config user.email tony.thayer@gmail.com
git add -A && git commit -q -m "$name: start from eurorack_template"
echo "created $dest - next: open it with Claude Code and start Phase 0 (CLAUDE.md)"
