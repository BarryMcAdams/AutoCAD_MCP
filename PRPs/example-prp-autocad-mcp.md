# PRP for AutoCAD MCP Server Development

## Goal

Develop a highly capable Model Context Protocol (MCP) server for AutoCAD 2025 that enables programmatic automation of advanced 3D CAD operations through Python scripts. The server must integrate seamlessly with Visual Studio Code (VS Code) extensions such as Roo Code, Claude Code, and Cline for AI-assisted plugin and script creation. Key features include support for basic and advanced CAD operations, a plugin framework for custom utilities, and specific tools for unfolding 3D entities into 2D patterns for CNC cutting (approximating double-curvature surfaces via segmentation, triangulation, geodesic path calculation, and 2D polyline generation) and placing 3D entities into layout tabs with automatic dimensioning.

## Why

- Automate repetitive and complex 3D CAD workflows in AutoCAD 2025, reducing manual errors and design iteration time by at least 50%, particularly for industries like manufacturing, engineering, and architecture where 3D modeling is predominant.
- Enable CAD designers to create custom plugins and scripts with separate interfaces, pre-programmed logic, and user input variables, enhancing productivity without requiring deep programming expertise.
- Facilitate AI-assisted development in VS Code, allowing natural language prompts to generate advanced code for tasks like surface unfolding (mimicking SmartUnfold functionality for non-developable surfaces) and layout dimensioning, which are not natively robust in AutoCAD.
- Provide a stable, extensible bridge between AutoCAD's COM API and modern Python ecosystems, addressing limitations in existing tools by incorporating custom approximation algorithms for unfolding to achieve high accuracy (<0.1% distortion in area comparison between 3D surface and 2D pattern).

## What

A Flask-based HTTP server (running on localhost:5000 by default) that exposes APIs for interacting with AutoCAD 2025 via pyautocad, supporting 3D-focused operations, plugin registration, and utilities for unfolding (handling surfaces, meshes, and solids by segmenting into triangles/strips, computing geodesics using graph-based shortest paths, and generating 2D polylines with annotations) and layout dimensioning (creating viewports in paper space, setting 3D views, and adding associative dimensions to visible edges). The system includes a Python client library for VS Code integration, ensuring compatibility with AI extensions for code generation and debugging.

### Success Criteria

