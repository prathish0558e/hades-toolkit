import hashlib
try:
    import bcrypt
    BCRYPT_AVAILABLE = True
except ImportError:
    BCRYPT_AVAILABLE = False

try:
    import crypt
    CRYPT_AVAILABLE = True
except ImportError:
    CRYPT_AVAILABLE = False

from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen
import time
import itertools
import string
import os

def detect_hash_type(hash_string):
    """Detect the type of hash based on its characteristics"""
    hash_length = len(hash_string)

    # MD5
    if hash_length == 32 and all(c in '0123456789abcdefABCDEF' for c in hash_string):
        return "MD5"

    # SHA1
    elif hash_length == 40 and all(c in '0123456789abcdefABCDEF' for c in hash_string):
        return "SHA1"

    # SHA256
    elif hash_length == 64 and all(c in '0123456789abcdefABCDEF' for c in hash_string):
        return "SHA256"

    # SHA384
    elif hash_length == 96 and all(c in '0123456789abcdefABCDEF' for c in hash_string):
        return "SHA384"

    # SHA512
    elif hash_length == 128 and all(c in '0123456789abcdefABCDEF' for c in hash_string):
        return "SHA512"

    # bcrypt (starts with $2a$, $2b$, or $2y$)
    elif hash_string.startswith(('$2a$', '$2b$', '$2y$')):
        return "bcrypt"

    # crypt (traditional Unix)
    elif len(hash_string.split('$')) >= 3:
        return "crypt"

    else:
        return "Unknown"

def crack_md5(hash_string, wordlist_path=None):
    """Crack MD5 hash"""
    if wordlist_path and os.path.exists(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if hashlib.md5(word.encode()).hexdigest() == hash_string:
                    return word
    return None

def crack_sha1(hash_string, wordlist_path=None):
    """Crack SHA1 hash"""
    if wordlist_path and os.path.exists(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if hashlib.sha1(word.encode()).hexdigest() == hash_string:
                    return word
    return None

def crack_sha256(hash_string, wordlist_path=None):
    """Crack SHA256 hash"""
    if wordlist_path and os.path.exists(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                if hashlib.sha256(word.encode()).hexdigest() == hash_string:
                    return word
    return None

def crack_bcrypt(hash_string, wordlist_path=None):
    """Crack bcrypt hash"""
    if not BCRYPT_AVAILABLE:
        return None

    if wordlist_path and os.path.exists(wordlist_path):
        with open(wordlist_path, 'r', encoding='utf-8', errors='ignore') as f:
            for line in f:
                word = line.strip()
                try:
                    if bcrypt.checkpw(word.encode(), hash_string.encode()):
                        return word
                except:
                    continue
    return None

def brute_force_attack(hash_type, hash_string, max_length=4):
    """Simple brute force attack for short passwords"""
    chars = string.ascii_letters + string.digits

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        console=console
    ) as progress:
        task = progress.add_task(f"Brute forcing {hash_type}...", total=None)

        for length in range(1, max_length + 1):
            for attempt in itertools.product(chars, repeat=length):
                password = ''.join(attempt)

                if hash_type == "MD5":
                    if hashlib.md5(password.encode()).hexdigest() == hash_string:
                        return password
                elif hash_type == "SHA1":
                    if hashlib.sha1(password.encode()).hexdigest() == hash_string:
                        return password
                elif hash_type == "SHA256":
                    if hashlib.sha256(password.encode()).hexdigest() == hash_string:
                        return password

                progress.update(task, description=f"Trying: {password}")
    return None

def hash_cracker():
    """Main hash cracker function"""
    clear_screen()

    console.print(Panel(
        "[bold cyan]🔓 Hash Cracker[/bold cyan]\n\n"
        "Crack password hashes using various methods:\n"
        "• Dictionary attack with wordlist\n"
        "• Brute force attack (short passwords)\n"
        "• Support for MD5, SHA1, SHA256, bcrypt, crypt\n\n"
        "[bold yellow]⚠️  For educational purposes only![/bold yellow]",
        title="[bold yellow]Hash Cracker[/bold yellow]",
        border_style="cyan"
    ))

    while True:
        console.print("\n" + "="*60)

        hash_string = Prompt.ask("[cyan]Enter hash to crack[/cyan]")
        if not hash_string:
            continue

        # Detect hash type
        hash_type = detect_hash_type(hash_string)
        console.print(f"[bold green]Detected hash type: {hash_type}[/bold green]")

        if hash_type == "Unknown":
            console.print("[bold red]Could not detect hash type![/bold red]")
            continue

        # Get wordlist path
        wordlist_path = "/home/prathi/Desktop/hacking/hades-toolkit/data/wordlist.txt"
        if not os.path.exists(wordlist_path):
            console.print("[yellow]Wordlist not found. Using brute force only.[/yellow]")
            wordlist_path = None

        console.print("\n[bold cyan]Select cracking method:[/bold cyan]")
        console.print("[cyan]1.[/cyan] Dictionary attack")
        console.print("[cyan]2.[/cyan] Brute force attack (short passwords)")
        console.print("[cyan]3.[/cyan] Both methods")

        method = Prompt.ask("[cyan]Choose method[/cyan]", choices=['1', '2', '3'], default='1')

        password = None
        start_time = time.time()

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            console=console
        ) as progress:
            if method in ['1', '3']:
                task = progress.add_task("Running dictionary attack...", total=None)

                if hash_type == "MD5":
                    password = crack_md5(hash_string, wordlist_path)
                elif hash_type == "SHA1":
                    password = crack_sha1(hash_string, wordlist_path)
                elif hash_type == "SHA256":
                    password = crack_sha256(hash_string, wordlist_path)
                elif hash_type == "bcrypt":
                    password = crack_bcrypt(hash_string, wordlist_path)

                progress.update(task, completed=True)

            if not password and method in ['2', '3']:
                task = progress.add_task("Running brute force attack...", total=None)
                password = brute_force_attack(hash_type, hash_string, max_length=4)
                progress.update(task, completed=True)

        end_time = time.time()

        # Display results
        if password:
            console.print(f"\n[bold green]✅ Password found: {password}[/bold green]")
            console.print(f"[cyan]Time taken: {end_time - start_time:.2f} seconds[/cyan]")
        else:
            console.print(f"\n[bold red]❌ Password not found[/bold red]")
            console.print(f"[cyan]Time taken: {end_time - start_time:.2f} seconds[/cyan]")

        # Ask to crack another hash
        if Prompt.ask("[cyan]Crack another hash?[/cyan]", choices=['y', 'n'], default='y') == 'n':
            break

    console.print("[bold green]Returning to main menu...[/bold green]")

if __name__ == "__main__":
    hash_cracker()
