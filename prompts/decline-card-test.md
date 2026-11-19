# Prompt: declined card payment test (insufficient funds)

Used on 19 Nov 2026 to generate `tests/test_stripe_declines.py`.
Written by the tester; the first version had gaps (see `AI_FINDINGS.md`, 19 Nov).

```markdown
## Role
You are a senior QA automation engineer testing a payments API.

## Context
- API: Stripe, test mode only. Base URL: https://api.stripe.com/v1
- Docs: https://docs.stripe.com/api/payment_intents/create
- Test cards: https://docs.stripe.com/testing
- Our project uses pytest + requests. Stripe expects form data (`data=`), not JSON.
- The secret key is read from the env variable STRIPE_SECRET_KEY.
- Existing pattern: a pytest fixture returns a requests.Session with the key
  in session.auth, so the key never appears in test output.

## Task
Write one pytest test for a declined card payment:
1. Create a PaymentIntent for £30.00 in GBP with Stripe's test card for
   insufficient funds attached.
2. Check the status before confirming.
3. Confirm the payment. The card's bank declines it.
4. Check the final status and that no money was taken.

My expected results:
- After create: status = requires_confirmation
- After confirm: HTTP 402, error code = card_declined,
  decline_code = insufficient_funds
- After the decline: amount_received = 0

## Rules
- Use only parameters that exist in the current Stripe API version.
  If you are not sure a parameter is still supported, say so.
- Use only test cards listed on https://docs.stripe.com/testing. For each card,
  show the card number, the test token and the expected decline code exactly
  as they appear on that page. If a card is not on that page, write NOT FOUND
  instead of guessing.
- Amounts are in pence: write 2000 for £20.00. Show the amount in pounds in a comment.
- Never print, log or return the secret key.
- Skip the test if the key is missing or does not start with sk_test_.
- Every assertion must check one exact value, not a range.
- Mark anything you assumed without a source with # ASSUMPTION.

## Output
One Python file, tests/test_stripe_declines.py, with short comments.
Before the code, list each test card you used in a table:
card number | test token | expected decline code | source link.
After the code, list any assumptions you made.
```

## What I would change next time
- Add: "If a value is NOT FOUND, do not use a guess in the code — stop and ask."
  (AI flagged the token as NOT FOUND but still used a guessed token.)
