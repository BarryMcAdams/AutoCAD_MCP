# AutoCAD MCP Development Guidelines

## Core Development Rules

### File Management - PERMANENT RULE
**NEVER DELETE OR REMOVE FILES** - Always move files to the `DELETED/` folder instead of deleting them.

This rule applies to:
- Source code files
- Configuration files  
- Documentation files
- Test files
- Any other project files

When a file needs to be "removed":
1. Create `DELETED/` folder if it doesn't exist
2. Move the file to `DELETED/` folder
3. Preserve the original directory structure within `DELETED/` if needed
4. Document the reason for moving the file

### Development Principles
- Maintain backward compatibility
- Preserve all existing functionality
- Use lazy loading patterns for optional dependencies
- Follow the existing code architecture
- Add comprehensive error handling and logging

### Environment & Path Considerations - IMPORTANT
**Cross-Platform Development Environment:**
- **Development/Analysis Environment**: Linux/WSL2 at `/mnt/c/users/adamslaptop/source/repos/autocad_mcp`
- **Windows Deployment Path**: `C:\Users\AdamsLaptop\source\repos\AutoCAD_MCP`
- **AutoCAD Compatibility**: This project requires Windows for AutoCAD COM integration
- **Testing Limitations**: Windows-specific modules (`pythoncom`, `win32com.client`) will fail imports on Linux - this is expected
- **Configuration Files**: All path references should use the Windows path format for deployment

**Key Implications:**
- Import failures for Windows-specific modules during Linux testing are normal
- MCP configuration and deployment scripts should reference Windows paths
- Cross-platform testing requires mock implementations for Windows-only dependencies

### Project Status
This is the AutoCAD MCP (Model Context Protocol) server project for AutoCAD 2025 automation and 3D surface unfolding operations.

Key features:
- AutoCAD COM integration
- 3D surface unfolding algorithms (LSCM and simple methods)
- Manufacturing drawing generation
- Pattern optimization and nesting
- Batch processing capabilities
- MCP server integration

### Testing and Quality
- All modules should handle missing optional dependencies gracefully
- Comprehensive error handling for AutoCAD COM operations
- Proper validation of input parameters
- Detailed logging for debugging and monitoring