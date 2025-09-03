from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

console = Console()

def clear_screen():
    """Clears the console screen."""
    console.clear()

def print_banner(title):
    """Prints an impressive ASCII art banner for Hades Toolkit."""
    banner = """
[bold red]
██╗░░██╗░█████╗░██████╗░███████╗░██████╗  ████████╗░█████╗░░█████╗░██╗░░░░░██╗░░██╗██╗████████╗
██║░░██║██╔══██╗██╔══██╗██╔════╝██╔════╝  ╚══██╔══╝██╔══██╗██╔══██╗██║░░░░░██║░██╔╝██║╚══██╔══╝
███████║███████║██║░░██║█████╗░░╚█████╗░  ░░░██║░░░██║░░██║██║░░██║██║░░░░░█████═╝░██║░░░██║░░░
██╔══██║██╔══██║██║░░██║██╔══╝░░░╚═══██╗  ░░░██║░░░██║░░██║██║░░██║██║░░░░░██╔═██╗░██║░░░██║░░░
██║░░██║██║░░██║██████╔╝███████╗██████╔╝  ░░░██║░░░╚█████╔╝╚█████╔╝███████╗██║░╚██╗██║░░░██║░░░
╚═╝░░╚═╝╚═╝░░╚═╝╚═════╝░╚══════╝╚═════╝░  ░░░╚═╝░░░░╚════╝░░╚════╝░╚══════╝╚═╝░░╚═╝╚═╝░░░╚═╝░░░
[/bold red]
[bold yellow]═══════════════════════════════════════════════════════════════════════════════════════════════[/bold yellow]
[bold red]                           🔥 HADES TOOLKIT - Underworld Hacking Arsenal 🔥[/bold red]
[bold yellow]═══════════════════════════════════════════════════════════════════════════════════════════════[/bold yellow]
[bold red]                                    ⚔️  Master the Dark Arts of Cybersecurity  ⚔️[/bold red]
[bold yellow]═══════════════════════════════════════════════════════════════════════════════════════════════[/bold yellow]
"""
    console.print(banner)

def display_menu(options):
    """Displays a menu with the given options."""
    console.print(Panel("[bold yellow]Main Menu[/bold yellow]", border_style="yellow"))
    for idx, option in enumerate(options, start=1):
        console.print(f"[bold green]{idx}.[/bold green] {option}")
    console.print()

def get_user_choice(prompt, choices):
    """Prompts the user for a choice and validates it."""
    choice = Prompt.ask(prompt, choices=choices)
    return choice

def display_message(message, style="green"):
    """Displays a message with the specified style."""
    console.print(f"[{style}]{message}[/{style}]")