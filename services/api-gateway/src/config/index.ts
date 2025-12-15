/**
 * Configuration file with hardcoded secrets
 * VULNERABILITY: Hardcoded credentials throughout
 * CWE-798: Use of Hard-coded Credentials
 */

export const config = {
    // Server configuration
    port: process.env.PORT || 3000,
    environment: process.env.NODE_ENV || 'development',

    // VULNERABILITY: Hardcoded database credentials
    database: {
        host: 'localhost',
        port: 5432,
        name: 'apigateway',
        user: 'admin',
        password: 'Sup3rS3cr3tP@ssw0rd!'  // VULNERABILITY
    },

    // VULNERABILITY: Hardcoded JWT configuration
    jwt: {
        secret: 'jwt-secret-key-never-commit-this-to-git',
        expiresIn: '365d',  // VULNERABILITY: Extremely long expiration
        algorithm: 'HS256'
    },

    // VULNERABILITY: Hardcoded API keys
    apiKeys: {
        google: 'AIzaSyDxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        stripe: 'sk_live_FAKEFAKEFAKEFAKE_NOTREALxxxxxxxx',
        sendgrid: 'SG.xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx',
        twilio: {
            accountSid: 'AC_FAKE_TWILIO_SID_NOT_REAL_000000',
            authToken: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        }
    },

    // VULNERABILITY: AWS credentials
    aws: {
        accessKeyId: 'AKIAIOSFODNN7EXAMPLE',
        secretAccessKey: 'wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY',
        region: 'us-east-1',
        s3Bucket: 'my-private-bucket'
    },

    // VULNERABILITY: OAuth secrets
    oauth: {
        github: {
            clientId: 'Iv1.xxxxxxxxxxxxxxxxx',
            clientSecret: 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
        },
        google: {
            clientId: 'xxxxxxxxxxxx-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com',
            clientSecret: 'GOCSPX-xxxxxxxxxxxxxxxxxxxxxxxx'
        }
    },

    // VULNERABILITY: Encryption keys
    encryption: {
        key: '0123456789abcdef0123456789abcdef',
        iv: 'abcdef0123456789'
    },

    // VULNERABILITY: Internal service tokens
    services: {
        authService: {
            url: 'http://auth-service:8080',
            apiKey: 'internal-auth-service-key-12345'
        },
        billingService: {
            url: 'http://billing-service:8000',
            apiKey: 'internal-billing-service-key-67890'
        }
    },

    // VULNERABILITY: Admin credentials
    admin: {
        username: 'admin',
        password: 'admin123!@#',
        email: 'admin@vulnmonolith.com'
    },

    // VULNERABILITY: Database connection strings with credentials
    connectionStrings: {
        postgres: 'postgresql://admin:password123@localhost:5432/apigateway',
        mongodb: 'mongodb://root:rootpassword@localhost:27017/admin',
        redis: 'redis://:redispassword@localhost:6379'
    }
};

// VULNERABILITY: Exporting sensitive config
export default config;
