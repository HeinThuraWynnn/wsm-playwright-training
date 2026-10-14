---
name: safe-refactoring
description: Change structure while preserving behavior. Activate when an authorized refactor has a defined purpose.
---
# Safe Refactoring

## Purpose
Change structure while preserving behavior.

## Activation
An authorized refactor has a defined purpose.

## Inputs
Scope, current behavior and baseline checks.

## Procedure
Establish passing baseline; make small structural steps, preserve contracts and run affected tests after each step. Inspect the final diff.

## Constraints
Do not bundle features or destructive migrations into refactors.

## Outputs
Focused diff and before/after verification.

## Completion
Behavior and public contracts remain verified.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
