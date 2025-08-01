# MCP Configuration Options

This project provides multiple MCP (Model Context Protocol) configuration files to support different Python package managers and setups.

## Configuration Files

### 1. `mcp_config.json` (UV-based)
**Requirements**: UV package manager installed
```json
{
  "command": "uv",
  "args": ["run", "python", "src/mcp_server.py"]
}
```

### 2. `mcp_config_poetry.json` (Poetry-based)  
**Requirements**: Poetry package manager installed
```json
{
  "command": "poetry", 
  "args": ["run", "python", "src/mcp_server.py"]
}
```

### 3. `mcp_config_python.json` (Direct Python)
**Requirements**: Python with dependencies installed globally or in active venv
```json
{
  "command": "python",
  "args": ["src/mcp_server.py"]
}
```

## How to Use

1. **Choose the appropriate config file** based on your Python package manager
2. **Copy or rename** the chosen config to `mcp_config.json` (if required by your MCP client)
3. **Ensure dependencies are installed** using your chosen package manager:
   - UV: `uv sync`
   - Poetry: `poetry install`
   - Pip: `pip install -r requirements.txt` (you may need to generate this from pyproject.toml)

## Path Configuration

All configurations use the Windows path format:
```
"cwd": "C:/Users/AdamsLaptop/source/repos/AutoCAD_MCP"
```

This is correct for Windows deployment even when developing on Linux/WSL2.

## Troubleshooting

- **Command not found**: Ensure your chosen package manager is installed and in PATH
- **Module not found**: Verify dependencies are installed in the correct environment
- **Path errors**: Confirm the `cwd` path matches your actual project location