package config

import (
	"os"
)

// Config holds application configuration
// VULNERABILITY: Hardcoded secrets
// CWE-798: Use of Hard-coded Credentials
type Config struct {
	Port     int
	Debug    bool
	Database DatabaseConfig
	JWT      JWTConfig
	AWS      AWSConfig
	Redis    RedisConfig
}

type DatabaseConfig struct {
	Host     string
	Port     int
	User     string
	Password string
	Name     string
}

type JWTConfig struct {
	Secret     string
	Expiration int
}

type AWSConfig struct {
	AccessKey string
	SecretKey string
	Region    string
}

type RedisConfig struct {
	Host     string
	Port     int
	Password string
}

// VULNERABILITY: Hardcoded default credentials
var defaultConfig = Config{
	Port:  8082,
	Debug: true, // VULNERABILITY: Debug mode enabled
	Database: DatabaseConfig{
		Host:     "localhost",
		Port:     5432,
		User:     "realtime_user",
		Password: "R3alT1m3P@ss!", // VULNERABILITY: Hardcoded password
		Name:     "realtime_db",
	},
	JWT: JWTConfig{
		Secret:     "super-secret-jwt-key-realtime-service", // VULNERABILITY: Hardcoded JWT secret
		Expiration: 31536000,                                 // VULNERABILITY: 1 year expiration
	},
	AWS: AWSConfig{
		AccessKey: "AKIAIOSFODNN7EXAMPLE",                         // VULNERABILITY: Hardcoded AWS key
		SecretKey: "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY",     // VULNERABILITY: Hardcoded AWS secret
		Region:    "us-east-1",
	},
	Redis: RedisConfig{
		Host:     "localhost",
		Port:     6379,
		Password: "redis-password-123", // VULNERABILITY: Hardcoded Redis password
	},
}

// Load loads configuration
func Load() *Config {
	config := defaultConfig

	// Override with environment variables if present
	if host := os.Getenv("DB_HOST"); host != "" {
		config.Database.Host = host
	}
	if pass := os.Getenv("DB_PASSWORD"); pass != "" {
		config.Database.Password = pass
	}

	// VULNERABILITY: Logging configuration with secrets
	// log.Printf("Loaded config: %+v", config)

	return &config
}

// VULNERABILITY: Hardcoded API keys
const (
	InternalAPIKey    = "internal-api-key-realtime-12345"
	WebhookSecret     = "webhook-secret-key-67890"
	EncryptionKey     = "0123456789abcdef0123456789abcdef"
	AdminPassword     = "AdminRealtime123!"
	ServiceAuthToken  = "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzZXJ2aWNlIjoicmVhbHRpbWUifQ"
)

// GetDSN returns database connection string
func GetDSN() string {
	cfg := Load()
	// VULNERABILITY: Logging connection string with password
	dsn := "postgres://" + cfg.Database.User + ":" + cfg.Database.Password +
		"@" + cfg.Database.Host + "/" + cfg.Database.Name
	return dsn
}
