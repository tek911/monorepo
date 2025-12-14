# Data Pipeline

Scala Spark data processing with vulnerabilities.

## Technology Stack

- Scala 2.12
- Apache Spark 3.0
- Hadoop
- Kafka

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | jobs/Query.scala:45 | Critical |
| Insecure Deserialization | utils/Serializer.scala:23 | Critical |
| Command Injection | jobs/Export.scala:67 | High |
| Path Traversal | io/FileLoader.scala:34 | High |
| XXE | parsers/XmlParser.scala:56 | High |
| Hardcoded Credentials | config/Hadoop.scala:12 | Critical |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| jackson-databind | 2.9.8 | CVE-2019-12086 | High |
| log4j-core | 2.14.1 | CVE-2021-44228 | Critical |
| hadoop-common | 2.7.0 | Multiple | High |
| spark-core | 3.0.0 | CVE-2021-XXXXX | Medium |

## Build

```bash
cd services/data-pipeline
sbt compile
```
