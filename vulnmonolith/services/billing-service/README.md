# Billing Service

Python FastAPI payment processing service with intentional vulnerabilities.

## Technology Stack

- Python 3.9
- FastAPI
- SQLAlchemy
- Jinja2
- Various vulnerable dependencies

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| SQL Injection | db/queries.py:34 | Critical |
| SQL Injection | routers/invoices.py:56 | Critical |
| Pickle Deserialization | utils/cache.py:23 | Critical |
| SSTI | templates/email.py:45 | High |
| Path Traversal | routers/reports.py:67 | High |
| Hardcoded Credentials | config/stripe.py:12 | Critical |
| Insecure Redirect | routers/oauth.py:89 | Medium |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| PyYAML | 5.3 | CVE-2020-1747 | Critical |
| Pillow | 8.0.0 | CVE-2021-25287 | High |
| requests | 2.20.0 | CVE-2018-18074 | Medium |
| urllib3 | 1.24.1 | CVE-2019-11324 | Medium |
| Jinja2 | 2.10 | CVE-2019-10906 | Medium |

### Secrets

- Stripe API keys in config files
- Database URL with credentials
- AWS keys in environment defaults

## Build

```bash
cd services/billing-service
pip install -r requirements.txt
uvicorn main:app --reload
```
