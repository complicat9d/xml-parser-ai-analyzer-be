import sqlalchemy as sa

from database.models import Base
from database.models.sale import Sale


class Product(Base):
    __tablename__ = "product"

    product_id = sa.Column(sa.Integer, nullable=False)
    sale_id = sa.Column(sa.ForeignKey(Sale.id, ondelete="CASCADE"), nullable=False)
    name = sa.Column(sa.String, nullable=False)
    quantity = sa.Column(sa.Integer, server_default="0")
    price = sa.Column(sa.Float, server_default="0")
    category = sa.Column(sa.String, nullable=False)

    __table_args__ = (sa.PrimaryKeyConstraint(product_id, sale_id),)
