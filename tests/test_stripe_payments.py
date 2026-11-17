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


def test_successful_payment_intent_flow(stripe):
    # Step 1: create the payment with a test card attached, but don't confirm yet
    create = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={
            "amount": 2000,
            "currency": "gbp",
            "payment_method": "pm_card_visa",
            "automatic_payment_methods[enabled]": "true",
            "automatic_payment_methods[allow_redirects]": "never",
        },
        timeout=TIMEOUT,
    )
    assert create.status_code == 200, create.text
    intent = create.json()
    assert intent["amount"] == 2000
    assert intent["currency"] == "gbp"
    assert intent["status"] == "requires_confirmation"
    assert intent["amount_received"] == 0

    # Step 2: confirm the payment
    confirm = stripe.post(f"{STRIPE_URL}/payment_intents/{intent['id']}/confirm", timeout=TIMEOUT)
    assert confirm.status_code == 200, confirm.text
    confirmed = confirm.json()
    assert confirmed["status"] == "succeeded"
    assert confirmed["amount_received"] == 2000