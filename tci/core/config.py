from pathlib import Path
from typing import Optional
from urllib.parse import quote_plus

from dotenv import load_dotenv
from pydantic.v1 import BaseSettings

# Load .env file
load_dotenv()


class Settings(BaseSettings):
    """Application settings"""

    # Environment
    ENV: str = "development"

    # Project paths
    PROJECT_ROOT: Path = Path(__file__).parent.parent.parent.parent

    # Database settings
    POSTGRES_USER: str = "postgres"
    POSTGRES_PASSWORD: str = "postgres"
    POSTGRES_HOST: str = "localhost"
    POSTGRES_PORT: str = "5432"
    POSTGRES_DB: str = "tci"
    POSTGRES_URL: str = None  # Will be constructed

    MONGODB_URL: str = "mongodb://localhost:27017"
    QDRANT_URL: str = "http://localhost:6333"

    # ML settings
    MODEL_PATH: Path = PROJECT_ROOT / "models"
    EMBEDDING_MODEL: str = "all-MiniLM-L6-v2"

    # Scraping settings
    SCRAPE_DELAY: int = 2
    USER_AGENT: str = "TCI Bot/1.0"

    # Auth settings
    SECRET_KEY: str = "change-me-in-production"
    TOKEN_EXPIRE_MINUTES: int = 1440

    # Security settings
    PASSWORD_MIN_LENGTH: int = 8
    BCRYPT_LOG_ROUNDS: int = 12

    class Config:
        env_prefix = "TCI_"
        env_file = ".env"
        env_file_encoding = "utf-8"

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.POSTGRES_URL = "postgresql://{}:{}@{}:{}/{}".format(
            self.POSTGRES_USER,
            quote_plus(self.POSTGRES_PASSWORD),
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )


settings = Settings()
