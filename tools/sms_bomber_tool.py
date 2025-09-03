import os
import subprocess
import sys

# Add project root to the Python path to allow imports from 'utils'
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
if project_root not in sys.path:
    sys.path.insert(0, project_root)

from utils.ui import console

def run_bomber():
    """
    Runs the hades_bomber.py script.
    """
    script_path = os.path.join(os.path.dirname(__file__), 'sms_bomber', 'hades_bomber.py')
    
    if not os.path.exists(script_path):
        console.print(f"[bold red]Error: The script was not found at {script_path}[/bold red]")
        return

    console.print("[bold green]Launching Hades Bomber...[/bold green]")
    
    # We use subprocess.run to execute the script.
    # This is better than os.system because it gives more control.
    # We pass sys.executable to ensure we're using the same python interpreter.
    process = subprocess.run([sys.executable, script_path], check=False)
    
    if process.returncode != 0:
        console.print(f"[bold red]Hades Bomber exited with an error (code: {process.returncode}).[/bold red]")

if __name__ == '__main__':
    run_bomber()
