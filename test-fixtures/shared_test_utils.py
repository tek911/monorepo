"""
Shared Test Utilities
WARNING: This file contains a REAL vulnerability hidden in test code.
Scanners SHOULD detect this even though it's in a test directory.
"""
import os
import subprocess
import pickle
import yaml


class TestConfig:
    """Configuration for test environment."""

    # REAL VULNERABILITY: Hardcoded production credentials
    # This should be detected because it's in a shared utility
    PROD_DB_HOST = "prod-db.internal.company.com"
    PROD_DB_USER = "prod_admin"
    PROD_DB_PASS = "Pr0d_Passw0rd_2024!"

    # REAL VULNERABILITY: API key used in production
    PROD_API_KEY = "sk_live_real_production_key_12345"


def load_test_config(config_path):
    """
    Load test configuration from YAML.
    REAL VULNERABILITY: Uses unsafe yaml.load()
    This is a shared utility that may be imported by production code.
    """
    with open(config_path, 'r') as f:
        # REAL VULNERABILITY - unsafe YAML load
        return yaml.load(f, Loader=yaml.Loader)


def deserialize_test_data(data_path):
    """
    Deserialize test data from pickle file.
    REAL VULNERABILITY: Uses unsafe pickle.load()
    """
    with open(data_path, 'rb') as f:
        # REAL VULNERABILITY - unsafe pickle deserialization
        return pickle.load(f)


def run_test_command(command):
    """
    Run a test command.
    REAL VULNERABILITY: Shell injection possible if used with user input.
    This utility might be called from non-test code.
    """
    # REAL VULNERABILITY - shell=True with string command
    return subprocess.run(command, shell=True, capture_output=True)


def get_test_env_var(var_name):
    """
    Get environment variable for tests.
    REAL VULNERABILITY: Falls back to hardcoded secrets.
    """
    value = os.environ.get(var_name)
    if not value:
        # REAL VULNERABILITY - hardcoded fallback secrets
        fallbacks = {
            "DATABASE_URL": "postgres://admin:admin123@localhost/test",
            "SECRET_KEY": "development_secret_key_12345",
            "AWS_ACCESS_KEY_ID": "AKIAIOSFODNN7EXAMPLE",
            "AWS_SECRET_ACCESS_KEY": "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",
        }
        value = fallbacks.get(var_name)
    return value


# REAL VULNERABILITY: Exposed credentials at module level
DEFAULT_ADMIN_PASSWORD = "admin123"
JWT_SECRET = "super_secret_jwt_token_for_testing_and_production"
