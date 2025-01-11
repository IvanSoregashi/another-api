from pydantic import BaseModel


class UserSchema(BaseModel):
    username: str
    password: bytes


class Token(BaseModel):
    access_token: str
    token_type: str
