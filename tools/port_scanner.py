import socket
from rich.panel import Panel
from rich.prompt import Prompt

# நமது சொந்த utility கோப்புகளிலிருந்து இறக்குமதி செய்தல்
from utils.ui import console, clear_screen

def run():
    """Scans for open ports on a target host."""
    clear_screen()
    console.print(Panel("[bold red]Network Port Scanner[/bold red]", border_style="red"))
    console.print("[bold yellow]DISCLAIMER: This tool is for educational purposes only. Only scan hosts you have explicit permission to test.[/bold yellow]\n")

    target = Prompt.ask("[cyan]Enter the target IP address or domain (e.g., scanme.nmap.org)[/cyan]")
    
    common_ports = [21, 22, 23, 25, 53, 80, 110, 139, 443, 445, 3306, 3389, 5900, 8080, 8443]
    open_ports = []

    try:
        target_ip = socket.gethostbyname(target)
        console.print(f"\n[cyan]Scanning target: {target} ({target_ip})[/cyan]")

        with console.status("[bold green]Scanning common ports...[/bold green]", spinner="line") as status:
            for i, port in enumerate(common_ports):
                status.update(f"[bold green]Scanning port {port}... ({i+1}/{len(common_ports)})[/bold green]")
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                socket.setdefaulttimeout(0.5)
                result = sock.connect_ex((target_ip, port))
                if result == 0:
                    open_ports.append(port)
                sock.close()

        console.print("\n[green]Scan Complete.[/green]")
        if open_ports:
            console.print(Panel(
                f"[bold]Open Ports Found on {target}:[/bold]\n" + "\n".join([f"- [green]Port {p}[/green]" for p in open_ports]),
                title="[bold yellow]Scan Results[/bold yellow]", border_style="green"
            ))
        else:
            console.print(Panel("[yellow]No common open ports found.[/yellow]", title="[bold yellow]Scan Results[/bold yellow]"))

    except socket.gaierror:
        console.print(f"[bold red]Hostname could not be resolved. Please check the address and try again.[/bold red]")
    except socket.error:
        console.print(f"[bold red]Couldn't connect to server.[/bold red]")
    except Exception as e:
        console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]")

    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")