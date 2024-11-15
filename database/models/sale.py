import sqlalchemy as sa

from database.models import Base


class Sale(Base):
    __tablename__ = "sale"

    id = sa.Column(sa.Integer, primary_key=True)
    timestamp = sa.Column(sa.Date, nullable=False)
    report = sa.Column(sa.String, nullable=True)