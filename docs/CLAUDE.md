# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## 🚨 CRITICAL INSTRUCTIONS
**NEVER ADD AUTHORSHIP CREDITS** - Do NOT add any authorship credits anywhere. Remove them when you see them. Credits will be assigned upon production release.

## Project Overview
AutoCAD Master Coder is a comprehensive development platform that transforms AutoCAD 2025 into an advanced automation environment with expert-level Python, AutoLISP, and VBA capabilities. Built on a production-ready manufacturing foundation, it provides enhanced COM wrapper, interactive development tools, VS Code integration, and comprehensive code generation while maintaining 100% backward compatibility with existing manufacturing workflows.

## Development Commands

### Environment Setup
```bash
# Install dependencies
poetry install

# Activate virtual environment (if needed)
poetry shell
```

### Core Development Commands
```bash
# Start Flask HTTP server (Manufacturing system - PRESERVED)
poetry run python src/server.py

# Start Enhanced MCP server (Master Coder + Manufacturing)
poetry run python src/mcp_integration/enhanced_mcp_server.py

# Start Legacy MCP server (Original manufacturing only)
poetry run python src/mcp_server.py

# Run all tests including backward compatibility
poetry run pytest

# Run backward compatibility test suite
poetry run python tests/test_backward_compatibility.py

# Run tests with coverage
poetry run pytest --cov=src

# Master Coder Enhanced Development Commands
# Format code (includes new modules)
poetry run black .

# Lint code (comprehensive analysis)
poetry run ruff check .

# Type checking (enhanced modules)
poetry run mypy src/enhanced_autocad src/mcp_integration src/tools

# Security analysis
poetry run bandit -r src/enhanced_autocad src/mcp_integration src/tools

# Complete code quality check
poetry run black . && poetry run ruff check . && poetry run mypy src/enhanced_autocad src/mcp_integration src/tools
```

### Manual Testing
```bash
# Test manufacturing server health (PRESERVED)
curl http://localhost:5001/health
# Expected: {"status":"ok","success":true,"timestamp":"...","version":"1.0.0"}

# Test AutoCAD connection status (PRESERVED)
curl http://localhost:5001/acad-status
# Expected: {"error":"AutoCAD is not connected",...} when AutoCAD not running

# Test basic line drawing (PRESERVED)
curl -X POST http://localhost:5001/draw/line \
  -H "Content-Type: application/json" \
  -d '{"start_point": [0,0,0], "end_point": [100,100,0]}'

# Master Coder Enhanced Testing
# Test enhanced AutoCAD wrapper directly
poetry run python -c "
from src.enhanced_autocad.compatibility_layer import Autocad
acad = Autocad()
print('Enhanced AutoCAD Status:', acad.get_connection_status())
"

# Test migration analysis
poetry run python src/tools/migrate_pyautocad.py . --dry-run

# Test performance baseline (when AutoCAD available)
poetry run python -c "
from src.tools.performance_baseline import PerformanceBaseline
baseline = PerformanceBaseline('.')
print('Performance tools initialized successfully')
"
```

## Architecture Overview

### Enhanced Multi-Server Architecture
- **Flask HTTP Server** (`src/server.py`): Manufacturing REST API on localhost:5001 with 25+ endpoints (PRESERVED)
- **Enhanced MCP Server** (`src/mcp_integration/enhanced_mcp_server.py`): Master Coder development + manufacturing tools
- **Legacy MCP Server** (`src/mcp_server.py`): Original manufacturing-only MCP integration (PRESERVED)
- **Enhanced AutoCAD Integration**: Enhanced COM wrapper with 100% pyautocad compatibility plus advanced features

