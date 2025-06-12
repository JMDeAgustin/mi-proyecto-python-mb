from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session

from auth.hashing import verify_password, hash_password
from auth.jwt import (create_access_token, create_refresh_token, create_reset_token,
                      decode_token, REFRESH_TOKEN_EXPIRE_MINUTES)
from auth.token_store import save_refresh, delete_refresh, is_refresh_valid
from auth.dependencies import get_current_user
from crud.user import create_user, get_user_by_email
from db.database import get_session
from models.user import UserCreate, UserRead

router = APIRouter()

@router.post("/users/register", status_code=status.HTTP_201_CREATED)
def register_user(form: OAuth2PasswordRequestForm = Depends(),
                  session: Session = Depends(get_session)):
    if get_user_by_email(form.username, session):
        raise HTTPException(status_code=400, detail="El email ya existe")

    user = create_user(
        UserCreate(email=form.username, password=form.password), session
    )
    return {"id": user.id, "email": user.email}

@router.post("/login")
def login(form: OAuth2PasswordRequestForm = Depends(),
          session: Session = Depends(get_session)):
    user = get_user_by_email(form.username, session)
    if not user or not verify_password(form.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Credenciales incorrectas")

    access_token = create_access_token(str(user.id), user.role)
    refresh_token = create_refresh_token(str(user.id))
    save_refresh(refresh_token, REFRESH_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

@router.post("/refresh")
def refresh(refresh_token: str = Body(..., embed=True)):
    if not is_refresh_valid(refresh_token):
        raise HTTPException(status_code=401, detail="Refresh-token revocado o caducado")

    payload = decode_token(refresh_token)
    if payload.get("type") != "refresh":
        raise HTTPException(status_code=400, detail="Token incorrecto")

    access_token = create_access_token(payload["sub"], payload.get("role", "cliente"))
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
def logout(refresh_token: str = Body(..., embed=True)):
    delete_refresh(refresh_token)
    return {"detail": "Sesión cerrada"}

@router.get("/users/me", response_model=UserRead)
def read_me(current_user=Depends(get_current_user)):
    return current_user

@router.post("/password/forgot")
def forgot_password(email: str = Body(..., embed=True),
                    session: Session = Depends(get_session)):
    user = get_user_by_email(email, session)
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    reset_token = create_reset_token(str(user.id))
    return {"reset_token": reset_token}


@router.post("/password/reset")
def reset_password(token: str = Body(...),
                   new_password: str = Body(...),
                   session: Session = Depends(get_session)):
    payload = decode_token(token)
    if payload.get("type") != "reset":
        raise HTTPException(status_code=400, detail="Token incorrecto")

    user = session.get(UserRead.__annotations__['id'], int(payload["sub"]))
    if not user:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    user.hashed_password = hash_password(new_password)
    session.add(user)
    session.commit()
    return {"detail": "Contraseña actualizada"}
