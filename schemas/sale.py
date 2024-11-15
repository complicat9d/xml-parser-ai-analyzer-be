from pydantic import BaseModel
from datetime import date
from typing import Optional


class SaleSchema(BaseModel):
    id: int
    timestamp: date
    report: Optional[str] = None
