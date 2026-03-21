#!/usr/bin/env python3
import sys, os, platform, ctypes, subprocess, datetime
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table

# --- MODULE IMPORTS ---
try:
    from modules.recon.acquisition_hunter import run_workflow as acquisition_flow
    from modules.recon.cloudflare_bypass import run_bypass
    from modules.recon.watchdog import monitor_targets
    from modules.vuln.payload_gen import generate_oppo_payloads
    from scripts.report_gen import generate_h1_report
except ImportError as e:
    print(f"[!] Critical Import Error: {e}")

# --- INITIALIZE UI ---
console = Console()

# --- PATH CONFIGURATION ---
BASE_DIR = os.path.expanduser("~/Argus-Pro")
LIB_PATH = os.path.join(BASE_DIR, "lib/fast_scan.so")
CS_EXE = "/root/Argus-Pro/bin/cloud_audit.exe" # Path inside Debian
LOG_FILE = os.path.join(BASE_DIR, "reports/session_log.txt")

# --- LOAD POLYGLOT ENGINE (C++ SNIPER) ---
try:
    fast_lib = ctypes.CDLL(LIB_PATH)
    CPP_READY = True
except Exception:
    CPP_READY = False

# --- SYSTEM FUNCTIONS ---

def log_finding(category, data):
    """Saves every discovery for the HackerOne Report."""
    os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open(LOG_FILE, "a") as f:
        f.write(f"[{timestamp}] [{category}] {data}\n")
    console.print(f"[bold green][LOG][/bold green] Entry synced to session_log.txt")

def run_diagnostic():
    """Verify April 1st Readiness."""
    table = Table(title="Argus-Pro v2.2 | Diagnostic Dashboard")
    table.add_column("Engine", style="cyan")
    table.add_column("Status", style="bold")
    
    table.add_row("C++ Sniper (.so)", "[green]READY[/green]" if CPP_READY else "[red]OFFLINE[/red]")
    
    cs_path = os.path.expanduser("~/../usr/var/lib/proot-distro/installed-rootfs/debian/root/Argus-Pro/bin/cloud_audit.exe")
    table.add_row("C# Consultant (.exe)", "[green]READY[/green]" if os.path.exists(cs_path) else "[red]MISSING[/red]")
    
    x11_active = os.path.exists("/tmp/.X11-unix/X1")
    table.add_row("X11 GUI Bridge", "[green]ACTIVE[/green]" if x11_active else "[yellow]STANDBY[/yellow]")
    
    console.print(table)

def main():
    banner = "[bold cyan]ARGUS-PRO v2.2 | OPPO CAMPAIGN MASTER[/bold cyan]"
    console.print(Panel(banner, subtitle="Recon | Bypass | Audit | Exploit | Report", expand=False))

    while True:
        console.print("\n[bold yellow]BATTLE STATION MENU[/bold yellow]")
        console.print("[bold]1.[/bold] [cyan]Acquisition Recon[/cyan] (OPPO/HeyTap Mapping)")
        console.print("[bold]2.[/bold] [magenta]Cloudflare Bypass[/magenta] (Origin IP Discovery)")
        console.print("[bold]3.[/bold] [green]Enterprise Cloud Audit[/green] (C# / Oracle / AWS)")
        console.print("[bold]4.[/bold] [blue]L1-L7 Fast Probe[/blue] (C++ Sniper Engine)")
        console.print("[bold]5.[/bold] [yellow]Payload Generator[/yellow] (IDOR/XSS for OPPO)")
        console.print("[bold]6.[/bold] [red]Launch Burp Suite[/red] (X11 GUI Bridge)")
        console.print("[bold]7.[/bold] [white]System Diagnostic[/white] (Health Check)")
        console.print("[bold]8.[/bold] [bold green]HackerOne Reporter[/bold green] (Professional Template)")
        console.print("[bold]9.[/bold] [bold red]OPPO Watchdog[/bold red] (24/7 Asset Monitor)")
        console.print("[bold]0.[/bold] Exit")

        choice = Prompt.ask("Select Task", choices=["1", "2", "3", "4", "5", "6", "7", "8", "9", "0"])

        if choice == "1":
            target = Prompt.ask("Enter Target Domain", default="oppo.com")
            acquisition_flow(target)
            log_finding("RECON", f"Mapped infrastructure for {target}")

        elif choice == "2":
            target = Prompt.ask("Enter Domain for Bypass")
            origins = run_bypass(target)
            if origins:
                log_finding("BYPASS", f"Origin IPs for {target}: {origins}")

        elif choice == "3":
            target = Prompt.ask("Enter Cloud Asset/Bucket")
            # Execute C# Module inside Debian
            subprocess.run(["proot-distro", "login", "debian", "--", "mono", CS_EXE, target])
            log_finding("CLOUD_AUDIT", f"C# Audit performed on: {target}")

        elif choice == "4":
            if CPP_READY:
                target = Prompt.ask("Enter Target IP")
                fast_lib.fast_scan(target.encode())
                log_finding("CPP_SCAN", f"L1-L7 Scan on {target}")
            else:
                console.print("[red]Error: C++ Engine not compiled or linked.[/red]")

        elif choice == "5":
            generate_oppo_payloads()

        elif choice == "6":
            os.system(f"{BASE_DIR}/scripts/start_gui.sh")

        elif choice == "7":
            run_diagnostic()

        elif choice == "8":
            generate_h1_report()

        elif choice == "9":
            target = Prompt.ask("Watch which domain?", default="oppo.com")
            monitor_targets(target)

        elif choice == "0":
            console.print("[bold red]Argus-Pro v2.2 Shutting Down. Go get that bounty, Freddy![/bold red]")
            break

if __name__ == "__main__":
    main()
