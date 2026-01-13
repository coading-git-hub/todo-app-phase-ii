import logging
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware import Middleware
from sqlmodel import SQLModel
from .api import auth, tasks
from .config import settings
from .middleware.logging import LoggingMiddleware
from .db.database import async_engine
# Import models to register them with SQLModel
# Import from __init__.py to ensure proper relationship resolution
from .models import Task, User


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_app() -> FastAPI:
    app = FastAPI(title="Todo API", version="1.0.0")

    @app.on_event("startup")
    async def on_startup():
        """Initialize database tables on startup."""
        try:
            async with async_engine.begin() as conn:
                await conn.run_sync(SQLModel.metadata.create_all)
            logger.info("Database tables initialized successfully")
        except Exception as e:
            logger.error(f"Failed to initialize database tables: {e}")
            logger.warning("Make sure your database is running and migrations are applied")

    # Add logging middleware first
    app.add_middleware(LoggingMiddleware)

    # CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.cors_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Include routers
    app.include_router(auth.router, prefix="/api/auth", tags=["auth"])
    app.include_router(tasks.router, prefix="/api/tasks", tags=["tasks"])

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
                }
            }
        }

    @app.get("/health")
    def health_check():
        return {"status": "healthy"}

    @app.middleware("http")
    async def log_requests(request, call_next):
        logger.info(f"Request: {request.method} {request.url}")
        response = await call_next(request)
        logger.info(f"Response: {response.status_code}")
        return response

    return app


app = create_app()