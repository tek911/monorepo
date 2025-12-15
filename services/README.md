# Services

This directory contains microservices in various languages, each with intentionally seeded vulnerabilities.

## Service Overview

| Service | Language/Framework | Port | Description |
|---------|-------------------|------|-------------|
| api-gateway | Node.js/TypeScript/Express | 3000 | API gateway with routing and auth |
| auth-service | Java/Spring Boot | 8080 | Authentication and authorization |
| billing-service | Python/FastAPI | 8000 | Payment processing |
| data-pipeline | Scala/Spark | - | Data processing jobs |
| legacy-monolith | PHP | 80 | Legacy application |
| ml-inference | Python + C++ | 5000 | ML model serving |
| mobile-bff | Kotlin/Ktor | 8081 | Mobile backend-for-frontend |
| realtime-service | Go + Rust FFI | 8082 | WebSocket/real-time features |

## Vulnerability Categories by Service

### api-gateway (Node.js)
- Prototype pollution
- Command injection
- SSRF
- Path traversal
- ReDoS

### auth-service (Java)
- SQL injection
- XXE
- Insecure deserialization
- Weak cryptography
- Log4Shell (CVE-2021-44228)

### billing-service (Python)
- SQL injection
- Pickle deserialization RCE
- SSTI
- Hardcoded API keys

### legacy-monolith (PHP)
- SQL injection (raw queries)
- Remote code execution (eval)
- Local file inclusion
- Unrestricted file upload

### realtime-service (Go + Rust)
- SQL injection
- Command injection
- Race conditions
- Memory safety issues

## Scanner Challenges

- Multi-language scanning in single repository
- Service-to-service dependency tracking
- Container image vulnerability correlation
- API security (OpenAPI spec analysis)
- Cross-service data flow analysis
