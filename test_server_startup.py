"""
Test script to verify server startup and route registration.
"""

import sys
import os

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

try:
    print("Testing imports...")
    from server import app
    from config import config
    
    print("[OK] Imports successful")
    
    # Print all registered routes
    print("\nRegistered routes:")
    for rule in app.url_map.iter_rules():
        print(f"  {rule.rule} -> {rule.methods}")
    
    print(f"\nConfiguration:")
    print(f"  Host: {config.HOST}")
    print(f"  Port: {config.PORT}")
    print(f"  Debug: {config.DEBUG}")
    
    print("\nStarting server...")
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
    
except Exception as e:
    print(f"[ERROR] Error: {e}")
    import traceback
    traceback.print_exc()