#!/usr/bin/env python3
"""
Detailed CORS and error testing to identify the 500 Internal Server Error
"""

from src.main import app
from fastapi.testclient import TestClient

def test_detailed_error():
    print("Testing detailed error scenarios...")

    client = TestClient(app)

    # Test with a valid-looking but fake JWT token to see if authentication causes 500
    print("\n1. Testing GET /api/tasks/ with fake JWT token:")
    try:
        response = client.get("/api/tasks/", headers={
            "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
        })
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test with malformed token
    print("\n2. Testing GET /api/tasks/ with malformed token:")
    try:
        response = client.get("/api/tasks/", headers={
            "Authorization": "Bearer invalid.token.format"
        })
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test without any authorization header
    print("\n3. Testing GET /api/tasks/ without Authorization header:")
    try:
        response = client.get("/api/tasks/")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test POST without authorization
    print("\n4. Testing POST /api/tasks/ without Authorization header:")
    try:
        response = client.post("/api/tasks/", json={"title": "test"})
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

    # Test a simple endpoint to make sure the server itself works
    print("\n5. Testing health endpoint:")
    try:
        response = client.get("/health")
        print(f"   Status: {response.status_code}")
        print(f"   Response: {response.text}")
    except Exception as e:
        print(f"   Exception: {e}")

    print("\nDetailed error testing completed.")

if __name__ == "__main__":
    test_detailed_error()