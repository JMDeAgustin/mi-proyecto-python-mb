import os
from dotenv import load_dotenv
from sqlmodel import create_engine, Session

load_dotenv()

DATABASE_URL = os.getenv(
    "DATABASE_URL",
    "postgresql+psycopg2://miusuario:supersecret@db:5432/mi_proyecto",
)

# Engine PostgreSQL
engine = create_engine(DATABASE_URL, echo=False, pool_pre_ping=True)

def get_session():
    with Session(engine) as session:
        yield session
