import hashlib
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    clear_screen()
    print_banner("Hash Generator")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold blue]Hash Generator[/bold blue]", border_style="blue"))
    console.print("[yellow]This tool generates various hash values for a given text or file.[/yellow]\n")
    
    text = Prompt.ask("[cyan]Enter text to hash[/cyan]")
    
    hashes = {
        "MD5": hashlib.md5(text.encode()).hexdigest(),
        "SHA-1": hashlib.sha1(text.encode()).hexdigest(),
        "SHA-256": hashlib.sha256(text.encode()).hexdigest(),
        "SHA-512": hashlib.sha512(text.encode()).hexdigest(),
    }
    
    info = "\n".join([f"[bold]{algo}:[/bold] [green]{hash_val}[/green]" for algo, hash_val in hashes.items()])
    console.print(Panel(info, title="[bold yellow]Hash Values[/bold yellow]", border_style="blue"))
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
