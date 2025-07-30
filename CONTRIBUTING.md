# Contributing to AutoCAD MCP Server

Thank you for your interest in contributing to the AutoCAD MCP Server! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

### Prerequisites
- Python 3.12+
- AutoCAD 2025 (recommended, compatible with 2021-2024)
- Git
- VS Code (recommended)

### Development Setup
1. **Fork and clone the repository:**
   ```bash
   git clone https://github.com/your-username/AutoCAD_MCP.git
   cd AutoCAD_MCP
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   pip install -r requirements-prod.txt  # For additional dev tools
   ```

3. **Run tests to verify setup:**
   ```bash
   pytest tests/
   ```

## 🤝 How to Contribute

### Reporting Issues
- Use GitHub Issues to report bugs or request features
- Provide detailed information including:
  - AutoCAD version
  - Python version
  - Operating system
  - Steps to reproduce
  - Expected vs actual behavior

### Submitting Changes
1. **Create a feature branch:**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes following our coding standards**

3. **Add or update tests as needed**

4. **Run the test suite:**
   ```bash
   pytest tests/
   python -m ruff check src/
   python -m black src/
   ```

5. **Commit your changes:**
   ```bash
   git commit -m "Add feature: description of your changes"
   ```

6. **Push and create a pull request**

## 📝 Coding Standards

### Python Style
- Follow PEP 8 guidelines
- Use Black formatter for consistent formatting
- Use Ruff linter for code quality
- Add type hints to all functions
- Write comprehensive docstrings

### Testing
- Maintain >90% test coverage
- Write unit tests for new functionality
- Include integration tests where appropriate
- Use the mock AutoCAD system for testing

### Documentation
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Update API documentation as needed

## 🧪 Testing

### Running Tests
```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src

# Run specific test files
pytest tests/test_specific_feature.py
```

### Test Categories
- **Unit Tests**: Test individual components
- **Integration Tests**: Test component interactions
- **Mock Tests**: Use mock AutoCAD for offline testing

## 🏗️ Project Structure

```
AutoCAD_MCP/
├── src/                    # Main source code
│   ├── enhanced_autocad/   # Core AutoCAD integration
│   ├── mcp_integration/    # MCP protocol implementation
│   ├── ai_features/        # AI-powered features
│   ├── enterprise/         # Enterprise capabilities
│   └── testing/           # Testing framework
├── tests/                 # Test suite
├── k8s/                   # Kubernetes deployment
├── DELETED/               # Archived development files
└── requirements*.txt      # Dependencies
```

## 🔒 Security

- Never commit sensitive information (API keys, passwords)
- Follow secure coding practices
- Run security scans before submitting PRs
- Report security issues privately

## 📋 Code Review Process

1. **Automated Checks**: All PRs must pass automated tests and linting
2. **Peer Review**: At least one maintainer review required
3. **Security Review**: Security-sensitive changes need additional review
4. **Documentation**: User-facing changes must include documentation updates

## 🚀 Release Process

The project follows semantic versioning (SemVer):
- **Major**: Breaking changes
- **Minor**: New features (backward compatible)
- **Patch**: Bug fixes

## 💬 Community

- **GitHub Discussions**: For questions and general discussion
- **GitHub Issues**: For bug reports and feature requests
- **Pull Requests**: For code contributions

## 📄 License

By contributing to this project, you agree that your contributions will be licensed under the MIT License.

---

Thank you for contributing to the AutoCAD MCP Server! Your contributions help make AutoCAD development more efficient and enjoyable for everyone.