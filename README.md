# AGD-governed Playwright QA training
Guest cart training for https://demo.nopcommerce.com/cart using the user's Universal AGD 2.1.
Start with docs/qa-strategy.md and docs/test-cases.md. Governance is in AGENTS.md and .agd/.

## Setup and execution
Node.js and npm are required. From this directory:
```sh
npm ci
npx playwright install chromium
npm run typecheck
npm run test:unit
npm run test:list
npm run test:smoke
npm run test:sanity
npm run test:regression
npm run report
```
Use governed npm suite commands for classification and retained evidence. Direct Playwright
can exit zero on skipped cases; that is not proof of cart functionality.
One worker, no retries, fresh guest contexts, no checkout and no challenge bypass.
If Cloudflare appears, stop and record BLOCKED. A human may inspect the site manually;
that inspection does not establish an automation pass or authorize bypass techniques.

## AGD checks
The pinned runner is vendor/universal-agd/agd.py; provenance is in docs/agd-source.json.
Only local gates are configured; live suites are deliberate manual invocations.
```sh
python3 vendor/universal-agd/agd.py validate
python3 vendor/universal-agd/agd.py verify --task local-unique-id --trust-config
```
Review .agd/framework.json before trusting it. Use a new task ID per verification.
An AGD gate pass establishes only that gate's result, not full acceptance or E2E coverage.
See docs/handoff.md for actual validation and limitations.
