# Circular import example - Module C
# Creates circular dependency chain: A -> B -> C -> A

from module_a import API_KEY
from module_b import DB_PASSWORD

# VULNERABILITY: JWT Secret
JWT_SECRET = "jwt_circular_secret"

def function_c():
    """Function in module C"""
    # Uses imports from both A and B
    return f"API: {API_KEY}, DB: {DB_PASSWORD}, JWT: {JWT_SECRET}"
