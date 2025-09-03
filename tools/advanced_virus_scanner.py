import os
import hashlib
import threading
import logging
from tkinter import Tk, Label, Button, Entry, filedialog, messagebox, Text, Scrollbar, END
from tkinter import ttk

# Sample malware signatures (expand with real hashes from sources like VirusTotal)
MALWARE_SIGNATURES = {
    'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855': 'Known Trojan',
    # Add more hashes here
}

logging.basicConfig(filename='virus_scan.log', level=logging.INFO, format='%(asctime)s - %(message)s')

class VirusScanner:
    def __init__(self):
        self.suspicious_files = []
        self.quarantine_dir = os.path.join(os.getcwd(), 'quarantine')
        os.makedirs(self.quarantine_dir, exist_ok=True)

    def calculate_hash(self, file_path):
        hash_md5 = hashlib.md5()
        try:
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_md5.update(chunk)
            return hash_md5.hexdigest()
        except Exception as e:
            logging.error(f"Error hashing {file_path}: {e}")
            return None

    def scan_file(self, file_path):
        file_hash = self.calculate_hash(file_path)
        if file_hash and file_hash in MALWARE_SIGNATURES:
            self.suspicious_files.append((file_path, MALWARE_SIGNATURES[file_hash]))
            logging.warning(f"Malware detected: {file_path} - {MALWARE_SIGNATURES[file_hash]}")
        elif self.is_suspicious(file_path):
            self.suspicious_files.append((file_path, 'Heuristic: Suspicious file'))
            logging.warning(f"Suspicious file: {file_path}")

    def is_suspicious(self, file_path):
        # Simple heuristics: executable in temp dirs, large scripts, etc.
        if file_path.endswith(('.exe', '.bat', '.scr')) and 'temp' in file_path.lower():
            return True
        if file_path.endswith('.py') and os.path.getsize(file_path) > 1000000:  # >1MB Python file
            return True
        return False

    def scan_directory(self, directory, progress_callback=None):
        threads = []
        for root, dirs, files in os.walk(directory):
            for file in files:
                file_path = os.path.join(root, file)
                thread = threading.Thread(target=self.scan_file, args=(file_path,))
                threads.append(thread)
                thread.start()
                if progress_callback:
                    progress_callback()
        for thread in threads:
            thread.join()

    def quarantine_file(self, file_path):
        try:
            os.rename(file_path, os.path.join(self.quarantine_dir, os.path.basename(file_path)))
            logging.info(f"Quarantined: {file_path}")
        except Exception as e:
            logging.error(f"Failed to quarantine {file_path}: {e}")

def gui_main():
    scanner = VirusScanner()
    root = Tk()
    root.title("Advanced Virus Scanner")

    Label(root, text="Select Directory to Scan:").pack()
    dir_var = Entry(root)
    dir_var.pack()

    def browse_dir():
        directory = filedialog.askdirectory()
        if directory:
            dir_var.delete(0, END)
            dir_var.insert(0, directory)

    Button(root, text="Browse", command=browse_dir).pack()

    progress = ttk.Progressbar(root, orient="horizontal", mode="indeterminate")
    progress.pack()

    result_text = Text(root, height=10)
    scrollbar = Scrollbar(root, command=result_text.yview)
    result_text.config(yscrollcommand=scrollbar.set)
    result_text.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")

    def start_scan():
        directory = dir_var.get()
        if not directory or not os.path.isdir(directory):
            messagebox.showerror("Error", "Invalid directory")
            return
        progress.start()
        scanner.suspicious_files = []
        scanner.scan_directory(directory, lambda: progress.step(1))
        progress.stop()
        result_text.delete(1.0, END)
        if scanner.suspicious_files:
            for file, reason in scanner.suspicious_files:
                result_text.insert(END, f"{file}: {reason}\n")
        else:
            result_text.insert(END, "No threats detected.\n")

    def quarantine_selected():
        selected = result_text.get("sel.first", "sel.last")
        if selected:
            file_path = selected.split(':')[0].strip()
            scanner.quarantine_file(file_path)
            messagebox.showinfo("Quarantined", f"{file_path} moved to quarantine.")

    Button(root, text="Start Scan", command=start_scan).pack()
    Button(root, text="Quarantine Selected", command=quarantine_selected).pack()

    root.mainloop()

def main():
    from utils.ui import print_banner
    print_banner("Hades Toolkit")
    if len(sys.argv) > 1 and sys.argv[1] == '--gui':
        gui_main()
    else:
        scanner = VirusScanner()
        directory = input("Enter directory to scan: ").strip()
        if os.path.isdir(directory):
            scanner.scan_directory(directory)
            if scanner.suspicious_files:
                print("Suspicious files:")
                for file, reason in scanner.suspicious_files:
                    print(f"{file}: {reason}")
            else:
                print("No threats detected.")
        else:
            print("Invalid directory.")

if __name__ == "__main__":
    import sys
    main()
