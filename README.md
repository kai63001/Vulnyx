# Vulnyx Scanner

A web security scanner tool written in Go.

## Features

- User authentication system
- Web scanner functionality
- Dashboard to view scan results
- Simple and clean interface

## Requirements

- Go 1.21 or higher
- SQLite3

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/vulnyx.git
   cd vulnyx
   ```

2. Install dependencies:
   ```bash
   go mod download
   ```

3. Build the application:
   ```bash
   go build -o vulnyx
   ```

## Running

Run the compiled binary:

```bash
./vulnyx
```

The application will be available at http://localhost:8080

## Development

For development, you can use:

```bash
go run main.go
```

## Project Structure

```
.
├── internal/             # Internal application code
│   ├── auth/             # Authentication functionality
│   ├── dashboard/        # Dashboard functionality
│   ├── db/               # Database functionality
│   └── scanner/          # Scanner functionality
├── public/               # Static files (CSS, JS, images)
├── templates/            # HTML templates
├── main.go               # Application entry point
├── go.mod                # Go module file
└── README.md             # This file
```

## License

[Your license]
