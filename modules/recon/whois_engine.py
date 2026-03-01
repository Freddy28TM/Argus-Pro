import whois
from rich.console import Console

console = Console()

def get_whois(domain):
    try:
        w = whois.whois(domain)
        return {
            "registrar": w.registrar,
            "creation_date": w.creation_date,
            "expiry_date": w.expiration_date,
            "emails": w.emails,
            "name_servers": w.name_servers
        }
    except Exception as e:
        return {"error": str(e)}
