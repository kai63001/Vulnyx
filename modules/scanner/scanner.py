import random
import string
from numba import jit

@jit(nopython=True)
def calculate_score(x):
    # Example JIT function for heavy calculations
    result = 0
    for i in range(x):
        result += i * i
    return result

def simulate_vulnerability_scan(domain, scan_type):
    """Simulate a vulnerability scan and return results."""
    vuln_types = [
        "SQL Injection", "XSS", "CSRF", "Open Redirect", 
        "Insecure Deserialization", "XML External Entity", 
        "Server-Side Request Forgery", "Command Injection"
    ]
    
    severity_levels = ["High", "Medium", "Low"]
    
    # Simulate finding different numbers of vulnerabilities based on scan type
    num_vulns = 0
    if scan_type == "full":
        num_vulns = random.randint(3, 8)
    elif scan_type == "vuln":
        num_vulns = random.randint(2, 5)
    elif scan_type == "quick":
        num_vulns = random.randint(0, 3)
    elif scan_type == "recon":
        num_vulns = random.randint(0, 2)
    
    vulnerabilities = []
    for _ in range(num_vulns):
        vuln_type = random.choice(vuln_types)
        severity = random.choice(severity_levels)
        
        # Generate random paths based on vulnerability type
        if vuln_type == "SQL Injection":
            path = f"/api/{random.choice(['users', 'products', 'search'])}"
        elif vuln_type == "XSS":
            path = f"/{random.choice(['contact', 'comments', 'profile'])}"
        else:
            path = f"/{random.choice(string.ascii_lowercase)}/{random.choice(string.ascii_lowercase)}"
        
        # Generate sample code for the vulnerability
        code = None
        if random.random() > 0.5:
            if vuln_type == "SQL Injection":
                code = 'query = f"SELECT * FROM users WHERE username = \'{username}\'"'
            elif vuln_type == "XSS":
                code = 'element.innerHTML = userInput'
            elif vuln_type == "Command Injection":
                code = 'os.system("ping " + user_supplied_ip)'
        
        # Generate descriptions and recommendations
        descriptions = {
            "SQL Injection": "The application doesn't properly sanitize user input before using it in SQL queries.",
            "XSS": "User input is reflected in the page without proper encoding.",
            "CSRF": "The application doesn't implement anti-CSRF tokens for sensitive actions.",
            "Open Redirect": "The application redirects to URLs provided in parameters without validation.",
            "Insecure Deserialization": "The application deserializes untrusted data without proper validation.",
            "Command Injection": "User input is passed directly to system commands without proper sanitization."
        }
        
        recommendations = {
            "SQL Injection": "Use parameterized queries or an ORM instead of string concatenation.",
            "XSS": "Implement output encoding and Content Security Policy (CSP).",
            "CSRF": "Implement anti-CSRF tokens for all state-changing operations.",
            "Open Redirect": "Validate redirect URLs against a whitelist or use relative paths.",
            "Insecure Deserialization": "Implement integrity checks and don't deserialize data from untrusted sources.",
            "Command Injection": "Use safer alternatives or strictly validate and sanitize all user input."
        }
        
        vulnerabilities.append({
            "type": vuln_type,
            "path": path,
            "severity": severity,
            "description": descriptions.get(vuln_type, "A security vulnerability was detected."),
            "recommendation": recommendations.get(vuln_type, "Review and fix the issue following security best practices."),
            "code": code
        })
    
    # Simulate discovered paths for reconnaissance
    paths = []
    if scan_type in ["full", "recon"]:
        common_paths = ["/admin", "/api", "/login", "/register", "/upload", "/backup", 
                        "/config", "/dashboard", "/users", "/profile", "/settings"]
        num_paths = random.randint(5, 15)
        paths = random.sample(common_paths + [f"/{random.choice(string.ascii_lowercase)}" for _ in range(10)], num_paths)
    
    # Calculate the risk score based on vulnerabilities
    high_risk = sum(1 for v in vulnerabilities if v["severity"] == "High")
    medium_risk = sum(1 for v in vulnerabilities if v["severity"] == "Medium")
    low_risk = sum(1 for v in vulnerabilities if v["severity"] == "Low")
    
    risk_score = (high_risk * 10) + (medium_risk * 5) + (low_risk * 2)
    
    return {
        "vulnerabilities": vulnerabilities,
        "paths": paths,
        "high_risk": high_risk,
        "medium_risk": medium_risk,
        "low_risk": low_risk,
        "risk_score": risk_score
    } 