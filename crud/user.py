from sqlmodel import Session, select

from models.user import User, UserCreate
from auth.hashing import hash_password

def get_user_by_email(email: str, session: Session) -> User | None:
    return session.exec(
        select(User).where(User.email == email)
    ).first()


def get_all_users(session: Session) -> list[User]:
    return session.exec(select(User)).all()


def create_user(user_in: UserCreate,
                session: Session,
                role: str = "cliente") -> User:
    user = User(
        email=user_in.email,
        hashed_password=hash_password(user_in.password),
        role=role,
        is_active=True,
    )
    session.add(user)
    session.commit()
    session.refresh(user)
    return user
