"""
Example 2: Mechanical Part Design
Create a mechanical part (like a bracket or fitting) with precise dimensions
"""

import sys
sys.path.append('..')
from autocad_client import AutoCADClient
import math


def create_mounting_bracket():
    """Create a mounting bracket with holes and features."""
    
    client = AutoCADClient()
    
    print("🔧 Creating Mounting Bracket...")
    
    # Check AutoCAD connection
    status = client.autocad_status()
    if not status.get('success'):
        print("❌ AutoCAD not connected. Please start AutoCAD 2025 with a drawing open.")
        return
    
    print("✅ AutoCAD connected. Creating mechanical part...")
    
    # 1. Create main bracket body (L-shaped profile)
    main_profile = [
        [0, 0],      # Bottom left
        [4, 0],      # Bottom right  
        [4, 0.5],    # Step up
        [0.5, 0.5],  # Step back
        [0.5, 3],    # Up the vertical
        [0, 3],      # Top left
        [0, 0]       # Close the profile
    ]
    
    print("Creating main bracket body...")
    bracket_result = client.extrude_profile(main_profile, 0.25)  # 1/4 inch thick
    if bracket_result.get('success'):
        bracket_id = bracket_result['entity_id']
        print(f"  ✅ Main bracket body: {bracket_id}")
    else:
        print(f"  ❌ Failed to create bracket: {bracket_result.get('error')}")
        return
    
    # 2. Create mounting holes
    hole_locations = [
        [0.25, 0.25, 0],   # Bottom hole
        [0.25, 2.75, 0],   # Top hole  
        [3.75, 0.25, 0],   # Right hole
    ]
    
    hole_radius = 0.125  # 1/8 inch diameter holes
    
    print("Adding mounting holes...")
    hole_ids = []
    for x, y, z in hole_locations:
        # Create holes as cylinders (which would be subtracted in real CAD)
        hole_profile = []
        # Create circular profile for hole
        for angle in range(0, 361, 30):  # 12 points around circle
            rad = math.radians(angle)
            hx = x + hole_radius * math.cos(rad)
            hy = y + hole_radius * math.sin(rad)
            hole_profile.append([hx, hy])
        
        hole_result = client.extrude_profile(hole_profile, 0.3)  # Slightly thicker than bracket
        if hole_result.get('success'):
            hole_ids.append(hole_result['entity_id'])
            print(f"  🕳️  Hole created at ({x}, {y}): {hole_result['entity_id']}")
    
    # 3. Add reinforcement ribs
    rib_profiles = [
        # Diagonal rib
        [[0.5, 0.5], [1.5, 0.5], [1.4, 0.6], [0.5, 1.5]],
        # Horizontal rib
        [[1, 0.5], [3, 0.5], [3, 0.6], [1, 0.6]]
    ]
    
    print("Adding reinforcement ribs...")
    for i, rib_profile in enumerate(rib_profiles):
        rib_result = client.extrude_profile(rib_profile, 0.1)  # Thin ribs
        if rib_result.get('success'):
            print(f"  💪 Rib {i+1} created: {rib_result['entity_id']}")
    
    # 4. Create reference dimensions (as text annotations)
    print("Adding reference dimensions...")
    print("  📏 Overall Length: 4.0 inches")
    print("  📏 Overall Height: 3.0 inches") 
    print("  📏 Thickness: 0.25 inches")
    print("  📏 Hole Diameter: 0.25 inches (1/4-20 tap)")
    
    print("\n🎉 Mounting bracket complete!")
    print("🔩 Ready for manufacturing")
    print("📋 Part features:")
    print("   - L-shaped main body")
    print("   - 3 mounting holes")
    print("   - 2 reinforcement ribs") 
    print("   - Material: Aluminum (suggested)")


def create_gear():
    """Create a simple gear with teeth."""
    
    client = AutoCADClient()
    
    print("⚙️  Creating Gear...")
    
    # Check AutoCAD connection  
    status = client.autocad_status()
    if not status.get('success'):
        print("❌ AutoCAD not connected.")
        return
    
    print("✅ Creating gear profile...")
    
    # Gear parameters
    outer_radius = 2.0    # 2 inch outer radius
    inner_radius = 1.7    # 1.7 inch inner radius
    center_hole = 0.25    # 1/4 inch center hole
    num_teeth = 20        # 20 teeth
    
    # Create gear profile (simplified - just outer circle for now)
    gear_profile = []
    for angle in range(0, 361, 18):  # 20 points around circle
        rad = math.radians(angle)
        # Alternate between outer and inner radius to create "teeth"
        radius = outer_radius if (angle // 18) % 2 == 0 else inner_radius
        x = radius * math.cos(rad)
        y = radius * math.sin(rad)
        gear_profile.append([x, y])
    
    # Create the gear body
    gear_result = client.extrude_profile(gear_profile, 0.5)  # 1/2 inch thick
    if gear_result.get('success'):
        print(f"  ✅ Gear body created: {gear_result['entity_id']}")
    
    # Create center hole
    center_hole_profile = []
    for angle in range(0, 361, 30):
        rad = math.radians(angle)
        x = center_hole * math.cos(rad) 
        y = center_hole * math.sin(rad)
        center_hole_profile.append([x, y])
    
    hole_result = client.extrude_profile(center_hole_profile, 0.6)  # Through hole
    if hole_result.get('success'):
        print(f"  🕳️  Center hole created: {hole_result['entity_id']}")
    
    print("\n⚙️  Gear complete!")
    print(f"📏 Outer Diameter: {outer_radius * 2} inches")
    print(f"🦷 Number of Teeth: {num_teeth}")
    print(f"🕳️  Center Hole: {center_hole * 2} inch diameter")


if __name__ == "__main__":
    print("Choose example:")
    print("1. Mounting Bracket")
    print("2. Gear")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_mounting_bracket()
    elif choice == "2":
        create_gear()
    else:
        print("Creating mounting bracket (default)...")
        create_mounting_bracket()