
"""
AutoCAD MCP Server - Phase 1 Implementation
A Model Context Protocol server for AutoCAD 2025 automation.
"""

import logging
import math
import os
from datetime import datetime

from flask import Flask, jsonify, request
from pyautocad import Autocad

try:
    # Try relative imports first (for package usage)
    from .config import config
    from .decorators import handle_autocad_errors, log_api_call, require_autocad_connection
    from .utils import get_autocad_instance, create_success_response, create_error_response
    from .dimensioning import DimensioningSystem, create_manufacturing_drawing
    from .pattern_optimization import (PatternNestingOptimizer, Pattern, MaterialSheet, 
                                     create_patterns_from_unfolding_results, optimize_material_usage)
except ImportError:
    # Fall back to absolute imports (for standalone usage)
    from config import config
    from decorators import handle_autocad_errors, log_api_call, require_autocad_connection
    from utils import get_autocad_instance, create_success_response, create_error_response
    from dimensioning import DimensioningSystem, create_manufacturing_drawing
    from pattern_optimization import (PatternNestingOptimizer, Pattern, MaterialSheet,
                                    create_patterns_from_unfolding_results, optimize_material_usage)

# Initialize Flask application
app = Flask(__name__)
app.config['DEBUG'] = config.DEBUG

# Set up logging
def setup_logging():
    """Configure logging for the application."""
    # Create logs directory if it doesn't exist
    log_dir = os.path.dirname(config.LOG_FILE)
    if log_dir and not os.path.exists(log_dir):
        os.makedirs(log_dir)
    
    # Configure logging
    logging.basicConfig(
        level=getattr(logging, config.LOG_LEVEL.upper()),
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.FileHandler(config.LOG_FILE),
            logging.StreamHandler()
        ]
    )
    
    # Set werkzeug logger to WARNING to reduce noise
    logging.getLogger('werkzeug').setLevel(logging.WARNING)

# Initialize logging
setup_logging()
logger = logging.getLogger(__name__)

logger.info("Starting AutoCAD MCP Server")
logger.info(f"Configuration: Host={config.HOST}, Port={config.PORT}, Debug={config.DEBUG}")

# Health and Status Endpoints

@app.route('/health', methods=['GET'])
@log_api_call
def health():
    """Get server health status."""
    return jsonify(create_success_response({
        'status': 'ok',
        'timestamp': datetime.utcnow().isoformat(),
        'version': '1.0.0'
    }))

@app.route('/acad-status', methods=['GET'])
@log_api_call  
@handle_autocad_errors
def acad_status():
    """Get AutoCAD connection status and information."""
    try:
        acad = get_autocad_instance()
        return jsonify(create_success_response({
            'status': 'connected',
            'version': acad.app.Version,
            'document': acad.doc.Name,
            'visible': acad.Visible
        }))
    except ConnectionError:
        response, status_code = create_error_response(
            'AutoCAD is not connected',
            'AUTOCAD_NOT_CONNECTED',
            {'suggestion': 'Start AutoCAD 2025 and ensure it is visible'},
            503
        )
        return jsonify(response), status_code

# Basic Drawing Operations

@app.route('/draw/line', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_line():
    """Create a line in AutoCAD from start point to end point."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_point3d, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'start_point' not in data or 'end_point' not in data:
        return jsonify(create_error_response(
            'Missing required fields: start_point and/or end_point',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['start_point', 'end_point']}
        )), 400
    
    try:
        # Validate input parameters
        start_point = validate_point3d(data['start_point'])
        end_point = validate_point3d(data['end_point'])
        layer = validate_layer_name(data.get('layer', '0'))
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create line in AutoCAD
        line = acad.model.AddLine(start_point, end_point)
        # Skip layer assignment due to COM compatibility issues
        # line.Layer = layer
        
        # Extract entity properties
        properties = extract_entity_properties(line)
        
        logger.info(f"Created line {line.ObjectID} on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': line.ObjectID,
            'entity_type': line.ObjectName,
            'layer': layer,
            'length': properties.get('length'),
            'start_point': start_point,
            'end_point': end_point
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that points are [x, y, z] format and layer name is valid'}
        )), 400

@app.route('/draw/circle', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_circle():
    """Create a circle in AutoCAD with specified center and radius."""
    from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE'
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'center_point' not in data or 'radius' not in data:
        return jsonify(create_error_response(
            'Missing required fields: center_point and/or radius',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['center_point', 'radius']}
        )), 400
    
    try:
        # Validate input parameters
        center_point = validate_point3d(data['center_point'])
        radius = float(data['radius'])
        if radius <= 0:
            raise ValueError("Radius must be positive")
        layer = validate_layer_name(data.get('layer', '0'))
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create circle in AutoCAD
        circle = acad.model.AddCircle(center_point, radius)
        # Skip layer assignment due to COM compatibility issues
        # circle.Layer = layer
        
        # Extract entity properties
        properties = extract_entity_properties(circle)
        
        logger.info(f"Created circle {circle.ObjectID} with radius {radius} on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': circle.ObjectID,
            'entity_type': circle.ObjectName,
            'layer': layer,
            'center_point': center_point,
            'radius': radius,
            'area': properties.get('area'),
            'circumference': 2 * 3.14159 * radius
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that center_point is [x, y, z] format and radius is positive'}
        )), 400

@app.route('/draw/polyline', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_polyline():
    """Create a polyline in AutoCAD from multiple points."""
    from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    import array
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE'
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'points' not in data:
        return jsonify(create_error_response(
            'Missing required field: points',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['points']}
        )), 400
    
    try:
        # Validate input parameters
        points_list = data['points']
        if not isinstance(points_list, list) or len(points_list) < 2:
            raise ValueError("Points must be a list with at least 2 points")
        
        # Validate each point
        validated_points = []
        for i, point in enumerate(points_list):
            try:
                validated_points.append(validate_point3d(point))
            except ValueError as e:
                raise ValueError(f"Invalid point at index {i}: {e}")
        
        closed = data.get('closed', False)
        layer = validate_layer_name(data.get('layer', '0'))
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Convert points to flat array format for AutoCAD
        # AutoCAD expects flat array: [x1, y1, x2, y2, x3, y3, ...]
        flat_points = []
        for point in validated_points:
            flat_points.extend(point[:2])  # Only use X, Y for polyline
        
        point_array = array.array('d', flat_points)
        
        # Create polyline in AutoCAD
        polyline = acad.model.AddLightWeightPolyline(point_array)
        polyline.Layer = layer
        polyline.Closed = closed
        
        # Extract entity properties
        properties = extract_entity_properties(polyline)
        
        logger.info(f"Created polyline {polyline.ObjectID} with {len(validated_points)} points on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': polyline.ObjectID,
            'entity_type': polyline.ObjectName,
            'layer': layer,
            'points': validated_points,
            'point_count': len(validated_points),
            'closed': closed,
            'length': properties.get('length'),
            'area': properties.get('area') if closed else None
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that points is a list of [x, y, z] coordinates with at least 2 points'}
        )), 400

@app.route('/draw/rectangle', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_rectangle():
    """Create a rectangle in AutoCAD from two corner points."""
    from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    import array
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE'
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'corner1' not in data or 'corner2' not in data:
        return jsonify(create_error_response(
            'Missing required fields: corner1 and/or corner2',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['corner1', 'corner2']}
        )), 400
    
    try:
        # Validate input parameters
        corner1 = validate_point3d(data['corner1'])
        corner2 = validate_point3d(data['corner2'])
        layer = validate_layer_name(data.get('layer', '0'))
        
        # Calculate rectangle corners
        x1, y1, z1 = corner1
        x2, y2, z2 = corner2
        
        # Create rectangle points (assuming Z is the same for all corners)
        z = z1  # Use Z from first corner
        rect_points = [
            [x1, y1, z],  # Corner 1
            [x2, y1, z],  # Corner 2
            [x2, y2, z],  # Corner 3
            [x1, y2, z]   # Corner 4
        ]
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Convert to flat array for AutoCAD
        flat_points = []
        for point in rect_points:
            flat_points.extend(point[:2])  # Only X, Y
        
        point_array = array.array('d', flat_points)
        
        # Create closed polyline (rectangle)
        rectangle = acad.model.AddLightWeightPolyline(point_array)
        rectangle.Layer = layer
        rectangle.Closed = True
        
        # Extract entity properties
        properties = extract_entity_properties(rectangle)
        
        # Calculate dimensions
        width = abs(x2 - x1)
        height = abs(y2 - y1)
        
        logger.info(f"Created rectangle {rectangle.ObjectID} ({width}x{height}) on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': rectangle.ObjectID,
            'entity_type': rectangle.ObjectName,
            'layer': layer,
            'corner1': corner1,
            'corner2': corner2,
            'width': width,
            'height': height,
            'area': properties.get('area'),
            'perimeter': properties.get('length')
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that corner1 and corner2 are valid [x, y, z] coordinates'}
        )), 400

# 3D Operations (Phase 2)

@app.route('/draw/extrude', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_extrude():
    """Create 3D extruded solid from 2D profile."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_point3d, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'profile_points' not in data or 'height' not in data:
        return jsonify(create_error_response(
            'Missing required fields: profile_points and/or height',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['profile_points', 'height']}
        )), 400
    
    try:
        # Validate input parameters
        profile_points = [validate_point3d(point) for point in data['profile_points']]
        height = float(data['height'])
        taper_angle = float(data.get('taper_angle', 0.0))
        layer = validate_layer_name(data.get('layer', '3D_SOLIDS'))
        
        if len(profile_points) < 3:
            raise ValueError("Profile must have at least 3 points")
        if height <= 0:
            raise ValueError("Height must be positive")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create profile polyline first
        profile = acad.model.AddPolyline(profile_points)
        profile.Closed = True
        
        # Create extruded solid
        solid = acad.model.AddExtrudedSolid(profile, height, taper_angle)
        # Skip layer assignment due to COM compatibility issues
        # solid.Layer = layer
        
        # Clean up profile polyline (optional)
        # profile.Delete()
        
        # Extract entity properties
        properties = extract_entity_properties(solid)
        
        logger.info(f"Created extruded solid {solid.ObjectID} (height={height}) on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': solid.ObjectID,
            'entity_type': solid.ObjectName,
            'layer': layer,
            'height': height,
            'taper_angle': taper_angle,
            'volume': properties.get('volume'),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that profile_points is array of [x,y,z] coordinates and height > 0'}
        )), 400

