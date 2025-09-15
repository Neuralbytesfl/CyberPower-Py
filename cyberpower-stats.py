import hid
import re
import time
import csv
from pathlib import Path

VENDOR_ID = 0x0764
PRODUCT_ID = 0x0601
CSV_FILE = Path("ups_log.csv")

# Keep last valid readings
last_status = {}

def decode_report(data: list[int]) -> str:
    return ''.join(chr(b) if 32 <= b <= 126 else '' for b in data)

def parse_status(text: str) -> dict:
    status = {}
    if m := re.search(r'I(\d+\.\d+)', text):
        status['Input_V'] = float(m.group(1))
    if m := re.search(r'O(\d+\.\d+)', text):
        status['Output_V'] = float(m.group(1))
    if m := re.search(r'L(\d+)', text):
        status['Load_%'] = int(m.group(1))
    if m := re.search(r'B(\d+)', text):
        status['Battery_%'] = int(m.group(1))
    if m := re.search(r'R(\d+)', text):
        status['Runtime_min'] = int(m.group(1))
    if m := re.search(r'V(\d+\.\d+)', text):
        status['Battery_V'] = float(m.group(1))
    if m := re.search(r'F(\d+\.\d+)', text):
        status['Frequency_Hz'] = float(m.group(1))
    return status

def log_to_csv(status):
    """Append UPS status to CSV with timestamp."""
    new_file = not CSV_FILE.exists()
    with CSV_FILE.open("a", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["Time"] + list(status.keys()))
        if new_file:
            writer.writeheader()
        row = {"Time": time.strftime("%Y-%m-%d %H:%M:%S"), **status}
        writer.writerow(row)

def main():
    global last_status

    h = hid.device()
    h.open(VENDOR_ID, PRODUCT_ID)

    print("Connected to:", h.get_manufacturer_string(), h.get_product_string())
    print("Press Ctrl+C to stop.\n")

    while True:
        data = h.read(64)
        if not data:
            continue
        text = decode_report(data)
        status = parse_status(text)

        # Update last values
        last_status.update(status)

        # Print nicely
        print(
            f"[{time.strftime('%H:%M:%S')}] "
            f"In {last_status.get('Input_V')}V | "
            f"Out {last_status.get('Output_V')}V | "
            f"Load {last_status.get('Load_%')}% | "
            f"Battery {last_status.get('Battery_%')}% "
            f"({last_status.get('Runtime_min')} min) | "
            f"BattV {last_status.get('Battery_V')}V | "
            f"Freq {last_status.get('Frequency_Hz')}Hz"
        )

        # Optional logging
        log_to_csv(last_status)

if __name__ == "__main__":
    main()
