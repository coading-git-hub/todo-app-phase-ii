import pytest
from fastapi.testclient import TestClient
from sqlmodel import Session, select
from backend.src.main import app
from backend.src.models.user import User
from backend.src.models.task import Task
from backend.src.services.auth import create_access_token
from datetime import timedelta
import uuid


@pytest.fixture
def client():
    with TestClient(app) as test_client:
        yield test_client


def create_test_user_and_token(client, email: str = "test@example.com", password: str = "securepassword123"):
    """Helper function to create a test user and return their JWT token."""
    # Create user
    response = client.post(
        "/api/auth/signup",
        json={"email": email, "password": password}
    )
    assert response.status_code == 201

    # Sign in to get token
    response = client.post(
        "/api/auth/signin",
        json={"email": email, "password": password}
    )
    assert response.status_code == 200

    token = response.json()["access_token"]
    user_id = response.json()["user"]["id"]
    return token, user_id


@pytest.mark.asyncio
def test_get_tasks_returns_users_tasks_only(client):
    """Test that GET /api/tasks returns only the authenticated user's tasks."""
    # Create first user and get their token
    user1_token, user1_id = create_test_user_and_token(client, "user1@example.com")

    # Create second user and get their token
    user2_token, user2_id = create_test_user_and_token(client, "user2@example.com")

    # Create tasks for user 1
    headers1 = {"Authorization": f"Bearer {user1_token}"}
    client.post("/api/tasks", json={"title": "User 1 Task 1"}, headers=headers1)
    client.post("/api/tasks", json={"title": "User 1 Task 2"}, headers=headers1)

    # Create tasks for user 2
    headers2 = {"Authorization": f"Bearer {user2_token}"}
    client.post("/api/tasks", json={"title": "User 2 Task 1"}, headers=headers2)
    client.post("/api/tasks", json={"title": "User 2 Task 2"}, headers=headers2)

    # User 1 should only see their own tasks
    response1 = client.get("/api/tasks", headers=headers1)
    assert response1.status_code == 200
    user1_tasks = response1.json()
    assert len(user1_tasks) == 2
    for task in user1_tasks:
        assert task["user_id"] == user1_id

    # User 2 should only see their own tasks
    response2 = client.get("/api/tasks", headers=headers2)
    assert response2.status_code == 200
    user2_tasks = response2.json()
    assert len(user2_tasks) == 2
    for task in user2_tasks:
        assert task["user_id"] == user2_id


@pytest.mark.asyncio
def test_get_tasks_empty_if_no_tasks(client):
    """Test that GET /api/tasks returns an empty array if the user has no tasks."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.get("/api/tasks", headers=headers)
    assert response.status_code == 200
    tasks = response.json()
    assert tasks == []


@pytest.mark.asyncio
def test_get_tasks_requires_jwt(client):
    """Test that GET /api/tasks returns 401 without a valid JWT token."""
    response = client.get("/api/tasks")
    assert response.status_code == 401


@pytest.mark.asyncio
def test_data_isolation_between_users(client):
    """Test that users cannot access each other's tasks."""
    # Create first user and their tasks
    user1_token, user1_id = create_test_user_and_token(client, "isolation1@example.com")
    headers1 = {"Authorization": f"Bearer {user1_token}"}

    response = client.post("/api/tasks", json={"title": "Private Task"}, headers=headers1)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Create second user
    user2_token, _ = create_test_user_and_token(client, "isolation2@example.com")
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # User 2 should not be able to access user 1's task directly
    # This would require a specific endpoint to access individual tasks, which may not exist
    # But we can test that they only see their own tasks

    # User 2 should see no tasks
    response2 = client.get("/api/tasks", headers=headers2)
    assert response2.status_code == 200
    user2_tasks = response2.json()
    assert len(user2_tasks) == 0

    # User 1 should still see their task
    response1 = client.get("/api/tasks", headers=headers1)
    assert response1.status_code == 200
    user1_tasks = response1.json()
    assert len(user1_tasks) == 1
    assert user1_tasks[0]["id"] == task_id


