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


def check_error(response, status, error_type, code):
    # Every assert shows the real response, so we can compare it with the guess
    body = response.json()
    error = body.get("error", {})
    assert response.status_code == status, response.text
    assert error.get("type") == error_type, response.text
    assert error.get("code") == code, response.text


# --- 401: who are you? ---

def test_401_no_api_key():
    response = requests.post(f"{STRIPE_URL}/customers", timeout=TIMEOUT)  # no key at all
    check_error(response, 401, "invalid_request_error", None)  # guess confirmed 25 Nov


def test_401_invalid_api_key():
    response = requests.post(
        f"{STRIPE_URL}/customers",
        auth=("sk_test_this_key_does_not_exist", ""),  # fake key, safe to show
        timeout=TIMEOUT,
    )
    # Real response (25 Nov): no code field — AI had guessed "api_key_invalid"
    check_error(response, 401, "invalid_request_error", None)


# --- 400: your request is broken ---

def test_400_missing_amount(stripe):
    response = stripe.post(f"{STRIPE_URL}/payment_intents", data={"currency": "gbp"}, timeout=TIMEOUT)
    check_error(response, 400, "invalid_request_error", "parameter_missing")  # guess confirmed 25 Nov


def test_400_unknown_currency(stripe):
    response = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={"amount": 2000, "currency": "xyz"},  # not a real currency
        timeout=TIMEOUT,
    )
    # Real response (25 Nov): no code field, but param points to the wrong field — AI had guessed "invalid_currency"
    check_error(response, 400, "invalid_request_error", None)
    assert response.json()["error"]["param"] == "currency", response.text


# --- 402: request was fine, payment wasn't ---

def test_402_generic_card_decline(stripe):
    response = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={
            "amount": 2000,
            "currency": "gbp",
            "payment_method": "pm_card_visa_chargeDeclined",  # Source: https://docs.stripe.com/testing (Generic decline)
            "confirm": "true",
            "automatic_payment_methods[enabled]": "true",
            "automatic_payment_methods[allow_redirects]": "never",
        },
        timeout=TIMEOUT,
    )
    # KNOWN (19 Nov): declines return 402 + card_error + card_declined
    check_error(response, 402, "card_error", "card_declined")