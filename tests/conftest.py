"""
Global test configuration and fixtures for AutoCAD MCP tests.

Provides proper AutoCAD COM interface mocking to prevent
threading issues and enable reliable testing in CI/CD environments.
"""

import pytest
import logging
import threading
from unittest.mock import MagicMock, patch
from typing import Any, Dict, List

# Configure test logging
logging.basicConfig(level=logging.WARNING)
logging.getLogger('comtypes').setLevel(logging.ERROR)
logging.getLogger('win32com').setLevel(logging.ERROR)

class MockAutoCADEntity:
    """Mock AutoCAD entity for testing."""
    
    def __init__(self, entity_type: str = "Line", object_id: int = None):
        self.entity_type = entity_type
        self.ObjectID = object_id or id(self)
        self.Handle = str(self.ObjectID)
        self.Layer = "0"
        self.Color = 256  # ByLayer
        
    def Delete(self):
        """Mock entity deletion."""
        pass
        
    def Update(self):
        """Mock entity update."""
        pass

class MockAutoCADModelSpace:
    """Mock AutoCAD ModelSpace for testing."""
    
    def __init__(self):
        self._entities = []
        self._next_id = 1000
        
    def AddLine(self, start_point: List[float], end_point: List[float]) -> MockAutoCADEntity:
        """Mock line creation."""
        entity = MockAutoCADEntity("AcDbLine", self._next_id)
        entity.StartPoint = tuple(start_point)
        entity.EndPoint = tuple(end_point)
        self._entities.append(entity)
        self._next_id += 1
        return entity
        
    def AddCircle(self, center: List[float], radius: float) -> MockAutoCADEntity:
        """Mock circle creation."""
        entity = MockAutoCADEntity("AcDbCircle", self._next_id)
        entity.Center = tuple(center)
        entity.Radius = radius
        self._entities.append(entity)
        self._next_id += 1
        return entity
        
    def AddPolyFaceMesh(self, vertices: Any, faces: Any) -> MockAutoCADEntity:
        """Mock polyface mesh creation."""
        entity = MockAutoCADEntity("AcDbPolyFaceMesh", self._next_id)
        entity.Coordinates = vertices
        self._entities.append(entity)
        self._next_id += 1
        return entity

class MockAutoCADDocument:
    """Mock AutoCAD Document for testing."""
    
    def __init__(self):
        self.ModelSpace = MockAutoCADModelSpace()
        self.Name = "Test Document"
        self.Path = ""
        
    def Save(self):
        """Mock document save."""
        pass
        
    def SaveAs(self, filename: str):
        """Mock document save as."""
        self.Path = filename

class MockAutoCADApplication:
    """Mock AutoCAD Application for testing."""
    
    def __init__(self):
        self.Version = "25.0"  # AutoCAD 2025
        self.ActiveDocument = MockAutoCADDocument()
        self.Documents = [self.ActiveDocument]
        self.Visible = True
        
    def GetInterfaceObject(self, prog_id: str):
        """Mock interface object creation."""
        return MagicMock()

@pytest.fixture(scope="session", autouse=True)
def mock_autocad_com():
    """Global AutoCAD COM mocking for all tests."""
    
    mock_app = MockAutoCADApplication()
    
    # Patch win32com.client.Dispatch calls
    with patch('win32com.client.Dispatch') as mock_dispatch:
        mock_dispatch.return_value = mock_app
        
        # Patch comtypes calls
        with patch('comtypes.client.CreateObject') as mock_create:
            mock_create.return_value = mock_app
            
            yield mock_app

@pytest.fixture
def mock_autocad_wrapper():
    """Fixture for mocked AutoCAD wrapper."""
    from src.enhanced_autocad.enhanced_wrapper import EnhancedAutoCAD
    
    with patch.object(EnhancedAutoCAD, '_connect_to_autocad') as mock_connect:
        wrapper = EnhancedAutoCAD()
        wrapper._acad_app = MockAutoCADApplication()
        wrapper._is_connected = True
        mock_connect.return_value = True
        yield wrapper

@pytest.fixture
def disable_threading_issues():
    """Prevent COM threading issues during testing."""
    # Override thread detection to always return MainThread for COM operations
    original_current_thread = threading.current_thread
    
    def mock_current_thread():
        thread = original_current_thread()
        thread.name = "MainThread"  # Always claim to be main thread for COM
        return thread
    
    with patch('threading.current_thread', side_effect=mock_current_thread):
        yield

@pytest.fixture(autouse=True)
def suppress_com_errors():
    """Suppress COM-related error logging during tests."""
    com_loggers = [
        'comtypes.client',
        'win32com.client',
        'src.enhanced_autocad.error_handler',
        'src.mcp_integration.enhanced_mcp_server'
    ]
    
    original_levels = {}
    for logger_name in com_loggers:
        logger = logging.getLogger(logger_name)
        original_levels[logger_name] = logger.level
        logger.setLevel(logging.ERROR)
    
    yield
    
    # Restore original levels
    for logger_name, level in original_levels.items():
        logging.getLogger(logger_name).setLevel(level)

# Test data fixtures
@pytest.fixture
def sample_mesh_data():
    """Sample mesh data for testing."""
    import numpy as np
    
    # Simple triangle mesh
    vertices = np.array([
        [0.0, 0.0, 0.0],
        [1.0, 0.0, 0.0],
        [0.5, 1.0, 0.0]
    ])
    
    triangles = np.array([
        [0, 1, 2]
    ])
    
    return vertices, triangles

@pytest.fixture
def sample_lscm_result():
    """Sample LSCM result data for testing."""
    import numpy as np
    
    uv_coords = np.array([
        [0.0, 0.0],
        [1.0, 0.0],
        [0.5, 0.866]  # Approximate equilateral triangle in UV space
    ])
    
    return uv_coords