"""
Mesh utilities for AutoCAD integration and triangle mesh processing.
"""

import numpy as np
import logging
from typing import List, Tuple, Dict, Any, Optional

logger = logging.getLogger(__name__)


def extract_triangle_mesh(acad_entity) -> Tuple[np.ndarray, np.ndarray]:
    """
    Extract triangle mesh data from AutoCAD PolygonMesh entity.
    
    Args:
        acad_entity: AutoCAD PolygonMesh entity
        
    Returns:
        Tuple of (vertices, triangles) as numpy arrays
    """
    try:
        logger.info(f"Extracting triangle mesh from AutoCAD entity {acad_entity.ObjectID}")
        
        # Get coordinates from AutoCAD entity
        coordinates = acad_entity.Coordinates
        
        # Convert coordinates tuple to numpy array
        coords_array = np.array(coordinates).reshape(-1, 3)
        n_vertices = len(coords_array)
        
        logger.info(f"Extracted {n_vertices} vertices from AutoCAD mesh")
        
        # Determine mesh dimensions by analyzing coordinate patterns
        vertices = []
        for i in range(0, len(coordinates), 3):
            vertices.append([coordinates[i], coordinates[i+1], coordinates[i+2]])
        
        vertices = np.array(vertices)
        
        # Find unique X and Y coordinates to determine grid size
        x_coords = sorted(set(v[0] for v in vertices))
        y_coords = sorted(set(v[1] for v in vertices))
        
        m_size = len(x_coords)  # Number of unique X positions
        n_size = len(y_coords)  # Number of unique Y positions
        
        logger.info(f"Detected {m_size}x{n_size} grid mesh")
        
        # Generate triangle connectivity from mesh grid
        triangles = []
        
        # Create mapping from (x,y) coordinates to vertex indices
        coord_to_index = {}
        for i, vertex in enumerate(vertices):
            key = (vertex[0], vertex[1])
            coord_to_index[key] = i
        
        # Generate triangles from grid structure
        for i in range(m_size - 1):
            for j in range(n_size - 1):
                # Get the four corners of the grid cell
                x0, x1 = x_coords[i], x_coords[i + 1]
                y0, y1 = y_coords[j], y_coords[j + 1]
                
                # Find vertex indices for the four corners
                try:
                    v00 = coord_to_index[(x0, y0)]  # Bottom-left
                    v10 = coord_to_index[(x1, y0)]  # Bottom-right
                    v01 = coord_to_index[(x0, y1)]  # Top-left
                    v11 = coord_to_index[(x1, y1)]  # Top-right
                    
                    # Create two triangles per quad (split diagonal)
                    triangles.append([v00, v10, v01])  # Triangle 1
                    triangles.append([v10, v11, v01])  # Triangle 2
                    
                except KeyError as e:
                    logger.warning(f"Could not find vertex for coordinates {e}")
                    continue
        
        triangles = np.array(triangles)
        
        logger.info(f"Generated {len(triangles)} triangles from mesh grid")
        
        return vertices, triangles
        
    except Exception as e:
        logger.error(f"Failed to extract triangle mesh: {e}")
        raise


