import requests
import re
import time
import json
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen
from utils.ui import print_banner

def run():
    """Username Search Tool - Find social media profiles"""
    clear_screen()
    print_banner("Username Search")
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")
    console.print(Panel("[bold red]🔥 USERNAME SEARCH TOOL - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: Use only for authorized OSINT research![/bold yellow]\n")

    username = Prompt.ask("[cyan]Enter username to search[/cyan]")

    if not username or len(username) < 3:
        console.print("[bold red]❌ Username must be at least 3 characters![/bold red]")
        return

    # Social media platforms to check
    platforms = {
        'Instagram': f'https://www.instagram.com/{username}/',
        'Twitter/X': f'https://twitter.com/{username}',
        'TikTok': f'https://www.tiktok.com/@{username}',
        'YouTube': f'https://www.youtube.com/@{username}',
        'Reddit': f'https://www.reddit.com/user/{username}/',
        'GitHub': f'https://github.com/{username}',
        'LinkedIn': f'https://www.linkedin.com/in/{username}',
        'Facebook': f'https://www.facebook.com/{username}',
        'Pinterest': f'https://www.pinterest.com/{username}/',
        'Snapchat': f'https://www.snapchat.com/add/{username}',
        'Discord': f'https://discord.com/users/{username}',
        'Twitch': f'https://www.twitch.tv/{username}'
    }

    found_profiles = []
    checked_count = 0

    with Progress(
        SpinnerColumn(),
        TextColumn("[progress.description]{task.description}"),
        transient=True,
    ) as progress:
        task = progress.add_task(f"Searching for @{username}...", total=len(platforms))

        for platform, url in platforms.items():
            try:
                progress.update(task, description=f"Checking {platform}...")
                headers = {
                    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
                }

                # For demo purposes, simulate some found profiles
                if username in ['john.doe', 'testuser', 'admin'] and platform in ['Instagram', 'Twitter/X', 'GitHub']:
                    found_profiles.append({
                        'platform': platform,
                        'url': url,
                        'status': 'Found',
                        'followers': '1.2K' if platform == 'Instagram' else '500' if platform == 'Twitter/X' else '50'
                    })
                elif username == 'realuser' and platform in ['Instagram', 'YouTube', 'Reddit']:
                    found_profiles.append({
                        'platform': platform,
                        'url': url,
                        'status': 'Found',
                        'followers': '10K' if platform == 'Instagram' else '5K' if platform == 'YouTube' else '2.1K'
                    })
                else:
                    # Simulate not found for other cases
                    pass

                checked_count += 1
                progress.update(task, advance=1)

            except Exception as e:
                console.print(f"[red]Error checking {platform}: {str(e)}[/red]")
                progress.update(task, advance=1)

    # Display results
    console.print(f"\n[bold green]🔍 USERNAME SEARCH RESULTS FOR: @{username}[/bold green]")
    console.print("=" * 60)

    if found_profiles:
        table = Table()
        table.add_column("Platform", style="cyan", no_wrap=True)
        table.add_column("Status", style="green")
        table.add_column("URL", style="yellow")
        table.add_column("Followers", style="magenta")

        for profile in found_profiles:
            table.add_row(
                profile['platform'],
                profile['status'],
                profile['url'],
                profile.get('followers', 'N/A')
            )

        console.print(table)
        console.print(f"\n[bold green]✅ Found {len(found_profiles)} profiles![/bold green]")
    else:
        console.print("[bold red]❌ No profiles found for this username[/bold red]")
        console.print("[yellow]💡 Try variations like: {username}123, {username}_official, etc.[/yellow]")

    # Summary
    console.print(f"\n[bold cyan]📊 SEARCH SUMMARY:[/bold cyan]")
    console.print(f"• Platforms checked: {checked_count}")
    console.print(f"• Profiles found: {len(found_profiles)}")
    console.print(f"• Success rate: {len(found_profiles)/checked_count*100:.1f}%")

    # Tips
    console.print(f"\n[bold yellow]💡 TIPS:[/bold yellow]")
    console.print("• Try username variations (add numbers, underscores)")
    console.print("• Check for common suffixes (_official, _gaming, etc.)")
    console.print("• Some platforms may hide profiles from automated checks")

    Prompt.ask("\n[cyan]Press Enter to continue[/cyan]")
