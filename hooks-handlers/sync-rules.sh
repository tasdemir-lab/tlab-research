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
# Check for CLAUDE.md containing tlab marker
if [ -f "${CLAUDE_PROJECT_DIR}/CLAUDE.md" ]; then
  grep -q "tlab" "${CLAUDE_PROJECT_DIR}/CLAUDE.md" 2>/dev/null || exit 0
else
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
