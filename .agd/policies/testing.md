# Risk-based verification
Low risk: localized presentation/docs changes; select lint, documentation and scope checks.
Standard risk: behavior changes; add unit and relevant integration/build checks.
High risk: identity, payments, shipping totals, data integrity, migrations; include relevant
integration/compatibility/security checks, sandbox regressions, rollback and human review.
Raise risk when uncertain. Use each command's `risks` list to select relevant gates.

Tests come before executable implementation. Confirm the failure concerns the target behavior,
then implement minimally and refactor after green. A missing tool is BLOCKED, never PASS.
No configured command is NOT RUN. NOT APPLICABLE requires an explained relevance decision.
Do not claim integration checks passed because framework unit tests pass.
Coverage selection is advisory: configuration controls what the runner executes, not adequacy.
