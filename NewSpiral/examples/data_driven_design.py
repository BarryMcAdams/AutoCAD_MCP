"""
Example 3: Data-Driven Design
Read data from a file/database and automatically create 3D models
This is like "mail merge" but for CAD drawings
"""

import sys
sys.path.append('..')
from autocad_client import AutoCADClient
import json


def create_pipe_layout_from_data():
    """Create a piping layout from configuration data."""
    
    client = AutoCADClient()
    
    print("🔧 Creating Pipe Layout from Data...")
    
    # Check AutoCAD connection
    status = client.autocad_status()
    if not status.get('success'):
        print("❌ AutoCAD not connected. Please start AutoCAD 2025 with a drawing open.")
        return
    
    # Sample pipe data (in real project, this would come from CSV/Excel/database)
    pipe_data = [
        {
            "pipe_id": "P001",
            "start_point": [0, 0, 0],
            "end_point": [10, 0, 0],
            "diameter": 0.5,
            "material": "Steel",
            "pressure_rating": "150 PSI"
        },
        {
            "pipe_id": "P002", 
            "start_point": [10, 0, 0],
            "end_point": [10, 8, 0],
            "diameter": 0.5,
            "material": "Steel",
            "pressure_rating": "150 PSI"
        },
        {
            "pipe_id": "P003",
            "start_point": [10, 8, 0],
            "end_point": [20, 8, 0], 
            "diameter": 0.75,
            "material": "Copper",
            "pressure_rating": "200 PSI"
        },
        {
            "pipe_id": "P004",
            "start_point": [20, 8, 0],
            "end_point": [20, 0, 0],
            "diameter": 0.75,
            "material": "Copper", 
            "pressure_rating": "200 PSI"
        }
    ]
    
    print("✅ AutoCAD connected. Creating pipe layout...")
    
    created_pipes = []
    
    for pipe in pipe_data:
        print(f"\n📏 Creating pipe {pipe['pipe_id']}...")
        print(f"   Material: {pipe['material']}")
        print(f"   Diameter: {pipe['diameter']} inches")
        print(f"   From: {pipe['start_point']} to {pipe['end_point']}")
        
        # Create the pipe centerline
        line_result = client.draw_line(pipe['start_point'], pipe['end_point'])
        
        if line_result.get('success'):
            pipe_centerline_id = line_result['entity_id']
            print(f"   ✅ Centerline created: {pipe_centerline_id}")
            
            # Create pipe diameter indicators (circles at start and end)
            radius = pipe['diameter'] / 2
            
            start_circle = client.draw_circle(pipe['start_point'], radius)
            end_circle = client.draw_circle(pipe['end_point'], radius) 
            
            if start_circle.get('success') and end_circle.get('success'):
                print(f"   ✅ Diameter indicators created")
                
                created_pipes.append({
                    'pipe_id': pipe['pipe_id'],
                    'centerline_id': pipe_centerline_id,
                    'start_circle_id': start_circle['entity_id'],
                    'end_circle_id': end_circle['entity_id'],
                    'material': pipe['material'],
                    'diameter': pipe['diameter']
                })
        else:
            print(f"   ❌ Failed to create pipe {pipe['pipe_id']}: {line_result.get('error')}")
    
    # Create junction boxes at connection points
    junction_points = [
        [10, 0, 0],  # Connection point 1
        [10, 8, 0],  # Connection point 2  
        [20, 8, 0],  # Connection point 3
        [20, 0, 0],  # Connection point 4
    ]
    
    print(f"\n🔗 Creating junction boxes...")
    for i, point in enumerate(junction_points):
        # Create a small square to represent junction box
        box_size = 1
        box_profile = [
            [point[0] - box_size/2, point[1] - box_size/2],
            [point[0] + box_size/2, point[1] - box_size/2],
            [point[0] + box_size/2, point[1] + box_size/2],
            [point[0] - box_size/2, point[1] + box_size/2]
        ]
        
        box_result = client.extrude_profile(box_profile, 0.5)
        if box_result.get('success'):
            print(f"   ✅ Junction box {i+1} at {point}: {box_result['entity_id']}")
    
    print(f"\n🎉 Pipe layout complete!")
    print(f"📊 Summary:")
    print(f"   - Total pipes created: {len(created_pipes)}")
    print(f"   - Steel pipes: {len([p for p in created_pipes if p['material'] == 'Steel'])}")
    print(f"   - Copper pipes: {len([p for p in created_pipes if p['material'] == 'Copper'])}")
    print(f"   - Junction boxes: {len(junction_points)}")
    
    # Save the pipe data for reference
    with open('pipe_layout_report.json', 'w') as f:
        json.dump({
            'created_pipes': created_pipes,
            'junction_points': junction_points,
            'total_pipes': len(created_pipes)
        }, f, indent=2)
    
    print(f"📋 Pipe layout report saved to: pipe_layout_report.json")


def create_furniture_layout():
    """Create office furniture layout from data."""
    
    client = AutoCADClient()
    
    print("🪑 Creating Office Furniture Layout...")
    
    # Check AutoCAD connection
    status = client.autocad_status()
    if not status.get('success'):
        print("❌ AutoCAD not connected.")
        return
    
    # Furniture data (could come from spreadsheet)
    furniture_data = [
        {"type": "desk", "position": [2, 2, 0], "width": 5, "depth": 3, "height": 2.5},
        {"type": "desk", "position": [10, 2, 0], "width": 5, "depth": 3, "height": 2.5},
        {"type": "chair", "position": [4.5, 1, 0], "width": 2, "depth": 2, "height": 3},
        {"type": "chair", "position": [12.5, 1, 0], "width": 2, "depth": 2, "height": 3},
        {"type": "bookshelf", "position": [0, 8, 0], "width": 3, "depth": 1, "height": 6},
        {"type": "table", "position": [8, 8, 0], "width": 4, "depth": 2, "height": 2.5},
    ]
    
    print("✅ Creating furniture pieces...")
    
    for item in furniture_data:
        print(f"\n🪑 Creating {item['type']}...")
        
        # Create furniture as simple rectangular solids
        x, y, z = item['position']
        w, d, h = item['width'], item['depth'], item['height']
        
        # Define furniture footprint
        profile = [
            [x, y],
            [x + w, y], 
            [x + w, y + d],
            [x, y + d]
        ]
        
        result = client.extrude_profile(profile, h)
        
        if result.get('success'):
            print(f"   ✅ {item['type'].title()} created: {result['entity_id']}")
            print(f"      Position: ({x}, {y})")
            print(f"      Size: {w}' x {d}' x {h}'")
        else:
            print(f"   ❌ Failed to create {item['type']}")
    
    print(f"\n🏢 Office layout complete!")
    print(f"📊 Furniture count:")
    furniture_types = {}
    for item in furniture_data:
        furniture_types[item['type']] = furniture_types.get(item['type'], 0) + 1
    
    for ftype, count in furniture_types.items():
        print(f"   - {ftype.title()}: {count}")


if __name__ == "__main__":
    print("Choose data-driven example:")
    print("1. Pipe Layout (Industrial)")  
    print("2. Furniture Layout (Office)")
    
    choice = input("Enter choice (1 or 2): ").strip()
    
    if choice == "1":
        create_pipe_layout_from_data()
    elif choice == "2": 
        create_furniture_layout()
    else:
        print("Creating pipe layout (default)...")
        create_pipe_layout_from_data()