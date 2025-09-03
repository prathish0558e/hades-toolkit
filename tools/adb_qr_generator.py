import qrcode
import sys

def main():
    from utils.ui import print_banner
    print_banner("Hades Toolkit")
    print("\n=== ADB Wireless Pairing QR Code Generator ===\n")
    ip = input("Enter your device's IP address (e.g., 192.168.1.100): ").strip()
    port = input("Enter the pairing port (e.g., 12345): ").strip()
    pairing_code = input("Enter the pairing code (optional, press Enter to skip): ").strip()

    # Format for ADB QR code: 'WIFI:T:ADB;S:<ip>:<port>;P:<pairing_code>;;'
    # But Android expects: 'WIFI:T:ADB;S:<ip>:<port>;P:<pairing_code>;;' or just 'adb://<ip>:<port>'
    if pairing_code:
        qr_data = f"WIFI:T:ADB;S:{ip}:{port};P:{pairing_code};;"
    else:
        qr_data = f"adb://{ip}:{port}"

    print(f"\nQR Data: {qr_data}\nGenerating QR code...")
    img = qrcode.make(qr_data)
    output_file = f"adb_pair_qr_{ip.replace('.', '_')}_{port}.png"
    img.save(output_file)
    print(f"QR code saved as {output_file}\nScan this QR code with your Android device (Developer Options > Wireless debugging > Pair device with QR code).\n")

if __name__ == "__main__":
    main()
