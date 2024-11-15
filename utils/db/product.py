import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

import database.models as m
from schemas.product import ProductSchema


async def save_products(
    products: List[ProductSchema], sale_id: int, session: AsyncSession
):
    data = [
        {
            m.Product.product_id: product.product_id,
            m.Product.sale_id: sale_id,
            m.Product.name: product.name,
            m.Product.price: product.price,
            m.Product.category: product.category,
            m.Product.quantity: product.quantity,
        }
        for product in products
    ]
    q = sa.insert(m.Product).values(data)
    await session.execute(q)
