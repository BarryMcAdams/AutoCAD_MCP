## tech-stack.md

### Version: 1.0
### Date: July 22, 2025

This file defines the default technical choices for the AutoCAD MCP Server project. It ensures consistency across all development activities.

- **Programming Language**: Python 3.12 (primary for scripting and server implementation; chosen for its extensive libraries and compatibility with AutoCAD automation).
- **Core Libraries**:
  - pyautocad==0.2.0 (for simplified COM API interactions with AutoCAD 2025; preferred over raw pywin32/comtypes for ease of use in 3D manipulations).
  - Flask==3.0.3 (web framework for the MCP server to handle HTTP-based protocol endpoints).
  - NumPy==2.1.0 and SciPy==1.14.1 (for mathematical computations, e.g., matrix operations in 3D transformations and unfolding algorithms).
  - Tkinter (standard Python library for GUI interfaces in plugins, e.g., input forms).
- **Testing and Debugging**:
  - pytest==8.3.2 (for unit and integration tests).
  - black==24.8.0 (code formatter).
- **Database Integration**: SQLite (via sqlite3 standard library) for local session storage.
- **IDE/Environment**: Visual Studio Code 1.92+ with extensions: Roo Code, Claude Code, Cline.
- **Overrides**: For 3D-specific tasks (e.g., unfolding), incorporate external algorithms if needed, but prioritize built-in libraries to avoid dependencies.
- **Compatibility Notes**: Windows-only (due to AutoCAD COM requirements); ensure AutoCAD 2025 full version is installed.