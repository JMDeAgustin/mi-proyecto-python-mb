import os
from datetime import datetime, timedelta
from typing import Any

from jose import JWTError, jwt
from dotenv import load_dotenv

load_dotenv()

SECRET_KEY = os.getenv("SECRET_KEY", "changeme_supersecret_key")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
REFRESH_TOKEN_EXPIRE_MINUTES = int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES", "10080"))
RESET_TOKEN_EXPIRE_MINUTES = int(os.getenv("RESET_TOKEN_EXPIRE_MINUTES", "30"))


def _create_token(data: dict[str, Any], minutes: int) -> str:
    to_encode = data.copy()
    to_encode["exp"] = datetime.utcnow() + timedelta(minutes=minutes)
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)


def decode_token(token: str) -> dict[str, Any]:
    try:
        return jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
    except JWTError as err:
        raise ValueError("Token inválido o caducado") from err

def create_access_token(sub: str, role: str) -> str:
    return _create_token({"sub": sub, "role": role, "type": "access"},
                         ACCESS_TOKEN_EXPIRE_MINUTES)


def create_refresh_token(sub: str) -> str:
    return _create_token({"sub": sub, "type": "refresh"},
                         REFRESH_TOKEN_EXPIRE_MINUTES)


def create_reset_token(sub: str) -> str:
    return _create_token({"sub": sub, "type": "reset"},
                         RESET_TOKEN_EXPIRE_MINUTES)


def decode_access_token(token: str) -> dict[str, Any]:
    payload = decode_token(token)
    if payload.get("type") != "access":
        raise ValueError("Token no es de acceso")
    return payload
