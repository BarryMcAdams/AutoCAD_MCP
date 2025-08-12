#!/usr/bin/env python3
"""
Standalone Security Manager Test Runner
=======================================

Runs security manager tests without requiring pytest installation.
Validates core functionality and reports test results.
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Import required modules directly to avoid dependency issues
try:
    import importlib.util
    spec = importlib.util.spec_from_file_location(
        "security_manager", 
        project_root / "src" / "mcp_integration" / "security_manager.py"
    )
    security_manager_module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(security_manager_module)
    
    SecurityManager = security_manager_module.SecurityManager
    CodeValidator = security_manager_module.CodeValidator
    SecurityError = security_manager_module.SecurityError
    
    print("✓ Successfully imported SecurityManager modules")
except ImportError as e:
    print(f"✗ Failed to import SecurityManager modules: {e}")
    sys.exit(1)

class TestRunner:
    """Simple test runner for validation without pytest."""
    
    def __init__(self):
        self.passed = 0
        self.failed = 0
        self.errors = []
    
    def run_test(self, test_name, test_func):
        """Run a single test and track results."""
        try:
            test_func()
            print(f"✓ {test_name}")
            self.passed += 1
        except AssertionError as e:
            print(f"✗ {test_name}: {e}")
            self.failed += 1
            self.errors.append((test_name, str(e)))
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            self.failed += 1
            self.errors.append((test_name, f"ERROR: {e}"))
    
    def report(self):
        """Print test results summary."""
        total = self.passed + self.failed
        print("\n" + "="*50)
        print(f"Test Results: {self.passed}/{total} passed")
        
        if self.errors:
            print("\nFailures:")
            for test_name, error in self.errors:
                print(f"  - {test_name}: {error}")
        
        return self.failed == 0


def test_security_manager_initialization():
    """Test SecurityManager basic initialization."""
    sm = SecurityManager()
    assert len(sm.blocked_imports) > 20
    assert len(sm.blocked_builtins) > 10
    assert len(sm.safe_builtins) > 30
    assert sm.max_execution_time == 30.0


def test_validate_safe_code():
    """Test validation of safe Python code."""
    sm = SecurityManager()
    safe_code = """
