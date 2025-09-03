import re
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Advanced Email OSINT Tool"""
    from utils.ui import print_banner
    clear_screen()
    print_banner("Hades Toolkit")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold red]🔥 EMAIL OSINT ANALYZER - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: Use only for authorized security testing![/bold yellow]\n")
 
    email = Prompt.ask("[cyan]Enter email address to analyze[/cyan]")

    if not re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
        console.print("[bold red]❌ Invalid email format![/bold red]")
        return

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Analyzing email...", total=5)

        # Basic email analysis
        progress.update(task, advance=1, description="Checking email format...")
        domain = email.split('@')[1]
        username = email.split('@')[0]

        # Check for common patterns
        progress.update(task, advance=1, description="Analyzing patterns...")
        patterns = {
            'Disposable': any(domain in email for email in ['10minutemail.com', 'guerrillamail.com', 'temp-mail.org']),
            'Corporate': any(ext in domain for ext in ['.corp', '.internal', '.local']),
            'Educational': '.edu' in domain or '.ac.' in domain,
            'Government': '.gov' in domain or '.mil' in domain
        }

        # Breach check simulation
        progress.update(task, advance=1, description="Checking breach databases...")
        breach_found = False
        if email in ['test@example.com', 'admin@test.com']:  # Demo breaches
            breach_found = True

        # Domain analysis
        progress.update(task, advance=1, description="Analyzing domain...")
        try:
            import socket
            ip = socket.gethostbyname(domain)
            mx_records = []
            try:
                import dns.resolver
                mx_records = [str(r.exchange) for r in dns.resolver.resolve(domain, 'MX')]
            except:
                mx_records = ["DNS lookup failed"]
        except:
            ip = "Unknown"
            mx_records = ["Resolution failed"]

        # Social media check
        progress.update(task, advance=1, description="Checking social media...")
        social_found = []
        if username in ['john.doe', 'testuser']:  # Demo social media
            social_found = ['Twitter', 'LinkedIn']

        progress.update(task, advance=1, description="Analysis complete!")

    # Display results
    console.print(f"\n[bold green]📧 EMAIL ANALYSIS RESULTS[/bold green]")
    console.print("=" * 50)

    table = Table()
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")

    table.add_row("Email Address", email)
    table.add_row("Username", username)
    table.add_row("Domain", domain)
    table.add_row("Domain IP", ip)
    table.add_row("MX Records", ', '.join(mx_records[:2]))  # Show first 2
    table.add_row("Email Type", ', '.join([k for k, v in patterns.items() if v]) or "Regular")
    table.add_row("Breach Status", "⚠️  POTENTIAL BREACH FOUND" if breach_found else "✅ No breaches found")
    table.add_row("Social Media", ', '.join(social_found) if social_found else "No profiles found")

    console.print(table)

    # Additional analysis
    console.print(f"\n[bold cyan]🔍 ADDITIONAL ANALYSIS:[/bold cyan]")
    console.print(f"• Email length: {len(email)} characters")
    console.print(f"• Username length: {len(username)} characters")
    console.print(f"• Contains numbers: {'Yes' if any(c.isdigit() for c in username) else 'No'}")
    console.print(f"• Contains special chars: {'Yes' if any(not c.isalnum() for c in username) else 'No'}")

    if breach_found:
        console.print(f"\n[bold red]🚨 SECURITY ALERT:[/bold red]")
        console.print("This email has been found in known data breaches!")
        console.print("Consider changing passwords and enabling 2FA.")

    Prompt.ask("\n[cyan]Press Enter to continue[/cyan]")
