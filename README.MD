# Screen Time Tracker for Windows

[![Alpha](https://img.shields.io/badge/status-alpha-orange)](https://github.com/KaiAlan/screen-time-tracker-cli-tool)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)

A lightweight Windows utility to track application usage time and generate productivity reports. 

**Warning**: This is early alpha software - expect potential bugs and missing features!

## Features

- 🕵️ Real-time application usage tracking
- 📊 Live CLI dashboard (htop-style interface)
- 📅 Daily/weekly usage reports
- 💾 SQLite database for persistent storage
- 🖥️ Windows foreground window detection

## Requirements

- Windows 10/11
- Python 3.8+

## Installation

### For Users Without Python

1. Download Python:
   - [Python 3.12 for Windows](https://www.python.org/downloads/windows/)
   - During installation, check "Add python.exe to PATH"

2. Verify Python installation:
   ```bash
   python --version
   ```

### Install Dependencies

```bash
pip install -r requirements.txt
```

Required packages:
- `psutil` (Process monitoring)
- `pywin32` (Windows API access)

## Usage

### Start Tracking
```bash
pythonw tracker.py
```

This will run the tracker in the background with no visible window.

### View Data

#### Live Dashboard
```bash
python cli.py live
```
![Live Dashboard Example](https://postimg.cc/67jLCWsF)

#### Generate Weekly Report
```bash
python cli.py report
```

#### Generate Custom Report (e.g., 30 days)
```bash
python cli.py report --days 30
```

### Stop Tracking
1. Open Task Manager (`Ctrl + Shift + Esc`)
2. Find and kill `pythonw.exe` process

## Building from Source

```bash
git clone https://github.com/KaiAlan/screen-time-tracker-cli-tool.git
cd screen-time-tracker-cli-tool
pip install -r requirements.txt
```

## File Structure
```
screen-time-tracker-cli-tool/
├── tracker.py       # Background tracking daemon
├── cli.py           # CLI interface
├── screen_time.db   # Database (auto-generated)
├── requirements.txt # Dependencies
└── README.MD
```

## Known Issues
- May not detect some UWP apps (Windows Store apps)
- First run might show "file is not a database" error - just restart tracker
- High CPU usage when switching apps rapidly

## Contributing
This project is in early development. Please report issues and suggestions!