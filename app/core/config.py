from pathlib import Path

from pydantic import BaseModel

BASE_DIR_PATH = Path(__file__).parent.parent.parent
DB_PATH = BASE_DIR_PATH / "data.db"


class DBSettings(BaseModel):
    url: str = f""
    echo: bool = True


class AuthJWT(BaseModel):
    private_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-private.pem"
    public_key_path: Path = BASE_DIR_PATH / "certs" / "jwt-public.pem"
    algorithm: str = "RSA256"


class Settings(BaseModel):
    db: DBSettings = DBSettings()
    auth_jwt: AuthJWT = AuthJWT()


settings = Settings()