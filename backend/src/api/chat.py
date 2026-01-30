from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Dict, Any
from ..db.database_async import get_async_session
from ..models.message import MessageCreate
from ..models.user import User
from ..services.conversation_service import ConversationService
from ..agents.todo_agent import TodoAgent
import uuid
from sqlalchemy import select
from ..middleware.jwt_auth import verify_token

router = APIRouter()

@router.post("/chat")
async def process_chat_message(
    message_data: Dict[str, Any],
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    """
    Process natural language chat message from the user.

    Args:
        message_data: Contains conversation_id (optional) and message content
        current_user: The authenticated user
        session: Database session

    Returns:
        Dict with conversation_id, response, and tool_calls
    """
    try:
        # Extract message and conversation_id from request
        message_content = message_data.get("message")
        if not message_content:
            raise HTTPException(status_code=400, detail="Message content is required")

        conversation_id = message_data.get("conversation_id")

        # Initialize services
        conversation_service = ConversationService(session)

        # Get or create conversation using the authenticated user
        if conversation_id:
            conversation = await conversation_service.get_conversation_by_id(conversation_id, current_user.id)
            if not conversation:
                raise HTTPException(status_code=404, detail="Conversation not found")
        else:
            conversation = await conversation_service.create_conversation(current_user.id)

        # Initialize the TodoAgent and process the request
        # Create a separate session for the agent to avoid transaction issues
        todo_agent = TodoAgent(session)
        result = await todo_agent.process_request(str(current_user.id), message_content)

        return {
            "conversation_id": conversation.id,
            "response": result["response"],
            "tool_calls": result["tool_calls"]
        }

    except Exception as e:
        # Log the error but try to return a basic response
        print(f"Error in chat processing: {str(e)}")
        # If the conversation was created successfully but agent failed,
        # we might still have partial data in the session that needs cleanup
        try:
            session.rollback()
        except:
            pass

        raise HTTPException(status_code=500, detail=f"Error processing chat message: {str(e)}")