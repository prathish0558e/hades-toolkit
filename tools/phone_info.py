import os
import time
import sys
import phonenumbers
from phonenumbers import geocoder, carrier, timezone, phonenumberutil
from utils.ui import console
from rich.panel import Panel
from rich.prompt import Prompt

def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

def get_number_type(number):
    number_type = phonenumberutil.number_type(number)
    types = {
        phonenumberutil.PhoneNumberType.FIXED_LINE: "Landline",
        phonenumberutil.PhoneNumberType.MOBILE: "Mobile",
        phonenumberutil.PhoneNumberType.FIXED_LINE_OR_MOBILE: "Landline or Mobile",
        phonenumberutil.PhoneNumberType.TOLL_FREE: "Toll-free",
        phonenumberutil.PhoneNumberType.PREMIUM_RATE: "Premium Rate",
        phonenumberutil.PhoneNumberType.SHARED_COST: "Shared Cost",
        phonenumberutil.PhoneNumberType.VOIP: "VoIP",
        phonenumberutil.PhoneNumberType.PERSONAL_NUMBER: "Personal Number",
        phonenumberutil.PhoneNumberType.PAGER: "Pager",
        phonenumberutil.PhoneNumberType.UAN: "UAN",
        phonenumberutil.PhoneNumberType.VOICEMAIL: "Voicemail",
    }
    return types.get(number_type, "Unknown")

def phone_info_tool():
    clear_screen()
    console.print(Panel("[bold cyan]Advanced Phone Number OSINT Tool[/bold cyan]", border_style="cyan"))
    console.print("[yellow]This tool provides basic info and generates search links for public data. It cannot automatically retrieve private data like name or address.[/yellow]\n")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    
    while True:
        phone_number_str = Prompt.ask("[yellow]Enter the full phone number (e.g., +919876543210)[/yellow] or type 'back' to return")
        
        if phone_number_str.lower() == 'back':
            break

        try:
            console.print(f"\n[cyan]Gathering intelligence for {phone_number_str}...[/cyan]")
            
            parsed_number = phonenumbers.parse(phone_number_str, None)
            
            if not phonenumbers.is_valid_number(parsed_number):
                console.print("[bold red]Invalid or incomplete phone number. Please enter a full number with a country code.[/bold red]\n")
                continue

            with console.status("[bold green]Analyzing number and searching public databases...[/bold green]", spinner="dots"):
                time.sleep(2)
                country = geocoder.description_for_number(parsed_number, "en")
                service_provider = carrier.name_for_number(parsed_number, "en")
                time_zones = timezone.time_zones_for_number(parsed_number)
                number_type_str = get_number_type(parsed_number)
                
                formats = {
                    "E.164": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.E164),
                    "International": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.INTERNATIONAL),
                    "National": phonenumbers.format_number(parsed_number, phonenumbers.PhoneNumberFormat.NATIONAL),
                }

            console.print("[green]Analysis complete.[/green]\n")
            
            search_links = {
                "Truecaller (Name Lookup)": f"https://www.truecaller.com/search/in/{formats['E.164'].replace('+', '')}",
                "Sync.me (Name Lookup)": f"https://sync.me/search/?number={formats['E.164']}",
                "Google": f"https://www.google.com/search?q=%22{formats['E.164']}%22",
                "Facebook": f"https://www.facebook.com/search/top/?q={formats['E.164']}",
                "LinkedIn": f"https://www.linkedin.com/search/results/all/?keywords={formats['E.164']}",
                "Telegram": f"https://t.me/{formats['E.164'].replace('+', '')}"
            }
            
            console.print(Panel(
                f"[bold]Country:[/bold] [green]{country or 'N/A'}[/green]\n"
                f"[bold]Carrier:[/bold] [green]{service_provider or 'N/A'}[/green]\n"
                f"[bold]Time Zone(s):[/bold] [green]{', '.join(time_zones) if time_zones else 'N/A'}[/green]\n"
                f"[bold]Number Type:[/bold] [green]{number_type_str}[/green]",
                title="[bold yellow]Basic Details[/bold yellow]", border_style="cyan"
            ))

            console.print(Panel(
                "\n".join([f"[bold]{name}:[/bold] [green]{num}[/green]" for name, num in formats.items()]),
                title="[bold yellow]Number Formats[/bold yellow]", border_style="cyan"
            ))

            console.print(Panel(
                "\n".join([f"[bold cyan]{site}:[/bold cyan] [green]{url}[/green]" for site, url in search_links.items()]),
                title="[bold yellow]OSINT Investigation Links[/bold yellow]", border_style="cyan"
            ))
            console.print()

        except phonenumbers.phonenumberutil.NumberParseException as e:
            console.print(f"[bold red]Error: {e}. Please enter a valid number.[/bold red]\n")
        except Exception as e:
            console.print(f"[bold red]An unexpected error occurred: {e}[/bold red]\n")

    Prompt.ask("[yellow]Press Enter to return to the main menu.[/yellow]")