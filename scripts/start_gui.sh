#!/data/data/com.termux/files/usr/bin/bash

# 1. CLEANUP: Kill any old X11 or Burp processes
echo "[*] Cleaning up old sessions..."
pkill -f termux.x11
pkill -f java
rm -rf /tmp/.X11-unix
sleep 1

# 2. START X11: Launch the server in the background
echo "[*] Starting Termux-X11 Server..."
termux-x11 :1 >/dev/null 2>&1 &

# 3. GUI BRIDGE: Wake up the Termux-X11 Android App
echo "[*] Launching X11 GUI App..."
am start --user 0 -n com.termux.x11/com.termux.x11.MainActivity > /dev/null 2>&1
sleep 2

# 4. DEBIAN LAUNCH: Log in and run Burp Suite
echo "[*] Bridging to Debian and launching Burp Suite..."
proot-distro login debian --shared-tmp -- /bin/bash -c "export DISPLAY=:1 && java -Xmx1024M -jar /root/burpsuite_community.jar"
