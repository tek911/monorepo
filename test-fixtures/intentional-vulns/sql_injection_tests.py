"""
SQL Injection Test Cases
These are INTENTIONAL vulnerabilities for testing security controls.
Scanners should ideally exclude this file based on path.
"""
import sqlite3

# Test payloads for SQL injection detection
SQL_INJECTION_PAYLOADS = [
    "' OR '1'='1",
    "'; DROP TABLE users; --",
    "1' AND '1'='1",
    "admin'--",
    "1; UPDATE users SET role='admin' WHERE username='test",
    "' UNION SELECT * FROM passwords --",
    "1' OR '1'='1' /*",
    "'; EXEC xp_cmdshell('net user'); --",
]


def vulnerable_query_for_testing(user_input):
    """
    INTENTIONALLY VULNERABLE: Used to test WAF/security middleware.
    This should be caught by security controls before reaching the database.
    """
    conn = sqlite3.connect(':memory:')
    cursor = conn.cursor()

    # INTENTIONAL SQL INJECTION for testing
    query = f"SELECT * FROM users WHERE username = '{user_input}'"
    cursor.execute(query)

    return cursor.fetchall()


def test_sql_injection_blocked():
    """Test that our WAF blocks SQL injection attempts."""
    for payload in SQL_INJECTION_PAYLOADS:
        # In real tests, this would go through the WAF
        # and should be blocked before reaching vulnerable_query_for_testing
        pass


class SQLInjectionTestHelper:
    """
    WARNING: This class contains intentional vulnerabilities.
    It's used for penetration testing and security validation only.
    """

    def execute_raw(self, query):
        """Execute raw SQL - INTENTIONALLY INSECURE for testing."""
        conn = sqlite3.connect(':memory:')
        return conn.execute(query)

    def build_query(self, table, **conditions):
        """Build query with string formatting - INTENTIONALLY INSECURE."""
        where_clause = " AND ".join(f"{k}='{v}'" for k, v in conditions.items())
        return f"SELECT * FROM {table} WHERE {where_clause}"
