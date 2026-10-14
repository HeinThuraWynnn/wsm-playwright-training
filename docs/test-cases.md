# Traceable test cases
Common setup: fresh isolated guest context, English demo, USD display, no saved session.
Access must succeed; Cloudflare means BLOCKED. Each case is independently reproducible.

| ID / requirement | Suites | Preconditions | Steps | Expected result |
|---|---|---|---|---|
| CART-001 / R1 | smoke, regression | Fresh cart | Open /cart | Shopping cart heading; empty message; zero product rows |
| CART-002 / R2 | smoke, sanity, regression | HTC One M8 Android L 5.0 available | Open product; add; open cart | Success notification; one matching product; quantity 1 |
| CART-003 / R3 | sanity, regression | Independently add product | Capture unit price; set quantity 2; update | Quantity 2; displayed line subtotal equals unit × 2 in cents |
| CART-004 / R4 | sanity, regression | Independently add product | Check removal; update | Zero rows and empty cart message |
| CART-005 / R5 | regression | Independently add product | Reload cart | Same product and quantity 1 remain |

Implementation: tests/cart.spec.ts. The title carries the stable ID; tags select suites.
CART-003 checks a line subtotal, not tax, shipping or payable order total.
Product availability and selectors require live verification. Missing products are setup
issues to triage, not automatic evidence that cart logic failed. Do not silently skip them.
