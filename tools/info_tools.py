from rich.panel import Panel
from rich.prompt import Prompt

# நமது சொந்த utility கோப்புகளிலிருந்து இறக்குமதி செய்தல்
from utils.ui import console, clear_screen

def remote_access_info():
    """Provides educational information about Remote Access Trojans (RATs) and screen hacking."""
    clear_screen()
    console.print(Panel("[bold red]Screen Hacking & Remote Access Info[/bold red]", border_style="red"))
    console.print("[bold yellow]DISCLAIMER: Unauthorized access to any computer is illegal. This is for educational purposes only.[/bold yellow]\n")
    
    info_text = """
    [bold]How "Screen Hacking" Works:[/bold]
    "Screen Hacking" is usually achieved using a [bold]Remote Access Trojan (RAT)[/bold]. This is a type of malware that gives an attacker complete control over the victim's computer.

    [bold]Capabilities of a RAT:[/bold]
    -   [bold]View & Control Screen:[/bold] See everything the user does in real-time and control their mouse and keyboard.
    -   [bold]File Management:[/bold] Upload, download, delete, and execute files.
    -   [bold]Keylogging:[/bold] Record every keystroke to steal passwords and private messages.
    -   [bold]Webcam & Mic Spying:[/bold] Activate the camera and microphone secretly.
    -   [bold]System Information:[/bold] Gather details about the computer, network, and installed software.

    [bold]How Attackers Spread RATs:[/bold]
    -   [bold]Phishing Emails:[/bold] Disguised as legitimate attachments (e.g., "invoice.pdf.exe").
    -   [bold]Cracked Software:[/bold] Bundled with pirated games or applications.
    -   [bold]Fake Updates:[/bold] Pop-ups that trick you into installing a malicious "update" for Flash or Java.

    [bold]How Police & Investigators Use This:[/bold]
    In [bold]legal and authorized[/bold] situations, law enforcement might use similar tools (often called "Lawful Interception" tools) with a warrant to monitor a suspect's computer activity as part of a criminal investigation.

    [bold]How to Protect Yourself:[/bold]
    -   Use a reputable Antivirus and Firewall.
    -   NEVER download files from untrusted sources.
    -   Be suspicious of unsolicited emails and attachments.
    -   Keep your operating system and all software fully updated.
    """
    console.print(Panel(info_text, title="[bold cyan]Educational Information[/bold cyan]"))
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")

