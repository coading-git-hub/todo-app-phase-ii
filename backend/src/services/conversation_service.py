from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.conversation import Conversation, ConversationCreate
from ..models.message import Message
import uuid


class ConversationService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_conversation(self, user_id: uuid.UUID) -> Conversation:
        """Create a new conversation for a user."""
        conversation = Conversation(user_id=user_id)
        self.session.add(conversation)
        await self.session.commit()
        await self.session.refresh(conversation)
        return conversation

    async def get_conversation_by_id(self, conversation_id: int, user_id: uuid.UUID) -> Optional[Conversation]:
        """Get a conversation by ID for a user."""
        query = select(Conversation).where(
            Conversation.id == conversation_id,
            Conversation.user_id == user_id
        )
        result = await self.session.execute(query)
        return result.scalars().first()

    async def get_user_conversations(self, user_id: uuid.UUID) -> List[Conversation]:
        """Get all conversations for a user."""
        query = select(Conversation).where(Conversation.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_conversation_messages(self, conversation_id: int, user_id: uuid.UUID) -> List[Message]:
        """Get all messages for a conversation, ensuring user owns the conversation."""
        query = select(Message).join(Conversation).where(
            Message.conversation_id == conversation_id,
            Conversation.user_id == user_id
        ).order_by(Message.created_at.asc())
        result = await self.session.execute(query)
        return result.scalars().all()