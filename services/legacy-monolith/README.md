# Legacy Monolith

Intentionally terrible PHP application demonstrating every anti-pattern.

## Technology Stack

- PHP 5.6 / 7.0 (mixed syntax)
- MySQL (raw queries)
- jQuery 2.2.4
- No framework (procedural PHP)

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | login.php:23 | Critical |
| SQL Injection | users.php:45 | Critical |
| Remote Code Execution | admin/eval.php:12 | Critical |
| Local File Inclusion | includes/router.php:34 | Critical |
| XSS (Reflected) | search.php:56 | High |
| XSS (Stored) | comments.php:78 | High |
| Command Injection | utils/image.php:90 | Critical |
| File Upload | upload.php:34 | High |
| Weak Crypto (MD5) | auth/password.php:12 | High |
| Session Fixation | auth/login.php:45 | Medium |
| CSRF | forms/*.php | Medium |

### Code Quality Issues

- Direct `$_GET`/`$_POST`/`$_REQUEST` usage
- `eval()` with user input
- `include()`/`require()` with user-controlled paths
- Global variables everywhere
- No namespace usage
- Mixed PHP 5 and PHP 7 syntax
- Deeply nested require chains
- No input validation
- No output encoding
- No CSRF protection

### SCA Findings

| Dependency | Version | Issue |
|------------|---------|-------|
| jQuery | 2.2.4 | XSS vulnerabilities |
| PHPMailer | 5.2.0 | RCE vulnerabilities |
| (Vendored) | Various | Abandoned packages |

## Anti-Patterns

- Database credentials in config.php
- Error messages exposing system info
- Debug mode enabled in production
- No prepared statements
- No parameterized queries
- register_globals assumed ON
- magic_quotes_gpc assumed ON
