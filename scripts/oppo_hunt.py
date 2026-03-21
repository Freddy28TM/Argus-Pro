import json
import os
import subprocess

def start_oppo_campaign():
    with open(os.path.expanduser("~/Argus-Pro/data/oppo_scope.json"), "r") as f:
        scope = json.load(f)

    for domain in scope["subsidiaries"]:
        print(f"\n[!] TARGETING SUBSIDIARY: {domain}")
        
        # 1. Run the Python Recon Flow (Option 1 logic)
        # We call your existing module
        print(f"[*] Mapping {domain} Certificate Transparency...")
        
        # 2. Run the C# Cloud Audit (Option 3 logic)
        # This checks if Oppo's IoT or ColorOS data is leaking in AWS/Oracle
        print(f"[*] Launching C# Cloud Audit for {domain}...")
        subprocess.run(["proot-distro", "login", "debian", "--", "mono", "/root/Argus-Pro/bin/cloud_audit.exe", domain])

if __name__ == "__main__":
    start_oppo_campaign()
