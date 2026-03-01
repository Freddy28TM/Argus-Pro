import requests
from rich.console import Console

console = Console()

def scan_env(url):
    """Checks for exposed .env files at the root of a domain."""
    if not url.startswith("http"):
        url = f"http://{url}"
    
    target = f"{url.rstrip('/')}/.env"
    paths = [".env", "api/.env", "config/.env", ".env.backup", ".env.old"]
    
    found_leaks = []
    
    for path in paths:
        try:
            full_url = f"{url.rstrip('/')}/{path}"
            response = requests.get(full_url, timeout=5, allow_redirects=False)
            
            # Professional check: 200 OK + keywords like 'DB_PASSWORD' or 'API_KEY'
            if response.status_code == 200 and ("DB_" in response.text or "KEY" in response.text):
                found_leaks.append(full_url)
        except Exception:
            continue
            
    return found_leaks
