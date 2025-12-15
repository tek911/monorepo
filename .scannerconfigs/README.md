# Scanner Configurations

This directory contains example configuration files for various security scanning tools.

## Purpose

- Test how tools handle custom configurations
- Provide baseline configs for testing exclusion rules
- Document expected behavior for different tools

## Included Configurations

- `.semgrepignore` - Semgrep exclusion patterns
- `.snyk` - Snyk configuration
- `.trivyignore` - Trivy exclusion patterns
- `checkov.yaml` - Checkov configuration
- `sonar-project.properties` - SonarQube configuration
- `codeql-config.yml` - CodeQL configuration
- `.gitleaks.toml` - Gitleaks secret detection config
- `bandit.yaml` - Python Bandit configuration
- `.hadolint.yaml` - Dockerfile linting
- `tfsec.yaml` - Terraform security scanning

## Testing Scenarios

1. **Exclusion Testing**: Verify scanners respect ignore patterns
2. **Severity Mapping**: Test custom severity configurations
3. **Rule Customization**: Test enabling/disabling specific rules
4. **Path Filtering**: Test include/exclude path patterns
