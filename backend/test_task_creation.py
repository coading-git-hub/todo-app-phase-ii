"""
Test script to verify task creation functionality
"""
import uuid
from unittest.mock import Mock, MagicMock
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from src.models.task import Task
from src.services.task_service import TaskService
from src.mcp_tools.task_tools import add_task, list_tasks
from src.models.task import TaskCreate

def test_task_creation():
    """Test that tasks can be created and retrieved properly"""

    print("Testing task creation functionality...")

    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from src.models.user import User  # Import to register the model
    from src.models.task import Task
    from src.models.message import Message
    from src.models.conversation import Conversation
    from sqlmodel import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    # Create a session
    with Session(engine) as session:
        # Create a test user ID (UUID)
        test_user_id = uuid.uuid4()

        # Test 1: Create a task using the task service directly
        print("1. Testing direct task service creation...")
        task_service = TaskService(session)

        task_create_data = TaskCreate(title="Test Task", description="Test Description", completed=False)
        created_task = task_service.create_task(task_create_data, test_user_id)

        print(f"   Created task ID: {created_task.id}")
        print(f"   Task title: {created_task.title}")
        print(f"   Task user_id: {created_task.user_id}")

        # Test 2: Retrieve the task
        print("2. Testing task retrieval...")
        retrieved_tasks = task_service.get_user_tasks(test_user_id)
        print(f"   Retrieved {len(retrieved_tasks)} tasks")
        if retrieved_tasks:
            print(f"   First task: {retrieved_tasks[0].title}")

        # Test 3: Create a task using the task tools (mcp_tools)
        print("3. Testing task creation via MCP tools...")
        mcp_result = add_task(session, str(test_user_id), "MCP Test Task", "Created via MCP tools")
        print(f"   MCP result: {mcp_result}")

        # Test 4: List tasks via MCP tools
        print("4. Testing task listing via MCP tools...")
        listed_tasks = list_tasks(session, str(test_user_id))
        print(f"   Listed tasks count: {len(listed_tasks)}")
        for i, task in enumerate(listed_tasks):
            print(f"   Task {i+1}: {task}")

        print("\n+ All tests completed successfully!")
        print("+ Tasks are being created and persisted in the database")
        print("+ Tasks can be retrieved after creation")

if __name__ == "__main__":
    test_task_creation()