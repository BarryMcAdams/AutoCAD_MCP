"""
Final 30-second AutoCAD test - runs on port 5001 to avoid conflicts.
"""

import sys
import os
import time
import requests

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_test():
    # Override config to use port 5001
    os.environ['MCP_PORT'] = '5001'
    
    from server import app
    from config import config
    import threading
    
    print("Final AutoCAD MCP Test")
    print("=" * 30)
    
    # Start server in background thread
    def start_server():
        app.run(host='localhost', port=5001, debug=False, use_reloader=False)
    
    server_thread = threading.Thread(target=start_server, daemon=True)
    server_thread.start()
    
    # Wait for server to start
    print("Starting server on port 5001...")
    time.sleep(3)
    
    base_url = "http://localhost:5001"
    
    try:
        # Test 1: Health check
        print("1. Health check...")
        response = requests.get(f"{base_url}/health", timeout=5)
        if response.status_code == 200:
            print("   [OK] Server healthy")
        else:
            print(f"   [FAIL] Health check failed: {response.status_code}")
            return
        
        # Test 2: AutoCAD status
        print("2. AutoCAD status...")
        response = requests.get(f"{base_url}/acad-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   [OK] AutoCAD connected")
                
                # Test 3: Draw line
                print("3. Drawing line...")
                line_data = {
                    'start_point': [0, 0, 0],
                    'end_point': [100, 100, 0],
                    'layer': 'MCP_TEST'
                }
                response = requests.post(f"{base_url}/draw/line", json=line_data, timeout=10)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        print(f"   [OK] Line created - ID: {result.get('entity_id')}")
                        
                        # Test 4: Draw circle  
                        print("4. Drawing circle...")
                        circle_data = {
                            'center_point': [50, 50, 0],
                            'radius': 25,
                            'layer': 'MCP_TEST'
                        }
                        response = requests.post(f"{base_url}/draw/circle", json=circle_data, timeout=10)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get('success'):
                                print(f"   [OK] Circle created - ID: {result.get('entity_id')}")
                                print("\n[SUCCESS] All tests passed!")
                                print("Check AutoCAD for line and circle on layer MCP_TEST")
                                return True
                        
                print("   [FAIL] Drawing operations failed")
            else:
                print(f"   [FAIL] AutoCAD response: {data.get('error', 'Unknown error')}")
        else:
            print(f"   [FAIL] AutoCAD not connected (status: {response.status_code})")
            if response.status_code == 503:
                print("   AutoCAD might not be running - start AutoCAD 2025 first")
        
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to server")
    except Exception as e:
        print(f"[FAIL] Test error: {e}")
    
    return False

if __name__ == '__main__':
    success = run_test()
    if success:
        print("\nTest completed successfully!")
    else:
        print("\nSome tests failed - check AutoCAD is running")
    
    input("Press Enter to exit...")