---
name: bug-diagnosis
description: Identify the cause of a defect before fixing it. Activate when a failure has an uncertain cause.
---
# Bug Diagnosis

## Purpose
Identify the cause of a defect before fixing it.

## Activation
A failure has an uncertain cause.

## Inputs
Reproduction, expected behavior and repository findings.

## Procedure
Reproduce safely, trace affected data and boundaries, test competing explanations, then add a regression case and hand it to the TDD procedure.

## Constraints
Do not modify unrelated components or infer runtime state from source alone.

## Outputs
Reproduction and supported causal explanation.

## Completion
A regression case distinguishes the cause from symptoms.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
