#!/bin/bash

# --- CONFIGURATION ---
# Replace the URL below with your actual Discord Webhook URL
WEBHOOK_URL="https://discord.com/api/webhooks/YOUR_ACTUAL_TOKEN_HERE"
# ---------------------

# Accept an optional message as an argument, or use a default
CUSTOM_MSG=$1
DEVICE_NAME=$(hostname)
TIMESTAMP=$(date '+%Y-%m-%d %H:%M:%S')

if [ -z "$CUSTOM_MSG" ]; then
    MESSAGE="🚀 **Argus-Pro: Cloud Sync Successful**\n**Device:** \`$DEVICE_NAME\`\n**Time:** \`$TIMESTAMP\`\nCheck your GitHub for the latest Oppo scan logs."
else
    MESSAGE="🔔 **Argus-Pro Alert:**\n$CUSTOM_MSG\n**Time:** \`$TIMESTAMP\`"
fi

# Send to Discord
curl -H "Content-Type: application/json" \
     -X POST \
     -d "{\"content\": \"$MESSAGE\"}" \
     "$WEBHOOK_URL"
