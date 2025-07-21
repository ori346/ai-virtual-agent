"""
Custom validators for Tavern integration tests.

This module provides custom validation functions for testing API responses
that require more complex validation than Tavern's built-in capabilities.
"""


def validate_contains_text(response, expected_text):
    """
    Validate that the response body contains the expected text.

    This validator is useful for streaming responses or text responses
    where we need to check if certain content is present. For SSE responses,
    it extracts and combines all text content from the data chunks.

    Args:
        response: The HTTP response object from the request
        expected_text: The text string that should be present in the response body

    Returns:
        bool: True if validation passes

    Raises:
        AssertionError: If the expected text is not found in the response body
    """
    import json

    # Get response body as text
    if hasattr(response, "text"):
        body_text = response.text
    elif hasattr(response, "content"):
        body_text = (
            response.content.decode("utf-8")
            if isinstance(response.content, bytes)
            else str(response.content)
        )
    else:
        body_text = str(response)

    # For SSE responses, extract and combine all text content
    combined_text = ""
    sse_lines = body_text.split("\n")

    for line in sse_lines:
        if line.startswith("data: ") and line != "data: [DONE]":
            try:
                # Remove 'data: ' prefix and parse JSON
                json_data = json.loads(line[6:])  # Remove 'data: ' (6 chars)
                if json_data.get("type") == "text" and "content" in json_data:
                    combined_text += json_data["content"]
            except (json.JSONDecodeError, KeyError):
                # Skip lines that aren't valid JSON or don't have expected structure
                continue

    # Check if expected text is in the combined text or raw response
    if expected_text in combined_text or expected_text in body_text:
        return True

    raise AssertionError(
        f"Expected text '{expected_text}' not found in response. "
        f"Combined text from SSE chunks: '{combined_text}' "
        f"Raw response body: {body_text[:500]}..."  # Show first 500 chars for debugging
    )


def validate_models_response(response):
    """
    Validate that the models API response contains the expected structure
    """
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # Check that we have at least one model
    assert len(json_data) > 0, "Response should contain at least one model"

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

    return True


def validate_virtual_assistants_response(response):
    """
    Validate that the virtual assistants API response contains the expected structure
    """
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

    return True


def validate_tools_response(response):
    """
    Validate that the tools API response contains the expected structure
    """
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # If we have tools, check their structure
    if len(json_data) > 0:
        for tool in json_data:
            assert "toolgroup_id" in tool, f"Tool {tool} missing toolgroup_id"
            assert "name" in tool, f"Tool {tool} missing name"

    return True


def validate_embedding_models_response(response):
    """
    Validate that the embedding models API response contains the expected structure
    """
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # Check that we have at least one embedding model
    if len(json_data) > 0:
        # Check that all models have required fields
        for model in json_data:
            assert "name" in model, f"Embedding model {model} missing name"
            assert (
                "provider_resource_id" in model
            ), f"Embedding model {model} missing provider_resource_id"
            assert "model_type" in model, f"Embedding model {model} missing model_type"

    return True


def validate_api_response_structure(response, expected_fields=None):
    """
    Generic validator for API response structure

    Args:
        response: HTTP response object
        expected_fields: List of required fields for each item in response
    """
    json_data = response.json()

    # Check that response is a list
    assert isinstance(json_data, list), "Response should be a list"

    # If we have items and expected fields, check structure
    if len(json_data) > 0 and expected_fields:
        for item in json_data:
            for field in expected_fields:
                assert field in item, f"Item {item} missing required field: {field}"

    return True


def validate_sse_contains_text(response, expected_text):
    """
    Validate that Server-Sent Events response contains the expected text.

    Specifically designed for SSE responses that come in the format:
    data: {"type":"text","content":"some text"}\n\n

    Args:
        response: The HTTP response object from the request
        expected_text: The text string that should be present in the SSE data

    Returns:
        bool: True if validation passes

    Raises:
        AssertionError: If the expected text is not found in the SSE response
    """
    # Get response body as text
    if hasattr(response, "text"):
        body_text = response.text
    elif hasattr(response, "content"):
        body_text = (
            response.content.decode("utf-8")
            if isinstance(response.content, bytes)
            else str(response.content)
        )
    else:
        body_text = str(response)

    # For SSE responses, check if the expected text appears in any data line
    sse_lines = body_text.split("\n")
    data_lines = [line for line in sse_lines if line.startswith("data:")]

    found_text = False
    for data_line in data_lines:
        if expected_text in data_line:
            found_text = True
            break

    if not found_text:
        raise AssertionError(
            f"Expected text '{expected_text}' not found in SSE data lines. "
            f"Data lines: {data_lines[:10]}..."  # Show first 10 lines
        )

    return True
