
"""
AutoCAD MCP Server - Phase 1 Implementation
A Model Context Protocol server for AutoCAD 2025 automation.
"""

import logging
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
        line.Layer = layer
        
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
        circle.Layer = layer
        
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
