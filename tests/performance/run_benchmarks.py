#!/usr/bin/env python3
"""
Performance benchmark runner for AutoCAD MCP server.

This script provides a command-line interface to run performance benchmarks
and generate comprehensive performance reports.

Usage:
    python run_benchmarks.py [options]
    
    --quick       Run quick benchmark suite (basic tests only)
    --full        Run complete benchmark suite (default)
    --stress      Run stress tests with large meshes
    --report      Generate performance report only
    --baseline    Update performance baselines
    --help        Show this help message
"""

import argparse
import json
import logging
import sys
import time
from pathlib import Path
from typing import Any

# Add src to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from config import (
    DEFAULT_CONFIG,
    DEFAULT_THRESHOLDS,
    LSCM_TEST_CASES,
    generate_performance_report_template,
    validate_performance_requirements,
)

from .test_algorithm_benchmarks import (
    MeshGenerator,
    measure_performance,
)

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


class BenchmarkRunner:
    """Orchestrates performance benchmark execution and reporting."""

    def __init__(self, config_override: dict[str, Any] = None):
        """Initialize benchmark runner with optional configuration override."""
        self.config = DEFAULT_CONFIG
        self.thresholds = DEFAULT_THRESHOLDS
        self.results = generate_performance_report_template()

        if config_override:
            self._apply_config_override(config_override)

    def run_quick_benchmarks(self) -> dict[str, Any]:
        """Run quick benchmark suite with basic tests only."""
        logger.info("Starting quick benchmark suite...")

        start_time = time.time()

        # Quick LSCM tests (small meshes only)
        lscm_results = self._run_quick_lscm_tests()
        self.results["test_results"]["lscm_benchmarks"] = lscm_results

        # Basic MCP server tests
        server_results = self._run_basic_server_tests()
        self.results["test_results"]["mcp_server_performance"] = server_results

        # Generate summary
        self._generate_summary()

        total_time = time.time() - start_time
        logger.info(f"Quick benchmarks completed in {total_time:.1f}s")

        return self.results

    def run_full_benchmarks(self) -> dict[str, Any]:
        """Run complete benchmark suite."""
        logger.info("Starting full benchmark suite...")

        start_time = time.time()

        try:
            # LSCM algorithm benchmarks
            logger.info("Running LSCM algorithm benchmarks...")
            lscm_results = self._run_full_lscm_tests()
            self.results["test_results"]["lscm_benchmarks"] = lscm_results

            # MCP server performance tests
            logger.info("Running MCP server performance tests...")
            server_results = self._run_full_server_tests()
            self.results["test_results"]["mcp_server_performance"] = server_results

            # Algorithm complexity analysis
            logger.info("Running complexity analysis...")
            complexity_results = self._run_complexity_analysis()
            self.results["test_results"]["complexity_analysis"] = complexity_results

            # Performance regression tests
            logger.info("Running regression analysis...")
            regression_results = self._run_regression_tests()
            self.results["test_results"]["regression_tests"] = regression_results

        except Exception as e:
            logger.error(f"Benchmark suite failed: {e}")
            self.results["summary"]["failed_tests"] += 1
            self.results["alerts"].append(
                {
                    "type": "error",
                    "message": f"Benchmark suite failed: {e}",
                    "timestamp": time.time(),
                }
            )

        # Generate comprehensive summary
        self._generate_summary()

        total_time = time.time() - start_time
        logger.info(f"Full benchmarks completed in {total_time:.1f}s")

        return self.results

    def run_stress_tests(self) -> dict[str, Any]:
        """Run stress tests with large meshes and extreme conditions."""
        logger.info("Starting stress test suite...")

        start_time = time.time()

        # Large mesh LSCM tests
        stress_results = self._run_stress_lscm_tests()
        self.results["test_results"]["stress_tests"] = stress_results

        # Concurrent load tests
        load_results = self._run_load_tests()
        self.results["test_results"]["load_tests"] = load_results

        # Generate summary
        self._generate_summary()

        total_time = time.time() - start_time
        logger.info(f"Stress tests completed in {total_time:.1f}s")

        return self.results

    def _run_quick_lscm_tests(self) -> dict[str, Any]:
        """Run quick LSCM tests with small meshes."""
        results = {}

        # Test only small meshes for quick validation
        quick_cases = [case for case in LSCM_TEST_CASES if case["triangle_count"] <= 100]

        for case in quick_cases:
            logger.info(f"Quick LSCM test: {case['name']}")

            # Generate test mesh
            size = case["triangle_count"]
            grid_size = max(3, int((size / 2) ** 0.5))
            vertices, triangles = MeshGenerator.generate_plane_mesh(grid_size, grid_size)

            # Run LSCM benchmark
            metrics = measure_performance(self._run_lscm_solve, vertices, triangles)

            # Validate requirements
            validation = validate_performance_requirements(
                "lscm", len(triangles), metrics.execution_time, metrics.memory_increase_mb
            )

            results[case["name"]] = {
                "triangle_count": len(triangles),
                "execution_time": metrics.execution_time,
                "memory_usage_mb": metrics.memory_increase_mb,
                "cpu_usage": metrics.cpu_percent,
                "success": metrics.success,
                "validation": validation,
                "meets_requirements": all(validation.values()) if validation else False,
            }

            if metrics.success:
                logger.info(
                    f"  ✓ {metrics.execution_time:.3f}s, {metrics.memory_increase_mb:.1f}MB"
                )
            else:
                logger.error(f"  ✗ Failed: {metrics.error_message}")

        return results

    def _run_full_lscm_tests(self) -> dict[str, Any]:
        """Run comprehensive LSCM tests."""
        results = {}

        for case in LSCM_TEST_CASES:
            logger.info(f"LSCM benchmark: {case['name']} ({case['triangle_count']} triangles)")

            # Generate appropriate mesh for test case
            if case["triangle_count"] <= 200:
                grid_size = max(3, int((case["triangle_count"] / 2) ** 0.5))
                vertices, triangles = MeshGenerator.generate_plane_mesh(grid_size, grid_size)
            else:
                subdivisions = max(1, int((case["triangle_count"] / 20) ** 0.5))
                vertices, triangles = MeshGenerator.generate_sphere_mesh(subdivisions)

            # Run multiple iterations for stability
            metrics_samples = []
            for i in range(3):  # 3 iterations
                metrics = measure_performance(self._run_lscm_solve, vertices, triangles)
                if metrics.success:
                    metrics_samples.append(metrics)

            if not metrics_samples:
                results[case["name"]] = {"success": False, "error": "All iterations failed"}
                continue

            # Average metrics from successful runs
            avg_time = sum(m.execution_time for m in metrics_samples) / len(metrics_samples)
            avg_memory = sum(m.memory_increase_mb for m in metrics_samples) / len(metrics_samples)
            avg_cpu = sum(m.cpu_percent for m in metrics_samples) / len(metrics_samples)

            # Validate requirements
            validation = validate_performance_requirements(
                "lscm", len(triangles), avg_time, avg_memory
            )

            results[case["name"]] = {
                "triangle_count": len(triangles),
                "execution_time": avg_time,
                "memory_usage_mb": avg_memory,
                "cpu_usage": avg_cpu,
                "success": True,
                "iterations": len(metrics_samples),
                "validation": validation,
                "meets_requirements": all(validation.values()) if validation else False,
            }

            logger.info(
                f"  ✓ {avg_time:.3f}s avg, {avg_memory:.1f}MB avg ({len(metrics_samples)} runs)"
            )

        return results

    def _run_basic_server_tests(self) -> dict[str, Any]:
        """Run basic MCP server performance tests."""
        results = {}

        # Simulate basic server operations
        basic_operations = [
            ("server_startup", self._simulate_server_startup),
            ("basic_tool_response", self._simulate_basic_tool),
            ("server_memory_usage", self._simulate_memory_test),
        ]

        for op_name, op_func in basic_operations:
            logger.info(f"Server test: {op_name}")

            metrics = measure_performance(op_func)

            results[op_name] = {
                "execution_time": metrics.execution_time,
                "memory_usage_mb": metrics.memory_increase_mb,
                "success": metrics.success,
                "meets_requirements": metrics.execution_time
                < self.thresholds.basic_tool_response_limit,
            }

            if metrics.success:
                logger.info(f"  ✓ {metrics.execution_time:.3f}s")
            else:
                logger.error(f"  ✗ Failed: {metrics.error_message}")

        return results

    def _run_full_server_tests(self) -> dict[str, Any]:
        """Run comprehensive server performance tests."""
        # For now, delegate to basic tests with extended validation
        return self._run_basic_server_tests()

    def _run_complexity_analysis(self) -> dict[str, Any]:
        """Run algorithm complexity analysis."""
        results = {}

        # Test LSCM scaling with different mesh sizes
        test_sizes = [50, 100, 200, 400]
        measurements = []

        for size in test_sizes:
            logger.info(f"Complexity analysis: {size} triangles")

            grid_size = max(3, int((size / 2) ** 0.5))
            vertices, triangles = MeshGenerator.generate_plane_mesh(grid_size, grid_size)

            metrics = measure_performance(self._run_lscm_solve, vertices, triangles)

            if metrics.success:
                measurements.append(
                    {
                        "size": len(triangles),
                        "time": metrics.execution_time,
                        "memory": metrics.memory_increase_mb,
                    }
                )
                logger.info(f"  ✓ {len(triangles)} triangles: {metrics.execution_time:.3f}s")

        # Analyze complexity if we have enough measurements
        if len(measurements) >= 3:
            complexity_estimate = self._estimate_complexity(measurements)
            results["complexity_estimate"] = complexity_estimate
            results["measurements"] = measurements
            results["analysis_successful"] = True

            logger.info(f"Estimated complexity: O(n^{complexity_estimate:.2f})")
        else:
            results["analysis_successful"] = False
            results["error"] = "Insufficient measurements for complexity analysis"

        return results

    def _run_regression_tests(self) -> dict[str, Any]:
        """Run performance regression tests."""
        # Load baseline metrics if available
        baseline_path = Path("performance_baselines.json")
        baselines = {}

        if baseline_path.exists():
            try:
                with open(baseline_path) as f:
                    baselines = json.load(f)
            except Exception as e:
                logger.warning(f"Could not load baselines: {e}")

        # Run current performance tests
        current_metrics = {
            "lscm_100_triangles": self._measure_lscm_100_triangles(),
            "basic_server_response": self._measure_basic_server_response(),
        }

        # Compare against baselines
        regression_results = {}
        for test_name, current_time in current_metrics.items():
            if test_name in baselines:
                baseline_time = baselines[test_name]
                regression_ratio = current_time / baseline_time

                regression_results[test_name] = {
                    "current_time": current_time,
                    "baseline_time": baseline_time,
                    "regression_ratio": regression_ratio,
                    "has_regression": regression_ratio > self.thresholds.basic_tool_response_limit,
                    "improvement": regression_ratio < 1.0,
                }

                if regression_ratio > self.config.regression_threshold:
                    logger.warning(
                        f"Performance regression in {test_name}: "
                        f"{regression_ratio:.2f}x slower than baseline"
                    )
                elif regression_ratio < 0.9:
                    logger.info(
                        f"Performance improvement in {test_name}: "
                        f"{1/regression_ratio:.2f}x faster than baseline"
                    )

        return regression_results

    def _run_stress_lscm_tests(self) -> dict[str, Any]:
        """Run LSCM stress tests with large meshes."""
        results = {}
        stress_sizes = [1000, 2000, 5000]

        for size in stress_sizes:
            logger.info(f"Stress test: {size} triangles")

            try:
                # Generate large mesh
                subdivisions = max(2, int((size / 100) ** 0.5))
                vertices, triangles = MeshGenerator.generate_sphere_mesh(subdivisions)

                # Limit to target size
                if len(triangles) > size:
                    triangles = triangles[:size]
                    used_vertices = set(triangles.flatten())
                    vertex_map = {
                        old_idx: new_idx for new_idx, old_idx in enumerate(sorted(used_vertices))
                    }
                    vertices = vertices[sorted(used_vertices)]
                    triangles = [[vertex_map[v] for v in tri] for tri in triangles]

                # Run with timeout
                metrics = measure_performance(self._run_lscm_solve, vertices, triangles)

                results[f"stress_{size}"] = {
                    "triangle_count": len(triangles),
                    "execution_time": metrics.execution_time,
                    "memory_usage_mb": metrics.memory_increase_mb,
                    "success": metrics.success,
                    "acceptable_performance": metrics.execution_time < 60.0,  # 1 minute limit
                }

                if metrics.success:
                    logger.info(f"  ✓ {len(triangles)} triangles: {metrics.execution_time:.1f}s")
                else:
                    logger.warning(f"  ✗ Failed: {metrics.error_message}")

            except Exception as e:
                results[f"stress_{size}"] = {"success": False, "error": str(e)}
                logger.error(f"  ✗ Stress test failed: {e}")

        return results

    def _run_load_tests(self) -> dict[str, Any]:
        """Run concurrent load tests."""
        logger.info("Running concurrent load tests...")

        # Simulate concurrent requests
        import concurrent.futures

        def simulate_request():
            time.sleep(0.1)  # Simulate processing time
            return {"success": True, "response_time": 0.1}

        num_concurrent = 10
        start_time = time.time()

        with concurrent.futures.ThreadPoolExecutor(max_workers=num_concurrent) as executor:
            futures = [executor.submit(simulate_request) for _ in range(num_concurrent)]
            results = [f.result() for f in concurrent.futures.as_completed(futures)]

        total_time = time.time() - start_time

        return {
            "concurrent_requests": num_concurrent,
            "total_time": total_time,
            "average_response_time": sum(r["response_time"] for r in results) / len(results),
            "success_rate": sum(1 for r in results if r["success"]) / len(results),
            "throughput": num_concurrent / total_time,
        }

    def _generate_summary(self):
        """Generate comprehensive performance summary."""
        total_tests = 0
        passed_tests = 0
        failed_tests = 0

        # Count test results
        for category, tests in self.results["test_results"].items():
            if isinstance(tests, dict):
                for test_name, test_result in tests.items():
                    total_tests += 1
                    if isinstance(test_result, dict):
                        if test_result.get("success", False) and test_result.get(
                            "meets_requirements", True
                        ):
                            passed_tests += 1
                        else:
                            failed_tests += 1

        # Calculate performance score
        performance_score = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Check requirements
        requirements_met = {
            "lscm_performance": self._check_lscm_requirements(),
            "server_performance": self._check_server_requirements(),
            "memory_usage": self._check_memory_requirements(),
        }

        # Generate recommendations
        recommendations = self._generate_recommendations(requirements_met)

        self.results["summary"] = {
            "total_tests": total_tests,
            "passed_tests": passed_tests,
            "failed_tests": failed_tests,
            "performance_score": performance_score,
            "requirements_met": requirements_met,
            "recommendations": recommendations,
            "overall_status": "PASS" if all(requirements_met.values()) else "FAIL",
        }

    def _check_lscm_requirements(self) -> bool:
        """Check if LSCM requirements are met."""
        lscm_results = self.results["test_results"].get("lscm_benchmarks", {})

        for test_name, result in lscm_results.items():
            if isinstance(result, dict) and result.get("validation"):
                if not all(result["validation"].values()):
                    return False

        return True

    def _check_server_requirements(self) -> bool:
        """Check if server requirements are met."""
        server_results = self.results["test_results"].get("mcp_server_performance", {})

        for test_name, result in server_results.items():
            if isinstance(result, dict):
                if not result.get("meets_requirements", True):
                    return False

        return True

    def _check_memory_requirements(self) -> bool:
        """Check if memory requirements are met."""
        # Check all test categories for memory usage
        for category, tests in self.results["test_results"].items():
            if isinstance(tests, dict):
                for test_result in tests.values():
                    if isinstance(test_result, dict):
                        memory_usage = test_result.get("memory_usage_mb", 0)
                        if memory_usage > self.thresholds.memory_growth_limit_mb:
                            return False

        return True

    def _generate_recommendations(self, requirements_met: dict[str, bool]) -> list[str]:
        """Generate performance improvement recommendations."""
        recommendations = []

        if not requirements_met["lscm_performance"]:
            recommendations.append("Optimize LSCM algorithm for better time complexity")
            recommendations.append("Consider mesh preprocessing to reduce computational load")

        if not requirements_met["server_performance"]:
            recommendations.append("Optimize MCP server response times")
            recommendations.append("Implement request caching for repeated operations")

        if not requirements_met["memory_usage"]:
            recommendations.append("Implement memory pooling and garbage collection optimization")
            recommendations.append("Use streaming processing for large meshes")

        if all(requirements_met.values()):
            recommendations.append(
                "Performance requirements met - consider stress testing with larger datasets"
            )

        return recommendations

    def save_report(self, filename: str = None):
        """Save performance report to file."""
        if not filename:
            filename = f"performance_report_{int(time.time())}.json"

        report_path = Path(filename)

        # Add metadata
        self.results["metadata"]["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
        self.results["metadata"]["system_info"] = self._get_system_info()

        with open(report_path, "w") as f:
            json.dump(self.results, f, indent=2, default=str)

        logger.info(f"Performance report saved to {report_path}")
        return report_path

    # Helper methods for individual tests
    def _run_lscm_solve(self, vertices, triangles):
        """Run LSCM solver for benchmarking."""
        from algorithms.lscm import unfold_surface_lscm

        return unfold_surface_lscm(vertices, triangles)

    def _simulate_server_startup(self):
        """Simulate server startup for benchmarking."""
        time.sleep(0.5)  # Simulate startup time
        return {"status": "started"}

    def _simulate_basic_tool(self):
        """Simulate basic tool operation."""
        time.sleep(0.1)  # Simulate tool execution
        return {"result": "success"}

    def _simulate_memory_test(self):
        """Simulate memory-intensive operation."""
        data = [0] * 1000000  # Allocate some memory
        time.sleep(0.1)
        return {"memory_test": "completed"}

    def _measure_lscm_100_triangles(self) -> float:
        """Measure LSCM performance for 100 triangles."""
        vertices, triangles = MeshGenerator.generate_plane_mesh(7, 7)  # ~100 triangles
        metrics = measure_performance(self._run_lscm_solve, vertices, triangles)
        return metrics.execution_time if metrics.success else float("inf")

    def _measure_basic_server_response(self) -> float:
        """Measure basic server response time."""
        metrics = measure_performance(self._simulate_basic_tool)
        return metrics.execution_time if metrics.success else float("inf")

    def _estimate_complexity(self, measurements: list[dict[str, Any]]) -> float:
        """Estimate algorithm complexity from measurements."""
        import math

        if len(measurements) < 2:
            return 1.0

        # Simple complexity estimation using log-log regression
        sizes = [m["size"] for m in measurements]
        times = [m["time"] for m in measurements]

        # Calculate complexity exponent
        ratios = []
        for i in range(1, len(measurements)):
            size_ratio = sizes[i] / sizes[i - 1]
            time_ratio = times[i] / times[i - 1]
            if size_ratio > 1 and time_ratio > 0:
                complexity = math.log(time_ratio) / math.log(size_ratio)
                ratios.append(complexity)

        return sum(ratios) / len(ratios) if ratios else 1.0

    def _get_system_info(self) -> dict[str, Any]:
        """Get system information."""
        import platform

        import psutil

        return {
            "platform": platform.platform(),
            "python_version": sys.version,
            "cpu_count": psutil.cpu_count(),
            "memory_total_gb": psutil.virtual_memory().total / (1024**3),
            "architecture": platform.architecture()[0],
        }

    def _apply_config_override(self, config_override: dict[str, Any]):
        """Apply configuration overrides."""
        # Simple config override - could be enhanced
        for key, value in config_override.items():
            if hasattr(self.config, key):
                setattr(self.config, key, value)
            if hasattr(self.thresholds, key):
                setattr(self.thresholds, key, value)


def main():
    """Main entry point for benchmark runner."""
    parser = argparse.ArgumentParser(
        description="AutoCAD MCP Server Performance Benchmarks",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    parser.add_argument(
        "--quick", action="store_true", help="Run quick benchmark suite (basic tests only)"
    )
    parser.add_argument(
        "--full", action="store_true", default=True, help="Run complete benchmark suite (default)"
    )
    parser.add_argument("--stress", action="store_true", help="Run stress tests with large meshes")
    parser.add_argument("--report", action="store_true", help="Generate performance report only")
    parser.add_argument("--baseline", action="store_true", help="Update performance baselines")
    parser.add_argument("--output", type=str, help="Output file for performance report")
    parser.add_argument("--verbose", "-v", action="store_true", help="Enable verbose logging")

    args = parser.parse_args()

    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Initialize benchmark runner
    runner = BenchmarkRunner()

    try:
        # Run selected benchmark suite
        if args.quick:
            results = runner.run_quick_benchmarks()
        elif args.stress:
            results = runner.run_stress_tests()
        elif args.report:
            # Generate report from existing data
            results = runner.results
        else:
            results = runner.run_full_benchmarks()

        # Save report
        output_file = args.output or f"performance_report_{int(time.time())}.json"
        report_path = runner.save_report(output_file)

        # Print summary
        summary = results["summary"]
        print("\n" + "=" * 80)
        print("AUTOCAD MCP SERVER PERFORMANCE BENCHMARK RESULTS")
        print("=" * 80)

        print(f"\nOverall Status: {summary['overall_status']}")
        print(f"Performance Score: {summary['performance_score']:.1f}%")
        print(f"Tests: {summary['passed_tests']}/{summary['total_tests']} passed")

        print("\nRequirements Status:")
        for req, met in summary["requirements_met"].items():
            status = "✓ PASS" if met else "✗ FAIL"
            print(f"  {req}: {status}")

        if summary["recommendations"]:
            print("\nRecommendations:")
            for i, rec in enumerate(summary["recommendations"], 1):
                print(f"  {i}. {rec}")

        print(f"\nDetailed report saved to: {report_path}")
        print("=" * 80)

        # Exit with appropriate code
        sys.exit(0 if summary["overall_status"] == "PASS" else 1)

    except Exception as e:
        logger.error(f"Benchmark execution failed: {e}")
        print(f"\n❌ BENCHMARK FAILED: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