@app.route('/draw/revolve', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_revolve():
    """Create 3D revolved solid around axis."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_point3d, validate_layer_name, extract_entity_properties, normalize_vector
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_point3d, validate_layer_name, extract_entity_properties, normalize_vector
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['profile_points', 'axis_point', 'axis_vector', 'angle']
    if not all(field in data for field in required_fields):
        return jsonify(create_error_response(
            f'Missing required fields: {[f for f in required_fields if f not in data]}',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': required_fields}
        )), 400
    
    try:
        # Validate input parameters
        profile_points = [validate_point3d(point) for point in data['profile_points']]
        axis_point = validate_point3d(data['axis_point'])
        axis_vector = normalize_vector(validate_point3d(data['axis_vector']))
        angle = float(data['angle'])
        layer = validate_layer_name(data.get('layer', '3D_SOLIDS'))
        
        if len(profile_points) < 3:
            raise ValueError("Profile must have at least 3 points")
        if not (0 < angle <= 360):
            raise ValueError("Angle must be between 0 and 360 degrees")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create profile polyline first
        profile = acad.model.AddPolyline(profile_points)
        profile.Closed = True
        
        # Convert angle to radians
        angle_rad = angle * math.pi / 180.0
        
        # Create revolved solid
        solid = acad.model.AddRevolvedSolid(profile, axis_point, axis_vector, angle_rad)
        solid.Layer = layer
        
        # Clean up profile polyline (optional)
        # profile.Delete()
        
        # Extract entity properties
        properties = extract_entity_properties(solid)
        
        logger.info(f"Created revolved solid {solid.ObjectID} (angle={angle}°) on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': solid.ObjectID,
            'entity_type': solid.ObjectName,
            'layer': layer,
            'angle': angle,
            'axis_point': axis_point,
            'axis_vector': axis_vector,
            'volume': properties.get('volume'),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check profile_points, axis parameters, and angle (0-360)'}
        )), 400

@app.route('/draw/boolean-union', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_boolean_union():
    """Perform boolean union on multiple solids."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_entity_id, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_entity_id, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'entity_ids' not in data:
        return jsonify(create_error_response(
            'Missing required field: entity_ids',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['entity_ids']}
        )), 400
    
    try:
        # Validate input parameters
        entity_ids = [validate_entity_id(eid) for eid in data['entity_ids']]
        layer = validate_layer_name(data.get('layer', '3D_SOLIDS'))
        
        if len(entity_ids) < 2:
            raise ValueError("Need at least 2 entities for union operation")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Get entities by ID
        entities = []
        for eid in entity_ids:
            entity = acad.get_entity_by_id(eid)
            if entity is None:
                raise ValueError(f"Entity with ID {eid} not found")
            entities.append(entity)
        
        # Perform union operation
        base_entity = entities[0]
        union_entities = entities[1:]
        result = acad.union_solids(base_entity, union_entities)
        result.Layer = layer
        
        # Extract entity properties
        properties = extract_entity_properties(result)
        
        logger.info(f"Created union solid {result.ObjectID} from {len(entity_ids)} entities on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': result.ObjectID,
            'entity_type': result.ObjectName,
            'layer': layer,
            'source_entities': entity_ids,
            'operation': 'union',
            'volume': properties.get('volume'),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that entity_ids contains valid solid entity IDs'}
        )), 400

