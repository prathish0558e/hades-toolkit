import requests
import sys
import os
import concurrent.futures
from urllib.parse import urlparse

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui import console
from rich.prompt import Prompt
from rich.panel import Panel
from rich.progress import Progress, SpinnerColumn, TextColumn

# A common list of subdomains. For a real-world tool, this would be a much larger file.
COMMON_SUBDOMAINS = [
    "www", "mail", "ftp", "localhost", "webmail", "smtp", "pop", "ns1", "ns2", "admin",
    "api", "dev", "test", "staging", "beta", "shop", "blog", "m", "mobile", "support",
    "help", "docs", "portal", "cpanel", "webdisk", "autodiscover", "owa", "vpn", "secure",
    "login", "signin", "signup", "register", "status", "dashboard", "app", "store",
    "files", "assets", "static", "cdn", "media", "images", "img", "video", "vids",
    "remote", "git", "svn", "db", "sql", "mysql", "mongo", "redis", "backup", "cloud",
    "sso", "auth", "oauth", "identity", "id", "account", "accounts", "billing", "payment",
    "payments", "forum", "community", "chat", "jobs", "careers", "hr", "internal",
    "intranet", "extranet", "partner", "partners", "affiliate", "affiliates", "devops",
    "jenkins", "ci", "cd", "jira", "confluence", "wiki", "analytics", "stats", "metrics",
    "tracking", "events", "log", "logs", "monitor", "monitoring", "news", "press",
    "investors", "ir", "about", "contact", "us", "uk", "au", "ca", "de", "fr", "jp"
]

def check_subdomain(domain, subdomain):
    """Checks if a single subdomain exists."""
    url = f"http://{subdomain}.{domain}"
    try:
        # Use a HEAD request for speed, we only need the status code
        requests.head(url, timeout=3, allow_redirects=True)
        return url
    except requests.ConnectionError:
        return None
    except Exception:
        return None

def run():
    """Main function to run the Subdomain Scanner."""
    console.print(Panel("[bold green]🌐 Subdomain Scanner 🌐[/bold green]", subtitle="[cyan]Discover hidden subdomains of a target[/cyan]"))

    target_domain = Prompt.ask("[yellow]Enter the target domain (e.g., google.com)[/yellow]").strip()
    
    if not target_domain or '.' not in target_domain:
        console.print("[bold red]Invalid domain format.[/bold red]")
        return

    # Clean the input
    parsed_domain = urlparse(f"//{target_domain}").netloc or target_domain
    
    console.print(f"\n[cyan]Scanning [bold]{parsed_domain}[/bold] for subdomains...[/cyan]")
    
    found_subdomains = []
    
    with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"), transient=True) as progress:
        task = progress.add_task("Scanning...", total=len(COMMON_SUBDOMAINS))
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=50) as executor:
            future_to_sub = {executor.submit(check_subdomain, parsed_domain, sub): sub for sub in COMMON_SUBDOMAINS}
            
            for future in concurrent.futures.as_completed(future_to_sub):
                result = future.result()
                if result:
                    console.print(f"[bold green][+] Found: {result}[/bold green]")
                    found_subdomains.append(result)
                progress.update(task, advance=1)

    if found_subdomains:
        console.print(f"\n[bold green]✅ Scan Complete. Found {len(found_subdomains)} subdomains.[/bold green]")
    else:
        console.print("\n[bold yellow]ℹ️ Scan Complete. No subdomains found from the common list.[/bold yellow]")

if __name__ == "__main__":
    run()
