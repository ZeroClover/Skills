import importlib.util
import unittest
from pathlib import Path


SCRIPT_PATH = Path(__file__).parents[1] / "skills" / "docs-style" / "scripts" / "lint_docs.py"
SPEC = importlib.util.spec_from_file_location("docs_style_linter", SCRIPT_PATH)
assert SPEC and SPEC.loader
LINTER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(LINTER)


class DocsStyleLinterTest(unittest.TestCase):
    def test_rules_expose_preferred_guidance(self) -> None:
        for rule in LINTER.RULES:
            self.assertIn("guidance", rule)
            self.assertNotIn("message", rule)
            self.assertNotIn("fix", rule)

    def test_context_dependent_prose_has_no_heuristic_findings(self) -> None:
        prose = [
            "However, research and testing continue.",
            "For example, Linux and macOS are supported.",
        ]

        for line in prose:
            matches = [
                rule["id"]
                for rule in LINTER.RULES
                if LINTER.re.search(rule["regex"], line, LINTER.re.IGNORECASE)
            ]
            self.assertEqual(matches, [], line)

    def test_heading_check_handles_product_names_and_title_case_as_context(self) -> None:
        for heading in ("# Use Visual Studio Code", "# Create Storage Bucket"):
            self.assertEqual(LINTER.check_heading(heading, 1, set()), [])

    def test_heading_punctuation_reports_positive_guidance(self) -> None:
        issues = LINTER.check_heading("# Configure the client:", 1, set())

        self.assertEqual([issue["rule_id"] for issue in issues], ["GDG-061"])
        self.assertEqual(issues[0]["severity"], "WARNING")
        self.assertIn("guidance", issues[0])
        self.assertNotIn("message", issues[0])
        self.assertNotIn("fix", issues[0])


if __name__ == "__main__":
    unittest.main()
