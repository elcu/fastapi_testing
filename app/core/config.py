import tomllib
from pathlib import Path

from pydantic import computed_field
from pydantic_settings import BaseSettings, SettingsConfigDict
from yarl import URL

PROJECT_DIR = Path(__file__).parent.parent.parent
PROJECT_TOML_PATH = PROJECT_DIR / "pyproject.toml"

with open(PROJECT_TOML_PATH, "rb") as f:
    PYPROJECT_CONTENT = tomllib.load(f)["project"]


class Settings(BaseSettings):
    """
    Application settings.
    By inheriting from BaseSettings, class automatically tries to populate every field in the class (postgres_host etc.) from env vars, then from .env file.
    Env file can be dropped once the vars get loaded to env vars.
    """

    # Config path to .env file
    model_config = SettingsConfigDict(
        env_file="app/core/.env",  # Looks for env file in CWD
        env_ignore_empty=False,
        extra="ignore",
    )

    app_name: str = PYPROJECT_CONTENT["name"]
    app_version: str = PYPROJECT_CONTENT["version"]
    app_description: str = PYPROJECT_CONTENT["description"]

    # Variables for the database
    postgres_host: str
    postgres_port: int
    postgres_user: str
    postgres_password: str
    postgres_db: str
    postgres_db_schema: str

    @computed_field
    @property
    def db_url(self) -> str:
        """
        Assemble database URL from settings.
        """
        url = URL.build(
            scheme="postgresql+asyncpg",
            host=self.postgres_host,
            port=self.postgres_port,
            user=self.postgres_user,
            password=self.postgres_password,
            path=f"/{self.postgres_db}",
        )

        return URL.human_repr(url)


settings = Settings()
