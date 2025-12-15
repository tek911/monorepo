# Orphaned Code

This directory contains "deleted" or abandoned code that still exists in the repository.

## Purpose

Test whether scanners:
- Scan all directories regardless of apparent abandonment
- Detect vulnerabilities in unmaintained code
- Handle stale dependency manifests

## Contents

### Abandoned Projects
- `old-api-v1/` - Previous API version, never deleted
- `prototype-auth/` - Authentication prototype, abandoned
- `failed-migration/` - Incomplete migration code
- `vendor-poc/` - Vendor proof-of-concept, never removed

### Characteristics

1. **No Recent Commits**: Last modified 2+ years ago
2. **Outdated Dependencies**: Ancient package versions
3. **Deprecated Patterns**: Old coding styles and APIs
4. **Missing Documentation**: Unclear purpose
5. **Broken Builds**: May not compile with current tooling

## Vulnerability Categories

- **Extremely Outdated Dependencies**: Libraries from 2018-2019
- **Deprecated Security APIs**: MD5, SHA1, DES, etc.
- **Old Framework Versions**: With known CVEs
- **Hardcoded Credentials**: From development/testing

## Scanner Challenges

1. **Discovery**: Are all directories scanned regardless of git activity?
2. **Priority**: How are findings in orphaned code prioritized?
3. **Manifest Handling**: Old package-lock.json, requirements.txt, pom.xml
4. **False Positive Management**: Old code may trigger more findings

## Real-World Scenario

This simulates a common enterprise pattern:
- Projects get abandoned but not deleted
- "Temporary" code becomes permanent
- Old dependencies never get updated
- Security debt accumulates silently

## Expected Findings

Orphaned code should produce:
- Higher severity findings due to age
- Known CVEs from 2019-2021 timeframe
- Deprecated cryptography warnings
- Unmaintained dependency alerts
