"""
MCP (Model Context Protocol) tools for todo operations.

These tools will be used by the AI agent to perform todo operations.
Each function corresponds to an MCP tool that can be called by the AI.
"""

from typing import List, Dict, Any, Optional
from ..models.task import TaskCreate, TaskUpdate
from ..services.task_service import TaskService
from sqlalchemy.ext.asyncio import AsyncSession
import uuid


async def add_task(session: AsyncSession, user_id: str, title: str, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Add a new task for the user.

    Args:
        session: Database session
        user_id: User ID as string (will be converted to UUID)
        title: Task title
        description: Optional task description

    Returns:
        Dictionary with task information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Initialize task service
        task_service = TaskService(session)

        # Create task data
        task_create_data = TaskCreate(title=title, description=description, completed=False)

        # Create the task
        task = await task_service.create_task(task_create_data, user_uuid)

        return {
            "task_id": task.id,
            "status": "created",
            "title": task.title,
            "description": task.description,
            "completed": task.completed
        }
    except Exception as e:
        return {
            "error": f"Failed to add task: {str(e)}"
        }


async def list_tasks(session: AsyncSession, user_id: str, status: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    List tasks for the user.

    Args:
        session: Database session
        user_id: User ID as string (will be converted to UUID)
        status: Optional status filter ('completed', 'incomplete', or None for all)

    Returns:
        List of task dictionaries
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Initialize task service
        task_service = TaskService(session)

        # Determine completed filter based on status
        completed_filter = None
        if status == "completed":
            completed_filter = True
        elif status == "incomplete":
            completed_filter = False

        # Get tasks
        tasks = await task_service.get_user_tasks(user_uuid, completed_filter)

        return [
            {
                "task_id": task.id,
                "title": task.title,
                "description": task.description,
                "completed": task.completed
            }
            for task in tasks
        ]
    except Exception as e:
        return [{"error": f"Failed to list tasks: {str(e)}"}]


async def complete_task(session: AsyncSession, user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Mark a task as completed.

    Args:
        session: Database session
        user_id: User ID as string (will be converted to UUID)
        task_id: Task ID to complete

    Returns:
        Dictionary with task information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Initialize task service
        task_service = TaskService(session)

        # Complete the task
        task = await task_service.complete_task(task_id, user_uuid)

        if task:
            return {
                "task_id": task.id,
                "status": "completed",
                "title": task.title
            }
        else:
            return {
                "error": "Task not found or user not authorized"
            }
    except Exception as e:
        return {
            "error": f"Failed to complete task: {str(e)}"
        }


async def delete_task(session: AsyncSession, user_id: str, task_id: int) -> Dict[str, Any]:
    """
    Delete a task for the user.

    Args:
        session: Database session
        user_id: User ID as string (will be converted to UUID)
        task_id: Task ID to delete

    Returns:
        Dictionary with operation result
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Initialize task service
        task_service = TaskService(session)

        # Delete the task
        success = await task_service.delete_task(task_id, user_uuid)

        if success:
            return {
                "task_id": task_id,
                "status": "deleted"
            }
        else:
            return {
                "error": "Task not found or user not authorized"
            }
    except Exception as e:
        return {
            "error": f"Failed to delete task: {str(e)}"
        }


async def update_task(session: AsyncSession, user_id: str, task_id: int, title: Optional[str] = None, description: Optional[str] = None) -> Dict[str, Any]:
    """
    Update a task for the user.

    Args:
        session: Database session
        user_id: User ID as string (will be converted to UUID)
        task_id: Task ID to update
        title: New title (optional)
        description: New description (optional)

    Returns:
        Dictionary with task information
    """
    try:
        # Convert user_id to UUID
        user_uuid = uuid.UUID(user_id)

        # Initialize task service
        task_service = TaskService(session)

        # Prepare update data
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description

        task_update = TaskUpdate(**update_data)

        # Update the task
        task = await task_service.update_task(task_id, task_update, user_uuid)

        if task:
            return {
                "task_id": task.id,
                "status": "updated",
                "title": task.title,
                "description": task.description
            }
        else:
            return {
                "error": "Task not found or user not authorized"
            }
    except Exception as e:
        return {
            "error": f"Failed to update task: {str(e)}"
        }