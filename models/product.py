from typing import List, Optional

from sqlmodel import SQLModel, Field


class Product(SQLModel):
    id: int
    title: str
    description: str
    price: float
    discountPercentage: float
    rating: float
    stock: int
    brand: Optional[str] = None   
    category: str
    thumbnail: str
    images: List[str] = Field(default_factory=list)

    model_config = {"extra": "ignore"}
