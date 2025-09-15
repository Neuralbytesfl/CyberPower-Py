# UPS Monitor (CyberPower HID)

A simple Python script to monitor a CyberPower UPS over USB using hidapi.

## Requirements
- Python 3.8 or newer
- hidapi library

Install with:
pip install hidapi

## Usage
Run the script:
python battery.py

Example output:
[16:25:01] In 114.8V | Out 114.8V | Load 28% | Battery 100% (24 min) | BattV 27.5V | Freq 60.0Hz
[16:25:02] In 114.9V | Out 114.9V | Load 30% | Battery 100% (23 min) | BattV 27.5V | Freq 60.0Hz

## Features
- Input and Output voltage
- Load percentage
- Battery charge percentage
- Runtime left in minutes
- Battery voltage
- Line frequency
- Logs to ups_log.csv

## License
MIT
