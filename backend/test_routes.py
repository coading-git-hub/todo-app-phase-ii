import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.main import app

def test_available_routes():
    """Test to see what routes are available in the app"""
    print("Available routes:")
    for route in app.routes:
        if hasattr(route, 'methods') and hasattr(route, 'path'):
            print(f"  {route.methods} {route.path}")
        elif hasattr(route, 'path'):
            print(f"  {route.path}")

if __name__ == "__main__":
    test_available_routes()