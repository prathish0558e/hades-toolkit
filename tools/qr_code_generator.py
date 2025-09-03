import qrcode
import os
import sys
from PIL import Image

# Add project root to Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.ui import console
from rich.prompt import Prompt
from rich.panel import Panel

def run():
    """Main function to run the QR Code Phishing Generator."""
    console.print(Panel("[bold magenta]🔗 QR Code Phishing Generator 🔗[/bold magenta]", subtitle="[cyan]Create a QR code that points to any URL[/cyan]"))

    url = Prompt.ask("[yellow]Enter the full URL to encode (e.g., https://your-phishing-site.com)[/yellow]").strip()
    if not url.startswith(('http://', 'https://')):
        console.print("[bold red]Invalid URL. Please make sure it starts with 'http://' or 'https://'[/bold red]")
        return

    filename = Prompt.ask("[yellow]Enter the filename for the QR code image (e.g., qr_code.png)[/yellow]", default="phishing_qr.png").strip()
    
    # Ensure the filename ends with a valid image extension
    if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
        filename += ".png"

    try:
        # --- QR Code Generation ---
        console.print(f"\n[cyan]Generating QR code for:[/] [bold white]{url}[/bold white]")
        
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(url)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        
        # --- Saving the Image ---
        # Save to a dedicated 'output' directory
        output_dir = os.path.join(os.path.dirname(__file__), '..', 'output')
        os.makedirs(output_dir, exist_ok=True)
        save_path = os.path.join(output_dir, filename)
        
        img.save(save_path)

        console.print(f"\n[bold green]✅ Success! QR code saved to:[/bold green] [white]{os.path.abspath(save_path)}[/white]")

    except Exception as e:
        console.print(f"[bold red]An error occurred: {e}[/bold red]")

if __name__ == "__main__":
    run()
