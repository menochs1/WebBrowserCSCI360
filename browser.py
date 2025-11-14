import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QLineEdit, QToolBar, QAction
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


class SimpleBrowser(QMainWindow):
    """Minimal single-window web browser using PyQt6.

    Requirements:
      - PyQt6
      - PyQt6-WebEngine
    """

    def __init__(self, homepage: str = "https://www.google.com"):
        super().__init__()
        self.setWindowTitle("Simple Web Browser")
        self.setGeometry(80, 80, 1200, 800)

        # Web view
        self.view = QWebEngineView()
        self.setCentralWidget(self.view)

        # Toolbar
        toolbar = QToolBar()
        self.addToolBar(toolbar)

        back_action = QAction("Back", self)
        back_action.triggered.connect(self.view.back)
        toolbar.addAction(back_action)

        forward_action = QAction("Forward", self)
        forward_action.triggered.connect(self.view.forward)
        toolbar.addAction(forward_action)

        reload_action = QAction("Reload", self)
        reload_action.triggered.connect(self.view.reload)
        toolbar.addAction(reload_action)

        home_action = QAction("Home", self)
        home_action.triggered.connect(lambda: self.navigate_to(homepage))
        toolbar.addAction(home_action)

        # Address bar
        self.address = QLineEdit()
        self.address.returnPressed.connect(self.on_enter_address)
        toolbar.addWidget(self.address)

        # Go button
        go_action = QAction("Go", self)
        go_action.triggered.connect(self.on_enter_address)
        toolbar.addAction(go_action)

        # Update address when page changes
        self.view.urlChanged.connect(self.update_address)

        # Load homepage
        self.navigate_to(homepage)

    def on_enter_address(self):
        url_text = self.address.text().strip()
        if not url_text:
            return
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
    win = SimpleBrowser()
    win.show()
    sys.exit(app.exec())
