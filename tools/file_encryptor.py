from cryptography.fernet import Fernet
import base64
import hashlib
from utils.ui import console

def generate_key(password):
    # Derive a key from password using PBKDF2
    salt = b'static_salt'  # In production, use a random salt per file
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, 100000)
    return base64.urlsafe_b64encode(key)

def encrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        encrypted = fernet.encrypt(data)
        with open(file_path + '.enc', 'wb') as f:
            f.write(encrypted)
        console.print(f"[green]File encrypted: {file_path}.enc[/green]")
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Encryption failed: {e}[/red]")

def decrypt_file(file_path, password):
    key = generate_key(password)
    fernet = Fernet(key)
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
        decrypted = fernet.decrypt(data)
        original_path = file_path.replace('.enc', '')
        with open(original_path, 'wb') as f:
            f.write(decrypted)
        console.print(f"[green]File decrypted: {original_path}[/green]")
    except FileNotFoundError:
        console.print(f"[red]File not found: {file_path}[/red]")
    except Exception as e:
        console.print(f"[red]Decryption failed: {e}[/red]")

def main():
    from utils.ui import print_banner
    from rich.prompt import Prompt
    print_banner("Hades Toolkit")
    console.print("\n=== File Encryptor/Decryptor ===\n")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    action = Prompt.ask("[cyan]Encrypt (e) or Decrypt (d)?[/cyan]", choices=["e", "d"], default="e")
    file_path = Prompt.ask("[yellow]Enter file path[/yellow]")
    password = Prompt.ask("[yellow]Enter password[/yellow]", password=True)
    if action == 'e':
        encrypt_file(file_path, password)
    elif action == 'd':
        decrypt_file(file_path, password)

if __name__ == "__main__":
    main()
