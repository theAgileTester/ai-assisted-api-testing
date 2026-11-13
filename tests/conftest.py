import os

import pytest
from dotenv import load_dotenv

load_dotenv()


@pytest.fixture(scope="session")
def base_url():
    url = os.getenv("BASE_URL")
    if not url:
        pytest.fail("BASE_URL is not set. Copy .env.example to .env first.")
    return url.rstrip("/")
