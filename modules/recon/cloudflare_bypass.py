import socket
import requests
import mmh3 # pip install mmh3 if not present
import codecs
from rich.console import Console

console = Console()

def get_favicon_hash(url):
    """Calculates the favicon hash for Shodan/Censys searching."""
    try:
        response = requests.get(f"{url}/favicon.ico", timeout=5, verify=False)
        favicon = codecs.encode(response.content, "base64")
        hash_val = mmh3.hash(favicon)
        return hash_val
    except:
        return None

def check_direct_connect(domain):
    """Checks for common subdomains that often point directly to the origin."""
    subdomains = ["mail", "dev", "vpn", "direct", "origin", "ftp", "staging"]
    results = []
    
    for sub in subdomains:
        target = f"{sub}.{domain}"
        try:
            ip = socket.gethostbyname(target)
            # Check if IP is NOT in Cloudflare's known ranges
            console.print(f"[green][+][/green] Potential Origin Found: {ip} ({target})")
            results.append(ip)
        except:
            continue
    return results

def run_bypass(domain):
    console.print(f"\n[bold yellow][*] Bypassing Cloudflare for:[/bold yellow] {domain}")
    
    # 1. Favicon Search String
    f_hash = get_favicon_hash(f"https://{domain}")
    if f_hash:
        console.print(f"[cyan][i][/cyan] Shodan Search: http.favicon.hash:{f_hash}")
    
    # 2. Subdomain Check
    origin_ips = check_direct_connect(domain)
    
    return origin_ips
