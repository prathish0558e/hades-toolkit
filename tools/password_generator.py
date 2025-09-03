import random
import string
import secrets
import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Advanced Password Generator Tool"""
    from utils.ui import print_banner
    clear_screen()
    print_banner("Hades Toolkit")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold red]🔥 ADVANCED PASSWORD GENERATOR - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: Generate strong passwords for security![/bold yellow]\n")

    console.print("[bold cyan]Select password generation mode:[/bold cyan]")
    console.print("1. Basic Random Password")
    console.print("2. Advanced Secure Password")
    console.print("3. Memorable Password (with words)")
    console.print("4. PIN Code Generator")
    console.print("5. WiFi Password Generator")
    console.print("6. Custom Pattern Password")

    choice = Prompt.ask("[cyan]Choose option[/cyan]", choices=['1', '2', '3', '4', '5', '6'])

    if choice == '1':
        generate_basic_password()
    elif choice == '2':
        generate_advanced_password()
    elif choice == '3':
        generate_memorable_password()
    elif choice == '4':
        generate_pin()
    elif choice == '5':
        generate_wifi_password()
    elif choice == '6':
        generate_custom_password()

def generate_basic_password():
    """Generate basic random password"""
    console.print("\n[bold green]🔐 BASIC PASSWORD GENERATOR[/bold green]")

    length = Prompt.ask("[cyan]Enter password length[/cyan]", default="12")
    try:
        length = int(length)
        if length < 4:
            length = 8
    except:
        length = 12

    # Generate password
    chars = string.ascii_letters + string.digits + "!@#$%^&*"
    password = ''.join(random.choice(chars) for _ in range(length))

    display_password(password, "Basic Random")

def generate_advanced_password():
    """Generate advanced secure password using secrets"""
    console.print("\n[bold green]🔐 ADVANCED SECURE PASSWORD GENERATOR[/bold green]")

    length = Prompt.ask("[cyan]Enter password length (8-64)[/cyan]", default="16")
    try:
        length = int(length)
        if length < 8:
            length = 16
        elif length > 64:
            length = 64
    except:
        length = 16

    # Use secrets for cryptographically strong random
    alphabet = string.ascii_letters + string.digits + "!@#$%^&*()-_=+[]{}|;:,.<>?"
    password = ''.join(secrets.choice(alphabet) for _ in range(length))

    display_password(password, "Advanced Secure")

def generate_memorable_password():
    """Generate memorable password with words"""
    console.print("\n[bold green]🔐 MEMORABLE PASSWORD GENERATOR[/bold green]")

    words = [
        'apple', 'banana', 'cherry', 'dragon', 'eagle', 'falcon', 'guitar', 'hammer',
        'island', 'jungle', 'kitten', 'lemon', 'mountain', 'ninja', 'ocean', 'piano',
        'queen', 'rocket', 'sunset', 'tiger', 'unicorn', 'violet', 'whale', 'xylophone',
        'yellow', 'zebra', 'alpha', 'bravo', 'charlie', 'delta', 'echo', 'foxtrot'
    ]

    num_words = Prompt.ask("[cyan]Number of words (2-5)[/cyan]", default="3")
    try:
        num_words = int(num_words)
        if num_words < 2:
            num_words = 2
        elif num_words > 5:
            num_words = 5
    except:
        num_words = 3

    # Generate password with words
    selected_words = [secrets.choice(words) for _ in range(num_words)]
    password = ''.join(selected_words)

    # Add numbers and symbols
    password += str(secrets.randbelow(100))
    password += secrets.choice('!@#$%^&*')

    display_password(password, "Memorable")

def generate_pin():
    """Generate PIN codes"""
    console.print("\n[bold green]🔐 PIN CODE GENERATOR[/bold green]")

    length = Prompt.ask("[cyan]PIN length (4-12)[/cyan]", default="6")
    try:
        length = int(length)
        if length < 4:
            length = 4
        elif length > 12:
            length = 12
    except:
        length = 6

    # Generate numeric PIN
    pin = ''.join(secrets.choice('0123456789') for _ in range(length))

    display_password(pin, f"PIN ({length} digits)")

def generate_wifi_password():
    """Generate WiFi-style password"""
    console.print("\n[bold green]🔐 WIFI PASSWORD GENERATOR[/bold green]")

    # Generate WPA2-style password
    adjectives = ['Fast', 'Secure', 'Super', 'Ultra', 'Mega', 'Power', 'Speed', 'Turbo']
    nouns = ['WiFi', 'Network', 'Internet', 'Connection', 'Router', 'Signal', 'Wave', 'Link']

    adj = secrets.choice(adjectives)
    noun = secrets.choice(nouns)
    number = secrets.randbelow(1000)
    symbol = secrets.choice('!@#$%^&*')

    password = f"{adj}{noun}{number}{symbol}"

    display_password(password, "WiFi Password")

def generate_custom_password():
    """Generate password with custom pattern"""
    console.print("\n[bold green]🔐 CUSTOM PATTERN PASSWORD GENERATOR[/bold green]")

    console.print("[yellow]Pattern symbols:[/yellow]")
    console.print("• L = Lowercase letter")
    console.print("• U = Uppercase letter")
    console.print("• D = Digit")
    console.print("• S = Special character")
    console.print("• A = Any character")
    console.print("\nExample: UUUUUULLLLDDDSS")

    pattern = Prompt.ask("[cyan]Enter pattern[/cyan]", default="UUUUUULLLLDDDSS")

    password = ""
    for char in pattern.upper():
        if char == 'L':
            password += secrets.choice(string.ascii_lowercase)
        elif char == 'U':
            password += secrets.choice(string.ascii_uppercase)
        elif char == 'D':
            password += secrets.choice(string.digits)
        elif char == 'S':
            password += secrets.choice('!@#$%^&*()-_=+[]{}|;:,.<>?')
        elif char == 'A':
            password += secrets.choice(string.ascii_letters + string.digits + '!@#$%^&*')
        else:
            password += char  # Keep literal characters

    display_password(password, f"Custom Pattern ({pattern})")

def display_password(password, password_type):
    """Display generated password with analysis"""
    console.print(f"\n[bold cyan]🎯 GENERATED {password_type.upper()} PASSWORD:[/bold cyan]")
    console.print("=" * 50)

    # Display password (partially hidden for security)
    hidden_password = password[:4] + "•" * (len(password) - 8) + password[-4:] if len(password) > 8 else password
    console.print(f"[bold green]Password: {password}[/bold green]")
    console.print(f"[dim]Preview: {hidden_password}[/dim]")

    # Password analysis
    console.print(f"\n[bold yellow]🔍 PASSWORD ANALYSIS:[/bold yellow]")

    analysis_table = Table()
    analysis_table.add_column("Property", style="cyan")
    analysis_table.add_column("Value", style="yellow")

    analysis_table.add_row("Length", str(len(password)))
    analysis_table.add_row("Uppercase", str(sum(1 for c in password if c.isupper())))
    analysis_table.add_row("Lowercase", str(sum(1 for c in password if c.islower())))
    analysis_table.add_row("Digits", str(sum(1 for c in password if c.isdigit())))
    analysis_table.add_row("Special Chars", str(sum(1 for c in password if not c.isalnum())))

    # Strength rating
    strength = calculate_strength(password)
    analysis_table.add_row("Strength", strength)

    console.print(analysis_table)

    # Copy to clipboard (if possible)
    try:
        import pyperclip
        pyperclip.copy(password)
        console.print(f"\n[bold green]✅ Password copied to clipboard![/bold green]")
    except:
        console.print(f"\n[yellow]💡 Copy the password manually[/yellow]")

    # Save option
    save_choice = Prompt.ask("\n[cyan]Save password to file? (y/n)[/cyan]", default="n")
    if save_choice.lower() == 'y':
        filename = Prompt.ask("[cyan]Enter filename[/cyan]", default="generated_passwords.txt")
        try:
            with open(filename, 'a') as f:
                f.write(f"{time.strftime('%Y-%m-%d %H:%M:%S')} - {password_type}: {password}\n")
            console.print(f"[bold green]✅ Password saved to {filename}![/bold green]")
        except:
            console.print("[bold red]❌ Failed to save password[/bold red]")

def calculate_strength(password):
    """Calculate password strength"""
    score = 0
    if len(password) >= 8:
        score += 1
    if len(password) >= 12:
        score += 1
    if any(c.isupper() for c in password):
        score += 1
    if any(c.islower() for c in password):
        score += 1
    if any(c.isdigit() for c in password):
        score += 1
    if any(not c.isalnum() for c in password):
        score += 1

    if score <= 2:
        return "[red]Weak[/red]"
    elif score <= 4:
        return "[yellow]Medium[/yellow]"
    elif score <= 5:
        return "[green]Strong[/green]"
    else:
        return "[bold green]Very Strong[/bold green]"

    Prompt.ask("\n[cyan]Press Enter to continue[/cyan]")
