# AutoCAD MCP Server

**A Development Platform for AutoCAD Automation Research**

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/flask-3.0-green.svg)](https://flask.palletsprojects.com/)
[![AutoCAD 2025](https://img.shields.io/badge/AutoCAD-2025-red.svg)](https://www.autodesk.com/products/autocad)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

The AutoCAD MCP Server is a research and development platform for AutoCAD 2025 automation, featuring experimental 3D surface unfolding algorithms, automated dimensioning prototypes, and material optimization research tools through a REST API.

**🚨 Current Status: Development Platform**
- ✅ **Server Infrastructure**: Fully functional with 19+ REST endpoints
- ✅ **Core Algorithms**: LSCM surface unfolding and pattern optimization implemented
- ✅ **AutoCAD Integration**: COM interface with robust error handling
- 🔬 **Research Stage**: Algorithms and features under active development
- 📋 **Testing Required**: AutoCAD integration needs validation on target systems

## 🚀 Quick Start

### Prerequisites
- **AutoCAD 2025** (full version) installed and activated
- **Python 3.12** or higher
- **Windows OS** (required for AutoCAD COM interface)
- **Poetry** or **uv** for dependency management

### Installation Options

#### Option 1: Claude Desktop Integration (Recommended)

This project can be integrated with Claude Desktop as a Model Context Protocol (MCP) server for AI-assisted AutoCAD automation.

**Claude Desktop Setup:**

1. **Install from gitmcp.io (easiest method):**
   - Visit [gitmcp.io/BarryMcAdams/AutoCAD_MCP](https://gitmcp.io/BarryMcAdams/AutoCAD_MCP)
   - Follow the installation instructions provided

2. **Manual Installation:**
   ```bash
   # Clone the repository
   git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
   cd AutoCAD_MCP
   
   # Install dependencies
   uv sync  # or: poetry install
   
   # Test MCP server
   uv run python src/server.py  # or: poetry run python src/server.py
   ```

3. **Configure Claude Desktop:**
   
   Add to your Claude Desktop MCP configuration:
   ```json
   {
     "mcpServers": {
       "autocad-mcp": {
         "command": "uv",
         "args": ["run", "python", "src/server.py"],
         "cwd": "C:\\path\\to\\your\\AutoCAD_MCP",
         "env": {
           "PYTHONPATH": "src",
           "PYTHONIOENCODING": "utf-8"
         }
       }
     }
   }
   ```

4. **Start AutoCAD 2025:**
   - Launch AutoCAD 2025
   - Open or create a drawing
   - Start a new Claude Desktop conversation

5. **Test MCP Integration:**
   Ask Claude: *"Check the status of the AutoCAD MCP server and draw a line from origin to point (100, 100, 0)"*

#### Option 2: Standalone REST API Server

1. **Clone and install:**
   ```bash
   git clone https://github.com/BarryMcAdams/AutoCAD_MCP.git
   cd AutoCAD_MCP
   poetry install
   ```

2. **Start AutoCAD 2025:**
   - Launch AutoCAD 2025
   - Open or create a drawing with 3D surfaces

3. **Run the Flask server:**
   ```bash
   poetry run python src/mcp_server.py  # For REST API mode
   ```

4. **Test the connection:**
   ```bash
   curl http://localhost:5001/health
   # Expected response: {"status":"ok","success":true,"timestamp":"...","version":"1.0.0"}
   ```

### Available MCP Tools (Claude Desktop)

When integrated with Claude Desktop, the following AutoCAD tools are available for natural language interaction:

- **draw_line** - Draw lines between 3D points
- **draw_circle** - Create circles with center and radius
- **extrude_profile** - Create 3D solids by extruding 2D profiles
- **revolve_profile** - Create 3D solids by revolving profiles around axes
- **list_entities** - List all entities in the current AutoCAD drawing
- **get_entity_info** - Get detailed information about specific entities
- **server_status** - Check MCP server and AutoCAD connection status

**Example MCP Commands:**
- *"Draw a line from origin to (100, 100, 0)"*
- *"Create a circle at (50, 50, 0) with radius 25"*  
- *"List all entities in the current drawing"*
- *"Check if the MCP server is connected to AutoCAD"*

### First API Call (REST Mode)

Create a simple line in AutoCAD:
```bash
curl -X POST http://localhost:5001/draw/line \
  -H "Content-Type: application/json" \
  -d '{
    "start_point": [0, 0, 0],
    "end_point": [100, 100, 0]
  }'
```

## 🎯 Key Features

### 🔧 Advanced Surface Unfolding (Experimental)
- **LSCM Algorithm**: Least Squares Conformal Mapping for 3D surface parameterization
- **Geodesic Calculations**: Research-stage fold line placement algorithms
- **Multiple Methods**: Simple grid, advanced LSCM, and hybrid approaches
- **Quality Validation**: Distortion measurement and analysis tools

### 📐 Automated Dimensioning (Prototype)
- **Linear & Angular Dimensions**: Basic dimensioning functionality
- **Manufacturing Drawings**: Template-based technical drawing generation
- **Text Annotations**: Automated manufacturing notes
- **Layer Management**: CAD layer organization tools

### 📦 Pattern Optimization (Research)
- **Material Nesting**: Experimental pattern placement algorithms
- **Multiple Algorithms**: Best-fit, genetic algorithm research implementations
- **Cost Optimization**: Material usage calculation tools
- **Standard Materials**: Configurable material specifications

### ⚡ Batch Processing (Development)
- **Multi-Surface Processing**: Batch operation framework
- **Workflow Integration**: Research-stage automation pipelines
- **Scalability Testing**: Performance analysis tools
- **Error Handling**: Comprehensive logging and recovery mechanisms

## 📚 API Documentation

### Basic Drawing Operations

#### Create Line
```http
POST /draw/line
Content-Type: application/json

{
  "start_point": [0, 0, 0],
  "end_point": [100, 100, 0]
}
```

#### Create Circle
```http
POST /draw/circle
Content-Type: application/json

{
  "center": [50, 50, 0],
  "radius": 25
}
```

### 3D Operations

#### Extrude Profile
```http
POST /draw/extrude
Content-Type: application/json

{
  "profile_points": [[0,0], [100,0], [100,50], [0,50]],
  "extrude_height": 25
}
```

#### Boolean Union
```http
POST /draw/boolean-union
Content-Type: application/json

{
  "entity_ids": [12345, 67890]
}
```

### Surface Unfolding

#### Basic Unfolding
```http
POST /surface/unfold
Content-Type: application/json

{
  "entity_id": 12345,
  "tolerance": 0.01
}
```

#### Advanced LSCM Unfolding
```http
POST /surface/unfold-advanced
Content-Type: application/json

{
  "entity_id": 12345,
  "algorithm": "lscm",
  "tolerance": 0.001,
  "generate_fold_lines": true
}
```

### Dimensioning

#### Linear Dimension
```http
POST /dimension/linear
Content-Type: application/json

{
  "start_point": [0, 0, 0],
  "end_point": [100, 0, 0],
  "dimension_line_point": [50, -15, 0]
}
```

#### Manufacturing Drawing
```http
POST /dimension/manufacturing-drawing
Content-Type: application/json

{
  "pattern_data": {
    "pattern_bounds": {"min": [0,0], "max": [100,50]},
    "fold_lines": [...],
    "method": "LSCM"
  }
}
```

### Pattern Optimization

#### Optimize Nesting
```http
POST /pattern/optimize-nesting
Content-Type: application/json

{
  "patterns": [
    {
      "id": "part_1",
      "width": 100,
      "height": 50,
      "rotation_allowed": true
    }
  ],
  "material_sheets": [
    {
      "width": 1219.2,
      "height": 2438.4,
      "material_type": "steel"
    }
  ],
  "algorithm": "best_fit_decreasing"
}
```

#### Get Standard Materials
```http
GET /pattern/material-sheets
```

### Batch Processing

#### Batch Surface Unfolding
```http
POST /batch/surface-unfold
Content-Type: application/json

{
  "entity_ids": [12345, 67890, 11111],
  "algorithm": "lscm",
  "create_manufacturing_drawings": true,
  "optimize_material_usage": true,
  "material_sheets": [
    {"width": 1219.2, "height": 2438.4, "material_type": "steel"}
  ]
}
```

## 🏗️ Architecture

### System Components

```
AutoCAD MCP Server (Development Platform)
├── Flask REST API (19+ endpoints) ✅ Functional
├── AutoCAD COM Integration ✅ Implemented
├── Research Algorithms
│   ├── LSCM Surface Unfolding 🔬 Experimental
│   ├── Geodesic Path Calculation 🔬 Research
│   └── Pattern Optimization 🔬 Prototype
├── Development Features
│   ├── Automated Dimensioning 🚧 In Progress
│   ├── Technical Drawing Generation 🚧 Basic
│   └── Material Optimization 🔬 Research
└── Testing Tools
    ├── Batch Processing Framework 🚧 Development
    ├── Quality Validation Tools 🔬 Experimental
    └── Performance Monitoring ✅ Basic
```

### File Structure

```
src/
├── server.py                 # Main Flask application
├── utils.py                  # AutoCAD integration utilities
├── dimensioning.py           # Dimensioning and annotation system
├── pattern_optimization.py   # Material nesting algorithms
├── algorithms/
│   ├── lscm.py              # LSCM surface unfolding
│   ├── geodesic.py          # Geodesic path calculations
│   └── mesh_utils.py        # Triangle mesh processing
├── decorators.py            # Request handling decorators
└── config.py               # Configuration management
```

## 🎯 Use Cases

### Manufacturing & Production
- **Sheet Metal Fabrication**: Unfold complex 3D surfaces for cutting
- **Architectural Panels**: Generate patterns for building facades
- **Product Packaging**: Create unfolded patterns for boxes and containers
- **Aerospace Components**: Precision unfolding for aircraft panels

### Engineering Applications
- **Technical Documentation**: Automated manufacturing drawing generation
- **Cost Estimation**: Material usage optimization for project planning
- **Quality Control**: Distortion analysis and tolerance validation
- **Design Optimization**: Minimize material waste in production

### Integration Scenarios
- **CAM Software**: Feed optimized patterns to cutting systems
- **ERP Integration**: Material cost and usage reporting
- **PLM Systems**: Technical drawing management and versioning
- **Manufacturing Execution**: Production workflow automation

## 📊 Development Status & Testing

### ✅ Validated Components
- **Server Infrastructure**: Flask server starts successfully on port 5001
- **Health Monitoring**: `/health` endpoint returns proper JSON responses
- **AutoCAD Detection**: `/acad-status` correctly identifies connection state
- **Core Algorithms**: LSCM algorithm imports and loads without errors
- **API Endpoints**: 19+ REST endpoints confirmed available and responding

### 🔬 Research Performance Targets
- **Distortion Measurement**: LSCM algorithm includes distortion calculation
- **Processing Goals**: <1 second for simple operations, <10 seconds for complex unfolding
- **Scalability Research**: Testing with various mesh sizes and complexities
- **Integration Testing**: Ongoing validation with AutoCAD 2025 instances

### 🚧 Development Priorities
- **AutoCAD Integration**: Full COM interface testing with real AutoCAD instances
- **Algorithm Validation**: Performance benchmarking and accuracy testing
- **User Interface**: API documentation and example implementations
- **Production Readiness**: Comprehensive testing and stability improvements

## 🔧 Configuration

### Environment Variables
```bash
# Server Configuration
HOST=localhost
PORT=5001
DEBUG=false

# Logging
LOG_LEVEL=INFO
LOG_FILE=logs/autocad_mcp.log

# AutoCAD Settings
AUTOCAD_TIMEOUT=30
MAX_BATCH_SIZE=100
```

### config.py Settings
```python
class Config:
    # Server settings
    HOST = os.getenv('HOST', 'localhost')
    PORT = int(os.getenv('PORT', 5001))
    DEBUG = os.getenv('DEBUG', 'false').lower() == 'true'
    
    # Performance settings
    MAX_BATCH_SIZE = int(os.getenv('MAX_BATCH_SIZE', 100))
    PROCESSING_TIMEOUT = int(os.getenv('PROCESSING_TIMEOUT', 300))
    
    # Quality settings
    DEFAULT_TOLERANCE = 0.001
    MAX_DISTORTION_THRESHOLD = 0.1
```

## 🧪 Testing & Validation

### Infrastructure Testing ✅ Completed
```bash
# Test server startup and health
poetry install
poetry run python src/server.py
curl http://localhost:5001/health
# Expected: {"status":"ok","success":true,"timestamp":"...","version":"1.0.0"}

# Test AutoCAD connection detection
curl http://localhost:5001/acad-status
# Expected: Connection status or "AutoCAD is not connected" message
```

### Development Testing 🚧 In Progress
```bash
# Run available tests (note: some tests have import path issues)
poetry run pytest

# Test core algorithm loading
python -c "from src.algorithms.lscm import LSCMSolver; print('LSCM loads successfully')"

# Test drawing operations (requires AutoCAD running)
curl -X POST http://localhost:5001/draw/line \
  -H "Content-Type: application/json" \
  -d '{"start_point": [0,0,0], "end_point": [100,100,0]}'
```

### Integration Testing 📋 Required
- **AutoCAD 2025**: Full testing with actual AutoCAD installation
- **Real Surfaces**: Validation with complex 3D surfaces and meshes
- **Performance**: Benchmarking with large datasets
- **Error Handling**: Edge case testing and recovery mechanisms

## 📖 Examples

### Complete Workflow Example

1. **Create a 3D Surface**
   ```http
   POST /surface/3d-mesh
   {
     "m_size": 4,
     "n_size": 4,
     "coordinates": [/* 16 3D points */]
   }
   ```

2. **Unfold the Surface**
   ```http
   POST /surface/unfold-advanced
   {
     "entity_id": 12345,
     "algorithm": "lscm",
     "generate_fold_lines": true
   }
   ```

3. **Create Manufacturing Drawing**
   ```http
   POST /dimension/manufacturing-drawing
   {
     "pattern_data": {/* unfold result */}
   }
   ```

4. **Optimize Material Usage**
   ```http
   POST /pattern/optimize-from-unfolding
   {
     "unfolding_results": [{/* unfold result */}],
     "material_sheets": [{/* steel sheet specs */}]
   }
   ```

### Python Integration Example

```python
import requests
import json

class AutoCADMCPClient:
    def __init__(self, base_url="http://localhost:5001"):
        self.base_url = base_url
    
    def unfold_surface(self, entity_id, algorithm="lscm"):
        response = requests.post(
            f"{self.base_url}/surface/unfold-advanced",
            json={
                "entity_id": entity_id,
                "algorithm": algorithm,
                "tolerance": 0.001,
                "generate_fold_lines": True
            }
        )
        return response.json()
    
    def optimize_patterns(self, unfolding_results, material_sheets):
        response = requests.post(
            f"{self.base_url}/pattern/optimize-from-unfolding",
            json={
                "unfolding_results": unfolding_results,
                "material_sheets": material_sheets
            }
        )
        return response.json()

# Usage
client = AutoCADMCPClient()
unfold_result = client.unfold_surface(12345)
optimization = client.optimize_patterns([unfold_result], [steel_sheet])
```

## 🚨 Troubleshooting

### Common Issues

#### AutoCAD Connection Failed
```
Error: Could not connect to AutoCAD instance
```
**Solutions:**
- Ensure AutoCAD 2025 is running
- Check that a drawing is open in AutoCAD
- Verify no other applications are using AutoCAD COM interface

#### Entity Not Found
```
Error: Entity with ID 12345 not found
```
**Solutions:**
- Verify the entity exists in the current drawing
- Check that the entity is a valid 3D surface or mesh
- Use AutoCAD's Properties panel to confirm the entity ID

#### High Distortion in Unfolding
```
Warning: Surface distortion exceeds tolerance (0.15% > 0.1%)
```
**Solutions:**
- Try the LSCM algorithm for complex surfaces
- Increase tolerance if acceptable for your application
- Consider mesh simplification for highly complex surfaces

#### Material Optimization Failed
```
Error: No valid patterns could be created
```
**Solutions:**
- Check that unfolding results contain valid pattern data
- Verify material sheet dimensions are sufficient
- Ensure pattern dimensions are reasonable for the material

### Debug Mode

Enable debug logging:
```python
# In config.py
DEBUG = True
LOG_LEVEL = "DEBUG"
```

Check logs:
```bash
tail -f logs/autocad_mcp.log
```

### Performance Issues

#### Slow Processing
- **Large Meshes**: Use mesh optimization before unfolding
- **Complex Surfaces**: Consider increasing tolerance slightly
- **Batch Operations**: Process in smaller batches if memory is limited

#### Memory Usage
- **Monitor**: Use Task Manager to monitor memory usage
- **Optimize**: Close unnecessary AutoCAD drawings
- **Limit**: Set MAX_BATCH_SIZE to appropriate value for your system

## 🤝 Contributing

### Development Setup
1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Install development dependencies: `poetry install --with dev`
4. Make changes and add tests
5. Run tests: `poetry run pytest`
6. Submit a pull request

### Code Style
- Follow PEP 8 Python style guidelines
- Use Black formatter: `poetry run black .`
- Check with Ruff linter: `poetry run ruff check .`
- Add type hints to all functions
- Include comprehensive docstrings

### Testing Requirements
- Add unit tests for new functionality
- Maintain >90% test coverage
- Include integration tests for API endpoints
- Test with real AutoCAD entities when possible

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **AutoCAD COM API** - Foundation for CAD integration
- **SciPy Community** - Advanced mathematical algorithms
- **Flask Team** - Excellent web framework
- **Manufacturing Community** - Real-world requirements and feedback

## 📞 Support

### Documentation
- **API Reference**: Complete endpoint documentation with examples
- **User Stories**: Real-world use cases and scenarios
- **Technical Guide**: Implementation details and architecture

### Community
- **Issues**: [GitHub Issues](https://github.com/BarryMcAdams/AutoCAD_MCP/issues)
- **Discussions**: [GitHub Discussions](https://github.com/BarryMcAdams/AutoCAD_MCP/discussions)

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=BarryMcAdams/AutoCAD_MCP&type=Date)](https://star-history.com/#BarryMcAdams/AutoCAD_MCP&Date)

---

**AutoCAD MCP Server** - Research Platform for AutoCAD Automation

*Development platform for CAD automation research and experimentation*

## 📈 Project Status Summary

**January 2025**: Initial development and infrastructure fixes  
**August 2025**: Testing validation completed  
- ✅ Server infrastructure functional
- ✅ Core algorithms implemented  
- ✅ AutoCAD COM integration working
- 🔬 Research algorithms under development
- 📋 Full AutoCAD integration testing required

This is an active research and development project. Contributors and researchers welcome!