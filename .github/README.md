# GitHub Configuration

This directory contains GitHub-specific configurations including CI/CD workflows.

## Security Issues to Test

### Workflow Vulnerabilities
- Unsafe use of `${{ github.event.issue.title }}` (injection)
- Overly permissive `permissions` blocks
- Use of `pull_request_target` with checkout of PR code
- Hardcoded secrets instead of using GitHub Secrets
- Unsafe artifact handling
- Missing `persist-credentials: false` on checkout

### Dependabot Issues
- Misconfigured update schedules
- Missing security update configurations
- Overly broad ignore rules

## Scanner Challenges

- YAML parsing with complex anchors and aliases
- Multi-line strings with embedded code
- Expression injection detection in workflow syntax
