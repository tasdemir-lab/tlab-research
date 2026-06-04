#!/usr/bin/env python3
"""Convert BibTeX entries to Zotero connector-compatible JSON and import them.

Usage:
    # Import from bibtex file (preferred — avoids shell quoting issues)
    python3 bib_to_zotero.py --file refs.bib

    # Import from bibtex string via stdin
    python3 bib_to_zotero.py < refs.bib

    # Just convert (don't import)
    python3 bib_to_zotero.py --dry-run --file refs.bib

    # Target a specific collection (show reminder)
    python3 bib_to_zotero.py --collection "english-medium"

Output: JSON with results for each entry.

NOTE: Requires bibtexparser 1.x API (tested with 1.4.x).
      Version 2.x has an incompatible API — do not upgrade without updating this script.
"""

import argparse
import hashlib
import json
import re
import sys
import time
import urllib.request

import bibtexparser


# ── BibTeX type → Zotero itemType ──────────────────────────────────────────
BIBTEX_TO_ZOTERO_TYPE = {
    "article": "journalArticle",
    "book": "book",
    "inbook": "bookSection",
    "incollection": "bookSection",
    "inproceedings": "conferencePaper",
    "conference": "conferencePaper",
    "mastersthesis": "thesis",
    "phdthesis": "thesis",
    "techreport": "report",
    "manual": "document",
    "misc": "document",
    "unpublished": "manuscript",
    "proceedings": "book",
    "booklet": "document",
    "online": "webpage",       # biblatex type
    "electronic": "webpage",   # biblatex alias
}

# ── BibTeX field → Zotero field (common across types) ──────────────────────
FIELD_MAP = {
    "title": "title",
    "year": "date",
    "doi": "DOI",
    "abstract": "abstractNote",
    "volume": "volume",
    "pages": "pages",
    "url": "url",
    "isbn": "ISBN",
    "issn": "ISSN",
    "language": "language",
    "publisher": "publisher",
    "address": "place",
    "edition": "edition",
    "keywords": "_keywords",  # handled separately
    # note is deliberately NOT mapped — extra is reserved for the original
    # citation key and Better BibTeX directives.
}

# Type-specific field mappings
TYPE_FIELDS = {
    "journalArticle": {"journal": "publicationTitle", "number": "issue"},
    "book": {"series": "series"},
    "bookSection": {
        "booktitle": "bookTitle",
        "series": "series",
        "chapter": "section",
    },
    "conferencePaper": {"booktitle": "proceedingsTitle"},
    "report": {
        "institution": "institution",
        "number": "reportNumber",
        "type": "reportType",
        "series": "seriesTitle",
    },
    "thesis": {"school": "university", "type": "thesisType"},
}


def _is_braced_unit(text: str) -> bool:
    """Check if text is entirely wrapped in braces: {World Bank}."""
    text = text.strip()
    return text.startswith("{") and text.endswith("}") and text.count("{") == 1


def parse_authors(author_str: str) -> list[dict]:
    """Parse BibTeX author string into Zotero creator objects.

    Handles:
    - "Last, First" (comma format — most reliable)
    - "First Last" (space format — last word is surname)
    - "{World Bank}" (braced institutional name — single-unit, no split)
    - Compound surnames only work reliably in comma format: "de la Cruz, Maria"
    """
    creators = []
    # Split on ' and ' (bibtex convention)
    parts = re.split(r"\s+and\s+", author_str.strip())
    for part in parts:
        part = part.strip()
        if not part:
            continue
        # Institutional author: entire name in braces → single-unit name
        if _is_braced_unit(part):
            creators.append(
                {
                    "creatorType": "author",
                    "lastName": _clean_creator_name(part.strip("{}").strip()),
                    "firstName": "",
                    "fieldMode": 1,  # Zotero: single-field (institutional) name
                }
            )
            continue
        # Remove wrapping braces that aren't institutional (e.g., {Açemoğlu})
        part = re.sub(r"^\{(.+)\}$", r"\1", part)
        if "," in part:
            # "Last, First" or "Last, First Middle"
            pieces = [p.strip() for p in part.split(",", 1)]
            creators.append(
                {
                    "creatorType": "author",
                    "lastName": _clean_creator_name(_strip_braces(pieces[0])),
                    "firstName": _clean_creator_name(_strip_braces(pieces[1])) if len(pieces) > 1 else "",
                }
            )
        else:
            # "First Last" — last word is surname
            words = part.split()
            if len(words) == 1:
                creators.append(
                    {
                        "creatorType": "author",
                        "lastName": _clean_creator_name(_strip_braces(words[0])),
                        "firstName": "",
                    }
                )
            else:
                creators.append(
                    {
                        "creatorType": "author",
                        "lastName": _clean_creator_name(_strip_braces(words[-1])),
                        "firstName": _clean_creator_name(_strip_braces(" ".join(words[:-1]))),
                    }
                )
    return creators


def _strip_braces(text: str) -> str:
    """Remove outer braces from a string, preserving inner content."""
    text = text.strip()
    while text.startswith("{") and text.endswith("}"):
        text = text[1:-1].strip()
    return text


