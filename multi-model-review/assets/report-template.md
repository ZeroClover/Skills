# Review report

- Run ID: {{run_id}}
- Round: {{round}}
- Reviewer: {{reviewer_name}} ({{harness}} / {{model}} / {{reasoning}})
- Stage: {{proposal | implementation | other}}
- Version: {{version_stamp}}
- Verdict: {{PASS | CHANGES_REQUIRED | INCOMPLETE}}

Keep the six header lines above exactly in this form; the orchestrator parses them and rejects a report whose Run ID, Round, Reviewer, Stage, or Version differs from the round, or whose Verdict is not exactly one token (PASS, CHANGES_REQUIRED, INCOMPLETE). Everything below is free-form, written in English; quote user requirements in their original language where the wording matters.

## Scope and verification

- Requirement coverage check: did the effective-requirements list in the brief faithfully cover the original user requests? Note any omission, drift, or unmarked interpretation.
- What you inspected (files, specs, commands, interfaces) and at which version.
- Verification you ran, with commands and actual results.
- What you could not verify, and why. An unverified area is reported as unverified, never as passing.

## Blocking issues

Issues that prevent acceptance of the current stage. Give each a stable ID (`{{reviewer_name}}-B1`, `-B2`, ...).

For every issue, in this stage of the workflow:
- Requirement or constraint it violates (quote or reference the source).
- Location and the condition under which it occurs.
- Expected versus actual behavior and the impact.
- Evidence: requirement text, spec, code path, interface fact, counterexample, or experiment result.

## Non-blocking findings

Improvements, risks, and inconsistencies that do not block acceptance (`{{reviewer_name}}-N1`, ...). Same evidence standard.

## Items to confirm

Important points you could not settle with available evidence (`{{reviewer_name}}-Q1`, ...). State what information or experiment would settle each.

## Conclusion

One or two sentences supporting the verdict. PASS means no blocking issues at the inspected version. CHANGES_REQUIRED means at least one blocking issue. INCOMPLETE means required verification could not be performed.
