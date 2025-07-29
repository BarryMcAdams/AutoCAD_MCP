"""
Enhanced MCP Server for Master AutoCAD Coder
==========================================

Extended MCP server that combines existing manufacturing functionality
with new interactive development tools for VS Code integration.
Maintains 100% backward compatibility while adding enhanced capabilities.
"""

import logging
import asyncio
import time
from typing import Any, Dict, List, Optional
from mcp.server import FastMCP
from mcp import McpError
from mcp.types import Tool

# Import enhanced AutoCAD functionality and local modules
from ..enhanced_autocad.compatibility_layer import Autocad
from .context_manager import ContextManager
from .security_manager import SecurityManager
from ..interactive.python_repl import PythonREPL
from ..interactive.execution_engine import ExecutionEngine
from ..inspection.object_inspector import ObjectInspector, InspectionDepth
from ..inspection.property_analyzer import PropertyAnalyzer
from ..inspection.method_discoverer import MethodDiscoverer
from ..inspection.intellisense_provider import IntelliSenseProvider

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
        
        # Initialize interactive components
        self.python_repl = PythonREPL(
            autocad_wrapper=self.autocad_wrapper,
            security_manager=self.security_manager,
            context_manager=self.context_manager
        )
        self.execution_engine = ExecutionEngine(
            security_manager=self.security_manager
        )

        # Initialize inspection components
        self.object_inspector = ObjectInspector(self.autocad_wrapper)
        self.property_analyzer = PropertyAnalyzer()
        self.method_discoverer = MethodDiscoverer()
        self.intellisense_provider = IntelliSenseProvider(self.autocad_wrapper)

        # Register all MCP tools
        self._register_manufacturing_tools()
        self._register_development_tools()
        self._register_interactive_tools()
        self._register_inspection_tools()
        self._register_diagnostic_tools()

        logger.info("Enhanced MCP Server initialized with interactive capabilities")

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

    def _register_interactive_tools(self):
        """Register interactive development MCP tools for REPL and advanced execution."""

        @self.mcp.tool()
        def start_autocad_repl(session_id: Optional[str] = None) -> str:
            """
            Start interactive Python REPL with AutoCAD context.
            
            Args:
                session_id: Optional session identifier (auto-generated if None)
            
            Returns:
                Session startup information and available objects
            """
            try:
                result = self.python_repl.start_repl_session(session_id)
                
                if result["success"]:
                    return f"""REPL Session Started Successfully!
Session ID: {result['session_id']}
Available Objects: {', '.join(result['available_objects'])}
AutoCAD Status: {result['autocad_status']['message']}

Startup Output:
{result['startup_output']}

Ready for interactive Python development with AutoCAD!
Type your Python code and press Enter to execute."""
                else:
                    raise McpError("REPL_ERROR", result["error"])
                    
            except Exception as e:
                logger.error(f"Error starting REPL: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to start REPL: {str(e)}")

        @self.mcp.tool()
        def execute_python_in_autocad(code: str, session_id: Optional[str] = None) -> str:
            """
            Execute Python code in AutoCAD context with persistence.
            
            Args:
                code: Python code to execute
                session_id: REPL session identifier (None for default session)
            
            Returns:
                Execution result with output and timing information
            """
            try:
                # If no session specified, try to create one
                if session_id is None:
                    session_id = "default_session"
                    if session_id not in self.python_repl.active_sessions:
                        self.python_repl.start_repl_session(session_id)
                
                result = self.python_repl.execute_code(code, session_id)
                
                if result["success"]:
                    output_lines = [
                        f"Command #{result.get('command_number', 1)} executed successfully",
                        f"Execution time: {result['execution_time']:.3f}s"
                    ]
                    
                    if result["output"]:
                        output_lines.append(f"Output:\n{result['output']}")
                    
                    if result.get("continuation"):
                        output_lines.append(f"\nWaiting for more input...")
                        output_lines.append(f"Prompt: {result.get('prompt', '...')}")
                    
                    return "\n".join(output_lines)
                else:
                    return f"Execution Error:\n{result.get('error', 'Unknown error')}\n\nExecution time: {result['execution_time']:.3f}s"
                    
            except Exception as e:
                logger.error(f"Error executing Python in REPL: {e}")
                raise McpError("EXECUTION_ERROR", f"REPL execution failed: {str(e)}")

        @self.mcp.tool()
        def get_repl_history(session_id: str, limit: int = 10) -> str:
            """
            Retrieve REPL command history.
            
            Args:
                session_id: REPL session identifier
                limit: Maximum number of history entries to return
            
            Returns:
                Formatted command history
            """
            try:
                result = self.python_repl.get_session_history(session_id, limit)
                
                if result["success"]:
                    if not result["history"]:
                        return f"No command history for session {session_id}"
                    
                    history_lines = [
                        f"Command History for Session: {session_id}",
                        f"Total Commands: {result['total_commands']}",
                        f"Session Age: {result['session_age']:.1f} seconds",
                        f"Showing last {len(result['history'])} commands:",
                        "=" * 50
                    ]
                    
                    for entry in result["history"]:
                        cmd_num = entry["command_number"]
                        timestamp = time.strftime("%H:%M:%S", time.localtime(entry["timestamp"]))
                        code = entry["code"].replace("\n", "\\n")[:100]
                        status = "✅" if entry["success"] else "❌"
                        exec_time = entry["execution_time"]
                        
                        history_lines.append(f"[{cmd_num}] {timestamp} ({exec_time:.3f}s) {status}")
                        history_lines.append(f"    {code}")
                        
                        if entry.get("output"):
                            output = entry["output"][:200].replace("\n", "\\n")
                            history_lines.append(f"    → {output}")
                        history_lines.append("")
                    
                    return "\n".join(history_lines)
                else:
                    return f"Error retrieving history: {result['error']}"
                    
            except Exception as e:
                logger.error(f"Error getting REPL history: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to get REPL history: {str(e)}")

        @self.mcp.tool()
        def clear_repl_session(session_id: str) -> str:
            """
            Clear REPL session and free resources.
            
            Args:
                session_id: REPL session identifier
            
            Returns:
                Clear operation result
            """
            try:
                result = self.python_repl.clear_session(session_id)
                
                if result["success"]:
                    return f"Session {session_id} cleared successfully.\nAutoCAD context reloaded and ready for new commands."
                else:
                    return f"Error clearing session: {result.get('error', 'Unknown error')}"
                    
            except Exception as e:
                logger.error(f"Error clearing REPL session: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to clear REPL session: {str(e)}")

        @self.mcp.tool()
        def stop_repl_session(session_id: str) -> str:
            """
            Stop and remove REPL session.
            
            Args:
                session_id: REPL session identifier
            
            Returns:
                Stop operation result
            """
            try:
                result = self.python_repl.stop_session(session_id)
                
                if result["success"]:
                    return f"REPL session {session_id} stopped and resources freed."
                else:
                    return f"Error stopping session: {result.get('error', 'Session not found')}"
                    
            except Exception as e:
                logger.error(f"Error stopping REPL session: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to stop REPL session: {str(e)}")

    def _register_inspection_tools(self):
        """Register AutoCAD object inspection MCP tools."""

        @self.mcp.tool()
        def inspect_autocad_object(object_name: str, depth: str = "basic") -> str:
            """
            Inspect AutoCAD object with specified depth.
            
            Args:
                object_name: Name of object to inspect ('app', 'doc', 'model', 'acad')
                depth: Inspection depth ('basic', 'detailed', 'comprehensive', 'hierarchical')
            
            Returns:
                Detailed object inspection report
            """
            try:
                # Validate depth parameter
                valid_depths = {"basic": InspectionDepth.BASIC, 
                               "detailed": InspectionDepth.DETAILED,
                               "comprehensive": InspectionDepth.COMPREHENSIVE,
                               "hierarchical": InspectionDepth.HIERARCHICAL}
                
                if depth not in valid_depths:
                    raise McpError("INVALID_PARAMS", f"Invalid depth '{depth}'. Valid options: {list(valid_depths.keys())}")
                
                # Perform inspection
                result = self.object_inspector.inspect_by_name(object_name, valid_depths[depth])
                
                # Format result
                report_lines = [
                    f"=== AutoCAD Object Inspection: {result.object_name} ===",
                    f"Object Type: {result.object_type}",
                    f"Object ID: {result.object_id}",
                    f"Inspection Depth: {result.depth.value}",
                    f"Inspection Time: {result.inspection_time:.3f}s",
                    f"Properties Found: {len(result.properties)}",
                    f"Methods Found: {len(result.methods)}",
                    ""
                ]
                
                # Add properties section
                if result.properties:
                    report_lines.append("=== Properties ===")
                    for prop in result.properties[:20]:  # Limit to first 20
                        access_info = ""
                        if not prop.is_writable:
                            access_info = " (read-only)"
                        elif not prop.is_readable:
                            access_info = " (write-only)"
                        
                        value_str = str(prop.value)[:100] if prop.value is not None else "None"
                        report_lines.append(f"  {prop.name}: {prop.type_name}{access_info} = {value_str}")
                        
                        if prop.description and depth in ["detailed", "comprehensive"]:
                            report_lines.append(f"    Description: {prop.description[:200]}")
                    
                    if len(result.properties) > 20:
                        report_lines.append(f"  ... and {len(result.properties) - 20} more properties")
                    report_lines.append("")
                
                # Add methods section
                if result.methods:
                    report_lines.append("=== Methods ===")
                    for method in result.methods[:15]:  # Limit to first 15
                        report_lines.append(f"  {method.signature}")
                        if method.description and depth in ["detailed", "comprehensive"]:
                            desc = method.description.split('\n')[0][:150]  # First line, truncated
                            report_lines.append(f"    {desc}")
                    
                    if len(result.methods) > 15:
                        report_lines.append(f"  ... and {len(result.methods) - 15} more methods")
                    report_lines.append("")
                
                # Add hierarchy if available
                if result.hierarchy and depth in ["comprehensive", "hierarchical"]:
                    report_lines.append("=== Object Hierarchy ===")
                    report_lines.append(f"  Type: {result.hierarchy.get('type', 'Unknown')}")
                    report_lines.append(f"  Module: {result.hierarchy.get('module', 'Unknown')}")
                    if result.hierarchy.get('mro'):
                        report_lines.append(f"  MRO: {' -> '.join(result.hierarchy['mro'])}")
                    if result.hierarchy.get('com_type'):
                        report_lines.append(f"  COM Type: {result.hierarchy['com_type']}")
                        report_lines.append(f"  COM Class: {result.hierarchy.get('com_class', 'Unknown')}")
                    report_lines.append("")
                
                # Add metadata
                if result.metadata:
                    report_lines.append("=== Metadata ===")
                    for key, value in result.metadata.items():
                        if key != "error":
                            report_lines.append(f"  {key}: {value}")
                
                return "\n".join(report_lines)
                
            except ValueError as e:
                raise McpError("INVALID_PARAMS", str(e))
            except Exception as e:
                logger.error(f"Error inspecting object {object_name}: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to inspect object: {str(e)}")

        @self.mcp.tool()
        def discover_object_methods(object_name: str, search_pattern: str = "") -> str:
            """
            Discover methods for AutoCAD object with optional filtering.
            
            Args:
                object_name: Name of object to analyze ('app', 'doc', 'model', 'acad')
                search_pattern: Optional pattern to filter methods (regex supported)
            
            Returns:
                Detailed method discovery report
            """
            try:
                # Get the object
                result = self.object_inspector.inspect_by_name(object_name, InspectionDepth.BASIC)
                obj = self.object_inspector._get_object_by_name(object_name)
                
                if obj is None:
                    raise ValueError(f"Object '{object_name}' not found")
                
                # Discover all methods
                if search_pattern:
                    methods = self.method_discoverer.find_methods_by_pattern(obj, search_pattern, "name")
                else:
                    methods = self.method_discoverer.discover_all_methods(obj, include_inherited=False)
                
                # Format report
                report_lines = [
                    f"=== Method Discovery: {object_name} ===",
                    f"Search Pattern: '{search_pattern}' (empty = all methods)" if search_pattern else "Showing all methods",
                    f"Methods Found: {len(methods)}",
                    ""
                ]
                
                for method in methods[:25]:  # Limit to first 25
                    report_lines.append(f"Method: {method.name}")
                    report_lines.append(f"  Signature: {method.signature}")
                    report_lines.append(f"  Type: {method.method_type.value}")
                    
                    if method.parameters:
                        param_names = [p.name for p in method.parameters if p.name not in ['self', 'cls']]
                        if param_names:
                            report_lines.append(f"  Parameters: {', '.join(param_names)}")
                    
                    if method.documentation and method.documentation.description:
                        desc = method.documentation.description[:200]
                        report_lines.append(f"  Description: {desc}")
                    
                    if method.is_inherited:
                        report_lines.append(f"  Inherited from: {method.source_class}")
                    
                    report_lines.append("")
                
                if len(methods) > 25:
                    report_lines.append(f"... and {len(methods) - 25} more methods")
                
                return "\n".join(report_lines)
                
            except ValueError as e:
                raise McpError("INVALID_PARAMS", str(e))
            except Exception as e:
                logger.error(f"Error discovering methods for {object_name}: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to discover methods: {str(e)}")

        @self.mcp.tool()
        def analyze_object_property(object_name: str, property_name: str) -> str:
            """
            Analyze specific property of AutoCAD object.
            
            Args:
                object_name: Name of object containing the property
                property_name: Name of property to analyze
            
            Returns:
                Detailed property analysis report
            """
            try:
                # Get the object
                obj = self.object_inspector._get_object_by_name(object_name)
                if obj is None:
                    raise ValueError(f"Object '{object_name}' not found")
                
                # Analyze the property
                prop_info = self.property_analyzer.analyze_property(obj, property_name)
                
                # Format report
                report_lines = [
                    f"=== Property Analysis: {object_name}.{property_name} ===",
                    f"Property Name: {prop_info.name}",
                    f"Data Type: {prop_info.data_type}",
                    f"Property Type: {prop_info.property_type.value}",
                    f"Access Level: {prop_info.access_level.value}",
                    f"Current Value: {prop_info.current_value}",
                    ""
                ]
                
                # Add constraints if any
                if prop_info.constraints:
                    report_lines.append("=== Constraints ===")
                    for constraint in prop_info.constraints:
                        report_lines.append(f"  Type: {constraint.constraint_type}")
                        if constraint.min_value is not None:
                            report_lines.append(f"    Min Value: {constraint.min_value}")
                        if constraint.max_value is not None:
                            report_lines.append(f"    Max Value: {constraint.max_value}")
                        if constraint.allowed_values:
                            report_lines.append(f"    Allowed Values: {constraint.allowed_values}")
                        if constraint.description:
                            report_lines.append(f"    Description: {constraint.description}")
                        report_lines.append("")
                
                # Add documentation if available
                if prop_info.documentation:
                    doc = prop_info.documentation
                    report_lines.append("=== Documentation ===")
                    report_lines.append(f"  Description: {doc.description}")
                    
                    if doc.usage_examples:
                        report_lines.append("  Usage Examples:")
                        for example in doc.usage_examples[:3]:
                            report_lines.append(f"    {example}")
                    
                    if doc.related_properties:
                        report_lines.append(f"  Related Properties: {', '.join(doc.related_properties)}")
                    
                    if doc.warnings:
                        report_lines.append("  Warnings:")
                        for warning in doc.warnings:
                            report_lines.append(f"    ⚠️ {warning}")
                    
                    report_lines.append("")
                
                # Add inheritance info
                if prop_info.is_inherited:
                    report_lines.append(f"Inherited from: {prop_info.source_class}")
                
                # Add metadata
                if prop_info.metadata:
                    report_lines.append("=== Metadata ===")
                    for key, value in prop_info.metadata.items():
                        if key != "error":
                            report_lines.append(f"  {key}: {value}")
                
                # Generate code examples
                report_lines.append("=== Code Examples ===")
                get_code = self.property_analyzer.generate_property_code(obj, property_name, "get")
                report_lines.append(f"Get Value: {get_code}")
                
                if prop_info.access_level in ["read_write", "write_only"]:
                    set_code = self.property_analyzer.generate_property_code(obj, property_name, "set")
                    report_lines.append(f"Set Value: {set_code}")
                
                return "\n".join(report_lines)
                
            except ValueError as e:
                raise McpError("INVALID_PARAMS", str(e))
            except Exception as e:
                logger.error(f"Error analyzing property {property_name}: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to analyze property: {str(e)}")

        @self.mcp.tool()
        def search_autocad_api(search_term: str, object_scope: str = "all") -> str:
            """
            Search AutoCAD API for properties and methods.
            
            Args:
                search_term: Term to search for in properties/methods
                object_scope: Scope to search ('app', 'doc', 'model', 'all')
            
            Returns:
                Search results with matching properties and methods
            """
            try:
                if object_scope == "all":
                    # Search across all main objects
                    all_results = []
                    for obj_name in ["app", "doc", "model", "acad"]:
                        try:
                            results = self.object_inspector.search_objects(search_term, "all")
                            all_results.extend(results)
                        except:
                            continue
                    results = all_results
                else:
                    # Search specific object
                    results = self.object_inspector.search_objects(search_term, "all")
                
                # Format results
                report_lines = [
                    f"=== AutoCAD API Search Results ===",
                    f"Search Term: '{search_term}'",
                    f"Scope: {object_scope}",
                    f"Results Found: {len(results)}",
                    ""
                ]
                
                # Group results by type
                properties = [r for r in results if r.get("type") == "property"]
                methods = [r for r in results if r.get("type") == "method"]
                
                if properties:
                    report_lines.append("=== Properties ===")
                    for prop in properties[:15]:
                        score = prop.get("match_score", 0)
                        report_lines.append(f"  {prop['object']}.{prop['name']} ({prop['value_type']}) - Score: {score:.2f}")
                    
                    if len(properties) > 15:
                        report_lines.append(f"  ... and {len(properties) - 15} more properties")
                    report_lines.append("")
                
                if methods:
                    report_lines.append("=== Methods ===")
                    for method in methods[:15]:
                        score = method.get("match_score", 0)
                        signature = method.get("signature", method['name'] + "(...)")
                        report_lines.append(f"  {method['object']}.{signature} - Score: {score:.2f}")
                    
                    if len(methods) > 15:
                        report_lines.append(f"  ... and {len(methods) - 15} more methods")
                    report_lines.append("")
                
                if not results:
                    report_lines.append("No matches found. Try a different search term or check object availability.")
                
                return "\n".join(report_lines)
                
            except Exception as e:
                logger.error(f"Error searching AutoCAD API: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to search API: {str(e)}")

        @self.mcp.tool()
        def get_intellisense_completions(context: str, position: int = 0) -> str:
            """
            Get IntelliSense completions for AutoCAD development.
            
            Args:
                context: Code context for completion (e.g., "acad.app.")
                position: Cursor position in context
            
            Returns:
                Available completions with descriptions
            """
            try:
                # Simulate document and position for IntelliSense provider
                document_text = context
                position_info = {"line": 0, "character": position or len(context)}
                
                # Get completions
                completions = self.intellisense_provider.get_completions(document_text, position_info)
                
                # Format results
                report_lines = [
                    f"=== IntelliSense Completions ===",
                    f"Context: '{context}'",
                    f"Position: {position}",
                    f"Completions Found: {len(completions)}",
                    ""
                ]
                
                for completion in completions[:20]:  # Limit to first 20
                    kind_name = completion.kind.name if hasattr(completion.kind, 'name') else str(completion.kind)
                    report_lines.append(f"  {completion.label} ({kind_name})")
                    
                    if completion.detail:
                        report_lines.append(f"    Type: {completion.detail}")
                    
                    if completion.documentation:
                        doc = completion.documentation[:100]
                        report_lines.append(f"    Description: {doc}")
                    
                    if completion.insert_text and completion.insert_text != completion.label:
                        report_lines.append(f"    Insert: {completion.insert_text}")
                    
                    report_lines.append("")
                
                if len(completions) > 20:
                    report_lines.append(f"... and {len(completions) - 20} more completions")
                
                return "\n".join(report_lines)
                
            except Exception as e:
                logger.error(f"Error getting IntelliSense completions: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to get completions: {str(e)}")

        @self.mcp.tool()
        def clear_inspection_cache() -> str:
            """
            Clear object inspection cache to force fresh analysis.
            
            Returns:
                Cache clear confirmation
            """
            try:
                self.object_inspector.clear_cache()
                return "✅ Object inspection cache cleared successfully. Next inspections will use fresh analysis."
            except Exception as e:
                logger.error(f"Error clearing inspection cache: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to clear cache: {str(e)}")

        @self.mcp.tool()
        def list_active_repl_sessions() -> str:
            """
            List all active REPL sessions.
            
            Returns:
                Information about active REPL sessions
            """
            try:
                sessions_info = self.python_repl.get_active_sessions()
                
                if not sessions_info["active_sessions"]:
                    return "No active REPL sessions."
                
                info_lines = [
                    f"Active REPL Sessions: {sessions_info['total_sessions']}",
                    "=" * 40
                ]
                
                for session_id, info in sessions_info["active_sessions"].items():
                    age = info["age_seconds"]
                    last_used = time.strftime("%H:%M:%S", time.localtime(info["last_executed"]))
                    
                    info_lines.append(f"Session: {session_id}")
                    info_lines.append(f"  Commands: {info['command_count']}")
                    info_lines.append(f"  Age: {age:.1f}s")
                    info_lines.append(f"  Last Used: {last_used}")
                    info_lines.append(f"  Status: {info['status']}")
                    info_lines.append("")
                
                return "\n".join(info_lines)
                
            except Exception as e:
                logger.error(f"Error listing REPL sessions: {e}")
                raise McpError("INTERNAL_ERROR", f"Failed to list REPL sessions: {str(e)}")

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
