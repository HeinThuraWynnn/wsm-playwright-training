---
name: documentation
description: Update maintained documentation for changed behavior. Activate when contracts, setup, usage or architecture have changed.
---
# Documentation

## Purpose
Update maintained documentation for changed behavior.

## Activation
Contracts, setup, usage or architecture have changed.

## Inputs
Final implementation, verified commands and affected documents.

## Procedure
Update canonical sources and examples; check local links, avoid duplicate policies, record significant decisions as ADRs.

## Constraints
Do not describe unfinished functionality as available.

## Outputs
Accurate docs and any required ADR.

## Completion
Examples match the implemented contract and limitations are explicit.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
