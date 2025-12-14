package db

import (
	"database/sql"
	"fmt"
	"log"

	_ "github.com/lib/pq"
	"github.com/vulnmonolith/realtime-service/config"
)

var connection *sql.DB

// GetConnection returns the database connection
func GetConnection() *sql.DB {
	if connection == nil {
		cfg := config.Load()

		// VULNERABILITY: Connection string with credentials logged
		connStr := fmt.Sprintf(
			"host=%s port=%d user=%s password=%s dbname=%s sslmode=disable",
			cfg.Database.Host,
			cfg.Database.Port,
			cfg.Database.User,
			cfg.Database.Password,
			cfg.Database.Name,
		)

		// VULNERABILITY: Logging connection string
		log.Printf("Connecting to database: %s", connStr)

		var err error
		connection, err = sql.Open("postgres", connStr)
		if err != nil {
			log.Fatal(err)
		}

		// VULNERABILITY: No connection pool limits
		// Can lead to connection exhaustion
	}

	return connection
}

// ExecuteRaw executes a raw SQL query
// VULNERABILITY: Designed for SQL injection
func ExecuteRaw(query string) (*sql.Rows, error) {
	return GetConnection().Query(query)
}

// ExecRaw executes a raw SQL statement
// VULNERABILITY: Designed for SQL injection
func ExecRaw(query string) (sql.Result, error) {
	return GetConnection().Exec(query)
}
