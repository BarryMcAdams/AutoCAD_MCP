import os
import sys

import pytest

# Ensure the project root is in the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
sys.path.insert(0, project_root)


@pytest.fixture(scope="session")
def project_configuration():
    """Provide a consistent configuration for integration tests."""
    return {
        "project_root": project_root,
        "src_directory": os.path.join(project_root, "src"),
        "test_data_directory": os.path.join(project_root, "tests", "test_data"),
        "mcp_tools_directory": os.path.join(project_root, "src", "mcp_integration"),
    }


@pytest.fixture
def mock_autocad_environment(monkeypatch):
    """Create a mock AutoCAD environment for testing."""

    # Simulated AutoCAD connection
    class MockAutoCAD:
        def __init__(self):
            self.connected = False

        def connect(self):
            self.connected = True
            return self

        def disconnect(self):
            self.connected = False

    return MockAutoCAD()


def pytest_configure(config):
    """Configure pytest with custom markers and settings."""
    config.addinivalue_line("markers", "mcp_tool: mark test as an MCP tool integration test")
    config.addinivalue_line("markers", "performance: mark test as a performance integration test")
