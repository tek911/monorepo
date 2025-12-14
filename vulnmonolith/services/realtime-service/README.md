# Realtime Service

Go service with Rust FFI for real-time features.

## Technology Stack

- Go 1.18
- Rust 1.60 (via cgo)
- WebSocket
- gRPC

## Vulnerabilities

### Go SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | db/queries.go:45 | Critical |
| Command Injection | handlers/exec.go:23 | Critical |
| Path Traversal | handlers/files.go:56 | High |
| SSRF | clients/http.go:34 | High |
| Insecure TLS | config/tls.go:12 | High |
| Race Condition | cache/memory.go:78 | Medium |
| Weak Crypto | crypto/hash.go:23 | Medium |

### Rust SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| Unsafe Block | src/ffi.rs:34 | High |
| Buffer Overflow | src/parser.rs:56 | Critical |
| Use After Free | src/cache.rs:78 | Critical |
| Memory Leak | src/connection.rs:90 | Medium |

### SCA Findings (Go)

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| golang.org/x/crypto | 0.0.0-2021... | Multiple | High |
| github.com/dgrijalva/jwt-go | 3.2.0 | CVE-2020-26160 | High |

### SCA Findings (Rust)

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| smallvec | 0.6.0 | CVE-2019-15551 | Critical |
| crossbeam | 0.7.0 | CVE-2020-35863 | High |

## Build

```bash
cd services/realtime-service
go build ./...
```
