from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import select
from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..middleware.jwt_auth import verify_token
from ..db.database import get_async_session
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from ..utils.sanitization import sanitize_title, sanitize_description


router = APIRouter()


@router.get("/", response_model=list[TaskRead])
async def get_tasks(
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    """Get all tasks for the authenticated user."""
    result = await session.execute(
        select(Task).where(Task.user_id == current_user.id)
    )
    tasks = result.scalars().all()
    return tasks


@router.post("/", response_model=TaskRead, status_code=status.HTTP_201_CREATED)
async def create_task(
    task_create: TaskCreate,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    """Create a new task for the authenticated user."""
    # Sanitize inputs
    sanitized_title = sanitize_title(task_create.title)
    sanitized_description = sanitize_description(task_create.description) if task_create.description else None

    # Validate input
    if not sanitized_title or len(sanitized_title.strip()) == 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title is required"
        )

    if len(sanitized_title) > 200:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Title must be at most 200 characters"
        )

    if sanitized_description and len(sanitized_description) > 2000:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Description must be at most 2000 characters"
        )

    # Create task
    db_task = Task(
        title=sanitized_title,
        description=sanitized_description,
        completed=False,
        user_id=current_user.id
    )
    session.add(db_task)
    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: UUID,
    task_update: TaskUpdate,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    """Update a task for the authenticated user."""
    # Get the task
    result = await session.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    )
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Update task fields if provided
    update_data = task_update.dict(exclude_unset=True)
    if not update_data:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="At least one field must be provided for update"
        )

    # Sanitize inputs before updating
    for field, value in update_data.items():
        if field == "title" and value is not None:
            update_data[field] = sanitize_title(value)
        elif field == "description" and value is not None:
            update_data[field] = sanitize_description(value)

    for field, value in update_data.items():
        setattr(db_task, field, value)

    # Update timestamp
    from datetime import datetime
    db_task.updated_at = datetime.utcnow()

    await session.commit()
    await session.refresh(db_task)

    return db_task


@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: UUID,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    """Delete a task for the authenticated user."""
    # Get the task
    result = await session.execute(
        select(Task).where(Task.id == task_id).where(Task.user_id == current_user.id)
    )
    db_task = result.scalar_one_or_none()

    if not db_task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    # Delete the task
    await session.delete(db_task)
    await session.commit()

    return