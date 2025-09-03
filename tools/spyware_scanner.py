#!/usr/bin/env python3
"""
Anti-Spyware Removal Tool
This tool scans a website for potential spyware indicators and provides feedback.
"""
import sys
import requests
from PyQt5.QtWidgets import QApplication, QLabel, QMainWindow, QVBoxLayout, QWidget, QPushButton, QLineEdit
from PyQt5.QtCore import Qt

def scan_site(url):
    """Analyzes website content for potential malware"""
    suspicious_patterns = [
        'download', 'update', 'install',
        '.exe', '.bat', '.vbs', '.ps1'
    ]
    try:
        response = requests.get(url, timeout=5)
        # Check URL length
        if len(response.text) > 20_000_000:  # Overload protection (bytes)
            return f"SUSPICIOUS: Large document detected ({len(response.text)/1000}Kb)"
        text = response.text.lower()
        # Search for suspicious keywords
        for pattern in suspicious_patterns:
            if pattern in text and url.count(pattern) < 2:
                return f"POTENTIAL SPOOF: '{pattern}' found"
    except Exception as e:
        return str(e)
    return "Clean: No obvious threats detected"

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    central_widget = QWidget()
    layout = QVBoxLayout(central_widget)
    # URL input field
    url_label = QLabel("Enter website URL:")
    layout.addWidget(url_label, alignment=Qt.AlignTop)
    url_field = QLineEdit()
    layout.addWidget(url_field, alignment=Qt.AlignTop | Qt.AlignLeft)
    # Button and result area
    btn_scan = QPushButton("Scan")
    result_text = QLabel("Enter a website to scan...")
    def on_click():
        target_url = url_field.text().strip()
        if not target_url.startswith("http://") and not target_url.startswith("https://"):
            target_url = "http://" + target_url
        result_text.setText(scan_site(target_url))
    # Connect button click event
    btn_scan.clicked.connect(on_click)
    layout.addWidget(btn_scan)
    layout.addWidget(result_text, stretch=1)
    # Make window
    window.setWindowTitle("Anti-Spyware Scanner")
    window.setCentralWidget(central_widget)
    window.resize(600, 400)  # Reasonable size for web scanning
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
