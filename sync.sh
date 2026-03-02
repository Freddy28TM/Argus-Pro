#!/bin/bash
cd ~/Argus-Pro
git add .
git commit -m "Automated Sync: $(date)"
git push origin main

# If the push was successful, notify Discord
if [ $? -eq 0 ]; then
    ./notify.sh
fi

# --- OPPO ASSET WATCHER ---
echo "--- NEW SUBDOMAINS FOUND ---" > ~/Argus-Pro/data/oppo/diff.txt
subfinder -d oppo.com | grep -v -f ~/Argus-Pro/data/oppo/subdomains.txt >> ~/Argus-Pro/data/oppo/diff.txt

# If diff.txt is not empty, notify Discord
if [ -s ~/Argus-Pro/data/oppo/diff.txt ]; then
    ./notify.sh "New Oppo assets detected! Check GitHub logs."
    # Update main list so we don't get alerted for the same ones twice
    cat ~/Argus-Pro/data/oppo/diff.txt >> ~/Argus-Pro/data/oppo/subdomains.txt
fi
