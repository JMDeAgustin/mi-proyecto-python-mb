from fastapi import APIRouter, Depends
from sqlmodel import Session

from auth.dependencies import require_role
from crud.user import get_all_users
from db.database import get_session
from models.user import UserRead

router = APIRouter(prefix="/admin")


@router.get("/users", response_model=list[UserRead])
def list_users(session: Session = Depends(get_session),
               current_admin=Depends(require_role("admin"))):
    return get_all_users(session)
