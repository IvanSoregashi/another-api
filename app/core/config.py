from pathlib import Path
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR_PATH = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR_PATH / "data.db"


class SQLiteSettings(BaseSettings):
    path: str | Path = DB_PATH
    url: str = "sqlite+aiosqlite:///data.db"
    echo: bool = True

    def __post_init__(self):
        self.url += self.path


class AWSConfig(BaseSettings):
    aws_access_key_id: str
    aws_secret_access_key: str
    region_name: str


class AuthJWT(BaseSettings):
    private_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-public.pem"
    algorithm: str = "RS256"
    access_token_expire_minutes: int = 3


class Settings(BaseSettings):
    model_config = SettingsConfigDict(extra="ignore", env_nested_delimiter="__")  # extra = forbid, allow
    aws: AWSConfig
    db: SQLiteSettings = SQLiteSettings()
    auth_jwt: AuthJWT = AuthJWT()
    mode: Literal["sql-orm", "sql-core", "dynamodb", "test", "test_dynamodb"]


settings = Settings(_env_file=BASE_DIR_PATH / ".env.test", mode="test_dynamodb")
print(settings.model_dump())
