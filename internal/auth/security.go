package auth

import (
	"errors"
	"time"

	"github.com/gin-gonic/gin"
	"github.com/golang-jwt/jwt/v5"
	"github.com/jmoiron/sqlx"
)

// JWT configuration
const (
	secretKey       = "CHANGE_THIS_TO_A_SECURE_SECRET_IN_PRODUCTION"
	tokenExpiration = 30 * time.Minute
)

// Claims represents the JWT claims
type Claims struct {
	Username string `json:"username"`
	jwt.RegisteredClaims
}

// AuthenticateUser authenticates a user by username and password
func AuthenticateUser(db *sqlx.DB, username, password string) (*User, error) {
	var user User
	query := "SELECT * FROM users WHERE username = ?"
	err := db.Get(&user, query, username)
	if err != nil {
		return nil, errors.New("invalid username or password")
	}

	if !CheckPasswordHash(password, user.HashedPassword) {
		return nil, errors.New("invalid username or password")
	}

	return &user, nil
}

// GenerateToken creates a new JWT token for a user
func GenerateToken(username string) (string, error) {
	expirationTime := time.Now().Add(tokenExpiration)
	claims := &Claims{
		Username: username,
		RegisteredClaims: jwt.RegisteredClaims{
			ExpiresAt: jwt.NewNumericDate(expirationTime),
			IssuedAt:  jwt.NewNumericDate(time.Now()),
			Subject:   username,
		},
	}

	token := jwt.NewWithClaims(jwt.SigningMethodHS256, claims)
	return token.SignedString([]byte(secretKey))
}

// ValidateToken validates a JWT token
func ValidateToken(tokenString string) (*Claims, error) {
	claims := &Claims{}
	token, err := jwt.ParseWithClaims(tokenString, claims, func(token *jwt.Token) (interface{}, error) {
		return []byte(secretKey), nil
	})

	if err != nil {
		return nil, err
	}

	if !token.Valid {
		return nil, errors.New("invalid token")
	}

	return claims, nil
}

// IsFirstUser checks if there are no users in the system
func IsFirstUser(db *sqlx.DB) (bool, error) {
	var count int
	err := db.Get(&count, "SELECT COUNT(*) FROM users")
	if err != nil {
		return false, err
	}
	return count == 0, nil
}

// AuthMiddleware is a Gin middleware to authenticate requests
func AuthMiddleware(db *sqlx.DB) gin.HandlerFunc {
	return func(c *gin.Context) {
		tokenString, err := c.Cookie("auth_token")
		if err != nil {
			c.Redirect(302, "/login")
			c.Abort()
			return
		}

		claims, err := ValidateToken(tokenString)
		if err != nil {
			c.Redirect(302, "/login")
			c.Abort()
			return
		}

		// Get user from database
		var user User
		err = db.Get(&user, "SELECT * FROM users WHERE username = ?", claims.Username)
		if err != nil {
			c.Redirect(302, "/login")
			c.Abort()
			return
		}

		// Store user in context
		c.Set("user", user)
		c.Next()
	}
}
