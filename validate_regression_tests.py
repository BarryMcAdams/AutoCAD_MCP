#!/usr/bin/env python3
"""
Quick validation script for the regression test suite.

This script validates that the regression tests can run properly
and that all basic MCP tools are accessible for testing.

Usage:
    python validate_regression_tests.py
"""

import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def main():
    """Validate regression test setup."""
    print("AutoCAD MCP Regression Test Validation")
    print("=" * 50)
    
    validation_results = {
        "imports": {},
        "tools": {},
        "test_files": {},
        "overall": False
    }
    
    # 1. Test imports
    print("\n1. Testing imports...")
    
    try:
        from src.mcp_server import mcp
        validation_results["imports"]["mcp_server"] = True
        print("   ✅ MCP server import successful")
    except Exception as e:
        validation_results["imports"]["mcp_server"] = False
        print(f"   ❌ MCP server import failed: {e}")
    
    try:
        from tests.regression.test_basic_tools_regression import TestBasicToolsRegression
        validation_results["imports"]["regression_tests"] = True
        print("   ✅ Regression test classes import successful")
    except Exception as e:
        validation_results["imports"]["regression_tests"] = False
        print(f"   ❌ Regression test import failed: {e}")
    
    try:
        import pytest
        import psutil
        from concurrent.futures import ThreadPoolExecutor
        validation_results["imports"]["dependencies"] = True
        print("   ✅ Test dependencies available")
    except Exception as e:
        validation_results["imports"]["dependencies"] = False
        print(f"   ❌ Missing test dependencies: {e}")
    
    # 2. Test basic tool availability
    print("\n2. Testing basic tool availability...")
    
    basic_tools = [
        "draw_line", "draw_circle", "extrude_profile", 
        "revolve_profile", "list_entities", "get_entity_info", "server_status"
    ]
    
    if validation_results["imports"]["mcp_server"]:
        try:
            from src.mcp_server import mcp
            available_tools = list(mcp.tool_handlers.keys())
            
            for tool in basic_tools:
                if tool in available_tools:
                    validation_results["tools"][tool] = True
                    print(f"   ✅ {tool} - Available")
                else:
                    validation_results["tools"][tool] = False
                    print(f"   ❌ {tool} - Not found")
            
            print(f"   📊 Total tools in registry: {len(available_tools)}")
            
        except Exception as e:
            print(f"   ❌ Error checking tools: {e}")
            for tool in basic_tools:
                validation_results["tools"][tool] = False
    else:
        print("   ⏭️  Skipped - MCP server import failed")
        for tool in basic_tools:
            validation_results["tools"][tool] = False
    
    # 3. Test file structure
    print("\n3. Testing file structure...")
    
    required_files = [
        "tests/regression/__init__.py",
        "tests/regression/test_basic_tools_regression.py", 
        "tests/regression/run_regression_tests.py",
        "tests/regression/README.md"
    ]
    
    for file_path in required_files:
        full_path = project_root / file_path
        if full_path.exists():
            validation_results["test_files"][file_path] = True
            print(f"   ✅ {file_path}")
        else:
            validation_results["test_files"][file_path] = False
            print(f"   ❌ {file_path} - Missing")
    
    # 4. Quick functionality test
    print("\n4. Quick functionality test...")
    
    if validation_results["imports"]["mcp_server"]:
        try:
            from unittest.mock import Mock, patch
            from src.mcp_server import mcp
            
            # Test server_status with mock
            with patch('src.utils.get_autocad_instance') as mock_get_acad:
                mock_acad = Mock()
                mock_acad.ActiveDocument.Name = "ValidationTest.dwg"
                mock_get_acad.return_value = mock_acad
                
                result = mcp.tool_handlers["server_status"]()
                response = json.loads(result) if isinstance(result, str) else result
                
                if response.get("success", False):
                    print("   ✅ Basic tool execution test passed")
                    validation_results["functionality"] = True
                else:
                    print(f"   ❌ Basic tool execution failed: {response}")
                    validation_results["functionality"] = False
                    
        except Exception as e:
            print(f"   ❌ Functionality test error: {e}")
            validation_results["functionality"] = False
    else:
        print("   ⏭️  Skipped - MCP server not available")
        validation_results["functionality"] = False
    
    # 5. Overall assessment
    print("\n5. Overall assessment...")
    
    # Calculate scores
    import_score = sum(validation_results["imports"].values())
    tools_score = sum(validation_results["tools"].values()) 
    files_score = sum(validation_results["test_files"].values())
    functionality_score = 1 if validation_results.get("functionality", False) else 0
    
    total_possible = len(validation_results["imports"]) + len(basic_tools) + len(required_files) + 1
    total_score = import_score + tools_score + files_score + functionality_score
    
    print(f"   📊 Import tests: {import_score}/{len(validation_results['imports'])}")
    print(f"   📊 Tool availability: {tools_score}/{len(basic_tools)}")  
    print(f"   📊 File structure: {files_score}/{len(required_files)}")
    print(f"   📊 Functionality: {functionality_score}/1")
    print(f"   📊 Overall score: {total_score}/{total_possible} ({total_score/total_possible*100:.1f}%)")
    
    validation_results["overall"] = total_score == total_possible
    
    if validation_results["overall"]:
        print("\n🎉 VALIDATION PASSED")
        print("✅ Regression test suite is ready to run")
        print("\nNext steps:")
        print("  python tests/regression/run_regression_tests.py")
        print("  pytest tests/regression/ -v")
        return 0
    else:
        print("\n❌ VALIDATION FAILED") 
        print("⚠️  Some issues need to be resolved before running regression tests")
        
        # Provide specific guidance
        if not validation_results["imports"]["mcp_server"]:
            print("\n🔧 Fix MCP server import issues:")
            print("  - Check that src/mcp_server.py exists")
            print("  - Verify all dependencies are installed")
            print("  - Check Python path configuration")
        
        if tools_score < len(basic_tools):
            print(f"\n🔧 Fix tool availability ({tools_score}/{len(basic_tools)} available):")
            missing_tools = [tool for tool in basic_tools if not validation_results["tools"].get(tool, False)]
            for tool in missing_tools:
                print(f"  - Register {tool} in mcp_server.py")
        
        if files_score < len(required_files):
            print(f"\n🔧 Fix missing files ({files_score}/{len(required_files)} present):")
            missing_files = [f for f in required_files if not validation_results["test_files"].get(f, False)]
            for file_path in missing_files:
                print(f"  - Create {file_path}")
        
        return 1
    
    # Save validation results
    try:
        with open(project_root / "regression_validation_results.json", "w") as f:
            json.dump(validation_results, f, indent=2)
        print(f"\n💾 Validation results saved to regression_validation_results.json")
    except Exception as e:
        print(f"\n⚠️  Could not save validation results: {e}")


if __name__ == "__main__":
    sys.exit(main())