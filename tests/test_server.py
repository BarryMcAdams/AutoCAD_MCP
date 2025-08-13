
import pytest
from unittest.mock import patch, MagicMock

def test_server_module_import():
    """Test that server module can be imported."""
    from src import server
    assert hasattr(server, 'main')

def test_mcp_server_import():
    """Test that MCP server can be imported."""
    from src.mcp_server import mcp
    assert mcp is not None

@patch('src.mcp_integration.enhanced_mcp_server.EnhancedMCPServer')
def test_mcp_server_initialization(mock_server):
    """Test MCP server initialization."""
    mock_instance = MagicMock()
    mock_server.return_value = mock_instance
    
    from src.mcp_server import get_server
    server = get_server()
    assert server is not None

def test_server_entry_point():
    """Test server entry point exists."""
    import src.server
    assert hasattr(src.server, 'main')
    # Test that main function is callable
    assert callable(src.server.main)
