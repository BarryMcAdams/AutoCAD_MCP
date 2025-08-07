"""
Performance testing configuration and thresholds.

This module defines the performance requirements, test parameters, and 
validation thresholds for the AutoCAD MCP server performance benchmarks.
"""

from dataclasses import dataclass
from typing import Dict, Any


@dataclass
class PerformanceThresholds:
    """Performance requirement thresholds for validation."""
    
    # LSCM Algorithm Requirements
    lscm_small_mesh_time_limit: float = 2.0    # <100 triangles in <2s
    lscm_medium_mesh_time_limit: float = 10.0  # 500 triangles in <10s
    lscm_memory_limit_mb: float = 100.0        # <100MB additional memory
    
    # MCP Server Requirements
    basic_tool_response_limit: float = 1.0     # Basic tools in <1s
    advanced_tool_response_limit: float = 5.0  # Advanced tools in <5s
    server_startup_limit: float = 5.0          # Startup in <5s
    server_shutdown_limit: float = 2.0         # Shutdown in <2s
    
    # Concurrency and Load Requirements
    concurrent_efficiency_min: float = 2.0     # Minimum speedup from parallelism
    memory_growth_limit_mb: float = 200.0      # Max memory growth under load
    memory_leak_threshold_mb: float = 1.0      # Memory growth per iteration
    
    # Algorithm Complexity Requirements
    max_complexity_exponent: float = 2.5       # Max O(n^x) where x < 2.5
    min_complexity_exponent: float = 1.0       # Min O(n^x) where x > 1.0
    memory_per_triangle_limit: float = 1.0     # Max MB per triangle


@dataclass
class TestConfiguration:
    """Configuration parameters for performance tests."""
    
    # Mesh Test Cases
    small_mesh_triangles: int = 50
    medium_mesh_triangles: int = 100
    large_mesh_triangles: int = 500
    stress_test_triangles: int = 1000
    
    # Concurrency Testing
    max_concurrent_requests: int = 8
    load_test_iterations: int = 100
    memory_sample_interval: int = 20
    
    # Timeout Settings
    test_timeout_seconds: float = 30.0
    stress_test_timeout_seconds: float = 60.0
    concurrent_request_timeout: float = 30.0
    
    # Performance Monitoring
    monitoring_sample_interval: float = 0.1    # 100ms sampling
    performance_report_path: str = "performance_report.json"
    baseline_metrics_path: str = "performance_baselines.json"
    
    # Regression Detection
    regression_threshold: float = 1.5          # 50% performance degradation
    baseline_update_threshold: float = 0.9     # Update baseline if 10% faster


# Default configuration instances
DEFAULT_THRESHOLDS = PerformanceThresholds()
DEFAULT_CONFIG = TestConfiguration()


# Test case definitions for different mesh sizes
LSCM_TEST_CASES = [
    {
        "name": "tiny_mesh",
        "description": "Minimal mesh for basic functionality",
        "triangle_count": 10,
        "expected_max_time": 0.1,
        "expected_max_memory": 10
    },
    {
        "name": "small_mesh", 
        "description": "Small mesh within <2s requirement",
        "triangle_count": 50,
        "expected_max_time": 0.5,
        "expected_max_memory": 20
    },
    {
        "name": "medium_mesh",
        "description": "Medium mesh at 100 triangle boundary",
        "triangle_count": 100,
        "expected_max_time": 2.0,
        "expected_max_memory": 50
    },
    {
        "name": "large_mesh",
        "description": "Large mesh within <10s requirement",
        "triangle_count": 500,
        "expected_max_time": 10.0,
        "expected_max_memory": 100
    },
    {
        "name": "stress_mesh",
        "description": "Stress test mesh for scalability validation",
        "triangle_count": 1000,
        "expected_max_time": 20.0,
        "expected_max_memory": 200
    }
]


# MCP Server test configurations
MCP_SERVER_TESTS = {
    "basic_tools": {
        "tools": ["draw_line", "draw_circle", "draw_rectangle"],
        "max_response_time": DEFAULT_THRESHOLDS.basic_tool_response_limit,
        "description": "Basic geometric drawing operations"
    },
    "advanced_tools": {
        "tools": ["surface_unfold", "parametric_design", "pattern_optimization"],
        "max_response_time": DEFAULT_THRESHOLDS.advanced_tool_response_limit,
        "description": "Advanced algorithmic operations"
    },
    "concurrent_load": {
        "concurrent_requests": DEFAULT_CONFIG.max_concurrent_requests,
        "test_duration": 30.0,
        "description": "Concurrent request handling capacity"
    }
}


# Complexity analysis configurations
COMPLEXITY_ANALYSIS = {
    "test_sizes": [20, 40, 80, 160, 320, 640],
    "min_successful_measurements": 3,
    "complexity_methods": ["lscm_solve", "mesh_generation", "distortion_analysis"],
    "scaling_factors": [2, 4, 8, 16, 32]
}


