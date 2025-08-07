# MCP Advanced Tools Integration Tests

This document describes the comprehensive test suite for MCP (Model Context Protocol) integration of advanced algorithmic tools, specifically the LSCM (Least Squares Conformal Mapping) surface unfolding algorithm.

## Overview

The `test_mcp_advanced_tools.py` file contains **6 major test classes** with **30+ test methods** that validate:

- ✅ MCP protocol compliance and tool registration
- ✅ JSON schema validation and error handling
- ✅ LSCM algorithm integration correctness
- ✅ Input validation and response structure
- ✅ End-to-end workflow testing
- ✅ Performance and robustness validation

## Test Structure

### 🔧 TestMCPAdvancedToolRegistration
**Purpose**: Validates tool registration within MCP framework

- `test_unfold_surface_lscm_tool_appears_in_list()` - Verifies tool registration
- `test_lscm_tool_description_accuracy()` - Validates description content
- `test_lscm_json_schema_validation()` - Tests JSON schema compliance
- `test_lscm_json_schema_validation_mocked()` - Mocked version for CI/CD

**Key Validations**:
- Tool name: `unfold_surface_lscm`
- Required fields: `vertices`, `triangles`
- Optional fields: `boundary_constraints`, `tolerance`
- Description contains: "LSCM", "manufacturing", "distortion"

### 📡 TestMCPProtocolCompliance
**Purpose**: Ensures MCP protocol standards compliance

- `test_valid_input_schema_compliance()` - Valid input handling
- `test_invalid_input_schema_handling()` - Invalid input error handling
- `test_mcp_textcontent_response_format()` - Response format validation
- `test_error_response_format_standards()` - Error response standards
- `test_missing_arguments_handling()` - Missing argument validation
- `test_none_arguments_handling()` - Null argument handling

**Key Validations**:
- MCP TextContent response format
- JSON response structure
- Error handling consistency

### 🚀 TestAdvancedMCPIntegration
**Purpose**: Tests LSCM algorithm integration through MCP

- `test_successful_lscm_execution_with_valid_mesh()` - Success path testing
- `test_error_handling_for_invalid_inputs()` - Comprehensive error handling
- `test_json_response_validity_and_algorithm_metadata()` - Response validation
- `test_boundary_constraints_integration()` - Constraint handling

**Key Validations**:
- Algorithm execution success
- Metadata completeness
- Performance metrics inclusion

### ✅ TestLSCMInputValidation
**Purpose**: Validates input parameter handling

- `test_vertices_array_validation_3d_coordinates()` - 3D vertex validation
- `test_triangle_indices_validation()` - Triangle index validation
- `test_boundary_constraints_and_tolerance_parameters()` - Parameter validation
- `test_minimum_mesh_requirements()` - Minimum data requirements

**Key Validations**:
- 3D coordinate format [x, y, z]
- Valid triangle indices (0-based)
- Boundary constraint format [vertex_idx, u, v]
- Tolerance parameter bounds

### 📊 TestLSCMResponseStructure
**Purpose**: Validates response structure and content

- `test_success_response_required_fields()` - Success response validation
- `test_error_response_structure()` - Error response validation
- `test_algorithm_metadata_validation()` - Metadata validation
- `test_manufacturing_data_structure()` - Manufacturing data validation
- `test_distortion_metrics_structure()` - Distortion metrics validation

**Expected Success Response Fields**:
```json
{
  "success": true,
  "method": "LSCM",
  "uv_coordinates": [[x1,y1], [x2,y2], ...],
  "triangle_indices": [[i1,j1,k1], ...],
  "pattern_size": [width, height],
  "distortion_metrics": {
    "mean_area_distortion": 1.0,
    "max_area_distortion": 1.0,
    "mean_angle_distortion": 0.1,
    "max_angle_distortion": 0.2,
    "area_distortion_variance": 0.01
  },
  "manufacturing_data": {
    "recommended_material_size": [width, height],
    "distortion_acceptable": true
  },
  "algorithm": "LSCM (Least Squares Conformal Mapping)",
  "performance": {
    "tolerance": 0.001,
    "processing_method": "Advanced mathematical algorithm..."
  }
}
```

**Expected Error Response Fields**:
```json
{
  "success": false,
  "error": "Error description",
  "algorithm": "LSCM (Least Squares Conformal Mapping)",
  "message": "Failed to unfold surface using LSCM algorithm",
  "input_mesh": {
    "vertices_count": 0,
    "triangles_count": 0
  }
}
```

### 🔄 TestMCPEndToEndWorkflow
**Purpose**: Complete workflow testing from registration to response

- `test_complete_workflow_simple_triangle()` - Basic workflow
- `test_complex_surface_processing_workflow()` - Complex surface handling
- `test_boundary_constraints_workflow()` - Constraint workflow
- `test_concurrent_request_handling()` - Concurrency testing
- `test_error_recovery_workflow()` - Error recovery
- `test_performance_monitoring_workflow()` - Performance monitoring

**Key Validations**:
- Complete MCP workflow
- Concurrent request handling
- Error recovery mechanisms
- Performance monitoring

## Test Data Constants

### SIMPLE_TRIANGLE_DATA
```python
{
  "vertices": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [0.5, 1.0, 0.0]],
  "triangles": [[0, 1, 2]],
  "tolerance": 0.001
}
```

