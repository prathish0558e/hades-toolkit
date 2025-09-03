import re
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen

def check_password_strength(password):
    score = 0
    feedback = []
    
    # Length check
    if len(password) >= 8:
        score += 1
    else:
        feedback.append("Password should be at least 8 characters long")
    
    # Lowercase check
    if re.search(r'[a-z]', password):
        score += 1
    else:
        feedback.append("Add lowercase letters")
    
    # Uppercase check
    if re.search(r'[A-Z]', password):
        score += 1
    else:
        feedback.append("Add uppercase letters")
    
    # Digit check
    if re.search(r'\d', password):
        score += 1
    else:
        feedback.append("Add numbers")
    
    # Special character check
    if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
        score += 1
    else:
        feedback.append("Add special characters")
    
    # Strength levels
    if score <= 2:
        strength = "[red]Weak[/red]"
    elif score <= 3:
        strength = "[yellow]Medium[/yellow]"
    elif score <= 4:
        strength = "[green]Strong[/green]"
    else:
        strength = "[bold green]Very Strong[/bold green]"
    
    return strength, feedback, score

def run():
    clear_screen()
    console.print(Panel("[bold blue]Password Strength Checker[/bold blue]", border_style="blue"))
    console.print("[yellow]This tool checks the strength of your password and provides improvement suggestions.[/yellow]\n")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    
    password = Prompt.ask("[cyan]Enter a password to check[/cyan]", password=True)
    
    strength, feedback, score = check_password_strength(password)
    
    info = f"""
[bold]Password Strength:[/bold] {strength}
[bold]Score:[/bold] {score}/5

[bold]Suggestions:[/bold]
{chr(10).join(f"- {item}" for item in feedback) if feedback else "Your password is strong!"}
    """
    console.print(Panel(info.strip(), title="[bold yellow]Password Analysis[/bold yellow]", border_style="blue"))
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
