"""
Pytest configuration and fixtures for AI Virtual Agent tests
"""

import pytest
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from .config import config


@pytest.fixture(scope="session")
def test_config():
    """
    Test configuration fixture
    """
    config.print_config()
    return config


@pytest.fixture(scope="session")
def api_session():
    """
    Create a requests session with retry logic for API calls
    """
    session = requests.Session()

    # Configure retry strategy
    retry_strategy = Retry(
        total=config.MAX_RETRIES,
        backoff_factor=1,
        status_forcelist=[429, 500, 502, 503, 504],
    )

    adapter = HTTPAdapter(max_retries=retry_strategy)
    session.mount("http://", adapter)
    session.mount("https://", adapter)

    # Set default timeout
    session.timeout = config.REQUEST_TIMEOUT

    return session


@pytest.fixture(scope="session")
def api_endpoints(test_config):
    """
    API endpoints fixture
    """
    return test_config.get_endpoints()


@pytest.fixture(scope="session")
def service_urls(test_config):
    """
    Service URLs fixture
    """
    return test_config.get_service_urls()


@pytest.fixture(scope="session")
def base_url(test_config):
    """
    Base URL for API calls (frontend)
    """
    return test_config.FRONTEND_URL


# Who is the first president of the united states?


@pytest.fixture(scope="session")
def backend_url(test_config):
    """
    Backend URL for direct API calls
    """
    return test_config.BACKEND_URL


@pytest.fixture(scope="session")
def llamastack_url(test_config):
    """
    LlamaStack URL for direct API calls
    """
    return test_config.LLAMASTACK_URL


@pytest.fixture(scope="session", autouse=True)
def verify_services_running(service_urls, api_session):
    """
    Verify that all required services are running before tests
    """
    for service_name, url in service_urls.items():
        try:
            api_session.get(url, timeout=5)
            print(f"✅ {service_name.capitalize()} is running at {url}")
        except requests.exceptions.RequestException as e:
            pytest.fail(f"❌ {service_name.capitalize()} is not running at {url}: {e}")


def pytest_configure(config):
    """
    Configure pytest with custom markers
    """
    config.addinivalue_line("markers", "integration: mark test as integration test")
    config.addinivalue_line("markers", "unit: mark test as unit test")
    config.addinivalue_line("markers", "slow: mark test as slow running")
