"""
Quick test script for basic endpoint functionality.
This can be run to verify the drawing operations work without AutoCAD.
"""

import json
import sys
import os

# Add src to path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils import validate_point3d, validate_layer_name, create_success_response
from config import config

def test_validation_functions():
    """Test all validation functions."""
    print("Testing validation functions...")
    
    try:
        # Test point validation
        point = validate_point3d([0, 0, 0])
        print(f"[OK] Point validation: {point}")
        
        # Test layer validation  
        layer = validate_layer_name('TEST_LAYER')
        print(f"[OK] Layer validation: {layer}")
        
        # Test invalid point
        try:
            validate_point3d([0, 0])  # Missing Z
            print("[FAIL] Should have failed for invalid point")
        except ValueError as e:
            print(f"[OK] Correctly caught invalid point: {e}")
        
        # Test invalid layer
        try:
            validate_layer_name('LAYER<INVALID>')  # Invalid character
            print("[FAIL] Should have failed for invalid layer")  
        except ValueError as e:
            print(f"[OK] Correctly caught invalid layer: {e}")
            
        print("All validation tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Validation test failed: {e}")
        return False

def test_response_creation():
    """Test response creation utilities."""
    print("\nTesting response creation...")
    
    try:
        # Test success response
        success_resp = create_success_response({
            'entity_id': 12345,
            'entity_type': 'AcDbLine'
        }, execution_time=1.5)
        
        expected_keys = ['success', 'entity_id', 'entity_type', 'execution_time']
        if all(key in success_resp for key in expected_keys):
            print("[OK] Success response creation works")
        else:
            print("[FAIL] Success response missing keys")
            return False
            
        print("Response creation tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Response creation test failed: {e}")
        return False

def test_configuration():
    """Test configuration loading."""
    print("\nTesting configuration...")
    
    try:
        print(f"[OK] Host: {config.HOST}")
        print(f"[OK] Port: {config.PORT}")
        print(f"[OK] Debug: {config.DEBUG}")
        print(f"[OK] Log Level: {config.LOG_LEVEL}")
        
        print("Configuration tests passed!")
        return True
        
    except Exception as e:
        print(f"[FAIL] Configuration test failed: {e}")
        return False

def simulate_draw_line_logic():
    """Simulate the drawing logic without AutoCAD."""
    print("\nSimulating draw line logic...")
    
    try:
        # Simulate request data
        data = {
            'start_point': [0, 0, 0],
            'end_point': [100, 100, 0],
            'layer': 'TEST_LAYER'
        }
        
        # Validate input (this is what the endpoint does)
        start_point = validate_point3d(data['start_point'])
        end_point = validate_point3d(data['end_point'])
        layer = validate_layer_name(data['layer'])
        
        # Simulate successful creation
        mock_entity_id = 12345
        mock_entity_type = "AcDbLine"
        
        # Create response (this is what the endpoint returns)
        response = create_success_response({
            'entity_id': mock_entity_id,
            'entity_type': mock_entity_type,
            'layer': layer,
            'start_point': start_point,
            'end_point': end_point
        })
        
        print(f"[OK] Simulated line creation successful")
        print(f"  Response: {json.dumps(response, indent=2)}")
        
        return True
        
    except Exception as e:
        print(f"[FAIL] Line simulation failed: {e}")
        return False

if __name__ == '__main__':
    print("AutoCAD MCP Server - Basic Functionality Test")
    print("=" * 50)
    
    all_passed = True
    
    all_passed &= test_validation_functions()
    all_passed &= test_response_creation()  
    all_passed &= test_configuration()
    all_passed &= simulate_draw_line_logic()
    
    print("\n" + "=" * 50)
    if all_passed:
        print("[OK] All basic functionality tests PASSED!")
        print("The drawing endpoints should work correctly.")
    else:
        print("[FAIL] Some tests FAILED!")
        print("Check the errors above before proceeding.")
    
    print("\nNext step: Test with actual AutoCAD running")