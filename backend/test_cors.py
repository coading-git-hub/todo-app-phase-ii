#!/usr/bin/env python3
"""
Test script to verify that CORS headers are properly configured after our fixes.
"""

from src.main import app
from fastapi.testclient import TestClient

def test_cors_headers():
    print("Testing CORS headers configuration...")

    client = TestClient(app)

    # Test a preflight OPTIONS request to simulate CORS
    headers = {
        "Origin": "http://localhost:3000",
        "Access-Control-Request-Method": "GET",
        "Access-Control-Request-Headers": "X-Requested-With, content-type",
    }

    # Test preflight request to tasks endpoint
    response = client.options("/api/tasks/", headers=headers)
    print(f"CORS preflight (OPTIONS) to /api/tasks/ status: {response.status_code}")

    if response.status_code == 200:
        cors_headers = {
            'access-control-allow-origin': response.headers.get('access-control-allow-origin'),
            'access-control-allow-credentials': response.headers.get('access-control-allow-credentials'),
            'access-control-allow-methods': response.headers.get('access-control-allow-methods'),
            'access-control-allow-headers': response.headers.get('access-control-allow-headers'),
        }

        print(f"CORS Headers received: {cors_headers}")

        # Check if the origin is allowed
        if cors_headers['access-control-allow-origin'] == "http://localhost:3000":
            print("✅ SUCCESS: CORS origin is properly configured!")
        elif cors_headers['access-control-allow-origin'] == "*":
            print("✅ SUCCESS: CORS wildcard origin is configured (less secure but functional)")
        else:
            print(f"❌ ISSUE: Origin not properly set. Got: {cors_headers['access-control-allow-origin']}")

        # Test a regular GET request with origin header
        get_response = client.get("/api/tasks/", headers={"Origin": "http://localhost:3000"})
        print(f"GET request with origin status: {get_response.status_code}")

        if get_response.status_code == 401:  # Expected due to authentication
            print("✅ GET request returns 401 (expected - requires auth), not 404 or CORS error")
        elif get_response.status_code == 404:
            print("❌ GET request returns 404 - route not found")
        else:
            print(f"GET request returns: {get_response.status_code}")

    else:
        print(f"❌ Preflight request failed with status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")

    # Test the health endpoint for CORS as well
    health_response = client.options("/health", headers=headers)
    print(f"CORS preflight to /health status: {health_response.status_code}")

if __name__ == "__main__":
    test_cors_headers()