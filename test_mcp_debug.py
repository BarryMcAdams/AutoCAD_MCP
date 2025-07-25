"""
Test client for AutoCAD MCP Debug Server
"""

import requests
import json

# MCP server configuration
BASE_URL = "http://localhost:8000"
AUTH_TOKEN = "debug_autocad_2025"
HEADERS = {
    "Authorization": f"Bearer {AUTH_TOKEN}",
    "Content-Type": "application/json"
}

def test_mcp_server():
    print("Testing AutoCAD MCP Debug Server")
    print("=" * 40)
    
    try:
        # Test 1: Health check
        print("1. Health check...")
        response = requests.get(f"{BASE_URL}/health", timeout=10)
        if response.status_code == 200:
            data = response.json()
            print(f"   [OK] Server healthy")
            print(f"   AutoCAD Status: {data['autocad_connection']['status']}")
            print(f"   Document: {data['autocad_connection'].get('document', 'N/A')}")
            print(f"   Entity Count: {data['autocad_connection'].get('entity_count', 'N/A')}")
        else:
            print(f"   [FAIL] Health check failed: {response.status_code}")
            return False
        
        # Test 2: Get document info
        print("\n2. Getting document info...")
        payload = {
            "tool_name": "get_document_info",
            "parameters": {}
        }
        response = requests.post(f"{BASE_URL}/mcp/v1/execute", json=payload, headers=HEADERS, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print(f"   [FAIL] Error: {data['error']}")
            else:
                result = data['result']
                print(f"   [OK] Document: {result['document_name']}")
                print(f"   Path: {result['full_path']}")
                print(f"   Entity Count: {result['entity_count']}")
                print(f"   Active Layer: {result['active_layer']}")
        
        # Test 3: Create a line using MCP server
        print("\n3. Creating line via MCP server...")
        payload = {
            "tool_name": "create_line",
            "parameters": {
                "start_point": [0, 0, 0],
                "end_point": [100, 100, 0]
            }
        }
        response = requests.post(f"{BASE_URL}/mcp/v1/execute", json=payload, headers=HEADERS, timeout=15)
        if response.status_code == 200:
            data = response.json()
            if data.get('error'):
                print(f"   [FAIL] Error: {data['error']}")
            else:
                result = data['result']
                print(f"   [OK] Line created!")
                print(f"   Handle: {result['handle']}")
                print(f"   Message: {result['message']}")
                print(f"   Entity Count: {result['entity_count']}")
                
                # Test 4: Create a circle
                print("\n4. Creating circle via MCP server...")
                payload = {
                    "tool_name": "create_circle",
                    "parameters": {
                        "center": [50, 50, 0],
                        "radius": 25
                    }
                }
                response = requests.post(f"{BASE_URL}/mcp/v1/execute", json=payload, headers=HEADERS, timeout=15)
                if response.status_code == 200:
                    data = response.json()
                    if data.get('error'):
                        print(f"   [FAIL] Error: {data['error']}")
                    else:
                        result = data['result']
                        print(f"   [OK] Circle created!")
                        print(f"   Handle: {result['handle']}")
                        print(f"   Entity Count: {result['entity_count']}")
                        
                        # Test 5: Count entities to verify
                        print("\n5. Counting entities...")
                        payload = {
                            "tool_name": "count_entities",
                            "parameters": {}
                        }
                        response = requests.post(f"{BASE_URL}/mcp/v1/execute", json=payload, headers=HEADERS, timeout=10)
                        if response.status_code == 200:
                            data = response.json()
                            if data.get('error'):
                                print(f"   [FAIL] Error: {data['error']}")
                            else:
                                result = data['result']
                                print(f"   [OK] Total entities: {result['total_count']}")
                                print("   Sample entities:")
                                for entity in result['sample_entities']:
                                    print(f"     - {entity['type']} (Handle: {entity['handle']}, Layer: {entity['layer']})")
                                
                                print("\n[SUCCESS] MCP server tests completed!")
                                print("** CHECK AUTOCAD NOW FOR VISIBLE ENTITIES **")
                                return True
        
        print("\n[FAIL] Some operations failed")
        return False
        
    except requests.exceptions.ConnectionError:
        print("[FAIL] Could not connect to MCP server - make sure it's running on port 8000")
        return False
    except Exception as e:
        print(f"[FAIL] Test error: {e}")
        return False

if __name__ == '__main__':
    print("IMPORTANT: Make sure autocad_mcp_server_debug.py is running on port 8000!")
    print("And AutoCAD 2025 should be open with a drawing.")
    
    success = test_mcp_server()
    if success:
        print("\nMCP server is working! Check AutoCAD for visible entities.")
    else:
        print("\nMCP server tests failed.")
    
    print("Test completed.")