x = 5
y = 10
result = x + y
print(f"Result: {result}")
"""
    is_safe, violations = sm.validate_python_code(safe_code)
    assert is_safe is True
    assert violations == []


def test_validate_blocked_imports():
    """Test validation blocks dangerous imports."""
    sm = SecurityManager()
    dangerous_imports = ["os", "sys", "subprocess", "pickle"]
    
    for module in dangerous_imports:
        code = f"import {module}"
        is_safe, violations = sm.validate_python_code(code)
        assert is_safe is False, f"Should block import {module}"
        assert len(violations) > 0


def test_validate_blocked_builtins():
    """Test validation blocks dangerous built-ins."""
    sm = SecurityManager()
    dangerous_builtins = ["eval", "exec", "__import__", "open"]
    
    for builtin in dangerous_builtins:
        code = f"{builtin}('test')"
        is_safe, violations = sm.validate_python_code(code)
        assert is_safe is False, f"Should block {builtin}"
        assert len(violations) > 0


def test_validate_infinite_loops():
    """Test validation detects infinite loops."""
    sm = SecurityManager()
    
    # Test while True
    code = "while True:\n    pass"
    is_safe, violations = sm.validate_python_code(code)
    assert is_safe is False
    assert any("infinite" in v.lower() for v in violations)


def test_validate_code_length():
    """Test validation enforces code length limits."""
    sm = SecurityManager()
    
    # Test code exceeding limits - create code longer than max_code_length (10000)
    base_code = "x = 1234567890\n"  # 15 chars per line
    repeat_count = (sm.max_code_length // len(base_code)) + 100  # Ensure we exceed the limit
    long_code = base_code * repeat_count
    
    # Verify the code is actually longer than the limit
    assert len(long_code) > sm.max_code_length, f"Generated code {len(long_code)} not longer than limit {sm.max_code_length}"
    
    is_safe, violations = sm.validate_python_code(long_code)
    assert is_safe is False
    assert any("too long" in v.lower() for v in violations)


def test_validate_empty_code():
    """Test validation rejects empty code."""
    sm = SecurityManager()
    
    empty_codes = ["", "   ", "\n\n", "\t\t"]
    for code in empty_codes:
        is_safe, violations = sm.validate_python_code(code)
        assert is_safe is False
        assert any("empty" in v.lower() for v in violations)


def test_get_safe_builtins():
    """Test safe builtins dictionary creation."""
    sm = SecurityManager()
    safe_builtins = sm.get_safe_builtins()
    
    # Verify safe functions are included
    required_safe = ["print", "len", "range", "sum"]
    for func in required_safe:
        assert func in safe_builtins, f"Missing safe builtin: {func}"
    
    # Verify dangerous functions are excluded
    dangerous = ["eval", "exec", "open", "__import__"]
    for func in dangerous:
        assert func not in safe_builtins, f"Dangerous builtin present: {func}"


def test_create_safe_globals():
    """Test creation of safe global namespace."""
    sm = SecurityManager()
    safe_globals = sm.create_safe_globals()
    
    # Verify required keys
    required_keys = ["__builtins__", "__name__", "__doc__", "math"]
    for key in required_keys:
        assert key in safe_globals, f"Missing key: {key}"
    
    # Verify math module functions
    math_obj = safe_globals["math"]
    math_functions = ["sin", "cos", "sqrt", "pi"]
    for func in math_functions:
        assert hasattr(math_obj, func), f"Missing math function: {func}"


def test_get_security_report():
    """Test security configuration report."""
    sm = SecurityManager()
    report = sm.get_security_report()
    
    required_keys = [
        "blocked_imports_count",
        "blocked_builtins_count", 
        "blocked_attributes_count",
        "safe_builtins_count",
        "validation_enabled",
        "sandboxing_enabled"
    ]
    
    for key in required_keys:
        assert key in report, f"Missing report key: {key}"
    
    assert report["validation_enabled"] is True
    assert report["sandboxing_enabled"] is True


def test_code_validator():
    """Test CodeValidator AST visitor."""
    sm = SecurityManager()
    validator = CodeValidator(sm)
    
    assert validator.security_manager is sm
    assert validator.violations == []
    
    # Test with dangerous import
    import ast
    code = "import os"
    tree = ast.parse(code)
    validator.visit(tree)
    assert len(validator.violations) > 0


def test_string_pattern_validation():
    """Test string-based validation patterns."""
    sm = SecurityManager()
    
    dangerous_patterns = [
        "os.system('rm -rf /')",
        "subprocess.popen('malicious')",
        "__import__('dangerous')",
        "exec('malicious code')"
    ]
    
    for pattern in dangerous_patterns:
        violations = sm._validate_code_strings(pattern)
        assert len(violations) > 0, f"Should detect pattern: {pattern}"


def test_security_error():
    """Test SecurityError exception."""
    error_msg = "Test security violation"
    error = SecurityError(error_msg)
    
    assert str(error) == error_msg
    assert isinstance(error, Exception)


def main():
    """Run all tests."""
    print("Security Manager Standalone Test Suite")
    print("=====================================\n")
    
    runner = TestRunner()
    
    # Run all tests
    test_functions = [
        ("SecurityManager Initialization", test_security_manager_initialization),
        ("Validate Safe Code", test_validate_safe_code),
        ("Validate Blocked Imports", test_validate_blocked_imports),
        ("Validate Blocked Builtins", test_validate_blocked_builtins),
        ("Validate Infinite Loops", test_validate_infinite_loops),
        ("Validate Code Length", test_validate_code_length),
        ("Validate Empty Code", test_validate_empty_code),
        ("Get Safe Builtins", test_get_safe_builtins),
        ("Create Safe Globals", test_create_safe_globals),
        ("Get Security Report", test_get_security_report),
        ("Code Validator", test_code_validator),
        ("String Pattern Validation", test_string_pattern_validation),
        ("Security Error", test_security_error),
    ]
    
    for test_name, test_func in test_functions:
        runner.run_test(test_name, test_func)
    
    success = runner.report()
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())