### Core Components
```
src/
├── server.py                    # Main Flask application (HTTP API) - PRESERVED
├── mcp_server.py                # Legacy MCP server for IDE integration - PRESERVED
├── utils.py                     # AutoCAD COM utilities and validation - PRESERVED
├── dimensioning.py              # Automated dimensioning and manufacturing drawings - PRESERVED
├── pattern_optimization.py      # Material nesting and optimization algorithms - PRESERVED
├── decorators.py                # Request handling and error management - PRESERVED
├── config.py                   # Configuration management - PRESERVED
├── enhanced_autocad/           # Master Coder Enhanced AutoCAD wrapper (NEW)
│   ├── enhanced_wrapper.py    # Main EnhancedAutoCAD class with 100% pyautocad compatibility
│   ├── connection_manager.py  # Automatic connection recovery and health monitoring
│   ├── performance_monitor.py # Comprehensive operation tracking and metrics
│   ├── error_handler.py       # Intelligent error categorization and recovery
│   └── compatibility_layer.py # Drop-in pyautocad replacement
├── mcp_integration/           # Master Coder MCP integration layer (NEW)
│   ├── enhanced_mcp_server.py # Extended MCP server with development + manufacturing tools
│   ├── context_manager.py     # Session management for interactive development
│   ├── security_manager.py    # Code execution security and sandboxing
│   └── vscode_tools.py        # VS Code command palette and integration utilities
├── tools/                     # Development and migration tools (NEW)
│   ├── migrate_pyautocad.py   # Automated migration script with rollback capability
│   └── performance_baseline.py # Performance testing and comparison framework
└── algorithms/               # Advanced mathematical algorithms - PRESERVED
    ├── lscm.py              # Least Squares Conformal Mapping
    ├── geodesic.py          # Geodesic path calculations
    └── mesh_utils.py        # Triangle mesh processing utilities
```

### Key Technical Features

#### Manufacturing System (PRESERVED)
- **Surface Unfolding**: LSCM algorithm with <0.1% distortion tolerance
- **Automated Dimensioning**: Manufacturing-grade technical drawings
- **Pattern Optimization**: 85-95% material utilization with nesting algorithms
- **Batch Processing**: High-volume manufacturing workflows
- **3D Operations**: Extrusion, revolution, boolean operations, mesh creation

#### Master Coder Enhancements (NEW)
- **Enhanced COM Wrapper**: 100% pyautocad compatibility with automatic connection recovery
- **Performance Monitoring**: Real-time operation tracking, success rates, and metrics
- **Intelligent Error Handling**: Error categorization with recovery suggestions
- **Interactive Development**: Session-based Python code execution with VS Code integration
- **Security Framework**: Sandboxed code execution with comprehensive validation
- **Migration Tools**: Automated pyautocad to enhanced wrapper migration with rollback
- **Quality Analysis**: Integrated linting, type checking, and security scanning

## AutoCAD Integration Patterns

### Connection Management

#### Enhanced AutoCAD Wrapper (RECOMMENDED)
Use the enhanced wrapper for improved reliability and features:
```python
from enhanced_autocad.compatibility_layer import Autocad

# Enhanced AutoCAD connection with automatic recovery
acad = Autocad()
# Includes: auto-retry, health monitoring, performance tracking, error handling

# Get detailed connection status
status = acad.get_connection_status()
print(f"Connected: {status['connected']}, Version: {status.get('autocad_version', 'Unknown')}")

# Performance and error metrics
metrics = acad.get_performance_metrics()
errors = acad.get_error_statistics()
```

#### Legacy Connection (PRESERVED)
Original connection method still available:
```python
from utils import get_autocad_instance

# Original AutoCAD connection (PRESERVED for backward compatibility)
acad = get_autocad_instance()
# Connection includes auto-retry and error handling
```

### Entity Creation Pattern
```python
# Standard entity creation with validation
@require_autocad_connection
@handle_autocad_errors
@log_api_call
def create_entity():
    acad = get_autocad_instance()
    entity = acad.model.AddLine(start_point, end_point)
    return entity.Handle
```

### Input Validation
All API endpoints use validation utilities:
```python
from utils import validate_point3d, validate_entity_id

# Validate 3D coordinates
start_point = validate_point3d(data.get('start_point'))
# Validate entity references
entity_id = validate_entity_id(data.get('entity_id'))
```

## Critical API Endpoints

### Core Drawing Operations
- `POST /draw/line` - Create lines with start/end points
- `POST /draw/circle` - Create circles with center/radius
- `POST /draw/extrude` - Create 3D extruded solids from 2D profiles
- `POST /draw/revolve` - Create 3D revolved solids around axis
- `POST /draw/boolean-union` - Combine multiple solids
- `POST /draw/boolean-subtract` - Subtract solids from each other

### 3D Surface Operations
- `POST /surface/3d-mesh` - Create rectangular mesh surfaces
- `POST /surface/polyface-mesh` - Create complex polyface meshes
- `POST /surface/unfold` - Basic surface unfolding
- `POST /surface/unfold-advanced` - LSCM surface unfolding with fold lines

### Manufacturing Features
- `POST /dimension/linear` - Create linear dimensions
- `POST /dimension/angular` - Create angular dimensions
- `POST /dimension/manufacturing-drawing` - Generate complete technical drawings
- `POST /pattern/optimize-nesting` - Optimize material usage with nesting
- `POST /batch/surface-unfold` - Batch process multiple surfaces

