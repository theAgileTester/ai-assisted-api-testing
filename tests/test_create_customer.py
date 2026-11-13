import os

import requests

REQRES_URL = os.getenv("REQRES_URL", "https://reqres.in/api")


def test_create_customer():
    payload = {
        "first_name": "Jane",
        "last_name": "Doe",
        "email": "jane.doe@example.com",
    }

    response = requests.post(f"{REQRES_URL}/users", json=payload, timeout=10)

    body = response.json()
    assert body["first_name"] == payload["first_name"]
    assert body["last_name"] == payload["last_name"]
    assert body["email"] == payload["email"]
    assert body["id"], "id should not be empty"
    assert "createdAt" in body