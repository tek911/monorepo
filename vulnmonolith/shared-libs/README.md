# Shared Libraries

This directory contains internal libraries and generated code used across services.

## Structure

### internal-sdk/
Internal SDK used by multiple services with:
- Its own set of vulnerabilities
- Multiple version branches (simulating version drift)
- Dependencies that conflict with service dependencies
- Should trigger findings for each importing service

### legacy-utils/
Vendored legacy utilities with:
- Copy-pasted vulnerable code
- No package manifest reference
- Outdated security practices
- Tests whether scanners detect vendored vulnerabilities

### generated/
Generated code directories:
- `protobuf/` - Protocol buffer generated files
- `graphql/` - GraphQL code generation output
- `openapi/` - OpenAPI client generation
- `thrift/` - Apache Thrift generated code

## Scanner Challenges

### internal-sdk/
- Should scanners follow internal imports?
- How are transitive internal dependencies handled?
- Version conflict detection across services

### legacy-utils/
- Detection without manifest file reference
- Matching vendored code to known vulnerable libraries
- False positive management for intentionally copied code

### generated/
- Should generated code be scanned?
- Can scanners identify and exclude generated files?
- Do scanners understand generation markers/comments?
- Performance impact of scanning generated code

## Testing Scenarios

1. **Transitive Vulnerability Tracking**: If internal-sdk has a vulnerability, do all importing services get flagged?
2. **Vendored Code Detection**: Can scanners match copied code to known vulnerable versions?
3. **Generated Code Exclusion**: Do scanners respect generated code markers?
4. **Version Conflict Resolution**: How do scanners handle conflicting versions in shared code?
