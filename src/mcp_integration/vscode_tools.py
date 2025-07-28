"""
VS Code Integration Tools
========================

Provides specific tools and utilities for VS Code integration,
command palette functionality, and interactive development features.
"""

import logging
import time
from typing import Dict, Any, List, Optional

logger = logging.getLogger(__name__)


class VSCodeTools:
    """
    Tools and utilities for VS Code integration.
    """

    def __init__(self, autocad_wrapper=None, context_manager=None):
        """
        Initialize VS Code tools.

        Args:
            autocad_wrapper: AutoCAD wrapper instance
            context_manager: Context manager for sessions
        """
        self.autocad_wrapper = autocad_wrapper
        self.context_manager = context_manager
        self.command_history = []

        logger.info("VS Code Tools initialized")

    def get_autocad_connection_indicator(self) -> Dict[str, Any]:
        """
        Get AutoCAD connection status for VS Code status bar.

        Returns:
            Dictionary containing status bar information
        """
        try:
            if not self.autocad_wrapper:
                return {
                    "connected": False,
                    "status_text": "AutoCAD: Not Connected",
                    "tooltip": "AutoCAD connection not available",
                    "color": "red",
                }

            status = self.autocad_wrapper.get_connection_status()

            if status["connected"]:
                return {
                    "connected": True,
                    "status_text": f"AutoCAD: Connected ({status.get('documents_count', 0)} docs)",
                    "tooltip": f"AutoCAD {status.get('autocad_version', 'Unknown')} - Connected",
                    "color": "green",
                }
            else:
                return {
                    "connected": False,
                    "status_text": "AutoCAD: Disconnected",
                    "tooltip": "AutoCAD not connected - Ensure AutoCAD 2025 is running",
                    "color": "yellow",
                }

        except Exception as e:
            logger.error(f"Error getting connection indicator: {str(e)}")
            return {
                "connected": False,
                "status_text": "AutoCAD: Error",
                "tooltip": f"Connection error: {str(e)}",
                "color": "red",
            }

    def get_command_palette_items(self) -> List[Dict[str, Any]]:
        """
        Get items for VS Code command palette.

        Returns:
            List of command palette items
        """
        commands = [
            # Connection commands
            {
                "id": "autocad.checkConnection",
                "title": "AutoCAD: Check Connection Status",
                "description": "Check AutoCAD connection and get detailed status",
            },
            {
                "id": "autocad.recoverConnection",
                "title": "AutoCAD: Recover Connection",
                "description": "Attempt to recover lost AutoCAD connection",
            },
            # Drawing commands
            {
                "id": "autocad.drawLine",
                "title": "AutoCAD: Draw Line",
                "description": "Draw a line in AutoCAD",
            },
            {
                "id": "autocad.drawCircle",
                "title": "AutoCAD: Draw Circle",
                "description": "Draw a circle in AutoCAD",
            },
            # Interactive development
            {
                "id": "autocad.startREPL",
                "title": "AutoCAD: Start Interactive Session",
                "description": "Start interactive Python session with AutoCAD context",
            },
            {
                "id": "autocad.executeCode",
                "title": "AutoCAD: Execute Selected Code",
                "description": "Execute selected Python code in AutoCAD context",
            },
            # Diagnostic commands
            {
                "id": "autocad.generateReport",
                "title": "AutoCAD: Generate Diagnostic Report",
                "description": "Generate comprehensive diagnostic report",
            },
            {
                "id": "autocad.performanceMetrics",
                "title": "AutoCAD: Show Performance Metrics",
                "description": "Display performance metrics and statistics",
            },
            # Manufacturing commands (preserved)
            {
                "id": "autocad.surfaceUnfolding",
                "title": "AutoCAD: Surface Unfolding",
                "description": "Access surface unfolding tools",
            },
            {
                "id": "autocad.patternOptimization",
                "title": "AutoCAD: Pattern Optimization",
                "description": "Access pattern nesting optimization tools",
            },
        ]

        return commands

    def execute_vscode_command(
        self, command_id: str, args: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        """
        Execute VS Code command.

        Args:
            command_id: Command identifier
            args: Command arguments

        Returns:
            Command execution result
        """
        try:
            result = self._handle_command(command_id, args or {})

            # Record command in history
            self.command_history.append(
                {
                    "timestamp": time.time(),
                    "command_id": command_id,
                    "args": args,
                    "success": True,
                    "result": result,
                }
            )

            # Keep only last 50 commands
            if len(self.command_history) > 50:
                self.command_history = self.command_history[-50:]

            return {"success": True, "result": result}

        except Exception as e:
            error_result = {"success": False, "error": str(e)}

            # Record failed command
            self.command_history.append(
                {
                    "timestamp": time.time(),
                    "command_id": command_id,
                    "args": args,
                    "success": False,
                    "error": str(e),
                }
            )

            logger.error(f"VS Code command failed: {command_id} - {str(e)}")
            return error_result

    def _handle_command(self, command_id: str, args: Dict[str, Any]) -> Any:
        """
        Handle specific VS Code command.

        Args:
            command_id: Command identifier
            args: Command arguments

        Returns:
            Command result
        """
        if command_id == "autocad.checkConnection":
            return self._handle_check_connection()

        elif command_id == "autocad.recoverConnection":
            return self._handle_recover_connection()

        elif command_id == "autocad.drawLine":
            return self._handle_draw_line(args)

        elif command_id == "autocad.drawCircle":
            return self._handle_draw_circle(args)

        elif command_id == "autocad.executeCode":
            return self._handle_execute_code(args)

        elif command_id == "autocad.generateReport":
            return self._handle_generate_report()

        elif command_id == "autocad.performanceMetrics":
            return self._handle_performance_metrics()

        else:
            raise ValueError(f"Unknown command: {command_id}")

    def _handle_check_connection(self) -> Dict[str, Any]:
        """Handle check connection command."""
        if not self.autocad_wrapper:
            return {"status": "No AutoCAD wrapper available"}

        status = self.autocad_wrapper.get_connection_status()
        performance = self.autocad_wrapper.get_performance_metrics()

        return {
            "connection_status": status,
            "performance_summary": {
                "total_operations": performance.get("total_operations", 0),
                "success_rate": performance.get("overall_success_rate", 0),
                "average_duration": performance.get("average_operation_duration", 0),
            },
        }

    def _handle_recover_connection(self) -> Dict[str, Any]:
        """Handle recover connection command."""
        if not self.autocad_wrapper:
            return {"success": False, "message": "No AutoCAD wrapper available"}

        success = self.autocad_wrapper.recover_connection()
        return {
            "success": success,
            "message": (
                "Connection recovered successfully" if success else "Connection recovery failed"
            ),
        }

    def _handle_draw_line(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle draw line command."""
        start_point = args.get("start_point", [0, 0, 0])
        end_point = args.get("end_point", [100, 100, 0])

        if not self.autocad_wrapper:
            raise ValueError("AutoCAD wrapper not available")

        entity_id = self.autocad_wrapper.draw_line(start_point, end_point)
        return {"entity_id": entity_id, "start_point": start_point, "end_point": end_point}

    def _handle_draw_circle(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle draw circle command."""
        center = args.get("center", [0, 0, 0])
        radius = args.get("radius", 50.0)

        if not self.autocad_wrapper:
            raise ValueError("AutoCAD wrapper not available")

        entity_id = self.autocad_wrapper.draw_circle(center, radius)
        return {"entity_id": entity_id, "center": center, "radius": radius}

    def _handle_execute_code(self, args: Dict[str, Any]) -> Dict[str, Any]:
        """Handle execute code command."""
        code = args.get("code", "")
        session_id = args.get("session_id")

        if not code.strip():
            raise ValueError("No code provided")

        # This would integrate with the enhanced MCP server's execute_simple_python
        # For now, return a placeholder response
        return {
            "code": code,
            "session_id": session_id,
            "result": "Code execution would be handled by MCP server",
        }

    def _handle_generate_report(self) -> Dict[str, Any]:
        """Handle generate report command."""
        if not self.autocad_wrapper:
            return {"report": "No AutoCAD wrapper available for diagnostics"}

        report = self.autocad_wrapper.create_diagnostic_report()
        return {"diagnostic_report": report}

    def _handle_performance_metrics(self) -> Dict[str, Any]:
        """Handle performance metrics command."""
        if not self.autocad_wrapper:
            return {"metrics": "No AutoCAD wrapper available for metrics"}

        metrics = self.autocad_wrapper.get_performance_metrics()
        return {"performance_metrics": metrics}

    def get_intellisense_completions(self, context: str, position: int) -> List[Dict[str, Any]]:
        """
        Get IntelliSense completions for AutoCAD context.

        Args:
            context: Code context around cursor
            position: Cursor position

        Returns:
            List of completion items
        """
        completions = []

        # AutoCAD object completions
        autocad_completions = [
            {
                "label": "acad.app",
                "kind": "property",
                "detail": "AutoCAD Application object",
                "documentation": "Access to AutoCAD application instance",
            },
            {
                "label": "acad.doc",
                "kind": "property",
                "detail": "Active AutoCAD document",
                "documentation": "Currently active AutoCAD document",
            },
            {
                "label": "acad.model",
                "kind": "property",
                "detail": "Model space object",
                "documentation": "AutoCAD model space for entity creation",
            },
            {
                "label": "acad.draw_line",
                "kind": "method",
                "detail": "draw_line(start_point, end_point)",
                "documentation": "Draw a line from start to end point",
            },
            {
                "label": "acad.draw_circle",
                "kind": "method",
                "detail": "draw_circle(center, radius)",
                "documentation": "Draw a circle with specified center and radius",
            },
        ]

        # Filter completions based on context
        if "acad." in context:
            completions.extend(autocad_completions)

        return completions

    def get_command_history(self, limit: int = 10) -> List[Dict[str, Any]]:
        """
        Get recent command history.

        Args:
            limit: Maximum number of commands to return

        Returns:
            List of recent commands
        """
        return self.command_history[-limit:] if limit > 0 else self.command_history

    def clear_command_history(self) -> None:
        """Clear command history."""
        self.command_history.clear()
        logger.info("VS Code command history cleared")

    def get_vscode_integration_status(self) -> Dict[str, Any]:
        """
        Get VS Code integration status.

        Returns:
            Dictionary containing integration status
        """
        return {
            "autocad_wrapper_available": self.autocad_wrapper is not None,
            "context_manager_available": self.context_manager is not None,
            "command_palette_items": len(self.get_command_palette_items()),
            "command_history_count": len(self.command_history),
            "integration_active": True,
        }
