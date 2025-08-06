"""
Example 1: Automated Building Floor Plan Generation
This shows how to create a complete floor plan programmatically
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from autocad_client import AutoCADClient


def create_building_floor_plan():
    """Create a simple building floor plan automatically."""
    
    client = AutoCADClient()
    
    print("[BUILDING] Creating Building Floor Plan...")
    
    # Check AutoCAD connection
    status = client.autocad_status()
    if not status.get('success'):
        print("[ERROR] AutoCAD not connected. Please start AutoCAD 2025 with a drawing open.")
        return
    
    print("[SUCCESS] AutoCAD connected. Drawing floor plan...")
    
    # 1. Create exterior walls (40x30 foot building)
    exterior_walls = [
        # Bottom wall
        ([0, 0, 0], [40, 0, 0]),
        # Right wall  
        ([40, 0, 0], [40, 30, 0]),
        # Top wall
        ([40, 30, 0], [0, 30, 0]),
        # Left wall
        ([0, 30, 0], [0, 0, 0])
    ]
    
    print("Drawing exterior walls...")
    wall_ids = []
    for start, end in exterior_walls:
        result = client.draw_line(start, end)
        if result.get('success'):
            wall_ids.append(result['entity_id'])
            print(f"  [OK] Wall created: {result['entity_id']}")
    
    # 2. Create interior walls (divide into 4 rooms)
    interior_walls = [
        # Vertical divider
        ([20, 0, 0], [20, 30, 0]),
        # Horizontal divider  
        ([0, 15, 0], [40, 15, 0])
    ]
    
    print("Drawing interior walls...")
    for start, end in interior_walls:
        result = client.draw_line(start, end)
        if result.get('success'):
            print(f"  ✅ Interior wall created: {result['entity_id']}")
    
    # 3. Add doors (gaps in walls - we'll just mark door locations)
    door_locations = [
        # Front door
        ([18, 0, 0], 4),  # Center of front wall, 4 feet wide
        # Interior doors
        ([20, 12, 0], 3),  # Door between rooms
        ([8, 15, 0], 3),   # Door between rooms
    ]
    
    print("Marking door locations...")
    for (center_x, center_y, z), width in door_locations:
        # Draw a small rectangle to mark door
        door_corners = [
            [center_x - width/2, center_y, z],
            [center_x + width/2, center_y, z],
            [center_x + width/2, center_y + 1, z],
            [center_x - width/2, center_y + 1, z]
        ]
        result = client.extrude_profile(door_corners, 0.1)  # Very thin extrusion
        if result.get('success'):
            print(f"  🚪 Door marked: {result['entity_id']}")
    
    # 4. Add windows (circles for simplicity)
    window_locations = [
        ([10, 30, 0], 1.5),  # North wall window
        ([30, 30, 0], 1.5),  # North wall window
        ([40, 10, 0], 1.5),  # East wall window
        ([40, 20, 0], 1.5),  # East wall window
    ]
    
    print("Adding windows...")
    for (x, y, z), radius in window_locations:
        result = client.draw_circle([x, y, z], radius)
        if result.get('success'):
            print(f"  🪟 Window created: {result['entity_id']}")
    
    print("\n🎉 Floor plan complete!")
    print("📏 Building size: 40' x 30'")
    print("🏠 Rooms: 4 (divided by interior walls)")
    print("🚪 Doors: 3 marked locations")
    print("🪟 Windows: 4 on north and east walls")


if __name__ == "__main__":
    create_building_floor_plan()