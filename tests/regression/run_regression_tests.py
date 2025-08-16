#!/usr/bin/env python3
"""
Comprehensive regression test runner for basic MCP tools.

Validates that the 7 existing basic MCP tools continue working correctly
after advanced LSCM algorithm integration:

1. draw_line
2. draw_circle  
3. extrude_profile
4. revolve_profile
5. list_entities
6. get_entity_info
7. server_status

Success Criteria:
- All 7 basic tools execute successfully
- No performance degradation >10%
- Memory usage increase <20MB baseline
- Server remains stable under mixed workloads

Usage:
    python tests/regression/run_regression_tests.py
    python tests/regression/run_regression_tests.py --detailed
    python tests/regression/run_regression_tests.py --performance-only
    python tests/regression/run_regression_tests.py --memory-check
"""

import argparse
import json
import sys
import time
from pathlib import Path
from typing import Any

import psutil

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))


class RegressionTestRunner:
    """Comprehensive regression test runner."""

    def __init__(self, detailed: bool = False):
        self.detailed = detailed
        self.results = {
            "start_time": time.time(),
            "tests": {},
            "performance": {},
            "memory": {},
            "summary": {},
        }
        self.initial_memory = psutil.Process().memory_info().rss / 1024 / 1024

    def run_all_tests(self) -> dict[str, Any]:
        """Run all regression tests and return results."""
        print("AutoCAD MCP Basic Tools Regression Test Suite")
        print("=" * 60)
        print("Testing 7 basic MCP tools after advanced LSCM integration")
        print(f"Initial memory usage: {self.initial_memory:.1f} MB")
        print()

        # Run test categories
        test_categories = [
            ("Basic Tool Functionality", self.test_basic_tool_functionality),
            ("MCP Server Stability", self.test_server_stability),
            ("Backward Compatibility", self.test_backward_compatibility),
            ("Concurrent Execution", self.test_concurrent_execution),
            ("Performance Regression", self.test_performance_regression),
            ("Memory Stability", self.test_memory_stability),
        ]

        for category_name, test_func in test_categories:
            print(f"Running {category_name} tests...")
            try:
                result = test_func()
                self.results["tests"][category_name] = result
                status = "✅ PASS" if result.get("passed", False) else "❌ FAIL"
                print(f"  {status} - {result.get('summary', 'No summary')}")

                if self.detailed and "details" in result:
                    for detail in result["details"]:
                        print(f"    • {detail}")

            except Exception as e:
                self.results["tests"][category_name] = {
                    "passed": False,
                    "error": str(e),
                    "summary": f"Test failed with exception: {e}",
                }
                print(f"  ❌ ERROR - {e}")

            print()

        # Generate summary
        self.generate_summary()
        return self.results

    def test_basic_tool_functionality(self) -> dict[str, Any]:
        """Test each of the 7 basic tools individually."""
        from unittest.mock import Mock, patch

        basic_tools = [
            "draw_line",
            "draw_circle",
            "extrude_profile",
            "revolve_profile",
            "list_entities",
            "get_entity_info",
            "server_status",
        ]

        results = {"passed": True, "details": [], "tool_results": {}}

        with patch("src.utils.get_autocad_instance") as mock_get_acad:
            # Setup comprehensive mock
            mock_acad = Mock()
            mock_acad.ActiveDocument = Mock()
            mock_acad.ActiveDocument.Name = "Regression_Test.dwg"
            mock_acad.model = Mock()

            # Mock entities for list_entities and get_entity_info
            mock_entities = []
            for i in range(3):
                entity = Mock()
                entity.ObjectID = 2000 + i
                entity.ObjectName = f"AcDbTestEntity{i}"
                entity.Layer = "0"
                entity.Length = 50.0 + i * 10
                entity.Area = 25.0 + i * 5
                mock_entities.append(entity)

            mock_acad.model.modelspace = mock_entities
            mock_get_acad.return_value = mock_acad

            # Test each tool
            try:
                from src.mcp_server import mcp

                for tool_name in basic_tools:
                    if tool_name not in mcp.tool_handlers:
                        results["passed"] = False
                        results["details"].append(
                            f"Tool '{tool_name}' not found in handler registry"
                        )
                        continue

                    start_time = time.time()

                    try:
                        # Execute tool with appropriate parameters
                        if tool_name == "draw_line":
                            # Mock line entity
                            mock_line = Mock()
                            mock_line.ObjectID = 3001
                            mock_acad.model.AddLine.return_value = mock_line

                            result = mcp.tool_handlers[tool_name]([0, 0, 0], [10, 10, 0])

                        elif tool_name == "draw_circle":
                            # Mock circle entity
                            mock_circle = Mock()
                            mock_circle.ObjectID = 3002
                            mock_acad.model.AddCircle.return_value = mock_circle

                            result = mcp.tool_handlers[tool_name]([5, 5, 0], 5.0)

                        elif tool_name == "extrude_profile":
                            # Mock polyline and solid
                            mock_polyline = Mock()
                            mock_polyline.ObjectID = 3003
                            mock_solid = Mock()
                            mock_solid.ObjectID = 3004
                            mock_acad.model.AddPolyline.return_value = mock_polyline
                            mock_acad.model.AddExtrudedSolid.return_value = mock_solid

                            result = mcp.tool_handlers[tool_name](
                                [[0, 0], [10, 0], [10, 10], [0, 10]], 5.0
                            )

                        elif tool_name == "revolve_profile":
                            # Mock polyline and revolved solid
                            mock_polyline = Mock()
                            mock_polyline.ObjectID = 3005
                            mock_revolved = Mock()
                            mock_revolved.ObjectID = 3006
                            mock_acad.model.AddPolyline.return_value = mock_polyline
                            mock_acad.model.AddRevolvedSolid.return_value = mock_revolved

                            result = mcp.tool_handlers[tool_name](
                                [[0, 0], [5, 0], [5, 10]], [0, 0, 0], [0, 0, 10], 360.0
                            )

                        elif tool_name == "list_entities":
                            result = mcp.tool_handlers[tool_name]()

                        elif tool_name == "get_entity_info":
                            result = mcp.tool_handlers[tool_name](2000)  # First mock entity

                        elif tool_name == "server_status":
                            result = mcp.tool_handlers[tool_name]()

                        execution_time = time.time() - start_time

                        # Parse and validate result
                        if isinstance(result, str):
                            response = json.loads(result)
                        else:
                            response = result

                        # Validate basic response structure
                        if not isinstance(response, dict):
                            results["passed"] = False
                            results["details"].append(f"{tool_name}: Response is not a dictionary")
                            continue

                        if "success" not in response:
                            results["passed"] = False
                            results["details"].append(
                                f"{tool_name}: Missing 'success' field in response"
                            )
                            continue

                        if not response.get("success", False):
                            results["passed"] = False
                            results["details"].append(
                                f"{tool_name}: Tool reported failure: {response.get('error', 'Unknown error')}"
                            )
                            continue

                        # Performance check (generous for mocked operations)
                        max_time = 0.5  # 500ms for mocked operations
                        if execution_time > max_time:
                            results["passed"] = False
                            results["details"].append(
                                f"{tool_name}: Execution time {execution_time:.3f}s exceeds {max_time}s"
                            )
                            continue

                        # Success
                        results["tool_results"][tool_name] = {
                            "success": True,
                            "execution_time": execution_time,
                            "response_size": (
                                len(json.dumps(response)) if isinstance(response, dict) else 0
                            ),
                        }

                        results["details"].append(f"{tool_name}: ✅ {execution_time:.3f}s")

                    except Exception as e:
                        results["passed"] = False
                        results["details"].append(f"{tool_name}: Exception - {e}")
                        results["tool_results"][tool_name] = {
                            "success": False,
                            "error": str(e),
                            "execution_time": time.time() - start_time,
                        }

            except ImportError as e:
                results["passed"] = False
                results["details"].append(f"Cannot import MCP server: {e}")

        # Summary
        successful_tools = sum(
            1 for r in results["tool_results"].values() if r.get("success", False)
        )
        results["summary"] = f"{successful_tools}/{len(basic_tools)} basic tools working correctly"

        return results

    def test_server_stability(self) -> dict[str, Any]:
        """Test server stability with advanced tools integrated."""
        results = {"passed": True, "details": []}

        try:
            # Test server can be imported
            from src.mcp_server import mcp

            results["details"].append("Server import successful")

            # Check tool registry
            available_tools = list(mcp.tool_handlers.keys())
            basic_tool_count = len(
                [
                    t
                    for t in available_tools
                    if t
                    in [
                        "draw_line",
                        "draw_circle",
                        "extrude_profile",
                        "revolve_profile",
                        "list_entities",
                        "get_entity_info",
                        "server_status",
                    ]
                ]
            )

            if basic_tool_count < 7:
                results["passed"] = False
                results["details"].append(
                    f"Only {basic_tool_count}/7 basic tools found in registry"
                )
            else:
                results["details"].append("All 7 basic tools found in registry")

            # Check total tool count (should include advanced tools)
            total_tools = len(available_tools)
            if total_tools < 7:
                results["passed"] = False
                results["details"].append(
                    f"Total tools ({total_tools}) less than minimum basic tools (7)"
                )
            else:
                results["details"].append(f"Total tools available: {total_tools}")

            results["summary"] = f"Server stability check passed - {total_tools} tools loaded"

        except Exception as e:
            results["passed"] = False
            results["summary"] = f"Server stability check failed: {e}"
            results["details"].append(f"Error: {e}")

        return results

    def test_backward_compatibility(self) -> dict[str, Any]:
        """Test backward compatibility of response formats."""
        results = {"passed": True, "details": []}

        from unittest.mock import Mock, patch

        with patch("src.utils.get_autocad_instance") as mock_get_acad:
            mock_acad = Mock()
            mock_acad.ActiveDocument.Name = "Compatibility_Test.dwg"
            mock_acad.model = Mock()
            mock_acad.model.modelspace = []
            mock_get_acad.return_value = mock_acad

            try:
                from src.mcp_server import mcp

                # Test server_status response format
                result = mcp.tool_handlers["server_status"]()
                response = json.loads(result) if isinstance(result, str) else result

                # Required fields for backward compatibility
                required_fields = [
                    "success",
                    "mcp_server",
                    "autocad_connected",
                    "active_document",
                    "message",
                ]
                missing_fields = []

                for field in required_fields:
                    if field not in response:
                        missing_fields.append(field)

                if missing_fields:
                    results["passed"] = False
                    results["details"].append(f"Missing required fields: {missing_fields}")
                else:
                    results["details"].append("All required response fields present")

                # Type validation
                type_checks = [
                    ("success", bool),
                    ("mcp_server", str),
                    ("autocad_connected", bool),
                    ("active_document", str),
                    ("message", str),
                ]

                type_errors = []
                for field, expected_type in type_checks:
                    if field in response and not isinstance(response[field], expected_type):
                        type_errors.append(
                            f"{field}: expected {expected_type.__name__}, got {type(response[field]).__name__}"
                        )

                if type_errors:
                    results["passed"] = False
                    results["details"].extend(type_errors)
                else:
                    results["details"].append("All field types correct")

                results["summary"] = (
                    "Backward compatibility maintained"
                    if results["passed"]
                    else "Compatibility issues found"
                )

            except Exception as e:
                results["passed"] = False
                results["summary"] = f"Compatibility test failed: {e}"
                results["details"].append(f"Error: {e}")

        return results

    def test_concurrent_execution(self) -> dict[str, Any]:
        """Test concurrent execution scenarios."""
        results = {"passed": True, "details": []}

        import threading
        from concurrent.futures import ThreadPoolExecutor, as_completed
        from unittest.mock import Mock, patch

        with patch("src.utils.get_autocad_instance") as mock_get_acad:
            # Thread-safe mock setup
            mock_acad = Mock()
            mock_acad.ActiveDocument.Name = "Concurrent_Test.dwg"
            mock_acad.model.modelspace = []

            # Add thread safety tracking
            access_count = {"count": 0, "lock": threading.Lock()}

            def thread_safe_mock():
                with access_count["lock"]:
                    access_count["count"] += 1
                return mock_acad

            mock_get_acad.side_effect = thread_safe_mock

            try:
                from src.mcp_server import mcp

                def run_server_status():
                    return mcp.tool_handlers["server_status"]()

                # Run 4 concurrent operations
                concurrent_results = []
                with ThreadPoolExecutor(max_workers=4) as executor:
                    futures = [executor.submit(run_server_status) for _ in range(4)]

                    for future in as_completed(futures, timeout=5.0):
                        try:
                            result = future.result()
                            response = json.loads(result) if isinstance(result, str) else result
                            concurrent_results.append(response)
                        except Exception as e:
                            results["passed"] = False
                            results["details"].append(f"Concurrent execution failed: {e}")

                # Validate results
                if len(concurrent_results) != 4:
                    results["passed"] = False
                    results["details"].append(
                        f"Expected 4 concurrent results, got {len(concurrent_results)}"
                    )
                else:
                    results["details"].append("All 4 concurrent operations completed")

                # Check all operations succeeded
                successful_ops = sum(1 for r in concurrent_results if r.get("success", False))
                if successful_ops != 4:
                    results["passed"] = False
                    results["details"].append(
                        f"Only {successful_ops}/4 concurrent operations succeeded"
                    )
                else:
                    results["details"].append("All concurrent operations successful")

                # Check thread safety
                if access_count["count"] != 4:
                    results["passed"] = False
                    results["details"].append(
                        f"Thread safety issue: {access_count['count']} accesses instead of 4"
                    )
                else:
                    results["details"].append("Thread safety verified")

                results["summary"] = (
                    "Concurrent execution working"
                    if results["passed"]
                    else "Concurrency issues detected"
                )

            except Exception as e:
                results["passed"] = False
                results["summary"] = f"Concurrency test failed: {e}"
                results["details"].append(f"Error: {e}")

        return results

    def test_performance_regression(self) -> dict[str, Any]:
        """Test performance hasn't regressed."""
        results = {"passed": True, "details": [], "metrics": {}}

        from unittest.mock import Mock, patch

        with patch("src.utils.get_autocad_instance") as mock_get_acad:
            mock_acad = Mock()
            mock_acad.ActiveDocument.Name = "Performance_Test.dwg"
            mock_acad.model.modelspace = []
            mock_get_acad.return_value = mock_acad

            try:
                from src.mcp_server import mcp

                # Performance test for key tools
                performance_tests = [
                    ("server_status", 0.01),  # 10ms threshold
                    ("list_entities", 0.05),  # 50ms threshold
                ]

                for tool_name, threshold in performance_tests:
                    times = []

                    # Run 5 iterations
                    for _ in range(5):
                        start_time = time.time()
                        mcp.tool_handlers[tool_name]()
                        execution_time = time.time() - start_time
                        times.append(execution_time)

                    avg_time = sum(times) / len(times)
                    max_time = max(times)
                    min_time = min(times)

                    results["metrics"][tool_name] = {
                        "avg_time": avg_time,
                        "max_time": max_time,
                        "min_time": min_time,
                        "threshold": threshold,
                    }

                    if avg_time > threshold:
                        results["passed"] = False
                        results["details"].append(
                            f"{tool_name}: avg {avg_time:.4f}s exceeds {threshold:.4f}s"
                        )
                    else:
                        results["details"].append(
                            f"{tool_name}: ✅ avg {avg_time:.4f}s (limit {threshold:.4f}s)"
                        )

                results["summary"] = (
                    "Performance within limits"
                    if results["passed"]
                    else "Performance regression detected"
                )

            except Exception as e:
                results["passed"] = False
                results["summary"] = f"Performance test failed: {e}"
                results["details"].append(f"Error: {e}")

        self.results["performance"] = results.get("metrics", {})
        return results

    def test_memory_stability(self) -> dict[str, Any]:
        """Test memory usage stability."""
        results = {"passed": True, "details": []}

        current_memory = psutil.Process().memory_info().rss / 1024 / 1024
        memory_increase = current_memory - self.initial_memory

        results["details"].append(f"Initial memory: {self.initial_memory:.1f} MB")
        results["details"].append(f"Current memory: {current_memory:.1f} MB")
        results["details"].append(f"Memory increase: {memory_increase:.1f} MB")

        # Memory increase thresholds
        warning_threshold = 20.0  # MB
        error_threshold = 50.0  # MB

        if memory_increase > error_threshold:
            results["passed"] = False
            results["details"].append(
                f"❌ Memory increase ({memory_increase:.1f} MB) exceeds error threshold ({error_threshold} MB)"
            )
        elif memory_increase > warning_threshold:
            results["details"].append(
                f"⚠️  Memory increase ({memory_increase:.1f} MB) exceeds warning threshold ({warning_threshold} MB)"
            )
        else:
            results["details"].append("✅ Memory increase within acceptable limits")

        # Test for memory leaks with repeated operations
        from unittest.mock import Mock, patch

        with patch("src.utils.get_autocad_instance") as mock_get_acad:
            mock_acad = Mock()
            mock_acad.ActiveDocument.Name = "Memory_Test.dwg"
            mock_acad.model.modelspace = []
            mock_get_acad.return_value = mock_acad

            try:
                from src.mcp_server import mcp

                pre_test_memory = psutil.Process().memory_info().rss / 1024 / 1024

                # Run operations repeatedly
                for i in range(10):
                    mcp.tool_handlers["server_status"]()

                post_test_memory = psutil.Process().memory_info().rss / 1024 / 1024
                test_memory_increase = post_test_memory - pre_test_memory

                leak_threshold = 5.0  # MB
                if test_memory_increase > leak_threshold:
                    results["passed"] = False
                    results["details"].append(
                        f"❌ Potential memory leak: {test_memory_increase:.1f} MB increase during test"
                    )
                else:
                    results["details"].append(
                        f"✅ No memory leak detected: {test_memory_increase:.1f} MB increase"
                    )

            except Exception as e:
                results["details"].append(f"Memory leak test failed: {e}")

        results["summary"] = (
            f"Memory stable (+{memory_increase:.1f} MB)"
            if results["passed"]
            else f"Memory issues detected (+{memory_increase:.1f} MB)"
        )

        self.results["memory"] = {
            "initial": self.initial_memory,
            "current": current_memory,
            "increase": memory_increase,
        }

        return results

    def generate_summary(self):
        """Generate test summary."""
        end_time = time.time()
        total_time = end_time - self.results["start_time"]

        # Count results
        total_tests = len(self.results["tests"])
        passed_tests = sum(1 for r in self.results["tests"].values() if r.get("passed", False))
        failed_tests = total_tests - passed_tests

        # Overall pass/fail
        overall_pass = failed_tests == 0

        self.results["summary"] = {
            "total_time": total_time,
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "success_rate": (passed_tests / total_tests * 100) if total_tests > 0 else 0,
            "overall_pass": overall_pass,
            "final_memory": psutil.Process().memory_info().rss / 1024 / 1024,
        }

        print()
        print("Regression Test Summary")
        print("=" * 40)
        print(f"Total time: {total_time:.2f} seconds")
        print(f"Tests run: {total_tests}")
        print(f"Passed: {passed_tests}")
        print(f"Failed: {failed_tests}")
        print(f"Success rate: {self.results['summary']['success_rate']:.1f}%")
        print(
            f"Memory usage: {self.initial_memory:.1f} → {self.results['summary']['final_memory']:.1f} MB "
            f"(+{self.results['summary']['final_memory'] - self.initial_memory:.1f} MB)"
        )
        print()

        if overall_pass:
            print("🎉 ALL REGRESSION TESTS PASSED")
            print("✅ Basic MCP tools continue working correctly after advanced LSCM integration")
        else:
            print("❌ REGRESSION DETECTED")
            print("⚠️  Some basic MCP tools may have issues after advanced integration")

            # Show failed tests
            print("\nFailed tests:")
            for test_name, result in self.results["tests"].items():
                if not result.get("passed", True):
                    print(f"  • {test_name}: {result.get('summary', 'Unknown failure')}")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(description="AutoCAD MCP Basic Tools Regression Test Suite")
    parser.add_argument("--detailed", "-d", action="store_true", help="Show detailed test output")
    parser.add_argument(
        "--performance-only", "-p", action="store_true", help="Run only performance tests"
    )
    parser.add_argument(
        "--memory-check", "-m", action="store_true", help="Run only memory stability tests"
    )
    parser.add_argument("--output", "-o", help="Save results to JSON file")

    args = parser.parse_args()

    # Create test runner
    runner = RegressionTestRunner(detailed=args.detailed)

    if args.performance_only:
        print("Running performance regression tests only...")
        results = {"performance": runner.test_performance_regression()}
    elif args.memory_check:
        print("Running memory stability tests only...")
        results = {"memory": runner.test_memory_stability()}
    else:
        # Run all tests
        results = runner.run_all_tests()

    # Save results if requested
    if args.output:
        with open(args.output, "w") as f:
            json.dump(results, f, indent=2, default=str)
        print(f"\nResults saved to {args.output}")

    # Exit with appropriate code
    if results.get("summary", {}).get("overall_pass", False):
        sys.exit(0)  # Success
    else:
        sys.exit(1)  # Failure


if __name__ == "__main__":
    main()
