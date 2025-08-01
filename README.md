<div align="center">

# AutoCAD MCP Server

<p align="center">
  <strong>A Windows-only MCP server for AutoCAD COM automation</strong>
</p>

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.12+-blue.svg" alt="Python Version">
  <img src="https://img.shields.io/badge/AutoCAD-2025-orange.svg" alt="AutoCAD Version">
  <img src="https://img.shields.io/badge/License-MIT-green.svg" alt="License">
  <img src="https://img.shields.io/badge/Status-Alpha-red.svg" alt="Status">
  <img src="https://img.shields.io/badge/Platform-Windows%20ONLY-red.svg" alt="Platform">
</p>

---

</div>

## Overview

This is an experimental Model Context Protocol (MCP) server that provides basic AutoCAD COM automation through Python. It includes some 3D surface unfolding algorithms and basic drawing operations.

**⚠️ IMPORTANT**: This project is in early development and requires Windows with AutoCAD 2025 installed. It will not work on Linux, macOS, or without AutoCAD.

## Current Features

- Basic AutoCAD drawing operations (lines, circles)
- 3D extrusion and revolution operations
- Entity listing and inspection
- LSCM surface unfolding algorithm (experimental)
- Simple pattern optimization

## Requirements

### Mandatory Requirements
- **Windows 10/11** (REQUIRED - will not work on other platforms)
- **AutoCAD 2025** installed and licensed (specific version required)
- **Python 3.12+**

### Known Limitations
- This project uses Windows-specific COM libraries (`pythoncom`, `win32com.client`, `pyautocad`)
- Will crash immediately on Linux/macOS due to missing Windows dependencies
- No cross-platform compatibility planned
- Mock AutoCAD system exists but is not integrated with main functionality

## Installation (Windows Only)

⚠️ **Prerequisites**: Must have AutoCAD 2025 installed and running on Windows

1. **Clone the repository:**
   ```bash
   git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
   cd AutoCAD_MCP
   ```

2. **Install dependencies:**
   ```bash
   pip install -e .
   ```
   Note: `pypiwin32` dependency will fail on non-Windows systems

3. **Configure MCP client:**
   - Use the provided `mcp_config.json` 
   - Update the `cwd` path to your actual installation directory

4. **Run the server:**
   ```bash
   python src/mcp_server.py
   ```

**Troubleshooting:**
- If imports fail, you're probably not on Windows
- If AutoCAD connection fails, ensure AutoCAD 2025 is running
- Path issues: Update `mcp_config.json` with your actual paths

## Project Status

This is an **experimental/alpha** project with the following status:

### What Works
- Basic drawing operations (lines, circles) via COM
- 3D solid creation (extrusion, revolution)
- Entity inspection and property extraction
- LSCM algorithm implementation (mathematical)

### What's Incomplete
- Many advanced features are stubbed out or partially implemented
- Enterprise features exist in code but are untested
- AI features are framework only
- Documentation may not match actual functionality

### Development Notes
- Developed in Linux/WSL2 environment but deployed to Windows
- Contains extensive mock systems for testing that aren't used in production
- Path configurations assume specific Windows directory structure

## Contributing

This is a personal project but contributions are welcome:

- **Issues**: Report bugs or suggest improvements
- **Testing**: Help test on different Windows/AutoCAD configurations  
- **Code**: Pull requests welcome for bug fixes or feature completions

Note: All testing must be done on Windows with AutoCAD 2025.

## 📄 License

This project is licensed under the MIT License. See the [LICENSE](./LICENSE) file for details.

## Acknowledgments

- [pyautocad](https://pypi.org/project/pyautocad/) - Python AutoCAD COM wrapper
- [FastMCP](https://github.com/anthropics/mcp-python) - MCP server framework
- NumPy/SciPy - Mathematical operations for surface unfolding

---

**AutoCAD MCP Server** - Experimental AutoCAD automation via MCP

*This is a personal project for AutoCAD COM automation experiments.*