@pytest.mark.asyncio
def test_create_task_with_title_only(client):
    """Test creating a task with only a title."""
    token, user_id = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/tasks", json={"title": "Test Task"}, headers=headers)
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] is None
    assert data["completed"] is False
    assert data["user_id"] == user_id


@pytest.mark.asyncio
def test_create_task_with_title_and_description(client):
    """Test creating a task with title and description."""
    token, user_id = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/tasks",
        json={"title": "Test Task", "description": "Test Description"},
        headers=headers
    )
    assert response.status_code == 201

    data = response.json()
    assert data["title"] == "Test Task"
    assert data["description"] == "Test Description"
    assert data["completed"] is False
    assert data["user_id"] == user_id


@pytest.mark.asyncio
def test_create_task_requires_jwt(client):
    """Test that creating a task requires a valid JWT token."""
    response = client.post("/api/tasks", json={"title": "Test Task"})
    assert response.status_code == 401


@pytest.mark.asyncio
def test_create_task_validates_title_required(client):
    """Test that creating a task requires a title."""
    token = create_test_user_and_token(client)[0]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/tasks", json={"description": "No title"}, headers=headers)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
def test_create_task_validates_title_max_length(client):
    """Test that creating a task validates title max length."""
    token = create_test_user_and_token(client)[0]
    headers = {"Authorization": f"Bearer {token}"}

    long_title = "x" * 201  # Exceeds max length of 200
    response = client.post("/api/tasks", json={"title": long_title}, headers=headers)
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
def test_create_task_validates_description_max_length(client):
    """Test that creating a task validates description max length."""
    token = create_test_user_and_token(client)[0]
    headers = {"Authorization": f"Bearer {token}"}

    long_description = "x" * 2001  # Exceeds max length of 2000
    response = client.post(
        "/api/tasks",
        json={"title": "Test", "description": long_description},
        headers=headers
    )
    assert response.status_code == 422  # Validation error


@pytest.mark.asyncio
def test_update_task_title(client):
    """Test updating a task's title."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post("/api/tasks", json={"title": "Original Title"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Update the task
    response = client.put(f"/api/tasks/{task_id}", json={"title": "Updated Title"}, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["title"] == "Updated Title"
    assert data["id"] == task_id


@pytest.mark.asyncio
def test_update_task_description(client):
    """Test updating a task's description."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post(
        "/api/tasks",
        json={"title": "Test Title", "description": "Original Description"},
        headers=headers
    )
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Update the task
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"description": "Updated Description"},
        headers=headers
    )
    assert response.status_code == 200

    data = response.json()
    assert data["description"] == "Updated Description"
    assert data["title"] == "Test Title"  # Title should remain unchanged
    assert data["id"] == task_id


