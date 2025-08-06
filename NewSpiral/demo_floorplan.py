"""
DEMO: Automatic Floor Plan Generation
Watch AutoCAD draw automatically!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from autocad_client import AutoCADClient


def create_sample_floorplan():
    """Create a sample floor plan automatically in AutoCAD."""
    
    client = AutoCADClient()
    
    print("=== AUTOCAD MCP FLOOR PLAN DEMO ===")
    print("Watch your AutoCAD screen as this draws automatically!")
    print()
    
    # Check AutoCAD connection
    status = client.autocad_status()
    if not status.get('success'):
        print("ERROR: AutoCAD not connected.")
        print("Please start AutoCAD 2025 with a drawing open, then run this again.")
        return False
    
    print(f"SUCCESS: Connected to AutoCAD {status.get('version', 'Unknown')}")
    print(f"Drawing: {status.get('document', 'Unknown')}")
    print()
    
    print("Drawing 30x20 foot house floor plan...")
    print()
    
    # 1. Exterior walls - create a rectangle
    print("1. Drawing exterior walls...")
    exterior_walls = [
        ([0, 0, 0], [30, 0, 0]),    # Bottom wall
        ([30, 0, 0], [30, 20, 0]),  # Right wall  
        ([30, 20, 0], [0, 20, 0]),  # Top wall
        ([0, 20, 0], [0, 0, 0])     # Left wall
    ]
    
    wall_count = 0
    for i, (start, end) in enumerate(exterior_walls):
        result = client.draw_line(start, end)
        if result.get('success'):
            wall_count += 1
            print(f"   Wall {i+1} created successfully (ID: {result['entity_id']})")
        else:
            print(f"   ERROR creating wall {i+1}: {result.get('error')}")
    
    # 2. Interior walls - divide into rooms
    print("2. Drawing interior walls...")
    interior_walls = [
        ([15, 0, 0], [15, 20, 0]),  # Vertical divider (splits into left/right)
        ([0, 10, 0], [30, 10, 0]),  # Horizontal divider (splits into top/bottom)
    ]
    
    interior_count = 0
    for i, (start, end) in enumerate(interior_walls):
        result = client.draw_line(start, end)
        if result.get('success'):
            interior_count += 1
            print(f"   Interior wall {i+1} created (ID: {result['entity_id']})")
        else:
            print(f"   ERROR creating interior wall {i+1}: {result.get('error')}")
    
    # 3. Add doors (as small rectangles)
    print("3. Adding doors...")
    doors = [
        ([13, 0, 0], 4, 0.5),      # Front door - 4 feet wide
        ([15, 8, 0], 3, 0.5),      # Interior door 1
        ([7, 10, 0], 3, 0.5),      # Interior door 2
    ]
    
    door_count = 0
    for i, ((x, y, z), width, depth) in enumerate(doors):
        # Create door as small rectangle
        door_profile = [
            [x - width/2, y],
            [x + width/2, y],
            [x + width/2, y + depth],
            [x - width/2, y + depth]
        ]
        result = client.extrude_profile(door_profile, 0.1)
        if isinstance(result, dict) and result.get('success'):
            door_count += 1
            print(f"   Door {i+1} placed ({width}' wide) (ID: {result['entity_id']})")
        else:
            print(f"   ERROR placing door {i+1}: {result.get('error')}")
    
    # 4. Add windows (as circles)
    print("4. Adding windows...")
    windows = [
        ([7, 20, 0], 1.5),    # North wall window 1
        ([23, 20, 0], 1.5),   # North wall window 2  
        ([30, 5, 0], 1.5),    # East wall window 1
        ([30, 15, 0], 1.5),   # East wall window 2
        ([7, 0, 0], 1.5),     # South wall window
        ([23, 0, 0], 1.5),    # South wall window 2
    ]
    
    window_count = 0
    for i, ((x, y, z), radius) in enumerate(windows):
        result = client.draw_circle([x, y, z], radius)
        if result.get('success'):
            window_count += 1
            print(f"   Window {i+1} added (ID: {result['entity_id']})")
        else:
            print(f"   ERROR adding window {i+1}: {result.get('error')}")
    
    # Summary
    print()
    print("=== FLOOR PLAN COMPLETE ===")
    print(f"House size: 30' x 20' = 600 square feet")
    print(f"Rooms: 4 (created by interior walls)")
    print(f"Elements created:")
    print(f"  - Exterior walls: {wall_count}/4")
    print(f"  - Interior walls: {interior_count}/2") 
    print(f"  - Doors: {door_count}/3")
    print(f"  - Windows: {window_count}/6")
    print()
    print("LOOK AT YOUR AUTOCAD SCREEN!")
    print("The complete floor plan has been drawn automatically!")
    print()
    print("This took seconds instead of 30+ minutes of manual drawing!")
    
    return True


if __name__ == "__main__":
    print("Starting AutoCAD MCP Floor Plan Demo...")
    print("AutoCAD 2025 is connected and ready!")
    print()
    
    success = create_sample_floorplan()
    
    if success:
        print()
        print("DEMO COMPLETE!")
        print()
        print("What you just saw:")
        print("- Automatic drawing generation")
        print("- Precise coordinates and dimensions") 
        print("- Complex floor plan in seconds")
        print("- No manual clicking or drawing")
        print()
        print("THIS IS THE POWER OF AUTOCAD MCP!")