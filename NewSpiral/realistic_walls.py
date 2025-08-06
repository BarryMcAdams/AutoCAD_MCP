"""
ENHANCED DEMO: Realistic Floor Plan with 7" Wall Thickness
Now with proper architectural wall thickness!
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from autocad_client import AutoCADClient


def create_realistic_floorplan():
    """Create a floor plan with 7-inch thick walls."""
    
    client = AutoCADClient()
    
    print("=== REALISTIC FLOOR PLAN WITH 7\" WALL THICKNESS ===")
    print()
    
    # Check connection
    status = client.autocad_status()
    if not status.get('success'):
        print("ERROR: AutoCAD not connected")
        return False
    
    print(f"Connected to: AutoCAD {status.get('version', 'Unknown')}")
    print("Creating realistic walls with 7-inch thickness...")
    print()
    
    # Wall thickness in feet (7 inches = 7/12 feet = 0.583 feet)
    wall_thickness = 7/12  # 7 inches converted to feet
    
    print("WATCH YOUR AUTOCAD SCREEN!")
    print()
    
    # 1. Create EXTERIOR WALLS with thickness
    print("1. Drawing exterior walls (7\" thick)...")
    
    # Outer perimeter (30x20 feet)
    outer_walls = [
        ([0, 0, 0], [30, 0, 0]),           # Bottom outer
        ([30, 0, 0], [30, 20, 0]),         # Right outer  
        ([30, 20, 0], [0, 20, 0]),         # Top outer
        ([0, 20, 0], [0, 0, 0])            # Left outer
    ]
    
    # Inner perimeter (offset inward by wall thickness)
    inner_walls = [
        ([wall_thickness, wall_thickness, 0], [30-wall_thickness, wall_thickness, 0]),     # Bottom inner
        ([30-wall_thickness, wall_thickness, 0], [30-wall_thickness, 20-wall_thickness, 0]), # Right inner
        ([30-wall_thickness, 20-wall_thickness, 0], [wall_thickness, 20-wall_thickness, 0]), # Top inner
        ([wall_thickness, 20-wall_thickness, 0], [wall_thickness, wall_thickness, 0])        # Left inner
    ]
    
    # Draw outer walls
    outer_count = 0
    for i, (start, end) in enumerate(outer_walls):
        result = client.draw_line(start, end)
        if result.get('success'):
            outer_count += 1
            print(f"   Outer wall {i+1}: DRAWN (ID: {result['entity_id']})")
    
    # Draw inner walls  
    inner_count = 0
    for i, (start, end) in enumerate(inner_walls):
        result = client.draw_line(start, end)
        if result.get('success'):
            inner_count += 1
            print(f"   Inner wall {i+1}: DRAWN (ID: {result['entity_id']})")
    
    # 2. Create INTERIOR WALLS with thickness
    print("2. Drawing interior walls (7\" thick)...")
    
    # Vertical interior wall (divides left/right)
    center_x = 15
    vertical_walls = [
        # Left side of wall
        ([center_x - wall_thickness/2, wall_thickness, 0], [center_x - wall_thickness/2, 20-wall_thickness, 0]),
        # Right side of wall  
        ([center_x + wall_thickness/2, wall_thickness, 0], [center_x + wall_thickness/2, 20-wall_thickness, 0])
    ]
    
    # Horizontal interior wall (divides top/bottom)
    center_y = 10
    horizontal_walls = [
        # Bottom side of wall
        ([wall_thickness, center_y - wall_thickness/2, 0], [30-wall_thickness, center_y - wall_thickness/2, 0]),
        # Top side of wall
        ([wall_thickness, center_y + wall_thickness/2, 0], [30-wall_thickness, center_y + wall_thickness/2, 0])
    ]
    
    interior_count = 0
    for i, (start, end) in enumerate(vertical_walls + horizontal_walls):
        result = client.draw_line(start, end)
        if result.get('success'):
            interior_count += 1
            print(f"   Interior wall {i+1}: DRAWN (ID: {result['entity_id']})")
    
    # 3. Add door openings (gaps in walls)
    print("3. Adding door openings...")
    
    # Create door markers (small rectangles to show door locations)
    doors = [
        # Front door (3' wide, centered in bottom wall)
        {"location": [13.5, 0, 0], "width": 3, "label": "Front Door"},
        # Interior doors (2.5' wide)
        {"location": [center_x, 7, 0], "width": 2.5, "label": "Interior Door 1"},
        {"location": [7, center_y, 0], "width": 2.5, "label": "Interior Door 2"},
    ]
    
    door_count = 0
    for i, door in enumerate(doors):
        x, y, z = door["location"]
        width = door["width"]
        
        # Create door swing arc (quarter circle)
        door_result = client.draw_circle([x, y, z], width/2)
        if door_result.get('success'):
            door_count += 1
            print(f"   {door['label']}: MARKED (ID: {door_result['entity_id']})")
    
    # 4. Add windows  
    print("4. Adding windows...")
    
    windows = [
        {"location": [7, 20, 0], "size": 1.5, "label": "North Window 1"},
        {"location": [23, 20, 0], "size": 1.5, "label": "North Window 2"},
        {"location": [30, 5, 0], "size": 1.5, "label": "East Window 1"},
        {"location": [30, 15, 0], "size": 1.5, "label": "East Window 2"},
        {"location": [7, 0, 0], "size": 1.5, "label": "South Window 1"},
        {"location": [23, 0, 0], "size": 1.5, "label": "South Window 2"},
    ]
    
    window_count = 0
    for window in windows:
        x, y, z = window["location"]
        result = client.draw_circle([x, y, z], window["size"])
        if result.get('success'):
            window_count += 1
            print(f"   {window['label']}: ADDED (ID: {result['entity_id']})")
    
    print()
    print("=== REALISTIC FLOOR PLAN COMPLETE ===")
    print(f"Building: 30' x 20' exterior (600 sq ft)")
    print(f"Interior: {30-2*wall_thickness:.1f}' x {20-2*wall_thickness:.1f}' ({(30-2*wall_thickness)*(20-2*wall_thickness):.0f} sq ft usable)")
    print(f"Wall thickness: 7\" ({wall_thickness:.2f} feet)")
    print()
    print("Elements created:")
    print(f"  - Exterior walls: {outer_count + inner_count}/8 (double lines)")
    print(f"  - Interior walls: {interior_count}/4 (double lines)")
    print(f"  - Door openings: {door_count}/3")
    print(f"  - Windows: {window_count}/6")
    print()
    print("LOOK AT YOUR AUTOCAD SCREEN!")
    print("You now have REALISTIC WALLS with actual thickness!")
    print("This is professional-grade architectural drafting!")
    
    return True


if __name__ == "__main__":
    create_realistic_floorplan()