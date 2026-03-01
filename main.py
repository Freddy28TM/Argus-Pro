#!/usr/bin/env python3
import sys, os, platform
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Universal imports
from modules.reversing.handler import BinaryEngine
from modules.recon.universal_dissector import UniversalDissector
from modules.vuln.exploit_suggester import ExploitSuggester

console = Console()

def get_platform_info():
    """Detects environment and unlocks hidden capabilities for Desktop."""
    is_termux = "com.termux" in sys.executable or os.path.exists("/data/data/com.termux")
    sys_type = platform.system()
    return {"termux": is_termux, "os": sys_type}

def show_banner(env):
    mode = "MOBILE-MODE" if env["termux"] else "DESKTOP-ULTRA"
    banner = f"""[bold cyan]ARGUS-PRO v1.3 | {mode}[/bold cyan]"""
    console.print(Panel(banner, subtitle="Reboot-Persistent Edition", border_style="green"))

def main():
    env = get_platform_info()
    show_banner(env)
    
    # Desktop-Only Feature: Higher Threading / Raw Socket Unlock
    if not env["termux"]:
        console.print("[bold yellow][!] Desktop Detected: High-Speed Raw Sockets Unlocked.[/bold yellow]")

    while True:
        console.print("\n[bold]1.[/bold] L1-L7 Universal Stack Scan")
        console.print("[bold]2.[/bold] Binary Reversing (Clang Engine)")
        console.print("[bold]3.[/bold] Vulnerability & Exploit Suggester")
        console.print("[bold]4.[/bold] Exit")
        
        choice = Prompt.ask("Select Task", choices=["1", "2", "3", "4"])

        if choice == "1":
            target = Prompt.ask("Enter Target IP")
            dissector = UniversalDissector(target)
            dissector.run_full_stack()
            
        elif choice == "2":
            # Access the Clang logic we built
            engine = BinaryEngine()
            data = Prompt.ask("Hex Data")
            console.print(f"Decoded: [green]{engine.hex_decode(data)}[/green]")
            
        elif choice == "3":
            banner = Prompt.ask("Paste Service Banner (e.g. Apache 2.4.49)")
            suggester = ExploitSuggester()
            console.print(suggester.suggest(banner))

        elif choice == "4":
            break

if __name__ == "__main__":
    main()
