from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from datetime import datetime

from ..models.task import Task, TaskCreate, TaskUpdate, TaskRead
from ..models.user import User
from ..middleware.jwt_auth import verify_token
from ..db.database_async import get_async_session
from ..utils.sanitization import sanitize_title, sanitize_description
from ..services.task_service import TaskService


router = APIRouter(

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
    task_service = TaskService(session)
    tasks = await task_service.get_user_tasks(current_user.id)
    return tasks


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

    # Create a new TaskCreate with sanitized data
    sanitized_task_create = TaskCreate(
        title=title,
        description=description,
        completed=task_create.completed
    )

    task_service = TaskService(session)
    task = await task_service.create_task(
        sanitized_task_create,
        current_user.id
    )

    return task


# =========================
# UPDATE TASK
# =========================
@router.put("/{task_id}", response_model=TaskRead)
async def update_task(
    task_id: int,
    task_update: TaskUpdate,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    task = await task_service.update_task(task_id, task_update, current_user.id)

    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    return task


# =========================
# DELETE TASK
# =========================
@router.delete("/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_task(
    task_id: int,
    current_user: User = Depends(verify_token),
    session: AsyncSession = Depends(get_async_session)
):
    task_service = TaskService(session)
    success = await task_service.delete_task(task_id, current_user.id)

    if not success:
        raise HTTPException(status_code=404, detail="Task not found")

    # Response is handled by status code for 204