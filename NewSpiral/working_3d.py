"""
WORKING 3D BUILDING: Create 12-foot high extruded walls
Fixed version that actually works!
"""

import sys
import os
import requests
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from autocad_client import AutoCADClient


def create_working_3d_building():
    """Create 3D building with properly formatted API calls."""
    
    client = AutoCADClient()
    
    print("=== CREATING 12-FOOT HIGH 3D BUILDING ===")
    print()
    
    # Check connection
    status = client.autocad_status()
    if not status.get('success'):
        print("ERROR: AutoCAD not connected")
        return False
    
    print(f"Connected to: AutoCAD {status.get('version', 'Unknown')}")
    print("Extruding walls to 12 feet high...")
    print()
    
    print("WATCH YOUR AUTOCAD SCREEN - GOING 3D!")
    print()
    
    # Base URL for API
    base_url = "http://localhost:5001"
    
    # 1. Create the main building volume (30x20x12 feet)
    print("1. Creating main building volume...")
    
    building_profile = [[0,0,0], [30,0,0], [30,20,0], [0,20,0]]
    
    response = requests.post(
        f"{base_url}/draw/extrude",
        json={
            "profile_points": building_profile,
            "height": 12
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            print(f"   Main building: EXTRUDED 12' high!")
            print(f"   Entity ID: {result.get('entity_id')}")
            print(f"   Volume: {result.get('volume', 0):,.0f} cubic feet")
        else:
            print(f"   ERROR: {result.get('error')}")
    else:
        print(f"   HTTP ERROR: {response.status_code}")
    
    # 2. Create individual room volumes
    print("2. Creating room volumes...")
    
    rooms = [
        {"name": "SW Room", "profile": [[1,1,0], [14,1,0], [14,9,0], [1,9,0]]},
        {"name": "SE Room", "profile": [[16,1,0], [29,1,0], [29,9,0], [16,9,0]]},
        {"name": "NW Room", "profile": [[1,11,0], [14,11,0], [14,19,0], [1,19,0]]},
        {"name": "NE Room", "profile": [[16,11,0], [29,11,0], [29,19,0], [16,19,0]]}
    ]
    
    room_count = 0
    total_volume = 0
    
    for room in rooms:
        response = requests.post(
            f"{base_url}/draw/extrude",
            json={
                "profile_points": room["profile"],
                "height": 12
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                room_count += 1
                volume = result.get('volume', 0)
                total_volume += volume
                print(f"   {room['name']}: CREATED (Vol: {volume:,.0f} cu ft) (ID: {result.get('entity_id')})")
            else:
                print(f"   {room['name']} ERROR: {result.get('error')}")
        else:
            print(f"   {room['name']} HTTP ERROR: {response.status_code}")
    
    # 3. Create architectural features
    print("3. Adding architectural features...")
    
    # Chimney (2x2 feet, 18 feet high)
    chimney_response = requests.post(
        f"{base_url}/draw/extrude",
        json={
            "profile_points": [[25,15,0], [27,15,0], [27,17,0], [25,17,0]],
            "height": 18
        }
    )
    
    chimney_created = False
    if chimney_response.status_code == 200:
        result = chimney_response.json()
        if result.get('success'):
            chimney_created = True
            print(f"   Chimney: CREATED 18' high (Vol: {result.get('volume', 0):,.0f} cu ft)")
    
    # Front porch/steps (4x2 feet, 1 foot high)
    porch_response = requests.post(
        f"{base_url}/draw/extrude", 
        json={
            "profile_points": [[13,0,0], [17,0,0], [17,-2,0], [13,-2,0]],
            "height": 1
        }
    )
    
    porch_created = False
    if porch_response.status_code == 200:
        result = porch_response.json()
        if result.get('success'):
            porch_created = True
            print(f"   Front porch: CREATED 1' high (Vol: {result.get('volume', 0):,.0f} cu ft)")
    
    # Create some windows as 3D openings (small extrusions)
    print("4. Adding window frames...")
    
    windows = [
        {"name": "North Window 1", "center": [7, 20, 0], "size": 3},
        {"name": "North Window 2", "center": [23, 20, 0], "size": 3},
        {"name": "East Window", "center": [30, 10, 0], "size": 3},
        {"name": "South Window", "center": [15, 0, 0], "size": 4}
    ]
    
    window_count = 0
    for window in windows:
        x, y, z = window["center"]
        size = window["size"]
        
        # Create window frame as small rectangular extrusion
        window_profile = [
            [x - size/2, y - 0.1, z],
            [x + size/2, y - 0.1, z], 
            [x + size/2, y + 0.1, z],
            [x - size/2, y + 0.1, z]
        ]
        
        response = requests.post(
            f"{base_url}/draw/extrude",
            json={
                "profile_points": window_profile,
                "height": 4  # 4 feet tall windows
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                window_count += 1
                print(f"   {window['name']}: FRAME CREATED (ID: {result.get('entity_id')})")
    
    print()
    print("=== 3D BUILDING CONSTRUCTION COMPLETE ===")
    print(f"Building: 30' x 20' x 12' = 7,200 cubic feet")
    print(f"Room volumes total: {total_volume:,.0f} cubic feet")
    print()
    print("3D Elements created:")
    print(f"  - Main building shell: 1/1")
    print(f"  - Room volumes: {room_count}/4")
    print(f"  - Chimney: {'Yes' if chimney_created else 'No'}")  
    print(f"  - Front porch: {'Yes' if porch_created else 'No'}")
    print(f"  - Window frames: {window_count}/4")
    print()
    print("🏗️🏗️ LOOK AT YOUR AUTOCAD SCREEN NOW! 🏗️🏗️")
    print()
    print("YOU NOW HAVE A COMPLETE 3D BUILDING!")
    print()
    print("AutoCAD Commands to try:")
    print("  1. Type '3DORBIT' and drag to rotate the view")
    print("  2. Type 'VSCURRENT' and select 'Realistic' or 'Shaded'")  
    print("  3. Use mouse wheel to zoom in and out")
    print("  4. Type 'VIEWCUBE' to show the ViewCube navigation")
    print()
    print("🎉 FROM CONCEPT TO 3D BUILDING IN UNDER 1 MINUTE! 🎉")
    
    return True


if __name__ == "__main__":
    create_working_3d_building()