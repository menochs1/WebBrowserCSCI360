Tiny Browser (Python + PyQt6)
================================

What is this?
- A single-file, minimal web browser using PyQt6 + WebEngine.
- File: `browser.py`

Quick Start (any OS)
- Install Python 3.10+ from python.org (or system packages).
- Open a terminal in this folder and run:

```
python -m venv .venv
".venv/bin/pip" install -U pip
".venv/bin/pip" install -r requirements.txt
".venv/bin/python" browser.py
```

On Windows (PowerShell):
```
python -m venv .venv
.\.venv\Scripts\pip install -U pip
.\.venv\Scripts\pip install -r requirements.txt
.\.venv\Scripts\python browser.py
```

Download as ZIP and Run
1) Download the repo ZIP, extract anywhere.
2) Run `run.sh` (Linux/macOS) or `run.bat` (Windows). These will create a venv, install dependencies, and launch the app.

Run Scripts
- Linux/macOS: `./run.sh`
- Windows: double-click `run.bat` or run it in Command Prompt.

Notes for Linux
- If you see missing library errors when launching (Qt/X11), install:
```
sudo apt update
sudo apt install -y libnss3 libxkbcommon-x11-0 libxcb-cursor0
```

Headless/Containers
- This is a GUI app. In a headless dev container or SSH session without X/Wayland display, it will not show a window. Use a local desktop or enable X forwarding.

Troubleshooting
- Blank window or crashes: update GPU drivers or run with software rendering: `QTWEBENGINE_DISABLE_GPU=1 .venv/bin/python browser.py`.
- If Python opens the script in an editor on double-click, run it from a terminal or use the provided scripts.

