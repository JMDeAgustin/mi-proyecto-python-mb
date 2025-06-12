from typing import List

from fastapi import APIRouter, Depends, Query, HTTPException
from requests.exceptions import HTTPError

from auth.dependencies import get_current_user
from crud.product import fetch_products
from models.product import Product

router = APIRouter(prefix="/products")


@router.get("/", response_model=List[Product])
def list_products(
    current_user=Depends(get_current_user),  # protege la ruta
    skip: int = Query(0, ge=0, description="Índice inicial"),
    limit: int = Query(10, ge=1, le=100, description="Máximo de ítems"),
    search: str | None = Query(None, description="Búsqueda por texto"),
    category: str | None = Query(None, description="Filtrar por categoría"),
    sort: str | None = Query(
        None, description="Ordenar por 'price', 'rating', etc."
    ),
):
    try:
        data = fetch_products(
            skip=skip,
            limit=limit,
            search=search,
            category=category,
            sort=sort,
        )
    except HTTPError as err:
        raise HTTPException(status_code=502, detail="Error al consultar DummyJSON") from err

    return data.get("products", [])
