from datetime import timedelta, datetime, UTC

import bcrypt
import jwt
# from cryptography.hazmat.primitives import serialization
from app.core.config import settings
from app.core.models.users import UserSchema

db = {}


def register(user: UserSchema):
    pass


def login(user: UserSchema):
    pass


def encode_jwt(
        payload: dict,
        key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
):
    to_encode = payload.copy()
    now = datetime.now(UTC)

    if expire_timedelta:
        expire = now + expire_timedelta
    else:
        expire = now + timedelta(minutes=expire_minutes)

    # key = serialization.load_pem_private_key(key.encode(), password=None)

    to_encode.update(
        iat=int(now.timestamp()),
        exp=int(expire.timestamp()),
    )
    print(to_encode, key, algorithm)
    encoded = jwt.encode(to_encode, key, algorithm=algorithm)
    return encoded


def decode_jwt(
        token: str | bytes,
        key: str = settings.auth_jwt.public_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm
):
    decoded = jwt.decode(token, key, algorithms=[algorithm])
    return decoded


def hash_password(password: str) -> bytes:
    salt = bcrypt.gensalt()
    password_bytes = password.encode()
    return bcrypt.hashpw(password_bytes, salt)


def validate_password(password: str, hashed_password: bytes):
    return bcrypt.checkpw(password.encode(), hashed_password)
