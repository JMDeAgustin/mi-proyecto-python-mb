from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from fastapi.responses import StreamingResponse
from sqlmodel import Session

from auth.dependencies import get_current_user, require_role
from crud.order import list_orders_by_user, list_all_orders
from db.database import get_session
from models.order import Order
from utils import export as exp

router = APIRouter(prefix="/orders/export", tags=["exportaciones"])


def _select_orders(user_is_admin: bool, user_id: int, session: Session,
                   target_user: int | None) -> List[Order]:
    if user_is_admin:
        if target_user is not None:
            return list_orders_by_user(target_user, session)
        return list_all_orders(session)
    # cliente
    return list_orders_by_user(user_id, session)


@router.get("/csv")
def export_csv(
    session: Session = Depends(get_session),
    current_user=Depends(get_current_user),
    user_id: int | None = Query(None, description="Solo admin: exportar usuario"),
):
    orders = _select_orders(current_user.role == "admin",
                            current_user.id, session, user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="Sin pedidos")
    data = exp.to_csv(orders)
    return StreamingResponse(
        iter([data]),
        media_type="text/csv",
        headers={"Content-Disposition": "attachment; filename=orders.csv"},
    )

@router.get("/excel")
def export_excel(session: Session = Depends(get_session),
                 current_user=Depends(get_current_user),
                 user_id: int | None = Query(None)):
    orders = _select_orders(current_user.role == "admin",
                            current_user.id, session, user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="Sin pedidos")
    data = exp.to_excel(orders)
    return StreamingResponse(
        iter([data]),
        media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        headers={"Content-Disposition": "attachment; filename=orders.xlsx"},
    )

@router.get("/pdf")
def export_pdf(session: Session = Depends(get_session),
               current_user=Depends(get_current_user),
               user_id: int | None = Query(None)):
    orders = _select_orders(current_user.role == "admin",
                            current_user.id, session, user_id)
    if not orders:
        raise HTTPException(status_code=404, detail="Sin pedidos")
    data = exp.to_pdf(orders)
    return StreamingResponse(
        iter([data]),
        media_type="application/pdf",
        headers={"Content-Disposition": "attachment; filename=orders.pdf"},
    )
