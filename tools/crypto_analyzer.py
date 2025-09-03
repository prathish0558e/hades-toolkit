import hashlib
import base64
import binascii
import re
import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Extreme Level Cryptographic Analysis Tool"""
    clear_screen()
    console.print(Panel("[bold red]🔥 CRYPTOGRAPHIC ANALYZER - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: This tool analyzes cryptographic functions. Use responsibly![/bold yellow]\n")
    
    console.print("[bold cyan]Select an option:[/bold cyan]")
    console.print("1. Hash Analysis & Cracking")
    console.print("2. Encryption/Decryption")
    console.print("3. Password Strength Analysis")
    console.print("4. Cryptographic Hash Generation")
    
    choice = Prompt.ask("[cyan]Enter your choice (1-4)[/cyan]")
    
    if choice == '1':
        hash_analysis()
    elif choice == '2':
        encryption_decryption()
    elif choice == '3':
        password_strength()
    elif choice == '4':
        hash_generation()
    else:
        console.print("[bold red]Invalid choice![/bold red]")

def hash_analysis():
    """Analyze and attempt to crack hashes"""
    console.print("\n[bold cyan]🔍 HASH ANALYSIS & CRACKING[/bold cyan]")
    hash_input = Prompt.ask("[cyan]Enter hash to analyze[/cyan]")
    
    with console.status("[bold green]Analyzing hash...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        # Detect hash type
        hash_type = detect_hash_type(hash_input)
        console.print(f"[green]Detected Hash Type:[/green] [cyan]{hash_type}[/cyan]")
        
        # Basic wordlist attack simulation
        console.print("\n[bold yellow]Attempting dictionary attack (demo mode)...[/bold yellow]")
        common_passwords = ['password', '123456', 'admin', 'letmein', 'qwerty', 'monkey', 'dragon', 'baseball']
        
        cracked = False
        for password in common_passwords:
            if hash_type == 'MD5':
                hashed = hashlib.md5(password.encode()).hexdigest()
            elif hash_type == 'SHA1':
                hashed = hashlib.sha1(password.encode()).hexdigest()
            elif hash_type == 'SHA256':
                hashed = hashlib.sha256(password.encode()).hexdigest()
            else:
                hashed = password  # Unknown type
            
            if hashed == hash_input.lower():
                console.print(f"[bold green]✓ Password cracked: {password}[/bold green]")
                cracked = True
                break
        
        if not cracked:
            console.print("[yellow]Password not found in basic dictionary[/yellow]")
            console.print("[cyan]💡 Tip: Use tools like John the Ripper or Hashcat for advanced cracking[/cyan]")

def detect_hash_type(hash_str):
    """Detect the type of hash"""
    length = len(hash_str)
    if length == 32:
        return "MD5"
    elif length == 40:
        return "SHA1"
    elif length == 64:
        return "SHA256"
    elif length == 128:
        return "SHA512"
    else:
        return "Unknown"

def encryption_decryption():
    """Basic encryption/decryption operations"""
    console.print("\n[bold cyan]🔐 ENCRYPTION/DECRYPTION[/bold cyan]")
    console.print("1. Base64 Encode")
    console.print("2. Base64 Decode")
    console.print("3. Hex Encode")
    console.print("4. Hex Decode")
    
    choice = Prompt.ask("[cyan]Enter your choice (1-4)[/cyan]")
    text = Prompt.ask("[cyan]Enter text[/cyan]")
    
    try:
        if choice == '1':
            result = base64.b64encode(text.encode()).decode()
            console.print(f"[green]Encoded:[/green] [cyan]{result}[/cyan]")
        elif choice == '2':
            result = base64.b64decode(text).decode()
            console.print(f"[green]Decoded:[/green] [cyan]{result}[/cyan]")
        elif choice == '3':
            result = binascii.hexlify(text.encode()).decode()
            console.print(f"[green]Hex Encoded:[/green] [cyan]{result}[/cyan]")
        elif choice == '4':
            result = binascii.unhexlify(text).decode()
            console.print(f"[green]Hex Decoded:[/green] [cyan]{result}[/cyan]")
        else:
            console.print("[bold red]Invalid choice![/bold red]")
    except Exception as e:
        console.print(f"[bold red]Error: {e}[/bold red]")

def password_strength():
    """Analyze password strength"""
    console.print("\n[bold cyan]🔒 PASSWORD STRENGTH ANALYSIS[/bold cyan]")
    password = Prompt.ask("[cyan]Enter password to analyze[/cyan]", password=True)
    
    with console.status("[bold green]Analyzing password strength...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        score = 0
        feedback = []
        
        # Length check
        if len(password) >= 8:
            score += 1
        else:
            feedback.append("Password should be at least 8 characters long")
        
        # Complexity checks
        if re.search(r'[a-z]', password):
            score += 1
        else:
            feedback.append("Add lowercase letters")
            
        if re.search(r'[A-Z]', password):
            score += 1
        else:
            feedback.append("Add uppercase letters")
            
        if re.search(r'\d', password):
            score += 1
        else:
            feedback.append("Add numbers")
            
        if re.search(r'[!@#$%^&*(),.?":{}|<>]', password):
            score += 1
        else:
            feedback.append("Add special characters")
        
        # Strength rating
        if score <= 2:
            strength = "[bold red]Very Weak[/bold red]"
        elif score <= 3:
            strength = "[bold yellow]Weak[/bold yellow]"
        elif score <= 4:
            strength = "[bold green]Good[/bold green]"
        else:
            strength = "[bold green]Very Strong[/bold green]"
        
        console.print(f"[green]Password Strength:[/green] {strength}")
        console.print(f"[green]Score:[/green] [cyan]{score}/5[/cyan]")
        
        if feedback:
            console.print(Panel(
                "\n".join([f"[yellow]•[/yellow] {item}" for item in feedback]),
                title="[bold yellow]Improvement Suggestions[/bold yellow]", border_style="yellow"
            ))

def hash_generation():
    """Generate various cryptographic hashes"""
    console.print("\n[bold cyan]🔑 CRYPTOGRAPHIC HASH GENERATION[/bold cyan]")
    text = Prompt.ask("[cyan]Enter text to hash[/cyan]")
    
    with console.status("[bold green]Generating hashes...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        hashes = {
            'MD5': hashlib.md5(text.encode()).hexdigest(),
            'SHA1': hashlib.sha1(text.encode()).hexdigest(),
            'SHA256': hashlib.sha256(text.encode()).hexdigest(),
            'SHA384': hashlib.sha384(text.encode()).hexdigest(),
            'SHA512': hashlib.sha512(text.encode()).hexdigest()
        }
        
        for hash_type, hash_value in hashes.items():
            console.print(f"[green]{hash_type}:[/green] [cyan]{hash_value}[/cyan]")
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
