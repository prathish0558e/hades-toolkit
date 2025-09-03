import ssl
import socket
import datetime
import time
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    """SSL Certificate Analysis Tool"""
    clear_screen()
    print_banner("SSL Checker")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold red]🔥 SSL CERTIFICATE ANALYZER - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: Use only for authorized security testing![/bold yellow]\n")

    target = Prompt.ask("[cyan]Enter domain or IP to analyze[/cyan]")

    # Remove protocol if present
    if '://' in target:
        target = target.split('://')[1]

    # Remove port if present
    if ':' in target:
        target = target.split(':')[0]

    console.print(f"\n[bold cyan]🔍 Analyzing SSL certificate for: {target}[/bold cyan]")

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task("Connecting to server...", total=4)

        try:
            # Create SSL context
            context = ssl.create_default_context()
            context.check_hostname = False
            context.verify_mode = ssl.CERT_NONE

            progress.update(task, advance=1, description="Establishing SSL connection...")

            # Connect to server
            with socket.create_connection((target, 443), timeout=10) as sock:
                progress.update(task, advance=1, description="Performing SSL handshake...")

                with context.wrap_socket(sock, server_hostname=target) as ssock:
                    progress.update(task, advance=1, description="Retrieving certificate...")

                    # Get certificate
                    cert = ssock.getpeercert(binary_form=True)
                    cert_pem = ssl.DER_cert_to_PEM_cert(cert)
                    cert_obj = ssl.DER_cert_to_PEM_cert(cert)
                    x509_cert = ssl.load_certificate(ssl.PEM_CERT, cert_obj)

                    progress.update(task, advance=1, description="Analyzing certificate...")

                    # Extract certificate information
                    cert_info = extract_cert_info(x509_cert, target)

                    progress.update(task, advance=1, description="Analysis complete!")

        except ssl.SSLError as e:
            console.print(f"[bold red]❌ SSL Error: {str(e)}[/bold red]")
            return
        except socket.gaierror:
            console.print(f"[bold red]❌ Could not resolve hostname: {target}[/bold red]")
            return
        except socket.timeout:
            console.print(f"[bold red]❌ Connection timeout[/bold red]")
            return
        except Exception as e:
            console.print(f"[bold red]❌ Error: {str(e)}[/bold red]")
            return

    # Display results
    display_cert_info(cert_info)

def extract_cert_info(cert, hostname):
    """Extract certificate information"""
    info = {}

    # Basic information
    info['hostname'] = hostname
    info['subject'] = dict(cert.get_subject().get_components())
    info['issuer'] = dict(cert.get_issuer().get_components())

    # Dates
    info['not_before'] = cert.get_notBefore().decode('ascii')
    info['not_after'] = cert.get_notAfter().decode('ascii')

    # Calculate days until expiry
    expiry_date = datetime.datetime.strptime(info['not_after'], '%Y%m%d%H%M%SZ')
    days_until_expiry = (expiry_date - datetime.datetime.utcnow()).days
    info['days_until_expiry'] = days_until_expiry

    # Serial number
    info['serial_number'] = str(cert.get_serial_number())

    # Version
    info['version'] = cert.get_version() + 1

    # Signature algorithm
    info['signature_algorithm'] = cert.get_signature_algorithm().decode('ascii')

    # Public key info
    public_key = cert.get_pubkey()
    info['public_key_bits'] = public_key.bits()
    info['public_key_type'] = 'RSA' if public_key.type() == 6 else 'Unknown'

    # Subject Alternative Names
    try:
        san_extension = None
        for i in range(cert.get_extension_count()):
            ext = cert.get_extension(i)
            if ext.get_short_name() == b'subjectAltName':
                san_extension = ext
                break

        if san_extension:
            san_list = str(san_extension).split(', ')
            info['subject_alt_names'] = san_list
        else:
            info['subject_alt_names'] = []
    except:
        info['subject_alt_names'] = []

    # Certificate validation
    info['is_expired'] = days_until_expiry < 0
    info['is_self_signed'] = info['subject'].get(b'O') == info['issuer'].get(b'O') and info['subject'].get(b'CN') == info['issuer'].get(b'CN')

    return info

def display_cert_info(info):
    """Display certificate information"""
    console.print(f"\n[bold green]🔒 SSL CERTIFICATE ANALYSIS RESULTS[/bold green]")
    console.print("=" * 60)

    # Main certificate info
    table = Table()
    table.add_column("Property", style="cyan", no_wrap=True)
    table.add_column("Value", style="yellow")

    # Subject information
    subject_str = ""
    for key, value in info['subject'].items():
        subject_str += f"{key.decode('utf-8')}={value.decode('utf-8')}, "
    table.add_row("Subject", subject_str.rstrip(', '))

    # Issuer information
    issuer_str = ""
    for key, value in info['issuer'].items():
        issuer_str += f"{key.decode('utf-8')}={value.decode('utf-8')}, "
    table.add_row("Issuer", issuer_str.rstrip(', '))

    # Validity
    table.add_row("Valid From", info['not_before'])
    table.add_row("Valid Until", info['not_after'])

    # Expiry status
    if info['is_expired']:
        table.add_row("Status", "[bold red]EXPIRED[/bold red]")
    elif info['days_until_expiry'] < 30:
        table.add_row("Status", f"[bold yellow]EXPIRES SOON ({info['days_until_expiry']} days)[/bold yellow]")
    else:
        table.add_row("Status", f"[bold green]VALID ({info['days_until_expiry']} days)[/bold green]")

    # Technical details
    table.add_row("Version", f"v{info['version']}")
    table.add_row("Serial Number", info['serial_number'])
    table.add_row("Signature Algorithm", info['signature_algorithm'])
    table.add_row("Public Key", f"{info['public_key_type']} {info['public_key_bits']} bits")

    # Self-signed check
    if info['is_self_signed']:
        table.add_row("Certificate Type", "[bold yellow]SELF-SIGNED[/bold yellow]")
    else:
        table.add_row("Certificate Type", "[bold green]CA-SIGNED[/bold green]")

    console.print(table)

    # Subject Alternative Names
    if info['subject_alt_names']:
        console.print(f"\n[bold cyan]🌐 SUBJECT ALTERNATIVE NAMES:[/bold cyan]")
        for san in info['subject_alt_names']:
            console.print(f"• {san}")

    # Security analysis
    console.print(f"\n[bold yellow]🔍 SECURITY ANALYSIS:[/bold yellow]")

    issues = []

    if info['is_expired']:
        issues.append("❌ Certificate is expired")
    elif info['days_until_expiry'] < 30:
        issues.append(f"⚠️  Certificate expires in {info['days_until_expiry']} days")

    if info['is_self_signed']:
        issues.append("⚠️  Self-signed certificate (not recommended for production)")

    if info['public_key_bits'] < 2048:
        issues.append(f"⚠️  Weak public key ({info['public_key_bits']} bits)")

    if not issues:
        console.print("[bold green]✅ No security issues found[/bold green]")
    else:
        for issue in issues:
            console.print(issue)

    # Recommendations
    console.print(f"\n[bold cyan]💡 RECOMMENDATIONS:[/bold cyan]")
    if info['days_until_expiry'] < 90:
        console.print("• Renew certificate before expiry")
    if info['public_key_bits'] < 2048:
        console.print("• Consider upgrading to 2048-bit or higher key")
    if info['is_self_signed']:
        console.print("• Obtain certificate from trusted CA for production use")
    console.print("• Enable HSTS header for additional security")
    console.print("• Regularly monitor certificate expiry")

    Prompt.ask("\n[cyan]Press Enter to continue[/cyan]")
