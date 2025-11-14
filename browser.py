import subprocess
import sys
import os

# Check if running in headless environment
if not os.environ.get('DISPLAY') and not os.environ.get('WAYLAND_DISPLAY'):
    # Headless: use CLI version
    print("🌐 Simple Web Browser (CLI Mode)\n")
    
    import requests
    
    while True:
        url = input("Enter URL (or 'quit'): ").strip()
        
        if url.lower() == 'quit':
            break
        
        if not url:
            continue
        
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url
        
        try:
            response = requests.get(url, timeout=5)
            print(f"✓ Status: {response.status_code}")
            print(f"  Title: {response.headers.get('Content-Type', 'Unknown')}\n")
        except Exception as e:
            print(f"✗ Error: {e}\n")
else:
    # GUI mode
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
            self.url_bar.setText("https://google.com")
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
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            self.browser.setUrl(QUrl(url))
            self.url_bar.setText(url)

    if __name__ == "__main__":
        app = QApplication(sys.argv)
        browser = SimpleBrowser()
        browser.show()
        sys.exit(app.exec())
