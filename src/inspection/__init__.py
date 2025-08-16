"""
AutoCAD Object Inspection Module
===============================

Comprehensive AutoCAD object inspection system for Master AutoCAD Coder.
Provides multi-level object inspection, property analysis, method discovery,
and VS Code IntelliSense integration for enhanced development experience.

Week 4 Implementation - Phase 2: Interactive Development Tools
"""

from .intellisense_provider import IntelliSenseProvider
from .method_discoverer import MethodDiscoverer
from .object_inspector import ObjectInspector
from .property_analyzer import PropertyAnalyzer

__all__ = ["ObjectInspector", "PropertyAnalyzer", "MethodDiscoverer", "IntelliSenseProvider"]

# Version information
__version__ = "1.0.0"
__author__ = "AutoCAD MCP Contributors"
