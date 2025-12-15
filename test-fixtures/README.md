# Test Fixtures

This directory contains test files that should typically be EXCLUDED from security scanning.

## Purpose

Test whether security scanners correctly handle test exclusion configurations.

## Structure

### intentional-vulns/
Files containing intentional vulnerabilities for:
- Unit tests verifying security controls work
- Integration tests for WAF/security middleware
- Penetration testing payloads
- Security scanner validation

These SHOULD be excluded from scan results.

### security-tests/
Security test files including:
- OWASP test vectors
- Fuzzing inputs
- Malformed data samples
- Exploit proof-of-concepts for testing detection

These SHOULD be excluded from scan results.

## Scanner Challenges

1. **Path-Based Exclusion**: Do scanners respect `test/`, `tests/`, `__tests__/` patterns?
2. **File Naming Exclusion**: Do scanners exclude `*_test.go`, `*.spec.ts`, `test_*.py`?
3. **Content-Based Detection**: Can scanners identify test code by content?
4. **False Negatives**: Excluding too much could miss real vulnerabilities in test utilities

## Configuration Testing

### Expected Exclusions
```
# Patterns that SHOULD exclude this directory
**/test-fixtures/**
**/intentional-vulns/**
**/security-tests/**
```

### Common Failures
- Scanners that don't support recursive glob patterns
- Scanners that only exclude by filename, not path
- Scanners that don't read custom configuration files
- Default configurations that include test directories

## Real Vulnerabilities Hidden Here

To test scanner thoroughness, some REAL vulnerabilities are hidden in:
- Test utility functions that are used in production
- Shared test helpers imported by main code
- Configuration files that affect production builds

These SHOULD be detected despite being in test directories.
