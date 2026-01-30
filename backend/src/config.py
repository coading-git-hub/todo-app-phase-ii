from pydantic_settings import BaseSettings
from pydantic import ConfigDict
from typing import Optional
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Settings(BaseSettings):
    model_config = ConfigDict(extra='ignore', env_file=".env")

    # Database settings
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./todo_app.db")
    NEON_API_URL: Optional[str] = os.getenv("NEON_API_URL")

    # JWT settings
    JWT_SECRET: str = os.getenv("JWT_SECRET", "your-super-secret-jwt-key-here-make-it-long-and-random")
    JWT_EXPIRE_DAYS: int = int(os.getenv("JWT_EXPIRE_DAYS", "7"))

    # Google Gemini settings
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

    # OpenAI settings
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")

    # Application settings
    APP_NAME: str = "AI Todo Chatbot Backend"
    API_V1_STR: str = "/api/v1"

    # Alias the fields for backward compatibility
    @property
    def database_url(self):
        return self.DATABASE_URL

    @property
    def jwt_secret(self):
        return self.JWT_SECRET

    @property
    def jwt_expiry_days(self):
        return self.JWT_EXPIRE_DAYS

    @property
    def debug(self):
        return os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()