@app.route('/draw/boolean-subtract', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def draw_boolean_subtract():
    """Perform boolean subtraction on solids."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_entity_id, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_entity_id, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['base_entity_id', 'subtract_entity_ids']
    if not all(field in data for field in required_fields):
        return jsonify(create_error_response(
            f'Missing required fields: {[f for f in required_fields if f not in data]}',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': required_fields}
        )), 400
    
    try:
        # Validate input parameters
        base_entity_id = validate_entity_id(data['base_entity_id'])
        subtract_entity_ids = [validate_entity_id(eid) for eid in data['subtract_entity_ids']]
        layer = validate_layer_name(data.get('layer', '3D_SOLIDS'))
        
        if len(subtract_entity_ids) < 1:
            raise ValueError("Need at least 1 entity to subtract")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Get base entity
        base_entity = acad.get_entity_by_id(base_entity_id)
        if base_entity is None:
            raise ValueError(f"Base entity with ID {base_entity_id} not found")
        
        # Get subtract entities
        subtract_entities = []
        for eid in subtract_entity_ids:
            entity = acad.get_entity_by_id(eid)
            if entity is None:
                raise ValueError(f"Subtract entity with ID {eid} not found")
            subtract_entities.append(entity)
        
        # Perform subtraction operation
        result = acad.subtract_solids(base_entity, subtract_entities)
        result.Layer = layer
        
        # Extract entity properties
        properties = extract_entity_properties(result)
        
        logger.info(f"Created subtract solid {result.ObjectID} from base {base_entity_id} on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': result.ObjectID,
            'entity_type': result.ObjectName,
            'layer': layer,
            'base_entity_id': base_entity_id,
            'subtract_entity_ids': subtract_entity_ids,
            'operation': 'subtract',
            'volume': properties.get('volume'),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that all entity IDs refer to valid solid entities'}
        )), 400

# Phase 3: Surface Mesh Operations

@app.route('/surface/3d-mesh', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def create_3d_mesh():
    """Create 3D mesh surface from rectangular grid of vertices."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_point3d, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'm_size' not in data or 'n_size' not in data or 'vertices' not in data:
        return jsonify(create_error_response(
            'Missing required fields: m_size, n_size, and/or vertices',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['m_size', 'n_size', 'vertices']}
        )), 400
    
    try:
        # Validate input parameters
        m_size = int(data['m_size'])
        n_size = int(data['n_size'])
        vertices = [validate_point3d(vertex) for vertex in data['vertices']]
        layer = validate_layer_name(data.get('layer', 'SURFACES'))
        
        if m_size < 2 or n_size < 2:
            raise ValueError("Mesh dimensions must be at least 2x2")
        if len(vertices) != m_size * n_size:
            raise ValueError(f"Expected {m_size * n_size} vertices, got {len(vertices)}")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create 3D mesh
        mesh = acad.model.Add3DMesh(m_size, n_size, vertices)
        # mesh.Layer = layer  # Skip layer assignment due to COM compatibility
        
        # Extract entity properties
        properties = extract_entity_properties(mesh)
        
        logger.info(f"Created 3D mesh {mesh.ObjectID} ({m_size}x{n_size}) on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': mesh.ObjectID,
            'entity_type': mesh.ObjectName,
            'layer': layer,
            'm_size': m_size,
            'n_size': n_size,
            'vertex_count': len(vertices),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check m_size, n_size are >= 2 and vertices array matches dimensions'}
        )), 400

