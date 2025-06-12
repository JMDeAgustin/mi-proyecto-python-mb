from typing import Optional
from sqlmodel import Field, SQLModel
from pydantic import PositiveInt


class Order(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    product_id: int
    quantity: PositiveInt = Field(gt=0)
