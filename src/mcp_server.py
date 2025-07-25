"""
AutoCAD MCP Server - Model Context Protocol implementation
Converts the Flask HTTP server to proper MCP server for VS Code/Roo Code integration
"""

from mcp.server import FastMCP
from mcp import McpError
from mcp.types import Tool
import asyncio
import logging
from typing import Any, Dict, List, Optional, Tuple
import json

# Import existing AutoCAD functionality
from utils import get_autocad_instance
# from decorators import handle_autocad_errors  # Not needed for MCP

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server
mcp = FastMCP("AutoCAD MCP Server")

@mcp.tool()
def draw_line(start_point: List[float], end_point: List[float]) -> str:
    """
    Draw a line in AutoCAD from start point to end point.
    
    Args:
        start_point: [x, y, z] coordinates for line start
        end_point: [x, y, z] coordinates for line end
    
    Returns:
        Success message with entity information
    """
    try:
        acad = get_autocad_instance()
        entity_id = acad.draw_line(start_point, end_point)
        return f"Line created successfully with entity ID: {entity_id}"
    except Exception as e:
        logger.error(f"Error drawing line: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to draw line: {str(e)}")

@mcp.tool()
def draw_circle(center: List[float], radius: float) -> str:
    """
    Draw a circle in AutoCAD.
    
    Args:
        center: [x, y, z] coordinates for circle center
        radius: Circle radius
    
    Returns:
        Success message with entity information
    """
    try:
        acad = get_autocad_instance()
        entity_id = acad.draw_circle(center, radius)
        return f"Circle created successfully with entity ID: {entity_id}"
    except Exception as e:
        logger.error(f"Error drawing circle: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to draw circle: {str(e)}")

@mcp.tool()
def extrude_profile(profile_points: List[List[float]], extrude_height: float) -> str:
    """
    Create 3D extruded solid from 2D profile.
    
    Args:
        profile_points: List of [x, y] coordinates defining the profile
        extrude_height: Height to extrude the profile
    
    Returns:
        Success message with entity information
    """
    try:
        acad = get_autocad_instance()
        entity_id = acad.extrude_profile(profile_points, extrude_height)
        return f"Extruded solid created successfully with entity ID: {entity_id}"
    except Exception as e:
        logger.error(f"Error creating extrusion: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to create extrusion: {str(e)}")

@mcp.tool()
def revolve_profile(profile_points: List[List[float]], axis_start: List[float], axis_end: List[float], angle: float = 360.0) -> str:
    """
    Create 3D revolved solid from 2D profile around an axis.
    
    Args:
        profile_points: List of [x, y] coordinates defining the profile
        axis_start: [x, y, z] coordinates for revolution axis start
        axis_end: [x, y, z] coordinates for revolution axis end
        angle: Revolution angle in degrees (default: 360)
    
    Returns:
        Success message with entity information
    """
    try:
        acad = get_autocad_instance()
        entity_id = acad.revolve_profile(profile_points, axis_start, axis_end, angle)
        return f"Revolved solid created successfully with entity ID: {entity_id}"
    except Exception as e:
        logger.error(f"Error creating revolution: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to create revolution: {str(e)}")

@mcp.tool()
def boolean_union(entity_ids: List[int]) -> str:
    """
    Combine multiple solids into a single solid using boolean union.
    
    Args:
        entity_ids: List of entity IDs to combine
    
    Returns:
        Success message with resulting entity information
    """
    try:
        acad = get_autocad_instance()
        result_id = acad.boolean_union(entity_ids)
        return f"Boolean union completed successfully. Result entity ID: {result_id}"
    except Exception as e:
        logger.error(f"Error performing boolean union: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to perform boolean union: {str(e)}")

@mcp.tool()
def boolean_subtract(target_id: int, subtract_ids: List[int]) -> str:
    """
    Subtract solids from a target solid using boolean subtraction.
    
    Args:
        target_id: Entity ID of the target solid
        subtract_ids: List of entity IDs to subtract from target
    
    Returns:
        Success message with resulting entity information
    """
    try:
        acad = get_autocad_instance()
        result_id = acad.boolean_subtract(target_id, subtract_ids)
        return f"Boolean subtraction completed successfully. Result entity ID: {result_id}"
    except Exception as e:
        logger.error(f"Error performing boolean subtraction: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to perform boolean subtraction: {str(e)}")

