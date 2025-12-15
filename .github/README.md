# VulnMonolith - AppSec Tool Testing Monorepo

## Purpose

VulnMonolith is a purposefully vulnerable monorepo designed to stress-test application security tools including:

- **SAST** (Static Application Security Testing)
- **SCA** (Software Composition Analysis)
- **IAST** (Interactive Application Security Testing)
- **RASP** (Runtime Application Self-Protection)
- **IaC Scanning** (Infrastructure as Code)
- **Secrets Detection**

## Goals

This repository evaluates how security tools handle:

1. **Monorepo scale and complexity** - 50,000+ files across 15+ languages
2. **Multiple languages and build systems** - Gradle, Maven, npm, pip, cargo, go modules, CMake, Bazel
3. **Edge cases that cause parser failures** - Malformed syntax, extreme file sizes, encoding issues
4. **Realistic enterprise anti-patterns** - Vendored code, version conflicts, abandoned directories
5. **Selective scanning and exclusion capabilities** - Test fixture exclusion, generated code handling

## Structure Overview

```
vulnmonolith/
├── .github/workflows/          # CI configs with security issues
├── .scannerconfigs/            # Example configs for various scanners
├── build-systems/              # Multiple build system examples
├── services/                   # Microservices in various languages
├── infrastructure/             # IaC (Terraform, K8s, CloudFormation, etc.)
├── shared-libs/                # Internal libraries and generated code
├── vendor/                     # Vendored third-party code
├── test-fixtures/              # Test files (should be excluded)
├── tools/                      # Internal tooling
├── docs/                       # Documentation with code blocks
├── stress-tests/               # Parser breakers and scale tests
└── orphaned/                   # Abandoned code that still gets scanned
```

## Services

| Service | Language | Key Vulnerabilities |
|---------|----------|---------------------|
| auth-service | Java Spring Boot | SQLi, XXE, Insecure Deserialization, Log4Shell |
| api-gateway | Node.js/TypeScript | Prototype Pollution, SSRF, Command Injection |
| billing-service | Python FastAPI | SQLi, Pickle RCE, SSTI, Hardcoded Keys |
| data-pipeline | Scala Spark | Unsafe Deserialization, Injection |
| legacy-monolith | PHP | Everything wrong with PHP security |
| ml-inference | Python + C++ | Buffer Overflows, Unsafe Extensions |
| mobile-bff | Kotlin | Insecure Data Storage, Weak Crypto |
| realtime-service | Go + Rust | Race Conditions, Memory Issues |

## Usage

### For Security Tool Testing

1. Point your security scanner at this repository
2. Compare findings against `VULNERABILITY_INVENTORY.md`
3. Evaluate false positives/negatives
4. Test scanning performance and parser robustness

### For Tool Configuration Testing

1. Use configs in `.scannerconfigs/` as templates
2. Test exclusion patterns work correctly
3. Verify severity mappings
4. Test incremental scanning capabilities

## Warning

**This repository contains intentionally vulnerable code and fake (but valid-format) secrets.**

- Do NOT deploy any code from this repository
- Do NOT use any credentials found here (they are fake but properly formatted)
- This is for security tool testing ONLY

## Contributing

See `CONTRIBUTING.md` for guidelines on adding new vulnerability patterns.

## Vulnerability Inventory

See `VULNERABILITY_INVENTORY.md` for a complete list of seeded vulnerabilities with:
- File paths and line numbers
- Vulnerability type and severity
- Expected detection by tool category
- CWE/CVE references where applicable

## License

MIT License - Use freely for security testing and research.
