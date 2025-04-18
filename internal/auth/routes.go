package auth

import (
	"net/http"

	"github.com/gin-gonic/gin"
	"github.com/jmoiron/sqlx"
)

// RegisterRoutes registers all auth routes with the given router
func RegisterRoutes(router *gin.Engine, db *sqlx.DB) {
	// Login routes
	router.GET("/login", func(c *gin.Context) {
		// Check if user is already logged in
		tokenString, err := c.Cookie("auth_token")
		if err == nil {
			// Try to validate token
			_, err := ValidateToken(tokenString)
			if err == nil {
				c.Redirect(http.StatusSeeOther, "/")
				return
			}
		}

		// Check if registration is allowed
		isFirst, err := IsFirstUser(db)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Database error",
			})
			return
		}

		c.HTML(http.StatusOK, "login.html", gin.H{
			"can_register": isFirst,
		})
	})

	router.POST("/login", func(c *gin.Context) {
		username := c.PostForm("username")
		password := c.PostForm("password")

		user, err := AuthenticateUser(db, username, password)
		if err != nil {
			isFirst, _ := IsFirstUser(db)
			c.HTML(http.StatusUnauthorized, "login.html", gin.H{
				"error":        "Incorrect username or password",
				"can_register": isFirst,
			})
			return
		}

		// Generate token
		token, err := GenerateToken(user.Username)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Error generating authentication token",
			})
			return
		}

		// Set cookie
		c.SetCookie(
			"auth_token",
			token,
			1800, // 30 minutes
			"/",
			"",
			false,
			true,
		)

		c.Redirect(http.StatusSeeOther, "/")
	})

	// Register routes
	router.GET("/register", func(c *gin.Context) {
		// Check if registration is allowed
		isFirst, err := IsFirstUser(db)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Database error",
			})
			return
		}

		if !isFirst {
			c.HTML(http.StatusOK, "register.html", gin.H{
				"disabled":      true,
				"is_first_user": false,
			})
			return
		}

		c.HTML(http.StatusOK, "register.html", gin.H{
			"is_first_user": isFirst,
		})
	})

	router.POST("/register", func(c *gin.Context) {
		// Check if registration is allowed
		isFirst, err := IsFirstUser(db)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Database error",
			})
			return
		}

		if !isFirst {
			c.HTML(http.StatusOK, "register.html", gin.H{
				"disabled":      true,
				"is_first_user": false,
			})
			return
		}

		// Get form data
		username := c.PostForm("username")
		email := c.PostForm("email")
		password := c.PostForm("password")
		confirmPassword := c.PostForm("confirm_password")

		// Validate input
		if password != confirmPassword {
			c.HTML(http.StatusBadRequest, "register.html", gin.H{
				"error":         "Passwords do not match",
				"is_first_user": isFirst,
			})
			return
		}

		// Check if username exists
		var userCount int
		err = db.Get(&userCount, "SELECT COUNT(*) FROM users WHERE username = ?", username)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Database error",
			})
			return
		}

		if userCount > 0 {
			c.HTML(http.StatusBadRequest, "register.html", gin.H{
				"error":         "Username already exists",
				"is_first_user": isFirst,
			})
			return
		}

		// Check if email exists
		err = db.Get(&userCount, "SELECT COUNT(*) FROM users WHERE email = ?", email)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Database error",
			})
			return
		}

		if userCount > 0 {
			c.HTML(http.StatusBadRequest, "register.html", gin.H{
				"error":         "Email already exists",
				"is_first_user": isFirst,
			})
			return
		}

		// Hash password
		hashedPassword, err := HashPassword(password)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Error hashing password",
			})
			return
		}

		// Create user
		_, err = db.Exec(
			"INSERT INTO users (username, email, hashed_password, is_admin) VALUES (?, ?, ?, ?)",
			username, email, hashedPassword, isFirst,
		)
		if err != nil {
			c.HTML(http.StatusInternalServerError, "error.html", gin.H{
				"error": "Error creating user",
			})
			return
		}

		c.HTML(http.StatusOK, "login.html", gin.H{
			"message":      "Registration successful. You can now log in.",
			"can_register": false,
		})
	})

	// Logout route
	router.GET("/logout", func(c *gin.Context) {
		c.SetCookie("auth_token", "", -1, "/", "", false, true)
		c.Redirect(http.StatusSeeOther, "/login")
	})
}
