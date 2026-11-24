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


@pytest.fixture
def paid_payment(stripe):
    # A successful £20.00 payment to refund (created and confirmed in one call)
    response = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={
            "amount": 2000,  # £20.00
            "currency": "gbp",
            "payment_method": "pm_card_visa",
            "confirm": "true",
            "automatic_payment_methods[enabled]": "true",
            "automatic_payment_methods[allow_redirects]": "never",
        },
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    payment = response.json()
    assert payment["status"] == "succeeded"
    return payment


def refund(stripe, payment_id, amount=None):
    data = {"payment_intent": payment_id}
    if amount is not None:
        data["amount"] = amount  # in pence
    return stripe.post(f"{STRIPE_URL}/refunds", data=data, timeout=TIMEOUT)


def amount_refunded(stripe, payment):
    # ASSUMPTION: the refunded total is stored on the payment's charge, not on the PaymentIntent
    charge = stripe.get(f"{STRIPE_URL}/charges/{payment['latest_charge']}", timeout=TIMEOUT)
    return charge.json()["amount_refunded"]


# --- Basic refund tests (written by AI) ---

def test_full_refund(stripe, paid_payment):
    response = refund(stripe, paid_payment["id"])  # no amount = refund everything

    assert response.status_code == 200, response.text
    body = response.json()
    assert body["object"] == "refund"
    assert body["amount"] == 2000
    assert body["status"] == "succeeded"  # ASSUMPTION: card refunds succeed immediately in test mode
    assert amount_refunded(stripe, paid_payment) == 2000


def test_partial_refund(stripe, paid_payment):
    response = refund(stripe, paid_payment["id"], amount=500)  # £5.00

    assert response.status_code == 200, response.text
    assert response.json()["amount"] == 500
    assert amount_refunded(stripe, paid_payment) == 500


# --- Edge cases (tester's scenarios) ---

def test_over_refund_is_rejected(stripe, paid_payment):
    response = refund(stripe, paid_payment["id"], amount=3000)  # £30 on a £20 payment

    assert response.status_code == 400, response.text  # ASSUMPTION: code not in the docs
    assert amount_refunded(stripe, paid_payment) == 0   # nothing was refunded


def test_partial_refunds_cannot_exceed_payment(stripe, paid_payment):
    first = refund(stripe, paid_payment["id"], amount=1500)   # £15
    second = refund(stripe, paid_payment["id"], amount=1000)  # £10 — only £5 left

    assert first.status_code == 200, first.text
    assert second.status_code == 400, second.text  # confirmed by running on 24 Nov
    assert amount_refunded(stripe, paid_payment) == 1500  # only the first refund went through