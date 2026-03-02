import socket
import scapy.config
from scapy.all import *
from rich.console import Console

# --- MOBILE PERMISSION FIX ---
# This tells Scapy to use Layer 3 Raw Sockets which sometimes 
# works better in Termux environments than Layer 2.
try:
    conf.L3socket = L3RawSocket
except:
    pass
# -----------------------------

console = Console()

class UniversalDissector:
    def __init__(self, target):
        self.target = target

    def layer2_3_check(self):
        """ARP and ICMP: Finding the hardware and network route."""
        console.print("[bold cyan][L2/L3] Probing Network Path...[/bold cyan]")
        conf.verb = 0
        try:
            # We use a standard ICMP ping if ARP (Layer 2) is blocked by Android
            ans, unans = sr(IP(dst=self.target)/ICMP(), timeout=2, verbose=0)
            if ans:
                console.print(f"[green][+] Target {self.target} is UP and Responding[/green]")
        except PermissionError:
            console.print("[yellow][!] L2 Raw Sockets blocked. Skipping MAC discovery (Non-Root).[/yellow]")
        
    def layer4_check(self, port):
        """TCP/UDP: Checking the Transport Layer using Standard Sockets."""
        try:
            # Using socket.socket instead of Scapy for L4 to bypass PermissionError
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
            s.close()
            return result == 0
        except:
            return False

    def layer7_protocol_id(self, port):
        """Application Layer: Identifying the service protocol."""
        protocols = {
            21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP",
            53: "DNS", 80: "HTTP", 443: "HTTPS", 3306: "MySQL",
            5432: "PostgreSQL", 8080: "HTTP-Proxy"
        }
        
        service = protocols.get(port, "Unknown Service")
        console.print(f"[bold yellow][L7] Port {port}: {service}[/bold yellow]")
        
        # Banner Grabbing
        try:
            with socket.socket() as s:
                s.settimeout(2)
                s.connect((self.target, port))
                banner = s.recv(1024).decode(errors='ignore').strip()
                if banner:
                    console.print(f"   [white]Banner: {banner}[/white]")
        except:
            pass

    def run_full_stack(self, ports=[21, 22, 80, 443, 8080]):
        self.layer2_3_check()
        for p in ports:
            if self.layer4_check(p):
                self.layer7_protocol_id(p)
