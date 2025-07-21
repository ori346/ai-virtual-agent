"""
Configuration settings for integration tests
"""

import os
from typing import Dict


class TestConfig:
    """Test configuration with environment variable support"""

    # Base URLs - can be overridden by environment variables
    FRONTEND_URL = os.getenv("TEST_FRONTEND_URL", "http://localhost:5173")
    BACKEND_URL = os.getenv("TEST_BACKEND_URL", "http://localhost:8000")
    LLAMASTACK_URL = os.getenv("TEST_LLAMASTACK_URL", "http://localhost:8321")

    # API endpoints
    API_BASE_PATH = "/api"

    # Request settings
    REQUEST_TIMEOUT = int(os.getenv("TEST_REQUEST_TIMEOUT", "10"))
    MAX_RETRIES = int(os.getenv("TEST_MAX_RETRIES", "1"))

    @classmethod
    def get_api_url(cls, endpoint: str) -> str:
        """Get full API URL for an endpoint"""
        return f"{cls.FRONTEND_URL}{cls.API_BASE_PATH}{endpoint}"

    @classmethod
    def get_endpoints(cls) -> Dict[str, str]:
        """Get all API endpoints"""
        return {
            "llms": cls.get_api_url("/llama_stack/llms"),
            "embedding_models": cls.get_api_url("/llama_stack/embedding_models"),
            "providers": cls.get_api_url("/llama_stack/providers"),
            "tools": cls.get_api_url("/llama_stack/tools"),
            "virtual_assistants": cls.get_api_url("/virtual_assistants/"),
            "knowledge_bases": cls.get_api_url("/knowledge_bases/"),
            "chat": cls.get_api_url("/llama_stack/chat"),
            "chat_sessions": cls.get_api_url("/chat_sessions/"),
        }

    @classmethod
    def get_service_urls(cls) -> Dict[str, str]:
        """Get all service URLs"""
        return {
            "frontend": cls.FRONTEND_URL,
            "backend": cls.BACKEND_URL,
            "llamastack": cls.LLAMASTACK_URL,
        }

    @classmethod
    def print_config(cls):
        """Print current configuration"""
        print("🔧 Test Configuration:")
        print(f"  Frontend URL: {cls.FRONTEND_URL}")
        print(f"  Backend URL: {cls.BACKEND_URL}")
        print(f"  LlamaStack URL: {cls.LLAMASTACK_URL}")
        print(f"  Request Timeout: {cls.REQUEST_TIMEOUT}s")
        print(f"  Max Retries: {cls.MAX_RETRIES}")


# Global config instance
config = TestConfig()
