---
name: verification
description: Run selected quality gates and record results. Activate when code or documentation is ready for checks.
---
# Verification

## Purpose
Run selected quality gates and record results.

## Activation
Code or documentation is ready for checks.

## Inputs
Reviewed configuration, detected commands and risk.

## Procedure
Validate config, inspect command argv and trust boundary, select relevant gates, run in a safe environment, record actual output and statuses. Explain missing tools and unverified behavior.

## Constraints
Do not assert results without execution. Never run real payment tests.

## Outputs
Machine evidence plus an adequacy review of selected checks.

## Completion
Applicable gates pass or remaining blockers are clearly reported.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
