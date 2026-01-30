#!/usr/bin/env python3
"""
Debug script to test the authentication flow and understand why 403 is returned instead of 401
"""

from src.main import app
from fastapi.testclient import TestClient

def debug_auth():
    print("Debugging authentication flow...")

    client = TestClient(app)

    # Test without any Authorization header
    print("\n1. Testing GET /api/tasks/ without Authorization header:")
    response = client.get("/api/tasks/")
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    # Test with malformed Authorization header
    print("\n2. Testing GET /api/tasks/ with malformed Authorization header:")
    response = client.get("/api/tasks/", headers={"Authorization": "InvalidToken"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    # Test with proper Bearer format but invalid token
    print("\n3. Testing GET /api/tasks/ with Bearer + invalid token:")
    response = client.get("/api/tasks/", headers={"Authorization": "Bearer invalid_token_here"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    # Test POST without Authorization
    print("\n4. Testing POST /api/tasks/ without Authorization header:")
    response = client.post("/api/tasks/", json={"title": "test"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    # Test POST with invalid Authorization
    print("\n5. Testing POST /api/tasks/ with invalid Authorization header:")
    response = client.post("/api/tasks/", json={"title": "test"}, headers={"Authorization": "Bearer invalid_token"})
    print(f"   Status: {response.status_code}")
    print(f"   Response: {response.text}")

    print("\nThe authentication flow debug completed.")

if __name__ == "__main__":
    debug_auth()