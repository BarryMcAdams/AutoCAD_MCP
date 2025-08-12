#!/usr/bin/env python3
"""
Simple test runner for validation engine tests.
Can be used when pytest is not available in the environment.
"""

import sys
import os
import traceback
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def run_basic_validation_tests():
    """Run basic validation tests to verify functionality."""
    print("=" * 60)
    print("VALIDATION ENGINE TEST SUITE")
    print("=" * 60)
    
    try:
        from src.code_generation.validation_engine import ValidationEngine, ValidationIssue, ValidationResult
        print("✓ Successfully imported validation engine classes")
    except ImportError as e:
        print(f"✗ Failed to import validation engine classes: {e}")
        return False
    
    engine = ValidationEngine()
    test_results = []
    
    # Test 1: Basic initialization
    print("\nTest 1: Basic Initialization")
    try:
        assert engine.python_validators is not None
        assert engine.autolisp_validators is not None
        assert engine.vba_validators is not None
        assert engine.common_patterns is not None
        print("✓ PASSED: ValidationEngine initialized correctly")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 2: Python validation
    print("\nTest 2: Python Code Validation")
    try:
        valid_python = '''
import logging
def main():
    try:
        print("Hello World")
    except Exception as e:
        logging.error(f"Error: {e}")

if __name__ == "__main__":
    main()
'''
        result = engine.validate_code(valid_python, "python")
        assert isinstance(result, ValidationResult)
        assert result.language == "python"
        assert result.quality_score > 0
        print(f"✓ PASSED: Python validation (Score: {result.quality_score})")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 3: Syntax error detection
    print("\nTest 3: Syntax Error Detection")
    try:
        invalid_python = "def broken(\n    print('missing parenthesis')"
        result = engine.validate_code(invalid_python, "python")
        syntax_errors = [issue for issue in result.issues if issue.category == "syntax"]
        assert len(syntax_errors) > 0
        assert not result.valid
        print(f"✓ PASSED: Detected {len(syntax_errors)} syntax errors")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 4: Security pattern detection
    print("\nTest 4: Security Pattern Detection")
    try:
        insecure_code = '''
password = "secret123"
api_key = "abc123xyz"
'''
        result = engine.validate_code(insecure_code, "python")
        security_issues = [issue for issue in result.issues if issue.category == "security"]
        assert len(security_issues) > 0
        print(f"✓ PASSED: Detected {len(security_issues)} security issues")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 5: AutoLISP validation
    print("\nTest 5: AutoLISP Code Validation")
    try:
        autolisp_code = '''
(defun c:testcmd ()
  ;; Test command
  (princ "Hello AutoLISP")
  (princ)
)
'''
        result = engine.validate_code(autolisp_code, "autolisp")
        assert isinstance(result, ValidationResult)
        assert result.language == "autolisp"
        print(f"✓ PASSED: AutoLISP validation (Score: {result.quality_score})")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 6: AutoLISP parentheses balance
    print("\nTest 6: AutoLISP Parentheses Balance")
    try:
        unbalanced_lisp = "(defun test ( (print 'missing close')"
        result = engine.validate_code(unbalanced_lisp, "autolisp")
        syntax_issues = [issue for issue in result.issues if issue.category == "syntax"]
        assert any("parentheses" in issue.message.lower() for issue in syntax_issues)
        print("✓ PASSED: Detected unbalanced parentheses")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 7: VBA validation
    print("\nTest 7: VBA Code Validation")
    try:
        vba_code = '''
Option Explicit

Sub TestSub()
    On Error GoTo ErrorHandler
    
    Dim x As Integer
    x = 5
    
    Exit Sub
    
ErrorHandler:
    ' Error handling
End Sub
'''
        result = engine.validate_code(vba_code, "vba")
        assert isinstance(result, ValidationResult)
        assert result.language == "vba"
        print(f"✓ PASSED: VBA validation (Score: {result.quality_score})")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 8: Language detection
    print("\nTest 8: Language Detection")
    try:
        python_code = "import os\ndef my_function():\n    return 'python'"
        detected = engine._detect_language(python_code)
        assert detected == "python"
        
        autolisp_code = "(defun c:test () (princ))"
        detected = engine._detect_language(autolisp_code)
        assert detected == "autolisp"
        
        vba_code = "Option Explicit\nSub Test()\nEnd Sub"
        detected = engine._detect_language(vba_code)
        assert detected == "vba"
        
        print("✓ PASSED: Language detection working correctly")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 9: Quality scoring
    print("\nTest 9: Quality Score Calculation")
    try:
        # Test perfect score
        perfect_score = engine._calculate_quality_score([])
        assert perfect_score == 100.0
        
        # Test with errors
        issues = [
            ValidationIssue("error", "syntax", "Error 1"),
            ValidationIssue("warning", "style", "Warning 1"),
            ValidationIssue("info", "style", "Info 1")
        ]
        score = engine._calculate_quality_score(issues)
        expected = 100 - 20 - 10 - 2  # error + warning + info penalties
        assert score == expected
        
        print(f"✓ PASSED: Quality scoring (Perfect: {perfect_score}, With issues: {score})")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 10: Multiple file validation
    print("\nTest 10: Multiple File Validation")
    try:
        files = {
            "test.py": "def hello(): print('Python')",
            "test.lsp": "(defun c:test () (princ))",
            "test.bas": "Sub Test()\nEnd Sub"
        }
        results = engine.validate_multiple_files(files)
        
        assert len(results) == 3
        assert "test.py" in results
        assert "test.lsp" in results
        assert "test.bas" in results
        assert results["test.py"].language == "python"
        assert results["test.lsp"].language == "autolisp"
        assert results["test.bas"].language == "vba"
        
        print("✓ PASSED: Multiple file validation")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 11: Unsupported language handling
    print("\nTest 11: Unsupported Language Handling")
    try:
        result = engine.validate_code("some code", "javascript")
        assert not result.valid
        assert result.language == "javascript"
        assert result.quality_score == 0
        assert any("unsupported language" in issue.message.lower() for issue in result.issues)
        print("✓ PASSED: Unsupported language handling")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 12: Unicode handling
    print("\nTest 12: Unicode Character Handling")
    try:
        unicode_code = '''
def test_unicode():
    message = "Hello, 世界! 🌍"
    print(message)
'''
        result = engine.validate_code(unicode_code, "python")
        assert isinstance(result, ValidationResult)
        assert result.language == "python"
        # Should handle unicode without syntax errors
        syntax_errors = [issue for issue in result.issues if issue.category == "syntax"]
        assert len(syntax_errors) == 0
        print("✓ PASSED: Unicode character handling")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Test 13: Empty code handling
    print("\nTest 13: Empty Code Handling")
    try:
        result = engine.validate_code("", "python")
        assert isinstance(result, ValidationResult)
        assert result.language == "python"
        
        result = engine.validate_code("   \n\t  \n  ", "python")
        assert isinstance(result, ValidationResult)
        assert result.language == "python"
        
        print("✓ PASSED: Empty code handling")
        test_results.append(True)
    except Exception as e:
        print(f"✗ FAILED: {e}")
        test_results.append(False)
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = sum(test_results)
    total = len(test_results)
    pass_rate = (passed / total) * 100 if total > 0 else 0
    
    print(f"Tests Run: {total}")
    print(f"Tests Passed: {passed}")
    print(f"Tests Failed: {total - passed}")
    print(f"Pass Rate: {pass_rate:.1f}%")
    
    if passed == total:
        print("\n🎉 ALL TESTS PASSED!")
        return True
    else:
        print(f"\n⚠️  {total - passed} TESTS FAILED")
        return False