### SQUARE_MESH_DATA
```python
{
  "vertices": [[0.0, 0.0, 0.0], [1.0, 0.0, 0.0], [1.0, 1.0, 0.0], [0.0, 1.0, 0.0]],
  "triangles": [[0, 1, 2], [0, 2, 3]],
  "boundary_constraints": [[0, 0.0, 0.0], [1, 1.0, 0.0]],
  "tolerance": 0.001
}
```

### COMPLEX_SURFACE_DATA
```python
{
  "vertices": [9 vertices with slight Z variations],
  "triangles": [8 triangles forming grid pattern],
  "boundary_constraints": [[0, 0.0, 0.0], [2, 2.0, 0.0], [6, 0.0, 2.0]],
  "tolerance": 0.005
}
```

## Requirements

### Dependencies
```toml
[tool.poetry.group.dev.dependencies]
pytest = "^8.3.2"
pytest-asyncio = "^0.21.0"
pytest-mock = "^3.12.0"
numpy = "^2.1.0"
```

### MCP Dependencies
```toml
[tool.poetry.dependencies]
mcp = "^1.0.0"
```

## Running Tests

### Prerequisites
```bash
# Install Poetry environment
poetry install

# Install dev dependencies
poetry install --with dev
```

### Run All MCP Integration Tests
```bash
# Run complete test suite
pytest tests/unit/test_mcp_advanced_tools.py -v

# Run with coverage
pytest tests/unit/test_mcp_advanced_tools.py --cov=src.server --cov-report=html

# Run specific test class
pytest tests/unit/test_mcp_advanced_tools.py::TestMCPAdvancedToolRegistration -v
```

### Run Individual Test Categories
```bash
# Test tool registration
pytest tests/unit/test_mcp_advanced_tools.py::TestMCPAdvancedToolRegistration -v

# Test protocol compliance
pytest tests/unit/test_mcp_advanced_tools.py::TestMCPProtocolCompliance -v

# Test integration
pytest tests/unit/test_mcp_advanced_tools.py::TestAdvancedMCPIntegration -v

# Test end-to-end workflow
pytest tests/unit/test_mcp_advanced_tools.py::TestMCPEndToEndWorkflow -v
```

### Validation Without Full Environment
```bash
# Run minimal validation (no pytest/MCP required)
python3 validate_mcp_tests_minimal.py
```

## Conditional Testing

The test suite includes **graceful fallback** for environments where dependencies are not available:

### MCP Availability
- `@requires_mcp` decorator skips tests when MCP not available
- Mock fixtures provide test structure validation
- Conditional imports prevent import errors

### LSCM Availability
- `@requires_lscm` decorator skips tests when LSCM algorithm not available
- Mock LSCM responses for testing MCP integration without algorithm

## Integration with CI/CD

### GitHub Actions Example
```yaml
name: MCP Integration Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: actions/setup-python@v4
        with:
          python-version: '3.12'
      - name: Install Poetry
        run: pip install poetry
      - name: Install dependencies
        run: poetry install --with dev
      - name: Run MCP integration tests
        run: poetry run pytest tests/unit/test_mcp_advanced_tools.py -v
      - name: Run validation
        run: python3 validate_mcp_tests_minimal.py
```

## Performance Testing

### Test Performance Benchmarks
- **Simple triangle**: < 2 seconds execution
- **Complex surfaces**: < 10 seconds execution  
- **Memory usage**: < 100MB additional
- **Concurrent requests**: 4 simultaneous requests

### Performance Test Methods
- `test_execution_time_small_mesh()`
- `test_memory_usage()`
- `test_large_mesh_handling()`
- `test_concurrent_request_handling()`

## Error Scenarios Tested

### Input Validation Errors
- Missing Z coordinates in vertices
- Invalid triangle indices  
- Malformed boundary constraints
- Non-numeric tolerance values

### Algorithm Errors
- Degenerate triangles (zero area)
- Disconnected mesh components
- Numerical instability cases
- Large coordinate values

### MCP Protocol Errors
- Missing required arguments
- Invalid JSON format
- Timeout scenarios
- Concurrent access conflicts

## Coverage Goals

- **Tool Registration**: 100% coverage
- **Protocol Compliance**: 100% coverage
- **Input Validation**: 95% coverage
- **Error Handling**: 90% coverage
- **Algorithm Integration**: 85% coverage

## Contributing

When adding new tests:

1. Follow naming convention: `test_descriptive_name()`
2. Include both positive and negative test cases
3. Use appropriate decorators (`@requires_mcp`, `@requires_lscm`)
4. Add validation to `validate_mcp_tests_minimal.py`
5. Update this documentation

## Troubleshooting

### Common Issues

**Import Errors**: Use conditional imports and decorators
```python
@requires_mcp
def test_mcp_functionality(self):
    # Test code here
```

**Async Issues**: Use `@pytest.mark.asyncio` for async tests
```python
@pytest.mark.asyncio
async def test_async_functionality(self):
    result = await handle_call_tool(...)
```

**Mock Setup**: Use fixtures for consistent mocking
```python
def test_with_mocks(self, sample_lscm_response):
    # Test code using fixture
```

---

This test suite provides comprehensive validation of MCP integration for advanced algorithmic tools, ensuring reliability, performance, and protocol compliance for production deployment.