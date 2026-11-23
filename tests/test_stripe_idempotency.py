import os
import uuid

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


def create_payment(stripe, idempotency_key, amount):
    # Create only — no confirm, so no money moves
    return stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={"amount": amount, "currency": "gbp"},  # amount in pence
        headers={"Idempotency-Key": idempotency_key},
        timeout=TIMEOUT,
    )


def test_same_key_same_params_returns_same_payment(stripe):
    key = f"qa-{uuid.uuid4()}"  # new unique key for every run

    first = create_payment(stripe, key, 2000)   # £20.00
    second = create_payment(stripe, key, 2000)  # same request again (a "retry")

    assert first.status_code == 200, first.text
    assert second.status_code == 200, second.text
    # Same PaymentIntent returned = only one payment exists
    assert second.json()["id"] == first.json()["id"]


def test_same_key_different_params_is_rejected(stripe):
    key = f"qa-{uuid.uuid4()}"

    first = create_payment(stripe, key, 2000)   # £20.00
    second = create_payment(stripe, key, 3000)  # £30.00 with the SAME key

    assert first.status_code == 200, first.text
    assert second.json()["error"]["type"] == "idempotency_error"
    assert second.status_code == 400  # ASSUMPTION: HTTP code not found in the docs