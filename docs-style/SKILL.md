---
name: docs-style
description: "Write, review, and lint developer documentation in the Google developer documentation style (developers.google.com/style). Use when creating or editing READMEs, how-to guides, tutorials, concept guides, references for APIs and CLIs, troubleshooting guides, or any Markdown documentation. Covers voice, headings, procedures, code formatting, UI text, word choice, inclusive language, and accessibility."
---

# Docs style

Write developer documentation the way the Google developer documentation style guide describes it: clear, direct, and friendly, so that readers can act on it the first time they read it.

Apply this style in whatever language the document uses. Rules tied to English grammar (contractions, capitalization, spelling) apply to English text.

## Ten rules that cover most cases

1. **Talk to the reader as "you", in active voice.** Make the actor the subject: "The server updates the database." "You can export the report."
2. **Write in present tense.** "The function returns a token."
3. **Use sentence case for headings.** Capitalize the first word and proper nouns. Start task headings with a bare-infinitive verb: "Create an API key".
4. **Put the condition or location before the action.** "In the **Port** field, enter `8080`." "To start the server, run `npm start`."
5. **Bold UI labels, and write a menu path as one bold span.** "Click **File > New > Document**."
6. **Use code font for code.** Filenames, paths, commands, flags, variables, HTTP methods, and status codes: `config.yaml`, `--verbose`, `GET`, `200 OK`.
7. **Use the serial comma.** "HTML, CSS, and JavaScript."
8. **Make link text name the destination.** "See the [Cloud SDK installation guide](https://example.com/sdk)."
9. **State facts about what the product does.** Specifics replace adjectives: "Handles 50,000 requests per second."
10. **Use inclusive terms and singular *they*.** `allowlist`, `denylist`, `primary`, `replica`.

## Workflow

### Write a new document

1. Pick the document type and start from its template in `assets/`:
   - Task or how-to guide: `assets/task-procedure.md`
   - Concept or overview: `assets/concept-guide.md`
   - Tutorial or quickstart: `assets/tutorial-quickstart.md`
   - API or CLI reference: `assets/api-reference.md`
   - Troubleshooting guide: `assets/troubleshooting-guide.md`
2. Draft with the ten rules. Open the matching file in `references/` when a detailed question comes up.
3. Lint the draft with `python3 scripts/lint_docs.py PATH` (script path relative to this skill directory).
4. Resolve every reported item, then read the document once as the reader would.

### Review or refactor an existing document

1. Run the linter to get a first list.
2. Read for structure: turn paragraphs that describe steps into numbered lists, and give each section a task-oriented heading.
3. Read for voice: make the actor the subject of each sentence, address the reader as "you", and move conditions ahead of actions.
4. Read for precision: name the link target in each link, put code in code font, bold UI labels, and confirm that samples run as written.

## References

| Topic | File | Contents |
| :--- | :--- | :--- |
| Voice and tone | `references/voice-and-tone.md` | Person, voice, tense, condition-first sentences, contractions, timeless writing, factual tone, global audience |
| Formatting and structure | `references/formatting-and-structure.md` | Headings, lists, procedures, tables, notices, numbers, dates, paragraphs, cross-references |
| Code and APIs | `references/code-and-apis.md` | Inline code font, code blocks, command lines, placeholders, example values, reference descriptions |
| UI and interaction | `references/ui-and-interaction.md` | UI labels, menu paths, interaction verbs, locating elements, keyboard shortcuts |
| Inclusive and accessible | `references/inclusive-and-accessible.md` | Terminology, pronouns, link text, alt text, tables, color |
| Word list and punctuation | `references/word-list-and-terminology.md` | Word choices, spelling, hyphenation, abbreviations, punctuation |

## Linter

`scripts/lint_docs.py` checks Markdown prose for patterns that a regular expression can catch: filler adverbs, hype, time-bound words, terminology, link text, Latin abbreviations, and heading case. It skips fenced code blocks and inline code.

```bash
python3 scripts/lint_docs.py docs/getting-started.md
python3 scripts/lint_docs.py docs/ --json
python3 scripts/lint_docs.py docs/ --strict --ignore-rules GDG-050
```

The exit code is 1 when errors are found, or when warnings are found with `--strict`. Treat the output as a starting list; the references cover what the linter cannot see.
