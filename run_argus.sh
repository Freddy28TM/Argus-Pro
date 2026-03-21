#!/data/data/com.termux/files/usr/bin/sh
# 1. Prevent Android from sleeping the process
termux-wake-lock

# 2. Ensure Cron is active for your sync/notify scripts
pgrep crond > /dev/null || crond

# 3. Clean up temporary logs from previous runs
rm -f ~/Argus-Pro/logs/session.tmp

# 4. Launch the main UI
python3 ~/Argus-Pro/main.py
