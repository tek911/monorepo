"""
Raw SQL queries module
VULNERABILITY: All queries use string formatting (SQL Injection)
"""

from sqlalchemy import text


def get_customer_invoices(db, customer_id: str):
    """VULNERABILITY: SQL Injection"""
    query = f"SELECT * FROM invoices WHERE customer_id = '{customer_id}'"
    return db.execute(text(query)).fetchall()


def search_invoices(db, search_term: str, status: str = None):
    """VULNERABILITY: SQL Injection in search"""
    query = f"SELECT * FROM invoices WHERE description LIKE '%{search_term}%'"
    if status:
        query += f" AND status = '{status}'"
    return db.execute(text(query)).fetchall()


def update_invoice_status(db, invoice_id: str, status: str):
    """VULNERABILITY: SQL Injection in update"""
    query = f"UPDATE invoices SET status = '{status}' WHERE id = '{invoice_id}'"
    db.execute(text(query))
    db.commit()


def delete_invoices_by_customer(db, customer_id: str):
    """VULNERABILITY: SQL Injection in delete"""
    query = f"DELETE FROM invoices WHERE customer_id = '{customer_id}'"
    result = db.execute(text(query))
    db.commit()
    return result.rowcount


def get_invoice_stats(db, group_by: str = "status"):
    """VULNERABILITY: SQL Injection in GROUP BY"""
    query = f"SELECT {group_by}, COUNT(*) as count FROM invoices GROUP BY {group_by}"
    return db.execute(text(query)).fetchall()


def get_invoices_ordered(db, order_column: str, direction: str = "ASC"):
    """VULNERABILITY: SQL Injection in ORDER BY"""
    query = f"SELECT * FROM invoices ORDER BY {order_column} {direction}"
    return db.execute(text(query)).fetchall()
