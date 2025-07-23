"""
Utility functions for AutoCAD MCP Server.
"""

import math
import logging
from typing import List, Tuple, Dict, Any, Optional
import pythoncom
import win32com.client

from pyautocad import Autocad

logger = logging.getLogger(__name__)

# Type alias for 3D points
Point3D = List[float]


def validate_point3d(point: Any) -> Point3D:
    """
    Validate and normalize 3D point coordinates.
    
    Args:
        point: Input point data (should be [x, y, z])
        
    Returns:
        List[float]: Validated 3D point coordinates
        
    Raises:
        ValueError: If point format is invalid
    """
    if not isinstance(point, (list, tuple)):
        raise ValueError("Point must be a list or tuple")
        
    if len(point) != 3:
        raise ValueError("Point must have exactly 3 coordinates [x, y, z]")
        
    try:
        return [float(coord) for coord in point]
    except (TypeError, ValueError) as e:
        raise ValueError(f"Point coordinates must be numeric: {e}")


def validate_entity_id(entity_id: Any) -> int:
    """
    Validate entity ID is positive integer.
    
    Args:
        entity_id: Input entity ID
        
    Returns:
        int: Validated entity ID
        
    Raises:
        ValueError: If entity ID is invalid
    """
    try:
        eid = int(entity_id)
        if eid <= 0:
            raise ValueError("Entity ID must be positive")
        return eid
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid entity ID: {e}")


def validate_tolerance(tolerance: Any) -> float:
    """
    Validate tolerance is within acceptable range.
    
    Args:
        tolerance: Input tolerance value
        
    Returns:
        float: Validated tolerance
        
    Raises:
        ValueError: If tolerance is invalid
    """
    try:
        tol = float(tolerance)
        if not (0.001 <= tol <= 1.0):
            raise ValueError("Tolerance must be between 0.001 and 1.0")
        return tol
    except (TypeError, ValueError) as e:
        raise ValueError(f"Invalid tolerance: {e}")


def validate_layer_name(layer: Any) -> str:
    """
    Validate AutoCAD layer name.
    
    Args:
        layer: Input layer name
        
    Returns:
        str: Validated layer name
        
    Raises:
        ValueError: If layer name is invalid
    """
    if not isinstance(layer, str):
        raise ValueError("Layer name must be a string")
        
    if not layer.strip():
        raise ValueError("Layer name cannot be empty")
        
    # Check for invalid characters in AutoCAD layer names
    invalid_chars = ['<', '>', '/', '\\', '"', ':', ';', '?', '*', '|', '=', '`']
    for char in invalid_chars:
        if char in layer:
            raise ValueError(f"Layer name contains invalid character: {char}")
            
    return layer.strip()


def distance_3d(point1: Point3D, point2: Point3D) -> float:
    """
    Calculate 3D distance between two points.
    
    Args:
        point1: First point [x, y, z]
        point2: Second point [x, y, z]
        
    Returns:
        float: Distance between points
    """
    dx = point2[0] - point1[0]
    dy = point2[1] - point1[1]
    dz = point2[2] - point1[2]
    return math.sqrt(dx*dx + dy*dy + dz*dz)


def midpoint_3d(point1: Point3D, point2: Point3D) -> Point3D:
    """
    Calculate midpoint between two 3D points.
    
    Args:
        point1: First point [x, y, z]
        point2: Second point [x, y, z]
        
    Returns:
        Point3D: Midpoint coordinates
    """
    return [
        (point1[0] + point2[0]) / 2,
        (point1[1] + point2[1]) / 2,
        (point1[2] + point2[2]) / 2
    ]


def normalize_vector(vector: Point3D) -> Point3D:
    """
    Normalize a 3D vector to unit length.
    
    Args:
        vector: Vector [x, y, z]
        
    Returns:
        Point3D: Normalized vector
        
    Raises:
        ValueError: If vector has zero length
    """
    length = math.sqrt(vector[0]**2 + vector[1]**2 + vector[2]**2)
    if length == 0:
        raise ValueError("Cannot normalize zero-length vector")
        
    return [vector[0]/length, vector[1]/length, vector[2]/length]


def cross_product(vector1: Point3D, vector2: Point3D) -> Point3D:
    """
    Calculate cross product of two 3D vectors.
    
    Args:
        vector1: First vector [x, y, z]
        vector2: Second vector [x, y, z]
        
    Returns:
        Point3D: Cross product vector
    """
    return [
        vector1[1] * vector2[2] - vector1[2] * vector2[1],
        vector1[2] * vector2[0] - vector1[0] * vector2[2],
        vector1[0] * vector2[1] - vector1[1] * vector2[0]
    ]


def degrees_to_radians(degrees: float) -> float:
    """Convert degrees to radians."""
    return degrees * math.pi / 180.0


def radians_to_degrees(radians: float) -> float:
    """Convert radians to degrees."""
    return radians * 180.0 / math.pi


