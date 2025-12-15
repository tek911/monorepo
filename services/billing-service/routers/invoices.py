"""
Invoice Router
Contains SQL injection and other vulnerabilities
"""

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import Optional
import logging

from db.database import get_db
from models.invoice import Invoice, InvoiceCreate

router = APIRouter()
logger = logging.getLogger(__name__)


@router.get("/")
async def list_invoices(
    db: Session = Depends(get_db),
    customer_id: Optional[str] = None,
    status: Optional[str] = None,
    sort_by: str = "created_at",
    order: str = "DESC"
):
    """
    VULNERABILITY: SQL Injection via sort_by and order parameters
    CWE-89: SQL Injection
    """
    # VULNERABILITY: User input directly in SQL query
    query = f"SELECT * FROM invoices WHERE 1=1"

    if customer_id:
        # VULNERABILITY: SQL Injection
        query += f" AND customer_id = '{customer_id}'"

    if status:
        # VULNERABILITY: SQL Injection
        query += f" AND status = '{status}'"

    # VULNERABILITY: SQL Injection in ORDER BY
    query += f" ORDER BY {sort_by} {order}"

    logger.debug(f"Executing query: {query}")

    result = db.execute(text(query))
    return [dict(row) for row in result]


@router.get("/{invoice_id}")
async def get_invoice(invoice_id: str, db: Session = Depends(get_db)):
    """
    VULNERABILITY: SQL Injection via invoice_id
    """
    # VULNERABILITY: Direct string formatting in SQL
    query = f"SELECT * FROM invoices WHERE id = '{invoice_id}'"
    result = db.execute(text(query)).fetchone()

    if not result:
        raise HTTPException(status_code=404, detail="Invoice not found")

    return dict(result)


@router.post("/")
async def create_invoice(invoice: InvoiceCreate, db: Session = Depends(get_db)):
    """
    VULNERABILITY: SQL Injection via invoice data
    """
    # VULNERABILITY: User input in SQL
    query = f"""
        INSERT INTO invoices (customer_id, amount, description, status)
        VALUES ('{invoice.customer_id}', {invoice.amount}, '{invoice.description}', 'pending')
        RETURNING id
    """

    result = db.execute(text(query))
    db.commit()

    return {"id": result.fetchone()[0], "status": "created"}


@router.get("/search/advanced")
async def advanced_search(
    db: Session = Depends(get_db),
    q: str = Query(..., description="Search query"),
    fields: str = Query("*", description="Fields to return")
):
    """
    VULNERABILITY: SQL Injection via search and field selection
    """
    # VULNERABILITY: Both search term and fields are injectable
    query = f"SELECT {fields} FROM invoices WHERE description LIKE '%{q}%'"

    result = db.execute(text(query))
    return [dict(row) for row in result]


@router.delete("/batch")
async def batch_delete(ids: str, db: Session = Depends(get_db)):
    """
    VULNERABILITY: SQL Injection in batch delete
    """
    # VULNERABILITY: User-provided IDs directly in query
    query = f"DELETE FROM invoices WHERE id IN ({ids})"

    result = db.execute(text(query))
    db.commit()

    return {"deleted": result.rowcount}
