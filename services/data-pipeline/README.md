# Data Pipeline Service

ETL and data processing pipeline for analytics.

## Stack
- Python 3.9
- Apache Spark
- Apache Kafka
- PostgreSQL

## Vulnerabilities for Testing

### Data Security
- SQL injection in dynamic queries
- Unsafe deserialization of data
- Hardcoded database credentials

### Processing Security
- Command injection in data transformations
- SSRF in data source fetching
- Path traversal in file operations

### Infrastructure
- Exposed metrics and debugging
- Missing authentication on admin endpoints
- Insecure Kafka/Spark configurations
