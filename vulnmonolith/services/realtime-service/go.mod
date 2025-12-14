module github.com/vulnmonolith/realtime-service

go 1.18

require (
	// VULNERABLE: jwt-go with CVE-2020-26160
	github.com/dgrijalva/jwt-go v3.2.0+incompatible

	// VULNERABLE: Old crypto library with issues
	golang.org/x/crypto v0.0.0-20210322153248-0c34fe9e7dc2

	// VULNERABLE: Old version of gorilla/websocket
	github.com/gorilla/websocket v1.4.0

	// VULNERABLE: Old gin with security issues
	github.com/gin-gonic/gin v1.6.0

	// Database drivers
	github.com/lib/pq v1.9.0
	github.com/go-sql-driver/mysql v1.5.0

	// VULNERABLE: Old yaml library
	gopkg.in/yaml.v2 v2.2.8

	// Utilities
	github.com/sirupsen/logrus v1.7.0
	github.com/spf13/viper v1.7.1
)
