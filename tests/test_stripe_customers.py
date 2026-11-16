import os
import uuid

import pytest
import requests

STRIPE_URL = "https://api.stripe.com/v1"
TIMEOUT = 10


@pytest.fixture(scope="session")
def stripe_auth():
    key = os.getenv("STRIPE_SECRET_KEY")
    if not key or not key.startswith("sk_test_"):
        pytest.skip("STRIPE_SECRET_KEY missing or not a TEST key")
    return (key, "")


@pytest.fixture
def customer(stripe_auth):
    email = f"qa-{uuid.uuid4().hex[:8]}@example.com"
    response = requests.post(
        f"{STRIPE_URL}/customers",
        data={"name": "Jane Doe", "email": email},
        auth=stripe_auth,
        timeout=TIMEOUT,
    )
    assert response.status_code == 200, response.text
    created = response.json()

    yield created

    requests.delete(f"{STRIPE_URL}/customers/{created['id']}", auth=stripe_auth, timeout=TIMEOUT)


def test_create_customer(customer):
    assert customer["id"].startswith("cus_")
    assert customer["object"] == "customer"
    assert customer["name"] == "Jane Doe"
    assert customer["email"].startswith("qa-")
    assert customer["livemode"] is False


def test_read_customer(customer, stripe_auth):
    response = requests.get(f"{STRIPE_URL}/customers/{customer['id']}", auth=stripe_auth, timeout=TIMEOUT)

    assert response.status_code == 200
    body = response.json()
    assert body["id"] == customer["id"]
    assert body["email"] == customer["email"]


def test_update_customer(customer, stripe_auth):
    response = requests.post(
        f"{STRIPE_URL}/customers/{customer['id']}",
        data={"name": "Jane Smith"},
        auth=stripe_auth,
        timeout=TIMEOUT,
    )

    assert response.status_code == 200
    assert response.json()["name"] == "Jane Smith"


def test_delete_customer(customer, stripe_auth):
    response = requests.delete(f"{STRIPE_URL}/customers/{customer['id']}", auth=stripe_auth, timeout=TIMEOUT)

    assert response.status_code == 200
    assert response.json()["deleted"] is True

    # [ASSUMPTION] reading a deleted customer still returns 200 with deleted=true
    after = requests.get(f"{STRIPE_URL}/customers/{customer['id']}", auth=stripe_auth, timeout=TIMEOUT)
    assert after.json().get("deleted") is True