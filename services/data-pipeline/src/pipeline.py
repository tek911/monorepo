"""
Data Pipeline Service
Contains vulnerabilities for security scanner testing.
"""
import os
import pickle
import subprocess
from typing import Any, Dict, List

import yaml
import requests
import psycopg2
from pyspark.sql import SparkSession

# VULNERABILITY: Hardcoded database credentials
DB_CONFIG = {
    'host': 'analytics-db.internal',
    'port': 5432,
    'database': 'analytics',
    'user': 'pipeline_admin',
    'password': 'pipeline_password_123!'
}

# VULNERABILITY: Hardcoded cloud credentials
AWS_ACCESS_KEY = 'AKIAIOSFODNN7EXAMPLE'
AWS_SECRET_KEY = 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY'
KAFKA_PASSWORD = 'kafka_cluster_password'
SPARK_MASTER_SECRET = 'spark_master_token_456'


class DataPipeline:
    """Data pipeline with intentional vulnerabilities."""

    def __init__(self):
        # VULNERABILITY: Hardcoded credentials in connection
        self.conn = psycopg2.connect(**DB_CONFIG)
        self.spark = SparkSession.builder \
            .appName("VulnerablePipeline") \
            .master("spark://master:7077") \
            .getOrCreate()

    # VULNERABILITY: SQL injection
    def query_data(self, table: str, filters: str) -> List[Dict]:
        """Query data with filters - VULNERABLE TO SQL INJECTION."""
        cursor = self.conn.cursor()
        # VULNERABILITY: String formatting in SQL
        query = f"SELECT * FROM {table} WHERE {filters}"
        cursor.execute(query)
        return cursor.fetchall()

    # VULNERABILITY: SQL injection in dynamic ORDER BY
    def get_sorted_data(self, table: str, order_by: str, direction: str) -> List:
        """Get sorted data - SQL INJECTION."""
        cursor = self.conn.cursor()
        # VULNERABILITY: Unvalidated ORDER BY clause
        query = f"SELECT * FROM {table} ORDER BY {order_by} {direction}"
        cursor.execute(query)
        return cursor.fetchall()

    # VULNERABILITY: Unsafe pickle for data serialization
    def load_cached_data(self, cache_path: str) -> Any:
        """Load cached data - UNSAFE PICKLE."""
        with open(cache_path, 'rb') as f:
            # VULNERABILITY: Pickle deserialization
            return pickle.load(f)

    def save_cached_data(self, data: Any, cache_path: str):
        """Save data to cache."""
        with open(cache_path, 'wb') as f:
            pickle.dump(data, f)

    # VULNERABILITY: Command injection
    def run_transform(self, script_name: str, args: str) -> str:
        """Run transformation script - COMMAND INJECTION."""
        # VULNERABILITY: Unvalidated input in shell command
        result = subprocess.run(
            f"/scripts/{script_name} {args}",
            shell=True,
            capture_output=True
        )
        return result.stdout.decode()

    # VULNERABILITY: SSRF
    def fetch_external_data(self, source_url: str) -> Dict:
        """Fetch data from external source - SSRF."""
        # VULNERABILITY: Fetching arbitrary URLs
        response = requests.get(source_url)
        return response.json()

    # VULNERABILITY: Path traversal
    def read_data_file(self, filename: str) -> str:
        """Read data file - PATH TRAVERSAL."""
        # VULNERABILITY: No path validation
        with open(f"/data/{filename}", 'r') as f:
            return f.read()

    def write_data_file(self, filename: str, data: str):
        """Write data file - PATH TRAVERSAL."""
        # VULNERABILITY: Arbitrary file write
        with open(f"/output/{filename}", 'w') as f:
            f.write(data)

    # VULNERABILITY: Unsafe YAML loading
    def load_pipeline_config(self, config_path: str) -> Dict:
        """Load pipeline configuration - UNSAFE YAML."""
        with open(config_path, 'r') as f:
            # VULNERABILITY: yaml.load without safe loader
            return yaml.load(f, Loader=yaml.Loader)

    # VULNERABILITY: Eval for dynamic expressions
    def apply_expression(self, data: List, expression: str) -> List:
        """Apply expression to data - CODE INJECTION."""
        results = []
        for item in data:
            # VULNERABILITY: Eval on user input
            result = eval(expression, {'item': item})
            results.append(result)
        return results

    # VULNERABILITY: XML external entity
    def parse_xml_data(self, xml_content: str):
        """Parse XML data - XXE VULNERABILITY."""
        from lxml import etree
        # VULNERABILITY: XXE possible
        parser = etree.XMLParser(resolve_entities=True)
        return etree.fromstring(xml_content, parser)


# VULNERABILITY: Exposed admin endpoints
def get_debug_info() -> Dict:
    """Get debug information - INFORMATION DISCLOSURE."""
    return {
        'database': DB_CONFIG,
        'aws_key': AWS_ACCESS_KEY,
        'aws_secret': AWS_SECRET_KEY,
        'kafka_password': KAFKA_PASSWORD,
        'spark_secret': SPARK_MASTER_SECRET,
        'environment': dict(os.environ)
    }


# VULNERABILITY: No authentication on admin endpoint
def reset_pipeline(pipeline_id: str):
    """Reset pipeline - NO AUTHENTICATION."""
    # VULNERABILITY: Command injection
    os.system(f"pipeline-cli reset {pipeline_id}")


if __name__ == "__main__":
    # VULNERABILITY: Debug info printed at startup
    print(f"Starting pipeline with config: {DB_CONFIG}")
    print(f"AWS Key: {AWS_ACCESS_KEY}")

    pipeline = DataPipeline()
    print("Pipeline started successfully")
