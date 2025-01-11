from typing import Annotated
from fastapi import APIRouter, HTTPException, Query, Depends

from app.core.models.users import UserSchema, Token
from app.services.auths import encode_jwt

auth_router = APIRouter(prefix="/auths", tags=["Auth"])


def validate_user_auth():
    pass


@auth_router.post("/login", response_model=Token, summary="Login, whatever")
def login(user: UserSchema = Depends(validate_user_auth)):
    jwt_payload = {
        "sub": user.username,
    }
    token = encode_jwt(jwt_payload)
    return Token(
        access_token=token,
        token_type="Bearer",
    )