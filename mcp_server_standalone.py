"""
Standalone AutoCAD MCP Server - Working version without import dependencies
"""

from mcp.server import FastMCP
from mcp import McpError
from mcp.types import Tool
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
import json

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("AutoCAD MCP Server")

@mcp.tool()
def mcp_server_status() -> str:
    """
    Get MCP server status - basic health check.
    
    Returns:
        Server status information
    """
    return json.dumps({
        "status": "running",
        "server_name": "AutoCAD MCP Server",
        "message": "MCP server is operational. AutoCAD connection requires AutoCAD 2025 to be running."
    }, indent=2)

@mcp.tool()
def test_basic_functionality() -> str:
    """
    Test basic MCP functionality without AutoCAD dependency.
    
    Returns:
        Test results
    """
    try:
        import win32com.client
        import pyautocad
        import numpy
        import scipy
        
        return json.dumps({
            "status": "success",
            "message": "All dependencies are available",
            "dependencies": {
                "win32com.client": "Available",
                "pyautocad": "Available", 
                "numpy": "Available",
                "scipy": "Available"
            }
        }, indent=2)
    except ImportError as e:
        return json.dumps({
            "status": "error",
            "message": f"Missing dependency: {e}",
        }, indent=2)

@mcp.tool()
def check_autocad_connection() -> str:
    """
    Check if AutoCAD is running and accessible.
    
    Returns:
        Connection status information
    """
    try:
        import win32com.client
        import pythoncom
        
        pythoncom.CoInitialize()
        
        # Try to connect to AutoCAD 2025
        try:
            app = win32com.client.GetActiveObject("AutoCAD.Application.25")
            app.Visible = True
            doc_name = app.ActiveDocument.Name
            
            return json.dumps({
                "status": "connected",
                "autocad_version": "2025",
                "active_document": doc_name,
                "message": "Successfully connected to AutoCAD 2025"
            }, indent=2)
            
        except Exception as e:
            try:
                # Try other AutoCAD versions
                app = win32com.client.GetActiveObject("AutoCAD.Application")
                app.Visible = True
                doc_name = app.ActiveDocument.Name
                
                return json.dumps({
                    "status": "connected",
                    "autocad_version": "Unknown version",
                    "active_document": doc_name,
                    "message": "Connected to AutoCAD (version not 2025)"
                }, indent=2)
                
            except Exception as e2:
                return json.dumps({
                    "status": "not_connected", 
                    "error": str(e2),
                    "message": "AutoCAD is not running or not accessible. Please start AutoCAD with an open document."
                }, indent=2)
                
    except Exception as e:
        return json.dumps({
            "status": "error",
            "error": str(e),
            "message": "Failed to check AutoCAD connection"
        }, indent=2)

@mcp.resource("autocad://server-status")  
def get_server_status() -> str:
    """Get current MCP server status."""
    try:
        return json.dumps({
            "mcp_server": "running",
            "tools_available": 3,
            "resources_available": 1,
            "message": "MCP server is operational"
        }, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.prompt("autocad-help")
def autocad_help_prompt() -> str:
    """Get help with AutoCAD MCP tools."""
    return """
    AutoCAD MCP Server Help
    ======================
    
    Available tools:
    1. mcp_server_status - Check if MCP server is running
    2. test_basic_functionality - Test all dependencies
    3. check_autocad_connection - Test AutoCAD connection
    
    To use these tools:
    1. Make sure AutoCAD 2025 is running
    2. Open a document in AutoCAD
    3. Use the MCP tools through your MCP client
    
    For manufacturing features, ensure AutoCAD has drawing entities loaded.
    """

if __name__ == "__main__":
    # Run the MCP server
    print("Starting standalone AutoCAD MCP Server...")
    mcp.run()