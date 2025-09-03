import whois
import socket
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    clear_screen()
    print_banner("WHOIS Lookup")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold blue]WHOIS Lookup Tool[/bold blue]", border_style="blue"))
    console.print("[yellow]This tool performs WHOIS lookups to get domain registration information.[/yellow]\n")
    
    domain = Prompt.ask("[cyan]Enter a domain name to lookup (e.g., google.com, example.com)[/cyan]")
    
    # Remove www. if present
    if domain.startswith('www.'):
        domain = domain[4:]
    
    try:
        console.print(f"[cyan]Looking up WHOIS information for: {domain}[/cyan]")
        
        # First check if domain resolves
        try:
            ip = socket.gethostbyname(domain)
            console.print(f"[green]✓ Domain resolves to IP: {ip}[/green]")
        except socket.gaierror:
            console.print(f"[yellow]⚠ Domain does not resolve to an IP (might not exist or DNS not configured)[/yellow]")
        
        # Perform WHOIS lookup
        w = whois.whois(domain)
        
        # Check if we got valid data
        if w.domain_name is None and w.registrar is None:
            console.print(f"[red]✗ No WHOIS information found for {domain}[/red]")
            console.print("[yellow]This could mean:[/yellow]")
            console.print("  - The domain doesn't exist or isn't registered")
            console.print("  - The domain is not publicly registered")
            console.print("  - WHOIS data is private/protected")
            console.print("  - The WHOIS server is not responding")
            console.print("[cyan]Try a different domain like 'google.com' or 'example.com'[/cyan]")
            return
        
        # Format the information
        info_lines = []
        
        if w.domain_name:
            domain_names = w.domain_name if isinstance(w.domain_name, list) else [w.domain_name]
            info_lines.append(f"[bold]Domain Name(s):[/bold] {', '.join(str(d) for d in domain_names)}")
        
        if w.registrar:
            info_lines.append(f"[bold]Registrar:[/bold] {w.registrar}")
        
        if w.creation_date:
            creation_dates = w.creation_date if isinstance(w.creation_date, list) else [w.creation_date]
            info_lines.append(f"[bold]Creation Date:[/bold] {creation_dates[0].strftime('%Y-%m-%d') if hasattr(creation_dates[0], 'strftime') else creation_dates[0]}")
        
        if w.expiration_date:
            expiration_dates = w.expiration_date if isinstance(w.expiration_date, list) else [w.expiration_date]
            info_lines.append(f"[bold]Expiration Date:[/bold] {expiration_dates[0].strftime('%Y-%m-%d') if hasattr(expiration_dates[0], 'strftime') else expiration_dates[0]}")
        
        if w.name_servers:
            ns_list = w.name_servers if isinstance(w.name_servers, list) else [w.name_servers]
            info_lines.append(f"[bold]Name Servers:[/bold] {', '.join(str(ns) for ns in ns_list)}")
        
        if w.registrant:
            info_lines.append(f"[bold]Registrant:[/bold] {w.registrant}")
        
        if w.admin:
            info_lines.append(f"[bold]Admin Contact:[/bold] {w.admin}")
        
        if w.tech:
            info_lines.append(f"[bold]Tech Contact:[/bold] {w.tech}")
        
        if w.status:
            status_list = w.status if isinstance(w.status, list) else [w.status]
            info_lines.append(f"[bold]Status:[/bold] {', '.join(str(s) for s in status_list)}")
        
        info = "\n".join(info_lines)
        console.print(Panel(info, title="[bold yellow]WHOIS Information[/bold yellow]", border_style="blue"))
        
    except Exception as e:
        console.print(f"[red]Could not perform WHOIS lookup: {e}[/red]")
        console.print("[yellow]Try a different domain or check if the domain exists.[/yellow]")
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
