from typing import List, Optional
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from ..models.task import Task, TaskCreate, TaskUpdate
from ..models.user import User
import uuid
from datetime import datetime, timezone


class TaskService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_task(self, task_data: TaskCreate, user_id: uuid.UUID) -> Task:
        """Create a new task for a user."""
        task = Task(**task_data.model_dump(), user_id=user_id)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def get_user_tasks(self, user_id: uuid.UUID, completed: Optional[bool] = None) -> List[Task]:
        """Get all tasks for a user, optionally filtered by completion status."""
        query = select(Task).where(Task.user_id == user_id)

        if completed is not None:
            query = query.where(Task.completed == completed)

        result = await self.session.execute(query)
        return result.scalars().all()

    async def get_task_by_id(self, task_id: int, user_id: uuid.UUID) -> Optional[Task]:
        """Get a specific task by ID for a user."""
        query = select(Task).where(Task.id == task_id, Task.user_id == user_id)
        result = await self.session.execute(query)
        return result.scalars().first()

    async def update_task(self, task_id: int, task_update: TaskUpdate, user_id: uuid.UUID) -> Optional[Task]:
        """Update a task for a user."""
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return None

        update_data = task_update.model_dump(exclude_unset=True)
        for field, value in update_data.items():
            setattr(task, field, value)

        task.updated_at = datetime.now(timezone.utc)
        self.session.add(task)
        await self.session.commit()
        await self.session.refresh(task)
        return task

    async def delete_task(self, task_id: int, user_id: uuid.UUID) -> bool:
        """Delete a task for a user."""
        task = await self.get_task_by_id(task_id, user_id)
        if not task:
            return False

        await self.session.delete(task)
        await self.session.commit()
        return True

    async def complete_task(self, task_id: int, user_id: uuid.UUID) -> Optional[Task]:
        """Mark a task as completed."""
        return await self.update_task(task_id, TaskUpdate(completed=True), user_id)