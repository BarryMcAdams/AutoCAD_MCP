"""
Testing Framework for AutoCAD Automation.

This module provides comprehensive testing capabilities for AutoCAD automation code,
including mock AutoCAD support, automatic test generation, and performance testing.
"""

from .autocad_test_framework import AutoCADTestFramework
from .ci_integration import CIIntegration
from .mock_autocad import MockAutoCAD
from .performance_tester import PerformanceTester
from .test_generators import TestGenerator

__all__ = [
    "AutoCADTestFramework",
    "MockAutoCAD",
    "TestGenerator",
    "PerformanceTester",
    "CIIntegration",
]