- [ ] MCP server starts successfully, connects to AutoCAD 2025, and handles at least 100 API calls per minute without crashes.
- [ ] Basic 3D operations (e.g., extrude solid, union/subtract) execute correctly, verified by querying entity properties post-operation.
- [ ] Unfolding utility processes a double-curvature surface (e.g., a segmented mesh) into a 2D pattern with <0.1% area deviation, including curve projections (e.g., marking lines) as demonstrated in the reference video (https://www.youtube.com/watch?v=vJLOilqgN0k).
- [ ] Layout dimensioning utility places a 3D entity in a new layout tab, sets an isometric view, and auto-adds linear/angular dimensions to all visible edges, with associative updates.
- [ ] Plugin framework allows registration of a custom module with Tkinter GUI for user inputs, pre-programmed logic (e.g., conditional checks), and variable acceptance, executable via VS Code.
- [ ] VS Code integration: Client scripts run in terminal, compatible with Roo Code autocompletion, Claude Code prompt-based generation, and Cline CLI execution.
- [ ] Comprehensive error handling: Auto-reconnects on COM disconnections, logs to mcp.log, and returns JSON error responses.
- [ ] Performance: Unfolding a moderate-complexity surface (<1000 faces) completes in <5 seconds; dimensioning in <2 seconds.
- [ ] Testing coverage: >90% for unit/integration tests; no failures in validation loops.

## All Needed Context

### Documentation & References

- url: https://pypi.org/project/pyautocad/
  why: Official pyautocad documentation for COM API wrappers, including examples for 3D entity creation (e.g., AddExtrudedSolid, Add3DMesh) and manipulation.

- url: https://developer.autodesk.com/api/autocad/
  why: Autodesk AutoCAD API reference for COM methods, particularly 3D solids/surfaces (e.g., AddRevolvedSolid, SectionSolid), layout management (Layouts collection, AddPViewport), and dimensioning (AddDimAligned, AddDimAngular).

- url: https://github.com/zh19980811/Easy-MCP-AutoCad
  why: Reference implementation for basic MCP server setup using pywin32/comtypes; adapt for pyautocad and extend to 3D.

- url: https://github.com/daobataotie/CAD-MCP
  why: Example of extending MCP for NLP-driven CAD control; use as inspiration for plugin framework and entity selection.

- doc: https://docs.scipy.org/doc/scipy/reference/generated/scipy.spatial.Delaunay.html
  why: SciPy Delaunay triangulation for segmenting surfaces into triangles during unfolding approximation.

- doc: https://networkx.org/documentation/stable/reference/algorithms/generated/networkx.algorithms.shortest_paths.generic.shortest_path.html
  why: NetworkX for geodesic path calculation on graph representations of triangulated meshes.

- file: tech-stack.md (from Agent OS standards)
  why: Defines project stack (Python 3.12, pyautocad==0.2.0, Flask==3.0.3, NumPy==2.1.0, SciPy==1.14.1) to ensure consistency.

- file: code-style.md (from Agent OS standards)
  why: Naming conventions (snake_case), formatting (Black), and structure for all code.

- file: best-practices.md (from Agent OS standards)
  why: TDD, modularity, error resilience patterns (e.g., context managers for AutoCAD sessions).

- file: mission.md (from Agent OS product)
  why: High-level vision for 3D automation focus.

- file: roadmap.md (from Agent OS product)
  why: Phased development plan to guide implementation.

- file: PRD.md (from Agent OS specs)
  why: Detailed requirements, including API endpoints (e.g., /unfold_surface, /create_layout) and non-functional specs.

- url: https://www.youtube.com/watch?v=vJLOilqgN0k
  why: Demonstration of unfolding double-curvature surfaces; replicate functionality for single/multi-surfaces, including curve projections and high accuracy.

- doc: https://www.smartunfold.com/
  why: Reference for unfolding logic; implement custom approximation since plugin invocation may not be direct—focus on triangulation and conformal mapping.

### Known Gotchas

# CRITICAL: pyautocad requires AutoCAD 2025 to be running and visible; handle visibility with acad.Visible = True and auto-launch if needed.

# CRITICAL: COM interactions are Windows-only; raise PlatformError if not on Windows.

# CRITICAL: For unfolding non-developable surfaces, approximations may introduce minor distortions—always compute and log area deviation; use tolerance parameter to control segmentation density.

# CRITICAL: Geodesic calculations on dense meshes (>10,000 vertices) can be computationally intensive—optimize with mesh decimation (e.g., via SciPy) and warn on high complexity.

# CRITICAL: Layout dimensioning in paper space must use associative dimensions to handle model updates; avoid model space dimensions to prevent scaling issues.

# CRITICAL: Validate all API inputs (e.g., point coordinates as [x, y, z] floats) to prevent COM errors; use try-except for AutoCADException.

# CRITICAL: Ensure server shutdown gracefully releases COM objects to avoid AutoCAD hangs (e.g., del acad).

# CRITICAL: VS Code extensions may require specific Python environments—use virtualenvs and configure debug settings accordingly.

## Implementation Blueprint

### High-Level Architecture

- Server: Flask app with routes for APIs; use pyautocad.Autocad() in a singleton pattern for session management.
- Client: mcp_client.py library with methods mirroring APIs (e.g., client.unfold_surface(entity_id, tolerance)).
- Plugins: Decorator-based registration (@plugin.register) in a plugins/ directory; each plugin has init_gui() for Tkinter inputs, execute_logic(variables) for processing.

### Step-by-Step Tasks

1. Setup Project Structure:
   - Create directories: src/ (server.py, apis.py, utilities.py, plugins/), tests/, docs/.
   - Initialize with pyproject.toml for dependencies.

2. Implement Core Server:
   - In server.py: app = Flask(__name__); @app.route('/health', methods=['GET']) returns {'status': 'ok'}.
   - Connect to AutoCAD: def get_acad(): return Autocad(create_if_not_exists=True).
   - Handle auto-reconnect: Use a wrapper with try-except to relaunch on failure.

3. Basic CAD APIs:
   - POST /draw/extrude: {'profile_id': int, 'height': float} -> acad.model.AddExtrudedSolid(profile, height, 0).
   - GET /entities: Return list of entity dicts with ID, type, properties.

4. Unfolding Utility (in utilities.py):
   - def unfold_surface(entity_id, tolerance=0.01, method='triangulation'):
     - Get entity = acad.doc.GetEntity(entity_id); if type not surface/mesh, raise error.
     - Extract geometry: vertices = entity.GetPointsMatrix() or similar for surfaces.
     - Triangulate: Use SciPy Delaunay on projected points.
     - Build graph: NetworkX Graph with edges as triangle sides.
     - Compute geodesics: shortest_path for boundary curves.
     - Flatten: Use least-squares optimization (SciPy minimize) to position points in 2D with minimal strain.
     - Generate 2D: AddPolyline for contours, AddText for annotations.
     - Compute deviation: Compare areas (3D surface area vs. 2D polygon area).
   - API: POST /unfold_surface returns {'pattern_id': int, 'deviation': float}.

5. Layout Dimensioning Utility:
   - def create_layout(entity_id, layout_name, scale=1.0, view_type='isometric'):
     - layout = acad.doc.Layouts.Add(layout_name); acad.doc.ActiveLayout = layout.
     - viewport = layout.Block.AddPViewport(center, width, height); viewport.Scale = scale.
     - Set view: viewport.DView(entity_id, view_type).
     - Auto-dimension: Get visible edges (via bounding box or ray casting simulation), add AddDimAligned(point1, point2, text_point) for each.
   - API: POST /create_layout returns {'layout_name': str, 'dimensions_added': int}.

6. Plugin Framework:
   - In plugins.py: registry = {}; def register(name): def decorator(func): registry[name] = func.
   - Example plugin: @register('stair_generator') def generate_stairs(variables): # logic with inputs like height, steps.

7. VS Code Integration:
   - Client library: class McpClient: def __init__(self, host='localhost:5000'): self.session = requests.Session().
   - Ensure scripts import pyautocad and use client for calls.

8. Error Handling and Logging:
   - Use logging module to mcp.log; JSON responses with 'error' key.

### Pseudocode for Key Algorithms

For Unfolding:
```
def approximate_unfold(mesh_vertices, faces, tolerance):
    tri = Delaunay(mesh_vertices[:, :2])  # Project to 2D for initial triangulation
    G = nx.Graph()
    for face in faces:
        G.add_edges_from(combinations(face, 2), weight=distance)
    geodesics = {}
    for boundary_edge in boundary_edges:
        geodesics[boundary_edge] = nx.shortest_path(G, source, target, weight='weight')
    # Flatten using optimization
    def objective(flat_points):
        strain = sum(dist(flat_points[i], flat_points[j]) - original_dist for i,j in edges)
        return strain**2
    result = minimize(objective, initial_flat_points, method='L-BFGS-B')
    return add_polyline(result.x.reshape(-1, 2))
```

For Dimensioning:
```
def auto_dimension_visible_edges(entity, viewport):
    edges = get_visible_edges(entity, viewport)  # Simulate with bounding box projection
    for edge in edges:
        p1, p2 = edge.points
        dim_pos = midpoint(p1, p2) + offset
        acad.model.AddDimAligned(p1, p2, dim_pos)
```

## Validation Loop

### Level 1: Syntax & Style

black --check .
ruff check . --fix
mypy .

### Level 2: Unit Tests

pytest tests/test_apis.py -v  # Mock pyautocad with unittest.mock for API calls
pytest tests/test_utilities.py -v  # Test unfolding math with sample meshes (e.g., assert deviation < 0.001)

### Level 3: Integration Test

# Start server in background
python src/server.py &

# Test unfolding
curl -X POST http://localhost:5000/unfold_surface \
  -H "Content-Type: application/json" \
  -d '{"entity_id": 123, "tolerance": 0.01}' | jq '.success'  # Expect true, check mcp.log for deviation

# Test layout
curl -X POST http://localhost:5000/create_layout \
  -H "Content-Type: application/json" \
  -d '{"entity_id": 123, "layout_name": "TestLayout", "scale": 1.0}' | jq '.dimensions_added > 0'

# Manual verification: Open AutoCAD, inspect drawing for 2D pattern and layout dimensions

# Kill server
pkill -f server.py

### Level 4: End-to-End VS Code Script Test

# In VS Code terminal:
python client_script.py --unfold sample.dwg  # Script loads DWG, calls API, saves output; verify with AutoCAD open