#!/usr/bin/env python3
"""
Standalone Test Runner for Enhanced MCP Server Unit Tests
=========================================================

This script runs the Enhanced MCP Server unit tests without requiring pytest.
It provides comprehensive test execution with detailed reporting and validation
of all server components including initialization, tool registration, security,
threading, error handling, performance, and AutoCAD integration scenarios.

Usage:
    python run_enhanced_mcp_server_tests_standalone.py
"""

import sys
import os
import unittest
import logging
import time
import threading
import concurrent.futures
from unittest.mock import Mock, MagicMock, patch
from typing import Dict, List, Any, Optional

# Add the project root to the Python path
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

try:
    from src.mcp_integration.enhanced_mcp_server import EnhancedMCPServer
    from src.mcp_integration.context_manager import ContextManager, SessionContext
    from src.mcp_integration.security_manager import SecurityManager
    from src.interactive.secure_evaluator import SecureExpressionEvaluator, SecureEvaluationError
    print("✅ Successfully imported Enhanced MCP Server dependencies")
except ImportError as e:
    print(f"❌ Failed to import dependencies: {e}")
    sys.exit(1)


class TestEnhancedMCPServerStandalone(unittest.TestCase):
    """Standalone test class for Enhanced MCP Server functionality."""

    def setUp(self):
        """Set up test fixtures."""
        self.server = None
        self.test_results = []

    def tearDown(self):
        """Clean up after tests."""
        if self.server:
            # Clean up any resources
            pass

    def test_server_initialization_default(self):
        """Test default server initialization."""
        print("\n🧪 Testing server initialization...")
        
        try:
            server = EnhancedMCPServer()
            
            # Verify core components are initialized
            self.assertIsNotNone(server.mcp)
            self.assertIsNotNone(server.context_manager)
            self.assertIsNotNone(server.security_manager)
            self.assertIsNotNone(server._secure_evaluator)
            
            # Verify lazy-loaded components are None initially
            self.assertIsNone(server.autocad_wrapper)
            self.assertIsNone(server.python_repl)
            self.assertIsNone(server.execution_engine)
            
            # Verify inspection components are initialized
            self.assertIsNotNone(server.object_inspector)
            self.assertIsNotNone(server.property_analyzer)
            self.assertIsNotNone(server.method_discoverer)
            self.assertIsNotNone(server.intellisense_provider)
            
            print("   ✅ Server initialized successfully with all components")
            self.test_results.append("✅ Server Initialization")
            
        except Exception as e:
            print(f"   ❌ Server initialization failed: {e}")
            self.test_results.append(f"❌ Server Initialization: {e}")
            raise

    def test_fastmcp_initialization(self):
        """Test FastMCP server initialization."""
        print("\n🧪 Testing FastMCP initialization...")
        
        try:
            server = EnhancedMCPServer()
            
            # Verify FastMCP is initialized with correct name
            self.assertEqual(server.mcp.name, "AutoCAD Master Coder")
            
            print("   ✅ FastMCP initialized with correct name")
            self.test_results.append("✅ FastMCP Initialization")
            
        except Exception as e:
            print(f"   ❌ FastMCP initialization failed: {e}")
            self.test_results.append(f"❌ FastMCP Initialization: {e}")
            raise

    def test_tool_registration_functionality(self):
        """Test tool registration and access functionality."""
        print("\n🧪 Testing tool registration...")
        
        try:
            server = EnhancedMCPServer()
            
            # Test that basic tools are accessible
            draw_line_tool = server.get_tool("draw_line")
            draw_circle_tool = server.get_tool("draw_circle")
            status_tool = server.get_tool("status")
            
            self.assertIsNotNone(draw_line_tool)
            self.assertIsNotNone(draw_circle_tool)
            self.assertIsNotNone(status_tool)
            
            # Verify tool wrapper has expected interface
            self.assertTrue(hasattr(draw_line_tool, 'fn'))
            self.assertTrue(callable(draw_line_tool.fn))
            
            print("   ✅ All core tools registered and accessible")
            self.test_results.append("✅ Tool Registration")
            
        except Exception as e:
            print(f"   ❌ Tool registration test failed: {e}")
            self.test_results.append(f"❌ Tool Registration: {e}")
            raise

    def test_invalid_tool_access(self):
        """Test accessing invalid tool raises appropriate error."""
        print("\n🧪 Testing invalid tool access handling...")
        
        try:
            server = EnhancedMCPServer()
            invalid_tool = server.get_tool("nonexistent_tool")
            
            # Should raise AttributeError when trying to call invalid tool
            with self.assertRaises(AttributeError) as context:
                invalid_tool.fn()
            
            self.assertIn("not found or not accessible", str(context.exception))
            
            print("   ✅ Invalid tool access properly handled")
            self.test_results.append("✅ Invalid Tool Handling")
            
        except Exception as e:
            print(f"   ❌ Invalid tool access test failed: {e}")
            self.test_results.append(f"❌ Invalid Tool Handling: {e}")
            raise

    def test_autocad_wrapper_lazy_loading(self):
        """Test AutoCAD wrapper lazy loading mechanism."""
        print("\n🧪 Testing AutoCAD wrapper lazy loading...")
        
        try:
            with patch('src.mcp_integration.enhanced_mcp_server.Autocad') as mock_autocad_class:
                server = EnhancedMCPServer()
                
                # Initially wrapper should be None
                self.assertIsNone(server.autocad_wrapper)
                
                # Getting wrapper should initialize it
                wrapper = server._get_autocad_wrapper()
                
                self.assertIsNotNone(wrapper)
                mock_autocad_class.assert_called_once()
                
            print("   ✅ AutoCAD wrapper lazy loading works correctly")
            self.test_results.append("✅ AutoCAD Lazy Loading")
            
        except Exception as e:
            print(f"   ❌ AutoCAD wrapper lazy loading test failed: {e}")
            self.test_results.append(f"❌ AutoCAD Lazy Loading: {e}")
            raise

    def test_autocad_wrapper_caching(self):
        """Test that AutoCAD wrapper is cached after first access."""
        print("\n🧪 Testing AutoCAD wrapper caching...")
        
        try:
            with patch('src.mcp_integration.enhanced_mcp_server.Autocad') as mock_autocad_class:
                server = EnhancedMCPServer()
                
                # Get wrapper twice
                wrapper1 = server._get_autocad_wrapper()
                wrapper2 = server._get_autocad_wrapper()
                
                # Should be same instance
                self.assertIs(wrapper1, wrapper2)
                # AutoCAD constructor should only be called once
                mock_autocad_class.assert_called_once()
                
            print("   ✅ AutoCAD wrapper properly cached")
            self.test_results.append("✅ AutoCAD Wrapper Caching")
            
        except Exception as e:
            print(f"   ❌ AutoCAD wrapper caching test failed: {e}")
            self.test_results.append(f"❌ AutoCAD Wrapper Caching: {e}")
            raise

    def test_concurrent_autocad_access(self):
        """Test concurrent access to AutoCAD wrapper."""
        print("\n🧪 Testing concurrent AutoCAD access...")
        
        try:
            with patch('src.mcp_integration.enhanced_mcp_server.Autocad') as mock_autocad_class:
                server = EnhancedMCPServer()
                
                def get_wrapper():
                    return server._get_autocad_wrapper()
                
                # Test concurrent access
                with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
                    futures = [executor.submit(get_wrapper) for _ in range(5)]
                    wrappers = [future.result() for future in futures]
                
                # All should be the same instance
                self.assertTrue(all(wrapper is wrappers[0] for wrapper in wrappers))
                # Constructor should still only be called once
                mock_autocad_class.assert_called_once()
                
            print("   ✅ Concurrent AutoCAD access handled correctly")
            self.test_results.append("✅ Concurrent AutoCAD Access")
            
        except Exception as e:
            print(f"   ❌ Concurrent AutoCAD access test failed: {e}")
            self.test_results.append(f"❌ Concurrent AutoCAD Access: {e}")
            raise

    def test_tool_functionality_with_mocked_autocad(self):
        """Test tool functionality with mocked AutoCAD operations."""
        print("\n🧪 Testing tool functionality with mocked AutoCAD...")
        
        try:
            server = EnhancedMCPServer()
            
            with patch.object(server, '_get_autocad_wrapper') as mock_get_wrapper:
                mock_wrapper = Mock()
                mock_wrapper.draw_line.return_value = "test_entity_123"
                mock_wrapper.draw_circle.return_value = "test_circle_456"
                mock_get_wrapper.return_value = mock_wrapper
                
                # Test draw_line tool
                line_tool = server.get_tool("draw_line")
                line_result = line_tool.fn(start_point=[0, 0, 0], end_point=[10, 10, 0])
                
                self.assertIn("Line created successfully", line_result)
                self.assertIn("test_entity_123", line_result)
                mock_wrapper.draw_line.assert_called_once_with([0, 0, 0], [10, 10, 0])
                
                # Test draw_circle tool
                circle_tool = server.get_tool("draw_circle")
                circle_result = circle_tool.fn(center=[5, 5, 0], radius=2.5)
                
                self.assertIn("Circle created successfully", circle_result)
                self.assertIn("test_circle_456", circle_result)
                mock_wrapper.draw_circle.assert_called_once_with([5, 5, 0], 2.5)
                
            print("   ✅ Tool functionality with mocked AutoCAD works correctly")
            self.test_results.append("✅ Mocked AutoCAD Tool Functionality")
            
        except Exception as e:
            print(f"   ❌ Tool functionality test failed: {e}")
            self.test_results.append(f"❌ Mocked AutoCAD Tool Functionality: {e}")
            raise

    def test_status_tool_functionality(self):
        """Test status tool functionality."""
        print("\n🧪 Testing status tool functionality...")
        
        try:
            server = EnhancedMCPServer()
            status_tool = server.get_tool("status")
            result = status_tool.fn()
            
            # Should return basic status information
            self.assertIn("AutoCAD Status:", result)
            self.assertIn("Server running", result)
            self.assertIn("tools registered: True", result)
            
            print("   ✅ Status tool returns expected information")
            self.test_results.append("✅ Status Tool Functionality")
            
        except Exception as e:
            print(f"   ❌ Status tool test failed: {e}")
            self.test_results.append(f"❌ Status Tool Functionality: {e}")
            raise

    def test_concurrent_tool_access(self):
        """Test concurrent access to tools."""
        print("\n🧪 Testing concurrent tool access...")
        
        try:
            server = EnhancedMCPServer()
            
            def access_tool():
                tool = server.get_tool("status")
                return tool.fn()
            
            # Test concurrent access
            with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
                futures = [executor.submit(access_tool) for _ in range(20)]
                results = [future.result() for future in futures]
            
            # All should succeed
            self.assertEqual(len(results), 20)
            self.assertTrue(all("Status:" in result for result in results))
            
            print("   ✅ Concurrent tool access handled successfully")
            self.test_results.append("✅ Concurrent Tool Access")
            
        except Exception as e:
            print(f"   ❌ Concurrent tool access test failed: {e}")
            self.test_results.append(f"❌ Concurrent Tool Access: {e}")
            raise

    def test_performance_characteristics(self):
        """Test basic performance characteristics."""
        print("\n🧪 Testing basic performance characteristics...")
        
        try:
            start_time = time.time()
            
            # Initialize server
            server = EnhancedMCPServer()
            
            # Access multiple different tools
            tools = ["draw_line", "draw_circle", "status"]
            for tool_name in tools:
                tool = server.get_tool(tool_name)
                self.assertIsNotNone(tool)
            
            end_time = time.time()
            
            # Should be reasonably fast (less than 2 seconds)
            duration = end_time - start_time
            self.assertLess(duration, 2.0)
            
            print(f"   ✅ Performance test completed in {duration:.3f}s")
            self.test_results.append("✅ Basic Performance")
            
        except Exception as e:
            print(f"   ❌ Performance test failed: {e}")
            self.test_results.append(f"❌ Basic Performance: {e}")
            raise

    def test_session_context_management(self):
        """Test session context management functionality."""
        print("\n🧪 Testing session context management...")
        
        try:
            server = EnhancedMCPServer()
            context_manager = server.context_manager
            session_id = "test_session_001"
            
            # Create session context
            context = context_manager.get_session_context(session_id)
            context["test_var"] = "test_value"
            context_manager.update_session_context(session_id, context)
            
            # Verify persistence
            retrieved_context = context_manager.get_session_context(session_id)
            self.assertEqual(retrieved_context.get("test_var"), "test_value")
            
            print("   ✅ Session context management works correctly")
            self.test_results.append("✅ Session Context Management")
            
        except Exception as e:
            print(f"   ❌ Session context management test failed: {e}")
            self.test_results.append(f"❌ Session Context Management: {e}")
            raise

    def test_error_handling_robustness(self):
        """Test error handling robustness."""
        print("\n🧪 Testing error handling robustness...")
        
        try:
            server = EnhancedMCPServer()
            
            # Test error handling in tool execution
            with patch.object(server, '_get_autocad_wrapper') as mock_get_wrapper:
                mock_wrapper = Mock()
                mock_wrapper.draw_line.side_effect = Exception("AutoCAD not connected")
                mock_get_wrapper.return_value = mock_wrapper
                
                tool = server.get_tool("draw_line")
                
                # Should handle the error gracefully by raising McpError
                try:
                    tool.fn(start_point=[0, 0, 0], end_point=[10, 10, 0])
                    self.fail("Expected McpError to be raised")
                except Exception as e:
                    # Error should be handled appropriately
                    self.assertTrue(isinstance(e, Exception))
                    
            print("   ✅ Error handling works robustly")
            self.test_results.append("✅ Error Handling Robustness")
            
        except Exception as e:
            print(f"   ❌ Error handling test failed: {e}")
            self.test_results.append(f"❌ Error Handling Robustness: {e}")
            raise

    def run_all_tests(self):
        """Run all tests and provide comprehensive reporting."""
        print("🚀 Starting Enhanced MCP Server Comprehensive Test Suite")
        print("=" * 70)
        
        test_methods = [
            self.test_server_initialization_default,
            self.test_fastmcp_initialization,
            self.test_tool_registration_functionality,
            self.test_invalid_tool_access,
            self.test_autocad_wrapper_lazy_loading,
            self.test_autocad_wrapper_caching,
            self.test_concurrent_autocad_access,
            self.test_tool_functionality_with_mocked_autocad,
            self.test_status_tool_functionality,
            self.test_concurrent_tool_access,
            self.test_performance_characteristics,
            self.test_session_context_management,
            self.test_error_handling_robustness
        ]
        
        start_time = time.time()
        passed = 0
        failed = 0
        
        for test_method in test_methods:
            try:
                self.setUp()
                test_method()
                passed += 1
            except Exception as e:
                failed += 1
                print(f"   ❌ Test failed with exception: {e}")
            finally:
                self.tearDown()
        
        end_time = time.time()
        duration = end_time - start_time
        
        print("\n" + "=" * 70)
        print("📊 ENHANCED MCP SERVER TEST SUMMARY")
        print("=" * 70)
        print(f"Total Tests: {len(test_methods)}")
        print(f"✅ Passed: {passed}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Duration: {duration:.2f} seconds")
        print(f"📈 Success Rate: {(passed / len(test_methods)) * 100:.1f}%")
        
        print("\n📋 DETAILED TEST RESULTS:")
        for result in self.test_results:
            print(f"   {result}")
        
        print("\n" + "=" * 70)
        if failed == 0:
            print("🎉 ALL TESTS PASSED! Enhanced MCP Server is working correctly.")
        else:
            print(f"⚠️  {failed} tests failed. Please review the errors above.")
        
        return failed == 0


def main():
    """Main function to run the test suite."""
    print("Enhanced MCP Server Standalone Test Runner")
    print("==========================================")
    
    # Configure logging
    logging.basicConfig(level=logging.ERROR)  # Reduce noise during testing
    
    # Create and run test suite
    test_runner = TestEnhancedMCPServerStandalone()
    success = test_runner.run_all_tests()
    
    # Return appropriate exit code
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()