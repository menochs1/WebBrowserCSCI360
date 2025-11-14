# Simple Web Browser

A simple Python web browser that works on both desktop and headless environments.

## Quick Start

### 1. Install Dependencies

```bash
python install.py
```

### 2. Run the Browser

```bash
python browser.py
```

## How It Works

The browser automatically detects your environment:

- **On a desktop** (Linux, macOS, Windows with display): Opens a **graphical browser window** with an address bar
- **In a headless terminal** (like a dev container): Opens a **CLI browser** in the terminal

## GUI Mode (Desktop)

When you have a display server:

1. A window opens with a simple interface
2. Type a URL in the address bar (e.g., `google.com`)
3. Press Enter or click "Go"
4. The page loads and displays

**Features:**
- Simple address bar
- Automatic `https://` detection
- Full page rendering

## CLI Mode (Terminal/Headless)

When there's no display:

```
🌐 Simple Web Browser (CLI Mode)

Enter URL (or 'quit'): google.com
✓ Status: 200
  Title: text/html; charset=UTF-8

Enter URL (or 'quit'): github.com
✓ Status: 200
  Title: text/html; charset=UTF-8

Enter URL (or 'quit'): quit
```

**Features:**
- Type URLs in the terminal
- Shows HTTP status and content type
- Automatic `https://` detection

## Files

- `browser.py` - Main browser (auto-detects GUI or CLI mode)
- `install.py` - Dependency installer
- `requirements.txt` - Required packages

## Dependencies

Automatically installed by `install.py`:

- **PyQt6** - GUI framework (for graphical mode)
- **PyQt6-WebEngine** - Browser engine (for graphical mode)
- **requests** - HTTP library (for CLI mode)

## Usage

### Installation and Run (One Command)

```bash
python install.py && python browser.py
```

### Just Run (if already installed)

```bash
python browser.py
```

## Troubleshooting

**Display errors (libGL.so.1)?**
- You're in a headless environment - the CLI mode will work automatically

**Import errors?**
- Run `python install.py` first to install dependencies

**Connection errors?**
- Check your internet connection with `ping google.com`