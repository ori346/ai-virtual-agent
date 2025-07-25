"""
Custom validators for Tavern integration tests.

This module provides custom validation functions for testing API responses
that require more complex validation than Tavern's built-in capabilities.
"""


def validate_exact_text(response, expected_text):
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
    if expected_text == combined_text:
        return True

    raise AssertionError(
        f"Expected text '{expected_text}' not found in response. "
        f"Combined text from SSE chunks: '{combined_text}' "
        f"Raw response body: {body_text[:500]}..."  # Show first 500 chars for debugging
    )
