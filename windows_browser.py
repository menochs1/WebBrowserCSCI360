#!/usr/bin/env python3
"""
windows_browser.py

A self-contained web browser for Windows that:
1. Automatically installs PyQt6 + PyQt6-WebEngine into a local venv
2. Creates a minimal GUI browser window
3. Works without requiring manual pip commands

Just run: python windows_browser.py

Or pass a URL: python windows_browser.py https://example.com
"""

import sys
import os
import subprocess
import shutil
import argparse
from pathlib import Path

# Configuration
SCRIPT_DIR = Path(__file__).parent
VENV_DIR = SCRIPT_DIR / ".venv_browser"
REQUIREMENTS = ["PyQt6==6.7.0", "PyQt6-WebEngine==6.7.0"]
DEFAULT_URL = "https://www.google.com"


def get_venv_python() -> Path:
    """Get the path to the venv's Python executable (Windows-specific)."""
    return VENV_DIR / "Scripts" / "python.exe"


def create_and_setup_venv():
    """Create venv and install requirements."""
    if VENV_DIR.exists():
        print(f"✓ Using existing venv at: {VENV_DIR}")
        return
    
    print(f"Creating venv at: {VENV_DIR}")
    subprocess.check_call([sys.executable, "-m", "venv", str(VENV_DIR)])
    
    venv_python = get_venv_python()
    print("Upgrading pip...")
    subprocess.check_call([str(venv_python), "-m", "pip", "install", "--upgrade", "pip", "-q"])
    
    print(f"Installing {len(REQUIREMENTS)} packages...")
    for req in REQUIREMENTS:
        print(f"  • {req}")
        subprocess.check_call([str(venv_python), "-m", "pip", "install", req, "-q"])
    
    print("✓ Setup complete!")


def run_browser(url: str):
    """Run the PyQt6 GUI browser in the venv."""
    venv_python = get_venv_python()
    
    browser_code = f'''
import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class SimpleBrowser(QMainWindow):
    def __init__(self, homepage: str = "{url}"):
        super().__init__()
        self.setWindowTitle("Web Browser")
        self.setGeometry(100, 100, 1200, 800)
        
        # Web view
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)
        
        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)
        
        back_action = QAction("← Back", self)
        back_action.triggered.connect(self.view.back)
        toolbar.addAction(back_action)
        
        forward_action = QAction("Forward →", self)
        forward_action.triggered.connect(self.view.forward)
        toolbar.addAction(forward_action)
        
        reload_action = QAction("↻ Reload", self)
        reload_action.triggered.connect(self.view.reload)
        toolbar.addAction(reload_action)
        
        home_action = QAction("⌂ Home", self)
        home_action.triggered.connect(lambda: self.navigate_to(homepage))
        toolbar.addAction(home_action)
        
        # Address bar
        self.address = QLineEdit()
        self.address.setText(homepage)
        self.address.returnPressed.connect(self.on_address_enter)
        toolbar.addWidget(self.address)
        
        go_action = QAction("Go", self)
        go_action.triggered.connect(self.on_address_enter)
        toolbar.addAction(go_action)
        
        # Sync address when URL changes
        self.view.urlChanged.connect(self.update_address)
        
        # Load homepage
        self.navigate_to(homepage)
    
    def on_address_enter(self):
        url_text = self.address.text().strip()
        if url_text:
            if not url_text.startswith(("http://", "https://")):
                url_text = "https://" + url_text
            self.navigate_to(url_text)
    
    def navigate_to(self, url: str):
        qurl = QUrl(url)
        if not qurl.isValid():
            qurl = QUrl("https://" + url)
        self.view.setUrl(qurl)
    
    def update_address(self, qurl: QUrl):
        self.address.setText(qurl.toString())


if __name__ == "__main__":
    app = QApplication(sys.argv)
    browser = SimpleBrowser()
    browser.show()
    sys.exit(app.exec())
'''
    
    print(f"\n🌐 Launching browser → {url}\n")
    subprocess.run([str(venv_python), "-c", browser_code])


def cleanup_old_venv():
    """Remove old .venv directory if it exists (for migration)."""
    old_venv = SCRIPT_DIR / ".venv"
    if old_venv.exists() and old_venv != VENV_DIR:
        print("Cleaning up old venv...")
        shutil.rmtree(old_venv, ignore_errors=True)


def main():
    parser = argparse.ArgumentParser(
        description="Simple web browser for Windows",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python windows_browser.py                 # Opens Google
  python windows_browser.py https://github.com
  python windows_browser.py python.org
        """
    )
    parser.add_argument(
        "url",
        nargs="?",
        default=DEFAULT_URL,
        help=f"URL to open (default: {DEFAULT_URL})"
    )
    parser.add_argument(
        "--recreate",
        action="store_true",
        help="Delete and recreate the venv"
    )
    args = parser.parse_args()
    
    try:
        # Cleanup if requested
        if args.recreate and VENV_DIR.exists():
            print("Removing old venv...")
            shutil.rmtree(VENV_DIR)
        
        cleanup_old_venv()
        
        # Setup venv and install packages
        print("=" * 60)
        print("Windows Web Browser Launcher")
        print("=" * 60)
        create_and_setup_venv()
        
        # Run the browser
        run_browser(args.url)
        
    except KeyboardInterrupt:
        print("\n\nBrowser closed.")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("  1. Make sure you're using Python 3.8 or later")
        print("  2. Use 64-bit Python (not 32-bit)")
        print("  3. On Windows, you may need Microsoft Visual C++ Redistributable:")
        print("     https://support.microsoft.com/en-us/help/2977003/")
        sys.exit(1)


if __name__ == "__main__":
    main()
