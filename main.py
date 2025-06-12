import os
from dotenv import load_dotenv

from fastapi import FastAPI, Request
from sqlmodel import SQLModel, Session

from db.database import engine
from crud.user import get_user_by_email, create_user
from models.user import UserCreate
from routes import auth as auth_routes
from routes import admin as admin_routes
from routes import product as product_routes
from routes import order as order_routes
from routes import export as export_routes

from log_config import logger          
from middleware.logging import AccessLogMiddleware
import exceptions

load_dotenv()

app = FastAPI(title="Tienda Online API")

app.add_middleware(AccessLogMiddleware)

app.add_exception_handler(
    exceptions.HTTPException, exceptions.http_exception_handler
)
app.add_exception_handler(
    Exception, exceptions.unhandled_exception_handler
)

@app.on_event("startup")
def on_startup() -> None:
    SQLModel.metadata.create_all(engine)

    admin_email = os.getenv("ADMIN_EMAIL")
    admin_password = os.getenv("ADMIN_PASSWORD")
    if admin_email and admin_password:
        with Session(engine) as session:
            if not get_user_by_email(admin_email, session):
                create_user(
                    UserCreate(email=admin_email, password=admin_password),
                    session,
                    role="admin",
                )
                logger.info(f"Usuario admin creado: {admin_email}")


@app.get("/health", tags=["diagnóstico"])
def health_check():
    return {"status": "ok"}


app.include_router(auth_routes.router, tags=["auth"])
app.include_router(admin_routes.router, tags=["admin"])
app.include_router(product_routes.router, tags=["productos"])
app.include_router(order_routes.router, tags=["pedidos"])
app.include_router(export_routes.router)

