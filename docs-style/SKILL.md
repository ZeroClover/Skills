---
name: docs-style
description: "Write, review, and lint developer documentation in the Google developer documentation style (developers.google.com/style). Use for READMEs, how-to guides, tutorials, concept guides, API and CLI references, troubleshooting guides, and other developer-facing Markdown. Covers voice, structure, procedures, code, UI text, terminology, inclusive language, and accessibility."
---

# Docs style

Write clear, direct, and friendly developer documentation so that readers can act on it the first time they read it.

Apply this style in whatever language the document uses. Rules tied to English grammar (contractions, capitalization, spelling) apply to English text.

Frame guidance around the desired wording, behavior, and result. Lead with the preferred version. Mention earlier wording only when an exact identifier, diagnosis, or quoted source requires it.

## Decision order

Use the following order when two guidelines differ:

1. Follow the user's request and the project's established terminology and style.
2. Choose the wording that best serves the document's readers, format, and accessibility needs.
3. Apply the [Google developer documentation style guide](https://developers.google.com/style).
4. Keep the chosen style consistent across the document.

Treat the guide as editorial guidance. A consistent project-specific choice can provide a better reader experience.

## Ten rules that cover most cases

1. **Talk to the reader as "you", in active voice.** Make the actor the subject: "The server updates the database." "You can export the report."
2. **Write in present tense.** "The function returns a token."
3. **Use sentence case for headings.** Capitalize the first word and proper nouns. Start task headings with a bare-infinitive verb: "Create an API key".
4. **Put the condition or location before the action.** "In the **Port** field, enter `8080`." "To start the server, run `npm start`."
5. **Bold UI labels and make navigation sequences accessible.** Use one bold span with accessible separators, or spell out the transitions: "In the **File** menu, select **New**, and then select **Document**."
6. **Format technical elements consistently.** Use code font for filenames, paths, commands, flags, variables, HTTP methods, and status codes: `config.yaml`, `--verbose`, `GET`, `200 OK`. Format replaceable inline values as *`PLACEHOLDER_NAME`*.
7. **Use the serial comma.** "HTML, CSS, and JavaScript."
8. **Make link text name the destination.** "See the [Cloud SDK installation guide](https://example.com/sdk)."
9. **State facts, capabilities, and boundaries.** "Handles 50,000 requests per second." "Names can contain up to 63 characters."
10. **Use inclusive terms and singular *they*.** `allowlist`, `denylist`, `primary`, `replica`.

## Workflow

### Write a new document

1. Pick the document type. Use the matching template when its structure fits the task:
   - Task or how-to guide: [assets/task-procedure.md](assets/task-procedure.md)
   - Concept or overview: [assets/concept-guide.md](assets/concept-guide.md)
   - Tutorial or quickstart: [assets/tutorial-quickstart.md](assets/tutorial-quickstart.md)
   - API or CLI reference: [assets/api-reference.md](assets/api-reference.md)
   - Troubleshooting guide: [assets/troubleshooting-guide.md](assets/troubleshooting-guide.md)
2. Draft with the ten rules. Read the relevant reference before writing format-specific details.
3. Resolve this skill directory to an absolute path, and lint the draft from any working directory:

   ```bash
   DOCS_STYLE_SKILL=/absolute/path/to/docs-style
   uv run --project "$DOCS_STYLE_SKILL/.." python "$DOCS_STYLE_SKILL/scripts/lint_docs.py" PATH
   ```

4. Review each reported match in context. Apply the suggested wording when it improves accuracy and clarity.
5. Read the document once in the order and environment that its reader will use.

### Review or refactor an existing document

1. Run the linter to collect candidate edits.
2. Read for structure: turn paragraphs that describe steps into numbered lists, and give each section a task-oriented heading.
3. Read for voice: make the actor the subject of each sentence, address the reader as "you", and move conditions ahead of actions.
4. Read for precision: name the link target in each link, format technical elements consistently, bold UI labels, and confirm that samples run as written.

## References

| Topic | File | Contents |
| :--- | :--- | :--- |
| Voice and tone | [references/voice-and-tone.md](references/voice-and-tone.md) | Person, voice, tense, recommendations, contractions, current features, factual tone, global audience |
| Formatting and structure | [references/formatting-and-structure.md](references/formatting-and-structure.md) | Headings, lists, procedures, tables, notices, numbers, dates, paragraphs, cross-references |
| Code and APIs | [references/code-and-apis.md](references/code-and-apis.md) | Inline code, code blocks, command lines, placeholders, example values, reference descriptions |
| UI and interaction | [references/ui-and-interaction.md](references/ui-and-interaction.md) | UI labels, accessible menu paths, interaction verbs, element context, keyboard input |
| Inclusive and accessible | [references/inclusive-and-accessible.md](references/inclusive-and-accessible.md) | Terminology, pronouns, links, images, tables, color, keyboard access |
| Word list and punctuation | [references/word-list-and-terminology.md](references/word-list-and-terminology.md) | Word choices, spelling, hyphenation, abbreviations, punctuation |

## Linter

`scripts/lint_docs.py` checks English Markdown prose for patterns that regular expressions can identify reliably: filler adverbs, hype, time-bound words, terminology, generic link text, Latin abbreviations, and heading punctuation. It skips fenced code blocks and inline code.

```bash
DOCS_STYLE_SKILL=/absolute/path/to/docs-style
uv run --project "$DOCS_STYLE_SKILL/.." python "$DOCS_STYLE_SKILL/scripts/lint_docs.py" docs/getting-started.md
uv run --project "$DOCS_STYLE_SKILL/.." python "$DOCS_STYLE_SKILL/scripts/lint_docs.py" docs/ --json
uv run --project "$DOCS_STYLE_SKILL/.." python "$DOCS_STYLE_SKILL/scripts/lint_docs.py" docs/ --strict --ignore-rules GDG-020
```

The exit code is 1 when errors are found, or when warnings are found with `--strict`. Treat each finding as a review prompt; the references and document context determine the final wording.
