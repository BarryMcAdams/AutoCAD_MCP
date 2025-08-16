"""
Enhanced MCP Integration Layer
============================

Enhanced Model Context Protocol integration for Master AutoCAD Coder.
Provides VS Code integration, interactive development tools, and advanced
MCP capabilities while maintaining 100% backward compatibility.
"""

from .context_manager import ContextManager
from .enhanced_mcp_server import EnhancedMCPServer
from .security_manager import SecurityManager
from .vscode_tools import VSCodeTools

__all__ = ["EnhancedMCPServer", "VSCodeTools", "ContextManager", "SecurityManager"]

# Version information
__version__ = "1.0.0"
__author__ = "AutoCAD MCP Contributors"
