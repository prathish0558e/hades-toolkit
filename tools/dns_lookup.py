import socket
import dns.resolver
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    clear_screen()
    print_banner("DNS Lookup")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold blue]DNS Lookup Tool[/bold blue]", border_style="blue"))
    console.print("[yellow]This tool performs DNS lookups to resolve domain names to IP addresses and vice versa.[/yellow]\n")
    
    domain = Prompt.ask("[cyan]Enter a domain name or IP address to lookup[/cyan]")
    
    try:
        # Try to resolve domain to IP
        try:
            ip = socket.gethostbyname(domain)
            console.print(f"[green]Domain {domain} resolves to IP: {ip}[/green]")
        except socket.gaierror:
            console.print(f"[red]Could not resolve {domain} to IP[/red]")
        
        # Try reverse DNS lookup if it's an IP
        try:
            hostname = socket.gethostbyaddr(domain)[0]
            console.print(f"[green]IP {domain} resolves to hostname: {hostname}[/green]")
        except socket.herror:
            console.print(f"[red]Could not reverse resolve {domain}[/red]")
        
        # DNS records lookup
        try:
            answers = dns.resolver.resolve(domain, 'A')
            console.print(f"[green]A records for {domain}:[/green]")
            for rdata in answers:
                console.print(f"  - {rdata}")
        except Exception as e:
            console.print(f"[red]Could not fetch A records: {e}[/red]")
            
    except Exception as e:
        console.print(f"[red]An error occurred: {e}[/red]")
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
