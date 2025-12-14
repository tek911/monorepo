# API Gateway

Node.js/TypeScript Express gateway with intentional vulnerabilities.

## Technology Stack

- Node.js 16
- TypeScript 4.5
- Express 4.16.0
- Various vulnerable dependencies

## Vulnerabilities

### SAST Findings

| Type | Location | Severity |
|------|----------|----------|
| Prototype Pollution | utils/merge.ts:34 | Critical |
| Command Injection | handlers/file.ts:56 | Critical |
| SSRF | handlers/preview.ts:23 | High |
| Path Traversal | middleware/static.ts:45 | High |
| ReDoS | validators/email.ts:12 | Medium |
| Timing Attack | auth/compare.ts:8 | Medium |
| XSS | templates/error.ts:67 | High |

### SCA Findings

| Dependency | Version | CVE | Severity |
|------------|---------|-----|----------|
| lodash | 4.17.15 | CVE-2020-8203 | High |
| axios | 0.21.0 | CVE-2021-3749 | High |
| express | 4.16.0 | CVE-2019-15138 | Medium |
| minimist | 1.2.0 | CVE-2020-7598 | High |
| node-fetch | 2.6.0 | CVE-2022-0235 | Medium |

### Secrets

- API keys in .env.example
- Hardcoded tokens in config/
- Base64-encoded credentials in tests

## Build

```bash
cd services/api-gateway
npm install
npm run build
npm start
```
