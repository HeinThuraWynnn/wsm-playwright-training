---
name: code-review
description: Review changes against criteria and risk. Activate when implementation is ready for review or review is the task.
---
# Code Review

## Purpose
Review changes against criteria and risk.

## Activation
Implementation is ready for review or review is the task.

## Inputs
Diff, acceptance criteria, baseline and evidence.

## Procedure
Inspect changed paths and callers for correctness, security, compatibility and scope. Prioritize actionable findings. An independent reviewer is useful when available; single-agent review remains supported.

## Constraints
Do not treat generated evidence as proof of provenance or claim independent review when self-reviewing.

## Outputs
Findings with file references, severity and unresolved risk.

## Completion
Blocking findings are resolved or explicitly handed back as blocked.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
