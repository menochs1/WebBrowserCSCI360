import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView


class TinyBrowser(QWidget):
    def __init__(self, start_url: str = "https://example.org"):
        super().__init__()
        self.setWindowTitle("Tiny Browser")
        self.resize(900, 600)

        self.view = QWebEngineView()
        self.addr = QLineEdit(start_url)
        self.addr.setPlaceholderText("Enter URL and press Enter…")
        self.addr.returnPressed.connect(self.load_url)
        self.view.urlChanged.connect(self.sync_url)

        layout = QVBoxLayout(self)
        layout.addWidget(self.addr)
        layout.addWidget(self.view)

        self.load_url()

    def load_url(self):
        url = (self.addr.text() or "").strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.view.setUrl(QUrl(url or "https://example.org"))

    def sync_url(self, url: QUrl):
        self.addr.setText(url.toString())


def main():
    app = QApplication(sys.argv)
    w = TinyBrowser()
    w.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
import sys
from PyQt6.QtCore import QUrl
from PyQt6.QtWidgets import QApplication, QWidget, QLineEdit, QVBoxLayout
from PyQt6.QtWebEngineWidgets import QWebEngineView

class TinyBrowser(QWidget):
    def __init__(self, start_url="https://example.org"):
        super().__init__()
        self.setWindowTitle("Tiny Browser")
        self.resize(900, 600)

        self.view = QWebEngineView()
        self.addr = QLineEdit(start_url)
        self.addr.returnPressed.connect(self.load_url)
        self.view.urlChanged.connect(self.sync_url)

        layout = QVBoxLayout(self)
        layout.addWidget(self.addr)
        layout.addWidget(self.view)

        self.load_url()

    def load_url(self):
        url = self.addr.text().strip()
        if url and not url.startswith(("http://", "https://")):
            url = "https://" + url
        self.view.setUrl(QUrl(url or "https://example.org"))

    def sync_url(self, url: QUrl):
        self.addr.setText(url.toString())

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = TinyBrowser()
    w.show()
    sys.exit(app.exec())