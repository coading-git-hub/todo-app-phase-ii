"""
Test script to check if the TodoAgent initializes properly
"""
import os
from unittest.mock import Mock
from src.agents.todo_agent import TodoAgent
from sqlmodel import Session

def test_agent_initialization():
    """Test if the TodoAgent initializes without errors"""

    print("Testing TodoAgent initialization...")

    # Create a mock session
    mock_session = Mock(spec=Session)

    try:
        # Initialize the agent
        agent = TodoAgent(mock_session)

        print(f"+ TodoAgent initialized successfully")
        print(f"  Gemini model available: {agent.gemini_model is not None}")
        print(f"  OpenAI client available: {agent.openai_client is not None}")

        if agent.gemini_model:
            print(f"  Using Gemini model: {agent.gemini_model.model_name}")

        # Test a simple process request
        test_result = agent.process_request("test-user-id", "hello")
        print(f"+ Simple request processed successfully")
        print(f"  Response: {test_result['response'][:100]}...")

    except Exception as e:
        print(f"- TodoAgent initialization failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_agent_initialization()