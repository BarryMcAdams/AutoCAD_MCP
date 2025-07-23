## CLAUDE.md

### Project-Specific Guidelines for Claude Code

1. **Core Principles**: Adhere to KISS (Keep It Simple, Stupid) and YAGNI (You Aren't Gonna Need It); focus on 3D CAD essentials first.
2. **Code Structure**: Limit files to <500 lines; functions to <50 lines; use modules for utilities/plugins.
3. **Architecture**: MCP server as central hub; pyautocad for CAD interactions; Flask for APIs; plugins in separate directory.
4. **Testing**: Require unit tests for all APIs; integration tests with mocked AutoCAD.
5. **Style Conventions**: Follow code-style.md; use type hints everywhere.
6. **Development Commands**:
   - Run server: python src/server.py
   - Tests: pytest -v
   - Lint: black . && ruff check .
