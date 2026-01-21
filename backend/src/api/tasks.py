from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..middleware.jwt_auth import verify_token
from ..db.database import get_async_session
from ..utils.sanitization import sanitize_title, sanitize_description


router = APIRouter(
    prefix="/tasks",
    tags=["tasks"]
)


# =========================
# GET ALL TASKS
# =========================
@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Task).where(Task.user_id == current_user.id)
    )
    return result.scalars().all()


# =========================
# CREATE TASK
# =========================
@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    title = sanitize_title(task_create.title)
    description = (
        sanitize_description(task_create.description)
        if task_create.description
        else None
    )

    if not title or not title.strip():
        raise HTTPException(status_code=400, detail="Title is required")

    if len(title) > 200:
        raise HTTPException(status_code=400, detail="Title max 200 characters")

    if description and len(description) > 2000:
        raise HTTPException(status_code=400, detail="Description max 2000 characters")

    task = Task(
        title=title,
        description=description,
        completed=False,
        user_id=current_user.id
    )

    session.add(task)
    await session.commit()
    await session.refresh(task)

    return task


# =========================
# UPDATE TASK
# =========================
@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    update_data = task_update.model_dump(exclude_unset=True)

    if "title" in update_data:
        title = sanitize_title(update_data["title"])
        if not title.strip():
            raise HTTPException(status_code=400, detail="Title cannot be empty")
        if len(title) > 200:
            raise HTTPException(status_code=400, detail="Title max 200 characters")
        task.title = title

    if "description" in update_data:
        description = sanitize_description(update_data["description"])
        if description and len(description) > 2000:
            raise HTTPException(status_code=400, detail="Description max 2000 characters")
        task.description = description

    if "completed" in update_data:
        task.completed = update_data["completed"]

    task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(task)

    return task


# =========================
# DELETE TASK
# =========================
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    result = await session.execute(
        select(Task)
        .where(Task.id == task_id)
        .where(Task.user_id == current_user.id)
    )
    task = result.scalar_one_or_none()

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    await session.delete(task)
    await session.commit()
