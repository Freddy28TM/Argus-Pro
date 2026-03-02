#!/bin/bash
TARGET_DOMAIN="oppo.com"
# We test the addresses you just found
IP_LIST=("129.227.29.0" "106.3.18.178" "119.147.175.93")

for ip in "${IP_LIST[@]}"; do
    echo "[*] Testing IP: $ip for $TARGET_DOMAIN bypass..."
    # We ask the IP directly for the website's content
    # -k (ignore SSL errors), -H (Manual Host Header), -I (Show Headers only)
    curl -I -k -s -H "Host: $TARGET_DOMAIN" "https://$ip" | grep -E "Server|HTTP/|cloudflare"
    echo "-----------------------------------"
done