def analyze_mesh_curvature(vertices: np.ndarray, triangles: np.ndarray) -> Dict[str, Any]:
    """
    Analyze curvature properties of a triangle mesh.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        triangles: Mx3 array of triangle indices
        
    Returns:
        Dictionary containing curvature analysis results
    """
    logger.info("Analyzing mesh curvature...")
    
    try:
        n_vertices = len(vertices)
        vertex_curvatures = np.zeros(n_vertices)
        vertex_normals = np.zeros((n_vertices, 3))
        vertex_areas = np.zeros(n_vertices)
        
        # Calculate face normals and areas
        face_normals = []
        face_areas = []
        
        for triangle in triangles:
            v0, v1, v2 = vertices[triangle]
            
            # Compute face normal and area
            edge1 = v1 - v0
            edge2 = v2 - v0
            face_normal = np.cross(edge1, edge2)
            face_area = np.linalg.norm(face_normal) / 2.0
            
            if face_area > 1e-12:
                face_normal = face_normal / (2.0 * face_area)  # Normalize
            else:
                face_normal = np.array([0, 0, 1])  # Default normal for degenerate triangles
            
            face_normals.append(face_normal)
            face_areas.append(face_area)
            
            # Accumulate vertex normals (area-weighted)
            for vertex_idx in triangle:
                vertex_normals[vertex_idx] += face_normal * face_area
                vertex_areas[vertex_idx] += face_area / 3.0  # Distribute area equally
        
        # Normalize vertex normals
        for i in range(n_vertices):
            if vertex_areas[i] > 1e-12:
                vertex_normals[i] = vertex_normals[i] / np.linalg.norm(vertex_normals[i])
        
        # Calculate mean curvature using cotangent weights (simplified)
        for i, vertex in enumerate(vertices):
            curvature_sum = 0.0
            weight_sum = 0.0
            
            # Find triangles adjacent to this vertex
            adjacent_triangles = []
            for tri_idx, triangle in enumerate(triangles):
                if i in triangle:
                    adjacent_triangles.append((tri_idx, triangle))
            
            # Calculate curvature contribution from each adjacent triangle
            for tri_idx, triangle in adjacent_triangles:
                # Find the other two vertices in the triangle
                other_vertices = [v for v in triangle if v != i]
                if len(other_vertices) != 2:
                    continue
                
                v1, v2 = vertices[other_vertices]
                
                # Simple curvature approximation using angle between edges
                edge1 = v1 - vertex
                edge2 = v2 - vertex
                
                edge1_norm = np.linalg.norm(edge1)
                edge2_norm = np.linalg.norm(edge2)
                
                if edge1_norm > 1e-12 and edge2_norm > 1e-12:
                    cos_angle = np.clip(np.dot(edge1, edge2) / (edge1_norm * edge2_norm), -1, 1)
                    angle = np.arccos(cos_angle)
                    
                    # Weight by triangle area
                    weight = face_areas[tri_idx]
                    curvature_sum += angle * weight
                    weight_sum += weight
            
            if weight_sum > 1e-12:
                vertex_curvatures[i] = curvature_sum / weight_sum
        
        # Calculate curvature statistics
        mean_curvature = np.mean(vertex_curvatures)
        max_curvature = np.max(vertex_curvatures)
        min_curvature = np.min(vertex_curvatures)
        curvature_variance = np.var(vertex_curvatures)
        
        # Classify surface type based on curvature
        if max_curvature - min_curvature < 0.1:
            surface_type = "nearly_flat"
        elif max_curvature > 2.0:
            surface_type = "highly_curved"
        else:
            surface_type = "moderately_curved"
        
        curvature_analysis = {
            'vertex_curvatures': vertex_curvatures.tolist(),
            'vertex_normals': vertex_normals.tolist(),
            'mean_curvature': mean_curvature,
            'max_curvature': max_curvature,
            'min_curvature': min_curvature,
            'curvature_variance': curvature_variance,
            'surface_type': surface_type,
            'total_surface_area': np.sum(face_areas),
            'n_vertices': n_vertices,
            'n_triangles': len(triangles)
        }
        
        logger.info(f"Curvature analysis completed: {surface_type} surface, "
                   f"mean curvature = {mean_curvature:.3f}")
        
        return curvature_analysis
        
    except Exception as e:
        logger.error(f"Curvature analysis failed: {e}")
        return {'error': str(e)}