def fake_link_info():
    """Creates advanced phishing-style links with multiple obfuscation methods."""
    import requests
    import base64
    import urllib.parse
    import random
    import string
    from rich.table import Table
    from rich.columns import Columns

    clear_screen()
    console.print(Panel("[bold red]🔗 ADVANCED PHISHING LINK GENERATOR 🔗[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  DISCLAIMER: Use only for awareness, education, or with permission. Do not use for malicious purposes.[/bold yellow]\n")

    # Get target URL
    real_url = Prompt.ask("[cyan]Enter the real URL you want to disguise[/cyan]", default="https://facebook.com")

    if not real_url.startswith(('http://', 'https://')):
        real_url = 'https://' + real_url

    # Social engineering templates
    templates = {
        '1': ("Facebook Login", "https://facebook.com/login", ["fb", "facebook", "meta", "login"]),
        '2': ("Instagram Login", "https://instagram.com/accounts/login", ["ig", "instagram", "insta", "photo"]),
        '3': ("Google Account", "https://accounts.google.com", ["google", "gmail", "youtube", "drive"]),
        '4': ("Netflix Login", "https://www.netflix.com/login", ["netflix", "streaming", "movies", "tv"]),
        '5': ("PayPal", "https://www.paypal.com/signin", ["paypal", "payment", "money", "bank"]),
        '6': ("Amazon", "https://www.amazon.com/ap/signin", ["amazon", "shopping", "buy", "store"]),
        '7': ("Twitter/X", "https://twitter.com/login", ["twitter", "x", "tweet", "social"]),
        '8': ("Custom Target", real_url, ["custom", "target", "link"])
    }

    console.print("\n[bold cyan]Choose a social engineering template:[/bold cyan]")
    for key, (name, url, keywords) in templates.items():
        console.print(f"[yellow]{key}.[/yellow] {name}")

    template_choice = Prompt.ask("\n[cyan]Select template[/cyan]", choices=list(templates.keys()), default='1')
    selected_template = templates[template_choice]

    # Multiple obfuscation methods
    console.print("\n[bold cyan]Generating multiple obfuscated links...[/bold cyan]")

    with console.status("[bold green]Creating phishing links...[/bold green]", spinner="dots") as status:
        # Method 1: Base64 encoding
        b64_url = base64.urlsafe_b64encode(real_url.encode()).decode()
        method1 = f"https://secure-login-{random.choice(selected_template[2])}.com/?redirect={b64_url}"

        # Method 2: URL encoding
        encoded_url = urllib.parse.quote(real_url, safe='')
        method2 = f"https://{random.choice(selected_template[2])}-auth.net/login?return={encoded_url}"

        # Method 3: Hex encoding
        hex_url = real_url.encode().hex()
        method3 = f"https://account-{random.choice(selected_template[2])}.org/verify?data={hex_url}"

        # Method 4: Double encoding
        double_encoded = urllib.parse.quote(urllib.parse.quote(real_url))
        method4 = f"https://{random.choice(selected_template[2])}-secure.com/auth?next={double_encoded}"

        # Method 5: Fake subdomain
        fake_domains = [
            f"secure.{random.choice(selected_template[2])}.login.com",
            f"auth.{random.choice(selected_template[2])}.account.net",
            f"login.{random.choice(selected_template[2])}.secure.org",
            f"verify.{random.choice(selected_template[2])}.auth.io"
        ]
        method5 = f"https://{random.choice(fake_domains)}/?url={base64.urlsafe_b64encode(real_url.encode()).decode()}"

        # Try multiple URL shorteners
        shorteners = []
        try:
            # TinyURL
            resp = requests.get(f"https://tinyurl.com/api-create.php?url={real_url}", timeout=5)
            if resp.status_code == 200:
                shorteners.append(("TinyURL", resp.text))
        except:
            pass

        try:
            # Bitly (would need API key for real implementation)
            # For demo purposes, we'll simulate
            shorteners.append(("Bitly", f"https://bit.ly/{random.randint(100000, 999999)}"))
        except:
            pass

        try:
            # Shorten URL
            shorteners.append(("Short", f"https://short.url/{random.randint(1000, 9999)}"))
        except:
            pass

    # Display results in a beautiful table
    table = Table(title="[bold red]🔥 GENERATED PHISHING LINKS 🔥[/bold red]")
    table.add_column("[bold cyan]Method[/bold cyan]", style="cyan", no_wrap=True)
    table.add_column("[bold green]Obfuscated Link[/bold green]", style="green")
    table.add_column("[bold yellow]Type[/bold yellow]", style="yellow")

    table.add_row("Base64 Obfuscation", method1, "Parameter Encoding")
    table.add_row("URL Encoding", method2, "Query String")
    table.add_row("Hex Encoding", method3, "Data Encoding")
    table.add_row("Double Encoding", method4, "Nested Encoding")
    table.add_row("Fake Subdomain", method5, "Domain Spoofing")

    console.print(table)

    # Shortened URLs table
    if shorteners:
        short_table = Table(title="[bold blue]📱 SHORTENED URLS 📱[/bold blue]")
        short_table.add_column("[bold cyan]Service[/bold cyan]", style="cyan")
        short_table.add_column("[bold green]Short Link[/bold green]", style="green")

        for service, url in shorteners:
            short_table.add_row(service, url)

        console.print(short_table)

    # Social engineering tips
    tips_panel = Panel(
        """
[bold]🎯 Social Engineering Tips:[/bold]

• [green]Use urgent language:[/green] "Your account will be suspended!"
• [green]Create fear:[/green] "Security breach detected!"
• [green]Offer rewards:[/green] "Verify to receive bonus!"
• [green]Use trusted domains:[/green] Similar looking domains
• [green]Mobile friendly:[/green] Test on mobile devices
• [green]SSL Certificate:[/green] Use HTTPS for credibility

[bold]🛡️ Detection Avoidance:[/bold]

• [yellow]Avoid obvious words:[/yellow] "phish", "hack", "steal"
• [yellow]Use legitimate domains:[/yellow] When possible
• [yellow]Test link previews:[/yellow] How it appears on social media
• [yellow]Use URL shorteners:[/yellow] Hide the real destination
• [yellow]Mobile optimization:[/yellow] Responsive design
        """,
        title="[bold red]🎭 Advanced Phishing Techniques[/bold red]",
        border_style="red"
    )

    console.print(tips_panel)

    # Copy to clipboard option
    console.print("\n[bold cyan]💡 Tip: You can copy any of these links for testing purposes[/bold cyan]")

    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")

def camera_hacking_info():
    """Provides educational information about camera hacking."""
    clear_screen()
    console.print(Panel("[bold red]Camera Hacking Info[/bold red]", border_style="red"))
    console.print("[bold yellow]DISCLAIMER: Unauthorized access to any camera is illegal and a severe invasion of privacy.[/bold yellow]\n")
    
    info_text = """
    [bold]How Camera Hacking Works:[/bold]
    1.  [bold]Malicious Software (Malware):[/bold] An attacker tricks a user into installing software (e.g., a RAT - Remote Access Trojan) that gives them control over the device, including the camera.
    2.  [bold]Phishing:[/bold] Users are sent links to fake websites that request camera permissions. If granted, the site can access the camera.
    3.  [bold]Insecure IoT Devices:[/bold] Many web-connected cameras have default passwords or security flaws that can be exploited.

    [bold]How to Protect Yourself:[/bold]
    -   Cover your webcam when not in use.
    -   Be cautious about links and attachments from unknown sources.
    -   Keep your software and operating system updated.
    -   Use strong, unique passwords for all your accounts and devices.
    """
    console.print(Panel(info_text, title="[bold cyan]Educational Information[/bold cyan]"))
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")