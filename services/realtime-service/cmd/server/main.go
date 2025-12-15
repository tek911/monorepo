package main

import (
	"fmt"
	"log"
	"net/http"

	"github.com/vulnmonolith/realtime-service/config"
	"github.com/vulnmonolith/realtime-service/handlers"
)

func main() {
	cfg := config.Load()

	// VULNERABILITY: Logging sensitive configuration
	log.Printf("Starting server with config: %+v", cfg)

	http.HandleFunc("/ws", handlers.WebSocketHandler)
	http.HandleFunc("/api/query", handlers.QueryHandler)
	http.HandleFunc("/api/exec", handlers.ExecHandler)
	http.HandleFunc("/api/file", handlers.FileHandler)
	http.HandleFunc("/api/fetch", handlers.FetchHandler)
	http.HandleFunc("/api/cache", handlers.CacheHandler)

	addr := fmt.Sprintf(":%d", cfg.Port)
	log.Printf("Server listening on %s", addr)

	// VULNERABILITY: No TLS configuration
	if err := http.ListenAndServe(addr, nil); err != nil {
		log.Fatal(err)
	}
}
