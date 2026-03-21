import requests
import json
import os

def fetch_recent_exploits():
    print("[*] Connecting to high-speed CVE source...")
    # Using a different endpoint that is more mobile-friendly
    url = "https://cve.circl.lu/api/last/30"
    headers = {'User-Agent': 'Mozilla/5.0'}
    
    try:
        # Increased timeout to 30 seconds for slow mobile connections
        response = requests.get(url, headers=headers, timeout=30)
        
        if response.status_code == 200:
            cves = response.json()
            db_path = os.path.expanduser("~/Argus-Pro/data/exploit_db.json")
            os.makedirs(os.path.dirname(db_path), exist_ok=True)
            
            formatted_data = {"exploits": []}
            for item in cves:
                formatted_data["exploits"].append({
                    "name": item.get("summary", "No Description")[:100],
                    "id": item.get("id", "Unknown"),
                    "cvss": item.get("cvss", "N/A")
                })
                
            with open(db_path, "w") as f:
                json.dump(formatted_data, f, indent=4)
            print(f"[+] Success! Local database updated.")
        else:
            print(f"[!] Server returned status: {response.status_code}")
            
    except Exception as e:
        print(f"[!] Connection failed: {e}")
        print("[*] TIP: Check your internet or try using a VPN if you're on a restricted network.")

if __name__ == "__main__":
    fetch_recent_exploits()
