import requests

TIMEOUT = 10


def test_latest_returns_200_and_expected_fields(base_url):
    response = requests.get(f"{base_url}/latest", timeout=TIMEOUT)

    assert response.status_code == 200
    body = response.json()
    assert set(body.keys()) == {"amount", "base", "date", "rates"}


def test_usd_to_gbp_returns_only_gbp(base_url):
    response = requests.get(
        f"{base_url}/latest", params={"base": "USD", "symbols": "GBP"}, timeout=TIMEOUT
    )

    assert response.status_code == 200
    body = response.json()
    assert body["base"] == "USD"
    assert list(body["rates"].keys()) == ["GBP"]


def test_invalid_base_currency_returns_4xx(base_url):
    response = requests.get(f"{base_url}/latest", params={"base": "XXX"}, timeout=TIMEOUT)

    assert 400 <= response.status_code < 500
