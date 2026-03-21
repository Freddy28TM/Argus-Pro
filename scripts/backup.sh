#!/bin/bash
cd ~/Argus-Pro
# Add everything, including the new OPPO files and the lib/ folders
git add . 
git commit -m "OPPO Campaign Prep: $(date)"
git push origin main
echo "[*] Full Project Backup Complete."