@mcp.tool()
def create_3d_mesh(m_size: int, n_size: int, coordinates: List[List[float]]) -> str:
    """
    Create a 3D rectangular mesh surface.
    
    Args:
        m_size: Number of vertices in M direction
        n_size: Number of vertices in N direction
        coordinates: List of [x, y, z] coordinates for mesh vertices
    
    Returns:
        Success message with entity information
    """
    try:
        acad = get_autocad_instance()
        entity_id = acad.create_3d_mesh(m_size, n_size, coordinates)
        return f"3D mesh created successfully with entity ID: {entity_id}"
    except Exception as e:
        logger.error(f"Error creating 3D mesh: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to create 3D mesh: {str(e)}")

@mcp.tool()
def unfold_surface(entity_id: int, tolerance: float = 0.01, algorithm: str = "lscm") -> str:
    """
    Unfold a 3D surface into a 2D pattern with manufacturing data.
    
    Args:
        entity_id: ID of the 3D surface to unfold
        tolerance: Distortion tolerance (default: 0.01)
        algorithm: Unfolding algorithm ("lscm", "geodesic", or "simple")
    
    Returns:
        JSON string with unfolding results including pattern data and fold lines
    """
    try:
        acad = get_autocad_instance()
        result = acad.unfold_surface_advanced(entity_id, algorithm, tolerance, generate_fold_lines=True)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error unfolding surface: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to unfold surface: {str(e)}")

@mcp.tool()
def add_linear_dimension(start_point: List[float], end_point: List[float], dimension_line_point: List[float]) -> str:
    """
    Add a linear dimension to the drawing.
    
    Args:
        start_point: [x, y, z] coordinates for dimension start
        end_point: [x, y, z] coordinates for dimension end
        dimension_line_point: [x, y, z] coordinates for dimension line position
    
    Returns:
        Success message with dimension information
    """
    try:
        acad = get_autocad_instance()
        dim_id = acad.add_linear_dimension(start_point, end_point, dimension_line_point)
        return f"Linear dimension added successfully with ID: {dim_id}"
    except Exception as e:
        logger.error(f"Error adding linear dimension: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to add linear dimension: {str(e)}")

@mcp.tool()
def optimize_pattern_nesting(patterns: List[Dict], material_sheets: List[Dict], algorithm: str = "best_fit_decreasing") -> str:
    """
    Optimize pattern nesting for material efficiency.
    
    Args:
        patterns: List of pattern dictionaries with dimensions
        material_sheets: List of material sheet dictionaries  
        algorithm: Nesting algorithm to use
    
    Returns:
        JSON string with optimization results and material utilization
    """
    try:
        acad = get_autocad_instance()
        result = acad.optimize_pattern_nesting(patterns, material_sheets, algorithm)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error optimizing pattern nesting: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to optimize pattern nesting: {str(e)}")

@mcp.tool()
def batch_surface_unfold(entity_ids: List[int], algorithm: str = "lscm", create_manufacturing_drawings: bool = True) -> str:
    """
    Batch process multiple surfaces for unfolding with full manufacturing workflow.
    
    Args:
        entity_ids: List of surface entity IDs to process
        algorithm: Unfolding algorithm to use
        create_manufacturing_drawings: Whether to create manufacturing drawings
    
    Returns:
        JSON string with batch processing results
    """
    try:
        acad = get_autocad_instance()
        result = acad.batch_surface_unfold(entity_ids, algorithm, create_manufacturing_drawings)
        return json.dumps(result, indent=2)
    except Exception as e:
        logger.error(f"Error in batch surface unfolding: {e}")
        raise McpError("INTERNAL_ERROR", f"Failed to batch unfold surfaces: {str(e)}")

@mcp.resource("autocad://status")  
def get_autocad_status() -> str:
    """Get current AutoCAD connection status and drawing information."""
    try:
        acad = get_autocad_instance()
        status = acad.get_status()
        return json.dumps(status, indent=2)
    except Exception as e:
        return json.dumps({"status": "disconnected", "error": str(e)})

@mcp.resource("autocad://entities")
def list_entities() -> str:
    """List all entities in the current AutoCAD drawing."""
    try:
        acad = get_autocad_instance()
        entities = acad.list_entities()
        return json.dumps(entities, indent=2)
    except Exception as e:
        return json.dumps({"error": str(e)})

@mcp.prompt("manufacturing-workflow")
def manufacturing_workflow_prompt(surface_description: str) -> str:
    """Generate a complete manufacturing workflow for a described surface."""
    return f"""
    Create a complete manufacturing workflow for: {surface_description}

    Please follow these steps:
    1. Create the 3D surface using appropriate AutoCAD tools
    2. Unfold the surface using LSCM algorithm with <0.1% distortion tolerance
    3. Add manufacturing dimensions and annotations
    4. Optimize material nesting for efficiency
    5. Generate fold lines and manufacturing notes

    Use the available AutoCAD MCP tools to execute each step and provide detailed results.
    """

if __name__ == "__main__":
    # Run the MCP server
    mcp.run()