import time
import os
from rich.console import Console

console = Console()

def monitor_targets(domain):
    """Background monitor to check when a new acquisition goes 'Live'."""
    console.print(f"[bold yellow][!][/bold yellow] Watchdog started for: {domain}")
    known_assets = []
    
    # Load previous findings to avoid duplicates
    report_path = os.path.expanduser(f"~/Argus-Pro/data/{domain}_assets.json")
    if os.path.exists(report_path):
        with open(report_path, "r") as f:
            import json
            known_assets = json.load(f)

    try:
        while True:
            # Here you would trigger a fresh 'fetch_crt_sh'
            # For brevity, we simulate finding a 'new' dev portal
            new_find = f"dev-internal-{int(time.time())}.{domain}"
            
            console.print(f"[bold green][+ WATCHDOG][/bold green] New Asset Detected: {new_find}")
            # Sound alert for Termux
            os.system("termux-tts-speak 'New OPPO asset detected'") 
            
            # Log it immediately
            with open(os.path.expanduser("~/Argus-Pro/reports/session_log.txt"), "a") as l:
                l.write(f"[{time.ctime()}] [WATCHDOG] NEW_ASSET: {new_find}\n")
            
            break # Remove break for 24/7 monitoring
            time.sleep(3600) # Check every hour
    except KeyboardInterrupt:
        console.print("[red]Watchdog stopped.[/red]")
