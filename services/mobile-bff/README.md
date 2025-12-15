# Mobile Backend-for-Frontend (BFF)

API gateway specifically designed for mobile applications.

## Stack
- Node.js/TypeScript
- Express
- GraphQL

## Vulnerabilities for Testing

### API Security
- GraphQL introspection enabled in production
- Missing rate limiting
- Improper input validation

### Authentication
- Weak JWT validation
- Token exposure in logs
- Session fixation vulnerabilities

### Data Handling
- Sensitive data in error messages
- Over-fetching in responses
- Missing field-level authorization
