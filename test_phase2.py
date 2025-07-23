"""
Phase 2 Test Script - 3D Operations
Tests extrusion, revolution, and boolean operations
"""

import sys
import os
import time
import requests
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def run_phase2_test():
    # Override config to use port 5001
    os.environ['MCP_PORT'] = '5001'
    
    from server import app
    import threading
    
    print("Phase 2 AutoCAD MCP Test - 3D Operations")
    print("=" * 50)
    
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
            return False
        
        # Test 2: AutoCAD status
        print("2. AutoCAD status...")
        response = requests.get(f"{base_url}/acad-status", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print(f"   [OK] AutoCAD connected")
                
                # Test 3: Create extruded solid
                print("3. Creating extruded solid (rectangular profile)...")
                extrude_data = {
                    'profile_points': [
                        [0, 0, 0],
                        [50, 0, 0], 
                        [50, 30, 0],
                        [0, 30, 0]
                    ],
                    'height': 20.0,
                    'taper_angle': 0.0,
                    'layer': 'PHASE2_TEST'
                }
                response = requests.post(f"{base_url}/draw/extrude", json=extrude_data, timeout=15)
                if response.status_code == 200:
                    result = response.json()
                    if result.get('success'):
                        extrude_id = result.get('entity_id')
                        print(f"   [OK] Extruded solid created - ID: {extrude_id}")
                        
                        # Test 4: Create revolved solid
                        print("4. Creating revolved solid (semicircle profile)...")
                        revolve_data = {
                            'profile_points': [
                                [60, 0, 0],
                                [80, 0, 0],
                                [80, 10, 0],
                                [70, 15, 0],
                                [60, 10, 0]
                            ],
                            'axis_point': [60, 0, 0],
                            'axis_vector': [0, 0, 1],
                            'angle': 180.0,
                            'layer': 'PHASE2_TEST'
                        }
                        response = requests.post(f"{base_url}/draw/revolve", json=revolve_data, timeout=15)
                        if response.status_code == 200:
                            result = response.json()
                            if result.get('success'):
                                revolve_id = result.get('entity_id')
                                print(f"   [OK] Revolved solid created - ID: {revolve_id}")
                                
                                # Test 5: Boolean union
                                print("5. Testing boolean union...")
                                union_data = {
                                    'entity_ids': [extrude_id, revolve_id],
                                    'layer': 'PHASE2_TEST'
                                }
                                response = requests.post(f"{base_url}/draw/boolean-union", json=union_data, timeout=15)
                                if response.status_code == 200:
                                    result = response.json()
                                    if result.get('success'):
                                        union_id = result.get('entity_id')
                                        print(f"   [OK] Boolean union completed - ID: {union_id}")
                                        
                                        # Test 6: Create another solid for subtraction
                                        print("6. Creating solid for subtraction test...")
                                        subtract_extrude_data = {
                                            'profile_points': [
                                                [10, 5, 0],
                                                [40, 5, 0], 
                                                [40, 25, 0],
                                                [10, 25, 0]
                                            ],
                                            'height': 25.0,
                                            'layer': 'PHASE2_TEST'
                                        }
                                        response = requests.post(f"{base_url}/draw/extrude", json=subtract_extrude_data, timeout=15)
                                        if response.status_code == 200:
                                            result = response.json()
                                            if result.get('success'):
                                                subtract_id = result.get('entity_id')
                                                print(f"   [OK] Subtraction solid created - ID: {subtract_id}")
                                                
                                                # Test 7: Boolean subtraction
                                                print("7. Testing boolean subtraction...")
                                                subtract_data = {
                                                    'base_entity_id': union_id,
                                                    'subtract_entity_ids': [subtract_id],
                                                    'layer': 'PHASE2_TEST'
                                                }
                                                response = requests.post(f"{base_url}/draw/boolean-subtract", json=subtract_data, timeout=15)
                                                if response.status_code == 200:
                                                    result = response.json()
                                                    if result.get('success'):
                                                        print(f"   [OK] Boolean subtraction completed - ID: {result.get('entity_id')}")
                                                        print("\n[SUCCESS] All Phase 2 tests passed!")
                                                        print("Check AutoCAD for 3D solids on layer PHASE2_TEST")
                                                        return True
                                                        
                print("   [FAIL] Some 3D operations failed")
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
    print("IMPORTANT: AutoCAD 2025 should be running for this test!")
    print("Starting Phase 2 test automatically...")
    
    success = run_phase2_test()
    if success:
        print("\nPhase 2 testing completed successfully!")
    else:
        print("\nSome Phase 2 tests failed - check AutoCAD connection and logs")
    
    print("Test completed.")