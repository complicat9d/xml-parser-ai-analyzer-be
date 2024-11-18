import sqlalchemy as sa
from sqlalchemy.orm import Session
from datetime import datetime

import database.models as m


def create_sale(date: datetime, session: Session) -> int:
    q = sa.insert(m.Sale).values(timestamp=date).returning(m.Sale.id)
    sale_id = (session.execute(q)).scalar()

    return sale_id


def add_report(sale_id: int, report: str, session: Session):
    q = sa.update(m.Sale).values(report=report).where(m.Sale.id == sale_id)
    session.execute(q)
