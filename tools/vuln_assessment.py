import requests
import re
import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Extreme Level Vulnerability Assessment Tool"""
    clear_screen()
    console.print(Panel("[bold red]🔥 VULNERABILITY ASSESSMENT - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: This tool performs security assessments. Use only on authorized targets![/bold yellow]\n")
    
    target = Prompt.ask("[cyan]Enter target URL (e.g., http://example.com)[/cyan]")
    
    if not target.startswith(('http://', 'https://')):
        target = 'http://' + target
    
    try:
        with console.status("[bold green]Performing comprehensive vulnerability assessment...[/bold green]", spinner="dots") as status:
            time.sleep(2)
            
            # Basic web server info
            console.print("\n[bold cyan]🔍 PHASE 1: Web Server Analysis[/bold cyan]")
            try:
                response = requests.get(target, timeout=10)
                server = response.headers.get('Server', 'Unknown')
                console.print(f"[green]Server:[/green] [cyan]{server}[/cyan]")
                console.print(f"[green]Status Code:[/green] [cyan]{response.status_code}[/cyan]")
                console.print(f"[green]Content-Type:[/green] [cyan]{response.headers.get('Content-Type', 'Unknown')}[/cyan]")
            except requests.exceptions.RequestException as e:
                console.print(f"[red]✗ Connection failed: {e}[/red]")
                return
            
            # Security headers check
            console.print("\n[bold cyan]🔍 PHASE 2: Security Headers Analysis[/bold cyan]")
            security_headers = {
                'X-Frame-Options': 'Clickjacking protection',
                'X-Content-Type-Options': 'MIME type sniffing protection',
                'X-XSS-Protection': 'XSS protection',
                'Strict-Transport-Security': 'HTTPS enforcement',
                'Content-Security-Policy': 'Content injection protection',
                'Referrer-Policy': 'Referrer information control'
            }
            
            missing_headers = []
            present_headers = []
            
            for header, description in security_headers.items():
                if header in response.headers:
                    present_headers.append(f"[green]✓[/green] {header}: {description}")
                else:
                    missing_headers.append(f"[red]✗[/red] {header}: {description}")
            
            if present_headers:
                console.print(Panel(
                    "\n".join(present_headers),
                    title="[bold green]Present Security Headers[/bold green]", border_style="green"
                ))
            
            if missing_headers:
                console.print(Panel(
                    "\n".join(missing_headers),
                    title="[bold red]Missing Security Headers[/bold red]", border_style="red"
                ))
            
            # Common vulnerability checks
            console.print("\n[bold cyan]�� PHASE 3: Common Vulnerability Checks[/bold cyan]")
            vulnerabilities = []
            
            # Check for directory listing
            try:
                dir_response = requests.get(target.rstrip('/') + '/', timeout=5)
                if 'Index of' in dir_response.text or 'directory listing' in dir_response.text.lower():
                    vulnerabilities.append("Directory listing enabled - Information disclosure")
            except:
                pass
            
            # Check for common vulnerable files
            vulnerable_files = ['/admin.php', '/login.php', '/config.php', '/backup.sql', '/.env', '/wp-admin/', '/phpmyadmin/']
            for file in vulnerable_files:
                try:
                    file_response = requests.get(target.rstrip('/') + file, timeout=3)
                    if file_response.status_code == 200:
                        vulnerabilities.append(f"Potentially sensitive file accessible: {file}")
                except:
                    pass
            
            # SQL injection basic check
            sql_payloads = ["'", "\"", "1' OR '1'='1", "1\" OR \"1\"=\"1"]
            for payload in sql_payloads:
                try:
                    sql_response = requests.get(target + payload, timeout=3)
                    if 'sql' in sql_response.text.lower() or 'mysql' in sql_response.text.lower():
                        vulnerabilities.append("Potential SQL injection vulnerability detected")
                        break
                except:
                    pass
            
            if vulnerabilities:
                console.print(Panel(
                    "\n".join([f"[red]⚠️[/red] {vuln}" for vuln in vulnerabilities]),
                    title="[bold red]Potential Vulnerabilities[/bold red]", border_style="red"
                ))
            else:
                console.print("[green]✓ No common vulnerabilities detected[/green]")
            
            # Recommendations
            console.print("\n[bold cyan]🔍 PHASE 4: Security Recommendations[/bold cyan]")
            recommendations = [
                "Implement HTTPS if not already in use",
                "Add security headers (CSP, HSTS, X-Frame-Options, etc.)",
                "Disable directory listing",
                "Use parameterized queries to prevent SQL injection",
                "Regular security audits and penetration testing",
                "Keep software and dependencies updated"
            ]
            
            console.print(Panel(
                "\n".join([f"[cyan]•[/cyan] {rec}" for rec in recommendations]),
                title="[bold yellow]Security Recommendations[/bold yellow]", border_style="yellow"
            ))
            
        console.print("\n[bold green]✓ Vulnerability assessment completed![/bold green]")
        
    except Exception as e:
        console.print(f"[bold red]✗ Assessment failed: {e}[/bold red]")
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
