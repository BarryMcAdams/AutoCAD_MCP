"""
Final AutoCAD Test - Apply lessons learned to create visible entities
"""

import win32com.client
import pythoncom
import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def create_working_autocad_connection():
    """Create a working AutoCAD connection using lessons learned"""
    print("Final AutoCAD Connection Test")
    print("=" * 35)
    
    try:
        # Step 1: Initialize COM
        pythoncom.CoInitialize()
        print("1. COM initialized")
        
        # Step 2: Connect using the only method that works
        app = win32com.client.Dispatch("AutoCAD.Application.25")
        app.Visible = True
        print("2. Connected to AutoCAD.Application.25")
        
        # Step 3: Access document (with error handling)
        try:
            doc = app.ActiveDocument
            print(f"3. Document accessed: {doc.Name}")
            
            # Step 4: Access model space
            try:
                ms = doc.ModelSpace
                initial_count = ms.Count
                print(f"4. Model space accessed - Initial entity count: {initial_count}")
                
                # Step 5: Create entities with proper VARIANT arrays
                print("\n5. Creating entities...")
                
                # Create Line
                pt1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0.0, 0.0, 0.0])
                pt2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [100.0, 100.0, 0.0])
                line = ms.AddLine(pt1, pt2)
                print(f"   [OK] Line created: Handle {line.Handle}")
                
                # Create Circle  
                center = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [50.0, 50.0, 0.0])
                circle = ms.AddCircle(center, 25.0)
                print(f"   [OK] Circle created: Handle {circle.Handle}")
                
                # Create 3D Box (the working primitive)
                corner = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [120.0, 0.0, 0.0])
                box = ms.AddBox(corner, 30.0, 20.0, 15.0)
                print(f"   [OK] 3D Box created: Handle {box.Handle}")
                
                # Step 6: Force visibility
                print("\n6. Making entities visible...")
                doc.Regen(1)  # Regenerate all viewports
                app.ZoomExtents()  # Zoom to show all objects
                print("   [OK] Regenerated and zoomed to extents")
                
                # Step 7: Verify creation
                final_count = ms.Count
                print(f"\n7. Final entity count: {final_count}")
                print(f"   Entities added: {final_count - initial_count}")
                
                if final_count > initial_count:
                    print("\n[SUCCESS] Entities created and should be visible in AutoCAD!")
                    print("** CHECK AUTOCAD NOW - YOU SHOULD SEE A LINE, CIRCLE, AND 3D BOX **")
                    return True
                else:
                    print("\n[FAIL] No entities were added")
                    return False
                    
            except Exception as e:
                print(f"   [FAIL] Model space error: {e}")
                return False
                
        except Exception as e:
            print(f"   [FAIL] Document access error: {e}")
            return False
            
    except Exception as e:
        print(f"[FAIL] Connection error: {e}")
        return False

if __name__ == '__main__':
    print("CRITICAL: AutoCAD 2025 must be running with a drawing open!")
    print("This test applies all lessons learned to create VISIBLE entities.\n")
    
    success = create_working_autocad_connection()
    
    if success:
        print("\n" + "="*60)
        print("PHASE 2 BREAKTHROUGH ACHIEVED!")
        print("The AutoCAD COM interface is now working correctly.")
        print("You should see visible entities in AutoCAD 2025.")
        print("="*60)
    else:
        print("\nFinal test failed - AutoCAD 2025 COM interface issues persist")
    
    input("\nPress Enter to exit...")