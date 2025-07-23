## best-practices.md

### Version: 1.0
### Date: July 22, 2025

This file outlines the development philosophy, patterns to follow, and anti-patterns to avoid.

- **Philosophy**:
  - Prioritize modularity: Design components (e.g., plugins) as independent modules for extensibility.
  - Test-Driven Development (TDD): Write tests before code; aim for >90% coverage.
  - Error Resilience: Implement auto-reconnect to AutoCAD; log all operations verbosely.
- **Patterns to Follow**:
  - Use decorators for plugin registration (e.g., @plugin.register).
  - Employ context managers for AutoCAD sessions (e.g., with Autocad() as acad: ...).
  - For complex algorithms (e.g., unfolding), break into sub-functions: triangulate_mesh(), compute_geodesics(), generate_2d_polyline().
  - Document rationale in comments for non-obvious choices.
- **Anti-Patterns to Avoid**:
  - Avoid global variables; use dependency injection.
  - Do not hardcode paths or ports; use configurations.
  - Prevent tight coupling: Abstract pyautocad calls behind MCP APIs to allow future library swaps.
- **Performance Considerations**: Optimize for CAD operations (e.g., batch entity manipulations); profile with cProfile if needed.
- **Security**: Validate all API inputs; restrict to localhost by default.