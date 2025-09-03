import os
import platform
import socket
import psutil
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def gather_system_info():
    """Gathers system information including OS, CPU, and memory details."""
    os_info = {
        "System": platform.system(),
        "Release": platform.release(),
        "Version": platform.version(),
        "Architecture": platform.machine(),
        "Hostname": socket.gethostname(),
        "IP Address": socket.gethostbyname(socket.gethostname()),
    }

    cpu_info = {
        "Physical Cores": psutil.cpu_count(logical=False),
        "Total Cores": psutil.cpu_count(logical=True),
        "Max Frequency": f"{psutil.cpu_freq().max:.2f} MHz",
        "Current Frequency": f"{psutil.cpu_freq().current:.2f} MHz",
        "CPU Usage": f"{psutil.cpu_percent(interval=1)}%",
    }

    mem = psutil.virtual_memory()
    mem_info = {
        "Total": f"{mem.total / (1024**3):.2f} GB",
        "Available": f"{mem.available / (1024**3):.2f} GB",
        "Used": f"{mem.used / (1024**3):.2f} GB",
        "Percentage": f"{mem.percent}%",
    }

    return os_info, cpu_info, mem_info

def display_system_info():
    """Displays the gathered system information in a formatted manner."""
    os_info, cpu_info, mem_info = gather_system_info()

    console.print(Panel("\n".join([f"[bold]{k}:[/bold] [cyan]{v}[/cyan]" for k, v in os_info.items()]), title="[bold yellow]Operating System[/bold yellow]", border_style="green"))
    console.print(Panel("\n".join([f"[bold]{k}:[/bold] [cyan]{v}[/cyan]" for k, v in cpu_info.items()]), title="[bold yellow]CPU[/bold yellow]", border_style="green"))
    console.print(Panel("\n".join([f"[bold]{k}:[/bold] [cyan]{v}[/cyan]" for k, v in mem_info.items()]), title="[bold yellow]Memory (RAM)[/bold yellow]", border_style="green"))
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")

def main():
    """Main function to execute the system information tool."""
    console.print(Panel("[bold green]System Information Gatherer[/bold green]", border_style="green"))
    console.print("[yellow]This tool collects and displays hardware, OS, and network information from the local machine.[/yellow]\n")
    
    display_system_info()
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")

if __name__ == "__main__":
    main()