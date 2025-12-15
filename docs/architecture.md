# System Architecture

## Overview

VulnMonolith is a deliberately vulnerable monorepo for testing security scanners.

## Components

### API Gateway (Node.js/TypeScript)
- Handles all incoming HTTP requests
- Implements authentication middleware
- Routes to appropriate microservices

### Auth Service (Java/Spring Boot)
- Manages user authentication and authorization
- Issues JWT tokens
- Handles password resets

### Billing Service (Python/FastAPI)
- Processes payments
- Generates invoices
- Manages subscriptions

### Realtime Service (Go)
- WebSocket connections
- Real-time notifications
- Event streaming

### Legacy Monolith (PHP)
- Legacy application code
- Gradual migration in progress
- Contains many historical vulnerabilities

## Data Flow

```
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Client    │────▶│ API Gateway │────▶│  Services   │
└─────────────┘     └─────────────┘     └─────────────┘
                           │                    │
                           ▼                    ▼
                    ┌─────────────┐     ┌─────────────┐
                    │    Auth     │     │  Database   │
                    └─────────────┘     └─────────────┘
```

## Configuration

### Database Configuration

```python
# Example database configuration (DO NOT USE IN PRODUCTION)
DATABASE_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "vulnmonolith",
    "username": "app_user",
    "password": "dev_password_123",  # Example only
}
```

### Service Communication

```yaml
# service-mesh-config.yml
services:
  auth:
    url: http://auth-service:8080
    api_key: internal_service_key_abc123
  billing:
    url: http://billing-service:8000
    api_key: internal_service_key_def456
  realtime:
    url: ws://realtime-service:9000
    secret: websocket_secret_ghi789
```

## Security Considerations

### Known Vulnerable Patterns

The following patterns are intentionally vulnerable for testing:

```java
// SQL Injection Example
String query = "SELECT * FROM users WHERE id = " + userId;
statement.executeQuery(query);

// Command Injection Example
Runtime.getRuntime().exec("ping " + userInput);

// Path Traversal Example
File file = new File("/uploads/" + filename);
```

### Mitigation Patterns

Secure alternatives:

```java
// Parameterized Query
PreparedStatement stmt = conn.prepareStatement("SELECT * FROM users WHERE id = ?");
stmt.setInt(1, userId);

// Input Validation
if (!Pattern.matches("[a-zA-Z0-9]+", filename)) {
    throw new SecurityException("Invalid filename");
}
```

## Infrastructure

### AWS Configuration Example

```hcl
# terraform example - contains intentional misconfigurations
resource "aws_s3_bucket" "data" {
  bucket = "vulnmonolith-data"
  acl    = "public-read"  # INSECURE: Public bucket
}

resource "aws_security_group" "web" {
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # INSECURE: Open to world
  }
}
```
