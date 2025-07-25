"""
Direct Drawing Test - Bypass decorators to test core functionality
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_direct_drawing():
    print("Direct AutoCAD Drawing Test")
    print("=" * 30)
    
    try:
        # Import our utilities
        from utils import get_autocad_instance
        
        print("1. Getting AutoCAD instance...")
        acad = get_autocad_instance()
        print(f"   [OK] Connected to AutoCAD")
        print(f"   App: {acad.app.Name}")
        print(f"   Doc: {acad.doc.Name}")
        
        print("2. Testing basic line creation...")
        start_point = [0, 0, 0]
        end_point = [100, 100, 0]
        
        line = acad.model.AddLine(start_point, end_point)
        # Skip layer assignment - may be causing the issue
        # line.Layer = "DIRECT_TEST"
        
        print(f"   [OK] Line created - ID: {line.ObjectID}")
        
        print("3. Testing circle creation...")
        center_point = [50, 50, 0]
        radius = 25
        
        circle = acad.model.AddCircle(center_point, radius)
        # Skip layer assignment
        # circle.Layer = "DIRECT_TEST"
        
        print(f"   [OK] Circle created - ID: {circle.ObjectID}")
        
        print("4. Testing 3D box creation...")
        box_corner = [0, 0, 0]
        box = acad.model.modelspace.AddBox(box_corner, 30, 20, 15)
        # Skip layer assignment
        # box.Layer = "DIRECT_TEST"
        
        print(f"   [OK] 3D Box created - ID: {box.ObjectID}")
        
        print("\n[SUCCESS] All direct operations completed!")
        print("Check AutoCAD for entities on layer DIRECT_TEST")
        return True
        
    except Exception as e:
        print(f"   [FAIL] Error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == '__main__':
    print("IMPORTANT: AutoCAD 2025 should be running!")
    
    success = test_direct_drawing()
    if success:
        print("\nDirect operations work - the issue is with decorators/Flask integration")
    else:
        print("\nDirect operations failed - fundamental connection issue")
    
    print("Test completed.")