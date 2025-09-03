import os
import time
import platform
import psutil
from rich.panel import Panel
from rich.prompt import Prompt
from rich.progress import Progress, SpinnerColumn, TextColumn
from utils.ui import console, clear_screen

def run():
    """Extreme Level Digital Forensics Tool"""
    clear_screen()
    console.print(Panel("[bold red]🔥 DIGITAL FORENSICS - EXTREME LEVEL 🔥[/bold red]", border_style="red"))
    console.print("[bold yellow]⚠️  WARNING: This tool performs system analysis. Use only on authorized systems![/bold yellow]\n")
    
    console.print("[bold cyan]Select forensic analysis type:[/bold cyan]")
    console.print("1. System Information Gathering")
    console.print("2. Process Analysis")
    console.print("3. Network Connections")
    console.print("4. File System Analysis")
    console.print("5. Memory Analysis")
    
    choice = Prompt.ask("[cyan]Enter your choice (1-5)[/cyan]")
    
    if choice == '1':
        system_info()
    elif choice == '2':
        process_analysis()
    elif choice == '3':
        network_connections()
    elif choice == '4':
        file_system_analysis()
    elif choice == '5':
        memory_analysis()
    else:
        console.print("[bold red]Invalid choice![/bold red]")

def system_info():
    """Gather comprehensive system information"""
    console.print("\n[bold cyan]🔍 SYSTEM INFORMATION GATHERING[/bold cyan]")
    
    with console.status("[bold green]Collecting system data...[/bold green]", spinner="dots") as status:
        time.sleep(2)
        
        info = {
            'OS': platform.system() + " " + platform.release(),
            'Architecture': platform.machine(),
            'Processor': platform.processor(),
            'Python Version': platform.python_version(),
            'Hostname': platform.node(),
            'CPU Cores': psutil.cpu_count(),
            'Total Memory': f"{psutil.virtual_memory().total / (1024**3):.2f} GB",
            'Available Memory': f"{psutil.virtual_memory().available / (1024**3):.2f} GB",
            'Disk Usage': f"{psutil.disk_usage('/').percent}% used"
        }
        
        for key, value in info.items():
            console.print(f"[green]{key}:[/green] [cyan]{value}[/cyan]")
        
        # Boot time
        boot_time = psutil.boot_time()
        console.print(f"[green]System Boot Time:[/green] [cyan]{time.ctime(boot_time)}[/cyan]")

def process_analysis():
    """Analyze running processes"""
    console.print("\n[bold cyan]🔍 PROCESS ANALYSIS[/bold cyan]")
    
    with console.status("[bold green]Analyzing processes...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_percent']):
            try:
                processes.append(proc.info)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Sort by CPU usage
        processes.sort(key=lambda x: x['cpu_percent'], reverse=True)
        
        console.print(Panel(
            "\n".join([f"[green]PID {p['pid']}[/green] - [cyan]{p['name']}[/cyan] - CPU: {p['cpu_percent']:.1f}% - MEM: {p['memory_percent']:.1f}%" 
                      for p in processes[:10]]),
            title="[bold yellow]Top 10 Processes by CPU Usage[/bold yellow]", border_style="yellow"
        ))

def network_connections():
    """Analyze network connections"""
    console.print("\n[bold cyan]🔍 NETWORK CONNECTIONS ANALYSIS[/bold cyan]")
    
    with console.status("[bold green]Analyzing network connections...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        connections = psutil.net_connections()
        connection_info = []
        
        for conn in connections:
            if conn.status == 'ESTABLISHED':
                try:
                    proc = psutil.Process(conn.pid)
                    connection_info.append({
                        'pid': conn.pid,
                        'process': proc.name(),
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    })
                except:
                    connection_info.append({
                        'pid': conn.pid or 'N/A',
                        'process': 'Unknown',
                        'local': f"{conn.laddr.ip}:{conn.laddr.port}",
                        'remote': f"{conn.raddr.ip}:{conn.raddr.port}" if conn.raddr else "N/A"
                    })
        
        if connection_info:
            console.print(Panel(
                "\n".join([f"[green]PID {c['pid']}[/green] - [cyan]{c['process']}[/cyan]\n  Local: {c['local']} ↔ Remote: {c['remote']}" 
                          for c in connection_info[:10]]),
                title="[bold yellow]Active Network Connections[/bold yellow]", border_style="yellow"
            ))
        else:
            console.print("[yellow]No active connections found[/yellow]")

def file_system_analysis():
    """Analyze file system"""
    console.print("\n[bold cyan]🔍 FILE SYSTEM ANALYSIS[/bold cyan]")
    
    path = Prompt.ask("[cyan]Enter directory path to analyze[/cyan]", default="/home")
    
    if not os.path.exists(path):
        console.print(f"[bold red]Path does not exist: {path}[/bold red]")
        return
    
    with console.status("[bold green]Analyzing file system...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        total_files = 0
        total_dirs = 0
        file_types = {}
        
        for root, dirs, files in os.walk(path):
            total_dirs += len(dirs)
            for file in files:
                total_files += 1
                ext = os.path.splitext(file)[1].lower()
                if ext in file_types:
                    file_types[ext] += 1
                else:
                    file_types[ext] = 1
        
        console.print(f"[green]Total Directories:[/green] [cyan]{total_dirs}[/cyan]")
        console.print(f"[green]Total Files:[/green] [cyan]{total_files}[/cyan]")
        
        if file_types:
            top_types = sorted(file_types.items(), key=lambda x: x[1], reverse=True)[:10]
            console.print(Panel(
                "\n".join([f"[cyan]{ext}[/cyan]: {count} files" for ext, count in top_types]),
                title="[bold yellow]Top File Types[/bold yellow]", border_style="yellow"
            ))

def memory_analysis():
    """Analyze system memory"""
    console.print("\n[bold cyan]🔍 MEMORY ANALYSIS[/bold cyan]")
    
    with console.status("[bold green]Analyzing memory usage...[/bold green]", spinner="dots") as status:
        time.sleep(1)
        
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        
        console.print(f"[green]Total Memory:[/green] [cyan]{memory.total / (1024**3):.2f} GB[/cyan]")
        console.print(f"[green]Available Memory:[/green] [cyan]{memory.available / (1024**3):.2f} GB[/cyan]")
        console.print(f"[green]Used Memory:[/green] [cyan]{memory.used / (1024**3):.2f} GB ({memory.percent}%)[/cyan]")
        console.print(f"[green]Memory Usage:[/green] [cyan]{memory.percent}%[/cyan]")
        
        console.print(f"\n[green]Swap Total:[/green] [cyan]{swap.total / (1024**3):.2f} GB[/cyan]")
        console.print(f"[green]Swap Used:[/green] [cyan]{swap.used / (1024**3):.2f} GB ({swap.percent}%)[/cyan]")
        console.print(f"[green]Swap Free:[/green] [cyan]{swap.free / (1024**3):.2f} GB[/cyan]")
        
        # Top memory consuming processes
        processes = []
        for proc in psutil.process_iter(['pid', 'name', 'memory_percent']):
            try:
                processes.append(proc.info)
            except:
                continue
        
        processes.sort(key=lambda x: x['memory_percent'], reverse=True)
        
        console.print(Panel(
            "\n".join([f"[green]PID {p['pid']}[/green] - [cyan]{p['name']}[/cyan] - MEM: {p['memory_percent']:.1f}%" 
                      for p in processes[:10]]),
            title="[bold yellow]Top 10 Memory Consuming Processes[/bold yellow]", border_style="yellow"
        ))
    
    Prompt.ask("\n[yellow]Press Enter to return to the main menu.[/yellow]")