def _clean_creator_name(name: str) -> str:
    """Clean LaTeX markup from a creator name and convert accents to UTF-8."""
    return clean_latex(name)


def parse_editors(editor_str: str) -> list[dict]:
    """Parse BibTeX editor string into Zotero creator objects with editor type."""
    creators = parse_authors(editor_str)
    for c in creators:
        c["creatorType"] = "editor"
    return creators


# LaTeX accent commands → UTF-8. Prefer native Unicode (XeLaTeX-friendly).
_LATEX_ACCENT_MAP = {
    # Umlauts / diaeresis
    '\\"a': "ä", '\\"o': "ö", '\\"u': "ü", '\\"A': "Ä", '\\"O': "Ö", '\\"U': "Ü",
    '\\"e': "ë", '\\"i': "ï",
    # Acute
    "\\'a": "á", "\\'e": "é", "\\'i": "í", "\\'o": "ó", "\\'u": "ú",
    "\\'A": "Á", "\\'E": "É", "\\'I": "Í", "\\'O": "Ó", "\\'U": "Ú",
    # Grave
    "\\`a": "à", "\\`e": "è", "\\`i": "ì", "\\`o": "ò", "\\`u": "ù",
    # Circumflex
    "\\^a": "â", "\\^e": "ê", "\\^i": "î", "\\^o": "ô", "\\^u": "û",
    # Tilde
    "\\~n": "ñ", "\\~a": "ã", "\\~o": "õ", "\\~N": "Ñ",
    # Turkish-specific
    "\\c{c}": "ç", "\\c{C}": "Ç", "\\c c": "ç", "\\c C": "Ç",
    "\\u{g}": "ğ", "\\u{G}": "Ğ", "\\u g": "ğ", "\\u G": "Ğ",
    "\\.{I}": "İ", "\\.I": "İ",
    "\\i": "ı",  # dotless i
    "\\c{s}": "ş", "\\c{S}": "Ş", "\\c s": "ş", "\\c S": "Ş",
    "\\v{s}": "š", "\\v{S}": "Š",  # caron (Czech/Slovak), not Turkish ş
    # Nordic / other European
    "\\aa": "å", "\\AA": "Å", "\\ae": "æ", "\\AE": "Æ",
    "\\oe": "œ", "\\OE": "Œ", "\\o": "ø", "\\O": "Ø",
    "\\ss": "ß",
    # Caron
    "\\v{c}": "č", "\\v{C}": "Č", "\\v{z}": "ž", "\\v{Z}": "Ž",
    "\\v{r}": "ř", "\\v{R}": "Ř",
}


def clean_latex(text: str) -> str:
    """Remove LaTeX markup and convert accent macros to UTF-8 characters."""
    if not text:
        return text
    # Convert accent commands with braces: \"{o} → ö, \c{c} → ç
    # Pattern: \cmd{char} where cmd is one of the accent commands
    def _replace_braced_accent(m):
        cmd = m.group(1)  # e.g., '"', "'", 'c', 'u', 'v', '.'
        char = m.group(2)  # e.g., 'o', 'c', 'g'
        key = f"\\{cmd}{{{char}}}"
        return _LATEX_ACCENT_MAP.get(key, char)

    text = re.sub(r"\\([\"'`^~cuv.])\{(\w)\}", _replace_braced_accent, text)

    # Convert accent commands without braces: \"o → ö, \'e → é
    # Must come after braced version to avoid partial matches.
    # Only replace when NOT followed by a letter — prevents \i matching inside \infty,
    # \o inside \overline, \ss inside \subset, etc.
    for latex_cmd, utf_char in _LATEX_ACCENT_MAP.items():
        if "{" not in latex_cmd:
            text = re.sub(re.escape(latex_cmd) + r"(?![a-zA-Z])", utf_char, text)

    # Common LaTeX commands
    text = text.replace("\\&", "&")
    text = text.replace("\\%", "%")
    text = text.replace("\\$", "$")
    text = text.replace("~", " ")
    text = text.replace("``", '"')
    text = text.replace("''", '"')
    # Remove \textit{}, \textbf{}, \emph{} keeping content
    text = re.sub(r"\\(?:textit|textbf|emph|textrm)\s*", "", text)
    # Remove remaining braces (but not escaped ones)
    text = re.sub(r"(?<!\\)[{}]", "", text)
    return text.strip()


