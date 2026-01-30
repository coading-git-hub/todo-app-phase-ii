"""
Test script to verify the chat API endpoint is working properly
"""
import uuid
from src.api.chat import process_chat_message
from sqlmodel import Session, create_engine
from sqlmodel.pool import StaticPool
from src.db.session import get_session

def test_chat_api():
    """Test the chat API endpoint directly"""

    print("Testing chat API endpoint...")

    # Create an in-memory SQLite database for testing
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )

    # Create tables
    from src.models.user import User
    from src.models.task import Task
    from src.models.message import Message
    from src.models.conversation import Conversation
    from src.models import SQLModel
    SQLModel.metadata.create_all(bind=engine)

    # Create a session
    with Session(engine) as session:
        # Create a test user ID (UUID)
        test_user_id = str(uuid.uuid4())

        # Prepare test message data
        message_data = {
            "message": "Add a test task: Buy groceries",
            "conversation_id": None
        }

        try:
            # Call the chat API endpoint function directly
            result = process_chat_message(
                user_id=test_user_id,
                message_data=message_data,
                session=session
            )

            print(f" ok API call succeeded!")
            print(f"  Conversation ID: {result['conversation_id']}")
            print(f"  Response: {result['response']}")
            print(f"  Tool calls: {len(result['tool_calls'])}")

            # Try another message to list tasks
            list_message_data = {
                "message": "List my tasks",
                "conversation_id": result['conversation_id']
            }

            list_result = process_chat_message(
                user_id=test_user_id,
                message_data=list_message_data,
                session=session
            )

            print(f"ok List tasks succeeded!")
            print(f"  Response: {list_result['response']}")

        except Exception as e:
            print(f" API call failed: {str(e)}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    test_chat_api()