import sqlalchemy as sa
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

import database.models as m
from database.session import async_session


async def create_sale(date: datetime) -> int:
    async with async_session() as session:
        q = sa.insert(m.Sale).values(date=date).returning(m.Sale.id)
        sale_id = (await session.execute(q)).scalar()

        return sale_id


async def add_report(sale_id: int, report: str):
    async with async_session() as session:
        q = sa.update(m.Sale).values(report=report).where(m.Sale.id == sale_id)
        await session.execute(q)
