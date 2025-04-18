package dashboard

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
	"github.com/romeo/vulnyx/internal/auth"
)

// RegisterRoutes registers all dashboard routes with the given router
func RegisterRoutes(router *gin.Engine, db *sqlx.DB) {
	// Routes requiring authentication
	authGroup := router.Group("/")
	authGroup.Use(auth.AuthMiddleware(db))

	// Main dashboard
	authGroup.GET("/", func(c *gin.Context) {
		// Get user from context
		user, exists := c.Get("user")
		if !exists {
			c.Redirect(http.StatusSeeOther, "/login")
			return
		}

		c.HTML(http.StatusOK, "dashboard.html", gin.H{
			"user": user,
		})
	})
}
