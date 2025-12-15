# Internal Tools

This directory contains internal tooling and scripts.

## Structure

### scripts/
- Build automation scripts
- Deployment helpers
- Development utilities
- Data migration tools

## Vulnerability Categories

### Shell Scripts
- Command injection via unquoted variables
- Unsafe use of `eval`
- World-readable credential files
- Hardcoded paths with privilege escalation potential
- Missing input validation

### Python Scripts
- Subprocess calls with shell=True
- Pickle usage for data serialization
- Unsafe YAML loading
- Hardcoded credentials

### Internal Scanners
- Custom security tools with their own vulnerabilities
- Tests whether scanners scan the scanners

## Scanner Challenges

1. **Shell Script Analysis**: Many scanners ignore `.sh` files
2. **Script Language Detection**: Shebang-based language detection
3. **Utility Code**: Often excluded but may contain real issues
4. **Cross-Script Flow**: Data flowing between scripts

## Expected Findings

| File | Vulnerability | Severity |
|------|--------------|----------|
| scripts/deploy.sh | Command injection | High |
| scripts/backup.py | Hardcoded credentials | Critical |
| scripts/migrate.sh | Unsafe temp file creation | Medium |
| scripts/build.sh | Path traversal | Medium |
