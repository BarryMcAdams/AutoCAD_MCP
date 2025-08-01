# AutoCAD MCP Server Setup for VS Code & Roo Code

This guide shows you how to set up the AutoCAD MCP Server to work with VS Code and Roo Code extensions.

## Prerequisites

1. **AutoCAD 2025** installed and running
2. **Python 3.12+** installed  
3. **Poetry** installed for dependency management
4. **VS Code** with MCP support (version 1.102+)
5. **Roo Code extension** installed in VS Code

## Installation Steps

### 1. Install Dependencies

```bash
# Navigate to the project directory
cd C:/Users/barrya/source/repos/AutoCAD_MCP

# Install MCP dependencies
poetry add "mcp[cli]"

# Install all dependencies
poetry install
```

### 2. Test MCP Server Locally

```bash
# Test the MCP server directly
poetry run python src/mcp_server.py

# Or use uv for development
uv run python src/mcp_server.py
```

## VS Code Configuration

### Enable MCP in VS Code

1. Open VS Code Settings (Ctrl+,)
2. Search for "MCP"
3. Enable "MCP: Enable" setting
4. Set "MCP: Config Path" to the project's `mcp_config.json`

### Alternative: Global MCP Settings

Add to your VS Code settings.json:

```json
{
  "mcp.enabled": true,
  "mcp.configPath": "C:/Users/barrya/source/repos/AutoCAD_MCP/mcp_config.json"
}
```

## Roo Code Configuration

### Method 1: Project-Level Configuration
The `.roo/mcp.json` file is already configured in the project.

### Method 2: Global Configuration
Add to your Roo Code settings (`cline_mcp_settings.json`):

```json
{
  "mcpServers": {
    "autocad-mcp": {
      "command": "python",
      "args": ["src/mcp_server.py"],
      "cwd": "C:/Users/barrya/source/repos/AutoCAD_MCP",
      "env": {
        "PYTHONPATH": "src"
      },
      "alwaysAllow": [
        "draw_line",
        "draw_circle", 
        "get_autocad_status"
      ]
    }
  }
}
```

## Usage Examples

### In VS Code with MCP
Once configured, you can use natural language commands:

```
"Draw a line from (0,0,0) to (100,100,0) in AutoCAD"
"Create a circle at the origin with radius 50"
"Unfold the surface with entity ID 12345 using LSCM algorithm"
```

### In Roo Code
Ask Roo Code to help with AutoCAD automation:

```
"Help me create a 3D manufacturing workflow using the AutoCAD MCP tools"
"Unfold this complex surface and optimize the material nesting"
"Generate manufacturing drawings with proper dimensions"
```

## Available MCP Tools

### Basic Drawing
- `draw_line(start_point, end_point)` - Draw lines
- `draw_circle(center, radius)` - Draw circles

### 3D Operations  
- `extrude_profile(profile_points, height)` - Create extruded solids
- `revolve_profile(profile_points, axis_start, axis_end, angle)` - Create revolved solids
- `boolean_union(entity_ids)` - Combine solids
- `boolean_subtract(target_id, subtract_ids)` - Subtract solids

### Surface Operations
- `create_3d_mesh(m_size, n_size, coordinates)` - Create 3D meshes
- `unfold_surface(entity_id, tolerance, algorithm)` - Surface unfolding

### Manufacturing
- `add_linear_dimension(start, end, dim_line)` - Add dimensions
- `optimize_pattern_nesting(patterns, materials, algorithm)` - Material optimization
- `batch_surface_unfold(entity_ids, algorithm, create_drawings)` - Batch processing

### Information
- `get_autocad_status()` - Check AutoCAD connection
- `list_entities()` - List drawing entities

## Troubleshooting

### MCP Server Not Found
- Verify the command path in config files
- Check that Python and Poetry are in your PATH
- Ensure AutoCAD 2025 is running

### Permission Errors
- Run VS Code as Administrator if needed
- Check Windows firewall settings
- Verify AutoCAD COM permissions

### Connection Issues
- Ensure AutoCAD 2025 is open with a drawing
- Check that no other applications are using AutoCAD COM
- Restart both VS Code and AutoCAD if needed

### Debug Mode
Enable detailed logging by setting environment variable:
```bash
set MCP_LOG_LEVEL=DEBUG
```

## Advanced Usage

### Custom Prompts
Use the built-in manufacturing workflow prompt:
```
@manufacturing-workflow "complex curved panel for aircraft wing"
```

### Resource Access
Access AutoCAD status and entity information:
- `autocad://status` - Current connection status
- `autocad://entities` - List of drawing entities

### Batch Operations
Process multiple surfaces efficiently:
```python
# Example: Batch unfold multiple surfaces
entity_ids = [12345, 67890, 11111]
result = batch_surface_unfold(entity_ids, "lscm", True)
```

## Next Steps

1. Test basic drawing operations first
2. Try 3D operations with simple geometries  
3. Experiment with surface unfolding
4. Explore manufacturing workflow automation
5. Integrate with your CAD/CAM pipeline

The MCP server provides a standardized way for AI assistants to interact with AutoCAD, enabling powerful automation workflows while maintaining the flexibility of your existing tools.