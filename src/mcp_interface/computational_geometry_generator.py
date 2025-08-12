"""
Computational Geometry Algorithm Generator for MCP Interface

Provides advanced geometric operations and spatial analysis capabilities.
"""

import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from scipy.spatial import ConvexHull, Delaunay
from src.mcp_interface.algorithm_interface import (
    AbstractAlgorithmGenerator, 
    AlgorithmSpecification, 
    AlgorithmCategory
)

class ComputationalGeometryGenerator(AbstractAlgorithmGenerator):
    """
    Specialized generator for computational geometry algorithms.
    
    Provides capabilities for advanced geometric operations:
    - Convex hull computation
    - Spatial partitioning
    - Polygon intersection
    - Point-in-polygon tests
    """
    
    def generate_algorithm(
        self, 
        problem_description: str, 
        constraints: Optional[Dict[str, Any]] = None
    ) -> AlgorithmSpecification:
        """
        Generate a computational geometry algorithm specification.
        
        Args:
            problem_description: Natural language description of geometric operation
            constraints: Optional geometric constraints
        
        Returns:
            Fully specified computational geometry algorithm
        """
        # Default algorithm specification
        base_spec = AlgorithmSpecification(
            name="Advanced Computational Geometry Operations",
            description="Sophisticated geometric analysis and transformation",
            category=AlgorithmCategory.COMPUTATIONAL_GEOMETRY,
            inputs={
                "points": np.ndarray,
                "operation_type": str,
                "additional_geometry": Optional[np.ndarray]
            },
            outputs={
                "result": Any,
                "metadata": dict
            }
        )
        
        # Customize based on problem description
        if "convex hull" in problem_description.lower():
            base_spec.description += " with convex hull computation"
        
        if "polygon" in problem_description.lower():
            base_spec.description += " and polygon operations"
        
        return base_spec
    
    def execute_algorithm(
        self, 
        algorithm: AlgorithmSpecification, 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the computational geometry algorithm.
        
        Args:
            algorithm: Algorithm specification to execute
            input_data: Input data matching the algorithm's specification
        
        Returns:
            Geometric operation results
        """
        # Validate inputs
        for key, expected_type in algorithm.inputs.items():
            if key not in input_data and key != 'additional_geometry':
                raise ValueError(f"Missing required input: {key}")
            if (key in input_data and 
                not isinstance(input_data[key], expected_type)):
                raise TypeError(f"Invalid type for {key}")
        
        points = input_data['points']
        operation_type = input_data.get('operation_type', 'convex_hull')
        additional_geometry = input_data.get('additional_geometry')
        
        # Computational geometry operations
        if operation_type == 'convex_hull':
            return self._compute_convex_hull(points)
        
        elif operation_type == 'delaunay_triangulation':
            return self._delaunay_triangulation(points)
        
        elif operation_type == 'point_in_polygon':
            if additional_geometry is None:
                raise ValueError("Additional geometry required for point-in-polygon test")
            return self._point_in_polygon(points, additional_geometry)
        
        elif operation_type == 'polygon_intersection':
            if additional_geometry is None:
                raise ValueError("Additional geometry required for polygon intersection")
            return self._polygon_intersection(points, additional_geometry)
        
        else:
            raise ValueError(f"Unsupported operation type: {operation_type}")
    
    def _compute_convex_hull(self, points: np.ndarray) -> Dict[str, Any]:
        """
        Compute the convex hull of a set of points.
        
        Args:
            points: Input points
        
        Returns:
            Convex hull computation results
        """
        hull = ConvexHull(points)
        
        return {
            'result': points[hull.vertices],
            'metadata': {
                'hull_vertices': hull.vertices.tolist(),
                'hull_area': hull.area,
                'hull_volume': hull.volume
            }
        }
    
    def _delaunay_triangulation(self, points: np.ndarray) -> Dict[str, Any]:
        """
        Compute Delaunay triangulation for a set of points.
        
        Args:
            points: Input points
        
        Returns:
            Delaunay triangulation results
        """
        triangulation = Delaunay(points)
        
        return {
            'result': {
                'triangles': triangulation.simplices,
                'neighbors': triangulation.neighbors
            },
            'metadata': {
                'point_count': len(points),
                'triangle_count': len(triangulation.simplices)
            }
        }
    
    def _point_in_polygon(
        self, 
        points: np.ndarray, 
        polygon: np.ndarray
    ) -> Dict[str, Any]:
        """
        Determine if points are inside a given polygon.
        
        Args:
            points: Points to test
            polygon: Polygon vertices
        
        Returns:
            Point-in-polygon test results
        """
        def point_inside_polygon(point, poly):
            """
            Ray casting algorithm for point-in-polygon test.
            """
            n = len(poly)
            inside = False
            p1x, p1y = poly[0]
            for i in range(n + 1):
                p2x, p2y = poly[i % n]
                if points[point][1] > min(p1y, p2y):
                    if points[point][1] <= max(p1y, p2y):
                        if points[point][0] <= max(p1x, p2x):
                            if p1y != p2y:
                                xinters = (points[point][1] - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                            if p1x == p2x or points[point][0] <= xinters:
                                inside = not inside
                p1x, p1y = p2x, p2y
            return inside
        
        # Test each point against the polygon
        results = [point_inside_polygon(i, polygon) for i in range(len(points))]
        
        return {
            'result': results,
            'metadata': {
                'points_tested': len(points),
                'points_inside': sum(results)
            }
        }
    
    def _polygon_intersection(
        self, 
        polygon1: np.ndarray, 
        polygon2: np.ndarray
    ) -> Dict[str, Any]:
        """
        Compute intersection of two polygons.
        
        Args:
            polygon1: First polygon vertices
            polygon2: Second polygon vertices
        
        Returns:
            Polygon intersection results
        """
        def cross_product(o, a, b):
            """Compute cross product to determine orientation."""
            return (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
        
        def segment_intersection(p1, p2, p3, p4):
            """
            Determine if line segments (p1,p2) and (p3,p4) intersect.
            """
            o1 = cross_product(p1, p2, p3)
            o2 = cross_product(p1, p2, p4)
            o3 = cross_product(p3, p4, p1)
            o4 = cross_product(p3, p4, p2)
            
            if o1 * o2 < 0 and o3 * o4 < 0:
                # Compute intersection point
                x1, y1 = p1
                x2, y2 = p2
                x3, y3 = p3
                x4, y4 = p4
                
                px = ( (x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4) ) / \
                     ( (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) )
                py = ( (x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4) ) / \
                     ( (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4) )
                
                return (px, py)
            return None
        
        # Find intersection points
        intersections = []
        for i in range(len(polygon1)):
            for j in range(len(polygon2)):
                p1, p2 = polygon1[i], polygon1[(i+1) % len(polygon1)]
                p3, p4 = polygon2[j], polygon2[(j+1) % len(polygon2)]
                
                inter_point = segment_intersection(p1, p2, p3, p4)
                if inter_point:
                    intersections.append(inter_point)
        
        return {
            'result': np.array(intersections),
            'metadata': {
                'intersection_points': len(intersections),
                'polygon1_vertices': len(polygon1),
                'polygon2_vertices': len(polygon2)
            }
        }
    
    def validate_algorithm(
        self, 
        algorithm: AlgorithmSpecification
    ) -> bool:
        """
        Validate the computational geometry algorithm specification.
        
        Args:
            algorithm: Algorithm specification to validate
        
        Returns:
            Boolean indicating algorithm validity
        """
        # Check category
        if algorithm.category != AlgorithmCategory.COMPUTATIONAL_GEOMETRY:
            return False
        
        # Check input specifications
        required_inputs = [
            "points", 
            "operation_type"
        ]
        
        for input_name in required_inputs:
            if input_name not in algorithm.inputs:
                return False
        
        return True

# Example usage demonstration
def _example_usage():
    """
    Demonstrates basic usage of the Computational Geometry Generator.
    """
    generator = ComputationalGeometryGenerator()
    
    # Example problem description
    problem = "Compute convex hull and polygon operations"
    
    # Generate algorithm specification
    algo_spec = generator.generate_algorithm(problem)
    
    # Prepare example input data for convex hull
    points = np.array([
        [0, 0],
        [1, 0],
        [1, 1],
        [0, 1],
        [0.5, 0.5]
    ])
    
    # Execute convex hull algorithm
    convex_hull_result = generator.execute_algorithm(algo_spec, {
        'points': points,
        'operation_type': 'convex_hull'
    })
    
    # Execute Delaunay triangulation
    delaunay_result = generator.execute_algorithm(algo_spec, {
        'points': points,
        'operation_type': 'delaunay_triangulation'
    })
    
    # Prepare polygons for polygon operations
    polygon1 = np.array([
        [0, 0],
        [2, 0],
        [2, 2],
        [0, 2]
    ])
    polygon2 = np.array([
        [1, 1],
        [3, 1],
        [3, 3],
        [1, 3]
    ])
    
    # Execute polygon intersection
    intersection_result = generator.execute_algorithm(algo_spec, {
        'points': polygon1,
        'operation_type': 'polygon_intersection',
        'additional_geometry': polygon2
    })
    
    print("Convex Hull Result:")
    print(f"Hull Vertices: {convex_hull_result['result']}")
    print(f"Hull Area: {convex_hull_result['metadata']['hull_area']}")
    
    print("\nDelaunay Triangulation Result:")
    print(f"Triangle Count: {delaunay_result['metadata']['triangle_count']}")
    
    print("\nPolygon Intersection Result:")
    print(f"Intersection Points: {intersection_result['result']}")
    print(f"Point Count: {intersection_result['metadata']['intersection_points']}")

if __name__ == "__main__":
    _example_usage()