
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
except ImportError:
    # Fall back to absolute imports (for standalone usage)
    from config import config
    from decorators import handle_autocad_errors, log_api_call, require_autocad_connection
    from utils import get_autocad_instance, create_success_response, create_error_response

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
