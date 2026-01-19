from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List


class Settings(BaseSettings):
    # Neon PostgreSQL database URL
    # Get connection string from Neon Console -> Connection Details
    # Format should be: postgresql+asyncpg://username:password@host:port/database?sslmode=require
    database_url: str = "postgresql+asyncpg://username:password@localhost:5432/todo_app"
    jwt_secret: str = "your-super-secret-jwt-secret-key-change-in-production"
    jwt_expiry_days: int = 20
    cors_origins: str ="https://todo-app-phase-ii-kappa.vercel.app,https://kiran-ahmed-todo-phase-ii.hf.space,http://localhost:3000,http://localhost:3001,http://192.168.100.21:3000"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
        env_ignore_empty=True
    )

    @property
    def cors_origins_list(self) -> List[str]:
        """Convert the comma-separated cors_origins string to a list."""
        return [origin.strip() for origin in self.cors_origins.split(",")]


settings = Settings()