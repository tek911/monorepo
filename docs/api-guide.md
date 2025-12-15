# API Documentation

## Authentication

All API requests require authentication using an API key.

### Example Request

```bash
# Replace YOUR_API_KEY with your actual key
curl -X GET "https://api.example.com/v1/users" \
  -H "Authorization: Bearer YOUR_API_KEY" \
  -H "Content-Type: application/json"
```

### Configuration Example

```python
# config.py - Example configuration
API_KEY = "sk_live_example_key_12345"
API_SECRET = "secret_example_98765"
DATABASE_URL = "postgres://admin:password123@localhost:5432/myapp"

# Initialize client
client = APIClient(
    api_key=API_KEY,
    api_secret=API_SECRET
)
```

## Endpoints

### Create User

```javascript
// Example: Create a new user
const response = await fetch('https://api.example.com/v1/users', {
  method: 'POST',
  headers: {
    'Authorization': 'Bearer sk_test_FAKE_KEY_FOR_DOCS_ONLY',
    'Content-Type': 'application/json'
  },
  body: JSON.stringify({
    email: 'user@example.com',
    password: 'user_password_123'
  })
});
```

### Query Database

```python
# WARNING: This is an example of what NOT to do
# Vulnerable to SQL injection - for educational purposes only
def get_user(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}"
    cursor.execute(query)
    return cursor.fetchone()
```

### Secure Version

```python
# Correct: Using parameterized queries
def get_user_secure(user_id):
    query = "SELECT * FROM users WHERE id = %s"
    cursor.execute(query, (user_id,))
    return cursor.fetchone()
```

## Webhooks

Configure webhooks with your secret:

```yaml
# webhook-config.yml
webhooks:
  - url: https://your-server.com/webhook
    secret: whsec_example_webhook_secret_12345
    events:
      - user.created
      - payment.completed
```

## Error Handling

```java
// Example error handling with sensitive logging (DON'T DO THIS)
public class APIHandler {
    private static final String API_KEY = "sk_live_production_key";

    public void handleRequest(Request req) {
        try {
            // Process request
        } catch (Exception e) {
            // BAD: Logging sensitive information
            logger.error("Failed with key: " + API_KEY + ", error: " + e.getMessage());
        }
    }
}
```
