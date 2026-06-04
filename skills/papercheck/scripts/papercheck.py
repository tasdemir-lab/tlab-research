#!/usr/bin/env python3
"""
papercheck.py - Extract evidence from academic PDFs about specific methodological concerns.

Requires: Antigravity CLI (https://antigravity.google)
Install: Visit https://antigravity.google to download, then run `agy install`
"""
import argparse, hashlib, json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

# Default timeout for Antigravity CLI calls (5 minutes)
DEFAULT_TIMEOUT_SECONDS = 300

# Required fields in the output schema
REQUIRED_FIELDS = ["paper", "verdict", "what_they_do", "evidence"]
REQUIRED_PAPER_FIELDS = ["title", "year", "journal"]
REQUIRED_EVIDENCE_FIELDS = ["page", "quote"]

PROMPT_TEMPLATE = r"""
You are extracting evidence from an academic paper PDF.

TASK:
Determine whether the paper addresses the following issue/threat/confounder/methodological concern:

ISSUE: {issue}

Return ONLY valid JSON with this schema:
{{
  "paper": {{
    "title": "actual paper title",
    "year": "publication year",
    "journal": "journal or venue name"
  }},
  "verdict": "Yes|No|Partially|Unclear",
  "what_they_do": ["list ONLY the methods actually used from: controls, robustness checks, placebos/falsification, sensitivity/bounds, discussion only"],
  "where_in_paper": ["e.g. Section 4.2, Table 3, Appendix B"],
  "evidence": [
    {{"page": "PDF page number (integer)", "quote": "verbatim quote from paper"}},
    {{"page": "PDF page number (integer)", "quote": "verbatim quote from paper"}},
    {{"page": "PDF page number (integer)", "quote": "verbatim quote from paper"}}
  ],
  "implication_for_my_work": "what this means for the user's research design",
  "caveats": ["any limitations or uncertainties"]
}}

RULES:
- Include at least 3 evidence items if verdict is Yes or Partially.
- Every evidence item MUST include a PDF page number (as shown in PDF viewer, starting from 1) and a verbatim quote.
- For what_they_do, include ONLY the methods the paper actually uses - do not list all options.
- If you cannot find page numbers or cannot verify quotes, set verdict to "Unclear" and explain why in caveats.
- Prefer main text over appendix, but include appendix evidence if that's where the robustness is.
- Be conservative: if it's ambiguous, say Unclear.

Now analyze this PDF:
{pdf_ref}
""".strip()

def sha256_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()

def extract_json_loose(text: str) -> dict:
    """
    Extract a JSON object from CLI output that may contain surrounding text.

    Antigravity CLI (-p mode) returns plain text. The JSON is usually the entire
    output, but may be wrapped in markdown fences or have trailing text.
    """
    text = text.strip()

    # First, try to parse the outer wrapper
    try:
        wrapper = json.loads(text)
        # Check if this is a wrapper format (legacy Gemini CLI compatibility)
        if isinstance(wrapper, dict) and "response" in wrapper:
            response_text = wrapper["response"]
            # Strip markdown code fences if present
            response_text = re.sub(r'^```(?:json)?\s*', '', response_text.strip())
            response_text = re.sub(r'\s*```$', '', response_text.strip())
            # Parse the inner JSON
            return json.loads(response_text)
        # If no "response" field, assume it's already the right format
        return wrapper
    except Exception:
        pass

    # Fallback: find balanced JSON object using brace counting
    start_idx = text.find('{')
    if start_idx == -1:
        raise ValueError("No JSON object found in output.")

    depth = 0
    in_string = False
    escape_next = False
    end_idx = start_idx

    for i, char in enumerate(text[start_idx:], start=start_idx):
        if escape_next:
            escape_next = False
            continue
        if char == '\\' and in_string:
            escape_next = True
            continue
        if char == '"' and not escape_next:
            in_string = not in_string
            continue
        if in_string:
            continue
        if char == '{':
            depth += 1
        elif char == '}':
            depth -= 1
            if depth == 0:
                end_idx = i
                break

    if depth != 0:
        raise ValueError("Unbalanced braces in JSON output.")

    return json.loads(text[start_idx:end_idx + 1])


