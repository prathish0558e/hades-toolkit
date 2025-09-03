import os


# Try pyexiftool, else fallback to subprocess
try:
    import pyexiftool
    EXIFTOOL_AVAILABLE = 'pyexiftool'
except ImportError:
    import subprocess
    EXIFTOOL_AVAILABLE = 'subprocess' if subprocess.call(['which', 'exiftool'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL) == 0 else False

try:
    from PIL import Image
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False

import requests
from rich.panel import Panel
from rich.prompt import Prompt
from rich.table import Table
from rich.console import Console
from utils.ui import console, clear_screen
import json
import hashlib
from datetime import datetime
import re

def get_file_hash(file_path):
    """Calculate file hash"""
    hash_md5 = hashlib.md5()
    hash_sha1 = hashlib.sha1()
    hash_sha256 = hashlib.sha256()

    try:
        with open(file_path, "rb") as f:
            for chunk in iter(lambda: f.read(4096), b""):
                hash_md5.update(chunk)
                hash_sha1.update(chunk)
                hash_sha256.update(chunk)
        return {
            'MD5': hash_md5.hexdigest(),
            'SHA1': hash_sha1.hexdigest(),
            'SHA256': hash_sha256.hexdigest()
        }
    except:
        return {'Error': 'Could not calculate hash'}

def extract_image_metadata(file_path):
    """Extract EXIF metadata from images"""
    if not EXIFTOOL_AVAILABLE:
        return {'Error': 'exiftool not available. Install with: pip install pyexiftool or install exiftool binary.'}

    try:
        if EXIFTOOL_AVAILABLE == 'pyexiftool':
            with pyexiftool.ExifToolHelper() as et:
                metadata = et.get_metadata(file_path)[0]
        elif EXIFTOOL_AVAILABLE == 'subprocess':
            import json
            result = subprocess.run(['exiftool', '-j', file_path], capture_output=True, text=True)
            metadata = json.loads(result.stdout)[0] if result.stdout else {}
        else:
            return {'Error': 'No exiftool method available.'}

        # Filter out common metadata
        important_metadata = {}
        for key, value in metadata.items():
            if any(keyword in key.lower() for keyword in [
                'datetime', 'gps', 'camera', 'software', 'make', 'model',
                'resolution', 'orientation', 'flash', 'focal', 'iso',
                'exposure', 'aperture', 'shutter', 'lens', 'artist',
                'copyright', 'description', 'comment'
            ]):
                important_metadata[key] = value

        return important_metadata
    except Exception as e:
        return {'Error': f'Could not extract EXIF data: {str(e)}'}

def extract_file_metadata(file_path):
    """Extract basic file metadata"""
    try:
        stat = os.stat(file_path)
        metadata = {
            'File Path': file_path,
            'File Size': f"{stat.st_size} bytes",
            'Created': datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
            'Modified': datetime.fromtimestamp(stat.st_mtime).strftime('%Y-%m-%d %H:%M:%S'),
            'Accessed': datetime.fromtimestamp(stat.st_atime).strftime('%Y-%m-%d %H:%M:%S'),
            'File Extension': os.path.splitext(file_path)[1].lower(),
            'File Name': os.path.basename(file_path)
        }
        return metadata
    except Exception as e:
        return {'Error': f'Could not extract file metadata: {str(e)}'}

def analyze_text_file(file_path):
    """Analyze text files for patterns"""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            content = f.read()

        analysis = {
            'Total Characters': len(content),
            'Total Lines': len(content.split('\n')),
            'Total Words': len(content.split()),
            'Contains Email': bool(re.search(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)),
            'Contains URL': bool(re.search(r'http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', content)),
            'Contains Phone': bool(re.search(r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b', content)),
            'Contains IP Address': bool(re.search(r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', content))
        }
        return analysis
    except Exception as e:
        return {'Error': f'Could not analyze text file: {str(e)}'}

def metadata_extractor():
    """Main metadata extractor function"""
    clear_screen()

    console.print(Panel(
        "[bold cyan]📁 Metadata Extractor[/bold cyan]\n\n"
        "Extract hidden metadata from files including:\n"
        "• File hashes (MD5, SHA1, SHA256)\n"
        "• EXIF data from images\n"
        "• File system metadata\n"
        "• Text file analysis\n\n"
        "[bold red]⚠️  Note: This tool requires exiftool to be installed[/bold red]",
        title="[bold yellow]Metadata Extractor[/bold yellow]",
        border_style="cyan"
    ))
    console.print("[bold magenta]Instagram: Prathi_hades[/bold magenta]")

    while True:
        console.print("\n" + "="*60)
        file_path = Prompt.ask("[cyan]Enter file path to analyze[/cyan]")

        if not os.path.exists(file_path):
            console.print("[bold red]File not found![/bold red]")
            continue

        console.print(f"\n[bold yellow]🔍 Analyzing: {file_path}[/bold yellow]")

        # Basic file metadata
        console.print("\n[bold cyan]📄 Basic File Information:[/bold cyan]")
        basic_metadata = extract_file_metadata(file_path)
        table = Table()
        table.add_column("Property", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")

        for key, value in basic_metadata.items():
            table.add_row(key, str(value))
        console.print(table)

        # File hashes
        console.print("\n[bold cyan]🔐 File Hashes:[/bold cyan]")
        hashes = get_file_hash(file_path)
        hash_table = Table()
        hash_table.add_column("Algorithm", style="cyan", no_wrap=True)
        hash_table.add_column("Hash", style="magenta")

        for algorithm, hash_value in hashes.items():
            hash_table.add_row(algorithm, hash_value)
        console.print(hash_table)

        # Check if it's an image file
        image_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff', '.webp']
        if os.path.splitext(file_path)[1].lower() in image_extensions:
            console.print("\n[bold cyan]📷 Image EXIF Metadata:[/bold cyan]")
            exif_data = extract_image_metadata(file_path)
            if exif_data:
                exif_table = Table()
                exif_table.add_column("EXIF Tag", style="cyan", no_wrap=True)
                exif_table.add_column("Value", style="magenta")

                for tag, value in exif_data.items():
                    exif_table.add_row(tag, str(value))
                console.print(exif_table)
            else:
                console.print("[yellow]No EXIF data found or exiftool not available.[/yellow]")

        # Check if it's a text file
        text_extensions = ['.txt', '.md', '.py', '.js', '.html', '.css', '.json', '.xml', '.csv']
        if os.path.splitext(file_path)[1].lower() in text_extensions:
            console.print("\n[bold cyan]📝 Text File Analysis:[/bold cyan]")
            text_analysis = analyze_text_file(file_path)
            text_table = Table()
            text_table.add_column("Analysis", style="cyan", no_wrap=True)
            text_table.add_column("Result", style="magenta")

            for key, value in text_analysis.items():
                text_table.add_row(key, str(value))
            console.print(text_table)

        # Ask to analyze another file
        if Prompt.ask("[cyan]Analyze another file?[/cyan]", choices=['y', 'n'], default='y') == 'n':
            break

    console.print("[bold green]Returning to main menu...[/bold green]")

if __name__ == "__main__":
    metadata_extractor()
