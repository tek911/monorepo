"""
Configuration Settings
VULNERABILITY: Hardcoded secrets and credentials
CWE-798: Use of Hard-coded Credentials
"""

import os


class Settings:
    # Application
    DEBUG: bool = True  # VULNERABILITY: Debug enabled
    APP_NAME: str = "Billing Service"
    VERSION: str = "1.0.0"

    # VULNERABILITY: Hardcoded database credentials
    DATABASE_URL: str = "postgresql://billing_user:B1ll1ngP@ssw0rd!@localhost:5432/billing"

    # VULNERABILITY: Hardcoded Stripe keys (fake but valid format)
    STRIPE_API_KEY: str = "sk_test_FAKEFAKEFAKEFAKE_NOTREAL"
    STRIPE_WEBHOOK_SECRET: str = "whsec_test_secret_12345"
    STRIPE_PUBLISHABLE_KEY: str = "pk_test_FAKEFAKEFAKEFAKE_NOTREAL"

    # VULNERABILITY: Hardcoded webhook secret
    WEBHOOK_SECRET: str = "webhook-secret-key-12345"

    # VULNERABILITY: Hardcoded JWT secret
    JWT_SECRET: str = "billing-jwt-secret-never-share"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 525600  # VULNERABILITY: 1 year expiration

    # VULNERABILITY: Hardcoded AWS credentials
    AWS_ACCESS_KEY_ID: str = "AKIAIOSFODNN7EXAMPLE"
    AWS_SECRET_ACCESS_KEY: str = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
    AWS_REGION: str = "us-east-1"
    S3_BUCKET: str = "billing-invoices-bucket"

    # VULNERABILITY: Hardcoded encryption key
    ENCRYPTION_KEY: str = "0123456789abcdef0123456789abcdef"

    # VULNERABILITY: Hardcoded API keys for services
    SENDGRID_API_KEY: str = "SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
    TWILIO_ACCOUNT_SID: str = "AC_FAKE_TWILIO_SID_NOT_REAL_000000"
    TWILIO_AUTH_TOKEN: str = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"

    # VULNERABILITY: Hardcoded admin credentials
    ADMIN_EMAIL: str = "admin@billing.vulnmonolith.com"
    ADMIN_PASSWORD: str = "AdminBilling123!"

    # Redis
    REDIS_URL: str = "redis://:redispassword@localhost:6379/0"

    # VULNERABILITY: Internal service tokens
    AUTH_SERVICE_TOKEN: str = "internal-auth-token-billing-12345"

    # Email
    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_USER: str = "billing@vulnmonolith.com"
    SMTP_PASSWORD: str = "EmailP@ssw0rd123!"


settings = Settings()
