"""
Direct COM interface test - try different AutoCAD connection approaches
"""

import win32com.client
import pythoncom

def test_autocad_com_approaches():
    print("Testing Different AutoCAD COM Approaches")
    print("=" * 45)
    
    try:
        pythoncom.CoInitialize()
        
        # Approach 1: Try GetActiveObject first
        print("1. Testing GetActiveObject...")
        try:
            app = win32com.client.GetActiveObject("AutoCAD.Application")
            print(f"   [OK] Connected via GetActiveObject")
            print(f"   Version: {app.Version}")
            
            # Try to access document
            try:
                doc = app.ActiveDocument
                print(f"   Document Name: {doc.Name}")
                
                # Try to access model space
                try:
                    ms = doc.ModelSpace
                    print(f"   Model Space Count: {ms.Count}")
                    
                    # Try to create a simple line
                    print("\n2. Attempting to create line...")
                    try:
                        # Use variant arrays for points
                        pt1 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [0, 0, 0])
                        pt2 = win32com.client.VARIANT(pythoncom.VT_ARRAY | pythoncom.VT_R8, [100, 100, 0])
                        
                        line = ms.AddLine(pt1, pt2)
                        print(f"   [SUCCESS] Line created! Handle: {line.Handle}")
                        
                        # Force regeneration and zoom
                        doc.Regen(1)  # Regen all viewports
                        app.ZoomExtents()
                        
                        print(f"   New Model Space Count: {ms.Count}")
                        print("   ** CHECK AUTOCAD FOR VISIBLE LINE **")
                        
                        return True
                        
                    except Exception as e:
                        print(f"   [FAIL] Line creation error: {e}")
                        
                except Exception as e:
                    print(f"   [FAIL] Model space access error: {e}")
                    
            except Exception as e:
                print(f"   [FAIL] Document access error: {e}")
                
        except Exception as e:
            print(f"   [FAIL] GetActiveObject error: {e}")
            
        # Approach 2: Try Dispatch
        print("\n3. Testing Dispatch approach...")
        try:
            app = win32com.client.Dispatch("AutoCAD.Application")
            print(f"   [OK] Connected via Dispatch")
            print(f"   Visible: {app.Visible}")
            
        except Exception as e:
            print(f"   [FAIL] Dispatch error: {e}")
            
        # Approach 3: Try specific version
        print("\n4. Testing specific version...")
        try:
            app = win32com.client.Dispatch("AutoCAD.Application.25")
            print(f"   [OK] Connected to version 25")
            
        except Exception as e:
            print(f"   [FAIL] Version 25 error: {e}")
            
    except Exception as e:
        print(f"[FAIL] COM initialization error: {e}")
        
    return False

if __name__ == '__main__':
    print("IMPORTANT: AutoCAD 2025 should be running!")
    
    success = test_autocad_com_approaches()
    if success:
        print("\nDirect COM approach working!")
    else:
        print("\nAll COM approaches failed.")
    
    print("Test completed.")