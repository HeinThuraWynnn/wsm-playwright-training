---
name: handoff
description: Prepare a concise evidence-based continuity report. Activate when a task is complete or must be handed back blocked.
---
# Handoff

## Purpose
Prepare a concise evidence-based continuity report.

## Activation
A task is complete or must be handed back blocked.

## Inputs
Scope, acceptance status, diff, check results and approvals.

## Procedure
Use `.agd/templates/handoff.md`; list commands and results, changed files, unverified behavior, approval decisions, blockers and next actions. Distinguish framework validation from target application testing.

## Constraints
Do not label blocked work complete or omit skipped checks.

## Outputs
Reviewable handoff with evidence references.

## Completion
Another person can assess completion and resume unresolved work.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
