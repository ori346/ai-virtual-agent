"""
Specific test for the models API that matches the original curl command requirement
"""

import pytest


@pytest.mark.integration
def test_models_api_curl_equivalent(api_endpoints, api_session):
    """
    Test equivalent to: curl -s {tavern.env_vars.TEST_FRONTEND_URL}/api/llama_stack/llms
    Expected response:
    [
        {"model_name":"llama3.2:3b-instruct-fp16","provider_resource_id":"llama3.2:3b-instruct-fp16","model_type":"llm"},
    ]
    """
    # Make the exact request from the user's curl command
    response = api_session.get(api_endpoints["llms"])

    # Check that the request was successful
    assert response.status_code == 200

    # Parse the response
    json_data = response.json()

    # Expected exact response (as specified in the user's question)
    expected_response = [
        {
            "model_name": "llama3.2:3b-instruct-fp16",
            "provider_resource_id": "llama3.2:3b-instruct-fp16",
            "model_type": "llm",
        },
    ]

    # Verify the response matches exactly
    assert (
        json_data == expected_response
    ), f"Response does not match expected. Got: {json_data}"

    # Print success message
    print("✅ API response matches expected format exactly!")
    print(f"URL tested: {api_endpoints['llms']}")
    print("Response:", json_data)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "-s"])
