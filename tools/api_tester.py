import requests
import json
import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """REST API Testing Tool"""
    clear_screen()
    console.print(Panel("[bold red]🔥 REST API TESTER - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: Use only on authorized APIs![/bold yellow]\n")

    console.print("[bold cyan]Select HTTP method:[/bold cyan]")
    console.print("1. GET")
    console.print("2. POST")
    console.print("3. PUT")
    console.print("4. DELETE")
    console.print("5. PATCH")
    console.print("6. HEAD")
    console.print("7. OPTIONS")

    method_choice = Prompt.ask("[cyan]Choose method[/cyan]", choices=['1', '2', '3', '4', '5', '6', '7'])

    methods = {
        '1': 'GET',
        '2': 'POST',
        '3': 'PUT',
        '4': 'DELETE',
        '5': 'PATCH',
        '6': 'HEAD',
        '7': 'OPTIONS'
    }

    method = methods[method_choice]
    url = Prompt.ask("[cyan]Enter API endpoint URL[/cyan]")

    # Headers
    console.print(f"\n[bold yellow]📝 HEADERS (press Enter for none):[/bold yellow]")
    headers = {}
    while True:
        header_name = Prompt.ask("[cyan]Header name (or 'done' to finish)[/cyan]")
        if header_name.lower() == 'done':
            break
        header_value = Prompt.ask(f"[cyan]Value for {header_name}[/cyan]")
        headers[header_name] = header_value

    # Request body for POST/PUT/PATCH
    data = None
    if method in ['POST', 'PUT', 'PATCH']:
        console.print(f"\n[bold yellow]📝 REQUEST BODY:[/bold yellow]")
        body_choice = Prompt.ask("[cyan]Body type: 1. JSON  2. Form Data  3. Raw Text[/cyan]", choices=['1', '2', '3'])

        if body_choice == '1':
            json_str = Prompt.ask("[cyan]Enter JSON data[/cyan]")
            try:
                data = json.loads(json_str)
                headers['Content-Type'] = 'application/json'
            except:
                console.print("[bold red]❌ Invalid JSON![/bold red]")
                return
        elif body_choice == '2':
            data = {}
            while True:
                key = Prompt.ask("[cyan]Form field name (or 'done')[/cyan]")
                if key.lower() == 'done':
                    break
                value = Prompt.ask(f"[cyan]Value for {key}[/cyan]")
                data[key] = value
        else:
            data = Prompt.ask("[cyan]Enter raw text[/cyan]")

    # Authentication
    console.print(f"\n[bold yellow]🔐 AUTHENTICATION:[/bold yellow]")
    auth_choice = Prompt.ask("[cyan]Auth type: 1. None  2. Basic Auth  3. Bearer Token  4. API Key[/cyan]", choices=['1', '2', '3', '4'])

    if auth_choice == '2':
        username = Prompt.ask("[cyan]Username[/cyan]")
        password = Prompt.ask("[cyan]Password[/cyan]", password=True)
        auth = (username, password)
    elif auth_choice == '3':
        token = Prompt.ask("[cyan]Bearer token[/cyan]")
        headers['Authorization'] = f'Bearer {token}'
        auth = None
    elif auth_choice == '4':
        key_name = Prompt.ask("[cyan]API key header name[/cyan]", default="X-API-Key")
        key_value = Prompt.ask("[cyan]API key value[/cyan]")
        headers[key_name] = key_value
        auth = None
    else:
        auth = None

    # Make the request
    console.print(f"\n[bold cyan]🚀 SENDING {method} REQUEST...[/bold cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Sending request...", total=1)

        start_time = time.time()
        try:
            if method == 'GET':
                response = requests.get(url, headers=headers, auth=auth, timeout=30)
            elif method == 'POST':
                response = requests.post(url, headers=headers, json=data if isinstance(data, dict) else None, data=data if isinstance(data, str) else None, auth=auth, timeout=30)
            elif method == 'PUT':
                response = requests.put(url, headers=headers, json=data if isinstance(data, dict) else None, data=data if isinstance(data, str) else None, auth=auth, timeout=30)
            elif method == 'DELETE':
                response = requests.delete(url, headers=headers, auth=auth, timeout=30)
            elif method == 'PATCH':
                response = requests.patch(url, headers=headers, json=data if isinstance(data, dict) else None, data=data if isinstance(data, str) else None, auth=auth, timeout=30)
            elif method == 'HEAD':
                response = requests.head(url, headers=headers, auth=auth, timeout=30)
            elif method == 'OPTIONS':
                response = requests.options(url, headers=headers, auth=auth, timeout=30)

            response_time = time.time() - start_time
            progress.update(task, advance=1, description="Request completed!")

        except requests.exceptions.RequestException as e:
            console.print(f"[bold red]❌ Request failed: {str(e)}[/bold red]")
            return

    # Display results
    display_response(response, response_time, method, url)

def display_response(response, response_time, method, url):
    """Display API response details"""
    console.print(f"\n[bold green]📡 API RESPONSE ANALYSIS[/bold green]")
    console.print("=" * 50)

    # Response info table
    table = Table()
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")

    table.add_row("Method", method)
    table.add_row("URL", url)
    table.add_row("Status Code", f"{response.status_code} {response.reason}")
    table.add_row("Response Time", f"{response_time:.3f}s")
    table.add_row("Content Type", response.headers.get('content-type', 'Unknown'))
    table.add_row("Content Length", response.headers.get('content-length', 'Unknown'))

    console.print(table)

    # Status analysis
    if response.status_code >= 200 and response.status_code < 300:
        console.print(f"\n[bold green]✅ SUCCESS: {response.status_code}[/bold green]")
    elif response.status_code >= 300 and response.status_code < 400:
        console.print(f"\n[bold yellow]⚠️  REDIRECT: {response.status_code}[/bold yellow]")
    elif response.status_code >= 400 and response.status_code < 500:
        console.print(f"\n[bold red]❌ CLIENT ERROR: {response.status_code}[/bold red]")
    elif response.status_code >= 500:
        console.print(f"\n[bold red]💥 SERVER ERROR: {response.status_code}[/bold red]")

    # Response headers
    console.print(f"\n[bold cyan]📋 RESPONSE HEADERS:[/bold cyan]")
    headers_table = Table()
    headers_table.add_column("Header", style="cyan")
    headers_table.add_column("Value", style="yellow")

    for header, value in response.headers.items():
        headers_table.add_row(header, value)

    console.print(headers_table)

    # Response body
    console.print(f"\n[bold cyan]📝 RESPONSE BODY:[/bold cyan]")

    if response.text:
        try:
            # Try to parse as JSON
            json_data = response.json()
            console.print("[green]JSON Response:[/green]")
            console.print(json.dumps(json_data, indent=2))
        except:
            # Display as text
            if len(response.text) > 1000:
                console.print(response.text[:1000] + "...")
                console.print(f"[dim](Showing first 1000 characters of {len(response.text)} total)[/dim]")
            else:
                console.print(response.text)
    else:
        console.print("[dim]No response body[/dim]")

    # Performance analysis
    console.print(f"\n[bold yellow]⚡ PERFORMANCE ANALYSIS:[/bold yellow]")
    if response_time < 0.5:
        console.print("• Response time: [bold green]Excellent[/bold green]")
    elif response_time < 2.0:
        console.print("• Response time: [bold yellow]Good[/bold yellow]")
    else:
        console.print("• Response time: [bold red]Slow[/bold red]")

    # Security analysis
    console.print(f"\n[bold yellow]🔒 SECURITY ANALYSIS:[/bold yellow]")
    security_issues = []

    if 'https' not in url:
        security_issues.append("❌ Not using HTTPS")

    if response.headers.get('x-powered-by'):
        security_issues.append("⚠️  Server info leaked (X-Powered-By)")

    if response.headers.get('server'):
        security_issues.append("⚠️  Server info leaked (Server header)")

    if not response.headers.get('x-frame-options'):
        security_issues.append("⚠️  Missing X-Frame-Options header")

    if not response.headers.get('x-content-type-options'):
        security_issues.append("⚠️  Missing X-Content-Type-Options header")

    if not security_issues:
        console.print("[bold green]✅ No obvious security issues found[/bold green]")
    else:
        for issue in security_issues:
            console.print(issue)

    Prompt.ask("\n[cyan]Press Enter to continue[/cyan]")
