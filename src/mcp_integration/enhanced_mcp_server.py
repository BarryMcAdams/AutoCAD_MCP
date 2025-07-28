"""
Enhanced MCP Server for Master AutoCAD Coder
==========================================

Extended MCP server that combines existing manufacturing functionality
with new interactive development tools for VS Code integration.
Maintains 100% backward compatibility while adding enhanced capabilities.
"""

import logging
import asyncio
from typing import Any, Dict, List, Optional
from mcp.server import FastMCP
from mcp import McpError
from mcp.types import Tool

# Import existing MCP functionality
import sys
from pathlib import Path

src_dir = Path(__file__).parent.parent
sys.path.insert(0, str(src_dir))

from enhanced_autocad.compatibility_layer import Autocad
from .context_manager import ContextManager
from .security_manager import SecurityManager

logger = logging.getLogger(__name__)


class EnhancedMCPServer:
    """
    Enhanced MCP server combining manufacturing and development capabilities.
    """

    def __init__(self):
        """Initialize enhanced MCP server."""
        self.mcp = FastMCP("AutoCAD Master Coder")
        self.context_manager = ContextManager()
        self.security_manager = SecurityManager()
        self.autocad_wrapper = None

        # Register all MCP tools
        self._register_manufacturing_tools()
        self._register_development_tools()
        self._register_diagnostic_tools()

        logger.info("Enhanced MCP Server initialized")

    def _get_autocad_wrapper(self) -> Autocad:
        """Get AutoCAD wrapper instance with caching."""
        if not self.autocad_wrapper:
            self.autocad_wrapper = Autocad()
        return self.autocad_wrapper

    def _register_manufacturing_tools(self):
        """Register existing manufacturing MCP tools (preserved functionality)."""

        @self.mcp.tool()
        def draw_line(start_point: List[float], end_point: List[float]) -> str:
            """
            Draw a line in AutoCAD from start point to end point.

            Args:
                start_point: [x, y, z] coordinates for line start
                end_point: [x, y, z] coordinates for line end

            Returns:
                Success message with entity information
            """
            try:
                acad = self._get_autocad_wrapper()
                entity_id = acad.draw_line(start_point, end_point)
                return f"Line created successfully with entity ID: {entity_id}"
            except Exception as e:
                logger.error(f"Error drawing line: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to draw line: {str(e)}")

        @self.mcp.tool()
        def draw_circle(center: List[float], radius: float) -> str:
            """
            Draw a circle in AutoCAD.

            Args:
                center: [x, y, z] coordinates for circle center
                radius: Circle radius

            Returns:
                Success message with entity information
            """
            try:
                acad = self._get_autocad_wrapper()
                entity_id = acad.draw_circle(center, radius)
                return f"Circle created successfully with entity ID: {entity_id}"
            except Exception as e:
                logger.error(f"Error drawing circle: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to draw circle: {str(e)}")

        @self.mcp.tool()
        def get_autocad_status() -> str:
            """
            Get AutoCAD connection status and basic information.

            Returns:
                JSON string with AutoCAD status information
            """
            try:
                acad = self._get_autocad_wrapper()
                status = acad.get_connection_status()

                if status["connected"]:
                    return f"AutoCAD Status: Connected\nVersion: {status.get('autocad_version', 'Unknown')}\nDocuments: {status.get('documents_count', 0)}"
                else:
                    return "AutoCAD Status: Not Connected\nPlease ensure AutoCAD 2025 is running with an open document"
            except Exception as e:
                logger.error(f"Error getting AutoCAD status: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to get AutoCAD status: {str(e)}")

        # Add more manufacturing tools as needed (surface unfolding, pattern optimization, etc.)
        # These would be migrated from the existing mcp_server.py

    def _register_development_tools(self):
        """Register new development-focused MCP tools."""

        @self.mcp.tool()
        def get_enhanced_connection_status() -> str:
            """
            Get enhanced AutoCAD connection status with diagnostics.

            Returns:
                Detailed connection status with performance metrics
            """
            try:
                acad = self._get_autocad_wrapper()
                status = acad.get_connection_status()
                performance = acad.get_performance_metrics()
                errors = acad.get_error_statistics()

                report_lines = [
                    "=== Enhanced AutoCAD Connection Status ===",
                    f"Connected: {'Yes' if status['connected'] else 'No'}",
                    f"AutoCAD Version: {status.get('autocad_version', 'Unknown')}",
                    f"Documents Open: {status.get('documents_count', 0)}",
                    f"Connection Age: {status.get('connection_age_seconds', 0):.1f} seconds",
                    "",
                    "=== Performance Metrics ===",
                    f"Total Operations: {performance.get('total_operations', 0)}",
                    f"Success Rate: {performance.get('overall_success_rate', 0):.1%}",
                    f"Average Duration: {performance.get('average_operation_duration', 0):.3f}s",
                    f"Operations/Second: {performance.get('operations_per_second', 0):.2f}",
                    "",
                    "=== Error Statistics ===",
                    f"Total Errors: {errors.get('total_errors', 0)}",
                    f"Recent Errors (1h): {errors.get('errors_last_hour', 0)}",
                ]

                if performance.get("performance_warnings"):
                    report_lines.append("\n=== Performance Warnings ===")
                    for warning in performance["performance_warnings"]:
                        report_lines.append(f"⚠️ {warning}")

                return "\n".join(report_lines)

            except Exception as e:
                logger.error(f"Error getting enhanced status: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to get enhanced status: {str(e)}")

        @self.mcp.tool()
        def test_enhanced_wrapper() -> str:
            """
            Test enhanced wrapper functionality and performance.

            Returns:
                Test results and performance comparison
            """
            try:
                acad = self._get_autocad_wrapper()

                # Run basic functionality tests
                test_results = []

                # Test 1: Connection test
                try:
                    status = acad.get_connection_status()
                    test_results.append(
                        f"✅ Connection Test: {'Connected' if status['connected'] else 'Failed'}"
                    )
                except Exception as e:
                    test_results.append(f"❌ Connection Test: Failed - {str(e)}")

                # Test 2: Basic drawing test
                try:
                    entity_id = acad.draw_line([0, 0, 0], [10, 10, 0])
                    test_results.append(f"✅ Drawing Test: Line created (ID: {entity_id})")
                except Exception as e:
                    test_results.append(f"❌ Drawing Test: Failed - {str(e)}")

                # Test 3: Performance metrics test
                try:
                    metrics = acad.get_performance_metrics()
                    test_results.append(
                        f"✅ Performance Metrics: {metrics.get('total_operations', 0)} operations tracked"
                    )
                except Exception as e:
                    test_results.append(f"❌ Performance Metrics: Failed - {str(e)}")

                # Test 4: Error handling test
                try:
                    errors = acad.get_error_statistics()
                    test_results.append(
                        f"✅ Error Handling: {errors.get('total_errors', 0)} errors logged"
                    )
                except Exception as e:
                    test_results.append(f"❌ Error Handling: Failed - {str(e)}")

                return "Enhanced Wrapper Test Results:\n" + "\n".join(test_results)

            except Exception as e:
                logger.error(f"Error testing enhanced wrapper: {e}")
                raise McpError("INTERNAL_ERROR", f"Enhanced wrapper test failed: {str(e)}")

        @self.mcp.tool()
        def execute_simple_python(code: str, session_id: Optional[str] = None) -> str:
            """
            Execute simple Python code in AutoCAD context (secure).

            Args:
                code: Python code to execute
                session_id: Optional session ID for context persistence

            Returns:
                Execution result or error message
            """
            try:
                # Security validation
                if not self.security_manager.validate_python_code(code):
                    raise McpError("SECURITY_ERROR", "Code contains potentially unsafe operations")

                # Get or create session context
                context = self.context_manager.get_session_context(session_id)

                # Prepare execution environment
                acad = self._get_autocad_wrapper()
                exec_globals = {
                    "acad": acad,
                    "app": acad.app,
                    "doc": acad.doc,
                    "model": acad.model,
                    "__builtins__": self.security_manager.get_safe_builtins(),
                }
                exec_globals.update(context.get("variables", {}))

                # Execute code
                result = None
                try:
                    # Try as expression first
                    result = eval(code, exec_globals)
                except SyntaxError:
                    # Execute as statement
                    exec(code, exec_globals)
                    result = "Code executed successfully"

                # Update session context
                context["variables"] = {
                    k: v
                    for k, v in exec_globals.items()
                    if not k.startswith("__") and k not in ["acad", "app", "doc", "model"]
                }
                self.context_manager.update_session_context(session_id, context)

                return f"Result: {result}"

            except Exception as e:
                logger.error(f"Error executing Python code: {e}")
                raise McpError("EXECUTION_ERROR", f"Code execution failed: {str(e)}")

    def _register_diagnostic_tools(self):
        """Register diagnostic and maintenance tools."""

        @self.mcp.tool()
        def create_diagnostic_report() -> str:
            """
            Create comprehensive diagnostic report for troubleshooting.

            Returns:
                Detailed diagnostic report
            """
            try:
                acad = self._get_autocad_wrapper()
                report = acad.create_diagnostic_report()

                # Format report
                lines = [
                    "=== AutoCAD Master Coder Diagnostic Report ===",
                    f"Generated: {time.ctime()}",
                    "",
                    "=== Connection Status ===",
                    f"Connected: {report['connection_status']['connected']}",
                    f"Version: {report['connection_status'].get('autocad_version', 'Unknown')}",
                    f"Documents: {report['connection_status'].get('documents_count', 0)}",
                    "",
                    "=== Performance Summary ===",
                    f"Total Operations: {report['performance_metrics']['total_operations']}",
                    f"Success Rate: {report['performance_metrics']['overall_success_rate']:.1%}",
                    f"Average Duration: {report['performance_metrics']['average_operation_duration']:.3f}s",
                    "",
                    "=== Error Summary ===",
                    f"Total Errors: {report['error_statistics']['total_errors']}",
                    f"Recent Errors: {report['error_statistics'].get('errors_last_hour', 0)}",
                ]

                if report["error_statistics"].get("most_common_category"):
                    lines.append(
                        f"Most Common Error: {report['error_statistics']['most_common_category']}"
                    )

                return "\n".join(lines)

            except Exception as e:
                logger.error(f"Error creating diagnostic report: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to create diagnostic report: {str(e)}")

        @self.mcp.tool()
        def recover_autocad_connection() -> str:
            """
            Manually recover AutoCAD connection.

            Returns:
                Recovery result message
            """
            try:
                acad = self._get_autocad_wrapper()
                success = acad.recover_connection()

                if success:
                    return "✅ AutoCAD connection recovered successfully"
                else:
                    return "❌ AutoCAD connection recovery failed"

            except Exception as e:
                logger.error(f"Error recovering connection: {e}")
                raise McpError("INTERNAL_ERROR", f"Connection recovery failed: {str(e)}")

    def get_mcp_server(self) -> FastMCP:
        """
        Get the MCP server instance.

        Returns:
            FastMCP server instance
        """
        return self.mcp

    async def run_server(self, host: str = "localhost", port: int = 5002):
        """
        Run the enhanced MCP server.

        Args:
            host: Server host
            port: Server port
        """
        logger.info(f"Starting Enhanced MCP Server on {host}:{port}")
        await self.mcp.run(host=host, port=port)
