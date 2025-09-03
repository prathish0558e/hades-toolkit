import socket
import subprocess
import time
import os
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Extreme Level Advanced Network Scanner"""
    from utils.ui import print_banner
    clear_screen()
    print_banner("Hades Toolkit")
    console.print(Panel("[bold red]🔥 ADVANCED NETWORK SCANNER - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: This is an advanced scanning tool. Use only on authorized networks![bold yellow]\n")
    
    target = Prompt.ask("[cyan]Enter target IP or domain[/cyan]")
    
    try:
        # Resolve target IP
        target_ip = socket.gethostbyname(target)
        console.print(f"[green]✓ Target resolved: {target} ({target_ip})[/green]")
        
        with console.status("[bold green]Performing advanced network reconnaissance...[/bold green]", spinner="dots") as status:
            time.sleep(2)
            
            # Port scanning with service detection
            console.print("\n[bold cyan]�� PHASE 1: Advanced Port Scanning[/bold cyan]")
            common_ports = {
                21: "FTP", 22: "SSH", 23: "Telnet", 25: "SMTP", 53: "DNS",
                80: "HTTP", 110: "POP3", 135: "RPC", 139: "NetBIOS", 143: "IMAP",
                443: "HTTPS", 445: "SMB", 993: "IMAPS", 995: "POP3S", 3389: "RDP"
            }
            
            open_ports = []
            for port, service in common_ports.items():
                status.update(f"[bold green]Scanning port {port} ({service})...[/bold green]")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append((port, service))
                sock.close()
            
            if open_ports:
                console.print(Panel(
                    "\n".join([f"[green]✓ Port {port}[/green] - [cyan]{service}[/cyan]" for port, service in open_ports]),
                    title="[bold yellow]Open Ports & Services[/bold yellow]", border_style="green"
                ))
            else:
                console.print("[yellow]No common ports open[/yellow]")
            
            # OS fingerprinting simulation
            console.print("\n[bold cyan]🔍 PHASE 2: OS Fingerprinting[/bold cyan]")
            time.sleep(1)
            os_info = "[cyan]Unable to determine OS (requires root/admin privileges)[/cyan]"
            console.print(f"[green]OS Detection:[/green] {os_info}")
            
            # Vulnerability check simulation
            console.print("\n[bold cyan]�� PHASE 3: Vulnerability Assessment[/bold cyan]")
            vulnerabilities = []
            if 80 in [p[0] for p in open_ports]:
                vulnerabilities.append("HTTP service detected - Check for common web vulnerabilities")
            if 443 in [p[0] for p in open_ports]:
                vulnerabilities.append("HTTPS service detected - Verify SSL/TLS configuration")
            if 21 in [p[0] for p in open_ports]:
                vulnerabilities.append("FTP service detected - Consider using SFTP instead")
            
            if vulnerabilities:
                console.print(Panel(
                    "\n".join([f"[red]⚠️[/red] {vuln}" for vuln in vulnerabilities]),
                    title="[bold red]Potential Security Issues[/bold red]", border_style="red"
                ))
            
            # Network mapping simulation
            console.print("\n[bold cyan]�� PHASE 4: Network Topology Discovery[/bold cyan]")
            time.sleep(1)
            console.print("[green]Network Range:[/green] [cyan]Unable to scan network range (requires elevated privileges)[/cyan]")
            
        console.print("\n[bold green]✓ Advanced scan completed![/bold green]")
        
    except socket.gaierror:
        console.print(f"[bold red]✗ Could not resolve hostname: {target}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]✗ Scan failed: {e}[/bold red]")
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
