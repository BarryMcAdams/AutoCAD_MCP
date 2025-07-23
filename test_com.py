"""
Test COM connection to AutoCAD
"""
import pythoncom
import win32com.client

def test_autocad_com():
    pythoncom.CoInitialize()
    
    # Test different prog IDs
    prog_ids = [
        "AutoCAD.Application",
        "AutoCAD.Application.25", 
        "AutoCAD.Application.24",
        "AutoCAD.Application.23"
    ]
    
    for prog_id in prog_ids:
        try:
            print(f"Trying {prog_id}...")
            app = win32com.client.GetActiveObject(prog_id)
            print(f"SUCCESS: Connected to {prog_id}")
            print(f"Version: {app.Version}")
            print(f"Document: {app.ActiveDocument.Name}")
            return app
        except Exception as e:
            print(f"Failed {prog_id}: {e}")
    
    print("No AutoCAD instance found")
    return None

if __name__ == "__main__":
    test_autocad_com()