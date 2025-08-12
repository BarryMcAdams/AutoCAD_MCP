#!/usr/bin/env python3
"""
Standalone test runner for debugger tests.

This runner can execute basic validation tests without requiring the full 
pytest infrastructure, making it useful for environments where dependencies
are not available.
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def create_mock_dependencies():
    """Create mock dependencies for testing."""
    from enum import Enum
    
    # Create mock ErrorCategory enum
    class MockErrorCategory(Enum):
        CONNECTION_ERROR = "connection_error"
        COM_INTERFACE_ERROR = "com_interface_error"
        AUTOCAD_COMMAND_ERROR = "autocad_command_error"
        VALIDATION_ERROR = "validation_error"
        RUNTIME_ERROR = "runtime_error"
        SECURITY_ERROR = "security_error"
    
    # Create mock InspectionDepth enum
    class MockInspectionDepth(Enum):
        BASIC = "basic"
        DETAILED = "detailed"
        COMPREHENSIVE = "comprehensive"
    
    # Mock MCP related modules first (these are imported early)
    mcp_mock = type(sys)('mock_mcp')
    mcp_mock.McpError = type('McpError', (Exception,), {})
    sys.modules['mcp'] = mcp_mock
    
    # Mock psutil
    psutil_mock = type(sys)('mock_psutil')
    psutil_mock.Process = type('Process', (), {})
    psutil_mock.cpu_percent = lambda: 50.0
    psutil_mock.virtual_memory = lambda: type('Memory', (), {'percent': 75.0})()
    sys.modules['psutil'] = psutil_mock
    
    # Mock modules that might not be available
    mock_modules = {
        'src.enhanced_autocad.error_handler': type(sys)('mock_error_handler'),
        'src.enhanced_autocad.performance_monitor': type(sys)('mock_performance_monitor'),
        'src.inspection.method_discoverer': type(sys)('mock_method_discoverer'),
        'src.inspection.object_inspector': type(sys)('mock_object_inspector'),
        'src.inspection.property_analyzer': type(sys)('mock_property_analyzer'),
        'src.mcp_integration': type(sys)('mock_mcp_integration'),
        'src.mcp_integration.enhanced_mcp_server': type(sys)('mock_enhanced_mcp_server'),
        'src.mcp_integration.security_manager': type(sys)('mock_security_manager'),
        'src.mcp_integration.context_manager': type(sys)('mock_context_manager'),
    }
    
    # Add mock classes and enums
    mock_modules['src.enhanced_autocad.error_handler'].ErrorHandler = type('ErrorHandler', (), {})
    mock_modules['src.enhanced_autocad.error_handler'].ErrorCategory = MockErrorCategory
    mock_modules['src.enhanced_autocad.performance_monitor'].PerformanceMonitor = type('PerformanceMonitor', (), {})
    mock_modules['src.enhanced_autocad.performance_monitor'].OperationMetrics = type('OperationMetrics', (), {})
    mock_modules['src.inspection.method_discoverer'].MethodDiscoverer = type('MethodDiscoverer', (), {})
    mock_modules['src.inspection.object_inspector'].ObjectInspector = type('ObjectInspector', (), {})
    mock_modules['src.inspection.object_inspector'].InspectionDepth = MockInspectionDepth
    mock_modules['src.inspection.property_analyzer'].PropertyAnalyzer = type('PropertyAnalyzer', (), {})
    
    # Add MCP integration mocks
    mock_modules['src.mcp_integration.enhanced_mcp_server'].EnhancedMCPServer = type('EnhancedMCPServer', (), {})
    mock_modules['src.mcp_integration.security_manager'].SecurityManager = type('SecurityManager', (), {})
    mock_modules['src.mcp_integration.security_manager'].SecurityError = type('SecurityError', (Exception,), {})
    mock_modules['src.mcp_integration.context_manager'].ContextManager = type('ContextManager', (), {})
    
    # Install mocks
    for module_name, module_obj in mock_modules.items():
        sys.modules[module_name] = module_obj


def run_basic_validation():
    """Run basic validation tests without pytest."""
    
    print("🧪 AutoCAD Debugger Test Suite - Standalone Runner")
    print("=" * 60)
    
    test_results = {
        'passed': 0,
        'failed': 0,
        'errors': []
    }
    
    try:
        print("\n📦 Testing Module Imports...")
        
        # Create mock dependencies first
        create_mock_dependencies()
        
        # Test secure evaluator import
        secure_evaluator_available = False
        try:
            from src.interactive.secure_evaluator import (
                SecureEvaluationError,
                safe_eval,
                is_safe_expression,
                SecureExpressionEvaluator
            )
            print("✅ Secure evaluator imports successful")
            test_results['passed'] += 1
            secure_evaluator_available = True
        except Exception as e:
            print(f"❌ Secure evaluator import failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Secure evaluator import: {e}")
            # Continue without secure evaluator functions
        
        # Test debugger imports
        try:
            from src.interactive.debugger import (
                AutoCADDebugger,
                BreakpointType,
                DebugState,
                Breakpoint,
                DebugFrame,
                VariableWatch,
            )
            print("✅ Debugger imports successful")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Debugger import failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Debugger import: {e}")
            return test_results
        
        print("\n🔧 Testing Basic Functionality...")
        
        # Test enum values
        try:
            assert BreakpointType.LINE.value == "line"
            assert BreakpointType.FUNCTION.value == "function"
            assert BreakpointType.VARIABLE.value == "variable"
            assert BreakpointType.CONDITIONAL.value == "conditional"
            
            assert DebugState.IDLE.value == "idle"
            assert DebugState.RUNNING.value == "running"
            assert DebugState.PAUSED.value == "paused"
            
            print("✅ Enum values correct")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Enum test failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Enum values: {e}")
        
        # Test Breakpoint creation
        try:
            bp = Breakpoint(
                id="test_bp_001",
                type=BreakpointType.LINE,
                filename="test.py",
                line_number=10
            )
            assert bp.id == "test_bp_001"
            assert bp.type == BreakpointType.LINE
            assert bp.filename == "test.py"
            assert bp.line_number == 10
            assert bp.enabled is True
            
            print("✅ Breakpoint creation works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Breakpoint creation failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Breakpoint creation: {e}")
        
        # Test DebugFrame creation
        try:
            frame = DebugFrame(
                frame_id="frame_001",
                filename="test.py",
                line_number=5,
                function_name="test_func",
                local_variables={"x": 1},
                global_variables={"__name__": "__main__"},
                autocad_objects={},
                call_stack=[]
            )
            assert frame.frame_id == "frame_001"
            assert frame.filename == "test.py"
            assert frame.local_variables["x"] == 1
            
            print("✅ DebugFrame creation works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ DebugFrame creation failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"DebugFrame creation: {e}")
        
        # Test VariableWatch creation
        try:
            watch = VariableWatch(
                name="test_watch",
                expression="x + y",
                current_value=42
            )
            assert watch.name == "test_watch"
            assert watch.expression == "x + y"
            assert watch.current_value == 42
            assert watch.change_count == 0
            
            print("✅ VariableWatch creation works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ VariableWatch creation failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"VariableWatch creation: {e}")
        
        # Test AutoCADDebugger instantiation
        try:
            debugger = AutoCADDebugger()
            assert debugger.state == DebugState.IDLE
            assert debugger.session_id is None
            assert debugger.breakpoints == {}
            assert debugger.variable_watches == {}
            assert debugger.max_trace_size == 1000
            
            print("✅ AutoCADDebugger instantiation works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ AutoCADDebugger instantiation failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"AutoCADDebugger instantiation: {e}")
        
        print("\n🎮 Testing Debugger Operations...")
        
        # Test debug session lifecycle
        try:
            debugger = AutoCADDebugger()
            
            # Start session
            session_id = debugger.start_debug_session()
            assert session_id is not None
            assert debugger.state == DebugState.RUNNING
            assert debugger.session_id == session_id
            
            # Stop session
            summary = debugger.stop_debug_session()
            assert "session_id" in summary
            assert summary["session_id"] == session_id
            assert debugger.state == DebugState.IDLE
            assert debugger.session_id is None
            
            print("✅ Debug session lifecycle works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Debug session lifecycle failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Debug session lifecycle: {e}")
        
        # Test breakpoint management
        try:
            debugger = AutoCADDebugger()
            
            # Add breakpoint
            bp_id = debugger.add_breakpoint("line", filename="test.py", line_number=10)
            assert bp_id in debugger.breakpoints
            assert debugger.breakpoints[bp_id].type == BreakpointType.LINE
            
            # Remove breakpoint
            result = debugger.remove_breakpoint(bp_id)
            assert result is True
            assert bp_id not in debugger.breakpoints
            
            print("✅ Breakpoint management works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Breakpoint management failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Breakpoint management: {e}")
        
        # Test variable watch management
        try:
            debugger = AutoCADDebugger()
            
            # Add watch
            watch_id = debugger.add_variable_watch("test_watch", "x + y")
            assert watch_id in debugger.variable_watches
            assert debugger.variable_watches[watch_id].expression == "x + y"
            
            # Remove watch
            result = debugger.remove_variable_watch(watch_id)
            assert result is True
            assert watch_id not in debugger.variable_watches
            
            print("✅ Variable watch management works")
            test_results['passed'] += 1
        except Exception as e:
            print(f"❌ Variable watch management failed: {e}")
            test_results['failed'] += 1
            test_results['errors'].append(f"Variable watch management: {e}")
        
        if secure_evaluator_available:
            print("\n🔒 Testing Secure Evaluation...")
            
            # Test safe expressions
            try:
                safe_expressions = [
                    "1 + 2",
                    "len([1, 2, 3])",
                    "x if x > 0 else 0", 
                    "[i * 2 for i in range(5)]",
                    "{'a': 1, 'b': 2}",
                    "max(1, 2, 3)",
                ]
                
                for expr in safe_expressions:
                    assert is_safe_expression(expr) is True, f"Expression should be safe: {expr}"
                
                print("✅ Safe expression validation works")
                test_results['passed'] += 1
            except Exception as e:
                print(f"❌ Safe expression validation failed: {e}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Safe expression validation: {e}")
            
            # Test unsafe expressions
            try:
                unsafe_expressions = [
                    "__import__('os')",
                    "exec('print(1)')",
                    "eval('1+1')",
                    "open('/etc/passwd')",
                    "__builtins__",
                ]
                
                for expr in unsafe_expressions:
                    assert is_safe_expression(expr) is False, f"Expression should be unsafe: {expr}"
                
                print("✅ Unsafe expression blocking works")
                test_results['passed'] += 1
            except Exception as e:
                print(f"❌ Unsafe expression blocking failed: {e}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Unsafe expression blocking: {e}")
            
            # Test safe evaluation
            try:
                result = safe_eval("2 + 3", {"x": 10}, {"y": 20})
                assert result == 5
                
                result = safe_eval("x * 2", {"x": 10}, {})
                assert result == 20
                
                print("✅ Safe evaluation works")
                test_results['passed'] += 1
            except Exception as e:
                print(f"❌ Safe evaluation failed: {e}")
                test_results['failed'] += 1
                test_results['errors'].append(f"Safe evaluation: {e}")
        else:
            print("\n⚠️  Secure evaluator not available - skipping security tests")
        
    except Exception as e:
        print(f"💥 Critical error during testing: {e}")
        test_results['failed'] += 1
        test_results['errors'].append(f"Critical error: {e}")
        traceback.print_exc()
    
    return test_results


def print_summary(test_results):
    """Print test summary."""
    print("\n" + "=" * 60)
    print("📊 TEST SUMMARY")
    print("=" * 60)
    
    total_tests = test_results['passed'] + test_results['failed']
    pass_rate = (test_results['passed'] / total_tests * 100) if total_tests > 0 else 0
    
    print(f"Total Tests: {total_tests}")
    print(f"Passed: {test_results['passed']} ✅")
    print(f"Failed: {test_results['failed']} ❌")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if test_results['errors']:
        print("\n🔍 ERROR DETAILS:")
        for i, error in enumerate(test_results['errors'], 1):
            print(f"  {i}. {error}")
    
    if test_results['failed'] == 0:
        print("\n🎉 ALL TESTS PASSED! The debugger test suite is structurally sound.")
    else:
        print(f"\n⚠️  {test_results['failed']} test(s) failed. Review errors above.")
    
    return test_results['failed'] == 0


if __name__ == "__main__":
    print("Starting AutoCAD Debugger standalone test validation...")
    results = run_basic_validation()
    success = print_summary(results)
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)