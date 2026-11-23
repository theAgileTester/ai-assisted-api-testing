import os
import uuid

import pytest
import requests

STRIPE_URL = "https://api.stripe.com/v1"
TIMEOUT = 10


@pytest.fixture(scope="session")
def stripe():
    # The key lives inside the session, so it never appears in test output
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key or not key.startswith("sk_test_"):
        pytest.skip("STRIPE_SECRET_KEY missing or not a TEST key")
    session = requests.Session()
    session.auth = (key, "")
    return session


@pytest.fixture
def customer(stripe):
    email = f"qa-{uuid.uuid4().hex[:8]}@example.com"
    response = stripe.post(
        f"{STRIPE_URL}/customers",
        data={"name": "Jane Doe", "email": email},
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    created = response.json()

    yield created

    stripe.delete(f"{STRIPE_URL}/customers/{created['id']}", timeout=TIMEOUT)


def test_create_customer(customer):
    assert customer["id"].startswith("cus_")
    assert customer["object"] == "customer"
    assert customer["name"] == "Jane Doe"
    assert customer["email"].startswith("qa-")
    assert customer["livemode"] is False


def test_read_customer(customer, stripe):
    response = stripe.get(f"{STRIPE_URL}/customers/{customer['id']}", timeout=TIMEOUT)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == customer["id"]
    assert body["email"] == customer["email"]


def test_update_customer(customer, stripe):
    response = stripe.post(
        f"{STRIPE_URL}/customers/{customer['id']}",
        data={"name": "Jane Smith"},
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Jane Smith"


def test_delete_customer(customer, stripe):
    response = stripe.delete(f"{STRIPE_URL}/customers/{customer['id']}", timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["deleted"] is True

    # Confirmed by running (16 Nov): reading a deleted customer returns deleted=true
    after = stripe.get(f"{STRIPE_URL}/customers/{customer['id']}", timeout=TIMEOUT)
    assert after.json().get("deleted") is True
