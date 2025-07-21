"""
Integration tests for the Models API using pytest and requests
"""

import pytest


@pytest.mark.integration
def test_llama_stack_llms_endpoint(api_endpoints, api_session):
    """
    Test that the LLM models endpoint returns expected data structure
    """
    # Make request to the models API
    response = api_session.get(api_endpoints["llms"])

    # Check status code
    assert response.status_code == 200

    # Check content type
    assert response.headers["content-type"] == "application/json"

    # Parse JSON response
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # Check that we have at least one model
    assert len(json_data) > 0, "Response should contain at least one model"

    # Expected models
    expected_models = ["llama3.2:3b-instruct-fp16"]

    # Check that all models have required fields
    for model in json_data:
        assert "model_name" in model, f"Model {model} missing model_name"
        assert (
            "provider_resource_id" in model
        ), f"Model {model} missing provider_resource_id"
        assert "model_type" in model, f"Model {model} missing model_type"
        assert (
            model["model_type"] == "llm"
        ), f"Model {model} has incorrect model_type: {model['model_type']}"

    # Check that expected models are present
    actual_model_names = [model["model_name"] for model in json_data]
    for expected_model in expected_models:
        assert (
            expected_model in actual_model_names
        ), f"Expected model {expected_model} not found in response"

    # Print models for debugging
    print(f"Found {len(json_data)} models:")
    for model in json_data:
        print(f"  - {model['model_name']} ({model['provider_resource_id']})")


@pytest.mark.integration
def test_llama_stack_llms_exact_response(api_endpoints, api_session):
    """
    Test that the LLM models endpoint returns the exact expected response
    """
    # Make request to the models API
    response = api_session.get(api_endpoints["llms"])

    # Check status code
    assert response.status_code == 200

    # Parse JSON response
    json_data = response.json()

    # Expected exact response structure
    expected_response = [
        {
            "model_name": "llama3.2:3b-instruct-fp16",
            "provider_resource_id": "llama3.2:3b-instruct-fp16",
            "model_type": "llm",
        }
    ]

    # Check that we have exactly 3 models
    assert len(json_data) == len(
        expected_response
    ), f"Expected {len(expected_response)} models, got {len(json_data)}"

    # Check that each expected model is present
    for expected_model in expected_response:
        assert (
            expected_model in json_data
        ), f"Expected model {expected_model} not found in response"


@pytest.mark.integration
def test_virtual_assistants_endpoint(api_endpoints, api_session):
    """
    Test that the Virtual Assistants endpoint returns expected data structure
    """
    # Make request to the virtual assistants API
    response = api_session.get(api_endpoints["virtual_assistants"])

    # Check status code
    assert response.status_code == 200

    # Check content type
    assert response.headers["content-type"] == "application/json"

    # Parse JSON response
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # If we have assistants, check their structure
    if len(json_data) > 0:
        for assistant in json_data:
            assert "id" in assistant, f"Assistant {assistant} missing id"
            assert "name" in assistant, f"Assistant {assistant} missing name"
            assert (
                "model_name" in assistant
            ), f"Assistant {assistant} missing model_name"
            assert "prompt" in assistant, f"Assistant {assistant} missing prompt"
            assert "tools" in assistant, f"Assistant {assistant} missing tools"
            assert (
                "knowledge_base_ids" in assistant
            ), f"Assistant {assistant} missing knowledge_base_ids"

        print(f"Found {len(json_data)} virtual assistants:")
        for assistant in json_data:
            print(f"  - {assistant['name']} (model: {assistant['model_name']})")
    else:
        print("No virtual assistants found")


@pytest.mark.skip(reason="Skipping embedding models test for now")
@pytest.mark.integration
def test_embedding_models_endpoint(api_endpoints, api_session):
    """
    Test that the Embedding Models endpoint returns expected data structure
    """
    # Make request to the embedding models API
    response = api_session.get(api_endpoints["embedding_models"])

    # Check status code
    assert response.status_code == 200

    # Check content type
    assert response.headers["content-type"] == "application/json"

    # Parse JSON response
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # Check that we have at least one embedding model
    assert len(json_data) > 0, "Response should contain at least one embedding model"

    # Check that all models have required fields
    for model in json_data:
        assert "name" in model, f"Embedding model {model} missing name"
        assert (
            "provider_resource_id" in model
        ), f"Embedding model {model} missing provider_resource_id"
        assert "model_type" in model, f"Embedding model {model} missing model_type"

    print(f"Found {len(json_data)} embedding models:")
    for model in json_data:
        print(f"  - {model['name']} ({model['provider_resource_id']})")


@pytest.mark.integration
def test_tools_endpoint(api_endpoints, api_session):
    """
    Test that the Tools endpoint returns expected data structure
    """
    # Make request to the tools API
    response = api_session.get(api_endpoints["tools"])

    # Check status code
    assert response.status_code == 200

    # Check content type
    assert response.headers["content-type"] == "application/json"

    # Parse JSON response
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # If we have tools, check their structure
    if len(json_data) > 0:
        for tool in json_data:
            assert "id" in tool, f"Tool {tool} missing id"
            assert "name" in tool, f"Tool {tool} missing name"
            assert "toolgroup_id" in tool, f"Tool {tool} missing toolgroup_id"

        print(f"Found {len(json_data)} tools:")
        for tool in json_data:
            print(f"  - {tool['name']} (id: {tool['toolgroup_id']})")
    else:
        print("No tools found")


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
