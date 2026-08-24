#!/usr/bin/env python3
"""Lint Markdown prose against Google developer documentation style rules.

Usage:
    uv run --project SKILL_PARENT python lint_docs.py PATH [PATH ...] [--json] [--strict] [--ignore-rules IDS]

Fenced code blocks and inline code are skipped. Each finding names the rule,
the matched text, and the preferred wording.
"""

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any, Dict, List, Set

RULES = [
    {
        "id": "GDG-001",
        "name": "Filler adverbs",
        "severity": "WARNING",
        "regex": r"\b(simply|just|easily|easy|obviously|of course|clearly|very simple|a breeze|quickly)\b",
        "guidance": "Use a direct imperative or a measurable estimate of the work.",
    },
    {
        "id": "GDG-002",
        "name": "Hype",
        "severity": "WARNING",
        "regex": r"\b(robust|powerful|blazing[- ]fast|cutting-edge|industry-leading|ultra-fast|ultra-secure|seamless(?:ly)?|magic|super easy|best-in-class|world-class)\b",
        "guidance": "State a specification, number, or concrete capability.",
    },
    {
        "id": "GDG-010",
        "name": "Terminology: allowlist and denylist",
        "severity": "ERROR",
        "regex": r"\b(whitelist(?:ed|ing|s)?|blacklist(?:ed|ing|s)?)\b",
        "guidance": "Use 'allowlist' and 'denylist', or describe the allow and block behavior directly.",
    },
    {
        "id": "GDG-011",
        "name": "Terminology: primary and replica",
        "severity": "WARNING",
        "regex": r"\b(master|slave)\b",
        "guidance": "Use the technical relationship that fits the context, such as 'primary' / 'replica', 'main' / 'worker', or 'leader' / 'follower'. Preserve exact external identifiers in code font.",
    },
    {
        "id": "GDG-012",
        "name": "Terminology: other",
        "severity": "ERROR",
        "regex": r"\b(sanity check|dummy (?:data|value|values)|grandfathered|man-hours|manpower|tribal knowledge)\b",
        "guidance": "Choose the precise term for the context: 'smoke test', 'sample value', 'placeholder', 'legacy', 'person-hours', or 'institutional knowledge'.",
    },
    {
        "id": "GDG-020",
        "name": "Time-bound words",
        "severity": "WARNING",
        "regex": r"\b(currently|at present|as of now|at this time|in the future|soon|upcoming|recently|newly)\b",
        "guidance": "Describe stable behavior in present tense. State the version or date when timing carries meaning.",
    },
    {
        "id": "GDG-030",
        "name": "Link text",
        "severity": "ERROR",
        "regex": r"\[(click here|here|link|this link|this page|this doc|this document|read more|learn more|more info|more)\]\([^)]+\)",
        "guidance": "Use the title or subject of the destination as the link text.",
    },
    {
        "id": "GDG-040",
        "name": "Word list: cannot",
        "severity": "WARNING",
        "regex": r"\bcan not\b",
        "guidance": "Write 'cannot' as one word.",
    },
    {
        "id": "GDG-041",
        "name": "Word list: Latin abbreviations",
        "severity": "WARNING",
        "regex": r"(?<![\w.])(e\.g\.|i\.e\.|etc\.|vs\.)(?!\w)",
        "guidance": "Use 'for example', 'such as', 'that is', a complete list, or 'versus', according to the meaning.",
    },
    {
        "id": "GDG-042",
        "name": "Word list: and/or",
        "severity": "WARNING",
        "regex": r"\band/or\b",
        "guidance": "Write 'or', or state the inclusive choices as 'A, B, or both'.",
    },
    {
        "id": "GDG-043",
        "name": "Word list: filename",
        "severity": "WARNING",
        "regex": r"\bfile name\b",
        "guidance": "Write 'filename' as one word.",
    },
]

INLINE_CODE = re.compile(r"`+[^`]*`+")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")


def strip_inline_code(line: str) -> str:
    return INLINE_CODE.sub(" ", line)


