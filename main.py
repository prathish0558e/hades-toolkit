import sys
import os
from rich.panel import Panel
from rich.prompt import Prompt
from utils.ui import console, clear_screen, print_banner
from tools import (
    phone_info,
    port_scanner,
    wifi_cracker,
    ip_tracer,
    web_vuln_scanner,
    system_info,
    info_tools,
    dns_lookup,
    whois_lookup,
    password_checker,
    hash_generator,
    social_media_hacking,
    social_media_osint,
    metadata_extractor,
    hash_cracker,
    advanced_scanner,
    crypto_analyzer,
    forensic_tools,
    vuln_assessment,
    email_osint,
    username_search,
    password_generator,
    ssl_checker,
    api_tester,
    sms_bomber_tool,
    subdomain_scanner,
    qr_code_generator,
    spyware_scanner,
    adb_qr_generator,
    advanced_virus_scanner,
    file_encryptor
)

tools = {
    '1': ("Advanced Phone Number OSINT", phone_info.phone_info_tool),
    '2': ("Network Port Scanner", port_scanner.run),
    '3': ("WiFi Password Cracking (Sim)", wifi_cracker.run),
    '4': ("IP Address Tracer", ip_tracer.run),
    '5': ("Web Vulnerability Scanner (Sim)", web_vuln_scanner.web_vuln_scanner_tool),
    '6': ("System Information Gatherer", system_info.display_system_info),
    '7': ("Screen Hacking / RAT Info", info_tools.remote_access_info),
    '8': ("Fake Link Creation Info", info_tools.fake_link_info),
    '9': ("Camera Hacking Info", info_tools.camera_hacking_info),
    '10': ("DNS Lookup", dns_lookup.run),
    '11': ("WHOIS Lookup", whois_lookup.run),
    '12': ("Password Strength Checker", password_checker.run),
    '13': ("Hash Generator", hash_generator.run),
    '14': ("Social Media Hacking (Phishing Link Generator)", social_media_hacking.social_media_hacking),
    '15': ("Social Media OSINT Tool", social_media_osint.social_media_osint),
    '16': ("Metadata Extractor", metadata_extractor.metadata_extractor),
    '17': ("Hash Cracker", hash_cracker.hash_cracker),
    '18': ("Advanced Network Scanner", advanced_scanner.run),
    '19': ("Cryptographic Analyzer", crypto_analyzer.run),
    '20': ("Digital Forensics Tool", forensic_tools.run),
    '21': ("Vulnerability Assessment", vuln_assessment.run),
    '22': ("Email OSINT Analyzer", email_osint.run),
    '23': ("Username Search Tool", username_search.run),
    '24': ("Advanced Password Generator", password_generator.run),
    '25': ("SSL Certificate Checker", ssl_checker.run),
    '26': ("REST API Tester", api_tester.run),
    '27': ("Hades SMS Bomber", sms_bomber_tool.run_bomber),
    '28': ("Subdomain Scanner", subdomain_scanner.run),
    '29': ("QR Code Phishing Generator", qr_code_generator.run),
    '30': ("Anti-Spyware Website Scanner (GUI)", spyware_scanner.main),
    '31': ("ADB QR Generator", adb_qr_generator.main),
    '32': ("Advanced Virus Scanner", advanced_virus_scanner.main),
    '33': ("File Encryptor/Decryptor", file_encryptor.main),
}

def main_menu():
    while True:
        clear_screen()
        print_banner("Hades Toolkit")
        menu_lines = []
        for key, (name, _) in tools.items():
            color = "cyan" if key in ['1', '4', '6', '10', '11', '22', '23'] else "red" if key in ['2', '3', '5', '18', '19', '20', '21', '25', '26', '27'] else "yellow"
            menu_lines.append(f"[bold {color}]{key}.[/bold {color}] {name}")
        menu_lines.append("[bold white]0.[/bold white] Exit")
        menu_text = "\n".join(menu_lines)
        console.print(Panel(
            menu_text,
            title="[bold yellow]Hades Toolkit Menu[/bold yellow]",
            border_style="yellow"
        ))
        choice = Prompt.ask("[cyan]Choose an option[/cyan]", default="1")
        if choice == '0':
            clear_screen()
            print_banner("Hades Toolkit")
            console.print("[bold red]Exiting... Goodbye![/bold red]")
            break

        selected_tool = tools[choice][1]
        if hasattr(selected_tool, 'run') and callable(selected_tool.run):
            selected_tool.run()
        elif callable(selected_tool):
            selected_tool()
        else:
            console.print(f"[bold red]Error: Tool {tools[choice][0]} is not configured correctly.[/bold red]")
            Prompt.ask("[yellow]Press Enter to continue.[/yellow]")
            continue

        # After tool execution, just ask what to do next (no extra options listed)
        next_action = Prompt.ask("[cyan]What would you like to do next? (1: Main Menu, 0: Exit)[/cyan]", choices=['1', '0'], default='1')
        if next_action == '1':
            continue  # Return to menu
        elif next_action == '0':
            console.print("[bold red]Exiting... Goodbye![/bold red]")
            break

if __name__ == "__main__":
    try:
        script_dir = os.path.dirname(os.path.abspath(__file__))
        wordlist_path = os.path.join(script_dir, "data", "wordlist.txt")
        if not os.path.exists(wordlist_path):
            console.print(f"[yellow]Warning: '{wordlist_path}' not found. Creating a sample file.[/yellow]")
            os.makedirs(os.path.join(script_dir, "data"), exist_ok=True)
            with open(wordlist_path, "w") as f:
                f.write("password123\n")
                f.write("admin\n")
                f.write("123456\n")
                f.write("qwerty\n")
        main_menu()
    except KeyboardInterrupt:
        print_banner("Hades Toolkit")
        console.print("\n[bold red]Interrupted by user. Exiting...[/bold red]")
        sys.exit(0)
    except ImportError as e:
        print_banner("Hades Toolkit")
        console.print(f"\n[bold red]Error: A required module is missing: {e}[/bold red]")
        console.print("[yellow]Please run 'pip install -r requirements.txt' to install dependencies.[/yellow]")
        sys.exit(1)
    except Exception as e:
        print_banner("Hades Toolkit")
        console.print(f"\n[bold red]An unexpected error occurred: {e}[/bold red]")
        sys.exit(1)