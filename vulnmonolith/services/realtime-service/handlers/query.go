package handlers

import (
	"database/sql"
	"encoding/json"
	"fmt"
	"log"
	"net/http"

	"github.com/vulnmonolith/realtime-service/db"
)

// QueryHandler handles database queries
// VULNERABILITY: SQL Injection
func QueryHandler(w http.ResponseWriter, r *http.Request) {
	userID := r.URL.Query().Get("user_id")
	table := r.URL.Query().Get("table")
	orderBy := r.URL.Query().Get("order_by")

	// VULNERABILITY: SQL Injection via string concatenation
	// CWE-89: SQL Injection
	query := fmt.Sprintf("SELECT * FROM %s WHERE user_id = '%s'", table, userID)

	if orderBy != "" {
		// VULNERABILITY: SQL Injection in ORDER BY
		query += fmt.Sprintf(" ORDER BY %s", orderBy)
	}

	// VULNERABILITY: Logging sensitive query
	log.Printf("Executing query: %s", query)

	conn := db.GetConnection()
	rows, err := conn.Query(query)
	if err != nil {
		// VULNERABILITY: Detailed error message exposure
		http.Error(w, fmt.Sprintf("Query error: %v", err), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	results := make([]map[string]interface{}, 0)
	cols, _ := rows.Columns()

	for rows.Next() {
		columns := make([]interface{}, len(cols))
		columnPointers := make([]interface{}, len(cols))
		for i := range columns {
			columnPointers[i] = &columns[i]
		}

		rows.Scan(columnPointers...)

		m := make(map[string]interface{})
		for i, colName := range cols {
			m[colName] = columns[i]
		}
		results = append(results, m)
	}

	json.NewEncoder(w).Encode(results)
}

// SearchHandler handles search requests
// VULNERABILITY: SQL Injection in search
func SearchHandler(w http.ResponseWriter, r *http.Request) {
	searchTerm := r.URL.Query().Get("q")
	field := r.URL.Query().Get("field")

	// VULNERABILITY: SQL Injection
	query := fmt.Sprintf("SELECT * FROM items WHERE %s LIKE '%%%s%%'", field, searchTerm)

	conn := db.GetConnection()
	rows, err := conn.Query(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}
	defer rows.Close()

	// ... process results
	w.Write([]byte("Search completed"))
}

// BatchDeleteHandler handles batch deletion
// VULNERABILITY: SQL Injection in batch operations
func BatchDeleteHandler(w http.ResponseWriter, r *http.Request) {
	ids := r.URL.Query().Get("ids")

	// VULNERABILITY: User input directly in query
	query := fmt.Sprintf("DELETE FROM items WHERE id IN (%s)", ids)

	conn := db.GetConnection()
	result, err := conn.Exec(query)
	if err != nil {
		http.Error(w, err.Error(), http.StatusInternalServerError)
		return
	}

	affected, _ := result.RowsAffected()
	w.Write([]byte(fmt.Sprintf("Deleted %d rows", affected)))
}

// UnsafeQuery demonstrates prepared statement bypass
// VULNERABILITY: Improper use of prepared statements
func UnsafeQuery(db *sql.DB, userInput string) error {
	// VULNERABILITY: Building query string then using Prepare
	// The injection happens before Prepare is called
	queryStr := fmt.Sprintf("SELECT * FROM users WHERE name = '%s'", userInput)
	stmt, err := db.Prepare(queryStr)
	if err != nil {
		return err
	}
	defer stmt.Close()

	_, err = stmt.Exec()
	return err
}
