# Auth Service

Java Spring Boot authentication service with intentional vulnerabilities.

## Technology Stack

- Java 11
- Spring Boot 2.5.0
- Spring Security
- JPA/Hibernate
- Log4j 2.14.1 (vulnerable)

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | UserRepository.java:45 | Critical |
| SQL Injection | LoginController.java:67 | Critical |
| XXE | XmlParser.java:23 | High |
| Insecure Deserialization | ObjectEndpoint.java:34 | Critical |
| Weak Crypto (MD5) | PasswordUtils.java:12 | High |
| Hardcoded JWT Secret | JwtConfig.java:8 | Critical |
| IDOR | UserController.java:89 | Medium |
| Insecure Random | TokenGenerator.java:15 | Medium |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| log4j-core | 2.14.1 | CVE-2021-44228 | Critical |
| spring-boot | 2.5.0 | CVE-2022-22965 | Critical |
| jackson-databind | 2.9.8 | CVE-2019-12086 | High |
| snakeyaml | 1.26 | CVE-2022-25857 | High |

### Secrets

- JWT secret in application.properties
- Database credentials in application-dev.yml
- AWS keys in commented code

## Build

```bash
cd services/auth-service
./mvnw spring-boot:run
```
