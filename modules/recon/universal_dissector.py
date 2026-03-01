import socket
from scapy.all import *
from rich.console import Console

console = Console()

class UniversalDissector:
    def __init__(self, target):
        self.target = target

    def layer2_3_check(self):
        """ARP and ICMP: Finding the hardware and network route."""
        console.print("[bold cyan]Checking L2/L3 (Data Link & Network)...[/bold cyan]")
        conf.verb = 0
        ans, unans = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=self.target), timeout=2)
        for snd, rcv in ans:
            console.print(f"[green][+] MAC Address Found: {rcv.hwsrc}[/green]")
        
    def layer4_check(self, port):
        """TCP/UDP: Checking the Transport Layer."""
        try:
            s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            s.settimeout(1)
            result = s.connect_ex((self.target, port))
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
        
        # Banner Grabbing for more detail
        try:
            with socket.socket() as s:
                s.settimeout(2)
                s.connect((self.target, port))
                banner = s.recv(1024).decode(errors='ignore').strip()
                if banner:
                    console.print(f"   [white]Banner: {banner}[/white]")
        except:
            pass

    def run_full_stack(self, ports=[22, 80, 443, 3306]):
        self.layer2_3_check()
        for p in ports:
            if self.layer4_check(p):
                self.layer7_protocol_id(p)
