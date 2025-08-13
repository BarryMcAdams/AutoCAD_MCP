"""
Legacy MCP server interface for regression testing compatibility.

This module provides compatibility with existing test code that expects
the 'mcp' object to be importable from src.mcp_server.
"""

import logging
from typing import Any, Dict

from src.mcp_integration.enhanced_mcp_server import EnhancedMCPServer

logger = logging.getLogger(__name__)

# Create a global MCP server instance for regression testing compatibility
try:
    mcp = EnhancedMCPServer()
    logger.info("Legacy MCP server interface initialized successfully")
except Exception as e:
    logger.warning(f"Could not initialize MCP server interface: {e}")
    # Create a mock object for testing environments
    class MockMCPServer:
        def __init__(self):
            self.tools = {}
            
        def get_tool(self, name: str):
            return MockTool(name)
    
    class MockTool:
        def __init__(self, name: str):
            self.name = name
            
        def fn(self, **kwargs):
            return f"Mock response for {self.name} with args {kwargs}"
    
    mcp = MockMCPServer()
    logger.info("Using mock MCP server for testing compatibility")

def get_server():
    """Get the MCP server instance."""
    return mcp

def list_tools():
    """List available MCP tools."""
    if hasattr(mcp, 'tools'):
        return list(mcp.tools.keys())
    return []

def get_tool_info(tool_name: str) -> Dict[str, Any]:
    """Get information about a specific tool."""
    if hasattr(mcp, 'get_tool'):
        tool = mcp.get_tool(tool_name)
        if tool:
            return {
                'name': tool_name,
                'available': True,
                'description': getattr(tool, 'description', 'No description available')
            }
    
    return {
        'name': tool_name,
        'available': False,
        'description': 'Tool not found'
    }