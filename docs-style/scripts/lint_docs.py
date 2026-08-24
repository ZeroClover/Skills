#!/usr/bin/env python3
"""Lint Markdown prose against Google developer documentation style rules.

Usage:
    python3 lint_docs.py PATH [PATH ...] [--json] [--strict] [--ignore-rules IDS]

Checks fenced code blocks and inline code are skipped. Each finding names the
rule, the matched text, and the preferred wording.
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
        "message": "'{match}' comments on difficulty. State the instruction on its own.",
        "fix": "Remove the word, or replace the sentence with a direct imperative.",
    },
    {
        "id": "GDG-002",
        "name": "Hype",
        "severity": "WARNING",
        "regex": r"\b(robust|powerful|blazing[- ]fast|cutting-edge|industry-leading|ultra-fast|ultra-secure|seamless(?:ly)?|magic|super easy|best-in-class|world-class)\b",
        "message": "'{match}' is a judgment. Give a measurable fact instead.",
        "fix": "Replace with a specification, number, or concrete capability.",
    },
    {
        "id": "GDG-010",
        "name": "Terminology: allowlist and denylist",
        "severity": "ERROR",
        "regex": r"\b(whitelist(?:ed|ing|s)?|blacklist(?:ed|ing|s)?)\b",
        "message": "Use 'allowlist' or 'denylist' in place of '{match}'.",
        "fix": "Replace with 'allowlist' / 'denylist' (or 'permitlist' / 'blocklist').",
    },
    {
        "id": "GDG-011",
        "name": "Terminology: primary and replica",
        "severity": "WARNING",
        "regex": r"\b(master|slave)\b",
        "message": "Use 'primary' / 'replica', 'main' / 'worker', or 'leader' / 'follower' in place of '{match}'. Keep external identifiers such as branch names in code font.",
        "fix": "Replace with the neutral pair that fits the context, or put an unavoidable identifier in code font.",
    },
    {
        "id": "GDG-012",
        "name": "Terminology: other",
        "severity": "ERROR",
        "regex": r"\b(sanity check|dummy (?:data|value|values)|grandfathered|man-hours|manpower|tribal knowledge)\b",
        "message": "Use a neutral term in place of '{match}'.",
        "fix": "Use 'smoke test' for 'sanity check', 'sample value' or 'placeholder' for 'dummy', 'legacy' for 'grandfathered', 'person-hours' for 'man-hours', 'institutional knowledge' for 'tribal knowledge'.",
    },
    {
        "id": "GDG-020",
        "name": "Time-bound words",
        "severity": "WARNING",
        "regex": r"\b(currently|at present|as of now|at this time|in the future|soon|upcoming|recently|newly)\b",
        "message": "'{match}' anchors the sentence to a moment. Describe the behavior as a plain present-tense fact.",
        "fix": "Remove the word, or state the version or date where timing matters.",
    },
    {
        "id": "GDG-030",
        "name": "Link text",
        "severity": "ERROR",
        "regex": r"\[(click here|here|link|this link|this page|this doc|this document|read more|learn more|more info|more)\]\([^)]+\)",
        "message": "Link text '{match}' reads the same for every link. Name the destination.",
        "fix": "Use the title or subject of the target page as the link text.",
    },
    {
        "id": "GDG-040",
        "name": "Word list: cannot",
        "severity": "WARNING",
        "regex": r"\bcan not\b",
        "message": "Use 'cannot' as one word.",
        "fix": "Change 'can not' to 'cannot'.",
    },
    {
        "id": "GDG-041",
        "name": "Word list: Latin abbreviations",
        "severity": "WARNING",
        "regex": r"(?<![\w.])(e\.g\.|i\.e\.|etc\.|vs\.)(?!\w)",
        "message": "Use plain English in place of '{match}'.",
        "fix": "Use 'for example' or 'such as' for 'e.g.', 'that is' for 'i.e.', a complete list or 'such as' for 'etc.', 'versus' for 'vs.'.",
    },
    {
        "id": "GDG-042",
        "name": "Word list: and/or",
        "severity": "WARNING",
        "regex": r"\band/or\b",
        "message": "Use 'or', or spell out 'A, B, or both'.",
        "fix": "Replace 'and/or' with 'or', or rephrase as 'A, B, or both'.",
    },
    {
        "id": "GDG-043",
        "name": "Word list: filename",
        "severity": "WARNING",
        "regex": r"\bfile name\b",
        "message": "Use 'filename' as one word.",
        "fix": "Change 'file name' to 'filename'.",
    },
    {
        "id": "GDG-044",
        "name": "Word list: please",
        "severity": "WARNING",
        "regex": r"\bplease\b",
        "message": "Instructions read more directly without 'please'.",
        "fix": "Remove 'please' and keep the imperative verb.",
    },
    {
        "id": "GDG-045",
        "name": "Word list: sign in",
        "severity": "WARNING",
        "regex": r"\b(log in|log into|logging in|logged in|log out|logging out|logged out)\b",
        "message": "Use 'sign in' / 'sign out' for the verb in place of '{match}'.",
        "fix": "Change 'log in' to 'sign in' and 'log out' to 'sign out'. Keep 'login' as a noun or adjective.",
    },
    {
        "id": "GDG-050",
        "name": "Serial comma",
        "severity": "WARNING",
        "regex": r"\b([A-Za-z0-9_-]+),\s+(?!(?:and|or|then|select|click|enter|run|open|choose|type|press|verify|which|but|so)\b)([A-Za-z0-9_-]+)\s+(and|or)\s+([A-Za-z0-9_-]+)\b",
        "message": "Possible series without a serial comma: '{match}'. This check is a heuristic.",
        "fix": "In a list of three or more, add a comma before 'and' or 'or': 'A, B, and C'.",
    },
]

PROPER_NOUNS = {
    "Node.js", "Python", "JavaScript", "TypeScript", "Go", "Rust", "Java", "Kotlin",
    "Google", "Cloud", "Docker", "Kubernetes", "Git", "GitHub", "GitLab", "Linux",
    "Windows", "Android", "Chrome", "Firebase", "PostgreSQL", "MySQL", "Redis",
    "Terraform", "Ansible", "Storage", "Run", "Functions", "Compute", "Engine",
}

FUNCTION_WORDS = {"with", "your", "from", "for", "the", "and", "under", "into", "to", "of", "in", "on", "a", "an"}

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
            "severity": "ERROR",
            "line_number": line_num,
            "matched_text": heading_text,
            "message": "Headings read best without end punctuation.",
            "fix": "Remove the trailing punctuation mark.",
        })

    if "GDG-060" in ignored:
        return issues

    clean = re.sub(r"`[^`]+`", "", heading_text)
    clean = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", clean)
    clean = re.sub(r"\[[^\]]+\]", "", clean)
    words = [w for w in re.split(r"[\s/:]+", clean.strip()) if w]
    if len(words) <= 1:
        return issues

    capitalized: List[str] = []
    for word in words[1:]:
        bare = word.strip("()\"'&,")
        if not bare:
            continue
        if bare.isupper() and len(bare) <= 6:
            continue
        if bare in PROPER_NOUNS:
            continue
        if bare[0].isupper() and bare[1:].islower():
            capitalized.append(bare)

    title_case = len(capitalized) >= 2 or (
        len(words) >= 3 and capitalized and capitalized[0].lower() in FUNCTION_WORDS
    )
    if title_case:
        issues.append({
            "rule_id": "GDG-060",
            "rule_name": "Heading sentence case",
            "severity": "WARNING",
            "line_number": line_num,
            "matched_text": heading_text,
            "message": f"Heading '{clean.strip()}' looks like title case. Sentence case capitalizes the first word and proper nouns.",
            "fix": "Lowercase the other words, keeping proper nouns and acronyms capitalized.",
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
            "message": f"Could not read the file: {exc}",
            "fix": "Check the path and permissions.",
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
                    "message": rule["message"].format(match=matched),
                    "fix": rule["fix"],
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
            print(f"  Text: {issue['matched_text']}")
            print(f"  Why:  {issue['message']}")
            print(f"  Fix:  {issue['fix']}")
        print(f"\n{errors} error(s), {warnings} warning(s).")

    if errors or (args.strict and warnings):
        sys.exit(1)
    sys.exit(0)


if __name__ == "__main__":
    main()