@pytest.mark.asyncio
def test_update_task_completion_status(client):
    """Test updating a task's completion status."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post("/api/tasks", json={"title": "Test Title"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Verify it starts as not completed
    response = client.get(f"/api/tasks", headers=headers)
    tasks = response.json()
    task = next((t for t in tasks if t["id"] == task_id), None)
    assert task is not None
    assert task["completed"] is False

    # Update the completion status
    response = client.put(f"/api/tasks/{task_id}", json={"completed": True}, headers=headers)
    assert response.status_code == 200

    data = response.json()
    assert data["completed"] is True
    assert data["id"] == task_id


@pytest.mark.asyncio
def test_update_task_requires_jwt(client):
    """Test that updating a task requires a valid JWT token."""
    # Create a task first
    token, _ = create_test_user_and_token(client, "update@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/tasks", json={"title": "Test Title"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Try to update without token
    response = client.put(f"/api/tasks/{task_id}", json={"title": "Updated"})
    assert response.status_code == 401


@pytest.mark.asyncio
def test_update_task_ownership_verification(client):
    """Test that users can only update their own tasks."""
    # Create first user and task
    user1_token, _ = create_test_user_and_token(client, "owner@example.com")
    headers1 = {"Authorization": f"Bearer {user1_token}"}

    response = client.post("/api/tasks", json={"title": "Owner's Task"}, headers=headers1)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Create second user
    user2_token, _ = create_test_user_and_token(client, "nonowner@example.com")
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # Second user should not be able to update first user's task
    response = client.put(f"/api/tasks/{task_id}", json={"title": "Hacked Title"}, headers=headers2)
    assert response.status_code == 404  # Should return 404 to avoid leaking information


@pytest.mark.asyncio
def test_update_nonexistent_task(client):
    """Test updating a nonexistent task."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to update a task with a random UUID
    fake_task_id = str(uuid.uuid4())
    response = client.put(f"/api/tasks/{fake_task_id}", json={"title": "Fake Update"}, headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_update_task_with_empty_body(client):
    """Test updating a task with an empty body (no fields)."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post("/api/tasks", json={"title": "Test Title"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Try to update with empty body
    response = client.put(f"/api/tasks/{task_id}", json={}, headers=headers)
    assert response.status_code == 400  # Should return 400 for no fields to update


@pytest.mark.asyncio
def test_delete_task_successful(client):
    """Test successfully deleting a task."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post("/api/tasks", json={"title": "Task to Delete"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Verify the task exists
    response = client.get("/api/tasks", headers=headers)
    tasks = response.json()
    assert len([t for t in tasks if t["id"] == task_id]) == 1

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Verify the task is gone
    response = client.get("/api/tasks", headers=headers)
    tasks = response.json()
    assert len([t for t in tasks if t["id"] == task_id]) == 0


@pytest.mark.asyncio
def test_delete_task_requires_jwt(client):
    """Test that deleting a task requires a valid JWT token."""
    # Create a task first
    token, _ = create_test_user_and_token(client, "delete@example.com")
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post("/api/tasks", json={"title": "Task to Delete"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Try to delete without token
    response = client.delete(f"/api/tasks/{task_id}")
    assert response.status_code == 401


@pytest.mark.asyncio
def test_delete_task_ownership_verification(client):
    """Test that users can only delete their own tasks."""
    # Create first user and task
    user1_token, _ = create_test_user_and_token(client, "owner@example.com")
    headers1 = {"Authorization": f"Bearer {user1_token}"}

    response = client.post("/api/tasks", json={"title": "Owner's Task"}, headers=headers1)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Create second user
    user2_token, _ = create_test_user_and_token(client, "nonowner@example.com")
    headers2 = {"Authorization": f"Bearer {user2_token}"}

    # Second user should not be able to delete first user's task
    response = client.delete(f"/api/tasks/{task_id}", headers=headers2)
    assert response.status_code == 404  # Should return 404 to avoid leaking information

    # First user should still be able to access their task
    response = client.get(f"/api/tasks", headers=headers1)
    tasks = response.json()
    assert len([t for t in tasks if t["id"] == task_id]) == 1


@pytest.mark.asyncio
def test_delete_nonexistent_task(client):
    """Test deleting a nonexistent task."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Try to delete a task with a random UUID
    fake_task_id = str(uuid.uuid4())
    response = client.delete(f"/api/tasks/{fake_task_id}", headers=headers)
    assert response.status_code == 404


@pytest.mark.asyncio
def test_delete_task_idempotent_behavior(client):
    """Test that deleting an already-deleted task returns 404."""
    token, _ = create_test_user_and_token(client)
    headers = {"Authorization": f"Bearer {token}"}

    # Create a task first
    response = client.post("/api/tasks", json={"title": "Task to Delete"}, headers=headers)
    assert response.status_code == 201
    task_id = response.json()["id"]

    # Delete the task
    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 204

    # Try to delete the same task again
    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 404  # Should return 404 for nonexistent task