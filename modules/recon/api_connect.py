import shodan
import os
from dotenv import load_dotenv

load_dotenv("configs/api_keys.env")

class IntelAPI:
    def __init__(self):
        self.shodan_key = os.getenv("SHODAN_API_KEY")
        self.api = shodan.Shodan(self.shodan_key) if self.shodan_key else None

    def shodan_ip(self, ip):
        if not self.api: return "Error: No Shodan Key"
        try:
            results = self.api.host(ip)
            return {
                "ports": results.get('ports', []),
                "os": results.get('os', 'Unknown'),
                "vulns": results.get('vulns', [])
            }
        except Exception as e:
            return {"error": str(e)}