def validate_mesh_manifold(vertices: np.ndarray, triangles: np.ndarray) -> Dict[str, Any]:
    """
    Validate that the mesh is a manifold suitable for LSCM.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        triangles: Mx3 array of triangle indices
        
    Returns:
        Dictionary containing validation results
    """
    logger.info("Validating mesh manifold properties...")
    
    try:
        n_vertices = len(vertices)
        n_triangles = len(triangles)
        
        # Check for degenerate triangles
        degenerate_triangles = []
        for i, triangle in enumerate(triangles):
            v0, v1, v2 = vertices[triangle]
            
            # Calculate triangle area
            edge1 = v1 - v0
            edge2 = v2 - v0
            area = np.linalg.norm(np.cross(edge1, edge2)) / 2.0
            
            if area < 1e-12:
                degenerate_triangles.append(i)
        
        # Check for duplicate vertices
        unique_vertices = np.unique(vertices, axis=0)
        n_unique_vertices = len(unique_vertices)
        
        # Build edge adjacency information
        edge_count = {}
        boundary_edges = []
        
        for triangle in triangles:
            for i in range(3):
                v1 = triangle[i]
                v2 = triangle[(i + 1) % 3]
                
                # Create canonical edge (smaller index first)
                edge = tuple(sorted([v1, v2]))
                
                if edge in edge_count:
                    edge_count[edge] += 1
                else:
                    edge_count[edge] = 1
        
        # Find boundary edges (appear only once)
        for edge, count in edge_count.items():
            if count == 1:
                boundary_edges.append(edge)
        
        # Check for non-manifold edges (appear more than twice)
        non_manifold_edges = [edge for edge, count in edge_count.items() if count > 2]
        
        # Calculate Euler characteristic (V - E + F)
        n_edges = len(edge_count)
        euler_characteristic = n_vertices - n_edges + n_triangles
        
        # For a closed manifold: chi = 2 - 2*genus
        # For a manifold with boundary: chi = 2 - 2*genus - boundary_components
        
        validation_result = {
            'is_manifold': len(non_manifold_edges) == 0,
            'n_vertices': n_vertices,
            'n_unique_vertices': n_unique_vertices,
            'n_triangles': n_triangles,
            'n_edges': n_edges,
            'n_boundary_edges': len(boundary_edges),
            'n_degenerate_triangles': len(degenerate_triangles),
            'n_non_manifold_edges': len(non_manifold_edges),
            'euler_characteristic': euler_characteristic,
            'has_boundary': len(boundary_edges) > 0,
            'is_closed': len(boundary_edges) == 0,
            'degenerate_triangles': degenerate_triangles,
            'non_manifold_edges': non_manifold_edges[:10],  # Limit output
            'boundary_edges': boundary_edges[:10]  # Limit output
        }
        
        # Overall assessment
        is_suitable = (validation_result['is_manifold'] and 
                      validation_result['n_degenerate_triangles'] == 0 and
                      validation_result['n_vertices'] == validation_result['n_unique_vertices'])
        
        validation_result['suitable_for_lscm'] = is_suitable
        
        if is_suitable:
            logger.info("✅ Mesh is suitable for LSCM processing")
        else:
            logger.warning("⚠️ Mesh has issues that may affect LSCM quality")
        
        return validation_result
        
    except Exception as e:
        logger.error(f"Mesh validation failed: {e}")
        return {'error': str(e), 'suitable_for_lscm': False}


def optimize_mesh_for_lscm(vertices: np.ndarray, triangles: np.ndarray, 
                          max_vertices: int = 10000) -> Tuple[np.ndarray, np.ndarray]:
    """
    Optimize mesh for LSCM processing by reducing complexity if needed.
    
    Args:
        vertices: Original vertex array
        triangles: Original triangle array  
        max_vertices: Maximum allowed vertices
        
    Returns:
        Optimized vertices and triangles arrays
    """
    if len(vertices) <= max_vertices:
        logger.info("Mesh size acceptable, no optimization needed")
        return vertices, triangles
    
    logger.info(f"Mesh too large ({len(vertices)} vertices), applying simplification...")
    
    # Simple decimation strategy - remove every nth vertex
    # In a production system, this would use sophisticated mesh decimation algorithms
    
    decimation_factor = len(vertices) / max_vertices
    keep_indices = np.arange(0, len(vertices), int(decimation_factor))
    
    # Create mapping from old to new vertex indices
    old_to_new = {old_idx: new_idx for new_idx, old_idx in enumerate(keep_indices)}
    
    # Keep only selected vertices
    optimized_vertices = vertices[keep_indices]
    
    # Update triangles to use new vertex indices
    optimized_triangles = []
    for triangle in triangles:
        new_triangle = []
        valid = True
        
        for vertex_idx in triangle:
            if vertex_idx in old_to_new:
                new_triangle.append(old_to_new[vertex_idx])
            else:
                valid = False
                break
        
        if valid and len(set(new_triangle)) == 3:  # Avoid degenerate triangles
            optimized_triangles.append(new_triangle)
    
    optimized_triangles = np.array(optimized_triangles)
    
    logger.info(f"Mesh optimized: {len(optimized_vertices)} vertices, {len(optimized_triangles)} triangles")
    
    return optimized_vertices, optimized_triangles


