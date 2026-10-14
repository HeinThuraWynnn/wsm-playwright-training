---
name: tdd
description: Develop executable behavior with regression evidence. Activate when changing behavior or fixing an executable defect.
---
# Tdd

## Purpose
Develop executable behavior with regression evidence.

## Activation
Changing behavior or fixing an executable defect.

## Inputs
Acceptance criteria and existing test tools.

## Procedure
Write the smallest behavioral test. Run it and confirm the intended failure. Implement minimum behavior, rerun, then refactor and rerun affected checks. Record commands and output.

## Constraints
Do not test destructive operations on real installations. Explain any TDD exception.

## Outputs
RED and GREEN evidence, code and tests.

## Completion
Relevant regression checks pass with no hidden failures.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
