import requests
import json
import re
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from utils.ui import console, clear_screen

def extract_username(url):
    """Extract username from social media URL"""
    patterns = {
        'instagram': r'instagram\.com/([a-zA-Z0-9_.]+)',
        'twitter': r'twitter\.com/([a-zA-Z0-9_]+)',
        'facebook': r'facebook\.com/([a-zA-Z0-9.]+)',
        'linkedin': r'linkedin\.com/in/([a-zA-Z0-9-]+)',
        'github': r'github\.com/([a-zA-Z0-9-]+)',
        'youtube': r'youtube\.com/(?:user/|channel/|c/)?([a-zA-Z0-9_-]+)',
        'tiktok': r'tiktok\.com/@([a-zA-Z0-9_.]+)',
        'reddit': r'reddit\.com/u/([a-zA-Z0-9_-]+)'
    }

    for platform, pattern in patterns.items():
        match = re.search(pattern, url)
        if match:
            return platform, match.group(1)
    return None, None

def check_instagram(username):
    """Check Instagram profile information"""
    try:
        url = f"https://www.instagram.com/{username}/"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            # Extract basic info from page (limited due to Instagram's restrictions)
            info = {
                'username': username,
                'url': url,
                'status': 'Profile exists',
                'is_private': 'is_private' in response.text,
                'verified': '"is_verified":true' in response.text
            }
            return info
        else:
            return {'username': username, 'status': 'Profile not found'}
    except:
        return {'username': username, 'status': 'Error checking profile'}

def check_twitter(username):
    """Check Twitter profile information"""
    try:
        url = f"https://twitter.com/{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            info = {
                'username': username,
                'url': url,
                'status': 'Profile exists'
            }
            return info
        else:
            return {'username': username, 'status': 'Profile not found'}
    except:
        return {'username': username, 'status': 'Error checking profile'}

def check_github(username):
    """Check GitHub profile information"""
    try:
        url = f"https://api.github.com/users/{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            data = response.json()
            info = {
                'username': data.get('login', username),
                'name': data.get('name', 'N/A'),
                'bio': data.get('bio', 'N/A'),
                'location': data.get('location', 'N/A'),
                'company': data.get('company', 'N/A'),
                'blog': data.get('blog', 'N/A'),
                'public_repos': data.get('public_repos', 0),
                'followers': data.get('followers', 0),
                'following': data.get('following', 0),
                'created_at': data.get('created_at', 'N/A'),
                'url': data.get('html_url', f"https://github.com/{username}")
            }
            return info
        else:
            return {'username': username, 'status': 'Profile not found'}
    except:
        return {'username': username, 'status': 'Error checking profile'}

def check_linkedin(username):
    """Check LinkedIn profile information"""
    try:
        url = f"https://www.linkedin.com/in/{username}"
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)

        if response.status_code == 200:
            info = {
                'username': username,
                'url': url,
                'status': 'Profile exists'
            }
            return info
        else:
            return {'username': username, 'status': 'Profile not found'}
    except:
        return {'username': username, 'status': 'Error checking profile'}

def social_media_osint():
    """Main Social Media OSINT tool function"""
    clear_screen()

    console.print(Panel(
        "[bold cyan]🔍 Social Media OSINT Tool[/bold cyan]\n\n"
        "This tool helps you gather information about social media profiles.\n"
        "Enter a username or profile URL to analyze.",
        title="[bold yellow]Social Media OSINT[/bold yellow]",
        border_style="cyan"
    ))

    console.print("\n[bold green]Supported Platforms:[/bold green]")
    platforms = [
        "Instagram", "Twitter/X", "Facebook", "LinkedIn",
        "GitHub", "YouTube", "TikTok", "Reddit"
    ]
    for i, platform in enumerate(platforms, 1):
        console.print(f"[cyan]{i}.[/cyan] {platform}")

    while True:
        console.print("\n" + "="*60)
        choice = Prompt.ask(
            "[cyan]Choose an option[/cyan]",
            choices=['1', '2', '3', '4', '5', '6', '7', '8', '9', '0']
        )

        if choice == '0':
            break

        platform_map = {
            '1': 'instagram',
            '2': 'twitter',
            '3': 'facebook',
            '4': 'linkedin',
            '5': 'github',
            '6': 'youtube',
            '7': 'tiktok',
            '8': 'reddit'
        }

        platform = platform_map.get(choice)
        if not platform:
            console.print("[bold red]Invalid choice![/bold red]")
            continue

        username = Prompt.ask(f"[cyan]Enter {platform} username[/cyan]")

        console.print(f"\n[bold yellow]🔍 Analyzing {platform} profile: @{username}[/bold yellow]")

        if platform == 'instagram':
            result = check_instagram(username)
        elif platform == 'twitter':
            result = check_twitter(username)
        elif platform == 'github':
            result = check_github(username)
        elif platform == 'linkedin':
            result = check_linkedin(username)
        else:
            console.print(f"[yellow]Detailed checking for {platform} not implemented yet.[/yellow]")
            continue

        # Display results
        table = Table(title=f"[bold cyan]{platform.title()} Profile Information[/bold cyan]")
        table.add_column("Field", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for key, value in result.items():
            table.add_row(key.replace('_', ' ').title(), str(value))

        console.print(table)

        # Ask to continue
        if Prompt.ask("[cyan]Check another profile?[/cyan]", choices=['y', 'n'], default='y') == 'n':
            break

    console.print("[bold green]Returning to main menu...[/bold green]")

if __name__ == "__main__":
    social_media_osint()
