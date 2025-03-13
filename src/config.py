from pathlib import Path

from dotenv import load_dotenv
from pydantic import Field, PostgresDsn
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv(override=True)


class Settings(BaseSettings):
    # Base directory
    BASE_DIR: Path = Field(
        default_factory=lambda: Path(__file__).resolve().parent.parent
    )
    SECRET_KEY: str

    # Database configurations
    POSTGRES_HOST: str
    POSTGRES_PORT: int
    POSTGRES_DATABASE: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str

    # test sqlite3 database
    DATABASE_URL_TEST: str

    @property
    def DATABASE_URL(self) -> PostgresDsn:
        return PostgresDsn.build(
            scheme="postgresql+asyncpg",
            username=self.POSTGRES_USER,
            password=self.POSTGRES_PASSWORD,
            host=self.POSTGRES_HOST,
            port=self.POSTGRES_PORT,
            path=self.POSTGRES_DATABASE,
        )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,  # This helps with variable name matching
        extra="ignore",
    )


settings = Settings()
