#!/bin/sh
# Create a new module from this template.
#
#   ./new_module.sh <name> [hp] [parent_dir]   copy into <parent_dir>/<name> (default: the folder that holds this template) with a new git repo
#   ./new_module.sh --here <name> [hp]         convert THIS checkout in place (after GitHub "Use this template")
#
# Commits use your normal git identity. Override with EURORACK_GIT_NAME / EURORACK_GIT_EMAIL.
set -e
here=; [ "$1" = "--here" ] && { here=1; shift; }
name=$1; hp=${2:-TBD}; parent=$3
[ -n "$name" ] || { sed -n '2,8p' "$0"; exit 1; }
echo "$name" | grep -qE '^[a-z0-9_]+$' || { echo "name: lowercase letters, digits, underscores"; exit 1; }
src=$(cd "$(dirname "$0")" && pwd)
[ -n "$parent" ] || parent=$(dirname "$src")
[ -f "$src/.template" ] || { echo "$src is not the template (no .template marker); already converted?"; exit 1; }

if [ -n "$here" ]; then
  dest=$src
else
  dest=$parent/$name
  [ ! -e "$dest" ] || { echo "$dest already exists"; exit 1; }
  mkdir -p "$dest"
  (cd "$src" && { git ls-files 2>/dev/null || find . -type f -not -path './.git/*'; }) | while read -r f; do
    mkdir -p "$dest/$(dirname "$f")"; cp -p "$src/$f" "$dest/$f"
  done
fi

cd "$dest"
rm -f .template LICENSE   # template license; the module's license is the Builder's choice
mv README.module.md README.md
grep -rlE '__MODULE__|__HP__' --exclude-dir=.git --exclude=new_module.sh . | while read -r f; do
  sed -i.bak -e "s/__MODULE__/$name/g" -e "s/__HP__/$hp/g" "$f" && rm -f "$f.bak"
done
[ "$hp" = TBD ] || { sed -i.bak "s/^# hp=.*/# hp=$hp/" docs/panel.csv && rm -f docs/panel.csv.bak; }
rm -f new_module.sh

[ -n "$here" ] || git init -q -b main
[ -z "$EURORACK_GIT_NAME" ] || git config user.name "$EURORACK_GIT_NAME"
[ -z "$EURORACK_GIT_EMAIL" ] || git config user.email "$EURORACK_GIT_EMAIL"
git add -A && git commit -q -m "$name: start from eurorack_template"
echo "created $dest: next, run 'make check' and start Phase 0 (see CLAUDE.md)"
