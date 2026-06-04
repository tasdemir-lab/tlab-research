#!/bin/bash
# Sync plugin rules to project .claude/rules/
# Rules can't be loaded by the plugin system (feature request #14200),
# so we copy them from the plugin cache to the project directory.
set -euo pipefail

RULES_SRC="${CLAUDE_PLUGIN_ROOT}/rules"
RULES_DST="${CLAUDE_PROJECT_DIR}/.claude/rules"

# Only sync if source rules exist
[ -d "$RULES_SRC" ] || exit 0

# Guard: only sync into research projects (prevents pollution if installed at --scope user)
# The tlab marker may live in AGENTS.md (canonical) or CLAUDE.md (pointer that @imports it).
# Explicit if-form (not inline && chains) is safe under `set -euo pipefail`.
found=0
for marker_file in AGENTS.md CLAUDE.md; do
  if [ -f "${CLAUDE_PROJECT_DIR}/${marker_file}" ] && grep -q "tlab" "${CLAUDE_PROJECT_DIR}/${marker_file}" 2>/dev/null; then
    found=1
    break
  fi
done
if [ "$found" -ne 1 ]; then
  exit 0
fi

mkdir -p "$RULES_DST"

for rule in "$RULES_SRC"/*.md; do
  [ -f "$rule" ] || continue
  basename=$(basename "$rule")
  target="${RULES_DST}/_plugin_${basename}"

  # Only copy if changed (skip if identical)
  if [ ! -f "$target" ] || ! cmp -s "$rule" "$target"; then
    cp "$rule" "$target"
  fi
done

exit 0
