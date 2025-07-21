# Test Configuration

The integration tests support flexible configuration through environment variables. This allows you to run tests against different environments without modifying code.

## Environment Variables

### Service URLs
- `TEST_FRONTEND_URL` - Frontend application URL (default: `http://localhost:5173`)
- `TEST_BACKEND_URL` - Backend API URL (default: `http://localhost:8000`)
- `TEST_LLAMASTACK_URL` - LlamaStack server URL (default: `http://localhost:8321`)

### Request Settings
- `TEST_REQUEST_TIMEOUT` - Request timeout in seconds (default: `10`)
- `TEST_MAX_RETRIES` - Maximum retry attempts (default: `3`)

## Usage Examples

### Development (Default)
```bash
# Uses default localhost URLs
pytest tests/integration/
```

### Custom URLs
```bash
# Set custom URLs
export TEST_FRONTEND_URL=http://localhost:3000
export TEST_BACKEND_URL=http://localhost:8080
export TEST_LLAMASTACK_URL=http://localhost:8322
pytest tests/integration/
```

### Docker/Container Setup
```bash
# Use container hostnames
export TEST_FRONTEND_URL=http://frontend:5173
export TEST_BACKEND_URL=http://backend:8000
export TEST_LLAMASTACK_URL=http://llamastack:8321
pytest tests/integration/
```

### Staging Environment
```bash
# Test against staging
export TEST_FRONTEND_URL=https://staging.example.com
export TEST_BACKEND_URL=https://api-staging.example.com
export TEST_LLAMASTACK_URL=https://llamastack-staging.example.com
pytest tests/integration/
```

### Production Environment
```bash
# Test against production
export TEST_FRONTEND_URL=https://app.example.com
export TEST_BACKEND_URL=https://api.example.com
export TEST_LLAMASTACK_URL=https://llamastack.example.com
pytest tests/integration/
```

## Using the Test Runner Script

The `run_tests.sh` script also supports environment variables:

```bash
# Use default settings
./run_tests.sh

# Override specific URLs
TEST_FRONTEND_URL=http://localhost:3000 ./run_tests.sh

# Run specific test
./run_tests.sh tests/integration/test_specific_models_api.py
```

## Configuration in Code

The test configuration is centralized in `tests/config.py`. You can also modify defaults there if needed:

```python
from tests.config import TestConfig

# Print current configuration
TestConfig.print_config()

# Get API endpoints
endpoints = TestConfig.get_endpoints()
print(endpoints["llms"])  # Full URL to LLMs endpoint
```

## Pytest Fixtures

The following fixtures are available in tests:

- `test_config` - Test configuration object
- `api_endpoints` - Dictionary of all API endpoints
- `service_urls` - Dictionary of service URLs
- `api_session` - Pre-configured requests session with retries
- `base_url` - Frontend URL
- `backend_url` - Backend URL
- `llamastack_url` - LlamaStack URL

Example usage:

```python
@pytest.mark.integration
def test_my_endpoint(api_endpoints, api_session):
    response = api_session.get(api_endpoints["llms"])
    assert response.status_code == 200
```
