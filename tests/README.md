# Integration Tests

This directory contains integration tests for the AI Virtual Agent application.

## Quick Start

### 1. Start Services Manually

First, start all required services:

```bash
# Option 1: Use the run_local.sh script (recommended)
./local_dev/run_local.sh
```
Or use the [Conribution](../CONTRIBUTING.md)

Option 2:
### 2. Run Tests

Once services are running:

```bash
# Run all integration tests
./run_tests.sh

# Run specific test file
./run_tests.sh tests/integration/test_models_api.py

# Run specific Tavern test file
./run_tests.sh tests/integration/test_chat_pipeline.tavern.yaml

# Run with custom configuration
TEST_FRONTEND_URL="http://localhost:3000" ./run_tests.sh
```

## Test Configuration

### Environment Variables

Configure test URLs using environment variables:

```bash
# Development (default)
export TEST_FRONTEND_URL="http://localhost:5173"
export TEST_BACKEND_URL="http://localhost:8000"
export TEST_LLAMASTACK_URL="http://localhost:8321"

# Custom configuration
export TEST_FRONTEND_URL="http://localhost:3000"
export TEST_BACKEND_URL="http://localhost:8080"
export TEST_LLAMASTACK_URL="http://localhost:8888"
```

### Docker/Container Setup

For containerized environments:

```bash
export TEST_FRONTEND_URL="http://frontend:5173"
export TEST_BACKEND_URL="http://backend:8000"
export TEST_LLAMASTACK_URL="http://llamastack:8321"
```

## Running Tests

### All Tests

```bash
# Run all integration tests
./run_tests.sh

# Run all tests with custom configuration
TEST_FRONTEND_URL="http://localhost:3000" ./run_tests.sh
```

### Specific Tests

```bash
# Run specific test file
./run_tests.sh tests/integration/test_models_api.py

# Run with pattern
./run_tests.sh tests/integration/test_specific_*

# Run with pytest options
./run_tests.sh tests/integration/test_models_api.py::test_models_api_response -v
```

### Manual pytest (Advanced)

```bash
# Activate virtual environment
source venv/bin/activate

# Install dependencies
pip install -r requirements-test.txt

# Run tests with custom configuration
TEST_FRONTEND_URL="http://localhost:3000" pytest tests/integration/ -v
```

## Service Management

### Manual Service Management

The test runner requires all services to be running before executing tests:

- **Backend**: `http://localhost:8000` (or `$TEST_BACKEND_URL`)
- **Frontend**: `http://localhost:5173` (or `$TEST_FRONTEND_URL`)
- **LlamaStack**: `http://localhost:8321` (or `$TEST_LLAMASTACK_URL`)

### Service Verification

The script checks if services are running and provides helpful instructions if they're not:

```bash
🔍 Checking if services are running...
✅ Backend is running at http://localhost:8000
✅ Frontend is running at http://localhost:5173
✅ LlamaStack is running at http://localhost:8321
```

If any service is not running, the script will exit with clear instructions on how to start them.

## Test Structure

### Test Files

**Python Tests:**
- `test_models_api.py` - Comprehensive API testing
- `test_specific_models_api.py` - Specific curl equivalent tests

**Tavern Tests (YAML-based):**
- `test_chat_pipeline.tavern.yaml` - End-to-end chat functionality with response validation
- `test_models_api.tavern.yaml` - API endpoint testing with structured validation
- `test_llama_stack_api.tavern.yaml` - LlamaStack service integration tests

**Shared Resources:**
- `validators.py` - Custom validation functions for both Python and Tavern tests

### Configuration

- `config.py` - Test configuration management
- `conftest.py` - pytest fixtures and setup
- `CONFIG.md` - Detailed configuration documentation

## Examples

### Basic Usage

```bash
# 1. Start services
./local_dev/run_local.sh

# 2. Run tests in another terminal
./run_tests.sh
```

### Custom Environment

```bash
# Start services on custom ports
# Then run tests with matching configuration
TEST_FRONTEND_URL="https://staging.example.com" \
TEST_BACKEND_URL="https://api-staging.example.com" \
TEST_LLAMASTACK_URL="https://llama-staging.example.com" \
./run_tests.sh
```

### Development Workflow

```bash
# Quick test during development
./run_tests.sh tests/integration/test_specific_models_api.py

# Run with verbose output
./run_tests.sh -v

# Run with detailed output
./run_tests.sh -vv --tb=short
```

## Troubleshooting

### Services Not Running

If the test runner shows that services aren't running:

1. **Check if services are actually running**: Use `ps aux | grep` or check the URLs in browser
2. **Start services manually**: Use `./local_dev/run_local.sh` or start each service individually
3. **Check port availability**: Ensure ports 8000, 5173, 8321 are not in use by other processes
4. **Verify configuration**: Make sure environment variables match your service URLs

### Service Startup Issues

If services fail to start:

1. **Check dependencies**: Ensure all required packages are installed
2. **Verify permissions**: Make sure scripts have execute permissions: `chmod +x local_dev/*.sh`
3. **Check logs**: Look at service output in tmux session or terminal
4. **Port conflicts**: Kill any processes using the required ports

### Configuration Issues

1. **Environment variables**: Verify `TEST_*_URL` variables are set correctly
2. **Service URLs**: Test URLs manually with `curl` or browser
3. **Network connectivity**: Ensure services are accessible from test runner

### Common Issues

1. **Services not accessible**: Check if services are bound to correct interfaces
2. **Port conflicts**: Another process might be using required ports
3. **Missing dependencies**: Backend/frontend dependencies not installed
4. **Permission denied**: Script files need execute permissions

## Dependencies

Test dependencies are managed in `requirements-test.txt`:

```
pytest>=7.0.0
requests>=2.25.0
```

## CI/CD Integration

The test runner is designed to work in CI/CD environments where services are pre-started:

```bash
# GitLab CI example
before_script:
  - ./local_dev/run_local.sh &
  - sleep 30  # Wait for services to start
script:
  - ./run_tests.sh

# GitHub Actions example
- name: Start Services
  run: ./local_dev/run_local.sh &
- name: Wait for Services
  run: sleep 30
- name: Run Integration Tests
  run: ./run_tests.sh
```

For more detailed configuration options, see `CONFIG.md`.
