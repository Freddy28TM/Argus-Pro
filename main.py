#!/usr/bin/env python3
import sys, os, platform
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

# Universal imports
from modules.recon.universal_dissector import UniversalDissector
from modules.reversing.handler import BinaryEngine
from modules.vuln.exploit_suggester import ExploitSuggester

console = Console()

def get_platform_info():
    is_termux = "com.termux" in sys.executable or os.path.exists("/data/data/com.termux")
    return {"termux": is_termux, "os": platform.system()}

def main():
    env = get_platform_info()
    banner = "[bold cyan]ARGUS-PRO v1.5 | REBOOT-PERSISTENT[/bold cyan]"
    console.print(Panel(banner, subtitle=f"Mode: {'Mobile' if env['termux'] else 'Desktop'}", border_style="green"))

    while True:
        console.print("\n[bold]1.[/bold] L1-L7 Universal Stack Scan")
        console.print("[bold]2.[/bold] Binary Reversing (Hex Decoder)")
        console.print("[bold]3.[/bold] Exploit Suggester")
        console.print("[bold]4.[/bold] Exit")
        
        choice = Prompt.ask("Select Task", choices=["1", "2", "3", "4"])

        if choice == "1":
            target = Prompt.ask("Enter Target IP")
            dissector = UniversalDissector(target)
            dissector.run_full_stack()
        elif choice == "2":
            engine = BinaryEngine()
            data = Prompt.ask("Enter Hex Data")
            console.print(f"Decoded: [green]{engine.hex_decode(data)}[/green]")
        elif choice == "3":
            banner_text = Prompt.ask("Paste Service Banner")
            suggester = ExploitSuggester()
            console.print(suggester.suggest(banner_text))
        elif choice == "4":
            break

if __name__ == "__main__":
    main()
