from pydantic import BaseModel, ConfigDict
from typing import Optional


class ProductSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    brandName: Optional[str] = None
    productId: str
    name: str
    qty: int
    price: int
    priceRRC: Optional[int] = None
    category: str
    details: dict
