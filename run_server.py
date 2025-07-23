"""
Standalone server runner that fixes import issues.
"""

import sys
import os

# Add src to Python path
src_path = os.path.join(os.path.dirname(__file__), 'src')
sys.path.insert(0, src_path)

# Now import and run the server
if __name__ == '__main__':
    from server import app
    from config import config
    
    print(f"Starting AutoCAD MCP Server on {config.HOST}:{config.PORT}")
    print("Make sure AutoCAD 2025 is running...")
    
    app.run(
        host=config.HOST,
        port=config.PORT,
        debug=config.DEBUG,
        threaded=True
    )