## Prerequisites & Dependencies

### Required Software
- **AutoCAD 2025** (full version) - Must be running and visible
- **Python 3.12+** - Required for modern type hints and features
- **Windows OS** - Required for AutoCAD COM interface
- **Poetry** - For dependency management

### Python Dependencies
- **Core**: Flask 3.0.3, pyautocad 0.2.0, mcp 1.0.0
- **Scientific**: NumPy 2.1.0, SciPy 1.14.1 (for LSCM/geodesic algorithms)
- **Windows**: pypiwin32 223 (for COM interface)
- **Dev**: pytest 8.3.2, black 24.8.0, ruff 0.5.5

## Code Quality Standards

### Type Hints & Documentation
All functions must include comprehensive type hints:
```python
def unfold_surface(entity_id: int, tolerance: float) -> Dict[str, Any]:
    """
    Unfold a 3D surface using LSCM algorithm.
    
    Args:
        entity_id: AutoCAD entity handle/ID
        tolerance: Maximum allowed distortion (default: 0.001)
        
    Returns:
        Dict containing unfolding results, pattern data, and metadata
        
    Raises:
        ValueError: If entity_id is invalid or surface cannot be unfolded
        ConnectionError: If AutoCAD connection is lost
    """
```

### Error Handling Patterns
Use the decorator pattern for consistent error handling:
```python
@handle_autocad_errors  # Handles COM errors and connection issues
@require_autocad_connection  # Ensures AutoCAD is connected
@log_api_call  # Logs request/response for debugging
def api_endpoint():
    # Implementation
```

### Performance Requirements
- Simple operations: <1 second response time
- Complex LSCM unfolding: <10 seconds for surfaces with thousands of triangles
- Batch operations: Progress tracking for long-running processes
- Memory: Efficient mesh processing with sparse matrix operations

## Testing Strategy

### Test Structure
```
tests/
├── test_server.py           # Main Flask API integration tests
└── unit/
    ├── test_drawing_operations.py  # Unit tests for drawing functions
    └── ...
```

### Test Coverage Requirements
- Target >90% test coverage
- Unit tests for all utility functions
- Integration tests for API endpoints with mocked AutoCAD
- Real AutoCAD testing during development phases

### Running Tests
```bash
# Run all tests with verbose output
poetry run pytest -v

# Run with coverage report
poetry run pytest --cov=src --cov-report=html

# Run specific test file
poetry run pytest tests/unit/test_drawing_operations.py
```

## Manufacturing Integration

### Surface Unfolding Workflow
1. Create/import 3D surface in AutoCAD
2. Call `/surface/unfold-advanced` with LSCM algorithm
3. Generate manufacturing drawing with `/dimension/manufacturing-drawing`
4. Optimize material usage with `/pattern/optimize-nesting`
5. Export patterns for cutting/fabrication

### Batch Processing
For high-volume manufacturing:
```python
# Process multiple surfaces in single operation
{
    "entity_ids": [12345, 67890, 11111],
    "algorithm": "lscm",
    "create_manufacturing_drawings": true,
    "optimize_material_usage": true,
    "material_sheets": [{"width": 1219.2, "height": 2438.4, "material_type": "steel"}]
}
```

## Configuration Management

### Environment Variables
```bash
# Server settings
HOST=localhost
PORT=5001
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autocad_mcp.log

# Performance
MAX_BATCH_SIZE=100
PROCESSING_TIMEOUT=300
```

### AutoCAD Requirements
- AutoCAD 2025 must be running and visible
- At least one drawing document must be open
- COM interface must be accessible (no other applications blocking)

## Troubleshooting

### Common AutoCAD Connection Issues
1. **"Could not connect to AutoCAD"**: Ensure AutoCAD 2025 is running with an open drawing
2. **"Entity not found"**: Verify entity ID exists in current drawing space
3. **COM interface errors**: Restart AutoCAD if COM interface becomes unresponsive

### Performance Optimization
- Use batch operations for multiple entities
- Set appropriate tolerance values for surface operations
- Monitor memory usage during complex mesh processing
- Enable debug logging to identify bottlenecks

### Development Workflow
1. Start AutoCAD 2025 with a test drawing
2. Run `poetry run python src/server.py` to start Flask server
3. Test endpoints with curl or API client
4. Use `/acad-status` to verify AutoCAD connection
5. Monitor logs in `logs/autocad_mcp.log` for debugging