def bib_entry_to_zotero(entry: dict) -> dict:
    """Convert a single bibtexparser entry dict to Zotero item format."""
    bib_type = entry.get("ENTRYTYPE", "misc").lower()
    zotero_type = BIBTEX_TO_ZOTERO_TYPE.get(bib_type, "document")

    item = {"itemType": zotero_type}

    # Map common fields
    for bib_field, zot_field in FIELD_MAP.items():
        val = entry.get(bib_field, "").strip()
        if val and zot_field != "_keywords":
            item[zot_field] = clean_latex(val)

    # Map type-specific fields
    type_map = TYPE_FIELDS.get(zotero_type, {})
    for bib_field, zot_field in type_map.items():
        val = entry.get(bib_field, "").strip()
        if val:
            item[zot_field] = clean_latex(val)

    # Parse creators
    creators = []
    if "author" in entry and entry["author"].strip():
        creators.extend(parse_authors(entry["author"]))
    if "editor" in entry and entry["editor"].strip():
        creators.extend(parse_editors(entry["editor"]))
    if creators:
        item["creators"] = creators

    # Keywords → tags
    kw = entry.get("keywords", "")
    if kw:
        tags = [{"tag": k.strip()} for k in re.split(r"[,;]", kw) if k.strip()]
        if tags:
            item["tags"] = tags

    # Handle date: prefer year, append month if available
    if "date" not in item and "year" in entry:
        item["date"] = entry["year"].strip()
    if "month" in entry and "date" in item:
        month = entry["month"].strip().lower()
        month_map = {
            "jan": "01", "feb": "02", "mar": "03", "apr": "04",
            "may": "05", "jun": "06", "jul": "07", "aug": "08",
            "sep": "09", "oct": "10", "nov": "11", "dec": "12",
            "january": "01", "february": "02", "march": "03",
            "april": "04", "june": "06", "july": "07", "august": "08",
            "september": "09", "october": "10", "november": "11",
            "december": "12",
        }
        if month in month_map:
            item["date"] = f"{item['date']}-{month_map[month]}"

    # Store original citation key in extra field for reference
    citekey = entry.get("ID", "")
    if citekey:
        extra = item.get("extra", "")
        if extra:
            extra += f"\nOriginal BibTeX key: {citekey}"
        else:
            extra = f"Original BibTeX key: {citekey}"
        item["extra"] = extra

    return item


def parse_bibtex(bib_string: str) -> list[dict]:
    """Parse a BibTeX string into a list of entry dicts."""
    parser = bibtexparser.bparser.BibTexParser(common_strings=True)
    parser.ignore_nonstandard_types = False
    db = bibtexparser.loads(bib_string, parser=parser)
    return db.entries


def import_to_zotero(items: list[dict], dry_run: bool = False) -> list[dict]:
    """Import items to Zotero via the local connector saveItems endpoint."""
    results = []
    for i, item in enumerate(items):
        title = item.get("title", "Unknown")
        if dry_run:
            results.append({"title": title, "status": "dry_run", "item": item})
            continue
        # Rate limit: small delay between imports to avoid overwhelming Zotero
        if i > 0:
            time.sleep(0.3)
        try:
            # Deterministic URI from title content (stable across runs)
            uri_hash = hashlib.md5(title.encode("utf-8")).hexdigest()[:12]
            payload = json.dumps({
                "uri": f"http://import.local/{uri_hash}",
                "items": [item],
            }).encode("utf-8")
            req = urllib.request.Request(
                "http://localhost:23119/connector/saveItems",
                data=payload,
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            with urllib.request.urlopen(req, timeout=10) as resp:
                status = resp.status
            results.append({"title": title, "status": "imported", "http": status})
        except Exception as e:
            results.append({"title": title, "status": "error", "error": str(e)})
    return results


def main():
    parser = argparse.ArgumentParser(description="Import BibTeX to Zotero")
    parser.add_argument("--file", "-f", help="BibTeX file to import")
    parser.add_argument(
        "--dry-run", action="store_true", help="Convert only, don't import"
    )
    parser.add_argument(
        "--collection", help="Expected Zotero collection (reminder only)"
    )
    args = parser.parse_args()

    # Read input
    if args.file:
        with open(args.file, encoding="utf-8") as fh:
            bib_string = fh.read()
    else:
        bib_string = sys.stdin.read()

    if not bib_string.strip():
        print(json.dumps({"error": "No BibTeX input provided"}))
        sys.exit(1)

    # Count @ entries in raw input to detect silent drops.
    # Exclude @string, @preamble, @comment — these are BibTeX infrastructure, not entries.
    raw_entry_count = len(re.findall(
        r"^\s*@(?!string|preamble|comment)\w+\s*\{", bib_string, re.MULTILINE | re.IGNORECASE
    ))

    # Parse and convert
    entries = parse_bibtex(bib_string)
    if not entries:
        print(json.dumps({"error": "No valid BibTeX entries found"}))
        sys.exit(1)

    if raw_entry_count > len(entries):
        dropped = raw_entry_count - len(entries)
        print(
            f"WARNING: {dropped} of {raw_entry_count} entries failed to parse and were skipped.",
            file=sys.stderr,
        )

    zotero_items = [bib_entry_to_zotero(e) for e in entries]

    # Collection reminder
    if args.collection:
        print(
            f"REMINDER: Select the '{args.collection}' collection in Zotero before importing.",
            file=sys.stderr,
        )

    # Import or dry-run
    results = import_to_zotero(zotero_items, dry_run=args.dry_run)

    # Output
    output = {
        "total": len(results),
        "imported": sum(1 for r in results if r["status"] == "imported"),
        "errors": sum(1 for r in results if r["status"] == "error"),
        "results": results,
    }
    print(json.dumps(output, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
