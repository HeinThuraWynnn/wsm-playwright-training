# Implementation plan and review
Task ID: qa-training-20261014. Risk: standard for scaffold and disposable guest cart;
checkout/payments remain excluded. Adopt no stack adapter: Universal AGD currently only
validates WordPress/WooCommerce adapters, so Playwright constraints live in project docs.

| Criterion | Implementation | Verification |
|---|---|---|
| Preserve work and pin AGD | Exclusive initial writes; docs/agd-source.json; vendor runner | Empty-directory discovery; AGD validation |
| Planning and traceability | qa-strategy.md, test-cases.md | Self-review of R1–R6 and stable IDs |
| Isolated suites | tests/cart.spec.ts, playwright.config.ts | Typecheck, case discovery, live suite reports |
| Access governance | tests/support/fixtures.ts | Live access evidence, outcome unit tests |
| Honest reports | scripts/run.mjs, scripts/outcomes.mjs | RED/GREEN unit checks, retained run artifacts |
| Handoff | docs/handoff.md, .agd/evidence | Actual commands and status review |

Sequence: discovery → specification → plan → reporter RED/GREEN → fixture and cart
scaffold (documented TDD exception) → local gates → low-volume smoke → review → handoff.
No push, deployment, checkout or account operations. Installation and target writes are
within the user's project-build request. Rollback: remove only files created by this task
after preserving evidence and checking for subsequent user edits; no automatic deletion.

Self-review: one worker, zero retries, bounded test duration, fresh guest context, no
stored cookies, no arbitrary target URL or production credentials, no order submission.
Repeated challenges stop new navigation within this worker. HTTP 403/429/5xx and
navigation errors are BLOCKED. Unknown assertion/selector failures remain FAIL for triage.
Typecheck and discovery do not verify page selectors. Review was by the implementing
agent; no independent review is claimed.

TDD evidence: initial classifier tests returned exit 1 because implementation did not
exist, then four tests returned exit 0. A meaningful missing-browser regression test
subsequently returned exit 1 (FAIL vs expected BLOCKED); after the classifier change,
all five returned exit 0. Local gate evidence retains the final unit output. The first
live attempt failed at browser startup and exercised no application behavior; its raw
FAIL is retained, with an environment-blocker interpretation recorded in handoff.