def validate_output(data: dict) -> list[str]:
    """
    Validate that the output contains all required fields.
    Returns a list of warning messages (empty if valid).
    """
    warnings = []

    for field in REQUIRED_FIELDS:
        if field not in data:
            warnings.append(f"Missing required field: {field}")

    if "paper" in data:
        for field in REQUIRED_PAPER_FIELDS:
            if field not in data["paper"]:
                warnings.append(f"Missing paper.{field}")

    if "evidence" in data:
        for i, ev in enumerate(data["evidence"]):
            for field in REQUIRED_EVIDENCE_FIELDS:
                if field not in ev or not str(ev.get(field, "")).strip():
                    warnings.append(f"Evidence item {i+1} missing or empty: {field}")

    return warnings


def check_agy_cli(agy_bin: str) -> bool:
    """Check if Antigravity CLI (agy) is available."""
    return shutil.which(agy_bin) is not None

def main():
    ap = argparse.ArgumentParser(
        description="Extract evidence from academic PDFs about methodological concerns.",
        epilog="Requires Antigravity CLI (agy) to be installed (https://antigravity.google)"
    )
    ap.add_argument("--pdf", action="append", required=True, help="Path to PDF (repeatable).")
    ap.add_argument("--issue", required=True, help="Confounder/threat/method question.")
    ap.add_argument("--outdir", default=".papercheck/packs", help="Output directory.")
    ap.add_argument("--agy-bin", default="agy", help="Antigravity CLI executable name/path.")
    ap.add_argument("--model", default="", help="Optional model override (e.g., 'Gemini 3.5 Flash (High)').")
    ap.add_argument("--timeout", type=int, default=DEFAULT_TIMEOUT_SECONDS,
                    help=f"Timeout in seconds for Antigravity CLI calls (default: {DEFAULT_TIMEOUT_SECONDS}).")
    ap.add_argument("--clear-cache", action="store_true", help="Clear all cached evidence packs.")
    ap.add_argument("--list-cache", action="store_true", help="List all cached evidence packs.")
    args = ap.parse_args()

    outdir = Path(args.outdir)
    outdir.mkdir(parents=True, exist_ok=True)

    # Handle cache management commands
    if args.clear_cache:
        count = 0
        for f in outdir.glob("*.json"):
            f.unlink()
            count += 1
        for f in outdir.glob("*.md"):
            f.unlink()
        for f in outdir.glob("*.raw.txt"):
            f.unlink()
        print(f"[papercheck] Cleared {count} cached evidence packs from {outdir}")
        return

    if args.list_cache:
        packs = sorted(outdir.glob("*.json"))
        if not packs:
            print(f"[papercheck] No cached evidence packs in {outdir}")
        else:
            print(f"[papercheck] {len(packs)} cached evidence packs in {outdir}:")
            for p in packs:
                try:
                    data = json.loads(p.read_text(encoding="utf-8"))
                    title = data.get("paper", {}).get("title", "(unknown)")
                    verdict = data.get("verdict", "?")
                    issue = data.get("_papercheck", {}).get("issue", "(unknown issue)")[:50]
                    print(f"  - {p.stem}: {title[:40]}... | {verdict} | {issue}...")
                except Exception:
                    print(f"  - {p.stem}: (could not read)")
        return

    # Check Antigravity CLI availability
    if not check_agy_cli(args.agy_bin):
        print(f"[papercheck] ERROR: Antigravity CLI not found: '{args.agy_bin}'", file=sys.stderr)
        print("[papercheck] Install from: https://antigravity.google", file=sys.stderr)
        print("[papercheck] Or specify a different path with --agy-bin", file=sys.stderr)
        sys.exit(1)

    results = []

    for pdf in args.pdf:
        pdf_path = Path(pdf).resolve()
        if not pdf_path.exists():
            print(f"[papercheck] PDF not found: {pdf_path}", file=sys.stderr)
            continue

        file_hash = sha256_file(pdf_path)
        issue_hash = hashlib.sha256(args.issue.encode("utf-8")).hexdigest()
        # Use longer hash prefixes (16 chars = 64 bits each) for better collision resistance
        key = f"{pdf_path.stem}__{file_hash[:16]}__{issue_hash[:16]}"
        json_path = outdir / f"{key}.json"
        md_path = outdir / f"{key}.md"
        raw_path = outdir / f"{key}.raw.txt"

        # Cache hit
        if json_path.exists():
            data = json.loads(json_path.read_text(encoding="utf-8"))
            results.append((pdf_path.name, key, data, "cache"))
            continue

        # Antigravity CLI reads files via @path syntax (resolved via tool calls).
        pdf_ref = f"@{str(pdf_path)}"
        prompt = PROMPT_TEMPLATE.format(issue=args.issue, pdf_ref=pdf_ref)

        cmd = [args.agy_bin, "-p", prompt, "--print-timeout", f"{args.timeout}s"]
        if args.model:
            cmd.extend(["--model", args.model])

        try:
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=args.timeout)
        except subprocess.TimeoutExpired:
            print(f"[papercheck] Antigravity CLI timed out after {args.timeout}s for {pdf_path.name}", file=sys.stderr)
            continue

        raw = (proc.stdout or "") + ("\n--- STDERR ---\n" + proc.stderr if proc.stderr else "")
        raw_path.write_text(raw, encoding="utf-8")

        if proc.returncode != 0:
            print(f"[papercheck] Antigravity CLI failed for {pdf_path.name} (see {raw_path})", file=sys.stderr)
            continue

        try:
            data = extract_json_loose(proc.stdout)
        except Exception as e:
            print(f"[papercheck] Could not parse JSON for {pdf_path.name}: {e} (see {raw_path})", file=sys.stderr)
            continue

        # Validate output schema
        validation_warnings = validate_output(data)
        if validation_warnings:
            print(f"[papercheck] Validation warnings for {pdf_path.name}:", file=sys.stderr)
            for w in validation_warnings:
                print(f"  - {w}", file=sys.stderr)

        # Enrich with provenance
        data["_papercheck"] = {
            "pdf": str(pdf_path),
            "issue": args.issue,
            "created_at": datetime.now(timezone.utc).isoformat(),
            "cache_key": key,
        }

        json_path.write_text(json.dumps(data, ensure_ascii=False, indent=2), encoding="utf-8")

        # Simple markdown rendering
        lines = []
        p = data.get("paper", {})
        lines.append(f"# Evidence pack: {p.get('title','(unknown title)')}")
        lines.append(f"- **PDF:** `{pdf_path.name}`")
        lines.append(f"- **Issue:** {args.issue}")
        lines.append(f"- **Verdict:** {data.get('verdict','Unclear')}")
        lines.append(f"- **What they do:** {', '.join(data.get('what_they_do', []))}")
        if data.get("where_in_paper"):
            lines.append(f"- **Where:** {', '.join(data.get('where_in_paper', []))}")
        lines.append("\n## Evidence (verbatim quotes)\n")
        for ev in data.get("evidence", []):
            page = str(ev.get("page", "")).strip()
            quote = str(ev.get("quote", "")).strip()
            if quote:
                lines.append(f"- **p.{page}** — “{quote}”")
        lines.append("\n## Implication for my work\n")
        lines.append(data.get("implication_for_my_work", "").strip() or "(none)")
        if data.get("caveats"):
            lines.append("\n## Caveats\n")
            for c in data.get("caveats", []):
                if c.strip():
                    lines.append(f"- {c.strip()}")

        md_path.write_text("\n".join(lines).strip() + "\n", encoding="utf-8")

        results.append((pdf_path.name, key, data, "fresh"))

    # Print a brief console summary (Claude can read this cheaply)
    for name, key, data, status in results:
        print(f"[{status}] {name} -> {key} | verdict={data.get('verdict','Unclear')}")

if __name__ == "__main__":
    main()