@app.route('/surface/polyface-mesh', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def create_polyface_mesh():
    """Create polyface mesh with variable vertex counts per face."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_point3d, validate_layer_name, extract_entity_properties
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_point3d, validate_layer_name, extract_entity_properties
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'vertices' not in data or 'faces' not in data:
        return jsonify(create_error_response(
            'Missing required fields: vertices and/or faces',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['vertices', 'faces']}
        )), 400
    
    try:
        # Validate input parameters
        vertices = [validate_point3d(vertex) for vertex in data['vertices']]
        faces = data['faces']
        layer = validate_layer_name(data.get('layer', 'SURFACES'))
        
        if len(vertices) < 4:
            raise ValueError("Polyface mesh requires at least 4 vertices")
        if len(faces) < 1:
            raise ValueError("Polyface mesh requires at least 1 face")
            
        # Validate face indices
        for i, face in enumerate(faces):
            if not isinstance(face, list) or len(face) < 3:
                raise ValueError(f"Face {i} must have at least 3 vertex indices")
            for vertex_idx in face:
                if not isinstance(vertex_idx, int) or vertex_idx < 0 or vertex_idx >= len(vertices):
                    raise ValueError(f"Face {i} contains invalid vertex index: {vertex_idx}")
            
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create polyface mesh
        mesh = acad.model.AddPolyFaceMesh(vertices, faces)
        # mesh.Layer = layer  # Skip layer assignment due to COM compatibility
        
        # Extract entity properties
        properties = extract_entity_properties(mesh)
        
        logger.info(f"Created polyface mesh {mesh.ObjectID} ({len(vertices)} vertices, {len(faces)} faces) on layer '{layer}'")
        
        return jsonify(create_success_response({
            'entity_id': mesh.ObjectID,
            'entity_type': mesh.ObjectName,
            'layer': layer,
            'vertex_count': len(vertices),
            'face_count': len(faces),
            'properties': properties
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check vertices are valid 3D points and faces contain valid vertex indices'}
        )), 400

@app.route('/surface/unfold', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def unfold_surface():
    """Analyze and unfold a 3D surface mesh for manufacturing."""
    try:
        from .decorators import validate_json_request
        from .utils import validate_entity_id, validate_tolerance, analyze_surface_mesh, unfold_surface_simple
    except ImportError:
        from decorators import validate_json_request
        from utils import validate_entity_id, validate_tolerance, analyze_surface_mesh, unfold_surface_simple
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'entity_id' not in data:
        return jsonify(create_error_response(
            'Missing required field: entity_id',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['entity_id']}
        )), 400
    
    try:
        # Validate input parameters
        entity_id = validate_entity_id(data['entity_id'])
        tolerance = validate_tolerance(data.get('tolerance', 0.01))
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Find the entity by ID
        entity = None
        for obj in acad.model.modelspace:
            if obj.ObjectID == entity_id:
                entity = obj
                break
                
        if entity is None:
            return jsonify(create_error_response(
                f'Entity with ID {entity_id} not found',
                'ENTITY_NOT_FOUND',
                {'suggestion': 'Check that the entity_id is valid and the entity exists'}
            )), 404
        
        # Analyze the surface
        logger.info(f"Analyzing surface entity {entity_id} for unfolding")
        analysis = analyze_surface_mesh(entity)
        
        if 'error' in analysis:
            return jsonify(create_error_response(
                f'Surface analysis failed: {analysis["error"]}',
                'SURFACE_ANALYSIS_FAILED',
                {'suggestion': 'Ensure the entity is a valid 3D mesh or surface'}
            )), 400
        
        # Perform unfolding
        logger.info(f"Unfolding surface with tolerance {tolerance}")
        unfolding_result = unfold_surface_simple(analysis, tolerance)
        
        if 'error' in unfolding_result:
            return jsonify(create_error_response(
                f'Surface unfolding failed: {unfolding_result["error"]}',
                'SURFACE_UNFOLDING_FAILED',
                {'suggestion': 'Check that the surface is suitable for unfolding'}
            )), 400
        
        logger.info(f"Successfully unfolded surface {entity_id}")
        
        return jsonify(create_success_response({
            'entity_id': entity_id,
            'analysis': analysis,
            'unfolding': unfolding_result,
            'tolerance': tolerance,
            'operation': 'surface_unfold'
        }))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that entity_id is valid and tolerance is between 0.001 and 1.0'}
        )), 400

# Phase 4: Advanced Surface Unfolding with LSCM

@app.route('/surface/unfold-advanced', methods=['POST'])
@log_api_call
@handle_autocad_errors
@require_autocad_connection
def unfold_surface_advanced():
    """Advanced surface unfolding using LSCM algorithm for complex curved surfaces."""
    try:
        from .algorithms import extract_triangle_mesh, analyze_mesh_curvature, find_key_vertices_for_folding, calculate_geodesic_paths
        from .algorithms.lscm import unfold_surface_lscm
        from .utils import validate_entity_id, validate_tolerance
    except ImportError:
        from algorithms import extract_triangle_mesh, analyze_mesh_curvature, find_key_vertices_for_folding, calculate_geodesic_paths
        from algorithms.lscm import unfold_surface_lscm
        from utils import validate_entity_id, validate_tolerance
    
    # Validate request has JSON data
    if not request.is_json:
        return jsonify(create_error_response(
            'Request must be JSON',
            'INVALID_CONTENT_TYPE',
            {'suggestion': 'Set Content-Type header to application/json'}
        )), 400
    
    data = request.get_json()
    
    # Validate required fields
    if 'entity_id' not in data:
        return jsonify(create_error_response(
            'Missing required field: entity_id',
            'MISSING_REQUIRED_FIELDS',
            {'required_fields': ['entity_id']}
        )), 400
    
    try:
        # Validate input parameters
        entity_id = validate_entity_id(data['entity_id'])
        tolerance = validate_tolerance(data.get('tolerance', 0.001))
        algorithm = data.get('algorithm', 'lscm')  # 'lscm' or 'simple'
        generate_fold_lines = data.get('generate_fold_lines', True)
        boundary_constraints = data.get('boundary_constraints', None)
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Find the entity by ID
        entity = None
        for obj in acad.model.modelspace:
            if obj.ObjectID == entity_id:
                entity = obj
                break
                
        if entity is None:
            return jsonify(create_error_response(
                f'Entity with ID {entity_id} not found',
                'ENTITY_NOT_FOUND',
                {'suggestion': 'Check that the entity_id is valid and the entity exists'}
            )), 404
        
        logger.info(f"Advanced unfolding entity {entity_id} using {algorithm} algorithm")
        
        # Extract triangle mesh from AutoCAD entity
        try:
            vertices, triangles = extract_triangle_mesh(entity)
            logger.info(f"Extracted mesh: {len(vertices)} vertices, {len(triangles)} triangles")
        except Exception as e:
            return jsonify(create_error_response(
                f'Failed to extract triangle mesh: {str(e)}',
                'MESH_EXTRACTION_FAILED',
                {'suggestion': 'Ensure the entity is a valid 3D mesh surface'}
            )), 400
        
        # Perform curvature analysis
        curvature_analysis = analyze_mesh_curvature(vertices, triangles)
        
        # Choose unfolding algorithm
        if algorithm == 'lscm':
            # Use LSCM algorithm for advanced unfolding
            unfolding_result = unfold_surface_lscm(vertices, triangles, boundary_constraints, tolerance)
        else:
            # Fall back to simple algorithm
            from utils import analyze_surface_mesh, unfold_surface_simple
            analysis = analyze_surface_mesh(entity)
            unfolding_result = unfold_surface_simple(analysis, tolerance)
        
        if not unfolding_result.get('success', False):
            return jsonify(create_error_response(
                f'Surface unfolding failed: {unfolding_result.get("error", "Unknown error")}',
                'SURFACE_UNFOLDING_FAILED',
                {'suggestion': 'Try different algorithm or check mesh quality'}
            )), 400
        
        # Generate advanced fold lines if requested
        fold_lines_data = None
        if generate_fold_lines and algorithm == 'lscm':
            try:
                # Find key vertices for fold line placement
                key_vertices = find_key_vertices_for_folding(vertices, triangles, curvature_analysis)
                
                if len(key_vertices) > 1:
                    # Calculate geodesic paths between key vertices
                    geodesic_result = calculate_geodesic_paths(vertices, triangles, key_vertices)
                    fold_lines_data = geodesic_result.get('fold_lines', [])
                    logger.info(f"Generated {len(fold_lines_data)} advanced fold lines")
                else:
                    logger.warning("Insufficient key vertices for fold line generation")
                    fold_lines_data = []
                    
            except Exception as e:
                logger.warning(f"Advanced fold line generation failed: {e}")
                fold_lines_data = []
        
        # Prepare comprehensive response
        response_data = {
            'entity_id': entity_id,
            'algorithm': algorithm,
            'tolerance': tolerance,
            'mesh_info': {
                'n_vertices': len(vertices),
                'n_triangles': len(triangles),
                'surface_type': curvature_analysis.get('surface_type', 'unknown')
            },
            'curvature_analysis': curvature_analysis,
            'unfolding_result': unfolding_result,
            'operation': 'advanced_surface_unfold'
        }
        
        # Add fold lines if generated
        if fold_lines_data is not None:
            response_data['fold_lines'] = fold_lines_data
            response_data['n_fold_lines'] = len(fold_lines_data)
        
        logger.info(f"Advanced surface unfolding completed successfully")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that entity_id is valid and tolerance is between 0.001 and 1.0'}
        )), 400
    except Exception as e:
        logger.error(f"Advanced surface unfolding failed: {e}")
        return jsonify(create_error_response(
            f'Advanced unfolding failed: {str(e)}',
            'ADVANCED_UNFOLDING_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500

# ============================================================================
# DIMENSIONING AND ANNOTATION ENDPOINTS - PHASE 4
# ============================================================================

@app.route('/dimension/linear', methods=['POST'])
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def create_linear_dimension():
    """
    Create a linear dimension between two points.
    
    Expected JSON payload:
    {
        "start_point": [x1, y1, z1],
        "end_point": [x2, y2, z2], 
        "dimension_line_point": [x3, y3, z3],
        "text_override": "optional custom text"
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'start_point' not in data or 'end_point' not in data or 'dimension_line_point' not in data:
            return jsonify(create_error_response(
                'Missing required parameters: start_point, end_point, dimension_line_point',
                'MISSING_PARAMETERS',
                {'required': ['start_point', 'end_point', 'dimension_line_point']}
            )), 400
        
        start_point = data['start_point']
        end_point = data['end_point']
        dimension_line_point = data['dimension_line_point']
        text_override = data.get('text_override')
        
        # Validate point format
        for point_name, point in [('start_point', start_point), ('end_point', end_point), ('dimension_line_point', dimension_line_point)]:
            if not isinstance(point, list) or len(point) != 3:
                return jsonify(create_error_response(
                    f'{point_name} must be a 3-element list [x, y, z]',
                    'INVALID_POINT_FORMAT',
                    {'example': '[0.0, 0.0, 0.0]'}
                )), 400
        
        logger.info(f"Creating linear dimension from {start_point} to {end_point}")
        
        # Get AutoCAD instance and create dimensioning system
        acad = get_autocad_instance()
        dim_system = DimensioningSystem(acad)
        
        # Create the linear dimension
        dimension_result = dim_system.create_linear_dimension(start_point, end_point, dimension_line_point, text_override)
        
        if 'error' in dimension_result:
            return jsonify(create_error_response(
                f'Failed to create linear dimension: {dimension_result["error"]}',
                'DIMENSION_CREATION_FAILED',
                {'suggestion': 'Check point coordinates and ensure AutoCAD is responsive'}
            )), 500
        
        # Zoom to show the dimension
        acad.app.ZoomExtents()
        
        response_data = {
            'dimension_info': dimension_result,
            'operation': 'create_linear_dimension',
            'dimension_type': 'linear'
        }
        
        logger.info(f"Linear dimension created successfully")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that all points are valid 3D coordinates'}
        )), 400
    except Exception as e:
        logger.error(f"Linear dimension creation failed: {e}")
        return jsonify(create_error_response(
            f'Dimension creation failed: {str(e)}',
            'DIMENSION_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/dimension/angular', methods=['POST'])
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def create_angular_dimension():
    """
    Create an angular dimension between two lines.
    
    Expected JSON payload:
    {
        "vertex_point": [x, y, z],
        "first_point": [x1, y1, z1],
        "second_point": [x2, y2, z2],
        "text_point": [x3, y3, z3]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        required_params = ['vertex_point', 'first_point', 'second_point', 'text_point']
        if not data or not all(param in data for param in required_params):
            return jsonify(create_error_response(
                f'Missing required parameters: {", ".join(required_params)}',
                'MISSING_PARAMETERS',
                {'required': required_params}
            )), 400
        
        vertex_point = data['vertex_point']
        first_point = data['first_point']
        second_point = data['second_point']
        text_point = data['text_point']
        
        # Validate point format
        for point_name, point in [('vertex_point', vertex_point), ('first_point', first_point), 
                                 ('second_point', second_point), ('text_point', text_point)]:
            if not isinstance(point, list) or len(point) != 3:
                return jsonify(create_error_response(
                    f'{point_name} must be a 3-element list [x, y, z]',
                    'INVALID_POINT_FORMAT',
                    {'example': '[0.0, 0.0, 0.0]'}
                )), 400
        
        logger.info(f"Creating angular dimension at vertex {vertex_point}")
        
        # Get AutoCAD instance and create dimensioning system
        acad = get_autocad_instance()
        dim_system = DimensioningSystem(acad)
        
        # Create the angular dimension
        dimension_result = dim_system.create_angular_dimension(vertex_point, first_point, second_point, text_point)
        
        if 'error' in dimension_result:
            return jsonify(create_error_response(
                f'Failed to create angular dimension: {dimension_result["error"]}',
                'DIMENSION_CREATION_FAILED',
                {'suggestion': 'Check point coordinates and ensure they form a valid angle'}
            )), 500
        
        # Zoom to show the dimension
        acad.app.ZoomExtents()
        
        response_data = {
            'dimension_info': dimension_result,
            'operation': 'create_angular_dimension',
            'dimension_type': 'angular'
        }
        
        logger.info(f"Angular dimension created successfully")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that all points are valid 3D coordinates'}
        )), 400
    except Exception as e:
        logger.error(f"Angular dimension creation failed: {e}")
        return jsonify(create_error_response(
            f'Dimension creation failed: {str(e)}',
            'DIMENSION_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/dimension/annotate', methods=['POST'])
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def create_text_annotation():
    """
    Create a text annotation.
    
    Expected JSON payload:
    {
        "insertion_point": [x, y, z],
        "text_content": "annotation text",
        "text_height": 2.5,  // optional
        "rotation": 0.0      // optional, degrees
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'insertion_point' not in data or 'text_content' not in data:
            return jsonify(create_error_response(
                'Missing required parameters: insertion_point, text_content',
                'MISSING_PARAMETERS',
                {'required': ['insertion_point', 'text_content']}
            )), 400
        
        insertion_point = data['insertion_point']
        text_content = data['text_content']
        text_height = data.get('text_height')
        rotation = data.get('rotation', 0.0)
        
        # Validate insertion point format
        if not isinstance(insertion_point, list) or len(insertion_point) != 3:
            return jsonify(create_error_response(
                'insertion_point must be a 3-element list [x, y, z]',
                'INVALID_POINT_FORMAT',
                {'example': '[0.0, 0.0, 0.0]'}
            )), 400
        
        # Validate text content
        if not isinstance(text_content, str) or len(text_content.strip()) == 0:
            return jsonify(create_error_response(
                'text_content must be a non-empty string',
                'INVALID_TEXT_CONTENT',
                {'example': 'Manufacturing Note: Check tolerances'}
            )), 400
        
        logger.info(f"Creating text annotation: '{text_content[:50]}...'")
        
        # Get AutoCAD instance and create dimensioning system
        acad = get_autocad_instance()
        dim_system = DimensioningSystem(acad)
        
        # Create the text annotation
        annotation_result = dim_system.create_text_annotation(insertion_point, text_content, text_height, rotation)
        
        if 'error' in annotation_result:
            return jsonify(create_error_response(
                f'Failed to create text annotation: {annotation_result["error"]}',
                'ANNOTATION_CREATION_FAILED',
                {'suggestion': 'Check point coordinates and text content'}
            )), 500
        
        # Zoom to show the annotation
        acad.app.ZoomExtents()
        
        response_data = {
            'annotation_info': annotation_result,
            'operation': 'create_text_annotation'
        }
        
        logger.info(f"Text annotation created successfully")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that insertion point is valid and text is non-empty'}
        )), 400
    except Exception as e:
        logger.error(f"Text annotation creation failed: {e}")
        return jsonify(create_error_response(
            f'Annotation creation failed: {str(e)}',
            'ANNOTATION_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/dimension/manufacturing-drawing', methods=['POST'])
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def create_manufacturing_drawing_endpoint():
    """
    Create a complete manufacturing drawing with automatic dimensioning.
    
    Expected JSON payload:
    {
        "pattern_data": {
            // Unfolded pattern data from surface/unfold endpoints
            "pattern_bounds": {...},
            "fold_lines": [...],
            "manufacturing_data": {...},
            "method": "LSCM" or "simple",
            ...
        }
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'pattern_data' not in data:
            return jsonify(create_error_response(
                'Missing required parameter: pattern_data',
                'MISSING_PARAMETERS',
                {'required': ['pattern_data'], 'suggestion': 'Use output from surface/unfold endpoints'}
            )), 400
        
        pattern_data = data['pattern_data']
        
        # Validate pattern data structure
        if not isinstance(pattern_data, dict):
            return jsonify(create_error_response(
                'pattern_data must be a dictionary containing unfolding results',
                'INVALID_PATTERN_DATA',
                {'suggestion': 'Use the output from /surface/unfold or /surface/unfold-advanced'}
            )), 400
        
        logger.info(f"Creating manufacturing drawing for {pattern_data.get('method', 'unknown')} unfolding")
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Create the complete manufacturing drawing
        drawing_result = create_manufacturing_drawing(acad, pattern_data)
        
        if 'error' in drawing_result:
            return jsonify(create_error_response(
                f'Failed to create manufacturing drawing: {drawing_result["error"]}',
                'MANUFACTURING_DRAWING_FAILED',
                {'suggestion': 'Check that pattern_data contains valid unfolding results'}
            )), 500
        
        response_data = {
            'drawing_result': drawing_result,
            'operation': 'create_manufacturing_drawing',
            'pattern_method': pattern_data.get('method', 'unknown')
        }
        
        logger.info(f"Manufacturing drawing created successfully with {drawing_result.get('total_elements', 0)} elements")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that pattern_data is valid unfolding result'}
        )), 400
    except Exception as e:
        logger.error(f"Manufacturing drawing creation failed: {e}")
        return jsonify(create_error_response(
            f'Manufacturing drawing creation failed: {str(e)}',
            'MANUFACTURING_DRAWING_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


# ============================================================================
# PATTERN OPTIMIZATION AND NESTING ENDPOINTS - PHASE 4
# ============================================================================

@app.route('/pattern/optimize-nesting', methods=['POST'])
@handle_autocad_errors
@log_api_call
def optimize_pattern_nesting():
    """
    Optimize pattern nesting for material efficiency.
    
    Expected JSON payload:
    {
        "patterns": [
            {
                "id": "pattern_1",
                "width": 100.0,
                "height": 50.0,
                "area": 5000.0,  // optional
                "vertices": [[0,0], [100,0], [100,50], [0,50]],  // optional
                "rotation_allowed": true,  // optional
                "priority": 1.0  // optional
            }
        ],
        "material_sheets": [
            {
                "width": 1000.0,
                "height": 600.0,
                "material_type": "steel_sheet",
                "cost_per_area": 0.01,  // optional
                "waste_factor": 0.05  // optional
            }
        ],
        "algorithm": "best_fit_decreasing",  // optional
        "max_sheets": 10,  // optional
        "rotation_angles": [0, 90, 180, 270]  // optional
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'patterns' not in data or 'material_sheets' not in data:
            return jsonify(create_error_response(
                'Missing required parameters: patterns, material_sheets',
                'MISSING_PARAMETERS',
                {'required': ['patterns', 'material_sheets']}
            )), 400
        
        patterns_data = data['patterns']
        sheets_data = data['material_sheets']
        algorithm = data.get('algorithm', 'best_fit_decreasing')
        max_sheets = data.get('max_sheets', 10)
        rotation_angles = data.get('rotation_angles', [0, 90, 180, 270])
        
        # Validate patterns data
        if not isinstance(patterns_data, list) or not patterns_data:
            return jsonify(create_error_response(
                'patterns must be a non-empty list',
                'INVALID_PATTERNS_DATA',
                {'example': '[{"id": "p1", "width": 100, "height": 50}]'}
            )), 400
        
        # Validate material sheets data
        if not isinstance(sheets_data, list) or not sheets_data:
            return jsonify(create_error_response(
                'material_sheets must be a non-empty list',
                'INVALID_SHEETS_DATA',
                {'example': '[{"width": 1000, "height": 600, "material_type": "steel"}]'}
            )), 400
        
        logger.info(f"Optimizing nesting for {len(patterns_data)} patterns on {len(sheets_data)} sheet types")
        
        try:
            # Create Pattern objects
            patterns = []
            for i, p_data in enumerate(patterns_data):
                if 'width' not in p_data or 'height' not in p_data:
                    return jsonify(create_error_response(
                        f'Pattern {i} missing required width/height',
                        'INVALID_PATTERN_FORMAT',
                        {'required': ['width', 'height']}
                    )), 400
                
                pattern = Pattern(
                    id=p_data.get('id', f'pattern_{i}'),
                    width=float(p_data['width']),
                    height=float(p_data['height']),
                    area=float(p_data.get('area', p_data['width'] * p_data['height'])),
                    vertices=p_data.get('vertices', []),
                    rotation_allowed=p_data.get('rotation_allowed', True),
                    priority=float(p_data.get('priority', 1.0))
                )
                patterns.append(pattern)
            
            # Create MaterialSheet objects
            material_sheets = []
            for i, s_data in enumerate(sheets_data):
                if 'width' not in s_data or 'height' not in s_data:
                    return jsonify(create_error_response(
                        f'Material sheet {i} missing required width/height',
                        'INVALID_SHEET_FORMAT',
                        {'required': ['width', 'height']}
                    )), 400
                
                sheet = MaterialSheet(
                    width=float(s_data['width']),
                    height=float(s_data['height']),
                    material_type=s_data.get('material_type', 'generic'),
                    cost_per_area=float(s_data.get('cost_per_area', 1.0)),
                    waste_factor=float(s_data.get('waste_factor', 0.05))
                )
                material_sheets.append(sheet)
                
        except (ValueError, TypeError) as e:
            return jsonify(create_error_response(
                f'Invalid numeric values in pattern/sheet data: {str(e)}',
                'INVALID_NUMERIC_DATA',
                {'suggestion': 'Ensure all dimensions and costs are valid numbers'}
            )), 400
        
        # Initialize optimizer and run optimization
        optimizer = PatternNestingOptimizer(material_sheets)
        result = optimizer.optimize_nesting(patterns, algorithm, max_sheets, rotation_angles)
        
        if not result['success']:
            return jsonify(create_error_response(
                f'Pattern nesting optimization failed: {result.get("error", "Unknown error")}',
                'OPTIMIZATION_FAILED',
                {'suggestion': 'Check pattern dimensions and material sheet sizes'}
            )), 500
        
        response_data = {
            'optimization_result': result,
            'operation': 'optimize_pattern_nesting',
            'algorithm_used': algorithm
        }
        
        logger.info(f"Pattern nesting optimized: {result['optimization_metrics']['total_material_utilization']:.1f}% utilization")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that all parameters are valid'}
        )), 400
    except Exception as e:
        logger.error(f"Pattern nesting optimization failed: {e}")
        return jsonify(create_error_response(
            f'Optimization failed: {str(e)}',
            'NESTING_OPTIMIZATION_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/pattern/optimize-from-unfolding', methods=['POST'])
@handle_autocad_errors
@log_api_call
def optimize_from_unfolding_results():
    """
    Optimize material usage from multiple unfolding results.
    
    Expected JSON payload:
    {
        "unfolding_results": [
            {
                // Output from surface/unfold or surface/unfold-advanced endpoints
                "success": true,
                "method": "LSCM",
                "pattern_bounds": {...},
                "pattern_size": [100, 50],
                "uv_coordinates": [...],
                "distortion_metrics": {...},
                ...
            }
        ],
        "material_sheets": [
            {
                "width": 1000.0,
                "height": 600.0,
                "material_type": "steel_sheet",
                "cost_per_area": 0.01
            }
        ],
        "algorithm": "best_fit_decreasing"  // optional
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'unfolding_results' not in data or 'material_sheets' not in data:
            return jsonify(create_error_response(
                'Missing required parameters: unfolding_results, material_sheets',
                'MISSING_PARAMETERS',
                {'required': ['unfolding_results', 'material_sheets']}
            )), 400
        
        unfolding_results = data['unfolding_results']
        sheets_data = data['material_sheets']
        algorithm = data.get('algorithm', 'best_fit_decreasing')
        
        # Validate unfolding results
        if not isinstance(unfolding_results, list) or not unfolding_results:
            return jsonify(create_error_response(
                'unfolding_results must be a non-empty list',
                'INVALID_UNFOLDING_RESULTS',
                {'suggestion': 'Use outputs from surface/unfold endpoints'}
            )), 400
        
        logger.info(f"Optimizing material usage from {len(unfolding_results)} unfolding results")
        
        try:
            # Create patterns from unfolding results
            patterns = create_patterns_from_unfolding_results(unfolding_results)
            
            if not patterns:
                return jsonify(create_error_response(
                    'No valid patterns could be created from unfolding results',
                    'NO_VALID_PATTERNS',
                    {'suggestion': 'Check that unfolding results contain valid pattern data'}
                )), 400
            
            # Create MaterialSheet objects
            material_sheets = []
            for i, s_data in enumerate(sheets_data):
                if 'width' not in s_data or 'height' not in s_data:
                    return jsonify(create_error_response(
                        f'Material sheet {i} missing required width/height',
                        'INVALID_SHEET_FORMAT',
                        {'required': ['width', 'height']}
                    )), 400
                
                sheet = MaterialSheet(
                    width=float(s_data['width']),
                    height=float(s_data['height']),
                    material_type=s_data.get('material_type', 'generic'),
                    cost_per_area=float(s_data.get('cost_per_area', 1.0)),
                    waste_factor=float(s_data.get('waste_factor', 0.05))
                )
                material_sheets.append(sheet)
                
        except (ValueError, TypeError) as e:
            return jsonify(create_error_response(
                f'Invalid data in unfolding results or material sheets: {str(e)}',
                'INVALID_INPUT_DATA',
                {'suggestion': 'Ensure all dimensions are valid numbers'}
            )), 400
        
        # Run material usage optimization
        result = optimize_material_usage(patterns, material_sheets, algorithm)
        
        if not result['success']:
            return jsonify(create_error_response(
                f'Material usage optimization failed: {result.get("error", "Unknown error")}',
                'OPTIMIZATION_FAILED',
                {'suggestion': 'Check pattern compatibility with material sheet sizes'}
            )), 500
        
        response_data = {
            'optimization_result': result,
            'patterns_created': len(patterns),
            'operation': 'optimize_from_unfolding_results',
            'algorithm_used': algorithm
        }
        
        logger.info(f"Material usage optimized from unfolding results: {result['optimization_metrics']['total_material_utilization']:.1f}% utilization")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that all parameters are valid'}
        )), 400
    except Exception as e:
        logger.error(f"Material usage optimization failed: {e}")
        return jsonify(create_error_response(
            f'Optimization failed: {str(e)}',
            'MATERIAL_OPTIMIZATION_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/pattern/material-sheets', methods=['GET'])
@log_api_call
def get_standard_material_sheets():
    """
    Get a list of standard material sheet sizes and specifications.
    
    Returns predefined material sheets commonly used in manufacturing.
    """
    try:
        # Standard material sheets for manufacturing
        standard_sheets = [
            {
                'name': 'Steel Sheet 4x8ft',
                'width': 1219.2,  # mm
                'height': 2438.4,  # mm  
                'material_type': 'steel',
                'thickness': 1.5,  # mm
                'cost_per_area': 0.015,  # cost per mm²
                'waste_factor': 0.05,
                'description': 'Standard 4x8 foot steel sheet'
            },
            {
                'name': 'Steel Sheet 5x10ft',
                'width': 1524.0,
                'height': 3048.0,
                'material_type': 'steel', 
                'thickness': 2.0,
                'cost_per_area': 0.018,
                'waste_factor': 0.05,
                'description': 'Large 5x10 foot steel sheet'
            },
            {
                'name': 'Aluminum Sheet 4x8ft',
                'width': 1219.2,
                'height': 2438.4,
                'material_type': 'aluminum',
                'thickness': 1.6,
                'cost_per_area': 0.025,
                'waste_factor': 0.04,
                'description': 'Standard 4x8 foot aluminum sheet'
            },
            {
                'name': 'Stainless Steel 3x6ft',
                'width': 914.4,
                'height': 1828.8,
                'material_type': 'stainless_steel',
                'thickness': 1.2,
                'cost_per_area': 0.035,  
                'waste_factor': 0.06,
                'description': '3x6 foot stainless steel sheet'
            },
            {
                'name': 'Cardboard Sheet A1',
                'width': 594.0,
                'height': 841.0,
                'material_type': 'cardboard',
                'thickness': 3.0,
                'cost_per_area': 0.002,
                'waste_factor': 0.08,
                'description': 'A1 size cardboard for prototyping'
            },
            {
                'name': 'Plywood Sheet 4x8ft',
                'width': 1219.2,
                'height': 2438.4,
                'material_type': 'plywood',
                'thickness': 12.0,
                'cost_per_area': 0.008,
                'waste_factor': 0.10,
                'description': '4x8 foot plywood sheet'
            }
        ]
        
        response_data = {
            'standard_sheets': standard_sheets,
            'count': len(standard_sheets),
            'operation': 'get_standard_material_sheets'
        }
        
        logger.info(f"Returned {len(standard_sheets)} standard material sheet specifications")
        
        return jsonify(create_success_response(response_data))
        
    except Exception as e:
        logger.error(f"Failed to get standard material sheets: {e}")
        return jsonify(create_error_response(
            f'Failed to retrieve material sheets: {str(e)}',
            'MATERIAL_SHEETS_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


# ============================================================================
# BATCH PROCESSING ENDPOINTS - PHASE 4
# ============================================================================

@app.route('/batch/surface-unfold', methods=['POST'])
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def batch_surface_unfold():
    """
    Batch process multiple surfaces for unfolding.
    
    Expected JSON payload:
    {
        "entity_ids": [123, 456, 789],
        "algorithm": "lscm",  // optional, default "simple"
        "tolerance": 0.001,   // optional
        "generate_fold_lines": true,  // optional
        "create_manufacturing_drawings": true,  // optional
        "optimize_material_usage": true,  // optional
        "material_sheets": [  // required if optimize_material_usage is true
            {
                "width": 1000.0,
                "height": 600.0,
                "material_type": "steel_sheet"
            }
        ]
    }
    """
    try:
        data = request.get_json()
        
        # Validate required parameters
        if not data or 'entity_ids' not in data:
            return jsonify(create_error_response(
                'Missing required parameter: entity_ids',
                'MISSING_PARAMETERS',
                {'required': ['entity_ids']}
            )), 400
        
        entity_ids = data['entity_ids']
        algorithm = data.get('algorithm', 'simple')
        tolerance = data.get('tolerance', 0.001)
        generate_fold_lines = data.get('generate_fold_lines', False)
        create_drawings = data.get('create_manufacturing_drawings', False)
        optimize_material = data.get('optimize_material_usage', False)
        material_sheets_data = data.get('material_sheets', [])
        
        # Validate entity_ids
        if not isinstance(entity_ids, list) or not entity_ids:
            return jsonify(create_error_response(
                'entity_ids must be a non-empty list of integers',
                'INVALID_ENTITY_IDS',
                {'example': '[123, 456, 789]'}
            )), 400
        
        logger.info(f"Starting batch surface unfolding for {len(entity_ids)} entities")
        
        # Get AutoCAD instance
        acad = get_autocad_instance()
        
        # Process each surface
        batch_results = []
        successful_unfoldings = []
        failed_unfoldings = []
        
        for i, entity_id in enumerate(entity_ids):
            try:
                logger.info(f"Processing entity {entity_id} ({i+1}/{len(entity_ids)})")
                
                # Get the entity
                try:
                    entity = acad.doc.ObjectIdToObject(entity_id)
                except:
                    logger.warning(f"Entity {entity_id} not found, skipping")
                    failed_unfoldings.append({
                        'entity_id': entity_id,
                        'error': 'Entity not found',
                        'stage': 'entity_retrieval'
                    })
                    continue
                
                # Perform unfolding based on algorithm
                if algorithm == 'lscm':
                    # Use advanced LSCM algorithm
                    try:
                        from algorithms.mesh_utils import extract_triangle_mesh, analyze_mesh_curvature
                        from algorithms.lscm import unfold_surface_lscm
                        from algorithms.geodesic import calculate_geodesic_paths, find_key_vertices_for_folding
                        
                        # Extract triangle mesh
                        vertices, triangles = extract_triangle_mesh(entity)
                        
                        # Perform curvature analysis
                        curvature_analysis = analyze_mesh_curvature(vertices, triangles)
                        
                        # Run LSCM unfolding
                        unfolding_result = unfold_surface_lscm(vertices, triangles, None, tolerance)
                        
                        # Generate fold lines if requested
                        if generate_fold_lines and unfolding_result.get('success', False):
                            try:
                                key_vertices = find_key_vertices_for_folding(vertices, triangles, curvature_analysis)
                                if len(key_vertices) > 1:
                                    geodesic_result = calculate_geodesic_paths(vertices, triangles, key_vertices)
                                    unfolding_result['fold_lines'] = geodesic_result.get('fold_lines', [])
                            except Exception as e:
                                logger.warning(f"Fold line generation failed for entity {entity_id}: {e}")
                                unfolding_result['fold_lines'] = []
                        
                    except Exception as e:
                        logger.error(f"LSCM unfolding failed for entity {entity_id}: {e}")
                        failed_unfoldings.append({
                            'entity_id': entity_id,
                            'error': str(e),
                            'stage': 'lscm_unfolding'
                        })
                        continue
                else:
                    # Use simple unfolding algorithm
                    try:
                        from utils import analyze_surface_mesh, unfold_surface_simple
                        
                        analysis = analyze_surface_mesh(entity)
                        unfolding_result = unfold_surface_simple(analysis, tolerance)
                        
                    except Exception as e:
                        logger.error(f"Simple unfolding failed for entity {entity_id}: {e}")
                        failed_unfoldings.append({
                            'entity_id': entity_id,
                            'error': str(e),
                            'stage': 'simple_unfolding'
                        })
                        continue
                
                if unfolding_result.get('success', False):
                    # Add entity ID to result
                    unfolding_result['entity_id'] = entity_id
                    unfolding_result['algorithm'] = algorithm
                    unfolding_result['processing_order'] = i + 1
                    
                    batch_results.append(unfolding_result)
                    successful_unfoldings.append(unfolding_result)
                    
                    logger.info(f"Successfully unfolded entity {entity_id}")
                else:
                    failed_unfoldings.append({
                        'entity_id': entity_id,
                        'error': unfolding_result.get('error', 'Unknown unfolding error'),
                        'stage': 'unfolding_processing'
                    })
                    
            except Exception as e:
                logger.error(f"Batch processing failed for entity {entity_id}: {e}")
                failed_unfoldings.append({
                    'entity_id': entity_id,
                    'error': str(e),
                    'stage': 'batch_processing'
                })
        
        # Create manufacturing drawings if requested
        drawing_results = []
        if create_drawings and successful_unfoldings:
            logger.info(f"Creating manufacturing drawings for {len(successful_unfoldings)} successful unfoldings")
            
            for unfolding in successful_unfoldings:
                try:
                    drawing_result = create_manufacturing_drawing(acad, unfolding)
                    if 'error' not in drawing_result:
                        drawing_results.append({
                            'entity_id': unfolding['entity_id'],
                            'drawing_result': drawing_result
                        })
                except Exception as e:
                    logger.warning(f"Manufacturing drawing failed for entity {unfolding['entity_id']}: {e}")
        
        # Optimize material usage if requested
        optimization_result = None
        if optimize_material and successful_unfoldings and material_sheets_data:
            logger.info(f"Optimizing material usage for {len(successful_unfoldings)} patterns")
            
            try:
                # Create material sheets
                material_sheets = []
                for s_data in material_sheets_data:
                    sheet = MaterialSheet(
                        width=float(s_data['width']),
                        height=float(s_data['height']),
                        material_type=s_data.get('material_type', 'generic'),
                        cost_per_area=float(s_data.get('cost_per_area', 1.0)),
                        waste_factor=float(s_data.get('waste_factor', 0.05))
                    )
                    material_sheets.append(sheet)
                
                # Optimize material usage
                optimization_result = optimize_material_usage(
                    create_patterns_from_unfolding_results(successful_unfoldings),
                    material_sheets
                )
                
            except Exception as e:
                logger.warning(f"Material optimization failed: {e}")
                optimization_result = {'success': False, 'error': str(e)}
        
        # Prepare comprehensive response
        response_data = {
            'batch_summary': {
                'total_entities': len(entity_ids),
                'successful_unfoldings': len(successful_unfoldings),
                'failed_unfoldings': len(failed_unfoldings),
                'algorithm_used': algorithm,
                'manufacturing_drawings_created': len(drawing_results),
                'material_optimization_performed': optimization_result is not None
            },
            'successful_results': successful_unfoldings,
            'failed_results': failed_unfoldings,
            'operation': 'batch_surface_unfold'
        }
        
        # Add optional results
        if drawing_results:
            response_data['manufacturing_drawings'] = drawing_results
        
        if optimization_result:
            response_data['material_optimization'] = optimization_result
        
        logger.info(f"Batch surface unfolding completed: {len(successful_unfoldings)}/{len(entity_ids)} successful")
        
        return jsonify(create_success_response(response_data))
        
    except ValueError as e:
        return jsonify(create_error_response(
            str(e),
            'INVALID_PARAMETERS',
            {'suggestion': 'Check that entity_ids are valid integers and parameters are correct'}
        )), 400
    except Exception as e:
        logger.error(f"Batch surface unfolding failed: {e}")
        return jsonify(create_error_response(
            f'Batch processing failed: {str(e)}',
            'BATCH_PROCESSING_ERROR',
            {'suggestion': 'Check server logs for detailed error information'}
        )), 500


@app.route('/batch/status/<batch_id>', methods=['GET'])
@log_api_call
def get_batch_status(batch_id: str):
    """
    Get the status of a batch processing job.
    
    Note: This is a placeholder for future implementation of asynchronous batch processing.
    Currently returns a simple response indicating synchronous processing.
    """
    try:
        # Placeholder for future async batch processing
        # In a full implementation, this would check the status of long-running batch jobs
        
        response_data = {
            'batch_id': batch_id,
            'status': 'synchronous_processing',
            'message': 'Current implementation processes batches synchronously',
            'operation': 'get_batch_status',
            'suggestion': 'Use /batch/surface-unfold for immediate processing'
        }
        
        logger.info(f"Batch status requested for {batch_id}")
        
        return jsonify(create_success_response(response_data))
        
    except Exception as e:
        logger.error(f"Failed to get batch status: {e}")
        return jsonify(create_error_response(
            f'Failed to retrieve batch status: {str(e)}',
            'BATCH_STATUS_ERROR',
            {'suggestion': 'Check that batch_id is valid'}
        )), 500


# Application startup
if __name__ == '__main__':
    logger.info(f"Starting server on {config.HOST}:{config.PORT}")
    
    try:
        app.run(
            host=config.HOST,
            port=config.PORT,
            debug=config.DEBUG,
            threaded=True
        )
    except Exception as e:
        logger.critical(f"Failed to start server: {e}")
        raise
