# Circular import example - Module A
# This creates a circular dependency with module_b

from module_b import function_b

# VULNERABILITY: Hardcoded secret
API_KEY = "sk_live_circular_import_test"

def function_a():
    """Function in module A that calls function from module B"""
    # VULNERABILITY: SQL Injection
    query = f"SELECT * FROM users WHERE key = '{API_KEY}'"
    return function_b()

# Import from C which imports from A (deeper circular)
from module_c import function_c
