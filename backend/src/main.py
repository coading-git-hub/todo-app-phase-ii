from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .config import settings
from .api.chat import router as chat_router
from .api.auth import router as auth_router
from .api.tasks import router as tasks_router
from .db.database_async import async_engine
# Import models to ensure they are registered with SQLModel
from .models.user import User
from .models.task import Task
from .models.conversation import Conversation
from .models.message import Message
from sqlmodel import SQLModel
import logging

logger = logging.getLogger(__name__)

# Add lifespan support for future compatibility
from contextlib import asynccontextmanager

async def create_db_and_tables():
    """Create database tables based on SQLModel models asynchronously."""
    try:
        async with async_engine.begin() as conn:
            await conn.run_sync(SQLModel.metadata.create_all)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Failed to create database tables: {e}")
        raise

@asynccontextmanager
async def lifespan(app):
    # Startup
    await create_db_and_tables()
    yield
    # Shutdown (if needed)

# Create FastAPI app instance with lifespan
app = FastAPI(
    title=settings.APP_NAME,
    debug=settings.debug,
    lifespan=lifespan
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:3001",
        # "https://todo-app-phase-ii-jt2k.vercel.app",
        "https://kiran-ahmed-todo-phase-3.hf.space",  # Allow requests from frontend
        "https://kiran-ahmed-todo-phase-ii.hf.space",  # Allow Hugging Face Space
        "*"  # Allow all origins during development (consider restricting in production)
    ],  # Frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    # Expose headers that the frontend might need to access
    expose_headers=["Authorization", "Content-Type", "Set-Cookie"],
)

# Include API routers
app.include_router(chat_router, prefix="/api")
app.include_router(auth_router, prefix="/api/auth")
app.include_router(tasks_router, prefix="/api/tasks")
app.include_router(tasks_router, prefix="/api/v1/tasks")  # Versioned API

@app.get("/")
def root():
        return {
            "message": "Welcome to Todo API",
            "version": "1.0.0",
            "endpoints": {
                "health": "/health",
                "docs": "/docs",
                "redoc": "/redoc",
                "auth": {
                    "signup": "/api/auth/signup",
                    "signin": "/api/auth/signin"
                },
                "tasks": {
                    "list": "GET /api/tasks",
                    "create": "POST /api/tasks",
                    "update": "PUT /api/tasks/{task_id}",
                    "delete": "DELETE /api/tasks/{task_id}"
                },
                "chat": {
                    "ai_agent": "POST /api/v1/chat"
                }
            }
        }



# The lifespan context manager is already defined earlier
# Database initialization happens in the lifespan context

@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "app": settings.APP_NAME}