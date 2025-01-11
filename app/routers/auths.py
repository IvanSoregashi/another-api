from typing import Annotated
from fastapi import APIRouter, HTTPException, Query

auth_router = APIRouter(prefix="/auths", tags=["Auth"])


@auth_router.post("/login", summary="Login, whatever")
def login(login: str, password: str):
    return