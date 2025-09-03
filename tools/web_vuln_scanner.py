import requests
import time
from urllib.parse import urljoin
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen

def web_vuln_scanner_tool():
    clear_screen()
    console.print(Panel("[bold red]Web Vulnerability Scanner (Real)[/bold red]", border_style="red"))
    console.print("[bold yellow]DISCLAIMER: This tool only performs safe, non-destructive checks. For legal/educational use only.[/bold yellow]\n")

    target_url = Prompt.ask("[cyan]Enter the full URL to scan (e.g., http://testphp.vulnweb.com)[/cyan]")
    if not target_url.startswith('http'):
        target_url = 'http://' + target_url

    console.print(f"\n[cyan]Starting real scan on {target_url}...[/cyan]")
    report = {}
    try:
        # Check connectivity and headers
        resp = requests.get(target_url, timeout=10)
        headers = resp.headers
        report["Host Reachable"] = "[bold green]Yes[/bold green]"
        # Security headers
        security_headers = {
            "Content-Security-Policy": headers.get("Content-Security-Policy"),
            "X-Frame-Options": headers.get("X-Frame-Options"),
            "Strict-Transport-Security": headers.get("Strict-Transport-Security"),
        }
        report["Security Headers"] = "\n" + "\n".join([f"  - [bold]{h}:[/bold] {'[bold green]Present[/bold green]' if v else '[bold yellow]Missing[/bold yellow]'}" for h, v in security_headers.items()])

        # robots.txt
        robots_url = urljoin(target_url, '/robots.txt')
        robots_resp = requests.get(robots_url, timeout=5)
        if robots_resp.status_code == 200:
            report["robots.txt"] = f"[bold green]Found[/bold green] ({robots_url})"
        else:
            report["robots.txt"] = f"[bold yellow]Not Found[/bold yellow] ({robots_url})"

        # Directory listing
        dir_resp = requests.get(target_url.rstrip('/') + '/', timeout=5)
        if "Index of /" in dir_resp.text:
            report["Directory Listing"] = "[bold red]Enabled[/bold red] (Potential Info Leak)"
        else:
            report["Directory Listing"] = "[bold green]Not Enabled[/bold green]"

        # Basic SQL Injection test (on ?id=1)
        if '?' in target_url:
            sqli_url = target_url + "'"
            sqli_resp = requests.get(sqli_url, timeout=5)
            if "sql" in sqli_resp.text.lower() or "syntax" in sqli_resp.text.lower() or "mysql" in sqli_resp.text.lower():
                report["SQL Injection"] = "[bold red]Possible SQLi vulnerability detected![/bold red]"
            else:
                report["SQL Injection"] = "[bold green]No obvious SQLi detected[/bold green]"
        else:
            report["SQL Injection"] = "[yellow]No parameter to test[/yellow]"

        # Basic reflected XSS test (on ?q=)
        if '?q=' in target_url:
            xss_payload = '<script>alert(1)</script>'
            xss_url = target_url + xss_payload
            xss_resp = requests.get(xss_url, timeout=5)
            if xss_payload in xss_resp.text:
                report["Reflected XSS"] = "[bold red]Possible XSS vulnerability detected![/bold red]"
            else:
                report["Reflected XSS"] = "[bold green]No reflected XSS detected[/bold green]"
        else:
            report["Reflected XSS"] = "[yellow]No ?q= parameter to test[/yellow]"

        # Server version
        server_software = headers.get('Server', 'Unknown')
        report["Server Software"] = f"[cyan]{server_software}[/cyan]"

    except requests.exceptions.RequestException as e:
        console.print(f"\n[bold red]Could not connect to {target_url}. Error: {e}[/bold red]")
        Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
        return

    console.print("\n[green]Scan Complete.[/green]")
    final_report = "\n".join([f"[bold]{vuln}:[/bold] {result}" for vuln, result in report.items()])
    console.print(Panel(final_report, title=f"[bold yellow]Vulnerability Report for {target_url}[/bold yellow]", border_style="red"))
    console.print("\n[yellow]This tool only does safe, basic checks. For deep testing, use professional tools like Nikto, Nmap, or Burp Suite.[/yellow]")
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")