import os
from modules.recon.universal_dissector import UniversalDissector

def scan_interesting_targets():
    # Only scan the high-value targets found by our filter
    target_file = "data/oppo/high_value.txt"
    if not os.path.exists(target_file):
        print("[-] No high-value targets found yet.")
        return

    with open(target_file, "r") as f:
        targets = f.read().splitlines()

    for target in targets:
        print(f"\n[🔥] High-Value Target Found: {target}")
        scanner = UniversalDissector(target)
        # Deep scan on interesting ports
        scanner.run_full_stack(ports=[22, 80, 443, 8080, 8443, 3306, 5432])

if __name__ == "__main__":
    scan_interesting_targets()
