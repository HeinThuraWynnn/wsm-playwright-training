# QA strategy and test plan
Target: https://demo.nopcommerce.com/cart. Scope: guest cart behavior on Chromium desktop.
This is a training framework, not certification of a public demo's release quality.

## Discovery and requirements
The requested directory was empty and not a Git repository on 2026-10-14.
Node 26.5.0 and npm 11.17.0 were detected. No CI or previous tests existed.
Parent AGENTS.md describes Clamora; the explicit user scope selects Playwright instead.
Universal AGD 2.1 is adopted from commit 38dc7df2bd7963442cd6fd52d120929cb50a1ebc,
with no source changes observed. No WordPress/WooCommerce adapter is selected.
The product path, English UI, USD formatting and selectors are provisional until live access
allows inspection. Expected results below are test oracles, not observed test outcomes.

## Acceptance criteria
1. Preserve existing work; adopt pinned AGD policies and reviewed local gates.
2. Provide strategy, plan, stable case IDs and suite-to-requirement traceability.
3. Implement independent smoke, sanity and regression cases with fresh guest contexts.
4. Classify Cloudflare/HTTP access restrictions as BLOCKED; never automate challenges.
5. Preserve timestamped reports and fail the governed command when blocked or incomplete.
6. Record executed validation separately from unverified target functionality.

## Requirements and coverage
| Requirement | Risk | Cases |
|---|---|---|
| R1 Empty guest cart is clear and contains no rows | medium | CART-001 |
| R2 Adding a simple product yields one correct row | high | CART-002 |
| R3 Updating quantity recalculates line subtotal | high | CART-003 |
| R4 Removing an item empties this guest cart | high | CART-004 |
| R5 Guest cart survives a page reload | medium | CART-005 |
| R6 Access blockers cannot appear as functional passes | high | local outcome tests, access fixture |

## Execution plan
1. Validate AGD configuration, unit checks and TypeScript, then discover cases with --list.
2. Attempt smoke once, with one worker and zero retries. Stop further navigation after
   a challenge, denied/rate-limited response or navigation outage. Do not solve CAPTCHA.
3. If accessible, review DOM assumptions; run sanity after cart changes and regression
   before handoff. Run suites serially; do not schedule recurring public-site traffic.
4. Review failure screenshots/traces to distinguish locator drift, environment issues,
   data availability and genuine application defects. Never relabel an unexplained
   assertion failure as an access blocker.
5. A functional release recommendation requires all selected cases actually passing,
   no unresolved blockers, and reviewed evidence. Listing/compilation is not E2E success.

Smoke: empty cart and add product. Sanity: targeted add/update/remove checks, selected
for cart changes. Regression: all five cases. Every case gets a new browser context;
no accounts or shared storage are used. Additions/removals affect only this disposable
guest session. Quantities stay at 1–2. No checkout, orders, payments, registration,
admin changes, fuzzing, load testing or real customer data are in scope.

## Deferred manual coverage
CART-M01: invalid quantities (0, negative, nonnumeric, maximum) — confirm application
contract before automation. CART-M02: discounts, tax, shipping and total — requires
controlled data and authoritative expected rules. CART-M03: terms/checkout validation —
stop before order submission; use a controlled environment. CART-M04: keyboard/mobile/
cross-browser behavior — extend after baseline is validated. These are NOT RUN.

## Evidence and defect handling
Governed suite commands create evidence/<UTC timestamp>-<suite>/execution.log,
playwright.json and summary.json. Playwright HTML, traces and screenshots are local
artifacts. JSON maps IDs to PASS, FAIL, BLOCKED or NOT RUN; exit 2 means blocked and
exit 1 means failure/incomplete. Unexpected runner errors cannot produce a pass.
Traces/screenshots may contain session details: inspect before sharing, never commit
cookies or credentials. Retain each run directory; current test-results and HTML may
be replaced by a subsequent run. Copy supporting binary artifacts into the run directory.
Defect reports must include case/requirement ID, reproduction, expected/actual result,
run path, environment and severity. Access incidents are separate environment tickets.

## Constraints and TDD
The report classifier uses RED→GREEN unit evidence. A missing-module RED demonstrates
an absent implementation, not a target application defect. Live E2E test definitions
have a TDD exception: this project does not own nopCommerce application code and cannot
force a known defect safely. No E2E green claim is made without an actual run.
