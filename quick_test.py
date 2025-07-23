"""
Quick 30-second test with real AutoCAD.
Creates a few simple entities to verify the endpoints work.
"""

import sys
import os
import time
import requests
import json
from threading import Thread
import subprocess

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def start_server():
    """Start the MCP server in a separate process."""
    import importlib.util
    spec = importlib.util.spec_from_file_location("server", "src/server.py")
    server_module = importlib.util.module_from_spec(spec)
    
    # Fix imports for standalone execution
    import src.config as config_module
    import src.decorators as decorators_module  
    import src.utils as utils_module
    
    sys.modules['config'] = config_module
    sys.modules['decorators'] = decorators_module
    sys.modules['utils'] = utils_module
    
    spec.loader.exec_module(server_module)

def test_endpoints():
    """Test the drawing endpoints with real AutoCAD."""
    base_url = "http://localhost:5000"
    
    print("AutoCAD MCP Server - Quick Live Test")
    print("=" * 40)
    
    # Wait for server to start
    print("Waiting for server to start...")
    time.sleep(2)
    
    try:
        # Test 1: Health check
        print("1. Testing health endpoint...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   [OK] Server is healthy")
        else:
            print(f"   [FAIL] Health check failed: {response.status_code}")
            return False
        
        # Test 2: AutoCAD status
        print("2. Testing AutoCAD connection...")
        response = requests.get(f"{base_url}/acad-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] AutoCAD connected - Version: {data.get('version', 'Unknown')}")
        else:
            print(f"   [FAIL] AutoCAD not connected: {response.status_code}")
            return False
        
        # Test 3: Create a line
        print("3. Testing line creation...")
        line_data = {
            'start_point': [0, 0, 0],
            'end_point': [100, 100, 0],
            'layer': 'MCP_TEST'
        }
        response = requests.post(f"{base_url}/draw/line", 
                               json=line_data, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Line created - Entity ID: {data.get('entity_id')}")
        else:
            print(f"   [FAIL] Line creation failed: {response.status_code}")
            if response.text:
                error_data = response.json()
                print(f"   Error: {error_data.get('error')}")
            return False
        
        # Test 4: Create a circle
        print("4. Testing circle creation...")
        circle_data = {
            'center_point': [50, 50, 0],
            'radius': 25,
            'layer': 'MCP_TEST'
        }
        response = requests.post(f"{base_url}/draw/circle", 
                               json=circle_data, 
                               timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Circle created - Entity ID: {data.get('entity_id')}")
        else:
            print(f"   [FAIL] Circle creation failed: {response.status_code}")
            return False
            
        print("\n" + "=" * 40)
        print("[SUCCESS] All tests passed!")
        print("\nYou should see a line and circle in your AutoCAD drawing.")
        print("Both entities are on layer 'MCP_TEST' for easy identification.")
        
        return True
        
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to MCP server")
        print("Make sure the server started properly")
        return False
    except Exception as e:
        print(f"[FAIL] Test error: {e}")
        return False

if __name__ == '__main__':
    print("Starting MCP server...")
    
    # Start server in background thread
    server_thread = Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Run tests
    success = test_endpoints()
    
    if success:
        print("\n🎉 Quick test completed successfully!")
        print("\nNext steps:")
        print("1. Check your AutoCAD drawing for the line and circle")
        print("2. You can delete layer 'MCP_TEST' to clean up")
        print("3. Close this test drawing and return to your work")
    else:
        print("\n❌ Some tests failed")
        print("Check the error messages above")
    
    input("\nPress Enter to exit...")