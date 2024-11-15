from pydantic import BaseModel


class ProductSchema(BaseModel):
    product_id: int
    name: str
    quantity: int
    price: int
    category: str
