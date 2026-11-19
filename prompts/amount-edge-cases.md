# Prompt: amount edge cases (GBP and JPY)

Used on 19 Nov 2026 to generate `tests/test_stripe_amounts.py`.
Written by AI on a time-limited day; reviewed by the tester (see `AI_FINDINGS.md`, 19 Nov).

```markdown
## Role
You are a senior QA automation engineer testing a payments API.

## Context
- API: Stripe, test mode only. Base URL: https://api.stripe.com/v1
- Docs: https://docs.stripe.com/api/payment_intents/create
- Currencies, zero-decimal list and minimum amounts: https://docs.stripe.com/currencies
- Our project uses pytest + requests. Stripe expects form data (`data=`), not JSON.
- The secret key is read from the env variable STRIPE_SECRET_KEY.
- Existing pattern: a pytest fixture returns a requests.Session with the key
  in session.auth, so the key never appears in test output.

## Task
1. Generate amount edge-case test data for creating a PaymentIntent, using
   boundary value analysis, for two currencies:
   - GBP (a two-decimal currency)
   - JPY (a zero-decimal currency)
   For each currency, cover: below the minimum, exactly the minimum,
   just above the minimum, zero, a negative amount, and a decimal value.
2. Write one data-driven pytest test (pytest.mark.parametrize) that creates a
   PaymentIntent for each row and checks the HTTP status code.
   Use the test card pm_card_visa. Do not confirm the payments.

## Rules
- Take minimum amounts and the zero-decimal rule only from
  https://docs.stripe.com/currencies. If you cannot find a value there,
  write NOT FOUND and do not use a guess in the code — stop and ask.
- Amounts are in the currency's smallest unit. For GBP, 2000 = £20.00.
  For JPY there is no smaller unit: 500 = ¥500. Show the human amount in a comment.
- Every expected result must be one exact HTTP status code, not a range.
- Use only parameters that exist in the current Stripe API version.
- Never print, log or return the secret key.
- Skip the test if the key is missing or does not start with sk_test_.
- Mark anything you assumed without a source with # ASSUMPTION.

## Output
1. First, a table of the test data:
   case | currency | amount (smallest unit) | human amount | expected status | source link
2. Then one Python file, tests/test_stripe_amounts.py, with short comments.
3. After the code, list any assumptions you made.
```

## What I would change next time
- Add to Context: "Our Stripe account is in the UK and settles in GBP."
  (JPY ¥50 was rejected because it must also convert to at least 30p.)
- Add to Rules: "Avoid boundaries that depend on exchange rates — they make tests flaky."
