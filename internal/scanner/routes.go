package scanner

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"github.com/romeo/vulnyx/internal/auth"
)

// RegisterRoutes registers all scanner routes with the given router
func RegisterRoutes(router *gin.Engine, db *sqlx.DB) {
	// Routes requiring authentication
	scannerGroup := router.Group("/scan")
	scannerGroup.Use(auth.AuthMiddleware(db))

	// Scan form page
	scannerGroup.GET("/", func(c *gin.Context) {
		user, _ := c.Get("user")
		c.HTML(http.StatusOK, "scan.html", gin.H{
			"user": user,
		})
	})

	// Start scan
	scannerGroup.POST("/", func(c *gin.Context) {
		user, _ := c.Get("user")
		target := c.PostForm("target")

		// Basic validation
		if target == "" {
			c.HTML(http.StatusBadRequest, "scan.html", gin.H{
				"user":  user,
				"error": "Target URL is required",
			})
			return
		}

		// Here we would start the actual scan process
		// For now we just return a placeholder

		c.HTML(http.StatusOK, "scan_results.html", gin.H{
			"user":   user,
			"target": target,
			"status": "Scan completed successfully",
			"results": []map[string]string{
				{
					"type":        "Info",
					"description": "Scan started for " + target,
				},
				{
					"type":        "Info",
					"description": "This is a placeholder for scan results",
				},
			},
		})
	})

	// Show scan history
	scannerGroup.GET("/history", func(c *gin.Context) {
		user, _ := c.Get("user")
		// Here we would retrieve scan history from the database

		c.HTML(http.StatusOK, "scan_history.html", gin.H{
			"user": user,
			"history": []map[string]string{
				{
					"id":        "1",
					"target":    "example.com",
					"timestamp": "2023-05-01 12:00:00",
					"status":    "Completed",
					"findings":  "2",
				},
			},
		})
	})
}
