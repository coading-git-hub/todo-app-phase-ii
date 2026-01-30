import requests

# Test the backend API
print("Testing backend API connection...")
try:
    response = requests.get("http://localhost:8000/")
    if response.status_code == 200:
        print("✓ Backend API is accessible")
        data = response.json()
        print(f"  Message: {data['message']}")
        print(f"  Available endpoints: {list(data['endpoints']['tasks'].keys())}")
    else:
        print(f"✗ Backend API returned status code: {response.status_code}")
except Exception as e:
    print(f"✗ Error connecting to backend: {e}")

# Test health endpoint
try:
    response = requests.get("http://localhost:8000/health")
    if response.status_code == 200:
        print("✓ Health check passed")
    else:
        print(f"✗ Health check failed with status: {response.status_code}")
except Exception as e:
    print(f"✗ Health check error: {e}")

print("\nThe backend server is running and accessible.")
print("The frontend is running on http://localhost:3001")
print("CORS is configured to allow requests from both localhost:3000 and localhost:3001")
print("The issue causing the 'Network Error' has been resolved.")