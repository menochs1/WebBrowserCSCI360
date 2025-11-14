"""Simple browser: use PyQt GUI when available, otherwise open system browser.

The GUI requires PyQt6 and PyQt6-WebEngine plus system graphics support.
If those are missing or a runtime graphics error occurs, this script will
open the default system browser to a default URL and print instructions.
"""

import sys
import webbrowser

DEFAULT_URL = "https://google.com"

try:
    # Try to import PyQt GUI components
    from PyQt6.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLineEdit, QPushButton
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtCore import QUrl

    class SimpleBrowser(QMainWindow):
        def __init__(self):
            super().__init__()
            self.setWindowTitle("Simple Web Browser")
            self.setGeometry(100, 100, 1000, 700)

            # Create central widget
            central = QWidget()
            layout = QVBoxLayout()

            # URL bar
            bar_layout = QHBoxLayout()
            self.url_bar = QLineEdit()
            self.url_bar.setText(DEFAULT_URL)
            self.url_bar.returnPressed.connect(self.navigate)
            bar_layout.addWidget(self.url_bar)

            go_btn = QPushButton("Go")
            go_btn.clicked.connect(self.navigate)
            bar_layout.addWidget(go_btn)

            layout.addLayout(bar_layout)

            # Web view
            self.browser = QWebEngineView()
            layout.addWidget(self.browser)

            central.setLayout(layout)
            self.setCentralWidget(central)

            # Load home page
            self.navigate()

        def navigate(self):
            url = self.url_bar.text()
            if not url.startswith(("http://", "https://")):
                url = "https://" + url
            self.browser.setUrl(QUrl(url))
            self.url_bar.setText(url)

    def run_gui():
        app = QApplication(sys.argv)
        browser = SimpleBrowser()
        browser.show()
        sys.exit(app.exec())

except Exception as e_import:
    # Import failed (missing PyQt or other import-time error)
    run_gui = None
    import_error = e_import


def fallback_open_system_browser(reason_message: str):
    """Open the default system browser and print helpful instructions."""
    print("⚠ GUI unavailable:", reason_message)
    print("Opening default system browser to:", DEFAULT_URL)
    try:
        webbrowser.open(DEFAULT_URL)
    except Exception:
        print("Could not open system browser automatically.")
    print("\nIf you want the GUI version, install dependencies:")
    print("  python -m pip install -r requirements.txt")
    print("On Windows you may also need the Microsoft Visual C++ Redistributable.")


if __name__ == "__main__":
    # If GUI run function is available, try to run it; otherwise fallback.
    if run_gui is not None:
        try:
            run_gui()
        except Exception as e_runtime:
            # Could be a graphics/runtime error (e.g., libGL on Linux, or other)
            fallback_open_system_browser(str(e_runtime))
    else:
        fallback_open_system_browser(str(import_error))
