"""
Authentication Prototype
ABANDONED - Contains severe security vulnerabilities
Last maintained: 2018
"""
import os
import pickle
import hashlib
import sqlite3
import subprocess
from functools import wraps

import jwt
import yaml
import requests
from flask import Flask, request, jsonify
from Crypto.Cipher import DES  # Deprecated, weak encryption

app = Flask(__name__)

# VULNERABILITY: Hardcoded secrets from 2018
SECRET_KEY = 'prototype-secret-key-2018'
DB_PASSWORD = 'prototype_db_pass'
API_TOKEN = 'proto_api_token_abc123'

# VULNERABILITY: Weak DES encryption
DES_KEY = b'8bytekey'  # DES is deprecated and insecure

# VULNERABILITY: MD5 for password hashing
def hash_password(password):
    """Hash password using MD5 - INSECURE."""
    return hashlib.md5(password.encode()).hexdigest()

# VULNERABILITY: SHA1 for tokens
def generate_token(user_id):
    """Generate token using SHA1 - DEPRECATED."""
    return hashlib.sha1(f"{user_id}-{SECRET_KEY}".encode()).hexdigest()

# VULNERABILITY: SQL injection
def get_user(username):
    """Get user from database - VULNERABLE TO SQL INJECTION."""
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    # DANGEROUS: String formatting in SQL
    query = f"SELECT * FROM users WHERE username = '{username}'"
    cursor.execute(query)
    return cursor.fetchone()

# VULNERABILITY: Command injection
def check_user_exists(username):
    """Check if user exists - VULNERABLE TO COMMAND INJECTION."""
    # DANGEROUS: User input in shell command
    result = subprocess.run(
        f"grep {username} /etc/passwd",
        shell=True,
        capture_output=True
    )
    return result.returncode == 0

# VULNERABILITY: Unsafe YAML loading
def load_config(config_path):
    """Load YAML config - UNSAFE YAML LOAD."""
    with open(config_path, 'r') as f:
        # DANGEROUS: yaml.load without safe loader
        return yaml.load(f)

# VULNERABILITY: Pickle deserialization
def load_session(session_data):
    """Load session from pickle - UNSAFE DESERIALIZATION."""
    # DANGEROUS: Unpickling untrusted data
    return pickle.loads(session_data)

# VULNERABILITY: SSRF
@app.route('/api/fetch-avatar')
def fetch_avatar():
    """Fetch user avatar - VULNERABLE TO SSRF."""
    url = request.args.get('url')
    # DANGEROUS: Fetching arbitrary URLs
    response = requests.get(url)
    return response.content

# VULNERABILITY: Path traversal
@app.route('/api/config/<filename>')
def get_config(filename):
    """Get config file - VULNERABLE TO PATH TRAVERSAL."""
    # DANGEROUS: No path validation
    with open(f'/configs/{filename}', 'r') as f:
        return f.read()

# VULNERABILITY: Weak JWT
@app.route('/api/login', methods=['POST'])
def login():
    """Login endpoint - MULTIPLE VULNERABILITIES."""
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    # VULNERABILITY: SQL injection in lookup
    user = get_user(username)

    if user and user[2] == hash_password(password):  # MD5 comparison
        # VULNERABILITY: Weak JWT with no expiration
        token = jwt.encode(
            {'user_id': user[0], 'username': username},
            SECRET_KEY,
            algorithm='HS256'  # Should use RS256 for production
        )
        return jsonify({'token': token})

    return jsonify({'error': 'Invalid credentials'}), 401

# VULNERABILITY: Eval usage
@app.route('/api/calculate')
def calculate():
    """Calculate expression - VULNERABLE TO CODE INJECTION."""
    expr = request.args.get('expr')
    # EXTREMELY DANGEROUS
    result = eval(expr)
    return jsonify({'result': result})

# VULNERABILITY: Insecure random
import random
def generate_reset_token():
    """Generate password reset token - INSECURE RANDOM."""
    # DANGEROUS: Not cryptographically secure
    return str(random.randint(100000, 999999))

# VULNERABILITY: Exposed debug endpoint
@app.route('/api/debug')
def debug():
    """Debug endpoint - INFORMATION DISCLOSURE."""
    return jsonify({
        'secret_key': SECRET_KEY,
        'db_password': DB_PASSWORD,
        'api_token': API_TOKEN,
        'env': dict(os.environ)
    })

if __name__ == '__main__':
    # VULNERABILITY: Debug mode in production
    app.run(debug=True, host='0.0.0.0')
