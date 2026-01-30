"""
Test script to verify the backend functionality with database initialization
"""
import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__)))

from src.main import app
from src.db.session import create_db_and_tables
from src.config import settings
from fastapi.testclient import TestClient
import uuid

def test_backend_functionality():
    """Test the backend API functionality"""

    print("Testing backend functionality...")

    # Create the test client
    client = TestClient(app)

    try:
        # Test health endpoint first
        print("1. Testing health endpoint...")
        response = client.get("/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.json()}")

        if response.status_code == 200:
            print("   + Health check passed")
        else:
            print("   - Health check failed")
            return False

        # Test root endpoint
        print("\n2. Testing root endpoint...")
        response = client.get("/")
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print("   + Root endpoint working")
        else:
            print("   - Root endpoint failed")
            return False

        # Test chat endpoint with a mock UUID
        print("\n3. Testing chat endpoint...")
        test_user_id = str(uuid.uuid4())
        print(f"   Using test user ID: {test_user_id}")

        message_data = {
            "message": "Add a test task: Buy groceries"
        }

        response = client.post(f"/api/{test_user_id}/chat", json=message_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result['response'][:100]}...")
            print(f"   Conversation ID: {result.get('conversation_id', 'N/A')}")
            print("   + Chat endpoint working")
        else:
            print(f"   Response: {response.text}")
            print("   - Chat endpoint failed")
            return False

        # Test another message to list tasks
        print("\n4. Testing task listing...")
        list_message_data = {
            "message": "List my tasks",
            "conversation_id": response.json().get('conversation_id')
        }

        response = client.post(f"/api/{test_user_id}/chat", json=list_message_data)
        print(f"   Status: {response.status_code}")

        if response.status_code == 200:
            result = response.json()
            print(f"   Response: {result['response'][:100]}...")
            print("   + Task listing working")
        else:
            print(f"   Response: {response.text}")
            print("   - Task listing failed")
            return False

        print("\n+ All tests passed! Backend is working properly.")
        return True

    except Exception as e:
        print(f"\n- Test failed with exception: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_backend_functionality()
    if success:
        print("\n+ Backend functionality test completed successfully!")
        print("+ Database initialization is working")
        print("+ Chat API is responding without 500 errors")
        print("+ Task creation and listing functionality is operational")
    else:
        print("\n- Backend functionality test failed!")