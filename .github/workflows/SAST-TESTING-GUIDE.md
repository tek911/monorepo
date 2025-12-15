# SAST/SCA Monorepo Testing Guide

This directory contains GitHub Actions workflows designed to test SAST (Static Application Security Testing) and SCA (Software Composition Analysis) tools against complex monorepo configurations.

## Purpose

Many SAST/SCA tools fail or produce misleading results when scanning monorepos due to:
- File count limits
- Scan time limits
- Incorrect scope detection
- Poor multi-language support
- Dependency resolution failures
- Cross-service taint tracking limitations

These workflows help identify these failure modes systematically.

## Workflows

### `monorepo-builds.yml` - Production-Style Build Configuration

Simulates a real-world monorepo CI/CD setup with:

| Job | Languages | Test Focus |
|-----|-----------|------------|
| `build-auth-service` | Java (Maven) | Maven dependency resolution, sparse checkout |
| `build-api-gateway` | Node.js (npm) | npm workspace handling, shared SDK linking |
| `build-billing-service` | Python (pip) | requirements.txt parsing, virtual envs |
| `build-realtime-service` | Go + Rust | Multi-language service, CGO/FFI boundaries |
| `build-mobile-bff` | TypeScript | TypeScript compilation, type-aware scanning |
| `build-ml-inference` | Python | Native extensions (numpy/torch), ML models |
| `build-data-pipeline` | Python | DAG definitions, dynamic imports |
| `build-legacy-monolith` | PHP | Mixed PHP/HTML, include paths |
| `scan-infrastructure` | Terraform/K8s/Ansible | IaC tool separation |
| `build-shared-libs` | Node.js | Shared library tracing |
| `build-orphaned` | Mixed | Exclusion handling |
| `build-stress-tests` | Mixed | Parser limits, file count limits |

### `sast-sca-testing.yml` - Dedicated Testing Workflow

Systematic test scenarios with configurable parameters:

#### Test Scenarios

**Scenario 1: Full Repository Scan**
- Tests file count limits
- Tests timeout behavior
- Tests cross-service finding mixing

**Scenario 2: Per-Service Isolated Scans**
- Tests scope isolation
- Tests for missing cross-service findings
- Tests shared-lib exclusion impact

**Scenario 3: Per-Service with Dependencies**
- Tests dependency tracing from service to shared-libs
- Tests finding attribution (service vs lib)

**Scenario 4: Per-Language Aggregated Scans**
- Tests language detection accuracy
- Tests manifest file handling per language
- Tests for incorrect dependency tree merging

**Scenario 5: Incremental/Diff-Based Scans**
- Tests for missed findings in unchanged code
- Tests new usage of existing vulnerable functions

**Scenario 6: IaC Isolated Scans**
- Tests IaC vs application code separation
- Tests Terraform module resolution
- Tests multi-tool IaC handling

**Scenario 7: SCA Dependency Resolution**
- Tests private package resolution
- Tests workspace/monorepo references
- Tests transitive dependency detection

**Scenario 8-9: Stress Tests**
- Tests file limit handling
- Tests parser edge cases (circular imports, encoding)
- Tests timeout behavior

**Scenario 10: Orphaned Code Detection**
- Tests exclusion config compliance
- Tests .gitignore respect

## Usage

### Running the Build Workflow

```bash
# Trigger via GitHub UI or CLI
gh workflow run monorepo-builds.yml

# Build specific services
gh workflow run monorepo-builds.yml -f services="auth,billing"

# Include orphaned code
gh workflow run monorepo-builds.yml -f include_orphaned=true
```

### Running SAST Testing

```bash
# Full repo scan test
gh workflow run sast-sca-testing.yml -f scan_scope=full-repo -f scanner=semgrep

# Per-service isolation test
gh workflow run sast-sca-testing.yml -f scan_scope=per-service -f scanner=codeql

# Include stress tests
gh workflow run sast-sca-testing.yml -f scan_scope=mixed -f scanner=all -f include_stress_tests=true
```

## Repository Structure Relevant to Testing

```
monorepo/
├── services/                    # Production services
│   ├── auth-service/           # Java/Maven
│   ├── api-gateway/            # Node.js/npm
│   ├── billing-service/        # Python/pip
│   ├── realtime-service/       # Go + Rust FFI
│   ├── mobile-bff/             # TypeScript
│   ├── ml-inference/           # Python + ML
│   ├── data-pipeline/          # Python
│   └── legacy-monolith/        # PHP
├── shared-libs/                 # Shared code (should be traced)
│   ├── internal-sdk/           # Node.js shared package
│   └── generated/protobuf/     # Generated code
├── infrastructure/              # IaC (separate scan scope)
│   ├── terraform/
│   ├── kubernetes/
│   ├── ansible/
│   └── cloudformation/
├── orphaned/                    # Should be excluded
├── stress-tests/                # Parser/limit testing
│   ├── scale-tests/many-files/
│   ├── parser-breakers/
│   └── encoding-edge-cases/
├── build-systems/               # Build tool configs (not services)
└── test-fixtures/               # Test data
```

## Expected SAST Tool Failure Modes

### 1. File/Time Limits
- **Symptom**: Scanner reports "completed" but findings are incomplete
- **Test**: Compare full-repo findings vs sum of per-service findings
- **Common limits**: Semgrep ~50k files, CodeQL ~100k files

### 2. Incorrect Scoping
- **Symptom**: Findings from orphaned/ or test-fixtures/ appear
- **Test**: Run with exclusions, verify no excluded paths in results

### 3. Missing Cross-Service Findings
- **Symptom**: Taint flow from Service A -> shared-lib -> Service B not detected
- **Test**: Per-service scan misses what full-repo finds

### 4. Dependency Resolution Failures
- **Symptom**: CVEs not reported, or wrong versions reported
- **Test**: Compare SCA results against known vulnerable dependencies

### 5. Language Detection Failures
- **Symptom**: Go service scanned as JavaScript, or vice versa
- **Test**: Per-language scan should only find files of that language

### 6. IaC/App Code Mixing
- **Symptom**: Terraform findings mixed with Python findings
- **Test**: IaC-isolated scan should have zero app-code findings

## Integrating Your SAST Tool

To test your SAST tool against this repo:

1. **Fork this repository**

2. **Add your scanner workflow** (example for Semgrep):
```yaml
- name: Run Semgrep
  uses: semgrep/semgrep-action@v1
  with:
    config: p/default
```

3. **Run with different scopes** and compare:
   - Full repo scan
   - Per-service with sparse checkout
   - Per-language scans

4. **Document findings**:
   - Files scanned vs expected
   - Time taken
   - Finding count consistency across scopes
   - False positives from orphaned code
   - Missing findings from shared-libs

## Contributing

When adding new test scenarios:

1. Identify a specific failure mode
2. Create reproducible test case
3. Document expected vs actual behavior
4. Add to appropriate workflow file
