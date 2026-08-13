# SiteFlight report contract

Use this structure for every audit.

## 1. Verdict

State `READY`, `NOT READY`, or `BLOCKED` first. Name the tested environment and the date. Add one sentence explaining the decision.

## 2. Launch blockers

List only P0/P1 failures and launch-critical blocked checks. For each, name the affected page or system and the exact next action. Write `None` when there are none.

## 3. Coverage

Report counts for `PASS`, `FAIL`, `BLOCKED`, and `NOT APPLICABLE`. The counts must total 40.

## 4. Forty-check evidence table

Use these columns:

| ID | Check | Status | Severity | Evidence | Recommendation |
|---|---|---|---|---|---|

Evidence must identify its surface:

- `SOURCE`: file and line or configuration path
- `LOCAL`: local rendered URL, viewport, and interaction
- `PREVIEW`: preview URL and interaction
- `LIVE`: production URL and interaction
- `ACCOUNT`: named external system and observed state, without secrets
- `BLOCKED`: missing access or evidence

Do not write vague evidence such as “looks good” or “implemented.”

## 5. Fix order

Group concrete work into:

- `Before launch`: P0/P1 defects and critical blocked verification
- `First week`: useful P2 improvements with direct value
- `Later`: optional maturity work

Avoid repeating the evidence table. Combine related fixes into durable implementation batches.

## 6. Limits

Name what was not tested, including account access, production deployment, legal review, real form delivery, payment processing, analytics receipt, mobile devices, or search indexing. Omit a limit only when it was actually verified.

## Example verdict language

> NOT READY. The preview was tested on desktop and phone on 2026-08-13. The inquiry form does not expose an error state, the production analytics property could not be verified, and the service pages share duplicate titles.

Do not copy this example when those facts are not true.
