import json
import os
from pathlib import Path

import pytest
import requests

STRIPE_URL = "https://api.stripe.com/v1"
TIMEOUT = 10
SCHEMA = json.loads((Path(__file__).parent.parent / "schemas" / "payment_intent.schema.json").read_text())


@pytest.fixture(scope="session")
def stripe():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key or not key.startswith("sk_test_"):
        pytest.skip("STRIPE_SECRET_KEY missing or not a TEST key")
    session = requests.Session()
    session.auth = (key, "")
    return session


def test_compare_ai_schema_with_real_payment_intent(stripe):
    response = stripe.post(
        f"{STRIPE_URL}/payment_intents",
        data={"amount": 2000, "currency": "gbp"},  # create only, no money moves
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    real_fields = set(response.json().keys())
    ai_fields = set(SCHEMA["properties"].keys())

    invented = sorted(ai_fields - real_fields)  # in the AI schema, not in the real response
    missed = sorted(real_fields - ai_fields)    # in the real response, not in the AI schema

    print("\nINVENTED by AI:", invented)
    print("MISSED by AI:", missed)

    # The AI's required fields must really exist
    assert set(SCHEMA["required"]) <= real_fields