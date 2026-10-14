---
name: planning
description: Plan a small complete implementation. Activate when a specified task needs more than a trivial edit.
---
# Planning

## Purpose
Plan a small complete implementation.

## Activation
A specified task needs more than a trivial edit.

## Inputs
Accepted criteria, discovered architecture and tooling.

## Procedure
Map criteria to files and checks; classify risk, identify approvals and rollback needs. Select the relevant adapter. Order changes so each step is reviewable.

## Constraints
Do not mandate delegation or broad restructuring.

## Outputs
Scoped steps, risk classification and gate selection.

## Completion
Each criterion has a planned verification mechanism.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