def generate_simple_mesh(rows: int = 5, cols: int = 5) -> Tuple[np.ndarray, np.ndarray]:
    """
    Generate a simple rectangular mesh for testing purposes.
    
    Args:
        rows: Number of rows in the mesh grid
        cols: Number of columns in the mesh grid
        
    Returns:
        Tuple of (vertices, triangles) arrays
    """
    logger.info(f"Generating simple {rows}x{cols} test mesh")
    
    # Generate grid vertices
    vertices = []
    for i in range(rows):
        for j in range(cols):
            x = float(j) / (cols - 1)
            y = float(i) / (rows - 1)
            z = 0.1 * np.sin(2 * np.pi * x) * np.sin(2 * np.pi * y)  # Small waves
            vertices.append([x, y, z])
    
    vertices = np.array(vertices)
    
    # Generate triangle connectivity
    triangles = []
    for i in range(rows - 1):
        for j in range(cols - 1):
            # Current quad vertices
            bottom_left = i * cols + j
            bottom_right = i * cols + (j + 1)
            top_left = (i + 1) * cols + j
            top_right = (i + 1) * cols + (j + 1)
            
            # Two triangles per quad
            triangles.append([bottom_left, bottom_right, top_left])
            triangles.append([bottom_right, top_right, top_left])
    
    triangles = np.array(triangles)
    
    logger.info(f"Generated mesh: {len(vertices)} vertices, {len(triangles)} triangles")
    return vertices, triangles


def validate_mesh(vertices: np.ndarray, triangles: np.ndarray) -> Dict[str, Any]:
    """
    Comprehensive mesh validation function.
    
    Args:
        vertices: Nx3 array of vertex coordinates
        triangles: Mx3 array of triangle indices
        
    Returns:
        Dictionary containing validation results and metrics
    """
    logger.info("Starting comprehensive mesh validation")
    
    validation_result = {
        'basic_checks': {},
        'manifold_validation': {},
        'geometry_metrics': {},
        'overall_status': 'unknown'
    }
    
    try:
        # Basic checks
        n_vertices = len(vertices)
        n_triangles = len(triangles)
        
        validation_result['basic_checks'] = {
            'n_vertices': n_vertices,
            'n_triangles': n_triangles,
            'vertices_shape_valid': vertices.shape[1] == 3,
            'triangles_shape_valid': triangles.shape[1] == 3,
            'indices_in_range': np.all(triangles >= 0) and np.all(triangles < n_vertices),
            'no_empty_mesh': n_vertices > 0 and n_triangles > 0
        }
        
        # Manifold validation
        validation_result['manifold_validation'] = validate_mesh_manifold(vertices, triangles)
        
        # Geometry metrics
        if n_vertices > 0 and n_triangles > 0:
            # Bounding box
            bbox_min = np.min(vertices, axis=0)
            bbox_max = np.max(vertices, axis=0)
            bbox_size = bbox_max - bbox_min
            
            # Triangle areas
            triangle_areas = []
            for triangle in triangles:
                v0, v1, v2 = vertices[triangle]
                edge1 = v1 - v0
                edge2 = v2 - v0
                area = np.linalg.norm(np.cross(edge1, edge2)) / 2.0
                triangle_areas.append(area)
            
            triangle_areas = np.array(triangle_areas)
            
            validation_result['geometry_metrics'] = {
                'bbox_min': bbox_min.tolist(),
                'bbox_max': bbox_max.tolist(),
                'bbox_size': bbox_size.tolist(),
                'total_surface_area': np.sum(triangle_areas),
                'min_triangle_area': np.min(triangle_areas),
                'max_triangle_area': np.max(triangle_areas),
                'mean_triangle_area': np.mean(triangle_areas),
                'area_std': np.std(triangle_areas)
            }
        
        # Overall assessment
        basic_valid = all(validation_result['basic_checks'].values())
        manifold_suitable = validation_result['manifold_validation'].get('suitable_for_lscm', False)
        
        if basic_valid and manifold_suitable:
            validation_result['overall_status'] = 'valid'
            logger.info("✅ Mesh passed comprehensive validation")
        elif basic_valid:
            validation_result['overall_status'] = 'basic_valid'
            logger.warning("⚠️ Mesh has basic validity but manifold issues")
        else:
            validation_result['overall_status'] = 'invalid'
            logger.error("❌ Mesh failed basic validation checks")
        
        return validation_result
        
    except Exception as e:
        logger.error(f"Mesh validation failed with error: {e}")
        validation_result['error'] = str(e)
        validation_result['overall_status'] = 'error'
        return validation_result