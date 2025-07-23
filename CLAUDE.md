# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## ✅ PHASE 1 COMPLETE (2025-07-23 11:30)

**STATUS**: Phase 1 successfully completed and committed to GitHub!

**VERIFIED WORKING**: 
- ✅ AutoCAD 2025 COM connection established
- ✅ Line drawing confirmed working (0,0 to 100,100)
- ✅ Server operational on localhost:5001
- ✅ All Flask endpoints functional
- ✅ Repository live at https://github.com/BarryMcAdams/AutoCAD_MCP

**CURRENT PHASE**: Phase 2 - 3D Operations Implementation

**PHASE 2 PRIORITIES**:
1. POST /draw/extrude - Create 3D extruded solids from 2D profiles
2. POST /draw/revolve - Create 3D revolved solids around axis
3. POST /draw/boolean-union - Combine multiple solids
4. POST /draw/boolean-subtract - Subtract solids from each other

**TESTING PROTOCOL**: User will pause AutoCAD work for testing phases

## Project Overview
AutoCAD MCP Server is a Python-based Model Context Protocol server for AutoCAD 2025 automation, specializing in 3D CAD operations. The system provides APIs for 3D entity manipulation, surface unfolding utilities (similar to SmartUnfold), and automated layout dimensioning via Flask web server and pyautocad COM integration.

## Architecture
- **MCP Server**: Flask-based HTTP server (localhost:5000) as central hub
- **CAD Integration**: pyautocad library for AutoCAD COM API interactions  
- **Core Logic**: src/server.py contains Flask routes and AutoCAD connection management
- **Plugin Framework**: Modular design for extensible CAD utilities
- **3D Focus**: Specialized in 3D-to-2D transformations and surface unfolding algorithms

## Development Commands

### Environment Setup
- Uses Poetry for dependency management
- Python 3.12 required

### Core Commands
- **Run server**: `python src/server.py`
- **Run tests**: `pytest -v` 
- **Format code**: `black . && ruff check .`
- **Install dependencies**: `poetry install`

### Testing Strategy
- Unit tests for all API endpoints
- Integration tests with mocked AutoCAD (tests use pytest)
- Target >90% test coverage following TDD approach

## Key Technical Patterns

### AutoCAD Connection Management
- Use `get_autocad_instance()` function in server.py for AutoCAD connections
- Implement auto-reconnect logic and verbose logging
- Employ context managers: `with Autocad() as acad:`

### API Design
- Flask routes follow REST conventions
- JSON input/output for complex operations
- Example: `POST /unfold_surface` with `{'entity_id': int, 'tolerance': float}`

### 3D Operations Focus
- Core APIs: AddExtrudedSolid, AddRevolvedSolid, Union, Subtract
- Surface operations: Add3DMesh, AddPolyFaceMesh, SectionSolid  
- Advanced utilities: surface unfolding with <0.1% distortion tolerance

### Plugin Architecture
- Use decorators for plugin registration: `@plugin.register`
- Separate directory for plugin modules
- Tkinter for plugin GUI interfaces

## Code Style Requirements
- Follow Black formatter (88 char line limit)
- snake_case for variables/functions, CamelCase for classes
- Type hints everywhere: `def unfold_surface(entity_id: int, tolerance: float) -> dict:`
- Comprehensive docstrings with parameters, returns, examples
- Specific exceptions with clear error messages

## Performance & Quality Standards
- Functions <50 lines, files <500 lines
- <1s response time for simple surface unfolding
- Batch entity manipulations for performance
- Profile with cProfile for optimization
- Windows-only compatibility (AutoCAD COM requirements)

## Dependencies
- **Core**: Flask 3.0.3, pyautocad 0.2.0, NumPy 2.1.0, SciPy 1.14.1
- **Dev**: pytest 8.3.2, black 24.8.0, ruff 0.5.5
- **Requirements**: AutoCAD 2025 full version, Windows OS

## Security Considerations  
- Validate all API inputs
- Restrict server to localhost by default
- No hardcoded paths or secrets in code