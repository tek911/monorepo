# Circular import example - Module B
# This creates a circular dependency with module_a

from module_a import function_a

# VULNERABILITY: Hardcoded password
DB_PASSWORD = "circular_password_123"

def function_b():
    """Function in module B that calls function from module A"""
    return function_a()

# Also import from C
from module_c import function_c