def check_heading(line: str, line_num: int, ignored: Set[str]) -> List[Dict[str, Any]]:
    issues: List[Dict[str, Any]] = []
    match = re.match(r"^(#{1,6})\s+(.+?)\s*$", line.strip())
    if not match:
        return issues

    heading_text = match.group(2).strip()

    if "GDG-061" not in ignored and heading_text.endswith((".", ":", ";", "!")):
        issues.append({
            "rule_id": "GDG-061",
            "rule_name": "Heading punctuation",
            "severity": "WARNING",
            "line_number": line_num,
            "matched_text": heading_text,
            "guidance": "Use a short heading that ends with its final word. A genuine reader question can end with a question mark.",
        })

    return issues


def lint_file(path: Path, ignored: Set[str]) -> List[Dict[str, Any]]:
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as exc:
        return [{
            "rule_id": "GDG-ERR",
            "rule_name": "File read",
            "severity": "ERROR",
            "file": str(path),
            "line_number": 0,
            "matched_text": "",
            "guidance": f"Provide a readable path. The file operation returned: {exc}",
        }]

    issues: List[Dict[str, Any]] = []
    fence_char = ""
    fence_len = 0

    for line_num, line in enumerate(content.splitlines(), start=1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if not fence_char:
                fence_char, fence_len = marker[0], len(marker)
                continue
            if marker[0] == fence_char and len(marker) >= fence_len:
                fence_char, fence_len = "", 0
                continue
        if fence_char:
            continue

        if line.lstrip().startswith("#"):
            for issue in check_heading(line, line_num, ignored):
                issue["file"] = str(path)
                issues.append(issue)

        prose = strip_inline_code(line)
        for rule in RULES:
            if rule["id"] in ignored:
                continue
            for match in re.finditer(rule["regex"], prose, re.IGNORECASE):
                matched = match.group(0)
                issues.append({
                    "rule_id": rule["id"],
                    "rule_name": rule["name"],
                    "severity": rule["severity"],
                    "file": str(path),
                    "line_number": line_num,
                    "matched_text": matched,
                    "guidance": rule["guidance"],
                })

    return issues


def main() -> None:
    parser = argparse.ArgumentParser(description="Lint Markdown prose against Google developer documentation style rules.")
    parser.add_argument("paths", nargs="+", help="Markdown files or directories")
    parser.add_argument("--json", action="store_true", help="Print results as JSON")
    parser.add_argument("--strict", action="store_true", help="Exit with code 1 on warnings as well as errors")
    parser.add_argument("--ignore-rules", default="", help="Comma-separated rule IDs to skip")
    args = parser.parse_args()

    ignored = {r.strip() for r in args.ignore_rules.split(",") if r.strip()}

    files: List[Path] = []
    for raw in args.paths:
        path = Path(raw)
        if path.is_file() and path.suffix.lower() == ".md":
            files.append(path)
        elif path.is_dir():
            files.extend(sorted(path.rglob("*.md")))

    if not files:
        print("No Markdown files found." if not args.json else json.dumps({"scanned_files": 0, "total_issues": 0, "issues": []}))
        sys.exit(0)

    issues: List[Dict[str, Any]] = []
    for file in files:
        issues.extend(lint_file(file, ignored))

    errors = sum(1 for i in issues if i["severity"] == "ERROR")
    warnings = sum(1 for i in issues if i["severity"] == "WARNING")

    if args.json:
        print(json.dumps({"scanned_files": len(files), "total_issues": len(issues), "errors": errors, "warnings": warnings, "issues": issues}, indent=2))
    else:
        print(f"Checked {len(files)} Markdown file(s).")
        for issue in issues:
            badge = "ERROR  " if issue["severity"] == "ERROR" else "WARNING"
            print(f"\n{badge} {issue['file']}:{issue['line_number']} [{issue['rule_id']} {issue['rule_name']}]")
            print(f"  Match:    {issue['matched_text']}")
            print(f"  Guidance: {issue['guidance']}")
        print(f"\n{errors} error(s), {warnings} warning(s).")

    if errors or (args.strict and warnings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
