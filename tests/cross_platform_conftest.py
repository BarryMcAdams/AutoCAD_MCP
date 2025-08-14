"""
Cross-platform test configuration for AutoCAD MCP.

This module ensures all tests can run on any platform by providing
comprehensive mocks for Windows-only dependencies.
"""

import sys
import pytest
import logging
from unittest.mock import MagicMock, patch, Mock
from typing import Any, Dict, List

# Suppress excessive logging during tests
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('win32com').setLevel(logging.ERROR)

def setup_cross_platform_environment():
    """Setup cross-platform environment for testing."""
    
    # Mock Windows COM modules if not available
    if 'win32com' not in sys.modules:
        win32com = MagicMock()
        win32com.client = MagicMock()
        win32com.client.Dispatch = MagicMock()
        sys.modules['win32com'] = win32com
        sys.modules['win32com.client'] = win32com.client
        
    if 'pythoncom' not in sys.modules:
        pythoncom = MagicMock()
        sys.modules['pythoncom'] = pythoncom
        
    if 'comtypes' not in sys.modules:
        comtypes = MagicMock()
        comtypes.client = MagicMock()
        comtypes.client.CreateObject = MagicMock()
        sys.modules['comtypes'] = comtypes
        sys.modules['comtypes.client'] = comtypes.client
        
    # Mock pyautocad if not available
    if 'pyautocad' not in sys.modules:
        pyautocad = MagicMock()
        sys.modules['pyautocad'] = pyautocad

# Auto-setup when module is imported
setup_cross_platform_environment()

@pytest.fixture(scope="session", autouse=True)
def cross_platform_setup():
    """Automatically setup cross-platform environment for all tests."""
    setup_cross_platform_environment()
    yield
    
@pytest.fixture
def mock_autocad_application():
    """Provide a mock AutoCAD application for testing."""
    from src.testing.mock_autocad import MockAutoCAD
    return MockAutoCAD()

@pytest.fixture  
def skip_windows_only():
    """Skip tests that require Windows-only functionality."""
    if sys.platform != 'win32':
        pytest.skip("Test requires Windows platform")

@pytest.fixture
def mock_windows_environment():
    """Mock Windows environment for cross-platform testing."""
    with patch('sys.platform', 'win32'):
        yield

# Marker for platform-specific tests
def pytest_configure(config):
    """Configure custom pytest markers."""
    config.addinivalue_line(
        "markers", "windows_only: mark test as requiring Windows platform"
    )
    config.addinivalue_line(
        "markers", "cross_platform: mark test as cross-platform compatible"
    )

def pytest_collection_modifyitems(config, items):
    """Modify test collection to handle platform-specific tests."""
    for item in items:
        # Skip Windows-only tests on non-Windows platforms
        if item.get_closest_marker("windows_only") and sys.platform != 'win32':
            item.add_marker(pytest.mark.skip(reason="Windows-only test"))