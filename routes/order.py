from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session

from auth.dependencies import get_current_user
from crud.order import create_order, list_orders_by_user
from crud.product import fetch_products
from db.database import get_session
from models.order import Order

router = APIRouter(prefix="/orders")


@router.post("/", response_model=Order, status_code=status.HTTP_201_CREATED)
def place_order(
    product_id: int,
    quantity: int,
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    try:
        product_data = fetch_products(skip=0, limit=1, search=None, category=None, sort=None)
        exists = any(p["id"] == product_id for p in product_data["products"])
    except Exception:
        exists = False

    if not exists:
        raise HTTPException(status_code=404, detail="Producto no encontrado")

    return create_order(
        user_id=current_user.id,
        product_id=product_id,
        quantity=quantity,
        session=session,
    )


@router.get("/", response_model=list[Order])
def my_orders(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
):
    return list_orders_by_user(current_user.id, session)
