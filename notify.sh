#!/bin/bash
WEBHOOK_URL="YOUR_DISCORD_WEBHOOK_URL_HERE"
MESSAGE="🚀 **Argus-Pro Sync Alert**\n**Device:** $(hostname)\n**Status:** Cloud Backup Successful\n**Timestamp:** $(date)"

curl -H "Content-Type: application/json" \
     -X POST \
     -d "{\"content\": \"$MESSAGE\"}" \
     $WEBHOOK_URL
