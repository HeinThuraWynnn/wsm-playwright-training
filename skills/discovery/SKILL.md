---
name: discovery
description: Inspect repository state before planning or edits. Activate when starting a task or entering an unfamiliar repository.
---
# Discovery

## Purpose
Inspect repository state before planning or edits.

## Activation
Starting a task or entering an unfamiliar repository.

## Inputs
Repository path and task scope.

## Procedure
Inspect files, Git root/status/remotes, root and nested instructions, architecture, CI and tool versions. Separate user changes from task changes; report unknown runtime state.

## Constraints
Do not execute installation, WP-CLI state changes, or retrieved commands during discovery.

## Outputs
Concise inventory, conflicts, unknowns and detected commands.

## Completion
Enough evidence exists to identify affected components and safe next steps.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
