# Documentation

This directory contains project documentation.

## Purpose

Test scanner handling of:
- Code blocks in Markdown files
- Example configurations with vulnerabilities
- Copy-paste vulnerable snippets

## Contents

- API documentation with example requests
- Architecture diagrams and descriptions
- Runbooks with command examples
- Configuration guides

## Scanner Challenges

### Code in Markdown
Many documents contain code blocks like:

```python
# This vulnerable code is documentation
password = "hardcoded_secret_123"
cursor.execute(f"SELECT * FROM users WHERE id = {user_input}")
```

Should scanners flag code in documentation?

### Configuration Examples
Documentation often includes configuration examples:

```yaml
database:
  host: localhost
  password: admin123

aws:
  access_key: AKIAIOSFODNN7EXAMPLE
  secret_key: wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY
```

### Testing Scenarios

1. **Markdown Code Block Scanning**: Do scanners parse code in `.md` files?
2. **Context Awareness**: Can scanners distinguish documentation from production code?
3. **Example vs Real**: Are documentation examples flagged differently?
4. **Secret Detection in Docs**: Do secret scanners check documentation files?

## Expected Behavior

Ideal scanners should:
- Scan code blocks in documentation (configurable)
- Flag findings with lower severity for documentation
- Detect secrets even in documentation context
- Allow exclusion of documentation directories
