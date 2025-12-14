# Mobile BFF (Backend for Frontend)

Kotlin service for mobile clients.

## Technology Stack

- Kotlin 1.6
- Ktor
- Exposed (SQL)
- Kotlinx Serialization

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | db/UserQueries.kt:45 | Critical |
| Insecure Deserialization | utils/Serializer.kt:23 | High |
| Path Traversal | handlers/Files.kt:67 | High |
| SSRF | clients/External.kt:34 | High |
| Weak Crypto | crypto/Hasher.kt:12 | Medium |
| Hardcoded Secrets | config/ApiKeys.kt:56 | Critical |
| XXE | parsers/Xml.kt:78 | High |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| ktor-server | 1.6.0 | CVE-2021-XXXXX | Medium |
| kotlinx-serialization | 1.2.0 | None known | - |
| logback | 1.2.3 | CVE-2021-42550 | High |
| jackson-databind | 2.9.8 | CVE-2019-12086 | High |

## Build

```bash
cd services/mobile-bff
./gradlew build
```
