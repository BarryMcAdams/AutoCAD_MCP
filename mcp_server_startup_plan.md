# AutoCAD MCP Server Startup Plan

## Overview
This document outlines the systematic approach to testing and documenting all MCP server startup methods for the AutoCAD MCP Server project.

## Current Status
- [x] Research MCP server startup methods and best practices
- [x] Verify current project dependencies and environment setup
- [x] Create comprehensive MCP server startup plan
- [-] Test the main MCP server (src/mcp_server.py) using uv
- [ ] Test the standalone MCP server (mcp_server_standalone.py)
- [ ] Test the Flask HTTP server (src/server.py) for comparison
- [ ] Check MCP configuration and integration with VS Code/Roo Code
- [ ] Document startup procedures and troubleshooting steps
- [ ] Create startup scripts for different use cases

## Server Components

### 1. Main MCP Server (Primary Integration)
- **File**: `src/mcp_server.py`
- **Purpose**: Primary MCP server for VS Code/Roo Code integration using FastMCP
- **Configuration**: Defined in `mcp_config.json`
- **Startup Command**: `uv run python src/mcp_server.py`
- **Dependencies**: FastMCP, pyautocad, win32com, numpy, scipy

### 2. Standalone MCP Server (Testing)
- **File**: `mcp_server_standalone.py`
- **Purpose**: Simplified MCP server for basic testing and dependency validation
- **Startup Command**: `python mcp_server_standalone.py`
- **Dependencies**: Minimal set for basic MCP functionality

### 3. Flask HTTP Server (REST API)
- **File**: `src/server.py`
- **Purpose**: REST API server for HTTP-based AutoCAD operations
- **Startup Command**: `uv run python src/server.py`
- **Dependencies**: Flask, FastAPI, uvicorn

## Testing Workflow

### Phase 1: Prerequisites Verification
1. Verify Python 3.12+ installation
2. Verify `uv` package manager availability
3. Verify Poetry environment setup
4. Verify AutoCAD 2025 is running
5. Install dependencies: `poetry install`

### Phase 2: Main MCP Server Testing
1. **Test Command**: `uv run python src/mcp_server.py`
2. **Expected Output**: FastMCP server startup message
3. **Validation**: Check for successful initialization and no errors
4. **Integration**: Verify compatibility with VS Code/Roo Code extensions

### Phase 3: Standalone MCP Server Testing
1. **Test Command**: `python mcp_server_standalone.py`
2. **Expected Output**: Basic MCP server startup message
3. **Validation**: Check for simplified functionality without errors
4. **Purpose**: Verify minimal viable MCP server functionality

### Phase 4: Flask HTTP Server Testing
1. **Test Command**: `uv run python src/server.py`
2. **Expected Output**: Flask server startup on port 5000
3. **Validation**: Test HTTP endpoints and AutoCAD integration
4. **Comparison**: Compare performance and functionality with MCP servers

### Phase 5: Configuration and Integration Testing
1. **MCP Configuration**: Verify `mcp_config.json` settings
2. **VS Code Integration**: Test MCP server connection with VS Code
3. **Roo Code Integration**: Test MCP server connection with Roo Code
4. **Environment Variables**: Verify PYTHONPATH and other required settings

## Success Metrics

### Technical Success Criteria
- [ ] All servers start without errors
- [ ] Each server displays appropriate startup messages
- [ ] Servers listen on expected ports/interfaces
- [ ] No dependency conflicts or version issues
- [ ] AutoCAD integration functions correctly

### Integration Success Criteria
- [ ] VS Code MCP extension connects successfully
- [ ] Roo Code MCP integration works properly
- [ ] Configuration files are valid and functional
- [ ] Environment variables are properly set

### Performance Success Criteria
- [ ] Server startup time is reasonable (< 5 seconds)
- [ ] Memory usage is acceptable (< 100MB)
- [ ] Response times are adequate for interactive use
- [ ] No resource leaks or memory accumulation

## Troubleshooting Guide

### Common Issues and Solutions

#### 1. Dependency Issues
- **Problem**: Missing or conflicting dependencies
- **Solution**: Run `poetry install` and `poetry update`

#### 2. AutoCAD Connection Issues
- **Problem**: Cannot connect to AutoCAD 2025
- **Solution**: Ensure AutoCAD is running and pyautocad is properly installed

#### 3. MCP Server Initialization Errors
- **Problem**: FastMCP server fails to start
- **Solution**: Check mcp_config.json and verify all required dependencies

#### 4. Port Conflicts
- **Problem**: Server cannot bind to expected port
- **Solution**: Check for existing services on the port and adjust configuration

#### 5. Environment Variable Issues
- **Problem**: PYTHONPATH or other environment variables not set
- **Solution**: Verify environment variables are correctly configured

## Next Steps

### Immediate Actions
1. Execute the main MCP server test: `uv run python src/mcp_server.py`
2. Document any errors or issues encountered
3. Test standalone MCP server: `python mcp_server_standalone.py`
4. Test Flask HTTP server: `uv run python src/server.py`

### Documentation Deliverables
1. Updated startup procedures documentation
2. Troubleshooting guide with common solutions
3. Startup scripts for different use cases
4. Integration guide for VS Code and Roo Code

### Scripts to Create
1. `start_mcp_server.bat/sh` - Main MCP server startup
2. `start_standalone_mcp.bat/sh` - Standalone MCP server startup
3. `start_flask_server.bat/sh` - Flask HTTP server startup
4. `test_all_servers.bat/sh` - Comprehensive testing script

## Conclusion

This systematic approach ensures that all MCP server startup methods are thoroughly tested and documented. The plan covers technical validation, integration testing, and performance evaluation to ensure reliable operation across different use cases.

The final deliverables will provide clear startup procedures, troubleshooting guidance, and automation scripts to facilitate easy deployment and maintenance of the AutoCAD MCP Server.