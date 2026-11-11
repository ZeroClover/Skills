# Review report

- Run ID: {{run_id}}
- Round: {{round}}
- Reviewer: {{reviewer_name}} ({{harness}} / {{model}} / {{reasoning}})
- Stage: {{proposal | implementation | other}}
- Version: {{version_stamp}}
- Verdict: {{PASS | CHANGES_REQUIRED | INCOMPLETE}}

Keep the six header lines above exactly in this form. The orchestrator parses them and accepts the report when Run ID, Round, Reviewer, Stage, and Version match the round and Verdict is exactly one token: PASS, CHANGES_REQUIRED, or INCOMPLETE. Write the rest in English, quoting user requirements in their original language where the wording matters. Write each item as one direct claim followed by its evidence, so the orchestrator can check it straight from the report.

## Scope and verification

- Requirement coverage: whether the brief's effective-requirements list faithfully covers the original user requests; name each omission, drift, or unmarked interpretation.
- Inspected: files, specs, commands, and interfaces, with the version.
- Verification run: each command with its actual result.
- Unverified: each area you could not check, with the reason, so it is counted as unverified.

## Blocking issues

Issues that prevent acceptance of the current stage. Give each a stable ID (`{{reviewer_name}}-B1`, `-B2`, ...) and state:

- Requirement or constraint it violates, quoted or referenced to its source.
- Location and the condition under which it occurs.
- Expected versus actual behavior, and the impact.
- Evidence in its most direct form: a quoted requirement or spec line, a `file:line`, a command with its actual output, or a minimal counterexample.

## Non-blocking findings

Improvements, risks, and inconsistencies that do not block acceptance (`{{reviewer_name}}-N1`, ...), with the same fields.

## Items to confirm

Important points you could not settle with available evidence (`{{reviewer_name}}-Q1`, ...). State what information or experiment would settle each.

## Conclusion

The verdict and the issue IDs it rests on. PASS means no blocking issues at the inspected version. CHANGES_REQUIRED means at least one blocking issue. INCOMPLETE means required verification could not be performed.
