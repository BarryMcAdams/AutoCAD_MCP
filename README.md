# AutoCAD MCP Server

A Model Context Protocol (MCP) server that provides AutoCAD integration for AI assistants like Claude. Enables natural language control of AutoCAD 2025 through conversational interfaces.

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![MCP Compatible](https://img.shields.io/badge/MCP-Compatible-green.svg)](https://modelcontextprotocol.io/)
[![AutoCAD 2025](https://img.shields.io/badge/AutoCAD-2025-red.svg)](https://www.autodesk.com/products/autocad)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What it does

This MCP server connects AutoCAD 2025 to AI assistants, allowing you to create and manipulate CAD drawings through natural language. It includes production-ready tools for basic CAD operations and advanced algorithms for complex surface processing.

**Primary use cases:**
- **Coding Assistant Integration**: Use with Claude, Cursor, or other MCP-compatible tools for AutoCAD automation
- **Advanced Surface Unfolding**: LSCM algorithm for converting 3D surfaces to 2D manufacturing patterns
- **CAD Workflow Automation**: Natural language commands for drawing creation and manipulation

## Requirements

- **AutoCAD 2025** (full version, Windows only)
- **Python 3.12+**
- **Windows OS** (required for AutoCAD COM interface)

## Quick Start

### With Claude Desktop

1. **Install**
   ```bash
   git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
   cd AutoCAD_MCP
   uv sync  # or: poetry install
   ```

2. **Configure Claude Desktop**
   Add to your MCP settings:
   ```json
   {
     "mcpServers": {
       "autocad-mcp": {
         "command": "./.venv/Scripts/python.exe",
         "args": ["src/server.py"],
         "cwd": "C:\\path\\to\\your\\AutoCAD_MCP"
       }
     }
   }
   ```

3. **Use**
   - Open AutoCAD 2025 with a drawing
   - In Claude Desktop: *"Draw a line from (0,0,0) to (100,100,0)"*

### With Claude Code CLI

```bash
# Install and register
git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
cd AutoCAD_MCP
uv sync
claude mcp add autocad-mcp ./.venv/Scripts/python.exe src/server.py

# Use in development
claude
# Then: "Create a circle at origin with radius 25"
```

## Available Tools

| Tool | Function | Example |
|------|----------|---------|
| `draw_line` | Create lines between 3D points | *"Draw a line from origin to (100,50,0)"* |
| `draw_circle` | Create circles with center and radius | *"Make a circle at (50,50,0) radius 25"* |
| `extrude_profile` | Extrude 2D shapes into 3D solids | *"Extrude this rectangle 10 units"* |
| `revolve_profile` | Revolve profiles around axes | *"Revolve this arc 180 degrees around Y-axis"* |
| `list_entities` | List all drawing objects | *"Show all objects in the drawing"* |
| `get_entity_info` | Get detailed object information | *"Get info for entity 12345"* |
| `server_status` | Check connection status | *"Is AutoCAD connected?"* |

## Advanced Features

### LSCM Surface Unfolding
The server includes a complete implementation of Least Squares Conformal Maps (LSCM) for unfolding 3D surfaces into 2D patterns. Useful for:
- Manufacturing pattern generation
- Sheet metal unfolding
- Textile pattern creation
- Material optimization

### Core Algorithms (Tested & Working)
- **LSCM Solver**: Mathematical surface unfolding (12/12 tests passing)
- **Mesh Processing**: Validation, optimization, and analysis tools
- **Geometric Utils**: 3D math operations and validations (10/10 tests passing)

### Development Features
The codebase includes extensive development tools and research implementations:
- AI-powered code generation (AutoLISP, Python, VBA)
- Natural language processing for CAD commands  
- Performance monitoring and optimization
- Security frameworks and validation
- Interactive development tools

*Note: Advanced features are implemented but require integration and testing for production use.*

## Testing

```bash
# Test core functionality
python -c "from src.algorithms.lscm import LSCMSolver; print('LSCM loads successfully')"
python -c "from src.utils import calculate_distortion_metrics; print('Utils loads successfully')"

# Run test suite
poetry run pytest tests/unit/test_utils.py  # 10/10 passing
poetry run pytest tests/unit/test_lscm_algorithm.py  # 12/12 passing
```

## Architecture

**Production Components:**
- MCP server with 7 AutoCAD tools
- AutoCAD COM integration via pyautocad
- LSCM surface unfolding algorithms
- Comprehensive testing framework

**Development Codebase:**
- 25,000+ lines of research and development code
- AI-powered automation tools
- Enterprise architecture components
- Performance optimization systems

## Configuration

Environment variables:
```bash
HOST=localhost
PORT=5001
AUTOCAD_TIMEOUT=30
DEFAULT_TOLERANCE=0.001
```

See `src/config.py` for advanced configuration options.

## Limitations

- Windows only (AutoCAD COM requirement)
- Requires AutoCAD 2025 full version
- Some advanced features need integration work
- Performance testing shows 78% test pass rate (non-critical failures)

## Use Cases

**Manufacturing**: Surface unfolding for laser cutting, sheet metal work, pattern optimization

**Architecture**: Automated drawing generation, parametric design, technical documentation

**Engineering**: CAD automation, repetitive task elimination, design validation

**Development**: AutoCAD script generation, workflow automation, AI-assisted modeling

## Contributing

Issues and pull requests welcome. See development standards in the codebase for code quality requirements.

## License

MIT License

---

**Status**: Production-ready core functionality with extensive development codebase for advanced features.