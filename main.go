package main

import (
	"fmt"
	"log"

	"github.com/gin-gonic/gin"
	_ "github.com/mattn/go-sqlite3"
	"github.com/romeo/vulnyx/internal/auth"
	"github.com/romeo/vulnyx/internal/dashboard"
	"github.com/romeo/vulnyx/internal/db"
	"github.com/romeo/vulnyx/internal/scanner"
)

func main() {
	// Initialize database
	database, err := db.InitDB()
	if err != nil {
		log.Fatalf("Failed to initialize database: %v", err)
	}
	defer database.Close()

	// Create router
	router := gin.Default()

	// Set up templates
	router.LoadHTMLGlob("templates/*")

	// Set up static files
	router.Static("/static", "public")

	// Set up routes
	auth.RegisterRoutes(router, database)
	scanner.RegisterRoutes(router, database)
	dashboard.RegisterRoutes(router, database)

	// Start server
	fmt.Println("🚀 Vulnyx Scanner starting at http://localhost:8080")
	if err := router.Run(":8080"); err != nil {
		log.Fatalf("Failed to start server: %v", err)
	}
}
