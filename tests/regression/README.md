# Basic MCP Tools Regression Test Suite

Comprehensive regression tests to ensure the 7 existing basic MCP tools continue working correctly after the advanced LSCM algorithm integration.

## Overview

This test suite validates that advanced algorithm integration hasn't broken existing functionality. It tests:

### Basic MCP Tools (7 tools)
1. `draw_line` - Draw lines between 3D points
2. `draw_circle` - Draw circles with center and radius  
3. `extrude_profile` - Create 3D solids from 2D profiles
4. `revolve_profile` - Create 3D solids by revolution
5. `list_entities` - List all drawing entities
6. `get_entity_info` - Get detailed entity information
7. `server_status` - Check server and AutoCAD connection

### Test Categories

#### TestBasicToolsRegression
- ✅ Each tool executes successfully
- ✅ Response format validation
- ✅ Performance baseline preservation
- ✅ AutoCAD interaction verification

#### TestMCPServerStability  
- ✅ Server startup/shutdown with advanced tools
- ✅ Tool discovery includes all tools
- ✅ Memory usage baseline validation
- ✅ Mixed workload stability

#### TestBackwardCompatibility
- ✅ Response format consistency
- ✅ Field type validation
- ✅ Error handling compatibility
- ✅ Client integration preservation

#### TestConcurrentExecution
- ✅ Basic tools work during advanced operations
- ✅ No resource contention
- ✅ Proper error isolation
- ✅ Thread safety validation

## Success Criteria

✅ **All 7 basic tools execute successfully**
✅ **No performance degradation >10%**  
✅ **Memory usage increase <20MB baseline**
✅ **Server remains stable under mixed workloads**

## Usage

### Quick Test Run
```bash
# Run all regression tests
python tests/regression/run_regression_tests.py

# Run with detailed output
python tests/regression/run_regression_tests.py --detailed
```

### Specific Test Categories
```bash
# Performance regression only
python tests/regression/run_regression_tests.py --performance-only

# Memory stability only  
python tests/regression/run_regression_tests.py --memory-check

# Save results to file
python tests/regression/run_regression_tests.py --output regression_results.json
```

### Using pytest
```bash
# Run all regression tests
pytest tests/regression/ -v

# Run specific test class
pytest tests/regression/test_basic_tools_regression.py::TestBasicToolsRegression -v

# Run with performance focus
pytest tests/regression/ -k "performance" -v

# Run with coverage report
pytest tests/regression/ --cov=src --cov-report=html
```

## Test Configuration

### Performance Thresholds
```python
PERFORMANCE_THRESHOLDS = {
    "basic_tool_max_time": 0.1,      # 100ms for basic operations
    "server_status_max_time": 0.05,  # 50ms for status check
    "memory_increase_limit": 20,     # 20MB memory increase limit
    "total_memory_limit": 50,        # 50MB total memory limit
}
```

### Test Data
- **Mock AutoCAD instances** for consistent testing
- **Predefined entity sets** for list/query operations
- **Standard geometric parameters** for drawing operations
- **Thread-safe execution** for concurrency tests

## Expected Output

### Successful Run
```
AutoCAD MCP Basic Tools Regression Test Suite
============================================================
Testing 7 basic MCP tools after advanced LSCM integration
Initial memory usage: 45.2 MB

Running Basic Tool Functionality tests...
  ✅ PASS - 7/7 basic tools working correctly
    • draw_line: ✅ 0.008s
    • draw_circle: ✅ 0.006s
    • extrude_profile: ✅ 0.012s
    • revolve_profile: ✅ 0.015s
    • list_entities: ✅ 0.004s
    • get_entity_info: ✅ 0.003s
    • server_status: ✅ 0.002s

Running MCP Server Stability tests...
  ✅ PASS - Server stability check passed - 12 tools loaded

Running Backward Compatibility tests...
  ✅ PASS - Backward compatibility maintained

Running Concurrent Execution tests...
  ✅ PASS - Concurrent execution working

Running Performance Regression tests...
  ✅ PASS - Performance within limits

Running Memory Stability tests...
  ✅ PASS - Memory stable (+2.1 MB)

Regression Test Summary
========================================
Total time: 1.23 seconds
Tests run: 6
Passed: 6
Failed: 0
Success rate: 100.0%
Memory usage: 45.2 → 47.3 MB (+2.1 MB)

🎉 ALL REGRESSION TESTS PASSED
✅ Basic MCP tools continue working correctly after advanced LSCM integration
```