# Performance monitoring settings
MONITORING_CONFIG = {
    "metrics": {
        "execution_time": {"unit": "seconds", "precision": 3},
        "memory_usage": {"unit": "MB", "precision": 1},
        "cpu_usage": {"unit": "percent", "precision": 1},
        "throughput": {"unit": "operations/second", "precision": 2}
    },
    "alerts": {
        "memory_spike": 500.0,      # Alert if memory exceeds 500MB
        "execution_timeout": 60.0,  # Alert if any test exceeds 60s
        "failure_rate": 0.1         # Alert if >10% of tests fail
    }
}


def get_mesh_test_case(name: str) -> Dict[str, Any]:
    """Get test case configuration by name."""
    for case in LSCM_TEST_CASES:
        if case["name"] == name:
            return case.copy()
    raise ValueError(f"Test case '{name}' not found")


def validate_performance_requirements(
    operation: str,
    triangle_count: int,
    execution_time: float,
    memory_usage_mb: float
) -> Dict[str, bool]:
    """
    Validate performance metrics against requirements.
    
    Args:
        operation: Name of the operation being tested
        triangle_count: Number of triangles in test mesh
        execution_time: Measured execution time in seconds
        memory_usage_mb: Measured memory usage in MB
        
    Returns:
        Dictionary with validation results for each requirement
    """
    results = {}
    
    if operation == "lscm":
        # LSCM-specific requirements
        if triangle_count < 100:
            results["execution_time"] = execution_time < DEFAULT_THRESHOLDS.lscm_small_mesh_time_limit
        elif triangle_count <= 500:
            results["execution_time"] = execution_time < DEFAULT_THRESHOLDS.lscm_medium_mesh_time_limit
        else:
            results["execution_time"] = execution_time < 30.0  # Generous limit for larger meshes
            
        results["memory_usage"] = memory_usage_mb < DEFAULT_THRESHOLDS.lscm_memory_limit_mb
        
    elif operation.startswith("mcp_"):
        # MCP server requirements
        if "basic" in operation:
            results["execution_time"] = execution_time < DEFAULT_THRESHOLDS.basic_tool_response_limit
        else:
            results["execution_time"] = execution_time < DEFAULT_THRESHOLDS.advanced_tool_response_limit
            
        results["memory_usage"] = memory_usage_mb < DEFAULT_THRESHOLDS.memory_growth_limit_mb
    
    return results


def generate_performance_report_template() -> Dict[str, Any]:
    """Generate template structure for performance reports."""
    return {
        "metadata": {
            "timestamp": None,
            "test_version": "1.0.0",
            "system_info": {},
            "configuration": {
                "thresholds": DEFAULT_THRESHOLDS.__dict__,
                "test_config": DEFAULT_CONFIG.__dict__
            }
        },
        "test_results": {
            "lscm_benchmarks": {},
            "mcp_server_performance": {},
            "complexity_analysis": {},
            "regression_tests": {}
        },
        "summary": {
            "total_tests": 0,
            "passed_tests": 0,
            "failed_tests": 0,
            "performance_score": 0.0,
            "requirements_met": {},
            "recommendations": []
        },
        "detailed_metrics": {},
        "alerts": [],
        "trends": {}
    }


if __name__ == "__main__":
    # Print configuration summary
    print("AutoCAD MCP Performance Test Configuration")
    print("=" * 50)
    
    print(f"\nLSCM Algorithm Thresholds:")
    print(f"  Small mesh (<100 triangles): <{DEFAULT_THRESHOLDS.lscm_small_mesh_time_limit}s")
    print(f"  Medium mesh (500 triangles): <{DEFAULT_THRESHOLDS.lscm_medium_mesh_time_limit}s")
    print(f"  Memory usage limit: <{DEFAULT_THRESHOLDS.lscm_memory_limit_mb}MB")
    
    print(f"\nMCP Server Thresholds:")
    print(f"  Basic tool response: <{DEFAULT_THRESHOLDS.basic_tool_response_limit}s")
    print(f"  Advanced tool response: <{DEFAULT_THRESHOLDS.advanced_tool_response_limit}s")
    print(f"  Server startup: <{DEFAULT_THRESHOLDS.server_startup_limit}s")
    
    print(f"\nTest Configuration:")
    print(f"  Max concurrent requests: {DEFAULT_CONFIG.max_concurrent_requests}")
    print(f"  Load test iterations: {DEFAULT_CONFIG.load_test_iterations}")
    print(f"  Test timeout: {DEFAULT_CONFIG.test_timeout_seconds}s")
    
    print(f"\nTest Cases Defined:")
    for case in LSCM_TEST_CASES:
        print(f"  {case['name']}: {case['triangle_count']} triangles, "
              f"<{case['expected_max_time']}s, <{case['expected_max_memory']}MB")