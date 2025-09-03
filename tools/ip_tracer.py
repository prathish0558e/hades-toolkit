import requests
import time
from rich.panel import Panel
from rich.prompt import Prompt

# நமது சொந்த utility கோப்புகளிலிருந்து இறக்குமதி செய்தல்
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    """Traces an IP address to get geolocation information."""
    clear_screen()
    print_banner("IP Tracer")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold cyan]Advanced IP Address Tracer[/bold cyan]", border_style="cyan"))
    console.print("[yellow]This tool uses public APIs to find the geographical location of an IP address.[/yellow]\n")
    
    ip_address = Prompt.ask("[cyan]Enter the IP address to trace (e.g., 8.8.8.8)[/cyan]")
    
    try:
        with console.status(f"[bold green]Tracing IP: {ip_address}...[/bold green]", spinner="earth"):
            response = requests.get(f"http://ip-api.com/json/{ip_address}")
            response.raise_for_status() # பிழையான status code-களுக்கு exception எழுப்பும்
            data = response.json()
            time.sleep(2) # நீண்ட தேடலை சிமுலேட் செய்ய

        if data['status'] == 'success':
            console.print("\n[green]Trace Complete![/green]")
            info = (
                f"[bold]IP Address:[/bold] [green]{data.get('query', 'N/A')}[/green]\n"
                f"[bold]Country:[/bold] [green]{data.get('country', 'N/A')} ({data.get('countryCode', 'N/A')})[/green]\n"
                f"[bold]Region:[/bold] [green]{data.get('regionName', 'N/A')} ({data.get('region', 'N/A')})[/green]\n"
                f"[bold]City:[/bold] [green]{data.get('city', 'N/A')}[/green]\n"
                f"[bold]ZIP Code:[/bold] [green]{data.get('zip', 'N/A')}[/green]\n"
                f"[bold]Coordinates:[/bold] [green]Lat: {data.get('lat', 'N/A')}, Lon: {data.get('lon', 'N/A')}[/green]\n"
                f"[bold]Timezone:[/bold] [green]{data.get('timezone', 'N/A')}[/green]\n"
                f"[bold]ISP:[/bold] [green]{data.get('isp', 'N/A')}[/green]\n"
                f"[bold]Organization:[/bold] [green]{data.get('org', 'N/A')}[/green]"
            )
            console.print(Panel(info, title="[bold yellow]Geolocation Data[/bold yellow]", border_style="cyan"))
        else:
            console.print(f"[bold red]Could not trace the IP address. Reason: {data.get('message', 'Unknown error')}[/bold red]")

    except requests.exceptions.RequestException as e:
        console.print(f"[bold red]An error occurred while contacting the API: {e}[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")