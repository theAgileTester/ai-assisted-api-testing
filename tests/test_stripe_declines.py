import os

import pytest
import requests

STRIPE_URL = "https://api.stripe.com/v1"
TIMEOUT = 10

# Source: https://docs.stripe.com/testing (Declined payments > PaymentMethods)
INSUFFICIENT_FUNDS_TOKEN = "pm_card_visa_chargeDeclinedInsufficientFunds"


@pytest.fixture(scope="session")
def stripe():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key or not key.startswith("sk_test_"):
        pytest.skip("STRIPE_SECRET_KEY missing or not a TEST key")
    session = requests.Session()
    session.auth = (key, "")
    return session


def test_insufficient_funds_decline(stripe):
    # Step 1: create a £30.00 payment with the insufficient-funds test card
    create = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={
            "amount": 3000,  # £30.00
            "currency": "gbp",
            "payment_method": INSUFFICIENT_FUNDS_TOKEN,
            "automatic_payment_methods[enabled]": "true",
            "automatic_payment_methods[allow_redirects]": "never",
        },
        timeout=TIMEOUT,
    )
    assert create.status_code == 200, create.text
    intent = create.json()

    # Step 2: status before confirming
    assert intent["status"] == "requires_confirmation"

    # Step 3: confirm — the card's bank declines it
    confirm = stripe.post(f"{STRIPE_URL}/payment_intents/{intent['id']}/confirm", timeout=TIMEOUT)
    assert confirm.status_code == 402, confirm.text
    error = confirm.json()["error"]
    assert error["code"] == "card_declined"
    assert error["decline_code"] == "insufficient_funds"

    # Step 4: no money was taken
    after = stripe.get(f"{STRIPE_URL}/payment_intents/{intent['id']}", timeout=TIMEOUT)
    assert after.status_code == 200, after.text
    assert after.json()["amount_received"] == 0
    assert after.json()["status"] == "requires_payment_method"  # ASSUMPTION: not in my expected results