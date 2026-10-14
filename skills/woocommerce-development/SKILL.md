---
name: woocommerce-development
description: Apply WooCommerce compatibility and regression rules. Activate when wooCommerce is selected and cart, checkout or order behavior changes.
---
# Woocommerce Development

## Purpose
Apply WooCommerce compatibility and regression rules.

## Activation
WooCommerce is selected and cart, checkout or order behavior changes.

## Inputs
WordPress findings, checkout mode, HPOS state and affected components.

## Procedure
Read `.agd/adapters/woocommerce/governance.md`, `verification.md` and `regression-matrix.md`. Select affected rows, record fixtures and sandbox results.

## Constraints
No real payment, customer-data or live shipping-label side effects. Do not assume classic hooks work in Blocks.

## Outputs
Selected regression matrix and compatibility evidence.

## Completion
Relevant sandbox scenarios pass or unknown runtime compatibility is reported.

## Failure handling
Record the missing input or failed check. Stop dependent work, retain existing files,
and resume at the interrupted lifecycle state once the blocker is resolved.