def get_autocad_instance() -> Autocad:
    """
    Get AutoCAD instance with proper error handling.
    
    Returns:
        Autocad: Connected AutoCAD instance
        
    Raises:
        ConnectionError: If AutoCAD is not running or accessible
    """
    try:
        pythoncom.CoInitialize()
        
        # Try to connect to AutoCAD 2025 specifically
        try:
            # First try to get active AutoCAD 2025 instance
            app = win32com.client.GetActiveObject("AutoCAD.Application.25")
            # Create a custom wrapper that mimics pyautocad.Autocad
            class AutocadWrapper:
                def __init__(self, app):
                    self.app = app
                    self.doc = app.ActiveDocument
                    
                    # Create a model wrapper that handles COM calls properly
                    class ModelWrapper:
                        def __init__(self, modelspace):
                            self.modelspace = modelspace
                            
                        def AddLine(self, start_point, end_point):
                            # Convert Python lists to VBA arrays for COM
                            import win32com.client
                            return self.modelspace.AddLine(
                                win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, start_point),
                                win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, end_point)
                            )
                            
                        def AddCircle(self, center_point, radius):
                            import win32com.client
                            return self.modelspace.AddCircle(
                                win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, center_point),
                                radius
                            )
                    
                    self.model = ModelWrapper(app.ActiveDocument.ModelSpace)
                
                @property
                def Visible(self):
                    return self.app.Visible
                
                @Visible.setter
                def Visible(self, value):
                    self.app.Visible = value
            
            acad = AutocadWrapper(app)
            logger.info("Connected to AutoCAD.Application.25")
        except Exception as e1:
            logger.info(f"AutoCAD.Application.25 not found: {e1}")
            try:
                # Try generic AutoCAD application
                app = win32com.client.GetActiveObject("AutoCAD.Application")
                class AutocadWrapper:
                    def __init__(self, app):
                        self.app = app
                        self.doc = app.ActiveDocument
                        
                        # Create a model wrapper that handles COM calls properly
                        class ModelWrapper:
                            def __init__(self, modelspace):
                                self.modelspace = modelspace
                                
                            def AddLine(self, start_point, end_point):
                                # Convert Python lists to VBA arrays for COM
                                import win32com.client
                                return self.modelspace.AddLine(
                                    win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, start_point),
                                    win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, end_point)
                                )
                                
                            def AddCircle(self, center_point, radius):
                                import win32com.client
                                return self.modelspace.AddCircle(
                                    win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, center_point),
                                    radius
                                )
                        
                        self.model = ModelWrapper(app.ActiveDocument.ModelSpace)
                    
                    @property
                    def Visible(self):
                        return self.app.Visible
                    
                    @Visible.setter
                    def Visible(self, value):
                        self.app.Visible = value
                
                acad = AutocadWrapper(app)
                logger.info("Connected to AutoCAD.Application")
            except Exception as e2:
                logger.info(f"AutoCAD.Application not found: {e2}")
                # Last resort - let pyautocad handle it
                acad = Autocad(create_if_not_exists=True)
        
        if acad is None or acad.app is None:
            raise ConnectionError("AutoCAD is not running")
            
        # Test connection
        _ = acad.doc.Name
        
        # Ensure AutoCAD is visible
        if not acad.app.Visible:
            acad.app.Visible = True
            logger.info("Made AutoCAD visible")
            
        return acad
        
    except Exception as e:
        logger.error(f"Failed to connect to AutoCAD: {e}")
        raise ConnectionError(f"Cannot connect to AutoCAD: {e}")


def extract_entity_properties(entity) -> Dict[str, Any]:
    """
    Extract properties from an AutoCAD entity.
    
    Args:
        entity: AutoCAD entity object
        
    Returns:
        Dict[str, Any]: Entity properties
    """
    properties = {
        'id': entity.ObjectID,
        'type': entity.ObjectName,
        'layer': entity.Layer,
        'color': entity.Color,
    }
    
    try:
        # Add type-specific properties
        if hasattr(entity, 'Length'):
            properties['length'] = entity.Length
            
        if hasattr(entity, 'Radius'):
            properties['radius'] = entity.Radius
            
        if hasattr(entity, 'Area'):
            properties['area'] = entity.Area
            
        if hasattr(entity, 'Volume'):
            properties['volume'] = entity.Volume
            
        # Add bounding box if available
        if hasattr(entity, 'GetBoundingBox'):
            min_point, max_point = entity.GetBoundingBox()
            properties['bounding_box'] = {
                'min_point': list(min_point),
                'max_point': list(max_point)
            }
            
        # Add center of mass for solids
        if hasattr(entity, 'MassProp'):
            mass_props = entity.MassProp
            if len(mass_props) >= 3:
                properties['center_of_mass'] = list(mass_props[:3])
                
    except Exception as e:
        logger.warning(f"Could not extract some properties from entity {entity.ObjectID}: {e}")
        
    return properties


def create_error_response(
    error_message: str,
    error_code: str,
    details: Optional[Dict[str, Any]] = None,
    status_code: int = 500
) -> Tuple[Dict[str, Any], int]:
    """
    Create standardized error response.
    
    Args:
        error_message: Human-readable error message
        error_code: Machine-readable error code
        details: Additional error details
        status_code: HTTP status code
        
    Returns:
        Tuple[Dict, int]: Error response and status code
    """
    response = {
        'success': False,
        'error': error_message,
        'error_code': error_code,
        'details': details or {}
    }
    
    return response, status_code


def create_success_response(
    data: Dict[str, Any],
    execution_time: Optional[float] = None
) -> Dict[str, Any]:
    """
    Create standardized success response.
    
    Args:
        data: Response data
        execution_time: Operation execution time
        
    Returns:
        Dict[str, Any]: Success response
    """
    response = {
        'success': True,
        **data
    }
    
    if execution_time is not None:
        response['execution_time'] = execution_time
        
    return response