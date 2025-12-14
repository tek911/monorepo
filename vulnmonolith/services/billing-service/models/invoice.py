"""
Invoice Model
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class InvoiceBase(BaseModel):
    customer_id: str
    amount: float
    description: str
    due_date: Optional[datetime] = None


class InvoiceCreate(InvoiceBase):
    pass


class Invoice(InvoiceBase):
    id: int
    status: str
    created_at: datetime
    updated_at: Optional[datetime] = None

    class Config:
        orm_mode = True