### Failure Example
```
Running Basic Tool Functionality tests...
  ❌ FAIL - 5/7 basic tools working correctly
    • draw_line: ✅ 0.008s
    • draw_circle: Exception - 'AddCircle' not found
    • extrude_profile: ✅ 0.012s

❌ REGRESSION DETECTED
⚠️  Some basic MCP tools may have issues after advanced integration

Failed tests:
  • Basic Tool Functionality: 5/7 basic tools working correctly
```

## Test Architecture

### Mock Strategy
- **Comprehensive AutoCAD mocking** to ensure consistent test environment
- **Entity simulation** with realistic ObjectIDs and properties
- **Thread-safe mocks** for concurrency testing
- **Configurable failure scenarios** for error testing

### Performance Monitoring
- **Execution time measurement** for each tool
- **Memory usage tracking** throughout test suite
- **Baseline comparison** with pre-integration performance
- **Regression detection** with configurable thresholds

### Validation Approach
- **Response format verification** against expected schemas
- **Field type checking** for backward compatibility
- **Error structure validation** for consistent error handling
- **Integration point testing** for AutoCAD interactions

## Integration with CI/CD

### GitHub Actions
```yaml
- name: Run Regression Tests
  run: |
    python tests/regression/run_regression_tests.py --output regression_results.json
    
- name: Upload Regression Results
  uses: actions/upload-artifact@v3
  with:
    name: regression-test-results
    path: regression_results.json
```

### Quality Gates
- **All basic tools must pass** - No exceptions
- **Performance regression <10%** - Warning at 5%
- **Memory increase <20MB** - Warning at 10MB
- **Zero critical failures** - Any critical failure fails the build

## Troubleshooting

### Common Issues

#### Tool Not Found
```
Tool 'draw_line' not found in handler registry
```
**Solution**: Check that `src/mcp_server.py` properly registers all basic tools.

#### Performance Regression
```
draw_circle: avg 0.150s exceeds 0.100s
```
**Solution**: Check for blocking operations or resource contention in tool implementation.

#### Memory Leak Detection
```
Potential memory leak: 25.3 MB increase during test
```
**Solution**: Review object cleanup and reference management in recent changes.

#### AutoCAD Connection Issues
```
Cannot connect to AutoCAD: AutoCAD not running
```
**Solution**: Ensure mocks are properly configured for the test environment.

## Contributing

### Adding New Regression Tests
1. Create test methods in `TestBasicToolsRegression`
2. Use consistent mock setup patterns
3. Include performance and memory validation
4. Update success criteria documentation

### Test Naming Convention
- `test_[tool_name]_regression()` - Individual tool tests
- `test_[category]_validation()` - Category validation tests
- `test_[scenario]_compatibility()` - Compatibility tests

### Mock Guidelines
- Use `patch('src.utils.get_autocad_instance')` for AutoCAD mocking
- Create realistic entity objects with proper ObjectIDs
- Include thread-safety for concurrent tests
- Maintain consistent response formats

## Maintenance

### Regular Updates
- **Performance baselines** should be updated with significant improvements
- **Memory thresholds** may need adjustment with new features
- **Test data** should reflect realistic usage patterns
- **Mock objects** should match current AutoCAD API

### Version Compatibility
- Tests are designed for **AutoCAD 2025** compatibility
- Mock objects simulate **pyautocad** and **win32com** interfaces
- Response formats follow **MCP protocol** standards
- Error handling matches **AutoCAD COM** behavior

---

*This regression test suite ensures the reliability and stability of basic MCP functionality as the system evolves with advanced features.*