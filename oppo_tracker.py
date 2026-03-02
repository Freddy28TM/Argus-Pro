import os
from modules.recon.universal_dissector import UniversalDissector

def track_oppo():
    subdomain_file = "data/oppo/subdomains.txt"
    if not os.path.exists(subdomain_file):
        print("[-] No subdomain file found. Run discovery first.")
        return

    with open(subdomain_file, "r") as f:
        targets = f.read().splitlines()

    for target in targets:
        print(f"\n[!] Investigating: {target}")
        scanner = UniversalDissector(target)
        # Scan common web and admin ports
        scanner.run_full_stack(ports=[80, 443, 8080, 8443, 3306])

if __name__ == "__main__":
    track_oppo()
