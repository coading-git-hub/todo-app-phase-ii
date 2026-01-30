#!/usr/bin/env python3
"""
Test script to verify that the main modules can be imported without errors.
This helps identify issues with our fixes.
"""

def test_imports():
    print("Testing imports...")

    try:
        # Test main application
        from src.main import app
        print("[OK] Main app imported successfully")

        # Test models
        from src.models.task import Task, TaskCreate, TaskRead
        from src.models.user import User, UserCreate
        print("[OK] Models imported successfully")

        # Test API endpoints
        from src.api.tasks import router as tasks_router
        from src.api.chat import router as chat_router
        from src.api.auth import router as auth_router
        print("[OK] API routers imported successfully")

        # Test middleware
        from src.middleware.jwt_auth import verify_token_sync, verify_token
        print("[OK] JWT auth functions imported successfully")

        # Test services
        from src.services.task_service import TaskService
        print("[OK] Task service imported successfully")

        # Test database
        from src.db.session import get_session, engine
        print("[OK] Database session imported successfully")

        print("\nAll imports successful! The application should work correctly.")
        return True

    except Exception as e:
        print(f"[ERROR] Import error: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_imports()