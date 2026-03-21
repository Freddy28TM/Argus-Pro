
import requests
import json
import os
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

def fetch_crt_sh(domain):
    """
    Step 1 of the Chart: Identify infrastructure via SSL Certificate Logs.
    This bypasses basic DNS hiding.
    """
    console.print(f"[bold cyan][*][/bold cyan] Querying Certificate Transparency (crt.sh) for: [bold]{domain}[/bold]")
    url = f"https://crt.sh/?q=%25.{domain}&output=json"
    try:
        # User-Agent is important to avoid getting blocked by crt.sh
        headers = {'User-Agent': 'Mozilla/5.0 (Argus-Pro/1.9; Mobile-Pentest)'}
        response = requests.get(url, headers=headers, timeout=25)
        
        if response.status_code == 200:
            data = response.json()
            # Extract common_names and filter unique subdomains
            subdomains = sorted(set([item['common_name'] for item in data]))
            return subdomains
        else:
            console.print(f"[yellow][!] crt.sh returned status: {response.status_code}[/yellow]")
    except Exception as e:
        console.print(f"[red][!] Error reaching crt.sh: {e}[/red]")
    return []

def get_google_dorks(domain):
    """
    Step 2 of the Chart: Manual Recon via Dorking.
    Automates the generation of OPPO-specific search queries.
    """
    dorks = [
        {"title": "Dev/Staging Portals", "query": f"site:{domain} inurl:dev | inurl:staging"},
        {"title": "Exposed Log Files", "query": f"site:{domain} filetype:log | filetype:txt \"error\""},
        {"title": "Config & Backup Leaks", "query": f"site:{domain} filetype:env | filetype:bak | filetype:sql"},
        {"title": "Management Interfaces", "query": f"site:{domain} intitle:\"login\" | intitle:\"admin\""},
        {"title": "ColorOS Specifics (OPPO)", "query": f"site:coloros.com | site:heytap.com"}
    ]
    
    table = Table(title=f"Google Dorks for {domain}", show_header=True, header_style="bold yellow")
    table.add_column("Category", style="cyan")
    table.add_column("Search Link (Click to open)", style="blue")

    for dork in dorks:
        link = f"https://www.google.com/search?q={dork['query'].replace(' ', '+')}"
        table.add_row(dork['title'], link)
    
    console.print(table)

def run_workflow(target_domain):
    """
    The Main Entry Point for Option 1 in main.py.
    """
    console.print(Panel(f"ACQUISITION RECON FLOW: {target_domain.upper()}", style="bold magenta"))
    
    # 1. Certificate Enumeration
    subs = fetch_crt_sh(target_domain)
    
    if not subs:
        console.print("[red][!] No subdomains found via crt.sh. Checking fallback...[/red]")
    else:
        # Create a display table for the findings
        results_table = Table(title=f"Discovered Assets: {target_domain}")
        results_table.add_column("ID", style="dim")
        results_table.add_column("Subdomain", style="green")

        for idx, sub in enumerate(subs[:20]): # Show top 20 for brevity
            results_table.add_row(str(idx+1), sub)
        
        console.print(results_table)
        console.print(f"[bold green][+][/bold green] Total Assets Found: {len(subs)}")

        # 2. Save results to data folder for the C# and C++ engines
        output_file = os.path.expanduser(f"~/Argus-Pro/data/{target_domain}_assets.json")
        with open(output_file, "w") as f:
            json.dump(subs, f)
        console.print(f"[*] Discovery saved to: {output_file}")

    # 3. Generate Dorks for manual "Deep Dive"
    get_google_dorks(target_domain)
    
    console.print("\n[bold cyan][*] Recon Phase Complete.[/bold cyan] Ready for Cloudflare Bypass or C# Audit.")