def run_performance_tests():
    """Run basic performance tests."""
    print("\n" + "=" * 60)
    print("PERFORMANCE TESTS")
    print("=" * 60)
    
    try:
        from src.code_generation.validation_engine import ValidationEngine
        import time
        
        engine = ValidationEngine()
        
        # Large code test
        print("\nPerformance Test 1: Large Code Input")
        start_time = time.time()
        
        large_code = "# Large file\n" + "\n".join([
            f"def function_{i}():\n    return {i}" 
            for i in range(100)  # Reduced for faster testing
        ])
        
        result = engine.validate_code(large_code, "python")
        end_time = time.time()
        
        duration = end_time - start_time
        print(f"✓ Large code validation completed in {duration:.3f} seconds")
        print(f"  Code length: {len(large_code)} characters")
        print(f"  Quality score: {result.quality_score}")
        
        # Multiple files test
        print("\nPerformance Test 2: Multiple Files")
        start_time = time.time()
        
        files = {f"file_{i}.py": f"def func_{i}(): return {i}" for i in range(10)}
        results = engine.validate_multiple_files(files)
        
        end_time = time.time()
        duration = end_time - start_time
        
        print(f"✓ Multiple files validation completed in {duration:.3f} seconds")
        print(f"  Files validated: {len(results)}")
        
        return True
        
    except Exception as e:
        print(f"✗ Performance tests failed: {e}")
        traceback.print_exc()
        return False


def main():
    """Main test runner."""
    print(f"Python version: {sys.version}")
    print(f"Working directory: {os.getcwd()}")
    print(f"Project root: {project_root}")
    
    # Run basic tests
    basic_success = run_basic_validation_tests()
    
    # Run performance tests
    performance_success = run_performance_tests()
    
    # Final summary
    print("\n" + "=" * 60)
    print("FINAL RESULTS")
    print("=" * 60)
    
    if basic_success and performance_success:
        print("🎉 ALL TEST SUITES PASSED!")
        return 0
    else:
        print("⚠️  SOME TESTS FAILED")
        return 1


if __name__ == "__main__":
    sys.exit(main())