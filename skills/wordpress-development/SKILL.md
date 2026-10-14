---
name: wordpress-development
description: Apply WordPress development and verification rules. Activate when the selected adapter is WordPress and the task affects WordPress code.
---
# Wordpress Development

## Purpose
Apply WordPress development and verification rules.

## Activation
The selected adapter is WordPress and the task affects WordPress code.

## Inputs
Discovery results, relevant plugin/theme files and acceptance criteria.

## Procedure
Read `.agd/adapters/wordpress/governance.md` and `verification.md`. Determine ownership and request context, then use existing tests and tooling for the affected behavior.

## Constraints
Do not edit core/vendor code by default or equate nonces with authorization.

## Outputs
Scoped implementation and WordPress verification evidence.

## Completion
Applicable security and compatibility checks are addressed.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
