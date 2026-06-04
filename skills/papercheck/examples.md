# Examples

## Example prompt to Claude (triggers Skill)
"Claude Code says I must control for migration as a confounder. Check whether Autor-Dorn-Hanson address migration threats in their main identification, and whether they use controls or robustness. Use page-anchored quotes."

## Example command (what Claude will run)
```bash
# Locate the script dynamically
SCRIPT="$(find ~/.claude/plugins/cache/tlab-research -path '*/papercheck/scripts/papercheck.py' 2>/dev/null | sort -V | tail -1)"

python "$SCRIPT" \
  --pdf lit/papers/ADH2013.pdf \
  --issue "Does the paper address migration (endogenous sorting) as a confounder? Controls vs robustness vs placebo?" \
  --outdir .papercheck/packs
```

## Multiple PDFs in one run
```bash
python "$SCRIPT" \
  --pdf lit/papers/ADH2013.pdf \
  --pdf lit/papers/Pierce2016.pdf \
  --issue "Does the paper address pre-trends as an identification threat?" \
  --outdir .papercheck/packs
```

## What you should expect back
- A console summary: `[fresh] ADH2013.pdf -> ADH2013__a1b2c3... | verdict=Yes`
- A JSON evidence pack: `.papercheck/packs/<key>.json`
- A readable MD pack: `.papercheck/packs/<key>.md`
- On subsequent runs with same PDF+issue: `[cache]` instead of `[fresh]`

## Cache management examples
```bash
# List all cached evidence packs
python "$SCRIPT" --pdf x --issue x --list-cache

# Clear all cached packs (forces re-extraction)
python "$SCRIPT" --pdf x --issue x --clear-cache
```

## Error scenarios
- **Antigravity CLI not installed**: Script exits with error message and installation URL
- **PDF not found**: Script prints warning and continues with other PDFs
- **Timeout**: Script prints timeout warning; use `--timeout 600` for large PDFs
