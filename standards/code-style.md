## code-style.md

### Version: 1.0
### Date: July 22, 2025

This file specifies formatting rules, naming conventions, and preferences to maintain readable and consistent code.

- **Formatting**:
  - Use Black formatter with default settings (line length 88 characters).
  - Indentation: 4 spaces; no tabs.
  - Strings: Prefer double quotes ("") for consistency.
- **Naming Conventions**:
  - Variables and functions: snake_case (e.g., draw_line, entity_id).
  - Classes: CamelCase (e.g., McpServer).
  - Constants: UPPER_SNAKE_CASE (e.g., DEFAULT_PORT=5000).
  - Descriptive names: Avoid abbreviations unless standard (e.g., use entity_selection instead of ent_sel).
- **Structure**:
  - Imports: Group standard libraries first, then third-party, then local; alphabetize within groups.
  - Functions: Include docstrings with parameters, returns, and examples.
  - Error Handling: Use specific exceptions (e.g., ValueError for invalid inputs) with clear messages.
- **Examples**:
  - Good: def unfold_surface(entity_id: int, tolerance: float) -> dict: ...
  - Bad: def uf(e, t): ...