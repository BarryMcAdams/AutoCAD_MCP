"""
Pattern Generation Algorithm Generator for MCP Interface

Provides advanced capabilities for geometric pattern generation,
material nesting, and optimization strategies.
"""

import numpy as np
from typing import Dict, Any, Optional, List, Tuple
from scipy.spatial import ConvexHull
import itertools

from src.mcp_interface.algorithm_interface import (
    AbstractAlgorithmGenerator, 
    AlgorithmSpecification, 
    AlgorithmCategory
)

class PatternGenerationGenerator(AbstractAlgorithmGenerator):
    """
    Specialized generator for pattern generation and optimization algorithms.
    
    Provides capabilities for:
    - Material nesting optimization
    - Geometric pattern generation
    - Cutting path optimization
    - Waste minimization strategies
    """
    
    def generate_algorithm(
        self, 
        problem_description: str, 
        constraints: Optional[Dict[str, Any]] = None
    ) -> AlgorithmSpecification:
        """
        Generate a pattern generation algorithm specification.
        
        Args:
            problem_description: Natural language description of pattern generation requirements
            constraints: Optional generation constraints
        
        Returns:
            Fully specified pattern generation algorithm
        """
        # Default algorithm specification
        base_spec = AlgorithmSpecification(
            name="Advanced Pattern Generation and Optimization",
            description="Sophisticated geometric pattern and nesting algorithms",
            category=AlgorithmCategory.PATTERN_GENERATION,
            inputs={
                "shapes": List[np.ndarray],
                "optimization_type": str,
                "material_constraints": Optional[Dict[str, Any]]
            },
            outputs={
                "optimized_layout": List[np.ndarray],
                "waste_analysis": Dict[str, float],
                "cutting_instructions": List[Dict[str, Any]]
            }
        )
        
        # Customize based on problem description
        if "material nesting" in problem_description.lower():
            base_spec.description += " with material nesting optimization"
        
        if "laser cutting" in problem_description.lower():
            base_spec.description += " for laser cutting efficiency"
        
        return base_spec
    
    def execute_algorithm(
        self, 
        algorithm: AlgorithmSpecification, 
        input_data: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Execute the pattern generation algorithm.
        
        Args:
            algorithm: Algorithm specification to execute
            input_data: Input data matching the algorithm's specification
        
        Returns:
            Pattern generation and optimization results
        """
        # Validate inputs
        for key, expected_type in algorithm.inputs.items():
            if key not in input_data and key != 'material_constraints':
                raise ValueError(f"Missing required input: {key}")
            if (key in input_data and 
                not isinstance(input_data[key], expected_type)):
                raise TypeError(f"Invalid type for {key}")
        
        shapes = input_data['shapes']
        optimization_type = input_data.get('optimization_type', 'material_nesting')
        material_constraints = input_data.get('material_constraints', {})
        
        # Pattern generation operations
        if optimization_type == 'material_nesting':
            return self._optimize_material_nesting(shapes, material_constraints)
        
        elif optimization_type == 'cutting_path':
            return self._optimize_cutting_path(shapes, material_constraints)
        
        elif optimization_type == 'geometric_packing':
            return self._geometric_packing(shapes, material_constraints)
        
        else:
            raise ValueError(f"Unsupported optimization type: {optimization_type}")
    
    def _optimize_material_nesting(
        self, 
        shapes: List[np.ndarray], 
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize material nesting using a genetic algorithm approach.
        
        Args:
            shapes: List of shape geometries
            constraints: Material and cutting constraints
        
        Returns:
            Optimized material nesting results
        """
        # Material sheet dimensions (default or from constraints)
        sheet_width = constraints.get('sheet_width', 1000)
        sheet_height = constraints.get('sheet_height', 1000)
        
        # Compute bounding boxes for shapes
        shape_bounds = [self._compute_bounding_box(shape) for shape in shapes]
        
        # Initial population of random arrangements
        population_size = 50
        population = self._generate_initial_population(shape_bounds, sheet_width, sheet_height, population_size)
        
        # Genetic algorithm optimization
        best_layout = None
        best_fitness = float('inf')
        
        for generation in range(100):
            # Evaluate fitness of each layout
            population_fitness = [self._compute_layout_fitness(layout, sheet_width, sheet_height) for layout in population]
            
            # Select best layouts
            best_index = np.argmin(population_fitness)
            current_best_fitness = population_fitness[best_index]
            
            if current_best_fitness < best_fitness:
                best_fitness = current_best_fitness
                best_layout = population[best_index]
            
            # Generate new population through crossover and mutation
            population = self._evolve_population(population, population_fitness)
        
        # Compute waste analysis
        waste_analysis = self._analyze_waste(best_layout, sheet_width, sheet_height)
        
        return {
            'optimized_layout': best_layout,
            'waste_analysis': waste_analysis,
            'cutting_instructions': self._generate_cutting_instructions(best_layout)
        }
    
    def _optimize_cutting_path(
        self, 
        shapes: List[np.ndarray], 
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Optimize cutting path to minimize tool travel and wear.
        
        Args:
            shapes: List of shape geometries
            constraints: Cutting constraints
        
        Returns:
            Optimized cutting path results
        """
        # Compute centroids of shapes
        centroids = [np.mean(shape, axis=0) for shape in shapes]
        
        # Nearest neighbor algorithm for path optimization
        path_order = [0]
        unvisited = set(range(1, len(centroids)))
        
        while unvisited:
            current = path_order[-1]
            nearest = min(unvisited, key=lambda x: np.linalg.norm(centroids[current] - centroids[x]))
            path_order.append(nearest)
            unvisited.remove(nearest)
        
        return {
            'optimized_layout': [shapes[i] for i in path_order],
            'waste_analysis': {
                'total_path_length': self._compute_path_length(centroids, path_order)
            },
            'cutting_instructions': [
                {'shape_index': i, 'cutting_order': order} 
                for order, i in enumerate(path_order)
            ]
        }
    
    def _geometric_packing(
        self, 
        shapes: List[np.ndarray], 
        constraints: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Perform geometric packing with advanced placement strategies.
        
        Args:
            shapes: List of shape geometries
            constraints: Packing constraints
        
        Returns:
            Geometric packing results
        """
        # Sort shapes by area (largest first)
        sorted_shapes = sorted(enumerate(shapes), key=lambda x: self._compute_shape_area(x[1]), reverse=True)
        
        # Initialize packing grid
        grid_width = constraints.get('grid_width', 1000)
        grid_height = constraints.get('grid_height', 1000)
        grid = np.zeros((grid_height, grid_width), dtype=bool)
        
        packed_shapes = []
        placement_info = []
        
        for idx, shape in sorted_shapes:
            placed = False
            for rotation in [0, 90, 180, 270]:
                rotated_shape = self._rotate_shape(shape, rotation)
                placement = self._find_shape_placement(rotated_shape, grid)
                
                if placement:
                    x, y = placement
                    self._update_grid(grid, rotated_shape, x, y)
                    packed_shapes.append(rotated_shape)
                    placement_info.append({
                        'original_shape_index': idx,
                        'rotation': rotation,
                        'placement': (x, y)
                    })
                    placed = True
                    break
            
            if not placed:
                # Shape could not be packed
                placement_info.append({
                    'original_shape_index': idx,
                    'packed': False
                })
        
        return {
            'optimized_layout': packed_shapes,
            'waste_analysis': self._analyze_packing_efficiency(grid),
            'cutting_instructions': placement_info
        }
    
    def _compute_bounding_box(self, shape: np.ndarray) -> Tuple[float, float, float, float]:
        """Compute bounding box of a shape."""
        return (
            np.min(shape[:, 0]), np.min(shape[:, 1]),
            np.max(shape[:, 0]), np.max(shape[:, 1])
        )
    
    def _compute_shape_area(self, shape: np.ndarray) -> float:
        """Compute area of a shape using convex hull."""
        hull = ConvexHull(shape)
        return hull.area
    
    def _rotate_shape(self, shape: np.ndarray, angle: int) -> np.ndarray:
        """Rotate shape by specified angle."""
        # Simple rotation matrix
        if angle == 0:
            return shape
        elif angle == 90:
            rotation_matrix = np.array([[0, -1], [1, 0]])
        elif angle == 180:
            rotation_matrix = np.array([[-1, 0], [0, -1]])
        elif angle == 270:
            rotation_matrix = np.array([[0, 1], [-1, 0]])
        
        return np.dot(shape, rotation_matrix)
    
    def validate_algorithm(
        self, 
        algorithm: AlgorithmSpecification
    ) -> bool:
        """
        Validate the pattern generation algorithm specification.
        
        Args:
            algorithm: Algorithm specification to validate
        
        Returns:
            Boolean indicating algorithm validity
        """
        # Check category
        if algorithm.category != AlgorithmCategory.PATTERN_GENERATION:
            return False
        
        # Check input specifications
        required_inputs = [
            "shapes", 
            "optimization_type"
        ]
        
        for input_name in required_inputs:
            if input_name not in algorithm.inputs:
                return False
        
        return True
    
    # Helper methods would be implemented here (abbreviated for brevity)
    def _generate_initial_population(self, shape_bounds, sheet_width, sheet_height, population_size):
        """
        Generate initial population of random shape arrangements.
        
        Args:
            shape_bounds: List of bounding box tuples for each shape
            sheet_width: Width of material sheet
            sheet_height: Height of material sheet
            population_size: Number of layouts to generate
        
        Returns:
            List of layout configurations
        """
        population = []
        
        for _ in range(population_size):
            layout = []
            for bounds in shape_bounds:
                min_x, min_y, max_x, max_y = bounds
                shape_width = max_x - min_x
                shape_height = max_y - min_y
                
                # Random placement within sheet bounds
                x = np.random.uniform(0, max(0, sheet_width - shape_width))
                y = np.random.uniform(0, max(0, sheet_height - shape_height))
                rotation = np.random.choice([0, 90, 180, 270])
                
                layout.append({
                    'position': (x, y),
                    'rotation': rotation,
                    'bounds': bounds
                })
            
            population.append(layout)
        
        return population
    
    def _compute_layout_fitness(self, layout, sheet_width, sheet_height):
        """
        Compute fitness score for a layout (lower is better).
        
        Args:
            layout: Layout configuration
            sheet_width: Width of material sheet
            sheet_height: Height of material sheet
        
        Returns:
            Fitness score (lower values indicate better layouts)
        """
        penalty = 0.0
        
        # Check for shapes going out of bounds
        for shape_info in layout:
            x, y = shape_info['position']
            bounds = shape_info['bounds']
            min_x, min_y, max_x, max_y = bounds
            
            # Apply rotation to bounds
            if shape_info['rotation'] in [90, 270]:
                shape_width = max_y - min_y
                shape_height = max_x - min_x
            else:
                shape_width = max_x - min_x
                shape_height = max_y - min_y
            
            # Penalty for out-of-bounds placement
            if x + shape_width > sheet_width:
                penalty += (x + shape_width - sheet_width) ** 2
            if y + shape_height > sheet_height:
                penalty += (y + shape_height - sheet_height) ** 2
            if x < 0:
                penalty += x ** 2
            if y < 0:
                penalty += y ** 2
        
        # Check for overlaps between shapes
        for i, shape1 in enumerate(layout):
            for j, shape2 in enumerate(layout):
                if i >= j:
                    continue
                
                # Simplified overlap detection using bounding boxes
                x1, y1 = shape1['position']
                x2, y2 = shape2['position']
                
                bounds1 = shape1['bounds']
                bounds2 = shape2['bounds']
                
                # Apply rotation to get actual dimensions
                if shape1['rotation'] in [90, 270]:
                    w1, h1 = bounds1[3] - bounds1[1], bounds1[2] - bounds1[0]
                else:
                    w1, h1 = bounds1[2] - bounds1[0], bounds1[3] - bounds1[1]
                
                if shape2['rotation'] in [90, 270]:
                    w2, h2 = bounds2[3] - bounds2[1], bounds2[2] - bounds2[0]
                else:
                    w2, h2 = bounds2[2] - bounds2[0], bounds2[3] - bounds2[1]
                
                # Check for overlap
                if (x1 < x2 + w2 and x1 + w1 > x2 and
                    y1 < y2 + h2 and y1 + h1 > y2):
                    # Calculate overlap area
                    overlap_x = min(x1 + w1, x2 + w2) - max(x1, x2)
                    overlap_y = min(y1 + h1, y2 + h2) - max(y1, y2)
                    penalty += overlap_x * overlap_y * 1000  # High penalty for overlaps
        
        # Calculate material utilization (higher utilization = lower penalty)
        total_shape_area = sum([
            (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
            for shape_info in layout
            for bounds in [shape_info['bounds']]
        ])
        sheet_area = sheet_width * sheet_height
        utilization = total_shape_area / sheet_area if sheet_area > 0 else 0
        waste_penalty = (1 - utilization) * 100  # Penalty for low utilization
        
        return penalty + waste_penalty
    
    def _evolve_population(self, population, fitness_scores):
        """
        Evolve population using genetic algorithm operators.
        
        Args:
            population: Current population of layouts
            fitness_scores: Fitness scores for each layout
        
        Returns:
            New evolved population
        """
        new_population = []
        population_size = len(population)
        
        # Select top 20% as elite
        elite_count = max(1, population_size // 5)
        sorted_indices = np.argsort(fitness_scores)
        elite_indices = sorted_indices[:elite_count]
        
        # Add elite individuals to new population
        for idx in elite_indices:
            new_population.append(population[idx])
        
        # Generate rest through crossover and mutation
        while len(new_population) < population_size:
            # Tournament selection
            parent1_idx = self._tournament_selection(population, fitness_scores)
            parent2_idx = self._tournament_selection(population, fitness_scores)
            
            # Crossover
            child = self._crossover(population[parent1_idx], population[parent2_idx])
            
            # Mutation
            child = self._mutate(child)
            
            new_population.append(child)
        
        return new_population[:population_size]
    
    def _tournament_selection(self, population, fitness_scores, tournament_size=3):
        """Select individual using tournament selection."""
        tournament_indices = np.random.choice(len(population), tournament_size, replace=False)
        tournament_fitness = [fitness_scores[i] for i in tournament_indices]
        winner_idx = tournament_indices[np.argmin(tournament_fitness)]
        return winner_idx
    
    def _crossover(self, parent1, parent2):
        """Perform crossover between two parent layouts."""
        child = []
        for i in range(len(parent1)):
            # Randomly choose gene from either parent
            if np.random.random() < 0.5:
                child.append(parent1[i].copy())
            else:
                child.append(parent2[i].copy())
        return child
    
    def _mutate(self, layout, mutation_rate=0.1):
        """Apply mutation to a layout."""
        mutated_layout = []
        for shape_info in layout:
            mutated_shape = shape_info.copy()
            
            # Randomly mutate position or rotation
            if np.random.random() < mutation_rate:
                # Mutate position
                x, y = mutated_shape['position']
                x += np.random.normal(0, 10)  # Small random displacement
                y += np.random.normal(0, 10)
                mutated_shape['position'] = (max(0, x), max(0, y))
            
            if np.random.random() < mutation_rate:
                # Mutate rotation
                mutated_shape['rotation'] = np.random.choice([0, 90, 180, 270])
            
            mutated_layout.append(mutated_shape)
        
        return mutated_layout
    
    def _analyze_waste(self, layout, sheet_width, sheet_height):
        """
        Analyze waste and material utilization for a layout.
        
        Args:
            layout: Layout configuration
            sheet_width: Width of material sheet
            sheet_height: Height of material sheet
        
        Returns:
            Dictionary containing waste analysis metrics
        """
        if not layout:
            return {
                'material_utilization': 0.0,
                'waste_percentage': 100.0,
                'total_shape_area': 0.0,
                'sheet_area': sheet_width * sheet_height,
                'waste_area': sheet_width * sheet_height
            }
        
        # Calculate total area of shapes
        total_shape_area = 0.0
        for shape_info in layout:
            bounds = shape_info['bounds']
            shape_area = (bounds[2] - bounds[0]) * (bounds[3] - bounds[1])
            total_shape_area += shape_area
        
        # Calculate sheet area
        sheet_area = sheet_width * sheet_height
        
        # Calculate waste metrics
        waste_area = sheet_area - total_shape_area
        waste_percentage = (waste_area / sheet_area) * 100 if sheet_area > 0 else 100
        material_utilization = (total_shape_area / sheet_area) * 100 if sheet_area > 0 else 0
        
        # Calculate bounding box efficiency
        if layout:
            all_x = []
            all_y = []
            for shape_info in layout:
                x, y = shape_info['position']
                bounds = shape_info['bounds']
                
                # Apply rotation to get actual dimensions
                if shape_info['rotation'] in [90, 270]:
                    w, h = bounds[3] - bounds[1], bounds[2] - bounds[0]
                else:
                    w, h = bounds[2] - bounds[0], bounds[3] - bounds[1]
                
                all_x.extend([x, x + w])
                all_y.extend([y, y + h])
            
            used_width = max(all_x) - min(all_x) if all_x else 0
            used_height = max(all_y) - min(all_y) if all_y else 0
            bounding_box_area = used_width * used_height
            bounding_box_efficiency = (total_shape_area / bounding_box_area) * 100 if bounding_box_area > 0 else 0
        else:
            bounding_box_efficiency = 0
        
        return {
            'material_utilization': round(material_utilization, 2),
            'waste_percentage': round(waste_percentage, 2),
            'total_shape_area': round(total_shape_area, 2),
            'sheet_area': round(sheet_area, 2),
            'waste_area': round(waste_area, 2),
            'bounding_box_efficiency': round(bounding_box_efficiency, 2)
        }
    
    def _generate_cutting_instructions(self, layout):
        """
        Generate cutting instructions for optimized layout.
        
        Args:
            layout: Optimized layout configuration
        
        Returns:
            List of cutting instruction dictionaries
        """
        if not layout:
            return []
        
        instructions = []
        
        # Sort shapes by position (left to right, top to bottom)
        sorted_layout = sorted(layout, key=lambda x: (x['position'][1], x['position'][0]))
        
        for i, shape_info in enumerate(sorted_layout):
            x, y = shape_info['position']
            rotation = shape_info['rotation']
            bounds = shape_info['bounds']
            
            # Apply rotation to get actual dimensions
            if rotation in [90, 270]:
                width = bounds[3] - bounds[1]
                height = bounds[2] - bounds[0]
            else:
                width = bounds[2] - bounds[0]
                height = bounds[3] - bounds[1]
            
            instruction = {
                'shape_id': i,
                'cutting_order': i + 1,
                'position': {'x': round(x, 2), 'y': round(y, 2)},
                'rotation_degrees': rotation,
                'dimensions': {'width': round(width, 2), 'height': round(height, 2)},
                'cutting_type': 'laser',  # Default cutting method
                'start_point': {'x': round(x, 2), 'y': round(y, 2)},
                'end_point': {'x': round(x + width, 2), 'y': round(y + height, 2)}
            }
            
            instructions.append(instruction)
        
        return instructions
    
    def _compute_path_length(self, centroids, path_order):
        """
        Compute total path length for cutting sequence.
        
        Args:
            centroids: List of shape centroid coordinates
            path_order: Order in which shapes should be cut
        
        Returns:
            Total path length
        """
        if len(path_order) < 2:
            return 0.0
        
        total_length = 0.0
        
        for i in range(len(path_order) - 1):
            current_idx = path_order[i]
            next_idx = path_order[i + 1]
            
            # Calculate Euclidean distance between centroids
            distance = np.linalg.norm(
                np.array(centroids[current_idx]) - np.array(centroids[next_idx])
            )
            total_length += distance
        
        return round(total_length, 2)
    
    def _find_shape_placement(self, shape, grid):
        """
        Find optimal placement for a shape on the grid.
        
        Args:
            shape: Shape geometry to place
            grid: Current occupancy grid
        
        Returns:
            Placement coordinates (x, y) or None if no placement found
        """
        # Compute shape bounding box
        min_x, min_y = np.min(shape, axis=0).astype(int)
        max_x, max_y = np.max(shape, axis=0).astype(int)
        shape_width = max_x - min_x + 1
        shape_height = max_y - min_y + 1
        
        grid_height, grid_width = grid.shape
        
        # Try to find placement starting from top-left
        for y in range(grid_height - shape_height + 1):
            for x in range(grid_width - shape_width + 1):
                # Check if this placement is valid (no overlap with existing shapes)
                if self._can_place_shape(grid, x, y, shape_width, shape_height):
                    return (x, y)
        
        return None  # No valid placement found
    
    def _can_place_shape(self, grid, x, y, width, height):
        """
        Check if shape can be placed at given position without overlap.
        
        Args:
            grid: Current occupancy grid
            x, y: Placement coordinates
            width, height: Shape dimensions
        
        Returns:
            True if shape can be placed, False otherwise
        """
        # Check bounds
        if x + width > grid.shape[1] or y + height > grid.shape[0]:
            return False
        
        # Check for overlap with existing shapes
        region = grid[y:y+height, x:x+width]
        return not np.any(region)
    
    def _update_grid(self, grid, shape, x, y):
        """
        Update grid to mark shape placement.
        
        Args:
            grid: Occupancy grid to update
            shape: Shape geometry
            x, y: Placement coordinates
        """
        # Compute shape bounding box relative to placement
        min_x, min_y = np.min(shape, axis=0).astype(int)
        max_x, max_y = np.max(shape, axis=0).astype(int)
        shape_width = max_x - min_x + 1
        shape_height = max_y - min_y + 1
        
        # Mark the region as occupied
        end_x = min(x + shape_width, grid.shape[1])
        end_y = min(y + shape_height, grid.shape[0])
        grid[y:end_y, x:end_x] = True
    
    def _analyze_packing_efficiency(self, grid):
        """
        Analyze packing efficiency from occupancy grid.
        
        Args:
            grid: Occupancy grid showing placed shapes
        
        Returns:
            Dictionary containing packing efficiency metrics
        """
        total_cells = grid.size
        occupied_cells = np.sum(grid)
        
        if total_cells == 0:
            return {
                'packing_efficiency': 0.0,
                'waste_percentage': 100.0,
                'occupied_area': 0,
                'total_area': 0
            }
        
        packing_efficiency = (occupied_cells / total_cells) * 100
        waste_percentage = 100 - packing_efficiency
        
        # Calculate bounding box of occupied region
        if occupied_cells > 0:
            occupied_rows, occupied_cols = np.where(grid)
            bounding_box_area = (
                (np.max(occupied_rows) - np.min(occupied_rows) + 1) *
                (np.max(occupied_cols) - np.min(occupied_cols) + 1)
            )
            bounding_box_efficiency = (occupied_cells / bounding_box_area) * 100 if bounding_box_area > 0 else 0
        else:
            bounding_box_efficiency = 0
        
        return {
            'packing_efficiency': round(packing_efficiency, 2),
            'waste_percentage': round(waste_percentage, 2),
            'occupied_area': int(occupied_cells),
            'total_area': int(total_cells),
            'bounding_box_efficiency': round(bounding_box_efficiency, 2)
        }

# Example usage demonstration
def _example_usage():
    """
    Demonstrates basic usage of the Pattern Generation Generator.
    """
    generator = PatternGenerationGenerator()
    
    # Example problem description
    problem = "Optimize material nesting for laser cutting with irregular shapes"
    
    # Generate algorithm specification
    algo_spec = generator.generate_algorithm(problem)
    
    # Prepare example shapes (irregular polygons)
    shapes = [
        np.array([
            [0, 0], [2, 0], [2, 1], [1, 1], [1, 2], [0, 2]
        ]),
        np.array([
            [0, 0], [3, 0], [3, 3], [0, 3]
        ]),
        np.array([
            [0, 0], [1, 0], [1, 1], [0, 1]
        ])
    ]
    
    # Execute material nesting optimization
    nesting_result = generator.execute_algorithm(algo_spec, {
        'shapes': shapes,
        'optimization_type': 'material_nesting',
        'material_constraints': {
            'sheet_width': 10,
            'sheet_height': 10
        }
    })
    
    # Execute cutting path optimization
    cutting_path_result = generator.execute_algorithm(algo_spec, {
        'shapes': shapes,
        'optimization_type': 'cutting_path'
    })
    
    print("Material Nesting Result:")
    print(f"Waste Analysis: {nesting_result['waste_analysis']}")
    print(f"Cutting Instructions Count: {len(nesting_result['cutting_instructions'])}")
    
    print("\nCutting Path Result:")
    print(f"Path Length: {cutting_path_result['waste_analysis']['total_path_length']}")
    print(f"Cutting Order: {[inst['shape_index'] for inst in cutting_path_result['cutting_instructions']]}")

if __name__ == "__main__":
    _example_usage()