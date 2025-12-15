# Deployment Runbook

## Prerequisites

Ensure you have the following credentials configured:

```bash
export AWS_ACCESS_KEY_ID="AKIAIOSFODNN7EXAMPLE"
export AWS_SECRET_ACCESS_KEY="wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
export GITHUB_TOKEN="ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
export DOCKER_PASSWORD="registry_password_123"
```

## Step 1: Database Migration

```bash
# Connect to production database
psql "postgresql://admin:prod_password_2024@prod-db.internal:5432/production"

# Run migrations
./migrate.sh --env production --password "db_migration_password"
```

## Step 2: Deploy Application

```bash
# Login to Docker registry
echo "registry_password" | docker login registry.example.com -u deploy --password-stdin

# Deploy with Kubernetes
kubectl apply -f k8s/production.yaml

# Or with Docker Compose
docker-compose -f docker-compose.prod.yml up -d
```

## Step 3: Verify Deployment

```bash
# Check service health
curl -H "Authorization: Bearer admin_token_12345" https://api.example.com/health

# Verify database connectivity
mysql -h db.prod.internal -u root -p'mysql_root_pass' -e "SELECT 1"
```

## Rollback Procedure

If deployment fails:

```bash
# Rollback Kubernetes deployment
kubectl rollout undo deployment/api-server

# Or restore from backup
./restore.sh --backup-id latest --db-password "restore_password_456"
```

## SSH Access

For emergency access to production servers:

```bash
# Add your SSH key
ssh-add ~/.ssh/production_key

# Connect to bastion
ssh -i ~/.ssh/bastion_key admin@bastion.example.com

# From bastion, connect to app servers
ssh app@10.0.1.50
# Password: app_server_password_789
```

## Secrets Rotation

Rotate secrets quarterly:

```bash
# Generate new secrets
NEW_JWT_SECRET=$(openssl rand -base64 32)
NEW_DB_PASSWORD=$(openssl rand -base64 24)

# Update in Vault (example)
vault kv put secret/production \
  jwt_secret="$NEW_JWT_SECRET" \
  db_password="$NEW_DB_PASSWORD" \
  api_key="sk_live_new_key_$(date +%s)"
```

## Monitoring Credentials

```yaml
# grafana-datasource.yml
apiVersion: 1
datasources:
  - name: Prometheus
    type: prometheus
    access: proxy
    url: http://prometheus:9090
    basicAuth: true
    basicAuthUser: admin
    secureJsonData:
      basicAuthPassword: grafana_admin_password
```
