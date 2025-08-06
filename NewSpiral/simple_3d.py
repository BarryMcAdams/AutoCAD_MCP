"""
SIMPLE 3D BUILDING: Create 3D extruded walls
Direct approach to create 12-foot high walls
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from autocad_client import AutoCADClient


def create_simple_3d_building():
    """Create 3D building with simple extruded profiles."""
    
    client = AutoCADClient()
    
    print("=== CREATING 3D BUILDING - SIMPLE METHOD ===")
    print()
    
    # Check connection
    status = client.autocad_status()
    if not status.get('success'):
        print("ERROR: AutoCAD not connected")
        return False
    
    print(f"Connected to: AutoCAD {status.get('version', 'Unknown')}")
    print("Creating 3D walls by extruding profiles to 12 feet...")
    print()
    
    wall_height = 12  # 12 feet high
    
    print("CREATING 3D BUILDING...")
    print()
    
    # 1. Create simple room volumes (extruded rectangles)
    print("1. Creating room volumes (12' high)...")
    
    # Define the 4 rooms as separate volumes
    rooms = [
        {"name": "Room 1 (SW)", "profile": [[1, 1], [14, 1], [14, 9], [1, 9]]},
        {"name": "Room 2 (SE)", "profile": [[16, 1], [29, 1], [29, 9], [16, 9]]},  
        {"name": "Room 3 (NW)", "profile": [[1, 11], [14, 11], [14, 19], [1, 19]]},
        {"name": "Room 4 (NE)", "profile": [[16, 11], [29, 11], [29, 19], [16, 19]]}
    ]
    
    room_count = 0
    for room in rooms:
        print(f"   Creating {room['name']}...")
        
        # Use the REST API directly to avoid the list return issue
        import requests
        response = requests.post(
            "http://localhost:5001/draw/extrude",
            json={
                "profile_points": room["profile"],
                "extrude_height": wall_height
            }
        )
        
        if response.status_code == 200:
            result = response.json()
            if result.get('success'):
                room_count += 1
                print(f"     SUCCESS - {room['name']}: EXTRUDED (ID: {result.get('entity_id')})")
            else:
                print(f"     ERROR - {room['name']}: {result.get('error', 'Unknown error')}")
        else:
            print(f"     ERROR - {room['name']}: HTTP {response.status_code}")
    
    # 2. Create building envelope (outer shell)
    print("2. Creating building envelope...")
    
    building_envelope = [[0, 0], [30, 0], [30, 20], [0, 20]]
    
    import requests
    response = requests.post(
        "http://localhost:5001/draw/extrude", 
        json={
            "profile_points": building_envelope,
            "extrude_height": wall_height + 2  # Slightly taller for roof
        }
    )
    
    envelope_created = False
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            envelope_created = True
            print(f"   Building envelope: CREATED (ID: {result.get('entity_id')})")
        else:
            print(f"   Building envelope ERROR: {result.get('error', 'Unknown error')}")
    
    # 3. Create some 3D architectural elements
    print("3. Adding architectural elements...")
    
    # Chimney
    chimney_profile = [[25, 15], [27, 15], [27, 17], [25, 17]]
    response = requests.post(
        "http://localhost:5001/draw/extrude",
        json={
            "profile_points": chimney_profile, 
            "extrude_height": 18  # 18 feet high (6 feet above roof)
        }
    )
    
    chimney_created = False
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            chimney_created = True
            print(f"   Chimney: CREATED (ID: {result.get('entity_id')})")
    
    # Front steps
    steps_profile = [[13, -2], [17, -2], [17, 0], [13, 0]]
    response = requests.post(
        "http://localhost:5001/draw/extrude",
        json={
            "profile_points": steps_profile,
            "extrude_height": 1  # 1 foot high steps
        }
    )
    
    steps_created = False
    if response.status_code == 200:
        result = response.json()
        if result.get('success'):
            steps_created = True
            print(f"   Front steps: CREATED (ID: {result.get('entity_id')})")
    
    print()
    print("=== 3D BUILDING COMPLETE ===")
    print(f"Building: 30' x 20' x {wall_height}' high = {30*20*wall_height:,} cubic feet")
    print()
    print("3D Elements created:")
    print(f"  - Room volumes: {room_count}/4") 
    print(f"  - Building envelope: {'✓' if envelope_created else '✗'}")
    print(f"  - Chimney: {'✓' if chimney_created else '✗'}")
    print(f"  - Front steps: {'✓' if steps_created else '✗'}")
    print()
    print("🏗️ LOOK AT YOUR AUTOCAD SCREEN! 🏗️")
    print()
    print("You now have a FULL 3D BUILDING!")
    print("Try these AutoCAD commands:")
    print("  - Type '3DORBIT' to rotate around the building")
    print("  - Type 'VSCURRENT' and select 'Realistic' for better view")
    print("  - Use mouse wheel to zoom in/out")
    print()
    print("🎉 FROM 2D LINES TO 3D BUILDING IN MINUTES! 🎉")
    
    return True


if __name__ == "__main__":
    create_simple_3d_building()