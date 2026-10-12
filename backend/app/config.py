import os
from typing import List
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()
backend_env = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".env"))
if os.path.exists(backend_env):
    load_dotenv(dotenv_path=backend_env, override=True)

class Settings(BaseSettings):
    APP_NAME: str = "TripWise AI"
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    _default_db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "travel_app.db"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", f"sqlite:///{_default_db_path}")
    GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    PORT: int = int(os.getenv("PORT", "8000"))
    CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000",
        "http://127.0.0.1:3000",
        "*"
    ]

    model_config = {"case_sensitive": True}

settings = Settings()
