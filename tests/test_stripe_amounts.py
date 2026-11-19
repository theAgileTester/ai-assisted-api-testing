import os

import pytest
import requests

STRIPE_URL = "https://api.stripe.com/v1"
TIMEOUT = 10


@pytest.fixture(scope="session")
def stripe():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key or not key.startswith("sk_test_"):
        pytest.skip("STRIPE_SECRET_KEY missing or not a TEST key")
    session = requests.Session()
    session.auth = (key, "")
    return session


# Minimums from https://docs.stripe.com/currencies (found by the tester):
# GBP 0.30 -> 30 pence; JPY 50 -> 50 (zero-decimal, no smaller unit)
AMOUNT_CASES = [
    # (case id, currency, amount in smallest unit, expected status)
    ("gbp_below_min", "gbp", 29, 400),      # £0.29
    ("gbp_exact_min", "gbp", 30, 200),      # £0.30
    ("gbp_above_min", "gbp", 31, 200),      # £0.31
    ("gbp_zero", "gbp", 0, 400),            # £0.00
    ("gbp_negative", "gbp", -100, 400),     # -£1.00  # ASSUMPTION
    ("gbp_decimal", "gbp", "30.5", 400),    # not an integer  # ASSUMPTION
    # JPY: our account settles in GBP, so a JPY amount must ALSO convert to at least 30p.
    # Exchange rates change, so we avoid testing the exact converted boundary (flaky).
    ("jpy_below_currency_min", "jpy", 49, 400),           # ¥49 — below the JPY minimum (¥50)
    ("jpy_currency_min_below_gbp_min", "jpy", 50, 400),   # ¥50 ≈ £0.24 — below 30p (zero-decimal confirmed)
    ("jpy_safely_above_min", "jpy", 200, 200),            # ¥200 — above 30p at any realistic rate
    ("jpy_zero", "jpy", 0, 400),            # ¥0
    ("jpy_negative", "jpy", -100, 400),     # -¥100  # ASSUMPTION
    ("jpy_decimal", "jpy", "50.5", 400),    # not an integer  # ASSUMPTION
]


@pytest.mark.parametrize(
    "currency, amount, expected_status",
    [case[1:] for case in AMOUNT_CASES],
    ids=[case[0] for case in AMOUNT_CASES],
)
def test_payment_intent_amount_limits(stripe, currency, amount, expected_status):
    # Create only — the payment is not confirmed
    response = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={
            "amount": amount,
            "currency": currency,
            "payment_method": "pm_card_visa",
            "automatic_payment_methods[enabled]": "true",
            "automatic_payment_methods[allow_redirects]": "never",
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == expected_status, response.text