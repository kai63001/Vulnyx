# Vulnyx Scanner

A modern web security scanner with a terminal-inspired UI that helps identify vulnerabilities, perform reconnaissance, and track security issues in web applications.

## Features

- **Multiple Scan Types**: Full scan, quick scan, vulnerability scan, and reconnaissance
- **Vulnerability Detection**: Identifies common web vulnerabilities like SQL Injection, XSS, CSRF, etc.
- **Path Discovery**: Finds hidden directories and files during reconnaissance
- **Scan History**: Maintains a record of all completed scans
- **Detailed Reports**: Comprehensive vulnerability reports with severity ratings, descriptions, and recommendations
- **Modern UI**: Terminal-inspired interface built with terminal.css and Tailwind CSS

## Screenshots

- Dashboard with active scans and recent vulnerabilities
- Detailed vulnerability reports with risk assessment
- Scan history with filtering and sorting options

## Installation

1. Clone the repository:
```bash
git clone https://github.com/yourusername/vulnyx-scanner.git
cd vulnyx-scanner
```

2. Create a virtual environment and install dependencies:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

3. Run the application:
```bash
python main.py
```

4. Open your browser and navigate to http://localhost:8000

## Usage

1. Enter a domain name in the scan form (e.g., example.com)
2. Select the scan type (Full, Quick, Vulnerability, or Reconnaissance)
3. Click "Scan Website" to begin the scan
4. View the results in the dashboard, history, and vulnerability report sections

## Development

### Prerequisites

- Python 3.8+
- FastAPI
- Jinja2
- Tailwind CSS (via CDN)
- terminal.css (via CDN)

### Project Structure

```
vulnyx-scanner/
├── main.py            # Main application file
├── templates/         # Jinja2 templates
│   └── dashboard.html # Main UI template
├── public/            # Static assets
│   └── main.css       # Custom CSS styles
├── results/           # Scan results storage
└── requirements.txt   # Python dependencies
```

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
