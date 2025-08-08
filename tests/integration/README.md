# Integration Test Framework for AutoCAD MCP

## Overview
This directory contains comprehensive integration tests for the AutoCAD MCP Server, ensuring seamless interaction between components and verifying end-to-end functionality.

## Test Categories
- `mcp_tools/`: Tests for individual MCP tool integrations
- `algorithm_integration/`: Validation of complex algorithmic workflows
- `performance_checks/`: Performance and scalability tests
- `error_handling/`: Robustness and error management tests

## Test Configuration
- Framework: pytest
- Coverage: Aim for >90% integration test coverage
- Environment: Requires AutoCAD 2025 and Python 3.12+

## Running Tests
```bash
# Run all integration tests
poetry run pytest tests/integration

# Run specific test category
poetry run pytest tests/integration/mcp_tools

# Generate coverage report
poetry run pytest --cov=src tests/integration
```

## Best Practices
- Each test should be independent
- Mock external dependencies when possible
- Use fixtures for setup and teardown
- Document test cases thoroughly