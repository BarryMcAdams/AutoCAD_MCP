"""
Regression test package for AutoCAD MCP Server.

This package contains regression tests to ensure existing functionality
continues to work correctly after new feature integration, particularly
the advanced LSCM algorithm integration.

Test Categories:
- Basic tool functionality regression
- Performance baseline validation 
- Memory usage stability
- Backward compatibility
- Concurrent execution scenarios
- Error handling consistency

Usage:
    pytest tests/regression/ -v
    
    # Run specific test class
    pytest tests/regression/test_basic_tools_regression.py::TestBasicToolsRegression -v
    
    # Run performance regression only
    pytest tests/regression/ -k "performance" -v
    
    # Run with coverage
    pytest tests/regression/ --cov=src --cov-report=html
"""

__version__ = "1.0.0"
__author__ = "AutoCAD MCP Development Team"

# Test configuration
REGRESSION_TEST_CONFIG = {
    "performance_thresholds": {
        "basic_tool_max_time": 0.1,  # seconds
        "server_status_max_time": 0.05,  # seconds
        "memory_increase_limit": 20,  # MB
        "total_memory_limit": 50,  # MB
    },
    "stability_requirements": {
        "min_iterations": 10,
        "concurrent_threads": 4,
        "error_isolation": True,
    },
    "compatibility_checks": {
        "response_format_validation": True,
        "field_type_validation": True,
        "error_structure_validation": True,
    }
}

# Test utilities
def get_performance_threshold(test_type: str) -> float:
    """Get performance threshold for specific test type."""
    return REGRESSION_TEST_CONFIG["performance_thresholds"].get(f"{test_type}_max_time", 1.0)

def get_memory_limit(limit_type: str) -> float:
    """Get memory limit for specific test type."""
    if limit_type == "increase":
        return REGRESSION_TEST_CONFIG["performance_thresholds"]["memory_increase_limit"]
    elif limit_type == "total":
        return REGRESSION_TEST_CONFIG["performance_thresholds"]["total_memory_limit"]
    return 100.0  # Default limit